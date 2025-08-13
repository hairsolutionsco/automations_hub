#!/usr/bin/env python3
"""
Generate comprehensive documentation for all Notion databases.
This script creates individual markdown files for each database with detailed field documentation.
"""

import asyncio
import sys
import os
import httpx
from datetime import datetime
import json

# Add the current directory to Python path
sys.path.append('.')

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

def format_options_vertically(options, indent="  "):
    """Format options in vertical list with proper indentation."""
    if not options:
        return ""
    
    # Handle case where there are too many options (like 100 unit IDs)
    if len(options) > 20:
        first_option = options[0].get('name', '')
        last_option = options[-1].get('name', '')
        return f"{indent}**{len(options)} options** from `{first_option}` to `{last_option}`"
    
    formatted_options = []
    for option in options:
        option_name = option.get('name', '')
        formatted_options.append(f"{indent}- `{option_name}`")
    
    return "\n".join(formatted_options)

def group_properties_by_type(properties):
    """Group properties by their type for the overview section."""
    type_groups = {}
    
    for prop_name, prop_data in properties.items():
        prop_type = prop_data.get('type', 'unknown')
        if prop_type not in type_groups:
            type_groups[prop_type] = []
        type_groups[prop_type].append(prop_name)
    
    return type_groups

def generate_properties_overview(type_groups):
    """Generate the properties overview section with vertical listing."""
    overview = "## Properties Overview\n\n"
    
    # Sort types for consistent output
    for prop_type in sorted(type_groups.keys()):
        properties = sorted(type_groups[prop_type])
        overview += f"### {prop_type} ({len(properties)})\n"
        for prop in properties:
            overview += f"- `{prop}`\n"
        overview += "\n"
    
    return overview

def generate_detailed_documentation(properties):
    """Generate detailed documentation for each property."""
    doc = "## Detailed Property Documentation\n\n"
    
    # Sort properties alphabetically
    for prop_name in sorted(properties.keys()):
        prop_data = properties[prop_name]
        prop_type = prop_data.get('type', 'unknown')
        
        doc += f"### {prop_name}\n"
        doc += f"- **Type:** `{prop_type}`\n"
        
        # Handle different property types
        if prop_type == 'select':
            options = prop_data.get('select', {}).get('options', [])
            if options:
                doc += "- **Options:**\n"
                doc += format_options_vertically(options) + "\n"
        
        elif prop_type == 'multi_select':
            options = prop_data.get('multi_select', {}).get('options', [])
            if options:
                doc += "- **Options:**\n"
                doc += format_options_vertically(options) + "\n"
        
        elif prop_type == 'relation':
            relation_data = prop_data.get('relation', {})
            related_db = relation_data.get('database_id', '')
            if related_db:
                doc += f"- **Related Database:** `{related_db}`\n"
        
        elif prop_type == 'formula':
            formula_data = prop_data.get('formula', {})
            expression = formula_data.get('expression', '')
            if expression:
                doc += f"- **Formula:** `{expression}`\n"
        
        elif prop_type == 'rollup':
            rollup_data = prop_data.get('rollup', {})
            relation_prop = rollup_data.get('relation_property_name', '')
            rollup_prop = rollup_data.get('rollup_property_name', '')
            function = rollup_data.get('function', '')
            if relation_prop:
                doc += f"- **Relation Property:** `{relation_prop}`\n"
            if rollup_prop:
                doc += f"- **Rollup Property:** `{rollup_prop}`\n"
            if function:
                doc += f"- **Function:** `{function}`\n"
        
        doc += "\n"
    
    return doc

def find_related_databases(properties):
    """Find all related databases from relation properties."""
    related_dbs = {}
    
    for prop_name, prop_data in properties.items():
        if prop_data.get('type') == 'relation':
            relation_data = prop_data.get('relation', {})
            related_db_id = relation_data.get('database_id', '')
            if related_db_id:
                related_dbs[prop_name] = related_db_id
    
    return related_dbs

def generate_markdown_file(database_name, database_id, database_data):
    """Generate complete markdown documentation for a database."""
    properties = database_data.get('properties', {})
    created_time = database_data.get('created_time', '')
    last_edited_time = database_data.get('last_edited_time', '')
    
    # Group properties by type
    type_groups = group_properties_by_type(properties)
    
    # Generate markdown content
    content = f"# {database_name} Database\n\n"
    content += f"**Database ID:** `{database_id}`\n\n"
    
    if created_time:
        content += f"**Created:** {created_time}\n"
    if last_edited_time:
        content += f"**Last Modified:** {last_edited_time}\n"
    
    content += f"**Total Properties:** {len(properties)}\n\n"
    content += "---\n\n"
    
    # Add properties overview
    content += generate_properties_overview(type_groups)
    content += "---\n\n"
    
    # Add detailed documentation
    content += generate_detailed_documentation(properties)
    
    # Add related databases section
    related_dbs = find_related_databases(properties)
    if related_dbs:
        content += "## Related Databases\n\n"
        for prop_name, db_id in related_dbs.items():
            content += f"- **{prop_name}** (`{db_id}`)\n"
        content += "\n"
    
    content += "---\n\n"
    content += f"*Documentation generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
    
    return content

async def main():
    """Main function to process all databases."""
    # Database inventory - updated from notion-databases-inventory.md
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
    
    print("🚀 Starting database documentation generation...")
    print(f"📊 Found {len(databases)} databases to process")
    print()
    
    # Create databases directory if it doesn't exist
    os.makedirs("/workspaces/automations_hub/notion/databases", exist_ok=True)
    
    success_count = 0
    error_count = 0
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        for db_name, db_id in databases.items():
            print(f"📋 Processing: {db_name}")
            
            try:
                # Fetch database data
                database_data = await get_database_properties(client, db_id)
                
                if database_data:
                    # Generate markdown content
                    markdown_content = generate_markdown_file(db_name, db_id, database_data)
                    
                    # Create safe filename
                    safe_filename = db_name.lower().replace(" ", "_").replace("&", "and").replace("/", "_").replace(":", "").replace("⏰", "")
                    filepath = f"/workspaces/automations_hub/notion/databases/{safe_filename}.md"
                    
                    # Write file
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(markdown_content)
                    
                    properties_count = len(database_data.get('properties', {}))
                    print(f"   ✅ Generated {safe_filename}.md ({properties_count} properties)")
                    success_count += 1
                    
                else:
                    print(f"   ❌ Failed to fetch data for {db_name}")
                    error_count += 1
                    
            except Exception as e:
                print(f"   ❌ Error processing {db_name}: {str(e)}")
                error_count += 1
            
            # Small delay to be respectful to the API
            await asyncio.sleep(0.5)
    
    print()
    print("📊 Documentation Generation Summary:")
    print(f"   ✅ Successful: {success_count}")
    print(f"   ❌ Errors: {error_count}")
    print(f"   📁 Files saved to: /workspaces/automations_hub/notion/databases/")
    
    if success_count > 0:
        print()
        print("🎉 Database documentation generation completed!")
        print("📖 Each database now has its own detailed markdown file with:")
        print("   • Vertical property listings grouped by type")
        print("   • Detailed field documentation with options")
        print("   • Related database references")
        print("   • Comprehensive field type information")

if __name__ == "__main__":
    asyncio.run(main())
