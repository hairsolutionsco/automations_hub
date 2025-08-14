# N8N Credentials Setup Guide

## 🔐 Required Credentials for Secure Workflows

### 1. Stripe API Credentials

**Credential Type**: `stripeApi`
**Required for**: Payment sync, webhook handling

```
Name: Stripe API
Type: Stripe
Secret Key: sk_test_... (for testing) or sk_live_... (for production)
Webhook Secret: whsec_... (for webhook validation)
```

### 2. Notion API Credentials

**Credential Type**: `notionApi`
**Required for**: Database operations

```
Name: Notion API
Type: Notion
API Key: secret_... (from Notion integrations page)
```

### 3. Environment Variables

Set these in your n8n instance settings:

```bash
# Notion Database IDs
NOTION_PAYMENTS_DATABASE_ID=your-payments-database-id
NOTION_FAILED_PAYMENTS_DATABASE_ID=your-failed-payments-database-id

# Optional: Email settings
ADMIN_EMAIL=admin@yourcompany.com
```

## 🚀 Setup Steps in N8N Cloud

### Step 1: Add Stripe Credentials
1. Go to **Settings** → **Credentials**
2. Click **Add Credential**
3. Select **Stripe**
4. Enter your Stripe secret key
5. For webhooks, add the webhook secret
6. Save as "Stripe API"

### Step 2: Add Notion Credentials
1. Go to **Settings** → **Credentials**
2. Click **Add Credential**
3. Select **Notion**
4. Enter your Notion integration token
5. Save as "Notion API"

### Step 3: Set Environment Variables
1. Go to **Settings** → **Environment Variables**
2. Add each variable:
   - `NOTION_PAYMENTS_DATABASE_ID`
   - `NOTION_FAILED_PAYMENTS_DATABASE_ID`

### Step 4: Import Secure Workflows
```bash
# Import the secure workflow versions
./tools/import_workflows_api.sh -s secure/
```

## 🔍 Security Verification

### Check Credentials Are Used
- No hardcoded API keys in workflow JSON
- All sensitive values use `{{ $credentials.credentialName.field }}`
- Environment variables use `{{ $vars.VARIABLE_NAME }}`

### Webhook Security
- Webhook secrets stored in credentials
- Signature validation enabled
- HTTPS endpoints only

## 📋 Secure Workflow Files

- `Payment_Sync_to_Notion_Secure.json` - Secure payment sync
- `Stripe_Event_Handler_Secure.json` - Secure webhook handler

## ⚠️ Important Notes

1. **Never commit credentials** to Git repositories
2. **Use test keys** during development
3. **Rotate keys regularly** for production
4. **Monitor webhook endpoints** for unauthorized access
5. **Use environment variables** for all configuration

---
**Created**: August 14, 2025  
**Purpose**: Secure credential management for n8n workflows
