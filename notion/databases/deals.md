# Deals Database

**Database ID:** `226f4e0d-84e0-808c-af51-e09c154008db`

**Created:** 2025-07-04T23:04:00.000Z
**Last Modified:** 2025-08-13T19:15:00.000Z
**Total Properties:** 54

---

## Properties Overview

### button (2)
- `Create Income`
- `Refund Payment`

### checkbox (3)
- `Emergency List`
- `Orders Complete`
- `To check`

### date (5)
- `Close Date`
- `Last Activity Date`
- `Payment Date`
- `Plan End Date`
- `Plan Start Date`

### formula (9)
- `Auto Total`
- `Current Month profit`
- `Current Month?`
- `Formula`
- `Income`
- `Income Status`
- `Profit`
- `Retail Price`
- `Time since order`

### multi_select (1)
- `Deal Profile`

### number (10)
- `Amount`
- `Amount (USD)`
- `Annual contract value`
- `Annual recurring revenue`
- `Deal Size (#)`
- `Exchange rate`
- `Hubspot Deals Record ID`
- `Monthly recurring revenue`
- `Override Total`
- `Qty`

### relation (8)
- `Associated Client`
- `Associated Contacts`
- `Associated Orders`
- `Associated Plan`
- `Inventory Products`
- `Linked Subscriptions`
- `Month`
- `Tasks`

### rich_text (5)
- `Deal Name`
- `Deal Name (Archive)`
- `Next Activity Date`
- `Orders Tasks`
- `Summary`

### rollup (4)
- `Rollup`
- `Rollup 1`
- `Rollup 2`
- `profi`

### select (5)
- `Currency`
- `Deal Size`
- `Deal Stage`
- `Deal Type`
- `Priority`

### title (1)
- `Name`

### unique_id (1)
- `Notion Deals Record ID`

---

## Detailed Property Documentation

### Amount
- **Type:** `number`

### Amount (USD)
- **Type:** `number`

### Annual contract value
- **Type:** `number`

### Annual recurring revenue
- **Type:** `number`

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
- **Options:**
  - `USD`
  - `GBP`
  - `EUR`
  - `CAD`

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
- **Options:**
  - `Hair Sale`
  - `Plan`
  - `Wholesale`
  - `Retail`
  - `Hair Sale,Plan`
  - `Hair Sale,Retail`
  - `Hair Sale,Wholesale`
  - `Products Sale,Retail`
  - `Hair Sale,E-Commerce`
  - `Products Sale,Wholesale`
  - `Shipment/Repair/Other`
  - `Training/Certification`
  - `Products Sale,E-Commerce`
  - `Hair`
  - `Multi-Unit`

### Deal Size
- **Type:** `select`
- **Options:**
  - `1 Unit`
  - `2 Units`
  - `3 Units`
  - `4 Units`
  - `5 Units`
  - `6 Units`
  - `9 Units`

### Deal Size (#)
- **Type:** `number`

### Deal Stage
- **Type:** `select`
- **Options:**
  - `Subscription Active`
  - `Plan Renewal Needed`
  - `Payment Issues`
  - `Paid-in-full`
  - `Open`
  - `Completed`
  - `Closed Won`

### Deal Type
- **Type:** `select`
- **Options:**
  - `Custom`
  - `Premade`
  - `Maintenance Products`
  - `Order Shipment`
  - `Template Shipment`
  - `In-Person Training`
  - `Accessories`
  - `Online Course`
  - `3-Unit`
  - `Single-Unit`
  - `4-Unit`
  - `6-Unit`

### Emergency List
- **Type:** `checkbox`

### Exchange rate
- **Type:** `number`

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

### Payment Date
- **Type:** `date`

### Plan End Date
- **Type:** `date`

### Plan Start Date
- **Type:** `date`

### Priority
- **Type:** `select`
- **Options:**
  - `Low`
  - `Medium`
  - `High`

### Profit
- **Type:** `formula`
- **Formula:** `{{notion:block_property:wyf%3E:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}-({{notion:block_property:K%3AA%5E:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}.map(current.{{notion:block_property:U%3BZe:226f4e0d-84e0-814f-a468-d44302ee0478:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}).sum()*{{notion:block_property:u~mn:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}})`

### Qty
- **Type:** `number`

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

## 🚫 Empty & Unused Properties

*Analysis based on 942 pages*

### Completely Empty Properties (16)
*These properties have no data in any page:*

- `Associated Contacts` (relation)
- `Auto Total` (formula)
- `Current Month profit` (formula)
- `Current Month?` (formula)
- `Formula` (formula)
- `Income` (formula)
- `Income Status` (formula)
- `Inventory Products` (relation)
- `Linked Subscriptions` (relation)
- `Month` (relation)
- `Next Activity Date` (rich_text)
- `Override Total` (number)
- `Profit` (formula)
- `Qty` (number)
- `Retail Price` (formula)
- `Time since order` (formula)

### Mostly Empty Properties (6)
*These properties have data in less than 5% of pages:*

- `Associated Plan` (relation) - 99.9% empty, only 1 pages with data
- `To check` (checkbox) - 99.7% empty, only 3 pages with data
- `Orders Tasks` (rich_text) - 99.4% empty, only 6 pages with data
- `Orders Complete` (checkbox) - 98.6% empty, only 13 pages with data
- `Emergency List` (checkbox) - 96.9% empty, only 29 pages with data
- `Tasks` (relation) - 96.9% empty, only 29 pages with data

## Related Databases

- **Associated Plan** (`228f4e0d-84e0-815c-a108-e48054988ac0`)
- **Associated Client** (`226f4e0d-84e0-814c-ad70-d478cebeee30`)
- **Inventory Products** (`226f4e0d-84e0-814f-a468-d44302ee0478`)
- **Linked Subscriptions** (`228f4e0d-84e0-815c-a108-e48054988ac0`)
- **Associated Contacts** (`22bf4e0d-84e0-803f-98fe-f0a72401d33c`)
- **Associated Orders** (`228f4e0d-84e0-816f-8511-fab726d2c6ef`)
- **Tasks** (`226f4e0d-84e0-8168-8718-d8f6b2d1fe3d`)
- **Month** (`226f4e0d-84e0-8101-81e1-c9f2d6803291`)

---

*Documentation generated on 2025-08-13 19:50:11*
