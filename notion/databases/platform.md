# Platform Database

**Database ID:** `226f4e0d-84e0-81aa-a79c-ffad8081015e`

**Created:** 2025-07-04T20:24:00.000Z
**Last Modified:** 2025-08-13T19:15:00.000Z
**Total Properties:** 6

---

## Properties Overview

### formula (1)
- `No.Of Posts REP`

### relation (3)
- `Ad Campaigns`
- `Ads`
- `Content`

### rollup (1)
- `Rollup`

### title (1)
- `Name`

---

## Detailed Property Documentation

### Ad Campaigns
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-819d-be89-db73c48eaee4`

### Ads
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-817e-84e2-c9a983663070`

### Content
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-816a-ac2f-f089654d45fc`

### Name
- **Type:** `title`

### No.Of Posts REP
- **Type:** `formula`
- **Formula:** `{{notion:block_property:XAdJ:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}.length() + " Posts"`

### Rollup
- **Type:** `rollup`
- **Relation Property:** `Content`
- **Rollup Property:** `Stage`
- **Function:** `percent_per_group`

## 🚫 Empty & Unused Properties

*Analysis based on 6 pages*

### Completely Empty Properties (1)
*These properties have no data in any page:*

- `Ads` (relation)

## Related Databases

- **Ads** (`226f4e0d-84e0-817e-84e2-c9a983663070`)
- **Content** (`226f4e0d-84e0-816a-ac2f-f089654d45fc`)
- **Ad Campaigns** (`226f4e0d-84e0-819d-be89-db73c48eaee4`)

---

*Documentation generated on 2025-08-13 19:50:19*
