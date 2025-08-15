#!/bin/bash

# 🚀 Quick Setup Script for Deals Sync
# This script demonstrates the complete process for creating a Deals sync workflow

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
PURPLE='\033[0;35m'
NC='\033[0m'

echo -e "${BLUE}🔄 Setting up Notion ↔ HubSpot Deals Sync${NC}"
echo "=========================================="
echo ""

# Prompt for Notion database ID
echo -e "${YELLOW}📋 Step 1: Database Configuration${NC}"
read -p "Enter your Notion Deals database ID: " DEALS_DB_ID

if [[ -z "$DEALS_DB_ID" ]]; then
    echo -e "${RED}❌ Database ID is required${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Using database ID: $DEALS_DB_ID${NC}"
echo ""

# Step 1: Copy and modify property matcher
echo -e "${YELLOW}📋 Step 2: Creating Property Analysis Script${NC}"
cp /workspaces/automations_hub/property_matcher.py /workspaces/automations_hub/deals_property_matcher.py

# Update the database ID in the script
sed -i "s/226f4e0d-84e0-814c-ad70-d478cebeee30/$DEALS_DB_ID/g" /workspaces/automations_hub/deals_property_matcher.py

# Update object references
sed -i 's/contacts/deals/g' /workspaces/automations_hub/deals_property_matcher.py
sed -i 's/Contact/Deal/g' /workspaces/automations_hub/deals_property_matcher.py

echo -e "${GREEN}✅ Created deals_property_matcher.py${NC}"

# Step 2: Run property analysis
echo -e "${YELLOW}📋 Step 3: Analyzing Properties${NC}"
cd /workspaces/automations_hub
python deals_property_matcher.py

if [[ $? -eq 0 ]]; then
    echo -e "${GREEN}✅ Property analysis complete${NC}"
    echo "   Generated: notion_hubspot_deals_property_mapping.md"
else
    echo -e "${RED}❌ Property analysis failed${NC}"
    exit 1
fi

# Step 3: Copy workflow files
echo -e "${YELLOW}📋 Step 4: Creating Workflow Files${NC}"
cd n8n/workflows

# Copy webhook workflow
cp notion_hubspot_contact_sync.json notion_hubspot_deals_sync.json

# Copy polling workflow
cp notion_hubspot_contact_sync_polling.json notion_hubspot_deals_sync_polling.json

# Update workflow names and database IDs
sed -i 's/Contact Sync/Deals Sync/g' notion_hubspot_deals_sync.json
sed -i 's/Contact Sync/Deals Sync/g' notion_hubspot_deals_sync_polling.json
sed -i "s/226f4e0d-84e0-814c-ad70-d478cebeee30/$DEALS_DB_ID/g" notion_hubspot_deals_sync.json
sed -i "s/226f4e0d-84e0-814c-ad70-d478cebeee30/$DEALS_DB_ID/g" notion_hubspot_deals_sync_polling.json

# Update HubSpot object type
sed -i 's/"resource": "contact"/"resource": "deal"/g' notion_hubspot_deals_sync.json
sed -i 's/"resource": "contact"/"resource": "deal"/g' notion_hubspot_deals_sync_polling.json

# Update webhook paths
sed -i 's/hubspot-contact-updated/hubspot-deal-updated/g' notion_hubspot_deals_sync.json
sed -i 's/notion-contact-updated/notion-deal-updated/g' notion_hubspot_deals_sync.json

echo -e "${GREEN}✅ Created workflow files${NC}"

# Step 4: Create monitoring scripts
echo -e "${YELLOW}📋 Step 5: Creating Monitoring Scripts${NC}"
cd ../scripts

# Copy monitoring script
cp monitor_contact_sync.sh monitor_deals_sync.sh
sed -i 's/Contact Sync/Deals Sync/g' monitor_deals_sync.sh
sed -i 's/contact-updated/deal-updated/g' monitor_deals_sync.sh

# Copy testing script
cp test_contact_sync.sh test_deals_sync.sh
sed -i 's/Contact Sync/Deals Sync/g' test_deals_sync.sh
sed -i 's/contact.propertyChange/deal.propertyChange/g' test_deals_sync.sh
sed -i 's/hubspot-contact-updated/hubspot-deal-updated/g' test_deals_sync.sh
sed -i 's/"propertyName": "email"/"propertyName": "dealname"/g' test_deals_sync.sh
sed -i 's/"propertyValue": "test@example.com"/"propertyValue": "Test Deal"/g' test_deals_sync.sh

chmod +x monitor_deals_sync.sh
chmod +x test_deals_sync.sh

echo -e "${GREEN}✅ Created monitoring scripts${NC}"

# Step 5: Import workflows (if n8n credentials are available)
echo -e "${YELLOW}📋 Step 6: Workflow Import${NC}"
cd ..

if [[ -n "$N8N_API_KEY" && -n "$N8N_CLOUD_INSTANCE_URL" ]]; then
    echo "Importing workflows to n8n..."
    
    # Import webhook workflow
    WEBHOOK_RESULT=$(curl -s -w "%{http_code}" -X POST \
        -H "X-N8N-API-KEY: $N8N_API_KEY" \
        -H "Content-Type: application/json" \
        -d @workflows/notion_hubspot_deals_sync.json \
        "$N8N_CLOUD_INSTANCE_URL/api/v1/workflows/import" \
        -o webhook_import.json)
    
    # Import polling workflow
    POLLING_RESULT=$(curl -s -w "%{http_code}" -X POST \
        -H "X-N8N-API-KEY: $N8N_API_KEY" \
        -H "Content-Type: application/json" \
        -d @workflows/notion_hubspot_deals_sync_polling.json \
        "$N8N_CLOUD_INSTANCE_URL/api/v1/workflows/import" \
        -o polling_import.json)
    
    if [[ "$WEBHOOK_RESULT" == "200" ]] && [[ "$POLLING_RESULT" == "200" ]]; then
        echo -e "${GREEN}✅ Workflows imported successfully${NC}"
        
        # Get workflow IDs
        WEBHOOK_ID=$(cat webhook_import.json | jq -r '.data.id // "unknown"')
        POLLING_ID=$(cat polling_import.json | jq -r '.data.id // "unknown"')
        
        echo "   Webhook Workflow ID: $WEBHOOK_ID"
        echo "   Polling Workflow ID: $POLLING_ID"
    else
        echo -e "${RED}❌ Workflow import failed${NC}"
        echo "   Webhook: HTTP $WEBHOOK_RESULT"
        echo "   Polling: HTTP $POLLING_RESULT"
    fi
    
    # Cleanup
    rm -f webhook_import.json polling_import.json
else
    echo -e "${YELLOW}⚠️  N8N credentials not set - import workflows manually${NC}"
    echo "   1. Go to: $N8N_CLOUD_INSTANCE_URL"
    echo "   2. Import: workflows/notion_hubspot_deals_sync.json"
    echo "   3. Import: workflows/notion_hubspot_deals_sync_polling.json"
fi

echo ""

# Step 6: Generate summary
echo -e "${PURPLE}📊 Setup Complete!${NC}"
echo "======================"
echo ""
echo -e "${GREEN}✅ Created Files:${NC}"
echo "   📄 deals_property_matcher.py"
echo "   📄 notion_hubspot_deals_property_mapping.md"
echo "   📄 workflows/notion_hubspot_deals_sync.json"
echo "   📄 workflows/notion_hubspot_deals_sync_polling.json"
echo "   📄 scripts/monitor_deals_sync.sh"
echo "   📄 scripts/test_deals_sync.sh"
echo ""
echo -e "${YELLOW}🎯 Next Steps:${NC}"
echo "   1. Review property mapping: notion_hubspot_deals_property_mapping.md"
echo "   2. Customize property transformations in workflow files"
echo "   3. Test the setup: ./scripts/test_deals_sync.sh"
echo "   4. Monitor sync: ./scripts/monitor_deals_sync.sh"
echo ""
echo -e "${BLUE}📋 Manual Steps Still Needed:${NC}"
echo "   • Configure credential IDs in n8n workflows"
echo "   • Activate workflows in n8n dashboard"
echo "   • Test with real deal data"
echo ""

echo -e "${GREEN}🎉 Deals sync setup ready!${NC}"
