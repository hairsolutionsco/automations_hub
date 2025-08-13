# Yearly Reports Database

**Database ID:** `226f4e0d-84e0-8179-98cb-cca8ecbf0c15`

**Created:** 2025-07-04T20:24:00.000Z
**Last Modified:** 2025-08-13T19:16:00.000Z
**Total Properties:** 18

---

## Properties Overview

### formula (6)
- `Balance`
- `Current Year?`
- `🔺 Order Income REP`
- `🔻 Ads REP`
- `🔻 Inventory Restock REP`
- `🔻 Salaries REP`

### relation (4)
- `Associated Payments`
- `Forecasted Payments`
- `Months`
- `Orders`

### rich_text (4)
- `Balance label`
- `Expense label`
- `Income label`
- `Salaries label`

### rollup (3)
- `Total Expense`
- `Total Income`
- `Total Salaries`

### title (1)
- `Name`

---

## Detailed Property Documentation

### Associated Payments
- **Type:** `relation`
- **Related Database:** `22af4e0d-84e0-80c3-a7d6-f0209d93081d`

### Balance
- **Type:** `formula`
- **Formula:** `{{notion:block_property:yNCI:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}-{{notion:block_property:%3DIE%60:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}`

### Balance label
- **Type:** `rich_text`

### Current Year?
- **Type:** `formula`
- **Formula:** `contains({{notion:block_property:title:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}, formatDate(now(), "YYYY")) or contains({{notion:block_property:title:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}, formatDate(now(), "YYYY"))`

### Expense label
- **Type:** `rich_text`

### Forecasted Payments
- **Type:** `relation`
- **Related Database:** `22cf4e0d-84e0-802a-bf76-e564658fdc5f`

### Income label
- **Type:** `rich_text`

### Months
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-8101-81e1-c9f2d6803291`

### Name
- **Type:** `title`

### Orders
- **Type:** `relation`
- **Related Database:** `228f4e0d-84e0-816f-8511-fab726d2c6ef`

### Salaries label
- **Type:** `rich_text`

### Total Expense
- **Type:** `rollup`
- **Relation Property:** `Months`
- **Rollup Property:** `Expenses show`
- **Function:** `sum`

### Total Income
- **Type:** `rollup`
- **Relation Property:** `Months`
- **Rollup Property:** `Income show`
- **Function:** `sum`

### Total Salaries
- **Type:** `rollup`
- **Relation Property:** `Months`
- **Rollup Property:** `Salary show`
- **Function:** `sum`

### 🔺 Order Income REP
- **Type:** `formula`
- **Formula:** `"|- Orders Income: " + "$" + sum({{notion:block_property:PJ%5Ey:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}.map(current.{{notion:block_property:JJdI:226f4e0d-84e0-8101-81e1-c9f2d6803291:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}))`

### 🔻 Ads REP
- **Type:** `formula`
- **Formula:** `"|- Ad Campaigns: " + "$" + sum({{notion:block_property:PJ%5Ey:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}.map(current.{{notion:block_property:IcQz:226f4e0d-84e0-8101-81e1-c9f2d6803291:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}))`

### 🔻 Inventory Restock REP
- **Type:** `formula`
- **Formula:** `"|- Restock Expense: " + "$" + sum({{notion:block_property:PJ%5Ey:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}.map(current.{{notion:block_property:d%5Bi%60:226f4e0d-84e0-8101-81e1-c9f2d6803291:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}))`

### 🔻 Salaries REP
- **Type:** `formula`
- **Formula:** `"|- Salaries: " + "$" + sum({{notion:block_property:PJ%5Ey:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}.map(current.{{notion:block_property:LMj%3C:226f4e0d-84e0-8101-81e1-c9f2d6803291:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}))`

## ✅ Property Usage Analysis

*Analysis based on 9 pages*

**Great news!** All properties in this database have data. No completely empty or mostly unused properties were found.

## Related Databases

- **Associated Payments** (`22af4e0d-84e0-80c3-a7d6-f0209d93081d`)
- **Months** (`226f4e0d-84e0-8101-81e1-c9f2d6803291`)
- **Orders** (`228f4e0d-84e0-816f-8511-fab726d2c6ef`)
- **Forecasted Payments** (`22cf4e0d-84e0-802a-bf76-e564658fdc5f`)

---

*Documentation generated on 2025-08-13 19:50:37*
