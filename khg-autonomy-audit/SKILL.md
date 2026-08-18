---
name: khg-autonomy-audit
description: Audit whether the Kollective autonomous operating system is actually working. Use for readiness grading, owner/agent/objective/task coverage, scheduled-operation health, evidence quality, stale queues, policy compliance, and finding "fake complete" systems that exist on paper but are not executing.
metadata:
  version: 1.0.0
  owner: The Kollective Hospitality Group
---

# KHG Autonomy Audit

Audit execution, not documentation.

## Required Checks

For every scope being audited, verify:

1. **Identity** — canonical entity exists and is not a duplicate.
2. **Ownership** — accountable human owner and active GM/commander agent exist.
3. **Objective** — active measurable objective exists with next attack time.
4. **Tasks** — work is being generated, assigned, deduped, completed, and evidenced.
5. **Scheduler** — cron/scheduled operations have recent successful runs.
6. **Executor** — agent runs exist; tasks are not merely accumulating.
7. **Channels** — required marketing/sales/ops channels are connected or explicitly setup-required.
8. **Conversion** — CTA/offer/form/payment/booking route actually works.
9. **Observability** — incidents, errors, failures, and proof are logged.
10. **Guardrails** — external, money, legal, regulated, destructive, and cross-brand actions follow policy.
11. **Archive hygiene** — legacy/test resources are excluded without breaking active dependencies.

## Fake-Complete Flags

Mark a system NOT COMPLETE when any of these are true:
- agent row exists but no run history
- scheduled operation exists but has no successful execution
- task queue exists but is stale
- sender says enabled but connection is not ready
- website exists but conversion path is dead
- objective exists without owner/attack cadence
- dashboard says active while backend is setup-required
- archived resource still receives production traffic
- "automation" depends on a human remembering to start it

## Grade

Use:
- A = autonomous loop is demonstrably executing and self-monitoring
- B = executing with limited manual gates
- C = structure exists but meaningful manual execution remains
- D = disconnected pieces / stalled queues
- F = non-operational or dangerous

Every grade must cite evidence and list the shortest path to A.
