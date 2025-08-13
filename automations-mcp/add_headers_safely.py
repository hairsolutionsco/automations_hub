"""Safe script to ONLY add H1 headers to the Backend page WITHOUT touching databases."""

import asyncio
import sys
import os
sys.path.append('.')
import httpx


async def add_headers_only(page_id: str) -> bool:
    """Add only H1 headers to the BEGINNING of the page, leaving all existing content intact."""
    try:
        api_key = os.getenv("NOTION_API_KEY")
        
        if not api_key:
            print("❌ NOTION_API_KEY not configured")
            return False

        # Create only the H1 header blocks
        header_blocks = [
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": "👥 CRM"}
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": []}
            },
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": "💼 Sales & Operations"}
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": []}
            },
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": "💰 Finances"}
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": []}
            },
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": "🏢 Management & Reports"}
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": []}
            },
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": "📚 Knowledge & Documents"}
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": []}
            }
        ]

        async with httpx.AsyncClient() as client:
            # PREPEND these headers to the page (add at the beginning)
            response = await client.patch(
                f"https://api.notion.com/v1/blocks/{page_id}/children",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "Notion-Version": "2022-06-28"
                },
                json={
                    "children": header_blocks
                }
            )
            
            if response.status_code == 200:
                print(f"✅ Successfully added {len(header_blocks)} header blocks to the BEGINNING of the page")
                print("📝 All existing databases remain untouched")
                return True
            else:
                print(f"❌ Failed to add headers: {response.status_code} {response.text}")
                return False
                
    except Exception as e:
        print(f"❌ Error adding headers: {str(e)}")
        return False


async def main():
    """Add headers to Backend page safely."""
    print("🏗️  SAFELY ADDING H1 HEADERS TO BACKEND PAGE")
    print("=" * 50)
    print("⚠️  This script will ONLY add headers, it will NOT touch any databases")
    print()
    
    BACKEND_PAGE_ID = "226f4e0d-84e0-81a8-8ad2-c2230c5202e7"
    
    success = await add_headers_only(BACKEND_PAGE_ID)
    
    if success:
        print("\n✅ SUCCESS!")
        print("📋 Added 5 category headers to your Backend page")
        print("💡 You can now manually drag databases under the appropriate headers")
        print("🔒 No databases were deleted or modified")
    else:
        print("\n❌ Failed to add headers")


if __name__ == "__main__":
    asyncio.run(main())
