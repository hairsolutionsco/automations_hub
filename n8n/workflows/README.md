# Workflows Directory

## ⚠️ Important Notice

The workflow files in this directory were found corrupted during the August 14, 2025 review.
They contained `{"message": "Not Found"}` instead of actual workflow data.

## Restored Files

- `email-management.json` - Reset to basic template (originally corrupted)
- `test-agent-send-vincent-email.json` - Reset to basic template (originally corrupted)

## Actual Working Workflows

The **real, working workflows** are in the `exports/` directory:
- 9 workflows successfully exported from n8n cloud
- 196K total size
- Exported using REST API (proven method)

## Recommendation

1. **Use workflows from `exports/` directory** - these are the actual working workflows
2. **Recreate any needed workflows** in n8n cloud interface
3. **Export again using REST API** to keep this directory in sync

## Export Command

```bash
# Export latest workflows from cloud
./tools/export_workflows_api.sh
```

---
**Corruption discovered**: August 14, 2025  
**Action taken**: Reset to template structure  
**Working workflows**: Available in `exports/` directory
