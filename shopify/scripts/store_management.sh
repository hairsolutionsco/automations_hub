#!/bin/bash

# Shopify Store Management Script

echo "🛍️ Shopify Store Management"
echo "=========================="

# Load environment variables
if [ -f ../.env ]; then
    source ../.env
fi

# Check credentials
if [ -z "$SHOPIFY_STORE_URL" ] || [ -z "$SHOPIFY_ACCESS_TOKEN" ]; then
    echo "❌ Error: Shopify store credentials not set"
    echo "Please set SHOPIFY_STORE_URL and SHOPIFY_ACCESS_TOKEN"
    exit 1
fi

echo "🏪 Store: $SHOPIFY_STORE_URL"
echo ""

# Menu options
echo "What would you like to do?"
echo "1. List Products"
echo "2. List Collections"
echo "3. List Orders"
echo "4. Store Info"
echo "5. Create Test Product"
echo "6. Backup Store Data"

read -p "Enter your choice (1-6): " choice

case $choice in
    1)
        echo "📦 Fetching products..."
        npm run product:list
        ;;
    2)
        echo "📁 Fetching collections..."
        npm run collection:list
        ;;
    3)
        echo "📋 Fetching orders..."
        npm run order:list
        ;;
    4)
        echo "ℹ️ Store information..."
        shopify app info
        ;;
    5)
        echo "🆕 Creating test product..."
        curl -X POST "$SHOPIFY_STORE_URL/admin/api/2023-10/products.json" \
          -H "X-Shopify-Access-Token: $SHOPIFY_ACCESS_TOKEN" \
          -H "Content-Type: application/json" \
          -d '{
            "product": {
              "title": "Test Product - Agent Demo",
              "body_html": "<p>This is a test product created via the agent management script.</p>",
              "vendor": "Agent Demo",
              "product_type": "Demo",
              "status": "draft"
            }
          }'
        echo ""
        echo "✅ Test product created (draft status)"
        ;;
    6)
        echo "💾 Backing up store data..."
        mkdir -p ../backups
        DATE=$(date +%Y%m%d_%H%M%S)
        
        echo "Backing up products..."
        curl -s "$SHOPIFY_STORE_URL/admin/api/2023-10/products.json?limit=250" \
          -H "X-Shopify-Access-Token: $SHOPIFY_ACCESS_TOKEN" > ../backups/products_$DATE.json
        
        echo "Backing up collections..."
        curl -s "$SHOPIFY_STORE_URL/admin/api/2023-10/smart_collections.json?limit=250" \
          -H "X-Shopify-Access-Token: $SHOPIFY_ACCESS_TOKEN" > ../backups/collections_$DATE.json
        
        echo "✅ Backup completed: ../backups/*_$DATE.json"
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac
