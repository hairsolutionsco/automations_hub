"""Tool for Notion API operations."""

import os
import httpx
from typing import Annotated, Any, Optional
from pydantic import BaseModel, Field


class NotionResponse(BaseModel):
    """Response model for Notion API operations."""

    success: bool
    message: str
    data: dict[str, Any] | None = None


class NotionPageResponse(BaseModel):
    """Response model for Notion page operations."""

    success: bool
    page_id: str | None = None
    page_title: str | None = None
    message: str
    data: dict[str, Any] | None = None


async def search_notion(
    query: Annotated[str, Field(description="Search query for Notion content")],
    filter_type: Annotated[Optional[str], Field(description="Filter by type: 'page' or 'database'")] = None
) -> NotionResponse:
    """Search Notion workspace for pages and databases."""
    try:
        api_key = os.getenv("NOTION_API_KEY")
        
        if not api_key:
            return NotionResponse(
                success=False,
                message="NOTION_API_KEY not configured"
            )

        search_payload = {
            "query": query,
        }
        
        if filter_type:
            search_payload["filter"] = {
                "value": filter_type,
                "property": "object"
            }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.notion.com/v1/search",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "Notion-Version": "2022-06-28"
                },
                json=search_payload
            )
            
            if response.status_code == 200:
                search_results = response.json()
                return NotionResponse(
                    success=True,
                    message=f"Found {len(search_results.get('results', []))} results",
                    data=search_results
                )
            else:
                return NotionResponse(
                    success=False,
                    message=f"Notion search failed: {response.status_code} {response.text}"
                )
                
    except Exception as e:
        return NotionResponse(
            success=False,
            message=f"Error searching Notion: {str(e)}"
        )


async def get_notion_page(
    page_id: Annotated[str, Field(description="The ID of the Notion page to retrieve")]
) -> NotionPageResponse:
    """Get details of a specific Notion page."""
    try:
        api_key = os.getenv("NOTION_API_KEY")
        
        if not api_key:
            return NotionPageResponse(
                success=False,
                page_id=page_id,
                message="NOTION_API_KEY not configured"
            )

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.notion.com/v1/pages/{page_id}",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Notion-Version": "2022-06-28"
                }
            )
            
            if response.status_code == 200:
                page_data = response.json()
                page_title = None
                
                # Try to extract page title from properties
                properties = page_data.get("properties", {})
                for prop_name, prop_data in properties.items():
                    if prop_data.get("type") == "title":
                        title_array = prop_data.get("title", [])
                        if title_array:
                            page_title = title_array[0].get("plain_text", "")
                        break
                
                return NotionPageResponse(
                    success=True,
                    page_id=page_id,
                    page_title=page_title,
                    message="Page retrieved successfully",
                    data=page_data
                )
            else:
                return NotionPageResponse(
                    success=False,
                    page_id=page_id,
                    message=f"Failed to fetch page: {response.status_code} {response.text}"
                )
                
    except Exception as e:
        return NotionPageResponse(
            success=False,
            page_id=page_id,
            message=f"Error fetching page: {str(e)}"
        )


async def create_notion_page(
    parent_id: Annotated[str, Field(description="The ID of the parent page or database")],
    title: Annotated[str, Field(description="Title of the new page")],
    content: Annotated[Optional[str], Field(description="Content to add to the page")] = None
) -> NotionPageResponse:
    """Create a new page in Notion."""
    try:
        api_key = os.getenv("NOTION_API_KEY")
        
        if not api_key:
            return NotionPageResponse(
                success=False,
                message="NOTION_API_KEY not configured"
            )

        # Basic page creation payload
        page_data = {
            "parent": {"page_id": parent_id},
            "properties": {
                "title": {
                    "title": [
                        {
                            "text": {
                                "content": title
                            }
                        }
                    ]
                }
            }
        }
        
        # Add content if provided
        if content:
            page_data["children"] = [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": content
                                }
                            }
                        ]
                    }
                }
            ]

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.notion.com/v1/pages",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "Notion-Version": "2022-06-28"
                },
                json=page_data
            )
            
            if response.status_code == 200:
                created_page = response.json()
                return NotionPageResponse(
                    success=True,
                    page_id=created_page.get("id"),
                    page_title=title,
                    message="Page created successfully",
                    data=created_page
                )
            else:
                return NotionPageResponse(
                    success=False,
                    message=f"Failed to create page: {response.status_code} {response.text}"
                )
                
    except Exception as e:
        return NotionPageResponse(
            success=False,
            message=f"Error creating page: {str(e)}"
        )
