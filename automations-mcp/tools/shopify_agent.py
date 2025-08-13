"""Integration of Shopify Agent features into the main MCP server."""

import sys
import os

# Add the shopify directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'shopify'))

try:
    from shopify.agent.catalog_mcp import search_catalog, update_cart, list_mcp_tools
    from shopify.agent.checkout_kit import create_checkout_page, validate_checkout_compliance
    
    # Export for Golf MCP server
    __all__ = [
        "shopify_search_catalog",
        "shopify_update_cart", 
        "shopify_list_mcp_tools",
        "shopify_create_checkout",
        "shopify_compliance_check"
    ]
    
    # Wrapper functions for Golf MCP integration
    async def shopify_search_catalog(
        query: str,
        ships_to: str = "US",
        limit: int = 5,
        min_price: float = None,
        max_price: float = None,
        categories: str = None,
        ships_from: str = None,
        available_for_sale: int = 1,
        context: str = None
    ):
        """Search Shopify Catalog for products across merchants."""
        return await search_catalog(
            query=query,
            ships_to=ships_to,
            limit=limit,
            min_price=min_price,
            max_price=max_price,
            categories=categories,
            ships_from=ships_from,
            available_for_sale=available_for_sale,
            context=context
        )

    async def shopify_update_cart(
        cart_id: str = None,
        add_items: list = None,
        buyer_identity: dict = None,
        delivery_addresses_to_add: list = None
    ):
        """Update or create Universal Cart."""
        if add_items is None:
            add_items = []
        
        return await update_cart(
            cart_id=cart_id,
            add_items=add_items,
            buyer_identity=buyer_identity,
            delivery_addresses_to_add=delivery_addresses_to_add
        )

    async def shopify_list_mcp_tools():
        """List available Shopify MCP tools."""
        return await list_mcp_tools()

    async def shopify_create_checkout(
        checkout_url: str,
        custom_css: str = None,
        branding_colors: dict = None,
        embedded_mode: bool = False,
        payment_tokens: dict = None
    ):
        """Create branded checkout page."""
        return await create_checkout_page(
            checkout_url=checkout_url,
            custom_css=custom_css,
            branding_colors=branding_colors,
            embedded_mode=embedded_mode,
            payment_tokens=payment_tokens
        )

    async def shopify_compliance_check():
        """Check Shopify compliance status."""
        return await validate_checkout_compliance()

except ImportError as e:
    print(f"Warning: Shopify Agent features not available: {e}")
    
    # Provide stub functions if imports fail
    async def shopify_search_catalog(*args, **kwargs):
        return {
            "success": False,
            "message": "Shopify Agent features not configured. Install dependencies and set SHOPIFY_CATALOG_API_TOKEN."
        }
    
    async def shopify_update_cart(*args, **kwargs):
        return {
            "success": False,
            "message": "Shopify Agent features not configured. Install dependencies and set SHOPIFY_CATALOG_API_TOKEN."
        }
    
    async def shopify_list_mcp_tools(*args, **kwargs):
        return {
            "success": False,
            "message": "Shopify Agent features not configured. Install dependencies and set SHOPIFY_CATALOG_API_TOKEN."
        }
    
    async def shopify_create_checkout(*args, **kwargs):
        return {
            "success": False,
            "message": "Shopify Agent features not configured. Install dependencies."
        }
    
    async def shopify_compliance_check(*args, **kwargs):
        return {
            "success": False,
            "message": "Shopify Agent features not configured. Install dependencies."
        }
