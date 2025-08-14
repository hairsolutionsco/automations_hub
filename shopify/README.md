# Shopify Development Environment

A comprehensive Shopify development workspace following industry best practices for e-commerce development, theme management, and app creation.

## 🏗️ Project Structure

```
shopify/
├── 📁 apps/                     # Shopify Apps
│   └── shopify-agent/          # AI-enhanced shopping agent
├── 📁 themes/                  # Theme Development
│   ├── current_theme/          # → Live theme (ecomus)
│   ├── horizon_theme/          # → Development theme  
│   ├── ecomus_theme_*/         # Live Ecomus theme
│   └── horizon_theme_*/        # Horizon 2025 theme
├── 📁 extensions/              # Shopify Extensions
├── 📁 components/              # Reusable Components
│   └── agent-interface.html    # Agent UI component
├── 📁 data/                    # Data & Backups
│   └── store_backups/          # Complete store import
│       └── imported_data/      # Products, collections, etc.
├── 📁 tools/                   # Development Tools
│   └── scripts/                # Import & management scripts
├── 📁 config/                  # Configuration Files
│   ├── .env.store             # Store configuration
│   └── requirements.txt       # Python dependencies
├── 📁 docs/                    # Documentation
│   ├── shopify_README.md      # Main documentation
│   ├── shopify_examples.md    # Usage examples
│   ├── IMPORT_SUMMARY.md      # Import documentation
│   └── DEVELOPMENT_README.md  # Development guide
├── 📄 package.json             # Node.js dependencies & scripts
├── 📄 package-lock.json        # Locked dependencies
└── 🔗 shopify-cli              # Quick CLI access
```

## 🚀 Quick Start

### 1. **Store Data Available**
✅ **Complete import ready**: 184 products, 19 collections, 42 pages, 3,941 customers
📁 **Location**: `data/store_backups/imported_data/`

### 2. **Themes Ready for Development**
✅ **Live Theme**: Ecomus v1.9.1 (394 files) - `themes/current_theme/`
✅ **Dev Theme**: Horizon 2025 (367 files) - `themes/horizon_theme/`

### 3. **Development Tools**
```bash
# Quick CLI access
./shopify-cli import           # Import store data
./shopify-cli dev-server       # Start development server
./shopify-cli sync push        # Push theme changes

# Or via npm scripts
npm run import:all             # Import everything
npm run theme:dev              # Start theme dev server
npm run theme:deploy           # Deploy to store
```

## 🛠️ Development Workflows

### **Theme Development**
- **Live Theme Customization**: Modify `themes/current_theme/`
- **Modern Theme Testing**: Experiment with `themes/horizon_theme/`
- **A/B Testing**: Compare themes before deploying

### **App Development**
- **Shopify Agent**: AI-enhanced shopping in `apps/shopify-agent/`
- **Custom Extensions**: Add new functionality in `extensions/`

### **Data Analysis**
- **Store Analytics**: Use `data/store_backups/` for insights
- **Cross-Platform Integration**: Connect with N8N, Notion, HubSpot

## 📊 Available Data

- **Products**: 184 items with full details, variants, images
- **Collections**: 19 collections (smart + custom)
- **Pages**: 42 content pages with HTML
- **Customers**: 3,941 customer records (anonymized)
- **Orders**: Recent transaction data
- **Themes**: Complete live + development themes

## 🔧 Configuration

- **Store**: one-head-hair.myshopify.com
- **Environment**: Fully configured with API access
- **Themes**: Live (Ecomus) + Development (Horizon) ready
- **Tools**: Import scripts, CLI, development server

## 📚 Documentation

- **Main Guide**: `docs/shopify_README.md`
- **Examples**: `docs/shopify_examples.md`  
- **Import Details**: `docs/IMPORT_SUMMARY.md`
- **Development**: `docs/DEVELOPMENT_README.md`

---

🎯 **Enterprise-ready Shopify development environment** with complete store data, modern themes, and professional tooling.
