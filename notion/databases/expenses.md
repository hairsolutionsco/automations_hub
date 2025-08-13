# Expenses Database

**Database ID:** `226f4e0d-84e0-817e-84e2-c9a983663070`

**Created:** 2025-07-04T20:24:00.000Z
**Last Modified:** 2025-08-13T19:15:00.000Z
**Total Properties:** 35

---

## Properties Overview

### checkbox (1)
- `Archive`

### date (2)
- `Date`
- `Date completed (UTC)`

### formula (9)
- `Ads Expense show`
- `Campaign Status`
- `Current Month Expense`
- `Current Month?`
- `Freelance Sum`
- `Monthly Salary `
- `Number`
- `Salary Sum`
- `Total USD`

### number (6)
- `Amount Currency`
- `Exchange Rate`
- `Exchange To Amount`
- `Fee`
- `MCC`
- `Total Amount`

### relation (5)
- `Categories`
- `Month`
- `Platform`
- `Projects`
- `Restock Connection`

### rich_text (4)
- `Description`
- `ID`
- `Payer`
- `Spend program`

### rollup (2)
- `Product`
- `Year`

### select (5)
- `Currency`
- `Fee currency`
- `State`
- `Type`
- `Type 1`

### title (1)
- `Name`

---

## Detailed Property Documentation

### Ads Expense show
- **Type:** `formula`
- **Formula:** `if(contains({{notion:block_property:gAbR:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}, "Ad"),{{notion:block_property:A%3CsI:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}},0)`

### Amount Currency
- **Type:** `number`

### Archive
- **Type:** `checkbox`

### Campaign Status
- **Type:** `formula`
- **Formula:** `if(dateBetween(now(), dateEnd({{notion:block_property:gW_A:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}), "days") > 0, "✅ Completed", if(dateBetween(now(), dateStart({{notion:block_property:gW_A:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}), "days") > 0, "🟡 Running", "🔵 Planned"))`

### Categories
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-81a9-a37b-fc2aabd167c8`

### Currency
- **Type:** `select`
- **Options:**
  - `EUR`
  - `USD`
  - `BRL`
  - `CAD`
  - `GBP`

### Current Month Expense
- **Type:** `formula`
- **Formula:** `if({{notion:block_property:%3BY%3EU:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}, {{notion:block_property:ikIJ:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}, 0)`

### Current Month?
- **Type:** `formula`
- **Formula:** `and(formatDate({{notion:block_property:gW_A:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}, "M") == formatDate(now(), "M"), formatDate({{notion:block_property:gW_A:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}, "Y") == formatDate(now(), "Y"))`

### Date
- **Type:** `date`

### Date completed (UTC)
- **Type:** `date`

### Description
- **Type:** `rich_text`

### Exchange Rate
- **Type:** `number`

### Exchange To Amount
- **Type:** `number`

### Fee
- **Type:** `number`

### Fee currency
- **Type:** `select`
- **Options:**
  - `EUR`
  - `USD`
  - `CAD`
  - `GBP`

### Freelance Sum
- **Type:** `formula`
- **Formula:** `if(contains({{notion:block_property:gAbR:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}, "Freelance Pay"), {{notion:block_property:A%3CsI:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}, 0)`

### ID
- **Type:** `rich_text`

### MCC
- **Type:** `number`

### Month
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-8101-81e1-c9f2d6803291`

### Monthly Salary 
- **Type:** `formula`
- **Formula:** `if({{notion:block_property:gAbR:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} == "Salary Pay" and {{notion:block_property:%3BY%3EU:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}, {{notion:block_property:ikIJ:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}, 0)`

### Name
- **Type:** `title`

### Number
- **Type:** `formula`
- **Formula:** `abs({{notion:block_property:y%5C%3Dw:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}})`

### Payer
- **Type:** `rich_text`

### Platform
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-81aa-a79c-ffad8081015e`

### Product
- **Type:** `rollup`
- **Relation Property:** `Restock Connection`
- **Rollup Property:** `Product`
- **Function:** `show_original`

### Projects
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-816d-a749-e741b1ac0b30`

### Restock Connection
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-8166-8009-ca3a0c85201b`

### Salary Sum
- **Type:** `formula`
- **Formula:** `if({{notion:block_property:gAbR:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} == "Salary Pay", {{notion:block_property:ikIJ:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}, 0)`

### Spend program
- **Type:** `rich_text`

### State
- **Type:** `select`
- **Options:**
  - `COMPLETED`

### Total Amount
- **Type:** `number`

### Total USD
- **Type:** `formula`
- **Formula:** `{{notion:block_property:QReO:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} * {{notion:block_property:_EY%3B:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}`

### Type
- **Type:** `select`
- **Options:**
  - `Loan Repayment`
  - `Business Expense`
  - `Ad Campagn`
  - `Salary Pay`
  - `Hourly Pay`
  - `Freelance Pay`
  - `Inventory Restock`

### Type 1
- **Type:** `select`
- **Options:**
  - `TRANSFER`
  - `EXCHANGE`
  - `TOPUP`
  - `FEE`
  - `CARD_PAYMENT`
  - `CARD_CREDIT`
  - `REFUND`
  - `CARD_REFUND`

### Year
- **Type:** `rollup`
- **Relation Property:** `Month`
- **Rollup Property:** `Year`
- **Function:** `show_original`

## 🚫 Empty & Unused Properties

*Analysis based on 389 pages*

### Completely Empty Properties (6)
*These properties have no data in any page:*

- `Archive` (checkbox)
- `Platform` (relation)
- `Product` (rollup)
- `Projects` (relation)
- `Restock Connection` (relation)
- `Spend program` (rich_text)

## Related Databases

- **Projects** (`226f4e0d-84e0-816d-a749-e741b1ac0b30`)
- **Categories** (`226f4e0d-84e0-81a9-a37b-fc2aabd167c8`)
- **Platform** (`226f4e0d-84e0-81aa-a79c-ffad8081015e`)
- **Month** (`226f4e0d-84e0-8101-81e1-c9f2d6803291`)
- **Restock Connection** (`226f4e0d-84e0-8166-8009-ca3a0c85201b`)

---

*Documentation generated on 2025-08-13 19:50:26*
