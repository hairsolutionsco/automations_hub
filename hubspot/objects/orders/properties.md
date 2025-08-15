# 0rders Properties

**Object Name:** `orders`

**Object Type ID:** `2-145284183`

**Created:** 2025-07-25T11:07:28.972Z

**Last Modified:** 2025-07-25T11:07:30.768Z

**Total Properties:** 33

---

## Properties Overview

### bool (2)
- `Performed in an import`
- `Read only object`

### datetime (3)
- `Object create date/time`
- `Object last modified date/time`
- `Owner assigned date`

### enumeration (14)
- `All owner IDs`
- `All team IDs`
- `All teams`
- `Business units`
- `Merged record IDs`
- `Owner`
- `Owner's main team`
- `Owning Teams`
- `Record source`
- `Shared teams`
- `Shared users`
- `User IDs of all notification followers`
- `User IDs of all notification unfollowers`
- `User IDs of all owners`

### number (6)
- `Created by user ID`
- `Order Date`
- `Pinned Engagement ID`
- `Record ID`
- `Record creation source user ID`
- `Updated by user ID`

### string (8)
- `Order Number`
- `Order Status`
- `Record creation source`
- `Record creation source ID`
- `Record source detail 1`
- `Record source detail 2`
- `Record source detail 3`
- `Unique creation key`

---

## Detailed Property Documentation

### All owner IDs
- **Name:** `hs_all_owner_ids`
- **Type:** `enumeration`
- **Field Type:** `checkbox`
- **Description:** Values of all default and custom owner properties for this record.

### All team IDs
- **Name:** `hs_all_team_ids`
- **Type:** `enumeration`
- **Field Type:** `checkbox`
- **Description:** The team IDs of all default and custom owner properties for this record.

### All teams
- **Name:** `hs_all_accessible_team_ids`
- **Type:** `enumeration`
- **Field Type:** `checkbox`
- **Description:** The team IDs, including the team hierarchy, of all default and custom owner properties for this record.

### Business units
- **Name:** `hs_all_assigned_business_unit_ids`
- **Type:** `enumeration`
- **Field Type:** `checkbox`
- **Description:** The business units this record is assigned to.

### Created by user ID
- **Name:** `hs_created_by_user_id`
- **Type:** `number`
- **Field Type:** `number`
- **Description:** The user who created this record. This value is set automatically by HubSpot.

### Merged record IDs
- **Name:** `hs_merged_object_ids`
- **Type:** `enumeration`
- **Field Type:** `checkbox`
- **Description:** The list of record IDs that have been merged into this record. This value is set automatically by HubSpot.

### Object create date/time
- **Name:** `hs_createdate`
- **Type:** `datetime`
- **Field Type:** `date`
- **Description:** The date and time at which this object was created. This value is automatically set by HubSpot and may not be modified.

### Object last modified date/time
- **Name:** `hs_lastmodifieddate`
- **Type:** `datetime`
- **Field Type:** `date`
- **Description:** Most recent timestamp of any property update for this object. This includes HubSpot internal properties, which can be visible or hidden. This property is updated automatically.

### Order Date
- **Name:** `order_date`
- **Type:** `number`
- **Field Type:** `number`

### Order Number
- **Name:** `order_number`
- **Type:** `string`
- **Field Type:** `text`
- **Unique:** `true`

### Order Status
- **Name:** `order_status`
- **Type:** `string`
- **Field Type:** `text`

### Owner
- **Name:** `hubspot_owner_id`
- **Type:** `enumeration`
- **Field Type:** `select`
- **Description:** The owner of the object.

### Owner assigned date
- **Name:** `hubspot_owner_assigneddate`
- **Type:** `datetime`
- **Field Type:** `date`
- **Description:** The most recent timestamp of when an owner was assigned to this record. This value is set automatically by HubSpot.

### Owner's main team
- **Name:** `hubspot_team_id`
- **Type:** `enumeration`
- **Field Type:** `select`
- **Description:** The main team of the record owner. This value is set automatically by HubSpot.

### Owning Teams
- **Name:** `hs_owning_teams`
- **Type:** `enumeration`
- **Field Type:** `checkbox`
- **Description:** The teams that are attributed to this record.

### Performed in an import
- **Name:** `hs_was_imported`
- **Type:** `bool`
- **Field Type:** `booleancheckbox`
- **Description:** Object is part of an import

### Pinned Engagement ID
- **Name:** `hs_pinned_engagement_id`
- **Type:** `number`
- **Field Type:** `number`
- **Description:** The object ID of the current pinned engagement. This will only be shown in the app if there is already an association to the engagement.

### Read only object
- **Name:** `hs_read_only`
- **Type:** `bool`
- **Field Type:** `booleancheckbox`
- **Description:** Determines whether a record can be edited by a user.

### Record creation source
- **Name:** `hs_object_source`
- **Type:** `string`
- **Field Type:** `text`
- **Description:** Raw internal PropertySource present in the RequestMeta when this record was created.

### Record creation source ID
- **Name:** `hs_object_source_id`
- **Type:** `string`
- **Field Type:** `text`
- **Description:** Raw internal sourceId present in the RequestMeta when this record was created.

### Record creation source user ID
- **Name:** `hs_object_source_user_id`
- **Type:** `number`
- **Field Type:** `number`
- **Description:** Raw internal userId present in the RequestMeta when this record was created.

### Record ID
- **Name:** `hs_object_id`
- **Type:** `number`
- **Field Type:** `number`
- **Description:** The unique ID for this record. This value is set automatically by HubSpot.

### Record source
- **Name:** `hs_object_source_label`
- **Type:** `enumeration`
- **Field Type:** `select`
- **Description:** How this record was created.

### Record source detail 1
- **Name:** `hs_object_source_detail_1`
- **Type:** `string`
- **Field Type:** `text`
- **Description:** First level of detail on how this record was created.

### Record source detail 2
- **Name:** `hs_object_source_detail_2`
- **Type:** `string`
- **Field Type:** `text`
- **Description:** Second level of detail on how this record was created.

### Record source detail 3
- **Name:** `hs_object_source_detail_3`
- **Type:** `string`
- **Field Type:** `text`
- **Description:** Third level of detail on how this record was created.

### Shared teams
- **Name:** `hs_shared_team_ids`
- **Type:** `enumeration`
- **Field Type:** `checkbox`
- **Description:** Additional teams whose users can access the record based on their permissions. This can be set manually or through Workflows or APIs.

### Shared users
- **Name:** `hs_shared_user_ids`
- **Type:** `enumeration`
- **Field Type:** `checkbox`
- **Description:** Additional users that can access the record based on their permissions. This can be set manually or through Workflows and APIs.

### Unique creation key
- **Name:** `hs_unique_creation_key`
- **Type:** `string`
- **Field Type:** `text`
- **Unique:** `true`
- **Description:** Unique property used for idempotent creates

### Updated by user ID
- **Name:** `hs_updated_by_user_id`
- **Type:** `number`
- **Field Type:** `number`
- **Description:** The user who last updated this record. This value is set automatically by HubSpot.

### User IDs of all notification followers
- **Name:** `hs_user_ids_of_all_notification_followers`
- **Type:** `enumeration`
- **Field Type:** `checkbox`
- **Description:** The user IDs of all users that have clicked follow within the object to opt-in to getting follow notifications

### User IDs of all notification unfollowers
- **Name:** `hs_user_ids_of_all_notification_unfollowers`
- **Type:** `enumeration`
- **Field Type:** `checkbox`
- **Description:** The user IDs of all object owners that have clicked unfollow within the object to opt-out of getting follow notifications

### User IDs of all owners
- **Name:** `hs_user_ids_of_all_owners`
- **Type:** `enumeration`
- **Field Type:** `checkbox`
- **Description:** The user IDs of all owners of this record.

## 🚫 Empty & Unused Properties

*Analysis based on approximately 500 records*

### Completely Empty Properties (20)
*These properties have no data in any analyzed record:*

- `hs_all_accessible_team_ids`
- `hs_all_assigned_business_unit_ids`
- `hs_all_owner_ids`
- `hs_all_team_ids`
- `hs_merged_object_ids`
- `hs_object_source_detail_3`
- `hs_owning_teams`
- `hs_pinned_engagement_id`
- `hs_read_only`
- `hs_shared_team_ids`
- `hs_shared_user_ids`
- `hs_unique_creation_key`
- `hs_user_ids_of_all_notification_followers`
- `hs_user_ids_of_all_notification_unfollowers`
- `hs_user_ids_of_all_owners`
- `hubspot_owner_assigneddate`
- `hubspot_owner_id`
- `hubspot_team_id`
- `order_number`
- `order_status`

### Mostly Empty Properties (5)
*These properties have data in less than 5% of analyzed records:*

- `order_date` - 99.8% empty, only 1 records with data
- `hs_created_by_user_id` - 96.6% empty, only 17 records with data
- `hs_object_source_user_id` - 96.6% empty, only 17 records with data
- `hs_updated_by_user_id` - 96.6% empty, only 17 records with data
- `hs_was_imported` - 96.6% empty, only 17 records with data

---

*Documentation generated on 2025-08-14 13:43:05*