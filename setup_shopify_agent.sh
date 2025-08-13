#!/bin/bash

# Shopify Agent Features Setup Script

echo "🤖 Setting up Shopify Agent Features..."

# Check if we're in the right directory
if [[ ! -d "shopify/agent" ]]; then
    echo "❌ Error: Please run this script from the automations_hub root directory"
    exit 1
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install fastapi uvicorn httpx pydantic

# Check if dependencies are installed
echo "✅ Checking dependencies..."
python -c "import fastapi, uvicorn, httpx, pydantic; print('All dependencies installed successfully')" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Error installing dependencies. Please install manually:"
    echo "   pip install fastapi uvicorn httpx pydantic"
    exit 1
fi

# Check environment variables
echo "🔧 Checking environment configuration..."

if [ -z "$SHOPIFY_CATALOG_API_TOKEN" ]; then
    echo "⚠️  Warning: SHOPIFY_CATALOG_API_TOKEN not set"
    echo "   Apply for early access at: https://shopify.dev/docs/api/agentic-commerce"
    echo "   Then set: export SHOPIFY_CATALOG_API_TOKEN='your_token'"
else
    echo "✅ SHOPIFY_CATALOG_API_TOKEN is set"
fi

if [ -z "$SHOPIFY_STORE_URL" ] || [ -z "$SHOPIFY_ACCESS_TOKEN" ]; then
    echo "⚠️  Info: Store credentials not set (optional for agent features)"
    echo "   For local store integration, set:"
    echo "   export SHOPIFY_STORE_URL='https://your-store.myshopify.com'"
    echo "   export SHOPIFY_ACCESS_TOKEN='your_token'"
else
    echo "✅ Store credentials are set"
fi

# Test the API server
echo "🚀 Testing API server..."
cd shopify/agent

# Start server in background
python api_server.py &
SERVER_PID=$!

# Wait a moment for server to start
sleep 3

# Test the status endpoint
STATUS_RESPONSE=$(curl -s http://localhost:8000/api/status 2>/dev/null)

if [ $? -eq 0 ]; then
    echo "✅ API server is working"
    echo "📊 Status: $STATUS_RESPONSE"
else
    echo "⚠️  API server test failed - may need manual testing"
fi

# Stop the test server
kill $SERVER_PID 2>/dev/null

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📚 Next steps:"
echo "1. Apply for Shopify Agent early access (if not done already)"
echo "2. Set your SHOPIFY_CATALOG_API_TOKEN environment variable"
echo "3. Start the API server: cd shopify/agent && python api_server.py"
echo "4. Visit the demo: http://localhost:8000/demo"
echo "5. Check status: http://localhost:8000/api/status"
echo ""
echo "📖 Documentation: shopify/agent/README.md"
