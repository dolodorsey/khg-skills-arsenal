---
name: khg-marketing-automation
description: Event-driven growth automation across Supabase, n8n, GHL and approved APIs with retries, observability and no dead ends.
---

# KHG Marketing Automation

## Mission
Remove manual growth bottlenecks without creating invisible failures, spam loops or cross-brand data leakage.

## Architecture standard
Trigger → validate entity/data rights → normalize → dedupe/idempotency → enrich if permitted → score/route → action gate → write result → evidence/log → retry/dead-letter → escalation.

## Required automations
Inbound lead routing, social intent capture, outreach follow-up, content performance loops, sponsor progression, grant deadlines, ambassador lifecycle, CRM stage/SLA enforcement, attribution capture, source-quality monitoring and executive reporting.

## n8n pattern
Use one orchestrator per domain with reusable subflows for identity resolution, entity routing, compliance checks, GHL sync, messaging gates, evidence logging and incident creation. Never create a giant cross-brand workflow that loses entity context.

## GHL pattern
Each contact/opportunity must retain entity key, lead archetype, source, consent/DNC state, stage, owner, next action, last touch, attribution and campaign identifiers. Pipelines are entity- or program-specific where mixing would damage reporting.

## Reliability
Every automation requires idempotency key, retry policy, timeout, error payload, dead-letter path, run evidence and health metric. A workflow that silently fails is considered broken.

## Approval gates
External sends/publishing obey entity channel policy. Financial commitments, contracts, final grant submissions and regulated-category actions require the configured human approval.

## Backend contract
Use `growth_automation_playbooks`, `growth_automation_runs`, `scheduled_operations`, `tasks`, `enterprise_incidents`, `lead_engagement_queue`, `growth_data_usage_registry` and entity platform accounts.

## Quality bar
No dead ends. No duplicate sends. No unlogged actions. No cross-brand contact reuse. No automation declared complete until successful runs and failure handling are proven.