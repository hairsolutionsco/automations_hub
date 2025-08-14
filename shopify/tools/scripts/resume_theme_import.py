#!/usr/bin/env python3
"""
Resume Theme Import - Import only themes with rate limiting
"""

import asyncio
from shopify_importer import ShopifyImporter
import os

async def main():
    """Resume theme import only."""
    
    store_url = os.getenv("SHOPIFY_STORE_URL")
    access_token = os.getenv("SHOPIFY_ADMIN_API_ACCESS_TOKEN")
    
    if not store_url or not access_token:
        print("❌ Missing environment variables")
        return
    
    print(f"🏪 Connecting to store: {store_url}")
    print("🎨 Resuming theme import with rate limiting...")
    
    try:
        importer = ShopifyImporter(store_url, access_token)
        await importer.import_themes()
        await importer.generate_import_summary()
        
        print("\n🎉 Theme import completed successfully!")
        print(f"🎨 Themes saved to: /workspaces/automations_hub/shopify/themes")
        print(f"🔗 Current live theme: /workspaces/automations_hub/shopify/themes/current_theme")
        
    except Exception as e:
        print(f"❌ Theme import failed: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
