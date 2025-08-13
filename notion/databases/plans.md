# Plans Database

**Database ID:** `228f4e0d-84e0-815c-a108-e48054988ac0`

**Created:** 2025-07-06T17:06:00.000Z
**Last Modified:** 2025-08-13T19:15:00.000Z
**Total Properties:** 67

---

## Properties Overview

### checkbox (1)
- `To verify`

### date (9)
- `Churn date`
- `End date`
- `First Installment Date`
- `Last Installment Date`
- `Last Payment Date`
- `Next billing date`
- `Payment method`
- `Start date`
- `Subscription modified on`

### number (14)
- `Annual recurring revenue`
- `Annual recurring revenue in company currency`
- `Current Line Item IDs`
- `Last payment amount`
- `Monthly recurring revenue`
- `Monthly recurring revenue in company currency`
- `Net Payment Terms`
- `Next payment amount`
- `Number of completed payments`
- `Number of expected payments`
- `Recipient billing postal code`
- `Record ID`
- `Total Remaining Amount`
- `Total collected amount`

### relation (6)
- `Associated Client`
- `Associated Deal`
- `Monthly Reports`
- `Related Subscriptions`
- `Related to Contacts (1) (Related to Subscriptions (Associated Contacts))`
- `Related to Deals (Associated Subscriptions)`

### rich_text (16)
- `Allowed payment methods`
- `Contact email`
- `First Delivery ETA`
- `Recipient billing city`
- `Recipient billing country`
- `Recipient billing country code`
- `Recipient billing state/region`
- `Recipient billing street address`
- `Recipient billing street address 2`
- `Record source detail 1`
- `Record source detail 2`
- `Record source detail 3`
- `Store payment method at checkout`
- `Upcoming Line Item`
- `Upcoming Line Item IDs`
- `Update payment method link`

### rollup (4)
- `Installment Amount`
- `Plan Size`
- `Rollup`
- `Rollup 1`

### select (16)
- `Automatically email invoices`
- `Collection process`
- `Currency`
- `Currency code`
- `Current Line Item`
- `Delivery Frequency`
- `Invoice Creation`
- `Payment Enabled`
- `Payment Processor`
- `Payment source`
- `Processor`
- `Record source`
- `Recurring billing frequency`
- `Status`
- `Subscription Status`
- `Tax ID`

### title (1)
- `Name`

---

## Detailed Property Documentation

### Allowed payment methods
- **Type:** `rich_text`

### Annual recurring revenue
- **Type:** `number`

### Annual recurring revenue in company currency
- **Type:** `number`

### Associated Client
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-814c-ad70-d478cebeee30`

### Associated Deal
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-808c-af51-e09c154008db`

### Automatically email invoices
- **Type:** `select`
- **Options:**
  - `false`

### Churn date
- **Type:** `date`

### Collection process
- **Type:** `select`
- **Options:**
  - `Automatic payments`
  - `Manual payments`

### Contact email
- **Type:** `rich_text`

### Currency
- **Type:** `select`
- **Options:**
  - `GBP`
  - `CAD`
  - `USD`
  - `EUR`

### Currency code
- **Type:** `select`
- **Options:**
  - `CAD`
  - `USD`
  - `EUR`
  - `GBP`

### Current Line Item
- **Type:** `select`
- **Options:**
  - `3 Hair Systems Plan`
  - `4 Hair Systems Plan`
  - `6-Unit Plan`
  - `6 Hair Systems Plan`
  - `4-Unit Plan`

### Current Line Item IDs
- **Type:** `number`

### Delivery Frequency
- **Type:** `select`
- **Options:**
  - `1 unit every 8 weeks`
  - `1 unit every 10 weeks`
  - `1 unit every 12 weeks`

### End date
- **Type:** `date`

### First Delivery ETA
- **Type:** `rich_text`

### First Installment Date
- **Type:** `date`

### Installment Amount
- **Type:** `rollup`
- **Relation Property:** `Associated Deal`
- **Rollup Property:** `Monthly recurring revenue`
- **Function:** `show_original`

### Invoice Creation
- **Type:** `select`
- **Options:**
  - `checked`

### Last Installment Date
- **Type:** `date`

### Last Payment Date
- **Type:** `date`

### Last payment amount
- **Type:** `number`

### Monthly Reports
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-8101-81e1-c9f2d6803291`

### Monthly recurring revenue
- **Type:** `number`

### Monthly recurring revenue in company currency
- **Type:** `number`

### Name
- **Type:** `title`

### Net Payment Terms
- **Type:** `number`

### Next billing date
- **Type:** `date`

### Next payment amount
- **Type:** `number`

### Number of completed payments
- **Type:** `number`

### Number of expected payments
- **Type:** `number`

### Payment Enabled
- **Type:** `select`
- **Options:**
  - `false`

### Payment Processor
- **Type:** `select`
- **Options:**
  - `GoCardless`

### Payment method
- **Type:** `date`

### Payment source
- **Type:** `select`
- **Options:**
  - `Payment Link`
  - `Quote`
  - `Billing`

### Plan Size
- **Type:** `rollup`
- **Relation Property:** `Associated Deal`
- **Rollup Property:** `Deal Size`
- **Function:** `show_original`

### Processor
- **Type:** `select`
- **Options:**
  - `Stripe`
  - `None`

### Recipient billing city
- **Type:** `rich_text`

### Recipient billing country
- **Type:** `rich_text`

### Recipient billing country code
- **Type:** `rich_text`

### Recipient billing postal code
- **Type:** `number`

### Recipient billing state/region
- **Type:** `rich_text`

### Recipient billing street address
- **Type:** `rich_text`

### Recipient billing street address 2
- **Type:** `rich_text`

### Record ID
- **Type:** `number`

### Record source
- **Type:** `select`
- **Options:**
  - `Commerce Hub`
  - `Billing`

### Record source detail 1
- **Type:** `rich_text`

### Record source detail 2
- **Type:** `rich_text`

### Record source detail 3
- **Type:** `rich_text`

### Recurring billing frequency
- **Type:** `select`
- **Options:**
  - `Monthly`

### Related Subscriptions
- **Type:** `relation`
- **Related Database:** `228f4e0d-84e0-815c-a108-e48054988ac0`

### Related to Contacts (1) (Related to Subscriptions (Associated Contacts))
- **Type:** `relation`
- **Related Database:** `22bf4e0d-84e0-803f-98fe-f0a72401d33c`

### Related to Deals (Associated Subscriptions)
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-808c-af51-e09c154008db`

### Rollup
- **Type:** `rollup`
- **Relation Property:** `Related Subscriptions`
- **Rollup Property:** `Monthly Reports`
- **Function:** `show_original`

### Rollup 1
- **Type:** `rollup`
- **Relation Property:** `Related Subscriptions`
- **Rollup Property:** `Name`
- **Function:** `show_original`

### Start date
- **Type:** `date`

### Status
- **Type:** `select`
- **Options:**
  - `Active`
  - `Expired`
  - `Unpaid`
  - `Canceled`
  - `Paused`

### Store payment method at checkout
- **Type:** `rich_text`

### Subscription Status
- **Type:** `select`
- **Options:**
  - `Ended`
  - `Unresolved Failed Payment`

### Subscription modified on
- **Type:** `date`

### Tax ID
- **Type:** `select`
- **Options:**
  - `EE VAT EE102790519`

### To verify
- **Type:** `checkbox`

### Total Remaining Amount
- **Type:** `number`

### Total collected amount
- **Type:** `number`

### Upcoming Line Item
- **Type:** `rich_text`

### Upcoming Line Item IDs
- **Type:** `rich_text`

### Update payment method link
- **Type:** `rich_text`

## 🚫 Empty & Unused Properties

*Analysis based on 50 pages*

### Completely Empty Properties (27)
*These properties have no data in any page:*

- `Allowed payment methods` (rich_text)
- `Automatically email invoices` (select)
- `Churn date` (date)
- `Current Line Item` (select)
- `Current Line Item IDs` (number)
- `Invoice Creation` (select)
- `Net Payment Terms` (number)
- `Payment Enabled` (select)
- `Payment method` (date)
- `Recipient billing city` (rich_text)
- `Recipient billing country` (rich_text)
- `Recipient billing country code` (rich_text)
- `Recipient billing postal code` (number)
- `Recipient billing state/region` (rich_text)
- `Recipient billing street address` (rich_text)
- `Recipient billing street address 2` (rich_text)
- `Record source detail 1` (rich_text)
- `Record source detail 2` (rich_text)
- `Record source detail 3` (rich_text)
- `Recurring billing frequency` (select)
- `Related to Contacts (1) (Related to Subscriptions (Associated Contacts))` (relation)
- `Related to Deals (Associated Subscriptions)` (relation)
- `Store payment method at checkout` (rich_text)
- `Subscription modified on` (date)
- `Upcoming Line Item` (rich_text)
- `Upcoming Line Item IDs` (rich_text)
- `Update payment method link` (rich_text)

### Mostly Empty Properties (6)
*These properties have data in less than 5% of pages:*

- `First Delivery ETA` (rich_text) - 98.0% empty, only 1 pages with data
- `Associated Deal` (relation) - 98.0% empty, only 1 pages with data
- `Installment Amount` (rollup) - 98.0% empty, only 1 pages with data
- `Currency` (select) - 98.0% empty, only 1 pages with data
- `Plan Size` (rollup) - 98.0% empty, only 1 pages with data
- `Delivery Frequency` (select) - 98.0% empty, only 1 pages with data

## Related Databases

- **Associated Deal** (`226f4e0d-84e0-808c-af51-e09c154008db`)
- **Related to Contacts (1) (Related to Subscriptions (Associated Contacts))** (`22bf4e0d-84e0-803f-98fe-f0a72401d33c`)
- **Related to Deals (Associated Subscriptions)** (`226f4e0d-84e0-808c-af51-e09c154008db`)
- **Monthly Reports** (`226f4e0d-84e0-8101-81e1-c9f2d6803291`)
- **Associated Client** (`226f4e0d-84e0-814c-ad70-d478cebeee30`)
- **Related Subscriptions** (`228f4e0d-84e0-815c-a108-e48054988ac0`)

---

*Documentation generated on 2025-08-13 19:50:14*
