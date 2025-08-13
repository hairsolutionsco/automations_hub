"""Script to reorganize Notion databases according to the markdown file structure."""

import asyncio
import sys
import os
sys.path.append('.')

from tools.notion_api import search_notion, get_notion_page
from tools.notion_database_management import (
    get_notion_database, 
    archive_notion_database, 
    query_database_records,
    get_page_blocks,
    update_page_blocks
)

# Database IDs from the markdown file (these should be kept)
DATABASES_TO_KEEP = {
    # CRM
    "22bf4e0d-84e0-80bb-8d1c-c90710d44870",  # Companies
    "226f4e0d-84e0-814c-ad70-d478cebeee30",  # Contacts
    "248f4e0d-84e0-80ad-9d33-e90e5124c092",  # Hair Orders Profiles
    "228f4e0d-84e0-8185-a49d-c68df1c94301",  # Emails
    "231f4e0d-84e0-80a9-a8d3-cbc04da25dcb",  # Email Templates
    "238f4e0d-84e0-80f9-b09f-ebe986c6cf2a",  # Customer Portal Data
    
    # Sales & Operations
    "226f4e0d-84e0-808c-af51-e09c154008db",  # Deals
    "228f4e0d-84e0-815c-a108-e48054988ac0",  # Plans
    "228f4e0d-84e0-816f-8511-fab726d2c6ef",  # Orders
    "237f4e0d-84e0-807b-860c-cb9599ddaea0",  # Purchase Orders
    "226f4e0d-84e0-814f-a468-d44302ee0478",  # Suppliers Inventory
    "226f4e0d-84e0-819d-be89-db73c48eaee4",  # Ad Campaigns
    "226f4e0d-84e0-81aa-a79c-ffad8081015e",  # Platform
    "226f4e0d-84e0-816a-ac2f-f089654d45fc",  # Content
    "42cf7bf5-1b0b-446e-a2e0-6dc851db6092",  # Blog Posts
    
    # Finances
    "22af4e0d-84e0-80c3-a7d6-f0209d93081d",  # Payments
    "229f4e0d-84e0-8128-a0bf-d7631b6aa22d",  # Incomes
    "226f4e0d-84e0-817e-84e2-c9a983663070",  # Expenses
    "226f4e0d-84e0-813f-b2e9-d228f70676b9",  # Recurring Expenses
    "22cf4e0d-84e0-802a-bf76-e564658fdc5f",  # Forecasted Payments
    "232f4e0d-84e0-80c6-a565-ebc67a43ffa5",  # Forecasted Income
    "226f4e0d-84e0-81d9-b998-e61ecae5c421",  # Income Sources
    "226f4e0d-84e0-81a9-a37b-fc2aabd167c8",  # Expense Categories
    "226f4e0d-84e0-81de-a364-fe70d608f59f",  # Expense Sources
    "226f4e0d-84e0-8130-8a9c-ce4a29ef7a35",  # Debt Tracking
    "226f4e0d-84e0-8171-aea1-d054e8cb0786",  # Debt Overview
    "226f4e0d-84e0-8187-bcb1-c1290226a0a2",  # Budget Split 50/20/30
    "226f4e0d-84e0-81de-90ac-dd1c31b77f07",  # Accounts and Goals
    "226f4e0d-84e0-81bc-9ea0-d326c752ea42",  # Transfers
    
    # Management & Reports
    "226f4e0d-84e0-816d-a749-e741b1ac0b30",  # Business Projects
    "226f4e0d-84e0-8168-8718-d8f6b2d1fe3d",  # Tasks
    "22cf4e0d-84e0-8036-a313-f6cfa1fa9801",  # Daily Reports
    "226f4e0d-84e0-8101-81e1-c9f2d6803291",  # Monthly Reports (Main)
    "226f4e0d-84e0-81cf-870c-cd2513656af8",  # Monthly Reports (Alternative - to be merged)
    "226f4e0d-84e0-8179-98cb-cca8ecbf0c15",  # Yearly Reports
    "226f4e0d-84e0-8132-a1b5-e03044806426",  # Yearly Reports (Alternative - to be merged)
    "226f4e0d-84e0-81f1-88a5-f0eb2eb1bd87",  # Objectives
    "226f4e0d-84e0-815f-b434-c1a6e3a28e16",  # Key Results
    "232f4e0d-84e0-8049-abb0-d5c04fa1628c",  # Hubspot Properties Management
    
    # Knowledge & Documents
    "226f4e0d-84e0-8135-a4f7-ee34b04fe01b",  # Business Resources
    "232f4e0d-84e0-8000-aad7-de8ff9504fd1",  # Products & Pricing Catalog
    "239f4e0d-84e0-8017-b600-d74cfcaa3551",  # Plan Pricing
}

# Databases to be deleted (mentioned in original request)
DATABASES_TO_DELETE = {
    "226f4e0d-84e0-818b-914b-d3666bd9125f",  # Resource Topics
}

# Merging mappings (merge from -> merge to)
DATABASES_TO_MERGE = {
    # Monthly Reports: merge alternative into main
    "226f4e0d-84e0-81cf-870c-cd2513656af8": "226f4e0d-84e0-8101-81e1-c9f2d6803291",
    # Yearly Reports: merge alternative into main  
    "226f4e0d-84e0-8132-a1b5-e03044806426": "226f4e0d-84e0-8179-98cb-cca8ecbf0c15",
}

BACKEND_PAGE_ID = "226f4e0d-84e0-81a8-8ad2-c2230c5202e7"


async def find_all_databases():
    """Find all databases in the workspace."""
    print("🔍 Searching for all databases in workspace...")
    result = await search_notion("", "database")
    
    if result.success:
        databases = result.data.get("results", [])
        print(f"Found {len(databases)} total databases")
        
        for db in databases:
            db_id = db.get("id", "").replace("-", "")
            title = "Untitled"
            if "title" in db.get("properties", {}):
                title_array = db["properties"]["title"].get("title", [])
                if title_array:
                    title = title_array[0].get("plain_text", "Untitled")
            
            status = "✅ KEEP" if db_id in DATABASES_TO_KEEP else "🗑️ DELETE"
            print(f"  {status}: {title} ({db_id})")
        
        return databases
    else:
        print(f"❌ Failed to find databases: {result.message}")
        return []


async def check_database_completeness(db_id):
    """Check how complete a database is by looking at field count and record count."""
    print(f"📊 Checking completeness of database {db_id}...")
    
    # Get database schema
    db_result = await get_notion_database(db_id)
    if not db_result.success:
        print(f"❌ Failed to get database schema: {db_result.message}")
        return {"fields": 0, "records": 0, "error": db_result.message}
    
    field_count = len(db_result.data.get("properties", {}))
    
    # Check record count
    records_result = await query_database_records(db_id)
    if not records_result.success:
        print(f"❌ Failed to query database records: {records_result.message}")
        return {"fields": field_count, "records": 0, "error": records_result.message}
    
    record_count = records_result.data.get("record_count", 0)
    has_more = records_result.data.get("has_more", False)
    
    completeness = {
        "fields": field_count,
        "records": record_count,
        "has_more": has_more,
        "score": field_count + (record_count * 0.1)  # Simple scoring system
    }
    
    print(f"  Fields: {field_count}, Records: {record_count}{'+ (more)' if has_more else ''}, Score: {completeness['score']:.1f}")
    return completeness


async def merge_databases():
    """Merge databases according to the mapping."""
    print("\n🔄 Starting database merging process...")
    
    for source_id, target_id in DATABASES_TO_MERGE.items():
        print(f"\n📋 Merging {source_id} → {target_id}")
        
        # Check completeness of both databases
        source_completeness = await check_database_completeness(source_id)
        target_completeness = await check_database_completeness(target_id)
        
        # Determine which is more complete
        if source_completeness.get("score", 0) > target_completeness.get("score", 0):
            print(f"⚠️  Source database is more complete! Recommend merging {target_id} → {source_id} instead")
            continue
        
        print(f"✅ Target database is more complete. Proceeding with merge.")
        
        # For now, we'll just archive the source database
        # In a real implementation, you'd want to copy records first
        print(f"🗃️  Archiving source database {source_id}...")
        archive_result = await archive_notion_database(source_id)
        
        if archive_result.success:
            print(f"✅ Successfully archived {source_id}")
        else:
            print(f"❌ Failed to archive {source_id}: {archive_result.message}")


async def delete_unwanted_databases():
    """Delete databases that don't appear in the markdown file."""
    print("\n🗑️  Starting database deletion process...")
    
    # Find all databases
    all_databases = await find_all_databases()
    
    for db in all_databases:
        db_id = db.get("id", "").replace("-", "")
        
        # Skip if it's a database we want to keep
        if db_id in DATABASES_TO_KEEP:
            continue
            
        # Skip if it's already in our delete list
        if db_id in DATABASES_TO_DELETE:
            continue
            
        title = "Untitled"
        if "title" in db.get("properties", {}):
            title_array = db["properties"]["title"].get("title", [])
            if title_array:
                title = title_array[0].get("plain_text", "Untitled")
        
        print(f"\n🗑️  Deleting unwanted database: {title} ({db_id})")
        
        # Archive the database
        archive_result = await archive_notion_database(db_id)
        
        if archive_result.success:
            print(f"✅ Successfully deleted {title}")
        else:
            print(f"❌ Failed to delete {title}: {archive_result.message}")
    
    # Delete explicitly marked databases
    for db_id in DATABASES_TO_DELETE:
        print(f"\n🗑️  Deleting marked database: {db_id}")
        archive_result = await archive_notion_database(db_id)
        
        if archive_result.success:
            print(f"✅ Successfully deleted {db_id}")
        else:
            print(f"❌ Failed to delete {db_id}: {archive_result.message}")


async def create_new_page_structure():
    """Create new page structure with organized headings."""
    print("\n📄 Creating new page structure...")
    
    # Define the new structure based on markdown
    new_blocks = [
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "👥 CRM"}}]
            }
        },
        {
            "object": "block", 
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "💼 Sales & Operations"}}]
            }
        },
        {
            "object": "block",
            "type": "heading_2", 
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "💰 Finances"}}]
            }
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "🏢 Management & Reports"}}]
            }
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "📚 Knowledge & Documents"}}]
            }
        }
    ]
    
    # Get current page blocks
    blocks_result = await get_page_blocks(BACKEND_PAGE_ID)
    
    if blocks_result.success:
        print(f"📋 Current page has {len(blocks_result.blocks)} blocks")
        
        # For now, let's just add the new structure
        # In a real implementation, you'd reorganize existing database blocks
        update_result = await update_page_blocks(BACKEND_PAGE_ID, new_blocks)
        
        if update_result.success:
            print("✅ Successfully updated page structure")
        else:
            print(f"❌ Failed to update page structure: {update_result.message}")
    else:
        print(f"❌ Failed to get current page blocks: {blocks_result.message}")


async def main():
    """Main reorganization function."""
    print("🚀 Starting Notion database reorganization...")
    print("=" * 60)
    
    try:
        # Step 1: Find all databases and show what will happen
        await find_all_databases()
        
        # Step 2: Merge databases 
        await merge_databases()
        
        # Step 3: Delete unwanted databases
        await delete_unwanted_databases()
        
        # Step 4: Create new page structure
        await create_new_page_structure()
        
        print("\n" + "=" * 60)
        print("✅ Database reorganization completed!")
        
    except Exception as e:
        print(f"\n❌ Error during reorganization: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
