# N8N Workflow Examples

## Basic Automation Patterns

### Notion to HubSpot Sync
```json
{
  "name": "Notion to HubSpot Contact Sync",
  "nodes": [
    {
      "name": "Notion Trigger",
      "type": "n8n-nodes-base.notionTrigger",
      "parameters": {
        "databaseId": "your-database-id",
        "event": "rowCreated"
      }
    },
    {
      "name": "Create HubSpot Contact",
      "type": "n8n-nodes-base.hubspot",
      "parameters": {
        "resource": "contact",
        "operation": "create",
        "additionalFields": {
          "firstname": "={{ $node['Notion Trigger'].json.properties.Name.title[0].plain_text }}",
          "email": "={{ $node['Notion Trigger'].json.properties.Email.email }}"
        }
      }
    }
  ],
  "connections": {
    "Notion Trigger": {
      "main": [
        [
          {
            "node": "Create HubSpot Contact",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  }
}
```

### Shopify Order to Notion
```json
{
  "name": "Shopify Order to Notion Database",
  "nodes": [
    {
      "name": "Shopify Trigger",
      "type": "n8n-nodes-base.shopifyTrigger",
      "parameters": {
        "topic": "orders/create"
      }
    },
    {
      "name": "Create Notion Page",
      "type": "n8n-nodes-base.notion",
      "parameters": {
        "resource": "page",
        "operation": "create",
        "databaseId": "your-orders-database-id",
        "properties": {
          "Order ID": "={{ $node['Shopify Trigger'].json.order_number }}",
          "Customer": "={{ $node['Shopify Trigger'].json.customer.first_name }} {{ $node['Shopify Trigger'].json.customer.last_name }}",
          "Total": "={{ $node['Shopify Trigger'].json.total_price }}"
        }
      }
    }
  ]
}
```

## Advanced Patterns

### Multi-Platform Customer Journey
1. **Trigger**: New Shopify customer
2. **Action 1**: Create HubSpot contact
3. **Action 2**: Add to Notion CRM database  
4. **Action 3**: Send welcome email via HubSpot
5. **Action 4**: Create follow-up task

### Inventory Management Flow
1. **Trigger**: Low stock alert from Shopify
2. **Action 1**: Update Notion inventory database
3. **Action 2**: Create HubSpot task for purchasing team
4. **Action 3**: Send Slack notification
