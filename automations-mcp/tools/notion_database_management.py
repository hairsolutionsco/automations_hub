"""Extended Notion API tools for database management and reorganization."""

import os
import httpx
from typing import Annotated, Any, Optional, List
from pydantic import BaseModel, Field


class DatabaseResponse(BaseModel):
    """Response model for database operations."""
    success: bool
    database_id: str | None = None
    message: str
    data: dict[str, Any] | None = None


class PageBlocksResponse(BaseModel):
    """Response model for page blocks operations."""
    success: bool
    message: str
    blocks: List[dict[str, Any]] = []


async def get_notion_database(
    database_id: Annotated[str, Field(description="The ID of the database to retrieve")]
) -> DatabaseResponse:
    """Get details of a specific Notion database."""
    try:
        api_key = os.getenv("NOTION_API_KEY")
        
        if not api_key:
            return DatabaseResponse(
                success=False,
                database_id=database_id,
                message="NOTION_API_KEY not configured"
            )

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.notion.com/v1/databases/{database_id}",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Notion-Version": "2022-06-28"
                }
            )
            
            if response.status_code == 200:
                database_data = response.json()
                return DatabaseResponse(
                    success=True,
                    database_id=database_id,
                    message="Database retrieved successfully",
                    data=database_data
                )
            else:
                return DatabaseResponse(
                    success=False,
                    database_id=database_id,
                    message=f"Failed to fetch database: {response.status_code} {response.text}"
                )
                
    except Exception as e:
        return DatabaseResponse(
            success=False,
            database_id=database_id,
            message=f"Error fetching database: {str(e)}"
        )


async def archive_notion_database(
    database_id: Annotated[str, Field(description="The ID of the database to archive/delete")]
) -> DatabaseResponse:
    """Archive (soft delete) a Notion database."""
    try:
        api_key = os.getenv("NOTION_API_KEY")
        
        if not api_key:
            return DatabaseResponse(
                success=False,
                database_id=database_id,
                message="NOTION_API_KEY not configured"
            )

        async with httpx.AsyncClient() as client:
            response = await client.patch(
                f"https://api.notion.com/v1/databases/{database_id}",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "Notion-Version": "2022-06-28"
                },
                json={"archived": True}
            )
            
            if response.status_code == 200:
                return DatabaseResponse(
                    success=True,
                    database_id=database_id,
                    message="Database archived successfully"
                )
            else:
                return DatabaseResponse(
                    success=False,
                    database_id=database_id,
                    message=f"Failed to archive database: {response.status_code} {response.text}"
                )
                
    except Exception as e:
        return DatabaseResponse(
            success=False,
            database_id=database_id,
            message=f"Error archiving database: {str(e)}"
        )


async def get_page_blocks(
    page_id: Annotated[str, Field(description="The ID of the page to get blocks from")]
) -> PageBlocksResponse:
    """Get all blocks from a Notion page."""
    try:
        api_key = os.getenv("NOTION_API_KEY")
        
        if not api_key:
            return PageBlocksResponse(
                success=False,
                message="NOTION_API_KEY not configured"
            )

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.notion.com/v1/blocks/{page_id}/children",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Notion-Version": "2022-06-28"
                }
            )
            
            if response.status_code == 200:
                blocks_data = response.json()
                return PageBlocksResponse(
                    success=True,
                    message="Page blocks retrieved successfully",
                    blocks=blocks_data.get("results", [])
                )
            else:
                return PageBlocksResponse(
                    success=False,
                    message=f"Failed to fetch page blocks: {response.status_code} {response.text}"
                )
                
    except Exception as e:
        return PageBlocksResponse(
            success=False,
            message=f"Error fetching page blocks: {str(e)}"
        )


async def update_page_blocks(
    page_id: Annotated[str, Field(description="The ID of the page to update")],
    blocks: Annotated[List[dict], Field(description="List of blocks to add to the page")]
) -> PageBlocksResponse:
    """Update page blocks with new structure."""
    try:
        api_key = os.getenv("NOTION_API_KEY")
        
        if not api_key:
            return PageBlocksResponse(
                success=False,
                message="NOTION_API_KEY not configured"
            )

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
                return PageBlocksResponse(
                    success=True,
                    message="Page blocks updated successfully"
                )
            else:
                return PageBlocksResponse(
                    success=False,
                    message=f"Failed to update page blocks: {response.status_code} {response.text}"
                )
                
    except Exception as e:
        return PageBlocksResponse(
            success=False,
            message=f"Error updating page blocks: {str(e)}"
        )


async def query_database_records(
    database_id: Annotated[str, Field(description="The ID of the database to query")]
) -> DatabaseResponse:
    """Query records from a database to check if it's empty or has data."""
    try:
        api_key = os.getenv("NOTION_API_KEY")
        
        if not api_key:
            return DatabaseResponse(
                success=False,
                database_id=database_id,
                message="NOTION_API_KEY not configured"
            )

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://api.notion.com/v1/databases/{database_id}/query",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "Notion-Version": "2022-06-28"
                },
                json={"page_size": 1}  # Just check if there are any records
            )
            
            if response.status_code == 200:
                query_data = response.json()
                record_count = len(query_data.get("results", []))
                has_more = query_data.get("has_more", False)
                
                return DatabaseResponse(
                    success=True,
                    database_id=database_id,
                    message=f"Database query successful. Records found: {record_count}",
                    data={
                        "record_count": record_count,
                        "has_more": has_more,
                        "results": query_data.get("results", [])
                    }
                )
            else:
                return DatabaseResponse(
                    success=False,
                    database_id=database_id,
                    message=f"Failed to query database: {response.status_code} {response.text}"
                )
                
    except Exception as e:
        return DatabaseResponse(
            success=False,
            database_id=database_id,
            message=f"Error querying database: {str(e)}"
        )


export = get_notion_database
