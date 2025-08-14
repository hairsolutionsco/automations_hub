# 🏪 Shopify Complete Development Environment

A comprehensive development environment for importing, managing, and developing Shopify themes and store data with full sync capabilities.

## ✨ Features

- 📥 **Complete Data Import**: Import all products, collections, pages, blog posts, customers, orders, and themes
- 🎨 **Theme Development**: Local theme development with live reload and sync capabilities  
- 🔄 **Bidirectional Sync**: Push/pull changes between local and Shopify
- 👀 **File Watching**: Auto-sync changes to Shopify as you develop
- 🚀 **Development Server**: Local server with live reload for rapid development
- 💾 **Backup System**: Automatic backups before deploying to live theme
- 🛠️ **CLI Tools**: Easy-to-use command-line interface for all operations

## 🚀 Quick Start

### 1. Setup Environment

```bash
cd /workspaces/automations_hub/shopify/scripts
chmod +x setup.sh
./setup.sh
```

### 2. Configure Credentials

Set your Shopify store credentials:

```bash
export SHOPIFY_STORE_URL="one-head-hair.myshopify.com"
export SHOPIFY_ADMIN_API_ACCESS_TOKEN="shpat_your_access_token"
```

> **Note**: You can get the access token from your Shopify admin under Settings > Apps and sales channels > Develop apps

### 3. Import Everything

Import all your store data and themes:

```bash
cd /workspaces/automations_hub/shopify
./shopify-cli import
```

This will download:
- ✅ All products with variants and images
- ✅ All collections (smart and custom)
- ✅ All pages and blog posts
- ✅ Customer data (anonymized)
- ✅ Recent orders
- ✅ All themes including live theme

### 4. Set Up Development Environment

Create a development theme for safe editing:

```bash
./shopify-cli setup-dev my_development_theme
```

This creates:
- 🎯 New development theme on Shopify (copy of live theme)
- 📁 Local development directory with all theme files
- ⚙️ Development configuration
- 📖 README with development workflow

### 5. Start Developing

Start the development server with live reload:

```bash
./shopify-cli dev-server
```

Opens browser to `http://localhost:3000` with:
- 📋 Development dashboard
- 📁 File tree browser
- 🔄 Live reload functionality
- 🔗 Direct links to Shopify preview

## 🛠️ Development Workflow

### Making Changes

1. **Edit theme files** in your local development directory
2. **Save files** - changes are automatically detected
3. **Push changes** to Shopify for testing:
   ```bash
   ./shopify-cli sync push
   ```
4. **Preview changes** on your Shopify store using the preview URL
5. **Deploy to live** when ready:
   ```bash
   ./shopify-cli deploy
   ```

### Auto-Sync Development

For continuous development, use the watch mode:

```bash
./shopify-cli sync watch
```

This automatically pushes any file changes to your development theme on Shopify.

## 📁 Directory Structure

After import and setup, your directory structure will look like:

```
shopify/
├── shopify-cli                    # Main CLI tool
├── requirements.txt               # Python dependencies
├── imported_data/                 # All imported store data
│   ├── products/                  # Product data and images
│   ├── collections/              # Collection data
│   ├── pages/                    # Page content
│   ├── blogs/                    # Blog posts
│   ├── customers/                # Customer data (anonymized)
│   ├── orders/                   # Recent orders
│   └── import_summary.json       # Import summary
├── themes/                       # All themes
│   ├── live_theme_[name]_[id]/   # Your live theme
│   ├── dev_[name]_[id]/         # Development themes
│   └── current_theme             # Symlink to active development theme
└── scripts/                      # Development scripts
    ├── shopify_cli.py            # Main CLI
    ├── shopify_importer.py       # Data importer
    ├── theme_sync.py             # Theme sync tools
    ├── theme_dev_server.py       # Development server
    └── setup.sh                  # Setup script
```

## 🔧 CLI Commands

### Data Management
```bash
./shopify-cli import              # Import all store data and themes
./shopify-cli status              # Show current status
./shopify-cli list-themes         # List all themes in store
```

### Development Environment
```bash
./shopify-cli setup-dev [name]    # Set up development environment
./shopify-cli dev-server          # Start development server
./shopify-cli dev-server --port 4000  # Start on custom port
```

### Theme Synchronization
```bash
./shopify-cli sync push           # Push local changes to Shopify
./shopify-cli sync pull           # Pull changes from Shopify
./shopify-cli sync watch          # Watch and auto-sync changes
```

### Deployment
```bash
./shopify-cli deploy              # Deploy to live (with backup)
./shopify-cli deploy --no-backup  # Deploy without backup
```

## 🎨 Theme Development

### Local Development Structure

Each development theme has this structure:

```
dev_theme_name_123456/
├── assets/          # CSS, JS, images, fonts
├── config/          # Theme settings and schema
├── layout/          # Theme layouts (theme.liquid, etc.)
├── locales/         # Translation files
├── sections/        # Theme sections
├── snippets/        # Reusable code snippets
├── templates/       # Page templates
├── .dev_config.json # Development configuration
├── .gitignore       # Git ignore file
└── README.md        # Development guide
```

### Best Practices

1. **Always develop on a development theme** - never edit the live theme directly
2. **Use the development server** for rapid iteration with live reload
3. **Test changes** using the Shopify preview URL before deploying
4. **Commit changes to git** for version control
5. **Deploy during low-traffic periods** for live stores

### Live Reload Development

The development server provides:

- 🔄 **Auto-reload** when you save files
- 📱 **Responsive preview** for mobile/desktop testing
- 🔗 **Quick access** to Shopify preview
- 📊 **File change tracking** and recent changes view
- ⚡ **Fast development** cycle

## 🔐 Security & Credentials

### Required Permissions

Your Shopify private app needs these scopes:
- `read_products, write_products`
- `read_collections, write_collections`
- `read_content, write_content`
- `read_themes, write_themes`
- `read_customers` (for anonymized import)
- `read_orders` (for recent orders)

### Environment Variables

```bash
# Required
SHOPIFY_STORE_URL="one-head-hair.myshopify.com"
SHOPIFY_ADMIN_API_ACCESS_TOKEN="shpat_your_token"

# Optional
DEV_SERVER_PORT=3000              # Development server port
DEBUG=1                           # Enable debug output
```

### Credential Setup

1. Go to your Shopify admin
2. Navigate to Settings → Apps and sales channels
3. Click "Develop apps" 
4. Create a new private app
5. Configure the required scopes above
6. Generate Admin API access token
7. Set the environment variables

## 🔄 Sync Capabilities

### What Gets Synced

**From Local to Shopify (Push):**
- All theme files (Liquid templates, CSS, JS, images)
- Theme settings and configuration
- Section and snippet files

**From Shopify to Local (Pull):**
- Latest theme files
- Theme settings updates
- Changes made in the theme editor

### File Watching

The watch mode monitors these file types:
- `.liquid` - Liquid template files
- `.css`, `.scss` - Stylesheets  
- `.js` - JavaScript files
- `.json` - Configuration files
- Images and other assets

## 🚨 Deployment Safety

### Automatic Backups

Before deploying to live, the system:
1. ✅ Creates a backup copy of your live theme
2. ✅ Names it with timestamp for easy identification
3. ✅ Confirms the deployment action
4. ✅ Deploys your changes
5. ✅ Provides rollback instructions if needed

### Rollback Process

If you need to rollback:
1. Go to Shopify admin → Themes
2. Find the backup theme (named `backup_[theme_name]_[timestamp]`)
3. Click "Actions" → "Publish" to make it live

## 🐛 Troubleshooting

### Common Issues

**Import fails with authentication error:**
- Check your `SHOPIFY_ADMIN_API_ACCESS_TOKEN` is correct
- Verify your private app has the required scopes

**Development server won't start:**
- Check if port 3000 is already in use
- Try a different port: `./shopify-cli dev-server --port 4000`

**Sync fails:**
- Ensure you're in a theme directory with `.dev_config.json`
- Check your internet connection
- Verify theme ID exists on Shopify

**Live reload not working:**
- Check browser console for WebSocket errors
- Ensure development server is running
- Try refreshing the browser

### Debug Mode

Enable debug output for troubleshooting:

```bash
export DEBUG=1
./shopify-cli [command]
```

## 🎯 Advanced Usage

### Custom Theme Development

Create multiple development environments:

```bash
./shopify-cli setup-dev mobile_optimized
./shopify-cli setup-dev desktop_variant
./shopify-cli setup-dev experimental_features
```

### Batch Operations

Import and setup in one go:

```bash
./shopify-cli import && ./shopify-cli setup-dev
```

### Integration with Other Tools

The imported data can be used with:
- **Notion**: Import products/orders to Notion databases
- **HubSpot**: Sync customer and order data
- **N8N**: Create automated workflows
- **Custom Scripts**: Process exported JSON data

## 📝 Contributing

To extend this development environment:

1. **Add new importers** in `shopify_importer.py`
2. **Extend CLI commands** in `shopify_cli.py`
3. **Add new sync capabilities** in `theme_sync.py`
4. **Enhance development server** in `theme_dev_server.py`

## 📄 License

This project is part of the Automations Hub and follows the same licensing terms.

---

## 🎉 Happy Theme Development!

You now have a complete Shopify development environment that allows you to:
- Import all your store data locally
- Develop themes with live reload
- Sync changes safely
- Deploy with confidence
- Maintain version control

Start developing amazing Shopify themes! 🚀
