"""Simple recovery script with proper UUID formatting."""

import asyncio
import sys
import os
sys.path.append('.')
import httpx


async def restore_database_simple(database_id: str) -> bool:
    """Restore an archived database with proper UUID formatting."""
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
            elif response.status_code == 404:
                print(f"⚠️ Database {database_id} not found (may already be active or permanently deleted)")
                return False
            else:
                print(f"❌ Failed to restore database {database_id}: {response.status_code} {response.text}")
                return False
                
    except Exception as e:
        print(f"❌ Error restoring database {database_id}: {str(e)}")
        return False


def format_uuid(uuid_without_hyphens: str) -> str:
    """Format a UUID string by adding hyphens in the correct positions."""
    if len(uuid_without_hyphens) != 32:
        return uuid_without_hyphens  # Return as-is if not 32 characters
    
    return f"{uuid_without_hyphens[:8]}-{uuid_without_hyphens[8:12]}-{uuid_without_hyphens[12:16]}-{uuid_without_hyphens[16:20]}-{uuid_without_hyphens[20:]}"


async def main():
    """Simple recovery function."""
    print("🚨 SIMPLIFIED DATABASE RECOVERY")
    print("=" * 50)
    
    # Database IDs from markdown (without hyphens)
    databases_from_md = [
        "22bf4e0d84e080bb8d1cc90710d44870",  # Companies
        "226f4e0d84e0814cad70d478cebeee30",  # Contacts  
        "248f4e0d84e080ad9d33e90e5124c092",  # Hair Orders Profiles
        "228f4e0d84e08185a49dc68df1c94301",  # Emails
        "231f4e0d84e080a9a8d3cbc04da25dcb",  # Email Templates
        "238f4e0d84e080f9b09febe986c6cf2a",  # Customer Portal Data
        "226f4e0d84e0808caf51e09c154008db",  # Deals
        "228f4e0d84e0815ca108e48054988ac0",  # Plans
        "228f4e0d84e0816f8511fab726d2c6ef",  # Orders
        "237f4e0d84e0807b860ccb9599ddaea0",  # Purchase Orders
        "226f4e0d84e0814fa468d44302ee0478",  # Suppliers Inventory
        "226f4e0d84e0819dbe89db73c48eaee4",  # Ad Campaigns
        "226f4e0d84e081aaa79cffad8081015e",  # Platform
        "226f4e0d84e0816aac2ff089654d45fc",  # Content
        "42cf7bf51b0b446ea2e06dc851db6092",  # Blog Posts
        "22af4e0d84e080c3a7d6f0209d93081d",  # Payments
        "229f4e0d84e08128a0bfd7631b6aa22d",  # Incomes
        "226f4e0d84e0817e84e2c9a983663070",  # Expenses
        "226f4e0d84e0813fb2e9d228f70676b9",  # Recurring Expenses
        "22cf4e0d84e0802abf76e564658fdc5f",  # Forecasted Payments
        "232f4e0d84e080c6a565ebc67a43ffa5",  # Forecasted Income
        "226f4e0d84e081d9b998e61ecae5c421",  # Income Sources
        "226f4e0d84e081a9a37bfc2aabd167c8",  # Expense Categories
        "226f4e0d84e081dea364fe70d608f59f",  # Expense Sources
        "226f4e0d84e081308a9cce4a29ef7a35",  # Debt Tracking
        "226f4e0d84e08171aea1d054e8cb0786",  # Debt Overview
        "226f4e0d84e08187bcb1c1290226a0a2",  # Budget Split 50/20/30
        "226f4e0d84e081de90acdd1c31b77f07",  # Accounts and Goals
        "226f4e0d84e081bc9ea0d326c752ea42",  # Transfers
        "226f4e0d84e0816da749e741b1ac0b30",  # Business Projects
        "226f4e0d84e081688718d8f6b2d1fe3d",  # Tasks
        "22cf4e0d84e08036a313f6cfa1fa9801",  # Daily Reports
        "226f4e0d84e0810181e1c9f2d6803291",  # Monthly Reports (Main)
        "226f4e0d84e0817998cbcca8ecbf0c15",  # Yearly Reports
        "226f4e0d84e081f188a5f0eb2eb1bd87",  # Objectives
        "226f4e0d84e0815fb434c1a6e3a28e16",  # Key Results
        "232f4e0d84e08049abb0d5c04fa1628c",  # Hubspot Properties Management
        "226f4e0d84e08135a4f7ee34b04fe01b",  # Business Resources
        "232f4e0d84e08000aad7de8ff9504fd1",  # Products & Pricing Catalog
        "239f4e0d84e08017b600d74cfcaa3551",  # Plan Pricing
    ]
    
    restored_count = 0
    failed_count = 0
    not_found_count = 0
    
    for db_id in databases_from_md:
        # Format with hyphens
        formatted_id = format_uuid(db_id)
        print(f"\n🔄 Restoring: {formatted_id}")
        
        success = await restore_database_simple(formatted_id)
        if success:
            restored_count += 1
        else:
            failed_count += 1
    
    print(f"\n" + "=" * 50)
    print(f"📊 RECOVERY SUMMARY:")
    print(f"✅ Successfully restored: {restored_count} databases")
    print(f"❌ Failed to restore: {failed_count} databases")
    print(f"📝 Total attempts: {len(databases_from_md)} databases")


if __name__ == "__main__":
    asyncio.run(main())
