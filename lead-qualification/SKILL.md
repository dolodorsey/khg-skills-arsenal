---
name: lead-qualification
description: Evidence-based KHG lead qualification that scores entity fit, intent, timing, permission, value and next action without cross-brand contamination.
---

# Lead Qualification

## Mission
Turn sourced leads and relationship signals into a ranked, evidence-backed queue for one specific KHG entity. Qualification is a decision system, not a vanity score.

## Required context
Resolve the canonical entity first. Use the entity's current objective, audience, offer, conversion path, geographic scope, relationship archetype, contact permissions, DNC state and existing touch history. Never borrow another entity's scoring assumptions or customer/prospect data by default.

## Qualification dimensions
Score each candidate on: entity fit, current intent, recency, problem/need alignment, decision authority or influence, economic/strategic value, timing, relationship warmth, source trust, contact permission and evidence quality. Penalize duplicates, stale records, missing evidence, suppression/DNC conflicts, sensitive-data risk and over-contacting.

## Decision bands
- **Priority A** — strong fit + strong current signal + permitted next action. Route immediately with an owner and SLA.
- **Priority B** — good fit but weaker timing/signal. Route to nurture, monitoring or research with a defined next check.
- **Priority C** — plausible but materially incomplete. Require enrichment/verification before outreach.
- **Disqualify / Suppress** — wrong entity, no legitimate fit, prohibited use, DNC/suppression conflict, invalid identity, duplicate or low-value noise.

## Evidence standard
Every qualification must preserve source/reference, observed signal, timestamp/freshness, entity match rationale, permission/contact-use state, score inputs, decision band, owner and next action. Do not label a lead qualified when the evidence does not support it.

## Routing
Priority leads must never dead-end. Route them to the correct entity-specific engagement, outreach, sponsor, ambassador, partner, donor, customer, vendor or other relationship workflow. Set the next action and due time at qualification time.

## Backend contract
Use `lead_prospects`, `growth_signal_events`, `growth_relationships`, `growth_data_usage_registry`, `growth_pipeline_slas`, `growth_source_performance`, `v_growth_lead_command` and the canonical enterprise entity tables. Preserve entity IDs/keys throughout qualification and attribution.

## Metrics
Track qualified rate by source, evidence coverage, permission coverage, time-to-route, response rate, meetings/conversions, disqualification reasons, false-positive rate and downstream revenue/value.

## Guardrails
No sensitive-trait inference. No fabricated contact details or intent. No cross-brand person-level reuse by default. No automated contact unless channel, consent, suppression and entity policies permit it. Qualification may recommend an action; regulated, financial, contractual or otherwise approval-gated actions remain gated.
