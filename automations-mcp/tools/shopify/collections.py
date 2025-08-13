"""Shopify API tools for collection management."""

import os
import httpx
from typing import Annotated, Any, Optional, List, Dict
from pydantic import BaseModel, Field


class CollectionResponse(BaseModel):
    """Response model for collection operations."""
    success: bool
    data: Optional[Dict[str, Any]] = None
    message: str
    collections: Optional[List[Dict[str, Any]]] = None


async def create_shopify_collection(
    title: Annotated[str, Field(description="Collection title")],
    description: Annotated[str, Field(description="Collection description")] = "",
    published: Annotated[bool, Field(description="Whether collection is published")] = False
) -> CollectionResponse:
    """Create a new collection in Shopify store."""
    
    shopify_url = os.getenv("SHOPIFY_STORE_URL")
    shopify_token = os.getenv("SHOPIFY_ACCESS_TOKEN")
    
    if not shopify_url or not shopify_token:
        return CollectionResponse(
            success=False,
            message="Missing SHOPIFY_STORE_URL or SHOPIFY_ACCESS_TOKEN environment variables"
        )
    
    url = f"{shopify_url}/admin/api/2023-10/smart_collections.json"
    headers = {
        "X-Shopify-Access-Token": shopify_token,
        "Content-Type": "application/json"
    }
    
    collection_data = {
        "smart_collection": {
            "title": title,
            "body_html": description,
            "published": published
        }
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, headers=headers, json=collection_data)
            response.raise_for_status()
            
            data = response.json()
            return CollectionResponse(
                success=True,
                data=data.get("smart_collection", {}),
                message=f"Created collection: {title}"
            )
            
    except httpx.HTTPStatusError as e:
        return CollectionResponse(
            success=False,
            message=f"HTTP error {e.response.status_code}: {e.response.text}"
        )
    except Exception as e:
        return CollectionResponse(
            success=False,
            message=f"Error creating collection: {str(e)}"
        )


async def update_shopify_collection(
    collection_id: Annotated[str, Field(description="Collection ID to update")],
    title: Annotated[Optional[str], Field(description="New collection title")] = None,
    description: Annotated[Optional[str], Field(description="New collection description")] = None,
    published: Annotated[Optional[bool], Field(description="Whether collection is published")] = None
) -> CollectionResponse:
    """Update an existing collection in Shopify store."""
    
    shopify_url = os.getenv("SHOPIFY_STORE_URL")
    shopify_token = os.getenv("SHOPIFY_ACCESS_TOKEN")
    
    if not shopify_url or not shopify_token:
        return CollectionResponse(
            success=False,
            message="Missing SHOPIFY_STORE_URL or SHOPIFY_ACCESS_TOKEN environment variables"
        )
    
    url = f"{shopify_url}/admin/api/2023-10/smart_collections/{collection_id}.json"
    headers = {
        "X-Shopify-Access-Token": shopify_token,
        "Content-Type": "application/json"
    }
    
    update_data = {}
    if title is not None:
        update_data["title"] = title
    if description is not None:
        update_data["body_html"] = description
    if published is not None:
        update_data["published"] = published
    
    if not update_data:
        return CollectionResponse(
            success=False,
            message="No update data provided"
        )
    
    collection_data = {"smart_collection": update_data}
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.put(url, headers=headers, json=collection_data)
            response.raise_for_status()
            
            data = response.json()
            return CollectionResponse(
                success=True,
                data=data.get("smart_collection", {}),
                message=f"Updated collection: {collection_id}"
            )
            
    except httpx.HTTPStatusError as e:
        return CollectionResponse(
            success=False,
            message=f"HTTP error {e.response.status_code}: {e.response.text}"
        )
    except Exception as e:
        return CollectionResponse(
            success=False,
            message=f"Error updating collection: {str(e)}"
        )
