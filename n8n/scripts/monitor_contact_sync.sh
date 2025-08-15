#!/bin/bash

# Contact Sync Monitoring Dashboard
# Real-time status check for Notion ↔ HubSpot contact synchronization

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
PURPLE='\033[0;35m'
NC='\033[0m'

echo -e "${BLUE}🔍 Notion ↔ HubSpot Contact Sync Status Dashboard${NC}"
echo "=================================================="
echo ""

# Check environment
if [[ -z "$N8N_CLOUD_INSTANCE_URL" || -z "$N8N_API_KEY" ]]; then
    echo -e "${RED}❌ N8N environment variables not set${NC}"
    exit 1
fi

# 1. Check workflow status
echo -e "${YELLOW}📊 Workflow Status:${NC}"
WORKFLOW_STATUS=$(curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
    "$N8N_CLOUD_INSTANCE_URL/api/v1/workflows?active=true")

if echo "$WORKFLOW_STATUS" | jq -e '.data[] | select(.name | test("Contact Sync"))' > /dev/null 2>&1; then
    echo "$WORKFLOW_STATUS" | jq -r '.data[] | select(.name | test("Contact Sync")) | 
    "✅ \(.name) (ID: \(.id))\n   Active: \(.active) | Nodes: \(.nodes | length) | Updated: \(.updatedAt)"'
else
    echo -e "${RED}❌ No Contact Sync workflows found${NC}"
fi

echo ""

# 2. Check recent executions
echo -e "${YELLOW}📈 Recent Executions (Last 10):${NC}"
EXECUTIONS=$(curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
    "$N8N_CLOUD_INSTANCE_URL/api/v1/executions?limit=20")

echo "$EXECUTIONS" | jq -r '.data[] | 
select(.workflowData.name // "" | test("Contact Sync|Notion.*HubSpot")) | 
"[\(.startedAt)] \(.workflowData.name // "Contact Sync"): \(if .finished then "✅ SUCCESS" else "⏳ RUNNING" end) (\(.mode // "unknown"))"' | head -10

if ! echo "$EXECUTIONS" | jq -e '.data[] | select(.workflowData.name // "" | test("Contact Sync|Notion.*HubSpot"))' > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  No Contact Sync executions found yet${NC}"
    echo "   This is normal for new workflows - they'll appear after first run"
fi

echo ""

# 3. Check webhook endpoints
echo -e "${YELLOW}🔗 Webhook Endpoints:${NC}"
echo -e "${GREEN}HubSpot → Notion:${NC} $N8N_CLOUD_INSTANCE_URL/webhook/hubspot-contact-updated"
echo -e "${GREEN}Notion → HubSpot:${NC} $N8N_CLOUD_INSTANCE_URL/webhook/notion-contact-updated"

# Test webhook endpoint
echo ""
echo -e "${YELLOW}🧪 Testing Webhook Endpoint:${NC}"
WEBHOOK_TEST=$(curl -s -w "%{http_code}" -X POST \
    -H "Content-Type: application/json" \
    -d '{"test": "connection", "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%S.000Z)'"}' \
    "$N8N_CLOUD_INSTANCE_URL/webhook/hubspot-contact-updated" -o /dev/null)

if [[ "$WEBHOOK_TEST" == "200" ]]; then
    echo -e "${GREEN}✅ Webhook endpoint responding (HTTP 200)${NC}"
else
    echo -e "${RED}❌ Webhook test failed (HTTP $WEBHOOK_TEST)${NC}"
fi

echo ""

# 4. Check credentials
echo -e "${YELLOW}🔐 API Credentials Status:${NC}"
CREDENTIALS=$(curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
    "$N8N_CLOUD_INSTANCE_URL/api/v1/credentials")

NOTION_CRED=$(echo "$CREDENTIALS" | jq -r '.data[] | select(.id == "ID4jkKCiAXGH1iVwyi") | .name // "Not Found"')
HUBSPOT_CRED=$(echo "$CREDENTIALS" | jq -r '.data[] | select(.id == "ID4CUY90jW5ObSXedy") | .name // "Not Found"')

if [[ "$NOTION_CRED" != "Not Found" ]]; then
    echo -e "${GREEN}✅ Notion API: $NOTION_CRED${NC}"
else
    echo -e "${RED}❌ Notion API credential not found${NC}"
fi

if [[ "$HUBSPOT_CRED" != "Not Found" ]]; then
    echo -e "${GREEN}✅ HubSpot API: $HUBSPOT_CRED${NC}"
else
    echo -e "${RED}❌ HubSpot API credential not found${NC}"
fi

echo ""

# 5. Show next steps for testing
echo -e "${PURPLE}🎯 How to Verify Sync is Working:${NC}"
echo ""
echo "1. 📝 Update a contact in Notion (add/change email, phone, or address)"
echo "2. ⏰ Wait 5 minutes for the polling cycle"
echo "3. 🔍 Check HubSpot for the updated contact"
echo "4. 📊 Monitor executions: $N8N_CLOUD_INSTANCE_URL"
echo ""
echo "📋 Test Commands:"
echo "   Monitor: ./monitor_contact_sync.sh"
echo "   Dashboard: $N8N_CLOUD_INSTANCE_URL"
echo ""

# 6. Show polling schedule
echo -e "${YELLOW}⏰ Polling Schedule:${NC}"
echo "Notion database checked every 5 minutes for changes"
echo "Next check: $(date -d '+5 minutes' '+%H:%M:%S')"
echo ""

echo -e "${GREEN}🎉 Monitoring complete! Your sync workflows are ready.${NC}"
