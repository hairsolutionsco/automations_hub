#!/bin/bash

# N8N Native Git Sync System
# Leverages n8n's built-in export/import capabilities with Git version control

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
CREDENTIALS_DIR="$N8N_DIR/credentials"

# Ensure directories exist
mkdir -p "$WORKFLOWS_DIR" "$CREDENTIALS_DIR"

# Function to print colored output
print_status() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }
print_section() { echo -e "\n${PURPLE}=== $1 ===${NC}"; }

# Function to check if we're in a git repository
check_git_repo() {
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        print_warning "Not in a Git repository. Initialize one?"
        read -p "Initialize Git repo? (y/N): " init_git
        if [[ "$init_git" == "y" || "$init_git" == "Y" ]]; then
            git init
            git add .
            git commit -m "Initial commit: N8N workflows repository"
            print_success "Git repository initialized"
        else
            print_error "Git is required for version control features"
            return 1
        fi
    fi
}

# Function to show main menu
show_menu() {
    clear
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                N8N Native Git Sync System                   ║"
    echo "║         Using n8n's built-in export/import commands         ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    echo -e "${YELLOW}📥 EXPORT FROM N8N (Download):${NC}"
    echo "  1. Export all workflows (n8n → Git)"
    echo "  2. Export all credentials (n8n → Git)"
    echo "  3. Export everything (workflows + credentials)"
    echo ""
    
    echo -e "${YELLOW}📤 IMPORT TO N8N (Upload):${NC}"
    echo "  4. Import all workflows (Git → n8n)"
    echo "  5. Import all credentials (Git → n8n)"
    echo "  6. Import everything (workflows + credentials)"
    echo ""
    
    echo -e "${YELLOW}🔄 GIT OPERATIONS:${NC}"
    echo "  7. Commit current changes"
    echo "  8. Push to remote repository"
    echo "  9. Pull from remote repository"
    echo " 10. Show Git status"
    echo ""
    
    echo -e "${YELLOW}🔧 UTILITIES:${NC}"
    echo " 11. Setup Git repository"
    echo " 12. Validate workflow files"
    echo " 13. Show n8n connection status"
    echo ""
    
    echo -e "${YELLOW}⚡ SMART SYNC:${NC}"
    echo " 14. Full export + commit + push"
    echo " 15. Pull + import to n8n"
    echo ""
    
    echo "  0. Exit"
    echo ""
}

# Function to export workflows using n8n native command
export_workflows() {
    print_section "Exporting Workflows (n8n → Git)"
    
    # Use n8n's native export with separate files for better Git diff support
    print_status "Running: n8n export:workflow --backup --output=$WORKFLOWS_DIR/"
    
    if n8n export:workflow --backup --output="$WORKFLOWS_DIR/"; then
        print_success "Workflows exported successfully to $WORKFLOWS_DIR/"
        
        # Show what was exported
        workflow_count=$(find "$WORKFLOWS_DIR" -name "*.json" 2>/dev/null | wc -l)
        print_status "Exported $workflow_count workflow files"
        
        return 0
    else
        print_error "Failed to export workflows"
        return 1
    fi
}

# Function to export credentials using n8n native command
export_credentials() {
    print_section "Exporting Credentials (n8n → Git)"
    
    # Create credentials export
    cred_file="$CREDENTIALS_DIR/credentials.json"
    print_status "Running: n8n export:credentials --output=$cred_file"
    
    if n8n export:credentials --output="$cred_file"; then
        print_success "Credentials exported successfully to $cred_file"
        
        # Security warning
        print_warning "⚠️  IMPORTANT: Credentials contain sensitive data!"
        print_warning "    Make sure to review before committing to Git"
        print_warning "    Consider using .gitignore for sensitive files"
        
        return 0
    else
        print_error "Failed to export credentials"
        return 1
    fi
}

# Function to import workflows using n8n native command
import_workflows() {
    print_section "Importing Workflows (Git → n8n)"
    
    if [[ ! -d "$WORKFLOWS_DIR" ]] || [[ -z "$(ls -A "$WORKFLOWS_DIR" 2>/dev/null)" ]]; then
        print_error "No workflows directory found or directory is empty"
        return 1
    fi
    
    workflow_count=$(find "$WORKFLOWS_DIR" -name "*.json" 2>/dev/null | wc -l)
    print_status "Found $workflow_count workflow files to import"
    
    read -p "Continue with import? This will add/update workflows in n8n. (y/N): " confirm
    if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
        print_status "Import cancelled"
        return 0
    fi
    
    print_status "Running: n8n import:workflow --separate --input=$WORKFLOWS_DIR/"
    
    if n8n import:workflow --separate --input="$WORKFLOWS_DIR/"; then
        print_success "Workflows imported successfully from $WORKFLOWS_DIR/"
        return 0
    else
        print_error "Failed to import workflows"
        return 1
    fi
}

# Function to import credentials using n8n native command
import_credentials() {
    print_section "Importing Credentials (Git → n8n)"
    
    cred_file="$CREDENTIALS_DIR/credentials.json"
    
    if [[ ! -f "$cred_file" ]]; then
        print_error "No credentials file found at $cred_file"
        return 1
    fi
    
    print_warning "⚠️  This will import credentials to n8n"
    read -p "Continue? (y/N): " confirm
    if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
        print_status "Import cancelled"
        return 0
    fi
    
    print_status "Running: n8n import:credentials --input=$cred_file"
    
    if n8n import:credentials --input="$cred_file"; then
        print_success "Credentials imported successfully from $cred_file"
        return 0
    else
        print_error "Failed to import credentials"
        return 1
    fi
}

# Function to commit changes to Git
commit_changes() {
    print_section "Committing Changes to Git"
    
    check_git_repo || return 1
    
    # Check if there are changes
    if git diff --quiet && git diff --cached --quiet; then
        print_status "No changes to commit"
        return 0
    fi
    
    # Show status
    print_status "Current Git status:"
    git status --short
    
    echo ""
    read -p "Enter commit message (or press Enter for auto-generated): " commit_msg
    
    if [[ -z "$commit_msg" ]]; then
        commit_msg="Auto-sync: Update n8n workflows and credentials $(date '+%Y-%m-%d %H:%M:%S')"
    fi
    
    git add .
    git commit -m "$commit_msg"
    print_success "Changes committed with message: $commit_msg"
}

# Function to push to remote
push_to_remote() {
    print_section "Pushing to Remote Repository"
    
    check_git_repo || return 1
    
    # Check if remote exists
    if ! git remote get-url origin > /dev/null 2>&1; then
        print_error "No remote repository configured"
        print_status "Add a remote with: git remote add origin <your-repo-url>"
        return 1
    fi
    
    print_status "Pushing to origin..."
    if git push origin main 2>/dev/null || git push origin master 2>/dev/null; then
        print_success "Successfully pushed to remote repository"
    else
        print_error "Failed to push to remote repository"
        return 1
    fi
}

# Function to pull from remote
pull_from_remote() {
    print_section "Pulling from Remote Repository"
    
    check_git_repo || return 1
    
    # Check if remote exists
    if ! git remote get-url origin > /dev/null 2>&1; then
        print_error "No remote repository configured"
        return 1
    fi
    
    print_status "Pulling from origin..."
    if git pull origin main 2>/dev/null || git pull origin master 2>/dev/null; then
        print_success "Successfully pulled from remote repository"
    else
        print_error "Failed to pull from remote repository"
        return 1
    fi
}

# Function to show Git status
show_git_status() {
    print_section "Git Status"
    
    check_git_repo || return 1
    
    echo "Repository status:"
    git status
    
    echo ""
    echo "Recent commits:"
    git log --oneline -5
}

# Function to validate workflow files
validate_workflows() {
    print_section "Validating Workflow Files"
    
    if [[ ! -d "$WORKFLOWS_DIR" ]]; then
        print_warning "No workflows directory found"
        return 0
    fi
    
    json_files=($(find "$WORKFLOWS_DIR" -name "*.json" 2>/dev/null))
    
    if [[ ${#json_files[@]} -eq 0 ]]; then
        print_warning "No JSON files found in workflows directory"
        return 0
    fi
    
    valid_count=0
    invalid_count=0
    
    for file in "${json_files[@]}"; do
        filename=$(basename "$file")
        if python3 -m json.tool "$file" > /dev/null 2>&1; then
            echo -e "  ${GREEN}✅${NC} $filename"
            ((valid_count++))
        else
            echo -e "  ${RED}❌${NC} $filename"
            ((invalid_count++))
        fi
    done
    
    echo ""
    print_status "Validation complete: $valid_count valid, $invalid_count invalid files"
}

# Function to check n8n connection
check_n8n_status() {
    print_section "N8N Connection Status"
    
    # Try to get n8n version
    if n8n --version > /dev/null 2>&1; then
        n8n_version=$(n8n --version)
        print_success "N8N CLI available: $n8n_version"
    else
        print_error "N8N CLI not available or not working"
        return 1
    fi
    
    # Check if we can access local instance
    if curl -s http://localhost:5678/api/v1/health > /dev/null 2>&1; then
        print_success "Local N8N instance responding on http://localhost:5678"
    else
        print_warning "Local N8N instance not responding (may not be running)"
    fi
    
    # Check environment variables for cloud
    if [[ -n "$N8N_CLOUD_INSTANCE_URL" && -n "$N8N_API_KEY" ]]; then
        print_success "Cloud credentials configured"
        print_status "Cloud URL: $N8N_CLOUD_INSTANCE_URL"
    else
        print_warning "Cloud credentials not configured"
    fi
}

# Function for full export + commit + push
smart_export_sync() {
    print_section "Smart Export Sync (n8n → Git → Remote)"
    
    # Export everything
    print_status "Step 1: Exporting workflows..."
    export_workflows || return 1
    
    print_status "Step 2: Exporting credentials..."
    export_credentials || return 1
    
    # Commit changes
    print_status "Step 3: Committing changes..."
    commit_changes || return 1
    
    # Push to remote
    print_status "Step 4: Pushing to remote..."
    push_to_remote || return 1
    
    print_success "Smart export sync completed successfully!"
}

# Function for pull + import
smart_import_sync() {
    print_section "Smart Import Sync (Remote → Git → n8n)"
    
    # Pull from remote
    print_status "Step 1: Pulling from remote..."
    pull_from_remote || return 1
    
    # Import workflows
    print_status "Step 2: Importing workflows..."
    import_workflows || return 1
    
    # Import credentials
    print_status "Step 3: Importing credentials..."
    import_credentials || return 1
    
    print_success "Smart import sync completed successfully!"
}

# Main script execution
main() {
    while true; do
        show_menu
        read -p "Enter your choice (0-15): " choice
        
        case $choice in
            1) export_workflows ;;
            2) export_credentials ;;
            3) 
                export_workflows
                echo ""
                export_credentials
                ;;
            4) import_workflows ;;
            5) import_credentials ;;
            6) 
                import_workflows
                echo ""
                import_credentials
                ;;
            7) commit_changes ;;
            8) push_to_remote ;;
            9) pull_from_remote ;;
            10) show_git_status ;;
            11) check_git_repo ;;
            12) validate_workflows ;;
            13) check_n8n_status ;;
            14) smart_export_sync ;;
            15) smart_import_sync ;;
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
