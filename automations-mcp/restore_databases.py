"""Script to restore archived databases in Notion."""

import asyncio
import sys
import os
sys.path.append('.')

from tools.notion_api import search_notion
from tools.notion_database_management import get_notion_database
import httpx


async def restore_database(database_id: str) -> bool:
    """Restore an archived database."""
    try:
        api_key = os.getenv("NOTION_API_KEY")
        
        if not api_key:
            print(f"❌ NOTION_API_KEY not configured")
            return False

        async with httpx.AsyncClient() as client:
            response = await client.patch(
                f"https://api.notion.com/v1/databases/{database_id}",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "Notion-Version": "2022-06-28"
                },
                json={"archived": False}
            )
            
            if response.status_code == 200:
                print(f"✅ Successfully restored database {database_id}")
                return True
            else:
                print(f"❌ Failed to restore database {database_id}: {response.status_code} {response.text}")
                return False
                
    except Exception as e:
        print(f"❌ Error restoring database {database_id}: {str(e)}")
        return False


async def search_archived_databases():
    """Search for archived databases."""
    try:
        api_key = os.getenv("NOTION_API_KEY")
        
        if not api_key:
            print("❌ NOTION_API_KEY not configured")
            return []

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.notion.com/v1/search",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "Notion-Version": "2022-06-28"
                },
                json={
                    "filter": {
                        "value": "database",
                        "property": "object"
                    },
                    "page_size": 100
                }
            )
            
            if response.status_code == 200:
                search_results = response.json()
                all_databases = search_results.get("results", [])
                
                # Filter for archived databases
                archived_databases = [db for db in all_databases if db.get("archived", False)]
                
                print(f"Found {len(archived_databases)} archived databases")
                return archived_databases
            else:
                print(f"❌ Failed to search databases: {response.status_code} {response.text}")
                return []
                
    except Exception as e:
        print(f"❌ Error searching for archived databases: {str(e)}")
        return []


async def main():
    """Main recovery function."""
    print("🚨 EMERGENCY DATABASE RECOVERY")
    print("=" * 50)
    
    # Database IDs that should exist (from the markdown file)
    DATABASES_THAT_SHOULD_EXIST = {
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
        "226f4e0d-84e0-8179-98cb-cca8ecbf0c15",  # Yearly Reports
        "226f4e0d-84e0-81f1-88a5-f0eb2eb1bd87",  # Objectives
        "226f4e0d-84e0-815f-b434-c1a6e3a28e16",  # Key Results
        "232f4e0d-84e0-8049-abb0-d5c04fa1628c",  # Hubspot Properties Management
        
        # Knowledge & Documents
        "226f4e0d-84e0-8135-a4f7-ee34b04fe01b",  # Business Resources
        "232f4e0d-84e0-8000-aad7-de8ff9504fd1",  # Products & Pricing Catalog
        "239f4e0d-84e0-8017-b600-d74cfcaa3551",  # Plan Pricing
    }
    
    print(f"🔍 Looking for {len(DATABASES_THAT_SHOULD_EXIST)} databases that should exist...")
    
    # Search for archived databases
    archived_databases = await search_archived_databases()
    
    restored_count = 0
    failed_count = 0
    
    # Try to restore each database that should exist
    for db_id in DATABASES_THAT_SHOULD_EXIST:
        print(f"\n🔄 Attempting to restore database {db_id}...")
        
        # Format ID with hyphens for API call (correct UUID format)
        formatted_id = f"{db_id[:8]}-{db_id[8:12]}-{db_id[12:16]}-{db_id[16:20]}-{db_id[20:]}"
        
        success = await restore_database(formatted_id)
        if success:
            restored_count += 1
        else:
            failed_count += 1
    
    print(f"\n" + "=" * 50)
    print(f"📊 RECOVERY SUMMARY:")
    print(f"✅ Successfully restored: {restored_count} databases")
    print(f"❌ Failed to restore: {failed_count} databases")
    print(f"🔍 Total attempts: {len(DATABASES_THAT_SHOULD_EXIST)} databases")
    
    if failed_count > 0:
        print(f"\n⚠️  Some databases couldn't be restored automatically.")
        print(f"   They may have been permanently deleted or need manual recovery.")
        print(f"   Check your Notion trash for any remaining databases.")


if __name__ == "__main__":
    asyncio.run(main())
