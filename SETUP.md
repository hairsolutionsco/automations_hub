# Setup Guide - Automation Hub

## 🚀 Initial Setup (One-time)

### 1. Install Dependencies
All platform CLIs are already installed in their respective directories. If needed:
```bash
# Install all dependencies
cd n8n && npm install
cd ../hubspot && npm install  
cd ../shopify && npm install
cd ../automations-mcp && npm install
```

### 2. Authenticate with Platforms

#### HubSpot
```bash
npm run hubspot:auth
# Follow the prompts to authenticate with your HubSpot account
```

#### Shopify  
```bash
npm run shopify:auth
# Follow the prompts to authenticate with your Shopify store
```

#### Environment Variables
Create a `.env` file in the root directory:
```bash
# Shopify (if using API directly)
SHOPIFY_STORE_URL=https://your-store.myshopify.com
SHOPIFY_ACCESS_TOKEN=your-private-app-token

# N8N Cloud (optional)
N8N_CLOUD_INSTANCE_URL=https://your-instance.app.n8n.cloud
N8N_USER_EMAIL=your-email@example.com
N8N_API_KEY=your-api-key

# Notion is already configured ✅
```

## 🔧 Daily Workflow

### Starting Your Automation Environment

1. **Start all MCP servers**:
   ```bash
   npm run mcp:start:all
   ```

2. **Start N8N** (in a new terminal):
   ```bash
   npm run n8n:start
   ```

3. **Access N8N**: Open http://localhost:5678 in your browser

### Working with Workflows

1. **Create workflows** in N8N UI
2. **Export to version control**:
   ```bash
   npm run n8n:export
   git add n8n/workflows/
   git commit -m "Add new workflow"
   ```

3. **Import workflows** on new environments:
   ```bash
   npm run n8n:import
   ```

## 🎯 Platform-Specific Operations

### N8N Workflows
- **Local development**: `npm run n8n:dev` (with tunnel for webhooks)
- **Export/Import**: Use the npm scripts for version control
- **Cloud sync**: Use cloud:export/import scripts if you have N8N Cloud

### HubSpot CRM
- **MCP Server**: Automatically provides API access through Copilot
- **CLI Operations**: Use `cd hubspot && npm run <command>`
- **Custom properties**: Define in `hubspot/properties/`

### Shopify E-commerce
- **MCP Integration**: Available through Golf MCP server
- **CLI Operations**: Use `cd shopify && npm run <command>`
- **Theme development**: Use theme:dev for live editing

### Notion Database Management
- **MCP Server**: Already configured and working
- **35 databases**: Fully documented in `notion/databases/`
- **API access**: Through environment variable (already set)

## 🔍 Troubleshooting

### MCP Servers Not Starting
```bash
# Check if ports are available
lsof -i :3000  # Golf MCP
lsof -i :3001  # HubSpot MCP

# Restart individually
npm run golf:start
npm run hubspot:mcp:dev
```

### Authentication Issues
```bash
# Check authentication status
npm run hubspot:whoami
npm run shopify:whoami

# Re-authenticate if needed
npm run hubspot:auth
npm run shopify:auth
```

### N8N Connection Problems
```bash
# Check if N8N is running
curl http://localhost:5678/healthz

# Restart N8N
npm run n8n:start
```

## 📚 Next Steps

1. **Explore examples** in each platform directory
2. **Create your first cross-platform workflow** using N8N
3. **Use GitHub Copilot** with MCP servers for advanced automation
4. **Set up monitoring** and logging for your workflows

## 🆘 Getting Help

- **N8N Documentation**: https://docs.n8n.io/
- **HubSpot Developers**: https://developers.hubspot.com/
- **Shopify Developers**: https://developers.shopify.com/
- **Golf MCP**: https://docs.golf.dev/
- **Platform-specific README files** in each directory

---

**🎉 You're ready to automate your entire business stack!**
