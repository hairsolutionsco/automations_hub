# Expense Categories Database

**Database ID:** `226f4e0d-84e0-81a9-a37b-fc2aabd167c8`

**Created:** 2025-07-04T20:24:00.000Z
**Last Modified:** 2025-08-13T19:15:00.000Z
**Total Properties:** 9

---

## Properties Overview

### formula (2)
- `Budget Progress`
- `Status`

### number (1)
- `Monthly Budget`

### relation (1)
- `Expenses`

### rich_text (3)
- `Description`
- `Spent label`
- `budget label`

### rollup (1)
- `Expense this Month`

### title (1)
- `Name`

---

## Detailed Property Documentation

### Budget Progress
- **Type:** `formula`
- **Formula:** `round(({{notion:block_property:RuOY:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}/{{notion:block_property:%3Ci%3ES:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}})*100)/100`

### Description
- **Type:** `rich_text`

### Expense this Month
- **Type:** `rollup`
- **Relation Property:** `Expenses`
- **Rollup Property:** `Current Month Expense`
- **Function:** `sum`

### Expenses
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-817e-84e2-c9a983663070`

### Monthly Budget
- **Type:** `number`

### Name
- **Type:** `title`

### Spent label
- **Type:** `rich_text`

### Status
- **Type:** `formula`
- **Formula:** `if(empty({{notion:block_property:%3Ci%3ES:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}), "No Budget Limit added", if({{notion:block_property:RuOY:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} < {{notion:block_property:%3Ci%3ES:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}, style("✓ In Budget" ,"green","green_background","b"), style("⭕️ Budget Exceeded","red","b","red_background")))`

### budget label
- **Type:** `rich_text`

## ✅ Property Usage Analysis

*Analysis based on 8 pages*

**Great news!** All properties in this database have data. No completely empty or mostly unused properties were found.

## Related Databases

- **Expenses** (`226f4e0d-84e0-817e-84e2-c9a983663070`)

---

*Documentation generated on 2025-08-13 19:50:29*
