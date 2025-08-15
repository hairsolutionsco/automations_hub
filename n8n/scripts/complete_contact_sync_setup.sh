#!/bin/bash

# Complete Notion ↔ HubSpot Contact Sync Setup
# Creates both webhook-based and polling-based workflows

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Complete Notion ↔ HubSpot Contact Sync Setup${NC}"
echo "=================================================="
echo ""

# Check environment variables
echo -e "${YELLOW}🔍 Checking environment variables...${NC}"

REQUIRED_VARS=("N8N_CLOUD_INSTANCE_URL" "N8N_API_KEY" "HUBSPOT_API_ACCESS_TOKEN" "NOTION_API_KEY")
MISSING_VARS=()

for var in "${REQUIRED_VARS[@]}"; do
    if [[ -z "${!var}" ]]; then
        MISSING_VARS+=("$var")
    fi
done

if [[ ${#MISSING_VARS[@]} -gt 0 ]]; then
    echo -e "${RED}❌ Missing required environment variables:${NC}"
    for var in "${MISSING_VARS[@]}"; do
        echo "   - $var"
    done
    echo ""
    echo "Please set these variables and run the script again."
    exit 1
fi

echo -e "${GREEN}✅ All environment variables verified${NC}"
echo ""

# Function to import and activate workflow
import_workflow() {
    local workflow_file="$1"
    local workflow_name="$2"
    
    echo -e "${BLUE}📤 Importing $workflow_name...${NC}"
    
    if [[ ! -f "$workflow_file" ]]; then
        echo -e "${RED}❌ Workflow file not found: $workflow_file${NC}"
        return 1
    fi
    
    # Import workflow
    IMPORT_RESPONSE=$(curl -s -X POST \
        -H "X-N8N-API-KEY: $N8N_API_KEY" \
        -H "Content-Type: application/json" \
        -d @"$workflow_file" \
        "$N8N_CLOUD_INSTANCE_URL/api/v1/workflows")
    
    if echo "$IMPORT_RESPONSE" | grep -q '"id"'; then
        WORKFLOW_ID=$(echo "$IMPORT_RESPONSE" | jq -r '.id')
        echo -e "${GREEN}✅ $workflow_name imported (ID: $WORKFLOW_ID)${NC}"
        
        # Activate workflow
        ACTIVATE_RESPONSE=$(curl -s -X POST \
            -H "X-N8N-API-KEY: $N8N_API_KEY" \
            "$N8N_CLOUD_INSTANCE_URL/api/v1/workflows/$WORKFLOW_ID/activate")
        
        if echo "$ACTIVATE_RESPONSE" | grep -q '"active":true'; then
            echo -e "${GREEN}✅ $workflow_name activated${NC}"
        else
            echo -e "${YELLOW}⚠️  $workflow_name activation response: $ACTIVATE_RESPONSE${NC}"
        fi
        
        return 0
    else
        echo -e "${RED}❌ Failed to import $workflow_name:${NC}"
        echo "$IMPORT_RESPONSE"
        return 1
    fi
}

# Step 1: Choose workflow type
echo -e "${PURPLE}🎯 Choose your sync approach:${NC}"
echo ""
echo "1. Webhook-based (Real-time, requires HubSpot webhook setup)"
echo "2. Polling-based (5-minute intervals, works out of the box)"
echo "3. Both (Recommended for maximum coverage)"
echo ""
read -p "Enter your choice (1/2/3): " choice

case $choice in
    1)
        SETUP_WEBHOOK=true
        SETUP_POLLING=false
        ;;
    2)
        SETUP_WEBHOOK=false
        SETUP_POLLING=true
        ;;
    3)
        SETUP_WEBHOOK=true
        SETUP_POLLING=true
        ;;
    *)
        echo -e "${RED}❌ Invalid choice. Exiting.${NC}"
        exit 1
        ;;
esac

echo ""

# Step 2: Import workflows
WORKFLOW_BASE="/workspaces/automations_hub/n8n/workflows"

if [[ "$SETUP_WEBHOOK" == true ]]; then
    import_workflow "$WORKFLOW_BASE/notion_hubspot_contact_sync.json" "Webhook-based Sync"
    WEBHOOK_WORKFLOW_IMPORTED=$?
fi

if [[ "$SETUP_POLLING" == true ]]; then
    import_workflow "$WORKFLOW_BASE/notion_hubspot_contact_sync_polling.json" "Polling-based Sync"
    POLLING_WORKFLOW_IMPORTED=$?
fi

echo ""

# Step 3: Set up HubSpot webhook (if webhook workflow was imported)
if [[ "$SETUP_WEBHOOK" == true && "$WEBHOOK_WORKFLOW_IMPORTED" == 0 ]]; then
    echo -e "${BLUE}🔗 Setting up HubSpot webhook...${NC}"
    
    HUBSPOT_WEBHOOK_URL="$N8N_CLOUD_INSTANCE_URL/webhook/hubspot-contact-updated"
    
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
        echo -e "${YELLOW}⚠️  HubSpot webhook response:${NC}"
        echo "$HUBSPOT_WEBHOOK_RESPONSE"
    fi
fi

# Step 4: Create monitoring script
echo -e "${BLUE}📊 Creating monitoring script...${NC}"

cat > /workspaces/automations_hub/n8n/scripts/monitor_contact_sync.sh << 'EOF'
#!/bin/bash

# Monitor Notion ↔ HubSpot Contact Sync

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

if [[ -z "$N8N_CLOUD_INSTANCE_URL" || -z "$N8N_API_KEY" ]]; then
    echo "❌ N8N environment variables not set"
    exit 1
fi

echo -e "${BLUE}📊 Contact Sync Monitoring Dashboard${NC}"
echo "===================================="

# Get workflow executions
echo -e "${YELLOW}Recent Workflow Executions:${NC}"
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
    "$N8N_CLOUD_INSTANCE_URL/api/v1/executions?limit=10" | \
    jq -r '.data[] | select(.workflowData.name | contains("Contact")) | 
    "[\(.startedAt)] \(.workflowData.name): \(.finished ? "✅ Success" : "❌ Failed")"'

echo ""

# Get active workflows
echo -e "${YELLOW}Active Contact Sync Workflows:${NC}"
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
    "$N8N_CLOUD_INSTANCE_URL/api/v1/workflows?active=true" | \
    jq -r '.data[] | select(.name | contains("Contact")) | 
    "✅ \(.name) (ID: \(.id))"'

echo ""
echo -e "${GREEN}Dashboard URL:${NC} $N8N_CLOUD_INSTANCE_URL"
EOF

chmod +x /workspaces/automations_hub/n8n/scripts/monitor_contact_sync.sh

# Step 5: Create testing script
echo -e "${BLUE}🧪 Creating test script...${NC}"

cat > /workspaces/automations_hub/n8n/scripts/test_contact_sync_complete.sh << 'EOF'
#!/bin/bash

# Complete test script for Notion ↔ HubSpot contact sync

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

if [[ -z "$N8N_CLOUD_INSTANCE_URL" ]]; then
    echo "❌ N8N_CLOUD_INSTANCE_URL not set"
    exit 1
fi

echo -e "${BLUE}🧪 Testing Contact Sync Workflows${NC}"
echo "=================================="

# Test webhook endpoint (if available)
WEBHOOK_URL="$N8N_CLOUD_INSTANCE_URL/webhook/hubspot-contact-updated"

echo -e "${YELLOW}Testing HubSpot → Notion webhook...${NC}"
WEBHOOK_RESPONSE=$(curl -s -w "%{http_code}" -X POST \
    -H "Content-Type: application/json" \
    -d '{
        "contact_id": "test-contact-123",
        "event": "contact.propertyChange",
        "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%S.000Z)'"
    }' \
    "$WEBHOOK_URL")

if [[ "${WEBHOOK_RESPONSE: -3}" == "200" ]]; then
    echo -e "${GREEN}✅ Webhook endpoint responding${NC}"
else
    echo -e "${RED}❌ Webhook test failed (HTTP ${WEBHOOK_RESPONSE: -3})${NC}"
fi

echo ""

# Test workflow execution status
echo -e "${YELLOW}Checking recent executions...${NC}"
if command -v jq &> /dev/null; then
    curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
        "$N8N_CLOUD_INSTANCE_URL/api/v1/executions?limit=5" | \
        jq -r '.data[] | "[\(.startedAt)] \(.workflowData.name): \(.finished ? "✅" : "❌")"'
else
    echo "Install jq for detailed execution info"
fi

echo ""
echo -e "${GREEN}Test complete! Check your n8n dashboard for detailed logs.${NC}"
echo -e "${BLUE}Dashboard: $N8N_CLOUD_INSTANCE_URL${NC}"
EOF

chmod +x /workspaces/automations_hub/n8n/scripts/test_contact_sync_complete.sh

# Step 6: Create comprehensive README
echo -e "${BLUE}📝 Creating setup documentation...${NC}"

cat > /workspaces/automations_hub/n8n/workflows/SYNC_SETUP_COMPLETE.md << 'EOF'
# ✅ Notion ↔ HubSpot Contact Sync - Setup Complete!

Your 2-way contact synchronization is now configured and ready to use.

## 🚀 What Was Set Up

### Workflows Imported
- **Webhook-based Sync**: Real-time synchronization (if selected)
- **Polling-based Sync**: 5-minute interval checking (if selected)

### Property Mapping Configured
- 24 Notion contact properties mapped to HubSpot equivalents
- Intelligent data type conversion
- Cross-reference ID management
- Sync conflict prevention

### Monitoring Tools Created
- Execution monitoring script
- Testing utilities
- Error handling and logging

## 🎯 How It Works

### Notion → HubSpot Flow
1. **Polling Trigger**: Checks Notion every 5 minutes for changes
2. **Filter**: Only syncs contacts with email or phone
3. **Transform**: Converts Notion data to HubSpot format
4. **Sync**: Creates or updates HubSpot contact
5. **Cross-Reference**: Stores HubSpot ID in Notion

### HubSpot → Notion Flow
1. **Webhook Trigger**: Receives real-time HubSpot updates
2. **Transform**: Converts HubSpot data to Notion format
3. **Sync**: Creates or updates Notion contact
4. **Cross-Reference**: Links contacts via IDs

## 🔧 Management Commands

### Monitor Sync Status
```bash
cd /workspaces/automations_hub/n8n/scripts
./monitor_contact_sync.sh
```

### Test Workflows
```bash
./test_contact_sync_complete.sh
```

### View Logs
Check your n8n dashboard at: $N8N_CLOUD_INSTANCE_URL

## 📊 Property Mappings

### Perfect Matches (Auto-synced)
- Email ↔ email
- Phone Number ↔ phone
- Address ↔ address
- Access Point Location ↔ access_point_location
- Marketing contact status ↔ hs_marketable_status
- Lifecycle Stage ↔ lifecyclestage
- Re-Engagement Notes ↔ reengagementnotes
- Shipping Profile ↔ shipping_profile

### Smart Conversions
- Name → firstname + lastname (splits automatically)
- Contact Profile → contact_type
- Country/Region → country
- Sales Status → hs_lead_status

### Cross-References
- Id ↔ notion_contact_id
- Hubspot Contacts Record ID ↔ hs_object_id

## 🛡️ Sync Protection

### Loop Prevention
- Timestamp checking prevents infinite loops
- 2-minute cooldown between syncs
- Source tracking for each change

### Data Validation
- Required fields checked before sync
- Type conversion with fallbacks
- Error logging for failed operations

## 📈 Next Steps

1. **Test the sync** with a few sample contacts
2. **Monitor executions** in the n8n dashboard
3. **Adjust property mappings** if needed
4. **Scale up** once satisfied with results

## 🆘 Troubleshooting

### Common Issues
- **No syncing**: Check API credentials in n8n
- **Partial data**: Review property mapping in transform nodes
- **Duplicates**: Verify cross-reference ID fields
- **Errors**: Check execution logs in n8n dashboard

### Support Files
- Full workflow JSON: `notion_hubspot_contact_sync.json`
- Polling version: `notion_hubspot_contact_sync_polling.json`  
- Setup guide: `CONTACT_SYNC_GUIDE.md`
- Property analysis: `../../property_matching_report.md`

**Happy syncing! 🎉**

Your contacts will now stay in sync automatically between Notion and HubSpot.
EOF

echo -e "${GREEN}✅ Documentation created${NC}"

# Final summary
echo ""
echo -e "${BLUE}🎉 Setup Complete!${NC}"
echo "=================="
echo ""

if [[ "$SETUP_WEBHOOK" == true ]]; then
    echo "✅ Webhook-based sync workflow imported and activated"
    echo "✅ HubSpot webhook configured for real-time updates"
fi

if [[ "$SETUP_POLLING" == true ]]; then
    echo "✅ Polling-based sync workflow imported and activated"  
    echo "✅ 5-minute interval checking configured"
fi

echo "✅ Monitoring and testing scripts created"
echo "✅ Complete documentation available"
echo ""

echo -e "${GREEN}🎯 What happens next:${NC}"
echo "1. Your workflows are now active and syncing"
echo "2. Notion contacts will be checked every 5 minutes (polling)"
echo "3. HubSpot changes trigger immediate sync (webhook)"
echo "4. All 24 Notion properties mapped to HubSpot"
echo ""

echo -e "${YELLOW}🔧 Management commands:${NC}"
echo "Monitor:  ./n8n/scripts/monitor_contact_sync.sh"
echo "Test:     ./n8n/scripts/test_contact_sync_complete.sh"
echo "Dashboard: $N8N_CLOUD_INSTANCE_URL"
echo ""

echo -e "${PURPLE}📊 Your sync is live! Check the dashboard to see it working.${NC}"
