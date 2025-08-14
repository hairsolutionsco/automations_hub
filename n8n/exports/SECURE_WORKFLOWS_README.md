# Secure N8N Workflows

These workflows have been updated to use n8n credentials instead of hardcoded sensitive values.

## 🔒 Security Features

✅ **No Hardcoded API Keys** - All use n8n credential IDs  
✅ **Environment Variables** - Database IDs and sensitive configs  
✅ **OAuth2 Authentication** - Secure authentication flows  
✅ **Git Safe** - Can be committed without security risks  

## 📋 Available Secure Workflows

### 1. Payment Sync to Notion - Secure v2
**File**: `Payment_Sync_to_Notion_SECURE_v2.json`

**Features**:
- Fetches payments from Stripe and GoCardless
- Transforms and merges payment data
- Creates records in Notion database

**Credentials Used**:
- Stripe API: `ID3q1LYGrkaZIDtJar`
- GoCardless Bearer: `IDZjro27xRan8oQvXj`
- Notion API: `ID4jkKCiAXGH1iVwyi`

**Environment Variables**:
- `NOTION_PAYMENTS_DATABASE_ID`

### 2. Gmail Assistant - Secure v2
**File**: `Gmail_Assistant_SECURE_v2.json`

**Features**:
- Scheduled email checking (weekdays 8am)
- AI-powered email analysis with OpenAI
- Automatic categorization and priority setting
- Notion database logging
- Mark emails as read after processing

**Credentials Used**:
- Gmail OAuth2: `IDiRhtr9mcBtiwn0Jn`
- OpenAI API: `ID4X9TIhDpjNa5gM9J`
- Notion API: `ID4jkKCiAXGH1iVwyi`

**Environment Variables**:
- `NOTION_EMAILS_DATABASE_ID`

### 3. Personalised Outreach Emails - Secure v2
**File**: `Personalised_Outreach_Emails_SECURE_v2.json`

**Features**:
- Fetches contacts from HubSpot
- Analyzes email history for persona building
- AI-powered personalized email generation
- Creates draft emails for review
- Logs outreach activities to Notion

**Credentials Used**:
- HubSpot App Token: `ID4CUY90jW5ObSXedy`
- Gmail OAuth2: `IDiRhtr9mcBtiwn0Jn`
- OpenAI API: `ID4X9TIhDpjNa5gM9J`
- Notion API: `ID4jkKCiAXGH1iVwyi`

**Environment Variables**:
- `NOTION_OUTREACH_DATABASE_ID`

## 🔧 Setup Instructions

### 1. Import Credentials in N8N
Make sure these credentials are set up in your n8n instance:

- **HubSpot App Token** (`ID4CUY90jW5ObSXedy`)
- **Gmail OAuth2 API** (`IDiRhtr9mcBtiwn0Jn`)
- **Google OAuth2 API** (`IDuheZ3yW8cV9FMwIz`)
- **OpenAI API Key** (`ID4X9TIhDpjNa5gM9J`)
- **GoCardless Bearer Auth** (`IDZjro27xRan8oQvXj`)
- **Stripe API Key** (`ID3q1LYGrkaZIDtJar`)
- **Notion API Key** (`ID4jkKCiAXGH1iVwyi`)

### 2. Set Environment Variables
In your n8n instance, set these environment variables:

```bash
NOTION_PAYMENTS_DATABASE_ID=your-payments-database-id
NOTION_EMAILS_DATABASE_ID=your-emails-database-id
NOTION_OUTREACH_DATABASE_ID=your-outreach-database-id
```

### 3. Import Workflows
Use the secure import script to import these workflows:

```bash
# Import all secure workflows
./tools/import_workflows_api.sh -s exports/ -d  # Dry run first
./tools/import_workflows_api.sh -s exports/     # Actual import
```

## 🔄 Migration from Original Workflows

If you have the original workflows with hardcoded values:

1. **Backup existing workflows** using the export script
2. **Deactivate old workflows** in n8n interface
3. **Import secure versions** using the import script
4. **Update environment variables** as needed
5. **Test secure workflows** thoroughly
6. **Delete old workflows** once confirmed working

## 📊 Benefits of Secure Workflows

### Security
- No API keys in workflow files
- Centralized credential management
- Safe for version control
- Easy credential rotation

### Maintenance
- Update credentials without changing workflows
- Environment-specific configurations
- Better error handling
- Audit trail for credential usage

### Collaboration
- Safe to share workflow files
- Team-friendly development
- Consistent across environments
- Reduced security risks

## 🚨 Important Notes

1. **Test First**: Always test in a development environment
2. **Backup**: Keep backups of working workflows
3. **Credentials**: Ensure all credential IDs exist in your n8n instance
4. **Environment**: Set all required environment variables
5. **Permissions**: Verify credential permissions are sufficient

## 📚 Related Documentation

- [CREDENTIALS_REFERENCE.md](./CREDENTIALS_REFERENCE.md) - Complete credential ID reference
- [SECURITY_NOTICE.md](./SECURITY_NOTICE.md) - Security cleanup information
- [README.md](./README.md) - Main n8n documentation

---
**Created**: August 14, 2025  
**Purpose**: Secure workflow implementations with n8n credentials  
**Status**: ✅ Ready for import and use
