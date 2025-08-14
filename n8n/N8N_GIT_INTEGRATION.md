# N8N Native Git Integration Guide

## Overview

N8N has excellent **built-in capabilities** for version control and automation exchange with Git repositories. You don't need complex custom systems - n8n's native commands handle everything efficiently.

## Native N8N Commands

### Export Workflows
```bash
# Export all workflows as separate files (perfect for Git)
n8n export:workflow --backup --output=workflows/

# Export specific workflow
n8n export:workflow --id=workflow_id --output=my_workflow.json

# Export all workflows to single file
n8n export:workflow --all --output=all_workflows.json
```

### Import Workflows  
```bash
# Import all workflows from directory
n8n import:workflow --separate --input=workflows/

# Import single workflow file
n8n import:workflow --input=my_workflow.json

# Import to specific user/project
n8n import:workflow --input=workflows/ --separate --userId=user_id
```

### Export/Import Credentials
```bash
# Export credentials
n8n export:credentials --output=credentials.json

# Import credentials  
n8n import:credentials --input=credentials.json
```

## Perfect Git Workflow

### 1. Initial Setup
```bash
# Initialize Git repository
git init
git remote add origin https://github.com/your-username/n8n-workflows.git

# Create directory structure
mkdir -p workflows credentials backups
```

### 2. Export from N8N → Git
```bash
# Export all workflows as separate files (best for Git diffs)
n8n export:workflow --backup --output=workflows/

# Export credentials (be careful with sensitive data!)
n8n export:credentials --output=credentials/credentials.json

# Commit to Git
git add .
git commit -m "Update workflows: $(date)"
git push origin main
```

### 3. Import from Git → N8N
```bash
# Pull latest changes
git pull origin main

# Import workflows
n8n import:workflow --separate --input=workflows/

# Import credentials
n8n import:credentials --input=credentials/credentials.json
```

## Why N8N's Native System is Perfect

### ✅ **Built-in Version Control Support**
- `--separate` flag creates individual files per workflow
- Perfect for Git diffs and merge conflicts
- JSON format is human-readable and Git-friendly

### ✅ **No Additional Dependencies**
- No Python scripts, custom APIs, or complex tooling needed
- Works with any Git repository (GitHub, GitLab, Bitbucket)
- Standard Unix tools for automation

### ✅ **Handles All Data Types**
- Workflows (with full node configurations)
- Credentials (with proper security considerations)
- Maintains all metadata and relationships

### ✅ **Enterprise Ready**
- User and project assignment support
- Batch operations for large installations
- Backup format for disaster recovery

## Automated Git Sync

### Using Git Hooks
```bash
# .git/hooks/pre-commit
#!/bin/bash
n8n export:workflow --backup --output=workflows/
git add workflows/
```

### Using Cron Jobs
```bash
# Export workflows every hour
0 * * * * cd /path/to/n8n-repo && n8n export:workflow --backup --output=workflows/ && git add . && git commit -m "Auto-sync $(date)" && git push
```

### Using GitHub Actions
```yaml
name: N8N Sync
on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
  
jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Export N8N workflows
        run: |
          n8n export:workflow --backup --output=workflows/
          git add .
          git commit -m "Auto-sync workflows" || exit 0
          git push
```

## Directory Structure
```
n8n-workflows/
├── workflows/           # Individual workflow files
│   ├── workflow1.json
│   ├── workflow2.json
│   └── ...
├── credentials/         # Credentials export
│   └── credentials.json
├── backups/            # Timestamped backups
│   └── workflows_backup_20250814.tar.gz
├── scripts/            # Helper scripts
│   └── n8n_git_sync.sh
├── .gitignore          # Ignore sensitive files
└── README.md
```

## Security Considerations

### Credentials
```bash
# Add to .gitignore to exclude sensitive credentials
echo "credentials/credentials.json" >> .gitignore
echo "**/*password*" >> .gitignore
echo "**/*secret*" >> .gitignore
```

### Environment Variables
```bash
# For cloud operations
export N8N_CLOUD_INSTANCE_URL="https://your-instance.app.n8n.cloud"
export N8N_API_KEY="your-api-key"
export N8N_USER_EMAIL="your-email@domain.com"
```

## Integration with CI/CD

### GitLab CI Example
```yaml
deploy_to_production:
  script:
    - n8n import:workflow --separate --input=workflows/
  only:
    - main
```

### Jenkins Pipeline
```groovy
pipeline {
    agent any
    stages {
        stage('Deploy Workflows') {
            steps {
                sh 'n8n import:workflow --separate --input=workflows/'
            }
        }
    }
}
```

## Advanced Use Cases

### Multi-Environment Sync
```bash
# Development environment
n8n export:workflow --backup --output=environments/dev/

# Production environment  
N8N_CLOUD_INSTANCE_URL=$PROD_URL n8n export:workflow --backup --output=environments/prod/
```

### Selective Workflow Management
```bash
# Export specific workflows by ID
n8n export:workflow --id=workflow1 --output=critical/workflow1.json
n8n export:workflow --id=workflow2 --output=critical/workflow2.json
```

### Backup and Restore
```bash
# Create timestamped backup
DATE=$(date +%Y%m%d_%H%M%S)
n8n export:workflow --backup --output=backups/backup_$DATE/

# Restore from backup
n8n import:workflow --separate --input=backups/backup_20250814_143000/
```

## Quick Start Script

Use the provided `n8n_git_sync.sh` script for an interactive menu system that leverages all these native n8n capabilities with Git integration.

```bash
./scripts/n8n_git_sync.sh
```

---

**Bottom Line**: N8N's native export/import commands are perfectly designed for Git-based version control. No need to reinvent the wheel - just use what's already built-in!
