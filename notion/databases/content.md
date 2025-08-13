# Content Database

**Database ID:** `226f4e0d-84e0-816a-ac2f-f089654d45fc`

**Created:** 2025-07-04T20:24:00.000Z
**Last Modified:** 2025-08-13T19:15:00.000Z
**Total Properties:** 10

---

## Properties Overview

### created_time (1)
- `Created time`

### date (1)
- `Publish Date`

### files (1)
- `Files & media`

### formula (1)
- `Status`

### last_edited_time (1)
- `Last edited time`

### relation (1)
- `Platform`

### rich_text (1)
- `Description`

### select (1)
- `Type`

### status (1)
- `Stage`

### title (1)
- `Name`

---

## Detailed Property Documentation

### Created time
- **Type:** `created_time`

### Description
- **Type:** `rich_text`

### Files & media
- **Type:** `files`

### Last edited time
- **Type:** `last_edited_time`

### Name
- **Type:** `title`

### Platform
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-81aa-a79c-ffad8081015e`

### Publish Date
- **Type:** `date`

### Stage
- **Type:** `status`

### Status
- **Type:** `formula`
- **Formula:** `if({{notion:block_property:%3EB%7D%3A:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}=="Published", style("✓ Published","green","green_background"),if(
	{{notion:block_property:uPY%5D:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}==today(), ("Due Today").style("b","yellow"), 
 if((dateBetween(now(),{{notion:block_property:uPY%5D:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}},"days")*-1)<0, style("OVERDUE", "red","b","red_background"), (dateBetween(now(),{{notion:block_property:uPY%5D:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}},"days")*-1 + " Days left").style("b","grey"))))`

### Type
- **Type:** `select`
- **Options:**
  - `Reel`
  - `Short Video`
  - `Photo`
  - `Tweet`
  - `Blog`
  - `Video`

## 🚫 Empty & Unused Properties

*Analysis based on 5 pages*

### Completely Empty Properties (2)
*These properties have no data in any page:*

- `Description` (rich_text)
- `Files & media` (files)

## Related Databases

- **Platform** (`226f4e0d-84e0-81aa-a79c-ffad8081015e`)

---

*Documentation generated on 2025-08-13 19:50:20*
