# Shopify Agent Features

This directory contains the implementation for Shopify's new Agent features, enabling AI-powered commerce experiences.

## 🚀 Features

### ✅ Shopify Catalog MCP Integration
- **Search Catalog**: Search across hundreds of millions of products
- **Universal Product Identifiers**: Clustered results to avoid duplicates
- **Rich Metadata**: Product options, variants, pricing, availability
- **Web Components**: Interactive product cards and displays

### ✅ Universal Cart Management
- **Cross-Merchant Cart**: Add products from any store to a single cart
- **Automatic Grouping**: Items organized by merchant
- **Buyer Identity**: Persistent buyer information across sessions
- **Real-time Updates**: Live cart synchronization

### ✅ Checkout Kit Integration
- **Branded Checkout**: Native checkout experience with your branding
- **Compliance Ready**: GDPR, CCPA, PCI DSS v4, WCAG compliant
- **Payment Security**: Shopify handles all payment processing
- **Mobile & Web**: Works across all platforms

### ✅ Web Components
- **Rich Product Display**: Interactive product cards
- **Customizable Styling**: CSS-based theming
- **Responsive Design**: Mobile-first approach
- **Agent Branding**: Custom colors and typography

## 🔧 Setup

### 1. Early Access Application
**IMPORTANT**: This feature requires early access approval from Shopify.

1. Apply for early access at: [Shopify Agent Commerce Early Access](https://shopify.dev/docs/api/agentic-commerce)
2. Once approved, you'll receive a `SHOPIFY_CATALOG_API_TOKEN`

### 2. Environment Configuration
```bash
# Required for Agent features (from Shopify early access)
export SHOPIFY_CATALOG_API_TOKEN="your_catalog_api_token"

# Optional: Your existing Shopify store (for local products)
export SHOPIFY_STORE_URL="https://your-store.myshopify.com"
export SHOPIFY_ACCESS_TOKEN="your_store_access_token"
```

### 3. Install Dependencies
```bash
cd /workspaces/automations_hub/shopify
npm install fastapi uvicorn httpx pydantic
```

### 4. Start the Agent API Server
```bash
python agent/api_server.py
```

The server will be available at `http://localhost:8000`

## 📋 API Endpoints

### Catalog Search
```bash
POST /api/search-catalog
{
  "query": "lightweight running shoes",
  "ships_to": "US",
  "limit": 5,
  "context": "buyer prefers light and bright colors"
}
```

### Universal Cart
```bash
POST /api/update-cart
{
  "add_items": [
    {
      "product_variant_id": "gid://shopify/ProductVariant/123",
      "quantity": 1
    }
  ],
  "buyer_identity": {
    "email": "customer@example.com"
  }
}
```

### Checkout
```bash
POST /api/checkout
{
  "checkout_url": "https://shop.myshopify.com/cart/c/abc123?key=xyz",
  "branding_colors": {
    "primary": "#007bff",
    "accent": "#28a745"
  }
}
```

## 🌐 Web Interface

Access the demo interface at: `http://localhost:8000/demo`

Features:
- Product search and display
- Interactive product options
- Add to cart functionality
- Universal cart management
- Checkout integration

## 🔌 MCP Integration

The agent features are integrated into your existing MCP server structure:

```python
# Add to your MCP server
from shopify.agent.catalog_mcp import search_catalog, update_cart
from shopify.agent.checkout_kit import create_checkout_page

# Register as MCP tools
@app.tool("search_catalog")
async def tool_search_catalog(query: str, ships_to: str = "US"):
    return await search_catalog(query=query, ships_to=ships_to)

@app.tool("update_cart") 
async def tool_update_cart(add_items: list):
    return await update_cart(add_items=add_items)
```

## 🎨 Customization

### Branding Colors
```python
branding_colors = {
    "primary": "#your-primary-color",
    "secondary": "#your-secondary-color", 
    "accent": "#your-accent-color",
    "background": "#your-background-color",
    "text": "#your-text-color"
}
```

### Custom CSS
```css
shopify-product-card::part(product-title) {
    font-weight: 600;
    color: #2c3e50;
}

shopify-checkout::part(button-primary) {
    background-color: #28a745;
    border-radius: 6px;
}
```

## 🔒 Security & Compliance

✅ **Automatically Handled:**
- PCI DSS v4 compliance
- GDPR compliance
- CCPA compliance
- WCAG accessibility
- Payment processing security
- Marketplace compliance requirements

## 📊 Status Check

Check your setup status:
```bash
GET /api/status
```

Returns:
- Environment configuration status
- Integration readiness
- Required next steps

## 🚀 Next Steps

1. **Apply for Early Access**: Get your `SHOPIFY_CATALOG_API_TOKEN`
2. **Test Integration**: Use the demo interface to test functionality
3. **Customize Branding**: Apply your brand colors and styling
4. **Deploy**: Integrate into your production AI agent

## 📚 Resources

- [Shopify Agent Commerce Documentation](https://shopify.dev/docs/api/agentic-commerce)
- [MCP UI Documentation](https://shopify.dev/docs/api/mcp-ui)
- [Web Components Guide](https://shopify.dev/docs/storefront-api/web-components)
- [Checkout Kit Documentation](https://shopify.dev/docs/api/checkout-kit)

## ⚠️ Important Notes

- **Early Access Required**: Features require Shopify approval
- **Bearer Token Security**: Keep your API token private and secure
- **Rate Limits**: Respect Shopify's API rate limits
- **Terms of Service**: Usage subject to Shopify API License and Terms
