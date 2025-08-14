#!/bin/bash

# HubSpot MCP Server Daemon Script
# Ensures the server stays running in the background

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Configuration
PID_FILE="$SCRIPT_DIR/hubspot_mcp.pid"
LOG_FILE="$SCRIPT_DIR/hubspot_mcp.log"
ERROR_LOG="$SCRIPT_DIR/hubspot_mcp_error.log"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Load environment variables
source .env 2>/dev/null || true

start_server() {
    echo -e "${BLUE}🚀 Starting HubSpot MCP Server...${NC}"
    
    # Check if already running
    if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
        echo -e "${YELLOW}⚠️  Server is already running (PID: $(cat "$PID_FILE"))${NC}"
        return 1
    fi
    
    # Ensure environment is loaded
    if [ -z "$PRIVATE_APP_ACCESS_TOKEN" ]; then
        echo -e "${RED}❌ PRIVATE_APP_ACCESS_TOKEN not found. Check .env file${NC}"
        return 1
    fi
    
    echo "📋 Configuration:"
    echo "  🔑 Access Token: Configured"
    echo "  🌐 Server URL: http://127.0.0.1:3001"
    echo "  📁 Log File: $LOG_FILE"
    echo ""
    
    # Start the server in background
    nohup npm run mcp:start > "$LOG_FILE" 2> "$ERROR_LOG" &
    SERVER_PID=$!
    
    # Save PID
    echo $SERVER_PID > "$PID_FILE"
    
    # Wait a moment and check if it's still running
    sleep 3
    
    if kill -0 "$SERVER_PID" 2>/dev/null; then
        echo -e "${GREEN}✅ HubSpot MCP Server started successfully${NC}"
        echo -e "${GREEN}📋 PID: $SERVER_PID${NC}"
        echo -e "${GREEN}🌐 Available at: http://127.0.0.1:3001${NC}"
        
        # Test connection
        echo -e "${BLUE}🔍 Testing server connection...${NC}"
        sleep 2
        
        # Check if port is open
        if netstat -tuln | grep -q ":3001 "; then
            echo -e "${GREEN}✅ Server is listening on port 3001${NC}"
        else
            echo -e "${YELLOW}⚠️  Server may still be starting up...${NC}"
        fi
        
        return 0
    else
        echo -e "${RED}❌ Server failed to start${NC}"
        echo "Check error log: $ERROR_LOG"
        cat "$ERROR_LOG" 2>/dev/null
        rm -f "$PID_FILE"
        return 1
    fi
}

stop_server() {
    echo -e "${BLUE}🛑 Stopping HubSpot MCP Server...${NC}"
    
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            kill "$PID"
            echo -e "${GREEN}✅ Server stopped (PID: $PID)${NC}"
        else
            echo -e "${YELLOW}⚠️  Process not found${NC}"
        fi
        rm -f "$PID_FILE"
    else
        echo -e "${YELLOW}⚠️  No PID file found${NC}"
    fi
    
    # Kill any remaining processes
    pkill -f "@hubspot/mcp-server" 2>/dev/null && echo -e "${GREEN}✅ Cleaned up any remaining processes${NC}"
}

status_server() {
    echo -e "${BLUE}🔍 HubSpot MCP Server Status${NC}"
    echo "================================"
    
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            echo -e "${GREEN}✅ Server is running (PID: $PID)${NC}"
            
            # Check port
            if netstat -tuln | grep -q ":3001 "; then
                echo -e "${GREEN}✅ Listening on port 3001${NC}"
            else
                echo -e "${YELLOW}⚠️  Port 3001 not detected${NC}"
            fi
            
            # Show recent logs
            echo ""
            echo -e "${BLUE}📋 Recent logs:${NC}"
            tail -5 "$LOG_FILE" 2>/dev/null || echo "No logs available"
            
        else
            echo -e "${RED}❌ Server not running (stale PID file)${NC}"
            rm -f "$PID_FILE"
        fi
    else
        echo -e "${RED}❌ Server not running${NC}"
    fi
}

restart_server() {
    echo -e "${BLUE}🔄 Restarting HubSpot MCP Server...${NC}"
    stop_server
    sleep 2
    start_server
}

show_logs() {
    echo -e "${BLUE}📋 HubSpot MCP Server Logs${NC}"
    echo "============================"
    
    if [ -f "$LOG_FILE" ]; then
        echo -e "${BLUE}📄 Main Log:${NC}"
        tail -20 "$LOG_FILE"
    else
        echo "No main log file found"
    fi
    
    echo ""
    
    if [ -f "$ERROR_LOG" ]; then
        echo -e "${RED}🚨 Error Log:${NC}"
        tail -10 "$ERROR_LOG"
    else
        echo "No error log file found"
    fi
}

case "${1:-start}" in
    start)
        start_server
        ;;
    stop)
        stop_server
        ;;
    restart)
        restart_server
        ;;
    status)
        status_server
        ;;
    logs)
        show_logs
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|logs}"
        echo ""
        echo "Commands:"
        echo "  start   - Start HubSpot MCP server in background"
        echo "  stop    - Stop HubSpot MCP server"
        echo "  restart - Restart HubSpot MCP server"
        echo "  status  - Check server status"
        echo "  logs    - Show server logs"
        exit 1
        ;;
esac
