# Environment Variables Configuration

This guide explains how to set up environment variables for n8n workflow management and GitOps integration.

## Required Environment Variables

### n8n Cloud API Access

These variables are **required** for n8n CLI and API operations:

```bash
# n8n Cloud Instance URL
N8N_CLOUD_INSTANCE_URL="https://hairsolutionsco.app.n8n.cloud"

# User email for n8n cloud account
N8N_USER_EMAIL="info@oneheadhair.com"

# API key for n8n cloud instance
N8N_API_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### GitHub Integration (Optional)

For GitOps functionality:

```bash
# GitHub personal access token with 'repo' scope
GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"

# Repository owner/organization
REPO_OWNER="hairsolutionsco"

# Repository name
REPO_NAME="automations_hub"

# Path within repository for workflows
REPO_PATH="n8n/src/workflows/"
```

## Setting Environment Variables

### Method 1: Codespace Environment Variables (Recommended)

1. Go to your GitHub Codespace settings
2. Navigate to "Environment Variables"
3. Add each variable with its value
4. Restart your Codespace

**Advantages:**
- Persistent across terminal sessions
- Secure (not visible in command history)
- Available to all processes

### Method 2: Terminal Export (Temporary)

```bash
# Set variables in current terminal session
export N8N_CLOUD_INSTANCE_URL="https://hairsolutionsco.app.n8n.cloud"
export N8N_USER_EMAIL="info@oneheadhair.com"
export N8N_API_KEY="your-api-key-here"

# Verify variables are set
env | grep N8N
```

**Note:** These will be lost when terminal session ends.

### Method 3: Environment File (Not Recommended for Secrets)

Create `.env` file (already in .gitignore):

```bash
# .env file (DO NOT COMMIT TO GIT)
N8N_CLOUD_INSTANCE_URL="https://hairsolutionsco.app.n8n.cloud"
N8N_USER_EMAIL="info@oneheadhair.com"
N8N_API_KEY="your-api-key-here"
```

Source the file:
```bash
source .env
```

## Verification

### Check Environment Variables

```bash
# Check all n8n variables
env | grep N8N

# Check specific variable
echo $N8N_CLOUD_INSTANCE_URL

# Check if variables are properly formatted
echo "Instance URL: $N8N_CLOUD_INSTANCE_URL"
echo "User Email: $N8N_USER_EMAIL"
echo "API Key: ${N8N_API_KEY:+[SET]}"  # Shows [SET] if variable exists
```

### Test n8n API Connection

```bash
# Test API connectivity
curl -H "X-N8N-API-KEY: $N8N_API_KEY" \
     -H "Content-Type: application/json" \
     "$N8N_CLOUD_INSTANCE_URL/api/v1/workflows" | jq '.data | length'
```

Expected output: Number of workflows in your instance.

### Test n8n CLI

```bash
# Test CLI configuration
n8n export:workflow --help

# Test actual export (should not error on auth)
n8n export:workflow --all --dry-run
```

## Security Best Practices

### API Key Management

1. **Never commit API keys to Git**
2. **Rotate keys regularly** (every 90 days)
3. **Use minimum required permissions**
4. **Monitor API key usage**

### Variable Protection

```bash
# Check .gitignore includes environment files
grep -E "(\.env|\.environment)" ../.gitignore

# Verify no secrets in Git history
git log --all --full-history -- .env
```

### Access Control

- Limit Codespace access to authorized users
- Use GitHub organization environment variables when possible
- Implement key rotation policies

## Troubleshooting

### Common Issues

#### 1. Variables Not Persisting

**Problem**: Variables disappear after closing terminal

**Solution**: Use Codespace Environment Variables, not terminal export

#### 2. Authentication Errors

**Problem**: API returns 401 Unauthorized

**Solutions**:
```bash
# Check if API key is set
echo "${N8N_API_KEY:+API Key is set}"

# Test with curl
curl -I -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_CLOUD_INSTANCE_URL/api/v1/workflows"

# Verify API key format (should be JWT)
echo $N8N_API_KEY | cut -d. -f1 | base64 -d
```

#### 3. URL Format Issues

**Problem**: n8n CLI cannot connect to instance

**Solutions**:
```bash
# Check URL format (should include https://)
echo $N8N_CLOUD_INSTANCE_URL

# Test URL accessibility
curl -I "$N8N_CLOUD_INSTANCE_URL"

# Verify no trailing slashes
echo $N8N_CLOUD_INSTANCE_URL | grep "/$"
```

#### 4. Permission Errors

**Problem**: File permission errors on scripts

**Solution**:
```bash
# Fix script permissions
chmod +x tools/*.sh

# Check current permissions
ls -la tools/
```

### Debugging Commands

```bash
# Show all environment variables
printenv | sort

# Check n8n specific variables
printenv | grep -i n8n

# Verify variable format
if [[ $N8N_API_KEY =~ ^eyJ ]]; then
  echo "API key format looks correct (JWT)"
else
  echo "API key format may be incorrect"
fi

# Test complete setup
./tools/test_environment.sh
```

## Environment Templates

### Development Environment

```bash
# Development setup
export N8N_CLOUD_INSTANCE_URL="https://hairsolutionsco.app.n8n.cloud"
export N8N_USER_EMAIL="info@oneheadhair.com"
export N8N_API_KEY="dev-api-key"
export N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS="false"
export N8N_RUNNERS_ENABLED="true"
```

### Production Environment

```bash
# Production setup (use Codespace variables)
export N8N_CLOUD_INSTANCE_URL="https://hairsolutionsco.app.n8n.cloud"
export N8N_USER_EMAIL="info@oneheadhair.com"
export N8N_API_KEY="prod-api-key"
export N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS="true"
export N8N_RUNNERS_ENABLED="true"
export GITHUB_TOKEN="github-token-with-repo-access"
```

## Related Documentation

- [n8n Variables Configuration](variables.md)
- [GitOps Setup Guide](../docs/GITOPS_N8N_SETUP.md)
- [Troubleshooting Guide](../docs/troubleshooting.md)

---

*Last updated: August 14, 2025*
