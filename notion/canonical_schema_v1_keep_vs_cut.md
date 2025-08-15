# Canonical Schema v1 — Keep vs Cut Checklist (by Database)

Use with the simplified task list. “Keep/Compute” = fields to retain or add (incl. formulas/rollups). “Cut/Delete” = remove after shadow period.

---

## Companies
- Keep/Compute
  - Company name (title), Record ID (number; HS mirror), Company Profile (select)
  - Email, Phone Number, Website URL
  - Street Address, City, State/Region, Postal Code, Country/Region
  - Time Zone (text; compute), Tax ID (text)
  - Associated Orders (relation), Associated POs (relation; ADD)
- Cut/Delete
  - Rich-text “Associated …” placeholders (replace with relations)
  - CRM analytics not used: # Sessions, # Pageviews, # Times contacted, # Deals, Lead Source, Original Traffic Source, Lifecycle Stage, Industry group
  - Social: Facebook, Instagram, Logo URL
  - Empty/vanity: Industry group, Lead Status, Next Activity Date, Salon Name

---

## Contacts
- Keep/Compute
  - Name (title), Email, Phone Number
  - Street Address, City, State/Region, Postal Code, Country/Region
  - Hubspot Contacts Record ID (number), Notion Contacts Record ID (unique_id)
  - Associated Deals, Associated Orders, Associated Plans, hs_hair_profile (relation)
  - Payment Status (select; compute via payments), Last Order Date (rollup)
- Cut/Delete
  - All hair spec fields (move to hs_hair_profile)
  - Unused/empty: Files & media, Next Activity Date, Sales Status, Template Photo (on Contact)
  - Email body formulas/blocks: Order Email, Order Email Text, operational formula clutter

---

## hs_hair_profile (Hair Orders Profiles → rename)
- Keep/Compute
  - Name (title), Associated Contact (relation 1:1), Order Type (select)
  - Base Material, Base Size, Hair Color, Hairline Shape (select), Hairline Details (multi_select)
  - Hair Length (select), Density, Ventilation Method, Premade Compatibility (select)
  - Associated Orders (relation)
  - is_premade_compatible (formula), f_spec_hash (formula), rl_last_order_date (rollup)
- Cut/Delete
  - CRM clones/marketing/email tracking artifacts; empty media, Next Activity Date, Sales Status, Template Photo (if empty)

---

## Deals
- Keep/Compute
  - Name (title), Hubspot Deals Record ID, Notion Deals Record ID
  - Deal Stage (select), Deal Type (select), Deal Size (select)
  - Currency (select), Amount (number), Exchange rate (number)
  - Amount (USD) (compute = Amount*rate), Payment Date (date)
  - Associated Client, Associated Orders, Associated Plan
- Cut/Delete
  - Empty/unused: Auto Total, Retail Price, Income, Income Status, Linked Subscriptions, Month, Qty, Next Activity Date, etc.

---

## Plans
- Keep/Compute
  - Name (title), Status (select), Start date, End date
  - Next billing date, Last Payment Date, Monthly recurring revenue
  - Payment Processor (select), Currency (select)
  - Associated Client, Associated Deal
  - Plan Size (rollup), Delivery Frequency (select)
  - f_units_per_cycle (formula), is_active (formula)
- Cut/Delete
  - 27+ empty/unused props: Allowed payment methods, Automatically email invoices, contact address mirrors, etc.

---

## Orders
- Keep/Compute
  - Order Number (title), Notion Orders Record ID (unique_id)
  - Associated Deal, Client (Contact), Related Hair Profile, Associated PO
  - Order_Date, Order_ETA, Shipped Date, Order Status (select), Order Speed (select), Factory (select)
  - Tracking Number (text; TYPE FIX), Shipping Carrier (rename from “Shipping Courrier”)
  - Payment Date (rollup from payments), rl_cogs_usd (rollup from POs), f_margin_usd (formula), is_late (formula)
- Cut/Delete
  - Move Factory Invoice No → POs
  - Duplicate/derived date formulas (Order ETAs, Production Start Date formula)
  - Rarely used internals (Index) and <5% filled variants

---

## Purchase Orders
- Keep/Compute
  - PO Number (title), Notion Orders Record ID (unique_id)
  - Associated Order, Associated Deal (optional), Client (optional), Associated Companies (Supplier)
  - Order_Date, Production Start Date, Order ETA, Shipped Date
  - Payment Due, Payment Date, Payment Status (select)
  - Hair Unit Cost, Extras Cost, Shipment Cost, Total Cost (formula = sum)
  - Tracking Number (text; TYPE FIX), Shipping Carrier (rename), Inventory Product (relation)
- Cut/Delete
  - Duplicate/unused Inventory Products relation, Text scratch fields
  - Unused rollups (Density, Cost per Unit) unless Inventory is wired
  - Order Profile multi-select (redundant)

---

## hs_payments (Incomes → rename)
- Keep/Compute
  - Name (title), Payment Date (date), Amount (number)
  - Currency (select), Exchange Rate (number), Net USD (formula)
  - Processor (select: Stripe/GC/Shopify)
  - Related Deal (0..1), Related Order (0..1), Related Plan (0..1), Contact (1)
- Cut/Delete
  - Replace “Income”/“Order Income” formulas with proper relations + rollups

---

## Expenses
- Keep/Compute
  - Name (title), Date (date)
  - Currency (select), Total Amount (number), Exchange Rate (number), Total USD (formula)
  - Fee (number), Type (select)
  - Categories (relation), Month (relation)
  - ID (text), Payer (text)
- Cut/Delete
  - Empty relations: Platform, Projects, Restock Connection
  - Product rollup, Archive, other empty/unused props
