# Business Projects Database

**Database ID:** `226f4e0d-84e0-816d-a749-e741b1ac0b30`

**Created:** 2025-07-04T20:24:00.000Z
**Last Modified:** 2025-08-13T19:16:00.000Z
**Total Properties:** 23

---

## Properties Overview

### checkbox (1)
- `Archive`

### date (1)
- `Timeline`

### formula (6)
- `Auto progress`
- `Days left`
- `Expenses sum`
- `Tasks Ratio`
- `Total Project Cost`
- `Total Time Spent`

### last_edited_time (1)
- `Last edited time`

### people (1)
- `Assign Account`

### relation (6)
- `Events`
- `Expenses`
- `Parent item`
- `Resources`
- `Sub-item`
- `Tasks`

### rollup (4)
- `Done / All Tasks`
- `Task Progress`
- `Total Labour Cost`
- `Total Time (min)`

### select (1)
- `Priority`

### status (1)
- `Status`

### title (1)
- `Name`

---

## Detailed Property Documentation

### Archive
- **Type:** `checkbox`

### Assign Account
- **Type:** `people`

### Auto progress
- **Type:** `formula`
- **Formula:** `("Work " + format(round({{notion:block_property:OOoB:226f4e0d-84e0-81ae-be7b-000b1f6727d2:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} * 100))) + "% Completed"`

### Days left
- **Type:** `formula`
- **Formula:** `if(dateBetween(now(),dateEnd({{notion:block_property:lpLz:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}),"days")==0, style("Due Today","red","b"), (if({{notion:block_property:Ps%7Da:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}== "Completed", style("✓ Completed","green","b"), if((dateBetween(now(),dateEnd({{notion:block_property:lpLz:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}),"days")*-1)<0, style("◉ Overdue","red","b") ,style(( "◉ " + (dateBetween(now(),dateEnd({{notion:block_property:lpLz:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}),"days")*-1+1) + " Days Left"),"b","grey"))))) + "\n" + dateEnd({{notion:block_property:lpLz:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}})`

### Done / All Tasks
- **Type:** `rollup`
- **Relation Property:** `Tasks`
- **Rollup Property:** `Status`
- **Function:** `count_per_group`

### Events
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-8145-8cb8-c5896e49d0b5`

### Expenses
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-817e-84e2-c9a983663070`

### Expenses sum
- **Type:** `formula`
- **Formula:** `{{notion:block_property:Th%5EY:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}.map(current.{{notion:block_property:A%3CsI:226f4e0d-84e0-817e-84e2-c9a983663070:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}).sum()`

### Last edited time
- **Type:** `last_edited_time`

### Name
- **Type:** `title`

### Parent item
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-816d-a749-e741b1ac0b30`

### Priority
- **Type:** `select`
- **Options:**
  - `High Priority`
  - `Medium Priority`
  - `Low Priority`

### Resources
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-8135-a4f7-ee34b04fe01b`

### Status
- **Type:** `status`

### Sub-item
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-816d-a749-e741b1ac0b30`

### Task Progress
- **Type:** `rollup`
- **Relation Property:** `Tasks`
- **Rollup Property:** `Status`
- **Function:** `percent_per_group`

### Tasks
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-8168-8718-d8f6b2d1fe3d`

### Tasks Ratio
- **Type:** `formula`
- **Formula:** `format({{notion:block_property:%5D%3DF%5E:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} + " Tasks Done")`

### Timeline
- **Type:** `date`

### Total Labour Cost
- **Type:** `rollup`
- **Relation Property:** `Tasks`
- **Rollup Property:** `Total labour Cost`
- **Function:** `sum`

### Total Project Cost
- **Type:** `formula`
- **Formula:** `{{notion:block_property:%7D~Bb:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}.sum()+{{notion:block_property:Sh%7DB:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}`

### Total Time (min)
- **Type:** `rollup`
- **Relation Property:** `Tasks`
- **Rollup Property:** `Time Spent. (min)`
- **Function:** `sum`

### Total Time Spent
- **Type:** `formula`
- **Formula:** `format((if(({{notion:block_property:SDwY:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} >= 60), (format(floor({{notion:block_property:SDwY:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} / 60)) + " hours "), "") + if((({{notion:block_property:SDwY:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} % 60) > 0), (format({{notion:block_property:SDwY:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} % 60) + " minutes "), "0 minutes")))`

## 🚫 Empty & Unused Properties

*Analysis based on 5 pages*

### Completely Empty Properties (5)
*These properties have no data in any page:*

- `Archive` (checkbox)
- `Expenses` (relation)
- `Resources` (relation)
- `Task Progress` (rollup)
- `Tasks` (relation)

## Related Databases

- **Resources** (`226f4e0d-84e0-8135-a4f7-ee34b04fe01b`)
- **Tasks** (`226f4e0d-84e0-8168-8718-d8f6b2d1fe3d`)
- **Sub-item** (`226f4e0d-84e0-816d-a749-e741b1ac0b30`)
- **Parent item** (`226f4e0d-84e0-816d-a749-e741b1ac0b30`)
- **Expenses** (`226f4e0d-84e0-817e-84e2-c9a983663070`)
- **Events** (`226f4e0d-84e0-8145-8cb8-c5896e49d0b5`)

---

*Documentation generated on 2025-08-13 19:50:34*
