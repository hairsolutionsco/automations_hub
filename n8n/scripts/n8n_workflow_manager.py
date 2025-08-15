#!/usr/bin/env python3
"""
N8N Workflow Manager
A comprehensive system for importing, modifying, and pushing back automation JSON files to and from n8n.
"""

import os
import json
import asyncio
import httpx
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import subprocess
import shutil


@dataclass
class WorkflowInfo:
    """Information about a workflow."""
    id: str
    name: str
    active: bool
    created_at: str
    updated_at: str
    local_path: Optional[str] = None
    has_local_changes: bool = False


class N8NWorkflowManager:
    """Manages n8n workflows with full import/export/modify capabilities."""
    
    def __init__(self, workflows_dir: str = "workflows"):
        self.workflows_dir = Path(workflows_dir)
        self.workflows_dir.mkdir(exist_ok=True)
        
        # Load environment variables
        self.n8n_url = os.getenv("N8N_CLOUD_INSTANCE_URL")
        self.api_key = os.getenv("N8N_API_KEY")
        self.user_email = os.getenv("N8N_USER_EMAIL")
        
        # Local n8n instance settings (fallback)
        self.local_n8n_url = os.getenv("N8N_LOCAL_URL", "http://localhost:5678")
        
        self.backup_dir = self.workflows_dir / "backups"
        self.backup_dir.mkdir(exist_ok=True)
        
    def _validate_credentials(self) -> bool:
        """Validate that required credentials are available."""
        if not self.n8n_url or not self.api_key:
            print("❌ Missing N8N credentials. Please set:")
            print("  - N8N_CLOUD_INSTANCE_URL")
            print("  - N8N_API_KEY")
            print("  - N8N_USER_EMAIL (optional)")
            return False
        return True
    
    async def list_cloud_workflows(self) -> List[WorkflowInfo]:
        """List all workflows from n8n cloud instance."""
        if not self._validate_credentials():
            return []
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.n8n_url}/api/v1/workflows",
                    headers={
                        "X-N8N-API-KEY": self.api_key,
                        "Accept": "application/json"
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    workflows = []
                    
                    for workflow_data in data.get("data", []):
                        workflow = WorkflowInfo(
                            id=workflow_data.get("id"),
                            name=workflow_data.get("name"),
                            active=workflow_data.get("active", False),
                            created_at=workflow_data.get("createdAt", ""),
                            updated_at=workflow_data.get("updatedAt", "")
                        )
                        workflows.append(workflow)
                    
                    print(f"✅ Found {len(workflows)} workflows in cloud")
                    return workflows
                else:
                    print(f"❌ Failed to fetch workflows: {response.status_code}")
                    return []
                    
        except Exception as e:
            print(f"❌ Error fetching workflows: {str(e)}")
            return []
    
    async def download_workflow(self, workflow_id: str, save_path: Optional[str] = None) -> bool:
        """Download a specific workflow from n8n cloud."""
        if not self._validate_credentials():
            return False
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.n8n_url}/api/v1/workflows/{workflow_id}",
                    headers={
                        "X-N8N-API-KEY": self.api_key,
                        "Accept": "application/json"
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    workflow_data = response.json()
                    
                    # Determine save path
                    if not save_path:
                        workflow_name = workflow_data.get("name", f"workflow_{workflow_id}")
                        # Sanitize filename
                        safe_name = "".join(c for c in workflow_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
                        save_path = self.workflows_dir / f"{safe_name.replace(' ', '_').lower()}.json"
                    
                    # Add metadata
                    workflow_data["_metadata"] = {
                        "downloaded_at": datetime.now().isoformat(),
                        "source": "n8n_cloud",
                        "original_id": workflow_id
                    }
                    
                    # Save workflow
                    with open(save_path, 'w', encoding='utf-8') as f:
                        json.dump(workflow_data, f, indent=2, ensure_ascii=False)
                    
                    print(f"✅ Downloaded workflow '{workflow_data.get('name')}' to {save_path}")
                    return True
                else:
                    print(f"❌ Failed to download workflow {workflow_id}: {response.status_code}")
                    return False
                    
        except Exception as e:
            print(f"❌ Error downloading workflow {workflow_id}: {str(e)}")
            return False
    
    async def upload_workflow(self, workflow_path: str, workflow_id: Optional[str] = None) -> bool:
        """Upload a workflow to n8n cloud."""
        if not self._validate_credentials():
            return False
        
        try:
            with open(workflow_path, 'r', encoding='utf-8') as f:
                workflow_data = json.load(f)
            
            # Remove metadata if present
            if "_metadata" in workflow_data:
                del workflow_data["_metadata"]
            
            async with httpx.AsyncClient() as client:
                if workflow_id:
                    # Update existing workflow
                    response = await client.put(
                        f"{self.n8n_url}/api/v1/workflows/{workflow_id}",
                        headers={
                            "X-N8N-API-KEY": self.api_key,
                            "Content-Type": "application/json",
                            "Accept": "application/json"
                        },
                        json=workflow_data,
                        timeout=30.0
                    )
                else:
                    # Create new workflow
                    response = await client.post(
                        f"{self.n8n_url}/api/v1/workflows",
                        headers={
                            "X-N8N-API-KEY": self.api_key,
                            "Content-Type": "application/json",
                            "Accept": "application/json"
                        },
                        json=workflow_data,
                        timeout=30.0
                    )
                
                if response.status_code in [200, 201]:
                    result = response.json()
                    print(f"✅ Successfully uploaded workflow '{workflow_data.get('name')}'")
                    print(f"   ID: {result.get('id', 'N/A')}")
                    return True
                else:
                    print(f"❌ Failed to upload workflow: {response.status_code}")
                    print(f"   Response: {response.text}")
                    return False
                    
        except Exception as e:
            print(f"❌ Error uploading workflow: {str(e)}")
            return False
    
    async def sync_all_from_cloud(self, backup_existing: bool = True) -> bool:
        """Download all workflows from cloud to local directory."""
        print("🔄 Syncing all workflows from cloud...")
        
        if backup_existing and any(self.workflows_dir.glob("*.json")):
            await self.create_backup()
        
        workflows = await self.list_cloud_workflows()
        if not workflows:
            print("❌ No workflows found or failed to fetch workflows")
            return False
        
        success_count = 0
        for workflow in workflows:
            if await self.download_workflow(workflow.id):
                success_count += 1
        
        print(f"✅ Successfully synced {success_count}/{len(workflows)} workflows")
        return success_count > 0
    
    async def sync_all_to_cloud(self, force: bool = False) -> bool:
        """Upload all local workflows to cloud."""
        print("⬆️ Syncing all local workflows to cloud...")
        
        json_files = list(self.workflows_dir.glob("*.json"))
        if not json_files:
            print("❌ No local workflow files found")
            return False
        
        success_count = 0
        for workflow_file in json_files:
            if workflow_file.name.startswith("backup_"):
                continue  # Skip backup files
            
            try:
                with open(workflow_file, 'r', encoding='utf-8') as f:
                    workflow_data = json.load(f)
                
                # Check if workflow has an ID (existing workflow)
                original_id = None
                if "_metadata" in workflow_data:
                    original_id = workflow_data["_metadata"].get("original_id")
                elif "id" in workflow_data:
                    original_id = workflow_data["id"]
                
                if await self.upload_workflow(str(workflow_file), original_id):
                    success_count += 1
                    
            except Exception as e:
                print(f"❌ Error processing {workflow_file.name}: {str(e)}")
        
        print(f"✅ Successfully uploaded {success_count}/{len(json_files)} workflows")
        return success_count > 0
    
    async def create_backup(self) -> str:
        """Create a backup of current local workflows."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp}"
        backup_path = self.backup_dir / backup_name
        backup_path.mkdir(exist_ok=True)
        
        json_files = list(self.workflows_dir.glob("*.json"))
        if not json_files:
            print("ℹ️ No workflows to backup")
            return str(backup_path)
        
        for workflow_file in json_files:
            if not workflow_file.name.startswith("backup_"):
                shutil.copy2(workflow_file, backup_path / workflow_file.name)
        
        print(f"✅ Created backup at {backup_path}")
        return str(backup_path)
    
    def list_local_workflows(self) -> List[str]:
        """List all local workflow files."""
        json_files = [f.name for f in self.workflows_dir.glob("*.json") 
                     if not f.name.startswith("backup_")]
        return sorted(json_files)
    
    def modify_workflow(self, workflow_path: str, modifications: Dict[str, Any]) -> bool:
        """Apply modifications to a workflow file."""
        try:
            with open(workflow_path, 'r', encoding='utf-8') as f:
                workflow_data = json.load(f)
            
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
            
            # Update metadata
            if "_metadata" not in workflow_data:
                workflow_data["_metadata"] = {}
            workflow_data["_metadata"]["last_modified"] = datetime.now().isoformat()
            workflow_data["_metadata"]["modified_locally"] = True
            
            # Save modified workflow
            with open(workflow_path, 'w', encoding='utf-8') as f:
                json.dump(workflow_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Successfully modified workflow at {workflow_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error modifying workflow: {str(e)}")
            return False
    
    async def validate_workflow(self, workflow_path: str) -> bool:
        """Validate a workflow file structure."""
        try:
            with open(workflow_path, 'r', encoding='utf-8') as f:
                workflow_data = json.load(f)
            
            # Basic validation
            required_fields = ["name", "nodes"]
            for field in required_fields:
                if field not in workflow_data:
                    print(f"❌ Missing required field: {field}")
                    return False
            
            # Validate nodes
            nodes = workflow_data.get("nodes", [])
            if not isinstance(nodes, list):
                print("❌ 'nodes' must be a list")
                return False
            
            # Check for duplicate node IDs
            node_ids = [node.get("id") for node in nodes if "id" in node]
            if len(node_ids) != len(set(node_ids)):
                print("❌ Duplicate node IDs found")
                return False
            
            print(f"✅ Workflow validation passed for {workflow_path}")
            return True
            
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON: {str(e)}")
            return False
        except Exception as e:
            print(f"❌ Validation error: {str(e)}")
            return False


async def main():
    """Main CLI interface for the workflow manager."""
    import argparse
    
    parser = argparse.ArgumentParser(description="N8N Workflow Manager")
    parser.add_argument("--workflows-dir", default="workflows", help="Workflows directory")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # List commands
    list_parser = subparsers.add_parser("list", help="List workflows")
    list_parser.add_argument("--cloud", action="store_true", help="List cloud workflows")
    list_parser.add_argument("--local", action="store_true", help="List local workflows")
    
    # Download commands
    download_parser = subparsers.add_parser("download", help="Download workflow(s)")
    download_parser.add_argument("--all", action="store_true", help="Download all workflows")
    download_parser.add_argument("--id", help="Specific workflow ID to download")
    download_parser.add_argument("--backup", action="store_true", help="Backup existing before download")
    
    # Upload commands
    upload_parser = subparsers.add_parser("upload", help="Upload workflow(s)")
    upload_parser.add_argument("--all", action="store_true", help="Upload all local workflows")
    upload_parser.add_argument("--file", help="Specific workflow file to upload")
    upload_parser.add_argument("--id", help="Workflow ID to update (for existing workflows)")
    
    # Modify commands
    modify_parser = subparsers.add_parser("modify", help="Modify workflow")
    modify_parser.add_argument("file", help="Workflow file to modify")
    modify_parser.add_argument("--name", help="Change workflow name")
    modify_parser.add_argument("--active", type=bool, help="Change active status")
    
    # Utility commands
    subparsers.add_parser("backup", help="Create backup of local workflows")
    
    validate_parser = subparsers.add_parser("validate", help="Validate workflow file")
    validate_parser.add_argument("file", help="Workflow file to validate")
    
    args = parser.parse_args()
    
    manager = N8NWorkflowManager(args.workflows_dir)
    
    if args.command == "list":
        if args.cloud or not args.local:
            workflows = await manager.list_cloud_workflows()
            print(f"\n📋 Cloud Workflows ({len(workflows)}):")
            for w in workflows:
                status = "🟢" if w.active else "🔴"
                print(f"  {status} {w.name} ({w.id})")
        
        if args.local or not args.cloud:
            local_workflows = manager.list_local_workflows()
            print(f"\n📁 Local Workflows ({len(local_workflows)}):")
            for w in local_workflows:
                print(f"  📄 {w}")
    
    elif args.command == "download":
        if args.backup:
            await manager.create_backup()
        
        if args.all:
            await manager.sync_all_from_cloud(backup_existing=args.backup)
        elif args.id:
            await manager.download_workflow(args.id)
        else:
            print("❌ Specify --all or --id")
    
    elif args.command == "upload":
        if args.all:
            await manager.sync_all_to_cloud()
        elif args.file:
            await manager.upload_workflow(args.file, args.id)
        else:
            print("❌ Specify --all or --file")
    
    elif args.command == "modify":
        modifications = {}
        if args.name:
            modifications["name"] = args.name
        if args.active is not None:
            modifications["active"] = args.active
        
        if modifications:
            manager.modify_workflow(args.file, modifications)
        else:
            print("❌ No modifications specified")
    
    elif args.command == "backup":
        await manager.create_backup()
    
    elif args.command == "validate":
        await manager.validate_workflow(args.file)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    asyncio.run(main())
