# Automation Hub Scripts Organization

## 📁 Scripts Directory Structure

Each tool in the automation hub now has its own `scripts/` directory with specialized management and utility scripts.

```
automations_hub/
├── master_control.sh                    # 🏠 Master control script
├── setup_shopify_agent.sh              # 🤖 Shopify agent setup
│
├── shopify/scripts/
│   ├── agent_quickstart.sh             # 🚀 Quick start for agent features
│   ├── store_management.sh             # 🛍️ Store operations
│   └── dev_tools.sh                    # 🔧 Development utilities
│
├── n8n/scripts/
│   ├── workflow_manager.sh             # 🔄 Workflow management
│   └── cloud_sync.sh                   # ☁️ Cloud synchronization
│
├── notion/scripts/
│   ├── database_manager.sh             # 📊 Database operations
│   └── content_manager.sh              # 📄 Content management
│
├── hubspot/scripts/
│   ├── hubspot_manager.sh              # 🔗 HubSpot management
│   └── data_sync.sh                    # 🔄 Data synchronization
│
└── automations-mcp/scripts/
    ├── golf_server_manager.sh          # ⛳ MCP server management
    └── tools_dev.sh                    # 🔧 Tools development
```

## 🚀 Quick Start

### Master Control
```bash
# Run the master control script for overall management
./master_control.sh
```

### Individual Tool Management
```bash
# Shopify Agent Features
cd shopify/scripts && ./agent_quickstart.sh

# N8N Workflow Management
cd n8n/scripts && ./workflow_manager.sh

# Notion Database Management
cd notion/scripts && ./database_manager.sh

# HubSpot Integration
cd hubspot/scripts && ./hubspot_manager.sh

# MCP Server Management
cd automations-mcp/scripts && ./golf_server_manager.sh
```

## 📜 Script Categories

### 🏠 Master Control Scripts
- **`master_control.sh`** - Central control for all services
- **`setup_shopify_agent.sh`** - Setup script for Shopify agent features

### 🤖 Shopify Scripts
- **`agent_quickstart.sh`** - Quick start for Shopify agent features
  - Environment checks
  - Dependency installation
  - API server management
  - Testing tools

- **`store_management.sh`** - Store operations
  - Product management
  - Collection management
  - Order processing
  - Data backup

- **`dev_tools.sh`** - Development utilities
  - Shopify CLI tools
  - Authentication management
  - App/theme development

### 🔄 N8N Scripts
- **`workflow_manager.sh`** - Workflow management
  - Local N8N operations
  - Workflow validation
  - Backup/restore

- **`cloud_sync.sh`** - Cloud synchronization
  - Export/import workflows
  - Bidirectional sync
  - Automated scheduling

### 📊 Notion Scripts
- **`database_manager.sh`** - Database operations
  - Database analysis
  - Documentation generation
  - Structure validation

- **`content_manager.sh`** - Content management
  - Pages and blocks management
  - Content organization
  - Inventory generation

### 🔗 HubSpot Scripts
- **`hubspot_manager.sh`** - HubSpot management
  - Authentication
  - MCP server control
  - Integration testing

- **`data_sync.sh`** - Data synchronization
  - Export/import operations
  - Cross-platform sync
  - Automated scheduling

### ⛳ MCP Scripts
- **`golf_server_manager.sh`** - MCP server management
  - Server lifecycle
  - Configuration management
  - Testing and debugging

- **`tools_dev.sh`** - Tools development
  - Tool creation templates
  - Testing and validation
  - Performance analysis

## 🎯 Common Operations

### Start All Services
```bash
./master_control.sh
# Choose option 1: Start all services
```

### Check System Health
```bash
./master_control.sh
# Choose option 12: Health check all integrations
```

### Backup Everything
```bash
./master_control.sh
# Choose option 11: Backup all data
```

### Test Shopify Agent
```bash
cd shopify/scripts
./agent_quickstart.sh
# Choose option 2: Test API
```

### Sync N8N Workflows
```bash
cd n8n/scripts
./cloud_sync.sh
# Choose option 1: Export from cloud
```

### Generate Notion Documentation
```bash
cd notion/scripts
./database_manager.sh
# Choose option 2: Generate documentation
```

## 🔧 Environment Setup

### Required Environment Variables

**Shopify:**
```bash
export SHOPIFY_CATALOG_API_TOKEN="your_catalog_token"
export SHOPIFY_STORE_URL="https://your-store.myshopify.com"
export SHOPIFY_ACCESS_TOKEN="your_access_token"
```

**HubSpot:**
```bash
export HUBSPOT_ACCESS_TOKEN="your_hubspot_token"
```

**Notion:**
```bash
export NOTION_TOKEN="your_notion_token"
```

**N8N:**
```bash
export N8N_CLOUD_INSTANCE_URL="your_n8n_instance"
export N8N_USER_EMAIL="your_email"
export N8N_API_KEY="your_n8n_api_key"
```

**GitHub:**
```bash
export GITHUB_TOKEN="your_github_token"
```

## 📋 Script Features

### ✅ All Scripts Include:
- **Environment validation** - Check required variables
- **Dependency checking** - Verify installations
- **Error handling** - Graceful failure management
- **Logging** - Operation tracking
- **Help text** - Clear usage instructions
- **Interactive menus** - User-friendly operation

### 🛡️ Safety Features:
- **Backup creation** - Before destructive operations
- **Confirmation prompts** - For critical actions
- **Rollback options** - Undo capabilities
- **Status checking** - Service health monitoring

## 📊 Monitoring & Logs

### Log Locations:
```
logs/
├── mcp.log              # MCP server logs
├── hubspot.log          # HubSpot MCP logs
├── shopify_agent.log    # Shopify agent logs
├── n8n.log              # N8N logs
└── health_check_*.txt   # Health check reports
```

### Backup Locations:
```
backups/
├── full_backup_*/       # Complete system backups
├── notion_*/           # Notion-specific backups
├── workflows_*/        # N8N workflow backups
└── shopify_*/          # Shopify configuration backups
```

## 🚀 Advanced Usage

### Automated Operations
Scripts support automation through:
- **Silent mode** - Non-interactive execution
- **Configuration files** - Predefined settings
- **Cron job templates** - Scheduled operations
- **Exit codes** - Script chaining

### Integration Examples
```bash
# Chain operations
./master_control.sh && cd shopify/scripts && ./agent_quickstart.sh

# Automated backup
crontab -e
# Add: 0 2 * * * /path/to/master_control.sh 11

# Health monitoring
watch -n 300 ./master_control.sh 4
```

## 🆘 Troubleshooting

### Common Issues:

1. **Permission Denied**
   ```bash
   chmod +x script_name.sh
   ```

2. **Missing Dependencies**
   ```bash
   ./master_control.sh
   # Choose option 10: Update all dependencies
   ```

3. **Service Not Starting**
   ```bash
   ./master_control.sh
   # Choose option 4: Check all service status
   ```

4. **Environment Variables**
   ```bash
   # Check your .env files or export manually
   env | grep -E "(SHOPIFY|HUBSPOT|NOTION|N8N|GITHUB)"
   ```

## 📚 Documentation Links

- **Shopify Agent**: `/shopify/agent/README.md`
- **N8N Integration**: `/n8n/n8n_README.md`
- **Notion Setup**: `/notion/notion_README.md`
- **HubSpot Integration**: `/hubspot/hubspot_README.md`
- **MCP Tools**: `/automations-mcp/README.md`

---

🎉 **Your automation hub is now fully organized with comprehensive script management!**
