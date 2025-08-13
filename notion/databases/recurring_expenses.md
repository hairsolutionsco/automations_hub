# Recurring Expenses Database

**Database ID:** `226f4e0d-84e0-813f-b2e9-d228f70676b9`

**Created:** 2025-07-04T20:24:00.000Z
**Last Modified:** 2025-08-13T19:15:00.000Z
**Total Properties:** 10

---

## Properties Overview

### checkbox (1)
- `Added to the expense db as recurring?`

### date (1)
- `Cycle start Date`

### formula (3)
- `Monthly Expense`
- `Next Payment Date`
- `Yearly Expense`

### number (2)
- `Amount EUR`
- `Amount USD`

### select (2)
- `Frequency`
- `Type`

### title (1)
- `Name`

---

## Detailed Property Documentation

### Added to the expense db as recurring?
- **Type:** `checkbox`

### Amount EUR
- **Type:** `number`

### Amount USD
- **Type:** `number`

### Cycle start Date
- **Type:** `date`

### Frequency
- **Type:** `select`
- **Options:**
  - `Yearly`
  - `Monthly`

### Monthly Expense
- **Type:** `formula`
- **Formula:** `if({{notion:block_property:dBpv:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}=="Monthly", {{notion:block_property:MPTE:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}, {{notion:block_property:MPTE:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}/12)`

### Name
- **Type:** `title`

### Next Payment Date
- **Type:** `formula`
- **Formula:** `if({{notion:block_property:dBpv:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} == "Daily", dateAdd({{notion:block_property:%5B%3BCq:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}, dateBetween(now(), {{notion:block_property:%5B%3BCq:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}, "days") + 1, "days"), if({{notion:block_property:dBpv:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} == "Weekly", dateAdd({{notion:block_property:%5B%3BCq:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}, dateBetween(now(), {{notion:block_property:%5B%3BCq:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}, "weeks") + 1, "weeks"), if({{notion:block_property:dBpv:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} == "Monthly", dateAdd({{notion:block_property:%5B%3BCq:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}, dateBetween(now(), {{notion:block_property:%5B%3BCq:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}, "months") + 1, "months"), if({{notion:block_property:dBpv:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} == "Yearly", dateAdd({{notion:block_property:%5B%3BCq:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}, dateBetween(now(), {{notion:block_property:%5B%3BCq:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}, "years") + 1, "years"), if({{notion:block_property:dBpv:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} == "Quarterly", dateAdd({{notion:block_property:%5B%3BCq:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}, dateBetween(now(), {{notion:block_property:%5B%3BCq:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}, "quarters") + 1, "quarters"), today())))))`

### Type
- **Type:** `select`
- **Options:**
  - `AI`
  - `Drive`
  - `Workspace`
  - `Website`
  - `Research`
  - `Tools`

### Yearly Expense
- **Type:** `formula`
- **Formula:** `if({{notion:block_property:dBpv:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}=="Yearly", {{notion:block_property:MPTE:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}, {{notion:block_property:MPTE:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}*12)`

---

*Documentation generated on 2025-08-13 19:50:27*
## ✅ Property Usage Analysis

*Analysis based on 16 pages*

**Great news!** All properties in this database have data. No completely empty or mostly unused properties were found.

