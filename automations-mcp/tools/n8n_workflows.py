"""Tool for managing n8n workflows."""

import os
import httpx
from typing import Annotated, Any, Optional
from pydantic import BaseModel, Field


class WorkflowListResponse(BaseModel):
    """Response model for listing n8n workflows."""

    workflows: list[dict[str, Any]]
    count: int
    message: str | None = None


class WorkflowResponse(BaseModel):
    """Response model for n8n workflow operations."""

    success: bool
    workflow_id: str | None = None
    workflow_name: str | None = None
    message: str
    data: dict[str, Any] | None = None


async def list_n8n_workflows() -> WorkflowListResponse:
    """List all workflows from n8n Cloud instance."""
    try:
        # Get environment variables
        n8n_url = os.getenv("N8N_CLOUD_INSTANCE_URL")
        api_key = os.getenv("N8N_API_KEY")
        
        if not n8n_url or not api_key:
            return WorkflowListResponse(
                workflows=[],
                count=0,
                message="N8N_CLOUD_INSTANCE_URL or N8N_API_KEY not configured"
            )

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{n8n_url}/api/v1/workflows",
                headers={
                    "X-N8N-API-KEY": api_key,
                    "Accept": "application/json"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                workflows = data.get("data", [])
                return WorkflowListResponse(
                    workflows=workflows,
                    count=len(workflows),
                    message=f"Successfully retrieved {len(workflows)} workflows"
                )
            else:
                return WorkflowListResponse(
                    workflows=[],
                    count=0,
                    message=f"Failed to fetch workflows: {response.status_code} {response.text}"
                )
                
    except Exception as e:
        return WorkflowListResponse(
            workflows=[],
            count=0,
            message=f"Error fetching workflows: {str(e)}"
        )


async def get_n8n_workflow(
    workflow_id: Annotated[str, Field(description="The ID of the workflow to retrieve")]
) -> WorkflowResponse:
    """Get details of a specific n8n workflow."""
    try:
        n8n_url = os.getenv("N8N_CLOUD_INSTANCE_URL")
        api_key = os.getenv("N8N_API_KEY")
        
        if not n8n_url or not api_key:
            return WorkflowResponse(
                success=False,
                workflow_id=workflow_id,
                message="N8N_CLOUD_INSTANCE_URL or N8N_API_KEY not configured"
            )

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{n8n_url}/api/v1/workflows/{workflow_id}",
                headers={
                    "X-N8N-API-KEY": api_key,
                    "Accept": "application/json"
                }
            )
            
            if response.status_code == 200:
                workflow_data = response.json()
                return WorkflowResponse(
                    success=True,
                    workflow_id=workflow_id,
                    workflow_name=workflow_data.get("name"),
                    message="Workflow retrieved successfully",
                    data=workflow_data
                )
            else:
                return WorkflowResponse(
                    success=False,
                    workflow_id=workflow_id,
                    message=f"Failed to fetch workflow: {response.status_code} {response.text}"
                )
                
    except Exception as e:
        return WorkflowResponse(
            success=False,
            workflow_id=workflow_id,
            message=f"Error fetching workflow: {str(e)}"
        )


async def execute_n8n_workflow(
    workflow_id: Annotated[str, Field(description="The ID of the workflow to execute")],
    data: Annotated[Optional[dict], Field(description="Optional data to pass to the workflow")] = None
) -> WorkflowResponse:
    """Execute a specific n8n workflow."""
    try:
        n8n_url = os.getenv("N8N_CLOUD_INSTANCE_URL")
        api_key = os.getenv("N8N_API_KEY")
        
        if not n8n_url or not api_key:
            return WorkflowResponse(
                success=False,
                workflow_id=workflow_id,
                message="N8N_CLOUD_INSTANCE_URL or N8N_API_KEY not configured"
            )

        # Prepare execution payload
        execution_data = data if data else {}

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{n8n_url}/api/v1/workflows/{workflow_id}/execute",
                headers={
                    "X-N8N-API-KEY": api_key,
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                json=execution_data
            )
            
            if response.status_code == 200:
                execution_result = response.json()
                return WorkflowResponse(
                    success=True,
                    workflow_id=workflow_id,
                    message="Workflow executed successfully",
                    data=execution_result
                )
            else:
                return WorkflowResponse(
                    success=False,
                    workflow_id=workflow_id,
                    message=f"Failed to execute workflow: {response.status_code} {response.text}"
                )
                
    except Exception as e:
        return WorkflowResponse(
            success=False,
            workflow_id=workflow_id,
            message=f"Error executing workflow: {str(e)}"
        )
