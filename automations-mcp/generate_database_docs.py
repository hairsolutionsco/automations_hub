"""Script to generate detailed documentation for each Notion database."""

import asyncio
import sys
import os
import re
sys.path.append('.')

from tools.notion_api import search_notion
import httpx


async def get_database_details(database_id: str) -> dict:
    """Get detailed information about a database including all properties."""
    try:
        api_key = os.getenv("NOTION_API_KEY")
        
        if not api_key:
            print("❌ NOTION_API_KEY not configured")
            return None

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.notion.com/v1/databases/{database_id}",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Notion-Version": "2022-06-28"
                }
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Failed to get database {database_id}: {response.status_code}")
                return None
                
    except Exception as e:
        print(f"❌ Error getting database {database_id}: {str(e)}")
        return None


def format_property_details(prop_name: str, prop_data: dict) -> str:
    """Format property details for markdown documentation."""
    prop_type = prop_data.get("type", "unknown")
    
    details = f"### {prop_name}\n"
    details += f"- **Type:** `{prop_type}`\n"
    
    # Add type-specific details
    if prop_type == "select":
        options = prop_data.get("select", {}).get("options", [])
        if options:
            details += f"- **Options:** "
            option_names = [opt.get("name", "") for opt in options]
            details += ", ".join([f"`{name}`" for name in option_names if name])
            details += "\n"
    
    elif prop_type == "multi_select":
        options = prop_data.get("multi_select", {}).get("options", [])
        if options:
            details += f"- **Options:** "
            option_names = [opt.get("name", "") for opt in options]
            details += ", ".join([f"`{name}`" for name in option_names if name])
            details += "\n"
    
    elif prop_type == "number":
        number_format = prop_data.get("number", {}).get("format", "")
        if number_format:
            details += f"- **Format:** `{number_format}`\n"
    
    elif prop_type == "formula":
        expression = prop_data.get("formula", {}).get("expression", "")
        if expression:
            details += f"- **Formula:** `{expression}`\n"
    
    elif prop_type == "relation":
        database_id = prop_data.get("relation", {}).get("database_id", "")
        if database_id:
            details += f"- **Related Database:** `{database_id}`\n"
    
    elif prop_type == "rollup":
        rollup_info = prop_data.get("rollup", {})
        if rollup_info:
            relation_prop = rollup_info.get("relation_property_name", "")
            rollup_prop = rollup_info.get("rollup_property_name", "")
            function = rollup_info.get("function", "")
            if relation_prop:
                details += f"- **Relation Property:** `{relation_prop}`\n"
            if rollup_prop:
                details += f"- **Rollup Property:** `{rollup_prop}`\n"
            if function:
                details += f"- **Function:** `{function}`\n"
    
    details += "\n"
    return details


def clean_filename(name: str) -> str:
    """Clean a database name to be suitable for a filename."""
    # Remove or replace problematic characters
    cleaned = re.sub(r'[^\w\s-]', '', name)
    cleaned = re.sub(r'[-\s]+', '-', cleaned)
    return cleaned.lower()


async def generate_database_documentation(database_id: str, database_name: str) -> str:
    """Generate comprehensive documentation for a single database."""
    print(f"📋 Generating documentation for: {database_name}")
    
    db_details = await get_database_details(database_id)
    if not db_details:
        return None
    
    # Extract database information
    title = database_name
    properties = db_details.get("properties", {})
    created_time = db_details.get("created_time", "")
    last_edited_time = db_details.get("last_edited_time", "")
    
    # Build documentation
    doc = f"# {title}\n\n"
    doc += f"**Database ID:** `{database_id}`\n\n"
    doc += f"**Created:** {created_time}\n"
    doc += f"**Last Modified:** {last_edited_time}\n"
    doc += f"**Total Properties:** {len(properties)}\n\n"
    
    doc += "---\n\n"
    doc += "## Properties Overview\n\n"
    
    # Group properties by type
    property_types = {}
    for prop_name, prop_data in properties.items():
        prop_type = prop_data.get("type", "unknown")
        if prop_type not in property_types:
            property_types[prop_type] = []
        property_types[prop_type].append(prop_name)
    
    # Display property summary
    for prop_type, prop_names in sorted(property_types.items()):
        doc += f"- **{prop_type.title()}** ({len(prop_names)}): {', '.join([f'`{name}`' for name in prop_names])}\n"
    
    doc += "\n---\n\n"
    doc += "## Detailed Property Documentation\n\n"
    
    # Document each property in detail
    for prop_name, prop_data in sorted(properties.items()):
        doc += format_property_details(prop_name, prop_data)
    
    doc += "---\n\n"
    doc += "## Usage Notes\n\n"
    doc += "<!-- Add any specific usage notes, business logic, or important information about this database -->\n\n"
    
    doc += "## Related Databases\n\n"
    doc += "<!-- List any databases that this one relates to or depends on -->\n\n"
    
    return doc


async def main():
    """Generate documentation for all databases."""
    print("📚 GENERATING COMPREHENSIVE DATABASE DOCUMENTATION")
    print("=" * 60)
    
    # Get all databases
    result = await search_notion('', 'database')
    if not result.success:
        print(f"❌ Failed to search databases: {result.message}")
        return
    
    databases = result.data.get('results', [])
    print(f"📊 Found {len(databases)} databases to document")
    print()
    
    success_count = 0
    
    for db in databases:
        db_id = db.get('id', '')
        
        # Get database title
        title = 'Untitled Database'
        if 'title' in db.get('properties', {}):
            title_array = db['properties']['title'].get('title', [])
            if title_array:
                title = title_array[0].get('plain_text', 'Untitled Database')
        
        # Generate documentation
        documentation = await generate_database_documentation(db_id, title)
        
        if documentation:
            # Create filename
            filename = clean_filename(title)
            filepath = f"/workspaces/automations_hub/notion/databases/{filename}.md"
            
            # Write documentation to file
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(documentation)
                print(f"✅ Created: {filepath}")
                success_count += 1
            except Exception as e:
                print(f"❌ Failed to write {filepath}: {str(e)}")
        else:
            print(f"❌ Failed to generate documentation for {title}")
        
        # Small delay to avoid rate limits
        await asyncio.sleep(0.5)
    
    print(f"\n{'=' * 60}")
    print(f"📋 DOCUMENTATION GENERATION COMPLETE")
    print(f"✅ Successfully documented: {success_count}/{len(databases)} databases")
    print(f"📁 Files saved to: /workspaces/automations_hub/notion/databases/")


if __name__ == "__main__":
    asyncio.run(main())
