"""Shopify Agent features module."""

from .catalog_mcp import search_catalog, update_cart, list_mcp_tools
from .checkout_kit import create_checkout_page, validate_checkout_compliance
from .api_server import app

__version__ = "1.0.0"
__all__ = [
    "search_catalog",
    "update_cart", 
    "list_mcp_tools",
    "create_checkout_page",
    "validate_checkout_compliance",
    "app"
]
