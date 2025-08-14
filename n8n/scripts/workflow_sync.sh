#!/bin/bash

# Enhanced N8N Workflow Management Script
# Provides a comprehensive system for importing, modifying, and pushing back automation JSON files

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
N8N_DIR="$(dirname "$SCRIPT_DIR")"
WORKFLOWS_DIR="$N8N_DIR/workflows"
BACKUPS_DIR="$WORKFLOWS_DIR/backups"
MANAGER_SCRIPT="$N8N_DIR/n8n_workflow_manager.py"

# Ensure directories exist
mkdir -p "$WORKFLOWS_DIR" "$BACKUPS_DIR"

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

print_section() {
    echo -e "\n${PURPLE}=== $1 ===${NC}"
}

# Function to check dependencies
check_dependencies() {
    print_section "Checking Dependencies"
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is required but not installed"
        exit 1
    fi
    print_success "Python 3 found"
    
    # Check required Python packages
    python3 -c "import httpx, asyncio" 2>/dev/null || {
        print_warning "Installing required Python packages..."
        pip install httpx asyncio
    }
    print_success "Python dependencies satisfied"
    
    # Check environment variables
    if [[ -z "$N8N_CLOUD_INSTANCE_URL" || -z "$N8N_API_KEY" ]]; then
        print_warning "N8N cloud credentials not fully configured"
        echo "Please set the following environment variables:"
        echo "  export N8N_CLOUD_INSTANCE_URL='https://your-instance.app.n8n.cloud'"
        echo "  export N8N_API_KEY='your-api-key'"
        echo "  export N8N_USER_EMAIL='your-email@domain.com'  # Optional"
        echo ""
        echo "You can add these to your ~/.bashrc or ~/.zshrc file"
    else
        print_success "N8N cloud credentials configured"
    fi
}

# Function to display main menu
show_menu() {
    clear
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                    N8N Workflow Manager                      ║"
    echo "║              Import • Modify • Push System                   ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    echo -e "${YELLOW}📋 WORKFLOW OPERATIONS:${NC}"
    echo "  1. List all workflows (cloud + local)"
    echo "  2. Download all workflows from cloud"
    echo "  3. Download specific workflow"
    echo "  4. Upload all local workflows to cloud"
    echo "  5. Upload specific workflow"
    echo ""
    
    echo -e "${YELLOW}🔧 MODIFICATION TOOLS:${NC}"
    echo "  6. Modify workflow properties"
    echo "  7. Validate workflow file"
    echo "  8. Create workflow backup"
    echo ""
    
    echo -e "${YELLOW}🔄 SYNC OPERATIONS:${NC}"
    echo "  9. Two-way sync (smart merge)"
    echo " 10. Compare local vs cloud"
    echo " 11. Restore from backup"
    echo ""
    
    echo -e "${YELLOW}🛠️  UTILITIES:${NC}"
    echo " 12. Setup environment"
    echo " 13. Check workflow status"
    echo " 14. Export workflow templates"
    echo ""
    
    echo -e "${YELLOW}⚡ QUICK ACTIONS:${NC}"
    echo " 15. Quick sync from cloud"
    echo " 16. Quick push to cloud"
    echo ""
    
    echo "  0. Exit"
    echo ""
}

# Function to list workflows
list_workflows() {
    print_section "Listing Workflows"
    
    if [[ -f "$MANAGER_SCRIPT" ]]; then
        python3 "$MANAGER_SCRIPT" list
    else
        print_error "Workflow manager script not found at $MANAGER_SCRIPT"
        return 1
    fi
}

# Function to download all workflows
download_all_workflows() {
    print_section "Downloading All Workflows from Cloud"
    
    read -p "Create backup of existing workflows? (Y/n): " backup_choice
    backup_flag=""
    if [[ "$backup_choice" != "n" && "$backup_choice" != "N" ]]; then
        backup_flag="--backup"
    fi
    
    if [[ -f "$MANAGER_SCRIPT" ]]; then
        python3 "$MANAGER_SCRIPT" download --all $backup_flag
    else
        print_error "Workflow manager script not found"
        return 1
    fi
}

# Function to download specific workflow
download_specific_workflow() {
    print_section "Downloading Specific Workflow"
    
    # First list cloud workflows to help user choose
    print_status "Available cloud workflows:"
    python3 "$MANAGER_SCRIPT" list --cloud 2>/dev/null || {
        print_error "Failed to list cloud workflows"
        return 1
    }
    
    echo ""
    read -p "Enter workflow ID to download: " workflow_id
    
    if [[ -n "$workflow_id" ]]; then
        python3 "$MANAGER_SCRIPT" download --id "$workflow_id"
    else
        print_error "No workflow ID provided"
    fi
}

# Function to upload all workflows
upload_all_workflows() {
    print_section "Uploading All Local Workflows to Cloud"
    
    local_count=$(find "$WORKFLOWS_DIR" -name "*.json" -not -name "backup_*" | wc -l)
    
    if [[ $local_count -eq 0 ]]; then
        print_warning "No local workflow files found in $WORKFLOWS_DIR"
        return 1
    fi
    
    print_status "Found $local_count local workflow files"
    read -p "Continue with upload? (y/N): " confirm
    
    if [[ "$confirm" == "y" || "$confirm" == "Y" ]]; then
        python3 "$MANAGER_SCRIPT" upload --all
    else
        print_status "Upload cancelled"
    fi
}

# Function to upload specific workflow
upload_specific_workflow() {
    print_section "Uploading Specific Workflow"
    
    # List local workflows
    print_status "Available local workflows:"
    local files=($(find "$WORKFLOWS_DIR" -name "*.json" -not -name "backup_*" -exec basename {} \;))
    
    if [[ ${#files[@]} -eq 0 ]]; then
        print_warning "No local workflow files found"
        return 1
    fi
    
    for i in "${!files[@]}"; do
        echo "  $((i+1)). ${files[$i]}"
    done
    
    echo ""
    read -p "Enter file number or filename: " selection
    
    local file_to_upload=""
    
    # Check if it's a number
    if [[ "$selection" =~ ^[0-9]+$ ]]; then
        if [[ $selection -ge 1 && $selection -le ${#files[@]} ]]; then
            file_to_upload="$WORKFLOWS_DIR/${files[$((selection-1))]}"
        else
            print_error "Invalid selection"
            return 1
        fi
    else
        # Treat as filename
        if [[ -f "$WORKFLOWS_DIR/$selection" ]]; then
            file_to_upload="$WORKFLOWS_DIR/$selection"
        else
            print_error "File not found: $selection"
            return 1
        fi
    fi
    
    # Check if this is an update to existing workflow
    read -p "Is this an update to an existing workflow? (y/N): " is_update
    
    workflow_id=""
    if [[ "$is_update" == "y" || "$is_update" == "Y" ]]; then
        read -p "Enter existing workflow ID: " workflow_id
    fi
    
    if [[ -n "$workflow_id" ]]; then
        python3 "$MANAGER_SCRIPT" upload --file "$file_to_upload" --id "$workflow_id"
    else
        python3 "$MANAGER_SCRIPT" upload --file "$file_to_upload"
    fi
}

# Function to modify workflow
modify_workflow() {
    print_section "Modifying Workflow Properties"
    
    # List local workflows
    print_status "Available local workflows:"
    local files=($(find "$WORKFLOWS_DIR" -name "*.json" -not -name "backup_*" -exec basename {} \;))
    
    if [[ ${#files[@]} -eq 0 ]]; then
        print_warning "No local workflow files found"
        return 1
    fi
    
    for i in "${!files[@]}"; do
        echo "  $((i+1)). ${files[$i]}"
    done
    
    echo ""
    read -p "Enter file number or filename: " selection
    
    local file_to_modify=""
    
    # Check if it's a number
    if [[ "$selection" =~ ^[0-9]+$ ]]; then
        if [[ $selection -ge 1 && $selection -le ${#files[@]} ]]; then
            file_to_modify="$WORKFLOWS_DIR/${files[$((selection-1))]}"
        else
            print_error "Invalid selection"
            return 1
        fi
    else
        # Treat as filename
        if [[ -f "$WORKFLOWS_DIR/$selection" ]]; then
            file_to_modify="$WORKFLOWS_DIR/$selection"
        else
            print_error "File not found: $selection"
            return 1
        fi
    fi
    
    echo ""
    echo "What would you like to modify?"
    echo "1. Workflow name"
    echo "2. Active status"
    echo "3. Both"
    
    read -p "Enter choice (1-3): " mod_choice
    
    case $mod_choice in
        1)
            read -p "Enter new workflow name: " new_name
            if [[ -n "$new_name" ]]; then
                python3 "$MANAGER_SCRIPT" modify "$file_to_modify" --name "$new_name"
            fi
            ;;
        2)
            read -p "Set active status (true/false): " active_status
            if [[ "$active_status" == "true" || "$active_status" == "false" ]]; then
                python3 "$MANAGER_SCRIPT" modify "$file_to_modify" --active "$active_status"
            else
                print_error "Invalid active status. Use 'true' or 'false'"
            fi
            ;;
        3)
            read -p "Enter new workflow name: " new_name
            read -p "Set active status (true/false): " active_status
            
            args=""
            if [[ -n "$new_name" ]]; then
                args="$args --name \"$new_name\""
            fi
            if [[ "$active_status" == "true" || "$active_status" == "false" ]]; then
                args="$args --active $active_status"
            fi
            
            if [[ -n "$args" ]]; then
                eval "python3 \"$MANAGER_SCRIPT\" modify \"$file_to_modify\" $args"
            else
                print_error "No valid modifications specified"
            fi
            ;;
        *)
            print_error "Invalid choice"
            ;;
    esac
}

# Function to validate workflow
validate_workflow() {
    print_section "Validating Workflow File"
    
    # List local workflows
    print_status "Available local workflows:"
    local files=($(find "$WORKFLOWS_DIR" -name "*.json" -not -name "backup_*" -exec basename {} \;))
    
    if [[ ${#files[@]} -eq 0 ]]; then
        print_warning "No local workflow files found"
        return 1
    fi
    
    for i in "${!files[@]}"; do
        echo "  $((i+1)). ${files[$i]}"
    done
    
    echo ""
    read -p "Enter file number, filename, or 'all' for all files: " selection
    
    if [[ "$selection" == "all" ]]; then
        for file in "${files[@]}"; do
            print_status "Validating $file..."
            python3 "$MANAGER_SCRIPT" validate "$WORKFLOWS_DIR/$file"
        done
    elif [[ "$selection" =~ ^[0-9]+$ ]]; then
        if [[ $selection -ge 1 && $selection -le ${#files[@]} ]]; then
            python3 "$MANAGER_SCRIPT" validate "$WORKFLOWS_DIR/${files[$((selection-1))]}"
        else
            print_error "Invalid selection"
        fi
    else
        if [[ -f "$WORKFLOWS_DIR/$selection" ]]; then
            python3 "$MANAGER_SCRIPT" validate "$WORKFLOWS_DIR/$selection"
        else
            print_error "File not found: $selection"
        fi
    fi
}

# Function to create backup
create_backup() {
    print_section "Creating Workflow Backup"
    
    python3 "$MANAGER_SCRIPT" backup
}

# Function for quick sync from cloud
quick_sync_from_cloud() {
    print_section "Quick Sync from Cloud"
    print_warning "This will download all workflows from cloud and may overwrite local files"
    
    read -p "Continue? (y/N): " confirm
    
    if [[ "$confirm" == "y" || "$confirm" == "Y" ]]; then
        python3 "$MANAGER_SCRIPT" download --all --backup
    else
        print_status "Quick sync cancelled"
    fi
}

# Function for quick push to cloud
quick_push_to_cloud() {
    print_section "Quick Push to Cloud"
    print_warning "This will upload all local workflows to cloud"
    
    local_count=$(find "$WORKFLOWS_DIR" -name "*.json" -not -name "backup_*" | wc -l)
    print_status "Found $local_count local workflow files"
    
    read -p "Continue? (y/N): " confirm
    
    if [[ "$confirm" == "y" || "$confirm" == "Y" ]]; then
        python3 "$MANAGER_SCRIPT" upload --all
    else
        print_status "Quick push cancelled"
    fi
}

# Function to setup environment
setup_environment() {
    print_section "Environment Setup"
    
    echo "Current environment variables:"
    echo "N8N_CLOUD_INSTANCE_URL: ${N8N_CLOUD_INSTANCE_URL:-'Not set'}"
    echo "N8N_API_KEY: ${N8N_API_KEY:+Set}${N8N_API_KEY:-'Not set'}"
    echo "N8N_USER_EMAIL: ${N8N_USER_EMAIL:-'Not set'}"
    echo ""
    
    read -p "Would you like to set these now? (y/N): " setup_vars
    
    if [[ "$setup_vars" == "y" || "$setup_vars" == "Y" ]]; then
        read -p "Enter N8N Cloud Instance URL: " new_url
        read -p "Enter N8N API Key: " new_key
        read -p "Enter N8N User Email (optional): " new_email
        
        # Create or update .env file
        env_file="$N8N_DIR/.env"
        
        echo "# N8N Configuration" > "$env_file"
        echo "N8N_CLOUD_INSTANCE_URL=\"$new_url\"" >> "$env_file"
        echo "N8N_API_KEY=\"$new_key\"" >> "$env_file"
        if [[ -n "$new_email" ]]; then
            echo "N8N_USER_EMAIL=\"$new_email\"" >> "$env_file"
        fi
        
        print_success "Configuration saved to $env_file"
        print_status "To load these variables, run: source $env_file"
    fi
}

# Function to check workflow status
check_workflow_status() {
    print_section "Workflow Status Check"
    
    print_status "Local workflows:"
    ls -la "$WORKFLOWS_DIR"/*.json 2>/dev/null | grep -v backup_ || echo "No local workflows found"
    
    echo ""
    print_status "Recent backups:"
    ls -la "$BACKUPS_DIR" 2>/dev/null || echo "No backups found"
    
    echo ""
    if [[ -f "$MANAGER_SCRIPT" ]]; then
        print_status "Cloud workflows:"
        python3 "$MANAGER_SCRIPT" list --cloud
    fi
}

# Main script execution
main() {
    # Source environment file if it exists
    if [[ -f "$N8N_DIR/.env" ]]; then
        source "$N8N_DIR/.env"
    fi
    
    # Check dependencies
    check_dependencies
    
    while true; do
        show_menu
        read -p "Enter your choice (0-16): " choice
        
        case $choice in
            1) list_workflows ;;
            2) download_all_workflows ;;
            3) download_specific_workflow ;;
            4) upload_all_workflows ;;
            5) upload_specific_workflow ;;
            6) modify_workflow ;;
            7) validate_workflow ;;
            8) create_backup ;;
            9) print_warning "Two-way sync not implemented yet" ;;
            10) print_warning "Compare function not implemented yet" ;;
            11) print_warning "Restore from backup not implemented yet" ;;
            12) setup_environment ;;
            13) check_workflow_status ;;
            14) print_warning "Export templates not implemented yet" ;;
            15) quick_sync_from_cloud ;;
            16) quick_push_to_cloud ;;
            0) 
                print_success "Goodbye!"
                exit 0
                ;;
            *)
                print_error "Invalid choice. Please try again."
                ;;
        esac
        
        echo ""
        read -p "Press Enter to continue..."
    done
}

# Run the main function
main "$@"
