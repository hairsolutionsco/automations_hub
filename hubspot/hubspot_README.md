# HubSpot CRM Integration Platform

This directory contains HubSpot CRM integration with **full read/write access** through MCP (Model Context Protocol) servers for advanced AI-enhanced customer relationship management and sales automation.

## 🔑 Access & Permissions via MCP

**IMPORTANT**: This environment provides complete HubSpot CRM capabilities through:
- **HubSpot MCP Server**: Official HubSpot MCP server with direct API access
- **Golf MCP Server**: Additional HubSpot tools and cross-platform integrations
- **Real-Time CRM Operations**: Live contact, company, deal, and order management
- **Cross-Platform Sync**: Seamless data flow between HubSpot, Notion, N8N, and Shopify

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
