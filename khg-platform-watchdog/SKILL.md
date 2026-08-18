---
name: khg-platform-watchdog
description: Infrastructure and automation watchdog for the Kollective stack. Use to audit Supabase, GitHub, Vercel, deployments, Edge Functions, cron, queues, integrations, duplicate/obsolete resources, stale workflows, broken forms, and backend drift. Archive only high-confidence unused resources and preserve rollback evidence.
metadata:
  version: 1.0.0
  owner: The Kollective Hospitality Group
---

# KHG Platform Watchdog

Continuously reduce technical drag and operational attack surface.

## Canonical Control Sources

Start from:
- `platform_resource_registry`
- `enterprise_incidents`
- `scheduled_operations`
- `agent_run_log`
- `company_platform_accounts`
- `enterprise_directory_records`
- `company_execution_queue`
- Supabase advisors/logs/migrations/functions
- Vercel projects/deployments/runtime errors
- GitHub repositories/commits/CI

## Watchdog Loop

1. Detect failures, stale jobs, error spikes, disabled senders, broken forms, dead deployments, schema drift, and orphan resources.
2. Identify duplicates and temporary/probe/test infrastructure.
3. Classify each resource: `active`, `retain_readonly`, `archive_candidate`, `archived`, or `quarantined`.
4. Archive automatically only when evidence is strong and the change is reversible or the endpoint is already disabled.
5. For uncertain dependencies, quarantine/retain and open a migration task instead of deleting.
6. Verify after every change.
7. Record evidence and rollback path.

## Archive Standard

Never delete solely because a table has zero rows, an index has low usage, a repository looks old, or a deployment name looks temporary.

Require corroborating signals such as:
- canonical replacement exists
- no active dependency found
- old/empty/test naming
- no recent meaningful activity
- endpoint already disabled
- one-time purpose completed
- dependency migration completed

## Security

Treat credentials, webhook endpoints, admin RPCs, service-role functions, and cross-brand data access as high-risk. If a one-time endpoint contains embedded credentials, disable it immediately when safe and log the action.

## Output

Return:
- New incidents
- Resolved incidents
- Resources archived/quarantined
- Active technical debt
- Security findings
- Automation failures
- Evidence
- Next repair/cleanup action
