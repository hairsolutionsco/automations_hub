#!/bin/bash

# HubSpot MCP Server Management Script
# Provides complete management of HubSpot MCP server with full platform access

echo "🔗 HubSpot MCP Server Management"
echo "================================"

# Check if we're in the right directory
if [[ ! -f "package.json" ]]; then
    echo "❌ Error: Please run this script from the hubspot directory"
    exit 1
fi

# Load environment variables
if [ -f .env ]; then
    source .env
fi

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "🎯 HubSpot MCP Server Options:"
echo ""
echo "Server Management:"
echo "1. Start HubSpot MCP Server (Full Access)"
echo "2. Start MCP Server in Development Mode"
echo "3. Check Server Status"
echo "4. Stop MCP Server"
echo ""
echo "Authentication:"
echo "5. Check Authentication Status"
echo "6. Re-authenticate HubSpot"
echo "7. View Account Details"
echo ""
echo "Access Testing:"
echo "8. Test CRM Access (Contacts/Companies/Deals)"
echo "9. Test CMS Access (Pages/Templates)"
echo "10. Test Blog Access (Posts/Authors)"
echo "11. Test Design Manager Access"
echo "12. Test Marketing Tools Access"
echo ""
echo "Advanced:"
echo "13. Export HubSpot Configuration"
echo "14. Run Full Access Test Suite"
echo "15. View MCP Server Logs"

read -p "Enter your choice (1-15): " choice

case $choice in
    1)
        echo -e "${BLUE}🚀 Starting HubSpot MCP Server with Full Access...${NC}"
        echo "📋 Available Capabilities:"
        echo "  ✅ CRM (Contacts, Companies, Deals, Tickets)"
        echo "  ✅ CMS (Pages, Templates, Modules)"
        echo "  ✅ Design Manager (Assets, Files)"
        echo "  ✅ Blog (Posts, Authors, Topics)"
        echo "  ✅ Marketing (Forms, Lists, Campaigns)"
        echo "  ✅ Sales (Pipelines, Quotes)"
        echo "  ✅ Automation (Workflows, Properties)"
        echo ""
        echo -e "${GREEN}🔑 Authentication: Using Personal Access Key${NC}"
        echo -e "${GREEN}🌐 Server URL: http://127.0.0.1:3001${NC}"
        echo ""
        
        # Ensure environment variables are loaded
        source .env 2>/dev/null || true
        
        echo "Starting server..."
        npm run mcp:start
        ;;
    2)
        echo -e "${BLUE}🛠️ Starting HubSpot MCP Server in Development Mode...${NC}"
        source .env 2>/dev/null || true
        npm run mcp:dev
        ;;
    3)
        echo -e "${BLUE}🔍 Checking HubSpot MCP Server Status...${NC}"
        
        # Check if server is running on port 3001
        if lsof -Pi :3001 -sTCP:LISTEN -t >/dev/null ; then
            echo -e "${GREEN}✅ HubSpot MCP Server is running on port 3001${NC}"
            
            # Try to connect to server
            if curl -s --connect-timeout 5 http://127.0.0.1:3001 >/dev/null 2>&1; then
                echo -e "${GREEN}✅ Server is accessible at http://127.0.0.1:3001${NC}"
            else
                echo -e "${YELLOW}⚠️  Server is running but may not be fully ready${NC}"
            fi
        else
            echo -e "${RED}❌ HubSpot MCP Server is not running${NC}"
            echo "Start it with option 1 or 2"
        fi
        ;;
    4)
        echo -e "${BLUE}🛑 Stopping HubSpot MCP Server...${NC}"
        pkill -f "@hubspot/mcp-server" && echo -e "${GREEN}✅ Server stopped${NC}" || echo -e "${YELLOW}⚠️  No server process found${NC}"
        ;;
    5)
        echo -e "${BLUE}🔐 Checking HubSpot Authentication Status...${NC}"
        
        if [ -f "hubspot.config.yml" ]; then
            echo -e "${GREEN}✅ HubSpot configuration file found${NC}"
            
            # Extract portal ID and account name
            if command -v yq >/dev/null 2>&1; then
                PORTAL_ID=$(yq r hubspot.config.yml 'defaultPortal' 2>/dev/null)
                echo "📊 Default Portal ID: $PORTAL_ID"
            else
                echo "📊 Configuration file exists (install 'yq' for detailed info)"
            fi
        else
            echo -e "${RED}❌ No HubSpot configuration found${NC}"
            echo "Run option 6 to authenticate"
        fi
        
        if [ -f ".env" ] && grep -q "PRIVATE_APP_ACCESS_TOKEN" .env; then
            echo -e "${GREEN}✅ Environment variables configured${NC}"
        else
            echo -e "${RED}❌ Environment variables not configured${NC}"
        fi
        ;;
    6)
        echo -e "${BLUE}🔑 Re-authenticating with HubSpot...${NC}"
        echo "This will guide you through the authentication process..."
        npx hs auth personalaccesskey
        
        echo ""
        echo -e "${YELLOW}⚠️  Don't forget to update the .env file with your access token!${NC}"
        ;;
    7)
        echo -e "${BLUE}👤 HubSpot Account Details...${NC}"
        
        if [ -f "hubspot.config.yml" ]; then
            echo "📋 Configuration Details:"
            cat hubspot.config.yml | head -10
        else
            echo -e "${RED}❌ No configuration found${NC}"
        fi
        ;;
    8)
        echo -e "${BLUE}🧪 Testing CRM Access...${NC}"
        
        if [ -z "$PRIVATE_APP_ACCESS_TOKEN" ]; then
            echo -e "${RED}❌ Access token not found in environment${NC}"
            echo "Make sure .env file is configured and run 'source .env'"
            exit 1
        fi
        
        echo "🔍 Testing CRM endpoints..."
        
        # Test contacts endpoint
        echo "📧 Testing Contacts API..."
        CONTACTS_RESPONSE=$(curl -s -H "Authorization: Bearer $PRIVATE_APP_ACCESS_TOKEN" \
            "https://api.hubapi.com/crm/v3/objects/contacts?limit=1")
        
        if echo "$CONTACTS_RESPONSE" | grep -q '"results"'; then
            echo -e "${GREEN}✅ Contacts API: Working${NC}"
        else
            echo -e "${RED}❌ Contacts API: Failed${NC}"
        fi
        
        # Test companies endpoint
        echo "🏢 Testing Companies API..."
        COMPANIES_RESPONSE=$(curl -s -H "Authorization: Bearer $PRIVATE_APP_ACCESS_TOKEN" \
            "https://api.hubapi.com/crm/v3/objects/companies?limit=1")
        
        if echo "$COMPANIES_RESPONSE" | grep -q '"results"'; then
            echo -e "${GREEN}✅ Companies API: Working${NC}"
        else
            echo -e "${RED}❌ Companies API: Failed${NC}"
        fi
        
        # Test deals endpoint
        echo "💼 Testing Deals API..."
        DEALS_RESPONSE=$(curl -s -H "Authorization: Bearer $PRIVATE_APP_ACCESS_TOKEN" \
            "https://api.hubapi.com/crm/v3/objects/deals?limit=1")
        
        if echo "$DEALS_RESPONSE" | grep -q '"results"'; then
            echo -e "${GREEN}✅ Deals API: Working${NC}"
        else
            echo -e "${RED}❌ Deals API: Failed${NC}"
        fi
        ;;
    9)
        echo -e "${BLUE}🧪 Testing CMS Access...${NC}"
        
        if [ -z "$PRIVATE_APP_ACCESS_TOKEN" ]; then
            echo -e "${RED}❌ Access token not found${NC}"
            exit 1
        fi
        
        echo "📄 Testing CMS Pages API..."
        CMS_RESPONSE=$(curl -s -H "Authorization: Bearer $PRIVATE_APP_ACCESS_TOKEN" \
            "https://api.hubapi.com/cms/v3/pages?limit=1")
        
        if echo "$CMS_RESPONSE" | grep -q '"results"'; then
            echo -e "${GREEN}✅ CMS Pages API: Working${NC}"
        else
            echo -e "${RED}❌ CMS Pages API: Failed${NC}"
        fi
        ;;
    10)
        echo -e "${BLUE}🧪 Testing Blog Access...${NC}"
        
        if [ -z "$PRIVATE_APP_ACCESS_TOKEN" ]; then
            echo -e "${RED}❌ Access token not found${NC}"
            exit 1
        fi
        
        echo "📝 Testing Blog Posts API..."
        BLOG_RESPONSE=$(curl -s -H "Authorization: Bearer $PRIVATE_APP_ACCESS_TOKEN" \
            "https://api.hubapi.com/cms/v3/blogs/posts?limit=1")
        
        if echo "$BLOG_RESPONSE" | grep -q '"results"'; then
            echo -e "${GREEN}✅ Blog Posts API: Working${NC}"
        else
            echo -e "${RED}❌ Blog Posts API: Failed${NC}"
        fi
        ;;
    11)
        echo -e "${BLUE}🧪 Testing Design Manager Access...${NC}"
        
        if [ -z "$PRIVATE_APP_ACCESS_TOKEN" ]; then
            echo -e "${RED}❌ Access token not found${NC}"
            exit 1
        fi
        
        echo "🎨 Testing File Manager API..."
        FILES_RESPONSE=$(curl -s -H "Authorization: Bearer $PRIVATE_APP_ACCESS_TOKEN" \
            "https://api.hubapi.com/filemanager/api/v3/files/list")
        
        if echo "$FILES_RESPONSE" | grep -q '"objects"'; then
            echo -e "${GREEN}✅ Design Manager API: Working${NC}"
        else
            echo -e "${RED}❌ Design Manager API: Failed${NC}"
        fi
        ;;
    12)
        echo -e "${BLUE}🧪 Testing Marketing Tools Access...${NC}"
        
        if [ -z "$PRIVATE_APP_ACCESS_TOKEN" ]; then
            echo -e "${RED}❌ Access token not found${NC}"
            exit 1
        fi
        
        echo "📋 Testing Forms API..."
        FORMS_RESPONSE=$(curl -s -H "Authorization: Bearer $PRIVATE_APP_ACCESS_TOKEN" \
            "https://api.hubapi.com/forms/v2/forms?limit=1")
        
        if echo "$FORMS_RESPONSE" | grep -q '"total"'; then
            echo -e "${GREEN}✅ Forms API: Working${NC}"
        else
            echo -e "${RED}❌ Forms API: Failed${NC}"
        fi
        ;;
    13)
        echo -e "${BLUE}📤 Exporting HubSpot Configuration...${NC}"
        
        DATE=$(date +%Y%m%d_%H%M%S)
        EXPORT_DIR="exports/config_$DATE"
        mkdir -p "$EXPORT_DIR"
        
        if [ -f "hubspot.config.yml" ]; then
            cp hubspot.config.yml "$EXPORT_DIR/"
            echo -e "${GREEN}✅ Configuration exported to $EXPORT_DIR${NC}"
        fi
        
        if [ -f ".env" ]; then
            # Export .env without sensitive tokens
            grep -v "ACCESS_TOKEN" .env > "$EXPORT_DIR/env_template" || true
            echo -e "${GREEN}✅ Environment template exported${NC}"
        fi
        ;;
    14)
        echo -e "${BLUE}🔍 Running Full Access Test Suite...${NC}"
        echo "This will test all HubSpot API endpoints..."
        
        TESTS_PASSED=0
        TOTAL_TESTS=6
        
        if [ -z "$PRIVATE_APP_ACCESS_TOKEN" ]; then
            echo -e "${RED}❌ Access token not found. Cannot run tests.${NC}"
            exit 1
        fi
        
        # Test 1: CRM Contacts
        echo "1/6 Testing CRM Contacts..."
        if curl -s -H "Authorization: Bearer $PRIVATE_APP_ACCESS_TOKEN" \
            "https://api.hubapi.com/crm/v3/objects/contacts?limit=1" | grep -q '"results"'; then
            echo -e "${GREEN}  ✅ CRM Contacts: PASS${NC}"
            TESTS_PASSED=$((TESTS_PASSED + 1))
        else
            echo -e "${RED}  ❌ CRM Contacts: FAIL${NC}"
        fi
        
        # Test 2: CRM Companies
        echo "2/6 Testing CRM Companies..."
        if curl -s -H "Authorization: Bearer $PRIVATE_APP_ACCESS_TOKEN" \
            "https://api.hubapi.com/crm/v3/objects/companies?limit=1" | grep -q '"results"'; then
            echo -e "${GREEN}  ✅ CRM Companies: PASS${NC}"
            TESTS_PASSED=$((TESTS_PASSED + 1))
        else
            echo -e "${RED}  ❌ CRM Companies: FAIL${NC}"
        fi
        
        # Test 3: CMS Pages
        echo "3/6 Testing CMS Pages..."
        if curl -s -H "Authorization: Bearer $PRIVATE_APP_ACCESS_TOKEN" \
            "https://api.hubapi.com/cms/v3/pages?limit=1" | grep -q '"results"'; then
            echo -e "${GREEN}  ✅ CMS Pages: PASS${NC}"
            TESTS_PASSED=$((TESTS_PASSED + 1))
        else
            echo -e "${RED}  ❌ CMS Pages: FAIL${NC}"
        fi
        
        # Test 4: Blog Posts
        echo "4/6 Testing Blog Posts..."
        if curl -s -H "Authorization: Bearer $PRIVATE_APP_ACCESS_TOKEN" \
            "https://api.hubapi.com/cms/v3/blogs/posts?limit=1" | grep -q '"results"'; then
            echo -e "${GREEN}  ✅ Blog Posts: PASS${NC}"
            TESTS_PASSED=$((TESTS_PASSED + 1))
        else
            echo -e "${RED}  ❌ Blog Posts: FAIL${NC}"
        fi
        
        # Test 5: Design Manager
        echo "5/6 Testing Design Manager..."
        if curl -s -H "Authorization: Bearer $PRIVATE_APP_ACCESS_TOKEN" \
            "https://api.hubapi.com/filemanager/api/v3/files/list" | grep -q '"objects"'; then
            echo -e "${GREEN}  ✅ Design Manager: PASS${NC}"
            TESTS_PASSED=$((TESTS_PASSED + 1))
        else
            echo -e "${RED}  ❌ Design Manager: FAIL${NC}"
        fi
        
        # Test 6: Forms
        echo "6/6 Testing Marketing Forms..."
        if curl -s -H "Authorization: Bearer $PRIVATE_APP_ACCESS_TOKEN" \
            "https://api.hubapi.com/forms/v2/forms?limit=1" | grep -q '"total"'; then
            echo -e "${GREEN}  ✅ Marketing Forms: PASS${NC}"
            TESTS_PASSED=$((TESTS_PASSED + 1))
        else
            echo -e "${RED}  ❌ Marketing Forms: FAIL${NC}"
        fi
        
        echo ""
        echo "📊 Test Results: $TESTS_PASSED/$TOTAL_TESTS tests passed"
        
        if [ $TESTS_PASSED -eq $TOTAL_TESTS ]; then
            echo -e "${GREEN}🎉 All tests passed! You have full HubSpot access.${NC}"
        else
            echo -e "${YELLOW}⚠️  Some tests failed. Check your permissions or token scope.${NC}"
        fi
        ;;
    15)
        echo -e "${BLUE}📋 HubSpot MCP Server Logs...${NC}"
        
        if lsof -Pi :3001 -sTCP:LISTEN -t >/dev/null ; then
            echo "MCP Server is running. Here are recent logs:"
            echo "(Press Ctrl+C to exit log view)"
            journalctl --user -f -u hubspot-mcp 2>/dev/null || \
            tail -f /tmp/hubspot-mcp.log 2>/dev/null || \
            echo "No logs available. Server may be running without detailed logging."
        else
            echo -e "${RED}❌ MCP Server is not running${NC}"
        fi
        ;;
    *)
        echo -e "${RED}❌ Invalid option. Please choose 1-15.${NC}"
        ;;
esac
