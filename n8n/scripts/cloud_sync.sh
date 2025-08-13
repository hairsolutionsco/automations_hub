#!/bin/bash

# N8N Cloud Sync Script

echo "☁️ N8N Cloud Synchronization"
echo "============================"

# Check environment variables
if [ -z "$N8N_CLOUD_INSTANCE_URL" ] || [ -z "$N8N_USER_EMAIL" ] || [ -z "$N8N_API_KEY" ]; then
    echo "❌ Error: Cloud credentials not set"
    echo "Please set the following environment variables:"
    echo "  N8N_CLOUD_INSTANCE_URL"
    echo "  N8N_USER_EMAIL"
    echo "  N8N_API_KEY"
    exit 1
fi

echo "🌐 Cloud Instance: $N8N_CLOUD_INSTANCE_URL"
echo "👤 User: $N8N_USER_EMAIL"
echo ""

# Create workflows directory if it doesn't exist
mkdir -p ../workflows

echo "🎯 Sync Options:"
echo "1. Export all workflows from cloud (Download)"
echo "2. Import all workflows to cloud (Upload)"
echo "3. Backup current cloud workflows"
echo "4. Compare local vs cloud"
echo "5. Two-way sync (advanced)"

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo "⬇️ Exporting workflows from cloud..."
        cd ..
        n8n export:workflow --all --output workflows --separate \
          --baseUrl "$N8N_CLOUD_INSTANCE_URL" \
          --userEmail "$N8N_USER_EMAIL" \
          --password "$N8N_API_KEY"
        
        if [ $? -eq 0 ]; then
            echo "✅ Export completed successfully"
            echo "📊 Workflows exported:"
            ls -la workflows/*.json | wc -l
        else
            echo "❌ Export failed"
        fi
        ;;
    2)
        echo "⬆️ Importing workflows to cloud..."
        if [ ! -d "../workflows" ] || [ -z "$(ls -A ../workflows/*.json 2>/dev/null)" ]; then
            echo "❌ No local workflows found to import"
            exit 1
        fi
        
        cd ..
        n8n import:workflow --input workflows --separate \
          --baseUrl "$N8N_CLOUD_INSTANCE_URL" \
          --userEmail "$N8N_USER_EMAIL" \
          --password "$N8N_API_KEY"
        
        if [ $? -eq 0 ]; then
            echo "✅ Import completed successfully"
        else
            echo "❌ Import failed"
        fi
        ;;
    3)
        echo "💾 Backing up cloud workflows..."
        DATE=$(date +%Y%m%d_%H%M%S)
        mkdir -p ../backups/cloud_backups
        
        cd ..
        n8n export:workflow --all --output "backups/cloud_backups/cloud_$DATE" --separate \
          --baseUrl "$N8N_CLOUD_INSTANCE_URL" \
          --userEmail "$N8N_USER_EMAIL" \
          --password "$N8N_API_KEY"
        
        if [ $? -eq 0 ]; then
            echo "✅ Cloud backup created: backups/cloud_backups/cloud_$DATE/"
        else
            echo "❌ Backup failed"
        fi
        ;;
    4)
        echo "🔍 Comparing local vs cloud..."
        
        # Create temporary directory for cloud export
        TEMP_DIR="../temp_cloud_export"
        mkdir -p "$TEMP_DIR"
        
        cd ..
        n8n export:workflow --all --output temp_cloud_export --separate \
          --baseUrl "$N8N_CLOUD_INSTANCE_URL" \
          --userEmail "$N8N_USER_EMAIL" \
          --password "$N8N_API_KEY"
        
        echo ""
        echo "📊 Comparison Results:"
        echo "Local workflows:"
        ls workflows/*.json 2>/dev/null | wc -l || echo "0"
        echo "Cloud workflows:"
        ls temp_cloud_export/*.json 2>/dev/null | wc -l || echo "0"
        
        echo ""
        echo "🔍 Detailed comparison:"
        if [ -d "workflows" ] && [ -d "temp_cloud_export" ]; then
            for local_file in workflows/*.json; do
                filename=$(basename "$local_file")
                if [ -f "temp_cloud_export/$filename" ]; then
                    if diff -q "$local_file" "temp_cloud_export/$filename" > /dev/null; then
                        echo "  ✅ $filename - Identical"
                    else
                        echo "  ⚠️  $filename - Different"
                    fi
                else
                    echo "  📤 $filename - Local only"
                fi
            done
            
            for cloud_file in temp_cloud_export/*.json; do
                filename=$(basename "$cloud_file")
                if [ ! -f "workflows/$filename" ]; then
                    echo "  📥 $filename - Cloud only"
                fi
            done
        fi
        
        # Clean up
        rm -rf "$TEMP_DIR"
        ;;
    5)
        echo "🔄 Two-way sync (advanced)..."
        echo "⚠️  This will merge local and cloud workflows"
        read -p "Are you sure? (y/N): " confirm
        
        if [[ $confirm == [yY] ]]; then
            # First backup current state
            DATE=$(date +%Y%m%d_%H%M%S)
            mkdir -p "../backups/sync_$DATE"
            
            echo "📋 Creating backup before sync..."
            cp -r ../workflows "../backups/sync_$DATE/local_before" 2>/dev/null || echo "No local workflows to backup"
            
            # Export cloud to backup
            cd ..
            n8n export:workflow --all --output "backups/sync_$DATE/cloud_before" --separate \
              --baseUrl "$N8N_CLOUD_INSTANCE_URL" \
              --userEmail "$N8N_USER_EMAIL" \
              --password "$N8N_API_KEY"
            
            # Export cloud to local (this will merge)
            n8n export:workflow --all --output workflows --separate \
              --baseUrl "$N8N_CLOUD_INSTANCE_URL" \
              --userEmail "$N8N_USER_EMAIL" \
              --password "$N8N_API_KEY"
            
            # Import everything back to cloud
            n8n import:workflow --input workflows --separate \
              --baseUrl "$N8N_CLOUD_INSTANCE_URL" \
              --userEmail "$N8N_USER_EMAIL" \
              --password "$N8N_API_KEY"
            
            echo "✅ Two-way sync completed"
            echo "💾 Backup available at: backups/sync_$DATE/"
        else
            echo "❌ Sync cancelled"
        fi
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac
