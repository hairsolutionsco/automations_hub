# 🤖 Agent Quick Reference: Building Notion ↔ HubSpot Sync Workflows

## 🎯 Agent Instructions

When a user asks to create a sync workflow for a new object (deals, companies, products, etc.), follow this exact process:

### 1. 📋 Quick Setup (Automated)
```bash
# Use the template generator for instant setup
cd /workspaces/automations_hub/n8n
./scripts/generate_sync_template.sh [OBJECT_TYPE] [NOTION_DATABASE_ID]

# Examples:
./scripts/generate_sync_template.sh deals abc123-def456-789
./scripts/generate_sync_template.sh companies xyz789-abc123-456
```

### 2. 🔧 Manual Customization Process

#### A. Copy Base Files
```bash
# From the working contact sync:
cp property_matcher.py [OBJECT]_property_matcher.py
cp workflows/notion_hubspot_contact_sync.json workflows/notion_hubspot_[OBJECT]_sync.json
cp scripts/monitor_contact_sync.sh scripts/monitor_[OBJECT]_sync.sh
```

#### B. Required Modifications

**In `[OBJECT]_property_matcher.py`:**
- Update `NOTION_DATABASE_ID = "NEW_DATABASE_ID"`
- Change HubSpot endpoint: `/crm/v3/properties/[OBJECT]`
- Update object references throughout

**In workflow JSON files:**
- Update workflow names: `"name": "Notion HubSpot [Object] Sync"`
- Change database IDs: `"database_id": "NEW_DATABASE_ID"`
- Update HubSpot resource: `"resource": "[object]"`
- Modify webhook paths: `"path": "hubspot-[object]-updated"`
- Update property mappings in transformation nodes

**In monitoring scripts:**
- Update object references and webhook paths
- Modify test payloads for object-specific properties

### 3. 🎯 Object-Specific Configurations

#### For Deals:
- HubSpot endpoint: `/crm/v3/properties/deals`
- Key properties: `dealname`, `amount`, `dealstage`, `closedate`
- Resource: `"resource": "deal"`

#### For Companies:
- HubSpot endpoint: `/crm/v3/properties/companies`
- Key properties: `name`, `domain`, `industry`, `city`
- Resource: `"resource": "company"`

#### For Products:
- HubSpot endpoint: `/crm/v3/properties/products`
- Key properties: `name`, `price`, `description`, `hs_sku`
- Resource: `"resource": "product"`

#### For Tickets:
- HubSpot endpoint: `/crm/v3/properties/tickets`
- Key properties: `subject`, `hs_ticket_priority`, `content`
- Resource: `"resource": "ticket"`

### 4. 📤 Import & Deploy Process

```bash
# 1. Run property analysis
python [OBJECT]_property_matcher.py

# 2. Import workflows
curl -X POST \
  -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  -d @workflows/notion_hubspot_[OBJECT]_sync.json \
  "$N8N_CLOUD_INSTANCE_URL/api/v1/workflows/import"

# 3. Test setup
./scripts/monitor_[OBJECT]_sync.sh
```

### 5. ✅ Verification Checklist

Agent should confirm:
- [ ] Property analysis completed (shows mapping coverage %)
- [ ] Workflows imported successfully (returns workflow IDs)
- [ ] Both workflows show as "Active: true"
- [ ] Webhook endpoints responding (HTTP 200)
- [ ] Test executions running without errors

### 6. 🚨 Common Issues & Solutions

**Property Analysis Fails:**
- Check Notion database ID is correct
- Verify HubSpot object endpoint exists
- Ensure API credentials are set

**Workflow Import Fails:**
- Clean JSON files (remove IDs, credentials)
- Update credential references to existing IDs
- Check n8n node availability

**Sync Not Working:**
- Verify property mappings in transformation nodes
- Check API connectivity for both services
- Monitor execution logs for specific errors

### 7. 📁 File Structure Template

```
/workspaces/automations_hub/n8n/objects/[OBJECT]/
├── workflows/
│   ├── [object]_sync_webhook.json
│   └── [object]_sync_polling.json
├── scripts/
│   ├── monitor_[object]_sync.sh
│   └── test_[object]_sync.sh
├── docs/
│   └── [OBJECT]_SYNC_SETUP.md
└── [object]_property_matcher.py
```

### 8. 🎯 Success Metrics

**Property Coverage:** Target 80%+ mapping coverage
**Import Success:** Both workflows active in n8n
**Execution Health:** No errors in test runs
**Sync Verification:** Changes flow between systems within 5 minutes

## 🚀 Quick Commands for Agent

```bash
# Generate complete template
./scripts/generate_sync_template.sh deals YOUR_DB_ID

# Quick deals setup (example)
./scripts/setup_deals_sync.sh

# Monitor any object
./scripts/monitor_[OBJECT]_sync.sh

# Universal monitoring
./scripts/monitor_contact_sync.sh  # Works as pattern for all
```

## 📚 Reference Documentation

- **Complete Guide:** `/workspaces/automations_hub/n8n/WORKFLOW_REPLICATION_GUIDE.md`
- **Contact Verification:** `/workspaces/automations_hub/n8n/CONTACT_SYNC_VERIFICATION.md`
- **Working Examples:** `/workspaces/automations_hub/n8n/workflows/`

This provides everything needed to replicate the contact sync success for any object! 🎉
