# N8N Import Rule Book

**A comprehensive guide for successful workflow imports to n8n cloud instances**

## 🚨 Critical Discovery Summary

After extensive testing with n8n REST API imports, we discovered specific requirements and limitations that are **not documented** in the official n8n API documentation.

## ✅ Required Properties for Import

### Mandatory Workflow Structure
```json
{
  "name": "Workflow Name",
  "nodes": [...],
  "connections": {},
  "settings": {}
}
```

**❌ FAILS WITHOUT:** `settings` property is **required** even if empty
**✅ WORKS WITH:** `"settings": {}` minimum requirement

## ❌ Forbidden Properties for Import

### Properties That Must Be Removed
- `id` - Workflow ID (auto-generated on import)
- `createdAt` - Creation timestamp (auto-generated)
- `updatedAt` - Update timestamp (auto-generated)
- `isArchived` - Archive status (not accepted in imports)
- `versionId` - Version identifier (auto-generated)
- `triggerCount` - Trigger count (calculated by n8n)
- `meta` - Metadata object (rejected during import)
- `tags` - Tag arrays (often rejected, safer to add after import)
- `staticData` - Static data (auto-initialized)
- `active` - Active status (can be set after import)

## 🔧 Node-Specific Requirements

### Credential References
**✅ CORRECT FORMAT:**
```json
"credentials": {
  "stripeApi": {
    "id": "ID3q1LYGrkaZIDtJar",
    "name": "Stripe API Key"
  }
}
```

**❌ WRONG FORMAT:**
```json
"credentials": {
  "stripeApi": "ID3q1LYGrkaZIDtJar"  // Missing name property
}
```

### Position Arrays
**✅ REQUIRED:** All nodes must have `position` array
```json
"position": [240, 300]  // [x, y] coordinates
```

### Node IDs
**✅ REQUIRED:** Each node must have unique `id`
```json
"id": "unique-node-identifier"
```

## 🚫 Common Import Errors

### Error 1: "request/body must NOT have additional properties"
**Cause:** Including read-only properties in workflow JSON
**Solution:** Remove `id`, `createdAt`, `updatedAt`, `versionId`, `meta`, etc.

### Error 2: "request/body must have required property 'settings'"
**Cause:** Missing `settings` property
**Solution:** Add `"settings": {}` to workflow root

### Error 3: "Status 200 but reports as error"
**Cause:** Import script misinterpreting successful responses
**Reality:** Workflow was actually imported successfully
**Verification:** Check with export or n8n interface

### Error 4: "Duplicate object key"
**Cause:** JSON structure with repeated `parameters` keys
**Solution:** Merge parameters into single object

## 🔒 Security Requirements

### Sensitive Data Patterns to Remove
```bash
# Scan for these patterns before import:
sk_live_*        # Stripe live API keys
sk_test_*        # Stripe test API keys
whsec_*          # Webhook secrets
Bearer [A-Za-z0-9]{20,}  # Bearer tokens
api_key.*        # API key patterns
```

### Safe Credential References
Use n8n credential IDs instead of hardcoded values:
```json
"credentials": {
  "credentialType": {
    "id": "IDxxxxxxxxx",
    "name": "Credential Name"
  }
}
```

## 📋 Pre-Import Checklist

### Before Importing Any Workflow:
1. **Remove read-only properties**
   - [ ] `id`, `createdAt`, `updatedAt` removed
   - [ ] `versionId`, `triggerCount` removed
   - [ ] `meta`, `tags`, `staticData` removed

2. **Add required properties**
   - [ ] `settings: {}` exists
   - [ ] `connections: {}` exists (even if empty)

3. **Validate node structure**
   - [ ] All nodes have `id`, `name`, `type`, `position`
   - [ ] Credentials use proper format with `id` and `name`
   - [ ] No duplicate JSON keys

4. **Security scan**
   - [ ] No hardcoded API keys or tokens
   - [ ] Sensitive data replaced with credential references
   - [ ] Environment variables used for database IDs

5. **JSON validation**
   - [ ] Valid JSON syntax
   - [ ] No trailing commas
   - [ ] Proper nesting and brackets

## 🛠️ Import Script Behavior

### Expected Response Patterns
- **Success**: HTTP 200/201 with workflow ID in response
- **Error**: HTTP 400+ with error message
- **False Positive**: Script reports error on 200 status (bug in script)

### Verification Commands
```bash
# Test import (dry run)
./tools/import_workflows_api.sh -d -s directory/

# Actual import
./tools/import_workflows_api.sh -s directory/

# Verify import success
./tools/export_workflows_api.sh
```

## 📚 Lessons Learned

### 1. n8n API Documentation is Incomplete
- Required `settings` property not documented
- Forbidden properties not clearly listed
- Error messages sometimes misleading

### 2. Import vs Export Formats Differ
- Export includes read-only metadata
- Import requires clean, minimal structure
- Must transform exported workflows before re-import

### 3. Security Scanning is Essential
- GitHub secret scanning blocks commits with API keys
- Manual review required for all exported workflows
- Credential ID system is the safe approach

### 4. Testing Strategy
- Always dry-run first
- Verify import by re-exporting
- Test with minimal workflows before complex ones

## 🔄 Workflow Transformation Process

### From Export to Import-Ready
1. **Remove forbidden properties**: `id`, `createdAt`, etc.
2. **Add required properties**: `settings: {}`
3. **Replace sensitive data**: Use credential IDs
4. **Validate JSON**: Check syntax and structure
5. **Test import**: Dry run first
6. **Verify success**: Export to confirm

## 💡 Best Practices

### Workflow Design
- Use n8n credentials for all API access
- Environment variables for configuration
- Descriptive node names and documentation
- Minimal required structure for imports

### Security
- Never commit workflows with hardcoded secrets
- Regular security scans of export directories
- Credential rotation without workflow changes
- Environment-specific configurations

### Testing
- Develop in isolated n8n instance
- Export/import cycle testing
- Validate in production environment
- Backup before major changes

---

**Last Updated**: August 14, 2025  
**Based on**: Extensive testing with n8n cloud REST API  
**Status**: Active rulebook - update as new patterns discovered  
**Next Actions**: Continue building rules as edge cases found
