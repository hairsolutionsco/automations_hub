# HubSpot Configuration Examples

## Object Schemas

### Contact Properties
```json
{
  "name": "hair_type",
  "label": "Hair Type",
  "type": "enumeration",
  "fieldType": "select",
  "groupName": "contactinformation",
  "options": [
    {"label": "Straight", "value": "straight"},
    {"label": "Wavy", "value": "wavy"},
    {"label": "Curly", "value": "curly"},
    {"label": "Coily", "value": "coily"}
  ]
}
```

### Company Properties
```json
{
  "name": "business_type",
  "label": "Business Type",
  "type": "enumeration",
  "fieldType": "select",
  "groupName": "companyinformation",
  "options": [
    {"label": "Salon", "value": "salon"},
    {"label": "Barbershop", "value": "barbershop"},
    {"label": "Distributor", "value": "distributor"},
    {"label": "Retailer", "value": "retailer"}
  ]
}
```

## Workflow Examples

### Lead Nurturing Workflow
- Trigger: Contact form submission
- Actions:
  1. Add to "New Leads" list
  2. Send welcome email
  3. Create follow-up task
  4. Set lifecycle stage to "Lead"

### Order Processing Workflow  
- Trigger: Deal stage = "Closed Won"
- Actions:
  1. Create Shopify order
  2. Update inventory
  3. Send fulfillment notification
  4. Schedule follow-up survey
