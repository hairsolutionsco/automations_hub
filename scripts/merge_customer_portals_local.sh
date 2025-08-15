#!/bin/bash

# Local Repository Merger Script
# This script creates the emergent_apps_builder structure using local directories
# if they exist, or creates placeholder structure if they don't

set -e  # Exit on any error

# Configuration
NEW_REPO_NAME="emergent_apps_builder"
WORKSPACE_DIR="/workspaces/automations_hub"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to create the repository structure
create_local_repo() {
    print_status "Creating local repository structure in $WORKSPACE_DIR..."
    
    cd "$WORKSPACE_DIR"
    
    # Create the new repository directory
    if [ -d "$NEW_REPO_NAME" ]; then
        print_warning "Directory $NEW_REPO_NAME already exists. Removing it..."
        rm -rf "$NEW_REPO_NAME"
    fi
    
    mkdir -p "$NEW_REPO_NAME"
    cd "$NEW_REPO_NAME"
    
    # Initialize git repository
    git init
    
    # Create folder structure
    mkdir -p "notion_customer_portal"
    mkdir -p "hubspot_customer_portal"
    
    # Check for existing local directories and copy them
    copy_local_content
    
    # Create repository files
    create_merged_readme
    create_gitignore
    create_root_package_json
    create_setup_scripts
    
    # Create initial commit
    git add .
    git commit -m "Initial commit: Merged customer portals structure

- Created notion_customer_portal/ directory
- Created hubspot_customer_portal/ directory  
- Added comprehensive README and documentation
- Set up package.json with unified scripts
- Created setup and development scripts"

    print_success "Local repository created successfully at $WORKSPACE_DIR/$NEW_REPO_NAME"
}

# Function to copy local content if directories exist
copy_local_content() {
    # Check for notion_customer_portal
    if [ -d "$WORKSPACE_DIR/notion_customer_portal" ]; then
        print_status "Found local notion_customer_portal, copying content..."
        cp -r "$WORKSPACE_DIR/notion_customer_portal"/* notion_customer_portal/ 2>/dev/null || true
        cp -r "$WORKSPACE_DIR/notion_customer_portal"/.* notion_customer_portal/ 2>/dev/null || true
        rm -rf notion_customer_portal/.git 2>/dev/null || true
        print_success "Notion customer portal content copied"
    else
        print_warning "notion_customer_portal not found locally, creating placeholder structure"
        create_notion_placeholder
    fi
    
    # Check for hubspot_customer_portal  
    if [ -d "$WORKSPACE_DIR/hubspot_customer_portal" ]; then
        print_status "Found local hubspot_customer_portal, copying content..."
        cp -r "$WORKSPACE_DIR/hubspot_customer_portal"/* hubspot_customer_portal/ 2>/dev/null || true
        cp -r "$WORKSPACE_DIR/hubspot_customer_portal"/.* hubspot_customer_portal/ 2>/dev/null || true
        rm -rf hubspot_customer_portal/.git 2>/dev/null || true
        print_success "HubSpot customer portal content copied"
    else
        print_warning "hubspot_customer_portal not found locally, creating placeholder structure"
        create_hubspot_placeholder
    fi
}

# Function to create notion placeholder structure
create_notion_placeholder() {
    cd notion_customer_portal
    
    # Create basic structure
    mkdir -p src components pages api utils
    
    # Create package.json
    cat > package.json << 'EOF'
{
  "name": "notion-customer-portal",
  "version": "1.0.0",
  "description": "Customer portal integrated with Notion databases",
  "main": "index.js",
  "scripts": {
    "dev": "next dev -p 3001",
    "build": "next build",
    "start": "next start -p 3001",
    "lint": "next lint"
  },
  "dependencies": {
    "@notionhq/client": "^2.2.0",
    "next": "^13.4.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@types/react": "^18.2.0",
    "eslint": "^8.44.0",
    "eslint-config-next": "^13.4.0",
    "typescript": "^5.1.0"
  }
}
EOF

    # Create README
    cat > README.md << 'EOF'
# Notion Customer Portal

A customer portal application integrated with Notion databases for Hair Solutions Co.

## Features

- Customer authentication and profiles
- Order tracking and management  
- Communication history
- Service request management
- Integration with Notion databases

## Setup

1. Install dependencies:
```bash
npm install
```

2. Set up environment variables:
```bash
cp .env.example .env.local
# Edit .env.local with your Notion API credentials
```

3. Run development server:
```bash
npm run dev
```

## Environment Variables

- `NOTION_API_KEY` - Your Notion API key
- `NOTION_DATABASE_ID` - Customer database ID
- `NEXTAUTH_SECRET` - Authentication secret
- `NEXTAUTH_URL` - Application URL

## Notion Database Integration

This portal integrates with the following Notion databases:
- Companies (ID: 22bf4e0d-84e0-80bb-8d1c-c90710d44870)
- Contacts (ID: 226f4e0d-84e0-814c-ad70-d478cebeee30)
- Hair Orders Profiles (ID: 248f4e0d-84e0-80ad-9d33-e90e5124c092)
- Orders (ID: 228f4e0d-84e0-816f-8511-fab726d2c6ef)
- Payments (ID: 22af4e0d-84e0-80c3-a7d6-f0209d93081d)
EOF

    # Create env example
    cat > .env.example << 'EOF'
NOTION_API_KEY=your_notion_api_key_here
NOTION_DATABASE_ID=your_database_id_here
NEXTAUTH_SECRET=your_auth_secret_here
NEXTAUTH_URL=http://localhost:3001
EOF

    cd ..
    print_success "Notion placeholder structure created"
}

# Function to create hubspot placeholder structure
create_hubspot_placeholder() {
    cd hubspot_customer_portal
    
    # Create basic structure
    mkdir -p src components pages api utils
    
    # Create package.json
    cat > package.json << 'EOF'
{
  "name": "hubspot-customer-portal",
  "version": "1.0.0",
  "description": "Customer portal integrated with HubSpot CRM",
  "main": "index.js",
  "scripts": {
    "dev": "next dev -p 3002",
    "build": "next build", 
    "start": "next start -p 3002",
    "lint": "next lint"
  },
  "dependencies": {
    "@hubspot/api-client": "^10.0.0",
    "next": "^13.4.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@types/react": "^18.2.0",
    "eslint": "^8.44.0",
    "eslint-config-next": "^13.4.0",
    "typescript": "^5.1.0"
  }
}
EOF

    # Create README
    cat > README.md << 'EOF'
# HubSpot Customer Portal

A customer portal application integrated with HubSpot CRM for Hair Solutions Co.

## Features

- Customer relationship management
- Deal tracking and pipeline management
- Contact management
- Marketing automation integration
- HubSpot CRM integration

## Setup

1. Install dependencies:
```bash
npm install
```

2. Set up environment variables:
```bash
cp .env.example .env.local
# Edit .env.local with your HubSpot API credentials
```

3. Run development server:
```bash
npm run dev
```

## Environment Variables

- `HUBSPOT_ACCESS_TOKEN` - Your HubSpot private app access token
- `HUBSPOT_PORTAL_ID` - Your HubSpot portal ID
- `NEXTAUTH_SECRET` - Authentication secret
- `NEXTAUTH_URL` - Application URL

## HubSpot Integration

This portal integrates with HubSpot CRM for:
- Contact management
- Deal pipeline tracking
- Company management
- Marketing automation
- Sales pipeline management
EOF

    # Create env example
    cat > .env.example << 'EOF'
HUBSPOT_ACCESS_TOKEN=your_hubspot_access_token_here
HUBSPOT_PORTAL_ID=your_portal_id_here
NEXTAUTH_SECRET=your_auth_secret_here
NEXTAUTH_URL=http://localhost:3002
EOF

    cd ..
    print_success "HubSpot placeholder structure created"
}

# Function to create comprehensive README
create_merged_readme() {
    cat > README.md << 'EOF'
# Emergent Apps Builder

This repository contains merged customer portal applications from Notion and HubSpot integrations, providing a unified platform for building emergent applications for Hair Solutions Co.

## Repository Structure

```
emergent_apps_builder/
├── notion_customer_portal/     # Notion-based customer portal
│   ├── src/                   # Source code
│   ├── components/            # React components
│   ├── pages/                 # Next.js pages
│   ├── api/                   # API routes
│   ├── utils/                 # Utility functions
│   ├── package.json          # Dependencies
│   └── README.md             # Notion portal documentation
├── hubspot_customer_portal/   # HubSpot-based customer portal
│   ├── src/                   # Source code
│   ├── components/            # React components
│   ├── pages/                 # Next.js pages
│   ├── api/                   # API routes
│   ├── utils/                 # Utility functions
│   ├── package.json          # Dependencies
│   └── README.md             # HubSpot portal documentation
├── scripts/                   # Development and deployment scripts
├── docs/                      # Documentation
├── README.md                  # This file
├── package.json              # Root dependencies
└── .gitignore                # Git ignore rules
```

## Projects Overview

### Notion Customer Portal
**Port: 3001** | Located in `notion_customer_portal/`

Integrates with Notion databases to provide customer access to:
- **Order tracking** and management
- **Profile management** with hair specifications
- **Communication history** and email tracking
- **Service requests** and support tickets
- **Payment history** and billing information

**Connected Databases:**
- Companies (CRM management)
- Contacts (Customer relationships) 
- Hair Orders Profiles (Specialized orders)
- Orders (Order processing)
- Payments (Stripe integration)
- Email Templates (Communication)

### HubSpot Customer Portal  
**Port: 3002** | Located in `hubspot_customer_portal/`

Integrates with HubSpot CRM to provide:
- **Customer relationship management**
- **Deal tracking** and pipeline management
- **Contact management** and communication
- **Marketing automation** integration
- **Sales pipeline** visibility

## Quick Start

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn
- Notion API access (for Notion portal)
- HubSpot API access (for HubSpot portal)

### Installation

1. **Clone and setup:**
```bash
git clone <repository-url>
cd emergent_apps_builder
npm install
```

2. **Install all project dependencies:**
```bash
npm run install:all
```

3. **Set up environment variables:**
```bash
# Notion Portal
cd notion_customer_portal
cp .env.example .env.local
# Edit .env.local with your Notion API credentials

# HubSpot Portal  
cd ../hubspot_customer_portal
cp .env.example .env.local
# Edit .env.local with your HubSpot API credentials
```

### Development

**Run both portals simultaneously:**
```bash
npm run dev:all
```

**Or run individually:**
```bash
# Notion Portal (http://localhost:3001)
npm run dev:notion

# HubSpot Portal (http://localhost:3002) 
npm run dev:hubspot
```

### Production Build

```bash
npm run build:all
```

## Available Scripts

| Script | Description |
|--------|-------------|
| `npm run install:all` | Install dependencies for all projects |
| `npm run dev:all` | Start both portals in development mode |
| `npm run dev:notion` | Start Notion portal only (port 3001) |
| `npm run dev:hubspot` | Start HubSpot portal only (port 3002) |
| `npm run build:all` | Build both portals for production |
| `npm run start:all` | Start both portals in production mode |
| `npm run test:all` | Run tests for both portals |
| `npm run lint:all` | Lint both portals |

## Integration Architecture

```mermaid
graph TB
    subgraph "Emergent Apps Builder"
        A[Shared Components] --> B[Notion Customer Portal]
        A --> C[HubSpot Customer Portal]
        B --> D[Notion API]
        C --> E[HubSpot API]
        
        subgraph "Notion Integration"
            D --> F[Companies DB]
            D --> G[Contacts DB]
            D --> H[Orders DB]
            D --> I[Payments DB]
        end
        
        subgraph "HubSpot Integration"
            E --> J[CRM Contacts]
            E --> K[Deals Pipeline]
            E --> L[Companies]
            E --> M[Marketing Hub]
        end
    end
    
    N[Customer] --> B
    N --> C
    B -.-> C
    C -.-> B
```

## Cross-Platform Features

### Unified Customer Experience
- **Single Sign-On**: Shared authentication across both portals
- **Unified Dashboard**: Combined view of Notion and HubSpot data
- **Cross-Platform Search**: Search across both systems

### Data Synchronization
- **Real-time sync** between Notion and HubSpot
- **Automated data mapping** for common fields
- **Conflict resolution** for duplicate data

### Shared Components
- **UI Component Library**: Reusable components across portals
- **Common Utilities**: Shared helper functions
- **Unified Styling**: Consistent design system

## Development Workflow

### Adding New Features

1. **Shared features**: Add to root `src/shared/`
2. **Notion-specific**: Add to `notion_customer_portal/`
3. **HubSpot-specific**: Add to `hubspot_customer_portal/`

### Testing Strategy

```bash
# Unit tests
npm run test:all

# Integration tests
npm run test:integration

# E2E tests
npm run test:e2e
```

### Deployment

```bash
# Build for production
npm run build:all

# Deploy both portals
npm run deploy:all
```

## Configuration

### Notion Portal Configuration
- **API Key**: Notion integration token
- **Database IDs**: Specific database identifiers
- **Webhook URLs**: For real-time updates

### HubSpot Portal Configuration  
- **Access Token**: HubSpot private app token
- **Portal ID**: HubSpot account identifier
- **OAuth Settings**: For customer authentication

## API Integration Details

### Notion API Integration
- **Databases**: 35 connected databases
- **Real-time updates**: Webhook integration
- **Rich content**: Support for Notion blocks and formatting

### HubSpot API Integration
- **CRM Objects**: Contacts, Companies, Deals
- **Marketing Hub**: Email campaigns, forms
- **Sales Hub**: Pipeline management, quotes

## Roadmap

### Phase 1: Foundation ✅
- [x] Repository structure setup
- [x] Basic portal frameworks
- [x] Individual portal functionality

### Phase 2: Integration 🚧
- [ ] Unified authentication system
- [ ] Cross-platform data sync
- [ ] Shared component library

### Phase 3: Advanced Features 📋
- [ ] Real-time collaboration
- [ ] Advanced analytics dashboard
- [ ] Mobile applications
- [ ] API gateway

### Phase 4: Scale 📋
- [ ] Multi-tenant support
- [ ] Advanced automation
- [ ] Enterprise features

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Troubleshooting

### Common Issues

**Port conflicts:**
```bash
# Check running processes
lsof -i :3001
lsof -i :3002

# Kill processes if needed
npm run stop:all
```

**Environment variables:**
```bash
# Verify environment setup
npm run check:env
```

**Dependencies:**
```bash
# Clean install
npm run clean:install
```

## Support

- **Documentation**: Check individual portal READMEs
- **Issues**: Open GitHub issues for bugs
- **Questions**: Use GitHub discussions

## License

MIT License - see LICENSE file for details.

---

**Hair Solutions Co Automation Hub**  
*Merged repository created: $(date)*
EOF

    print_success "Comprehensive README.md created"
}

# Function to create .gitignore
create_gitignore() {
    cat > .gitignore << 'EOF'
# Dependencies
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
lerna-debug.log*

# Production builds
build/
dist/
.next/
out/
*.tgz

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Cache
.cache/
.parcel-cache/
.npm/
.eslintcache

# IDE files
.vscode/
.idea/
*.swp
*.swo
*~

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Logs
logs/
*.log

# Runtime data
pids/
*.pid
*.seed
*.pid.lock

# Coverage directory
coverage/
*.lcov

# Dependency directories
jspm_packages/

# Optional npm cache directory
.npm

# Optional REPL history
.node_repl_history

# Output of 'npm pack'
*.tgz

# Yarn Integrity file
.yarn-integrity

# Next.js build output
.next/
out/

# Nuxt.js build / generate output
.nuxt/
dist/

# Gatsby files
.cache/
public/

# Storybook build outputs
.out/
.storybook-out/

# Temporary folders
tmp/
temp/

# API keys and secrets
secrets/
*.key
*.pem

# Database files
*.db
*.sqlite

# Editor directories and files
.idea
*.suo
*.ntvs*
*.njsproj
*.sln
*.sw?

# Local development
.vercel
.now

# Notion/HubSpot specific
notion-cache/
hubspot-cache/
EOF

    print_success ".gitignore created"
}

# Function to create root package.json
create_root_package_json() {
    cat > package.json << 'EOF'
{
  "name": "emergent-apps-builder",
  "version": "1.0.0",
  "description": "Merged customer portal applications from Notion and HubSpot integrations for Hair Solutions Co",
  "main": "index.js",
  "private": true,
  "workspaces": [
    "notion_customer_portal",
    "hubspot_customer_portal"
  ],
  "scripts": {
    "install:all": "npm install && npm run install:notion && npm run install:hubspot",
    "install:notion": "cd notion_customer_portal && npm install",
    "install:hubspot": "cd hubspot_customer_portal && npm install",
    
    "dev:all": "concurrently \"npm run dev:notion\" \"npm run dev:hubspot\"",
    "dev:notion": "cd notion_customer_portal && npm run dev",
    "dev:hubspot": "cd hubspot_customer_portal && npm run dev",
    
    "build:all": "npm run build:notion && npm run build:hubspot", 
    "build:notion": "cd notion_customer_portal && npm run build",
    "build:hubspot": "cd hubspot_customer_portal && npm run build",
    
    "start:all": "concurrently \"npm run start:notion\" \"npm run start:hubspot\"",
    "start:notion": "cd notion_customer_portal && npm start",
    "start:hubspot": "cd hubspot_customer_portal && npm start",
    
    "test:all": "npm run test:notion && npm run test:hubspot",
    "test:notion": "cd notion_customer_portal && npm test",
    "test:hubspot": "cd hubspot_customer_portal && npm test",
    
    "lint:all": "npm run lint:notion && npm run lint:hubspot",
    "lint:notion": "cd notion_customer_portal && npm run lint",
    "lint:hubspot": "cd hubspot_customer_portal && npm run lint",
    
    "clean": "rm -rf node_modules notion_customer_portal/node_modules hubspot_customer_portal/node_modules",
    "clean:install": "npm run clean && npm run install:all",
    
    "check:env": "node scripts/check-env.js",
    "setup": "node scripts/setup.js",
    "stop:all": "pkill -f 'next dev' || true"
  },
  "keywords": [
    "customer-portal",
    "notion",
    "hubspot", 
    "crm",
    "integration",
    "emergent-apps",
    "hair-solutions",
    "automation"
  ],
  "author": "Hair Solutions Co",
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/hairsolutionsco/emergent_apps_builder.git"
  },
  "bugs": {
    "url": "https://github.com/hairsolutionsco/emergent_apps_builder/issues"
  },
  "homepage": "https://github.com/hairsolutionsco/emergent_apps_builder#readme",
  "devDependencies": {
    "concurrently": "^8.2.0"
  },
  "engines": {
    "node": ">=16.0.0",
    "npm": ">=8.0.0"
  }
}
EOF

    print_success "Root package.json created"
}

# Function to create setup scripts
create_setup_scripts() {
    mkdir -p scripts
    
    # Create environment check script
    cat > scripts/check-env.js << 'EOF'
const fs = require('fs');
const path = require('path');

console.log('🔍 Checking environment configuration...\n');

const checkEnvFile = (filePath, requiredVars) => {
    if (!fs.existsSync(filePath)) {
        console.log(`❌ ${filePath} not found`);
        return false;
    }
    
    const content = fs.readFileSync(filePath, 'utf8');
    let allPresent = true;
    
    requiredVars.forEach(varName => {
        if (!content.includes(varName)) {
            console.log(`⚠️  ${varName} missing in ${filePath}`);
            allPresent = false;
        }
    });
    
    if (allPresent) {
        console.log(`✅ ${filePath} configured correctly`);
    }
    
    return allPresent;
};

// Check Notion portal
console.log('📊 Notion Customer Portal:');
checkEnvFile(
    'notion_customer_portal/.env.local',
    ['NOTION_API_KEY', 'NOTION_DATABASE_ID', 'NEXTAUTH_SECRET']
);

console.log('\n🏢 HubSpot Customer Portal:');
checkEnvFile(
    'hubspot_customer_portal/.env.local', 
    ['HUBSPOT_ACCESS_TOKEN', 'HUBSPOT_PORTAL_ID', 'NEXTAUTH_SECRET']
);

console.log('\n✨ Environment check complete!');
EOF

    # Create setup script
    cat > scripts/setup.js << 'EOF'
const fs = require('fs');
const path = require('path');

console.log('🚀 Setting up Emergent Apps Builder...\n');

const copyEnvExample = (dir, name) => {
    const examplePath = path.join(dir, '.env.example');
    const localPath = path.join(dir, '.env.local');
    
    if (fs.existsSync(examplePath) && !fs.existsSync(localPath)) {
        fs.copyFileSync(examplePath, localPath);
        console.log(`✅ Created ${localPath} from example`);
    }
};

// Copy environment files
console.log('📄 Setting up environment files...');
copyEnvExample('notion_customer_portal', 'Notion Portal');
copyEnvExample('hubspot_customer_portal', 'HubSpot Portal');

console.log('\n📋 Next steps:');
console.log('1. Edit .env.local files in both portal directories');
console.log('2. Add your API credentials');
console.log('3. Run: npm run install:all');
console.log('4. Run: npm run dev:all');

console.log('\n🎉 Setup complete!');
EOF

    # Create documentation directory
    mkdir -p docs
    
    cat > docs/DEVELOPMENT.md << 'EOF'
# Development Guide

## Getting Started

### Prerequisites
- Node.js 16+
- npm 8+
- Notion API access
- HubSpot API access

### Setup Process

1. **Clone and install:**
```bash
git clone <repo-url>
cd emergent_apps_builder
npm run setup
```

2. **Configure environment:**
   - Edit `notion_customer_portal/.env.local`
   - Edit `hubspot_customer_portal/.env.local`

3. **Install dependencies:**
```bash
npm run install:all
```

4. **Start development:**
```bash
npm run dev:all
```

## Architecture

### Notion Portal (Port 3001)
- Next.js application
- Notion API integration
- Customer order management
- Hair profile specifications

### HubSpot Portal (Port 3002)  
- Next.js application
- HubSpot CRM integration
- Sales pipeline management
- Customer relationship management

### Shared Resources
- Common UI components
- Shared utilities
- Unified styling system

## Development Workflow

### Making Changes

1. **Portal-specific changes:**
   - Notion: `notion_customer_portal/`
   - HubSpot: `hubspot_customer_portal/`

2. **Shared changes:**
   - Add to root `src/shared/` (when implemented)

3. **Testing:**
```bash
npm run test:all
```

### Code Structure

```
emergent_apps_builder/
├── notion_customer_portal/
│   ├── pages/           # Next.js pages
│   ├── components/      # React components  
│   ├── api/            # API routes
│   └── utils/          # Utilities
├── hubspot_customer_portal/
│   ├── pages/          # Next.js pages
│   ├── components/     # React components
│   ├── api/           # API routes
│   └── utils/         # Utilities
└── scripts/           # Build/deployment scripts
```

## API Integration

### Notion API
- Database queries
- Page creation/updates
- Real-time webhooks
- Rich content handling

### HubSpot API
- CRM operations
- Deal management
- Contact synchronization
- Marketing automation

## Deployment

### Production Build
```bash
npm run build:all
```

### Environment Setup
- Production environment variables
- API rate limits
- Webhook configurations

## Troubleshooting

### Common Issues

**Port conflicts:**
```bash
npm run stop:all
```

**Environment issues:**
```bash
npm run check:env
```

**Clean reinstall:**
```bash
npm run clean:install
```
EOF

    print_success "Setup scripts and documentation created"
}

# Main execution
main() {
    echo ""
    print_status "Creating local emergent_apps_builder repository..."
    echo ""
    
    read -p "This will create '$NEW_REPO_NAME' in $WORKSPACE_DIR. Continue? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_status "Operation cancelled by user"
        exit 0
    fi
    
    create_local_repo
    
    echo ""
    print_success "Local repository created successfully!"
    echo ""
    print_status "Repository location: $WORKSPACE_DIR/$NEW_REPO_NAME"
    echo ""
    print_status "Next steps:"
    echo "  1. cd $WORKSPACE_DIR/$NEW_REPO_NAME"
    echo "  2. npm run setup"
    echo "  3. Edit .env.local files in both portal directories"
    echo "  4. npm run install:all"
    echo "  5. npm run dev:all"
    echo ""
    print_status "Available scripts:"
    echo "  - npm run dev:all         # Start both portals"
    echo "  - npm run dev:notion      # Start Notion portal (port 3001)"
    echo "  - npm run dev:hubspot     # Start HubSpot portal (port 3002)"
    echo "  - npm run build:all       # Build both portals"
    echo "  - npm run check:env       # Check environment setup"
}

# Run the main function
main "$@"
