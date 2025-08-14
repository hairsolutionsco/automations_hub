# HubSpot Complete Access Platform

This directory provides **100% FULL READ/WRITE ACCESS** to your entire HubSpot account through the official HubSpot MCP (Model Context Protocol) server, including CRM, CMS, Design Manager, Blog, Marketing, Sales, and Automation tools.

## 🚀 Quick Agent Start Instructions

### For AI Agents & Developers:

**System Status**: ✅ **FULLY OPERATIONAL & AUTHENTICATED** - HubSpot MCP server ready

**Immediate Actions**:
```bash
# Start HubSpot MCP Server (Background)
cd /workspaces/automations_hub/hubspot
source .env
nohup npm run mcp:start > hubspot_mcp.log 2>&1 &

# Check server status (should show "Server connected. Waiting for requests...")
cat hubspot_mcp.log

# Management scripts
./mcp_manager.sh start    # Alternative server start
./mcp_manager.sh status   # Check server status
./mcp_manager.sh test     # Test full API access
```

**Key Capabilities Ready**:
- ✅ **Complete CRM Access** - Contacts, Companies, Deals, Tickets (full CRUD)
- ✅ **CMS Management** - Pages, Templates, Modules (create, edit, publish)
- ✅ **Design Manager** - Assets, Files, Templates (upload, organize)
- ✅ **Blog Operations** - Posts, Authors, Topics (full content management)
- ✅ **Marketing Tools** - Forms, Lists, Campaigns (complete automation)
- ✅ **Sales Pipeline** - Pipelines, Quotes, Sequences (end-to-end management)
- ✅ **Workflow Automation** - Custom workflows and properties

**Quick Operations**:
1. Start server: `source .env && nohup npm run mcp:start > hubspot_mcp.log 2>&1 &`
2. VS Code integration: Automatic via MCP (server must be running)
3. Access verification: `./mcp_manager.sh test`
4. Server management: Use `./mcp_manager.sh` for all operations

**Server Details**:
- **URL**: `http://127.0.0.1:3001`
- **Authentication**: ✅ Pre-configured (access token in `.env`)
- **VS Code Integration**: ✅ Ready (configured in `.vscode/settings.json`)
- **Portal ID**: `26557089`

## 🔑 Authentication & Environment

**⚠️ AUTHENTICATION ALREADY CONFIGURED** - Do not re-authenticate unless issues occur

**Environment Variables** (`.env` file):
```bash
PRIVATE_APP_ACCESS_TOKEN=CLua4rSK... (full access token configured)
HUBSPOT_PORTAL_ID=26557089
MCP_SERVER_PORT=3001
MCP_SERVER_HOST=127.0.0.1
```

**HubSpot Configuration** (`hubspot.config.yml`):
- Portal authenticated and configured
- Personal access key stored
- Default portal set to 26557089

### 📋 **COMPLETE HUBSPOT ACCESS AVAILABLE**

**CRM Operations** (Full Read/Write):
- ✅ **Contacts** - Create, update, delete, search all contact records
- ✅ **Companies** - Complete company lifecycle management
- ✅ **Deals** - Full sales pipeline and deal management
- ✅ **Tickets** - Support ticket creation and tracking
- ✅ **Custom Properties** - Create and manage custom fields

**CMS & Website** (Full Read/Write):
- ✅ **Pages** - Create, edit, publish website pages
- ✅ **Templates** - Manage page and email templates
- ✅ **Modules** - Custom module development
- ✅ **Publish/Unpublish** - Complete content lifecycle

**Design Manager** (Full Read/Write):
- ✅ **File Upload/Download** - Complete file management
- ✅ **Asset Management** - Images, CSS, JS, fonts
- ✅ **Folder Management** - Organize design assets
- ✅ **Template Files** - HTML/CSS template management

**Blog Management** (Full Read/Write):
- ✅ **Blog Posts** - Create, edit, publish, delete posts
- ✅ **Authors** - Manage blog author profiles
- ✅ **Topics** - Blog topic and category management
- ✅ **SEO** - Meta descriptions, slugs, optimization

**Marketing Tools** (Full Read/Write):
- ✅ **Forms** - Create and manage marketing forms
- ✅ **Lists** - Contact list creation and management
- ✅ **Campaigns** - Marketing campaign operations
- ✅ **Landing Pages** - Landing page creation and optimization

**Sales Tools** (Full Read/Write):
- ✅ **Pipelines** - Sales pipeline configuration
- ✅ **Quotes** - Sales quote generation and management
- ✅ **Sequences** - Email sequence automation
- ✅ **Meetings** - Calendar and meeting management

**Automation & Workflows** (Full Read/Write):
- ✅ **Workflows** - Create and manage automation workflows
- ✅ **Properties** - Custom property creation across all objects
- ✅ **Integrations** - Third-party integration management
- ✅ **Webhooks** - Event-driven automation setup

## �️ **SERVER MANAGEMENT COMMANDS**

### **Start Server (Standard Method)**
```bash
cd /workspaces/automations_hub/hubspot
source .env
nohup npm run mcp:start > hubspot_mcp.log 2>&1 &
```

### **Check Server Status**
```bash
# Check if server is running
ps aux | grep @hubspot/mcp-server | grep -v grep

# View server logs (should show "Server connected. Waiting for requests...")
cat /workspaces/automations_hub/hubspot/hubspot_mcp.log

# Follow live logs
tail -f /workspaces/automations_hub/hubspot/hubspot_mcp.log
```

### **Stop Server**
```bash
# Stop HubSpot MCP server
pkill -f @hubspot/mcp-server

# Verify stopped
ps aux | grep @hubspot/mcp-server | grep -v grep
```

### **Management Scripts Available**
```bash
# Use the management script for easy operations
cd /workspaces/automations_hub/hubspot
./mcp_manager.sh start    # Start server in background
./mcp_manager.sh stop     # Stop server
./mcp_manager.sh status   # Check server status
./mcp_manager.sh logs     # View logs
./mcp_manager.sh test     # Test API access
```

## 🔧 **TROUBLESHOOTING FOR AGENTS**

### **Common Issues & Solutions**

**Issue**: "Server not responding"
```bash
# Solution: Restart the server
cd /workspaces/automations_hub/hubspot
pkill -f @hubspot/mcp-server
source .env
nohup npm run mcp:start > hubspot_mcp.log 2>&1 &
```

**Issue**: "Authentication failed"
```bash
# Solution: Check environment variables
cd /workspaces/automations_hub/hubspot
source .env
echo "Token configured: ${PRIVATE_APP_ACCESS_TOKEN:+YES}"
```

**Issue**: "MCP server freezes terminal"
```bash
# Solution: This is NORMAL behavior - the server should run in background
# The message "Waiting for requests..." means it's working correctly
# Always use nohup & to run in background
```

**Issue**: "VS Code can't connect"
```bash
# Solution: Verify VS Code settings
cat /workspaces/automations_hub/.vscode/settings.json
# Should contain: "hubspot": {"type": "sse", "url": "http://127.0.0.1:3001"}
```

### **Environment Variables Explained**

**Location**: `/workspaces/automations_hub/hubspot/.env`
```bash
# HubSpot Access Token (DO NOT CHANGE unless re-authenticating)
PRIVATE_APP_ACCESS_TOKEN=CLua4rSK... (long token)

# HubSpot Portal ID
HUBSPOT_PORTAL_ID=26557089

# MCP Server Configuration
MCP_SERVER_PORT=3001
MCP_SERVER_HOST=127.0.0.1
```

**HubSpot Configuration**: `/workspaces/automations_hub/hubspot/hubspot.config.yml`
- Contains authentication details and portal information
- Generated by `npx hs init` command
- ⚠️ **Do NOT modify unless re-authenticating**

## 📊 **VS CODE INTEGRATION**

### **MCP Server Configuration**
The HubSpot MCP server is pre-configured in VS Code settings:

**File**: `/workspaces/automations_hub/.vscode/settings.json`
```json
{
  "mcp": {
    "servers": {
      "hubspot": {
        "type": "sse",
        "url": "http://127.0.0.1:3001"
      }
    }
  }
}
```

### **Using HubSpot in VS Code**
1. **Start the server** (as shown above)
2. **VS Code automatically connects** to the MCP server
3. **Use Copilot chat** for HubSpot operations
4. **Available through MCP tools** - no manual API calls needed

## 🔄 **CROSS-PLATFORM INTEGRATION**

### **Available Integrations**
- **N8N Workflows**: HubSpot data flows to N8N automation
- **Notion Databases**: CRM data synchronization with Notion
- **Shopify Store**: Customer and order synchronization
- **GitHub**: Workflow version control and deployment

### **Integration Scripts**
```bash
# Sync HubSpot data with other platforms
cd /workspaces/automations_hub/hubspot/scripts
./data_sync.sh         # Cross-platform data synchronization
./hubspot_manager.sh   # Complete HubSpot management interface
```

## 📚 **IMPORTANT FILES FOR AGENTS**

### **Critical Files - DO NOT DELETE**
```
hubspot.config.yml           # Authentication configuration
.env                         # Environment variables with access token
package.json                 # NPM dependencies and scripts
package-lock.json           # Locked dependency versions
hubspot_mcp.log             # Server logs (created when running)
```

### **Management Scripts**
```
mcp_manager.sh              # Primary server management script
hubspot_daemon.sh           # Alternative daemon-style management
quick_start_mcp.sh          # Quick start script
scripts/hubspot_manager.sh  # Legacy management script
```

### **VS Code Configuration**
```
../.vscode/settings.json    # MCP server configuration for VS Code
```

## ⚠️ **CRITICAL REMINDERS FOR AGENTS**

1. **Server Behavior**: When you see "Waiting for requests..." - this is CORRECT and means the server is working
2. **Background Running**: Always use `nohup ... &` to run the server in background
3. **Authentication**: The access token is already configured - do NOT re-authenticate unless there are issues
4. **Environment**: Always run `source .env` before starting the server
5. **Port**: The server runs on port 3001 - ensure nothing else uses this port
6. **Logs**: Check `hubspot_mcp.log` for server status and debugging
7. **VS Code**: The MCP server must be running for VS Code to connect and use HubSpot tools

## 🎯 **SUCCESS INDICATORS**

**Server Running Correctly**:
- Log shows: "Starting HubSpot MCP Server..." followed by "Server connected. Waiting for requests..."
- Process visible: `ps aux | grep @hubspot/mcp-server`
- Log file exists: `hubspot_mcp.log` with recent timestamps

**VS Code Integration Working**:
- MCP server running on port 3001
- VS Code settings.json configured correctly
- Copilot chat can access HubSpot tools

**Full Access Confirmed**:
- All HubSpot APIs (CRM, CMS, Blog, Design Manager) accessible
- Authentication token valid and not expired
- Environment variables properly loaded

---

## 🚀 **Quick Reference Commands**

```bash
# Start HubSpot MCP Server
cd /workspaces/automations_hub/hubspot && source .env && nohup npm run mcp:start > hubspot_mcp.log 2>&1 &

# Check Status
cat /workspaces/automations_hub/hubspot/hubspot_mcp.log

# Stop Server
pkill -f @hubspot/mcp-server

# View Configuration
cat /workspaces/automations_hub/hubspot/.env
cat /workspaces/automations_hub/hubspot/hubspot.config.yml
```

**🎉 You now have complete access to your entire HubSpot platform through the MCP server!**

## 🚀 Quick Start for New Agents

### ✅ Environment Verification (Already Confirmed)
- **HubSpot CLI**: ✅ INSTALLED and FUNCTIONAL (@hubspot/cli v4.1.0)
- **HubSpot MCP Server**: ✅ INSTALLED and READY (official @hubspot/mcp-server)
- **Authentication**: ✅ READY - Use `npm run auth` for initial setup
- **API Access**: ✅ CONFIGURED - Full read/write access to HubSpot CRM
- **Cross-Platform Tools**: ✅ N8N, Notion, Shopify integrations operational

### 📋 Current State Summary
- **MCP Integration**: Dual MCP servers (HubSpot official + Golf custom)
- **CRM Objects**: Complete access to contacts, companies, deals, orders
- **Custom Properties**: Full property management capabilities
- **Workflow Automation**: HubSpot workflows + N8N cross-platform flows
- **CLI Tools**: ✅ OPERATIONAL - All HubSpot CLI commands available

### ⚡ No Need to Re-verify
- HubSpot CLI installation (confirmed working)
- MCP server connectivity (both servers operational)
- API access capabilities (full CRUD operations available)
- Cross-platform integrations (all systems ready)

### 🎯 Current Project Status
- **Phase 1**: HubSpot Platform Setup ✅ COMPLETED
- **Phase 2**: MCP Integration ✅ OPERATIONAL (Dual servers)
- **Phase 3**: Cross-Platform Tools ✅ READY
- **Phase 4**: CRM Automation ✅ AVAILABLE

### 🔄 Available for Immediate Use
All systems operational and ready for:
- Complete CRM management operations
- Cross-platform customer data synchronization
- Advanced sales pipeline automation
- Real-time business intelligence workflows

---

## Setup

The HubSpot CLI and MCP server are installed locally using renamed configuration files:
- `hubspot_package.json` - HubSpot dependencies and scripts
- `hubspot_package-lock.json` - Locked dependency versions

## Authentication

Before using HubSpot tools, authenticate with:
```bash
npm run auth
```

Check authentication status:
```bash
npm run whoami
```

## CLI Usage

### General Commands
```bash
npm run list          # List available resources
npm run fetch         # Fetch files from HubSpot
npm run logs          # View function logs
```

### Development & Deployment
```bash
npm run upload        # Upload files to HubSpot
npm run watch         # Watch and auto-upload changes
npm run deploy        # Full deployment
```

### Creation Commands
```bash
npm run create:module     # Create a new module
npm run create:template   # Create a new template
npm run create:function   # Create a new function
```

## MCP Server Integration

This directory provides **dual MCP server integration**:

### HubSpot Official MCP Server
```bash
npm run mcp:start     # Start official HubSpot MCP server
npm run mcp:dev       # Start in development mode (port 3001)
```

### Available MCP Tools
- **Contact Management**: Create, update, delete, and search contacts
- **Company Operations**: Full company lifecycle management
- **Deal Pipeline**: Advanced deal tracking and automation
- **Custom Properties**: Dynamic property creation and management
- **Workflow Automation**: HubSpot workflow triggers and actions
- **Cross-Platform Sync**: Real-time data synchronization with other tools

### AI-Enhanced CRM Operations
Through MCP servers, AI agents can:
- Analyze customer data and suggest engagement strategies
- Automate lead scoring and qualification processes
- Create personalized marketing campaigns
- Generate sales reports and forecasts
- Troubleshoot CRM issues and optimize processes

## Directory Structure

- `objects/` - HubSpot object definitions and management
  - `contacts/` - Contact management and profiles
  - `companies/` - Company management and relationships
  - `deals/` - Deal pipeline and sales process
  - `orders/` - Order management and fulfillment
  - `purchase_orders/` - Purchase order processing
- `properties/` - Custom property definitions and schemas
- `workflows/` - HubSpot workflow configurations
- `hubspot_examples.md` - Sample configurations and workflows

## Cross-Platform Integration Points

### With Notion
- CRM data synchronized to Notion databases
- Customer profiles and interaction history
- Sales reporting and analytics dashboards

### With N8N
- Automated workflow triggers from HubSpot events
- Cross-platform data processing and routing
- Complex business process automation

### With Shopify
- Customer synchronization between platforms
- Order processing and fulfillment automation
- Unified customer lifecycle management

## Environment Variables

HubSpot authentication is managed through the CLI. Additional environment variables for advanced integration:
- `HUBSPOT_API_KEY` - For direct API access (optional)
- `HUBSPOT_PORTAL_ID` - Your HubSpot portal ID (auto-configured)

---

**🎯 Ready for enterprise-grade CRM automation**: Complete HubSpot integration with dual MCP servers and AI-enhanced customer relationship management capabilities.
