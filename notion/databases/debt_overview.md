# Debt Overview Database

**Database ID:** `226f4e0d-84e0-8171-aea1-d054e8cb0786`

**Created:** 2025-07-04T20:28:00.000Z
**Last Modified:** 2025-08-13T19:16:00.000Z
**Total Properties:** 9

---

## Properties Overview

### formula (4)
- `Overall progress`
- `Paid`
- `To be paid`
- `Total Debt`

### relation (1)
- `Debt Tracking`

### rich_text (3)
- `Paid label`
- `To be paid label`
- `total label`

### title (1)
- `Name`

---

## Detailed Property Documentation

### Debt Tracking
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-8130-8a9c-ce4a29ef7a35`

### Name
- **Type:** `title`

### Overall progress
- **Type:** `formula`
- **Formula:** `round(({{notion:block_property:MYCD:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}/{{notion:block_property:PdX%5D:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}})*100)/100`

### Paid
- **Type:** `formula`
- **Formula:** `{{notion:block_property:t%3EOC:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}.map(current.{{notion:block_property:~uSr:226f4e0d-84e0-8130-8a9c-ce4a29ef7a35:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}).sum()`

### Paid label
- **Type:** `rich_text`

### To be paid
- **Type:** `formula`
- **Formula:** `{{notion:block_property:t%3EOC:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}.map(current.{{notion:block_property:knxx:226f4e0d-84e0-8130-8a9c-ce4a29ef7a35:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}).sum()`

### To be paid label
- **Type:** `rich_text`

### Total Debt
- **Type:** `formula`
- **Formula:** `{{notion:block_property:t%3EOC:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}.map(current.{{notion:block_property:nr%3EZ:226f4e0d-84e0-8130-8a9c-ce4a29ef7a35:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}).sum()`

### total label
- **Type:** `rich_text`

## ✅ Property Usage Analysis

*Analysis based on 1 pages*

**Great news!** All properties in this database have data. No completely empty or mostly unused properties were found.

## Related Databases

- **Debt Tracking** (`226f4e0d-84e0-8130-8a9c-ce4a29ef7a35`)

---

*Documentation generated on 2025-08-13 19:50:31*
