# Automation Hub - Multi-Platform Integration

A comprehensive automation hub integrating **N8N**, **Notion**, **HubSpot**, and **Shopify** with advanced Model Context Protocol (MCP) servers for AI-enhanced operations and cross-platform data synchronization.

## 🚀 Quick Start

1. **Open in GitHub Codespaces** (recommended)
2. **Install dependencies**: All CLIs are pre-configured per platform
3. **Start MCP servers**:
   ```bash
   npm run mcp:start:all
   ```
4. **Start N8N**:
   ```bash
   npm run n8n:start
   ```

## 🏗️ Project Structure

```
automation-hub/
├── n8n/                          # N8N Automation Platform
│   ├── workflows/                # Workflow JSON definitions
│   ├── n8n_package.json         # N8N CLI and scripts
│   ├── n8n_package-lock.json    # Locked dependencies
│   ├── n8n_README.md           # N8N platform documentation
│   └── n8n_examples.md         # Sample workflows
├── notion/                       # Notion Workspace Integration
│   ├── databases/               # Database documentation (35 databases)
│   ├── pages/                   # Page management
│   ├── blocks/                  # Block-level operations
│   └── notion_README.md        # Notion platform documentation
├── hubspot/                      # HubSpot CRM Integration
│   ├── objects/                 # CRM Object management
│   │   ├── contacts/
│   │   ├── companies/
│   │   ├── deals/
│   │   ├── orders/
│   │   └── purchase_orders/
│   ├── properties/              # Custom properties
│   ├── workflows/               # HubSpot workflows
│   ├── hubspot_package.json    # HubSpot CLI and MCP server
│   ├── hubspot_package-lock.json
│   ├── hubspot_README.md       # HubSpot platform documentation
│   └── hubspot_examples.md     # Sample configurations
├── shopify/                      # Shopify E-commerce Integration  
│   ├── products/                # Product management
│   ├── collections/             # Collection management
│   ├── web_components/          # Theme components
│   ├── shopify_package.json    # Shopify CLI
│   ├── shopify_package-lock.json
│   ├── shopify_README.md       # Shopify platform documentation
│   └── shopify_examples.md     # Sample configurations
└── automations-mcp/             # Golf MCP Server (Multi-tool)
    ├── tools/                   # MCP tools for all platforms
    │   ├── shopify/            # Shopify API tools
    │   ├── github_user.py      # GitHub integration
    │   ├── notion_api.py       # Notion tools
    │   └── n8n_workflows.py    # N8N management
    ├── resources/              # MCP resources
    ├── prompts/                # AI prompts
    └── golf.json              # MCP server config
```

## 🛠️ Platform Management

### N8N Workflow Automation
```bash
npm run n8n:start         # Start N8N locally
npm run n8n:dev          # Start with tunnel for webhooks
npm run n8n:export       # Export workflows to JSON
npm run n8n:import       # Import workflows from JSON
```

### HubSpot CRM Operations
```bash
npm run hubspot:auth       # Authenticate with HubSpot
npm run hubspot:whoami     # Check auth status  
npm run hubspot:mcp:start  # Start HubSpot MCP server
```

### Shopify E-commerce
```bash
npm run shopify:auth       # Authenticate with Shopify
npm run shopify:whoami     # Check auth status
```

### Golf MCP Multi-Tool Server
```bash
npm run golf:build         # Build the MCP server
npm run golf:run          # Run the MCP server
npm run golf:start        # Build and run
```

## 🔌 MCP Server Configuration

All MCP servers are configured in `.vscode/settings.json`:

| Server | URL | Purpose |
|--------|-----|---------|
| **GitHub MCP** | `https://api.githubcopilot.com/mcp/` | Repository management, PRs, issues |
| **Notion MCP** | `https://mcp.notion.com/mcp` | Database & page operations (35 databases) |
| **Golf MCP** | `http://127.0.0.1:3000` | Multi-tool server (N8N, Shopify, custom tools) |
| **HubSpot MCP** | `http://127.0.0.1:3001` | CRM operations, deals, contacts |

### Start All MCP Servers
```bash
npm run mcp:start:all      # Starts Golf + HubSpot MCP servers concurrently
```

## 🎯 Key Features

### ⚡ AI-Enhanced Operations
- **Direct API access** through MCP servers
- **No manual API key management** in Copilot chat
- **Advanced automation workflows** with N8N
- **Real-time synchronization** across platforms

### 🔄 Cross-Platform Integration
- **N8N ↔ Notion**: Workflow data to databases
- **HubSpot ↔ Shopify**: Customer/order synchronization  
- **GitHub ↔ All Platforms**: Version control for configurations
- **Unified automation** across your entire stack

### 📊 Business Intelligence
- **35 Notion databases** fully documented and accessible
- **HubSpot CRM data** with automated workflows
- **Shopify e-commerce** metrics and management
- **Automated reporting** through N8N workflows

## � Authentication Setup

### Required Environment Variables

**Notion** (already configured):
- `NOTION_API_KEY` ✅ 

**HubSpot**:
- Configure via: `npm run hubspot:auth`

**Shopify**:
- `SHOPIFY_STORE_URL` (e.g., https://your-store.myshopify.com)
- `SHOPIFY_ACCESS_TOKEN` (Private app token)
- Configure via: `npm run shopify:auth`

**N8N Cloud** (optional):
- `N8N_CLOUD_INSTANCE_URL`
- `N8N_USER_EMAIL` 
- `N8N_API_KEY`

## 📚 Platform Documentation

Each platform directory contains comprehensive documentation with "Quick Start for New Agents" sections:

- **[n8n/n8n_README.md](./n8n/n8n_README.md)** - Workflow automation platform
- **[notion/notion_README.md](./notion/notion_README.md)** - Database operations (35 databases verified)
- **[hubspot/hubspot_README.md](./hubspot/hubspot_README.md)** - CRM automation and customer management
- **[shopify/shopify_README.md](./shopify/shopify_README.md)** - E-commerce tools and store management
- **[automations-mcp/golf_README.md](./automations-mcp/golf_README.md)** - Multi-platform MCP server

### Platform-Specific Examples
- **[n8n/n8n_examples.md](./n8n/n8n_examples.md)** - Sample workflows and automation patterns
- **[hubspot/hubspot_examples.md](./hubspot/hubspot_examples.md)** - CRM configurations and workflows
- **[shopify/shopify_examples.md](./shopify/shopify_examples.md)** - E-commerce templates and configurations

## 🚀 Advanced Usage Examples

### Creating Cross-Platform Automations
1. **Design workflow** in N8N UI connecting multiple platforms
2. **Export to JSON**: `npm run n8n:export` for version control
3. **Deploy**: `npm run n8n:import` on new environments
4. **Monitor**: Real-time workflow execution through MCP

### Using MCP with AI Agents
- **Natural Language Operations**: "Create a HubSpot contact and sync to Notion"
- **Complex Workflows**: "Process Shopify orders through HubSpot to Notion reporting"
- **Data Analysis**: "Analyze customer lifecycle across all platforms"
- **Optimization**: "Suggest workflow improvements based on performance data"

## 🔄 Cross-Platform Data Synchronization

### Real-Time Integration Flows
- **Shopify → HubSpot → Notion**: Customer journey tracking across platforms
- **N8N Orchestration**: Automated workflows connecting all systems
- **Unified Customer Profiles**: Complete customer view across all touchpoints
- **Business Intelligence**: Aggregated analytics and reporting

### AI-Enhanced Operations
Through MCP servers, AI agents can:
- **Analyze Performance**: Cross-platform metrics and optimization opportunities
- **Automate Processes**: Complex multi-step business workflows
- **Generate Insights**: Real-time business intelligence and forecasting
- **Maintain Data Quality**: Automatic synchronization and validation
- Example: "Export N8N workflow and document it in Notion"

---

**🎯 Ready for enterprise-grade automation**: Complete integration of your business stack with AI-enhanced operations and version-controlled workflows.
