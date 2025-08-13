#!/bin/bash

# Golf MCP Server Management Script

echo "⛳ Golf MCP Server Management"
echo "============================"

# Check if we're in the right directory
if [[ ! -f "../golf.json" ]]; then
    echo "❌ Error: Please run this script from the automations-mcp/scripts directory"
    exit 1
fi

# Check if golf command is available
if ! command -v golf &> /dev/null; then
    echo "❌ Golf MCP command not found. Please install golf-mcp first."
    exit 1
fi

echo "🎯 MCP Server Operations:"
echo ""
echo "Development:"
echo "1. Build MCP server (development)"
echo "2. Run MCP server"
echo "3. Build and run (quick start)"
echo "4. Stop MCP server"
echo ""
echo "Management:"
echo "5. Check server status"
echo "6. View server logs"
echo "7. Test MCP tools"
echo "8. Restart server"
echo ""
echo "Configuration:"
echo "9. Edit golf.json config"
echo "10. Validate configuration"
echo "11. Backup configuration"
echo "12. Reset to defaults"

read -p "Enter your choice (1-12): " choice

case $choice in
    1)
        echo "🏗️ Building MCP server (development mode)..."
        cd ..
        golf build dev
        
        if [ $? -eq 0 ]; then
            echo "✅ Build completed successfully"
        else
            echo "❌ Build failed"
        fi
        ;;
    2)
        echo "🚀 Running MCP server..."
        cd ..
        echo "Server will start on port 3000 (configured in golf.json)"
        echo "Press Ctrl+C to stop the server"
        golf run
        ;;
    3)
        echo "⚡ Quick start: Build and run..."
        cd ..
        echo "Building..."
        golf build dev
        
        if [ $? -eq 0 ]; then
            echo "✅ Build successful, starting server..."
            golf run
        else
            echo "❌ Build failed, cannot start server"
        fi
        ;;
    4)
        echo "🛑 Stopping MCP server..."
        pkill -f "golf run"
        pkill -f "python.*golf"
        echo "✅ MCP server stopped"
        ;;
    5)
        echo "📊 Checking server status..."
        
        # Check if golf process is running
        if pgrep -f "golf run" > /dev/null; then
            echo "✅ Golf MCP server is running"
            
            # Try to connect to the server
            if curl -s http://localhost:3000/health &> /dev/null; then
                echo "✅ Server is responding on port 3000"
            else
                echo "⚠️  Server process running but not responding"
            fi
        else
            echo "❌ Golf MCP server is not running"
        fi
        
        # Check configuration
        if [ -f "../golf.json" ]; then
            echo "✅ Configuration file exists"
            echo "📋 Server config:"
            cat ../golf.json | python -m json.tool 2>/dev/null || cat ../golf.json
        else
            echo "❌ Configuration file missing"
        fi
        ;;
    6)
        echo "📜 Viewing server logs..."
        echo "Looking for recent log files..."
        
        # Look for common log locations
        if [ -f "../server.log" ]; then
            echo "📄 Server log (last 50 lines):"
            tail -50 ../server.log
        elif [ -f "../golf.log" ]; then
            echo "📄 Golf log (last 50 lines):"
            tail -50 ../golf.log
        else
            echo "ℹ️  No log files found. Server logs may be in stdout/stderr."
            echo "Run the server with: golf run > server.log 2>&1 &"
        fi
        ;;
    7)
        echo "🧪 Testing MCP tools..."
        
        # Check if server is running
        if ! curl -s http://localhost:3000/health &> /dev/null; then
            echo "❌ Server not running. Start it first with option 1-3."
            exit 1
        fi
        
        echo "🔍 Available MCP tools:"
        
        # Test basic endpoints
        echo "📡 Testing health endpoint..."
        curl -s http://localhost:3000/health && echo " ✅" || echo " ❌"
        
        echo "📡 Testing tools list..."
        curl -s http://localhost:3000/tools && echo " ✅" || echo " ❌"
        
        # Test specific tool integrations
        echo ""
        echo "🔧 Testing tool integrations:"
        
        # Check if Shopify tools are available
        if [ -f "../tools/shopify/products.py" ]; then
            echo "  📦 Shopify tools: Available"
        else
            echo "  📦 Shopify tools: Missing"
        fi
        
        # Check if Notion tools are available
        if [ -f "../tools/notion_api.py" ]; then
            echo "  📊 Notion tools: Available"
        else
            echo "  📊 Notion tools: Missing"
        fi
        
        # Check if GitHub tools are available
        if [ -f "../tools/github_user.py" ]; then
            echo "  🐙 GitHub tools: Available"
        else
            echo "  🐙 GitHub tools: Missing"
        fi
        ;;
    8)
        echo "🔄 Restarting MCP server..."
        
        echo "Stopping server..."
        pkill -f "golf run"
        pkill -f "python.*golf"
        
        sleep 2
        
        echo "Building..."
        cd ..
        golf build dev
        
        if [ $? -eq 0 ]; then
            echo "Starting server..."
            golf run &
            
            sleep 3
            
            if curl -s http://localhost:3000/health &> /dev/null; then
                echo "✅ Server restarted successfully"
            else
                echo "⚠️  Server may still be starting up"
            fi
        else
            echo "❌ Build failed, cannot restart server"
        fi
        ;;
    9)
        echo "⚙️ Editing golf.json configuration..."
        
        if command -v code &> /dev/null; then
            code ../golf.json
        elif command -v nano &> /dev/null; then
            nano ../golf.json
        elif command -v vi &> /dev/null; then
            vi ../golf.json
        else
            echo "❌ No editor found. Please edit golf.json manually:"
            echo "$(pwd)/../golf.json"
        fi
        ;;
    10)
        echo "✅ Validating configuration..."
        
        if [ -f "../golf.json" ]; then
            echo "📋 Configuration file exists"
            
            # Validate JSON syntax
            if python -m json.tool ../golf.json > /dev/null 2>&1; then
                echo "✅ JSON syntax is valid"
                
                # Display current configuration
                echo "📄 Current configuration:"
                python -m json.tool ../golf.json
                
            else
                echo "❌ Invalid JSON syntax in golf.json"
                echo "Please fix the JSON syntax errors"
            fi
        else
            echo "❌ Configuration file missing: golf.json"
        fi
        ;;
    11)
        echo "💾 Backing up configuration..."
        DATE=$(date +%Y%m%d_%H%M%S)
        mkdir -p ../backups
        
        # Backup main config
        cp ../golf.json "../backups/golf_config_$DATE.json"
        
        # Backup all related configs
        cp ../*.json "../backups/" 2>/dev/null
        cp ../*.py "../backups/" 2>/dev/null
        
        # Create backup info
        echo "=== MCP Configuration Backup ===" > "../backups/backup_info_$DATE.txt"
        echo "Date: $(date)" >> "../backups/backup_info_$DATE.txt"
        echo "Files backed up:" >> "../backups/backup_info_$DATE.txt"
        ls -la ../backups/*$DATE* >> "../backups/backup_info_$DATE.txt"
        
        echo "✅ Configuration backed up to: backups/golf_config_$DATE.json"
        ;;
    12)
        echo "🔄 Reset to default configuration..."
        echo "⚠️  This will overwrite your current golf.json"
        read -p "Are you sure? (y/N): " confirm
        
        if [[ $confirm == [yY] ]]; then
            # Create backup first
            DATE=$(date +%Y%m%d_%H%M%S)
            cp ../golf.json "../golf_backup_$DATE.json"
            
            # Reset to default
            cat > ../golf.json << 'EOF'
{
  "name": "automations-mcp",
  "description": "MCP server for automation hub with n8n, Notion, and GitHub integration",
  "host": "127.0.0.1",
  "port": 3000,
  "transport": "sse",
  "opentelemetry_enabled": false,
  "auth": {
    "enabled": false
  }
}
EOF
            
            echo "✅ Configuration reset to defaults"
            echo "💾 Previous config saved as: golf_backup_$DATE.json"
        else
            echo "❌ Reset cancelled"
        fi
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac
