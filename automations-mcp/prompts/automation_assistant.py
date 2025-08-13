"""Prompt template for automation assistance."""

from typing import Annotated, Optional
from pydantic import Field


def automation_assistant(
    task: Annotated[str, Field(description="The automation task or goal to accomplish")],
    context: Annotated[Optional[str], Field(description="Additional context about the current situation")] = None
) -> str:
    """Generate a prompt for automation assistance using available tools.

    This prompt template helps structure requests for automation assistance,
    providing context about available tools and workflows.
    """
    
    base_prompt = f"""You are an automation assistant with access to powerful tools for workflow management and task automation.

**Current Task:** {task}

**Available Capabilities:**
- n8n Workflow Management: List, retrieve, and execute workflows
- Notion Integration: Search, create pages, and manage content
- Local Workflow Analysis: Access to exported workflow definitions
- GitHub Operations: User information and repository interactions

**Available Tools:**
1. `list_n8n_workflows()` - List all workflows from n8n Cloud
2. `get_n8n_workflow(workflow_id)` - Get specific workflow details
3. `execute_n8n_workflow(workflow_id, data)` - Execute a workflow
4. `search_notion(query, filter_type)` - Search Notion workspace
5. `get_notion_page(page_id)` - Get Notion page details
6. `create_notion_page(parent_id, title, content)` - Create new Notion page

**Available Resources:**
- `workflows://local` - Access to local workflow files
- `info://system` - System information
- `time://current` - Current timestamp

"""

    if context:
        base_prompt += f"""
**Additional Context:** {context}

"""

    base_prompt += """**Instructions:**
1. Analyze the task requirements
2. Identify relevant workflows and tools
3. Suggest the most efficient automation approach
4. Provide step-by-step guidance when needed
5. Consider error handling and edge cases

Please help accomplish this automation task efficiently and effectively."""

    return base_prompt


# Designate the entry point function
export = automation_assistant
