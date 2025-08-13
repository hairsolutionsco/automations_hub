# Forecasted Payments Database

**Database ID:** `22cf4e0d-84e0-802a-bf76-e564658fdc5f`

**Created:** 2025-07-10T03:07:00.000Z
**Last Modified:** 2025-08-13T19:15:00.000Z
**Total Properties:** 104

---

## Properties Overview

### checkbox (1)
- `To verify`

### date (5)
- `First Installment Date`
- `Last Installment Date`
- `Last Payment Date`
- `Next billing date`
- `Payment Date`

### email (2)
- `Client Email`
- `Contact email`

### formula (2)
- `Net Amount`
- `Total USD`

### number (15)
- `Annual recurring revenue`
- `Annual recurring revenue in company currency`
- `Exchange Rate`
- `Fee`
- `Gross Amount`
- `Last payment amount`
- `Monthly recurring revenue`
- `Monthly recurring revenue in company currency`
- `Next payment amount`
- `Number of completed payments`
- `Number of expected payments`
- `Record ID`
- `Total Remaining Amount`
- `Total collected amount`
- `customer_facing_amount`

### people (1)
- `Associated Client 1`

### relation (5)
- `Daily Reports`
- `Monthly Reports`
- `Payouts`
- `Yearly Reports`
- `related_payout`

### rich_text (56)
- `Allowed payment methods`
- `Associated Companies`
- `Associated Contacts`
- `Associated Invoices`
- `Associated Payments`
- `Automatically email invoices`
- `Churn date`
- `Current Line Item`
- `Current Line Item IDs`
- `Invoice Creation`
- `Monthly Reports 1`
- `Monthly Reports 2`
- `Name`
- `Net Payment Terms`
- `Payment Enabled`
- `Payment ID`
- `Payment Processor`
- `Payment method`
- `Recipient billing city`
- `Recipient billing country`
- `Recipient billing country code`
- `Recipient billing postal code`
- `Recipient billing state/region`
- `Recipient billing street address`
- `Recipient billing street address 2`
- `Record source detail 1`
- `Record source detail 2`
- `Record source detail 3`
- `Recurring billing frequency`
- `Related Subscriptions`
- `Related to Contacts (1) (Related to Subscriptions (Associated Contacts))`
- `Related to Customers (Associated Subscriptions)`
- `Related to Deals (Associated Subscriptions)`
- `Related to Invoice Services (Subscriptions)`
- `Related to Payments (Associated Subscriptions)`
- `Rollup 1`
- `Rollup 1 1`
- `Rollup 2`
- `Store payment method at checkout`
- `Subscription modified on`
- `Tax ID`
- `Upcoming Line Item`
- `Upcoming Line Item IDs`
- `Update payment method link`
- `available_on`
- `balance_transaction_id`
- `card_country`
- `customer_name`
- `description`
- `dispute_reason`
- `invoice_id`
- `invoice_number`
- `payment_intent_id`
- `payout_id`
- `source_id`
- `subscription_id`

### select (16)
- `Collection process`
- `Currency code`
- `Income Type`
- `Payment Platorm`
- `Payment source`
- `Processor`
- `Record source`
- `Subscription Status`
- `account_id`
- `account_name`
- `currency`
- `customer_facing_currency`
- `payment_method_type`
- `reporting_category`
- `statement_descriptor`
- `status`

### title (1)
- `payment_id`

---

## Detailed Property Documentation

### Allowed payment methods
- **Type:** `rich_text`

### Annual recurring revenue
- **Type:** `number`

### Annual recurring revenue in company currency
- **Type:** `number`

### Associated Client 1
- **Type:** `people`

### Associated Companies
- **Type:** `rich_text`

### Associated Contacts
- **Type:** `rich_text`

### Associated Invoices
- **Type:** `rich_text`

### Associated Payments
- **Type:** `rich_text`

### Automatically email invoices
- **Type:** `rich_text`

### Churn date
- **Type:** `rich_text`

### Client Email
- **Type:** `email`

### Collection process
- **Type:** `select`
- **Options:**
  - `Automatic payments`
  - `Manual payments`

### Contact email
- **Type:** `email`

### Currency code
- **Type:** `select`
- **Options:**
  - `USD`
  - `GBP`
  - `CAD`
  - `EUR`

### Current Line Item
- **Type:** `rich_text`

### Current Line Item IDs
- **Type:** `rich_text`

### Daily Reports
- **Type:** `relation`
- **Related Database:** `22cf4e0d-84e0-8036-a313-f6cfa1fa9801`

### Exchange Rate
- **Type:** `number`

### Fee
- **Type:** `number`

### First Installment Date
- **Type:** `date`

### Gross Amount
- **Type:** `number`

### Income Type
- **Type:** `select`
- **Options:**
  - `Retail income`
  - `Plan income`

### Invoice Creation
- **Type:** `rich_text`

### Last Installment Date
- **Type:** `date`

### Last Payment Date
- **Type:** `date`

### Last payment amount
- **Type:** `number`

### Monthly Reports
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-8101-81e1-c9f2d6803291`

### Monthly Reports 1
- **Type:** `rich_text`

### Monthly Reports 2
- **Type:** `rich_text`

### Monthly recurring revenue
- **Type:** `number`

### Monthly recurring revenue in company currency
- **Type:** `number`

### Name
- **Type:** `rich_text`

### Net Amount
- **Type:** `formula`
- **Formula:** `subtract({{notion:block_property:GjA%3C:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}},{{notion:block_property:m%7CJJ:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}})`

### Net Payment Terms
- **Type:** `rich_text`

### Next billing date
- **Type:** `date`

### Next payment amount
- **Type:** `number`

### Number of completed payments
- **Type:** `number`

### Number of expected payments
- **Type:** `number`

### Payment Date
- **Type:** `date`

### Payment Enabled
- **Type:** `rich_text`

### Payment ID
- **Type:** `rich_text`

### Payment Platorm
- **Type:** `select`
- **Options:**
  - `GoCardless`
  - `Stripe`

### Payment Processor
- **Type:** `rich_text`

### Payment method
- **Type:** `rich_text`

### Payment source
- **Type:** `select`
- **Options:**
  - `Payment Link`
  - `Billing`
  - `Quote`

### Payouts
- **Type:** `relation`
- **Related Database:** `22af4e0d-84e0-803d-9f52-f0eb0e6d05fa`

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
- **Type:** `rich_text`

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
- **Type:** `rich_text`

### Related Subscriptions
- **Type:** `rich_text`

### Related to Contacts (1) (Related to Subscriptions (Associated Contacts))
- **Type:** `rich_text`

### Related to Customers (Associated Subscriptions)
- **Type:** `rich_text`

### Related to Deals (Associated Subscriptions)
- **Type:** `rich_text`

### Related to Invoice Services (Subscriptions)
- **Type:** `rich_text`

### Related to Payments (Associated Subscriptions)
- **Type:** `rich_text`

### Rollup 1
- **Type:** `rich_text`

### Rollup 1 1
- **Type:** `rich_text`

### Rollup 2
- **Type:** `rich_text`

### Store payment method at checkout
- **Type:** `rich_text`

### Subscription Status
- **Type:** `select`
- **Options:**
  - `Ended`
  - `Unresolved Failed Payment`

### Subscription modified on
- **Type:** `rich_text`

### Tax ID
- **Type:** `rich_text`

### To verify
- **Type:** `checkbox`

### Total Remaining Amount
- **Type:** `number`

### Total USD
- **Type:** `formula`
- **Formula:** `multiply({{notion:block_property:QQrJ:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}},{{notion:block_property:eEfT:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}})`

### Total collected amount
- **Type:** `number`

### Upcoming Line Item
- **Type:** `rich_text`

### Upcoming Line Item IDs
- **Type:** `rich_text`

### Update payment method link
- **Type:** `rich_text`

### Yearly Reports
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-8179-98cb-cca8ecbf0c15`

### account_id
- **Type:** `select`
- **Options:**
  - `acct_1Ftj4lIujH16tQT0`
  - `acct_1QHt3vB4LTFfNure`

### account_name
- **Type:** `select`
- **Options:**
  - `OneHead Europe`
  - `HAIR SOLUTIONS CO OÜ`

### available_on
- **Type:** `rich_text`

### balance_transaction_id
- **Type:** `rich_text`

### card_country
- **Type:** `rich_text`

### currency
- **Type:** `select`
- **Options:**
  - `usd`
  - `eur`
  - `gbp`
  - `cad`
  - `AUD`

### customer_facing_amount
- **Type:** `number`

### customer_facing_currency
- **Type:** `select`
- **Options:**
  - `usd`
  - `cad`
  - `eur`
  - `gbp`
  - `aud`

### customer_name
- **Type:** `rich_text`

### description
- **Type:** `rich_text`

### dispute_reason
- **Type:** `rich_text`

### invoice_id
- **Type:** `rich_text`

### invoice_number
- **Type:** `rich_text`

### payment_id
- **Type:** `title`

### payment_intent_id
- **Type:** `rich_text`

### payment_method_type
- **Type:** `select`
- **Options:**
  - `card`
  - `link`
  - `sepa_debit`

### payout_id
- **Type:** `rich_text`

### related_payout
- **Type:** `relation`
- **Related Database:** `22af4e0d-84e0-803d-9f52-f0eb0e6d05fa`

### reporting_category
- **Type:** `select`
- **Options:**
  - `charge`
  - `refund`
  - `dispute`

### source_id
- **Type:** `rich_text`

### statement_descriptor
- **Type:** `select`
- **Options:**
  - `ONEHEAD HAIR SOLUTIONS`

### status
- **Type:** `select`
- **Options:**
  - `paid_out`
  - `failed`
  - `cancelled`
  - `submitted`
  - `Expired`
  - `Canceled`
  - `Active`
  - `Unpaid`
  - `Paused`

### subscription_id
- **Type:** `rich_text`

## 🚫 Empty & Unused Properties

*Analysis based on 193 pages*

### Completely Empty Properties (65)
*These properties have no data in any page:*

- `Allowed payment methods` (rich_text)
- `Associated Client 1` (people)
- `Associated Companies` (rich_text)
- `Associated Invoices` (rich_text)
- `Associated Payments` (rich_text)
- `Automatically email invoices` (rich_text)
- `Churn date` (rich_text)
- `Client Email` (email)
- `Current Line Item` (rich_text)
- `Current Line Item IDs` (rich_text)
- `Exchange Rate` (number)
- `Fee` (number)
- `Gross Amount` (number)
- `Income Type` (select)
- `Invoice Creation` (rich_text)
- `Monthly Reports 1` (rich_text)
- `Net Payment Terms` (rich_text)
- `Payment Enabled` (rich_text)
- `Payment Platorm` (select)
- `Payment method` (rich_text)
- `Payouts` (relation)
- `Recipient billing city` (rich_text)
- `Recipient billing country` (rich_text)
- `Recipient billing country code` (rich_text)
- `Recipient billing postal code` (rich_text)
- `Recipient billing state/region` (rich_text)
- `Recipient billing street address` (rich_text)
- `Recipient billing street address 2` (rich_text)
- `Record source detail 1` (rich_text)
- `Record source detail 2` (rich_text)
- `Record source detail 3` (rich_text)
- `Recurring billing frequency` (rich_text)
- `Related to Contacts (1) (Related to Subscriptions (Associated Contacts))` (rich_text)
- `Related to Customers (Associated Subscriptions)` (rich_text)
- `Related to Deals (Associated Subscriptions)` (rich_text)
- `Related to Invoice Services (Subscriptions)` (rich_text)
- `Related to Payments (Associated Subscriptions)` (rich_text)
- `Rollup 1 1` (rich_text)
- `Store payment method at checkout` (rich_text)
- `Subscription modified on` (rich_text)
- `Upcoming Line Item` (rich_text)
- `Upcoming Line Item IDs` (rich_text)
- `Update payment method link` (rich_text)
- `account_id` (select)
- `account_name` (select)
- `available_on` (rich_text)
- `balance_transaction_id` (rich_text)
- `card_country` (rich_text)
- `currency` (select)
- `customer_facing_amount` (number)
- `customer_facing_currency` (select)
- `customer_name` (rich_text)
- `description` (rich_text)
- `dispute_reason` (rich_text)
- `invoice_id` (rich_text)
- `invoice_number` (rich_text)
- `payment_id` (title)
- `payment_intent_id` (rich_text)
- `payment_method_type` (select)
- `payout_id` (rich_text)
- `related_payout` (relation)
- `reporting_category` (select)
- `source_id` (rich_text)
- `statement_descriptor` (select)
- `subscription_id` (rich_text)

### Mostly Empty Properties (3)
*These properties have data in less than 5% of pages:*

- `Rollup 2` (rich_text) - 98.4% empty, only 3 pages with data
- `Rollup 1` (rich_text) - 98.4% empty, only 3 pages with data
- `Related Subscriptions` (rich_text) - 98.4% empty, only 3 pages with data

## Related Databases

- **Daily Reports** (`22cf4e0d-84e0-8036-a313-f6cfa1fa9801`)
- **Monthly Reports** (`226f4e0d-84e0-8101-81e1-c9f2d6803291`)
- **Payouts** (`22af4e0d-84e0-803d-9f52-f0eb0e6d05fa`)
- **related_payout** (`22af4e0d-84e0-803d-9f52-f0eb0e6d05fa`)
- **Yearly Reports** (`226f4e0d-84e0-8179-98cb-cca8ecbf0c15`)

---

*Documentation generated on 2025-08-13 19:50:28*
