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

## 📁 Key Directories

- `exports/` - 9 working workflows (196K total) ✅
- `tools/` - REST API scripts that actually work ✅
- `scripts/` - Legacy CLI scripts (mostly broken for cloud) ❌
- `workflows/` - Development workflows (some corrupted, fixed)

## 🔧 Environment Setup

```bash
export N8N_CLOUD_INSTANCE_URL="https://hairsolutionsco.app.n8n.cloud"
export N8N_API_KEY="your-api-key"
export N8N_USER_EMAIL="info@oneheadhair.com"
```

## 📊 Current Status

- ✅ **9 Workflows Exported** - All cloud workflows backed up
- ✅ **REST API Scripts** - Proven working export/import tools
- ✅ **Documentation** - Comprehensive guides updated
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
```

---
**Last Updated**: August 14, 2025  
**Status**: ✅ Fully operational with REST API integration
