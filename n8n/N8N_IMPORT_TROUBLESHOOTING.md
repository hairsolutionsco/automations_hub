# N8N Import Troubleshooting Guide

**Quick reference for solving common n8n workflow import issues**

## 🚨 Error: "request/body must NOT have additional properties"

### Problem
The workflow JSON contains properties that n8n doesn't accept during import.

### Root Cause
Exported workflows include read-only metadata that must be removed for imports.

### Solution
Remove these properties from the workflow JSON:
```bash
# Properties to REMOVE:
- id
- createdAt  
- updatedAt
- isArchived
- versionId
- triggerCount
- meta
- tags (sometimes)
- staticData
- active (set after import)
```

### Quick Fix Command
```bash
# Remove common forbidden properties
jq 'del(.id, .createdAt, .updatedAt, .isArchived, .versionId, .triggerCount, .meta, .tags, .staticData, .active)' input.json > output.json
```

---

## 🚨 Error: "request/body must have required property 'settings'"

### Problem
The workflow is missing the required `settings` property.

### Root Cause
n8n requires a `settings` object even if it's empty.

### Solution
Add to workflow root:
```json
{
  "name": "Workflow Name",
  "nodes": [...],
  "connections": {...},
  "settings": {}  // ← ADD THIS
}
```

### Quick Fix Command
```bash
# Add empty settings if missing
jq '. + {"settings": {}}' input.json > output.json
```

---

## 🚨 Error: "GitHub Push Protection - Secret Detected"

### Problem
GitHub detected API keys or secrets in the workflow files.

### Root Cause
Exported workflows contain hardcoded sensitive values.

### Patterns Detected
```bash
sk_live_*        # Stripe live keys
sk_test_*        # Stripe test keys  
whsec_*          # Webhook secrets
Bearer [token]   # Bearer tokens
api_key.*        # API key patterns
```

### Solution
Replace with n8n credential references:
```json
// ❌ WRONG (hardcoded)
"value": "Bearer sk_live_51QHt3vB4LTFfNure..."

// ✅ CORRECT (credential reference)  
"credentials": {
  "stripeApi": {
    "id": "ID3q1LYGrkaZIDtJar",
    "name": "Stripe API Key"
  }
}
```

### Quick Fix Commands
```bash
# Scan for sensitive data
grep -r "sk_live\|sk_test\|whsec_" exports/

# Remove sensitive patterns (backup first!)
sed -i 's/sk_live_[A-Za-z0-9]*/[STRIPE_API_KEY_REMOVED]/g' workflow.json
```

---

## 🚨 Error: "Status 200 but import reported as error"

### Problem
Import script reports error despite successful HTTP 200 response.

### Root Cause
Bug in import script - it misinterprets successful responses as errors.

### Reality Check
The workflow was likely imported successfully!

### Verification
```bash
# Check if workflow actually imported
./tools/export_workflows_api.sh

# Look for new workflow names in n8n interface
curl -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_CLOUD_INSTANCE_URL/api/v1/workflows" | jq '.data[].name'
```

---

## 🚨 Error: "Duplicate object key"

### Problem
JSON contains repeated keys (usually `parameters`).

### Root Cause
Malformed JSON structure during manual editing.

### Solution
Merge duplicate objects:
```json
// ❌ WRONG (duplicate parameters)
{
  "parameters": {...},
  "parameters": {...}  // Duplicate!
}

// ✅ CORRECT (single merged object)
{
  "parameters": {
    // merged properties
  }
}
```

### Quick Fix
Use a JSON validator and fix structure manually.

---

## 🚨 Error: "Invalid credential reference"

### Problem
Workflow references credentials that don't exist in target n8n instance.

### Root Cause
Credential IDs are environment-specific.

### Solution
Use the correct credential IDs for your instance:
```json
// Available credential IDs:
"hubspotAppToken": {"id": "ID4CUY90jW5ObSXedy"}
"gmailOAuth2": {"id": "IDiRhtr9mcBtiwn0Jn"}  
"openAiApi": {"id": "ID4X9TIhDpjNa5gM9J"}
"stripeApi": {"id": "ID3q1LYGrkaZIDtJar"}
"notionApi": {"id": "ID4jkKCiAXGH1iVwyi"}
```

### Verification
Check available credentials in n8n:
- Go to Settings → Credentials
- Note the correct IDs for your instance

---

## 🔧 Prevention Checklist

### Before Every Import:
1. **Clean exported workflows**
   ```bash
   # Remove forbidden properties
   jq 'del(.id, .createdAt, .updatedAt, .versionId, .triggerCount, .meta, .staticData)' 
   
   # Add required properties  
   jq '. + {"settings": {}}'
   ```

2. **Security scan**
   ```bash
   # Check for sensitive data
   grep -E "sk_|whsec_|Bearer.*[A-Za-z0-9]{20}" *.json
   ```

3. **Validate JSON**
   ```bash
   # Check syntax
   jq empty *.json && echo "Valid JSON" || echo "Invalid JSON"
   ```

4. **Dry run test**
   ```bash
   # Test before actual import
   ./tools/import_workflows_api.sh -d -s directory/
   ```

### After Import:
1. **Verify success**
   - Check n8n interface for new workflows
   - Test workflow execution
   - Verify credential connections

2. **Activate workflows**
   - Set active status in n8n interface
   - Configure any environment variables
   - Test triggers and connections

---

## 📚 Additional Resources

- **Rule Book**: `N8N_IMPORT_RULE_BOOK.md` - Complete import requirements
- **Quick Reference**: `QUICK_REFERENCE.md` - Essential commands and IDs
- **Security Guide**: `SECURITY_NOTICE.md` - Security best practices
- **Credentials Reference**: `CREDENTIALS_REFERENCE.md` - Available credential IDs

---

**Created**: August 14, 2025  
**Based on**: Real import testing and error resolution  
**Status**: Active troubleshooting guide  
**Update**: Add new errors as discovered
