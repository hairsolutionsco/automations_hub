"""Example integration of Shopify Agent features with existing workflows."""

import asyncio
import json
from typing import Dict, Any, List

# Import your existing MCP tools
from tools.shopify_agent import (
    shopify_search_catalog,
    shopify_update_cart,
    shopify_create_checkout,
    shopify_compliance_check
)

# Import your existing tools (examples)
# from tools.notion_api import create_notion_page
# from tools.n8n_workflows import trigger_workflow


async def ai_shopping_assistant_workflow(user_query: str, user_email: str) -> Dict[str, Any]:
    """
    Complete AI shopping assistant workflow using Shopify Agent features.
    
    This example shows how to:
    1. Search for products based on user intent
    2. Present options to the user
    3. Manage cart across multiple merchants
    4. Handle secure checkout
    5. Log the interaction in Notion
    """
    
    workflow_result = {
        "success": False,
        "steps": [],
        "cart_id": None,
        "checkout_url": None,
        "products_found": 0
    }
    
    try:
        # Step 1: Search catalog based on user query
        print(f"🔍 Searching catalog for: {user_query}")
        search_result = await shopify_search_catalog(
            query=user_query,
            ships_to="US",
            limit=5,
            context=f"User email: {user_email}, looking for products matching: {user_query}"
        )
        
        workflow_result["steps"].append({
            "step": "catalog_search",
            "status": "completed" if search_result.success else "failed",
            "message": search_result.message,
            "products_found": len(search_result.products or [])
        })
        
        if not search_result.success:
            return workflow_result
        
        workflow_result["products_found"] = len(search_result.products or [])
        
        # Step 2: Auto-select best matching product (AI logic here)
        if search_result.products:
            selected_product = search_result.products[0]  # For demo, select first
            print(f"🛍️ Selected product: {selected_product['title']}")
            
            # Step 3: Add to Universal Cart
            cart_items = [{
                "product_variant_id": selected_product["id"],
                "quantity": 1
            }]
            
            cart_result = await shopify_update_cart(
                add_items=cart_items,
                buyer_identity={"email": user_email}
            )
            
            workflow_result["steps"].append({
                "step": "add_to_cart",
                "status": "completed" if cart_result.success else "failed",
                "message": cart_result.message,
                "cart_id": cart_result.cart_id
            })
            
            if cart_result.success:
                workflow_result["cart_id"] = cart_result.cart_id
                workflow_result["checkout_url"] = cart_result.checkout_url
                
                # Step 4: Create branded checkout
                if cart_result.checkout_url:
                    checkout_result = await shopify_create_checkout(
                        checkout_url=cart_result.checkout_url,
                        branding_colors={
                            "primary": "#007bff",
                            "accent": "#28a745",
                            "background": "#ffffff"
                        }
                    )
                    
                    workflow_result["steps"].append({
                        "step": "create_checkout",
                        "status": "completed" if checkout_result.success else "failed",
                        "message": checkout_result.message
                    })
        
        # Step 5: Log interaction in Notion (if available)
        # Uncomment if you have Notion integration
        """
        try:
            notion_page = await create_notion_page(
                database_id="your_customer_interactions_db",
                properties={
                    "Customer Email": user_email,
                    "Query": user_query,
                    "Products Found": workflow_result["products_found"],
                    "Cart ID": workflow_result["cart_id"],
                    "Status": "Cart Created" if workflow_result["cart_id"] else "Search Only"
                }
            )
            
            workflow_result["steps"].append({
                "step": "log_to_notion",
                "status": "completed",
                "notion_page_id": notion_page.get("id")
            })
        except Exception as e:
            print(f"Warning: Could not log to Notion: {e}")
        """
        
        # Step 6: Trigger follow-up workflow in N8N (if needed)
        # Uncomment if you have N8N integration
        """
        try:
            await trigger_workflow(
                workflow_id="customer-shopping-followup",
                data={
                    "customer_email": user_email,
                    "cart_id": workflow_result["cart_id"],
                    "products_searched": user_query
                }
            )
            
            workflow_result["steps"].append({
                "step": "trigger_followup",
                "status": "completed"
            })
        except Exception as e:
            print(f"Warning: Could not trigger N8N workflow: {e}")
        """
        
        workflow_result["success"] = True
        return workflow_result
        
    except Exception as e:
        workflow_result["steps"].append({
            "step": "error",
            "status": "failed",
            "message": str(e)
        })
        return workflow_result


async def cross_platform_product_sync():
    """
    Example: Sync products between Shopify Catalog and your internal systems.
    """
    
    # Search for trending products
    trending_search = await shopify_search_catalog(
        query="trending products 2024",
        limit=10,
        context="Market research for product catalog expansion"
    )
    
    if trending_search.success and trending_search.products:
        print(f"Found {len(trending_search.products)} trending products")
        
        for product in trending_search.products:
            print(f"- {product['title']}: ${product['priceRange']['min']['amount']}")
            
            # Here you could:
            # 1. Add to your internal product database
            # 2. Create Notion pages for product research
            # 3. Trigger N8N workflows for price monitoring
            # 4. Update HubSpot with market data
    
    return trending_search


async def compliance_check_workflow():
    """
    Example: Automated compliance verification.
    """
    
    compliance_result = await shopify_compliance_check()
    
    if compliance_result["success"]:
        print("✅ All compliance requirements met:")
        for check_name, check_data in compliance_result["checks"].items():
            print(f"  - {check_name}: {check_data['status']}")
    
    return compliance_result


# Example usage
async def main():
    """
    Example usage of the Shopify Agent workflows.
    """
    
    print("🤖 Shopify Agent Workflow Examples")
    print("=" * 50)
    
    # Example 1: AI Shopping Assistant
    print("\n1. AI Shopping Assistant Workflow:")
    result = await ai_shopping_assistant_workflow(
        user_query="lightweight running shoes for marathon training",
        user_email="customer@example.com"
    )
    print(f"Success: {result['success']}")
    print(f"Products found: {result['products_found']}")
    print(f"Cart ID: {result['cart_id']}")
    
    # Example 2: Product Research
    print("\n2. Cross-Platform Product Sync:")
    sync_result = await cross_platform_product_sync()
    print(f"Sync completed: {sync_result.success}")
    
    # Example 3: Compliance Check
    print("\n3. Compliance Verification:")
    compliance = await compliance_check_workflow()
    print(f"Compliance status: {compliance.get('compliance_status', 'unknown')}")


if __name__ == "__main__":
    # Run the example workflows
    asyncio.run(main())
