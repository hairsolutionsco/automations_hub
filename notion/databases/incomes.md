# Incomes Database

**Database ID:** `229f4e0d-84e0-8128-a0bf-d7631b6aa22d`

**Created:** 2025-07-07T22:52:00.000Z
**Last Modified:** 2025-08-13T19:15:00.000Z
**Total Properties:** 8

---

## Properties Overview

### created_by (1)
- `Created by`

### created_time (1)
- `Created Date`

### date (1)
- `Payment Date`

### formula (2)
- `Income`
- `Order Income`

### number (1)
- `Amount`

### select (1)
- `Type`

### title (1)
- `Name`

---

## Detailed Property Documentation

### Amount
- **Type:** `number`

### Created Date
- **Type:** `created_time`

### Created by
- **Type:** `created_by`

### Income
- **Type:** `formula`
- **Formula:** `if({{notion:block_property:xTks:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}.contains("Order"), {{notion:block_property:L~%60O:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}, {{notion:block_property:PF%3AG:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}})`

### Name
- **Type:** `title`

### Order Income
- **Type:** `formula`
- **Formula:** `{{notion:block_property:EFwM:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}.map(current.{{notion:block_property:wyf%3E:229f4e0d-84e0-8126-94bd-000b055e80db:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}).sum()`

### Payment Date
- **Type:** `date`

### Type
- **Type:** `select`
- **Options:**
  - `General Income`
  - `Order Income`

---

*Documentation generated on 2025-08-13 19:50:21*
## 🚫 Empty & Unused Properties

*Analysis based on 23 pages*

### Completely Empty Properties (1)
*These properties have no data in any page:*

- `Amount` (number)

