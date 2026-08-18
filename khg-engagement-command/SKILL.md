---
name: khg-engagement-command
description: Strategic social/community engagement that creates relationships, captures intent and advances entity objectives without spam.
---

# KHG Engagement Command

## Mission
Turn attention into conversation and conversation into qualified relationship movement while protecting brand reputation and contact rules.

## Inputs
Read current objective, active content, engagement targets, recent touches, cooldowns, lead stages, relationship pipeline, response history and data-use rules.

## Target scoring
Prioritize by audience overlap, strategic relationship value, recent intent signal, relevance to active campaign, reciprocity potential, freshness and contact history. Penalize repetition, unanswered cold touches and low-evidence targeting.

## Engagement modes
Public comments, meaningful replies, story/reel interaction, community participation, partner amplification, creator warming, customer response, DM continuation and event/community follow-up.

## Execution loop
1. Build a ranked engagement queue.
2. Inspect context before touching an account.
3. Use a specific observation or shared context; never generic praise at scale.
4. Capture response and intent signals.
5. Convert qualified interactions into `lead_prospects` or `growth_relationships`.
6. Enforce cooldowns and unanswered-follow-up caps.
7. Schedule next action with owner and due time.
8. Report quality touches, replies, warm relationships and engagement-to-lead conversion.

## Backend contract
Use `growth_social_engagement_targets`, `lead_engagement_queue`, `lead_followup_log`, `growth_signal_events`, `growth_relationships`, and `v_growth_lead_command`.

## Quality bar
No bot-like repetitive comments. No blind mass DMs. No cross-brand identity reuse. No engagement counted as success unless it produces measurable audience, relationship or conversion value.