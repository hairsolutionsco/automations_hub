# Payments Database

**Database ID:** `22af4e0d-84e0-80c3-a7d6-f0209d93081d`

**Created:** 2025-07-08T18:13:00.000Z
**Last Modified:** 2025-08-13T19:15:00.000Z
**Total Properties:** 88

---

## Properties Overview

### checkbox (5)
- `Captured`
- `Disputed`
- `Livemode`
- `Paid`
- `Refunded`

### date (4)
- `Payment Date`
- `available_at`
- `created_at`
- `posted_at`

### email (1)
- `Client Email`

### formula (2)
- `Net Amount`
- `Total USD`

### number (8)
- `Amount captured`
- `Amount refunded`
- `Application fee amount`
- `Exchange Rate`
- `amount`
- `customer_facing_amount`
- `fees`
- `net`

### relation (6)
- `Associated Client`
- `Customer`
- `Monthly Reports`
- `Payouts`
- `Yearly Reports`
- `related_payout`

### rich_text (50)
- `Alternate statement descriptors`
- `Application`
- `Application fee`
- `Authorization code`
- `Available`
- `Billing details`
- `Calculated statement descriptor`
- `Connect reserved`
- `Destination`
- `Failure balance transaction`
- `Failure code`
- `Failure message`
- `Fraud details`
- `Instant available`
- `Invoice Number`
- `Issuing`
- `Level 3`
- `Metadata`
- `Object`
- `On behalf of`
- `Outcome`
- `Payment method details`
- `Pending`
- `Radar options`
- `Receipt email`
- `Receipt number`
- `Refunds`
- `Review`
- `Shipping`
- `Source`
- `Source transfer`
- `Statement descriptor suffix`
- `Stripe Record ID`
- `Transfer`
- `Transfer data`
- `Transfer group`
- `available_on`
- `balance_transaction_id`
- `card_country`
- `client_id`
- `customer_name`
- `description`
- `dispute_reason`
- `invoice_id`
- `invoice_number`
- `payment_intent_id`
- `payout_id`
- `payout_id (1)`
- `source_id`
- `subscription_id`

### rollup (1)
- `Rollup`

### select (10)
- `Income Type`
- `account_id`
- `account_name`
- `currency`
- `customer_facing_currency`
- `payment_method_type`
- `provider`
- `reporting_category`
- `statement_descriptor`
- `status`

### title (1)
- `payment_id`

---

## Detailed Property Documentation

### Alternate statement descriptors
- **Type:** `rich_text`

### Amount captured
- **Type:** `number`

### Amount refunded
- **Type:** `number`

### Application
- **Type:** `rich_text`

### Application fee
- **Type:** `rich_text`

### Application fee amount
- **Type:** `number`

### Associated Client
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-814c-ad70-d478cebeee30`

### Authorization code
- **Type:** `rich_text`

### Available
- **Type:** `rich_text`

### Billing details
- **Type:** `rich_text`

### Calculated statement descriptor
- **Type:** `rich_text`

### Captured
- **Type:** `checkbox`

### Client Email
- **Type:** `email`

### Connect reserved
- **Type:** `rich_text`

### Customer
- **Type:** `relation`
- **Related Database:** `238f4e0d-84e0-803b-aba6-ee2ffd6e0f1c`

### Destination
- **Type:** `rich_text`

### Disputed
- **Type:** `checkbox`

### Exchange Rate
- **Type:** `number`

### Failure balance transaction
- **Type:** `rich_text`

### Failure code
- **Type:** `rich_text`

### Failure message
- **Type:** `rich_text`

### Fraud details
- **Type:** `rich_text`

### Income Type
- **Type:** `select`
- **Options:**
  - `Retail income`
  - `Plan income`

### Instant available
- **Type:** `rich_text`

### Invoice Number
- **Type:** `rich_text`

### Issuing
- **Type:** `rich_text`

### Level 3
- **Type:** `rich_text`

### Livemode
- **Type:** `checkbox`

### Metadata
- **Type:** `rich_text`

### Monthly Reports
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-8101-81e1-c9f2d6803291`

### Net Amount
- **Type:** `formula`
- **Formula:** `subtract({{notion:block_property:GjA%3C:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}},{{notion:block_property:m%7CJJ:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}})`

### Object
- **Type:** `rich_text`

### On behalf of
- **Type:** `rich_text`

### Outcome
- **Type:** `rich_text`

### Paid
- **Type:** `checkbox`

### Payment Date
- **Type:** `date`

### Payment method details
- **Type:** `rich_text`

### Payouts
- **Type:** `relation`
- **Related Database:** `22af4e0d-84e0-803d-9f52-f0eb0e6d05fa`

### Pending
- **Type:** `rich_text`

### Radar options
- **Type:** `rich_text`

### Receipt email
- **Type:** `rich_text`

### Receipt number
- **Type:** `rich_text`

### Refunded
- **Type:** `checkbox`

### Refunds
- **Type:** `rich_text`

### Review
- **Type:** `rich_text`

### Rollup
- **Type:** `rollup`
- **Relation Property:** `Associated Client`
- **Rollup Property:** `Contact Profile`
- **Function:** `show_original`

### Shipping
- **Type:** `rich_text`

### Source
- **Type:** `rich_text`

### Source transfer
- **Type:** `rich_text`

### Statement descriptor suffix
- **Type:** `rich_text`

### Stripe Record ID
- **Type:** `rich_text`

### Total USD
- **Type:** `formula`
- **Formula:** `multiply({{notion:block_property:QQrJ:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}},{{notion:block_property:eEfT:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}})`

### Transfer
- **Type:** `rich_text`

### Transfer data
- **Type:** `rich_text`

### Transfer group
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

### amount
- **Type:** `number`

### available_at
- **Type:** `date`

### available_on
- **Type:** `rich_text`

### balance_transaction_id
- **Type:** `rich_text`

### card_country
- **Type:** `rich_text`

### client_id
- **Type:** `rich_text`

### created_at
- **Type:** `date`

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

### fees
- **Type:** `number`

### invoice_id
- **Type:** `rich_text`

### invoice_number
- **Type:** `rich_text`

### net
- **Type:** `number`

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

### payout_id (1)
- **Type:** `rich_text`

### posted_at
- **Type:** `date`

### provider
- **Type:** `select`
- **Options:**
  - `GoCardless`
  - `Stripe`

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
  - `succeeded`

### subscription_id
- **Type:** `rich_text`

## 🚫 Empty & Unused Properties

*Analysis based on 3234 pages*

### Completely Empty Properties (29)
*These properties have no data in any page:*

- `Alternate statement descriptors` (rich_text)
- `Application fee` (rich_text)
- `Authorization code` (rich_text)
- `Available` (rich_text)
- `Connect reserved` (rich_text)
- `Customer` (relation)
- `Destination` (rich_text)
- `Instant available` (rich_text)
- `Invoice Number` (rich_text)
- `Issuing` (rich_text)
- `Level 3` (rich_text)
- `On behalf of` (rich_text)
- `Payouts` (relation)
- `Pending` (rich_text)
- `Receipt email` (rich_text)
- `Receipt number` (rich_text)
- `Review` (rich_text)
- `Source` (rich_text)
- `Source transfer` (rich_text)
- `Statement descriptor suffix` (rich_text)
- `Transfer` (rich_text)
- `Transfer data` (rich_text)
- `Transfer group` (rich_text)
- `available_at` (date)
- `client_id` (rich_text)
- `created_at` (date)
- `net` (number)
- `payout_id (1)` (rich_text)
- `posted_at` (date)

### Mostly Empty Properties (8)
*These properties have data in less than 5% of pages:*

- `Failure balance transaction` (rich_text) - 100.0% empty, only 1 pages with data
- `Refunded` (checkbox) - 99.9% empty, only 2 pages with data
- `Disputed` (checkbox) - 99.4% empty, only 21 pages with data
- `dispute_reason` (rich_text) - 99.2% empty, only 25 pages with data
- `related_payout` (relation) - 98.6% empty, only 44 pages with data
- `Shipping` (rich_text) - 98.6% empty, only 44 pages with data
- `Failure code` (rich_text) - 98.6% empty, only 45 pages with data
- `Failure message` (rich_text) - 98.6% empty, only 46 pages with data

## Related Databases

- **Monthly Reports** (`226f4e0d-84e0-8101-81e1-c9f2d6803291`)
- **Customer** (`238f4e0d-84e0-803b-aba6-ee2ffd6e0f1c`)
- **Payouts** (`22af4e0d-84e0-803d-9f52-f0eb0e6d05fa`)
- **related_payout** (`22af4e0d-84e0-803d-9f52-f0eb0e6d05fa`)
- **Associated Client** (`226f4e0d-84e0-814c-ad70-d478cebeee30`)
- **Yearly Reports** (`226f4e0d-84e0-8179-98cb-cca8ecbf0c15`)

---

*Documentation generated on 2025-08-13 19:50:21*
