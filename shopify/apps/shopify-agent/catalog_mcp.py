"""Shopify Catalog MCP server integration for agent features."""

import os
import httpx
from typing import Annotated, Any, Optional, List, Dict
from pydantic import BaseModel, Field


class CatalogSearchResponse(BaseModel):
    """Response model for catalog search operations."""
    success: bool
    data: Optional[Dict[str, Any]] = None
    message: str
    products: Optional[List[Dict[str, Any]]] = None
    ui_resources: Optional[List[Dict[str, Any]]] = None


class UniversalCartResponse(BaseModel):
    """Response model for Universal Cart operations."""
    success: bool
    data: Optional[Dict[str, Any]] = None
    message: str
    cart_id: Optional[str] = None
    checkout_url: Optional[str] = None
    ui_resources: Optional[List[Dict[str, Any]]] = None


async def search_catalog(
    query: Annotated[str, Field(description="Search query for products")],
    ships_to: Annotated[str, Field(description="ISO 3166 country code")] = "US",
    limit: Annotated[int, Field(description="Maximum number of results (1-10)", ge=1, le=10)] = 5,
    min_price: Annotated[Optional[float], Field(description="Minimum price filter")] = None,
    max_price: Annotated[Optional[float], Field(description="Maximum price filter")] = None,
    categories: Annotated[Optional[str], Field(description="Comma-delimited taxonomy categories")] = None,
    ships_from: Annotated[Optional[str], Field(description="ISO 3166 country code")] = None,
    available_for_sale: Annotated[int, Field(description="Filter for availability (0 or 1)")] = 1,
    context: Annotated[Optional[str], Field(description="Additional context for search")] = None
) -> CatalogSearchResponse:
    """Search the Shopify Catalog for products across merchants."""
    
    api_token = os.getenv("SHOPIFY_CATALOG_API_TOKEN")
    
    if not api_token:
        return CatalogSearchResponse(
            success=False,
            message="Missing SHOPIFY_CATALOG_API_TOKEN environment variable. Contact Shopify for early access approval."
        )
    
    url = "https://catalog.shopify.com/api/mcp"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token}"
    }
    
    # Build search arguments
    search_args = {
        "query": query,
        "ships_to": ships_to,
        "limit": limit,
        "available_for_sale": available_for_sale
    }
    
    if min_price is not None:
        search_args["min_price"] = min_price
    if max_price is not None:
        search_args["max_price"] = max_price
    if categories:
        search_args["categories"] = categories
    if ships_from:
        search_args["ships_from"] = ships_from
    if context:
        search_args["context"] = context
    
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "id": 2,
        "params": {
            "name": "search_catalog",
            "arguments": search_args
        }
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            data = response.json()
            
            # Parse MCP response
            if "result" in data and "content" in data["result"]:
                content = data["result"]["content"]
                
                # Extract search results and UI resources
                search_results = None
                ui_resources = []
                
                for item in content:
                    if item.get("type") == "text":
                        # Parse JSON search results
                        import json
                        try:
                            search_results = json.loads(item["text"])
                        except json.JSONDecodeError:
                            search_results = item["text"]
                    elif item.get("type") == "resource":
                        ui_resources.append(item["resource"])
                
                return CatalogSearchResponse(
                    success=True,
                    data=search_results,
                    products=search_results if isinstance(search_results, list) else None,
                    ui_resources=ui_resources,
                    message=f"Found products for query: {query}"
                )
            else:
                return CatalogSearchResponse(
                    success=False,
                    message=f"Unexpected response format: {data}"
                )
            
    except httpx.HTTPStatusError as e:
        return CatalogSearchResponse(
            success=False,
            message=f"HTTP error {e.response.status_code}: {e.response.text}"
        )
    except Exception as e:
        return CatalogSearchResponse(
            success=False,
            message=f"Error searching catalog: {str(e)}"
        )


async def update_cart(
    cart_id: Annotated[Optional[str], Field(description="Existing cart ID, creates new if not provided")] = None,
    add_items: Annotated[List[Dict[str, Any]], Field(description="Items to add to cart")] = [],
    buyer_identity: Annotated[Optional[Dict[str, str]], Field(description="Buyer information")] = None,
    delivery_addresses_to_add: Annotated[Optional[List[Dict[str, Any]]], Field(description="Delivery addresses")] = None
) -> UniversalCartResponse:
    """Create or update a Universal Cart with products from any store."""
    
    api_token = os.getenv("SHOPIFY_CATALOG_API_TOKEN")
    
    if not api_token:
        return UniversalCartResponse(
            success=False,
            message="Missing SHOPIFY_CATALOG_API_TOKEN environment variable. Contact Shopify for early access approval."
        )
    
    url = "https://catalog.shopify.com/api/mcp"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token}"
    }
    
    # Build cart update arguments
    cart_args = {}
    
    if cart_id:
        cart_args["cart_id"] = cart_id
    if add_items:
        cart_args["add_items"] = add_items
    if buyer_identity:
        cart_args["buyer_identity"] = buyer_identity
    if delivery_addresses_to_add:
        cart_args["delivery_addresses_to_add"] = delivery_addresses_to_add
    
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "id": 3,
        "params": {
            "name": "update_cart",
            "arguments": cart_args
        }
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            data = response.json()
            
            # Parse MCP response
            if "result" in data and "content" in data["result"]:
                content = data["result"]["content"]
                
                # Extract cart data and UI resources
                cart_data = None
                ui_resources = []
                
                for item in content:
                    if item.get("type") == "text":
                        # Parse JSON cart results
                        import json
                        try:
                            cart_data = json.loads(item["text"])
                        except json.JSONDecodeError:
                            cart_data = item["text"]
                    elif item.get("type") == "resource":
                        ui_resources.append(item["resource"])
                
                cart_id = None
                checkout_url = None
                
                if isinstance(cart_data, dict):
                    cart_id = cart_data.get("id")
                    # Extract checkout URL from cart groups
                    cart_groups = cart_data.get("cartGroups", [])
                    if cart_groups and len(cart_groups) > 0:
                        carts = cart_groups[0].get("carts", [])
                        if carts and len(carts) > 0:
                            checkout_url = carts[0].get("checkoutUrl")
                
                return UniversalCartResponse(
                    success=True,
                    data=cart_data,
                    cart_id=cart_id,
                    checkout_url=checkout_url,
                    ui_resources=ui_resources,
                    message="Cart updated successfully"
                )
            else:
                return UniversalCartResponse(
                    success=False,
                    message=f"Unexpected response format: {data}"
                )
            
    except httpx.HTTPStatusError as e:
        return UniversalCartResponse(
            success=False,
            message=f"HTTP error {e.response.status_code}: {e.response.text}"
        )
    except Exception as e:
        return UniversalCartResponse(
            success=False,
            message=f"Error updating cart: {str(e)}"
        )


async def list_mcp_tools() -> Dict[str, Any]:
    """List available tools from the Shopify Catalog MCP server."""
    
    api_token = os.getenv("SHOPIFY_CATALOG_API_TOKEN")
    
    if not api_token:
        return {
            "success": False,
            "message": "Missing SHOPIFY_CATALOG_API_TOKEN environment variable. Contact Shopify for early access approval."
        }
    
    url = "https://catalog.shopify.com/api/mcp"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token}"
    }
    
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/list",
        "id": 1
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            data = response.json()
            return {
                "success": True,
                "data": data,
                "message": "Retrieved available MCP tools"
            }
            
    except httpx.HTTPStatusError as e:
        return {
            "success": False,
            "message": f"HTTP error {e.response.status_code}: {e.response.text}"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error listing MCP tools: {str(e)}"
        }
