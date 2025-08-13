# Tasks Database

**Database ID:** `226f4e0d-84e0-8168-8718-d8f6b2d1fe3d`

**Created:** 2025-07-04T20:24:00.000Z
**Last Modified:** 2025-08-13T19:16:00.000Z
**Total Properties:** 37

---

## Properties Overview

### checkbox (1)
- `Archive`

### created_by (1)
- `Created by`

### created_time (1)
- `Created time`

### date (2)
- `Activity date`
- `Timeline / due date`

### formula (7)
- `Date between`
- `Done?`
- `Due Status`
- `Hours spent formula`
- `Time Spent. (min)`
- `Total Time`
- `Total labour Cost`

### number (2)
- `Freelancer Pay`
- `Hubspot Tasks Record ID`

### people (1)
- `Assignee ping`

### relation (5)
- `Associated Contacts`
- `Associated Deals`
- `Parent item`
- `Project`
- `Sub-Tasks`

### rich_text (6)
- `AI summary`
- `Activity assigned to`
- `Associated Companies`
- `Associated Contacts (Text)`
- `Associated Deals (Text)`
- `Associated Tickets`

### rollup (6)
- `Current Factory`
- `Deal Associated Orders`
- `Last PO Cost`
- `New Factory`
- `Premade Compatibility`
- `Rollup 1`

### select (2)
- `Activity type`
- `Priority`

### status (1)
- `Status`

### title (1)
- `Name`

### unique_id (1)
- `Notion Tasks Record ID`

---

## Detailed Property Documentation

### AI summary
- **Type:** `rich_text`

### Activity assigned to
- **Type:** `rich_text`

### Activity date
- **Type:** `date`

### Activity type
- **Type:** `select`
- **Options:**
  - `Task`

### Archive
- **Type:** `checkbox`

### Assignee ping
- **Type:** `people`

### Associated Companies
- **Type:** `rich_text`

### Associated Contacts
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-814c-ad70-d478cebeee30`

### Associated Contacts (Text)
- **Type:** `rich_text`

### Associated Deals
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-808c-af51-e09c154008db`

### Associated Deals (Text)
- **Type:** `rich_text`

### Associated Tickets
- **Type:** `rich_text`

### Created by
- **Type:** `created_by`

### Created time
- **Type:** `created_time`

### Current Factory
- **Type:** `rollup`
- **Relation Property:** `Associated Contacts`
- **Rollup Property:** `Current Factory`
- **Function:** `show_original`

### Date between
- **Type:** `formula`
- **Formula:** `dateBetween(now(), dateEnd({{notion:block_property:xSF_:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}), "days")`

### Deal Associated Orders
- **Type:** `rollup`
- **Relation Property:** `Associated Deals`
- **Rollup Property:** `Associated Orders`
- **Function:** `show_original`

### Done?
- **Type:** `formula`
- **Formula:** `if({{notion:block_property:K%60Y%7C:226f4e0d-84e0-81d0-8c9a-000ba17de0e7:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} == "Done", true, false)`

### Due Status
- **Type:** `formula`
- **Formula:** `if({{notion:block_property:K%60Y%7C:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}== "Done" , style("✓ Completed","b","green"), (if({{notion:block_property:xl_p:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}<0,"Due in " + {{notion:block_property:xl_p:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}*-1 + " days" , if({{notion:block_property:xl_p:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} > 0, (("⭕ Overdue by " + format({{notion:block_property:xl_p:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}})) + if({{notion:block_property:xl_p:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} == 1, " day", " days")).style("b","c"), "Not Overdue"))))`

### Freelancer Pay
- **Type:** `number`

### Hours spent formula
- **Type:** `formula`
- **Formula:** `{{notion:block_property:l~Qx:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}/60`

### Hubspot Tasks Record ID
- **Type:** `number`

### Last PO Cost
- **Type:** `rollup`
- **Relation Property:** `Associated Contacts`
- **Rollup Property:** `Last PO Cost`
- **Function:** `show_original`

### Name
- **Type:** `title`

### New Factory
- **Type:** `rollup`
- **Relation Property:** `Associated Contacts`
- **Rollup Property:** `New Factory`
- **Function:** `show_original`

### Notion Tasks Record ID
- **Type:** `unique_id`

### Parent item
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-8168-8718-d8f6b2d1fe3d`

### Premade Compatibility
- **Type:** `rollup`
- **Relation Property:** `Associated Contacts`
- **Rollup Property:** `Premade Compatibiity`
- **Function:** `show_original`

### Priority
- **Type:** `select`
- **Options:**
  - `Medium`
  - `High`
  - `Low`
  - `None`

### Project
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-816d-a749-e741b1ac0b30`

### Rollup 1
- **Type:** `rollup`
- **Relation Property:** `Associated Contacts`
- **Rollup Property:** `Order Email`
- **Function:** `show_original`

### Status
- **Type:** `status`

### Sub-Tasks
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-8168-8718-d8f6b2d1fe3d`

### Time Spent. (min)
- **Type:** `formula`
- **Formula:** `{{notion:block_property:l~Qx:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}`

### Timeline / due date
- **Type:** `date`

### Total Time
- **Type:** `formula`
- **Formula:** `format((if(({{notion:block_property:l~Qx:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} >= 60), (format(floor({{notion:block_property:l~Qx:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} / 60)) + " hours "), "") + if((({{notion:block_property:l~Qx:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} % 60) > 0), (format({{notion:block_property:l~Qx:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} % 60) + " minutes "), "0 minutes")))`

### Total labour Cost
- **Type:** `formula`
- **Formula:** `if(empty({{notion:block_property:fNSB:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}),{{notion:block_property:cnz%3C:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}},{{notion:block_property:fNSB:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}})`

## 🚫 Empty & Unused Properties

*Analysis based on 207 pages*

### Completely Empty Properties (14)
*These properties have no data in any page:*

- `Activity assigned to` (rich_text)
- `Archive` (checkbox)
- `Assignee ping` (people)
- `Date between` (formula)
- `Due Status` (formula)
- `Freelancer Pay` (number)
- `Hours spent formula` (formula)
- `Parent item` (relation)
- `Project` (relation)
- `Sub-Tasks` (relation)
- `Time Spent. (min)` (formula)
- `Timeline / due date` (date)
- `Total Time` (formula)
- `Total labour Cost` (formula)

### Mostly Empty Properties (1)
*These properties have data in less than 5% of pages:*

- `Associated Tickets` (rich_text) - 99.5% empty, only 1 pages with data

## Related Databases

- **Sub-Tasks** (`226f4e0d-84e0-8168-8718-d8f6b2d1fe3d`)
- **Parent item** (`226f4e0d-84e0-8168-8718-d8f6b2d1fe3d`)
- **Associated Deals** (`226f4e0d-84e0-808c-af51-e09c154008db`)
- **Project** (`226f4e0d-84e0-816d-a749-e741b1ac0b30`)
- **Associated Contacts** (`226f4e0d-84e0-814c-ad70-d478cebeee30`)

---

*Documentation generated on 2025-08-13 19:50:35*
