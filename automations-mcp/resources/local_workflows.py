"""Resource that provides access to local n8n workflow files."""

import json
import os
from typing import Any

resource_uri = "workflows://local"


async def local_workflows() -> dict[str, Any]:
    """Provide access to locally stored n8n workflow files.

    This resource exposes the workflow JSON files stored in the
    workflows/ directory for analysis and reference.
    """
    workflows_dir = "/workspaces/automations_hub/workflows"
    workflows_data = {}
    
    try:
        if os.path.exists(workflows_dir):
            for filename in os.listdir(workflows_dir):
                if filename.endswith('.json'):
                    file_path = os.path.join(workflows_dir, filename)
                    try:
                        with open(file_path, 'r') as f:
                            workflow_data = json.load(f)
                            workflows_data[filename] = {
                                "name": workflow_data.get("name", filename),
                                "id": workflow_data.get("id"),
                                "active": workflow_data.get("active", False),
                                "nodes_count": len(workflow_data.get("nodes", [])),
                                "connections_count": len(workflow_data.get("connections", {})),
                                "full_data": workflow_data
                            }
                    except json.JSONDecodeError as e:
                        workflows_data[filename] = {
                            "error": f"Invalid JSON: {str(e)}"
                        }
        
        return {
            "resource_type": "local_workflows",
            "workflows_directory": workflows_dir,
            "total_workflows": len(workflows_data),
            "workflows": workflows_data,
            "available_files": list(workflows_data.keys()) if workflows_data else []
        }
    
    except Exception as e:
        return {
            "resource_type": "local_workflows",
            "error": f"Failed to read workflows: {str(e)}",
            "workflows_directory": workflows_dir,
            "total_workflows": 0,
            "workflows": {}
        }


# Designate the entry point function
export = local_workflows
