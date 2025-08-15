#!/usr/bin/env python3
"""
Notion Relation Fields Setup Guide
Based on Canonical Schema v1

This script creates all the relation fields required for the canonical schema.
"""

import asyncio
import sys
sys.path.append('/workspaces/automations_hub/notion')
from create_relation_properties import create_multiple_relations

# Database IDs from your workspace
DATABASE_IDS = {
    "companies": "22bf4e0d-84e0-80bb-8d1c-c90710d44870",
    "contacts": "226f4e0d-84e0-814c-ad70-d478cebeee30", 
    "hair_profiles": "248f4e0d-84e0-80ad-9d33-e90e5124c092",  # Hair Orders Profiles
    "deals": "226f4e0d-84e0-808c-af51-e09c154008db",
    "plans": "228f4e0d-84e0-815c-a108-e48054988ac0",
    "orders": "228f4e0d-84e0-816f-8511-fab726d2c6ef",
    "purchase_orders": "237f4e0d-84e0-807b-860c-cb9599ddaea0",
    "payments": "228f4e0d-84e0-81ba-b2c1-d0deaff9b8c9",  # Incomes -> hs_payments
    "expenses": "226f4e0d-84e0-8158-a8ce-dc0b8bbabfce",
    "suppliers_inventory": "226f4e0d-84e0-814f-a468-d44302ee0478"
}

# Complete relation configuration from canonical schema
CANONICAL_RELATIONS = [
    # =================================================================
    # CORE BUSINESS RELATIONS (High Priority - Create These First)
    # =================================================================
    
    # Companies Relations
    {
        "source_db_id": DATABASE_IDS["companies"],
        "property_name": "Associated Orders",
        "target_db_id": DATABASE_IDS["orders"],
        "is_dual_property": True,
        "priority": 1,
        "description": "Companies (B2B clients) to their Orders"
    },
    {
        "source_db_id": DATABASE_IDS["companies"], 
        "property_name": "Associated POs",
        "target_db_id": DATABASE_IDS["purchase_orders"],
        "is_dual_property": True,
        "priority": 1,
        "description": "Companies (Suppliers) to Purchase Orders"
    },
    
    # Contacts Core Relations
    {
        "source_db_id": DATABASE_IDS["contacts"],
        "property_name": "Associated Deals",
        "target_db_id": DATABASE_IDS["deals"],
        "is_dual_property": True,
        "priority": 1,
        "description": "Contacts to their Deals"
    },
    {
        "source_db_id": DATABASE_IDS["contacts"],
        "property_name": "Associated Orders", 
        "target_db_id": DATABASE_IDS["orders"],
        "is_dual_property": True,
        "priority": 1,
        "description": "Contacts to their Orders"
    },
    {
        "source_db_id": DATABASE_IDS["contacts"],
        "property_name": "Associated Plans",
        "target_db_id": DATABASE_IDS["plans"], 
        "is_dual_property": True,
        "priority": 1,
        "description": "Contacts to their Subscription Plans"
    },
    {
        "source_db_id": DATABASE_IDS["contacts"],
        "property_name": "Hair Orders Profiles",
        "target_db_id": DATABASE_IDS["hair_profiles"],
        "is_dual_property": True,
        "priority": 1,
        "description": "Contacts to their Hair Profiles (1:1 relationship)"
    },
    
    # Hair Profiles Relations  
    {
        "source_db_id": DATABASE_IDS["hair_profiles"],
        "property_name": "Associated Contact",
        "target_db_id": DATABASE_IDS["contacts"],
        "is_dual_property": True,
        "priority": 1,
        "description": "Hair Profile to Contact (1:1)"
    },
    {
        "source_db_id": DATABASE_IDS["hair_profiles"],
        "property_name": "Associated Orders",
        "target_db_id": DATABASE_IDS["orders"],
        "is_dual_property": True,
        "priority": 1,
        "description": "Hair Profile to Orders using this profile"
    },
    
    # Deals Core Relations
    {
        "source_db_id": DATABASE_IDS["deals"],
        "property_name": "Associated Client",
        "target_db_id": DATABASE_IDS["contacts"],
        "is_dual_property": True,
        "priority": 1,
        "description": "Deals to their Client (Contact)"
    },
    {
        "source_db_id": DATABASE_IDS["deals"],
        "property_name": "Associated Orders",
        "target_db_id": DATABASE_IDS["orders"],
        "is_dual_property": True,
        "priority": 1,
        "description": "Deals to Orders fulfilling the deal"
    },
    {
        "source_db_id": DATABASE_IDS["deals"],
        "property_name": "Associated Plan",
        "target_db_id": DATABASE_IDS["plans"],
        "is_dual_property": True,
        "priority": 1,
        "description": "Deals to Subscription Plans (if applicable)"
    },
    
    # Plans Core Relations
    {
        "source_db_id": DATABASE_IDS["plans"],
        "property_name": "Associated Client",
        "target_db_id": DATABASE_IDS["contacts"],
        "is_dual_property": True,
        "priority": 1,
        "description": "Plans to their Client"
    },
    {
        "source_db_id": DATABASE_IDS["plans"],
        "property_name": "Associated Deal",
        "target_db_id": DATABASE_IDS["deals"],
        "is_dual_property": True,
        "priority": 1,
        "description": "Plans to their originating Deal"
    },
    
    # Orders Core Relations
    {
        "source_db_id": DATABASE_IDS["orders"],
        "property_name": "Associated Deal",
        "target_db_id": DATABASE_IDS["deals"],
        "is_dual_property": True,
        "priority": 1,
        "description": "Orders to their source Deal"
    },
    {
        "source_db_id": DATABASE_IDS["orders"],
        "property_name": "Client",
        "target_db_id": DATABASE_IDS["contacts"],
        "is_dual_property": True,
        "priority": 1,
        "description": "Orders to their Client (Contact)"
    },
    {
        "source_db_id": DATABASE_IDS["orders"],
        "property_name": "Related Hair Profile",
        "target_db_id": DATABASE_IDS["hair_profiles"],
        "is_dual_property": True,
        "priority": 1,
        "description": "Orders to Hair Profile specs used"
    },
    {
        "source_db_id": DATABASE_IDS["orders"],
        "property_name": "Associated PO",
        "target_db_id": DATABASE_IDS["purchase_orders"],
        "is_dual_property": True,
        "priority": 1,
        "description": "Orders to their Purchase Orders (1:*)"
    },
    {
        "source_db_id": DATABASE_IDS["orders"],
        "property_name": "Associated Companies",
        "target_db_id": DATABASE_IDS["companies"],
        "is_dual_property": True,
        "priority": 1,
        "description": "Orders to B2B Client Companies (optional)"
    },
    
    # Purchase Orders Core Relations
    {
        "source_db_id": DATABASE_IDS["purchase_orders"],
        "property_name": "Associated Order",
        "target_db_id": DATABASE_IDS["orders"],
        "is_dual_property": True,
        "priority": 1,
        "description": "POs to their parent Order"
    },
    {
        "source_db_id": DATABASE_IDS["purchase_orders"],
        "property_name": "Associated Deal",
        "target_db_id": DATABASE_IDS["deals"],
        "is_dual_property": True,
        "priority": 1,
        "description": "POs to context Deal"
    },
    {
        "source_db_id": DATABASE_IDS["purchase_orders"],
        "property_name": "Client",
        "target_db_id": DATABASE_IDS["contacts"],
        "is_dual_property": True,
        "priority": 1,
        "description": "POs to end customer Contact"
    },
    {
        "source_db_id": DATABASE_IDS["purchase_orders"],
        "property_name": "Associated Companies",
        "target_db_id": DATABASE_IDS["companies"],
        "is_dual_property": True,
        "priority": 1,
        "description": "POs to Supplier Company"
    },
    {
        "source_db_id": DATABASE_IDS["purchase_orders"],
        "property_name": "Inventory Product",
        "target_db_id": DATABASE_IDS["suppliers_inventory"],
        "is_dual_property": True,
        "priority": 2,
        "description": "POs to Inventory/SKU items"
    },
    
    # =================================================================
    # PAYMENTS RELATIONS (New - High Priority for Finance)
    # =================================================================
    
    {
        "source_db_id": DATABASE_IDS["payments"],
        "property_name": "Related Deal",
        "target_db_id": DATABASE_IDS["deals"],
        "is_dual_property": True,
        "priority": 1,
        "description": "Payments to Deals (0..1 mapping)"
    },
    {
        "source_db_id": DATABASE_IDS["payments"],
        "property_name": "Related Order",
        "target_db_id": DATABASE_IDS["orders"],
        "is_dual_property": True,
        "priority": 1,
        "description": "Payments to Orders (0..1 mapping for reconciliation)"
    },
    {
        "source_db_id": DATABASE_IDS["payments"],
        "property_name": "Related Plan",
        "target_db_id": DATABASE_IDS["plans"],
        "is_dual_property": True,
        "priority": 1,
        "description": "Payments to Plans (subscription payments)"
    },
    {
        "source_db_id": DATABASE_IDS["payments"],
        "property_name": "Contact",
        "target_db_id": DATABASE_IDS["contacts"],
        "is_dual_property": True,
        "priority": 1,
        "description": "Payments to Contact (payer)"
    },
    
    # =================================================================
    # EXISTING RELATIONS TO PRESERVE (Priority 3 - Don't recreate if exist)
    # =================================================================
    
    {
        "source_db_id": DATABASE_IDS["expenses"],
        "property_name": "Categories",
        "target_db_id": "226f4e0d-84e0-814a-892f-e11dcc5e6e77",  # Expense Categories
        "is_dual_property": True,
        "priority": 3,
        "description": "Expenses to Categories (existing)"
    },
    {
        "source_db_id": DATABASE_IDS["expenses"],
        "property_name": "Month",
        "target_db_id": "226f4e0d-84e0-8134-958b-d1dc80f5e72e",  # Months
        "is_dual_property": True,
        "priority": 3,
        "description": "Expenses to Month periods (existing)"
    }
]

async def create_canonical_relations():
    """Create all canonical relations in priority order."""
    print("🔗 Creating Canonical Schema Relations")
    print("=" * 50)
    
    # Group by priority
    priority_groups = {}
    for rel in CANONICAL_RELATIONS:
        priority = rel.get("priority", 2)
        if priority not in priority_groups:
            priority_groups[priority] = []
        priority_groups[priority].append(rel)
    
    # Execute by priority
    all_results = []
    for priority in sorted(priority_groups.keys()):
        print(f"\n🎯 Priority {priority} Relations:")
        print("-" * 30)
        
        relations = priority_groups[priority]
        for rel in relations:
            print(f"  • {rel['description']}")
        
        results = await create_multiple_relations(relations)
        all_results.extend(results)
        
        # Small delay between priority groups
        if priority < max(priority_groups.keys()):
            print("⏳ Waiting before next priority group...")
            await asyncio.sleep(2)
    
    # Summary Report
    print("\n" + "=" * 50)
    print("📊 FINAL SUMMARY")
    print("=" * 50)
    
    success_count = sum(1 for r in all_results if r["result"]["success"])
    total_count = len(all_results)
    
    print(f"✅ Successful: {success_count}/{total_count}")
    print(f"❌ Failed: {total_count - success_count}/{total_count}")
    
    if total_count - success_count > 0:
        print("\n❌ Failed Relations:")
        for result in all_results:
            if not result["result"]["success"]:
                config = result["config"]
                print(f"  • {config['description']}: {result['result']['message']}")
    
    print("\n🎉 Canonical Schema Relations Setup Complete!")
    return all_results

async def setup_phase_1_critical():
    """Set up only the most critical relations first (Priority 1)."""
    critical_relations = [rel for rel in CANONICAL_RELATIONS if rel.get("priority", 2) == 1]
    
    print("🚀 Setting up Phase 1: Critical Relations Only")
    print("=" * 50)
    print(f"Creating {len(critical_relations)} critical relations...")
    
    results = await create_multiple_relations(critical_relations)
    
    success_count = sum(1 for r in results if r["result"]["success"])
    print(f"\n✅ Phase 1 Complete: {success_count}/{len(critical_relations)} successful")
    
    return results

if __name__ == "__main__":
    print("🔗 Notion Canonical Schema Relations Setup")
    print("=" * 50)
    print("Choose setup mode:")
    print("1. Full setup (all relations)")
    print("2. Phase 1 only (critical relations)")
    print("3. Show relation plan (no execution)")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        asyncio.run(create_canonical_relations())
    elif choice == "2":
        asyncio.run(setup_phase_1_critical())
    elif choice == "3":
        print("\n📋 Canonical Relations Plan:")
        for i, rel in enumerate(CANONICAL_RELATIONS, 1):
            priority = rel.get("priority", 2)
            print(f"{i:2d}. [P{priority}] {rel['description']}")
        print(f"\nTotal: {len(CANONICAL_RELATIONS)} relations to create")
    else:
        print("Invalid choice. Exiting.")
