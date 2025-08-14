"""Express API server for Shopify Agent features integration."""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

# Import your Shopify agent modules
from catalog_mcp import search_catalog, update_cart, list_mcp_tools
from checkout_kit import create_checkout_page, validate_checkout_compliance

app = FastAPI(title="Shopify Agent API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SearchRequest(BaseModel):
    query: str
    ships_to: str = "US"
    limit: int = 5
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    categories: Optional[str] = None
    ships_from: Optional[str] = None
    available_for_sale: int = 1
    context: Optional[str] = None


class CartUpdateRequest(BaseModel):
    cart_id: Optional[str] = None
    add_items: List[Dict[str, Any]] = []
    buyer_identity: Optional[Dict[str, str]] = None
    delivery_addresses_to_add: Optional[List[Dict[str, Any]]] = None


class CheckoutRequest(BaseModel):
    checkout_url: str
    custom_css: Optional[str] = None
    branding_colors: Optional[Dict[str, str]] = None
    embedded_mode: bool = False
    payment_tokens: Optional[Dict[str, str]] = None


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Shopify Agent API",
        "version": "1.0.0",
        "features": [
            "Catalog Search",
            "Universal Cart",
            "Checkout Kit",
            "Web Components"
        ],
        "status": "ready"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": "2025-01-13"}


@app.post("/api/search-catalog")
async def api_search_catalog(request: SearchRequest):
    """Search the Shopify Catalog for products."""
    try:
        result = await search_catalog(
            query=request.query,
            ships_to=request.ships_to,
            limit=request.limit,
            min_price=request.min_price,
            max_price=request.max_price,
            categories=request.categories,
            ships_from=request.ships_from,
            available_for_sale=request.available_for_sale,
            context=request.context
        )
        return result.dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/update-cart")
async def api_update_cart(request: CartUpdateRequest):
    """Update or create a Universal Cart."""
    try:
        result = await update_cart(
            cart_id=request.cart_id,
            add_items=request.add_items,
            buyer_identity=request.buyer_identity,
            delivery_addresses_to_add=request.delivery_addresses_to_add
        )
        return result.dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/checkout")
async def api_create_checkout(request: CheckoutRequest):
    """Create a branded checkout page."""
    try:
        result = await create_checkout_page(
            checkout_url=request.checkout_url,
            custom_css=request.custom_css,
            branding_colors=request.branding_colors,
            embedded_mode=request.embedded_mode,
            payment_tokens=request.payment_tokens
        )
        return result.dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/checkout/{checkout_url:path}", response_class=HTMLResponse)
async def get_checkout_page(checkout_url: str):
    """Get checkout page HTML."""
    try:
        result = await create_checkout_page(checkout_url=checkout_url)
        if result.success:
            return HTMLResponse(content=result.checkout_html)
        else:
            raise HTTPException(status_code=400, detail=result.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/mcp/tools")
async def api_list_mcp_tools():
    """List available MCP tools from Shopify Catalog."""
    try:
        result = await list_mcp_tools()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/compliance")
async def api_compliance_check():
    """Check compliance status."""
    try:
        result = await validate_checkout_compliance()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/demo", response_class=HTMLResponse)
async def demo_interface():
    """Serve the demo interface."""
    try:
        with open("web_components/agent-interface.html", "r") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="""
        <html>
            <body>
                <h1>Demo Interface Not Found</h1>
                <p>Please ensure the agent-interface.html file exists in the web_components directory.</p>
            </body>
        </html>
        """)


@app.get("/api/status")
async def api_status():
    """Get API and integration status."""
    
    # Check environment variables
    has_catalog_token = bool(os.getenv("SHOPIFY_CATALOG_API_TOKEN"))
    has_store_config = bool(os.getenv("SHOPIFY_STORE_URL")) and bool(os.getenv("SHOPIFY_ACCESS_TOKEN"))
    
    return {
        "api_status": "operational",
        "integrations": {
            "catalog_mcp": {
                "status": "ready" if has_catalog_token else "needs_token",
                "description": "Shopify Catalog MCP server integration"
            },
            "store_api": {
                "status": "ready" if has_store_config else "needs_config", 
                "description": "Direct Shopify store API access"
            },
            "checkout_kit": {
                "status": "ready",
                "description": "Shopify Checkout Kit integration"
            },
            "web_components": {
                "status": "ready",
                "description": "Shopify web components for UI"
            }
        },
        "environment": {
            "catalog_token_set": has_catalog_token,
            "store_url_set": bool(os.getenv("SHOPIFY_STORE_URL")),
            "store_token_set": bool(os.getenv("SHOPIFY_ACCESS_TOKEN"))
        },
        "next_steps": [
            "Apply for Shopify Agent early access" if not has_catalog_token else None,
            "Set SHOPIFY_CATALOG_API_TOKEN environment variable" if not has_catalog_token else None,
            "Configure store credentials" if not has_store_config else None
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
