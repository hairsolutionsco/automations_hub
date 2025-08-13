#!/bin/bash

# MCP Tools Development and Testing Script

echo "🔧 MCP Tools Development & Testing"
echo "=================================="

# Check if we're in the right directory
if [[ ! -d "../tools" ]]; then
    echo "❌ Error: Please run this script from the automations-mcp/scripts directory"
    exit 1
fi

echo "🎯 Development & Testing Options:"
echo ""
echo "Tool Development:"
echo "1. List all available tools"
echo "2. Test individual tool"
echo "3. Create new tool template"
echo "4. Validate tool syntax"
echo ""
echo "Integration Testing:"
echo "5. Test Shopify tools"
echo "6. Test Notion tools"
echo "7. Test GitHub tools"
echo "8. Test N8N workflow tools"
echo ""
echo "Performance & Debugging:"
echo "9. Run tool performance tests"
echo "10. Debug tool execution"
echo "11. Generate tool documentation"
echo "12. Tool usage analytics"

read -p "Enter your choice (1-12): " choice

case $choice in
    1)
        echo "📋 Listing all available MCP tools..."
        echo ""
        echo "🔧 Tool Structure:"
        tree ../tools/ 2>/dev/null || find ../tools -type f -name "*.py" | sort
        
        echo ""
        echo "📊 Tool Summary:"
        echo "Python tools: $(find ../tools -name "*.py" | wc -l)"
        echo "Total files: $(find ../tools -type f | wc -l)"
        
        echo ""
        echo "🏷️ Tool Categories:"
        for category in shopify notion github payments n8n hello; do
            count=$(find ../tools -name "*$category*" -type f | wc -l)
            if [ $count -gt 0 ]; then
                echo "  $category: $count files"
            fi
        done
        ;;
    2)
        echo "🧪 Testing individual tool..."
        echo "Available tools:"
        ls ../tools/*.py 2>/dev/null | xargs -n1 basename
        ls ../tools/*/*.py 2>/dev/null | xargs -n1 basename
        
        read -p "Enter tool filename (e.g., hello.py): " tool_name
        
        if [ -f "../tools/$tool_name" ]; then
            echo "🔍 Testing tool: $tool_name"
            python -c "
import sys
sys.path.insert(0, '../tools')
try:
    import ${tool_name%.py}
    print('✅ Tool imports successfully')
    
    # Try to call main functions if they exist
    module = ${tool_name%.py}
    if hasattr(module, 'main'):
        print('🚀 Running main function...')
        module.main()
    elif hasattr(module, 'test'):
        print('🧪 Running test function...')
        module.test()
    else:
        print('ℹ️  No main() or test() function found')
        
except ImportError as e:
    print(f'❌ Import error: {e}')
except Exception as e:
    print(f'⚠️  Runtime error: {e}')
"
        else
            # Check subdirectories
            FOUND=false
            for subdir in ../tools/*/; do
                if [ -f "$subdir$tool_name" ]; then
                    echo "🔍 Testing tool: $subdir$tool_name"
                    FOUND=true
                    python -c "
import sys
sys.path.insert(0, '$subdir')
try:
    import ${tool_name%.py}
    print('✅ Tool imports successfully')
except Exception as e:
    print(f'❌ Error: {e}')
"
                    break
                fi
            done
            
            if [ "$FOUND" = false ]; then
                echo "❌ Tool not found: $tool_name"
            fi
        fi
        ;;
    3)
        echo "📝 Creating new tool template..."
        read -p "Enter tool name (e.g., my_new_tool): " tool_name
        read -p "Enter tool category (e.g., api, data, utility): " tool_category
        
        # Sanitize tool name
        tool_name=$(echo "$tool_name" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9_]/_/g')
        
        # Create tool directory if needed
        if [ -n "$tool_category" ]; then
            mkdir -p "../tools/$tool_category"
            TOOL_PATH="../tools/$tool_category/${tool_name}.py"
        else
            TOOL_PATH="../tools/${tool_name}.py"
        fi
        
        # Generate tool template
        cat > "$TOOL_PATH" << EOF
"""${tool_name} - MCP tool for automation hub."""

import os
from typing import Annotated, Any, Optional
from pydantic import BaseModel, Field


class ${tool_name^}Response(BaseModel):
    """Response model for ${tool_name} operations."""
    success: bool
    data: Optional[Any] = None
    message: str


async def ${tool_name}_main(
    input_param: Annotated[str, Field(description="Main input parameter")]
) -> ${tool_name^}Response:
    """Main function for ${tool_name} tool."""
    
    try:
        # TODO: Implement your tool logic here
        result = f"Processed: {input_param}"
        
        return ${tool_name^}Response(
            success=True,
            data=result,
            message="Operation completed successfully"
        )
        
    except Exception as e:
        return ${tool_name^}Response(
            success=False,
            message=f"Error in ${tool_name}: {str(e)}"
        )


def test():
    """Test function for ${tool_name}."""
    import asyncio
    
    async def run_test():
        result = await ${tool_name}_main("test_input")
        print(f"Test result: {result}")
    
    asyncio.run(run_test())


if __name__ == "__main__":
    test()
EOF
        
        echo "✅ Tool template created: $TOOL_PATH"
        echo "📝 Next steps:"
        echo "  1. Edit the tool file to implement your logic"
        echo "  2. Test with: python $TOOL_PATH"
        echo "  3. Add to Golf MCP server configuration"
        ;;
    4)
        echo "✅ Validating tool syntax..."
        
        TOTAL_TOOLS=0
        VALID_TOOLS=0
        ERRORS=()
        
        # Check all Python tools
        while IFS= read -r -d '' file; do
            TOTAL_TOOLS=$((TOTAL_TOOLS + 1))
            filename=$(basename "$file")
            
            # Check syntax
            if python -m py_compile "$file" 2>/dev/null; then
                echo "  ✅ $filename"
                VALID_TOOLS=$((VALID_TOOLS + 1))
            else
                echo "  ❌ $filename - Syntax error"
                ERRORS+=("$filename")
            fi
        done < <(find ../tools -name "*.py" -print0)
        
        echo ""
        echo "📊 Validation Summary:"
        echo "Total tools: $TOTAL_TOOLS"
        echo "Valid tools: $VALID_TOOLS"
        echo "Invalid tools: $((TOTAL_TOOLS - VALID_TOOLS))"
        
        if [ ${#ERRORS[@]} -gt 0 ]; then
            echo ""
            echo "❌ Tools with syntax errors:"
            for error in "${ERRORS[@]}"; do
                echo "  - $error"
            done
        fi
        ;;
    5)
        echo "🛍️ Testing Shopify tools..."
        
        if [ -d "../tools/shopify" ]; then
            echo "📦 Found Shopify tools directory"
            
            # Test each Shopify tool
            for tool in ../tools/shopify/*.py; do
                if [ -f "$tool" ]; then
                    filename=$(basename "$tool")
                    echo "🧪 Testing $filename..."
                    
                    python -c "
import sys
sys.path.insert(0, '../tools/shopify')
try:
    import ${filename%.py}
    print('  ✅ Imports successfully')
except Exception as e:
    print(f'  ❌ Error: {e}')
"
                fi
            done
            
            # Check environment variables
            echo ""
            echo "🔧 Environment Check:"
            if [ -n "$SHOPIFY_STORE_URL" ]; then
                echo "  ✅ SHOPIFY_STORE_URL is set"
            else
                echo "  ⚠️  SHOPIFY_STORE_URL not set"
            fi
            
            if [ -n "$SHOPIFY_ACCESS_TOKEN" ]; then
                echo "  ✅ SHOPIFY_ACCESS_TOKEN is set"
            else
                echo "  ⚠️  SHOPIFY_ACCESS_TOKEN not set"
            fi
        else
            echo "❌ Shopify tools directory not found"
        fi
        ;;
    6)
        echo "📊 Testing Notion tools..."
        
        if [ -f "../tools/notion_api.py" ]; then
            echo "📝 Found Notion API tool"
            
            python -c "
import sys
sys.path.insert(0, '../tools')
try:
    import notion_api
    print('✅ Notion API tool imports successfully')
except Exception as e:
    print(f'❌ Error: {e}')
"
            
            # Check environment variables
            echo ""
            echo "🔧 Environment Check:"
            if [ -n "$NOTION_TOKEN" ]; then
                echo "  ✅ NOTION_TOKEN is set"
            else
                echo "  ⚠️  NOTION_TOKEN not set"
            fi
        else
            echo "❌ Notion API tool not found"
        fi
        ;;
    7)
        echo "🐙 Testing GitHub tools..."
        
        if [ -f "../tools/github_user.py" ]; then
            echo "👤 Found GitHub user tool"
            
            python -c "
import sys
sys.path.insert(0, '../tools')
try:
    import github_user
    print('✅ GitHub user tool imports successfully')
except Exception as e:
    print(f'❌ Error: {e}')
"
            
            # Check environment variables
            echo ""
            echo "🔧 Environment Check:"
            if [ -n "$GITHUB_TOKEN" ]; then
                echo "  ✅ GITHUB_TOKEN is set"
            else
                echo "  ⚠️  GITHUB_TOKEN not set"
            fi
        else
            echo "❌ GitHub user tool not found"
        fi
        ;;
    8)
        echo "🔄 Testing N8N workflow tools..."
        
        if [ -f "../tools/n8n_workflows.py" ]; then
            echo "⚡ Found N8N workflows tool"
            
            python -c "
import sys
sys.path.insert(0, '../tools')
try:
    import n8n_workflows
    print('✅ N8N workflows tool imports successfully')
except Exception as e:
    print(f'❌ Error: {e}')
"
            
            # Check environment variables
            echo ""
            echo "🔧 Environment Check:"
            if [ -n "$N8N_API_KEY" ]; then
                echo "  ✅ N8N_API_KEY is set"
            else
                echo "  ⚠️  N8N_API_KEY not set"
            fi
        else
            echo "❌ N8N workflows tool not found"
        fi
        ;;
    9)
        echo "⚡ Running tool performance tests..."
        
        echo "📊 Performance Test Results:" > tool_performance.txt
        echo "Generated: $(date)" >> tool_performance.txt
        echo "" >> tool_performance.txt
        
        # Test import times
        echo "🕐 Testing import times..."
        for tool in ../tools/*.py; do
            if [ -f "$tool" ]; then
                filename=$(basename "$tool" .py)
                echo "Testing import time for $filename..."
                
                time_result=$(python -c "
import time
import sys
sys.path.insert(0, '../tools')
start = time.time()
try:
    import $filename
    end = time.time()
    print(f'{end - start:.3f}s')
except:
    print('ERROR')
" 2>/dev/null)
                
                echo "$filename: $time_result" >> tool_performance.txt
            fi
        done
        
        echo "✅ Performance results saved to: tool_performance.txt"
        cat tool_performance.txt
        ;;
    10)
        echo "🐛 Debug tool execution..."
        
        echo "Available tools for debugging:"
        ls ../tools/*.py 2>/dev/null | xargs -n1 basename
        
        read -p "Enter tool filename to debug: " tool_name
        
        if [ -f "../tools/$tool_name" ]; then
            echo "🔍 Debugging tool: $tool_name"
            echo "Running in verbose mode..."
            
            python -v -c "
import sys
sys.path.insert(0, '../tools')
print('=== DEBUGGING $tool_name ===')
try:
    import ${tool_name%.py}
    print('=== IMPORT SUCCESSFUL ===')
    print('Available functions:')
    for attr in dir(${tool_name%.py}):
        if not attr.startswith('_'):
            print(f'  - {attr}')
except Exception as e:
    print(f'=== IMPORT FAILED ===')
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
"
        else
            echo "❌ Tool not found: $tool_name"
        fi
        ;;
    11)
        echo "📚 Generating tool documentation..."
        
        DOC_FILE="tools_documentation.md"
        echo "# MCP Tools Documentation" > "$DOC_FILE"
        echo "Generated: $(date)" >> "$DOC_FILE"
        echo "" >> "$DOC_FILE"
        
        echo "## Available Tools" >> "$DOC_FILE"
        echo "" >> "$DOC_FILE"
        
        # Document each tool
        for tool in ../tools/*.py; do
            if [ -f "$tool" ]; then
                filename=$(basename "$tool")
                echo "### $filename" >> "$DOC_FILE"
                echo "" >> "$DOC_FILE"
                
                # Extract docstring
                docstring=$(python -c "
import sys
sys.path.insert(0, '../tools')
try:
    import ${filename%.py}
    if ${filename%.py}.__doc__:
        print(${filename%.py}.__doc__)
    else:
        print('No documentation available')
except:
    print('Unable to load tool')
")
                echo "$docstring" >> "$DOC_FILE"
                echo "" >> "$DOC_FILE"
            fi
        done
        
        # Document subdirectory tools
        for subdir in ../tools/*/; do
            if [ -d "$subdir" ]; then
                dirname=$(basename "$subdir")
                echo "## $dirname Tools" >> "$DOC_FILE"
                echo "" >> "$DOC_FILE"
                
                for tool in "$subdir"*.py; do
                    if [ -f "$tool" ]; then
                        filename=$(basename "$tool")
                        echo "### $dirname/$filename" >> "$DOC_FILE"
                        echo "" >> "$DOC_FILE"
                        
                        # Try to get documentation
                        docstring=$(python -c "
import sys
sys.path.insert(0, '$subdir')
try:
    import ${filename%.py}
    if ${filename%.py}.__doc__:
        print(${filename%.py}.__doc__)
    else:
        print('No documentation available')
except:
    print('Unable to load tool')
")
                        echo "$docstring" >> "$DOC_FILE"
                        echo "" >> "$DOC_FILE"
                    fi
                done
            fi
        done
        
        echo "✅ Documentation generated: $DOC_FILE"
        echo "📄 Preview:"
        head -20 "$DOC_FILE"
        ;;
    12)
        echo "📈 Tool usage analytics..."
        
        ANALYTICS_FILE="tool_analytics.txt"
        echo "=== MCP Tools Analytics ===" > "$ANALYTICS_FILE"
        echo "Generated: $(date)" >> "$ANALYTICS_FILE"
        echo "" >> "$ANALYTICS_FILE"
        
        # Count tools by category
        echo "📊 Tools by Category:" >> "$ANALYTICS_FILE"
        echo "Python tools: $(find ../tools -name "*.py" | wc -l)" >> "$ANALYTICS_FILE"
        echo "Shopify tools: $(find ../tools -path "*/shopify/*.py" | wc -l)" >> "$ANALYTICS_FILE"
        echo "Payment tools: $(find ../tools -path "*/payments/*.py" | wc -l)" >> "$ANALYTICS_FILE"
        echo "" >> "$ANALYTICS_FILE"
        
        # Tool complexity (lines of code)
        echo "📏 Tool Complexity (lines of code):" >> "$ANALYTICS_FILE"
        for tool in ../tools/*.py ../tools/*/*.py; do
            if [ -f "$tool" ]; then
                lines=$(wc -l < "$tool")
                echo "$(basename "$tool"): $lines lines" >> "$ANALYTICS_FILE"
            fi
        done | sort -n >> "$ANALYTICS_FILE"
        
        echo "" >> "$ANALYTICS_FILE"
        
        # Recent modifications
        echo "📅 Recent Modifications:" >> "$ANALYTICS_FILE"
        find ../tools -name "*.py" -mtime -7 -exec ls -la {} \; >> "$ANALYTICS_FILE"
        
        echo "✅ Analytics generated: $ANALYTICS_FILE"
        cat "$ANALYTICS_FILE"
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac
