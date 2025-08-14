# N8N Automation Platform

Complete n8n workflow automation system with **proven REST API integration** for cloud instances.

## 🚨 CRITICAL INFORMATION FOR FUTURE AGENTS

**n8n CLI commands DO NOT WORK with cloud instances.** 
Use the REST API scripts in the `tools/` directory.

## 📁 Directory Structure

```
n8n/
├── README.md                    # This file - master guide
├── exports/                     # Exported workflows (9 workflows, 196K)
│   ├── README.md               # Export details and import instructions
│   └── *.json                  # Individual workflow files
├── tools/                       # Working scripts (REST API based)
│   ├── export_workflows_api.sh  # ✅ Export from cloud (WORKS)
│   └── import_workflows_api.sh  # ✅ Import to cloud (WORKS)
├── scripts/                     # Legacy scripts (n8n CLI - mostly broken)
│   ├── n8n_git_sync.sh         # ❌ Uses CLI (fails with cloud)
│   └── *.sh                    # ❌ Other CLI-based scripts
├── workflows/                   # Development workflows (broken files)
├── credentials/                 # Credentials (gitignored)
└── docs/                       # Documentation
    ├── N8N_GIT_INTEGRATION.md  # Updated with correct methods
    └── n8n_README.md           # Platform overview
```

## 🚀 Quick Start (CORRECT METHODS)

### Export Workflows from Cloud
```bash
# Use this script - it WORKS
./tools/export_workflows_api.sh

# Manual API call (if needed)
curl -H "X-N8N-API-KEY: $N8N_API_KEY" \
     "$N8N_CLOUD_INSTANCE_URL/api/v1/workflows"
```

### Import Workflows to Cloud
```bash
# Import from exports directory
./tools/import_workflows_api.sh

# Import with dry run (recommended first)
./tools/import_workflows_api.sh -d

# Import with overwrite
./tools/import_workflows_api.sh -o
```

### Environment Variables Required
```bash
export N8N_CLOUD_INSTANCE_URL="https://hairsolutionsco.app.n8n.cloud"
export N8N_API_KEY="your-api-key"
export N8N_USER_EMAIL="info@oneheadhair.com"  # Optional
```

## ✅ Current Status

- **9 Workflows Exported**: All workflows successfully exported using REST API
- **Export Size**: 196K total across all workflows
- **API Connection**: Validated and working
- **Scripts**: Proven working export/import scripts available

## 🔧 Available Workflows

| Workflow | Size | Description |
|----------|------|-------------|
| Gmail Assistant | 36K | Email automation and management |
| Rag 2.0 Template | 68K | RAG implementation template |
| Personalised Outreach | 24K | Customer data-driven outreach |
| CS Agent Lite | 12K | Customer service automation |
| Payment Sync to Notion | 8K | Payment tracking integration |
| AI Assistant | 8K | General AI assistant workflows |
| My workflow | 12K | Custom workflow |
| My workflow 2 | 16K | Custom workflow variant |
| My workflow 3 | 12K | Custom workflow variant |

## ❌ What DOESN'T Work

```bash
# These CLI commands FAIL with cloud instances:
npm run export                    # ❌ FAILS
npm run import                    # ❌ FAILS  
npm run cloud:export             # ❌ FAILS
npm run cloud:import             # ❌ FAILS
n8n export:workflow              # ❌ FAILS
n8n import:workflow              # ❌ FAILS
```

## ✅ What WORKS

```bash
# These REST API scripts WORK:
./tools/export_workflows_api.sh  # ✅ WORKS
./tools/import_workflows_api.sh  # ✅ WORKS
```

## 🔗 Integration Points

### MCP Server Access
- **Golf MCP Server**: Direct n8n workflow management via MCP
- **Cross-Platform**: Seamless integration with Notion, HubSpot, Shopify

### Git Integration
- Each workflow exported as individual JSON file
- Perfect for version control and diff tracking
- Automated backup system in place

### API Endpoints
- **Base URL**: https://hairsolutionsco.app.n8n.cloud
- **List Workflows**: GET /api/v1/workflows
- **Get Workflow**: GET /api/v1/workflows/{id}
- **Create Workflow**: POST /api/v1/workflows
- **Update Workflow**: PUT /api/v1/workflows/{id}

## 🛡️ Security

- API keys stored in environment variables
- Credentials directory gitignored
- No sensitive data in exported workflows

## 📚 Documentation

- `QUICK_REFERENCE.md` - Essential commands and credential IDs for quick lookup
- `N8N_IMPORT_RULE_BOOK.md` - **Complete guide for successful workflow imports**
- `N8N_IMPORT_TROUBLESHOOTING.md` - Solutions for common import errors
- `CREDENTIALS_REFERENCE.md` - Available n8n credential IDs
- `SECURITY_NOTICE.md` - Security cleanup information and best practices
- `exports/README.md` - Detailed export information
- `exports/SECURE_WORKFLOWS_README.md` - Guide for secure workflow versions
- `N8N_GIT_INTEGRATION.md` - Updated integration guide

## 🚨 Critical Notes for Future Development

1. **ALWAYS use REST API scripts** for cloud workflows
2. **n8n CLI only works** with local instances
3. **Environment variables must be set** before running scripts
4. **Test API connectivity first** before attempting operations
5. **Use dry-run mode** when importing to avoid accidents

---

**Last Updated**: August 14, 2025  
**Status**: ✅ Fully Operational with REST API integration  
**Next Steps**: GitOps implementation using proven REST API methods
