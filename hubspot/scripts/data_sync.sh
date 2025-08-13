#!/bin/bash

# HubSpot Data Sync Script

echo "🔄 HubSpot Data Synchronization"
echo "==============================="

# Check environment variables
if [ -z "$HUBSPOT_ACCESS_TOKEN" ]; then
    echo "⚠️  Warning: HUBSPOT_ACCESS_TOKEN not set"
    echo "Some operations may not work without authentication"
fi

echo "🎯 Sync Operations:"
echo ""
echo "Export from HubSpot:"
echo "1. Export all contacts"
echo "2. Export all companies"
echo "3. Export all deals"
echo "4. Export all tickets"
echo "5. Export custom objects"
echo ""
echo "Import to External Systems:"
echo "6. Sync contacts to Notion"
echo "7. Sync companies to Notion"
echo "8. Sync deals to Notion"
echo "9. Sync customers to Shopify"
echo ""
echo "Bidirectional Sync:"
echo "10. Full HubSpot ↔ Notion sync"
echo "11. Full HubSpot ↔ Shopify sync"
echo "12. Automated sync setup"

read -p "Enter your choice (1-12): " choice

DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p ../exports "../sync_logs"

case $choice in
    1)
        echo "👥 Exporting contacts from HubSpot..."
        
        # Create export file
        EXPORT_FILE="../exports/contacts_$DATE.json"
        
        if [ -n "$HUBSPOT_ACCESS_TOKEN" ]; then
            echo "📡 Calling HubSpot Contacts API..."
            curl -s "https://api.hubapi.com/crm/v3/objects/contacts?limit=100" \
                -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" \
                -H "Content-Type: application/json" > "$EXPORT_FILE"
            
            if [ $? -eq 0 ]; then
                echo "✅ Contacts exported to: $EXPORT_FILE"
                # Count contacts
                CONTACT_COUNT=$(grep -o '"id":' "$EXPORT_FILE" | wc -l)
                echo "📊 Exported $CONTACT_COUNT contacts"
            else
                echo "❌ Export failed"
            fi
        else
            echo "❌ HUBSPOT_ACCESS_TOKEN required for API access"
        fi
        ;;
    2)
        echo "🏢 Exporting companies from HubSpot..."
        
        EXPORT_FILE="../exports/companies_$DATE.json"
        
        if [ -n "$HUBSPOT_ACCESS_TOKEN" ]; then
            echo "📡 Calling HubSpot Companies API..."
            curl -s "https://api.hubapi.com/crm/v3/objects/companies?limit=100" \
                -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" \
                -H "Content-Type: application/json" > "$EXPORT_FILE"
            
            if [ $? -eq 0 ]; then
                echo "✅ Companies exported to: $EXPORT_FILE"
                COMPANY_COUNT=$(grep -o '"id":' "$EXPORT_FILE" | wc -l)
                echo "📊 Exported $COMPANY_COUNT companies"
            else
                echo "❌ Export failed"
            fi
        else
            echo "❌ HUBSPOT_ACCESS_TOKEN required for API access"
        fi
        ;;
    3)
        echo "💼 Exporting deals from HubSpot..."
        
        EXPORT_FILE="../exports/deals_$DATE.json"
        
        if [ -n "$HUBSPOT_ACCESS_TOKEN" ]; then
            echo "📡 Calling HubSpot Deals API..."
            curl -s "https://api.hubapi.com/crm/v3/objects/deals?limit=100" \
                -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" \
                -H "Content-Type: application/json" > "$EXPORT_FILE"
            
            if [ $? -eq 0 ]; then
                echo "✅ Deals exported to: $EXPORT_FILE"
                DEAL_COUNT=$(grep -o '"id":' "$EXPORT_FILE" | wc -l)
                echo "📊 Exported $DEAL_COUNT deals"
            else
                echo "❌ Export failed"
            fi
        else
            echo "❌ HUBSPOT_ACCESS_TOKEN required for API access"
        fi
        ;;
    4)
        echo "🎫 Exporting tickets from HubSpot..."
        
        EXPORT_FILE="../exports/tickets_$DATE.json"
        
        if [ -n "$HUBSPOT_ACCESS_TOKEN" ]; then
            echo "📡 Calling HubSpot Tickets API..."
            curl -s "https://api.hubapi.com/crm/v3/objects/tickets?limit=100" \
                -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" \
                -H "Content-Type: application/json" > "$EXPORT_FILE"
            
            if [ $? -eq 0 ]; then
                echo "✅ Tickets exported to: $EXPORT_FILE"
                TICKET_COUNT=$(grep -o '"id":' "$EXPORT_FILE" | wc -l)
                echo "📊 Exported $TICKET_COUNT tickets"
            else
                echo "❌ Export failed"
            fi
        else
            echo "❌ HUBSPOT_ACCESS_TOKEN required for API access"
        fi
        ;;
    5)
        echo "🔧 Exporting custom objects..."
        echo "⚠️  Custom object export requires specific object type IDs"
        echo "This would enumerate and export all custom objects"
        echo "Implementation depends on your HubSpot configuration"
        ;;
    6)
        echo "📊 Syncing contacts to Notion..."
        
        # Check if latest contacts export exists
        LATEST_CONTACTS=$(ls -t ../exports/contacts_*.json 2>/dev/null | head -1)
        
        if [ -f "$LATEST_CONTACTS" ]; then
            echo "📁 Using contacts file: $LATEST_CONTACTS"
            
            # Log sync operation
            echo "$(date): Starting contacts sync to Notion" >> "../sync_logs/notion_sync_$DATE.log"
            
            # This would use the Notion API to create/update records
            echo "🔄 Processing contacts for Notion format..."
            echo "📝 Would create entries in Notion contacts database"
            echo "⚠️  Implement Notion API integration here"
            
            echo "$(date): Contacts sync completed" >> "../sync_logs/notion_sync_$DATE.log"
            echo "✅ Sync logged to: sync_logs/notion_sync_$DATE.log"
        else
            echo "❌ No contacts export found. Run option 1 first."
        fi
        ;;
    7)
        echo "📊 Syncing companies to Notion..."
        
        LATEST_COMPANIES=$(ls -t ../exports/companies_*.json 2>/dev/null | head -1)
        
        if [ -f "$LATEST_COMPANIES" ]; then
            echo "📁 Using companies file: $LATEST_COMPANIES"
            echo "🔄 Processing companies for Notion format..."
            echo "📝 Would create entries in Notion companies database"
            echo "⚠️  Implement Notion API integration here"
            echo "✅ Companies sync would be completed"
        else
            echo "❌ No companies export found. Run option 2 first."
        fi
        ;;
    8)
        echo "📊 Syncing deals to Notion..."
        
        LATEST_DEALS=$(ls -t ../exports/deals_*.json 2>/dev/null | head -1)
        
        if [ -f "$LATEST_DEALS" ]; then
            echo "📁 Using deals file: $LATEST_DEALS"
            echo "🔄 Processing deals for Notion format..."
            echo "📝 Would create entries in Notion deals database"
            echo "⚠️  Implement Notion API integration here"
            echo "✅ Deals sync would be completed"
        else
            echo "❌ No deals export found. Run option 3 first."
        fi
        ;;
    9)
        echo "🛍️ Syncing customers to Shopify..."
        
        LATEST_CONTACTS=$(ls -t ../exports/contacts_*.json 2>/dev/null | head -1)
        
        if [ -f "$LATEST_CONTACTS" ]; then
            echo "📁 Using contacts file: $LATEST_CONTACTS"
            echo "🔄 Converting HubSpot contacts to Shopify customers..."
            echo "📝 Would create customer records in Shopify"
            echo "⚠️  Implement Shopify API integration here"
            echo "✅ Customer sync would be completed"
        else
            echo "❌ No contacts export found. Run option 1 first."
        fi
        ;;
    10)
        echo "🔄 Full HubSpot ↔ Notion bidirectional sync..."
        
        echo "📤 Phase 1: Export from HubSpot..."
        echo "  - Exporting contacts..."
        echo "  - Exporting companies..."
        echo "  - Exporting deals..."
        
        echo "📥 Phase 2: Import to Notion..."
        echo "  - Creating/updating Notion contacts database..."
        echo "  - Creating/updating Notion companies database..."
        echo "  - Creating/updating Notion deals database..."
        
        echo "📤 Phase 3: Export from Notion..."
        echo "  - Reading Notion database updates..."
        
        echo "📥 Phase 4: Import to HubSpot..."
        echo "  - Updating HubSpot records..."
        
        # Create sync report
        SYNC_REPORT="../sync_logs/full_notion_sync_$DATE.txt"
        echo "=== Full HubSpot ↔ Notion Sync Report ===" > "$SYNC_REPORT"
        echo "Date: $(date)" >> "$SYNC_REPORT"
        echo "Status: Would be implemented" >> "$SYNC_REPORT"
        echo "⚠️  Implement full bidirectional sync logic here"
        
        echo "✅ Full sync would be completed"
        echo "📋 Report: $SYNC_REPORT"
        ;;
    11)
        echo "🔄 Full HubSpot ↔ Shopify bidirectional sync..."
        
        echo "📤 Phase 1: Export customers from Shopify..."
        echo "📥 Phase 2: Import to HubSpot as contacts..."
        echo "📤 Phase 3: Export orders from Shopify..."
        echo "📥 Phase 4: Import to HubSpot as deals..."
        echo "📤 Phase 5: Export deals from HubSpot..."
        echo "📥 Phase 6: Update Shopify customer data..."
        
        SYNC_REPORT="../sync_logs/full_shopify_sync_$DATE.txt"
        echo "=== Full HubSpot ↔ Shopify Sync Report ===" > "$SYNC_REPORT"
        echo "Date: $(date)" >> "$SYNC_REPORT"
        echo "Status: Would be implemented" >> "$SYNC_REPORT"
        echo "⚠️  Implement full bidirectional sync logic here"
        
        echo "✅ Full sync would be completed"
        echo "📋 Report: $SYNC_REPORT"
        ;;
    12)
        echo "⚙️ Setting up automated sync..."
        
        # Create cron job template
        CRON_FILE="automated_sync_cron.txt"
        echo "# HubSpot Automated Sync Cron Jobs" > "$CRON_FILE"
        echo "# Add these to your crontab with: crontab $CRON_FILE" >> "$CRON_FILE"
        echo "" >> "$CRON_FILE"
        echo "# Daily export at 2 AM" >> "$CRON_FILE"
        echo "0 2 * * * cd $(pwd) && ./data_sync.sh 1 >> ../sync_logs/auto_contacts.log 2>&1" >> "$CRON_FILE"
        echo "5 2 * * * cd $(pwd) && ./data_sync.sh 2 >> ../sync_logs/auto_companies.log 2>&1" >> "$CRON_FILE"
        echo "10 2 * * * cd $(pwd) && ./data_sync.sh 3 >> ../sync_logs/auto_deals.log 2>&1" >> "$CRON_FILE"
        echo "" >> "$CRON_FILE"
        echo "# Weekly full sync on Sundays at 3 AM" >> "$CRON_FILE"
        echo "0 3 * * 0 cd $(pwd) && ./data_sync.sh 10 >> ../sync_logs/auto_full_sync.log 2>&1" >> "$CRON_FILE"
        
        echo "✅ Automated sync template created: $CRON_FILE"
        echo "📋 To enable:"
        echo "   1. Review the cron job schedule"
        echo "   2. Add to crontab: crontab $CRON_FILE"
        echo "   3. Monitor logs in sync_logs/ directory"
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac
