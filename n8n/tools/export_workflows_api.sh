#!/bin/bash

# export_workflows_api.sh - Export workflows using REST API (PROVEN METHOD)
# This script uses REST API calls which actually work with n8n cloud instances

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Check required environment variables
check_environment() {
    print_status "Checking environment variables..."
    
    if [[ -z "$N8N_CLOUD_INSTANCE_URL" ]]; then
        print_error "N8N_CLOUD_INSTANCE_URL is not set"
        exit 1
    fi
    
    if [[ -z "$N8N_API_KEY" ]]; then
        print_error "N8N_API_KEY is not set"
        exit 1
    fi
    
    print_success "Environment variables OK"
    print_status "Instance: $N8N_CLOUD_INSTANCE_URL"
}

# Test API connectivity
test_api() {
    print_status "Testing API connectivity..."
    
    local response=$(curl -s -w "%{http_code}" \
        -H "X-N8N-API-KEY: $N8N_API_KEY" \
        -H "Content-Type: application/json" \
        "$N8N_CLOUD_INSTANCE_URL/api/v1/workflows" \
        -o /tmp/api_test.json)
    
    if [[ "$response" != "200" ]]; then
        print_error "API test failed with status: $response"
        exit 1
    fi
    
    local workflow_count=$(jq '.data | length' /tmp/api_test.json)
    print_success "API connectivity OK - Found $workflow_count workflows"
    rm -f /tmp/api_test.json
}

# Setup directories
setup_directories() {
    local script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    local n8n_dir="$(dirname "$script_dir")"
    local exports_dir="$n8n_dir/exports"
    
    mkdir -p "$exports_dir"
    cd "$exports_dir"
    
    # Backup existing exports
    if [[ $(ls *.json 2>/dev/null | wc -l) -gt 0 ]]; then
        local backup_dir="backup_$(date +%Y%m%d_%H%M%S)"
        mkdir -p "$backup_dir"
        mv *.json "$backup_dir/" 2>/dev/null || true
        print_status "Previous exports backed up to $backup_dir"
    fi
    
    print_success "Export directory ready: $exports_dir"
}

# Export workflows using REST API
export_workflows() {
    print_status "Fetching workflow list..."
    
    # Get workflow list using REST API
    local workflows=$(curl -s \
        -H "X-N8N-API-KEY: $N8N_API_KEY" \
        -H "Content-Type: application/json" \
        "$N8N_CLOUD_INSTANCE_URL/api/v1/workflows" | \
        jq -r '.data[] | "\(.id)|\(.name)"')
    
    if [[ -z "$workflows" ]]; then
        print_error "No workflows found"
        return 1
    fi
    
    local count=0
    local total=$(echo "$workflows" | wc -l)
    
    print_status "Exporting $total workflows..."
    
    echo "$workflows" | while IFS='|' read -r id name; do
        count=$((count + 1))
        print_status "[$count/$total] Exporting: $name ($id)"
        
        # Clean filename
        local safe_name=$(echo "$name" | sed 's/[^a-zA-Z0-9._-]/_/g' | cut -c1-50)
        local output_file="${id}_${safe_name}.json"
        
        # Export workflow using REST API
        if curl -s \
            -H "X-N8N-API-KEY: $N8N_API_KEY" \
            "$N8N_CLOUD_INSTANCE_URL/api/v1/workflows/$id" | \
            jq '.' > "$output_file"; then
            
            local file_size=$(du -h "$output_file" | cut -f1)
            print_success "✓ $output_file ($file_size)"
        else
            print_error "✗ Failed: $name ($id)"
            rm -f "$output_file"
        fi
    done
}

# Generate summary
generate_summary() {
    local export_date=$(date)
    local total_files=$(ls *.json 2>/dev/null | wc -l)
    local total_size=$(du -sh . 2>/dev/null | cut -f1)
    
    cat > README.md << EOF
# N8N Workflows Export

**IMPORTANT**: These workflows were exported using **REST API calls**, not n8n CLI commands.
The n8n CLI does NOT work reliably with cloud instances.

## Export Summary

- **Export Date**: $export_date
- **Total Workflows**: $total_files
- **Total Size**: $total_size
- **Source**: $N8N_CLOUD_INSTANCE_URL
- **Method**: REST API (proven working method)

## Workflow Files

| Workflow ID | File Name | Size |
|-------------|-----------|------|
EOF
    
    for file in *.json; do
        if [[ -f "$file" ]]; then
            local id=$(echo "$file" | cut -d'_' -f1)
            local size=$(du -h "$file" | cut -f1)
            echo "| \`$id\` | $file | $size |" >> README.md
        fi
    done
    
    cat >> README.md << EOF

## Import Methods

### REST API (Recommended - Always Works)
\`\`\`bash
# Import specific workflow
curl -X POST \\
  -H "X-N8N-API-KEY: \$N8N_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d @workflow_file.json \\
  "\$N8N_CLOUD_INSTANCE_URL/api/v1/workflows"
\`\`\`

### n8n CLI (Local Instance Only)
\`\`\`bash
# Only works with local n8n instances, NOT cloud
n8n import:workflow --input=workflow_file.json
\`\`\`

## Critical Notes for Future Agents

🚨 **IMPORTANT**: n8n CLI commands (export:workflow, import:workflow) do NOT work with cloud instances.
Always use REST API calls for cloud workflows.

Environment variables required:
- N8N_CLOUD_INSTANCE_URL
- N8N_API_KEY
- N8N_USER_EMAIL (optional)

---
*Generated by export_workflows_api.sh - The proven working method*
EOF
    
    print_success "Summary generated: README.md"
}

# Main execution
main() {
    print_status "Starting n8n workflow export using REST API..."
    
    check_environment
    test_api
    setup_directories
    export_workflows
    generate_summary
    
    print_success "Export completed successfully!"
    print_status "Files available in: $(pwd)"
}

main "$@"
