#!/bin/bash

# Quick Start HubSpot MCP Server
# Provides immediate access to full HubSpot platform via MCP

echo "🚀 Starting HubSpot MCP Server with Full Access..."
echo "=================================================="

# Change to hubspot directory
cd /workspaces/automations_hub/hubspot

# Load environment variables
source .env 2>/dev/null || true

# Check if authentication is configured
if [ ! -f "hubspot.config.yml" ]; then
    echo "❌ HubSpot not authenticated. Run ./hubspot_mcp_manager.sh and choose option 6"
    exit 1
fi

if [ -z "$PRIVATE_APP_ACCESS_TOKEN" ]; then
    echo "❌ Access token not configured. Check .env file"
    exit 1
fi

echo "✅ Authentication configured"
echo "✅ Environment variables loaded"
echo "🌐 Server will be available at: http://127.0.0.1:3001"
echo ""
echo "📋 Full HubSpot Access Available:"
echo "  🔹 CRM (Contacts, Companies, Deals, Tickets)"
echo "  🔹 CMS (Pages, Templates, Modules)"
echo "  🔹 Design Manager (Assets, Files, Templates)"
echo "  🔹 Blog (Posts, Authors, Topics)"
echo "  🔹 Marketing (Forms, Lists, Campaigns)"
echo "  🔹 Sales (Pipelines, Quotes, Sequences)"
echo "  🔹 Automation (Workflows, Properties)"
echo ""
echo "🎯 Starting server..."

# Start the MCP server
npm run mcp:start
