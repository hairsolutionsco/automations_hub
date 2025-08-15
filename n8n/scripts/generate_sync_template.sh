#!/bin/bash

# 🏗️ Universal Notion ↔ HubSpot Sync Template Generator
# Creates complete sync workflows for any object type

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
PURPLE='\033[0;35m'
NC='\033[0m'

# Function to display usage
show_usage() {
    echo -e "${BLUE}🏗️  Notion ↔ HubSpot Sync Template Generator${NC}"
    echo "============================================"
    echo ""
    echo "Usage: $0 <object_type> <notion_database_id>"
    echo ""
    echo "Supported object types:"
    echo "  • contacts    - Contact records"
    echo "  • deals       - Deal/Opportunity records"
    echo "  • companies   - Company records"
    echo "  • products    - Product catalog"
    echo "  • tickets     - Support tickets"
    echo "  • orders      - Order/Transaction records"
    echo "  • custom      - Custom object (manual configuration)"
    echo ""
    echo "Example:"
    echo "  $0 deals abc123-def456-789"
    echo ""
}

# Check arguments
if [[ $# -lt 2 ]]; then
    show_usage
    exit 1
fi

OBJECT_TYPE=$1
NOTION_DB_ID=$2

# Validate object type
case $OBJECT_TYPE in
    contacts|deals|companies|products|tickets|orders|custom)
        ;;
    *)
        echo -e "${RED}❌ Unsupported object type: $OBJECT_TYPE${NC}"
        show_usage
        exit 1
        ;;
esac

echo -e "${BLUE}🚀 Creating $OBJECT_TYPE sync workflow${NC}"
echo "=================================="
echo "Object Type: $OBJECT_TYPE"
echo "Database ID: $NOTION_DB_ID"
echo ""

# Create object-specific directories
OBJECT_DIR="/workspaces/automations_hub/n8n/objects/$OBJECT_TYPE"
mkdir -p "$OBJECT_DIR"/{workflows,scripts,docs}

echo -e "${YELLOW}📁 Created directory structure: $OBJECT_DIR${NC}"

# Step 1: Generate property matcher
echo -e "${YELLOW}📋 Step 1: Creating Property Analysis Script${NC}"

cat > "$OBJECT_DIR/${OBJECT_TYPE}_property_matcher.py" << EOF
"""
Notion ↔ HubSpot ${OBJECT_TYPE^} Property Matcher
Analyzes and maps properties between Notion and HubSpot ${OBJECT_TYPE} objects.
Generated automatically by template generator.
"""

import os
import requests
import json
import csv
from datetime import datetime

class ${OBJECT_TYPE^}PropertyMatcher:
    def __init__(self):
        self.notion_token = os.getenv('NOTION_TOKEN')
        self.hubspot_token = os.getenv('HUBSPOT_TOKEN')
        self.notion_database_id = "${NOTION_DB_ID}"
        
        # Object-specific configurations
        self.object_configs = {
            'contacts': {'hubspot_endpoint': 'contacts', 'notion_name': 'Contact'},
            'deals': {'hubspot_endpoint': 'deals', 'notion_name': 'Deal'},
            'companies': {'hubspot_endpoint': 'companies', 'notion_name': 'Company'},
            'products': {'hubspot_endpoint': 'products', 'notion_name': 'Product'},
            'tickets': {'hubspot_endpoint': 'tickets', 'notion_name': 'Ticket'},
            'orders': {'hubspot_endpoint': 'line_items', 'notion_name': 'Order'},
            'custom': {'hubspot_endpoint': '${OBJECT_TYPE}', 'notion_name': '${OBJECT_TYPE^}'}
        }
        
        self.config = self.object_configs.get('${OBJECT_TYPE}', self.object_configs['custom'])
        
    def get_notion_properties(self):
        """Get properties from Notion database"""
        url = f"https://api.notion.com/v1/databases/{self.notion_database_id}"
        headers = {
            "Authorization": f"Bearer {self.notion_token}",
            "Notion-Version": "2022-06-28"
        }
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return self._parse_notion_properties(response.json())
        else:
            raise Exception(f"Failed to fetch Notion database: {response.status_code}")
    
    def get_hubspot_properties(self):
        """Get properties from HubSpot"""
        url = f"https://api.hubapi.com/crm/v3/properties/{self.config['hubspot_endpoint']}"
        headers = {"Authorization": f"Bearer {self.hubspot_token}"}
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get('results', [])
        else:
            raise Exception(f"Failed to fetch HubSpot properties: {response.status_code}")
    
    def _parse_notion_properties(self, database_info):
        """Parse Notion database properties"""
        properties = []
        db_properties = database_info.get('properties', {})
        
        for prop_name, prop_config in db_properties.items():
            prop_type = prop_config.get('type', 'unknown')
            properties.append({
                'name': prop_name,
                'type': prop_type,
                'id': prop_config.get('id', ''),
                'description': f"Notion {prop_type} property"
            })
        
        return properties
    
    def match_properties(self):
        """Match properties between Notion and HubSpot"""
        notion_props = self.get_notion_properties()
        hubspot_props = self.get_hubspot_properties()
        
        matches = []
        unmatched_notion = []
        
        for notion_prop in notion_props:
            best_match = self._find_best_match(notion_prop, hubspot_props)
            if best_match:
                matches.append({
                    'notion_name': notion_prop['name'],
                    'notion_type': notion_prop['type'],
                    'hubspot_name': best_match['name'],
                    'hubspot_type': best_match['type'],
                    'confidence': 'high' if notion_prop['name'].lower() == best_match['name'].lower() else 'medium'
                })
            else:
                unmatched_notion.append(notion_prop)
        
        return {
            'matches': matches,
            'unmatched_notion': unmatched_notion,
            'total_notion': len(notion_props),
            'total_hubspot': len(hubspot_props),
            'matched_count': len(matches)
        }
    
    def _find_best_match(self, notion_prop, hubspot_props):
        """Find best matching HubSpot property"""
        notion_name = notion_prop['name'].lower()
        
        # Exact name match
        for hs_prop in hubspot_props:
            if hs_prop['name'].lower() == notion_name:
                return hs_prop
        
        # Common mappings for ${OBJECT_TYPE}
        mappings = self._get_common_mappings()
        if notion_name in mappings:
            for hs_prop in hubspot_props:
                if hs_prop['name'].lower() == mappings[notion_name]:
                    return hs_prop
        
        return None
    
    def _get_common_mappings(self):
        """Get common property mappings for ${OBJECT_TYPE}"""
        mappings = {
            'contacts': {
                'email': 'email',
                'phone': 'phone',
                'first name': 'firstname',
                'last name': 'lastname',
                'company': 'company'
            },
            'deals': {
                'deal name': 'dealname',
                'amount': 'amount',
                'stage': 'dealstage',
                'close date': 'closedate',
                'pipeline': 'pipeline'
            },
            'companies': {
                'company name': 'name',
                'domain': 'domain',
                'industry': 'industry',
                'city': 'city',
                'state': 'state'
            },
            'products': {
                'product name': 'name',
                'price': 'price',
                'description': 'description',
                'sku': 'hs_sku'
            },
            'tickets': {
                'subject': 'subject',
                'priority': 'hs_ticket_priority',
                'category': 'hs_ticket_category',
                'content': 'content'
            }
        }
        
        return mappings.get('${OBJECT_TYPE}', {})
    
    def generate_report(self):
        """Generate comprehensive mapping report"""
        results = self.match_properties()
        
        # Generate markdown report
        markdown_content = self._generate_markdown_report(results)
        with open('${OBJECT_TYPE}_property_mapping.md', 'w') as f:
            f.write(markdown_content)
        
        # Generate CSV for import
        csv_content = self._generate_csv_report(results)
        with open('${OBJECT_TYPE}_mapping.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(csv_content)
        
        print(f"✅ Generated ${OBJECT_TYPE} property mapping report")
        print(f"   📄 ${OBJECT_TYPE}_property_mapping.md")
        print(f"   📊 ${OBJECT_TYPE}_mapping.csv")
        
        return results
    
    def _generate_markdown_report(self, results):
        """Generate markdown report"""
        coverage = (results['matched_count'] / results['total_notion']) * 100
        
        content = f"""# ${OBJECT_TYPE^} Property Mapping Report

## Summary
- **Notion Properties**: {results['total_notion']}
- **HubSpot Properties**: {results['total_hubspot']}
- **Matched Properties**: {results['matched_count']}
- **Coverage**: {coverage:.1f}%

## Matched Properties

| Notion Property | Type | HubSpot Property | Type | Confidence |
|---|---|---|---|---|
"""
        
        for match in results['matches']:
            content += f"| {match['notion_name']} | {match['notion_type']} | {match['hubspot_name']} | {match['hubspot_type']} | {match['confidence']} |\n"
        
        if results['unmatched_notion']:
            content += f"\n## Unmatched Notion Properties\n\n"
            for prop in results['unmatched_notion']:
                content += f"- **{prop['name']}** ({prop['type']})\n"
        
        return content
    
    def _generate_csv_report(self, results):
        """Generate CSV for workflow import"""
        rows = [['notion_property', 'hubspot_property', 'transformation']]
        
        for match in results['matches']:
            transformation = f"={{{{ \\$json.properties?.{match['notion_name']}?.{match['notion_type']} || \\$json.properties?.{match['hubspot_name']}?.value }}}}"
            rows.append([match['notion_name'], match['hubspot_name'], transformation])
        
        return rows

if __name__ == "__main__":
    matcher = ${OBJECT_TYPE^}PropertyMatcher()
    matcher.generate_report()
EOF

echo -e "${GREEN}✅ Created ${OBJECT_TYPE}_property_matcher.py${NC}"

# Step 2: Generate workflow templates
echo -e "${YELLOW}📋 Step 2: Creating Workflow Templates${NC}"

# Generate webhook workflow
cat > "$OBJECT_DIR/workflows/${OBJECT_TYPE}_sync_webhook.json" << EOF
{
  "name": "Notion HubSpot ${OBJECT_TYPE^} Sync - Webhook",
  "nodes": [
    {
      "parameters": {
        "path": "hubspot-${OBJECT_TYPE}-updated",
        "httpMethod": "POST",
        "options": {}
      },
      "id": "webhook-trigger",
      "name": "HubSpot ${OBJECT_TYPE^} Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [240, 300]
    },
    {
      "parameters": {
        "resource": "${OBJECT_TYPE%s}",
        "operation": "get",
        "objectId": "={{ \\$json.objectId }}"
      },
      "id": "hubspot-get",
      "name": "Get HubSpot ${OBJECT_TYPE^}",
      "type": "n8n-nodes-base.hubspot",
      "typeVersion": 2,
      "position": [460, 300]
    },
    {
      "parameters": {
        "database_id": "${NOTION_DB_ID}",
        "simple": false,
        "properties": {}
      },
      "id": "notion-update",
      "name": "Update Notion ${OBJECT_TYPE^}",
      "type": "n8n-nodes-base.notion",
      "typeVersion": 2,
      "position": [680, 300]
    }
  ],
  "connections": {
    "HubSpot ${OBJECT_TYPE^} Webhook": {
      "main": [
        [
          {
            "node": "Get HubSpot ${OBJECT_TYPE^}",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Get HubSpot ${OBJECT_TYPE^}": {
      "main": [
        [
          {
            "node": "Update Notion ${OBJECT_TYPE^}",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "pinData": {},
  "settings": {
    "executionOrder": "v1"
  },
  "staticData": null,
  "tags": [],
  "triggerCount": 0,
  "updatedAt": "$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)",
  "versionId": "$(uuidgen)"
}
EOF

# Generate polling workflow
cat > "$OBJECT_DIR/workflows/${OBJECT_TYPE}_sync_polling.json" << EOF
{
  "name": "Notion HubSpot ${OBJECT_TYPE^} Sync - Polling",
  "nodes": [
    {
      "parameters": {
        "rule": {
          "interval": [
            {
              "field": "cronExpression",
              "expression": "*/5 * * * *"
            }
          ]
        }
      },
      "id": "cron-trigger",
      "name": "Every 5 Minutes",
      "type": "n8n-nodes-base.cron",
      "typeVersion": 1,
      "position": [240, 300]
    },
    {
      "parameters": {
        "database_id": "${NOTION_DB_ID}",
        "simple": false,
        "filters": {
          "conditions": [
            {
              "key": "Last Modified",
              "condition": "after",
              "value": "={{ \\$now.minus({ minutes: 5 }).toISO() }}"
            }
          ]
        }
      },
      "id": "notion-query",
      "name": "Query Updated ${OBJECT_TYPE^}s",
      "type": "n8n-nodes-base.notion",
      "typeVersion": 2,
      "position": [460, 300]
    },
    {
      "parameters": {
        "resource": "${OBJECT_TYPE%s}",
        "operation": "upsert",
        "properties": {}
      },
      "id": "hubspot-upsert",
      "name": "Upsert HubSpot ${OBJECT_TYPE^}",
      "type": "n8n-nodes-base.hubspot",
      "typeVersion": 2,
      "position": [680, 300]
    }
  ],
  "connections": {
    "Every 5 Minutes": {
      "main": [
        [
          {
            "node": "Query Updated ${OBJECT_TYPE^}s",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Query Updated ${OBJECT_TYPE^}s": {
      "main": [
        [
          {
            "node": "Upsert HubSpot ${OBJECT_TYPE^}",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "pinData": {},
  "settings": {
    "executionOrder": "v1"
  },
  "staticData": null,
  "tags": [],
  "triggerCount": 0,
  "updatedAt": "$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)",
  "versionId": "$(uuidgen)"
}
EOF

echo -e "${GREEN}✅ Created workflow templates${NC}"

# Step 3: Generate monitoring script
echo -e "${YELLOW}📋 Step 3: Creating Monitoring Scripts${NC}"

cat > "$OBJECT_DIR/scripts/monitor_${OBJECT_TYPE}_sync.sh" << 'EOF'
#!/bin/bash

# Monitor script for OBJECT_TYPE sync
OBJECT_TYPE="OBJECT_TYPE_PLACEHOLDER"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🔍 Notion ↔ HubSpot ${OBJECT_TYPE^} Sync Monitor${NC}"
echo "============================================="
echo ""

# Check workflow status
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
    "$N8N_CLOUD_INSTANCE_URL/api/v1/workflows?active=true" | \
    jq -r ".data[] | select(.name | test(\"${OBJECT_TYPE^} Sync\")) | \"✅ \(.name) (ID: \(.id)) - Active: \(.active)\""

# Check recent executions
echo -e "\n${YELLOW}Recent Executions:${NC}"
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
    "$N8N_CLOUD_INSTANCE_URL/api/v1/executions?limit=5" | \
    jq -r ".data[] | select(.workflowData.name // \"\" | test(\"${OBJECT_TYPE^} Sync\")) | \"[\(.startedAt)] \(.workflowData.name): \(if .finished then \"✅ SUCCESS\" else \"⏳ RUNNING\" end)\""

echo -e "\n${GREEN}Monitor complete!${NC}"
EOF

# Replace placeholders
sed -i "s/OBJECT_TYPE_PLACEHOLDER/$OBJECT_TYPE/g" "$OBJECT_DIR/scripts/monitor_${OBJECT_TYPE}_sync.sh"
chmod +x "$OBJECT_DIR/scripts/monitor_${OBJECT_TYPE}_sync.sh"

echo -e "${GREEN}✅ Created monitoring script${NC}"

# Step 4: Generate documentation
echo -e "${YELLOW}📋 Step 4: Creating Documentation${NC}"

cat > "$OBJECT_DIR/docs/${OBJECT_TYPE^}_SYNC_SETUP.md" << EOF
# ${OBJECT_TYPE^} Sync Setup Guide

## Overview
This directory contains everything needed for Notion ↔ HubSpot ${OBJECT_TYPE} synchronization.

## Files Generated
- \`${OBJECT_TYPE}_property_matcher.py\` - Property analysis script
- \`workflows/${OBJECT_TYPE}_sync_webhook.json\` - Webhook-based sync workflow
- \`workflows/${OBJECT_TYPE}_sync_polling.json\` - Polling-based sync workflow
- \`scripts/monitor_${OBJECT_TYPE}_sync.sh\` - Monitoring script

## Setup Steps

### 1. Run Property Analysis
\`\`\`bash
cd $OBJECT_DIR
python ${OBJECT_TYPE}_property_matcher.py
\`\`\`

### 2. Customize Property Mappings
Edit the generated workflows to include your specific property mappings:
- Review \`${OBJECT_TYPE}_property_mapping.md\`
- Update transformation nodes in workflow JSON files

### 3. Import to n8n
\`\`\`bash
# Import webhook workflow
curl -X POST \\
  -H "X-N8N-API-KEY: \$N8N_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d @workflows/${OBJECT_TYPE}_sync_webhook.json \\
  "\$N8N_CLOUD_INSTANCE_URL/api/v1/workflows/import"

# Import polling workflow
curl -X POST \\
  -H "X-N8N-API-KEY: \$N8N_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d @workflows/${OBJECT_TYPE}_sync_polling.json \\
  "\$N8N_CLOUD_INSTANCE_URL/api/v1/workflows/import"
\`\`\`

### 4. Configure & Test
- Set up API credentials in n8n
- Activate both workflows
- Test with sample ${OBJECT_TYPE} data
- Monitor using: \`./scripts/monitor_${OBJECT_TYPE}_sync.sh\`

## Configuration
- **Notion Database ID**: \`${NOTION_DB_ID}\`
- **HubSpot Object**: \`${OBJECT_TYPE}\`
- **Sync Frequency**: Every 5 minutes

## Next Steps
1. Run property analysis
2. Review and customize property mappings
3. Import workflows to n8n
4. Test sync functionality
5. Monitor and refine as needed

Generated on: $(date)
EOF

echo -e "${GREEN}✅ Created setup documentation${NC}"

# Summary
echo ""
echo -e "${PURPLE}🎉 ${OBJECT_TYPE^} Sync Template Generated Successfully!${NC}"
echo "=================================================="
echo ""
echo -e "${GREEN}📁 Created in: $OBJECT_DIR${NC}"
echo ""
echo -e "${YELLOW}📋 Generated Files:${NC}"
echo "   📄 ${OBJECT_TYPE}_property_matcher.py"
echo "   📄 workflows/${OBJECT_TYPE}_sync_webhook.json"
echo "   📄 workflows/${OBJECT_TYPE}_sync_polling.json"
echo "   📄 scripts/monitor_${OBJECT_TYPE}_sync.sh"
echo "   📄 docs/${OBJECT_TYPE^}_SYNC_SETUP.md"
echo ""
echo -e "${BLUE}🎯 Next Steps:${NC}"
echo "   1. cd $OBJECT_DIR"
echo "   2. python ${OBJECT_TYPE}_property_matcher.py"
echo "   3. Review generated property mapping"
echo "   4. Customize workflow property transformations"
echo "   5. Import workflows to n8n"
echo "   6. Test and monitor"
echo ""
echo -e "${GREEN}✨ Template ready for customization!${NC}"
