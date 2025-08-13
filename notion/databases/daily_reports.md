# Daily Reports Database

**Database ID:** `22cf4e0d-84e0-8036-a313-f6cfa1fa9801`

**Created:** 2025-07-10T03:26:00.000Z
**Last Modified:** 2025-08-13T19:16:00.000Z
**Total Properties:** 37

---

## Properties Overview

### date (1)
- `Month Start`

### formula (13)
- `Ads Show`
- `Balance`
- `Current month?`
- `Expenses show`
- `Income show`
- `Profit made`
- `Profit made REP`
- `Restock Expense show`
- `Salary show`
- `🔺 Orders Income REP`
- `🔻 Ad Campaigns REP`
- `🔻 Restock REP`
- `🔻 Salary REP.`

### relation (8)
- `Associated Payments`
- `Associated Subscription Payments`
- `Expenses and Ads`
- `Forecasted Payments`
- `Forecasted Payments 1`
- `Monthly Reports`
- `Orders`
- `Stock Update`

### rich_text (5)
- `Balance label`
- `Expense label`
- `Income Label`
- `Orders Rep`
- `Salary REP`

### rollup (9)
- `Ads Sum`
- `Order Income`
- `Restock Expense`
- `Rollup`
- `Rollup 1`
- `Rollup 2`
- `Salary Payments`
- `Total Expense`
- `Total Income`

### title (1)
- `Name`

---

## Detailed Property Documentation

### Ads Show
- **Type:** `formula`
- **Formula:** `{{notion:block_property:gfBa:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}`

### Ads Sum
- **Type:** `rollup`
- **Relation Property:** `Expenses and Ads`
- **Rollup Property:** `Ads Expense show`
- **Function:** `sum`

### Associated Payments
- **Type:** `relation`
- **Related Database:** `22af4e0d-84e0-80c3-a7d6-f0209d93081d`

### Associated Subscription Payments
- **Type:** `relation`
- **Related Database:** `228f4e0d-84e0-815c-a108-e48054988ac0`

### Balance
- **Type:** `formula`
- **Formula:** `{{notion:block_property:RMH%60:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}-{{notion:block_property:%7DUpg:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}`

### Balance label
- **Type:** `rich_text`

### Current month?
- **Type:** `formula`
- **Formula:** `contains({{notion:block_property:title:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}, formatDate(now(), "MMMM YYYY")) or contains({{notion:block_property:title:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}, formatDate(now(), "YYYY MMMM"))`

### Expense label
- **Type:** `rich_text`

### Expenses and Ads
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-817e-84e2-c9a983663070`

### Expenses show
- **Type:** `formula`
- **Formula:** `{{notion:block_property:%7DUpg:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}`

### Forecasted Payments
- **Type:** `relation`
- **Related Database:** `22cf4e0d-84e0-802a-bf76-e564658fdc5f`

### Forecasted Payments 1
- **Type:** `relation`
- **Related Database:** `22cf4e0d-84e0-802a-bf76-e564658fdc5f`

### Income Label
- **Type:** `rich_text`

### Income show
- **Type:** `formula`
- **Formula:** `{{notion:block_property:RMH%60:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}`

### Month Start
- **Type:** `date`

### Monthly Reports
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-8101-81e1-c9f2d6803291`

### Name
- **Type:** `title`

### Order Income
- **Type:** `rollup`
- **Relation Property:** `Orders`
- **Rollup Property:** `Income`
- **Function:** `sum`

### Orders
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-81a5-acbe-d9803b31dd28`

### Orders Rep
- **Type:** `rich_text`

### Profit made
- **Type:** `formula`
- **Formula:** `{{notion:block_property:%5B%7CgF:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}.map(current.{{notion:block_property:%3FFFD:226f4e0d-84e0-81a5-acbe-d9803b31dd28:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}).sum()`

### Profit made REP
- **Type:** `formula`
- **Formula:** `("[ Profit: " + "$" + {{notion:block_property:p%3F%5CG:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} + " ]").style("grey")`

### Restock Expense
- **Type:** `rollup`
- **Relation Property:** `Stock Update`
- **Rollup Property:** `Expense Sum`
- **Function:** `sum`

### Restock Expense show
- **Type:** `formula`
- **Formula:** `{{notion:block_property:d%5Bi%60:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}`

### Rollup
- **Type:** `rollup`
- **Relation Property:** `Associated Payments`
- **Rollup Property:** `Income Type`
- **Function:** `count`

### Rollup 1
- **Type:** `rollup`
- **Relation Property:** `Associated Payments`
- **Rollup Property:** `Associated Client`
- **Function:** `show_original`

### Rollup 2
- **Type:** `rollup`
- **Relation Property:** `Associated Subscription Payments`
- **Rollup Property:** `Monthly recurring revenue in company currency`
- **Function:** `sum`

### Salary Payments
- **Type:** `rollup`
- **Relation Property:** `Expenses and Ads`
- **Rollup Property:** `Salary Sum`
- **Function:** `sum`

### Salary REP
- **Type:** `rich_text`

### Salary show
- **Type:** `formula`
- **Formula:** `{{notion:block_property:ULLp:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}`

### Stock Update
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-8166-8009-ca3a0c85201b`

### Total Expense
- **Type:** `rollup`
- **Relation Property:** `Expenses and Ads`
- **Rollup Property:** `Total USD`
- **Function:** `sum`

### Total Income
- **Type:** `rollup`
- **Relation Property:** `Associated Payments`
- **Rollup Property:** `Total USD`
- **Function:** `sum`

### 🔺 Orders Income REP
- **Type:** `formula`
- **Formula:** `("|- " + "Orders Income: " + "$" + {{notion:block_property:JJdI:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}).style("grey")`

### 🔻 Ad Campaigns REP
- **Type:** `formula`
- **Formula:** `("|- " + "Ad Campaigns: " + "$" + {{notion:block_property:gfBa:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}).style("grey")`

### 🔻 Restock REP
- **Type:** `formula`
- **Formula:** `("|- " + "Restock Expense: " + "$" + {{notion:block_property:d%5Bi%60:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}).style("grey")`

### 🔻 Salary REP.
- **Type:** `formula`
- **Formula:** `("|- " + "Salary Payments: " + "$" + {{notion:block_property:LMj%3C:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}).style("grey")`

## 🚫 Empty & Unused Properties

*Analysis based on 336 pages*

### Completely Empty Properties (8)
*These properties have no data in any page:*

- `Associated Payments` (relation)
- `Associated Subscription Payments` (relation)
- `Expenses and Ads` (relation)
- `Forecasted Payments` (relation)
- `Month Start` (date)
- `Orders` (relation)
- `Rollup 1` (rollup)
- `Stock Update` (relation)

### Mostly Empty Properties (5)
*These properties have data in less than 5% of pages:*

- `Salary REP` (rich_text) - 97.0% empty, only 10 pages with data
- `Balance label` (rich_text) - 97.0% empty, only 10 pages with data
- `Expense label` (rich_text) - 97.0% empty, only 10 pages with data
- `Orders Rep` (rich_text) - 97.0% empty, only 10 pages with data
- `Income Label` (rich_text) - 97.0% empty, only 10 pages with data

## Related Databases

- **Associated Payments** (`22af4e0d-84e0-80c3-a7d6-f0209d93081d`)
- **Forecasted Payments 1** (`22cf4e0d-84e0-802a-bf76-e564658fdc5f`)
- **Forecasted Payments** (`22cf4e0d-84e0-802a-bf76-e564658fdc5f`)
- **Orders** (`226f4e0d-84e0-81a5-acbe-d9803b31dd28`)
- **Stock Update** (`226f4e0d-84e0-8166-8009-ca3a0c85201b`)
- **Monthly Reports** (`226f4e0d-84e0-8101-81e1-c9f2d6803291`)
- **Associated Subscription Payments** (`228f4e0d-84e0-815c-a108-e48054988ac0`)
- **Expenses and Ads** (`226f4e0d-84e0-817e-84e2-c9a983663070`)

---

*Documentation generated on 2025-08-13 19:50:36*
