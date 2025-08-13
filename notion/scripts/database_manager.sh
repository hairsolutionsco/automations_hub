#!/bin/bash

# Notion Database Management Script

echo "📊 Notion Database Management"
echo "============================"

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "❌ Python not found. Please install Python first."
    exit 1
fi

# Check if we're in the right directory
if [[ ! -f "../analyze_empty_properties.py" ]]; then
    echo "❌ Error: Please run this script from the notion/scripts directory"
    exit 1
fi

echo "🎯 Database Management Options:"
echo ""
echo "Analysis & Documentation:"
echo "1. Analyze empty properties across databases"
echo "2. Generate documentation for all databases"
echo "3. Generate database inventory"
echo ""
echo "Database Operations:"
echo "4. List all databases"
echo "5. Backup database structure"
echo "6. Validate database connections"
echo ""
echo "Maintenance:"
echo "7. Clean up empty properties"
echo "8. Archive old databases"
echo "9. Generate usage report"

read -p "Enter your choice (1-9): " choice

case $choice in
    1)
        echo "🔍 Analyzing empty properties..."
        cd ..
        python analyze_empty_properties.py
        ;;
    2)
        echo "📝 Generating documentation for all databases..."
        cd ..
        python generate_all_database_docs.py
        echo "✅ Documentation generated in databases/ directory"
        ;;
    3)
        echo "📋 Generating database inventory..."
        cd ..
        if [ -f "notion-databases-inventory.md" ]; then
            echo "Current inventory:"
            wc -l notion-databases-inventory.md
            echo "Last updated: $(stat -c %y notion-databases-inventory.md)"
        else
            echo "❌ Inventory file not found. Run generate_all_database_docs.py first."
        fi
        ;;
    4)
        echo "📊 Listing all databases..."
        echo "Available database documentation:"
        ls -la databases/*.md 2>/dev/null | head -20
        echo ""
        echo "Total databases documented: $(ls databases/*.md 2>/dev/null | wc -l)"
        ;;
    5)
        echo "💾 Backing up database structure..."
        DATE=$(date +%Y%m%d_%H%M%S)
        mkdir -p ../backups
        
        # Copy database documentation
        if [ -d "../databases" ]; then
            tar -czf "../backups/notion_databases_$DATE.tar.gz" -C .. databases/
            echo "✅ Database structure backed up: backups/notion_databases_$DATE.tar.gz"
        fi
        
        # Copy inventory
        if [ -f "../notion-databases-inventory.md" ]; then
            cp "../notion-databases-inventory.md" "../backups/inventory_$DATE.md"
            echo "✅ Inventory backed up: backups/inventory_$DATE.md"
        fi
        ;;
    6)
        echo "🔗 Validating database connections..."
        echo "Checking if documentation files exist..."
        
        TOTAL=0
        VALID=0
        
        for file in ../databases/*.md; do
            if [ -f "$file" ]; then
                TOTAL=$((TOTAL + 1))
                if grep -q "Database ID:" "$file"; then
                    VALID=$((VALID + 1))
                    echo "  ✅ $(basename "$file")"
                else
                    echo "  ⚠️  $(basename "$file") - Missing Database ID"
                fi
            fi
        done
        
        echo ""
        echo "📊 Summary: $VALID/$TOTAL databases have valid structure"
        ;;
    7)
        echo "🧹 Clean up empty properties analysis..."
        read -p "This will analyze and suggest cleanup actions. Continue? (y/N): " confirm
        
        if [[ $confirm == [yY] ]]; then
            cd ..
            echo "Running empty properties analysis..."
            python analyze_empty_properties.py > scripts/cleanup_suggestions.txt
            echo "✅ Cleanup suggestions saved to scripts/cleanup_suggestions.txt"
            echo "Review the file before taking any action."
        else
            echo "❌ Cleanup cancelled"
        fi
        ;;
    8)
        echo "📦 Archive old databases..."
        echo "This will create an archive of databases not modified recently."
        
        DATE=$(date +%Y%m%d_%H%M%S)
        mkdir -p "../archives/archive_$DATE"
        
        # Find files older than 90 days
        find ../databases -name "*.md" -mtime +90 -exec cp {} "../archives/archive_$DATE/" \;
        
        ARCHIVED=$(ls "../archives/archive_$DATE/" 2>/dev/null | wc -l)
        echo "✅ Archived $ARCHIVED old database documentation files"
        ;;
    9)
        echo "📈 Generating usage report..."
        
        echo "=== Notion Database Usage Report ===" > usage_report.txt
        echo "Generated: $(date)" >> usage_report.txt
        echo "" >> usage_report.txt
        
        echo "📊 Database Statistics:" >> usage_report.txt
        echo "Total databases: $(ls ../databases/*.md 2>/dev/null | wc -l)" >> usage_report.txt
        echo "Inventory file exists: $([ -f '../notion-databases-inventory.md' ] && echo 'Yes' || echo 'No')" >> usage_report.txt
        echo "" >> usage_report.txt
        
        echo "📁 Database Categories:" >> usage_report.txt
        for category in "business" "financial" "customer" "content" "tracking"; do
            count=$(grep -l "$category" ../databases/*.md 2>/dev/null | wc -l)
            echo "$category: $count databases" >> usage_report.txt
        done
        
        echo "" >> usage_report.txt
        echo "📅 Recent Activity:" >> usage_report.txt
        echo "Modified in last 7 days: $(find ../databases -name "*.md" -mtime -7 | wc -l)" >> usage_report.txt
        echo "Modified in last 30 days: $(find ../databases -name "*.md" -mtime -30 | wc -l)" >> usage_report.txt
        
        echo "✅ Usage report generated: usage_report.txt"
        cat usage_report.txt
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac
