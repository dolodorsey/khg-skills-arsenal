---
name: khg-event-command
description: Autonomous event command skill for one exact Kollective event or event series. Use for countdown attacks, ticket/table sales, vendor/sponsor pipeline, promotion, production, staffing, guest experience, day-of readiness, closeout, and retention. Keep each event and series isolated unless explicitly coordinated.
metadata:
  version: 1.0.0
  owner: The Kollective Hospitality Group
---

# KHG Event Command

Own one event from objective to closeout.

## Event Preflight

Resolve the exact event entity in `enterprise_directory_records`. Load:
- current event objective
- event/channel plans
- commerce offers and ticket/reservation paths
- calendar event/date/location
- sponsor/vendor/application records when available
- staffing/resource requirements
- creative/assets
- sender/social readiness
- open tasks/incidents

Never substitute another event in the same series.

## Countdown Attack

Attack these lanes every day as the event approaches:

1. **Revenue** — tickets, tables, sponsors, vendors, deposits, upsells.
2. **Velocity** — actual pace vs required pace and deadline.
3. **Promotion** — content, email, SMS, ambassadors, partners, media, retargeting.
4. **Experience** — programming, talent, run-of-show, guest journey, VIP, hospitality.
5. **Production** — sound, lighting, staging, screens, power, load-in, technical redundancy.
6. **Operations** — venue, permits, security, staffing, parking, check-in, POS, supplies.
7. **Risk** — weather, safety, compliance, payment, capacity, vendor or talent failure.
8. **Closeout** — settlement, data capture, content, feedback, retention, next event conversion.

## Milestone Logic

Use event-specific backend cadence when present. Otherwise establish explicit milestone attacks based on the actual event date; do not invent a date.

## Evidence Standard

Do not mark ready because a plan exists. Verify live URLs, payment paths, inventory, confirmed people/resources, approved creative, and deployment state.

## Output

Return:
- Event objective/date
- Revenue/velocity status
- Readiness score by lane
- What moved
- Critical blockers
- Assigned agent/human
- Evidence
- Next 3 event moves
- Next countdown attack
