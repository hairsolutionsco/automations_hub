# Untitled Database

**Database ID:** `226f4e0d-84e0-808c-af51-e09c154008db`

**Created:** 2025-07-04T23:04:00.000Z
**Last Modified:** 2025-08-13T19:15:00.000Z
**Total Properties:** 54

---

## Properties Overview

- **Button** (2): `Refund Payment`, `Create Income`
- **Checkbox** (3): `Emergency List`, `To check`, `Orders Complete`
- **Date** (5): `Plan End Date`, `Payment Date`, `Plan Start Date`, `Close Date`, `Last Activity Date`
- **Formula** (9): `Profit`, `Auto Total`, `Current Month?`, `Formula`, `Income Status`, `Current Month profit`, `Time since order`, `Retail Price`, `Income`
- **Multi_Select** (1): `Deal Profile`
- **Number** (10): `Annual contract value`, `Amount (USD)`, `Annual recurring revenue`, `Exchange rate`, `Monthly recurring revenue`, `Override Total`, `Amount`, `Deal Size (#)`, `Qty`, `Hubspot Deals Record ID`
- **Relation** (8): `Associated Plan`, `Associated Client`, `Inventory Products`, `Linked Subscriptions`, `Associated Contacts`, `Associated Orders`, `Tasks`, `Month`
- **Rich_Text** (5): `Summary`, `Deal Name`, `Deal Name (Archive)`, `Orders Tasks`, `Next Activity Date`
- **Rollup** (4): `Rollup 2`, `Rollup`, `profi`, `Rollup 1`
- **Select** (5): `Deal Type`, `Priority`, `Deal Size`, `Deal Stage`, `Currency`
- **Title** (1): `Name`
- **Unique_Id** (1): `Notion Deals Record ID`

---

## Detailed Property Documentation

### Amount
- **Type:** `number`
- **Format:** `number`

### Amount (USD)
- **Type:** `number`
- **Format:** `dollar`

### Annual contract value
- **Type:** `number`
- **Format:** `number`

### Annual recurring revenue
- **Type:** `number`
- **Format:** `number`

### Associated Client
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-814c-ad70-d478cebeee30`

### Associated Contacts
- **Type:** `relation`
- **Related Database:** `22bf4e0d-84e0-803f-98fe-f0a72401d33c`

### Associated Orders
- **Type:** `relation`
- **Related Database:** `228f4e0d-84e0-816f-8511-fab726d2c6ef`

### Associated Plan
- **Type:** `relation`
- **Related Database:** `228f4e0d-84e0-815c-a108-e48054988ac0`

### Auto Total
- **Type:** `formula`
- **Formula:** `{{notion:block_property:u~mn:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}*{{notion:block_property:v%5Ds%3D:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}`

### Close Date
- **Type:** `date`

### Create Income
- **Type:** `button`

### Currency
- **Type:** `select`
- **Options:** `USD`, `GBP`, `EUR`, `CAD`

### Current Month profit
- **Type:** `formula`
- **Formula:** `if(formatDate({{notion:block_property:P%3FJ%40:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}, "MMMM, YYYY")==formatDate(today(), "MMMM, YYYY"), {{notion:block_property:%3FFFD:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}},0)`

### Current Month?
- **Type:** `formula`
- **Formula:** `formatDate({{notion:block_property:P%3FJ%40:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}, "MMMM, YYYY")==formatDate(today(), "MMMM, YYYY")`

### Deal Name
- **Type:** `rich_text`

### Deal Name (Archive)
- **Type:** `rich_text`

### Deal Profile
- **Type:** `multi_select`
- **Options:** `Hair Sale`, `Plan`, `Wholesale`, `Retail`, `Hair Sale,Plan`, `Hair Sale,Retail`, `Hair Sale,Wholesale`, `Products Sale,Retail`, `Hair Sale,E-Commerce`, `Products Sale,Wholesale`, `Shipment/Repair/Other`, `Training/Certification`, `Products Sale,E-Commerce`, `Hair`, `Multi-Unit`

### Deal Size
- **Type:** `select`
- **Options:** `1 Unit`, `2 Units`, `3 Units`, `4 Units`, `5 Units`, `6 Units`, `9 Units`

### Deal Size (#)
- **Type:** `number`
- **Format:** `number`

### Deal Stage
- **Type:** `select`
- **Options:** `Subscription Active`, `Plan Renewal Needed`, `Payment Issues`, `Paid-in-full`, `Open`, `Completed`, `Closed Won`

### Deal Type
- **Type:** `select`
- **Options:** `Custom`, `Premade`, `Maintenance Products`, `Order Shipment`, `Template Shipment`, `In-Person Training`, `Accessories`, `Online Course`, `3-Unit`, `Single-Unit`, `4-Unit`, `6-Unit`

### Emergency List
- **Type:** `checkbox`

### Exchange rate
- **Type:** `number`
- **Format:** `number`

### Formula
- **Type:** `formula`
- **Formula:** `if(
  {{notion:block_property:JaPq:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} == 0,
  "❌ No Orders",
  if(
    {{notion:block_property:JaPq:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} == {{notion:block_property:ll%3F%7C:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}},
    "✅ Complete",
    "🟡 In Progress"
  )
)`

### Hubspot Deals Record ID
- **Type:** `number`
- **Format:** `number`

### Income
- **Type:** `formula`
- **Formula:** `if({{notion:block_property:PP%40L:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}.contains("Refunded"),0,
if(empty({{notion:block_property:blon:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}),{{notion:block_property:%3FnBM:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}},{{notion:block_property:blon:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}))`

### Income Status
- **Type:** `formula`
- **Formula:** `if(empty({{notion:block_property:~AAP:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}),style("Income not created","red","b"),("✓ Income created").style("green","b"))`

### Inventory Products
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-814f-a468-d44302ee0478`

### Last Activity Date
- **Type:** `date`

### Linked Subscriptions
- **Type:** `relation`
- **Related Database:** `228f4e0d-84e0-815c-a108-e48054988ac0`

### Month
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-8101-81e1-c9f2d6803291`

### Monthly recurring revenue
- **Type:** `number`
- **Format:** `number`

### Name
- **Type:** `title`

### Next Activity Date
- **Type:** `rich_text`

### Notion Deals Record ID
- **Type:** `unique_id`

### Orders Complete
- **Type:** `checkbox`

### Orders Tasks
- **Type:** `rich_text`

### Override Total
- **Type:** `number`
- **Format:** `dollar`

### Payment Date
- **Type:** `date`

### Plan End Date
- **Type:** `date`

### Plan Start Date
- **Type:** `date`

### Priority
- **Type:** `select`
- **Options:** `Low`, `Medium`, `High`

### Profit
- **Type:** `formula`
- **Formula:** `{{notion:block_property:wyf%3E:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}-({{notion:block_property:K%3AA%5E:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}.map(current.{{notion:block_property:U%3BZe:226f4e0d-84e0-814f-a468-d44302ee0478:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}).sum()*{{notion:block_property:u~mn:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}})`

### Qty
- **Type:** `number`
- **Format:** `number`

### Refund Payment
- **Type:** `button`

### Retail Price
- **Type:** `formula`
- **Formula:** `{{notion:block_property:K%3AA%5E:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}.map(current.{{notion:block_property:OTrN:226f4e0d-84e0-814f-a468-d44302ee0478:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}).sum()`

### Rollup
- **Type:** `rollup`
- **Relation Property:** `Associated Orders`
- **Rollup Property:** `PO Number`
- **Function:** `show_original`

### Rollup 1
- **Type:** `rollup`
- **Relation Property:** `Associated Client`
- **Rollup Property:** `Associated Orders`
- **Function:** `show_original`

### Rollup 2
- **Type:** `rollup`
- **Relation Property:** `Associated Orders`
- **Rollup Property:** `Unit`
- **Function:** `show_original`

### Summary
- **Type:** `rich_text`

### Tasks
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-8168-8718-d8f6b2d1fe3d`

### Time since order
- **Type:** `formula`
- **Formula:** `("Ordered " + dateBetween(now(),{{notion:block_property:P%3FJ%40:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}, "days")+ " days ago").style("b","c")`

### To check
- **Type:** `checkbox`

### profi
- **Type:** `rollup`
- **Relation Property:** `Associated Orders`
- **Rollup Property:** `Order Profile`
- **Function:** `show_original`

---

## Usage Notes

<!-- Add any specific usage notes, business logic, or important information about this database -->

## Related Databases

<!-- List any databases that this one relates to or depends on -->

