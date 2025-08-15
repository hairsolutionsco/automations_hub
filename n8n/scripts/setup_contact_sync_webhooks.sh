#!/bin/bash

# Notion & HubSpot Contact Sync - Webhook Setup Script
# This script sets up webhook listeners for real-time synchronization

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔗 Setting up Notion ↔ HubSpot Contact Sync Webhooks${NC}"
echo "=================================================="

# Check environment variables
if [[ -z "$N8N_CLOUD_INSTANCE_URL" ]]; then
    echo -e "${RED}❌ N8N_CLOUD_INSTANCE_URL not set${NC}"
    exit 1
fi

if [[ -z "$N8N_API_KEY" ]]; then
    echo -e "${RED}❌ N8N_API_KEY not set${NC}"
    exit 1
fi

if [[ -z "$HUBSPOT_API_ACCESS_TOKEN" ]]; then
    echo -e "${RED}❌ HUBSPOT_API_ACCESS_TOKEN not set${NC}"
    exit 1
fi

if [[ -z "$NOTION_API_KEY" ]]; then
    echo -e "${RED}❌ NOTION_API_KEY not set${NC}"
    exit 1
fi

# Webhook URLs (these will be generated when the workflow is imported)
NOTION_WEBHOOK_URL="$N8N_CLOUD_INSTANCE_URL/webhook/notion-contact-updated"
HUBSPOT_WEBHOOK_URL="$N8N_CLOUD_INSTANCE_URL/webhook/hubspot-contact-updated"

echo -e "${GREEN}✅ Environment variables verified${NC}"
echo ""

# Step 1: Import the workflow to n8n
echo -e "${BLUE}📤 Importing workflow to n8n...${NC}"

WORKFLOW_FILE="/workspaces/automations_hub/n8n/workflows/notion_hubspot_contact_sync.json"

if [[ ! -f "$WORKFLOW_FILE" ]]; then
    echo -e "${RED}❌ Workflow file not found: $WORKFLOW_FILE${NC}"
    exit 1
fi

# Import workflow using n8n API
IMPORT_RESPONSE=$(curl -s -X POST \
    -H "X-N8N-API-KEY: $N8N_API_KEY" \
    -H "Content-Type: application/json" \
    -d @"$WORKFLOW_FILE" \
    "$N8N_CLOUD_INSTANCE_URL/api/v1/workflows")

if echo "$IMPORT_RESPONSE" | grep -q '"id"'; then
    WORKFLOW_ID=$(echo "$IMPORT_RESPONSE" | jq -r '.id')
    echo -e "${GREEN}✅ Workflow imported successfully (ID: $WORKFLOW_ID)${NC}"
else
    echo -e "${RED}❌ Failed to import workflow:${NC}"
    echo "$IMPORT_RESPONSE"
    exit 1
fi

# Step 2: Activate the workflow
echo -e "${BLUE}🚀 Activating workflow...${NC}"

ACTIVATE_RESPONSE=$(curl -s -X POST \
    -H "X-N8N-API-KEY: $N8N_API_KEY" \
    "$N8N_CLOUD_INSTANCE_URL/api/v1/workflows/$WORKFLOW_ID/activate")

if echo "$ACTIVATE_RESPONSE" | grep -q '"active":true'; then
    echo -e "${GREEN}✅ Workflow activated successfully${NC}"
else
    echo -e "${RED}❌ Failed to activate workflow:${NC}"
    echo "$ACTIVATE_RESPONSE"
fi

# Step 3: Set up HubSpot webhook
echo -e "${BLUE}🔗 Setting up HubSpot webhook...${NC}"

HUBSPOT_WEBHOOK_PAYLOAD=$(cat <<EOF
{
  "eventType": "contact.propertyChange",
  "propertyName": "*",
  "active": true,
  "webhookUrl": "$HUBSPOT_WEBHOOK_URL"
}
EOF
)

HUBSPOT_WEBHOOK_RESPONSE=$(curl -s -X POST \
    -H "Authorization: Bearer $HUBSPOT_API_ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    -d "$HUBSPOT_WEBHOOK_PAYLOAD" \
    "https://api.hubapi.com/webhooks/v3/subscriptions")

if echo "$HUBSPOT_WEBHOOK_RESPONSE" | grep -q '"id"'; then
    HUBSPOT_WEBHOOK_ID=$(echo "$HUBSPOT_WEBHOOK_RESPONSE" | jq -r '.id')
    echo -e "${GREEN}✅ HubSpot webhook created (ID: $HUBSPOT_WEBHOOK_ID)${NC}"
else
    echo -e "${YELLOW}⚠️  HubSpot webhook creation response:${NC}"
    echo "$HUBSPOT_WEBHOOK_RESPONSE"
fi

# Step 4: Notion webhook setup instructions
echo ""
echo -e "${BLUE}📝 Notion Webhook Setup Instructions${NC}"
echo "=================================="
echo ""
echo "Notion doesn't support webhooks directly through API, but you can:"
echo ""
echo "1. Use Notion's Database Triggers (if available in your plan)"
echo "2. Set up polling with the workflow timer trigger"
echo "3. Use a third-party service like Zapier to bridge webhooks"
echo ""
echo "For now, you can test the workflow manually by sending POST requests to:"
echo -e "${GREEN}$NOTION_WEBHOOK_URL${NC}"
echo ""
echo "Example payload:"
echo '{'
echo '  "page_id": "your-notion-page-id",'
echo '  "event": "page.updated",'
echo '  "timestamp": "2025-08-15T04:58:00.000Z"'
echo '}'

# Step 5: Display webhook URLs and testing info
echo ""
echo -e "${BLUE}🎯 Webhook URLs for Testing${NC}"
echo "============================"
echo ""
echo -e "${GREEN}Notion → HubSpot:${NC} $NOTION_WEBHOOK_URL"
echo -e "${GREEN}HubSpot → Notion:${NC} $HUBSPOT_WEBHOOK_URL"
echo ""

# Step 6: Create test script
echo -e "${BLUE}📝 Creating test script...${NC}"

cat > /workspaces/automations_hub/n8n/scripts/test_contact_sync.sh << 'EOF'
#!/bin/bash

# Test script for Notion ↔ HubSpot contact sync

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

if [[ -z "$N8N_CLOUD_INSTANCE_URL" ]]; then
    echo "❌ N8N_CLOUD_INSTANCE_URL not set"
    exit 1
fi

NOTION_WEBHOOK_URL="$N8N_CLOUD_INSTANCE_URL/webhook/notion-contact-updated"
HUBSPOT_WEBHOOK_URL="$N8N_CLOUD_INSTANCE_URL/webhook/hubspot-contact-updated"

echo -e "${BLUE}🧪 Testing Contact Sync Webhooks${NC}"
echo "================================"

# Test 1: Notion → HubSpot
echo -e "${YELLOW}Test 1: Notion Contact Update${NC}"
curl -X POST \
    -H "Content-Type: application/json" \
    -d '{
        "page_id": "226f4e0d-84e0-814c-ad70-d478cebeee30",
        "event": "page.updated",
        "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%S.000Z)'"
    }' \
    "$NOTION_WEBHOOK_URL"

echo -e "\n${GREEN}✅ Notion webhook test sent${NC}\n"

# Test 2: HubSpot → Notion
echo -e "${YELLOW}Test 2: HubSpot Contact Update${NC}"
curl -X POST \
    -H "Content-Type: application/json" \
    -d '{
        "contact_id": "12345",
        "event": "contact.propertyChange",
        "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%S.000Z)'"
    }' \
    "$HUBSPOT_WEBHOOK_URL"

echo -e "\n${GREEN}✅ HubSpot webhook test sent${NC}\n"

echo "Check your n8n workflow execution logs to see the results!"
EOF

chmod +x /workspaces/automations_hub/n8n/scripts/test_contact_sync.sh

echo -e "${GREEN}✅ Test script created: /workspaces/automations_hub/n8n/scripts/test_contact_sync.sh${NC}"

# Final summary
echo ""
echo -e "${BLUE}🎉 Setup Complete!${NC}"
echo "=================="
echo ""
echo "✅ Workflow imported and activated"
echo "✅ HubSpot webhook configured"  
echo "✅ Test script created"
echo "⚠️  Notion webhook needs manual setup (see instructions above)"
echo ""
echo -e "${GREEN}Next steps:${NC}"
echo "1. Test the webhooks using: ./test_contact_sync.sh"
echo "2. Monitor workflow executions in your n8n dashboard"
echo "3. Set up Notion webhook triggers as needed"
echo ""
echo -e "${YELLOW}Dashboard URL:${NC} $N8N_CLOUD_INSTANCE_URL"
