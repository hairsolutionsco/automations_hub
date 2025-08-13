# Purchase Orders Database

**Database ID:** `237f4e0d-84e0-807b-860c-cb9599ddaea0`

**Created:** 2025-07-21T14:21:00.000Z
**Last Modified:** 2025-08-13T19:15:00.000Z
**Total Properties:** 52

---

## Properties Overview

### button (2)
- `Create RH Order`
- `Send NT Order Email`

### date (7)
- `Order Delivery Due`
- `Order ETA`
- `Order_Date`
- `Payment Date`
- `Payment Due`
- `Production Start Date`
- `Shipped Date`

### formula (6)
- `Client Name`
- `Client Name (Formula)`
- `Client name text`
- `Factory Abbreviation`
- `Order Date Formatted`
- `Order Number (Formula)`

### multi_select (1)
- `Order Profile`

### number (8)
- `Extras Cost`
- `Hair Unit Cost`
- `Hubspot POs Record ID`
- `Last Index #`
- `Last PO Cost`
- `Shipment Cost`
- `Total Cost`
- `Tracking Number`

### relation (9)
- `Associated Companies`
- `Associated Deal`
- `Associated Order`
- `Client`
- `Inventory Product`
- `Inventory Products DB`
- `Relation`
- `Retail Products`
- `Year`

### rich_text (5)
- `Factory Invoice No`
- `Next Index #`
- `Notes`
- `Shipping Courrier`
- `Text`

### rollup (6)
- `Associated Deal's Orders`
- `Client Number`
- `Cost per Unit`
- `Density`
- `Rollup`
- `Rollup from Deal`

### select (6)
- `Factory`
- `Order Details`
- `Order Speed`
- `Order Status`
- `Payment Status`
- `Unit`

### title (1)
- `PO Number`

### unique_id (1)
- `Notion Orders Record ID`

---

## Detailed Property Documentation

### Associated Companies
- **Type:** `relation`
- **Related Database:** `22bf4e0d-84e0-80bb-8d1c-c90710d44870`

### Associated Deal
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-808c-af51-e09c154008db`

### Associated Deal's Orders
- **Type:** `rollup`
- **Relation Property:** `Associated Deal`
- **Rollup Property:** `Associated Orders`
- **Function:** `show_original`

### Associated Order
- **Type:** `relation`
- **Related Database:** `228f4e0d-84e0-816f-8511-fab726d2c6ef`

### Client
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-814c-ad70-d478cebeee30`

### Client Name
- **Type:** `formula`
- **Formula:** `{{notion:block_property:mYHK:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} + " " + "-" + " " +{{notion:block_property:NnbB:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}`

### Client Name (Formula)
- **Type:** `formula`
- **Formula:** `format({{notion:block_property:Rqg%7B:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}) `

### Client Number
- **Type:** `rollup`
- **Relation Property:** `Client`
- **Rollup Property:** `Client Number`
- **Function:** `show_original`

### Client name text
- **Type:** `formula`
- **Formula:** `format({{notion:block_property:mYHK:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}})
`

### Cost per Unit
- **Type:** `rollup`
- **Relation Property:** `Inventory Product`
- **Rollup Property:** `Cost per item`
- **Function:** `show_original`

### Create RH Order
- **Type:** `button`

### Density
- **Type:** `rollup`
- **Relation Property:** `Inventory Product`
- **Rollup Property:** `Hair Density`
- **Function:** `show_original`

### Extras Cost
- **Type:** `number`

### Factory
- **Type:** `select`
- **Options:**
  - `LuxHair`
  - `NewTimes Hair`
  - `RareHair`

### Factory Abbreviation
- **Type:** `formula`
- **Formula:** `if({{notion:block_property:NIr%3C:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} == "RareHair", "RH", if({{notion:block_property:NIr%3C:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} == "NewTimes Hair", "NT", "XX"))`

### Factory Invoice No
- **Type:** `rich_text`

### Hair Unit Cost
- **Type:** `number`

### Hubspot POs Record ID
- **Type:** `number`

### Inventory Product
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-814f-a468-d44302ee0478`

### Inventory Products DB
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-814f-a468-d44302ee0478`

### Last Index #
- **Type:** `number`

### Last PO Cost
- **Type:** `number`

### Next Index #
- **Type:** `rich_text`

### Notes
- **Type:** `rich_text`

### Notion Orders Record ID
- **Type:** `unique_id`

### Order Date Formatted
- **Type:** `formula`
- **Formula:** `formatDate({{notion:block_property:YN%3C%5C:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}, "YYYY-MM-DD") `

### Order Delivery Due
- **Type:** `date`

### Order Details
- **Type:** `select`
- **Options:**
  - `Repair Order`
  - `Client Templates Measurements`
  - `Premade Order`
  - `Custom Order`
  - `Order Shipment`
  - `Maintenance Products`
  - `Template Return Shipment`

### Order ETA
- **Type:** `date`

### Order Number (Formula)
- **Type:** `formula`
- **Formula:** `"OHS-" + format({{notion:block_property:LXcc:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}) + "-" + 
if({{notion:block_property:D%5CGc:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} < 10, "00", if({{notion:block_property:D%5CGc:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} < 100, "0", "")) + format({{notion:block_property:D%5CGc:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}})`

### Order Profile
- **Type:** `multi_select`
- **Options:**
  - `Hair`
  - `Retail`
  - `Plan`
  - `Wholesale`
  - `Shipment`
  - `Template Shipment`
  - `Products`
  - `Maintenance Products`
  - `Accessoories`
  - `Repair/Adjustment`
  - `Other`
  - `Single Unit`
  - `Plan Order (Active)`
  - `Wholesale Order`
  - `Hair Order`
  - `Shipment Order`
  - `Plan Unit Order`
  - `Single Unit Order`

### Order Speed
- **Type:** `select`
- **Options:**
  - `N/A`
  - `Rush`
  - `Standard`

### Order Status
- **Type:** `select`
- **Options:**
  - `Order Pending`
  - `Order Next Month`
  - `Need Order Now`
  - `Order Placed`
  - `Quote requested`
  - `In progress`
  - `Production Completed`
  - `Awaiting shipment`
  - `Shipped`
  - `Shipment issue`
  - `At pick-up location`
  - `Completed`
  - `Delivered`
  - `Cancelled`
  - `Inprogress`

### Order_Date
- **Type:** `date`

### PO Number
- **Type:** `title`

### Payment Date
- **Type:** `date`

### Payment Due
- **Type:** `date`

### Payment Status
- **Type:** `select`
- **Options:**
  - `Paid`

### Production Start Date
- **Type:** `date`

### Relation
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-814f-a468-d44302ee0478`

### Retail Products
- **Type:** `relation`
- **Related Database:** `232f4e0d-84e0-8000-aad7-de8ff9504fd1`

### Rollup
- **Type:** `rollup`
- **Relation Property:** `Inventory Product`
- **Rollup Property:** `Image Gallery`
- **Function:** `show_original`

### Rollup from Deal
- **Type:** `rollup`
- **Relation Property:** `Associated Deal`
- **Rollup Property:** `Associated Client`
- **Function:** `show_original`

### Send NT Order Email
- **Type:** `button`

### Shipment Cost
- **Type:** `number`

### Shipped Date
- **Type:** `date`

### Shipping Courrier
- **Type:** `rich_text`

### Text
- **Type:** `rich_text`

### Total Cost
- **Type:** `number`

### Tracking Number
- **Type:** `number`

### Unit
- **Type:** `select`
- **Options:**
  - `Unit 2`
  - `Unit 3`
  - `Unit 1`
  - `Unit 4`
  - `Unit 5`
  - `Unit 6`

### Year
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-8179-98cb-cca8ecbf0c15`

## 🚫 Empty & Unused Properties

*Analysis based on 1047 pages*

### Completely Empty Properties (7)
*These properties have no data in any page:*

- `Cost per Unit` (rollup)
- `Density` (rollup)
- `Inventory Product` (relation)
- `Relation` (relation)
- `Retail Products` (relation)
- `Rollup` (rollup)
- `Text` (rich_text)

### Mostly Empty Properties (8)
*These properties have data in less than 5% of pages:*

- `Inventory Products DB` (relation) - 99.9% empty, only 1 pages with data
- `Next Index #` (rich_text) - 99.5% empty, only 5 pages with data
- `Production Start Date` (date) - 99.5% empty, only 5 pages with data
- `Shipped Date` (date) - 98.7% empty, only 14 pages with data
- `Notes` (rich_text) - 97.8% empty, only 23 pages with data
- `Shipping Courrier` (rich_text) - 97.4% empty, only 27 pages with data
- `Payment Status` (select) - 96.7% empty, only 35 pages with data
- `Order ETA` (date) - 96.2% empty, only 40 pages with data

## Related Databases

- **Relation** (`226f4e0d-84e0-814f-a468-d44302ee0478`)
- **Inventory Product** (`226f4e0d-84e0-814f-a468-d44302ee0478`)
- **Year** (`226f4e0d-84e0-8179-98cb-cca8ecbf0c15`)
- **Associated Companies** (`22bf4e0d-84e0-80bb-8d1c-c90710d44870`)
- **Client** (`226f4e0d-84e0-814c-ad70-d478cebeee30`)
- **Associated Order** (`228f4e0d-84e0-816f-8511-fab726d2c6ef`)
- **Associated Deal** (`226f4e0d-84e0-808c-af51-e09c154008db`)
- **Retail Products** (`232f4e0d-84e0-8000-aad7-de8ff9504fd1`)
- **Inventory Products DB** (`226f4e0d-84e0-814f-a468-d44302ee0478`)

---

*Documentation generated on 2025-08-13 19:50:16*
