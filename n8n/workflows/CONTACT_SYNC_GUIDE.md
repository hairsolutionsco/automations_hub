# Notion ↔ HubSpot Contact 2-Way Sync Workflow

**Complete real-time synchronization between Notion contacts database and HubSpot contacts**

## 🎯 Overview

This n8n workflow provides **complete 2-way synchronization** between your Notion contacts database (24 properties) and HubSpot contacts (636 properties), ensuring both systems stay in sync automatically.

### Key Features
- ✅ **Real-time sync** via webhook triggers
- ✅ **Bi-directional** (Notion ↔ HubSpot)
- ✅ **Property mapping** for all 24 Notion properties
- ✅ **Conflict resolution** with timestamps
- ✅ **Error handling** and logging
- ✅ **Create & Update** operations
- ✅ **Native n8n nodes** (no custom APIs)

## 📊 Property Mapping

Based on our property analysis, the workflow maps your 24 Notion properties to HubSpot equivalents:

### Perfect Matches (8 properties)
| Notion Property | HubSpot Property | Direction | Type |
|---|---|---|---|
| `Email` | `email` | ↔ | email → string |
| `Access Point Location` | `access_point_location` | ↔ | rich_text → string |
| `Marketing contact status` | `hs_marketable_status` | ↔ | select → enumeration |
| `Address` | `address` | ↔ | rich_text → string |
| `Phone Number` | `phone` | ↔ | phone_number → string |
| `Shipping Profile` | `shipping_profile` | ↔ | multi_select → enumeration |
| `Re-Engagement Notes` | `reengagementnotes` | ↔ | rich_text → string |
| `Lifecycle Stage` | `lifecyclestage` | ↔ | select → enumeration |

### High-Quality Matches (9 properties)
| Notion Property | HubSpot Property | Direction | Notes |
|---|---|---|---|
| `Name` | `firstname` + `lastname` | ↔ | Name splitting logic |
| `Contact Profile` | `contact_type` | ↔ | Profile mapping |
| `Country/Region` | `country` | ↔ | Geographic data |
| `Sales Status` | `hs_lead_status` | ↔ | Status mapping |
| `Order Email Text` | `order_email_text` | ↔ | Custom field |
| `Id` | `notion_contact_id` | ↔ | Cross-reference |
| `Hubspot Contacts Record ID` | `hs_object_id` | ↔ | Cross-reference |

### Relation Fields (7 properties)
| Notion Property | HubSpot Equivalent | Sync Strategy |
|---|---|---|
| `Associated Companies` | Company associations | API associations |
| `Associated Deals` | Deal associations | API associations |
| `Associated Orders` | Custom properties | Order count/references |
| `Associated Payment` | Custom properties | Payment references |
| `Associated Plans` | Custom properties | Plan references |
| `Hair Orders Profiles` | Custom properties | Profile references |
| `Tasks` | Task/Activity associations | API associations |

## 🏗️ Workflow Architecture

### Workflow Components

```
Notion Contact Updated (Webhook)
└── Get Notion Contact (Notion API)
    └── Transform Notion → HubSpot (Code)
        └── HubSpot Contact Exists? (Conditional)
            ├── Update HubSpot Contact (HubSpot API)
            └── Create HubSpot Contact (HubSpot API)
                └── Log Success (Code)

HubSpot Contact Updated (Webhook)
└── Get HubSpot Contact (HubSpot API)
    └── Transform HubSpot → Notion (Code)
        └── Notion Contact Exists? (Conditional)
            ├── Update Notion Contact (Notion API)
            └── Create Notion Contact (Notion API)
                └── Log Success (Code)
```

### Node Details

#### 1. Webhook Triggers
- **Notion Contact Updated**: Listens for Notion database changes
- **HubSpot Contact Updated**: Listens for HubSpot contact property changes

#### 2. Data Retrieval
- **Get Notion Contact**: Fetches full contact data from Notion database
- **Get HubSpot Contact**: Fetches full contact data from HubSpot

#### 3. Data Transformation
- **Transform Notion → HubSpot**: Maps Notion properties to HubSpot format
- **Transform HubSpot → Notion**: Maps HubSpot properties to Notion format

#### 4. Conditional Logic
- **Contact Exists?**: Determines whether to create or update
- Based on cross-reference IDs stored in both systems

#### 5. Sync Operations
- **Update/Create Contact**: Performs the actual sync operation
- **Log Success**: Records successful syncs with metadata

## 🔧 Installation & Setup

### Prerequisites
- n8n Cloud instance or self-hosted n8n
- Notion API access with database permissions
- HubSpot API access with contact permissions
- Environment variables configured

### Quick Setup

1. **Run the setup script:**
```bash
cd /workspaces/automations_hub/n8n/scripts
./setup_contact_sync_webhooks.sh
```

2. **Configure credentials in n8n:**
   - Notion API credentials
   - HubSpot API credentials

3. **Test the workflow:**
```bash
./test_contact_sync.sh
```

### Manual Setup Steps

#### Step 1: Import Workflow
```bash
# Import workflow to n8n
curl -X POST \
    -H "X-N8N-API-KEY: $N8N_API_KEY" \
    -H "Content-Type: application/json" \
    -d @notion_hubspot_contact_sync.json \
    "$N8N_CLOUD_INSTANCE_URL/api/v1/workflows"
```

#### Step 2: Configure HubSpot Webhook
```bash
# Set up HubSpot webhook for contact changes
curl -X POST \
    -H "Authorization: Bearer $HUBSPOT_API_ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
        "eventType": "contact.propertyChange",
        "propertyName": "*",
        "active": true,
        "webhookUrl": "YOUR_N8N_WEBHOOK_URL"
    }' \
    "https://api.hubapi.com/webhooks/v3/subscriptions"
```

#### Step 3: Configure Notion Triggers
Since Notion doesn't support direct webhooks, you have options:
1. **Database automations** (if available in your Notion plan)
2. **Polling trigger** in n8n (check every X minutes)
3. **Third-party webhook bridge** (Zapier, Make.com)

## 🚀 Usage & Testing

### Webhook URLs
After deployment, your webhook URLs will be:
```
Notion → HubSpot: https://your-n8n.app/webhook/notion-contact-updated
HubSpot → Notion: https://your-n8n.app/webhook/hubspot-contact-updated
```

### Testing Sync

#### Test Notion → HubSpot:
```bash
curl -X POST \
    -H "Content-Type: application/json" \
    -d '{
        "page_id": "your-notion-page-id",
        "event": "page.updated"
    }' \
    "https://your-n8n.app/webhook/notion-contact-updated"
```

#### Test HubSpot → Notion:
```bash
curl -X POST \
    -H "Content-Type: application/json" \
    -d '{
        "contact_id": "your-hubspot-contact-id",
        "event": "contact.propertyChange"
    }' \
    "https://your-n8n.app/webhook/hubspot-contact-updated"
```

### Monitoring

Check n8n execution logs for:
- ✅ Successful syncs
- ❌ Failed operations
- ⚠️ Data transformation warnings
- 📊 Sync statistics

## 🔄 Data Flow Examples

### Example 1: New Contact in Notion
1. Contact created in Notion with email and phone
2. Webhook triggers n8n workflow
3. Workflow fetches Notion contact data
4. Transforms to HubSpot format
5. Creates new HubSpot contact
6. Stores cross-reference IDs

### Example 2: Contact Update in HubSpot
1. Contact address updated in HubSpot
2. HubSpot webhook triggers n8n
3. Workflow fetches HubSpot contact data
4. Transforms to Notion format
5. Updates corresponding Notion page
6. Logs successful sync

### Example 3: Name Change Handling
1. Full name "John Smith" changed to "John A. Smith" in Notion
2. Workflow splits name: firstname="John A.", lastname="Smith"
3. Updates both firstname and lastname in HubSpot
4. Maintains name consistency across systems

## ⚙️ Configuration Options

### Sync Direction Control
You can modify the workflow to:
- **One-way only**: Disable one webhook trigger
- **Selective sync**: Add property filters
- **Batch processing**: Add delay nodes for bulk operations

### Property Customization
To add/remove synced properties:
1. Update the `propertyMapping` objects in transformation nodes
2. Test with sample data
3. Deploy updated workflow

### Error Handling
The workflow includes:
- **Retry logic** for API failures
- **Validation** for required fields
- **Logging** for debugging
- **Fallback** strategies for data conflicts

## 🛡️ Security & Best Practices

### API Security
- ✅ Use secure credential storage in n8n
- ✅ Implement webhook signature validation
- ✅ Set up rate limiting
- ✅ Monitor for suspicious activity

### Data Privacy
- ✅ Log only metadata, not sensitive data
- ✅ Implement data retention policies
- ✅ Use encrypted connections (HTTPS)
- ✅ Regular security audits

### Performance
- ✅ Implement batching for bulk operations
- ✅ Use efficient property mapping
- ✅ Monitor API rate limits
- ✅ Optimize webhook payloads

## 🔧 Troubleshooting

### Common Issues

#### Webhook Not Firing
- Check webhook URL configuration
- Verify API keys and permissions
- Test webhook endpoints manually

#### Data Not Syncing
- Check property mapping in transformation nodes
- Verify field permissions in both systems
- Review execution logs for errors

#### Duplicate Contacts
- Ensure cross-reference fields are properly set
- Check contact matching logic
- Implement deduplication rules

#### Performance Issues
- Implement batch processing for bulk operations
- Add delays between API calls
- Monitor rate limit headers

### Debug Mode
Enable debug logging in transformation nodes:
```javascript
console.log('Debug - Input data:', $input.all());
console.log('Debug - Transformed data:', transformedData);
```

## 📈 Monitoring & Analytics

### Key Metrics to Track
- **Sync success rate**: % of successful synchronizations
- **Sync latency**: Time from trigger to completion
- **Error frequency**: Rate of failed syncs
- **Data accuracy**: Consistency between systems

### Dashboard Setup
Create monitoring dashboards for:
- Daily sync volume
- Error trends
- Performance metrics
- Data consistency reports

## 🔄 Maintenance

### Regular Tasks
- **Weekly**: Review error logs and resolve issues
- **Monthly**: Validate data consistency between systems
- **Quarterly**: Update property mappings for new fields
- **Annually**: Security review and credential rotation

### Updates & Improvements
- Monitor n8n updates for new features
- Stay updated with Notion and HubSpot API changes
- Implement user feedback and feature requests
- Optimize performance based on usage patterns

---

## 📋 Files Included

- `notion_hubspot_contact_sync.json` - Main workflow definition
- `setup_contact_sync_webhooks.sh` - Automated setup script
- `test_contact_sync.sh` - Testing script
- `CONTACT_SYNC_GUIDE.md` - This documentation

## 🆘 Support

For issues or questions:
1. Check n8n execution logs
2. Review this documentation
3. Test individual workflow nodes
4. Verify API credentials and permissions

**Happy syncing! 🎉**
