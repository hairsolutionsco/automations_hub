#!/usr/bin/env python3
"""
Link Contacts to Hair Orders Profiles by matching names.
This script finds contacts and hair profiles with the same name and creates the relation.
"""

import asyncio
import os
import httpx
from typing import Dict, List, Optional


async def get_database_pages(database_id: str, page_size: int = 100) -> Dict:
    """Get all pages from a database."""
    try:
        api_key = os.getenv("NOTION_API_KEY")
        if not api_key:
            return {"success": False, "message": "NOTION_API_KEY not configured"}

        all_pages = []
        start_cursor = None
        has_more = True

        async with httpx.AsyncClient(timeout=60.0) as client:
            while has_more:
                payload = {"page_size": page_size}
                if start_cursor:
                    payload["start_cursor"] = start_cursor

                response = await client.post(
                    f"https://api.notion.com/v1/databases/{database_id}/query",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                        "Notion-Version": "2022-06-28"
                    },
                    json=payload
                )
                
                if response.status_code != 200:
                    return {
                        "success": False,
                        "message": f"Failed to query database: {response.status_code} {response.text}"
                    }
                
                data = response.json()
                all_pages.extend(data.get("results", []))
                has_more = data.get("has_more", False)
                start_cursor = data.get("next_cursor")

        return {
            "success": True,
            "message": f"Retrieved {len(all_pages)} pages",
            "data": all_pages
        }
                
    except Exception as e:
        return {
            "success": False,
            "message": f"Error querying database: {str(e)}"
        }


async def update_page_relations(page_id: str, property_name: str, related_page_ids: List[str]) -> Dict:
    """Update a page's relation property with the specified page IDs."""
    try:
        api_key = os.getenv("NOTION_API_KEY")
        if not api_key:
            return {"success": False, "message": "NOTION_API_KEY not configured"}

        # Format relation data
        relation_data = [{"id": pid} for pid in related_page_ids]

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.patch(
                f"https://api.notion.com/v1/pages/{page_id}",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "Notion-Version": "2022-06-28"
                },
                json={
                    "properties": {
                        property_name: {
                            "relation": relation_data
                        }
                    }
                }
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "message": f"Successfully updated {property_name} relation"
                }
            else:
                return {
                    "success": False,
                    "message": f"Failed to update relation: {response.status_code} {response.text}"
                }
                
    except Exception as e:
        return {
            "success": False,
            "message": f"Error updating page relation: {str(e)}"
        }


def extract_title(page_properties: Dict) -> str:
    """Extract the title/name from a page's properties."""
    for prop_name, prop_data in page_properties.items():
        if prop_data.get("type") == "title":
            title_array = prop_data.get("title", [])
            if title_array:
                return title_array[0].get("plain_text", "").strip()
    return ""


async def link_contacts_to_hair_profiles():
    """Main function to link contacts to hair profiles by matching names."""
    print("🔗 Linking Contacts to Hair Orders Profiles by Name")
    print("=" * 60)
    
    contacts_db = "226f4e0d-84e0-814c-ad70-d478cebeee30"
    hair_profiles_db = "248f4e0d-84e0-80ad-9d33-e90e5124c092"
    
    # Step 1: Get all contacts
    print("📋 Fetching all contacts...")
    contacts_result = await get_database_pages(contacts_db)
    if not contacts_result["success"]:
        print(f"❌ Failed to get contacts: {contacts_result['message']}")
        return
    
    contacts = contacts_result["data"]
    print(f"✅ Found {len(contacts)} contacts")
    
    # Step 2: Get all hair profiles
    print("💇 Fetching all hair profiles...")
    profiles_result = await get_database_pages(hair_profiles_db)
    if not profiles_result["success"]:
        print(f"❌ Failed to get hair profiles: {profiles_result['message']}")
        return
    
    profiles = profiles_result["data"]
    print(f"✅ Found {len(profiles)} hair profiles")
    
    # Step 3: Create name-to-ID mapping for hair profiles
    print("🗺️  Creating name mapping...")
    profile_name_map = {}
    for profile in profiles:
        name = extract_title(profile["properties"])
        if name:
            profile_name_map[name.lower()] = profile["id"]
    
    print(f"✅ Mapped {len(profile_name_map)} hair profiles by name")
    
    # Step 4: Link contacts to matching hair profiles
    print("\n🔗 Linking contacts to hair profiles...")
    
    matched_count = 0
    updated_count = 0
    errors = []
    
    for contact in contacts:
        contact_name = extract_title(contact["properties"])
        if not contact_name:
            continue
            
        # Look for matching hair profile
        profile_id = profile_name_map.get(contact_name.lower())
        if profile_id:
            print(f"  🎯 Matching: '{contact_name}' -> Hair Profile")
            matched_count += 1
            
            # Update the contact's relation
            result = await update_page_relations(
                page_id=contact["id"],
                property_name="Hair Orders Profiles",
                related_page_ids=[profile_id]
            )
            
            if result["success"]:
                updated_count += 1
                print(f"    ✅ Linked successfully")
            else:
                errors.append(f"'{contact_name}': {result['message']}")
                print(f"    ❌ Failed: {result['message']}")
        else:
            print(f"  ❓ No match found for: '{contact_name}'")
        
        # Small delay to avoid rate limiting
        await asyncio.sleep(0.1)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 LINKING SUMMARY")
    print("=" * 60)
    print(f"👥 Total contacts: {len(contacts)}")
    print(f"💇 Total hair profiles: {len(profiles)}")
    print(f"🎯 Matches found: {matched_count}")
    print(f"✅ Successfully linked: {updated_count}")
    print(f"❌ Errors: {len(errors)}")
    
    if errors:
        print(f"\n❌ Errors encountered:")
        for error in errors[:10]:  # Show first 10 errors
            print(f"  • {error}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more")
    
    print(f"\n🎉 Linking complete! {updated_count} contacts now linked to hair profiles.")


if __name__ == "__main__":
    asyncio.run(link_contacts_to_hair_profiles())
