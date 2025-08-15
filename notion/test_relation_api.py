#!/usr/bin/env python3
"""Simple test to verify Notion API connection and relation creation capability."""

import asyncio
import os
import sys
sys.path.append('/workspaces/automations_hub/notion')
from create_relation_properties import create_relation_property, get_notion_database

async def test_api_connection():
    """Test basic Notion API connectivity."""
    print("🔍 Testing Notion API Connection...")
    
    # Test with the Orders database
    orders_db_id = "228f4e0d-84e0-816f-8511-fab726d2c6ef"
    
    result = await get_notion_database(orders_db_id)
    
    if result["success"]:
        print("✅ API Connection successful!")
        print(f"📊 Database: {result['data']['title'][0]['plain_text']}")
        print(f"🔢 Properties: {len(result['data']['properties'])}")
        return True
    else:
        print(f"❌ API Connection failed: {result['message']}")
        return False

async def test_relation_creation():
    """Test creating a simple relation (safe test)."""
    print("\n🧪 Testing Relation Creation...")
    
    # Use Orders database instead (more stable)
    orders_db = "228f4e0d-84e0-816f-8511-fab726d2c6ef"
    contacts_db = "226f4e0d-84e0-814c-ad70-d478cebeee30"
    
    result = await create_relation_property(
        database_id=orders_db,
        property_name="TEST - Client Contact",
        related_database_id=contacts_db,
        is_dual_property=True
    )
    
    if result["success"]:
        print("✅ Test relation created successfully!")
        print("🗑️  Remember to delete this test relation manually if not needed")
        return True
    else:
        if "already exists" in result["message"]:
            print("ℹ️  Test relation already exists (that's fine)")
            return True
        else:
            print(f"❌ Test relation creation failed: {result['message']}")
            return False

async def main():
    """Run all tests."""
    print("🚀 Notion Relation API Tests")
    print("=" * 40)
    
    # Test 1: API Connection
    api_ok = await test_api_connection()
    
    if not api_ok:
        print("\n❌ API connection failed. Check NOTION_API_KEY environment variable.")
        return
    
    # Test 2: Relation Creation
    relation_ok = await test_relation_creation()
    
    print("\n" + "=" * 40)
    if api_ok and relation_ok:
        print("🎉 All tests passed! Ready to create canonical relations.")
        print("\nNext steps:")
        print("1. Run: python setup_canonical_relations.py")
        print("2. Choose option 3 to see the full plan")
        print("3. Choose option 2 for critical relations first")
        print("4. Choose option 1 for full setup")
    else:
        print("❌ Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    asyncio.run(main())
