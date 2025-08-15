# N8N Automation Platform

Complete n8n workflow automation system with **proven REST API integration** for cloud instances and **production-ready Notion ↔ HubSpot sync workflows**.

## 🎯 **Latest: Notion ↔ HubSpot Contact Sync**

**✅ DEPLOYED & OPERATIONAL** - Complete 2-way sync system with 91.7% property coverage

### Quick Status Check
```bash
./scripts/monitor_contact_sync.sh  # Check sync status and recent executions
./scripts/test_contact_sync.sh     # Test webhook endpoints and functionality
```

### Sync System Features
- **Real-time sync**: Webhook-based instant updates
- **Polling backup**: 5-minute interval checks for reliability  
- **22 mapped properties**: Email, phone, name, company, address, etc.
- **Production monitoring**: Status dashboards and health checks
- **Template system**: Replicate for deals, companies, products, etc.

**📋 Workflow IDs**:
- Webhook: `gJuzphWxKj2rYuAO` 
- Polling: `dGlNn9kvIAjjq04f`

## 📚 Complete Documentation Automation Platform

Complete n8n workflow automation system with **proven REST API integration** for cloud instances.

## � Complete Documentation

**👉 See [N8N_WORKFLOWS_GUIDE.md](./N8N_WORKFLOWS_GUIDE.md) for the complete, comprehensive guide**

This guide contains everything you need:
- ✅ Working commands and scripts
- 📋 JSON workflow requirements
- 🔐 Credentials management
- 🛡️ Security guidelines
- 🚀 Complete workflow processes
- ⚡ Emergency commands

## 🚨 CRITICAL FOR FUTURE AGENTS

**n8n CLI commands DO NOT WORK with cloud instances.** 
Use the REST API scripts in the `scripts/` directory.

## 📁 Directory Structure

```
n8n/
├── CONTACT_SYNC_VERIFICATION.md    # 📊 Sync status and verification guide
├── WORKFLOW_REPLICATION_GUIDE.md   # 🏗️ Complete guide for new object syncs
├── AGENT_QUICK_REFERENCE.md        # 🤖 Quick reference for AI agents
├── N8N_WORKFLOWS_GUIDE.md          # 📖 COMPLETE GUIDE - Read This First!
├── README.md                       # This file - quick overview
├── scripts/                        # All working scripts & tools
│   ├── export_workflows_api.sh     # ✅ Export from cloud (REST API)
│   ├── import_workflows_api.sh     # ✅ Import to cloud (REST API)
│   ├── monitor_contact_sync.sh     # 📊 Monitor sync status
│   ├── test_contact_sync.sh        # 🧪 Test sync functionality
│   ├── generate_sync_template.sh   # 🏗️ Generate new object syncs
│   ├── setup_deals_sync.sh         # 📋 Example: Deals sync setup
│   ├── n8n_workflow_manager.py     # Python workflow manager
│   └── [other scripts...]
├── workflows/                      # 🔄 Production sync workflows
│   ├── notion_hubspot_contact_sync.json         # Webhook-based sync
│   ├── notion_hubspot_contact_sync_polling.json # Polling-based sync
│   └── [template workflows...]
├── exports/                        # 9 working workflows (196K total)
├── docs/                          # 📚 N8N help center documentation
├── credentials/                   # Credential storage (gitignored)
└── objects/                      # 📁 Generated sync templates (by object type)
```

## 🚀 Quick Start

### Monitor Active Sync Workflows
```bash
# Check sync status and health
./scripts/monitor_contact_sync.sh

# Test webhook endpoints
./scripts/test_contact_sync.sh

# Open n8n dashboard
open https://hairsolutionsco.app.n8n.cloud
```

### Create New Object Sync (e.g., Deals)
```bash
# Generate complete sync template
./scripts/generate_sync_template.sh deals YOUR_NOTION_DATABASE_ID

# Or use the example setup script
./scripts/setup_deals_sync.sh
```

### Export Workflows from Cloud
```bash
# Use this script - it WORKS
./scripts/export_workflows_api.sh

# Manual API call (if needed)
curl -H "X-N8N-API-KEY: $N8N_API_KEY" \
     "$N8N_CLOUD_INSTANCE_URL/api/v1/workflows"
```

### Import Workflows to Cloud
```bash
# Test first with dry run
./scripts/import_workflows_api.sh -d workflow.json

# Actual import
./scripts/import_workflows_api.sh workflow.json
```

### Full Documentation
**👉 For complete instructions, see [N8N_WORKFLOWS_GUIDE.md](./N8N_WORKFLOWS_GUIDE.md)**

---

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

## 🌍 Environment Variables
```bash
export N8N_CLOUD_INSTANCE_URL="https://hairsolutionsco.app.n8n.cloud"
export N8N_API_KEY="your-api-key"
export N8N_USER_EMAIL="info@oneheadhair.com"
```
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

### 🚀 New: Complete N8N Documentation Available
- **`docs/N8N_DOCS_INTEGRATION.md`** - **Integration summary and quick access guide**
- **`docs/docs/`** - **Complete n8n documentation repository** (1000+ pages)
  - **Getting Started**: `docs/docs/index.md` - Introduction and quick start
  - **API Reference**: `docs/docs/api/` - Complete REST API documentation
  - **Integrations**: `docs/docs/integrations/` - 1000+ pre-built node integrations
  - **Workflows**: `docs/_workflows/` - Example workflow templates
  - **Advanced AI**: `docs/docs/advanced-ai/` - AI-powered automation features
  - **Hosting**: `docs/docs/hosting/` - Self-hosting and deployment guides
  - **Code Examples**: `docs/docs/code/` - Node.js and Python integration examples

### Custom Documentation
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
