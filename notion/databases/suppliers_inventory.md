# Suppliers Inventory Database

**Database ID:** `226f4e0d-84e0-814f-a468-d44302ee0478`

**Created:** 2025-07-04T20:24:00.000Z
**Last Modified:** 2025-08-13T19:15:00.000Z
**Total Properties:** 71

---

## Properties Overview

### files (1)
- `Image Gallery`

### formula (10)
- `Current Month Sales`
- `Current Month profit #`
- `Current month profit`
- `Inventory Value`
- `No. of Orders`
- `Profit made`
- `Profit per item`
- `Total Profit made`
- `Total Sales`
- `latest restock Value`

### multi_select (3)
- `Category`
- `Hair Density`
- `Product Description Tags`

### number (11)
- `Cost per item`
- `Manual Quantity Overrried`
- `Price CAD`
- `Price EUR`
- `Price GBP`
- `Price USD`
- `Record ID`
- `Retail Price`
- `Size (ml)`
- `Unit cost`
- `item weight (KG)`

### relation (12)
- `Associated Deals`
- `Associated Purchase Order`
- `Companies`
- `Orders`
- `Parent item`
- `Purchase Orders`
- `Purchase Orders 1`
- `Restock`
- `Shopify Products`
- `Sub-item`
- `Supplier`
- `Supplier 1`

### rich_text (12)
- `Airtable Record ID`
- `Body HTML`
- `Image URL 2`
- `Image Url`
- `Price AED`
- `Price BRL`
- `Product Name`
- `Product description`
- `Record source detail 3`
- `SKU`
- `Short Description`
- `Tags`

### rollup (3)
- `Latest restock`
- `Qty Sold`
- `Stock Added`

### select (18)
- `Available Sizes`
- `Billing frequency`
- `Ecommerce product`
- `External Sync Source`
- `Hair Type`
- `Handle`
- `Product Type`
- `Product Type 2`
- `Record source`
- `Record source detail 1`
- `Record source detail 2`
- `Shopify Store`
- `Source store`
- `Status`
- `Storage Location`
- `Term`
- `URL`
- `Vendor`

### title (1)
- `Item Name`

---

## Detailed Property Documentation

### Airtable Record ID
- **Type:** `rich_text`

### Associated Deals
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-808c-af51-e09c154008db`

### Associated Purchase Order
- **Type:** `relation`
- **Related Database:** `237f4e0d-84e0-807b-860c-cb9599ddaea0`

### Available Sizes
- **Type:** `select`

### Billing frequency
- **Type:** `select`

### Body HTML
- **Type:** `rich_text`

### Category
- **Type:** `multi_select`
- **Options:**
  **23 options** from `Laptops` to `skin perimeters`

### Companies
- **Type:** `relation`
- **Related Database:** `22bf4e0d-84e0-80bb-8d1c-c90710d44870`

### Cost per item
- **Type:** `number`

### Current Month Sales
- **Type:** `formula`
- **Formula:** `{{notion:block_property:D_ED:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}.filter(current.{{notion:block_property:AeKt:226f4e0d-84e0-81a5-acbe-d9803b31dd28:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}==true).map(current.{{notion:block_property:u~mn:226f4e0d-84e0-81a5-acbe-d9803b31dd28:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}).sum()`

### Current Month profit #
- **Type:** `formula`
- **Formula:** `{{notion:block_property:D_ED:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}.map(current.{{notion:block_property:gIYo:226f4e0d-84e0-81a5-acbe-d9803b31dd28:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}).sum()`

### Current month profit
- **Type:** `formula`
- **Formula:** `("This Month Profit "+ "$" +{{notion:block_property:D_ED:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}.map(current.{{notion:block_property:gIYo:226f4e0d-84e0-81a5-acbe-d9803b31dd28:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}).sum()).style("c","green","b")`

### Ecommerce product
- **Type:** `select`

### External Sync Source
- **Type:** `select`

### Hair Density
- **Type:** `multi_select`

### Hair Type
- **Type:** `select`

### Handle
- **Type:** `select`

### Image Gallery
- **Type:** `files`

### Image URL 2
- **Type:** `rich_text`

### Image Url
- **Type:** `rich_text`

### Inventory Value
- **Type:** `formula`
- **Formula:** `{{notion:block_property:OTrN:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}*{{notion:block_property:OQJ%60:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}`

### Item Name
- **Type:** `title`

### Latest restock
- **Type:** `rollup`
- **Relation Property:** `Restock`
- **Rollup Property:** `Date`
- **Function:** `latest_date`

### Manual Quantity Overrried
- **Type:** `number`

### No. of Orders
- **Type:** `formula`
- **Formula:** `({{notion:block_property:D_ED:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}.length() + " Total Orders").style("c","purple","b")`

### Orders
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-81a5-acbe-d9803b31dd28`

### Parent item
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-814f-a468-d44302ee0478`

### Price AED
- **Type:** `rich_text`

### Price BRL
- **Type:** `rich_text`

### Price CAD
- **Type:** `number`

### Price EUR
- **Type:** `number`

### Price GBP
- **Type:** `number`

### Price USD
- **Type:** `number`

### Product Description Tags
- **Type:** `multi_select`

### Product Name
- **Type:** `rich_text`

### Product Type
- **Type:** `select`

### Product Type 2
- **Type:** `select`

### Product description
- **Type:** `rich_text`

### Profit made
- **Type:** `formula`
- **Formula:** `{{notion:block_property:D_ED:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}.map(current.{{notion:block_property:%3FFFD:226f4e0d-84e0-81a5-acbe-d9803b31dd28:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}).sum()`

### Profit per item
- **Type:** `formula`
- **Formula:** `{{notion:block_property:OTrN:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}-{{notion:block_property:U%3BZe:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}`

### Purchase Orders
- **Type:** `relation`
- **Related Database:** `237f4e0d-84e0-807b-860c-cb9599ddaea0`

### Purchase Orders 1
- **Type:** `relation`
- **Related Database:** `237f4e0d-84e0-807b-860c-cb9599ddaea0`

### Qty Sold
- **Type:** `rollup`
- **Relation Property:** `Orders`
- **Rollup Property:** `Qty`
- **Function:** `sum`

### Record ID
- **Type:** `number`

### Record source
- **Type:** `select`

### Record source detail 1
- **Type:** `select`

### Record source detail 2
- **Type:** `select`

### Record source detail 3
- **Type:** `rich_text`

### Restock
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-8166-8009-ca3a0c85201b`

### Retail Price
- **Type:** `number`

### SKU
- **Type:** `rich_text`

### Shopify Products
- **Type:** `relation`
- **Related Database:** `232f4e0d-84e0-8000-aad7-de8ff9504fd1`

### Shopify Store
- **Type:** `select`

### Short Description
- **Type:** `rich_text`

### Size (ml)
- **Type:** `number`

### Source store
- **Type:** `select`

### Status
- **Type:** `select`
- **Options:**
  - `Unavailable`
  - `Limited choice`
  - `In stock`

### Stock Added
- **Type:** `rollup`
- **Relation Property:** `Restock`
- **Rollup Property:** `Qty`
- **Function:** `sum`

### Storage Location
- **Type:** `select`
- **Options:**
  - `Warehouse`

### Sub-item
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-814f-a468-d44302ee0478`

### Supplier
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-81c8-858e-d10ff2e0ad9b`

### Supplier 1
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-8147-9f51-e56c81859411`

### Tags
- **Type:** `rich_text`

### Term
- **Type:** `select`

### Total Profit made
- **Type:** `formula`
- **Formula:** `("Total Profit "+ "$" +{{notion:block_property:D_ED:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}.map(current.{{notion:block_property:%3FFFD:226f4e0d-84e0-81a5-acbe-d9803b31dd28:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}).sum()).style("b","grey","c")`

### Total Sales
- **Type:** `formula`
- **Formula:** `{{notion:block_property:D_ED:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}.map(current.{{notion:block_property:u~mn:226f4e0d-84e0-81a5-acbe-d9803b31dd28:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}).sum()`

### URL
- **Type:** `select`

### Unit cost
- **Type:** `number`

### Vendor
- **Type:** `select`

### item weight (KG)
- **Type:** `number`

### latest restock Value
- **Type:** `formula`
- **Formula:** `{{notion:block_property:ZQGV:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}.map(current).sort(current.{{notion:block_property:%5D%60xr:226f4e0d-84e0-8166-8009-ca3a0c85201b:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}).last().{{notion:block_property:TGAo:226f4e0d-84e0-8166-8009-ca3a0c85201b:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}`

## 🚫 Empty & Unused Properties

*Analysis based on 77 pages*

### Completely Empty Properties (41)
*These properties have no data in any page:*

- `Airtable Record ID` (rich_text)
- `Associated Deals` (relation)
- `Available Sizes` (select)
- `Billing frequency` (select)
- `Body HTML` (rich_text)
- `Ecommerce product` (select)
- `External Sync Source` (select)
- `Hair Density` (multi_select)
- `Hair Type` (select)
- `Handle` (select)
- `Image URL 2` (rich_text)
- `Image Url` (rich_text)
- `Inventory Value` (formula)
- `Latest restock` (rollup)
- `Price AED` (rich_text)
- `Price BRL` (rich_text)
- `Price CAD` (number)
- `Price EUR` (number)
- `Price GBP` (number)
- `Price USD` (number)
- `Product Description Tags` (multi_select)
- `Product Name` (rich_text)
- `Product Type` (select)
- `Product Type 2` (select)
- `Product description` (rich_text)
- `Purchase Orders` (relation)
- `Purchase Orders 1` (relation)
- `Record ID` (number)
- `Record source` (select)
- `Record source detail 1` (select)
- `Record source detail 2` (select)
- `Record source detail 3` (rich_text)
- `SKU` (rich_text)
- `Shopify Store` (select)
- `Size (ml)` (number)
- `Source store` (select)
- `Tags` (rich_text)
- `Term` (select)
- `URL` (select)
- `Unit cost` (number)
- `Vendor` (select)

### Mostly Empty Properties (5)
*These properties have data in less than 5% of pages:*

- `Retail Price` (number) - 98.7% empty, only 1 pages with data
- `Associated Purchase Order` (relation) - 98.7% empty, only 1 pages with data
- `item weight (KG)` (number) - 98.7% empty, only 1 pages with data
- `Restock` (relation) - 96.1% empty, only 3 pages with data
- `latest restock Value` (formula) - 96.1% empty, only 3 pages with data

## Related Databases

- **Supplier** (`226f4e0d-84e0-81c8-858e-d10ff2e0ad9b`)
- **Supplier 1** (`226f4e0d-84e0-8147-9f51-e56c81859411`)
- **Orders** (`226f4e0d-84e0-81a5-acbe-d9803b31dd28`)
- **Companies** (`22bf4e0d-84e0-80bb-8d1c-c90710d44870`)
- **Shopify Products** (`232f4e0d-84e0-8000-aad7-de8ff9504fd1`)
- **Associated Deals** (`226f4e0d-84e0-808c-af51-e09c154008db`)
- **Associated Purchase Order** (`237f4e0d-84e0-807b-860c-cb9599ddaea0`)
- **Restock** (`226f4e0d-84e0-8166-8009-ca3a0c85201b`)
- **Sub-item** (`226f4e0d-84e0-814f-a468-d44302ee0478`)
- **Purchase Orders** (`237f4e0d-84e0-807b-860c-cb9599ddaea0`)
- **Purchase Orders 1** (`237f4e0d-84e0-807b-860c-cb9599ddaea0`)
- **Parent item** (`226f4e0d-84e0-814f-a468-d44302ee0478`)

---

*Documentation generated on 2025-08-13 19:50:17*
