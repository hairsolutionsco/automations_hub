#!/bin/bash

# N8N Management Script

echo "🔄 N8N Workflow Management"
echo "========================="

# Check if we're in the right directory
if [[ ! -f "../n8n_package.json" ]]; then
    echo "❌ Error: Please run this script from the n8n/scripts directory"
    exit 1
fi

# Load environment variables
if [ -f ../.env ]; then
    source ../.env
fi

echo "🎯 What would you like to do?"
echo ""
echo "Local Development:"
echo "1. Start N8N locally"
echo "2. Start N8N in development mode"
echo "3. Stop N8N"
echo ""
echo "Cloud Management:"
echo "4. Export workflows from cloud"
echo "5. Import workflows to cloud"
echo "6. Sync workflows (export from cloud)"
echo ""
echo "Workflow Management:"
echo "7. List local workflows"
echo "8. Validate workflows"
echo "9. Backup workflows"

read -p "Enter your choice (1-9): " choice

case $choice in
    1)
        echo "🚀 Starting N8N locally..."
        cd ..
        npm run start
        ;;
    2)
        echo "🛠️ Starting N8N in development mode..."
        cd ..
        npm run dev
        ;;
    3)
        echo "🛑 Stopping N8N..."
        pkill -f n8n
        echo "✅ N8N stopped"
        ;;
    4)
        echo "☁️ Exporting workflows from cloud..."
        if [ -z "$N8N_CLOUD_INSTANCE_URL" ] || [ -z "$N8N_API_KEY" ]; then
            echo "❌ Cloud credentials not set. Please set N8N_CLOUD_INSTANCE_URL and N8N_API_KEY"
            exit 1
        fi
        cd ..
        npm run cloud:export
        ;;
    5)
        echo "☁️ Importing workflows to cloud..."
        if [ -z "$N8N_CLOUD_INSTANCE_URL" ] || [ -z "$N8N_API_KEY" ]; then
            echo "❌ Cloud credentials not set. Please set N8N_CLOUD_INSTANCE_URL and N8N_API_KEY"
            exit 1
        fi
        cd ..
        npm run cloud:import
        ;;
    6)
        echo "🔄 Syncing workflows..."
        cd ..
        npm run workflows:sync
        ;;
    7)
        echo "📋 Local workflows:"
        ls -la ../workflows/*.json 2>/dev/null || echo "No workflows found in ../workflows/"
        ;;
    8)
        echo "✅ Validating workflows..."
        for file in ../workflows/*.json; do
            if [ -f "$file" ]; then
                echo "Checking: $(basename "$file")"
                python -m json.tool "$file" > /dev/null && echo "  ✅ Valid JSON" || echo "  ❌ Invalid JSON"
            fi
        done
        ;;
    9)
        echo "💾 Backing up workflows..."
        DATE=$(date +%Y%m%d_%H%M%S)
        mkdir -p ../backups
        
        if [ -d "../workflows" ]; then
            tar -czf "../backups/workflows_backup_$DATE.tar.gz" -C .. workflows/
            echo "✅ Backup created: ../backups/workflows_backup_$DATE.tar.gz"
        else
            echo "❌ No workflows directory found"
        fi
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac
