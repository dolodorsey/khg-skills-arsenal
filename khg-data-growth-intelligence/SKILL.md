---
name: khg-data-growth-intelligence
description: Growth data governance, segmentation, attribution, source economics, signal intelligence and entity-isolated data-use controls.
---

# KHG Data Growth Intelligence

## Mission
Make growth decisions from usable, governed data while preventing uncontrolled cross-brand data reuse.

## Data-use rule
Every dataset must state source type, allowed purpose, prohibited purpose, contact-use permission, consent requirement, cross-entity rule, retention, sharing, enrichment and compliance status before automation depends on it.

## Intelligence layers
1. Data quality: identity resolution, duplicates, stale fields, missing consent and source evidence.
2. Audience intelligence: segment size, intent, behavior, objections and channel preference.
3. Funnel intelligence: stage velocity, leakage, SLA failures and reactivation pools.
4. Source economics: qualified yield, reply rate, conversion, revenue, cost and refresh latency.
5. Attribution: first/last/assisted touches and confidence.
6. Experiment learning: winners, losers and reusable insights.

## Execution loop
Audit data permissions first. Then compute entity-level insights, find unexplained performance changes, identify missing instrumentation, create corrective tasks, and feed learnings back into source selection, campaigns, outreach and automation.

## Backend contract
Use `growth_data_usage_registry`, `growth_signal_events`, `growth_attribution_touchpoints`, `growth_experiments`, `lead_prospects`, `lead_followup_log`, `growth_programs` and analytics sources.

## Guardrails
Person-level records stay entity-scoped unless explicit rights permit broader use. Aggregate enterprise reporting is allowed when it does not expose or repurpose person-level data. Sensitive data is restricted.

## Quality bar
No dashboard theater. Every reported metric needs definition, timeframe and source. Every recommendation must tie to a measurable outcome or risk.