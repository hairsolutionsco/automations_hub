#!/usr/bin/env python3
"""
Analyze all Notion databases to identify empty properties (columns with no data).
This script will examine actual page data to determine which properties are unused.
"""

import asyncio
import sys
import os
import httpx
from datetime import datetime
import json
from collections import defaultdict

# Add the current directory to Python path
sys.path.append('.')

async def get_database_pages(client, database_id, page_size=100):
    """Fetch pages from a database to analyze property usage."""
    api_key = os.getenv('NOTION_API_KEY')
    
    all_pages = []
    has_more = True
    start_cursor = None
    
    while has_more:
        url = f'https://api.notion.com/v1/databases/{database_id}/query'
        payload = {
            'page_size': page_size
        }
        
        if start_cursor:
            payload['start_cursor'] = start_cursor
            
        response = await client.post(
            url,
            headers={
                'Authorization': f'Bearer {api_key}',
                'Notion-Version': '2022-06-28',
                'Content-Type': 'application/json'
            },
            json=payload
        )
        
        if response.status_code == 200:
            data = response.json()
            all_pages.extend(data.get('results', []))
            has_more = data.get('has_more', False)
            start_cursor = data.get('next_cursor')
        else:
            print(f'Error fetching pages from database {database_id}: {response.status_code} {response.text}')
            break
            
        # Add small delay to respect API limits
        await asyncio.sleep(0.1)
    
    return all_pages

async def get_database_properties(client, database_id):
    """Fetch database properties from Notion API."""
    api_key = os.getenv('NOTION_API_KEY')
    
    response = await client.get(
        f'https://api.notion.com/v1/databases/{database_id}',
        headers={
            'Authorization': f'Bearer {api_key}',
            'Notion-Version': '2022-06-28'
        }
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Error fetching database {database_id}: {response.status_code} {response.text}')
        return None

def is_property_empty(property_value, property_type):
    """Check if a property value is empty based on its type."""
    if not property_value:
        return True
        
    # Handle different property types
    if property_type == 'title':
        title_content = property_value.get('title', [])
        return not title_content or all(not item.get('plain_text', '').strip() for item in title_content)
    
    elif property_type == 'rich_text':
        rich_text_content = property_value.get('rich_text', [])
        return not rich_text_content or all(not item.get('plain_text', '').strip() for item in rich_text_content)
    
    elif property_type == 'number':
        return property_value.get('number') is None
    
    elif property_type == 'select':
        return property_value.get('select') is None
    
    elif property_type == 'multi_select':
        multi_select_content = property_value.get('multi_select', [])
        return not multi_select_content
    
    elif property_type == 'date':
        return property_value.get('date') is None
    
    elif property_type == 'checkbox':
        # Checkbox is never really "empty" as it's always true/false, but we can check if it's false
        return not property_value.get('checkbox', False)
    
    elif property_type == 'email':
        email_content = property_value.get('email', '')
        return not email_content or not str(email_content).strip()
    
    elif property_type == 'phone_number':
        phone_content = property_value.get('phone_number', '')
        return not phone_content or not str(phone_content).strip()
    
    elif property_type == 'url':
        url_content = property_value.get('url', '')
        return not url_content or not str(url_content).strip()
    
    elif property_type == 'relation':
        relation_content = property_value.get('relation', [])
        return not relation_content
    
    elif property_type == 'people':
        people_content = property_value.get('people', [])
        return not people_content
    
    elif property_type == 'files':
        files_content = property_value.get('files', [])
        return not files_content
    
    elif property_type == 'formula':
        # Formula results can be various types
        formula_result = property_value.get('formula', {})
        if not formula_result:
            return True
        
        formula_type = formula_result.get('type')
        if formula_type == 'string':
            result_value = formula_result.get('string', '')
            return not result_value or not str(result_value).strip()
        elif formula_type == 'number':
            return formula_result.get('number') is None
        elif formula_type == 'boolean':
            return formula_result.get('boolean') is None
        elif formula_type == 'date':
            return formula_result.get('date') is None
        else:
            return True
    
    elif property_type == 'rollup':
        rollup_result = property_value.get('rollup', {})
        if not rollup_result:
            return True
            
        rollup_type = rollup_result.get('type')
        if rollup_type == 'number':
            return rollup_result.get('number') is None
        elif rollup_type == 'array':
            return not rollup_result.get('array', [])
        else:
            return True
    
    elif property_type in ['created_time', 'last_edited_time']:
        # These are automatically populated, so never really empty
        return False
    
    elif property_type in ['created_by', 'last_edited_by']:
        # These are automatically populated, so never really empty
        return False
    
    elif property_type == 'status':
        return property_value.get('status') is None
    
    else:
        # Unknown property type, consider empty if no content
        return not property_value
    
def analyze_property_usage(pages, database_properties):
    """Analyze which properties are empty across all pages."""
    property_usage = {}
    
    # Initialize counters for all properties
    for prop_name, prop_data in database_properties.items():
        property_usage[prop_name] = {
            'type': prop_data.get('type', 'unknown'),
            'total_pages': 0,
            'empty_count': 0,
            'filled_count': 0
        }
    
    # Analyze each page
    for page in pages:
        page_properties = page.get('properties', {})
        
        for prop_name, prop_data in database_properties.items():
            property_usage[prop_name]['total_pages'] += 1
            
            if prop_name in page_properties:
                prop_value = page_properties[prop_name]
                prop_type = prop_data.get('type', 'unknown')
                
                if is_property_empty(prop_value, prop_type):
                    property_usage[prop_name]['empty_count'] += 1
                else:
                    property_usage[prop_name]['filled_count'] += 1
            else:
                # Property not present in page = empty
                property_usage[prop_name]['empty_count'] += 1
    
    return property_usage

def identify_empty_properties(property_usage, threshold=0.95):
    """Identify properties that are empty in most/all pages."""
    empty_properties = []
    mostly_empty_properties = []
    
    for prop_name, usage_data in property_usage.items():
        total_pages = usage_data['total_pages']
        empty_count = usage_data['empty_count']
        
        if total_pages == 0:
            continue
            
        empty_percentage = empty_count / total_pages
        
        if empty_percentage == 1.0:  # 100% empty
            empty_properties.append({
                'name': prop_name,
                'type': usage_data['type'],
                'empty_percentage': empty_percentage,
                'total_pages': total_pages
            })
        elif empty_percentage >= threshold:  # Mostly empty (95%+ by default)
            mostly_empty_properties.append({
                'name': prop_name,
                'type': usage_data['type'],
                'empty_percentage': empty_percentage,
                'total_pages': total_pages,
                'filled_count': usage_data['filled_count']
            })
    
    return empty_properties, mostly_empty_properties

async def analyze_database(client, db_name, db_id):
    """Analyze a single database for empty properties."""
    print(f"🔍 Analyzing: {db_name}")
    
    try:
        # Get database schema
        database_data = await get_database_properties(client, db_id)
        if not database_data:
            return None, None, None
        
        database_properties = database_data.get('properties', {})
        
        # Get all pages from the database
        pages = await get_database_pages(client, db_id)
        
        print(f"   📄 Found {len(pages)} pages with {len(database_properties)} properties")
        
        # Analyze property usage
        property_usage = analyze_property_usage(pages, database_properties)
        
        # Identify empty properties
        empty_props, mostly_empty_props = identify_empty_properties(property_usage)
        
        print(f"   ❌ Completely empty: {len(empty_props)}")
        print(f"   ⚠️  Mostly empty (95%+): {len(mostly_empty_props)}")
        
        return empty_props, mostly_empty_props, len(pages)
        
    except Exception as e:
        print(f"   ❌ Error analyzing {db_name}: {str(e)}")
        return None, None, None

def update_markdown_file(db_name, empty_props, mostly_empty_props, total_pages):
    """Update the existing markdown file to include empty properties section."""
    # Create safe filename - handle special characters and parentheses
    safe_filename = db_name.lower().replace(" ", "_").replace("&", "and").replace("/", "_").replace(":", "").replace("⏰", "").replace("(", "").replace(")", "")
    filepath = f"/workspaces/automations_hub/notion/databases/{safe_filename}.md"
    
    # Check for alternate filename patterns
    if not os.path.exists(filepath):
        # Try with parentheses in filename
        alt_filename = db_name.lower().replace(" ", "_").replace("&", "and").replace("/", "_").replace(":", "").replace("⏰", "")
        alt_filepath = f"/workspaces/automations_hub/notion/databases/{alt_filename}.md"
        if os.path.exists(alt_filepath):
            filepath = alt_filepath
        else:
            print(f"   ⚠️ File not found: {filepath} or {alt_filepath}")
            return False
    
    try:
        # Read existing content
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Prepare empty properties section
        empty_section = ""
        
        if empty_props or mostly_empty_props:
            empty_section += "## 🚫 Empty & Unused Properties\n\n"
            empty_section += f"*Analysis based on {total_pages} pages*\n\n"
            
            if empty_props:
                empty_section += f"### Completely Empty Properties ({len(empty_props)})\n"
                empty_section += "*These properties have no data in any page:*\n\n"
                for prop in sorted(empty_props, key=lambda x: x['name']):
                    empty_section += f"- `{prop['name']}` ({prop['type']})\n"
                empty_section += "\n"
            
            if mostly_empty_props:
                empty_section += f"### Mostly Empty Properties ({len(mostly_empty_props)})\n"
                empty_section += "*These properties have data in less than 5% of pages:*\n\n"
                for prop in sorted(mostly_empty_props, key=lambda x: x['empty_percentage'], reverse=True):
                    filled_count = prop['filled_count']
                    empty_pct = prop['empty_percentage'] * 100
                    empty_section += f"- `{prop['name']}` ({prop['type']}) - {empty_pct:.1f}% empty, only {filled_count} pages with data\n"
                empty_section += "\n"
        else:
            empty_section += "## ✅ Property Usage Analysis\n\n"
            empty_section += f"*Analysis based on {total_pages} pages*\n\n"
            empty_section += "**Great news!** All properties in this database have data. No completely empty or mostly unused properties were found.\n\n"
        
        # Find insertion point (before "Related Databases" or final separator)
        if "## Related Databases" in content:
            insert_point = content.find("## Related Databases")
        elif content.endswith("---\n\n*Documentation generated on"):
            insert_point = content.rfind("---\n\n*Documentation generated on")
        else:
            # Append at the end before the last line
            lines = content.split('\n')
            if lines and lines[-1].startswith('*Documentation generated on'):
                insert_point = len(content) - len(lines[-1]) - 1
            else:
                insert_point = len(content)
        
        # Insert the empty properties section
        new_content = content[:insert_point] + empty_section + content[insert_point:]
        
        # Write updated content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error updating file {filepath}: {str(e)}")
        return False

async def main():
    """Main function to analyze all databases for empty properties."""
    # Database inventory
    databases = {
        # CRM
        "Companies": "22bf4e0d-84e0-80bb-8d1c-c90710d44870",
        "Contacts": "226f4e0d-84e0-814c-ad70-d478cebeee30",
        "Hair Orders Profiles": "248f4e0d-84e0-80ad-9d33-e90e5124c092",
        "Emails": "228f4e0d-84e0-8185-a49d-c68df1c94301",
        "Email Templates": "231f4e0d-84e0-80a9-a8d3-cbc04da25dcb",
        "Customer Portal Data": "238f4e0d-84e0-80f9-b09f-ebe986c6cf2a",
        
        # Sales & Operations
        "Deals": "226f4e0d-84e0-808c-af51-e09c154008db",
        "Plans": "228f4e0d-84e0-815c-a108-e48054988ac0",
        "Orders": "228f4e0d-84e0-816f-8511-fab726d2c6ef",
        "Purchase Orders": "237f4e0d-84e0-807b-860c-cb9599ddaea0",
        "Suppliers Inventory": "226f4e0d-84e0-814f-a468-d44302ee0478",
        "Ad Campaigns": "226f4e0d-84e0-819d-be89-db73c48eaee4",
        "Platform": "226f4e0d-84e0-81aa-a79c-ffad8081015e",
        "Content": "226f4e0d-84e0-816a-ac2f-f089654d45fc",
        
        # Finances
        "Payments": "22af4e0d-84e0-80c3-a7d6-f0209d93081d",
        "Incomes": "229f4e0d-84e0-8128-a0bf-d7631b6aa22d",
        "Expenses": "226f4e0d-84e0-817e-84e2-c9a983663070",
        "Recurring Expenses": "226f4e0d-84e0-813f-b2e9-d228f70676b9",
        "Forecasted Payments": "22cf4e0d-84e0-802a-bf76-e564658fdc5f",
        "Income Sources": "226f4e0d-84e0-81d9-b998-e61ecae5c421",
        "Expense Categories": "226f4e0d-84e0-81a9-a37b-fc2aabd167c8",
        "Debt Tracking": "226f4e0d-84e0-8130-8a9c-ce4a29ef7a35",
        "Debt Overview": "226f4e0d-84e0-8171-aea1-d054e8cb0786",
        "Budget Split 50/20/30": "226f4e0d-84e0-8187-bcb1-c1290226a0a2",
        
        # Management & Reports
        "Business Projects": "226f4e0d-84e0-816d-a749-e741b1ac0b30",
        "Tasks": "226f4e0d-84e0-8168-8718-d8f6b2d1fe3d",
        "Daily Reports": "22cf4e0d-84e0-8036-a313-f6cfa1fa9801",
        "Monthly Reports (Main)": "226f4e0d-84e0-8101-81e1-c9f2d6803291",
        "Yearly Reports": "226f4e0d-84e0-8179-98cb-cca8ecbf0c15",
        "Objectives": "226f4e0d-84e0-81f1-88a5-f0eb2eb1bd87",
        "Key Results": "226f4e0d-84e0-815f-b434-c1a6e3a28e16",
        "Hubspot Properties Management": "232f4e0d-84e0-8049-abb0-d5c04fa1628c",
        
        # Knowledge & Documents
        "Business Resources": "226f4e0d-84e0-8135-a4f7-ee34b04fe01b",
        "Products & Pricing Catalog": "232f4e0d-84e0-8000-aad7-de8ff9504fd1",
        "Plan Pricing": "239f4e0d-84e0-8017-b600-d74cfcaa3551"
    }
    
    print("🚀 Starting empty properties analysis across all databases...")
    print(f"📊 Analyzing {len(databases)} databases for unused properties")
    print()
    
    total_empty_props = 0
    total_mostly_empty_props = 0
    success_count = 0
    error_count = 0
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        for db_name, db_id in databases.items():
            empty_props, mostly_empty_props, total_pages = await analyze_database(client, db_name, db_id)
            
            if empty_props is not None and mostly_empty_props is not None:
                # Update the markdown file
                if update_markdown_file(db_name, empty_props, mostly_empty_props, total_pages):
                    print(f"   ✅ Updated documentation file")
                    success_count += 1
                    total_empty_props += len(empty_props)
                    total_mostly_empty_props += len(mostly_empty_props)
                else:
                    print(f"   ❌ Failed to update documentation file")
                    error_count += 1
            else:
                error_count += 1
            
            print()
            
            # Delay between databases to be respectful to API
            await asyncio.sleep(1.0)
    
    print("📊 Analysis Complete!")
    print(f"   ✅ Successfully analyzed: {success_count} databases")
    print(f"   ❌ Errors: {error_count} databases")
    print(f"   🚫 Total completely empty properties found: {total_empty_props}")
    print(f"   ⚠️  Total mostly empty properties found: {total_mostly_empty_props}")
    print()
    print("🎉 All database documentation files have been updated with empty property analysis!")
    print("📖 Check each database's .md file for the new '🚫 Empty & Unused Properties' section.")

if __name__ == "__main__":
    asyncio.run(main())
