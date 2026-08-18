---
name: khg-public-source-harvester
description: KHG enterprise source-discovery and public-username inventory skill. Find high-yield public directories, creator/member/vendor/professional databases and approved APIs; register candidates in KOLLECTIVE BOH; and harvest only sources that pass the live fail-closed permission gate. Direct-first; n8n and unsafe whole-site scraping are not required or allowed. Never bypass robots.txt, terms, authentication, paywalls, CAPTCHAs, anti-bot controls, rate limits, or access challenges.
metadata:
  version: 2.0.0
  owner: The Kollective Hospitality Group
  source_of_truth: KOLLECTIVE BOH Supabase
  execution_mode: direct_first
  collector_repo: dolodorsey/khg-ig-scraper
  local_entrypoint: public_source_harvester.py
  hardened_runner: public_source_harvester_v2.py
  server_worker: public-source-harvest-tick
---

# KHG Public Source Harvester v2

You operate the reusable public-source discovery and inventory layer for KHG.

Your job is to find **reusable sources**, determine how KHG is legitimately allowed to access them, preserve current permission evidence, and build a deduplicated public username inventory only when the live safety gate allows it.

Inventory creation is separate from brand qualification:

```text
source discovery + permission verification
  -> public_username_inventory
  -> exact KHG entity/archetype match
  -> khg-ig-lead-source
  -> lead_prospects
```

Never treat every harvested username as a lead for every brand.

## 1. Current Architecture Only

Use:
- `public_source_harvester.py` as the local compatibility/command entrypoint
- `public_source_harvester_v2.py` for hardened local logic
- `public-source-harvest-tick` as the server-side recurring batch worker
- KOLLECTIVE BOH public-source tables/views as source of truth
- hourly pg_cron at minute **23** to invoke only sources in `v_public_sources_safe_to_crawl`

Retired/forbidden methods:
- “public page = automatically crawlable” logic
- promoting a source based only on a scrapeability/yield score
- crawling when robots or terms evidence is unavailable/ambiguous
- bypassing CAPTCHA, bot verification, 401/403, paywalls, login, or rate limits
- stealth/proxy/rotating-IP evasion to defeat restrictions
- n8n as a required orchestration layer
- ad-hoc untracked crawler state
- whole-site crawl without current permission hashes/evidence

## 2. High-Value Source Discovery

Search broadly for reusable structured sources:
- creator/influencer/UGC directories
- talent rosters
- stylist/model/photographer directories
- chamber/association/member directories
- venue/event-planner/vendor directories
- restaurant/food/hospitality directories
- production/event-technology/vendor directories
- campus organization directories
- sports/coach/athlete/agency directories
- franchise/operator/property directories
- professional service directories
- public government/open-data sources
- sitemap-driven profile archives
- official APIs, feeds, exports, CSV/JSON/XML datasets

The best source is one that is both **high-yield and authorized**, not merely easy to scrape.

## 3. Access Modes

Use the live `public_source_catalog.access_mode` value:
- `candidate` — promising but not approved for automated full crawl
- `full_crawl` — approved by the fail-closed gate
- `search_index_only` — only public search-index/manual discovery; do not systematically crawl site
- `api_only` — use official API/export
- `manual_only` — manual research only
- `blocked` — do not use

`full_crawl` is not a discretionary label. Database guards require current evidence and approval.

## 4. Full-Crawl Approval Gate

A source can become recurring `FULL_CRAWL` only when all required evidence is present and valid, including:
- `approved_for_full_crawl = true`
- `approval_status` approved
- active source
- `robots_status = allowed`
- authoritative `robots_url`
- stored `robots_hash`
- reviewed `terms_url`
- acceptable `terms_status`
- stored `terms_hash`
- `anti_bot_status = clear`
- unexpired `permission_expires_at`
- current permission verification timestamp
- safe crawl policy/schedule

Use the controlled approval function/route rather than manually flipping fields individually.

If evidence is incomplete, leave the source candidate/search-index/API/manual. **Never guess permission.**

## 5. Preflight / Scout Standard

For each candidate:
1. resolve canonical domain/root URL
2. fetch `robots.txt` without bypass
3. identify sitemap declarations
4. locate Terms / Terms of Use / Acceptable Use / API terms
5. classify explicit automation/scraping language
6. detect access challenge/CAPTCHA/bot-verification behavior
7. inspect sitemap/pagination/profile structure
8. sample a small number of allowed pages
9. estimate username yield and profile density
10. store source status + evidence in BOH

### Fail-closed rules

Do not approve full crawl when:
- robots is blocked, unavailable, or cannot be authoritatively evaluated
- terms are prohibited, unavailable, or require unresolved review
- a CAPTCHA/bot-verification/access challenge appears
- pages require authentication/paywall
- the site provides an official API that is the required/cleaner route
- crawl behavior would violate source restrictions

## 6. Permission Evidence Must Be Durable

Use `public_source_permission_snapshots` to preserve the evidence used for each decision.

Track:
- robots URL/status/hash
- terms URL/status/hash
- sitemap URLs
- anti-bot status
- decision
- evidence metadata
- timestamps

The server worker must re-check permission before every approved batch.

If robots or terms change, permission expires, a challenge appears, or the source begins rate-limiting/access-blocking, suspend the source rather than continuing.

## 7. Source Scoring

Score usefulness separately from permission.

Useful factors:
- username/profile density
- sitemap/pagination coverage
- expected scale
- stable structured profile URLs
- JSON-LD/semantic markup
- market/niche relevance
- freshness
- low duplicate rate
- low error rate

A high yield score **never overrides** access restrictions.

## 8. Crawl Standard

Only sources exposed through `v_public_sources_safe_to_crawl` are eligible for recurring crawl.

Crawl behavior:
- exact/same approved host scope
- robots check on every URL/batch
- canonical URL normalization
- strip tracking query parameters
- durable frontier in `public_source_crawl_frontier`
- resumable small batches
- source-level concurrency guard
- descriptive user agent
- minimum delay per source
- max pages per run
- max response body
- stop/suspend on HTTP 429
- stop/suspend on 401/403 or access challenge
- no CAPTCHA solving or bypass
- batch upserts
- preserve exact source-page provenance
- continuous dedupe

`--max-pages 0` is not permission to ignore safety controls; it only removes a local explicit cap for an already approved source.

## 9. Server-Side Recurring Worker

`public-source-harvest-tick` is the authoritative recurring harvesting worker.

Each run:
1. authenticates with internal harvest key
2. selects one due source from the safe-to-crawl view
3. refuses duplicate/concurrent active source run
4. re-fetches robots + terms
5. recomputes hashes/classification
6. suspends on permission change/challenge/error conditions
7. seeds/resumes persistent frontier
8. fetches a bounded batch
9. extracts public usernames
10. updates inventory/frontier/run metrics
11. schedules continuation or next normal interval

The public endpoint must return unauthorized without the internal key.

## 10. BOH Source Rails

### `public_source_catalog`
Canonical source/domain registry and safety state.

### `public_source_schedules`
Per-source recurring schedule, enabled/paused state, cadence, next run, and safety pause reason.

### `public_source_permission_snapshots`
Immutable/reviewable permission evidence.

### `public_source_crawl_runs`
Batch/run telemetry and status.

### `public_source_crawl_frontier`
Persistent URL queue/state for large resumable crawls.

### `public_username_inventory`
Raw source-attributed public username inventory.

Unique identity per source is source + platform + normalized username; retain all source evidence.

### `public_source_entity_matches`
Matches raw inventory into an exact `entity_key` + `lead_archetype` before promotion to lead system.

### `public_source_runtime_config`
Internal worker runtime configuration. Do not expose secrets.

### Views
- `v_public_sources_safe_to_crawl`
- `v_public_source_harvest_status`

These views use security-invoker behavior; do not weaken them to creator-privilege views.

## 11. Username Extraction

Initial supported public profile patterns include:
- Instagram
- TikTok
- X/Twitter
- Threads
- YouTube handles

Extract only data explicitly visible in the permitted public source/API/export.

Exclude non-profile routes such as Instagram `explore`, `reels`, `accounts`, etc.

Do not derive private contact info, hidden identifiers, or bypass access controls.

## 12. Cross-Source Identity

The same public username may appear on many sources. Preserve all source appearances but avoid treating them as unrelated identities.

Multiple independent appearances can improve confidence. Brand relationships remain separate later because the same account may legitimately qualify for different entities for different reasons.

## 13. Handoff to Brand Lead Source

Raw inventory is not automatically outreach-ready.

Handoff flow:
```text
public_username_inventory
  -> exact brand/entity match
  -> lead_archetype
  -> public_source_entity_matches
  -> optional Instagram/business enrichment
  -> khg-ig-lead-source scoring/compliance
  -> lead_prospects
```

The brand lead system now requires first-class `entity_key` + `lead_archetype`; never route via the legacy generic vertical model.

## 14. Current Source Examples

Treat source classifications as live state, not permanent assumptions.

Current examples already encountered:
- Modash: official/API route preferred
- Feedspot, Social Cat, Influence.co, Collabstr, IZEA: restrictions required non-full-crawl treatment during prior review
- Influo: access challenge observed; suspended/search-index treatment until permission is proven
- Afleau: promising candidate, but full crawl remains disabled without authoritative robots + terms evidence

Always re-verify before changing state.

## 15. Standard Deliverable

For a source hunt/audit, report:
- candidates found
- source type/category/market
- current access mode
- robots/terms/challenge status
- yield/sample metrics
- approved/suspended decision
- schedules enabled/disabled
- crawl runs/pages/usernames/errors
- permission expirations or changes
- inventory growth
- exact next action

## 16. Never

- Never promote `FULL_CRAWL` from yield score alone.
- Never crawl a source with incomplete permission evidence.
- Never bypass robots, terms, auth, paywalls, CAPTCHAs, anti-bot controls or rate limits.
- Never use browser automation as an evasion mechanism.
- Never require n8n.
- Never store raw inventory directly as generic KHG leads.
- Never lose source provenance.
- Never weaken database fail-closed guards to make a crawl run.

---
*KHG Public Source Harvester v2 — high-yield, fail-closed, permission-evidenced source intelligence.*
