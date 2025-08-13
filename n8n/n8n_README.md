# N8N Workflow Automation Platform

This directory contains N8N automation platform integration with **full read/write access** through MCP (Model Context Protocol) servers for advanced AI-enhanced workflow automation.

## 🔑 Access & Permissions via MCP

**IMPORTANT**: This environment provides complete N8N workflow automation capabilities through:
- **Golf MCP Server**: Direct N8N workflow management and creation
- **Cross-Platform Integration**: Seamless data flow between N8N, Notion, HubSpot, and Shopify
- **Real-Time Synchronization**: Live workflow updates and monitoring
- **Version Control Integration**: Automated workflow export/import with Git

## 🚀 Quick Start for New Agents

### ✅ Environment Verification (Already Confirmed)
- **N8N CLI**: ✅ INSTALLED and FUNCTIONAL (n8n v1.106.3)
- **MCP Integration**: ✅ Golf MCP server provides direct N8N access
- **Workflow Management**: ✅ Full CRUD operations on workflows confirmed  
- **Cross-Platform Tools**: ✅ Notion, HubSpot, Shopify integrations operational
- **Local Development**: ✅ N8N server ready on http://localhost:5678

### 📋 Current State Summary
- **Workflow Storage**: `workflows/` directory with JSON definitions
- **MCP Tools**: Full workflow automation through Golf MCP server
- **CLI Access**: Complete N8N CLI functionality available
- **Version Control**: ✅ CONFIGURED - Automatic workflow sync with Git
- **Cloud Integration**: ✅ READY - N8N Cloud export/import capabilities

### ⚡ No Need to Re-verify
- N8N installation (confirmed working)
- MCP server connectivity (Golf MCP operational)
- Workflow management capabilities (all tools available)
- Cross-platform integrations (Notion, HubSpot, Shopify ready)

### 🎯 Current Project Status
- **Phase 1**: N8N Platform Setup ✅ COMPLETED
- **Phase 2**: MCP Integration ✅ OPERATIONAL
- **Phase 3**: Cross-Platform Tools ✅ READY
- **Phase 4**: Workflow Templates ✅ AVAILABLE

### 🔄 Available for Immediate Use
All systems operational and ready for:
- Creating complex automation workflows
- Cross-platform data synchronization
- Real-time workflow monitoring
- Advanced business process automation

---

## Setup

The N8N CLI is installed locally in this directory using the renamed configuration files:
- `n8n_package.json` - N8N dependencies and scripts
- `n8n_package-lock.json` - Locked dependency versions

## Usage

### Starting N8N locally
```bash
npm run start
```

### Starting N8N with tunnel (for webhooks)
```bash
npm run dev
```

### Export workflows
```bash
npm run export
```

### Import workflows
```bash
npm run import
```

### Cloud operations (requires env vars)
```bash
npm run cloud:export
npm run cloud:import
```

## MCP Integration

This directory is **fully integrated** with the Golf MCP server, providing:

### Available MCP Tools
- **Workflow Creation**: Create new N8N workflows programmatically
- **Workflow Management**: Update, delete, and monitor existing workflows
- **Cross-Platform Triggers**: Connect N8N with Notion, HubSpot, and Shopify
- **Data Synchronization**: Real-time data flow between all platforms

### AI-Enhanced Operations
Through the MCP server, AI agents can:
- Analyze workflow performance and suggest optimizations
- Create complex multi-platform automation sequences
- Troubleshoot workflow errors and provide solutions
- Generate workflow documentation automatically

## Environment Variables

For cloud operations, set these environment variables:
- `N8N_CLOUD_INSTANCE_URL`
- `N8N_USER_EMAIL`
- `N8N_API_KEY`

## Directory Structure

- `workflows/` - JSON workflow definitions
- `n8n_package.json` - N8N CLI dependencies and scripts
- `n8n_package-lock.json` - Locked dependency versions
- `n8n_examples.md` - Sample workflows and patterns

## Cross-Platform Integration Points

### With Notion
- Database triggers and updates
- Page creation and management
- Property synchronization

### With HubSpot  
- Contact and company management
- Deal pipeline automation
- Custom property updates

### With Shopify
- Order processing workflows
- Inventory management
- Customer lifecycle automation

---

**🎯 Ready for enterprise-grade workflow automation**: Complete N8N integration with AI-enhanced operations and cross-platform synchronization capabilities.
