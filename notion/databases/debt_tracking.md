# Debt Tracking Database

**Database ID:** `226f4e0d-84e0-8130-8a9c-ce4a29ef7a35`

**Created:** 2025-07-04T20:28:00.000Z
**Last Modified:** 2025-08-13T19:15:00.000Z
**Total Properties:** 12

---

## Properties Overview

### formula (3)
- `Amount Left`
- `Amount Paid`
- `Progress`

### number (3)
- `Estimated Total`
- `Interest rate`
- `Original amount`

### relation (2)
- `Debt Overview`
- `Transactions`

### rich_text (3)
- `Amount left`
- `Amount paid`
- `Debt amount label`

### title (1)
- `Name`

---

## Detailed Property Documentation

### Amount Left
- **Type:** `formula`
- **Formula:** `if(empty({{notion:block_property:wqRk:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}),{{notion:block_property:GaXd:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}},{{notion:block_property:nr%3EZ:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}})-{{notion:block_property:~uSr:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}`

### Amount Paid
- **Type:** `formula`
- **Formula:** `{{notion:block_property:UZEE:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}.map(current.{{notion:block_property:K%5BSc:226f4e0d-84e0-81a9-a550-c00c043660bb:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}).sum()`

### Amount left
- **Type:** `rich_text`

### Amount paid
- **Type:** `rich_text`

### Debt Overview
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-8171-aea1-d054e8cb0786`

### Debt amount label
- **Type:** `rich_text`

### Estimated Total
- **Type:** `number`

### Interest rate
- **Type:** `number`

### Name
- **Type:** `title`

### Original amount
- **Type:** `number`

### Progress
- **Type:** `formula`
- **Formula:** `round(({{notion:block_property:~uSr:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}/if(empty({{notion:block_property:wqRk:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}),{{notion:block_property:GaXd:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}},{{notion:block_property:nr%3EZ:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}))*100)/100`

### Transactions
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-81a9-a550-c00c043660bb`

## 🚫 Empty & Unused Properties

*Analysis based on 3 pages*

### Completely Empty Properties (3)
*These properties have no data in any page:*

- `Estimated Total` (number)
- `Interest rate` (number)
- `Transactions` (relation)

## Related Databases

- **Debt Overview** (`226f4e0d-84e0-8171-aea1-d054e8cb0786`)
- **Transactions** (`226f4e0d-84e0-81a9-a550-c00c043660bb`)

---

*Documentation generated on 2025-08-13 19:50:30*
