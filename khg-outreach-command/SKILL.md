---
name: khg-outreach-command
description: Evidence-based multi-channel outbound, warm-up, follow-up and relationship progression for one KHG entity.
---

# KHG Outreach Command

## Mission
Create qualified conversations and pipeline movement, not raw send volume.

## Research standard
Before outreach, resolve entity objective, lead archetype, source evidence, recent signals, relationship context, permission/DNC state, best channel and desired next step.

## Prioritization
Score targets by strategic fit, intent, timing, personalization evidence, relationship warmth, reach/value, conversion potential and cost-to-pursue.

## Sequence architecture
Warm when possible before asking. Use channel-appropriate touches. Every sequence must define entry criteria, stop conditions, maximum unanswered follow-ups, response classification, SLA and next stage.

## Execution loop
1. Source or accept qualified targets.
2. Verify identity, source and entity fit.
3. Recheck DNC/contact-use rules.
4. Build a specific personalization hook from evidence.
5. Draft the shortest message that earns the next step.
6. Gate external sending according to entity policy.
7. Log every touch and response.
8. Classify reply: positive, question, objection, not-now, referral, unsubscribe/DNC, no-response.
9. Advance CRM stage and schedule next action.
10. Measure reply quality, meetings, opportunities, pipeline value and conversion.

## Backend contract
Use `lead_prospects`, `v_growth_lead_command`, `lead_engagement_queue`, `lead_followup_log`, `growth_relationships`, `growth_signal_events` and `growth_automation_playbooks`.

## Quality bar
No purchased-list blasting. No contact without a valid use basis. No endless follow-up. No cross-brand customer/prospect reuse by default. No outreach activity reported as success without pipeline movement.