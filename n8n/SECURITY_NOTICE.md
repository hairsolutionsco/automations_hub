# 🔒 N8N Security Notice

## Sensitive Data Removal

During the export process on August 14, 2025, the following sensitive data was detected and removed:

### Files Affected:
- `VsaLkCvopP9TByf8_Payment_Sync_to_Notion.json`
- `YKYcZEkyi0tldT9b_My_workflow_2.json`
- `backup_20250814_021505/VsaLkCvopP9TByf8_Payment_Sync_to_Notion.json`
- `backup_20250814_021505/YKYcZEkyi0tldT9b_My_workflow_2.json`

### Sensitive Data Removed:
- **Stripe API Keys**: `sk_live_*` keys replaced with `[STRIPE_API_KEY_REMOVED_FOR_SECURITY]`
- **Webhook Secrets**: `whsec_*` secrets replaced with `[WEBHOOK_SECRET_REMOVED_FOR_SECURITY]`

## ⚠️ Important for Future Exports

When exporting workflows from n8n cloud:

1. **Review exported files** for sensitive data before committing
2. **Use environment variables** for API keys in workflows
3. **Never commit** actual API keys, tokens, or secrets
4. **Check the exports/** directory for sensitive patterns

## Security Patterns to Watch

```bash
# Dangerous patterns that should never be committed:
sk_live_*        # Stripe live API keys
sk_test_*        # Stripe test API keys
pk_live_*        # Stripe publishable keys
whsec_*          # Webhook secrets
Bearer *         # Bearer tokens
api_key.*        # API key patterns
```

## Cleanup Commands

```bash
# Scan for sensitive data before committing
grep -r "sk_live\|sk_test\|whsec_" exports/
grep -r "Bearer.*[A-Za-z0-9]\{20,\}" exports/
```

---
**Security Review Date**: August 14, 2025  
**Status**: ✅ Sensitive data removed  
**Action**: Manual review and replacement completed
