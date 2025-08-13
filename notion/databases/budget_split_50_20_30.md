# Budget Split 50/20/30 Database

**Database ID:** `226f4e0d-84e0-8187-bcb1-c1290226a0a2`

**Created:** 2025-07-04T20:28:00.000Z
**Last Modified:** 2025-08-13T19:16:00.000Z
**Total Properties:** 9

---

## Properties Overview

### formula (4)
- `Budget Progress`
- `Current Month Expense`
- `Income Split`
- `Status`

### number (1)
- `Budget Split %`

### relation (3)
- `Expense Sources`
- `Income Source`
- `Transfers`

### title (1)
- `Name`

---

## Detailed Property Documentation

### Budget Progress
- **Type:** `formula`
- **Formula:** `round(({{notion:block_property:PfMx:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}/{{notion:block_property:cCVX:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}})*100)/100`

### Budget Split %
- **Type:** `number`

### Current Month Expense
- **Type:** `formula`
- **Formula:** `{{notion:block_property:%5E%7CZ%3E:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}.map(current.{{notion:block_property:%7D%3AK%60:226f4e0d-84e0-81de-a364-fe70d608f59f:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}).sum() + {{notion:block_property:v%3Az_:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}.map(current.{{notion:block_property:axp%3C:226f4e0d-84e0-81bc-9ea0-d326c752ea42:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}).sum()`

### Expense Sources
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-81de-a364-fe70d608f59f`

### Income Source
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-81d9-b998-e61ecae5c421`

### Income Split
- **Type:** `formula`
- **Formula:** `{{notion:block_property:Kuhf:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}*({{notion:block_property:%3FMB%60:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}.map(current.{{notion:block_property:%7D%3DfS:226f4e0d-84e0-81d9-b998-e61ecae5c421:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}).sum())`

### Name
- **Type:** `title`

### Status
- **Type:** `formula`
- **Formula:** `if({{notion:block_property:cCVX:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}==0, "", (if({{notion:block_property:PfMx:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}<{{notion:block_property:cCVX:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}},
("$" + replace(replace(format({{notion:block_property:cCVX:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}-{{notion:block_property:PfMx:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}), "(\d{1})(\d{3})$", "$1,$2"), "(\d{1})(\d{3},\d{3})", "$1,$2")).style("green","b") + ("").style("grey"), 

("$" + replace(replace(format({{notion:block_property:PfMx:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}-{{notion:block_property:cCVX:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}), "(\d{1})(\d{3})$", "$1,$2"), "(\d{1})(\d{3},\d{3})", "$1,$2")).style("red","b") + (" Over Budget").style("grey"))))`

### Transfers
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-81bc-9ea0-d326c752ea42`

## 🚫 Empty & Unused Properties

*Analysis based on 2 pages*

### Completely Empty Properties (2)
*These properties have no data in any page:*

- `Status` (formula)
- `Transfers` (relation)

## Related Databases

- **Income Source** (`226f4e0d-84e0-81d9-b998-e61ecae5c421`)
- **Expense Sources** (`226f4e0d-84e0-81de-a364-fe70d608f59f`)
- **Transfers** (`226f4e0d-84e0-81bc-9ea0-d326c752ea42`)

---

*Documentation generated on 2025-08-13 19:50:32*
