#!/usr/bin/env python3
"""Script to create relation properties in Notion databases via API."""

import asyncio
import os
import sys
import httpx
from typing import Dict, List, Optional


async def get_notion_database(database_id: str) -> Dict:
    """Get details of a specific Notion database."""
    try:
        api_key = os.getenv("NOTION_API_KEY")
        
        if not api_key:
            return {
                "success": False,
                "message": "NOTION_API_KEY not configured"
            }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"https://api.notion.com/v1/databases/{database_id}",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Notion-Version": "2022-06-28"
                }
            )
            
            if response.status_code == 200:
                database_data = response.json()
                return {
                    "success": True,
                    "message": "Database retrieved successfully",
                    "data": database_data
                }
            else:
                return {
                    "success": False,
                    "message": f"Failed to fetch database: {response.status_code} {response.text}"
                }
                
    except Exception as e:
        return {
            "success": False,
            "message": f"Error fetching database: {str(e)}"
        }


async def create_relation_property(
    database_id: str,
    property_name: str,
    related_database_id: str,
    is_dual_property: bool = True
) -> Dict:
    """
    Create a relation property in a Notion database.
    
    Args:
        database_id: ID of the database to add the property to
        property_name: Name of the new relation property
        related_database_id: ID of the database to relate to
        is_dual_property: Whether to create bidirectional relation (default: True)
    
    Returns:
        Dict with success status and response data
    """
    try:
        api_key = os.getenv("NOTION_API_KEY")
        
        if not api_key:
            return {
                "success": False,
                "message": "NOTION_API_KEY not configured"
            }

        # First, get the current database to see existing properties
        db_response = await get_notion_database(database_id)
        if not db_response["success"]:
            return {
                "success": False,
                "message": f"Could not retrieve database: {db_response['message']}"
            }

        current_properties = db_response["data"].get("properties", {})
        
        # Check if property already exists
        if property_name in current_properties:
            return {
                "success": False,
                "message": f"Property '{property_name}' already exists in database"
            }

        # Create the new relation property
        if is_dual_property:
            new_property = {
                property_name: {
                    "type": "relation",
                    "relation": {
                        "database_id": related_database_id,
                        "dual_property": {}
                    }
                }
            }
        else:
            new_property = {
                property_name: {
                    "type": "relation", 
                    "relation": {
                        "database_id": related_database_id,
                        "single_property": {}
                    }
                }
            }

        # Merge with existing properties
        updated_properties = {**current_properties, **new_property}

        # Update the database with the new property
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.patch(
                f"https://api.notion.com/v1/databases/{database_id}",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "Notion-Version": "2022-06-28"
                },
                json={
                    "properties": updated_properties
                }
            )
            
            if response.status_code == 200:
                response_data = response.json()
                return {
                    "success": True,
                    "message": f"Successfully created relation property '{property_name}'",
                    "data": response_data
                }
            else:
                return {
                    "success": False,
                    "message": f"Failed to create property: {response.status_code} - {response.text}"
                }
                
    except Exception as e:
        return {
            "success": False,
            "message": f"Error creating relation property: {str(e)}"
        }


async def create_multiple_relations(relations_config: List[Dict]) -> List[Dict]:
    """
    Create multiple relation properties from a configuration list.
    
    Args:
        relations_config: List of dicts with keys: 
            - source_db_id
            - property_name  
            - target_db_id
            - is_dual_property (optional, default True)
    
    Returns:
        List of results for each relation creation attempt
    """
    results = []
    
    for config in relations_config:
        print(f"Creating relation: {config['property_name']} in {config['source_db_id'][:8]}...")
        
        result = await create_relation_property(
            database_id=config["source_db_id"],
            property_name=config["property_name"],
            related_database_id=config["target_db_id"],
            is_dual_property=config.get("is_dual_property", True)
        )
        
        results.append({
            "config": config,
            "result": result
        })
        
        if result["success"]:
            print(f"✅ {result['message']}")
        else:
            print(f"❌ {result['message']}")
        
        # Small delay to avoid rate limiting
        await asyncio.sleep(0.5)
    
    return results


async def test_create_relation():
    """Test function to create a sample relation."""
    # Example: Create a relation from Orders to Clients
    relations_to_create = [
        {
            "source_db_id": "228f4e0d-84e0-816f-8511-fab726d2c6ef",  # Orders
            "property_name": "Test Client Relation",
            "target_db_id": "226f4e0d-84e0-814c-ad70-d478cebeee30",  # Contacts/Clients
            "is_dual_property": True
        }
    ]
    
    results = await create_multiple_relations(relations_to_create)
    
    print("\n📊 Results Summary:")
    for i, result in enumerate(results):
        config = result["config"]
        status = "✅ Success" if result["result"]["success"] else "❌ Failed"
        print(f"{i+1}. {config['property_name']}: {status}")


if __name__ == "__main__":
    print("🔗 Notion Relation Property Creator")
    print("===================================")
    
    # Uncomment to test
    # asyncio.run(test_create_relation())
    
    print("Ready to create relation properties!")
    print("Use create_relation_property() or create_multiple_relations() functions.")
