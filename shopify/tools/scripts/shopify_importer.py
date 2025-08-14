#!/usr/bin/env python3
"""
Comprehensive Shopify Data Importer
Imports products, collections, pages, themes, and other store data
"""

import os
import json
import asyncio
import httpx
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import zipfile
import tempfile
import time


class ShopifyImporter:
    """Main class for importing all Shopify store data."""
    
    def __init__(self, store_url: str = None, access_token: str = None):
        self.store_url = store_url or os.getenv("SHOPIFY_STORE_URL")
        self.access_token = access_token or os.getenv("SHOPIFY_ADMIN_API_ACCESS_TOKEN")
        
        if not self.store_url or not self.access_token:
            raise ValueError("Missing SHOPIFY_STORE_URL or SHOPIFY_ADMIN_API_ACCESS_TOKEN")
        
        # Ensure store URL has proper format
        if not self.store_url.startswith(("http://", "https://")):
            self.store_url = f"https://{self.store_url}"
        
        self.api_version = "2024-01"
        self.base_path = Path("/workspaces/automations_hub/shopify")
        self.data_path = self.base_path / "data" / "store_backups" / "imported_data"
        self.themes_path = self.base_path / "themes"
        
        # Create directories
        self.data_path.mkdir(exist_ok=True)
        self.themes_path.mkdir(exist_ok=True)
        
        self.headers = {
            "X-Shopify-Access-Token": self.access_token,
            "Content-Type": "application/json"
        }
    
    async def import_all(self):
        """Import all store data and themes."""
        print("🚀 Starting comprehensive Shopify import...")
        
        try:
            # Import store data
            await self.import_products()
            await self.import_collections()
            await self.import_pages()
            await self.import_blog_posts()
            await self.import_customers()
            await self.import_orders()
            await self.import_themes()
            
            # Generate summary
            await self.generate_import_summary()
            
            print("✅ Import completed successfully!")
            
        except Exception as e:
            print(f"❌ Import failed: {str(e)}")
            raise
    
    async def import_products(self):
        """Import all products with variants, images, and metafields."""
        print("📦 Importing products...")
        
        products_dir = self.data_path / "products"
        products_dir.mkdir(exist_ok=True)
        
        all_products = []
        page_info = None
        
        while True:
            url = f"{self.store_url}/admin/api/{self.api_version}/products.json"
            params = {"limit": 250}
            
            if page_info:
                params["page_info"] = page_info
            
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                
                data = response.json()
                products = data.get("products", [])
                
                if not products:
                    break
                
                all_products.extend(products)
                
                # Check for pagination
                link_header = response.headers.get("link")
                if link_header and "rel=\"next\"" in link_header:
                    # Extract page_info from link header
                    next_link = [link.strip() for link in link_header.split(",") if "rel=\"next\"" in link][0]
                    page_info = next_link.split("page_info=")[1].split("&")[0].split(">")[0]
                else:
                    break
        
        # Save products data
        with open(products_dir / "all_products.json", "w") as f:
            json.dump(all_products, f, indent=2)
        
        # Save individual product files
        for product in all_products:
            product_file = products_dir / f"product_{product['id']}.json"
            with open(product_file, "w") as f:
                json.dump(product, f, indent=2)
        
        print(f"✅ Imported {len(all_products)} products")
        return all_products
    
    async def import_collections(self):
        """Import all collections (smart and custom)."""
        print("📂 Importing collections...")
        
        collections_dir = self.data_path / "collections"
        collections_dir.mkdir(exist_ok=True)
        
        all_collections = []
        
        # Import smart collections
        smart_collections = await self._fetch_paginated("smart_collections")
        all_collections.extend(smart_collections)
        
        # Import custom collections
        custom_collections = await self._fetch_paginated("custom_collections")
        all_collections.extend(custom_collections)
        
        # Save collections data
        with open(collections_dir / "all_collections.json", "w") as f:
            json.dump(all_collections, f, indent=2)
        
        # Save individual collection files
        for collection in all_collections:
            collection_type = "smart" if "rules" in collection else "custom"
            collection_file = collections_dir / f"{collection_type}_collection_{collection['id']}.json"
            with open(collection_file, "w") as f:
                json.dump(collection, f, indent=2)
        
        print(f"✅ Imported {len(all_collections)} collections")
        return all_collections
    
    async def import_pages(self):
        """Import all pages."""
        print("📄 Importing pages...")
        
        pages_dir = self.data_path / "pages"
        pages_dir.mkdir(exist_ok=True)
        
        pages = await self._fetch_paginated("pages")
        
        # Save pages data
        with open(pages_dir / "all_pages.json", "w") as f:
            json.dump(pages, f, indent=2)
        
        # Save individual page files
        for page in pages:
            page_file = pages_dir / f"page_{page['id']}.json"
            with open(page_file, "w") as f:
                json.dump(page, f, indent=2)
            
            # Save page content as HTML
            if page.get("body_html"):
                html_file = pages_dir / f"page_{page['id']}.html"
                with open(html_file, "w") as f:
                    f.write(page["body_html"])
        
        print(f"✅ Imported {len(pages)} pages")
        return pages
    
    async def import_blog_posts(self):
        """Import all blog posts."""
        print("📝 Importing blog posts...")
        
        blogs_dir = self.data_path / "blogs"
        blogs_dir.mkdir(exist_ok=True)
        
        # First get all blogs
        blogs = await self._fetch_paginated("blogs")
        
        all_articles = []
        for blog in blogs:
            blog_id = blog["id"]
            articles = await self._fetch_paginated(f"blogs/{blog_id}/articles")
            
            for article in articles:
                article["blog_info"] = blog
                all_articles.append(article)
        
        # Save blog posts data
        with open(blogs_dir / "all_articles.json", "w") as f:
            json.dump(all_articles, f, indent=2)
        
        # Save individual article files
        for article in all_articles:
            article_file = blogs_dir / f"article_{article['id']}.json"
            with open(article_file, "w") as f:
                json.dump(article, f, indent=2)
            
            # Save article content as HTML
            if article.get("body_html"):
                html_file = blogs_dir / f"article_{article['id']}.html"
                with open(html_file, "w") as f:
                    f.write(article["body_html"])
        
        print(f"✅ Imported {len(all_articles)} blog posts from {len(blogs)} blogs")
        return all_articles
    
    async def import_customers(self):
        """Import customer data (without sensitive information)."""
        print("👥 Importing customers...")
        
        customers_dir = self.data_path / "customers"
        customers_dir.mkdir(exist_ok=True)
        
        customers = await self._fetch_paginated("customers")
        
        # Remove sensitive data
        safe_customers = []
        for customer in customers:
            safe_customer = {k: v for k, v in customer.items() 
                           if k not in ["email", "phone", "addresses"]}
            safe_customer["email_hash"] = hash(customer.get("email", ""))
            safe_customers.append(safe_customer)
        
        # Save customers data
        with open(customers_dir / "customers_summary.json", "w") as f:
            json.dump(safe_customers, f, indent=2)
        
        print(f"✅ Imported {len(safe_customers)} customers (anonymized)")
        return safe_customers
    
    async def import_orders(self):
        """Import order data (last 30 days for performance)."""
        print("🛒 Importing recent orders...")
        
        orders_dir = self.data_path / "orders"
        orders_dir.mkdir(exist_ok=True)
        
        # Get orders from last 30 days
        from datetime import timedelta
        thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat()
        
        orders = await self._fetch_paginated("orders", {"created_at_min": thirty_days_ago})
        
        # Save orders data
        with open(orders_dir / "recent_orders.json", "w") as f:
            json.dump(orders, f, indent=2)
        
        print(f"✅ Imported {len(orders)} recent orders")
        return orders
    
    async def import_themes(self):
        """Import only the current live theme."""
        print("🎨 Importing current live theme...")
        
        # Get all themes
        themes = await self._fetch_paginated("themes")
        
        # Find the live theme
        live_theme = next((t for t in themes if t.get("role") == "main"), None)
        
        if not live_theme:
            print("❌ No live theme found!")
            return []
        
        theme_id = live_theme["id"]
        theme_name = live_theme["name"]
        
        print(f"📥 Downloading live theme: {theme_name} (ID: {theme_id}) [LIVE]")
        
        # Create theme directory
        theme_dir = self.themes_path / f"live_theme_{theme_name}_{theme_id}"
        theme_dir.mkdir(exist_ok=True)
        
        # Save theme info
        with open(theme_dir / "theme_info.json", "w") as f:
            json.dump(live_theme, f, indent=2)
        
        # Download theme assets
        await self._download_theme_assets(theme_id, theme_dir)
        
        # Create a symlink to the live theme for easy access
        current_theme_link = self.themes_path / "current_theme"
        
        if current_theme_link.exists():
            current_theme_link.unlink()
        
        current_theme_link.symlink_to(theme_dir.name)
        
        print(f"✅ Imported live theme: {theme_name}")
        return [live_theme]
        
        print(f"✅ Imported live theme: {theme_name}")
        return [live_theme]
    
    async def _download_theme_assets(self, theme_id: int, theme_dir: Path):
        """Download all assets for a theme with rate limiting."""
        
        # Get theme assets
        url = f"{self.store_url}/admin/api/{self.api_version}/themes/{theme_id}/assets.json"
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            
            assets_data = response.json()
            assets = assets_data.get("assets", [])
            
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
                    await asyncio.sleep(0.5)  # 500ms delay between requests
                
                max_retries = 3
                for attempt in range(max_retries):
                    try:
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
    
    async def _fetch_paginated(self, endpoint: str, params: Dict = None) -> List[Dict]:
        """Fetch all data from a paginated endpoint."""
        all_data = []
        page_info = None
        
        if params is None:
            params = {}
        
        while True:
            url = f"{self.store_url}/admin/api/{self.api_version}/{endpoint}.json"
            request_params = {"limit": 250, **params}
            
            if page_info:
                request_params["page_info"] = page_info
            
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.get(url, headers=self.headers, params=request_params)
                response.raise_for_status()
                
                data = response.json()
                items = data.get(endpoint.split("/")[-1], [])
                
                if not items:
                    break
                
                all_data.extend(items)
                
                # Check for pagination
                link_header = response.headers.get("link")
                if link_header and "rel=\"next\"" in link_header:
                    # Extract page_info from link header
                    next_link = [link.strip() for link in link_header.split(",") if "rel=\"next\"" in link][0]
                    page_info = next_link.split("page_info=")[1].split("&")[0].split(">")[0]
                else:
                    break
        
        return all_data
    
    async def generate_import_summary(self):
        """Generate a summary of imported data."""
        print("📊 Generating import summary...")
        
        summary = {
            "import_date": datetime.now().isoformat(),
            "store_url": self.store_url,
            "data_summary": {}
        }
        
        # Count imported items
        for data_dir in self.data_path.iterdir():
            if data_dir.is_dir():
                files = list(data_dir.glob("*.json"))
                summary["data_summary"][data_dir.name] = len(files)
        
        # Count themes
        theme_dirs = [d for d in self.themes_path.iterdir() if d.is_dir()]
        summary["themes_count"] = len(theme_dirs)
        
        # Save summary
        with open(self.data_path / "import_summary.json", "w") as f:
            json.dump(summary, f, indent=2)
        
        print("📋 Import Summary:")
        for key, value in summary["data_summary"].items():
            print(f"  {key}: {value} items")
        print(f"  themes: {summary['themes_count']} themes")


async def main():
    """Main function to run the importer."""
    
    # Check environment variables
    store_url = os.getenv("SHOPIFY_STORE_URL")
    access_token = os.getenv("SHOPIFY_ADMIN_API_ACCESS_TOKEN")
    
    if not store_url:
        print("❌ Missing SHOPIFY_STORE_URL environment variable")
        print("Please set it to your store URL (e.g., 'your-store.myshopify.com')")
        return
    
    if not access_token:
        print("❌ Missing SHOPIFY_ADMIN_API_ACCESS_TOKEN environment variable")
        print("Please create a private app in your Shopify admin and set the access token")
        return
    
    print(f"🏪 Connecting to store: {store_url}")
    
    try:
        importer = ShopifyImporter(store_url, access_token)
        await importer.import_all()
        
        print("\n🎉 Import completed successfully!")
        print(f"📁 Data saved to: /workspaces/automations_hub/shopify/imported_data")
        print(f"🎨 Themes saved to: /workspaces/automations_hub/shopify/themes")
        print(f"🔗 Current live theme: /workspaces/automations_hub/shopify/themes/current_theme")
        
    except Exception as e:
        print(f"❌ Import failed: {str(e)}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
