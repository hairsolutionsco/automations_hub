#!/usr/bin/env python3
"""
Shopify Theme Development Environment with Sync Capabilities
Provides local theme development with push/pull sync to Shopify
"""

import os
import json
import asyncio
import httpx
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import base64
import hashlib
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class ThemeSync:
    """Theme synchronization between local and Shopify."""
    
    def __init__(self, store_url: str = None, access_token: str = None):
        self.store_url = store_url or os.getenv("SHOPIFY_STORE_URL")
        self.access_token = access_token or os.getenv("SHOPIFY_ADMIN_API_ACCESS_TOKEN")
        
        if not self.store_url or not self.access_token:
            raise ValueError("Missing SHOPIFY_STORE_URL or SHOPIFY_ADMIN_API_ACCESS_TOKEN")
        
        # Ensure store URL has proper format
        if not self.store_url.startswith(("http://", "https://")):
            self.store_url = f"https://{self.store_url}"
        
        self.api_version = "2024-01"
        self.themes_path = Path("/workspaces/automations_hub/shopify/themes")
        
        self.headers = {
            "X-Shopify-Access-Token": self.access_token,
            "Content-Type": "application/json"
        }
    
    async def create_development_theme(self, name: str = None) -> Dict:
        """Create a new development theme based on the live theme."""
        if not name:
            name = f"dev_theme_{int(time.time())}"
        
        print(f"🎨 Creating development theme: {name}")
        
        # Get live theme
        live_theme = await self.get_live_theme()
        if not live_theme:
            raise ValueError("No live theme found")
        
        # Create new theme
        url = f"{self.store_url}/admin/api/{self.api_version}/themes.json"
        
        theme_data = {
            "theme": {
                "name": name,
                "src": live_theme["id"]  # Copy from live theme
            }
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, headers=self.headers, json=theme_data)
            response.raise_for_status()
            
            new_theme = response.json()["theme"]
            
            print(f"✅ Created development theme: {new_theme['name']} (ID: {new_theme['id']})")
            print(f"🔗 Preview URL: {new_theme['preview_url']}")
            
            return new_theme
    
    async def get_live_theme(self) -> Optional[Dict]:
        """Get the current live theme."""
        url = f"{self.store_url}/admin/api/{self.api_version}/themes.json"
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            
            themes = response.json()["themes"]
            live_theme = next((t for t in themes if t.get("role") == "main"), None)
            
            return live_theme
    
    async def setup_local_development(self, theme_id: int = None, theme_name: str = "development"):
        """Set up local development environment for a theme."""
        if not theme_id:
            # Create a new development theme
            dev_theme = await self.create_development_theme(theme_name)
            theme_id = dev_theme["id"]
            theme_name = dev_theme["name"]
        
        # Create local development directory
        dev_dir = self.themes_path / f"dev_{theme_name}_{theme_id}"
        dev_dir.mkdir(exist_ok=True)
        
        print(f"📁 Setting up development environment: {dev_dir}")
        
        # Download theme assets
        await self._download_theme_assets(theme_id, dev_dir)
        
        # Create development configuration
        dev_config = {
            "theme_id": theme_id,
            "theme_name": theme_name,
            "created_at": datetime.now().isoformat(),
            "local_path": str(dev_dir),
            "sync_enabled": True,
            "auto_upload": False
        }
        
        with open(dev_dir / ".dev_config.json", "w") as f:
            json.dump(dev_config, f, indent=2)
        
        # Create gitignore for theme development
        gitignore_content = """
# Shopify theme development
.dev_config.json
*.log
.DS_Store
Thumbs.db

# Node modules (if using build tools)
node_modules/
npm-debug.log*

# Build outputs
dist/
build/

# IDE files
.vscode/
.idea/
*.swp
*.swo
"""
        
        with open(dev_dir / ".gitignore", "w") as f:
            f.write(gitignore_content.strip())
        
        # Create development README
        readme_content = f"""# Shopify Theme Development: {theme_name}

## Development Environment Setup

**Theme ID:** {theme_id}
**Local Path:** {dev_dir}
**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Available Commands

```bash
# Start theme development server with live reload
cd {dev_dir}
python3 ../scripts/theme_dev_server.py

# Sync changes to Shopify
python3 ../scripts/theme_sync.py push

# Pull latest changes from Shopify
python3 ../scripts/theme_sync.py pull

# Watch for changes and auto-sync
python3 ../scripts/theme_sync.py watch

# Deploy to live theme (BE CAREFUL!)
python3 ../scripts/theme_sync.py deploy
```

## Theme Structure

```
{theme_name}/
├── assets/          # CSS, JS, images
├── config/          # Theme settings
├── layout/          # Theme layouts
├── locales/         # Translations
├── sections/        # Theme sections
├── snippets/        # Reusable code snippets
├── templates/       # Page templates
└── .dev_config.json # Development configuration
```

## Development Workflow

1. Make changes to theme files locally
2. Test changes using the development server
3. Push changes to your development theme on Shopify
4. Preview changes using the Shopify preview URL
5. When ready, deploy changes to the live theme

## Preview URL
{f"https://{self.store_url.replace('https://', '').replace('http://', '')}?preview_theme_id={theme_id}"}

## Important Notes

- Always test changes in development theme first
- Use `deploy` command only when you're ready to go live
- Keep backups of your live theme
- Use version control (git) for your theme files
"""
        
        with open(dev_dir / "README.md", "w") as f:
            f.write(readme_content)
        
        print(f"✅ Development environment ready!")
        print(f"📂 Local path: {dev_dir}")
        print(f"🔗 Preview URL: https://{self.store_url.replace('https://', '').replace('http://', '')}?preview_theme_id={theme_id}")
        
        return dev_config
    
    async def push_theme_changes(self, local_path: str, theme_id: int = None):
        """Push local changes to Shopify theme."""
        local_dir = Path(local_path)
        
        if not local_dir.exists():
            raise ValueError(f"Local theme directory not found: {local_path}")
        
        # Load development config
        config_file = local_dir / ".dev_config.json"
        if config_file.exists() and not theme_id:
            with open(config_file) as f:
                config = json.load(f)
                theme_id = config["theme_id"]
        
        if not theme_id:
            raise ValueError("Theme ID not found. Please specify theme_id or ensure .dev_config.json exists")
        
        print(f"📤 Pushing changes to theme {theme_id}...")
        
        # Get all theme files
        theme_files = []
        
        for file_path in local_dir.rglob("*"):
            if file_path.is_file() and not file_path.name.startswith("."):
                relative_path = file_path.relative_to(local_dir)
                
                # Skip certain files
                if any(skip in str(relative_path) for skip in [".git", "node_modules", ".dev_config.json", "README.md"]):
                    continue
                
                theme_files.append((file_path, str(relative_path)))
        
        # Upload files to Shopify
        uploaded_count = 0
        
        for file_path, asset_key in theme_files:
            try:
                await self._upload_asset(theme_id, file_path, asset_key)
                uploaded_count += 1
                print(f"  ✅ {asset_key}")
                
            except Exception as e:
                print(f"  ❌ {asset_key}: {str(e)}")
        
        print(f"✅ Pushed {uploaded_count}/{len(theme_files)} files")
    
    async def pull_theme_changes(self, local_path: str, theme_id: int = None):
        """Pull changes from Shopify theme to local."""
        local_dir = Path(local_path)
        local_dir.mkdir(exist_ok=True)
        
        # Load development config
        config_file = local_dir / ".dev_config.json"
        if config_file.exists() and not theme_id:
            with open(config_file) as f:
                config = json.load(f)
                theme_id = config["theme_id"]
        
        if not theme_id:
            raise ValueError("Theme ID not found. Please specify theme_id or ensure .dev_config.json exists")
        
        print(f"📥 Pulling changes from theme {theme_id}...")
        
        await self._download_theme_assets(theme_id, local_dir)
        
        print("✅ Successfully pulled theme changes")
    
    async def deploy_to_live(self, local_path: str, backup: bool = True):
        """Deploy development theme to live theme (with backup)."""
        local_dir = Path(local_path)
        
        if not local_dir.exists():
            raise ValueError(f"Local theme directory not found: {local_path}")
        
        print("🚨 DEPLOYING TO LIVE THEME!")
        print("This will overwrite your live theme with local changes.")
        
        # Get live theme
        live_theme = await self.get_live_theme()
        if not live_theme:
            raise ValueError("No live theme found")
        
        live_theme_id = live_theme["id"]
        
        # Create backup if requested
        if backup:
            print("💾 Creating backup of live theme...")
            backup_name = f"backup_{live_theme['name']}_{int(time.time())}"
            backup_theme = await self.create_development_theme(backup_name)
            print(f"✅ Backup created: {backup_theme['name']} (ID: {backup_theme['id']})")
        
        # Deploy changes
        await self.push_theme_changes(local_path, live_theme_id)
        
        print("🎉 Successfully deployed to live theme!")
        print(f"🔗 Live store: {self.store_url}")
    
    async def _upload_asset(self, theme_id: int, file_path: Path, asset_key: str):
        """Upload a single asset to Shopify theme."""
        url = f"{self.store_url}/admin/api/{self.api_version}/themes/{theme_id}/assets.json"
        
        # Determine if file is binary or text
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Text file
            asset_data = {
                "asset": {
                    "key": asset_key,
                    "value": content
                }
            }
            
        except UnicodeDecodeError:
            # Binary file
            with open(file_path, "rb") as f:
                content = f.read()
                
            asset_data = {
                "asset": {
                    "key": asset_key,
                    "attachment": base64.b64encode(content).decode("utf-8")
                }
            }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.put(url, headers=self.headers, json=asset_data)
            response.raise_for_status()
    
    async def _download_theme_assets(self, theme_id: int, theme_dir: Path):
        """Download all assets for a theme."""
        url = f"{self.store_url}/admin/api/{self.api_version}/themes/{theme_id}/assets.json"
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            
            assets_data = response.json()
            assets = assets_data.get("assets", [])
            
            # Create asset directories
            for directory in ["templates", "sections", "snippets", "layout", "assets", "config", "locales"]:
                (theme_dir / directory).mkdir(exist_ok=True)
            
            # Download each asset
            for asset in assets:
                asset_key = asset["key"]
                
                # Get asset content
                asset_url = f"{self.store_url}/admin/api/{self.api_version}/themes/{theme_id}/assets.json"
                params = {"asset[key]": asset_key}
                
                asset_response = await client.get(asset_url, headers=self.headers, params=params)
                asset_response.raise_for_status()
                
                asset_data = asset_response.json()
                asset_content = asset_data["asset"]
                
                # Determine file path
                file_path = theme_dir / asset_key
                file_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Save asset content
                if "value" in asset_content:
                    # Text content
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(asset_content["value"])
                elif "attachment" in asset_content:
                    # Binary content (base64 encoded)
                    with open(file_path, "wb") as f:
                        f.write(base64.b64decode(asset_content["attachment"]))


class ThemeWatcher(FileSystemEventHandler):
    """File system watcher for auto-syncing theme changes."""
    
    def __init__(self, theme_sync: ThemeSync, local_path: str, theme_id: int):
        self.theme_sync = theme_sync
        self.local_path = Path(local_path)
        self.theme_id = theme_id
        self.last_sync = {}
        
    def on_modified(self, event):
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        
        # Skip certain files
        if any(skip in str(file_path) for skip in [".git", "node_modules", ".dev_config.json", "__pycache__"]):
            return
        
        # Debounce rapid changes
        now = time.time()
        if file_path in self.last_sync and now - self.last_sync[file_path] < 2:
            return
        
        self.last_sync[file_path] = now
        
        # Sync file
        relative_path = file_path.relative_to(self.local_path)
        print(f"🔄 Syncing: {relative_path}")
        
        try:
            asyncio.create_task(
                self.theme_sync._upload_asset(self.theme_id, file_path, str(relative_path))
            )
            print(f"  ✅ Synced: {relative_path}")
        except Exception as e:
            print(f"  ❌ Error syncing {relative_path}: {str(e)}")


async def watch_theme_changes(local_path: str, theme_id: int = None):
    """Watch for local theme changes and auto-sync to Shopify."""
    local_dir = Path(local_path)
    
    if not local_dir.exists():
        raise ValueError(f"Local theme directory not found: {local_path}")
    
    # Load theme ID from config if not provided
    if not theme_id:
        config_file = local_dir / ".dev_config.json"
        if config_file.exists():
            with open(config_file) as f:
                config = json.load(f)
                theme_id = config["theme_id"]
    
    if not theme_id:
        raise ValueError("Theme ID not found")
    
    print(f"👀 Watching for changes in: {local_path}")
    print(f"🎯 Auto-syncing to theme: {theme_id}")
    print("Press Ctrl+C to stop watching")
    
    theme_sync = ThemeSync()
    event_handler = ThemeWatcher(theme_sync, local_path, theme_id)
    observer = Observer()
    observer.schedule(event_handler, str(local_dir), recursive=True)
    observer.start()
    
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n⏹️  Stopped watching for changes")
    
    observer.join()


async def main():
    """Main CLI interface for theme development."""
    import sys
    
    if len(sys.argv) < 2:
        print("""
Shopify Theme Development CLI

Usage:
  python3 theme_sync.py <command> [options]

Commands:
  setup [theme_name]    - Set up local development environment
  push [local_path]     - Push local changes to Shopify
  pull [local_path]     - Pull changes from Shopify to local
  watch [local_path]    - Watch for changes and auto-sync
  deploy [local_path]   - Deploy to live theme (with backup)
  create [theme_name]   - Create new development theme

Examples:
  python3 theme_sync.py setup my_dev_theme
  python3 theme_sync.py push ./dev_my_theme_123456
  python3 theme_sync.py watch ./dev_my_theme_123456
  python3 theme_sync.py deploy ./dev_my_theme_123456
""")
        return
    
    command = sys.argv[1]
    theme_sync = ThemeSync()
    
    try:
        if command == "setup":
            theme_name = sys.argv[2] if len(sys.argv) > 2 else "development"
            await theme_sync.setup_local_development(theme_name=theme_name)
            
        elif command == "push":
            local_path = sys.argv[2] if len(sys.argv) > 2 else "./current_theme"
            await theme_sync.push_theme_changes(local_path)
            
        elif command == "pull":
            local_path = sys.argv[2] if len(sys.argv) > 2 else "./current_theme"
            await theme_sync.pull_theme_changes(local_path)
            
        elif command == "watch":
            local_path = sys.argv[2] if len(sys.argv) > 2 else "./current_theme"
            await watch_theme_changes(local_path)
            
        elif command == "deploy":
            local_path = sys.argv[2] if len(sys.argv) > 2 else "./current_theme"
            await theme_sync.deploy_to_live(local_path)
            
        elif command == "create":
            theme_name = sys.argv[2] if len(sys.argv) > 2 else None
            await theme_sync.create_development_theme(theme_name)
            
        else:
            print(f"Unknown command: {command}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
