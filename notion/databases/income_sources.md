# Income Sources Database

**Database ID:** `226f4e0d-84e0-81d9-b998-e61ecae5c421`

**Created:** 2025-07-04T20:28:00.000Z
**Last Modified:** 2025-08-13T19:15:00.000Z
**Total Properties:** 9

---

## Properties Overview

### formula (4)
- `Current Month`
- `Progress`
- `Remaining`
- `Total Income`

### number (1)
- `Monthly Goal`

### relation (1)
- `Budget Category`

### rich_text (2)
- `Goal Label`
- `Spent Label`

### title (1)
- `Name`

---

## Detailed Property Documentation

### Budget Category
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-8187-bcb1-c1290226a0a2`

### Current Month
- **Type:** `formula`
- **Formula:** `{{notion:block_property:ftyx:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}.map(current.{{notion:block_property:s%40a_:226f4e0d-84e0-81cb-9fc0-000baf8481c9:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}).sum()`

### Goal Label
- **Type:** `rich_text`

### Monthly Goal
- **Type:** `number`

### Name
- **Type:** `title`

### Progress
- **Type:** `formula`
- **Formula:** `round({{notion:block_property:%7D%3DfS:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}/{{notion:block_property:EN%3DR:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}*100)/100`

### Remaining
- **Type:** `formula`
- **Formula:** `if(empty({{notion:block_property:EN%3DR:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}), "", if({{notion:block_property:EN%3DR:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}>{{notion:block_property:%7D%3DfS:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}, ("$" +  replace(replace(format({{notion:block_property:EN%3DR:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}-{{notion:block_property:%7D%3DfS:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}), "(\d{1})(\d{3})$", "$1,$2"), "(\d{1})(\d{3},\d{3})", "$1,$2")+ " Remaining").style("red"),
("GOAL ACHIEVED").style("b","green")
	
)) `

### Spent Label
- **Type:** `rich_text`

### Total Income
- **Type:** `formula`
- **Formula:** `{{notion:block_property:ftyx:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}.map(current.{{notion:block_property:gFZJ:226f4e0d-84e0-81cb-9fc0-000baf8481c9:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}).sum()`

## ✅ Property Usage Analysis

*Analysis based on 2 pages*

**Great news!** All properties in this database have data. No completely empty or mostly unused properties were found.

## Related Databases

- **Budget Category** (`226f4e0d-84e0-8187-bcb1-c1290226a0a2`)

---

*Documentation generated on 2025-08-13 19:50:29*
