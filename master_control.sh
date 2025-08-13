#!/bin/bash

# Master Automation Hub Management Script

echo "🏠 Automation Hub Master Control"
echo "==============================="

# Check if we're in the root directory
if [[ ! -f "package.json" ]] || [[ ! -d "automations-mcp" ]]; then
    echo "❌ Error: Please run this script from the automation hub root directory"
    exit 1
fi

echo "🎯 Master Control Options:"
echo ""
echo "Quick Start:"
echo "1. Start all services"
echo "2. Stop all services"
echo "3. Restart all services"
echo "4. Check all service status"
echo ""
echo "Individual Services:"
echo "5. Manage N8N"
echo "6. Manage HubSpot"
echo "7. Manage Shopify"
echo "8. Manage Notion"
echo "9. Manage MCP Server"
echo ""
echo "Maintenance:"
echo "10. Update all dependencies"
echo "11. Backup all data"
echo "12. Health check all integrations"
echo "13. View system overview"

read -p "Enter your choice (1-13): " choice

case $choice in
    1)
        echo "🚀 Starting all services..."
        
        echo "📊 Starting MCP server..."
        (cd automations-mcp && nohup npm run golf:start > ../logs/mcp.log 2>&1 &)
        
        echo "🔗 Starting HubSpot MCP..."
        (cd hubspot && nohup npm run mcp:dev > ../logs/hubspot.log 2>&1 &)
        
        echo "🤖 Starting Shopify Agent API..."
        (cd shopify/agent && nohup python api_server.py > ../../logs/shopify_agent.log 2>&1 &)
        
        echo "🔄 Starting N8N..."
        (cd n8n && nohup npm run dev > ../logs/n8n.log 2>&1 &)
        
        sleep 5
        
        echo "✅ All services started! Check status with option 4"
        echo "📋 Logs available in logs/ directory"
        ;;
    2)
        echo "🛑 Stopping all services..."
        
        # Stop by process name
        pkill -f "golf run"
        pkill -f "n8n"
        pkill -f "api_server.py"
        pkill -f "hubspot.*mcp"
        
        echo "✅ All services stopped"
        ;;
    3)
        echo "🔄 Restarting all services..."
        
        # Stop first
        echo "Stopping services..."
        pkill -f "golf run"
        pkill -f "n8n"
        pkill -f "api_server.py"
        pkill -f "hubspot.*mcp"
        
        sleep 3
        
        # Start again
        echo "Starting services..."
        mkdir -p logs
        
        (cd automations-mcp && nohup npm run golf:start > ../logs/mcp.log 2>&1 &)
        (cd hubspot && nohup npm run mcp:dev > ../logs/hubspot.log 2>&1 &)
        (cd shopify/agent && nohup python api_server.py > ../../logs/shopify_agent.log 2>&1 &)
        (cd n8n && nohup npm run dev > ../logs/n8n.log 2>&1 &)
        
        sleep 5
        echo "✅ All services restarted"
        ;;
    4)
        echo "📊 Checking all service status..."
        
        echo "🔧 MCP Server (port 3000):"
        if curl -s http://localhost:3000/health &> /dev/null; then
            echo "  ✅ Running and responding"
        else
            echo "  ❌ Not responding"
        fi
        
        echo "🔗 HubSpot MCP (port 3001):"
        if curl -s http://localhost:3001/health &> /dev/null; then
            echo "  ✅ Running and responding"
        else
            echo "  ❌ Not responding"
        fi
        
        echo "🤖 Shopify Agent API (port 8000):"
        if curl -s http://localhost:8000/health &> /dev/null; then
            echo "  ✅ Running and responding"
        else
            echo "  ❌ Not responding"
        fi
        
        echo "🔄 N8N (port 5678):"
        if curl -s http://localhost:5678 &> /dev/null; then
            echo "  ✅ Running and responding"
        else
            echo "  ❌ Not responding"
        fi
        
        echo ""
        echo "📋 Process Status:"
        pgrep -f "golf run" > /dev/null && echo "  ✅ Golf MCP process running" || echo "  ❌ Golf MCP not running"
        pgrep -f "n8n" > /dev/null && echo "  ✅ N8N process running" || echo "  ❌ N8N not running"
        pgrep -f "api_server.py" > /dev/null && echo "  ✅ Shopify Agent running" || echo "  ❌ Shopify Agent not running"
        ;;
    5)
        echo "🔄 Managing N8N..."
        cd n8n/scripts
        ./workflow_manager.sh
        ;;
    6)
        echo "🔗 Managing HubSpot..."
        cd hubspot/scripts
        ./hubspot_manager.sh
        ;;
    7)
        echo "🛍️ Managing Shopify..."
        echo "Choose Shopify management tool:"
        echo "1. Agent Features"
        echo "2. Store Management"
        echo "3. Development Tools"
        
        read -p "Enter choice (1-3): " shopify_choice
        
        case $shopify_choice in
            1)
                cd shopify/scripts
                ./agent_quickstart.sh
                ;;
            2)
                cd shopify/scripts
                ./store_management.sh
                ;;
            3)
                cd shopify/scripts
                ./dev_tools.sh
                ;;
            *)
                echo "Invalid choice"
                ;;
        esac
        ;;
    8)
        echo "📊 Managing Notion..."
        echo "Choose Notion management tool:"
        echo "1. Database Management"
        echo "2. Content Management"
        
        read -p "Enter choice (1-2): " notion_choice
        
        case $notion_choice in
            1)
                cd notion/scripts
                ./database_manager.sh
                ;;
            2)
                cd notion/scripts
                ./content_manager.sh
                ;;
            *)
                echo "Invalid choice"
                ;;
        esac
        ;;
    9)
        echo "⛳ Managing MCP Server..."
        echo "Choose MCP management tool:"
        echo "1. Server Management"
        echo "2. Tools Development"
        
        read -p "Enter choice (1-2): " mcp_choice
        
        case $mcp_choice in
            1)
                cd automations-mcp/scripts
                ./golf_server_manager.sh
                ;;
            2)
                cd automations-mcp/scripts
                ./tools_dev.sh
                ;;
            *)
                echo "Invalid choice"
                ;;
        esac
        ;;
    10)
        echo "📦 Updating all dependencies..."
        
        echo "Updating root dependencies..."
        npm update
        
        echo "Updating N8N dependencies..."
        (cd n8n && npm update)
        
        echo "Updating HubSpot dependencies..."
        (cd hubspot && npm update)
        
        echo "Updating Shopify dependencies..."
        (cd shopify && npm update)
        
        echo "Updating Python dependencies..."
        pip install --upgrade fastapi uvicorn httpx pydantic
        
        echo "✅ All dependencies updated"
        ;;
    11)
        echo "💾 Backing up all data..."
        DATE=$(date +%Y%m%d_%H%M%S)
        mkdir -p "backups/full_backup_$DATE"
        
        echo "Backing up configurations..."
        cp *.json "backups/full_backup_$DATE/" 2>/dev/null
        cp *.md "backups/full_backup_$DATE/" 2>/dev/null
        
        echo "Backing up N8N workflows..."
        if [ -d "n8n/workflows" ]; then
            cp -r n8n/workflows "backups/full_backup_$DATE/"
        fi
        
        echo "Backing up Notion databases..."
        if [ -d "notion/databases" ]; then
            cp -r notion/databases "backups/full_backup_$DATE/"
        fi
        
        echo "Backing up MCP tools..."
        if [ -d "automations-mcp/tools" ]; then
            cp -r automations-mcp/tools "backups/full_backup_$DATE/"
        fi
        
        echo "Backing up Shopify configurations..."
        cp shopify/*.json "backups/full_backup_$DATE/" 2>/dev/null
        
        # Create backup manifest
        echo "=== Automation Hub Full Backup ===" > "backups/full_backup_$DATE/MANIFEST.txt"
        echo "Date: $(date)" >> "backups/full_backup_$DATE/MANIFEST.txt"
        echo "Contents:" >> "backups/full_backup_$DATE/MANIFEST.txt"
        ls -la "backups/full_backup_$DATE/" >> "backups/full_backup_$DATE/MANIFEST.txt"
        
        echo "✅ Full backup created: backups/full_backup_$DATE/"
        ;;
    12)
        echo "🏥 Health check all integrations..."
        
        HEALTH_REPORT="health_check_$(date +%Y%m%d_%H%M%S).txt"
        echo "=== Automation Hub Health Check ===" > "$HEALTH_REPORT"
        echo "Date: $(date)" >> "$HEALTH_REPORT"
        echo "" >> "$HEALTH_REPORT"
        
        # Check services
        echo "🔧 Service Health:" >> "$HEALTH_REPORT"
        
        curl -s http://localhost:3000/health &> /dev/null && echo "✅ MCP Server: Healthy" >> "$HEALTH_REPORT" || echo "❌ MCP Server: Down" >> "$HEALTH_REPORT"
        curl -s http://localhost:3001/health &> /dev/null && echo "✅ HubSpot MCP: Healthy" >> "$HEALTH_REPORT" || echo "❌ HubSpot MCP: Down" >> "$HEALTH_REPORT"
        curl -s http://localhost:8000/health &> /dev/null && echo "✅ Shopify Agent: Healthy" >> "$HEALTH_REPORT" || echo "❌ Shopify Agent: Down" >> "$HEALTH_REPORT"
        curl -s http://localhost:5678 &> /dev/null && echo "✅ N8N: Healthy" >> "$HEALTH_REPORT" || echo "❌ N8N: Down" >> "$HEALTH_REPORT"
        
        echo "" >> "$HEALTH_REPORT"
        
        # Check configurations
        echo "⚙️ Configuration Health:" >> "$HEALTH_REPORT"
        
        [ -f "package.json" ] && echo "✅ Root package.json exists" >> "$HEALTH_REPORT" || echo "❌ Root package.json missing" >> "$HEALTH_REPORT"
        [ -f "automations-mcp/golf.json" ] && echo "✅ MCP config exists" >> "$HEALTH_REPORT" || echo "❌ MCP config missing" >> "$HEALTH_REPORT"
        [ -f "n8n/n8n_package.json" ] && echo "✅ N8N config exists" >> "$HEALTH_REPORT" || echo "❌ N8N config missing" >> "$HEALTH_REPORT"
        
        echo "" >> "$HEALTH_REPORT"
        
        # Check integrations
        echo "🔗 Integration Health:" >> "$HEALTH_REPORT"
        
        [ -d "notion/databases" ] && echo "✅ Notion databases available" >> "$HEALTH_REPORT" || echo "❌ Notion databases missing" >> "$HEALTH_REPORT"
        [ -d "n8n/workflows" ] && echo "✅ N8N workflows available" >> "$HEALTH_REPORT" || echo "❌ N8N workflows missing" >> "$HEALTH_REPORT"
        [ -d "shopify/agent" ] && echo "✅ Shopify agent available" >> "$HEALTH_REPORT" || echo "❌ Shopify agent missing" >> "$HEALTH_REPORT"
        
        echo "✅ Health check completed: $HEALTH_REPORT"
        cat "$HEALTH_REPORT"
        ;;
    13)
        echo "📊 System Overview..."
        
        echo "🏠 Automation Hub System Overview"
        echo "================================="
        echo ""
        
        echo "📁 Directory Structure:"
        echo "  📂 automations-mcp/ - MCP server with tools"
        echo "  📂 n8n/ - Workflow automation"
        echo "  📂 hubspot/ - CRM integration"
        echo "  📂 shopify/ - E-commerce platform"
        echo "  📂 notion/ - Database and content management"
        echo ""
        
        echo "🔧 Available Services:"
        echo "  ⛳ Golf MCP Server (port 3000)"
        echo "  🔗 HubSpot MCP (port 3001)" 
        echo "  🤖 Shopify Agent API (port 8000)"
        echo "  🔄 N8N Workflows (port 5678)"
        echo ""
        
        echo "📊 Statistics:"
        echo "  MCP Tools: $(find automations-mcp/tools -name "*.py" 2>/dev/null | wc -l)"
        echo "  N8N Workflows: $(find n8n/workflows -name "*.json" 2>/dev/null | wc -l)"
        echo "  Notion Databases: $(find notion/databases -name "*.md" 2>/dev/null | wc -l)"
        echo "  Script Files: $(find . -name "scripts" -type d | wc -l) directories created"
        echo ""
        
        echo "🎯 Quick Access Scripts:"
        echo "  📜 ./master_control.sh - This script"
        echo "  📜 ./setup_shopify_agent.sh - Shopify agent setup"
        echo "  📜 Each service has its own scripts/ directory"
        echo ""
        
        echo "📚 Key Features:"
        echo "  ✅ Cross-platform automation"
        echo "  ✅ AI-powered commerce (Shopify Agent)"
        echo "  ✅ CRM integration (HubSpot)"
        echo "  ✅ Database management (Notion)"
        echo "  ✅ Workflow automation (N8N)"
        echo "  ✅ MCP server architecture"
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac
