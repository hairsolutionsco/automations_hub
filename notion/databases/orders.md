# Orders Database

**Database ID:** `228f4e0d-84e0-816f-8511-fab726d2c6ef`

**Created:** 2025-07-06T17:26:00.000Z
**Last Modified:** 2025-08-13T19:15:00.000Z
**Total Properties:** 47

---

## Properties Overview

### button (1)
- `Create RH Order`

### date (7)
- `Order Delivery Due`
- `Order_Date`
- `Order_ETA`
- `Payment Date`
- `Payment Due`
- `Production_Start_Date`
- `Shipped Date`

### formula (8)
- `Client Name`
- `Client Name (Formula)`
- `Factory Abbreviation`
- `Formula`
- `Order Date`
- `Order ETAs`
- `Order Number (Formula)`
- `Production Start Date`

### multi_select (1)
- `Order Profile`

### number (8)
- `Extras Cost`
- `Hair Unit Cost`
- `Hubspot POs Record ID`
- `Index`
- `Last PO Cost`
- `Shipment Cost`
- `Total Cost`
- `Tracking Number`

### relation (6)
- `Associated Companies`
- `Associated Deal`
- `Associated PO`
- `Client`
- `Related to Contacts (1) (Associated Orders)`
- `Year`

### rich_text (4)
- `Factory Invoice No`
- `Notes`
- `PO Number`
- `Shipping Courrier`

### rollup (4)
- `Associated Deal's POs`
- `Client Number`
- `Products`
- `Rollup from Deal`

### select (6)
- `Factory`
- `Order Details`
- `Order Speed`
- `Order Status`
- `Payment Status`
- `Unit`

### title (1)
- `Order Number`

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

### Associated Deal's POs
- **Type:** `rollup`
- **Relation Property:** `Associated PO`
- **Rollup Property:** `PO Number`
- **Function:** `show_original`

### Associated PO
- **Type:** `relation`
- **Related Database:** `237f4e0d-84e0-807b-860c-cb9599ddaea0`

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

### Create RH Order
- **Type:** `button`

### Extras Cost
- **Type:** `number`

### Factory
- **Type:** `select`
- **Options:**
  - `LuxHair`
  - `NewTimes Hair`
  - `RareHair`
  - `Rare Hair`

### Factory Abbreviation
- **Type:** `formula`
- **Formula:** `if({{notion:block_property:NIr%3C:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} == "RareHair", "RH", if({{notion:block_property:NIr%3C:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} == "NewTimes Hair", "NT", "XX"))`

### Factory Invoice No
- **Type:** `rich_text`

### Formula
- **Type:** `formula`
- **Formula:** `"📦 " + {{notion:block_property:title:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} + " | 🧾 " + {{notion:block_property:UKdS:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}`

### Hair Unit Cost
- **Type:** `number`

### Hubspot POs Record ID
- **Type:** `number`

### Index
- **Type:** `number`

### Last PO Cost
- **Type:** `number`

### Notes
- **Type:** `rich_text`

### Notion Orders Record ID
- **Type:** `unique_id`

### Order Date
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

### Order ETAs
- **Type:** `formula`
- **Formula:** `formatDate({{notion:block_property:t%3Eim:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}, "YYYY-MM-DD") `

### Order Number
- **Type:** `title`

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

### Order_ETA
- **Type:** `date`

### PO Number
- **Type:** `rich_text`

### Payment Date
- **Type:** `date`

### Payment Due
- **Type:** `date`

### Payment Status
- **Type:** `select`
- **Options:**
  - `Paid`

### Production Start Date
- **Type:** `formula`
- **Formula:** `formatDate({{notion:block_property:k%3Eed:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}, "YYYY-MM-DD") `

### Production_Start_Date
- **Type:** `date`

### Products
- **Type:** `rollup`
- **Relation Property:** `Associated PO`
- **Rollup Property:** `Inventory Products DB`
- **Function:** `show_original`

### Related to Contacts (1) (Associated Orders)
- **Type:** `relation`
- **Related Database:** `248f4e0d-84e0-80ad-9d33-e90e5124c092`

### Rollup from Deal
- **Type:** `rollup`
- **Relation Property:** `Associated Deal`
- **Rollup Property:** `Associated Client`
- **Function:** `show_original`

### Shipment Cost
- **Type:** `number`

### Shipped Date
- **Type:** `date`

### Shipping Courrier
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

*Analysis based on 1041 pages*

### Mostly Empty Properties (8)
*These properties have data in less than 5% of pages:*

- `Production_Start_Date` (date) - 99.3% empty, only 7 pages with data
- `Production Start Date` (formula) - 99.3% empty, only 7 pages with data
- `Shipped Date` (date) - 98.8% empty, only 12 pages with data
- `Notes` (rich_text) - 97.8% empty, only 23 pages with data
- `Payment Status` (select) - 96.6% empty, only 35 pages with data
- `Shipping Courrier` (rich_text) - 96.4% empty, only 37 pages with data
- `Order ETAs` (formula) - 96.1% empty, only 41 pages with data
- `Order_ETA` (date) - 96.1% empty, only 41 pages with data

## Related Databases

- **Related to Contacts (1) (Associated Orders)** (`248f4e0d-84e0-80ad-9d33-e90e5124c092`)
- **Year** (`226f4e0d-84e0-8179-98cb-cca8ecbf0c15`)
- **Associated Companies** (`22bf4e0d-84e0-80bb-8d1c-c90710d44870`)
- **Client** (`226f4e0d-84e0-814c-ad70-d478cebeee30`)
- **Associated Deal** (`226f4e0d-84e0-808c-af51-e09c154008db`)
- **Associated PO** (`237f4e0d-84e0-807b-860c-cb9599ddaea0`)

---

*Documentation generated on 2025-08-13 19:50:15*
