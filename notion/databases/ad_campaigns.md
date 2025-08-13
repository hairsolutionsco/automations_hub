# Ad Campaigns Database

**Database ID:** `226f4e0d-84e0-819d-be89-db73c48eaee4`

**Created:** 2025-07-04T20:24:00.000Z
**Last Modified:** 2025-08-13T19:15:00.000Z
**Total Properties:** 6

---

## Properties Overview

### date (1)
- `Duration`

### formula (2)
- `Status`
- `Total Cost`

### number (1)
- `Cost per day`

### relation (1)
- `Platform`

### title (1)
- `Name`

---

## Detailed Property Documentation

### Cost per day
- **Type:** `number`

### Duration
- **Type:** `date`

### Name
- **Type:** `title`

### Platform
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-81aa-a79c-ffad8081015e`

### Status
- **Type:** `formula`
- **Formula:** `if(dateBetween(now(), dateEnd({{notion:block_property:ECej:226f4e0d-84e0-811a-ab43-000b4f956ccc:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}), "days") > 0, "✅ Completed", if(dateBetween(now(), dateStart({{notion:block_property:ECej:226f4e0d-84e0-811a-ab43-000b4f956ccc:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}), "days") > 0, "🟡 Running", "🔵 Planned"))`

### Total Cost
- **Type:** `formula`
- **Formula:** `if(dateBetween(dateStart({{notion:block_property:ECej:226f4e0d-84e0-811a-ab43-000b4f956ccc:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}), dateEnd({{notion:block_property:ECej:226f4e0d-84e0-811a-ab43-000b4f956ccc:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}), "days") == 0, {{notion:block_property:k~%3A_:226f4e0d-84e0-811a-ab43-000b4f956ccc:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}, (dateBetween(dateStart({{notion:block_property:ECej:226f4e0d-84e0-811a-ab43-000b4f956ccc:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}), dateEnd({{notion:block_property:ECej:226f4e0d-84e0-811a-ab43-000b4f956ccc:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}), "days") * -1) * {{notion:block_property:k~%3A_:226f4e0d-84e0-811a-ab43-000b4f956ccc:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}})`

## ✅ Property Usage Analysis

*Analysis based on 1 pages*

**Great news!** All properties in this database have data. No completely empty or mostly unused properties were found.

## Related Databases

- **Platform** (`226f4e0d-84e0-81aa-a79c-ffad8081015e`)

---

*Documentation generated on 2025-08-13 19:50:19*
