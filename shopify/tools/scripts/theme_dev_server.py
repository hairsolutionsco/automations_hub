#!/usr/bin/env python3
"""
Shopify Theme Development Server with Live Reload
Provides local development server for theme files with auto-reload
"""

import os
import json
import asyncio
import aiofiles
from pathlib import Path
from aiohttp import web, WSMsgType
import aiohttp_cors
from aiohttp.web_ws import WSMsgType
import hashlib
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import webbrowser
from urllib.parse import urljoin


class ThemeDevServer:
    """Development server for Shopify themes with live reload."""
    
    def __init__(self, theme_path: str, port: int = 3000):
        self.theme_path = Path(theme_path)
        self.port = port
        self.websockets = set()
        self.file_hashes = {}
        
        # Load theme config
        self.config = self._load_theme_config()
        
        # Setup file watcher
        self.observer = Observer()
        self.observer.schedule(
            ThemeFileWatcher(self),
            str(self.theme_path),
            recursive=True
        )
    
    def _load_theme_config(self):
        """Load theme development configuration."""
        config_file = self.theme_path / ".dev_config.json"
        
        if config_file.exists():
            with open(config_file) as f:
                return json.load(f)
        
        return {
            "theme_name": self.theme_path.name,
            "auto_reload": True,
            "sync_enabled": False
        }
    
    async def start_server(self):
        """Start the development server."""
        app = web.Application()
        
        # Setup CORS
        cors = aiohttp_cors.setup(app, defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
                allow_methods="*"
            )
        })
        
        # Add routes
        app.router.add_get('/', self.serve_index)
        app.router.add_get('/ws', self.websocket_handler)
        app.router.add_get('/preview/{template}', self.serve_template_preview)
        app.router.add_static('/assets', self.theme_path / 'assets')
        app.router.add_static('/files', self.theme_path)
        
        # Add CORS to all routes
        for route in list(app.router.routes()):
            cors.add(route)
        
        # Start file watcher
        self.observer.start()
        
        print(f"🚀 Starting Shopify Theme Development Server")
        print(f"📁 Theme: {self.theme_path}")
        print(f"🌐 Server: http://localhost:{self.port}")
        print(f"🔄 Live Reload: {'Enabled' if self.config.get('auto_reload') else 'Disabled'}")
        
        if self.config.get("theme_id"):
            shopify_preview = f"https://{os.getenv('SHOPIFY_STORE_URL', 'one-head-hair.myshopify.com')}?preview_theme_id={self.config['theme_id']}"
            print(f"🔗 Shopify Preview: {shopify_preview}")
        
        print("\nPress Ctrl+C to stop the server")
        
        # Start server
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, 'localhost', self.port)
        await site.start()
        
        # Open browser
        webbrowser.open(f"http://localhost:{self.port}")
        
        try:
            # Keep server running
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\n⏹️  Stopping development server...")
        finally:
            self.observer.stop()
            self.observer.join()
            await runner.cleanup()
    
    async def serve_index(self, request):
        """Serve the main development interface."""
        html_content = await self._generate_dev_interface()
        return web.Response(text=html_content, content_type='text/html')
    
    async def serve_template_preview(self, request):
        """Serve a preview of a specific template."""
        template_name = request.match_info['template']
        template_path = self.theme_path / 'templates' / f"{template_name}.liquid"
        
        if not template_path.exists():
            return web.Response(text=f"Template not found: {template_name}", status=404)
        
        async with aiofiles.open(template_path, 'r') as f:
            template_content = await f.read()
        
        # Create a preview HTML page
        preview_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Preview: {template_name}</title>
    <link rel="stylesheet" href="/assets/theme.css">
    <style>
        .dev-preview-bar {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: #000;
            color: #fff;
            padding: 10px;
            font-family: monospace;
            z-index: 9999;
            font-size: 12px;
        }}
        .dev-preview-content {{
            margin-top: 50px;
        }}
    </style>
</head>
<body>
    <div class="dev-preview-bar">
        🎨 Template Preview: {template_name}.liquid | 
        <a href="/" style="color: #fff;">← Back to Dev Console</a>
    </div>
    <div class="dev-preview-content">
        <!-- Template content would be rendered here -->
        <pre style="background: #f5f5f5; padding: 20px; margin: 20px;">{template_content}</pre>
    </div>
    
    <script>
        // Live reload websocket
        const ws = new WebSocket('ws://localhost:{self.port}/ws');
        ws.onmessage = function(event) {{
            const data = JSON.parse(event.data);
            if (data.type === 'reload') {{
                location.reload();
            }}
        }};
    </script>
</body>
</html>
"""
        
        return web.Response(text=preview_html, content_type='text/html')
    
    async def websocket_handler(self, request):
        """Handle WebSocket connections for live reload."""
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        
        self.websockets.add(ws)
        print(f"🔌 WebSocket connected (total: {len(self.websockets)})")
        
        try:
            async for msg in ws:
                if msg.type == WSMsgType.TEXT:
                    data = json.loads(msg.data)
                    # Handle client messages if needed
                elif msg.type == WSMsgType.ERROR:
                    print(f'WebSocket error: {ws.exception()}')
        except Exception as e:
            print(f"WebSocket error: {e}")
        finally:
            self.websockets.discard(ws)
            print(f"🔌 WebSocket disconnected (total: {len(self.websockets)})")
        
        return ws
    
    async def broadcast_reload(self, file_path: str = None):
        """Broadcast reload message to all connected clients."""
        if not self.websockets:
            return
        
        message = {
            "type": "reload",
            "file": file_path,
            "timestamp": time.time()
        }
        
        # Remove closed websockets
        to_remove = set()
        for ws in self.websockets.copy():
            try:
                await ws.send_str(json.dumps(message))
            except Exception:
                to_remove.add(ws)
        
        for ws in to_remove:
            self.websockets.discard(ws)
        
        if file_path:
            print(f"🔄 Live reload triggered by: {file_path}")
    
    async def _generate_dev_interface(self):
        """Generate the main development interface HTML."""
        
        # Get theme file structure
        theme_files = self._get_theme_structure()
        
        # Get recent changes
        recent_files = self._get_recent_changes()
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Shopify Theme Development - {self.config.get('theme_name', 'Unknown Theme')}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f8f9fa;
            color: #333;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }}
        .header h1 {{ margin-bottom: 10px; }}
        .status {{
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 5px 15px;
            border-radius: 20px;
            margin: 0 10px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        .grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }}
        .card {{
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .card h2 {{
            color: #667eea;
            margin-bottom: 15px;
            font-size: 18px;
        }}
        .file-tree {{
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 5px;
            padding: 15px;
            max-height: 400px;
            overflow-y: auto;
        }}
        .file-item {{
            padding: 5px 0;
            font-family: monospace;
            font-size: 14px;
        }}
        .file-item.folder {{ color: #667eea; font-weight: bold; }}
        .file-item.file {{ color: #666; margin-left: 20px; }}
        .file-item.liquid {{ color: #e83e8c; }}
        .file-item.css {{ color: #17a2b8; }}
        .file-item.js {{ color: #ffc107; }}
        .recent-item {{
            padding: 10px;
            border: 1px solid #e9ecef;
            border-radius: 5px;
            margin-bottom: 10px;
            font-family: monospace;
            font-size: 14px;
        }}
        .toolbar {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}
        .btn {{
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            font-size: 14px;
            transition: all 0.3s;
        }}
        .btn-primary {{ background: #667eea; color: white; }}
        .btn-success {{ background: #28a745; color: white; }}
        .btn-info {{ background: #17a2b8; color: white; }}
        .btn-warning {{ background: #ffc107; color: #212529; }}
        .btn:hover {{ transform: translateY(-2px); }}
        .live-indicator {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: #28a745;
            color: white;
            padding: 10px 15px;
            border-radius: 5px;
            font-weight: bold;
            z-index: 1000;
        }}
        .live-indicator.disconnected {{
            background: #dc3545;
        }}
        @media (max-width: 768px) {{
            .grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="live-indicator" id="liveIndicator">🔴 Connecting...</div>
    
    <div class="header">
        <h1>🎨 Shopify Theme Development</h1>
        <div>
            <span class="status">📁 {self.config.get('theme_name', 'Unknown Theme')}</span>
            <span class="status">🆔 Theme ID: {self.config.get('theme_id', 'N/A')}</span>
            <span class="status">🔄 Live Reload: {'✅' if self.config.get('auto_reload') else '❌'}</span>
        </div>
    </div>
    
    <div class="container">
        <div class="card">
            <h2>⚡ Quick Actions</h2>
            <div class="toolbar">
                <a href="#" onclick="syncToShopify()" class="btn btn-primary">📤 Push to Shopify</a>
                <a href="#" onclick="pullFromShopify()" class="btn btn-info">📥 Pull from Shopify</a>
                <a href="#" onclick="openShopifyPreview()" class="btn btn-success">🔗 Open Shopify Preview</a>
                <a href="#" onclick="reloadFiles()" class="btn btn-warning">🔄 Reload File Tree</a>
            </div>
        </div>
        
        <div class="grid">
            <div class="card">
                <h2>📁 Theme Structure</h2>
                <div class="file-tree" id="fileTree">
                    {theme_files}
                </div>
            </div>
            
            <div class="card">
                <h2>⏱️ Recent Changes</h2>
                <div id="recentChanges">
                    {recent_files}
                </div>
            </div>
        </div>
        
        <div class="card">
            <h2>💡 Development Tips</h2>
            <ul style="margin-left: 20px; line-height: 1.6;">
                <li><strong>Live Reload:</strong> Save any file to automatically refresh the browser</li>
                <li><strong>Template Preview:</strong> Click on .liquid files to preview them</li>
                <li><strong>Sync Changes:</strong> Use "Push to Shopify" to upload your changes</li>
                <li><strong>Shopify Preview:</strong> Test changes on your actual store with preview mode</li>
                <li><strong>File Organization:</strong> Follow Shopify theme structure guidelines</li>
            </ul>
        </div>
    </div>
    
    <script>
        let ws;
        let reconnectAttempts = 0;
        const maxReconnectAttempts = 5;
        
        function connectWebSocket() {{
            ws = new WebSocket('ws://localhost:{self.port}/ws');
            
            ws.onopen = function() {{
                console.log('WebSocket connected');
                document.getElementById('liveIndicator').textContent = '🟢 Live Reload Active';
                document.getElementById('liveIndicator').className = 'live-indicator';
                reconnectAttempts = 0;
            }};
            
            ws.onmessage = function(event) {{
                const data = JSON.parse(event.data);
                if (data.type === 'reload') {{
                    console.log('Reloading due to file change:', data.file);
                    addRecentChange(data.file);
                    location.reload();
                }}
            }};
            
            ws.onclose = function() {{
                console.log('WebSocket disconnected');
                document.getElementById('liveIndicator').textContent = '🔴 Disconnected';
                document.getElementById('liveIndicator').className = 'live-indicator disconnected';
                
                // Try to reconnect
                if (reconnectAttempts < maxReconnectAttempts) {{
                    setTimeout(() => {{
                        reconnectAttempts++;
                        connectWebSocket();
                    }}, 2000);
                }}
            }};
            
            ws.onerror = function(error) {{
                console.log('WebSocket error:', error);
            }};
        }}
        
        function addRecentChange(filePath) {{
            const recentChanges = document.getElementById('recentChanges');
            const item = document.createElement('div');
            item.className = 'recent-item';
            item.innerHTML = `<strong>Modified:</strong> ${{filePath}} <small>(${{new Date().toLocaleTimeString()}})</small>`;
            recentChanges.insertBefore(item, recentChanges.firstChild);
            
            // Keep only last 10 items
            while (recentChanges.children.length > 10) {{
                recentChanges.removeChild(recentChanges.lastChild);
            }}
        }}
        
        function syncToShopify() {{
            alert('Sync functionality would trigger theme push to Shopify');
            // In a real implementation, this would call the sync API
        }}
        
        function pullFromShopify() {{
            alert('Pull functionality would download latest theme from Shopify');
            // In a real implementation, this would call the sync API
        }}
        
        function openShopifyPreview() {{
            const themeId = '{self.config.get("theme_id", "")}';
            const storeUrl = '{os.getenv("SHOPIFY_STORE_URL", "one-head-hair.myshopify.com")}';
            if (themeId) {{
                window.open(`https://${{storeUrl}}?preview_theme_id=${{themeId}}`, '_blank');
            }} else {{
                alert('No theme ID configured');
            }}
        }}
        
        function reloadFiles() {{
            location.reload();
        }}
        
        // Initialize WebSocket connection
        connectWebSocket();
    </script>
</body>
</html>
"""
        
        return html
    
    def _get_theme_structure(self):
        """Get HTML representation of theme file structure."""
        html_parts = []
        
        # Define theme directories in order
        directories = ['layout', 'templates', 'sections', 'snippets', 'assets', 'config', 'locales']
        
        for directory in directories:
            dir_path = self.theme_path / directory
            if dir_path.exists():
                html_parts.append(f'<div class="file-item folder">📁 {directory}/</div>')
                
                # List files in directory
                for file_path in sorted(dir_path.iterdir()):
                    if file_path.is_file():
                        file_class = "file"
                        if file_path.suffix == ".liquid":
                            file_class += " liquid"
                        elif file_path.suffix in [".css", ".scss"]:
                            file_class += " css"
                        elif file_path.suffix == ".js":
                            file_class += " js"
                        
                        html_parts.append(f'<div class="file-item {file_class}">📄 {file_path.name}</div>')
        
        return '\n'.join(html_parts) if html_parts else '<div class="file-item">No theme files found</div>'
    
    def _get_recent_changes(self):
        """Get HTML representation of recent file changes."""
        # This is a simplified version - in a real implementation,
        # you'd track actual file changes
        return '<div class="recent-item">No recent changes tracked yet</div>'


class ThemeFileWatcher(FileSystemEventHandler):
    """File system event handler for theme file changes."""
    
    def __init__(self, dev_server: ThemeDevServer):
        self.dev_server = dev_server
        self.last_reload = {}
    
    def on_modified(self, event):
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        
        # Skip certain files
        if any(skip in str(file_path) for skip in [
            ".git", "node_modules", ".dev_config.json", "__pycache__", 
            ".pyc", ".log", ".tmp", ".DS_Store"
        ]):
            return
        
        # Debounce rapid changes
        now = time.time()
        if file_path in self.last_reload and now - self.last_reload[file_path] < 1:
            return
        
        self.last_reload[file_path] = now
        
        # Get relative path
        try:
            relative_path = file_path.relative_to(self.dev_server.theme_path)
            # Trigger reload
            asyncio.create_task(self.dev_server.broadcast_reload(str(relative_path)))
        except ValueError:
            # File is outside theme directory
            pass


async def main():
    """Main function to start the development server."""
    import sys
    
    # Get theme path from command line or use current directory
    if len(sys.argv) > 1:
        theme_path = sys.argv[1]
    else:
        # Look for a theme directory
        current_dir = Path.cwd()
        if (current_dir / ".dev_config.json").exists():
            theme_path = str(current_dir)
        elif (current_dir / "themes" / "current_theme").exists():
            theme_path = str(current_dir / "themes" / "current_theme")
        else:
            print("❌ No theme directory found.")
            print("Usage: python3 theme_dev_server.py [theme_path]")
            print("Or run from a theme directory containing .dev_config.json")
            return
    
    # Get port from environment or use default
    port = int(os.getenv("DEV_SERVER_PORT", 3000))
    
    try:
        server = ThemeDevServer(theme_path, port)
        await server.start_server()
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except Exception as e:
        print(f"❌ Server error: {str(e)}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
