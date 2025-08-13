# Contacts Database

**Database ID:** `226f4e0d-84e0-814c-ad70-d478cebeee30`

**Created:** 2024-08-13T18:04:00.000Z
**Last Modified:** 2025-01-06T23:18:00.000Z
**Total Properties:** 141

---

## Properties Overview

### checkbox (3)
- `Automated Response Sent`
- `Consultation Email Sent`
- `Product Picked Up`

### date (5)
- `Confirmation Paid Date`
- `First Hair Order Paid Date`
- `Last Active`
- `Recent Sales Email Replied Date`
- `Zip Code`

### email (1)
- `Email`

### files (1)
- `Order PDF Linked`

### formula (3)
- `CRM Name`
- `Order Details`
- `Order Status`

### multi_select (3)
- `Email Groups`
- `Hair Characteristics`
- `Shipping Profile`

### number (2)
- `In Touch Sequence`
- `Lead Score`

### phone_number (1)
- `Phone Number`

### relation (6)
- `Companies`
- `Deals`
- `Hair Orders`
- `Plan Pricing`
- `Tasks`
- `Units`

### rich_text (34)
- `Additional Notes`
- `Base Material`
- `Birthday`
- `City`
- `Color Description`
- `Color Groups`
- `Country`
- `Customer Portal User ID`
- `Density`
- `Hair Color`
- `Hair Density Per Zones`
- `Hair Length`
- `Hairline Shape`
- `Hubspot Record ID`
- `Lead Source`
- `Monthly Rebill Amount`
- `Order Quantity`
- `Original Order Quantity`
- `Postal Code`
- `Re-Engagement Notes`
- `Recent Sales Email Clicked Date`
- `Recent Sales Email Opened Date`
- `Sales Status`
- `Shipping`
- `Street Address`
- `Street Address 2`
- `Stripe Record ID`
- `Subscriptions`
- `Tax`
- `Tax exempt`
- `Tax ids`
- `Template Photo`
- `Unit Sales`
- `Ventilation Method`
- `Website`

### rollup (2)
- `Rollup`
- `Template Based On`

### select (22)
- `Assignment Group`
- `Base Size`
- `Contact Status`
- `Contact Type`
- `Contact Work Status`
- `Email Status`
- `Hair Product Category`
- `Hairline Details`
- `Lifetime Value`
- `Notes`
- `Order Priority`
- `Order Type`
- `Payment Status`
- `Premade Compatibiity`
- `Premade Compatibility`
- `State/Region`
- `Style/Ventilation`
- `Template Creation Status`
- `Unit`
- `Unit and Hair System ID`
- `Unit ID`
- `Wave/Curls`

### title (1)
- `Name`

### url (1)
- `Hubspot Link`

---

## Detailed Property Documentation

### Additional Notes
- **Type:** `rich_text`

### Assignment Group
- **Type:** `select`
- **Options:**
  - `Processing and Production`
  - `Sales`
  - `Quality control`
  - `Shipping`
  - `New Business`
  - `Re-order`
  - `Retention`

### Automated Response Sent
- **Type:** `checkbox`

### Base Material
- **Type:** `rich_text`

### Base Size
- **Type:** `select`
- **Options:**
  - `Template`
  - `Measurements`
  - `Template, Measurements`

### Birthday
- **Type:** `rich_text`

### CRM Name
- **Type:** `formula`
- **Formula:** `prop("Name") + " (" + prop("Email") + ")"`

### City
- **Type:** `rich_text`

### Color Description
- **Type:** `rich_text`

### Color Groups
- **Type:** `rich_text`

### Companies
- **Type:** `relation`
- **Related Database:** `22bf4e0d-84e0-80bb-8d1c-c90710d44870`

### Confirmation Paid Date
- **Type:** `date`

### Consultation Email Sent
- **Type:** `checkbox`

### Contact Status
- **Type:** `select`
- **Options:**
  - `New Lead`
  - `Consulted`
  - `Qualified`
  - `Customer`
  - `Lost`
  - `Unqualified`

### Contact Type
- **Type:** `select`
- **Options:**
  - `Contact`
  - `Customer`
  - `Lead`

### Contact Work Status
- **Type:** `select`
- **Options:**
  - `In Touch Sequence`
  - `To Call`
  - `To Text`
  - `To Email`
  - `Called - no answer`
  - `Called - voicemail left`
  - `Texted`
  - `Emailed`
  - `Responded`
  - `Qualified`
  - `Customer`
  - `Lost`
  - `Unqualified`

### Country
- **Type:** `rich_text`

### Customer Portal User ID
- **Type:** `rich_text`

### Deals
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-808c-af51-e09c154008db`

### Density
- **Type:** `rich_text`

### Email
- **Type:** `email`

### Email Groups
- **Type:** `multi_select`
- **Options:**
  - `Cancelled`
  - `customer`
  - `Shipped Orders`
  - `New Leads`
  - `Re-order`
  - `Consultation Booked`
  - `Post order 3 days`
  - `Premade`
  - `Intro sequence`
  - `Order Delivery Updates`
  - `Order Updates`
  - `5 Days no response`
  - `Templates`
  - `Monthly Rebills`
  - `Lead Nurture`
  - `All Customers`
  - `All Contacts`
  - `Old Leads`
  - `Order Updates/Tracking`
  - `Deals won`
  - `All Prospects`

### Email Status
- **Type:** `select`
- **Options:**
  - `Active`
  - `Unsubscribed`
  - `Bounced`
  - `Suppressed`

### First Hair Order Paid Date
- **Type:** `date`

### Hair Characteristics
- **Type:** `multi_select`
- **Options:**
  - `Straight`
  - `Wavy`
  - `Curly`
  - `Thick`
  - `Medium`
  - `Thin`
  - `Natural Part`
  - `Side Part`
  - `Center Part`
  - `Widow's Peak`
  - `High Forehead`
  - `Receding Hairline`
  - `Male Pattern Baldness`
  - `Female Pattern Hair Loss`
  - `Alopecia`
  - `Gray Hair`
  - `White Hair`
  - `Blonde`
  - `Brown`
  - `Black`
  - `Red`
  - `Auburn`
  - `Sensitive Scalp`
  - `Oily Scalp`
  - `Dry Scalp`
  - `Previous Hair System User`
  - `First Time User`
  - `Full Coverage Needed`
  - `Partial Coverage Needed`
  - `Frontal Coverage`
  - `Crown Coverage`
  - `Temples Coverage`

### Hair Color
- **Type:** `rich_text`

### Hair Density Per Zones
- **Type:** `rich_text`

### Hair Length
- **Type:** `rich_text`

### Hair Orders
- **Type:** `relation`
- **Related Database:** `248f4e0d-84e0-80ad-9d33-e90e5124c092`

### Hair Product Category
- **Type:** `select`
- **Options:**
  - `Hair System`
  - `Tape`
  - `Glue`
  - `Shampoo`
  - `Conditioner`
  - `Styling Products`
  - `Tools`
  - `Accessories`
  - `Maintenance Kit`
  - `Removal Products`
  - `Scalp Care`
  - `Hair Care`
  - `Application Tools`
  - `Cleaning Products`
  - `Protective Products`

### Hairline Details
- **Type:** `select`
- **Options:**
  - `Realistic graduated density`
  - `Bleached single knots`
  - `Trim excess material`
  - `Dye-after process`
  - `Single knots`
  - `non-graduated`
  - `Graduated`
  - `*Not graduated* hairline`

### Hairline Shape
- **Type:** `rich_text`

### Hubspot Link
- **Type:** `url`

### Hubspot Record ID
- **Type:** `rich_text`

### In Touch Sequence
- **Type:** `number`

### Last Active
- **Type:** `date`

### Lead Score
- **Type:** `number`

### Lead Source
- **Type:** `rich_text`

### Lifetime Value
- **Type:** `select`
- **Options:**
  - `$0 - $999`
  - `$1,000 - $2,499`
  - `$2,500 - $4,999`
  - `$5,000 - $9,999`
  - `$10,000+`

### Monthly Rebill Amount
- **Type:** `rich_text`

### Name
- **Type:** `title`

### Notes
- **Type:** `select`
- **Options:**
  - `Custom Color Hair`
  - `Light color hair system - special handling required`

### Order Details
- **Type:** `formula`
- **Formula:** `if(prop("Hair Orders"), join(prop("Hair Orders").map(current.prop("Detailed Order Specification")), "\n\n---\n\n"), "No orders")`

### Order PDF Linked
- **Type:** `files`

### Order Priority
- **Type:** `select`
- **Options:**
  - `High`
  - `Medium`
  - `Low`
  - `Rush`

### Order Quantity
- **Type:** `rich_text`

### Order Status
- **Type:** `formula`
- **Formula:** `if(prop("Hair Orders"), join(prop("Hair Orders").map(current.prop("Order Status")), ", "), "No orders")`

### Order Type
- **Type:** `select`
- **Options:** `Custom`

### Original Order Quantity
- **Type:** `rich_text`

### Payment Status
- **Type:** `select`
- **Options:**
  - `Order Paid-in-full`
  - `Subscription Ended`
  - `Down Payment Paid`
  - `Subscription Active`

### Phone Number
- **Type:** `phone_number`

### Plan Pricing
- **Type:** `relation`
- **Related Database:** `239f4e0d-84e0-8017-b600-d74cfcaa3551`

### Postal Code
- **Type:** `rich_text`

### Premade Compatibiity
- **Type:** `select`
- **Options:**
  - `Yes `
  - `No`
  - `Maybe`

### Premade Compatibility
- **Type:** `select`
- **Options:**
  - `Standard Color`
  - `Custom Color`
  - `Special Color`

### Product Picked Up
- **Type:** `checkbox`

### Re-Engagement Notes
- **Type:** `rich_text`

### Recent Sales Email Clicked Date
- **Type:** `rich_text`

### Recent Sales Email Opened Date
- **Type:** `rich_text`

### Recent Sales Email Replied Date
- **Type:** `date`

### Rollup
- **Type:** `rollup`
- **Relation Property:** `Hair Orders`
- **Rollup Property:** `Template Based On`
- **Function:** `show_original`

### Sales Status
- **Type:** `rich_text`

### Shipping
- **Type:** `rich_text`

### Shipping Profile
- **Type:** `multi_select`
- **Options:**
  - `No signature is required`

### State/Region
- **Type:** `select`
- **Options:**
  - `Ontario`
  - `California`
  - `British Columbia`
  - `None`
  - `New York`
  - `Illinois`
  - `Prague`
  - `FL`
  - `Washington`
  - `Michigan`
  - `CA`
  - `TX`
  - `Yukon`
  - `Arizona`
  - `Kent`
  - `Pennsylvania`
  - `Alabama`
  - `England`
  - `MO`
  - `London`
  - `Colorado`
  - `BC`
  - `Maryland`
  - `Tennessee`
  - `Quebec`

### Street Address
- **Type:** `rich_text`

### Street Address 2
- **Type:** `rich_text`

### Stripe Record ID
- **Type:** `rich_text`

### Style/Ventilation
- **Type:** `select`
- **Options:**
  - `Freestyle`
  - `Flat effect from crown to sides`
  - `Left parting`
  - `Brushed back`
  - `No crown *important*`
  - `Right crown`
  - `Flat forward`
  - `Brushed back`

### Subscriptions
- **Type:** `rich_text`

### Tasks
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-8168-8718-d8f6b2d1fe3d`

### Tax
- **Type:** `rich_text`

### Tax exempt
- **Type:** `rich_text`

### Tax ids
- **Type:** `rich_text`

### Template Based On
- **Type:** `rollup`
- **Relation Property:** `Hair Orders`
- **Rollup Property:** `Template Based On`
- **Function:** `show_original`

### Template Creation Status
- **Type:** `select`
- **Options:**
  - `Template Received`
  - `Template Created`
  - `No Template Needed`
  - `Template Requested`

### Template Photo
- **Type:** `rich_text`

### Unit
- **Type:** `select`
- **Options:** 100 unit IDs from `HSC #001-01` to `HSC #001-100`

### Unit Sales
- **Type:** `rich_text`

### Unit and Hair System ID
- **Type:** `select`
- **Options:** 100 unit IDs from `HSC #001-01` to `HSC #001-100`

### Unit ID
- **Type:** `select`
- **Options:** 100 unit IDs from `HSC #001-01` to `HSC #001-100`

### Units
- **Type:** `relation`
- **Related Database:** `239f4e0d-84e0-8017-b600-d74cfcaa3551`

### Ventilation Method
- **Type:** `rich_text`

### Wave/Curls
- **Type:** `select`
- **Options:**
  - `Standard 3.6 cm (straight/body wave)`
  - `3.0 cm curl`
  - `2.4 cm curl (Z1)`
  - `2.6 cm curl (Z2`
  - `Z3) 2.8 cm curl (Z4-Z8)`
  - `3.2 cm curl`
  - `Straight hair`
  - `no curl`
  - `0.6 cm curl (afro)`
  - `1.8 cm curl`
  - `2.5 cm curl`
  - `No wave`
  - `straight`
  - `1.5 cm curl`
  - `0.8 cm curl`
  - `2.8 cm curl`
  - `2.2 cm curl`
  - `2.0 cm curl`
  - `3.4 cm curl`

### Website
- **Type:** `rich_text`

### Zip Code
- **Type:** `date`

---

## Usage Notes

This is the central customer database for Hair Solutions Co., containing detailed customer contact information, order history, and hair system specifications. It integrates with multiple other databases including Companies, Deals, Hair Orders, and Tasks.

## Related Databases

- **Companies** (`22bf4e0d-84e0-80bb-8d1c-c90710d44870`) - Company information for B2B contacts
- **Deals** (`226f4e0d-84e0-808c-af51-e09c154008db`) - Sales opportunities and deals
- **Hair Orders** (`248f4e0d-84e0-80ad-9d33-e90e5124c092`) - Detailed order specifications and history
- **Plan Pricing** (`239f4e0d-84e0-8017-b600-d74cfcaa3551`) - Pricing plans and unit information
- **Tasks** (`226f4e0d-84e0-8168-8718-d8f6b2d1fe3d`) - Task management related to contacts
