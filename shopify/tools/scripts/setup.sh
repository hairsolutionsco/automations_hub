#!/bin/bash
"""
Shopify Development Environment Setup Script
"""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Setting up Shopify Development Environment${NC}"
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "shopify_cli.py" ]; then
    echo -e "${RED}❌ Please run this script from the shopify/scripts directory${NC}"
    exit 1
fi

# Install Python dependencies
echo -e "${YELLOW}📦 Installing Python dependencies...${NC}"
pip install -r ../../config/requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Dependencies installed successfully${NC}"
else
    echo -e "${RED}❌ Failed to install dependencies${NC}"
    exit 1
fi

# Make scripts executable
echo -e "${YELLOW}🔧 Making scripts executable...${NC}"
chmod +x shopify_cli.py
chmod +x shopify_importer.py
chmod +x theme_sync.py
chmod +x theme_dev_server.py

# Create a convenient symlink in the parent directory
echo -e "${YELLOW}🔗 Creating convenient CLI access...${NC}"
cd ../..
if [ -L "shopify-cli" ]; then
    rm shopify-cli
fi
ln -s tools/scripts/shopify_cli.py shopify-cli
chmod +x shopify-cli

echo -e "${GREEN}✅ Setup completed successfully!${NC}"
echo ""
echo -e "${BLUE}📁 New Shopify Structure (Following Best Practices):${NC}"
echo "├── apps/           # Shopify apps & extensions"
echo "├── themes/         # Theme development"
echo "├── components/     # Reusable components"
echo "├── data/           # Store backups & data"
echo "├── tools/          # Development scripts"
echo "├── config/         # Configuration files"
echo "└── docs/           # Documentation"
echo ""
echo -e "${BLUE}📋 Quick Start Guide:${NC}"
echo "===================="
echo ""
echo "1. Set your Shopify credentials (if not already set):"
echo -e "   ${YELLOW}export SHOPIFY_STORE_URL=\"one-head-hair.myshopify.com\"${NC}"
echo -e "   ${YELLOW}export SHOPIFY_ADMIN_API_ACCESS_TOKEN=\"your-access-token\"${NC}"
echo ""
echo "2. Import all your store data and themes:"
echo -e "   ${YELLOW}./shopify-cli import${NC}"
echo ""
echo "3. Set up a development environment:"
echo -e "   ${YELLOW}./shopify-cli setup-dev my_theme${NC}"
echo ""
echo "4. Start the development server:"
echo -e "   ${YELLOW}./shopify-cli dev-server${NC}"
echo ""
echo "5. Work on your theme files, and sync changes:"
echo -e "   ${YELLOW}./shopify-cli sync push${NC}    # Push changes to Shopify"
echo -e "   ${YELLOW}./shopify-cli sync pull${NC}    # Pull changes from Shopify"
echo -e "   ${YELLOW}./shopify-cli sync watch${NC}   # Auto-sync on file changes"
echo ""
echo "6. Deploy to live when ready:"
echo -e "   ${YELLOW}./shopify-cli deploy${NC}"
echo ""
echo -e "${GREEN}🎉 You're all set! Happy theme development!${NC}"
echo ""
echo "For more options, run: ./shopify-cli --help"
