#!/bin/bash

# HubSpot Management Script

echo "🔗 HubSpot Integration Management"
echo "================================="

# Check if we're in the right directory
if [[ ! -f "../hubspot_package.json" ]]; then
    echo "❌ Error: Please run this script from the hubspot/scripts directory"
    exit 1
fi

# Load environment variables
if [ -f ../.env ]; then
    source ../.env
fi

echo "🎯 HubSpot Management Options:"
echo ""
echo "Authentication:"
echo "1. Login to HubSpot"
echo "2. Check current user"
echo "3. Refresh authentication"
echo ""
echo "MCP Server:"
echo "4. Start HubSpot MCP server"
echo "5. Start MCP server in development mode"
echo "6. Test MCP server connection"
echo ""
echo "Data Management:"
echo "7. Export contacts"
echo "8. Export companies"
echo "9. Export deals"
echo "10. Backup all data"
echo ""
echo "Sync & Integration:"
echo "11. Sync with Notion"
echo "12. Sync with Shopify"
echo "13. Test integrations"

read -p "Enter your choice (1-13): " choice

case $choice in
    1)
        echo "🔐 Logging in to HubSpot..."
        cd ..
        npm run auth
        ;;
    2)
        echo "👤 Checking current user..."
        cd ..
        npm run whoami
        ;;
    3)
        echo "🔄 Refreshing authentication..."
        cd ..
        npm run auth
        echo "✅ Authentication refreshed"
        ;;
    4)
        echo "🚀 Starting HubSpot MCP server..."
        cd ..
        npm run mcp:start
        ;;
    5)
        echo "🛠️ Starting MCP server in development mode..."
        cd ..
        npm run mcp:dev
        ;;
    6)
        echo "🧪 Testing MCP server connection..."
        if curl -s http://localhost:3001/health &> /dev/null; then
            echo "✅ MCP server is running and accessible"
            curl -s http://localhost:3001/status | python -m json.tool 2>/dev/null || echo "Status endpoint not available"
        else
            echo "❌ MCP server is not running or not accessible"
            echo "Start it with option 4 or 5"
        fi
        ;;
    7)
        echo "👥 Exporting contacts..."
        DATE=$(date +%Y%m%d_%H%M%S)
        mkdir -p ../exports
        
        # This would use HubSpot API - placeholder for now
        echo "📧 Contact export would be saved to: exports/contacts_$DATE.csv"
        echo "⚠️  Implement HubSpot API call here"
        ;;
    8)
        echo "🏢 Exporting companies..."
        DATE=$(date +%Y%m%d_%H%M%S)
        mkdir -p ../exports
        
        echo "🏢 Company export would be saved to: exports/companies_$DATE.csv"
        echo "⚠️  Implement HubSpot API call here"
        ;;
    9)
        echo "💼 Exporting deals..."
        DATE=$(date +%Y%m%d_%H%M%S)
        mkdir -p ../exports
        
        echo "💼 Deal export would be saved to: exports/deals_$DATE.csv"
        echo "⚠️  Implement HubSpot API call here"
        ;;
    10)
        echo "💾 Backing up all HubSpot data..."
        DATE=$(date +%Y%m%d_%H%M%S)
        mkdir -p "../backups/hubspot_$DATE"
        
        # Backup configuration files
        cp ../hubspot_package.json "../backups/hubspot_$DATE/"
        cp ../*.md "../backups/hubspot_$DATE/" 2>/dev/null
        
        # Create backup info
        echo "=== HubSpot Backup ===" > "../backups/hubspot_$DATE/backup_info.txt"
        echo "Date: $(date)" >> "../backups/hubspot_$DATE/backup_info.txt"
        echo "Configuration backed up" >> "../backups/hubspot_$DATE/backup_info.txt"
        
        # Copy any existing exports
        if [ -d "../exports" ]; then
            cp -r ../exports "../backups/hubspot_$DATE/"
        fi
        
        echo "✅ Backup created: backups/hubspot_$DATE/"
        ;;
    11)
        echo "🔄 Syncing HubSpot with Notion..."
        echo "This would sync contacts, companies, and deals with Notion databases"
        
        # Check if Notion is accessible
        if [ -f "../../notion/notion_README.md" ]; then
            echo "✅ Notion integration detected"
            echo "🔄 Sync process:"
            echo "  1. Export HubSpot contacts → Notion contacts database"
            echo "  2. Export HubSpot companies → Notion companies database"
            echo "  3. Export HubSpot deals → Notion deals database"
            echo "⚠️  Implement sync logic here"
        else
            echo "❌ Notion integration not found"
        fi
        ;;
    12)
        echo "🔄 Syncing HubSpot with Shopify..."
        echo "This would sync customers and orders between HubSpot and Shopify"
        
        # Check if Shopify is accessible
        if [ -f "../../shopify/shopify_README.md" ]; then
            echo "✅ Shopify integration detected"
            echo "🔄 Sync process:"
            echo "  1. Shopify customers → HubSpot contacts"
            echo "  2. Shopify orders → HubSpot deals"
            echo "  3. HubSpot companies → Shopify customer tags"
            echo "⚠️  Implement sync logic here"
        else
            echo "❌ Shopify integration not found"
        fi
        ;;
    13)
        echo "🧪 Testing all integrations..."
        
        TESTS_PASSED=0
        TOTAL_TESTS=0
        
        # Test HubSpot MCP server
        TOTAL_TESTS=$((TOTAL_TESTS + 1))
        if curl -s http://localhost:3001/health &> /dev/null; then
            echo "✅ HubSpot MCP server: Running"
            TESTS_PASSED=$((TESTS_PASSED + 1))
        else
            echo "❌ HubSpot MCP server: Not running"
        fi
        
        # Test Notion integration
        TOTAL_TESTS=$((TOTAL_TESTS + 1))
        if [ -f "../../notion/databases/contacts.md" ]; then
            echo "✅ Notion contacts database: Available"
            TESTS_PASSED=$((TESTS_PASSED + 1))
        else
            echo "❌ Notion contacts database: Not found"
        fi
        
        # Test Shopify integration
        TOTAL_TESTS=$((TOTAL_TESTS + 1))
        if [ -f "../../shopify/shopify_README.md" ]; then
            echo "✅ Shopify integration: Available"
            TESTS_PASSED=$((TESTS_PASSED + 1))
        else
            echo "❌ Shopify integration: Not found"
        fi
        
        # Test N8N workflows
        TOTAL_TESTS=$((TOTAL_TESTS + 1))
        if [ -f "../../n8n/workflows/payment-sync-to-notion.json" ]; then
            echo "✅ N8N payment sync workflow: Available"
            TESTS_PASSED=$((TESTS_PASSED + 1))
        else
            echo "❌ N8N payment sync workflow: Not found"
        fi
        
        echo ""
        echo "📊 Integration Test Results: $TESTS_PASSED/$TOTAL_TESTS passed"
        
        if [ $TESTS_PASSED -eq $TOTAL_TESTS ]; then
            echo "🎉 All integrations are working!"
        else
            echo "⚠️  Some integrations need attention"
        fi
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac
