# Shopify E-commerce Integration Platform

This directory contains Shopify e-commerce integration with **full read/write access** through MCP (Model Context Protocol) servers for advanced AI-enhanced e-commerce automation and store management.

## 🎉 **FULLY IMPORTED STORE DATA & THEMES**

**✅ COMPLETE IMPORT SUCCESSFUL**: Your entire Shopify store has been imported and is ready for development!

### 📊 **Imported Store Data** (One Head Hair - one-head-hair.myshopify.com)
- **184 Products** with full details, variants, and images
- **19 Collections** (smart + custom collections)
- **42 Pages** with content and HTML
- **3,941 Customers** (anonymized for privacy)
- **Recent Orders** (last 30 days)
- **Blog Posts** from 2 blogs

**Location**: `/shopify/imported_data/` (251 total files)

### 🎨 **Downloaded Themes**
#### **Live Theme**: Ecomus v1.9.1 Official ⭐
- **Currently Active** on your store
- **394 files** complete download
- **Location**: `/shopify/themes/current_theme/` (symlink)
- **Full Path**: `/shopify/themes/ecomus_theme_136180629665/`

#### **Development Theme**: Horizon 2025 🆕
- **Free Shopify 2025 theme** for testing/development
- **367 files** complete download
- **Location**: `/shopify/themes/horizon_theme/` (symlink)
- **Full Path**: `/shopify/themes/horizon_theme_138366222497/`

### 🚀 **Development Ready**
- **Theme Development**: Both themes ready for local customization
- **Store Data Analysis**: Complete data set for insights and optimization
- **Cross-Platform Integration**: All data available for N8N, Notion, HubSpot workflows
- **Backup & Recovery**: Complete store backup in JSON format

**Documentation**: See `IMPORT_SUMMARY.md` for complete details

## 🔑 Access & Permissions via MCP

**IMPORTANT**: This environment provides complete Shopify e-commerce capabilities through:
- **Golf MCP Server**: Custom Shopify tools integrated into multi-platform server
- **Direct Store Access**: Full product, collection, order, and customer management
- **Real-Time Operations**: Live inventory updates and order processing
- **Cross-Platform Sync**: Seamless data flow between Shopify, HubSpot, Notion, and N8N

## 🚀 Quick Start for New Agents

### ✅ Environment Verification (Already Confirmed)
- **Shopify CLI**: ✅ INSTALLED and FUNCTIONAL (@shopify/cli v3.69.0)
- **MCP Integration**: ✅ Golf MCP server provides direct Shopify API access
- **Store Management**: ✅ Full CRUD operations on products, collections, orders
- **Cross-Platform Tools**: ✅ HubSpot, Notion, N8N integrations operational
- **Theme Development**: ✅ Complete theme development and deployment tools

## 📋 **Current State Summary**
- **Store Data**: ✅ FULLY IMPORTED (184 products, 19 collections, 42 pages)
- **Live Theme**: ✅ DOWNLOADED (Ecomus v1.9.1 - 394 files)
- **Dev Theme**: ✅ DOWNLOADED (Horizon 2025 - 367 files)
- **MCP Tools**: ✅ Custom Shopify API tools in Golf MCP server
- **CLI Access**: ✅ Complete Shopify CLI functionality available
- **Store Operations**: ✅ Product management, collection handling, order processing
- **Development Tools**: ✅ READY - Theme dev, app development, liquid templating
- **API Integration**: ✅ CONFIGURED - Private app access tokens supported

### ⚡ No Need to Re-verify
- Shopify CLI installation (confirmed working)
- MCP server connectivity (Golf MCP operational with Shopify tools)
- Store access capabilities (full API operations available)
- Cross-platform integrations (all systems ready)

### 🎯 Current Project Status
- **Phase 1**: Shopify Platform Setup ✅ COMPLETED
- **Phase 2**: MCP Integration ✅ OPERATIONAL (Custom tools)
- **Phase 3**: Cross-Platform Tools ✅ READY
- **Phase 4**: E-commerce Automation ✅ AVAILABLE

### 🔄 **Available for Immediate Use**
All systems operational and ready for:
- **Complete store data analysis** and insights generation
- **Theme development and customization** with both live and modern themes
- **Cross-platform customer and order synchronization** using imported data
- **Advanced inventory management automation** with real-time data
- **Sales analytics workflows** using comprehensive historical data
- **A/B testing** between Ecomus (live) and Horizon (modern) themes

### 🤖 NEW: Shopify Agent Features (Early Access)
- **Catalog Search**: Search across hundreds of millions of products
- **Universal Cart**: Multi-merchant shopping cart management
- **Checkout Kit**: Branded, compliant checkout experiences
- **Web Components**: Rich, interactive product displays
- **AI Commerce**: Native shopping for AI conversations

**Status**: Ready for setup (requires Shopify early access approval)
**Location**: `/shopify/agent/` directory
**Documentation**: See `/shopify/agent/README.md`

---

## 🛠️ **Import Tools & Scripts**

### **Comprehensive Store Importer**
**Script**: `scripts/shopify_importer.py`
- **Purpose**: Import all store data and themes
- **Features**: Rate limiting, pagination, error handling
- **Output**: JSON files for all store entities

```bash
python scripts/shopify_importer.py
```

### **Theme-Specific Importers**
- **Ecomus Theme**: `scripts/import_ecomus_theme.py`
- **Horizon Theme**: `scripts/import_horizon_theme.py`
- **Custom Themes**: Modifiable scripts for any theme

### **Development CLI**
**Script**: `shopify-cli` (symlink to `scripts/shopify_cli.py`)
```bash
./shopify-cli import        # Import all data
./shopify-cli dev-server    # Start development server
./shopify-cli sync push     # Push theme changes
./shopify-cli sync pull     # Pull theme changes
./shopify-cli deploy        # Deploy to live
```

### **Setup & Environment**
**Script**: `scripts/setup.sh`
- Installs Python dependencies
- Creates convenient CLI access
- Prepares development environment

---

## Setup

The Shopify CLI is installed locally using renamed configuration files:
- `shopify_package.json` - Shopify dependencies and scripts
- `shopify_package-lock.json` - Locked dependency versions

## Authentication

Before using Shopify tools, authenticate with:
```bash
npm run login
```

Check authentication status:
```bash
npm run whoami
```

Logout:
```bash
npm run logout
```

## CLI Usage

### **Store Data Management**
```bash
npm run import:all        # Import complete store data and themes
npm run import:products   # Import products only
npm run import:themes     # Import themes only
npm run import:horizon    # Import Horizon theme specifically
```

### **Theme Development**
```bash
npm run theme:dev     # Start theme development server
npm run theme:build   # Build theme
npm run theme:deploy  # Deploy theme
npm run theme:pull    # Pull theme from store
npm run theme:push    # Push theme to store
npm run theme:list    # List themes
npm run theme:watch   # Auto-sync theme changes
```

### App Development
```bash
npm run app:dev       # Start app development server
npm run app:build     # Build the app
npm run app:deploy    # Deploy the app
npm run app:generate  # Generate app components
```

### Theme Development
```bash
npm run theme:dev     # Start theme development server
npm run theme:build   # Build theme
npm run theme:deploy  # Deploy theme
npm run theme:pull    # Pull theme from store
npm run theme:list    # List themes
```

### Admin Operations
```bash
npm run product:list    # List products
npm run collection:list # List collections
npm run order:list      # List orders
npm run customer:list   # List customers
```

## MCP Server Integration

Shopify functionality is **fully integrated** into the Golf MCP server with custom API tools:

### Available MCP Tools
- **get_shopify_products()** - Retrieve products from store with filtering options
- **get_shopify_collections()** - Retrieve collections and smart collections
- **create_shopify_product()** - Create new products with variants and options
- **create_shopify_collection()** - Create new collections with smart rules
- **update_shopify_collection()** - Update existing collection properties

### AI-Enhanced E-commerce Operations
Through the MCP server, AI agents can:
- Analyze product performance and suggest optimizations
- Automate inventory management and restocking
- Create personalized product recommendations
- Generate marketing content and product descriptions
- Process orders and manage customer lifecycle automation

## Directory Structure

- `products/` - Product management and configurations
- `collections/` - Collection management and smart collection rules
- `web_components/` - Custom web components, themes, and liquid templates
- `shopify_examples.md` - Sample product templates and configurations

## Cross-Platform Integration Points

### With HubSpot
- Customer synchronization between platforms
- Order data flowing to CRM for sales tracking
- Customer lifecycle management and follow-up automation

### With Notion
- Inventory tracking in Notion databases
- Product catalog documentation and management
- Sales analytics and reporting dashboards

### With N8N
- Automated order processing workflows
- Inventory alerts and restocking automation
- Customer communication and marketing automation

## Environment Variables

Set these for full API functionality:
- `SHOPIFY_STORE_URL` - Your store URL (e.g., https://your-store.myshopify.com)
- `SHOPIFY_ACCESS_TOKEN` - Private app access token

### Creating a Private App

1. Go to your Shopify admin → Apps → App and sales channel settings
2. Click "Develop apps for your store"
3. Create a private app with the necessary permissions:
   - **Products**: Read and write
   - **Collections**: Read and write
   - **Orders**: Read and write
   - **Customers**: Read and write
4. Copy the access token to your environment variables

## Advanced Features

### Liquid Theme Development
- Real-time theme editing with `npm run theme:dev`
- Custom section and block development
- Advanced templating and component architecture

### App Development
- Shopify app scaffolding and development
- Custom admin interfaces and functionality
- Webhook handling and API integrations

### Metafield Management
- Custom product and customer data fields
- Advanced product configuration options
- Personalization and customization features

---

**🎯 Ready for enterprise-grade e-commerce automation**: Complete Shopify integration with AI-enhanced operations and cross-platform synchronization capabilities.
