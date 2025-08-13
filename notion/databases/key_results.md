# Key Results Database

**Database ID:** `226f4e0d-84e0-815f-b434-c1a6e3a28e16`

**Created:** 2025-07-04T20:24:00.000Z
**Last Modified:** 2025-08-13T19:16:00.000Z
**Total Properties:** 8

---

## Properties Overview

### checkbox (1)
- `Complete (manual)`

### formula (2)
- `Complete formula`
- `Progress`

### number (2)
- `Current`
- `Target`

### relation (1)
- `Objectives`

### rollup (1)
- `Archived?`

### title (1)
- `Name`

---

## Detailed Property Documentation

### Archived?
- **Type:** `rollup`
- **Relation Property:** `Objectives`
- **Rollup Property:** `Archive`
- **Function:** `show_original`

### Complete (manual)
- **Type:** `checkbox`

### Complete formula
- **Type:** `formula`
- **Formula:** `if({{notion:block_property:F%5Bim:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}==true, true, if({{notion:block_property:pVjj:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}==1, true, false
	
))
	`

### Current
- **Type:** `number`

### Name
- **Type:** `title`

### Objectives
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-81f1-88a5-f0eb2eb1bd87`

### Progress
- **Type:** `formula`
- **Formula:** `if({{notion:block_property:F%5Bim:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}==true, 1, (({{notion:block_property:h%7D%5D%5D:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}/{{notion:block_property:I%5Ce%5C:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}})*100).round()/100)`

### Target
- **Type:** `number`

## 🚫 Empty & Unused Properties

*Analysis based on 22 pages*

### Completely Empty Properties (1)
*These properties have no data in any page:*

- `Complete (manual)` (checkbox)

## Related Databases

- **Objectives** (`226f4e0d-84e0-81f1-88a5-f0eb2eb1bd87`)

---

*Documentation generated on 2025-08-13 19:50:40*
