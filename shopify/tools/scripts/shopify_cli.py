#!/usr/bin/env python3
"""
Shopify Store Manager CLI
Comprehensive tool for importing, syncing, and managing Shopify store data and themes
"""

import os
import sys
import asyncio
import argparse
from pathlib import Path
import subprocess
import json
from datetime import datetime

# Add the current directory to path for imports
sys.path.append(str(Path(__file__).parent))

from shopify_importer import ShopifyImporter
from theme_sync import ThemeSync


class ShopifyStoreCLI:
    """Main CLI class for Shopify store management."""
    
    def __init__(self):
        self.base_path = Path("/workspaces/automations_hub/shopify")
        self.scripts_path = self.base_path / "scripts"
        
        # Ensure environment variables are set
        self.store_url = os.getenv("SHOPIFY_STORE_URL")
        self.access_token = os.getenv("SHOPIFY_ADMIN_API_ACCESS_TOKEN")
        
        if not self.store_url or not self.access_token:
            print("⚠️  Missing Shopify credentials!")
            print("Please set the following environment variables:")
            if not self.store_url:
                print("  - SHOPIFY_STORE_URL (e.g., 'one-head-hair.myshopify.com')")
            if not self.access_token:
                print("  - SHOPIFY_ADMIN_API_ACCESS_TOKEN")
            print("\nYou can set these in your shell or .env file")
    
    async def import_everything(self, **kwargs):
        """Import all store data and themes."""
        print("🚀 Starting comprehensive Shopify import...")
        print(f"🏪 Store: {self.store_url}")
        print(f"📁 Destination: {self.base_path}")
        
        if not await self._confirm_action("This will download all your store data and themes. Continue?"):
            return
        
        try:
            importer = ShopifyImporter(self.store_url, self.access_token)
            await importer.import_all()
            
            print("\n✅ Import completed successfully!")
            await self._show_import_summary()
            
        except Exception as e:
            print(f"❌ Import failed: {str(e)}")
            raise
    
    async def setup_development(self, theme_name: str = None, **kwargs):
        """Set up a local development environment."""
        print("🛠️  Setting up Shopify theme development environment...")
        
        if not theme_name:
            theme_name = f"dev_theme_{int(datetime.now().timestamp())}"
        
        try:
            theme_sync = ThemeSync(self.store_url, self.access_token)
            config = await theme_sync.setup_local_development(theme_name=theme_name)
            
            print(f"\n✅ Development environment ready!")
            print(f"📂 Local path: {config['local_path']}")
            print(f"🆔 Theme ID: {config['theme_id']}")
            
            # Show next steps
            print("\n🚀 Next Steps:")
            print("1. Navigate to your development theme directory")
            print("2. Start the development server:")
            print(f"   cd {config['local_path']}")
            print(f"   python3 {self.scripts_path}/theme_dev_server.py")
            print("3. Begin developing your theme!")
            
            return config
            
        except Exception as e:
            print(f"❌ Setup failed: {str(e)}")
            raise
    
    async def start_dev_server(self, theme_path: str = None, port: int = 3000, **kwargs):
        """Start the theme development server."""
        if not theme_path:
            # Try to find a development theme
            themes_dir = self.base_path / "themes"
            dev_themes = [d for d in themes_dir.glob("dev_*") if d.is_dir()]
            
            if not dev_themes:
                print("❌ No development themes found.")
                print("Run 'shopify-cli setup-dev' to create a development environment")
                return
            
            if len(dev_themes) == 1:
                theme_path = str(dev_themes[0])
            else:
                print("📁 Multiple development themes found:")
                for i, theme_dir in enumerate(dev_themes):
                    print(f"  {i + 1}. {theme_dir.name}")
                
                choice = input("Select theme (number): ").strip()
                try:
                    theme_path = str(dev_themes[int(choice) - 1])
                except (ValueError, IndexError):
                    print("Invalid selection")
                    return
        
        print(f"🚀 Starting development server for: {theme_path}")
        print(f"🌐 Server will be available at: http://localhost:{port}")
        
        # Set port environment variable
        os.environ["DEV_SERVER_PORT"] = str(port)
        
        # Start the development server
        try:
            cmd = [sys.executable, str(self.scripts_path / "theme_dev_server.py"), theme_path]
            subprocess.run(cmd)
        except KeyboardInterrupt:
            print("\n⏹️  Development server stopped")
    
    async def sync_theme(self, action: str, theme_path: str = None, **kwargs):
        """Sync theme files (push/pull)."""
        if not theme_path:
            theme_path = self._find_current_theme()
            if not theme_path:
                print("❌ No theme path specified and no current theme found")
                return
        
        theme_sync = ThemeSync(self.store_url, self.access_token)
        
        try:
            if action == "push":
                print(f"📤 Pushing local changes to Shopify...")
                await theme_sync.push_theme_changes(theme_path)
                print("✅ Push completed!")
                
            elif action == "pull":
                print(f"📥 Pulling changes from Shopify...")
                await theme_sync.pull_theme_changes(theme_path)
                print("✅ Pull completed!")
                
            elif action == "watch":
                print(f"👀 Watching for changes and auto-syncing...")
                from theme_sync import watch_theme_changes
                await watch_theme_changes(theme_path)
                
            else:
                print(f"❌ Unknown sync action: {action}")
                
        except Exception as e:
            print(f"❌ Sync failed: {str(e)}")
            raise
    
    async def deploy_theme(self, theme_path: str = None, backup: bool = True, **kwargs):
        """Deploy theme to live store."""
        if not theme_path:
            theme_path = self._find_current_theme()
            if not theme_path:
                print("❌ No theme path specified and no current theme found")
                return
        
        print("🚨 DEPLOYING TO LIVE THEME!")
        print("This will overwrite your live theme with local changes.")
        
        if backup:
            print("💾 A backup will be created automatically")
        
        if not await self._confirm_action("Are you sure you want to deploy to live?"):
            return
        
        try:
            theme_sync = ThemeSync(self.store_url, self.access_token)
            await theme_sync.deploy_to_live(theme_path, backup=backup)
            
            print("🎉 Successfully deployed to live theme!")
            
        except Exception as e:
            print(f"❌ Deployment failed: {str(e)}")
            raise
    
    async def list_themes(self, **kwargs):
        """List all themes in the store."""
        print("🎨 Listing Shopify themes...")
        
        try:
            theme_sync = ThemeSync(self.store_url, self.access_token)
            url = f"{theme_sync.store_url}/admin/api/{theme_sync.api_version}/themes.json"
            
            import httpx
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, headers=theme_sync.headers)
                response.raise_for_status()
                
                themes = response.json()["themes"]
                
                print(f"\n📋 Found {len(themes)} themes:")
                for theme in themes:
                    status = "🔴 LIVE" if theme.get("role") == "main" else "🟡 DEV" if theme.get("role") == "development" else "⚪ OTHER"
                    print(f"  {status} {theme['name']} (ID: {theme['id']})")
                    if theme.get("preview_url"):
                        print(f"    🔗 Preview: {theme['preview_url']}")
                
        except Exception as e:
            print(f"❌ Failed to list themes: {str(e)}")
            raise
    
    async def show_status(self, **kwargs):
        """Show current status of local themes and data."""
        print("📊 Shopify Store Status")
        print("=" * 50)
        
        # Store info
        print(f"🏪 Store: {self.store_url}")
        print(f"🔑 Access Token: {'✅ Set' if self.access_token else '❌ Missing'}")
        
        # Local data
        data_path = self.base_path / "imported_data"
        themes_path = self.base_path / "themes"
        
        print(f"\n📁 Local Data:")
        if data_path.exists():
            for data_dir in data_path.iterdir():
                if data_dir.is_dir():
                    files = list(data_dir.glob("*.json"))
                    print(f"  📂 {data_dir.name}: {len(files)} files")
        else:
            print("  ❌ No imported data found")
        
        print(f"\n🎨 Local Themes:")
        if themes_path.exists():
            for theme_dir in themes_path.iterdir():
                if theme_dir.is_dir() and not theme_dir.is_symlink():
                    config_file = theme_dir / ".dev_config.json"
                    if config_file.exists():
                        with open(config_file) as f:
                            config = json.load(f)
                        theme_id = config.get("theme_id", "Unknown")
                        print(f"  🛠️  {theme_dir.name} (ID: {theme_id})")
                    else:
                        print(f"  📁 {theme_dir.name}")
        else:
            print("  ❌ No local themes found")
        
        # Show last import
        summary_file = data_path / "import_summary.json"
        if summary_file.exists():
            with open(summary_file) as f:
                summary = json.load(f)
            
            import_date = summary.get("import_date", "Unknown")
            print(f"\n📅 Last Import: {import_date}")
    
    def _find_current_theme(self):
        """Find the current development theme."""
        themes_path = self.base_path / "themes"
        
        # Check for current_theme symlink
        current_link = themes_path / "current_theme"
        if current_link.exists():
            return str(current_link.resolve())
        
        # Check for development themes
        dev_themes = [d for d in themes_path.glob("dev_*") if d.is_dir()]
        if len(dev_themes) == 1:
            return str(dev_themes[0])
        
        return None
    
    async def _confirm_action(self, message: str) -> bool:
        """Ask for user confirmation."""
        response = input(f"{message} (y/N): ").strip().lower()
        return response in ["y", "yes"]
    
    async def _show_import_summary(self):
        """Show summary of imported data."""
        summary_file = self.base_path / "imported_data" / "import_summary.json"
        
        if summary_file.exists():
            with open(summary_file) as f:
                summary = json.load(f)
            
            print("\n📋 Import Summary:")
            for key, value in summary.get("data_summary", {}).items():
                print(f"  📂 {key}: {value} items")
            
            themes_count = summary.get("themes_count", 0)
            print(f"  🎨 themes: {themes_count} themes")
            
            print(f"\n📁 Data location: {self.base_path / 'imported_data'}")
            print(f"🎨 Themes location: {self.base_path / 'themes'}")


def create_cli():
    """Create and configure the CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Shopify Store Management CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s import                    # Import all store data and themes
  %(prog)s setup-dev my_theme        # Set up development environment
  %(prog)s dev-server                # Start development server
  %(prog)s sync push                 # Push local changes to Shopify
  %(prog)s sync pull                 # Pull changes from Shopify
  %(prog)s sync watch                # Watch for changes and auto-sync
  %(prog)s deploy                    # Deploy to live theme (with backup)
  %(prog)s list-themes               # List all themes in store
  %(prog)s status                    # Show current status
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Import command
    import_parser = subparsers.add_parser("import", help="Import all store data and themes")
    
    # Setup development command
    setup_parser = subparsers.add_parser("setup-dev", help="Set up local development environment")
    setup_parser.add_argument("theme_name", nargs="?", help="Name for the development theme")
    
    # Development server command
    dev_parser = subparsers.add_parser("dev-server", help="Start theme development server")
    dev_parser.add_argument("--theme-path", help="Path to theme directory")
    dev_parser.add_argument("--port", type=int, default=3000, help="Server port (default: 3000)")
    
    # Sync command
    sync_parser = subparsers.add_parser("sync", help="Sync theme files")
    sync_parser.add_argument("action", choices=["push", "pull", "watch"], help="Sync action")
    sync_parser.add_argument("--theme-path", help="Path to theme directory")
    
    # Deploy command
    deploy_parser = subparsers.add_parser("deploy", help="Deploy theme to live store")
    deploy_parser.add_argument("--theme-path", help="Path to theme directory")
    deploy_parser.add_argument("--no-backup", action="store_true", help="Skip creating backup")
    
    # List themes command
    list_parser = subparsers.add_parser("list-themes", help="List all themes in store")
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Show current status")
    
    return parser


async def main():
    """Main CLI entry point."""
    parser = create_cli()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cli = ShopifyStoreCLI()
    
    # Check if credentials are available for commands that need them
    if args.command != "status" and (not cli.store_url or not cli.access_token):
        print("❌ Missing Shopify credentials!")
        print("Please set SHOPIFY_STORE_URL and SHOPIFY_ADMIN_API_ACCESS_TOKEN")
        return
    
    try:
        if args.command == "import":
            await cli.import_everything()
            
        elif args.command == "setup-dev":
            await cli.setup_development(theme_name=args.theme_name)
            
        elif args.command == "dev-server":
            await cli.start_dev_server(theme_path=args.theme_path, port=args.port)
            
        elif args.command == "sync":
            await cli.sync_theme(action=args.action, theme_path=args.theme_path)
            
        elif args.command == "deploy":
            await cli.deploy_theme(theme_path=args.theme_path, backup=not args.no_backup)
            
        elif args.command == "list-themes":
            await cli.list_themes()
            
        elif args.command == "status":
            await cli.show_status()
            
    except KeyboardInterrupt:
        print("\n⏹️  Operation cancelled")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        if os.getenv("DEBUG"):
            raise


if __name__ == "__main__":
    asyncio.run(main())
