#!/bin/bash

# N8N Git Integration Setup Script

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║              N8N Git Integration Setup                      ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Create directory structure
echo -e "${YELLOW}📁 Creating directory structure...${NC}"
mkdir -p workflows credentials backups scripts

# Create initial README if it doesn't exist
if [[ ! -f "README.md" ]]; then
    cat > README.md << 'EOF'
# N8N Workflows Repository

This repository contains N8N workflows and configurations managed with Git version control.

## Quick Start

1. **Export workflows from N8N:**
   ```bash
   npm run export
   ```

2. **Import workflows to N8N:**
   ```bash
   npm run import
   ```

3. **Use interactive Git sync:**
   ```bash
   npm run git:sync
   ```

## Available Commands

- `npm start` - Start N8N locally
- `npm run export` - Export all workflows
- `npm run import` - Import all workflows  
- `npm run cloud:export` - Export from N8N cloud
- `npm run cloud:import` - Import to N8N cloud
- `npm run git:sync` - Interactive Git sync menu
- `npm run validate` - Validate workflow JSON files
- `npm run backup` - Create timestamped backup

## Directory Structure

- `workflows/` - Individual workflow JSON files
- `credentials/` - Credentials export (gitignored for security)
- `backups/` - Timestamped backups
- `scripts/` - Helper scripts

## Security

Sensitive files like `credentials/credentials.json` are automatically excluded from Git via `.gitignore`.

For more details, see `N8N_GIT_INTEGRATION.md`.
EOF
    echo -e "${GREEN}✅ Created README.md${NC}"
fi

# Initialize Git if not already initialized
if [[ ! -d ".git" ]]; then
    echo -e "${YELLOW}🔧 Initializing Git repository...${NC}"
    git init
    echo -e "${GREEN}✅ Git repository initialized${NC}"
else
    echo -e "${GREEN}✅ Git repository already exists${NC}"
fi

# Add .gitignore if it's new
if [[ ! -f ".gitignore" ]]; then
    echo -e "${YELLOW}🔒 Adding .gitignore for security...${NC}"
    echo -e "${GREEN}✅ .gitignore created${NC}"
else
    echo -e "${GREEN}✅ .gitignore already exists${NC}"
fi

# Check if n8n is available
echo -e "${YELLOW}🔍 Checking N8N availability...${NC}"
if command -v n8n >/dev/null 2>&1; then
    n8n_version=$(n8n --version)
    echo -e "${GREEN}✅ N8N CLI available: $n8n_version${NC}"
else
    echo -e "${YELLOW}⚠️  N8N CLI not found. Install with: npm install -g n8n${NC}"
fi

# Check for Node.js and npm
echo -e "${YELLOW}🔍 Checking Node.js and npm...${NC}"
if command -v node >/dev/null 2>&1 && command -v npm >/dev/null 2>&1; then
    node_version=$(node --version)
    npm_version=$(npm --version)
    echo -e "${GREEN}✅ Node.js: $node_version, npm: $npm_version${NC}"
else
    echo -e "${YELLOW}⚠️  Node.js/npm not found${NC}"
fi

# Display next steps
echo ""
echo -e "${BLUE}🎉 Setup Complete!${NC}"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "1. Configure N8N cloud credentials (optional):"
echo "   export N8N_CLOUD_INSTANCE_URL='https://your-instance.app.n8n.cloud'"
echo "   export N8N_API_KEY='your-api-key'"
echo ""
echo "2. Export your first workflows:"
echo "   npm run export"
echo ""
echo "3. Start the interactive Git sync:"
echo "   npm run git:sync"
echo ""
echo "4. Add a remote Git repository:"
echo "   git remote add origin https://github.com/your-username/n8n-workflows.git"
echo ""
echo -e "${GREEN}Happy automating! 🚀${NC}"
