#!/bin/bash

# Notion Blocks and Pages Management Script

echo "📄 Notion Blocks & Pages Management"
echo "=================================="

# Check if we're in the right directory
if [[ ! -d "../blocks" ]] && [[ ! -d "../pages" ]]; then
    echo "❌ Error: Please run this script from the notion/scripts directory"
    exit 1
fi

echo "🎯 Pages & Blocks Management:"
echo ""
echo "Content Management:"
echo "1. List all pages"
echo "2. List all blocks"
echo "3. Search content"
echo "4. Export pages structure"
echo ""
echo "Backup & Sync:"
echo "5. Backup all content"
echo "6. Validate content structure"
echo "7. Generate content inventory"
echo ""
echo "Maintenance:"
echo "8. Clean up temporary files"
echo "9. Organize content by type"
echo "10. Generate sitemap"

read -p "Enter your choice (1-10): " choice

case $choice in
    1)
        echo "📄 Listing all pages..."
        if [ -d "../pages" ]; then
            echo "Pages directory structure:"
            tree ../pages/ 2>/dev/null || find ../pages -type f -name "*.md" | sort
            echo ""
            echo "Total pages: $(find ../pages -name "*.md" 2>/dev/null | wc -l)"
        else
            echo "❌ No pages directory found"
        fi
        ;;
    2)
        echo "🧱 Listing all blocks..."
        if [ -d "../blocks" ]; then
            echo "Blocks directory structure:"
            tree ../blocks/ 2>/dev/null || find ../blocks -type f | sort
            echo ""
            echo "Total blocks: $(find ../blocks -type f 2>/dev/null | wc -l)"
        else
            echo "❌ No blocks directory found"
        fi
        ;;
    3)
        echo "🔍 Search content..."
        read -p "Enter search term: " search_term
        
        if [ -n "$search_term" ]; then
            echo "Searching in pages..."
            grep -r -l "$search_term" ../pages/ 2>/dev/null || echo "No matches in pages"
            
            echo ""
            echo "Searching in blocks..."
            grep -r -l "$search_term" ../blocks/ 2>/dev/null || echo "No matches in blocks"
            
            echo ""
            echo "Searching in databases..."
            grep -r -l "$search_term" ../databases/ 2>/dev/null || echo "No matches in databases"
        fi
        ;;
    4)
        echo "📊 Exporting pages structure..."
        
        echo "=== Notion Content Structure ===" > content_structure.txt
        echo "Generated: $(date)" >> content_structure.txt
        echo "" >> content_structure.txt
        
        if [ -d "../pages" ]; then
            echo "📄 PAGES:" >> content_structure.txt
            tree ../pages/ >> content_structure.txt 2>/dev/null || find ../pages -type f | sort >> content_structure.txt
            echo "" >> content_structure.txt
        fi
        
        if [ -d "../blocks" ]; then
            echo "🧱 BLOCKS:" >> content_structure.txt
            tree ../blocks/ >> content_structure.txt 2>/dev/null || find ../blocks -type f | sort >> content_structure.txt
            echo "" >> content_structure.txt
        fi
        
        if [ -d "../databases" ]; then
            echo "📊 DATABASES:" >> content_structure.txt
            ls -la ../databases/*.md >> content_structure.txt 2>/dev/null
        fi
        
        echo "✅ Structure exported to: content_structure.txt"
        ;;
    5)
        echo "💾 Backing up all content..."
        DATE=$(date +%Y%m%d_%H%M%S)
        mkdir -p ../backups
        
        # Create comprehensive backup
        tar -czf "../backups/notion_full_backup_$DATE.tar.gz" \
            ../pages ../blocks ../databases ../*.md ../*.py 2>/dev/null
        
        if [ $? -eq 0 ]; then
            echo "✅ Full backup created: backups/notion_full_backup_$DATE.tar.gz"
            ls -lh "../backups/notion_full_backup_$DATE.tar.gz"
        else
            echo "❌ Backup failed"
        fi
        ;;
    6)
        echo "✅ Validating content structure..."
        
        ISSUES=0
        
        echo "Checking pages structure..."
        if [ -d "../pages" ]; then
            # Check for markdown files
            MD_COUNT=$(find ../pages -name "*.md" | wc -l)
            echo "  📄 Found $MD_COUNT markdown files"
            
            # Check for empty files
            EMPTY_COUNT=$(find ../pages -name "*.md" -empty | wc -l)
            if [ $EMPTY_COUNT -gt 0 ]; then
                echo "  ⚠️  Found $EMPTY_COUNT empty files"
                ISSUES=$((ISSUES + 1))
            fi
        else
            echo "  ❌ Pages directory missing"
            ISSUES=$((ISSUES + 1))
        fi
        
        echo ""
        echo "Checking blocks structure..."
        if [ -d "../blocks" ]; then
            BLOCK_COUNT=$(find ../blocks -type f | wc -l)
            echo "  🧱 Found $BLOCK_COUNT block files"
        else
            echo "  ❌ Blocks directory missing"
            ISSUES=$((ISSUES + 1))
        fi
        
        echo ""
        echo "Checking database documentation..."
        if [ -d "../databases" ]; then
            DB_COUNT=$(find ../databases -name "*.md" | wc -l)
            echo "  📊 Found $DB_COUNT database documentation files"
        else
            echo "  ❌ Databases directory missing"
            ISSUES=$((ISSUES + 1))
        fi
        
        echo ""
        if [ $ISSUES -eq 0 ]; then
            echo "✅ Content structure is valid"
        else
            echo "⚠️  Found $ISSUES issues"
        fi
        ;;
    7)
        echo "📋 Generating content inventory..."
        
        echo "=== Notion Content Inventory ===" > content_inventory.md
        echo "Generated: $(date)" >> content_inventory.md
        echo "" >> content_inventory.md
        
        # Pages inventory
        if [ -d "../pages" ]; then
            echo "## 📄 Pages" >> content_inventory.md
            echo "" >> content_inventory.md
            find ../pages -name "*.md" | while read file; do
                filename=$(basename "$file")
                size=$(stat -c%s "$file" 2>/dev/null || echo "0")
                modified=$(stat -c%y "$file" 2>/dev/null || echo "unknown")
                echo "- **$filename** (${size} bytes, modified: $modified)" >> content_inventory.md
            done
            echo "" >> content_inventory.md
        fi
        
        # Blocks inventory
        if [ -d "../blocks" ]; then
            echo "## 🧱 Blocks" >> content_inventory.md
            echo "" >> content_inventory.md
            find ../blocks -type f | while read file; do
                filename=$(basename "$file")
                echo "- $filename" >> content_inventory.md
            done
            echo "" >> content_inventory.md
        fi
        
        # Database inventory
        if [ -d "../databases" ]; then
            echo "## 📊 Databases" >> content_inventory.md
            echo "" >> content_inventory.md
            find ../databases -name "*.md" | while read file; do
                filename=$(basename "$file" .md)
                echo "- [$filename](databases/$filename.md)" >> content_inventory.md
            done
        fi
        
        echo "✅ Inventory generated: content_inventory.md"
        ;;
    8)
        echo "🧹 Cleaning up temporary files..."
        
        # Remove common temporary files
        find .. -name "*.tmp" -delete 2>/dev/null
        find .. -name "*.bak" -delete 2>/dev/null
        find .. -name ".DS_Store" -delete 2>/dev/null
        find .. -name "Thumbs.db" -delete 2>/dev/null
        
        # Remove empty directories
        find .. -type d -empty -delete 2>/dev/null
        
        echo "✅ Cleanup completed"
        ;;
    9)
        echo "📁 Organizing content by type..."
        
        # Create organized structure
        mkdir -p ../organized/{business,financial,customer,content,technical}
        
        # Organize database docs by category
        if [ -d "../databases" ]; then
            for file in ../databases/*.md; do
                if [ -f "$file" ]; then
                    filename=$(basename "$file")
                    case $filename in
                        *business*|*project*|*company*)
                            cp "$file" ../organized/business/
                            ;;
                        *financial*|*payment*|*expense*|*income*|*budget*)
                            cp "$file" ../organized/financial/
                            ;;
                        *customer*|*contact*|*deal*|*order*)
                            cp "$file" ../organized/customer/
                            ;;
                        *content*|*email*|*template*)
                            cp "$file" ../organized/content/
                            ;;
                        *)
                            cp "$file" ../organized/technical/
                            ;;
                    esac
                fi
            done
        fi
        
        echo "✅ Content organized in ../organized/ directory"
        ;;
    10)
        echo "🗺️ Generating sitemap..."
        
        echo "# Notion Workspace Sitemap" > sitemap.md
        echo "Generated: $(date)" >> sitemap.md
        echo "" >> sitemap.md
        
        echo "## 📊 Databases" >> sitemap.md
        if [ -d "../databases" ]; then
            for file in ../databases/*.md; do
                if [ -f "$file" ]; then
                    name=$(basename "$file" .md)
                    echo "- [$name](databases/$name.md)" >> sitemap.md
                fi
            done
        fi
        echo "" >> sitemap.md
        
        echo "## 📄 Pages" >> sitemap.md
        if [ -d "../pages" ]; then
            find ../pages -name "*.md" | sort | while read file; do
                name=$(basename "$file")
                path=${file#../}
                echo "- [$name]($path)" >> sitemap.md
            done
        fi
        echo "" >> sitemap.md
        
        echo "## 🧱 Blocks" >> sitemap.md
        if [ -d "../blocks" ]; then
            find ../blocks -type f | sort | while read file; do
                name=$(basename "$file")
                path=${file#../}
                echo "- [$name]($path)" >> sitemap.md
            done
        fi
        
        echo "✅ Sitemap generated: sitemap.md"
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac
