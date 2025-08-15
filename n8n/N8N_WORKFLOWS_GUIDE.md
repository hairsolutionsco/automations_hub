# N8N Workflows Complete Guide

**The definitive guide for working with n8n workflows in cloud environments**

## 🎯 Quick Start for Future Agents

### Essential Commands (Use These Only)
```bash
# ✅ WORKING - REST API Scripts
./scripts/export_workflows_api.sh    # Export all workflows from cloud
./scripts/import_workflows_api.sh    # Import workflows to cloud
./scripts/import_workflows_api.sh -d # Dry run import

# ❌ NEVER USE - CLI Commands (Fail with Cloud)
n8n export:workflow               # FAILS with cloud instances
n8n import:workflow               # FAILS with cloud instances
```

### Critical Files & Directories
```
n8n/
├── scripts/                      # All working scripts & tools
│   ├── export_workflows_api.sh   # ✅ Export from cloud (REST API)
│   ├── import_workflows_api.sh   # ✅ Import to cloud (REST API)
│   ├── n8n_workflow_manager.py   # Python workflow manager
│   └── [other scripts...]
├── exports/                      # 9 working workflows (196K total)
├── credentials/                  # Credential storage (gitignored)
├── docs/                        # N8N help center documentation
└── workflows/                   # Development workflows
```

---

## 📋 Workflow JSON Requirements

### ✅ Required Properties (Import FAILS Without These)
```json
{
  "name": "Workflow Name",           // Required: Must be unique
  "nodes": [...],                   // Required: Array of workflow nodes
  "connections": {},                // Required: Node connections
  "settings": {}                    // Required: Even if empty object
}
```

### ❌ Forbidden Properties (Remove Before Import)
```json
// These properties MUST be removed for successful imports:
{
  "id": "...",                     // ❌ Auto-generated on import
  "createdAt": "...",              // ❌ Auto-generated timestamp
  "updatedAt": "...",              // ❌ Auto-generated timestamp
  "isArchived": false,             // ❌ Not accepted in imports
  "versionId": "...",              // ❌ Auto-generated version
  "triggerCount": 0,               // ❌ Calculated by n8n
  "meta": {...},                   // ❌ Rejected during import
  "tags": [...],                   // ❌ Often rejected, add after
  "staticData": {...},             // ❌ Auto-initialized
  "active": true                   // ❌ Set after import
}
```

### Quick Cleanup Command
```bash
# Remove forbidden properties from any workflow
jq 'del(.id, .createdAt, .updatedAt, .isArchived, .versionId, .triggerCount, .meta, .tags, .staticData, .active)' input.json > clean_workflow.json
```

---

## 🔐 Credentials Management

### Available Credential IDs (Use These)
```javascript
// CRM & Sales
const HUBSPOT_CREDENTIAL = "ID4CUY90jW5ObSXedy";        // HubSpot App Token

// Email & Communication  
const GMAIL_CREDENTIAL = "IDiRhtr9mcBtiwn0Jn";          // Gmail OAuth2

// Google Services
const GOOGLE_CREDENTIAL = "IDuheZ3yW8cV9FMwIz";         // Google OAuth2

// AI & ML
const OPENAI_CREDENTIAL = "ID4X9TIhDpjNa5gM9J";         // OpenAI API Key

// Payments & Finance
const GOCARDLESS_CREDENTIAL = "IDZjro27xRan8oQvXj";     // GoCardless Bearer
const STRIPE_CREDENTIAL = "ID3q1LYGrkaZIDtJar";         // Stripe API Key

// Productivity & Data
const NOTION_CREDENTIAL = "ID4jkKCiAXGH1iVwyi";         // Notion API Key
```

### Correct Credential Format in Nodes
```json
{
  "credentials": {
    "stripeApi": {
      "id": "ID3q1LYGrkaZIDtJar",
      "name": "Stripe API Key"
    },
    "notionApi": {
      "id": "ID4jkKCiAXGH1iVwyi", 
      "name": "Notion API Key"
    }
  }
}
```

---

## 🔧 Common Import Errors & Solutions

### Error: "must NOT have additional properties"
**Problem**: Workflow contains forbidden metadata properties  
**Solution**: Remove all forbidden properties listed above
```bash
jq 'del(.id, .createdAt, .updatedAt, .isArchived, .versionId, .triggerCount, .meta, .tags, .staticData, .active)' workflow.json > clean.json
```

### Error: "must have required property 'settings'"
**Problem**: Missing required settings object  
**Solution**: Add empty settings object
```json
{
  "name": "My Workflow",
  "nodes": [...],
  "connections": {},
  "settings": {}  // Add this if missing
}
```

### Error: "credential not found"
**Problem**: Credential ID doesn't exist in target instance  
**Solution**: Use the credential IDs from the table above

### Error: "webhook URL validation failed"
**Problem**: Webhook URLs contain old domain/environment  
**Solution**: Update webhook URLs or use relative paths

---

## 🛡️ Security Guidelines

### Sensitive Data Patterns (Never Commit These)
```bash
# Dangerous patterns to scan for:
sk_live_*        # Stripe live API keys
sk_test_*        # Stripe test API keys  
pk_live_*        # Stripe publishable keys
whsec_*          # Webhook secrets
Bearer [A-Za-z0-9]+  # Bearer tokens
```

### Pre-Commit Security Check
```bash
# Always run before committing workflows:
grep -r "sk_live\|sk_test\|whsec_\|Bearer.*[A-Za-z0-9]\{20,\}" exports/

# If anything found, clean it:
sed -i 's/sk_live_[A-Za-z0-9]*/[STRIPE_LIVE_KEY_REMOVED]/g' *.json
sed -i 's/whsec_[A-Za-z0-9]*/[WEBHOOK_SECRET_REMOVED]/g' *.json
```

### Environment Variables Setup
```bash
# Required environment variables:
export N8N_CLOUD_INSTANCE_URL="https://your-instance.app.n8n.cloud"
export N8N_API_KEY="n8n_api_your_api_key_here"
export N8N_USER_EMAIL="your@email.com"
```

---

## 🚀 Complete Workflow Process

### 1. Export from N8N Cloud
```bash
cd /workspaces/automations_hub/n8n
./scripts/export_workflows_api.sh
```

### 2. Clean Exported Workflows
```bash
# Remove sensitive data and forbidden properties
for file in exports/*.json; do
    jq 'del(.id, .createdAt, .updatedAt, .isArchived, .versionId, .triggerCount, .meta, .tags, .staticData, .active)' "$file" > "clean_$(basename "$file")"
done

# Security scan
grep -r "sk_live\|sk_test\|whsec_" exports/
```

### 3. Modify Workflows (If Needed)
```bash
# Use the Python workflow manager
python scripts/n8n_workflow_manager.py modify workflow.json --update-credential="stripeApi:ID3q1LYGrkaZIDtJar"
```

### 4. Import to N8N Cloud
```bash
# Dry run first
./scripts/import_workflows_api.sh -d clean_workflow.json

# Actual import
./scripts/import_workflows_api.sh clean_workflow.json
```

### 5. Git Workflow
```bash
git add .
git commit -m "feat: update workflows $(date +%Y-%m-%d)"
git push origin main
```

---

## 📚 Additional Resources

- **N8N Help Documentation**: `./docs/` (Complete n8n help center)
- **Working Scripts**: `./scripts/` (All tested and proven scripts)
- **Example Workflows**: `./exports/` (9 working production workflows)

---

## ⚡ Emergency Commands

### Backup All Workflows
```bash
./scripts/export_workflows_api.sh
cp -r exports/ "backup_$(date +%Y%m%d_%H%M%S)/"
```

### Restore from Backup
```bash
cd backup_20250814_120000/
for file in *.json; do
    ../scripts/import_workflows_api.sh "$file"
done
```

### Check Workflow Status
```bash
curl -H "X-N8N-API-KEY: $N8N_API_KEY" \
     "$N8N_CLOUD_INSTANCE_URL/api/v1/workflows" | jq '.data[] | {id, name, active}'
```

---

**Guide Version**: 1.0  
**Last Updated**: August 15, 2025  
**Status**: ✅ Tested and Verified  
**All methods proven working with n8n cloud instances**
