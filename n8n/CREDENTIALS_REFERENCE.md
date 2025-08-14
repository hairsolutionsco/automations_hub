# N8N Credentials Reference

This file contains the secure n8n credential IDs for all major apps used in workflows.
Use these credential IDs instead of hardcoded API keys or tokens.

## Available Credentials

### CRM & Sales
- **HubSpot App Token**
  - Credential ID: `ID4CUY90jW5ObSXedy`
  - Usage: HubSpot API operations, contact management, deals
  - Type: App Token

### Email & Communication
- **Gmail OAuth2 API**
  - Credential ID: `IDiRhtr9mcBtiwn0Jn`
  - Usage: Gmail automation, email sending/reading
  - Type: OAuth2

### Google Services
- **Google OAuth2 API**
  - Credential ID: `IDuheZ3yW8cV9FMwIz`
  - Usage: Google Sheets, Drive, Calendar, other Google services
  - Type: OAuth2

### AI & ML
- **OpenAI API Key**
  - Credential ID: `ID4X9TIhDpjNa5gM9J`
  - Usage: ChatGPT, GPT-4, AI text generation
  - Type: API Key

### Payments & Finance
- **GoCardless Bearer Auth**
  - Credential ID: `IDZjro27xRan8oQvXj`
  - Usage: Direct debit payments, subscription billing
  - Type: Bearer Token

- **Stripe API Key**
  - Credential ID: `ID3q1LYGrkaZIDtJar`
  - Usage: Payment processing, subscription management
  - Type: API Key

### Productivity & Data
- **Notion API Key**
  - Credential ID: `ID4jkKCiAXGH1iVwyi`
  - Usage: Database operations, page creation, content management
  - Type: API Key

## Usage in N8N Workflows

When creating or modifying workflows, reference credentials like this:

```json
{
  "credentials": {
    "stripeApi": {
      "id": "ID3q1LYGrkaZIDtJar",
      "name": "Stripe API Key"
    }
  }
}
```

## Security Benefits

✅ **Centralized Management**: Credentials managed in n8n interface
✅ **No Hardcoded Secrets**: No API keys in workflow JSON files
✅ **Easy Rotation**: Update credentials without changing workflows
✅ **Access Control**: n8n handles credential security
✅ **Git Safe**: Workflow files can be safely committed to version control

---
**Created**: August 14, 2025  
**Purpose**: Secure credential management for n8n workflows  
**Status**: ✅ Ready for use in workflow modifications
