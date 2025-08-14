"""Tool for managing n8n workflows."""

import os
import json
import httpx
from pathlib import Path
from datetime import datetime
from typing import Annotated, Any, Optional, List
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


async def import_workflow_from_file(
    file_path: Annotated[str, Field(description="Path to the workflow JSON file to import")],
    workflow_id: Annotated[Optional[str], Field(description="Existing workflow ID to update (leave empty for new workflow)")] = None
) -> WorkflowResponse:
    """Import a workflow from a local JSON file to n8n cloud."""
    try:
        n8n_url = os.getenv("N8N_CLOUD_INSTANCE_URL")
        api_key = os.getenv("N8N_API_KEY")
        
        if not n8n_url or not api_key:
            return WorkflowResponse(
                success=False,
                message="N8N_CLOUD_INSTANCE_URL or N8N_API_KEY not configured"
            )

        # Read and validate workflow file
        workflow_path = Path(file_path)
        if not workflow_path.exists():
            return WorkflowResponse(
                success=False,
                message=f"Workflow file not found: {file_path}"
            )

        try:
            with open(workflow_path, 'r', encoding='utf-8') as f:
                workflow_data = json.load(f)
        except json.JSONDecodeError as e:
            return WorkflowResponse(
                success=False,
                message=f"Invalid JSON in workflow file: {str(e)}"
            )

        # Remove metadata if present
        if "_metadata" in workflow_data:
            del workflow_data["_metadata"]

        async with httpx.AsyncClient() as client:
            if workflow_id:
                # Update existing workflow
                response = await client.put(
                    f"{n8n_url}/api/v1/workflows/{workflow_id}",
                    headers={
                        "X-N8N-API-KEY": api_key,
                        "Content-Type": "application/json",
                        "Accept": "application/json"
                    },
                    json=workflow_data,
                    timeout=30.0
                )
            else:
                # Create new workflow
                response = await client.post(
                    f"{n8n_url}/api/v1/workflows",
                    headers={
                        "X-N8N-API-KEY": api_key,
                        "Content-Type": "application/json",
                        "Accept": "application/json"
                    },
                    json=workflow_data,
                    timeout=30.0
                )
            
            if response.status_code in [200, 201]:
                result = response.json()
                return WorkflowResponse(
                    success=True,
                    workflow_id=result.get("id"),
                    workflow_name=result.get("name"),
                    message=f"Successfully imported workflow '{result.get('name')}'",
                    data=result
                )
            else:
                return WorkflowResponse(
                    success=False,
                    message=f"Failed to import workflow: {response.status_code} {response.text}"
                )
                
    except Exception as e:
        return WorkflowResponse(
            success=False,
            message=f"Error importing workflow: {str(e)}"
        )


async def export_workflow_to_file(
    workflow_id: Annotated[str, Field(description="The ID of the workflow to export")],
    file_path: Annotated[Optional[str], Field(description="Path to save the workflow (auto-generated if not provided)")] = None,
    workflows_dir: Annotated[str, Field(description="Directory to save workflows")] = "workflows"
) -> WorkflowResponse:
    """Export a workflow from n8n cloud to a local JSON file."""
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
                },
                timeout=30.0
            )
            
            if response.status_code == 200:
                workflow_data = response.json()
                
                # Determine save path
                if not file_path:
                    workflows_path = Path(workflows_dir)
                    workflows_path.mkdir(exist_ok=True)
                    
                    workflow_name = workflow_data.get("name", f"workflow_{workflow_id}")
                    # Sanitize filename
                    safe_name = "".join(c for c in workflow_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
                    file_path = workflows_path / f"{safe_name.replace(' ', '_').lower()}.json"
                
                # Add metadata
                workflow_data["_metadata"] = {
                    "exported_at": datetime.now().isoformat(),
                    "source": "n8n_cloud",
                    "original_id": workflow_id
                }
                
                # Save workflow
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(workflow_data, f, indent=2, ensure_ascii=False)
                
                return WorkflowResponse(
                    success=True,
                    workflow_id=workflow_id,
                    workflow_name=workflow_data.get("name"),
                    message=f"Successfully exported workflow to {file_path}",
                    data={"file_path": str(file_path)}
                )
            else:
                return WorkflowResponse(
                    success=False,
                    workflow_id=workflow_id,
                    message=f"Failed to export workflow: {response.status_code} {response.text}"
                )
                
    except Exception as e:
        return WorkflowResponse(
            success=False,
            workflow_id=workflow_id,
            message=f"Error exporting workflow: {str(e)}"
        )


async def sync_all_workflows_from_cloud(
    workflows_dir: Annotated[str, Field(description="Directory to save workflows")] = "workflows",
    backup_existing: Annotated[bool, Field(description="Create backup of existing workflows")] = True
) -> WorkflowResponse:
    """Sync all workflows from n8n cloud to local directory."""
    try:
        workflows_path = Path(workflows_dir)
        workflows_path.mkdir(exist_ok=True)
        
        # Create backup if requested
        if backup_existing and any(workflows_path.glob("*.json")):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = workflows_path / f"backup_{timestamp}"
            backup_dir.mkdir(exist_ok=True)
            
            for file in workflows_path.glob("*.json"):
                if not file.name.startswith("backup_"):
                    import shutil
                    shutil.copy2(file, backup_dir / file.name)
        
        # Get all workflows
        workflows_response = await list_n8n_workflows()
        if not workflows_response.workflows:
            return WorkflowResponse(
                success=False,
                message="No workflows found or failed to fetch workflows from cloud"
            )
        
        # Download each workflow
        success_count = 0
        total_count = len(workflows_response.workflows)
        
        for workflow in workflows_response.workflows:
            workflow_id = workflow.get("id")
            if workflow_id:
                export_response = await export_workflow_to_file(workflow_id, None, workflows_dir)
                if export_response.success:
                    success_count += 1
        
        return WorkflowResponse(
            success=success_count > 0,
            message=f"Successfully synced {success_count}/{total_count} workflows from cloud",
            data={"synced_count": success_count, "total_count": total_count}
        )
        
    except Exception as e:
        return WorkflowResponse(
            success=False,
            message=f"Error syncing workflows from cloud: {str(e)}"
        )


async def sync_all_workflows_to_cloud(
    workflows_dir: Annotated[str, Field(description="Directory containing workflow files")] = "workflows"
) -> WorkflowResponse:
    """Sync all local workflow files to n8n cloud."""
    try:
        workflows_path = Path(workflows_dir)
        
        if not workflows_path.exists():
            return WorkflowResponse(
                success=False,
                message=f"Workflows directory not found: {workflows_dir}"
            )
        
        # Find all JSON workflow files
        json_files = [f for f in workflows_path.glob("*.json") if not f.name.startswith("backup_")]
        
        if not json_files:
            return WorkflowResponse(
                success=False,
                message=f"No workflow files found in {workflows_dir}"
            )
        
        success_count = 0
        total_count = len(json_files)
        results = []
        
        for workflow_file in json_files:
            try:
                # Try to determine if this is an existing workflow
                with open(workflow_file, 'r', encoding='utf-8') as f:
                    workflow_data = json.load(f)
                
                original_id = None
                if "_metadata" in workflow_data:
                    original_id = workflow_data["_metadata"].get("original_id")
                elif "id" in workflow_data:
                    original_id = workflow_data["id"]
                
                # Import workflow
                import_response = await import_workflow_from_file(str(workflow_file), original_id)
                if import_response.success:
                    success_count += 1
                    results.append(f"✅ {workflow_file.name}")
                else:
                    results.append(f"❌ {workflow_file.name}: {import_response.message}")
                    
            except Exception as e:
                results.append(f"❌ {workflow_file.name}: {str(e)}")
        
        return WorkflowResponse(
            success=success_count > 0,
            message=f"Successfully synced {success_count}/{total_count} workflows to cloud",
            data={
                "synced_count": success_count,
                "total_count": total_count,
                "results": results
            }
        )
        
    except Exception as e:
        return WorkflowResponse(
            success=False,
            message=f"Error syncing workflows to cloud: {str(e)}"
        )


async def modify_workflow_file(
    file_path: Annotated[str, Field(description="Path to the workflow JSON file to modify")],
    modifications: Annotated[dict, Field(description="Dictionary of modifications to apply")]
) -> WorkflowResponse:
    """Modify a local workflow JSON file."""
    try:
        workflow_path = Path(file_path)
        if not workflow_path.exists():
            return WorkflowResponse(
                success=False,
                message=f"Workflow file not found: {file_path}"
            )

        # Read workflow
        try:
            with open(workflow_path, 'r', encoding='utf-8') as f:
                workflow_data = json.load(f)
        except json.JSONDecodeError as e:
            return WorkflowResponse(
                success=False,
                message=f"Invalid JSON in workflow file: {str(e)}"
            )

        # Apply modifications
        for key, value in modifications.items():
            if key == "name":
                workflow_data["name"] = value
            elif key == "active":
                workflow_data["active"] = value
            elif key == "nodes":
                # Modify specific nodes
                if isinstance(value, dict):
                    for node_id, node_modifications in value.items():
                        for node in workflow_data.get("nodes", []):
                            if node.get("id") == node_id:
                                node.update(node_modifications)
                                break
            elif key == "add_node":
                if "nodes" not in workflow_data:
                    workflow_data["nodes"] = []
                workflow_data["nodes"].append(value)
            elif key == "remove_node":
                if "nodes" in workflow_data:
                    workflow_data["nodes"] = [
                        node for node in workflow_data["nodes"] 
                        if node.get("id") != value
                    ]
            else:
                # Direct assignment for other keys
                workflow_data[key] = value

        # Update metadata
        if "_metadata" not in workflow_data:
            workflow_data["_metadata"] = {}
        workflow_data["_metadata"]["last_modified"] = datetime.now().isoformat()
        workflow_data["_metadata"]["modified_locally"] = True

        # Save modified workflow
        with open(workflow_path, 'w', encoding='utf-8') as f:
            json.dump(workflow_data, f, indent=2, ensure_ascii=False)

        return WorkflowResponse(
            success=True,
            message=f"Successfully modified workflow file: {file_path}",
            data={"modified_keys": list(modifications.keys())}
        )

    except Exception as e:
        return WorkflowResponse(
            success=False,
            message=f"Error modifying workflow file: {str(e)}"
        )
