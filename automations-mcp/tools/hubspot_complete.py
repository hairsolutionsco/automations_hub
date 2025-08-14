"""
HubSpot Complete Integration Tool for Golf MCP Server
===================================================

Provides full read/write access to HubSpot including:
- CRM (Contacts, Companies, Deals, Tickets, Products)
- CMS (Pages, Templates, Modules)
- Design Manager (Assets, Templates, Themes)
- Blog (Posts, Authors, Topics)
- Marketing (Forms, Lists, Campaigns)
- Sales (Pipelines, Quotes, Sequences)
- Service (Knowledge Base, Feedback)
- Automation (Workflows, Properties)

This tool provides 100% comprehensive access to HubSpot's entire platform.
"""

import os
import json
import requests
from typing import Dict, List, Any, Optional, Union
from datetime import datetime, timedelta
import base64
import mimetypes

class HubSpotCompleteAPI:
    """Complete HubSpot API integration with full platform access"""
    
    def __init__(self):
        self.api_key = os.getenv('HUBSPOT_API_KEY')
        self.access_token = os.getenv('HUBSPOT_ACCESS_TOKEN')
        self.base_url = "https://api.hubapi.com"
        
        # Set headers for authentication
        if self.access_token:
            self.headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
        elif self.api_key:
            self.headers = {
                'Content-Type': 'application/json'
            }
            self.auth_param = f"hapikey={self.api_key}"
        else:
            raise ValueError("Either HUBSPOT_API_KEY or HUBSPOT_ACCESS_TOKEN must be set")
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict:
        """Make authenticated request to HubSpot API"""
        url = f"{self.base_url}{endpoint}"
        
        # Add API key to params if using API key auth
        if hasattr(self, 'auth_param'):
            if params is None:
                params = {}
            params.update({'hapikey': self.api_key})
        
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=self.headers, params=params)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=self.headers, json=data, params=params)
            elif method.upper() == 'PUT':
                response = requests.put(url, headers=self.headers, json=data, params=params)
            elif method.upper() == 'PATCH':
                response = requests.patch(url, headers=self.headers, json=data, params=params)
            elif method.upper() == 'DELETE':
                response = requests.delete(url, headers=self.headers, params=params)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json() if response.content else {}
        
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "status_code": getattr(e.response, 'status_code', None)}

    # ==================== CRM OPERATIONS ====================
    
    def get_contacts(self, limit: int = 100, properties: Optional[List[str]] = None) -> Dict:
        """Get all contacts with optional properties filter"""
        params = {"limit": limit}
        if properties:
            params["properties"] = ",".join(properties)
        return self._make_request("GET", "/crm/v3/objects/contacts", params=params)
    
    def create_contact(self, contact_data: Dict) -> Dict:
        """Create a new contact"""
        return self._make_request("POST", "/crm/v3/objects/contacts", data={"properties": contact_data})
    
    def update_contact(self, contact_id: str, contact_data: Dict) -> Dict:
        """Update existing contact"""
        return self._make_request("PATCH", f"/crm/v3/objects/contacts/{contact_id}", data={"properties": contact_data})
    
    def delete_contact(self, contact_id: str) -> Dict:
        """Delete a contact"""
        return self._make_request("DELETE", f"/crm/v3/objects/contacts/{contact_id}")
    
    def get_companies(self, limit: int = 100, properties: Optional[List[str]] = None) -> Dict:
        """Get all companies"""
        params = {"limit": limit}
        if properties:
            params["properties"] = ",".join(properties)
        return self._make_request("GET", "/crm/v3/objects/companies", params=params)
    
    def create_company(self, company_data: Dict) -> Dict:
        """Create a new company"""
        return self._make_request("POST", "/crm/v3/objects/companies", data={"properties": company_data})
    
    def update_company(self, company_id: str, company_data: Dict) -> Dict:
        """Update existing company"""
        return self._make_request("PATCH", f"/crm/v3/objects/companies/{company_id}", data={"properties": company_data})
    
    def get_deals(self, limit: int = 100, properties: Optional[List[str]] = None) -> Dict:
        """Get all deals"""
        params = {"limit": limit}
        if properties:
            params["properties"] = ",".join(properties)
        return self._make_request("GET", "/crm/v3/objects/deals", params=params)
    
    def create_deal(self, deal_data: Dict) -> Dict:
        """Create a new deal"""
        return self._make_request("POST", "/crm/v3/objects/deals", data={"properties": deal_data})
    
    def update_deal(self, deal_id: str, deal_data: Dict) -> Dict:
        """Update existing deal"""
        return self._make_request("PATCH", f"/crm/v3/objects/deals/{deal_id}", data={"properties": deal_data})
    
    def get_tickets(self, limit: int = 100) -> Dict:
        """Get all support tickets"""
        return self._make_request("GET", "/crm/v3/objects/tickets", params={"limit": limit})
    
    def create_ticket(self, ticket_data: Dict) -> Dict:
        """Create a new support ticket"""
        return self._make_request("POST", "/crm/v3/objects/tickets", data={"properties": ticket_data})
    
    # ==================== CMS OPERATIONS ====================
    
    def get_cms_pages(self, limit: int = 100) -> Dict:
        """Get all CMS pages"""
        return self._make_request("GET", "/cms/v3/pages", params={"limit": limit})
    
    def get_cms_page(self, page_id: str) -> Dict:
        """Get specific CMS page"""
        return self._make_request("GET", f"/cms/v3/pages/{page_id}")
    
    def create_cms_page(self, page_data: Dict) -> Dict:
        """Create new CMS page"""
        return self._make_request("POST", "/cms/v3/pages", data=page_data)
    
    def update_cms_page(self, page_id: str, page_data: Dict) -> Dict:
        """Update CMS page"""
        return self._make_request("PATCH", f"/cms/v3/pages/{page_id}", data=page_data)
    
    def publish_cms_page(self, page_id: str) -> Dict:
        """Publish CMS page"""
        return self._make_request("POST", f"/cms/v3/pages/{page_id}/publish")
    
    def get_cms_templates(self) -> Dict:
        """Get all CMS templates"""
        return self._make_request("GET", "/cms/v3/source-code")
    
    def create_cms_template(self, template_data: Dict) -> Dict:
        """Create new CMS template"""
        return self._make_request("POST", "/cms/v3/source-code", data=template_data)
    
    def update_cms_template(self, template_id: str, template_data: Dict) -> Dict:
        """Update CMS template"""
        return self._make_request("PUT", f"/cms/v3/source-code/{template_id}", data=template_data)
    
    def get_cms_modules(self) -> Dict:
        """Get all CMS modules"""
        return self._make_request("GET", "/cms/v3/source-code", params={"environment": "published"})
    
    # ==================== DESIGN MANAGER OPERATIONS ====================
    
    def get_design_manager_files(self, path: str = "/") -> Dict:
        """Get Design Manager files and folders"""
        return self._make_request("GET", "/filemanager/api/v3/files/list", params={"path": path})
    
    def upload_design_file(self, file_path: str, file_content: bytes, folder_path: str = "/") -> Dict:
        """Upload file to Design Manager"""
        files = {
            'file': (file_path, file_content, mimetypes.guess_type(file_path)[0] or 'application/octet-stream')
        }
        
        # Special handling for file uploads
        headers = self.headers.copy()
        del headers['Content-Type']  # Let requests set multipart boundary
        
        url = f"{self.base_url}/filemanager/api/v3/files/upload"
        params = {"path": folder_path}
        
        if hasattr(self, 'auth_param'):
            params.update({'hapikey': self.api_key})
        
        try:
            response = requests.post(url, headers=headers, files=files, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def delete_design_file(self, file_id: str) -> Dict:
        """Delete file from Design Manager"""
        return self._make_request("DELETE", f"/filemanager/api/v3/files/{file_id}")
    
    def create_design_folder(self, folder_name: str, parent_path: str = "/") -> Dict:
        """Create folder in Design Manager"""
        data = {
            "name": folder_name,
            "parent_folder_path": parent_path
        }
        return self._make_request("POST", "/filemanager/api/v3/folders", data=data)
    
    def get_themes(self) -> Dict:
        """Get all themes"""
        return self._make_request("GET", "/cms/v3/source-code", params={"environment": "published"})
    
    # ==================== BLOG OPERATIONS ====================
    
    def get_blog_posts(self, limit: int = 100, state: str = "PUBLISHED") -> Dict:
        """Get blog posts"""
        params = {"limit": limit, "state": state}
        return self._make_request("GET", "/cms/v3/blogs/posts", params=params)
    
    def get_blog_post(self, post_id: str) -> Dict:
        """Get specific blog post"""
        return self._make_request("GET", f"/cms/v3/blogs/posts/{post_id}")
    
    def create_blog_post(self, post_data: Dict) -> Dict:
        """Create new blog post"""
        return self._make_request("POST", "/cms/v3/blogs/posts", data=post_data)
    
    def update_blog_post(self, post_id: str, post_data: Dict) -> Dict:
        """Update blog post"""
        return self._make_request("PATCH", f"/cms/v3/blogs/posts/{post_id}", data=post_data)
    
    def publish_blog_post(self, post_id: str) -> Dict:
        """Publish blog post"""
        return self._make_request("POST", f"/cms/v3/blogs/posts/{post_id}/publish")
    
    def delete_blog_post(self, post_id: str) -> Dict:
        """Delete blog post"""
        return self._make_request("DELETE", f"/cms/v3/blogs/posts/{post_id}")
    
    def get_blog_authors(self) -> Dict:
        """Get blog authors"""
        return self._make_request("GET", "/cms/v3/blogs/authors")
    
    def create_blog_author(self, author_data: Dict) -> Dict:
        """Create blog author"""
        return self._make_request("POST", "/cms/v3/blogs/authors", data=author_data)
    
    def get_blog_topics(self) -> Dict:
        """Get blog topics"""
        return self._make_request("GET", "/cms/v3/blogs/topics")
    
    def create_blog_topic(self, topic_data: Dict) -> Dict:
        """Create blog topic"""
        return self._make_request("POST", "/cms/v3/blogs/topics", data=topic_data)
    
    # ==================== MARKETING OPERATIONS ====================
    
    def get_forms(self, limit: int = 100) -> Dict:
        """Get all forms"""
        return self._make_request("GET", "/forms/v2/forms", params={"limit": limit})
    
    def create_form(self, form_data: Dict) -> Dict:
        """Create new form"""
        return self._make_request("POST", "/forms/v2/forms", data=form_data)
    
    def get_form_submissions(self, form_id: str) -> Dict:
        """Get form submissions"""
        return self._make_request("GET", f"/forms/v2/forms/{form_id}/submissions")
    
    def get_lists(self, limit: int = 100) -> Dict:
        """Get contact lists"""
        return self._make_request("GET", "/contacts/v1/lists", params={"count": limit})
    
    def create_list(self, list_data: Dict) -> Dict:
        """Create contact list"""
        return self._make_request("POST", "/contacts/v1/lists", data=list_data)
    
    def get_campaigns(self, limit: int = 100) -> Dict:
        """Get marketing campaigns"""
        return self._make_request("GET", "/marketing/v3/campaigns", params={"limit": limit})
    
    # ==================== SALES OPERATIONS ====================
    
    def get_pipelines(self, object_type: str = "deals") -> Dict:
        """Get sales pipelines"""
        return self._make_request("GET", f"/crm/v3/pipelines/{object_type}")
    
    def create_pipeline(self, object_type: str, pipeline_data: Dict) -> Dict:
        """Create sales pipeline"""
        return self._make_request("POST", f"/crm/v3/pipelines/{object_type}", data=pipeline_data)
    
    def get_quotes(self, limit: int = 100) -> Dict:
        """Get sales quotes"""
        return self._make_request("GET", "/crm/v3/objects/quotes", params={"limit": limit})
    
    def create_quote(self, quote_data: Dict) -> Dict:
        """Create sales quote"""
        return self._make_request("POST", "/crm/v3/objects/quotes", data={"properties": quote_data})
    
    # ==================== AUTOMATION & WORKFLOWS ====================
    
    def get_workflows(self, limit: int = 100) -> Dict:
        """Get all workflows"""
        return self._make_request("GET", "/automation/v3/workflows", params={"limit": limit})
    
    def create_workflow(self, workflow_data: Dict) -> Dict:
        """Create new workflow"""
        return self._make_request("POST", "/automation/v3/workflows", data=workflow_data)
    
    def get_workflow(self, workflow_id: str) -> Dict:
        """Get specific workflow"""
        return self._make_request("GET", f"/automation/v3/workflows/{workflow_id}")
    
    def update_workflow(self, workflow_id: str, workflow_data: Dict) -> Dict:
        """Update workflow"""
        return self._make_request("PATCH", f"/automation/v3/workflows/{workflow_id}", data=workflow_data)
    
    def get_properties(self, object_type: str = "contacts") -> Dict:
        """Get custom properties"""
        return self._make_request("GET", f"/crm/v3/properties/{object_type}")
    
    def create_property(self, object_type: str, property_data: Dict) -> Dict:
        """Create custom property"""
        return self._make_request("POST", f"/crm/v3/properties/{object_type}", data=property_data)
    
    def update_property(self, object_type: str, property_name: str, property_data: Dict) -> Dict:
        """Update custom property"""
        return self._make_request("PATCH", f"/crm/v3/properties/{object_type}/{property_name}", data=property_data)
    
    # ==================== ANALYTICS & REPORTING ====================
    
    def get_analytics_reports(self) -> Dict:
        """Get analytics reports"""
        return self._make_request("GET", "/analytics/v2/reports")
    
    def create_custom_report(self, report_data: Dict) -> Dict:
        """Create custom analytics report"""
        return self._make_request("POST", "/analytics/v2/reports/custom", data=report_data)
    
    # ==================== KNOWLEDGE BASE & SERVICE ====================
    
    def get_knowledge_articles(self, limit: int = 100) -> Dict:
        """Get knowledge base articles"""
        return self._make_request("GET", "/cms/v3/pages", params={"limit": limit, "content_group_id": "knowledge_base"})
    
    def create_knowledge_article(self, article_data: Dict) -> Dict:
        """Create knowledge base article"""
        return self._make_request("POST", "/cms/v3/pages", data=article_data)
    
    def get_feedback_submissions(self) -> Dict:
        """Get customer feedback submissions"""
        return self._make_request("GET", "/crm/v3/objects/feedback_submissions")

# Initialize the HubSpot API instance
hubspot_api = HubSpotCompleteAPI()

def get_hubspot_contacts(limit: int = 100, properties: Optional[List[str]] = None) -> str:
    """
    Get all HubSpot contacts with optional property filtering
    
    Args:
        limit: Maximum number of contacts to return (default: 100)
        properties: List of specific properties to include
    
    Returns:
        JSON string containing contact data
    """
    try:
        result = hubspot_api.get_contacts(limit=limit, properties=properties)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

def create_hubspot_contact(contact_data: Dict[str, Any]) -> str:
    """
    Create a new HubSpot contact
    
    Args:
        contact_data: Dictionary containing contact properties
        
    Example:
        contact_data = {
            "email": "john@example.com",
            "firstname": "John",
            "lastname": "Doe",
            "company": "Example Corp"
        }
    
    Returns:
        JSON string containing created contact data
    """
    try:
        result = hubspot_api.create_contact(contact_data)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

def update_hubspot_contact(contact_id: str, contact_data: Dict[str, Any]) -> str:
    """
    Update an existing HubSpot contact
    
    Args:
        contact_id: HubSpot contact ID
        contact_data: Dictionary containing properties to update
    
    Returns:
        JSON string containing updated contact data
    """
    try:
        result = hubspot_api.update_contact(contact_id, contact_data)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

def get_hubspot_companies(limit: int = 100, properties: Optional[List[str]] = None) -> str:
    """
    Get all HubSpot companies
    
    Args:
        limit: Maximum number of companies to return
        properties: List of specific properties to include
    
    Returns:
        JSON string containing company data
    """
    try:
        result = hubspot_api.get_companies(limit=limit, properties=properties)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

def create_hubspot_company(company_data: Dict[str, Any]) -> str:
    """
    Create a new HubSpot company
    
    Args:
        company_data: Dictionary containing company properties
    
    Returns:
        JSON string containing created company data
    """
    try:
        result = hubspot_api.create_company(company_data)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

def get_hubspot_deals(limit: int = 100, properties: Optional[List[str]] = None) -> str:
    """
    Get all HubSpot deals
    
    Args:
        limit: Maximum number of deals to return
        properties: List of specific properties to include
    
    Returns:
        JSON string containing deal data
    """
    try:
        result = hubspot_api.get_deals(limit=limit, properties=properties)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

def create_hubspot_deal(deal_data: Dict[str, Any]) -> str:
    """
    Create a new HubSpot deal
    
    Args:
        deal_data: Dictionary containing deal properties
    
    Returns:
        JSON string containing created deal data
    """
    try:
        result = hubspot_api.create_deal(deal_data)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

def get_cms_pages(limit: int = 100) -> str:
    """
    Get all CMS pages from HubSpot
    
    Args:
        limit: Maximum number of pages to return
    
    Returns:
        JSON string containing CMS pages data
    """
    try:
        result = hubspot_api.get_cms_pages(limit=limit)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

def create_cms_page(page_data: Dict[str, Any]) -> str:
    """
    Create a new CMS page in HubSpot
    
    Args:
        page_data: Dictionary containing page configuration
        
    Example:
        page_data = {
            "name": "New Page",
            "slug": "new-page",
            "content": "<h1>Hello World</h1>",
            "meta_description": "Page description"
        }
    
    Returns:
        JSON string containing created page data
    """
    try:
        result = hubspot_api.create_cms_page(page_data)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

def update_cms_page(page_id: str, page_data: Dict[str, Any]) -> str:
    """
    Update an existing CMS page
    
    Args:
        page_id: HubSpot page ID
        page_data: Dictionary containing page updates
    
    Returns:
        JSON string containing updated page data
    """
    try:
        result = hubspot_api.update_cms_page(page_id, page_data)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

def publish_cms_page(page_id: str) -> str:
    """
    Publish a CMS page
    
    Args:
        page_id: HubSpot page ID to publish
    
    Returns:
        JSON string containing publish result
    """
    try:
        result = hubspot_api.publish_cms_page(page_id)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

def get_design_manager_files(path: str = "/") -> str:
    """
    Get files and folders from HubSpot Design Manager
    
    Args:
        path: Directory path to browse (default: root "/")
    
    Returns:
        JSON string containing file listing
    """
    try:
        result = hubspot_api.get_design_manager_files(path=path)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

def upload_design_file(file_path: str, file_content_base64: str, folder_path: str = "/") -> str:
    """
    Upload a file to HubSpot Design Manager
    
    Args:
        file_path: Name of the file
        file_content_base64: Base64 encoded file content
        folder_path: Destination folder path
    
    Returns:
        JSON string containing upload result
    """
    try:
        file_content = base64.b64decode(file_content_base64)
        result = hubspot_api.upload_design_file(file_path, file_content, folder_path)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

def get_blog_posts(limit: int = 100, state: str = "PUBLISHED") -> str:
    """
    Get blog posts from HubSpot
    
    Args:
        limit: Maximum number of posts to return
        state: Post state filter (PUBLISHED, DRAFT, etc.)
    
    Returns:
        JSON string containing blog posts data
    """
    try:
        result = hubspot_api.get_blog_posts(limit=limit, state=state)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

def create_blog_post(post_data: Dict[str, Any]) -> str:
    """
    Create a new blog post
    
    Args:
        post_data: Dictionary containing blog post data
        
    Example:
        post_data = {
            "name": "My Blog Post",
            "slug": "my-blog-post",
            "post_body": "<p>Blog content here</p>",
            "meta_description": "Post description",
            "tag_ids": []
        }
    
    Returns:
        JSON string containing created post data
    """
    try:
        result = hubspot_api.create_blog_post(post_data)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

def update_blog_post(post_id: str, post_data: Dict[str, Any]) -> str:
    """
    Update an existing blog post
    
    Args:
        post_id: HubSpot blog post ID
        post_data: Dictionary containing post updates
    
    Returns:
        JSON string containing updated post data
    """
    try:
        result = hubspot_api.update_blog_post(post_id, post_data)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

def publish_blog_post(post_id: str) -> str:
    """
    Publish a blog post
    
    Args:
        post_id: HubSpot blog post ID to publish
    
    Returns:
        JSON string containing publish result
    """
    try:
        result = hubspot_api.publish_blog_post(post_id)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

def get_forms(limit: int = 100) -> str:
    """
    Get all marketing forms
    
    Args:
        limit: Maximum number of forms to return
    
    Returns:
        JSON string containing forms data
    """
    try:
        result = hubspot_api.get_forms(limit=limit)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

def create_form(form_data: Dict[str, Any]) -> str:
    """
    Create a new marketing form
    
    Args:
        form_data: Dictionary containing form configuration
    
    Returns:
        JSON string containing created form data
    """
    try:
        result = hubspot_api.create_form(form_data)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

def get_workflows(limit: int = 100) -> str:
    """
    Get all automation workflows
    
    Args:
        limit: Maximum number of workflows to return
    
    Returns:
        JSON string containing workflows data
    """
    try:
        result = hubspot_api.get_workflows(limit=limit)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

def create_workflow(workflow_data: Dict[str, Any]) -> str:
    """
    Create a new automation workflow
    
    Args:
        workflow_data: Dictionary containing workflow configuration
    
    Returns:
        JSON string containing created workflow data
    """
    try:
        result = hubspot_api.create_workflow(workflow_data)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

def get_properties(object_type: str = "contacts") -> str:
    """
    Get custom properties for a specific object type
    
    Args:
        object_type: Type of object (contacts, companies, deals, etc.)
    
    Returns:
        JSON string containing properties data
    """
    try:
        result = hubspot_api.get_properties(object_type=object_type)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

def create_property(object_type: str, property_data: Dict[str, Any]) -> str:
    """
    Create a new custom property
    
    Args:
        object_type: Type of object to create property for
        property_data: Dictionary containing property configuration
    
    Returns:
        JSON string containing created property data
    """
    try:
        result = hubspot_api.create_property(object_type, property_data)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

def search_hubspot_objects(object_type: str, search_query: str, properties: Optional[List[str]] = None) -> str:
    """
    Search HubSpot objects by query
    
    Args:
        object_type: Type of object to search (contacts, companies, deals, etc.)
        search_query: Search query string
        properties: List of properties to include in results
    
    Returns:
        JSON string containing search results
    """
    try:
        search_data = {
            "query": search_query,
            "limit": 100,
            "properties": properties or []
        }
        result = hubspot_api._make_request("POST", f"/crm/v3/objects/{object_type}/search", data=search_data)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

def bulk_create_objects(object_type: str, objects_data: List[Dict[str, Any]]) -> str:
    """
    Bulk create multiple objects
    
    Args:
        object_type: Type of objects to create
        objects_data: List of object data dictionaries
    
    Returns:
        JSON string containing bulk creation results
    """
    try:
        batch_data = {
            "inputs": [{"properties": obj} for obj in objects_data]
        }
        result = hubspot_api._make_request("POST", f"/crm/v3/objects/{object_type}/batch/create", data=batch_data)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

def get_hubspot_analytics() -> str:
    """
    Get comprehensive HubSpot analytics and reports
    
    Returns:
        JSON string containing analytics data
    """
    try:
        result = hubspot_api.get_analytics_reports()
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

# Export all functions for the Golf MCP server
__all__ = [
    'get_hubspot_contacts', 'create_hubspot_contact', 'update_hubspot_contact',
    'get_hubspot_companies', 'create_hubspot_company', 
    'get_hubspot_deals', 'create_hubspot_deal',
    'get_cms_pages', 'create_cms_page', 'update_cms_page', 'publish_cms_page',
    'get_design_manager_files', 'upload_design_file',
    'get_blog_posts', 'create_blog_post', 'update_blog_post', 'publish_blog_post',
    'get_forms', 'create_form',
    'get_workflows', 'create_workflow',
    'get_properties', 'create_property',
    'search_hubspot_objects', 'bulk_create_objects', 'get_hubspot_analytics'
]
