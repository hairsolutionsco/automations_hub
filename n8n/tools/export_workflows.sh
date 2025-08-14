#!/bin/bash

# export_workflows.sh - Export all workflows from n8n cloud instance
# This script exports all workflows and saves them with proper naming

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

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
    
    if [[ -z "$N8N_USER_EMAIL" ]]; then
        print_error "N8N_USER_EMAIL is not set"
        exit 1
    fi
    
    print_success "Environment variables OK"
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
        print_error "Response: $(cat /tmp/api_test.json)"
        exit 1
    fi
    
    local workflow_count=$(jq '.data | length' /tmp/api_test.json)
    print_success "API connectivity OK - Found $workflow_count workflows"
    rm -f /tmp/api_test.json
}

# Create exports directory
setup_directories() {
    print_status "Setting up directories..."
    
    local script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    local n8n_dir="$(dirname "$script_dir")"
    local exports_dir="$n8n_dir/exports"
    
    mkdir -p "$exports_dir"
    cd "$exports_dir"
    
    # Create backup of previous exports
    if [[ $(ls *.json 2>/dev/null | wc -l) -gt 0 ]]; then
        local backup_dir="backup_$(date +%Y%m%d_%H%M%S)"
        mkdir -p "$backup_dir"
        mv *.json "$backup_dir/" 2>/dev/null || true
        print_status "Previous exports backed up to $backup_dir"
    fi
    
    print_success "Directories ready: $exports_dir"
}

# Export all workflows
export_workflows() {
    print_status "Exporting workflows..."
    
    # Get workflow list
    local workflows=$(curl -s \
        -H "X-N8N-API-KEY: $N8N_API_KEY" \
        -H "Content-Type: application/json" \
        "$N8N_CLOUD_INSTANCE_URL/api/v1/workflows" | \
        jq -r '.data[] | "\(.id)|\(.name)"')
    
    if [[ -z "$workflows" ]]; then
        print_warning "No workflows found to export"
        return 0
    fi
    
    local count=0
    local total=$(echo "$workflows" | wc -l)
    
    echo "$workflows" | while IFS='|' read -r id name; do
        count=$((count + 1))
        print_status "Exporting [$count/$total]: $name ($id)"
        
        # Clean filename - remove/replace problematic characters
        local filename=$(echo "$name" | \
            sed 's/[[:space:]]/_/g' | \
            sed 's/[^a-zA-Z0-9._-]//g' | \
            cut -c1-50)  # Limit length
        
        # Export workflow
        local output_file="${id}_${filename}.json"
        
        if curl -s \
            -H "X-N8N-API-KEY: $N8N_API_KEY" \
            "$N8N_CLOUD_INSTANCE_URL/api/v1/workflows/$id" | \
            jq '.' > "$output_file"; then
            
            local file_size=$(du -h "$output_file" | cut -f1)
            print_success "Exported: $output_file ($file_size)"
        else
            print_error "Failed to export workflow: $name ($id)"
            rm -f "$output_file"
        fi
    done
    
    print_success "Export completed!"
}

# Generate export summary
generate_summary() {
    print_status "Generating export summary..."
    
    local total_files=$(ls *.json 2>/dev/null | wc -l)
    local total_size=$(du -sh . | cut -f1)
    local export_date=$(date)
    
    cat > README.md << EOF
# Exported Workflows

This directory contains workflows exported from the n8n cloud instance.

## Export Summary

- **Export Date**: $export_date
- **Total Workflows**: $total_files
- **Total Size**: $total_size
- **Source Instance**: $N8N_CLOUD_INSTANCE_URL

## Exported Files

| Workflow ID | File Name | Size | Last Modified |
|-------------|-----------|------|---------------|
EOF
    
    # Add file details to README
    for file in *.json; do
        if [[ -f "$file" ]]; then
            local id=$(echo "$file" | cut -d'_' -f1)
            local size=$(du -h "$file" | cut -f1)
            local modified=$(stat -c %y "$file" | cut -d' ' -f1)
            echo "| \`$id\` | $file | $size | $modified |" >> README.md
        fi
    done
    
    cat >> README.md << EOF

## Usage

These files can be:
- Imported back to n8n using the CLI or API
- Processed for GitOps integration
- Used as workflow templates
- Backed up for disaster recovery

## Import Commands

\`\`\`bash
# Import specific workflow
n8n import:workflow --input=$file

# Import all workflows
for file in *.json; do
  n8n import:workflow --input="\$file"
done
\`\`\`

---

*Generated automatically by export_workflows.sh*
EOF
    
    print_success "Summary generated: README.md"
}

# Main execution
main() {
    print_status "Starting n8n workflow export..."
    print_status "Instance: $N8N_CLOUD_INSTANCE_URL"
    
    check_environment
    test_api
    setup_directories
    export_workflows
    generate_summary
    
    print_success "Export process completed successfully!"
    print_status "Exported workflows are available in: $(pwd)"
}

# Run main function
main "$@"
