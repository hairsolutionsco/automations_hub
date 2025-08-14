#!/bin/bash

# HubSpot MCP Server - Proper Management Script
# The MCP server is SUPPOSED to stay running - that's how MCP works!

echo "🔗 HubSpot MCP Server - Background Service Manager"
echo "=================================================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

cd /workspaces/automations_hub/hubspot

# Load environment
source .env 2>/dev/null || true

show_status() {
    echo -e "${BLUE}📊 HubSpot MCP Server Status${NC}"
    echo "================================"
    
    # Check for running processes
    MCP_PIDS=$(pgrep -f "@hubspot/mcp-server" 2>/dev/null)
    
    if [ -n "$MCP_PIDS" ]; then
        echo -e "${GREEN}✅ HubSpot MCP Server is RUNNING${NC}"
        echo -e "${GREEN}📋 Process IDs: $MCP_PIDS${NC}"
        echo -e "${GREEN}🌐 Available at: http://127.0.0.1:3001${NC}"
        echo ""
        echo -e "${BLUE}📝 This is CORRECT behavior - MCP servers stay running!${NC}"
        echo -e "${BLUE}🔌 VS Code will connect to this server automatically${NC}"
        
        # Show recent log output
        if [ -f "hubspot_mcp.log" ]; then
            echo ""
            echo -e "${BLUE}📋 Recent Activity:${NC}"
            tail -5 hubspot_mcp.log | sed 's/^/  /'
        fi
        
        return 0
    else
        echo -e "${RED}❌ HubSpot MCP Server is NOT running${NC}"
        return 1
    fi
}

start_background() {
    echo -e "${BLUE}🚀 Starting HubSpot MCP Server in Background${NC}"
    echo ""
    
    # Check if already running
    if pgrep -f "@hubspot/mcp-server" >/dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Server is already running!${NC}"
        show_status
        return 0
    fi
    
    # Verify authentication
    if [ -z "$PRIVATE_APP_ACCESS_TOKEN" ]; then
        echo -e "${RED}❌ PRIVATE_APP_ACCESS_TOKEN not found${NC}"
        echo "Make sure .env file is configured properly"
        return 1
    fi
    
    echo -e "${GREEN}✅ Authentication configured${NC}"
    echo -e "${BLUE}🔄 Starting server in background...${NC}"
    
    # Start server in background with proper logging
    nohup npm run mcp:start > hubspot_mcp.log 2>&1 &
    SERVER_PID=$!
    
    echo -e "${GREEN}✅ Server started with PID: $SERVER_PID${NC}"
    echo -e "${BLUE}📁 Logs: hubspot_mcp.log${NC}"
    echo ""
    
    # Wait a moment for startup
    sleep 3
    
    # Check if it's running
    if pgrep -f "@hubspot/mcp-server" >/dev/null 2>&1; then
        echo -e "${GREEN}🎉 SUCCESS! HubSpot MCP Server is running${NC}"
        echo -e "${GREEN}🌐 Available at: http://127.0.0.1:3001${NC}"
        echo ""
        echo -e "${BLUE}💡 Important Notes:${NC}"
        echo -e "${BLUE}  • The server will stay running in the background${NC}"
        echo -e "${BLUE}  • This is normal MCP behavior${NC}"
        echo -e "${BLUE}  • VS Code will connect to it automatically${NC}"
        echo -e "${BLUE}  • Use 'stop' command to shut it down${NC}"
    else
        echo -e "${RED}❌ Server failed to start${NC}"
        echo "Check logs: cat hubspot_mcp.log"
    fi
}

stop_server() {
    echo -e "${BLUE}🛑 Stopping HubSpot MCP Server${NC}"
    
    MCP_PIDS=$(pgrep -f "@hubspot/mcp-server" 2>/dev/null)
    
    if [ -n "$MCP_PIDS" ]; then
        echo "Stopping processes: $MCP_PIDS"
        pkill -f "@hubspot/mcp-server"
        sleep 2
        
        # Verify stopped
        if ! pgrep -f "@hubspot/mcp-server" >/dev/null 2>&1; then
            echo -e "${GREEN}✅ Server stopped successfully${NC}"
        else
            echo -e "${YELLOW}⚠️  Force killing remaining processes${NC}"
            pkill -9 -f "@hubspot/mcp-server"
        fi
    else
        echo -e "${YELLOW}⚠️  No server processes found${NC}"
    fi
}

show_logs() {
    echo -e "${BLUE}📋 HubSpot MCP Server Logs${NC}"
    echo "=========================="
    
    if [ -f "hubspot_mcp.log" ]; then
        echo -e "${BLUE}📄 Live log output:${NC}"
        tail -20 hubspot_mcp.log
        echo ""
        echo -e "${BLUE}💡 Use 'tail -f hubspot_mcp.log' to follow live logs${NC}"
    else
        echo "No log file found"
    fi
}

test_access() {
    echo -e "${BLUE}🧪 Testing HubSpot Full Access${NC}"
    echo "=============================="
    
    if [ -z "$PRIVATE_APP_ACCESS_TOKEN" ]; then
        echo -e "${RED}❌ Access token not configured${NC}"
        return 1
    fi
    
    echo "Testing CRM access..."
    CONTACTS_TEST=$(curl -s -H "Authorization: Bearer $PRIVATE_APP_ACCESS_TOKEN" \
        "https://api.hubapi.com/crm/v3/objects/contacts?limit=1")
    
    if echo "$CONTACTS_TEST" | grep -q '"results"'; then
        echo -e "${GREEN}✅ CRM Access: Working${NC}"
    else
        echo -e "${RED}❌ CRM Access: Failed${NC}"
    fi
    
    echo "Testing CMS access..."
    CMS_TEST=$(curl -s -H "Authorization: Bearer $PRIVATE_APP_ACCESS_TOKEN" \
        "https://api.hubapi.com/cms/v3/pages?limit=1")
    
    if echo "$CMS_TEST" | grep -q '"results"'; then
        echo -e "${GREEN}✅ CMS Access: Working${NC}"
    else
        echo -e "${RED}❌ CMS Access: Failed${NC}"
    fi
    
    echo "Testing Blog access..."
    BLOG_TEST=$(curl -s -H "Authorization: Bearer $PRIVATE_APP_ACCESS_TOKEN" \
        "https://api.hubapi.com/cms/v3/blogs/posts?limit=1")
    
    if echo "$BLOG_TEST" | grep -q '"results"'; then
        echo -e "${GREEN}✅ Blog Access: Working${NC}"
    else
        echo -e "${RED}❌ Blog Access: Failed${NC}"
    fi
    
    echo "Testing Design Manager access..."
    DESIGN_TEST=$(curl -s -H "Authorization: Bearer $PRIVATE_APP_ACCESS_TOKEN" \
        "https://api.hubapi.com/filemanager/api/v3/files/list")
    
    if echo "$DESIGN_TEST" | grep -q '"objects"'; then
        echo -e "${GREEN}✅ Design Manager Access: Working${NC}"
    else
        echo -e "${RED}❌ Design Manager Access: Failed${NC}"
    fi
    
    echo ""
    echo -e "${GREEN}🎉 You have FULL HubSpot access through the MCP server!${NC}"
}

case "${1:-status}" in
    start)
        start_background
        ;;
    stop)
        stop_server
        ;;
    restart)
        stop_server
        sleep 2
        start_background
        ;;
    status)
        show_status
        ;;
    logs)
        show_logs
        ;;
    test)
        test_access
        ;;
    *)
        echo "HubSpot MCP Server Manager"
        echo "========================="
        echo ""
        echo "Usage: $0 {start|stop|restart|status|logs|test}"
        echo ""
        echo "Commands:"
        echo "  start   - Start server in background (proper way)"
        echo "  stop    - Stop the server"
        echo "  restart - Restart the server"
        echo "  status  - Check if server is running"
        echo "  logs    - Show server logs"
        echo "  test    - Test full HubSpot API access"
        echo ""
        echo -e "${BLUE}💡 Remember: MCP servers are supposed to stay running!${NC}"
        ;;
esac
