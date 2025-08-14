# N8N Quick Reference

⚡ **For Future Agents - Essential Commands**

## 🚨 CRITICAL: Use REST API Only for Cloud

```bash
# ✅ WORKING COMMANDS (REST API)
./tools/export_workflows_api.sh    # Export all workflows from cloud
./tools/import_workflows_api.sh    # Import workflows to cloud
./tools/import_workflows_api.sh -d # Dry run import

# ❌ BROKEN COMMANDS (CLI - don't use with cloud)
npm run export                     # FAILS with cloud
npm run import                     # FAILS with cloud
n8n export:workflow               # FAILS with cloud
n8n import:workflow               # FAILS with cloud
```

## � Import Requirements (CRITICAL!)

### ✅ Required Properties
```json
{
  "name": "Workflow Name",
  "nodes": [...],
  "connections": {},
  "settings": {}  // ← REQUIRED! Even if empty
}
```

### ❌ Forbidden Properties (REMOVE THESE!)
- `id`, `createdAt`, `updatedAt`, `versionId`
- `triggerCount`, `meta`, `tags`, `staticData`
- `isArchived`, `active` (can set after import)

### 🔒 Security Patterns to Remove
- `sk_live_*`, `sk_test_*` (Stripe keys)
- `whsec_*` (Webhook secrets)
- `Bearer [tokens]` (API tokens)

## �📁 Key Directories

- `exports/` - 9 working workflows (196K total) ✅
- `tools/` - REST API scripts that actually work ✅
- `scripts/` - Legacy CLI scripts (mostly broken for cloud) ❌
- `workflows/` - Development workflows (some corrupted, fixed)
- `secure_workflows/` - Clean workflows with credential IDs ✅

## 🔧 Environment Setup

```bash
export N8N_CLOUD_INSTANCE_URL="https://hairsolutionsco.app.n8n.cloud"
export N8N_API_KEY="your-api-key"
export N8N_USER_EMAIL="info@oneheadhair.com"
```

## 🔑 Available Credential IDs

| Service | Credential ID | Usage |
|---------|---------------|-------|
| HubSpot | `ID4CUY90jW5ObSXedy` | CRM operations |
| Gmail OAuth2 | `IDiRhtr9mcBtiwn0Jn` | Email automation |
| Google OAuth2 | `IDuheZ3yW8cV9FMwIz` | Google services |
| OpenAI | `ID4X9TIhDpjNa5gM9J` | AI operations |
| GoCardless | `IDZjro27xRan8oQvXj` | Payment processing |
| Stripe | `ID3q1LYGrkaZIDtJar` | Payment processing |
| Notion | `ID4jkKCiAXGH1iVwyi` | Database operations |

## 📊 Current Status

- ✅ **12 Workflows Total** - 9 original + 3 secure versions
- ✅ **REST API Scripts** - Proven working export/import tools
- ✅ **Documentation** - Comprehensive guides updated
- ✅ **Security** - Credential IDs implemented, sensitive data removed
- ✅ **Import Rule Book** - Complete guide for future imports
- ⚠️ **CLI Scripts** - Legacy scripts marked as non-functional for cloud

## 🚀 Quick Actions

```bash
# Test connection
curl -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_CLOUD_INSTANCE_URL/api/v1/workflows"

# Export all workflows
./tools/export_workflows_api.sh

# Import with safety check
./tools/import_workflows_api.sh -d

# View workflow list
ls -la exports/

# Import secure workflows
./tools/import_workflows_api.sh -s secure_workflows/
```

## 🔍 Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Import fails with "additional properties" | Remove `id`, `createdAt`, `updatedAt`, etc. |
| Import fails with "missing settings" | Add `"settings": {}` to workflow root |
| Security scan blocks commit | Remove API keys, use credential IDs |
| Script reports error on success | Check n8n interface - might have imported anyway |

## 📋 Pre-Import Checklist

- [ ] Remove forbidden properties (`id`, `createdAt`, etc.)
- [ ] Add required properties (`settings: {}`)
- [ ] Replace sensitive data with credential IDs
- [ ] Validate JSON syntax
- [ ] Run dry-run test first
- [ ] Verify import by checking n8n interface

---
**Last Updated**: August 14, 2025  
**Status**: ✅ Fully operational with REST API integration  
**Rule Book**: See `N8N_IMPORT_RULE_BOOK.md` for complete details
