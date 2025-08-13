# Hair Orders Profiles Database

**Database ID:** `248f4e0d-84e0-80ad-9d33-e90e5124c092`

**Created:** 2025-08-07T22:01:00.000Z
**Last Modified:** 2025-08-13T19:15:00.000Z
**Total Properties:** 75

---

## Properties Overview

### date (4)
- `Last Activity Date`
- `Last Engagement Date`
- `Next Activity Date`
- `Recent Sales Email Replied Date`

### email (1)
- `Email`

### files (1)
- `Files & media`

### formula (2)
- `Formula`
- `Formula (1)`

### multi_select (3)
- `Contact Profile`
- `Hairline Details`
- `Shipping Profile`

### number (3)
- `Balance`
- `Hubspot Contacts Record ID`
- `Last PO Cost`

### phone_number (1)
- `Phone Number`

### relation (7)
- `Associated Contact`
- `Associated Deals`
- `Associated Orders`
- `Associated Payment`
- `Associated Plans`
- `Plan Pricing`
- `Tasks`

### rich_text (34)
- `AI summary`
- `Access Point Location`
- `Address`
- `Archive (Associated Companies)`
- `Base Material`
- `Base Size`
- `Cash balance`
- `City`
- `Client Number`
- `Currency`
- `Customization Extras`
- `Date of last meeting booked in meetings tool`
- `Density`
- `Hair Color`
- `Id`
- `Name Text`
- `Number of Associated Deals`
- `Object`
- `Order Email`
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
- `Ventilation Method`

### rollup (3)
- `Factory`
- `Last Order Date`
- `Rollup`

### select (14)
- `Country/Region`
- `Current Factory`
- `Hair Length`
- `Hairline Shape`
- `Lifecycle Stage`
- `Marketing contact status`
- `New Factory`
- `Order Email Text`
- `Order Type`
- `Payment Status`
- `Premade Compatibiity`
- `Premade Compatibility`
- `State/Region`
- `Wave/Curls`

### title (1)
- `Name`

### unique_id (1)
- `Notion Contacts Record ID`

---

## Detailed Property Documentation

### AI summary
- **Type:** `rich_text`

### Access Point Location
- **Type:** `rich_text`

### Address
- **Type:** `rich_text`

### Archive (Associated Companies)
- **Type:** `rich_text`

### Associated Contact
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-814c-ad70-d478cebeee30`

### Associated Deals
- **Type:** `relation`
- **Related Database:** `226f4e0d-84e0-808c-af51-e09c154008db`

### Associated Orders
- **Type:** `relation`
- **Related Database:** `228f4e0d-84e0-816f-8511-fab726d2c6ef`

### Associated Payment
- **Type:** `relation`
- **Related Database:** `22af4e0d-84e0-80c3-a7d6-f0209d93081d`

### Associated Plans
- **Type:** `relation`
- **Related Database:** `228f4e0d-84e0-815c-a108-e48054988ac0`

### Balance
- **Type:** `number`

### Base Material
- **Type:** `rich_text`

### Base Size
- **Type:** `rich_text`

### Cash balance
- **Type:** `rich_text`

### City
- **Type:** `rich_text`

### Client Number
- **Type:** `rich_text`

### Contact Profile
- **Type:** `multi_select`
- **Options:**
  - `Lead`
  - `Client`
  - `Indirect Client`

### Country/Region
- **Type:** `select`
- **Options:**
  - `Canada`
  - `United States`
  - `UK`
  - `Czech Republic`
  - `USA`
  - `Malta`
  - `Israel`
  - `Spain`
  - `United Kingdom`
  - `England`
  - `en-CA`
  - `en-US`

### Currency
- **Type:** `rich_text`

### Current Factory
- **Type:** `select`
- **Options:**
  - `Rare Hair`
  - `NewTimes Hair`

### Customization Extras
- **Type:** `rich_text`

### Date of last meeting booked in meetings tool
- **Type:** `rich_text`

### Density
- **Type:** `rich_text`

### Email
- **Type:** `email`

### Factory
- **Type:** `rollup`
- **Relation Property:** `Associated Orders`
- **Rollup Property:** `Factory`
- **Function:** `show_original`

### Files & media
- **Type:** `files`

### Formula
- **Type:** `formula`
- **Formula:** `"Hi Juno,\n\nHere's a new custom order:\n\n" +

"Client: " + {{notion:block_property:title:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}+ {{notion:block_property:q%3EYL:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} + "\n" +
"Order Type: Rush Custom Order\n\n" +

"Order details:\n" +
"Order Type: " + "\n" +
"Base Material: " + {{notion:block_property:%3A%3E%3AH:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} + "\n" +
"Base Size: " + {{notion:block_property:Cumb:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} + "\n" +
"Hair Color: " + {{notion:block_property:fHRP:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} + "\n" +
"Hairline Shape: " + {{notion:block_property:%60QYz:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} + "\n" +
"Hairline Details: " + {{notion:block_property:B%60UR:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} + "\n" +
"Density: " + {{notion:block_property:boVD:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} + "\n" +
"Venting: " + {{notion:block_property:J%5DEn:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} + "\n" +
"Wave/Curl: " + {{notion:block_property:NVwH:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} + "\n" +
"Hair Length: " + {{notion:block_property:BZUd:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} + "\n\n" +

"Additional Instructions:\n" +
"- Please trim any extra lace or poly material from the front hairline, leaving approximately 1/4\" of material only.\n" +
"- Once the order is finished, please respond to the order email with photos for approval.\n\n" +

"Shipment Instructions:\n" +
"1. This is a OneHead Hair Solutions order, please ship in a OneHead Hair Solutions branded bag.\n" +
"2. Please ship using your FedEx or UPS account and charge us for the cost.\n" +
"3. The labels and commercial invoice need to be anonymous with no mention of RareHair anywhere.\n" +
"4. The shipment needs to be sent " + {{notion:block_property:iCAL:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} + " with signature required.\n\n" +

"Customer's location for shipping quote:\n" +
"Country: " + {{notion:block_property:W%40Wa:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} + "\n" +
"City: " + {{notion:block_property:isr%5C:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} + "\n" +
"State/Prov: " + {{notion:block_property:%7Bh%7D%3B:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} + "\n" +
"Postcode: " + {{notion:block_property:EAqq:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} + "\n\n" +

"Please update the Supplier Portal with the following information:\n" +
"1. Production Start Date *important*.\n" +
"2. Order ETA *important*.\n" +
"3. Invoice No.\n" +
"4. Hair Unit Cost\n" +
"5. Extras Cost\n" +
"6. Shipping Cost\n" +
"7. Total Cost\n\n" +

"Let me know if you have any questions or issues with the order tracker sheet.\n\n" +
"Thank you very much for your great work.\n\n" +
"Vincent"`

### Formula (1)
- **Type:** `formula`
- **Formula:** `"Hi Juno,\n\nHere's a new premade order:\n\n" +

"Client: " + {{notion:block_property:title:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}+ " " + {{notion:block_property:q%3EYL:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} + "\n" +
"Order Type: Premade\n\n" +

"Order details:\n" +
"Base Material: " + {{notion:block_property:%3A%3E%3AH:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} + "\n" +
"Base Size: Cut to size using client's template "+ {{notion:block_property:Cumb:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} + "\n" +
"Hair Color: " + {{notion:block_property:fHRP:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} + "\n" +
"Hairline Shape: " + {{notion:block_property:%60QYz:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} + "\n" +
"Hairline Details: " + {{notion:block_property:B%60UR:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} + "\n" +
"Density: Medium-Light\n" +

"Additional Instructions:\n" +
"- Please trim any extra lace or poly material from the front hairline, leaving approximately 1/4\" of material only.\n" +

"Shipment Instructions:\n" +
"1. This is a OneHead Hair Solutions order, please ship in a OneHead Hair Solutions branded bag.\n" +
"2. Please ship using your FedEx or UPS account and charge us for the cost.\n" +
"3. The labels and commercial invoice need to be anonymous with no mention of RareHair anywhere.\n" +
"4. The shipment needs to be sent " + {{notion:block_property:iCAL:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} + " with signature required.\n\n" +

"Customer's address for immediate shipment:\n" +

"" + {{notion:block_property:title:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}}+ "\n" +
"" + {{notion:block_property:%5Bluw:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} + "\n" +
"" + {{notion:block_property:FzsM:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} + "\n" +
"" + {{notion:block_property:%7Bh%7D%3B:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} + " " +{{notion:block_property:W%40Wa:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} + "\n" +
"" + {{notion:block_property:EAqq:00000000-0000-0000-0000-000000000000:a8b539e5-0ae7-44fd-8c7b-e99ed0fa6921}} + "\n\n" +

"Please update the Supplier Portal with the following information:\n" +
"1. Production Start Date *important*.\n" +
"2. Order ETA *important*.\n" +
"3. Invoice No.\n" +
"4. Hair Unit Cost\n" +
"5. Extras Cost\n" +
"6. Shipping Cost\n" +
"7. Total Cost\n\n" +

"Let me know if you have any questions or issues with the order tracker sheet.\n\n" +
"Thank you very much for your great work.\n\n" +
"Vincent"`

### Hair Color
- **Type:** `rich_text`

### Hair Length
- **Type:** `select`
- **Options:**
  - `Standard 6" (standard)`
  - `5" additional (Total 11")`
  - `8" additional (Total 14")`
  - `4" (shorter)`
  - `11" additional (Total) 17"`
  - `6" additional (Total 12")`
  - `4" (Shorter than standard)`
  - `3" additional (Total 9")`
  - `4" additional (Total 10")`
  - `2" additional (Total 8")`

### Hairline Details
- **Type:** `multi_select`
- **Options:**
  **28 options** from `Realistic graduated density` to `(no bleaching) single knots.`

### Hairline Shape
- **Type:** `select`
- **Options:**
  - `As per template`
  - `CC Shape`
  - `AA Shape`
  - `A Shape`
  - `C Shape`

### Hubspot Contacts Record ID
- **Type:** `number`

### Id
- **Type:** `rich_text`

### Last Activity Date
- **Type:** `date`

### Last Engagement Date
- **Type:** `date`

### Last Order Date
- **Type:** `rollup`
- **Relation Property:** `Associated Orders`
- **Rollup Property:** `Order_Date`
- **Function:** `latest_date`

### Last PO Cost
- **Type:** `number`

### Lifecycle Stage
- **Type:** `select`
- **Options:**
  - `Customer`
  - `Subscriber`

### Marketing contact status
- **Type:** `select`
- **Options:**
  - `Non-marketing contact`
  - `Marketing contact`

### Name
- **Type:** `title`

### Name Text
- **Type:** `rich_text`

### New Factory
- **Type:** `select`
- **Options:**
  - `Rare Hair`
  - `NewTimes Hair`

### Next Activity Date
- **Type:** `date`

### Notion Contacts Record ID
- **Type:** `unique_id`

### Number of Associated Deals
- **Type:** `rich_text`

### Object
- **Type:** `rich_text`

### Order Email
- **Type:** `rich_text`

### Order Email Text
- **Type:** `select`
- **Options:**
  **295 options** from `<– BASE MATERIAL –> 

<– BASE SIZE –> 
<– TEMPLATE MEASUREMENTS –> 
  Template measurements

Full Length – L1 = 
Width Hairline – W1 = 
Width Center – W2 = 
Width 1/3 From Back – W3 = 

<– HAIR COLOR –> 

<– HAIR COLOR PER ZONES –> 
  Zone 1: 
  Zone 2: 
  Zone 3: 
  Zone 4: 
  Zone 5: 
  Zone 6: 
  Zone 7: 
  Zone 8: 

<– HAIR DENSITY –> 
  Zone 1: 
  Zone 2: 
  Zone 3: 
  Zone 4: 
  Zone 5: 
  Zone 6: 
  Zone 7: 
  Zone 8: 

<– HAIRLINE DETAILS –> 

<– HAIRLINE SHAPE –> 

<– WAVES/CURLS –> 

<– STYLE/VENTILATION –> 

<– HAIR LENGTH –>` to `<– BASE MATERIAL –> 

<– BASE SIZE –> 
<– TEMPLATE MEASUREMENTS –> 
  Template measurements

Full Length – L1 = 
Width Hairline – W1 = 
Width Center – W2 = 
Width 1/3 From Back – W3 = 

<– HAIR COLOR –> 1B30/1B40 TBC after he fits the first one from OneHead

<– HAIR COLOR PER ZONES –> 
  Zone 1: 
  Zone 2: 
  Zone 3: 
  Zone 4: 
  Zone 5: 
  Zone 6: 
  Zone 7: 
  Zone 8: 

<– HAIR DENSITY –> 
  Zone 1: 
  Zone 2: 
  Zone 3: 
  Zone 4: 
  Zone 5: 
  Zone 6: 
  Zone 7: 
  Zone 8: 

<– HAIRLINE DETAILS –> 

<– HAIRLINE SHAPE –> 

<– WAVES/CURLS –> 

<– STYLE/VENTILATION –> 

<– HAIR LENGTH –> `

### Order Type
- **Type:** `select`
- **Options:**
  - `Premade`
  - `Custom`

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
- **Relation Property:** `Associated Deals`
- **Rollup Property:** `Deal Name (Archive)`
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
  **25 options** from `Ontario` to `Quebec`

### Street Address
- **Type:** `rich_text`

### Street Address 2
- **Type:** `rich_text`

### Stripe Record ID
- **Type:** `rich_text`

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

### Template Photo
- **Type:** `rich_text`

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

## 🚫 Empty & Unused Properties

*Analysis based on 1806 pages*

### Completely Empty Properties (6)
*These properties have no data in any page:*

- `Associated Contact` (relation)
- `Files & media` (files)
- `Last Order Date` (rollup)
- `Next Activity Date` (date)
- `Sales Status` (rich_text)
- `Template Photo` (rich_text)

### Mostly Empty Properties (12)
*These properties have data in less than 5% of pages:*

- `Currency` (rich_text) - 99.9% empty, only 1 pages with data
- `Plan Pricing` (relation) - 99.9% empty, only 1 pages with data
- `Order Email` (rich_text) - 99.7% empty, only 5 pages with data
- `Access Point Location` (rich_text) - 99.7% empty, only 6 pages with data
- `Shipping` (rich_text) - 99.2% empty, only 14 pages with data
- `Date of last meeting booked in meetings tool` (rich_text) - 99.2% empty, only 14 pages with data
- `Tasks` (relation) - 98.3% empty, only 31 pages with data
- `Shipping Profile` (multi_select) - 98.0% empty, only 37 pages with data
- `Associated Plans` (relation) - 97.3% empty, only 48 pages with data
- `Street Address 2` (rich_text) - 96.9% empty, only 56 pages with data
- `Order Type` (select) - 96.9% empty, only 56 pages with data
- `Recent Sales Email Clicked Date` (rich_text) - 95.7% empty, only 78 pages with data

## Related Databases

- **Associated Payment** (`22af4e0d-84e0-80c3-a7d6-f0209d93081d`)
- **Associated Orders** (`228f4e0d-84e0-816f-8511-fab726d2c6ef`)
- **Associated Contact** (`226f4e0d-84e0-814c-ad70-d478cebeee30`)
- **Plan Pricing** (`239f4e0d-84e0-8017-b600-d74cfcaa3551`)
- **Associated Deals** (`226f4e0d-84e0-808c-af51-e09c154008db`)
- **Associated Plans** (`228f4e0d-84e0-815c-a108-e48054988ac0`)
- **Tasks** (`226f4e0d-84e0-8168-8718-d8f6b2d1fe3d`)

---

*Documentation generated on 2025-08-13 19:50:08*
