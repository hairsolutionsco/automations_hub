#!/bin/bash
"""
Load Shopify Store Configuration
This script loads the store-specific configuration for one-head-hair.myshopify.com
"""

# Load store configuration
if [ -f "/workspaces/automations_hub/shopify/.env.store" ]; then
    source /workspaces/automations_hub/shopify/.env.store
    export SHOPIFY_STORE_URL
    echo "✅ Loaded store configuration for: $STORE_NAME"
    echo "🏪 Store URL: $SHOPIFY_STORE_URL"
else
    # Fallback to direct export
    export SHOPIFY_STORE_URL="one-head-hair.myshopify.com"
    echo "✅ Set store URL to: $SHOPIFY_STORE_URL"
fi

# The access token is already set as SHOPIFY_ADMIN_API_ACCESS_TOKEN
if [ -n "$SHOPIFY_ADMIN_API_ACCESS_TOKEN" ]; then
    echo "🔑 Access token: ✅ Available"
else
    echo "⚠️  Access token: ❌ Not set"
fi

echo "🚀 Ready for Shopify operations!"
