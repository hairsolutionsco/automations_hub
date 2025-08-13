#!/bin/bash

# Shopify Agent Features Quick Start Script

echo "🤖 Shopify Agent Features Quick Start"
echo "====================================="

# Check if we're in the right directory
if [[ ! -d "../agent" ]]; then
    echo "❌ Error: Please run this script from the shopify/scripts directory"
    exit 1
fi

# Function to check environment variables
check_env() {
    echo "🔧 Checking Environment Variables..."
    
    if [ -z "$SHOPIFY_CATALOG_API_TOKEN" ]; then
        echo "⚠️  SHOPIFY_CATALOG_API_TOKEN not set"
        echo "   Apply for early access: https://shopify.dev/docs/api/agentic-commerce"
        ENV_READY=false
    else
        echo "✅ SHOPIFY_CATALOG_API_TOKEN is set"
        ENV_READY=true
    fi
    
    if [ -z "$SHOPIFY_STORE_URL" ] || [ -z "$SHOPIFY_ACCESS_TOKEN" ]; then
        echo "ℹ️  Store credentials not set (optional)"
    else
        echo "✅ Store credentials are set"
    fi
}

# Function to check dependencies
check_deps() {
    echo "📦 Checking Dependencies..."
    
    python -c "import fastapi, uvicorn, httpx, pydantic" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "✅ All Python dependencies installed"
        DEPS_READY=true
    else
        echo "❌ Missing dependencies. Installing..."
        pip install fastapi uvicorn httpx pydantic
        DEPS_READY=true
    fi
}

# Function to start the API server
start_server() {
    echo "🚀 Starting Shopify Agent API Server..."
    cd ../agent
    
    echo "Starting server at http://localhost:8000"
    echo "API Docs: http://localhost:8000/docs"
    echo "Demo: http://localhost:8000/demo"
    echo "Status: http://localhost:8000/api/status"
    echo ""
    echo "Press Ctrl+C to stop the server"
    
    python api_server.py
}

# Function to test the API
test_api() {
    echo "🧪 Testing API..."
    
    # Wait for server to start
    sleep 3
    
    echo "Testing status endpoint..."
    curl -s http://localhost:8000/api/status | python -m json.tool
    
    if [ "$ENV_READY" = true ]; then
        echo "Testing catalog search..."
        curl -X POST http://localhost:8000/api/search-catalog \
          -H "Content-Type: application/json" \
          -d '{"query": "test product", "limit": 2}' | python -m json.tool
    else
        echo "⚠️  Skipping catalog test - API token not set"
    fi
}

# Main execution
check_env
check_deps

echo ""
echo "🎯 What would you like to do?"
echo "1. Start API Server"
echo "2. Test API (requires running server)"
echo "3. View Documentation"
echo "4. Check Status Only"

read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        start_server
        ;;
    2)
        test_api
        ;;
    3)
        echo "📚 Opening documentation..."
        if command -v code &> /dev/null; then
            code ../agent/README.md
        else
            cat ../agent/README.md
        fi
        ;;
    4)
        if curl -s http://localhost:8000/health &> /dev/null; then
            echo "✅ Server is running"
            curl -s http://localhost:8000/api/status | python -m json.tool
        else
            echo "❌ Server is not running"
            echo "Start it with: ./agent_quickstart.sh and choose option 1"
        fi
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac
