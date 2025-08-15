# 🔄 Complete Guide: Building Notion ↔ HubSpot Sync Workflows for Any Object

## 📋 Overview

This guide explains how to replicate the Contact sync workflow for other objects like Deals, Companies, Orders, etc. You'll follow the same proven pattern that successfully created your Contact sync system.

## 🎯 What You'll Build

Each new sync workflow will include:
- **Property Analysis & Mapping** (Python script)
- **2-Way Sync Workflows** (n8n JSON files)
- **Monitoring & Testing Scripts** (Bash scripts)
- **Documentation** (Markdown reports)

## 📁 Template Files Location

All template files are located in `/workspaces/automations_hub/n8n/`:

### Core Templates:
- `📄 property_matcher.py` - Property analysis script
- `📄 workflows/notion_hubspot_contact_sync.json` - Webhook workflow
- `📄 workflows/notion_hubspot_contact_sync_polling.json` - Polling workflow
- `📄 scripts/monitor_contact_sync.sh` - Monitoring script
- `📄 scripts/test_contact_sync.sh` - Testing script

### Generated Files:
- `📄 CONTACT_SYNC_VERIFICATION.md` - Status documentation

---

## 🚀 Step-by-Step Implementation

### Step 1: Property Analysis Setup

#### 1.1 Copy the Property Matcher Script
```bash
# Copy the base template
cp /workspaces/automations_hub/property_matcher.py /workspaces/automations_hub/[OBJECT]_property_matcher.py

# Example for Deals:
cp /workspaces/automations_hub/property_matcher.py /workspaces/automations_hub/deals_property_matcher.py
```

#### 1.2 Modify the Script for Your Object

**Required Changes in `[OBJECT]_property_matcher.py`:**

1. **Update Database Information:**
```python
# CHANGE THIS: Replace with your Notion database ID
NOTION_DATABASE_ID = "YOUR_NOTION_DATABASE_ID_HERE"

# CHANGE THIS: Update object name throughout
OBJECT_NAME = "deals"  # or "companies", "orders", etc.
```

2. **Update HubSpot Object Type:**
```python
# CHANGE THIS: HubSpot API endpoint
def get_hubspot_properties():
    url = f"{HUBSPOT_BASE_URL}/crm/v3/properties/deals"  # Change 'deals' to your object
    # OR: companies, line_items, products, tickets, etc.
```

3. **Update Notion Property Parsing:**
```python
# CHANGE THIS: Look for your specific properties
def _parse_notion_properties_from_api(self, database_info):
    # The property parsing logic usually stays the same
    # But verify field names match your database schema
```

4. **Update Output File Names:**
```python
# CHANGE THIS: Output file paths
markdown_file = f"notion_hubspot_{OBJECT_NAME}_property_mapping.md"
csv_file = f"notion_hubspot_{OBJECT_NAME}_mapping.csv"
```

#### 1.3 Run Property Analysis
```bash
cd /workspaces/automations_hub
python [OBJECT]_property_matcher.py

# This generates:
# - notion_hubspot_[OBJECT]_property_mapping.md
# - notion_hubspot_[OBJECT]_mapping.csv
```

### Step 2: Workflow Creation

#### 2.1 Copy Base Workflow Files
```bash
# Copy webhook workflow
cp /workspaces/automations_hub/n8n/workflows/notion_hubspot_contact_sync.json \
   /workspaces/automations_hub/n8n/workflows/notion_hubspot_[OBJECT]_sync.json

# Copy polling workflow  
cp /workspaces/automations_hub/n8n/workflows/notion_hubspot_contact_sync_polling.json \
   /workspaces/automations_hub/n8n/workflows/notion_hubspot_[OBJECT]_sync_polling.json
```

#### 2.2 Modify Workflow Files

**For both JSON files, update these sections:**

1. **Workflow Names:**
```json
{
  "name": "Notion HubSpot [Object] Sync - Webhook",
  "nodes": [...]
}
```

2. **Database IDs:**
```json
// Find Notion nodes and update database_id
{
  "parameters": {
    "database_id": "YOUR_NOTION_DATABASE_ID",
    "simple": false
  }
}
```

3. **HubSpot Object Types:**
```json
// Find HubSpot nodes and update object type
{
  "parameters": {
    "resource": "deal",  // Change to: company, line_item, etc.
    "operation": "create"
  }
}
```

4. **Webhook Endpoints:**
```json
// Update webhook paths
{
  "parameters": {
    "path": "hubspot-[object]-updated",  // e.g., "hubspot-deal-updated"
    "httpMethod": "POST"
  }
}
```

5. **Property Mappings:**
```json
// Update the transformation node with your property mappings
{
  "parameters": {
    "values": {
      "string": [
        {
          "name": "email",
          "value": "={{ $json.properties?.Email?.email || $json.properties?.email?.value }}"
        }
        // ADD YOUR PROPERTY MAPPINGS HERE based on the analysis
      ]
    }
  }
}
```

#### 2.3 Clean Workflow Files

**Remove Personal Data:**
```bash
# Clean the workflows (remove IDs, credentials, etc.)
cd /workspaces/automations_hub/n8n/workflows

# Use sed or manual editing to remove:
# - "id": "specific-node-id"  
# - credential references
# - execution data
```

### Step 3: Import to n8n

#### 3.1 Import Workflows
```bash
cd /workspaces/automations_hub/n8n

# Import webhook workflow
curl -X POST \
  -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  -d @workflows/notion_hubspot_[OBJECT]_sync.json \
  "$N8N_CLOUD_INSTANCE_URL/api/v1/workflows/import"

# Import polling workflow
curl -X POST \
  -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  -d @workflows/notion_hubspot_[OBJECT]_sync_polling.json \
  "$N8N_CLOUD_INSTANCE_URL/api/v1/workflows/import"
```

#### 3.2 Configure Credentials

**In n8n Dashboard:**
1. Go to **Credentials** tab
2. Verify **Notion API** credential exists
3. Verify **HubSpot API** credential exists  
4. Update workflows to use correct credential IDs

### Step 4: Monitoring & Testing Setup

#### 4.1 Create Monitoring Script
```bash
# Copy monitoring template
cp /workspaces/automations_hub/n8n/scripts/monitor_contact_sync.sh \
   /workspaces/automations_hub/n8n/scripts/monitor_[OBJECT]_sync.sh
```

**Update `monitor_[OBJECT]_sync.sh`:**
```bash
# CHANGE THESE VARIABLES:
OBJECT_NAME="deals"  # or your object name
WORKFLOW_PATTERN="Deal Sync"  # match your workflow names
WEBHOOK_PATH="hubspot-deal-updated"  # match your webhook path

# Update all echo statements to reflect the new object:
echo -e "${BLUE}🔍 Notion ↔ HubSpot ${OBJECT_NAME^} Sync Status Dashboard${NC}"
```

#### 4.2 Create Testing Script
```bash
# Copy testing template  
cp /workspaces/automations_hub/n8n/scripts/test_contact_sync.sh \
   /workspaces/automations_hub/n8n/scripts/test_[OBJECT]_sync.sh
```

**Update `test_[OBJECT]_sync.sh`:**
```bash
# CHANGE THESE VARIABLES:
OBJECT_NAME="deals"
WEBHOOK_ENDPOINT="hubspot-deal-updated"

# Update test payload to match HubSpot object structure:
TEST_PAYLOAD='[{
  "eventId": 12345,
  "subscriptionId": 54321,
  "portalId": 123456,
  "appId": 654321,
  "occurredAt": '$(date +%s000)',
  "subscriptionType": "deal.propertyChange",  # Change object type
  "attemptNumber": 0,
  "objectId": 98765,
  "changeSource": "MANUAL",
  "propertyName": "dealname",  # Object-specific property
  "propertyValue": "Test Deal"
}]'
```

### Step 5: Testing & Verification

#### 5.1 Run Complete Test Suite
```bash
cd /workspaces/automations_hub/n8n

# Make scripts executable
chmod +x scripts/monitor_[OBJECT]_sync.sh
chmod +x scripts/test_[OBJECT]_sync.sh

# Run tests
./scripts/monitor_[OBJECT]_sync.sh
./scripts/test_[OBJECT]_sync.sh
```

#### 5.2 Manual Testing

1. **Create/Update Object in Notion:**
   - Add a new record to your Notion database
   - Or update an existing record

2. **Wait & Verify:**
   - Wait 5 minutes for polling cycle
   - Check HubSpot for the new/updated object
   - Monitor n8n executions

3. **Test Reverse Sync:**
   - Update object in HubSpot
   - Check if webhook triggers
   - Verify update appears in Notion

---

## 🎯 Object-Specific Considerations

### For **Deals** (`/crm/v3/properties/deals`):
```python
# Key properties to map:
# - dealname → Deal Name
# - amount → Amount  
# - dealstage → Deal Stage
# - closedate → Close Date
# - pipeline → Pipeline
```

### For **Companies** (`/crm/v3/properties/companies`):
```python
# Key properties to map:
# - name → Company Name
# - domain → Website Domain
# - industry → Industry
# - city → City
# - state → State/Region
```

### For **Products** (`/crm/v3/properties/products`):
```python
# Key properties to map:
# - name → Product Name
# - price → Price
# - description → Description
# - hs_sku → SKU
```

### For **Tickets** (`/crm/v3/properties/tickets`):
```python
# Key properties to map:
# - subject → Ticket Subject
# - hs_ticket_priority → Priority
# - hs_ticket_category → Category
# - content → Description
```

---

## 📋 Complete File Checklist

### Files to Create for Each Object:
- [ ] `[OBJECT]_property_matcher.py`
- [ ] `workflows/notion_hubspot_[OBJECT]_sync.json`
- [ ] `workflows/notion_hubspot_[OBJECT]_sync_polling.json`
- [ ] `scripts/monitor_[OBJECT]_sync.sh`
- [ ] `scripts/test_[OBJECT]_sync.sh`
- [ ] `[OBJECT]_SYNC_VERIFICATION.md`

### Generated Reports:
- [ ] `notion_hubspot_[OBJECT]_property_mapping.md`
- [ ] `notion_hubspot_[OBJECT]_mapping.csv`

---

## 🔧 Common Modifications Needed

### 1. **Database Schema Differences:**
Some Notion databases may have:
- Different property types (relation, formula, rollup)
- Custom naming conventions
- Multi-select vs single-select fields

### 2. **HubSpot Object Variations:**
Different objects have:
- Unique required fields
- Different property naming patterns
- Object-specific workflows in HubSpot

### 3. **Business Logic Customizations:**
You may need to add:
- Custom field transformations
- Validation rules
- Conditional logic based on object state

---

## 🚨 Troubleshooting Guide

### Property Mapping Issues:
1. **Check HubSpot API Response:** Verify object endpoint returns properties
2. **Notion Database Structure:** Ensure database has expected properties
3. **Data Type Mismatches:** Add transformation logic for incompatible types

### Workflow Import Failures:
1. **Clean JSON Files:** Remove all IDs and personal data
2. **Update Credentials:** Ensure credential IDs are correct
3. **Check Node Dependencies:** Verify all required n8n nodes are available

### Sync Not Working:
1. **Check Webhook URLs:** Verify webhook endpoints are accessible
2. **Monitor Executions:** Look for error messages in n8n logs
3. **Test API Connections:** Verify both Notion and HubSpot APIs respond

---

## 🎉 Success Criteria

### Your sync is working when:
- ✅ Property analysis completes without errors
- ✅ Workflows import successfully to n8n
- ✅ Both workflows show as "Active"
- ✅ Test executions complete without errors
- ✅ Objects sync bidirectionally within 5 minutes
- ✅ Property mappings preserve data integrity

---

## 📚 Reference Commands

### Quick Setup Commands:
```bash
# 1. Copy files
cp property_matcher.py deals_property_matcher.py
cp workflows/notion_hubspot_contact_sync.json workflows/notion_hubspot_deals_sync.json

# 2. Run analysis
python deals_property_matcher.py

# 3. Import workflows
curl -X POST -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  -d @workflows/notion_hubspot_deals_sync.json \
  "$N8N_CLOUD_INSTANCE_URL/api/v1/workflows/import"

# 4. Test
./scripts/monitor_deals_sync.sh
```

This guide provides everything needed to replicate the contact sync pattern for any Notion ↔ HubSpot object synchronization! 🚀
