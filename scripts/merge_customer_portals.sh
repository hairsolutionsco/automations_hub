#!/bin/bash

# Script to merge notion_customer_portal and hubspot_customer_portal into emergent_apps_builder
# This script will create a new repository with two folders containing the merged content

set -e  # Exit on any error

# Configuration
NEW_REPO_NAME="emergent_apps_builder"
NOTION_REPO="notion_customer_portal"
HUBSPOT_REPO="hubspot_customer_portal"
GITHUB_OWNER="hairsolutionsco"  # Adjust this to your GitHub username/organization

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

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    if ! command_exists git; then
        print_error "Git is not installed. Please install Git first."
        exit 1
    fi
    
    if ! command_exists gh; then
        print_error "GitHub CLI is not installed. Please install gh first."
        exit 1
    fi
    
    # Check if user is authenticated with GitHub CLI
    if ! gh auth status >/dev/null 2>&1; then
        print_error "You are not authenticated with GitHub CLI. Please run 'gh auth login' first."
        exit 1
    fi
    
    print_success "All prerequisites met!"
}

# Function to clone repositories
clone_repositories() {
    print_status "Cloning repositories..."
    
    # Create temporary directory for the merge operation
    TEMP_DIR="/tmp/repo_merge_$$"
    mkdir -p "$TEMP_DIR"
    cd "$TEMP_DIR"
    
    # Clone notion_customer_portal
    print_status "Cloning $NOTION_REPO..."
    if gh repo clone "$GITHUB_OWNER/$NOTION_REPO" notion_temp; then
        print_success "Successfully cloned $NOTION_REPO"
    else
        print_warning "Failed to clone $NOTION_REPO from GitHub. Checking if it exists locally..."
        if [ -d "/workspaces/automations_hub/$NOTION_REPO" ]; then
            print_status "Found local copy of $NOTION_REPO, copying..."
            cp -r "/workspaces/automations_hub/$NOTION_REPO" notion_temp
        else
            print_error "Could not find $NOTION_REPO repository. Please check the repository name and permissions."
            exit 1
        fi
    fi
    
    # Clone hubspot_customer_portal
    print_status "Cloning $HUBSPOT_REPO..."
    if gh repo clone "$GITHUB_OWNER/$HUBSPOT_REPO" hubspot_temp; then
        print_success "Successfully cloned $HUBSPOT_REPO"
    else
        print_warning "Failed to clone $HUBSPOT_REPO from GitHub. Checking if it exists locally..."
        if [ -d "/workspaces/automations_hub/$HUBSPOT_REPO" ]; then
            print_status "Found local copy of $HUBSPOT_REPO, copying..."
            cp -r "/workspaces/automations_hub/$HUBSPOT_REPO" hubspot_temp
        else
            print_error "Could not find $HUBSPOT_REPO repository. Please check the repository name and permissions."
            exit 1
        fi
    fi
}

# Function to create the new merged repository structure
create_merged_repo() {
    print_status "Creating merged repository structure..."
    
    # Initialize new git repository
    mkdir -p "$NEW_REPO_NAME"
    cd "$NEW_REPO_NAME"
    git init
    
    # Create folder structure
    mkdir -p "notion_customer_portal"
    mkdir -p "hubspot_customer_portal"
    
    # Copy content from notion repository
    print_status "Copying Notion customer portal content..."
    if [ -d "../notion_temp" ]; then
        # Remove .git directory to avoid nested repositories
        rm -rf ../notion_temp/.git
        cp -r ../notion_temp/* notion_customer_portal/ 2>/dev/null || true
        cp -r ../notion_temp/.* notion_customer_portal/ 2>/dev/null || true
        # Remove the copied .git directory if it exists
        rm -rf notion_customer_portal/.git
        print_success "Notion content copied to notion_customer_portal/"
    fi
    
    # Copy content from hubspot repository
    print_status "Copying HubSpot customer portal content..."
    if [ -d "../hubspot_temp" ]; then
        # Remove .git directory to avoid nested repositories
        rm -rf ../hubspot_temp/.git
        cp -r ../hubspot_temp/* hubspot_customer_portal/ 2>/dev/null || true
        cp -r ../hubspot_temp/.* hubspot_customer_portal/ 2>/dev/null || true
        # Remove the copied .git directory if it exists
        rm -rf hubspot_customer_portal/.git
        print_success "HubSpot content copied to hubspot_customer_portal/"
    fi
    
    # Create a comprehensive README for the merged repository
    create_merged_readme
    
    # Create a .gitignore file
    create_gitignore
    
    # Create package.json for the root if both projects have them
    create_root_package_json
}

# Function to create a comprehensive README
create_merged_readme() {
    print_status "Creating merged repository README..."
    
    cat > README.md << 'EOF'
# Emergent Apps Builder

This repository contains the merged customer portal applications from Notion and HubSpot integrations, providing a unified platform for building emergent applications.

## Repository Structure

```
emergent_apps_builder/
├── notion_customer_portal/     # Notion-based customer portal
│   └── [Notion portal files]
├── hubspot_customer_portal/    # HubSpot-based customer portal
│   └── [HubSpot portal files]
├── README.md                   # This file
├── package.json               # Root dependencies (if applicable)
└── .gitignore                 # Git ignore rules
```

## Projects Overview

### Notion Customer Portal
Located in `notion_customer_portal/`

This portal integrates with Notion databases to provide customer access to:
- Order tracking and management
- Profile management
- Communication history
- Service requests

### HubSpot Customer Portal
Located in `hubspot_customer_portal/`

This portal integrates with HubSpot CRM to provide:
- Customer relationship management
- Deal tracking
- Contact management
- Marketing automation

## Getting Started

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn
- Access to Notion API (for Notion portal)
- Access to HubSpot API (for HubSpot portal)

### Installation

1. Clone this repository:
```bash
git clone https://github.com/hairsolutionsco/emergent_apps_builder.git
cd emergent_apps_builder
```

2. Install root dependencies (if any):
```bash
npm install
```

3. Set up Notion Customer Portal:
```bash
cd notion_customer_portal
npm install
# Follow setup instructions in notion_customer_portal/README.md
```

4. Set up HubSpot Customer Portal:
```bash
cd ../hubspot_customer_portal
npm install
# Follow setup instructions in hubspot_customer_portal/README.md
```

### Configuration

Each portal has its own configuration requirements:

#### Notion Portal
- Set up Notion API credentials
- Configure database connections
- Set up authentication

#### HubSpot Portal
- Set up HubSpot API credentials
- Configure CRM connections
- Set up authentication

Refer to the individual README files in each portal directory for detailed setup instructions.

## Development

### Running Both Portals

You can run both portals simultaneously during development:

```bash
# Terminal 1 - Notion Portal
cd notion_customer_portal
npm run dev

# Terminal 2 - HubSpot Portal
cd hubspot_customer_portal
npm run dev
```

### Building for Production

Build both portals for production:

```bash
# Build Notion Portal
cd notion_customer_portal
npm run build

# Build HubSpot Portal
cd ../hubspot_customer_portal
npm run build
```

## Integration Opportunities

This merged repository enables:

1. **Unified Customer Experience**: Combine Notion and HubSpot data
2. **Cross-Platform Analytics**: Aggregate insights from both portals
3. **Shared Components**: Reuse UI components across portals
4. **Consolidated Authentication**: Single sign-on across both systems
5. **Data Synchronization**: Keep customer data in sync between platforms

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Architecture

```mermaid
graph TB
    A[Emergent Apps Builder] --> B[Notion Customer Portal]
    A --> C[HubSpot Customer Portal]
    B --> D[Notion API]
    C --> E[HubSpot API]
    B --> F[Shared Components]
    C --> F
    F --> G[Common Authentication]
    F --> H[Shared Utilities]
```

## Roadmap

- [ ] Unified authentication system
- [ ] Shared component library
- [ ] Cross-platform data synchronization
- [ ] Consolidated analytics dashboard
- [ ] Mobile applications
- [ ] API gateway for unified access

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please check the individual portal documentation or open an issue in this repository.

---

*Generated during repository merge on $(date)*
EOF

    print_success "README.md created successfully"
}

# Function to create a comprehensive .gitignore
create_gitignore() {
    print_status "Creating .gitignore file..."
    
    cat > .gitignore << 'EOF'
# Dependencies
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Production builds
/build
/dist
*.tgz

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDE files
.vscode/
.idea/
*.swp
*.swo

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Logs
logs
*.log

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Coverage directory used by tools like istanbul
coverage/

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

# dotenv environment variables file
.env

# Next.js build output
.next

# Nuxt.js build output
.nuxt

# Gatsby files
.cache/
public

# Storybook build outputs
.out
.storybook-out

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

# Cache files
.cache
.parcel-cache

# Editor directories and files
.idea
*.suo
*.ntvs*
*.njsproj
*.sln
*.sw?
EOF

    print_success ".gitignore created successfully"
}

# Function to create root package.json if both projects have them
create_root_package_json() {
    print_status "Creating root package.json..."
    
    cat > package.json << 'EOF'
{
  "name": "emergent-apps-builder",
  "version": "1.0.0",
  "description": "Merged customer portal applications from Notion and HubSpot integrations",
  "main": "index.js",
  "scripts": {
    "install:all": "npm install && cd notion_customer_portal && npm install && cd ../hubspot_customer_portal && npm install",
    "build:all": "cd notion_customer_portal && npm run build && cd ../hubspot_customer_portal && npm run build",
    "dev:notion": "cd notion_customer_portal && npm run dev",
    "dev:hubspot": "cd hubspot_customer_portal && npm run dev",
    "start:notion": "cd notion_customer_portal && npm start",
    "start:hubspot": "cd hubspot_customer_portal && npm start",
    "test:all": "cd notion_customer_portal && npm test && cd ../hubspot_customer_portal && npm test",
    "lint:all": "cd notion_customer_portal && npm run lint && cd ../hubspot_customer_portal && npm run lint"
  },
  "keywords": [
    "customer-portal",
    "notion",
    "hubspot",
    "crm",
    "integration",
    "emergent-apps"
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
  }
}
EOF

    print_success "package.json created successfully"
}

# Function to commit and push the merged repository
commit_and_push() {
    print_status "Committing and pushing merged repository..."
    
    # Add all files
    git add .
    
    # Create initial commit
    git commit -m "Initial commit: Merge notion_customer_portal and hubspot_customer_portal

- Merged two customer portal repositories into unified structure
- Created notion_customer_portal/ directory with Notion integration
- Created hubspot_customer_portal/ directory with HubSpot integration
- Added comprehensive README with setup and usage instructions
- Configured root package.json with unified scripts
- Set up proper .gitignore for both Node.js projects

This merge enables:
- Unified customer portal development
- Shared components and utilities
- Cross-platform data integration
- Consolidated deployment and management"

    # Create repository on GitHub
    print_status "Creating repository on GitHub..."
    if gh repo create "$GITHUB_OWNER/$NEW_REPO_NAME" --public --description "Merged customer portal applications from Notion and HubSpot integrations"; then
        print_success "Repository created on GitHub"
    else
        print_warning "Repository might already exist or there was an error creating it"
    fi
    
    # Add remote and push
    git remote add origin "https://github.com/$GITHUB_OWNER/$NEW_REPO_NAME.git"
    git branch -M main
    git push -u origin main
    
    print_success "Repository pushed to GitHub successfully!"
}

# Function to clean up temporary files
cleanup() {
    print_status "Cleaning up temporary files..."
    cd /
    rm -rf "$TEMP_DIR"
    print_success "Cleanup completed"
}

# Function to display completion summary
show_summary() {
    print_success "Repository merge completed successfully!"
    echo ""
    print_status "Summary:"
    echo "  - Created new repository: $NEW_REPO_NAME"
    echo "  - Notion portal code: notion_customer_portal/"
    echo "  - HubSpot portal code: hubspot_customer_portal/"
    echo "  - Repository URL: https://github.com/$GITHUB_OWNER/$NEW_REPO_NAME"
    echo ""
    print_status "Next steps:"
    echo "  1. Clone the new repository: git clone https://github.com/$GITHUB_OWNER/$NEW_REPO_NAME.git"
    echo "  2. Install dependencies: cd $NEW_REPO_NAME && npm run install:all"
    echo "  3. Set up environment variables for both portals"
    echo "  4. Follow the setup instructions in each portal's README"
    echo ""
    print_status "Available scripts:"
    echo "  - npm run dev:notion      # Start Notion portal in development"
    echo "  - npm run dev:hubspot     # Start HubSpot portal in development"
    echo "  - npm run build:all       # Build both portals for production"
    echo "  - npm run install:all     # Install dependencies for all projects"
}

# Main execution
main() {
    echo ""
    print_status "Starting repository merge process..."
    echo ""
    
    # Check if user wants to proceed
    read -p "This will create a new repository '$NEW_REPO_NAME' by merging '$NOTION_REPO' and '$HUBSPOT_REPO'. Continue? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_status "Operation cancelled by user"
        exit 0
    fi
    
    # Execute the merge process
    check_prerequisites
    clone_repositories
    create_merged_repo
    commit_and_push
    cleanup
    show_summary
}

# Error handling
trap 'print_error "An error occurred. Cleaning up..."; cleanup; exit 1' ERR

# Run the main function
main "$@"
