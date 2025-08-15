# MCP Tools Directory

Collection of Model Context Protocol (MCP) tools for cross-platform automation and AI-enhanced operations.

## 🛠️ Available Tools

### Core Platform Integrations

#### `notion_api.py`
**Notion Database Management**
- Complete CRUD operations for databases, pages, and blocks
- Property analysis and schema management
- Bulk operations and data migration
- Real-time sync capabilities

```python
# Example usage
from tools.notion_api import NotionAPI
notion = NotionAPI()
databases = notion.list_databases()
```

#### `hubspot_complete.py` 
**HubSpot CRM Integration**
- Contact, company, deal, and ticket management
- Custom property creation and mapping
- Workflow automation
- Bulk import/export operations

```python
# Example usage
from tools.hubspot_complete import HubSpotAPI
hubspot = HubSpotAPI()
contacts = hubspot.get_contacts()
```

#### `n8n_workflows.py`
**N8N Workflow Management**
- Workflow import/export via REST API
- Execution monitoring and management
- Credential handling
- Template generation

```python
# Example usage
from tools.n8n_workflows import N8NWorkflows
n8n = N8NWorkflows()
workflows = n8n.list_workflows()
```

#### `shopify_agent.py`
**Shopify E-commerce Operations**
- Product and inventory management
- Order processing and fulfillment
- Customer data synchronization
- Theme and app management

```python
# Example usage
from tools.shopify_agent import ShopifyAgent
shopify = ShopifyAgent()
products = shopify.get_products()
```

#### `github_user.py`
**GitHub Integration**
- Repository management
- Issue and PR operations
- Code analysis and automation
- Version control integration

```python
# Example usage
from tools.github_user import GitHubAPI
github = GitHubAPI()
repos = github.list_repositories()
```

### Specialized Tools

#### `notion_database_management.py`
**Advanced Notion Operations**
- Database schema analysis
- Property mapping and transformation
- Relationship management
- Data validation and cleanup

#### `hello.py`
**MCP Server Test Tool**
- Connection testing
- Basic functionality verification
- Server health checks

## 🚀 Quick Start

### Setting Up MCP Tools

1. **Install Dependencies**:
```bash
cd /workspaces/automations_hub/automations-mcp
pip install -r requirements.txt
```

2. **Configure Environment**:
```bash
# Copy and configure environment variables
cp .env.example .env
# Edit .env with your API keys
```

3. **Test MCP Server**:
```bash
# Start the MCP server
python -m mcp_server

# Test with hello tool
python tools/hello.py
```

### Integration Examples

#### Notion ↔ HubSpot Sync
```python
from tools.notion_api import NotionAPI
from tools.hubspot_complete import HubSpotAPI

# Initialize APIs
notion = NotionAPI()
hubspot = HubSpotAPI()

# Sync contacts
notion_contacts = notion.query_database("contact_db_id")
for contact in notion_contacts:
    hubspot.create_or_update_contact(contact)
```

#### N8N Workflow Automation
```python
from tools.n8n_workflows import N8NWorkflows

# Deploy sync workflow
n8n = N8NWorkflows()
workflow_id = n8n.import_workflow("notion_hubspot_sync.json")
n8n.activate_workflow(workflow_id)
```

## 📁 Directory Structure

```
tools/
├── README.md                      # This file
├── notion_api.py                  # Notion database operations
├── hubspot_complete.py            # HubSpot CRM integration
├── n8n_workflows.py              # N8N workflow management
├── shopify_agent.py               # Shopify e-commerce operations
├── github_user.py                 # GitHub integration
├── notion_database_management.py  # Advanced Notion operations
├── hello.py                       # MCP test tool
├── shopify/                       # Shopify-specific tools
│   ├── product_manager.py
│   ├── order_processor.py
│   └── customer_sync.py
└── payments/                      # Payment processing tools
    ├── stripe_integration.py
    └── payment_processor.py
```

## 🔧 Configuration

### Environment Variables Required

```bash
# Notion API
NOTION_TOKEN=your_notion_token

# HubSpot API  
HUBSPOT_TOKEN=your_hubspot_token

# N8N Cloud Instance
N8N_CLOUD_INSTANCE_URL=https://your-instance.app.n8n.cloud
N8N_API_KEY=your_n8n_api_key

# Shopify API
SHOPIFY_STORE_URL=your-store.myshopify.com
SHOPIFY_ACCESS_TOKEN=your_shopify_token

# GitHub API
GITHUB_TOKEN=your_github_token
```

### MCP Server Configuration

The tools are designed to work with the Golf MCP server configuration in `../golf.json`:

```json
{
  "mcpServers": {
    "golf": {
      "command": "python",
      "args": ["-m", "mcp_server"],
      "env": {
        "NOTION_TOKEN": "your_token",
        "HUBSPOT_TOKEN": "your_token"
      }
    }
  }
}
```

## 🧪 Testing

### Run Individual Tool Tests
```bash
# Test Notion API
python tools/notion_api.py --test

# Test HubSpot integration
python tools/hubspot_complete.py --test

# Test N8N workflows
python tools/n8n_workflows.py --test
```

### Run All Tests
```bash
# Run comprehensive test suite
python -m pytest tests/
```

## 📚 Documentation

- **MCP Protocol**: See `../README.md` for MCP server setup
- **API References**: Each tool file contains detailed docstrings
- **Examples**: Check `../examples/` for usage examples
- **Troubleshooting**: See individual tool files for error handling

## 🔄 Integration with Sync Workflows

These tools power the automated sync workflows in `/n8n/workflows/`:

- **Property Analysis**: `notion_api.py` + `hubspot_complete.py`
- **Data Transformation**: All tools provide standardized data formats
- **Workflow Management**: `n8n_workflows.py` handles deployment
- **Monitoring**: Built-in health checks and status reporting

## 🎯 Best Practices

1. **Error Handling**: All tools include comprehensive error handling
2. **Rate Limiting**: Built-in respect for API rate limits
3. **Data Validation**: Input/output validation for all operations
4. **Logging**: Structured logging for debugging and monitoring
5. **Security**: Secure credential handling and data protection

## 🚀 Next Steps

1. **Review tool documentation** in individual files
2. **Set up environment variables** in `.env`
3. **Test individual tools** with your data
4. **Build custom workflows** using tool combinations
5. **Monitor and optimize** for your specific use cases

These tools provide the foundation for all automation workflows in the hub! 🎉
