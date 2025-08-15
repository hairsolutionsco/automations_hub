#!/bin/bash

# import_workflows.sh - Import workflows to n8n cloud instance
# This script imports workflows from the exports or src/workflows directory

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

# Default values
SOURCE_DIR=""
DRY_RUN=false
OVERWRITE=false

# Show usage
show_usage() {
    cat << EOF
Usage: $0 [OPTIONS] [SOURCE_DIRECTORY]

Import workflows to n8n cloud instance.

OPTIONS:
    -h, --help          Show this help message
    -d, --dry-run       Show what would be imported without actually importing
    -o, --overwrite     Overwrite existing workflows with same name
    -s, --source DIR    Source directory containing JSON workflows
                        (default: exports/ or src/workflows/)

EXAMPLES:
    $0                           # Import from exports/ directory
    $0 -s src/workflows          # Import from src/workflows directory
    $0 -d                        # Dry run - show what would be imported
    $0 -o exports/               # Import with overwrite enabled

ENVIRONMENT VARIABLES:
    N8N_CLOUD_INSTANCE_URL      n8n cloud instance URL
    N8N_API_KEY                 API key for authentication
    N8N_USER_EMAIL              User email for n8n account
EOF
}

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_usage
                exit 0
                ;;
            -d|--dry-run)
                DRY_RUN=true
                shift
                ;;
            -o|--overwrite)
                OVERWRITE=true
                shift
                ;;
            -s|--source)
                SOURCE_DIR="$2"
                shift 2
                ;;
            -*)
                print_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
            *)
                SOURCE_DIR="$1"
                shift
                ;;
        esac
    done
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

# Determine source directory
setup_source_directory() {
    local script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    local n8n_dir="$(dirname "$script_dir")"
    
    if [[ -z "$SOURCE_DIR" ]]; then
        # Try exports first, then src/workflows
        if [[ -d "$n8n_dir/exports" ]] && [[ $(ls "$n8n_dir/exports"/*.json 2>/dev/null | wc -l) -gt 0 ]]; then
            SOURCE_DIR="$n8n_dir/exports"
        elif [[ -d "$n8n_dir/src/workflows" ]] && [[ $(ls "$n8n_dir/src/workflows"/*.json 2>/dev/null | wc -l) -gt 0 ]]; then
            SOURCE_DIR="$n8n_dir/src/workflows"
        else
            print_error "No JSON workflow files found in exports/ or src/workflows/"
            print_error "Please specify a source directory with -s option"
            exit 1
        fi
    fi
    
    # Convert to absolute path
    SOURCE_DIR="$(cd "$SOURCE_DIR" && pwd)"
    
    if [[ ! -d "$SOURCE_DIR" ]]; then
        print_error "Source directory does not exist: $SOURCE_DIR"
        exit 1
    fi
    
    local file_count=$(ls "$SOURCE_DIR"/*.json 2>/dev/null | wc -l)
    if [[ $file_count -eq 0 ]]; then
        print_error "No JSON workflow files found in: $SOURCE_DIR"
        exit 1
    fi
    
    print_status "Source directory: $SOURCE_DIR ($file_count files)"
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
    
    print_success "API connectivity OK"
    rm -f /tmp/api_test.json
}

# Get existing workflows to check for conflicts
get_existing_workflows() {
    print_status "Fetching existing workflows..."
    
    curl -s \
        -H "X-N8N-API-KEY: $N8N_API_KEY" \
        -H "Content-Type: application/json" \
        "$N8N_CLOUD_INSTANCE_URL/api/v1/workflows" | \
        jq -r '.data[] | "\(.id)|\(.name)"' > /tmp/existing_workflows.txt
    
    local count=$(wc -l < /tmp/existing_workflows.txt)
    print_status "Found $count existing workflows"
}

# Check if workflow exists
workflow_exists() {
    local workflow_name="$1"
    grep -q "|$workflow_name$" /tmp/existing_workflows.txt
}

# Validate workflow JSON
validate_workflow() {
    local file="$1"
    
    # Check if file is valid JSON
    if ! jq empty "$file" 2>/dev/null; then
        print_error "Invalid JSON in file: $file"
        return 1
    fi
    
    # Check for required fields
    local name=$(jq -r '.name // empty' "$file")
    local nodes=$(jq -r '.nodes // empty' "$file")
    
    if [[ -z "$name" ]]; then
        print_error "Missing 'name' field in: $file"
        return 1
    fi
    
    if [[ -z "$nodes" ]]; then
        print_error "Missing 'nodes' field in: $file"
        return 1
    fi
    
    return 0
}

# Import single workflow
import_workflow() {
    local file="$1"
    local filename=$(basename "$file")
    
    print_status "Processing: $filename"
    
    # Validate workflow
    if ! validate_workflow "$file"; then
        return 1
    fi
    
    # Get workflow name
    local name=$(jq -r '.name' "$file")
    
    # Check for conflicts
    if workflow_exists "$name"; then
        if [[ "$OVERWRITE" = false ]]; then
            print_warning "Workflow '$name' already exists - skipping (use -o to overwrite)"
            return 0
        else
            print_warning "Workflow '$name' already exists - will overwrite"
        fi
    fi
    
    if [[ "$DRY_RUN" = true ]]; then
        print_success "Would import: $name"
        return 0
    fi
    
    # Import workflow
    local response=$(curl -s -w "%{http_code}" \
        -X POST \
        -H "X-N8N-API-KEY: $N8N_API_KEY" \
        -H "Content-Type: application/json" \
        -d @"$file" \
        "$N8N_CLOUD_INSTANCE_URL/api/v1/workflows" \
        -o /tmp/import_response.json)
    
    if [[ "$response" = "201" ]]; then
        local workflow_id=$(jq -r '.id' /tmp/import_response.json)
        print_success "Imported: $name (ID: $workflow_id)"
    else
        print_error "Failed to import: $name (Status: $response)"
        print_error "Response: $(cat /tmp/import_response.json)"
        return 1
    fi
    
    rm -f /tmp/import_response.json
}

# Import all workflows
import_workflows() {
    if [[ "$DRY_RUN" = true ]]; then
        print_status "DRY RUN - No workflows will be actually imported"
    fi
    
    print_status "Importing workflows from: $SOURCE_DIR"
    
    local total_files=0
    local success_count=0
    local error_count=0
    
    for file in "$SOURCE_DIR"/*.json; do
        if [[ -f "$file" ]]; then
            total_files=$((total_files + 1))
            
            if import_workflow "$file"; then
                success_count=$((success_count + 1))
            else
                error_count=$((error_count + 1))
            fi
        fi
    done
    
    print_status "Import Summary:"
    print_status "  Total files: $total_files"
    print_success "  Successful: $success_count"
    if [[ $error_count -gt 0 ]]; then
        print_error "  Errors: $error_count"
    fi
    
    # Clean up
    rm -f /tmp/existing_workflows.txt
}

# Main execution
main() {
    print_status "Starting n8n workflow import..."
    
    check_environment
    setup_source_directory
    test_api
    get_existing_workflows
    import_workflows
    
    if [[ "$DRY_RUN" = true ]]; then
        print_status "Dry run completed - no changes made"
    else
        print_success "Import process completed!"
    fi
}

# Parse arguments and run
parse_args "$@"
main
