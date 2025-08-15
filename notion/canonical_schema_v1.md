Here is v1 of the canonical, automation‑ready schema and cut plan. Questions first, then full deliverables.

## Pre‑flight: 5 targeted questions

1. Confirm canonical hair spec home = **Hair Orders Profiles** (rename → `hs_hair_profile`). Then delete duplicate hair fields from **Contacts**. &#x20;
2. Confirm **Companies** includes both Suppliers and B2B Clients via `Company Profile` values. If a separate Suppliers DB exists, specify; otherwise we’ll filter Companies by profile.&#x20;
3. Confirm **Incomes** is the payments ledger. If yes, we will rename to `hs_payments`, add relations to Deal/Order/Plan/Contact, and compute USD net.&#x20;
4. Approve aligning **Order** status set to ops SLA: `planned → submitted → awaiting_payment → in_production → qc_failed/qc_passed → awaiting_ship → shipped → shipping_issue → delivered/cancelled`, replacing current mixed labels.&#x20;
5. Approve unifying **Factory** options and carrier/tracking types; e.g., `RareHair` vs `Rare Hair`, `Tracking Number` to text. &#x20;

Assumptions used below if not answered now: A1 yes to all five.

---

## 1) Database Inventory

*Data from your current Notion DBs; “Current” = total properties now.*

| Database                                     | Purpose                                   | Current Prop Ct | Target Ct | Key Identifiers                                                           | Key Relations                                           |
| -------------------------------------------- | ----------------------------------------- | --------------: | --------: | ------------------------------------------------------------------------- | ------------------------------------------------------- |
| Companies                                    | B2B clients + suppliers registry          |             50  |        14 | `Company name` (title), `Record ID` (HubSpot mirror)                      | ↔ Orders, ↔ POs (Supplier)                              |
| Contacts                                     | People; CRM mirror; link to Hair Profile  |             75  |        18 | `Name` (title), `Hubspot Contacts Record ID`, `Notion Contacts Record ID` | ↔ Deals, ↔ Orders, ↔ Plans, 1:1 Hair Profile            |
| Hair Orders Profiles → **hs\_hair\_profile** | Canonical hair specs per person           |             75  |        16 | `Name` (title), `Notion Contacts Record ID`                               | 1:1 Contact, ↔ Orders                                   |
| Deals                                        | Commercial intent; HubSpot mirror for ops |             54  |        16 | `Name`, `Hubspot Deals Record ID`, `Notion Deals Record ID`               | 1:* Orders, 0..1 Plan, 1 Client                        |
| Plans                                        | Subscriptions for forecasting & order gen |             67  |        18 | `Name`, `Record ID`                                                       | 1 Client, 0..1 Deal, → generates Orders                 |
| Orders                                       | Customer orders; margin, ETA, tracking    |             47  |        20 | `Order Number`, `Notion Orders Record ID`                                 | 1 Deal, 1 Client, 1:* POs, 0..1 Hair Profile           |
| Purchase Orders                              | Supplier POs; costs + tracking in         |             52  |        18 | `PO Number`, `Notion Orders Record ID`                                    | *:1 Order, 1 Supplier(Company), 0..1 Inventory Product |
| Incomes → **hs\_payments**                   | Payments ledger (Stripe/GC)               |              8  |        12 | `Name` or `processor_payment_id`                                          | 0..1 Deal, 0..1 Order, 0..1 Plan, 1 Contact             |
| Expenses                                     | Opex ledger; multi‑currency → USD         |             35  |        16 | `Name`, external `ID`                                                     | ↔ Month, ↔ Categories                                   |

Average target ≤ 20 confirmed.

---

## 2) Property Rationalization per Database

Legend for **Score 0–5**: `O`ps / `A`utomation / `R`eporting / data `Q`uality risk / `L`egal|Finance. Example `O5 A5 R4 Q3 L2`.

### A) Companies  (source: Companies DB)&#x20;

**KEEP / COMPUTE set**

| Property          | Type     | Current Role                | Score 0–5      | Action  | Rationale                | Dependencies               |
| ----------------- | -------- | --------------------------- | -------------- | ------- | ------------------------ | -------------------------- |
| Company name      | title    | Display key                 | O5 A4 R3 Q5 L2 | KEEP    | Primary key for views    | —                          |
| Record ID         | number   | HubSpot ID mirror           | O3 A5 R2 Q4 L2 | KEEP    | Sync anchor              | n8n HS sync                |
| Company Profile   | select   | Distinguish Supplier/Client | O5 A5 R4 Q3 L3 | KEEP    | Drives routing and views | Used by Orders/POs filters |
| Email             | email    | B2B comms                   | O3 A3 R1 Q3 L1 | KEEP    | Supplier contact         | —                          |
| Phone Number      | phone    | Supplier/Client comms       | O2 A2 R0 Q2 L0 | KEEP    | Escalations              | —                          |
| Website URL       | url      | Domain dedupe               | O1 A2 R1 Q4 L0 | KEEP    | Dedupe key               | f\_domain()                |
| Country/Region    | text     | Address                     | O3 A1 R1 Q2 L2 | KEEP    | Compliance, shipping     | —                          |
| State/Region      | text     | Address                     | O3 A1 R1 Q2 L2 | KEEP    | Shipping                 | —                          |
| City              | text     | Address                     | O2 A1 R0 Q2 L1 | KEEP    | Shipping                 | —                          |
| Postal Code       | text     | Address                     | O2 A1 R0 Q2 L3 | KEEP    | VAT invoicing            | —                          |
| Street Address    | text     | Address                     | O2 A1 R0 Q2 L1 | KEEP    | Defaults                 | —                          |
| Time Zone         | text     | SLA calc                    | O2 A3 R1 Q2 L0 | COMPUTE | For contact window       | from address               |
| Tax ID            | text     | B2B compliance              | O1 A1 R2 Q1 L5 | KEEP    | Invoicing                | —                          |
| Associated Orders | relation | Company→Orders              | O3 A4 R4 Q3 L3 | KEEP    | Rollups                  | Orders                     |

**Top 20 to keep:** the 14 above.

**Cut List (highest impact first):**

1. Replace `Associated Purchase Orders` rich\_text → **ADD** relation to POs then delete rich\_text. O5 A5 R4 Q4 L3.
2. Delete CRM analytics not used in ops: `# Sessions`, `# Pageviews`, `# Times contacted`, `# Deals`, `Lead Source`, `Original Traffic Source`, `Lifecycle Stage`, `Industry group`. O0–1 A0 R0–1 Q2 L0.
3. Delete social: `Facebook`, `Instagram`, `Logo URL`. O0 A0 R0 Q1 L0.
4. Delete empty/vanity: `Industry group`, `Lead Status`, `Next Activity Date`, `Salon Name`. All empty.&#x20;
5. Delete “Associated …” rich\_text placeholders (`Associated Contacts/Deals/Invoices/Payments/Subscriptions`). Replace with real relations where needed or rely on other DBs’ back‑relations. O1 A1 R1 Q3 L1.

---

### B) Contacts  (source: Contacts DB)&#x20;

**KEEP / COMPUTE set (post‑move of hair fields to Hair Profile):**

| Property                   | Type       | Current Role        | Score          | Action  | Rationale             | Dependencies |
| -------------------------- | ---------- | ------------------- | -------------- | ------- | --------------------- | ------------ |
| Name                       | title      | Person key          | O5 A5 R4 Q5 L2 | KEEP    | Primary entity        | —            |
| Email                      | email      | Comms, dedupe       | O5 A5 R3 Q5 L2 | KEEP    | Identity + sync       | n8n HS sync  |
| Phone Number               | phone      | Comms               | O3 A3 R1 Q2 L1 | KEEP    | Service               | —            |
| Country/Region             | select     | Shipping defaults   | O3 A2 R1 Q2 L2 | KEEP    | Address               | —            |
| State/Region               | select     | Address             | O2 A1 R0 Q2 L1 | KEEP    | —                     | —            |
| City                       | text       | Address             | O2 A1 R0 Q2 L1 | KEEP    | —                     | —            |
| Postal Code                | text       | Address             | O2 A1 R0 Q2 L2 | KEEP    | —                     | —            |
| Street Address             | text       | Address             | O2 A1 R0 Q2 L1 | KEEP    | —                     | —            |
| Hubspot Contacts Record ID | number     | Sync anchor         | O3 A5 R2 Q4 L2 | KEEP    | Source of truth HS    | —            |
| Notion Contacts Record ID  | unique\_id | Internal key        | O3 A3 R2 Q5 L1 | KEEP    | Stable key            | —            |
| Associated Deals           | relation   | Pipeline linkage    | O3 A4 R3 Q3 L2 | KEEP    | Forecast rollups      | Deals        |
| Associated Orders          | relation   | Fulfillment linkage | O4 A5 R5 Q4 L3 | KEEP    | Ops dashboards        | Orders       |
| Associated Plans           | relation   | Renewal linkage     | O4 A5 R5 Q4 L3 | KEEP    | MRR                   | Plans        |
| Hair Orders Profiles       | relation   | Hair spec           | O5 A5 R4 Q4 L2 | KEEP    | 1:1                   | Hair Profile |
| Payment Status             | select     | CX quick view       | O2 A3 R3 Q2 L3 | COMPUTE | Roll up from payments | hs\_payments |
| Last Order Date            | rollup     | CX                  | O2 A3 R3 Q2 L1 | KEEP    | Attention lists       | Orders       |

**MOVE from Contacts → Hair Profile:** `Base Material`, `Base Size`, `Hair Color`, `Hairline Shape`, `Hairline Details`, `Hair Length`, `Density`, `Ventilation Method`, `Template Photo`, `Premade Compatibility`. These are duplicates now and many are unused here.&#x20;

**Cut List:**

* Delete unused/empty: `Files & media`, `Hair Orders Profiles` (if you keep the relation under canonical name only), `Next Activity Date`, `Sales Status`, `Template Photo` (on Contact).&#x20;
* Delete operational email‑body **Formula** fields and `Order Email`/`Order Email Text` blocks from Contacts. They belong to automation templates, not core entity. O0 A1 R0 Q3 L0.

---

### C) Hair Orders Profiles → **hs\_hair\_profile**  (source: Hair Orders Profiles DB)&#x20;

**KEEP / COMPUTE set**

| Property                | Type          | Role               | Score          | Action  | Rationale           | Dependencies |
| ----------------------- | ------------- | ------------------ | -------------- | ------- | ------------------- | ------------ |
| Name                    | title         | Profile label      | O3 A2 R1 Q3 L0 | KEEP    | e.g., “Default”     | —            |
| Associated Contact      | relation      | Owner              | O5 A5 R3 Q4 L1 | KEEP    | 1:1                 | Contacts     |
| Order Type              | select        | Default for orders | O4 A4 R2 Q2 L0 | KEEP    | Premade/Custom      | —            |
| Base Material           | text          | Spec               | O5 A3 R2 Q2 L0 | KEEP    | —                   | —            |
| Base Size               | text          | Spec               | O5 A3 R2 Q2 L0 | KEEP    | —                   | —            |
| Hair Color              | text          | Spec               | O5 A3 R2 Q2 L0 | KEEP    | —                   | —            |
| Hairline Shape          | select        | Spec               | O5 A3 R2 Q2 L0 | KEEP    | —                   | —            |
| Hairline Details        | multi\_select | Spec               | O4 A3 R2 Q2 L0 | KEEP    | —                   | —            |
| Hair Length             | select        | Spec               | O4 A3 R2 Q2 L0 | KEEP    | —                   | —            |
| Density                 | text          | Spec               | O4 A3 R1 Q2 L0 | KEEP    | —                   | —            |
| Ventilation Method      | text          | Spec               | O3 A2 R1 Q2 L0 | KEEP    | —                   | —            |
| Premade Compatibility   | select        | Routing            | O4 A4 R3 Q2 L0 | KEEP    | Stock routing       | Inventory    |
| Associated Orders       | relation      | Usage              | O3 A4 R3 Q3 L0 | KEEP    | Provenance          | Orders       |
| is\_premade\_compatible | formula       | Guardrail          | O4 A5 R2 Q3 L0 | COMPUTE | Normalize `Premade` | from select  |
| f\_spec\_hash           | formula       | Dedupe             | O4 A5 R2 Q5 L0 | COMPUTE | Hash of core spec   | Base fields  |
| rl\_last\_order\_date   | rollup        | CX                 | O2 A3 R3 Q2 L0 | KEEP    | Last use            | Orders       |

**Cut List:** Remove all CRM clones (`Country/Region`, marketing fields, email tracking, etc.). Empty properties flagged in source should be deleted here (e.g., `Files & media`, `Next Activity Date`, `Sales Status`, `Template Photo`).&#x20;

---

### D) Deals  (source: Deals DB)&#x20;

**KEEP / COMPUTE set**

| Property                | Type       | Role            | Score          | Action  | Rationale          |
| ----------------------- | ---------- | --------------- | -------------- | ------- | ------------------ |
| Name                    | title      | Deal key        | O5 A4 R3 Q5 L1 | KEEP    | Human label        |
| Hubspot Deals Record ID | number     | Sync            | O4 A5 R2 Q5 L2 | KEEP    | Source of truth    |
| Notion Deals Record ID  | unique\_id | Key             | O3 A3 R2 Q5 L1 | KEEP    | Internal key       |
| Deal Stage              | select     | Pipeline        | O5 A5 R4 Q4 L2 | KEEP    | SLA                |
| Deal Type               | select     | Type            | O4 A4 R3 Q3 L1 | KEEP    | Plan vs one‑off    |
| Deal Size               | select     | Units           | O4 A5 R4 Q3 L1 | KEEP    | Drives Plan/Orders |
| Currency                | select     | FX input        | O3 A4 R3 Q2 L3 | KEEP    | USD conv           |
| Amount                  | number     | Face value      | O4 A4 R4 Q3 L2 | KEEP    | Reporting          |
| Exchange rate           | number     | FX              | O3 A4 R3 Q3 L3 | KEEP    | USD                |
| Amount (USD)            | number     | Reporting       | O4 A5 R5 Q2 L3 | COMPUTE | `Amount*rate`      |
| Payment Date            | date       | Cash timing     | O3 A3 R3 Q2 L3 | KEEP    | Cohorts            |
| Associated Client       | relation   | Who             | O4 A5 R4 Q3 L2 | KEEP    | Rollups            |
| Associated Orders       | relation   | What fulfilled  | O5 A5 R5 Q3 L2 | KEEP    | Ops                |
| Associated Plan         | relation   | If subscription | O4 A4 R4 Q3 L2 | KEEP    | Forecast           |

**Cut List:** Delete empty/unused formulas and relations (`Auto Total`, `Retail Price`, `Income`, `Income Status`, `Linked Subscriptions`, `Month`, `Qty`, `Next Activity Date`, etc.). These are 100% or \~empty per source.&#x20;

---

### E) Plans  (source: Plans DB)&#x20;

**KEEP / COMPUTE set**

| Property                  | Type     | Role                | Score          | Action  | Rationale     |
| ------------------------- | -------- | ------------------- | -------------- | ------- | ------------- |
| Name                      | title    | Plan key            | O5 A4 R3 Q5 L1 | KEEP    | —             |
| Status                    | select   | Active/Paused/Ended | O5 A5 R4 Q3 L3 | KEEP    | SLA           |
| Start date                | date     | Start               | O4 A4 R3 Q3 L2 | KEEP    | Schedules     |
| End date                  | date     | End                 | O3 A3 R3 Q3 L2 | KEEP    | Churn         |
| Next billing date         | date     | Billing             | O5 A5 R4 Q3 L3 | KEEP    | Renewals      |
| Last Payment Date         | date     | Health              | O3 A3 R3 Q2 L3 | KEEP    | Dunning       |
| Monthly recurring revenue | number   | MRR                 | O4 A4 R5 Q2 L3 | KEEP    | KPI           |
| Payment Processor         | select   | Stripe/GC           | O4 A5 R3 Q2 L3 | KEEP    | Routing       |
| Currency                  | select   | FX input            | O3 A4 R3 Q2 L3 | KEEP    | USD calc      |
| Associated Client         | relation | Who                 | O4 A5 R4 Q3 L2 | KEEP    | —             |
| Associated Deal           | relation | Source              | O3 A4 R3 Q2 L2 | KEEP    | —             |
| Plan Size (rollup)        | rollup   | Units               | O4 A5 R4 Q2 L1 | KEEP    | Order gen     |
| Delivery Frequency        | select   | 8/10/12 weeks       | O4 A5 R4 Q2 L0 | KEEP    | Order cadence |
| Total Remaining Amount    | number   | AR                  | O3 A3 R4 Q2 L4 | KEEP    | Finance       |
| f\_units\_per\_cycle      | formula  | Units from size     | O4 A5 R3 Q2 L0 | COMPUTE | Normalization |
| is\_active                | formula  | Guardrail           | O5 A5 R3 Q3 L2 | COMPUTE | `Status`      |

**Cut List:** Remove 27+ empty properties (`Allowed payment methods`, `Automatically email invoices`, contact address mirrors, etc.).&#x20;

---

### F) Orders  (source: Orders DB)&#x20;

**KEEP / COMPUTE set (align to ops rules):**

| Property                | Type       | Role               | Score          | Action       | Rationale                     |
| ----------------------- | ---------- | ------------------ | -------------- | ------------ | ----------------------------- |
| Order Number            | title      | Key                | O5 A5 R4 Q5 L2 | KEEP         | External ref                  |
| Notion Orders Record ID | unique\_id | Key                | O4 A4 R3 Q5 L1 | KEEP         | Internal                      |
| Associated Deal         | relation   | Source             | O4 A5 R4 Q3 L2 | KEEP         | Forecast links                |
| Client                  | relation   | Contact            | O5 A5 R5 Q4 L2 | KEEP         | Service                       |
| Related Hair Profile    | relation   | Specs              | O5 A5 R4 Q3 L1 | KEEP         | Quality                       |
| Associated PO           | relation   | Supply             | O5 A5 R5 Q3 L3 | KEEP         | Costs/ETA                     |
| Order\_Date             | date       | Start              | O5 A5 R4 Q3 L2 | KEEP         | SLAs                          |
| Order\_ETA              | date       | Promise            | O5 A5 R5 Q3 L3 | KEEP         | Alerts                        |
| Shipped Date            | date       | Milestone          | O4 A4 R4 Q3 L2 | KEEP         | Delivery calc                 |
| Order Status            | select     | Canonical statuses | O5 A5 R5 Q3 L2 | KEEP         | SLA                           |
| Order Speed             | select     | Rush/Std           | O3 A4 R3 Q2 L0 | KEEP         | Routing                       |
| Factory                 | select     | Source plant       | O4 A4 R3 Q2 L2 | KEEP         | Routing                       |
| Tracking Number         | **text**   | Carrier tracking   | O5 A5 R4 Q3 L2 | **TYPE FIX** | Alphanumeric; today is number |
| Shipping Carrier        | text       | Carrier            | O4 A4 R3 Q2 L2 | RENAME       | from `Shipping Courrier`      |
| Payment Date            | date       | Cash timing        | O3 A3 R3 Q2 L3 | COMPUTE      | rollup from Payments          |
| rl\_cogs\_usd           | rollup     | COGS from POs      | O5 A5 R5 Q2 L5 | ADD          | Margin calc                   |
| f\_margin\_usd          | formula    | Revenue−COGS       | O5 A5 R5 Q2 L5 | ADD          | KPI                           |
| is\_late                | formula    | ETA breach         | O5 A5 R4 Q4 L1 | ADD          | Alerting                      |

**MOVE from Orders → POs:** `Factory Invoice No` belongs to supplier PO. **Delete** duplicate date formulas (`Order ETAs`, `Production Start Date` formula) and rarely used internals (`Index`). Many ETA/ship fields are <5% filled; keep the atomic date fields only.&#x20;

---

### G) Purchase Orders  (source: POs DB)&#x20;

**KEEP / COMPUTE set**

| Property                | Type       | Role              | Score          | Action       | Rationale                |
| ----------------------- | ---------- | ----------------- | -------------- | ------------ | ------------------------ |
| PO Number               | title      | Key               | O5 A5 R4 Q5 L2 | KEEP         | Supply key               |
| Notion Orders Record ID | unique\_id | Key               | O4 A4 R3 Q5 L1 | KEEP         | Internal                 |
| Associated Order        | relation   | Demand link       | O5 A5 R5 Q3 L3 | KEEP         | 1:*                     |
| Associated Deal         | relation   | Context           | O3 A3 R3 Q2 L2 | KEEP         | Optional                 |
| Client                  | relation   | End customer      | O3 A3 R2 Q2 L1 | KEEP         | For labeling             |
| Associated Companies    | relation   | Supplier          | O5 A5 R4 Q3 L4 | KEEP         | AP                       |
| Order\_Date             | date       | Start             | O4 A4 R3 Q3 L2 | KEEP         | —                        |
| Production Start Date   | date       | Start prod        | O4 A4 R3 Q3 L2 | KEEP         | —                        |
| Order ETA               | date       | Promise           | O5 A5 R5 Q3 L3 | KEEP         | —                        |
| Shipped Date            | date       | Milestone         | O4 A4 R4 Q3 L2 | KEEP         | —                        |
| Payment Due             | date       | AP due            | O4 A4 R3 Q2 L5 | KEEP         | AP control               |
| Payment Date            | date       | AP paid           | O4 A4 R3 Q2 L5 | KEEP         | AP control               |
| Payment Status          | select     | Paid/Unpaid       | O4 A4 R3 Q2 L5 | KEEP         | Reconciliation           |
| Hair Unit Cost          | number     | COGS              | O5 A5 R5 Q2 L5 | KEEP         | Margin                   |
| Extras Cost             | number     | COGS              | O4 A4 R4 Q2 L4 | KEEP         | Margin                   |
| Shipment Cost           | number     | COGS              | O4 A4 R4 Q2 L4 | KEEP         | Margin                   |
| Total Cost              | number     | Sum               | O4 A5 R5 Q2 L5 | COMPUTE      | add fields               |
| Tracking Number         | **text**   | Supplier tracking | O5 A5 R4 Q3 L2 | **TYPE FIX** | Alphanumeric             |
| Shipping Carrier        | text       | Carrier           | O4 A4 R3 Q2 L2 | RENAME       | from `Shipping Courrier` |
| Inventory Product       | relation   | SKU link          | O3 A4 R3 Q2 L2 | KEEP         | Routing                  |

**Cut List:** Delete empty `Inventory Products DB` duplicate relation, `Text`, unused rollups (`Density`, `Cost per Unit`) unless you wire Inventory first; remove `Order Profile` multi‑select (redundant). Empty/mostly empty fields listed in source can go.&#x20;

---

### H) Incomes → **hs\_payments**  (source: Incomes DB)&#x20;

**KEEP / COMPUTE set + new relations**

| Property      | Type     | Role              | Score          | Action         | Rationale |         |
| ------------- | -------- | ----------------- | -------------- | -------------- | --------- | ------- |
| Name          | title    | Payment label     | O3 A3 R2 Q3 L3 | KEEP           | —         |         |
| Payment Date  | date     | Cash timing       | O5 A5 R5 Q2 L5 | KEEP           | Reco      |         |
| Amount        | number   | Amount native     | O4 A4 R4 Q2 L5 | KEEP           | —         |         |
| Type          | select   | `Order           | General`      | O3 A4 R3 Q2 L3 | KEEP      | Routing |
| Currency      | select   | (ADD)             | O3 A5 R3 Q2 L5 | ADD            | FX        |         |
| Exchange Rate | number   | (ADD)             | O3 A5 R3 Q3 L5 | ADD            | USD       |         |
| Net USD       | formula  | (ADD)             | O5 A5 R5 Q2 L5 | ADD            | KPI       |         |
| Processor     | select   | Stripe/GC/Shopify | O3 A5 R3 Q2 L4 | ADD            | Routing   |         |
| Related Deal  | relation | 0..1              | O3 A4 R3 Q2 L5 | ADD            | Mapping   |         |
| Related Order | relation | 0..1              | O5 A5 R5 Q3 L5 | ADD            | Reco      |         |
| Related Plan  | relation | 0..1              | O4 A5 R4 Q2 L5 | ADD            | MRR       |         |
| Contact       | relation | 1                 | O4 A5 R4 Q2 L5 | ADD            | CX        |         |

**Cut List:** Keep lean. Existing `Income` and `Order Income` formulas can be replaced by relations + rollups.&#x20;

---

### I) Expenses  (source: Expenses DB)&#x20;

**KEEP / COMPUTE set**

| Property      | Type     | Role              | Score          | Action | Rationale |
| ------------- | -------- | ----------------- | -------------- | ------ | --------- |
| Name          | title    | Expense label     | O3 A3 R2 Q3 L5 | KEEP   | —         |
| Date          | date     | When              | O5 A5 R5 Q2 L5 | KEEP   | —         |
| Currency      | select   | Native            | O4 A5 R4 Q2 L5 | KEEP   | —         |
| Total Amount  | number   | Native gross      | O4 A5 R4 Q2 L5 | KEEP   | —         |
| Exchange Rate | number   | FX                | O3 A5 R3 Q3 L5 | KEEP   | —         |
| Total USD     | formula  | Reporting         | O5 A5 R5 Q2 L5 | KEEP   | KPI       |
| Fee           | number   | Fees              | O3 A3 R3 Q2 L5 | KEEP   | Net calc  |
| Type          | select   | Category macro    | O3 A4 R4 Q2 L5 | KEEP   | Budget    |
| Categories    | relation | Chart of accounts | O3 A4 R5 Q2 L5 | KEEP   | Reporting |
| Month         | relation | Period            | O3 A4 R5 Q2 L5 | KEEP   | Cohorts   |
| ID            | text     | External ref      | O2 A3 R2 Q4 L3 | KEEP   | Dedupe    |
| Payer         | text     | Control           | O2 A2 R1 Q2 L3 | KEEP   | Audit     |

**Cut List:** Remove empty relations (`Platform`, `Projects`, `Restock Connection`), `Product` rollup, and `Archive`. All empty per source.&#x20;

---

## 3) Move and Merge Plan

**Moves**

* Contacts → Hair Profile: all hair spec fields listed above. Reason: canonicalize specs; Contacts becomes clean CRM person.
* Orders → POs: `Factory Invoice No`. Reason: supplier doc lives on PO. &#x20;
* Payments: replace Order/Deal `Payment Date` free fields with rollups from **hs\_payments**.

**Merges / Renames**

* Hair Orders Profiles → rename DB to `hs_hair_profile`; standardized field prefixes: `is_`, `f_`, `rl_`.&#x20;
* Orders: `Shipping Courrier` → `Shipping Carrier`; `Tracking Number` type text; `Order Details` → `Order Type`.&#x20;
* POs: same carrier/tracking normalizations; unify `Factory` options (`RareHair`, `NewTimes Hair`, `LuxHair`).&#x20;
* Payments: rename **Incomes** → `hs_payments`; add relations listed.&#x20;

**Duplicate/Alias map (canonical ← aliases)**

* `Shipping Carrier` ← `Shipping Courrier` (Orders, POs). &#x20;
* `Order Type` ← `Order Details` (Orders, POs). &#x20;
* `hs_hair_profile` ← `Hair Orders Profiles`.&#x20;
* `Factory: RareHair` normalize from `Rare Hair`. (Orders)&#x20;

---

## 4) Relations Audit and Design

| From DB   | To DB             | Cardinality | Purpose               | Usage | Action             | Risk if removed        | Reason                           |
| --------- | ----------------- | ----------- | --------------------- | ----- | ------------------ | ---------------------- | -------------------------------- |
| Deals     | Contacts          | *:1        | Who the deal is with  | High  | KEEP               | Orphaned pipeline      | CRM truth; HubSpot mirror        |
| Deals     | Orders            | 1:*        | Fulfillment from deal | High  | KEEP               | No revenue realization | Ops flow                         |
| Deals     | Plans             | 0..1        | Subscription source   | Med   | KEEP               | Lost plan context      | Forecasting                      |
| Orders    | POs               | 1:*        | One PO per unit       | High  | KEEP               | No COGS                | Business rule                    |
| Orders    | Contacts          | *:1        | Customer              | High  | KEEP               | No comms/tracking      | Service                          |
| Orders    | Hair Profile      | 0..1:*     | Apply specs           | Med   | KEEP               | Spec drift             | QA                               |
| POs       | Companies         | *:1        | Supplier              | High  | KEEP               | AP not tied            | Supplier ops                     |
| Payments  | Orders            | 0..1:*     | Attribute cash in     | High  | **ADD**            | Payment gaps           | Reconciliation                   |
| Payments  | Deals             | 0..1:*     | Non‑order receipts    | Med   | **ADD**            | AR mismatch            | Finance                          |
| Payments  | Plans             | 0..1:*     | Recurring             | Med   | **ADD**            | MRR wrong              | Finance                          |
| Contacts  | Hair Profile      | 1:1         | Canonical spec        | High  | **ADD constraint** | Duplicates             | Move hair fields                 |
| Companies | Orders            | 1:*        | B2B client orders     | Low   | KEEP               | Less B2B rollups       | Optional; use Contact as primary |
| POs       | Inventory Product | *:1        | SKU link              | Med   | KEEP               | No BOM cost            | Supply routing                   |

**Anti‑patterns found**

* Rich‑text “Associated …” instead of relations in Companies. Replace.&#x20;
* Hair spec duplicated in Contacts and Hair Profiles. Remove from Contacts. &#x20;
* Tracking numbers stored as numbers. Switch to text. &#x20;
* Factory names inconsistent. Normalize. &#x20;

---

## 5) Minimal Canonical Schema v1 (≤20 each)

### Companies

* `title Company name` — display.
* `number Record ID` — HS ID mirror.
* `select Company Profile` — `Supplier|Wholesale Client|Salon|…`.
* `email Email`, `phone Phone`.
* Address: `text Street`, `text City`, `text State/Region`, `text Postal`, `text Country/Region`.
* `text Time Zone` (compute).
* `text Tax ID`.
* `relation Orders`, `relation POs`.

**Examples:**

* `is_supplier` (formula): `prop("Company Profile") == "Hair Products Supplier"`.
* `f_domain` (formula): `replaceAll(prop("Website URL"), "https?://(www\\.)?", "")`.
* `rl_open_pos` (rollup from POs→Status): count where `Status != "Paid"`.

### Contacts

* `title Name`, `email Email`, `phone Phone`.
* Address fields as above.
* `number Hubspot Contacts Record ID`, `unique_id Notion Contacts Record ID`.
* `relation Deals`, `relation Orders`, `relation Plans`, `relation hs_hair_profile`.
* `select Payment Status` (computed via payments rollup).

**Examples:**

* `is_vip` (formula): `rollup(MRR)>1000`.
* `rl_last_order_date` (rollup Orders→Order\_Date, latest).
* `status_contact` (formula): `"Active" if rl_last_order_date within 180 days else "Dormant"`.

### hs\_hair\_profile

* `relation Associated Contact` (unique).
* Core spec fields from section 2C.
* `select Premade Compatibility`, `formula is_premade_compatible`, `formula f_spec_hash`, `relation Orders`, `rollup rl_last_order_date`.

**Examples:**

* `is_incomplete` (formula): any empty core field → true.
* `f_spec_hash`: `sha256(concat(Base Material, Base Size, Hair Color, Hair Length))`.
* `status_profile` (formula): `"ready" if !`is_incomplete` else `"needs_input"`.

### Deals

* Keys + stage/type/size/currency/amount/exchange USD.
* Relations: `Associated Client`, `Associated Orders`, `Associated Plan`.

**Examples:**

* `is_open` (formula): `not contains(["Closed Won","Completed"], prop("Deal Stage"))`.
* `f_amount_usd` (formula): `prop("Amount") * prop("Exchange rate")`.
* `rl_units` (rollup Orders→Unit count).

### Plans

* Keys + status/start/end/next billing/last payment/MRR/currency/processor/delivery frequency.
* Relations: `Associated Client`, `Associated Deal`.
* `rollup Plan Size`.

**Examples:**

* `is_active` (formula): `prop("Status") == "Active"`.
* `f_units_per_cycle` (formula): map from `Plan Size`.
* `status_plan` (formula): `"dunning" if days since `Last Payment Date` > 7 and `is_active`.

### Orders

* Keys + relations + dates + status + factory + speed + carrier/tracking (text).
* `rollup rl_cogs_usd` from POs, `formula f_margin_usd`, `formula is_late`.

**Examples:**

* `is_late`: `now() > prop("Order_ETA") and prop("Order Status") != "delivered"`.
* `f_margin_usd`: `revenue_usd - prop("rl_cogs_usd")` (revenue from Deal or Payments).
* `status_order` (formula): normalize to canonical ladder.

### Purchase Orders

* Keys + relations + dates + payment fields + costs + carrier/tracking.
* `formula Total Cost` as sum of cost parts.

**Examples:**

* `is_unpaid`: `prop("Payment Status") != "Paid"`.
* `f_cogs_usd`: FX if needed via supplier currency (if added later).
* `status_po`: `"awaiting_payment"|"in_production"|"awaiting_ship"|"shipped"|"closed"`.

### hs\_payments

* Keys + date + amount + currency + exchange rate + net USD + processor.
* Relations to Deal/Order/Plan/Contact.

**Examples:**

* `is_refund` (formula): `prop("Amount") < 0`.
* `net_usd` (formula): `(Amount - fee_native)*rate`.
* `status_payment` (formula): `"posted" if linked to any entity else `"unmatched"`.

### Expenses

* Keys + date + currency + amount + rate + USD + type + category + month + fee + payer + external ID.

**Examples:**

* `is_ads` (formula): `contains(prop("Type"), "Ad")`.
* `net_usd` (formula): `prop("Total USD") - (prop("Fee")*prop("Exchange Rate"))`.
* `status_expense` (formula): `"completed" if `State == "COMPLETED"` else `"open"`.

---

## 6) Migration and Safety

**Order of operations**

1. **Add** new/renamed fields with prefixes (`is_`, `f_`, `rl_`, `hs_`) in each DB.
2. **Type fixes**: convert `Tracking Number` number→text in Orders and POs; rename carrier field. &#x20;
3. **Create relations**: hs\_payments↔Deals/Orders/Plans/Contacts; Companies↔POs. &#x20;
4. **Move hair fields**: copy from Contacts→hs\_hair\_profile then delete from Contacts. &#x20;
5. **Normalize selects**: unify `Factory` values; replace `Order Details` with `Order Type`. &#x20;
6. **Backfill rollups/formulas** and validate counts.
7. **Delete** cut‑list fields after 14‑day shadow period.

**Transforms (pseudocode)**

* **Copy hair specs**:

```
for contact in Contacts:
  profile = upsert hs_hair_profile by contact.id
  profile.specs = pick(contact, [Base Material, Base Size, Hair Color, Hairline Shape, Hairline Details, Hair Length, Density, Ventilation Method, Premade Compatibility])
```

* **Tracking type fix**: set new `Tracking Number (text)` = format(old\_number), then remove old.
* **Deal USD**: `Amount (USD) = Amount * Exchange rate`.
* **PO Total Cost**: `Total Cost = Hair Unit Cost + Extras Cost + Shipment Cost`.
* **Payment net\_usd**: `Net USD = Amount * Exchange Rate` (minus fees if added).

**Dedupe keys**

* Contacts: `lower(Email)`; fallback `Name+Phone`.
* Companies: domain from Website URL; fallback `Company name`.
* Deals: `Hubspot Deals Record ID`; fallback `Associated Client + Close Date`.&#x20;
* Orders: `Order Number` unique.&#x20;
* POs: `PO Number` unique.&#x20;
* Payments: processor payment ID (add).
* Expenses: external `ID`.

**Rollback**

* Keep “\_old” copies of deleted fields for 90 days (hidden view).
* All deletions after verifying parity views (below) show zero variance for 14 days.

**Data retention**

* Financial ledgers retained indefinitely.
* Operational logs (old formulas/rich\_text “Associated …”) retained 90 days then purge.

---

## 7) Validation and QA

**Saved views / filters**

1. **Orphans**

   * Orders without Client or Deal. Filter: `Client is empty OR Associated Deal is empty`. Must be 0.&#x20;
   * POs without Supplier or Order. Filter: `Associated Companies is empty OR Associated Order is empty`. Must be 0.&#x20;
2. **Payment reconciliation**

   * Payments `status_payment=="unmatched"`. Must be 0 after linking.&#x20;
   * Orders with `rl_cogs_usd is empty` where `Order Status` beyond `submitted`. Investigate.&#x20;
3. **Property cap**

   * Per DB, hidden view listing visible properties count ≤ target.
4. **Relation cycles**

   * Ensure no Orders→POs→Orders multi‑cycles beyond 1:* intended.
5. **Computed mismatches**

   * Orders where `is_late=true` but `Order Status` ∈ {delivered, cancelled}. Should be 0.
   * Deals where `Amount (USD)` != `Amount*Exchange rate` within tolerance.

**Acceptance criteria**

* Average properties per DB ≤ 20 with target counts above.
* All Orders link to ≥1 PO after `submitted`.
* All POs have Supplier and Payment Status.
* All active Plans have Next billing date.&#x20;
* All Contacts have exactly one Hair Profile or are flagged `is_incomplete`.&#x20;
* KPI parity: MRR, Revenue Net USD, COGS, Expenses match pre‑migration within 0.5% for last 60 days (computed from Deals/Plans/hs\_payments/Expenses).

---

## Final cut pressure points to hit the cap

* Companies: drop social + CRM analytics + rich\_text “Associated …”.
* Contacts: drop all hair spec + email template fields.
* Hair Profile: drop CRM artifacts.
* Deals: drop 16 empty formulas/relations.&#x20;
* Orders/POs: fix types, remove duplicate formulas, keep atomic dates. &#x20;
* Plans: remove 27 empty fields.&#x20;
* Expenses/Payments: keep lean ledger sets. &#x20;

If you confirm the five pre‑flight answers, I will supply exact Notion field creation/rename scripts and n8n nodes for the moves in your five‑workflow architecture.
