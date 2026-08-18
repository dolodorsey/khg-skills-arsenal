---
name: khg-lead-intelligence
description: Multi-source lead discovery, evidence capture, signal scoring, dedupe, data-use validation and entity routing.
---

# KHG Lead Intelligence

## Mission
Continuously produce fresh, qualified and usable lead intelligence for one entity. Optimize for downstream conversations and revenue, not database size.

## Source hierarchy
Prioritize zero/first-party intent, referrals, event/community interactions, approved public signals, entity-aligned directories/communities, then licensed enrichment. Every source must have a data-use record.

## Evidence standard
Store source URL/reference, observed signal, timestamp, entity fit, lead archetype, permission/contact-use state and freshness. A lead without evidence is low-confidence.

## Scoring model
Blend intent, fit, recency, source trust, relationship warmth, strategic value and contact permission. Penalize stale, duplicate, unverifiable, sensitive, non-permitted or over-contacted records.

## Execution loop
1. Select sources by historical yield and current objective.
2. Extract candidate identities and intent signals.
3. Normalize/dedupe against entity records.
4. Match only to relevant entity/archetype.
5. Verify permitted use and DNC state.
6. Create/update lead and signal evidence.
7. Score priority and route to engagement, outreach, nurture or research.
8. Track source yield, qualification rate, reply rate and conversion.
9. Lower or retire poor sources automatically.

## Backend contract
Use `public_source_catalog`, `public_source_entity_matches`, `lead_source_accounts`, `lead_prospects`, `growth_signal_events`, `growth_data_usage_registry`, `v_growth_lead_command` and source-performance metrics.

## Quality bar
No scraping merely because technically possible. No sensitive-trait inference. No cross-brand lead reuse by default. No contact automation unless the data-use and channel rules permit it.