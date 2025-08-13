"""Script to reorganize the Backend page with proper headers and database grouping."""

import asyncio
import sys
import os
sys.path.append('.')

from tools.notion_api import search_notion, get_notion_page
from tools.notion_database_management import get_page_blocks, update_page_blocks
import httpx


async def clear_page_blocks(page_id: str) -> bool:
    """Clear all blocks from a page."""
    try:
        api_key = os.getenv("NOTION_API_KEY")
        
        if not api_key:
            print("❌ NOTION_API_KEY not configured")
            return False

        # First get all blocks
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.notion.com/v1/blocks/{page_id}/children",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Notion-Version": "2022-06-28"
                }
            )
            
            if response.status_code != 200:
                print(f"❌ Failed to get page blocks: {response.status_code}")
                return False
            
            blocks_data = response.json()
            blocks = blocks_data.get("results", [])
            
            # Delete each block
            for block in blocks:
                block_id = block.get("id")
                if block_id:
                    delete_response = await client.delete(
                        f"https://api.notion.com/v1/blocks/{block_id}",
                        headers={
                            "Authorization": f"Bearer {api_key}",
                            "Notion-Version": "2022-06-28"
                        }
                    )
                    
                    if delete_response.status_code == 200:
                        print(f"✅ Deleted block {block_id}")
                    else:
                        print(f"❌ Failed to delete block {block_id}")
            
            return True
                
    except Exception as e:
        print(f"❌ Error clearing page blocks: {str(e)}")
        return False


async def add_blocks_to_page(page_id: str, blocks: list) -> bool:
    """Add blocks to a page."""
    try:
        api_key = os.getenv("NOTION_API_KEY")
        
        if not api_key:
            print("❌ NOTION_API_KEY not configured")
            return False

        async with httpx.AsyncClient() as client:
            response = await client.patch(
                f"https://api.notion.com/v1/blocks/{page_id}/children",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "Notion-Version": "2022-06-28"
                },
                json={"children": blocks}
            )
            
            if response.status_code == 200:
                print(f"✅ Successfully added {len(blocks)} blocks to page")
                return True
            else:
                print(f"❌ Failed to add blocks: {response.status_code} {response.text}")
                return False
                
    except Exception as e:
        print(f"❌ Error adding blocks to page: {str(e)}")
        return False


def create_database_block(database_id: str) -> dict:
    """Create a database block for embedding in the page."""
    return {
        "object": "block",
        "type": "child_database",
        "child_database": {
            "title": "",
            "database_id": database_id
        }
    }


async def main():
    """Reorganize the Backend page with proper structure."""
    print("🏗️  REORGANIZING BACKEND PAGE STRUCTURE")
    print("=" * 50)
    
    BACKEND_PAGE_ID = "226f4e0d-84e0-81a8-8ad2-c2230c5202e7"
    
    # Database organization from markdown file
    database_organization = {
        "👥 CRM": [
            "22bf4e0d-84e0-80bb-8d1c-c90710d44870",  # Companies
            "226f4e0d-84e0-814c-ad70-d478cebeee30",  # Contacts
            "248f4e0d-84e0-80ad-9d33-e90e5124c092",  # Hair Orders Profiles
            "228f4e0d-84e0-8185-a49d-c68df1c94301",  # Emails
            "231f4e0d-84e0-80a9-a8d3-cbc04da25dcb",  # Email Templates
            "238f4e0d-84e0-80f9-b09f-ebe986c6cf2a",  # Customer Portal Data
        ],
        "💼 Sales & Operations": [
            "226f4e0d-84e0-808c-af51-e09c154008db",  # Deals
            "228f4e0d-84e0-815c-a108-e48054988ac0",  # Plans
            "228f4e0d-84e0-816f-8511-fab726d2c6ef",  # Orders
            "237f4e0d-84e0-807b-860c-cb9599ddaea0",  # Purchase Orders
            "226f4e0d-84e0-814f-a468-d44302ee0478",  # Suppliers Inventory
            "226f4e0d-84e0-819d-be89-db73c48eaee4",  # Ad Campaigns
            "226f4e0d-84e0-81aa-a79c-ffad8081015e",  # Platform
            "226f4e0d-84e0-816a-ac2f-f089654d45fc",  # Content
        ],
        "💰 Finances": [
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
        ],
        "🏢 Management & Reports": [
            "226f4e0d-84e0-816d-a749-e741b1ac0b30",  # Business Projects
            "226f4e0d-84e0-8168-8718-d8f6b2d1fe3d",  # Tasks
            "22cf4e0d-84e0-8036-a313-f6cfa1fa9801",  # Daily Reports
            "226f4e0d-84e0-8101-81e1-c9f2d6803291",  # Monthly Reports (Main)
            "226f4e0d-84e0-8179-98cb-cca8ecbf0c15",  # Yearly Reports
            "226f4e0d-84e0-81f1-88a5-f0eb2eb1bd87",  # Objectives
            "226f4e0d-84e0-815f-b434-c1a6e3a28e16",  # Key Results
            "232f4e0d-84e0-8049-abb0-d5c04fa1628c",  # Hubspot Properties Management
        ],
        "📚 Knowledge & Documents": [
            "226f4e0d-84e0-8135-a4f7-ee34b04fe01b",  # Business Resources
            "232f4e0d-84e0-8000-aad7-de8ff9504fd1",  # Products & Pricing Catalog
            "239f4e0d-84e0-8017-b600-d74cfcaa3551",  # Plan Pricing
        ],
    }
    
    # Build the blocks structure
    all_blocks = []
    
    for section_title, database_ids in database_organization.items():
        print(f"\n📋 Creating section: {section_title}")
        
        # Add H1 header for the section
        header_block = {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": section_title}
                    }
                ]
            }
        }
        all_blocks.append(header_block)
        
        # Add databases for this section
        for db_id in database_ids:
            print(f"  📊 Adding database: {db_id}")
            db_block = create_database_block(db_id)
            all_blocks.append(db_block)
        
        # Add spacing between sections
        spacer_block = {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": []
            }
        }
        all_blocks.append(spacer_block)
    
    print(f"\n🏗️  Clearing existing page content...")
    clear_success = await clear_page_blocks(BACKEND_PAGE_ID)
    
    if not clear_success:
        print("❌ Failed to clear page content")
        return
    
    print(f"📝 Adding {len(all_blocks)} blocks to the page...")
    
    # Add blocks in batches (Notion has limits on batch size)
    batch_size = 100
    for i in range(0, len(all_blocks), batch_size):
        batch = all_blocks[i:i + batch_size]
        print(f"📦 Adding batch {i//batch_size + 1} ({len(batch)} blocks)...")
        
        success = await add_blocks_to_page(BACKEND_PAGE_ID, batch)
        if not success:
            print(f"❌ Failed to add batch {i//batch_size + 1}")
            return
        
        # Small delay to avoid rate limits
        await asyncio.sleep(1)
    
    print("\n" + "=" * 50)
    print("✅ Successfully reorganized Backend page!")
    print("🎉 Your databases are now properly grouped under category headers!")


if __name__ == "__main__":
    asyncio.run(main())
