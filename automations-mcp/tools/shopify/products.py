"""Shopify API tools for product management."""

import os
import httpx
from typing import Annotated, Any, Optional, List, Dict
from pydantic import BaseModel, Field


class ProductResponse(BaseModel):
    """Response model for product operations."""
    success: bool
    data: Optional[Dict[str, Any]] = None
    message: str
    products: Optional[List[Dict[str, Any]]] = None


class CollectionResponse(BaseModel):
    """Response model for collection operations."""
    success: bool
    data: Optional[Dict[str, Any]] = None
    message: str
    collections: Optional[List[Dict[str, Any]]] = None


async def get_shopify_products(
    limit: Annotated[int, Field(description="Number of products to retrieve (max 250)", ge=1, le=250)] = 50,
    status: Annotated[str, Field(description="Product status filter: active, archived, draft")] = "active"
) -> ProductResponse:
    """Get products from Shopify store."""
    
    shopify_url = os.getenv("SHOPIFY_STORE_URL")
    shopify_token = os.getenv("SHOPIFY_ACCESS_TOKEN")
    
    if not shopify_url or not shopify_token:
        return ProductResponse(
            success=False,
            message="Missing SHOPIFY_STORE_URL or SHOPIFY_ACCESS_TOKEN environment variables"
        )
    
    url = f"{shopify_url}/admin/api/2023-10/products.json"
    headers = {
        "X-Shopify-Access-Token": shopify_token,
        "Content-Type": "application/json"
    }
    
    params = {
        "limit": limit,
        "status": status
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            return ProductResponse(
                success=True,
                products=data.get("products", []),
                message=f"Retrieved {len(data.get('products', []))} products"
            )
            
    except httpx.HTTPStatusError as e:
        return ProductResponse(
            success=False,
            message=f"HTTP error {e.response.status_code}: {e.response.text}"
        )
    except Exception as e:
        return ProductResponse(
            success=False,
            message=f"Error fetching products: {str(e)}"
        )


async def get_shopify_collections(
    limit: Annotated[int, Field(description="Number of collections to retrieve (max 250)", ge=1, le=250)] = 50
) -> CollectionResponse:
    """Get collections from Shopify store."""
    
    shopify_url = os.getenv("SHOPIFY_STORE_URL")
    shopify_token = os.getenv("SHOPIFY_ACCESS_TOKEN")
    
    if not shopify_url or not shopify_token:
        return CollectionResponse(
            success=False,
            message="Missing SHOPIFY_STORE_URL or SHOPIFY_ACCESS_TOKEN environment variables"
        )
    
    url = f"{shopify_url}/admin/api/2023-10/smart_collections.json"
    headers = {
        "X-Shopify-Access-Token": shopify_token,
        "Content-Type": "application/json"
    }
    
    params = {"limit": limit}
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            return CollectionResponse(
                success=True,
                collections=data.get("smart_collections", []),
                message=f"Retrieved {len(data.get('smart_collections', []))} collections"
            )
            
    except httpx.HTTPStatusError as e:
        return CollectionResponse(
            success=False,
            message=f"HTTP error {e.response.status_code}: {e.response.text}"
        )
    except Exception as e:
        return CollectionResponse(
            success=False,
            message=f"Error fetching collections: {str(e)}"
        )


async def create_shopify_product(
    title: Annotated[str, Field(description="Product title")],
    description: Annotated[str, Field(description="Product description")] = "",
    product_type: Annotated[str, Field(description="Product type")] = "",
    vendor: Annotated[str, Field(description="Product vendor")] = "",
    status: Annotated[str, Field(description="Product status: active, archived, draft")] = "draft"
) -> ProductResponse:
    """Create a new product in Shopify store."""
    
    shopify_url = os.getenv("SHOPIFY_STORE_URL")
    shopify_token = os.getenv("SHOPIFY_ACCESS_TOKEN")
    
    if not shopify_url or not shopify_token:
        return ProductResponse(
            success=False,
            message="Missing SHOPIFY_STORE_URL or SHOPIFY_ACCESS_TOKEN environment variables"
        )
    
    url = f"{shopify_url}/admin/api/2023-10/products.json"
    headers = {
        "X-Shopify-Access-Token": shopify_token,
        "Content-Type": "application/json"
    }
    
    product_data = {
        "product": {
            "title": title,
            "body_html": description,
            "product_type": product_type,
            "vendor": vendor,
            "status": status
        }
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, headers=headers, json=product_data)
            response.raise_for_status()
            
            data = response.json()
            return ProductResponse(
                success=True,
                data=data.get("product", {}),
                message=f"Created product: {title}"
            )
            
    except httpx.HTTPStatusError as e:
        return ProductResponse(
            success=False,
            message=f"HTTP error {e.response.status_code}: {e.response.text}"
        )
    except Exception as e:
        return ProductResponse(
            success=False,
            message=f"Error creating product: {str(e)}"
        )
