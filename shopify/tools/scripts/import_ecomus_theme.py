#!/usr/bin/env python3
"""
Import specific Shopify theme - ecomus-v1-9-1-official
"""

import asyncio
import os
import json
import httpx
from pathlib import Path

async def import_ecomus_theme():
    """Import the ecomus-v1-9-1-official theme specifically."""
    
    store_url = os.getenv("SHOPIFY_STORE_URL")
    access_token = os.getenv("SHOPIFY_ADMIN_API_ACCESS_TOKEN")
    
    if not store_url or not access_token:
        print("❌ Missing environment variables")
        return
    
    if not store_url.startswith(("http://", "https://")):
        store_url = f"https://{store_url}"
    
    headers = {
        "X-Shopify-Access-Token": access_token,
        "Content-Type": "application/json"
    }
    
    api_version = "2024-01"
    themes_path = Path("/workspaces/automations_hub/shopify/themes")
    themes_path.mkdir(exist_ok=True)
    
    print(f"🏪 Connecting to store: {store_url}")
    print("🎨 Looking for ecomus-v1-9-1-official theme...")
    
    # Get all themes
    url = f"{store_url}/admin/api/{api_version}/themes.json"
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        
        themes_data = response.json()
        themes = themes_data.get("themes", [])
        
        # Find the ecomus theme
        ecomus_theme = None
        for theme in themes:
            if "ecomus" in theme["name"].lower():
                ecomus_theme = theme
                break
        
        if not ecomus_theme:
            print("❌ Could not find ecomus theme. Available themes:")
            for theme in themes:
                role = " [LIVE]" if theme.get("role") == "main" else ""
                print(f"  - {theme['name']} (ID: {theme['id']}){role}")
            return
        
        theme_id = ecomus_theme["id"]
        theme_name = ecomus_theme["name"]
        is_live = ecomus_theme.get("role") == "main"
        
        print(f"📥 Found theme: {theme_name} (ID: {theme_id})" + (" [LIVE]" if is_live else ""))
        
        # Create theme directory
        theme_dir = themes_path / f"ecomus_theme_{theme_id}"
        if is_live:
            theme_dir = themes_path / f"live_ecomus_theme_{theme_id}"
        
        theme_dir.mkdir(exist_ok=True)
        
        # Save theme info
        with open(theme_dir / "theme_info.json", "w") as f:
            json.dump(ecomus_theme, f, indent=2)
        
        # Get theme assets
        assets_url = f"{store_url}/admin/api/{api_version}/themes/{theme_id}/assets.json"
        assets_response = await client.get(assets_url, headers=headers)
        assets_response.raise_for_status()
        
        assets_data = assets_response.json()
        assets = assets_data.get("assets", [])
        
        print(f"📦 Downloading {len(assets)} theme assets...")
        
        # Create asset directories
        (theme_dir / "templates").mkdir(exist_ok=True)
        (theme_dir / "sections").mkdir(exist_ok=True)
        (theme_dir / "snippets").mkdir(exist_ok=True)
        (theme_dir / "layout").mkdir(exist_ok=True)
        (theme_dir / "assets").mkdir(exist_ok=True)
        (theme_dir / "config").mkdir(exist_ok=True)
        (theme_dir / "locales").mkdir(exist_ok=True)
        
        # Download each asset with rate limiting
        for i, asset in enumerate(assets):
            asset_key = asset["key"]
            print(f"  📄 Downloading: {asset_key} ({i+1}/{len(assets)})")
            
            # Add delay between requests to avoid rate limiting
            if i > 0:
                await asyncio.sleep(0.5)  # 500ms delay
            
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    # Get asset content
                    asset_url = f"{store_url}/admin/api/{api_version}/themes/{theme_id}/assets.json"
                    params = {"asset[key]": asset_key}
                    
                    asset_response = await client.get(asset_url, headers=headers, params=params)
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
                        import base64
                        with open(file_path, "wb") as f:
                            f.write(base64.b64decode(asset_content["attachment"]))
                    
                    break  # Success, exit retry loop
                    
                except httpx.HTTPStatusError as e:
                    if e.response.status_code == 429:  # Rate limited
                        retry_after = int(e.response.headers.get("Retry-After", 2))
                        print(f"    ⏳ Rate limited, waiting {retry_after} seconds...")
                        await asyncio.sleep(retry_after)
                        if attempt == max_retries - 1:
                            print(f"    ⚠️  Skipping {asset_key} after {max_retries} attempts")
                    else:
                        raise
        
        # Create a symlink to the theme for easy access
        current_theme_link = themes_path / "current_theme"
        
        if current_theme_link.exists():
            current_theme_link.unlink()
        
        current_theme_link.symlink_to(theme_dir.name)
        
        print(f"✅ Successfully downloaded ecomus theme!")
        print(f"📁 Theme saved to: {theme_dir}")
        print(f"🔗 Symlink created: {current_theme_link}")
        
        if is_live:
            print("🟢 This is your LIVE theme")

if __name__ == "__main__":
    asyncio.run(import_ecomus_theme())
