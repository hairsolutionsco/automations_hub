# n8n Variables Configuration

This guide explains how to configure variables within your n8n cloud instance for workflow automation and GitOps integration.

## What are n8n Variables?

n8n Variables are key-value pairs stored in your n8n instance that can be accessed across all workflows using the `$vars` function. They're ideal for:

- Configuration values that change between environments
- API keys and tokens (though credentials are preferred for sensitive data)
- Common settings shared across multiple workflows
- GitOps configuration parameters

## Access Variables in n8n Cloud

### Location
1. Log into your n8n cloud instance: https://hairsolutionsco.app.n8n.cloud
2. Go to **Settings** → **Variables**
3. Add, edit, or delete variables as needed

### Usage in Workflows
```javascript
// Access a variable in expressions
{{ $vars.variable_name }}

// Example: Get repository owner
{{ $vars.repo_owner }}

// Use in HTTP Request URLs
{{ $vars.api_base_url }}/endpoint

// Conditional logic with variables
{{ $vars.environment === 'production' ? 'prod-key' : 'dev-key' }}
```

## Required Variables for GitOps

### GitHub Integration Variables

Set these variables in your n8n instance for the backup workflow and GitOps functionality:

| Variable Name | Description | Example Value | Required |
|---------------|-------------|---------------|----------|
| `repo_owner` | GitHub repository owner/organization | `hairsolutionsco` | ✅ |
| `repo_name` | GitHub repository name | `automations_hub` | ✅ |
| `repo_path` | Path within repo for workflows | `n8n/src/workflows/` | ✅ |
| `github_token` | GitHub personal access token | `ghp_xxxxxxxxxxxx` | ✅ |
| `environment` | Current environment (dev/staging/prod) | `production` | ❌ |

### API Integration Variables

| Variable Name | Description | Example Value | Required |
|---------------|-------------|---------------|----------|
| `openai_api_key` | OpenAI API key for AI nodes | `sk-xxxxxxxxxxxx` | ✅ |
| `notion_api_key` | Notion integration token | `secret_xxxxxxxxxxxx` | ✅ |
| `fireflies_api_key` | Fireflies.ai API token | `bearer-token` | ❌ |
| `slack_webhook_url` | Slack webhook for notifications | `https://hooks.slack.com/...` | ❌ |

### Business Configuration Variables

| Variable Name | Description | Example Value | Required |
|---------------|-------------|---------------|----------|
| `company_name` | Company name for templates | `Hair Solutions Co` | ❌ |
| `support_email` | Support email address | `info@oneheadhair.com` | ❌ |
| `timezone` | Default timezone for workflows | `America/Toronto` | ❌ |

## Setting Up Variables

### Step-by-Step Setup

1. **Access Variables Panel**
   ```
   n8n Cloud Instance → Settings → Variables
   ```

2. **Add Required Variables**
   Click "Add Variable" and enter:
   - **Key**: `repo_owner`
   - **Value**: `hairsolutionsco`
   - **Type**: Text

3. **Repeat for All Variables**
   Add each variable from the tables above.

4. **Save Configuration**
   Variables are automatically saved when created.

### Bulk Import (Advanced)

If you have many variables, you can use the n8n API:

```bash
# Example: Set multiple variables via API
curl -X POST \
  -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "key": "repo_owner",
    "value": "hairsolutionsco"
  }' \
  "$N8N_CLOUD_INSTANCE_URL/api/v1/variables"
```

## Security Considerations

### Sensitive Data

⚠️ **Important**: While variables can store API keys, consider using **Credentials** for sensitive data instead:

**Variables**: Good for non-sensitive configuration
**Credentials**: Better for API keys, passwords, tokens

### Access Control

- Variables are accessible to all workflows in the instance
- No role-based access control for individual variables
- Consider environment separation for sensitive data

### Audit Trail

- Variable changes are logged in n8n
- Monitor variable access in workflow execution logs
- Regular review of variable usage recommended

## Variable Usage Examples

### GitHub Backup Workflow

```json
{
  "parameters": {
    "owner": {
      "__rl": true,
      "mode": "",
      "value": "={{ $vars.repo_owner }}"
    },
    "repository": {
      "__rl": true,
      "mode": "",
      "value": "={{ $vars.repo_name }}"
    },
    "filePath": "={{ $vars.repo_path }}workflows/{{ $node.id }}.json"
  }
}
```

### Environment-Specific Configuration

```javascript
// Use different API endpoints based on environment
const apiUrl = $vars.environment === 'production' 
  ? 'https://api.production.com' 
  : 'https://api.staging.com';

// Dynamic configuration based on variables
const config = {
  timeout: $vars.api_timeout || 30000,
  retries: $vars.api_retries || 3,
  baseUrl: $vars.api_base_url
};
```

### Template Personalization

```javascript
// Email template with company variables
const emailTemplate = `
Hello from ${$vars.company_name}!

For support, contact us at ${$vars.support_email}.

Best regards,
The ${$vars.company_name} Team
`;
```

## Troubleshooting Variables

### Common Issues

#### 1. Variable Not Found

**Error**: `Variable 'variable_name' not found`

**Solutions**:
1. Check variable exists in Settings → Variables
2. Verify exact spelling and case sensitivity
3. Ensure variable has a value set

#### 2. Permission Errors

**Error**: Cannot access variable

**Solutions**:
1. Verify user has access to n8n instance
2. Check if variable was deleted or renamed
3. Confirm workflow is running in correct instance

#### 3. Type Conversion Issues

**Error**: Unexpected variable type

**Solutions**:
```javascript
// Convert to string
{{ String($vars.numeric_value) }}

// Convert to number
{{ Number($vars.string_value) }}

// Handle undefined variables
{{ $vars.optional_value || 'default_value' }}
```

### Debugging Variables

```javascript
// Log all variables in a workflow
console.log('All variables:', $vars);

// Check specific variable exists
if ($vars.repo_owner) {
  console.log('Repository owner:', $vars.repo_owner);
} else {
  console.log('Warning: repo_owner variable not set');
}

// Validate required variables
const requiredVars = ['repo_owner', 'repo_name', 'repo_path'];
const missing = requiredVars.filter(key => !$vars[key]);
if (missing.length > 0) {
  throw new Error(`Missing required variables: ${missing.join(', ')}`);
}
```

## Migration and Backup

### Export Variables

Currently, n8n doesn't provide direct export of variables. Document them manually:

```bash
# Create variables backup documentation
cat > config/variables-backup.md << EOF
# n8n Variables Backup - $(date)

## GitHub Integration
- repo_owner: hairsolutionsco
- repo_name: automations_hub
- repo_path: n8n/src/workflows/

## API Keys
- openai_api_key: [REDACTED]
- notion_api_key: [REDACTED]

EOF
```

### Environment Migration

When moving between n8n instances:

1. **Document Current Variables**
   - Screenshot Variables page
   - Export variable list
   - Note sensitive values separately

2. **Setup New Instance**
   - Create variables in new instance
   - Test access from workflows
   - Update any changed values

3. **Validate Migration**
   - Run test workflows
   - Verify all variables accessible
   - Check GitOps functionality

## Best Practices

### Naming Conventions

```
# Use snake_case for consistency
repo_owner          ✅
repoOwner          ❌

# Use descriptive names
api_key            ❌
openai_api_key     ✅

# Group related variables
github_repo_owner
github_repo_name
github_api_token
```

### Organization

```
# Environment-specific prefixes
prod_api_url
dev_api_url

# Service-specific grouping
notion_api_key
notion_database_id
slack_webhook_url
slack_channel_id
```

### Documentation

- Document all variables and their purposes
- Include example values (masked for sensitive data)
- Note which workflows depend on each variable
- Keep documentation updated with changes

## Related Documentation

- [Environment Variables Configuration](environment.md)
- [GitOps Setup Guide](../docs/GITOPS_N8N_SETUP.md)
- [n8n API Reference](../docs/api-reference.md)

---

*Last updated: August 14, 2025*
