# Property Matching Report: Notion ↔ HubSpot
        
**Generated:** 2025-08-15 04:56:57

## Executive Summary

This report analyzes and matches properties between Notion databases and HubSpot contact properties, providing insights for data synchronization and integration planning.

### Statistics
- **Notion Databases Analyzed:** 1
- **Total Notion Properties:** 24
- **HubSpot Contact Properties:** 636
- **Potential Matches Found:** 44
- **High-Quality Matches:** 17
- **Medium-Quality Matches:** 15

## Matching Methodology

The matching algorithm uses a combination of:
1. **Semantic Similarity (70% weight):** String similarity between property names and labels
2. **Type Compatibility (30% weight):** Data type compatibility between systems
3. **Normalization:** Removes common prefixes/suffixes and standardizes naming

### Match Quality Levels
- **High (>0.8):** Strong confidence, likely direct mapping candidates
- **Medium (0.65-0.8):** Good candidates requiring validation
- **Low (0.5-0.65):** Possible matches requiring careful review


## 🟢 High-Quality Matches (Strong Candidates)

### contacts → HubSpot Contact

**Notion Property:** `Email` (email)  
**HubSpot Property:** `email` (string)  
**HubSpot Label:** Email  
**HubSpot Group:** contactinformation  

**Match Scores:**
- Semantic Similarity: 1.0
- Type Compatibility: 1.0
- Overall Score: 1.0 (High)

**HubSpot Description:** A contact's email address

---

### contacts → HubSpot Contact

**Notion Property:** `Access Point Location` (rich_text)  
**HubSpot Property:** `access_point_location` (string)  
**HubSpot Label:** Access Point Location  
**HubSpot Group:** address_&_shipping_information  

**Match Scores:**
- Semantic Similarity: 1.0
- Type Compatibility: 1.0
- Overall Score: 1.0 (High)

**HubSpot Description:** Access point details for client shipments.

---

### contacts → HubSpot Contact

**Notion Property:** `Marketing contact status` (select)  
**HubSpot Property:** `hs_marketable_status` (enumeration)  
**HubSpot Label:** Marketing contact status  
**HubSpot Group:** contactinformation  

**Match Scores:**
- Semantic Similarity: 1.0
- Type Compatibility: 1.0
- Overall Score: 1.0 (High)

**HubSpot Description:** The marketing status of a contact

---

### contacts → HubSpot Contact

**Notion Property:** `Address` (rich_text)  
**HubSpot Property:** `address` (string)  
**HubSpot Label:** Street Address  
**HubSpot Group:** contactinformation  

**Match Scores:**
- Semantic Similarity: 1.0
- Type Compatibility: 1.0
- Overall Score: 1.0 (High)

**HubSpot Description:** Contact's street address, including apartment or unit number.

---

### contacts → HubSpot Contact

**Notion Property:** `Phone Number` (phone_number)  
**HubSpot Property:** `phone` (string)  
**HubSpot Label:** Phone Number  
**HubSpot Group:** contactinformation  

**Match Scores:**
- Semantic Similarity: 1.0
- Type Compatibility: 1.0
- Overall Score: 1.0 (High)

**HubSpot Description:** A contact's primary phone number

---

### contacts → HubSpot Contact

**Notion Property:** `Shipping Profile` (multi_select)  
**HubSpot Property:** `shipping_profile` (enumeration)  
**HubSpot Label:** Shipping Profile  
**HubSpot Group:** contactinformation  

**Match Scores:**
- Semantic Similarity: 1.0
- Type Compatibility: 1.0
- Overall Score: 1.0 (High)

**HubSpot Description:** No description available

---

### contacts → HubSpot Contact

**Notion Property:** `Re-Engagement Notes` (rich_text)  
**HubSpot Property:** `reengagementnotes` (string)  
**HubSpot Label:** Re-Engagement Notes  
**HubSpot Group:** contactinformation  

**Match Scores:**
- Semantic Similarity: 1.0
- Type Compatibility: 1.0
- Overall Score: 1.0 (High)

**HubSpot Description:** No description available

---

### contacts → HubSpot Contact

**Notion Property:** `Lifecycle Stage` (select)  
**HubSpot Property:** `lifecyclestage` (enumeration)  
**HubSpot Label:** Lifecycle Stage  
**HubSpot Group:** contactinformation  

**Match Scores:**
- Semantic Similarity: 1.0
- Type Compatibility: 1.0
- Overall Score: 1.0 (High)

**HubSpot Description:** The qualification of contacts to sales readiness. It can be set through imports, forms, workflows, and manually on a per contact basis.

---

### contacts → HubSpot Contact

**Notion Property:** `Contact Profile` (multi_select)  
**HubSpot Property:** `contact_type` (enumeration)  
**HubSpot Label:** Contact Profile  
**HubSpot Group:** contactinformation  

**Match Scores:**
- Semantic Similarity: 1.0
- Type Compatibility: 1.0
- Overall Score: 1.0 (High)

**HubSpot Description:** No description available

---

### contacts → HubSpot Contact

**Notion Property:** `Contact Profile` (multi_select)  
**HubSpot Property:** `customer_profile` (enumeration)  
**HubSpot Label:** Sales Contact Profile  
**HubSpot Group:** contactinformation  

**Match Scores:**
- Semantic Similarity: 1.0
- Type Compatibility: 1.0
- Overall Score: 1.0 (High)

**HubSpot Description:** No description available

---

### contacts → HubSpot Contact

**Notion Property:** `Client Number` (rich_text)  
**HubSpot Property:** `client_number` (string)  
**HubSpot Label:** Client Number  
**HubSpot Group:** contactinformation  

**Match Scores:**
- Semantic Similarity: 1.0
- Type Compatibility: 1.0
- Overall Score: 1.0 (High)

**HubSpot Description:** Client number (with Division code: #EUR , #CANUS)

---

### contacts → HubSpot Contact

**Notion Property:** `Name` (title)  
**HubSpot Property:** `name_new` (string)  
**HubSpot Label:** Name  
**HubSpot Group:** contactinformation  

**Match Scores:**
- Semantic Similarity: 1.0
- Type Compatibility: 1.0
- Overall Score: 1.0 (High)

**HubSpot Description:** No description available

---

### contacts → HubSpot Contact

**Notion Property:** `Marketing contact status` (select)  
**HubSpot Property:** `hs_marketable_reason_type` (enumeration)  
**HubSpot Label:** Marketing contact status source type  
**HubSpot Group:** contactinformation  

**Match Scores:**
- Semantic Similarity: 0.8
- Type Compatibility: 1.0
- Overall Score: 0.86 (High)

**HubSpot Description:** The type of the activity that set the contact as a marketing contact

---

### contacts → HubSpot Contact

**Notion Property:** `Phone Number` (phone_number)  
**HubSpot Property:** `mobilephone` (string)  
**HubSpot Label:** Mobile Phone Number  
**HubSpot Group:** contactinformation  

**Match Scores:**
- Semantic Similarity: 0.774
- Type Compatibility: 1.0
- Overall Score: 0.842 (High)

**HubSpot Description:** A contact's mobile phone number

---

### contacts → HubSpot Contact

**Notion Property:** `Client Number` (rich_text)  
**HubSpot Property:** `fax` (string)  
**HubSpot Label:** Fax Number  
**HubSpot Group:** contactinformation  

**Match Scores:**
- Semantic Similarity: 0.75
- Type Compatibility: 1.0
- Overall Score: 0.825 (High)

**HubSpot Description:** A contact's primary fax number

---

### contacts → HubSpot Contact

**Notion Property:** `Contact Profile` (multi_select)  
**HubSpot Property:** `inquiry_profile` (enumeration)  
**HubSpot Label:** Lead Profile  
**HubSpot Group:** contactinformation  

**Match Scores:**
- Semantic Similarity: 0.737
- Type Compatibility: 1.0
- Overall Score: 0.816 (High)

**HubSpot Description:** No description available

---

### contacts → HubSpot Contact

**Notion Property:** `Phone Number` (phone_number)  
**HubSpot Property:** `hs_whatsapp_phone_number` (string)  
**HubSpot Label:** WhatsApp Phone Number  
**HubSpot Group:** contactinformation  

**Match Scores:**
- Semantic Similarity: 0.727
- Type Compatibility: 1.0
- Overall Score: 0.809 (High)

**HubSpot Description:** The phone number associated with the contact’s WhatsApp account.

---


## 🟡 Medium-Quality Matches (Good Candidates)

### contacts → HubSpot Contact

**Notion Property:** `Current Factory` (select)  
**HubSpot Property:** `contact_currency` (enumeration)  
**HubSpot Label:** Contact Currency  
**HubSpot Group:** contactinformation  

**Match Scores:**
- Semantic Similarity: 0.696
- Type Compatibility: 1.0
- Overall Score: 0.787 (Medium)

**HubSpot Description:** No description available

---

### contacts → HubSpot Contact

**Notion Property:** `New Factory` (select)  
**HubSpot Property:** `last_factory` (enumeration)  
**HubSpot Label:** Last Factory  
**HubSpot Group:** purchase_orders_sync_properties  

**Match Scores:**
- Semantic Similarity: 0.696
- Type Compatibility: 1.0
- Overall Score: 0.787 (Medium)

**HubSpot Description:** No description available

---

### contacts → HubSpot Contact

**Notion Property:** `Email` (email)  
**HubSpot Property:** `owneremail` (string)  
**HubSpot Label:** HubSpot Owner Email (legacy)  
**HubSpot Group:** sales_properties  

**Match Scores:**
- Semantic Similarity: 0.667
- Type Compatibility: 1.0
- Overall Score: 0.767 (Medium)

**HubSpot Description:** A legacy property used to identify the email address of the owner of the contact. This property is no longer in use.

---

### contacts → HubSpot Contact

**Notion Property:** `Address` (rich_text)  
**HubSpot Property:** `address_line_2` (string)  
**HubSpot Label:** Street Address 2  
**HubSpot Group:** contactinformation  

**Match Scores:**
- Semantic Similarity: 0.667
- Type Compatibility: 1.0
- Overall Score: 0.767 (Medium)

**HubSpot Description:** Additional address information

---

### contacts → HubSpot Contact

**Notion Property:** `Current Factory` (select)  
**HubSpot Property:** `last_factory` (enumeration)  
**HubSpot Label:** Last Factory  
**HubSpot Group:** purchase_orders_sync_properties  

**Match Scores:**
- Semantic Similarity: 0.667
- Type Compatibility: 1.0
- Overall Score: 0.767 (Medium)

**HubSpot Description:** No description available

---

### contacts → HubSpot Contact

**Notion Property:** `Client Number` (rich_text)  
**HubSpot Property:** `phone` (string)  
**HubSpot Label:** Phone Number  
**HubSpot Group:** contactinformation  

**Match Scores:**
- Semantic Similarity: 0.667
- Type Compatibility: 1.0
- Overall Score: 0.767 (Medium)

**HubSpot Description:** A contact's primary phone number

---

### contacts → HubSpot Contact

**Notion Property:** `Hubspot Contacts Record ID` (number)  
**HubSpot Property:** `hubspotscore` (number)  
**HubSpot Label:** HubSpot Score  
**HubSpot Group:** hubspot_properties  

**Match Scores:**
- Semantic Similarity: 0.667
- Type Compatibility: 1.0
- Overall Score: 0.767 (Medium)

**HubSpot Description:** The number that shows qualification of contacts to sales readiness. It can be set in HubSpot's Lead Scoring app.

---

### contacts → HubSpot Contact

**Notion Property:** `Name` (title)  
**HubSpot Property:** `lastname` (string)  
**HubSpot Label:** Last Name  
**HubSpot Group:** contactinformation  

**Match Scores:**
- Semantic Similarity: 0.667
- Type Compatibility: 1.0
- Overall Score: 0.767 (Medium)

**HubSpot Description:** A contact's last name

---

### contacts → HubSpot Contact

**Notion Property:** `Shipping Profile` (multi_select)  
**HubSpot Property:** `inquiry_profile` (enumeration)  
**HubSpot Label:** Lead Profile  
**HubSpot Group:** contactinformation  

**Match Scores:**
- Semantic Similarity: 0.645
- Type Compatibility: 1.0
- Overall Score: 0.752 (Medium)

**HubSpot Description:** No description available

---

### contacts → HubSpot Contact

**Notion Property:** `Hubspot Contacts Record ID` (number)  
**HubSpot Property:** `hubspot_score_2` (number)  
**HubSpot Label:** Old Hub Contacts Engagement Activities Score  
**HubSpot Group:** analyticsinformation  

**Match Scores:**
- Semantic Similarity: 0.632
- Type Compatibility: 1.0
- Overall Score: 0.742 (Medium)

**HubSpot Description:** The number that shows qualification of contacts to sales readiness. It can be set in HubSpot's Lead Scoring app.

---

### contacts → HubSpot Contact

**Notion Property:** `Hair Orders Profiles` (relation)  
**HubSpot Property:** `inquiry_profile` (enumeration)  
**HubSpot Label:** Lead Profile  
**HubSpot Group:** contactinformation  

**Match Scores:**
- Semantic Similarity: 0.625
- Type Compatibility: 1.0
- Overall Score: 0.738 (Medium)

**HubSpot Description:** No description available

---

### contacts → HubSpot Contact

**Notion Property:** `Name` (title)  
**HubSpot Property:** `firstname` (string)  
**HubSpot Label:** First Name  
**HubSpot Group:** contactinformation  

**Match Scores:**
- Semantic Similarity: 0.615
- Type Compatibility: 1.0
- Overall Score: 0.731 (Medium)

**HubSpot Description:** A contact's first name

---

### contacts → HubSpot Contact

**Notion Property:** `Hair Orders Profiles` (relation)  
**HubSpot Property:** `skin_hairline_borders_details` (enumeration)  
**HubSpot Label:** Skin Hairline/Borders Details  
**HubSpot Group:** order_customisation_details  

**Match Scores:**
- Semantic Similarity: 0.612
- Type Compatibility: 1.0
- Overall Score: 0.729 (Medium)

**HubSpot Description:** No description available

---

### contacts → HubSpot Contact

**Notion Property:** `Address` (rich_text)  
**HubSpot Property:** `shipping_address` (string)  
**HubSpot Label:** Shipping Address  
**HubSpot Group:** contactinformation  

**Match Scores:**
- Semantic Similarity: 0.609
- Type Compatibility: 1.0
- Overall Score: 0.726 (Medium)

**HubSpot Description:** The preferred address of the client to send package

---

### contacts → HubSpot Contact

**Notion Property:** `Country/Region` (select)  
**HubSpot Property:** `country` (string)  
**HubSpot Label:** Country/Region  
**HubSpot Group:** contactinformation  

**Match Scores:**
- Semantic Similarity: 1.0
- Type Compatibility: 0.0
- Overall Score: 0.7 (Medium)

**HubSpot Description:** The contact's country/region of residence. This might be set via import, form, or integration.

---


## 🟠 Low-Quality Matches (Requires Review)

### contacts → HubSpot Contact

**Notion Property:** `Associated Deals` (relation)  
**HubSpot Property:** `num_associated_deals` (number)  
**HubSpot Label:** Number of Associated Deals  
**HubSpot Group:** deal_information  

**Match Scores:**
- Semantic Similarity: 0.889
- Type Compatibility: 0.0
- Overall Score: 0.622 (Low)

**HubSpot Description:** Count of deals associated with this contact. Set automatically by HubSpot.

---

### contacts → HubSpot Contact

**Notion Property:** `Associated Companies` (relation)  
**HubSpot Property:** `associatedcompanyid` (number)  
**HubSpot Label:** Primary Associated Company ID  
**HubSpot Group:** contactinformation  

**Match Scores:**
- Semantic Similarity: 0.872
- Type Compatibility: 0.0
- Overall Score: 0.61 (Low)

**HubSpot Description:** HubSpot defined ID of a contact's primary associated company in HubSpot.

---

### contacts → HubSpot Contact

**Notion Property:** `Country/Region` (select)  
**HubSpot Property:** `hs_country_region_code` (string)  
**HubSpot Label:** Country/Region Code  
**HubSpot Group:** contactinformation  

**Match Scores:**
- Semantic Similarity: 0.848
- Type Compatibility: 0.0
- Overall Score: 0.594 (Low)

**HubSpot Description:** The contact's two-letter country code.

---

### contacts → HubSpot Contact

**Notion Property:** `Marketing contact status` (select)  
**HubSpot Property:** `hs_marketable_reason_id` (string)  
**HubSpot Label:** Marketing contact status source name  
**HubSpot Group:** contactinformation  

**Match Scores:**
- Semantic Similarity: 0.8
- Type Compatibility: 0.0
- Overall Score: 0.56 (Low)

**HubSpot Description:** The ID of the activity that set the contact as a marketing contact

---

### contacts → HubSpot Contact

**Notion Property:** `Notion Contacts Record ID` (unique_id)  
**HubSpot Property:** `notion_contact_id` (string)  
**HubSpot Label:** Notion Contact ID  
**HubSpot Group:** contactinformation  

**Match Scores:**
- Semantic Similarity: 0.778
- Type Compatibility: 0.0
- Overall Score: 0.544 (Low)

**HubSpot Description:** No description available

---

### contacts → HubSpot Contact

**Notion Property:** `Associated Orders` (relation)  
**HubSpot Property:** `num_associated_deals` (number)  
**HubSpot Label:** Number of Associated Deals  
**HubSpot Group:** deal_information  

**Match Scores:**
- Semantic Similarity: 0.757
- Type Compatibility: 0.0
- Overall Score: 0.53 (Low)

**HubSpot Description:** Count of deals associated with this contact. Set automatically by HubSpot.

---

### contacts → HubSpot Contact

**Notion Property:** `Associated Plans` (relation)  
**HubSpot Property:** `associatedcompanyid` (number)  
**HubSpot Label:** Primary Associated Company ID  
**HubSpot Group:** contactinformation  

**Match Scores:**
- Semantic Similarity: 0.743
- Type Compatibility: 0.0
- Overall Score: 0.52 (Low)

**HubSpot Description:** HubSpot defined ID of a contact's primary associated company in HubSpot.

---

### contacts → HubSpot Contact

**Notion Property:** `Access Point Location` (rich_text)  
**HubSpot Property:** `access_point` (enumeration)  
**HubSpot Label:** Access Point  
**HubSpot Group:** address_&_shipping_information  

**Match Scores:**
- Semantic Similarity: 0.727
- Type Compatibility: 0.0
- Overall Score: 0.509 (Low)

**HubSpot Description:** Ship to access point

---

### contacts → HubSpot Contact

**Notion Property:** `Associated Plans` (relation)  
**HubSpot Property:** `num_associated_deals` (number)  
**HubSpot Label:** Number of Associated Deals  
**HubSpot Group:** deal_information  

**Match Scores:**
- Semantic Similarity: 0.722
- Type Compatibility: 0.0
- Overall Score: 0.506 (Low)

**HubSpot Description:** Count of deals associated with this contact. Set automatically by HubSpot.

---

### contacts → HubSpot Contact

**Notion Property:** `Associated Tasks` (relation)  
**HubSpot Property:** `num_associated_deals` (number)  
**HubSpot Label:** Number of Associated Deals  
**HubSpot Group:** deal_information  

**Match Scores:**
- Semantic Similarity: 0.722
- Type Compatibility: 0.0
- Overall Score: 0.506 (Low)

**HubSpot Description:** Count of deals associated with this contact. Set automatically by HubSpot.

---

### contacts → HubSpot Contact

**Notion Property:** `Re-Engagement Notes` (rich_text)  
**HubSpot Property:** `hs_last_sales_activity_timestamp` (datetime)  
**HubSpot Label:** Last Engagement Date  
**HubSpot Group:** contact_activity  

**Match Scores:**
- Semantic Similarity: 0.718
- Type Compatibility: 0.0
- Overall Score: 0.503 (Low)

**HubSpot Description:** The last time a contact engaged with your site or a form, document, meetings link, or tracked email. This doesn't include marketing emails or emails to multiple contacts.

---

### contacts → HubSpot Contact

**Notion Property:** `Re-Engagement Notes` (rich_text)  
**HubSpot Property:** `hs_last_sales_activity_type` (enumeration)  
**HubSpot Label:** Last Engagement Type  
**HubSpot Group:** contactinformation  

**Match Scores:**
- Semantic Similarity: 0.718
- Type Compatibility: 0.0
- Overall Score: 0.503 (Low)

**HubSpot Description:** The type of the last engagement a contact performed. This doesn't include marketing emails or emails to multiple contacts.

---


## Database-by-Database Breakdown

### Contacts
- **Total Properties:** 24
- **Matches Found:** 44
- **Match Rate:** 183.3%

  - `Email` → `email` (High)
  - `Access Point Location` → `access_point_location` (High)
  - `Marketing contact status` → `hs_marketable_status` (High)
  - `Address` → `address` (High)
  - `Phone Number` → `phone` (High)
  - ... and 39 more matches


## Unmapped Properties Analysis

### Notion Properties Without Matches (2)

- **contacts**: `Archive (Associated Companies)` (rich_text)
- **contacts**: `Associated Payment` (relation)

### HubSpot Properties Without Matches (600)

- `accepts_shipments` (enumeration) - Accepts Shipments
- `active_client_profile` (enumeration) - Active Client Profile
- `additional_details_for_hybrid_bases` (string) - Hybrid Base - Additional Information
- `airtable_id` (string) - Airtable ID
- `annualrevenue` (string) - Annual Revenue
- `associatedcompanylastupdated` (number) - Associated Company Last Updated
- `average_pageviews__old_hub_` (number) - Average Pageviews (Old Hub)
- `barber_name` (string) - Barber Name
- `base_length___measurements` (string) - Full Length (L1)
- `base_material__factory_model_` (enumeration) - Base Material (Factory Model)
- `base_material_model` (enumeration) - Base Material
- `base_material_new` (string) - Base Material Details
- `base_size_master` (enumeration) - Base Size Master
- `base_width___measurements` (string) - Center Width (W1)
- `billing_address_city` (string) - Billing Address: City
- `billing_address_country` (string) - Billing Address: Country
- `billing_address_google_maps_url` (string) - Billing Address: Google Maps URL
- `billing_address_lat` (string) - Billing Address: Lat
- `billing_address_long` (string) - Billing Address: Long
- `billing_address_name` (string) - Billing Address: Name
- ... and 580 more


## Property Type Analysis

### Notion Property Types
- **relation**: 7 properties
- **rich_text**: 5 properties
- **select**: 5 properties
- **multi_select**: 2 properties
- **email**: 1 properties
- **unique_id**: 1 properties
- **phone_number**: 1 properties
- **number**: 1 properties
- **title**: 1 properties

### HubSpot Property Types
- **string**: 251 properties
- **enumeration**: 132 properties
- **number**: 117 properties
- **datetime**: 96 properties
- **bool**: 19 properties
- **date**: 15 properties
- **phone_number**: 4 properties
- **object_coordinates**: 2 properties

## Recommendations

### Immediate Actions
1. **Implement High-Quality Matches (17)**: These mappings have strong confidence and can be implemented with minimal validation.

2. **Validate Medium-Quality Matches (15)**: Review these mappings for business logic compatibility before implementation.

3. **Custom Property Strategy**: Consider creating custom HubSpot properties for unmapped Notion fields that are business-critical.

### Integration Strategy
1. **Start with Contact Synchronization**: Focus on the strongest matches for contact data first.
2. **Implement Bi-directional Sync**: Consider which direction should be the source of truth for each property.
3. **Data Validation**: Implement validation rules to ensure data integrity during synchronization.
4. **Regular Reviews**: Properties and business needs evolve; schedule quarterly reviews of mappings.

### Technical Considerations
1. **Data Type Conversion**: Plan for type conversions (e.g., multi-select to single values).
2. **Field Length Limits**: HubSpot has character limits for different field types.
3. **API Rate Limits**: Plan synchronization frequency considering API limitations.
4. **Error Handling**: Implement robust error handling for failed synchronizations.

---

*Report generated by Property Matcher v1.0*
