# Canonical Schema v1 — Simplified Task List

## 1) Pre‑flight confirmations (blocking)
- Hair specs live in Hair Orders Profiles → rename to hs_hair_profile; remove hair fields from Contacts.
- Companies holds Suppliers + B2B Clients via Company Profile (or specify separate Suppliers DB).
- Incomes is the payments ledger → rename to hs_payments; add relations; compute USD net.
- Approve canonical Order status ladder.
- Approve unified Factory options and carrier/tracking types; Tracking Number = text.

## 2) Global setup
- Adopt prefixes: is_ (flags), f_ (formulas), rl_ (rollups), hs_ (system), status_ (labels).
- Use snake_case and unit suffixes (_usd, _date, _pct, _count).
- Normalize selects and names: Shipping Courrier → Shipping Carrier; set Tracking Number to text.

## 3) Database changes
- Companies: keep core identity/address/profile; add real relations to Orders/POs; delete CRM analytics/social and “Associated …” rich-text.
- Contacts: keep core CRM; move hair fields to hs_hair_profile; relations (Deals/Orders/Plans/Profile); compute Payment Status; delete email-template formulas.
- hs_hair_profile: create/rename; keep core specs; 1:1 Contact; add is_premade_compatible, f_spec_hash, rl_last_order_date; link to Orders.
- Deals: keep keys + stage/type/size/currency/amount; add Amount (USD); relations to Client/Orders/Plan; remove unused formulas/relations.
- Plans: keep status/dates/MRR/currency/processor/frequency; add is_active, f_units_per_cycle; remove empty properties.
- Orders: Tracking Number → text; Shipping Courrier → Shipping Carrier; add rl_cogs_usd, f_margin_usd, is_late; keep atomic dates; move Factory Invoice No to POs; prune duplicate date formulas.
- Purchase Orders: ensure Supplier/Order relations; dates + payment fields; costs + Total Cost formula; tracking text + carrier rename; delete redundant/empty fields.
- hs_payments (Incomes): rename DB; add currency, exchange rate, net USD, processor; add relations (Deal/Order/Plan/Contact); replace ad‑hoc payment dates with rollups.
- Expenses: keep lean ledger set; ensure USD formula; remove empty relations/rollups.

## 4) Migration order (safe → risky)
- Add/rename fields with prefixes across DBs.
- Type fixes: Tracking Number → text; Shipping Courrier → Shipping Carrier.
- Create relations: hs_payments ↔ (Deals/Orders/Plans/Contacts), Companies ↔ POs.
- Move hair fields Contacts → hs_hair_profile; backfill values.
- Normalize selects (Factory, Order Type).
- Backfill formulas/rollups; validate counts.
- Shadow 14 days; then delete cut‑list fields.

## 5) Data quality and safety
- Dedupe keys per DB (e.g., Contacts by email; Orders by Order Number; POs by PO Number; Payments by processor ID).
- Saved views: orphans (Orders↔Deal/Client, POs↔Supplier/Order), unmatched payments, property cap ≤ targets, computed mismatches.
- Acceptance: linkage complete, property caps met, KPI parity within 0.5% (last 60 days).
- Rollback: keep _old copies hidden for 90 days; follow retention policy.

## 6) Deliverables
- Field create/rename scripts + n8n nodes.
- Normalized select option lists + status ladder.
- Validation views and runbook to execute steps above.
