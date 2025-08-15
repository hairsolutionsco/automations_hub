# Repository Merger Scripts Documentation

This directory contains scripts to merge the `notion_customer_portal` and `hubspot_customer_portal` repositories into a unified `emergent_apps_builder` repository.

## Available Scripts

### 1. `merge_customer_portals.sh` - Full GitHub Integration
**Best for:** Creating a new GitHub repository with full version history

**Features:**
- Clones repositories from GitHub
- Creates new GitHub repository
- Preserves git history from both repositories
- Handles remote repository creation
- Full GitHub integration with `gh` CLI

**Prerequisites:**
- GitHub CLI (`gh`) installed and authenticated
- Access to source repositories on GitHub
- Permission to create new repositories

**Usage:**
```bash
./scripts/merge_customer_portals.sh
```

### 2. `merge_customer_portals_local.sh` - Local Development Focus
**Best for:** Quick local setup and development

**Features:**
- Works with local directories if they exist
- Creates placeholder structure if repositories don't exist
- Focuses on development setup
- No GitHub dependencies required
- Creates comprehensive development environment

**Prerequisites:**
- Node.js and npm installed
- Local workspace access

**Usage:**
```bash
./scripts/merge_customer_portals_local.sh
```

## Repository Structure Created

Both scripts create the same unified structure:

```
emergent_apps_builder/
├── notion_customer_portal/          # Notion integration portal
│   ├── src/                        # Source code
│   ├── components/                 # React components
│   ├── pages/                      # Next.js pages
│   ├── api/                        # API routes
│   ├── utils/                      # Utility functions
│   ├── package.json               # Dependencies
│   ├── .env.example               # Environment template
│   └── README.md                  # Portal documentation
├── hubspot_customer_portal/        # HubSpot integration portal
│   ├── src/                        # Source code
│   ├── components/                 # React components
│   ├── pages/                      # Next.js pages
│   ├── api/                        # API routes
│   ├── utils/                      # Utility functions
│   ├── package.json               # Dependencies
│   ├── .env.example               # Environment template
│   └── README.md                  # Portal documentation
├── scripts/                        # Development scripts
│   ├── check-env.js               # Environment validation
│   └── setup.js                   # Initial setup
├── docs/                           # Documentation
│   └── DEVELOPMENT.md              # Development guide
├── README.md                       # Main documentation
├── package.json                   # Root dependencies & scripts
└── .gitignore                     # Git ignore rules
```

## Integration Features

### Unified Development Experience

**Root Package.json Scripts:**
```bash
npm run install:all     # Install dependencies for all projects
npm run dev:all         # Start both portals simultaneously
npm run dev:notion      # Start Notion portal (port 3001)
npm run dev:hubspot     # Start HubSpot portal (port 3002)
npm run build:all       # Build both portals for production
npm run test:all        # Run tests for both portals
npm run lint:all        # Lint both portals
npm run clean:install   # Clean reinstall all dependencies
npm run check:env       # Validate environment configuration
```

### Portal-Specific Features

**Notion Customer Portal (Port 3001):**
- Integration with 35 Notion databases
- Customer order tracking and management
- Hair profile specifications
- Payment history (Stripe integration)
- Email communication tracking

**HubSpot Customer Portal (Port 3002):**
- HubSpot CRM integration
- Deal pipeline management
- Contact relationship management
- Marketing automation
- Sales process tracking

## Setup Process

### Using the GitHub Script (Recommended for Production)

1. **Run the script:**
```bash
./scripts/merge_customer_portals.sh
```

2. **Follow prompts:**
   - Confirms repository creation
   - Handles authentication
   - Creates GitHub repository
   - Pushes initial commit

3. **Clone and setup:**
```bash
git clone https://github.com/hairsolutionsco/emergent_apps_builder.git
cd emergent_apps_builder
npm run setup
```

### Using the Local Script (Recommended for Development)

1. **Run the script:**
```bash
./scripts/merge_customer_portals_local.sh
```

2. **Navigate to created repository:**
```bash
cd emergent_apps_builder
npm run setup
```

3. **Configure environment:**
```bash
# Edit environment files
nano notion_customer_portal/.env.local
nano hubspot_customer_portal/.env.local
```

4. **Install and start:**
```bash
npm run install:all
npm run dev:all
```

## Environment Configuration

### Notion Portal Environment
```bash
# notion_customer_portal/.env.local
NOTION_API_KEY=your_notion_api_key_here
NOTION_DATABASE_ID=your_database_id_here
NEXTAUTH_SECRET=your_auth_secret_here
NEXTAUTH_URL=http://localhost:3001
```

### HubSpot Portal Environment
```bash
# hubspot_customer_portal/.env.local
HUBSPOT_ACCESS_TOKEN=your_hubspot_access_token_here
HUBSPOT_PORTAL_ID=your_portal_id_here
NEXTAUTH_SECRET=your_auth_secret_here
NEXTAUTH_URL=http://localhost:3002
```

## Connected Systems

### Notion Database Integration
The Notion portal connects to these Hair Solutions Co databases:

**CRM:**
- Companies (ID: `22bf4e0d-84e0-80bb-8d1c-c90710d44870`)
- Contacts (ID: `226f4e0d-84e0-814c-ad70-d478cebeee30`)
- Hair Orders Profiles (ID: `248f4e0d-84e0-80ad-9d33-e90e5124c092`)

**Sales & Operations:**
- Orders (ID: `228f4e0d-84e0-816f-8511-fab726d2c6ef`)
- Plans (ID: `228f4e0d-84e0-815c-a108-e48054988ac0`)
- Suppliers Inventory (ID: `226f4e0d-84e0-814f-a468-d44302ee0478`)

**Finances:**
- Payments (ID: `22af4e0d-84e0-80c3-a7d6-f0209d93081d`)
- Expenses (ID: `226f4e0d-84e0-817e-84e2-c9a983663070`)

### HubSpot CRM Integration
- Contact management and communication
- Deal pipeline and sales tracking
- Company relationship management
- Marketing automation integration

## Development Workflow

### Adding New Features

1. **Portal-specific features:**
   - Notion: Add to `notion_customer_portal/`
   - HubSpot: Add to `hubspot_customer_portal/`

2. **Shared components:**
   - Plan for future shared component library
   - Currently managed in each portal

3. **Testing:**
```bash
npm run test:all
```

### Deployment Strategy

1. **Development:**
```bash
npm run dev:all
```

2. **Build:**
```bash
npm run build:all
```

3. **Production deployment:**
   - Each portal can be deployed independently
   - Unified deployment scripts available

## Troubleshooting

### Common Issues

**Port conflicts:**
```bash
# Check what's running on ports
lsof -i :3001
lsof -i :3002

# Stop all processes
npm run stop:all
```

**Environment issues:**
```bash
# Check environment configuration
npm run check:env
```

**Dependency problems:**
```bash
# Clean reinstall
npm run clean:install
```

**Repository access:**
- Ensure GitHub CLI is authenticated: `gh auth status`
- Check repository permissions
- Verify repository names exist

## Future Enhancements

### Planned Features
- [ ] Unified authentication system
- [ ] Cross-platform data synchronization
- [ ] Shared component library
- [ ] Real-time collaboration features
- [ ] Mobile applications
- [ ] API gateway for unified access

### Integration Opportunities
- [ ] Notion ↔ HubSpot data sync
- [ ] Unified customer dashboard
- [ ] Cross-platform reporting
- [ ] Shared customer journey tracking

## Support

- **Script Issues:** Check script output and logs
- **Environment Setup:** Use `npm run check:env`
- **Development Help:** See `docs/DEVELOPMENT.md`
- **Repository Issues:** Open GitHub issues

---

**Created:** August 15, 2025  
**Hair Solutions Co Automation Hub**
