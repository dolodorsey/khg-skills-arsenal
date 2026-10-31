---
name: firecrawl-web-scraper
description: Public web scraping and extraction into the KHG crawl frontier — venues, sponsors, providers, and public sources — using Firecrawl as the fetch engine for the existing governed crawl system. Fail-closed; never bypass robots.txt, terms, authentication, paywalls, CAPTCHAs, anti-bot controls, or rate limits.
metadata:
  version: 1.0.0
  owner: The Kollective Hospitality Group
  source_of_truth: KOLLECTIVE BOH Supabase
  execution_mode: governed_first
  engine: firecrawl
  worker: firecrawl_crawl_worker.py
  related_skills: khg-public-source-harvester
---

# Firecrawl Web Scraper

You operate the Firecrawl fetch engine for the existing KHG governed crawl system. You do NOT build a parallel system. The source of truth is KOLLECTIVE BOH Supabase, project ref wfkohcwxxsrhcxhepfql.

## 1. Current Architecture Only

Use only:

- `public_source_catalog` — canonical source and domain registry and safety state.
- `v_public_sources_safe_to_crawl` — the only eligibility gate for recurring full crawl.
- `public_source_crawl_frontier` — persistent, resumable URL queue and per-URL state.
- `public_source_crawl_runs` — batch and run telemetry: status, pages_discovered, pages_fetched, pages_skipped, usernames_found, unique_usernames, error_summary, metadata.
- `public_source_schedules` and `public_source_runtime_config` — schedule and runtime policy.
- `lead_import_staging` — landing table for extracted people and organization rows that need a landing place before promotion.
- `public_source_entity_matches` — matched leads, with entity_key and lead_archetype, before promotion.
- Black Book dedupe path: `bb_people` and `bb_organizations`.
- The worker in this folder: `firecrawl_crawl_worker.py`.

Do not use `marketing_drive_crawl_staging` for web crawls. It is Google Drive only.

This skill is the missing ENGINE skill. It does not duplicate `khg-public-source-harvester` (discovery and permission evidence) or `khg-ig-lead-source` (Instagram lead sourcing and qualification). Those skills call this engine; this engine does not replace their gates.

## 2. Governance Is Law

- Respect `robots.txt` and the source's `crawl_policy`, `min_delay_seconds`, and `max_pages_per_run`.
- Same-domain only. Never follow a crawl off the approved host scope.
- No auth bypass, no paywall bypass, no CAPTCHA bypass, no bot-verification bypass, no stealth, proxy, or rotating-IP evasion.
- Stop and suspend on HTTP 429, 401, 403, or any access challenge. Never retry past a rate limit.
- Prefer official APIs and datasets where they exist. For an `api_only` source, use the official API, never Firecrawl scraping.
- Never crawl a source with incomplete, expired, or ambiguous permission evidence. Never promote a source to full crawl from a yield score alone.
- Never store raw inventory directly as generic KHG leads. Preserve exact source-page provenance on every row.

## 3. Worker Workflow

Run `firecrawl_crawl_worker.py`:

1. Read the source from `public_source_catalog` by `--source-key`.
2. Refuse unless the source is in `v_public_sources_safe_to_crawl` (full crawl) or is `api_only` with `terms_status = allowed`.
3. Read or seed due URLs from `public_source_crawl_frontier`, bounded by `max_pages_per_run`.
4. Fetch one bounded batch, waiting at least `min_delay_seconds` between requests for that source.
5. For full-crawl sources, call Firecrawl (section 4). For `api_only` sources, call the official API.
6. Update frontier status per URL, upsert extracted rows to `lead_import_staging` where applicable, and insert one `public_source_crawl_runs` row with real counts.
7. Report actual pages fetched, skipped, usernames found, errors, and the next action. Never report a run that did not happen.

## 4. Firecrawl Calls

Base URL: `https://api.firecrawl.dev`. Authentication: Bearer token read only from the environment variable `FIRECRAWL_API_KEY`. Never hardcode a key, never invent a key, never commit a key, and never paste a key into chat, a file, or a commit message.

- Scrape one URL: `POST /v2/scrape` with `formats: ["markdown", "links"]`.
- Crawl a site: `POST /v2/crawl`, then poll the returned job until it completes, fails, or times out.
- Structured extraction: `POST /v2/extract` with an explicit schema for venues, sponsors, or providers.
- Discovery only: `POST /v2/map` to list URLs; mapping is not fetching.

These map to the Firecrawl CLI commands `firecrawl scrape`, `firecrawl crawl`, and `firecrawl map`, documented in the repo's existing `firecrawl-cli/README.md` and `firecrawl-cli/skills/` (firecrawl-scrape, firecrawl-crawl, firecrawl-map, firecrawl-search, firecrawl-agent, firecrawl-download, firecrawl-browser, firecrawl-cli). Use the API in the worker so frontier state and run logging are enforced; the CLI alone does not log to `public_source_crawl_runs` and is not a governed run.

## 5. Official Firecrawl Skill and CLI — What Was Adopted

Evaluated: Firecrawl's official agent skill `firecrawl-build` (`npx skills add firecrawl/skills --skill firecrawl-build`) and the CLI setup command (`npx -y firecrawl-cli@latest setup build --browser`).

Adopted:

- The official endpoint and command patterns in section 4, and the CLI's markdown-plus-links scrape pattern.
- The CLI's env-var convention: the key is supplied as `FIRECRAWL_API_KEY` in the environment, never in code.
- The existing repo `firecrawl-cli` skills as reference, cross-referenced here instead of duplicated.

Not adopted as a production path:

- `firecrawl-build` was not installed into this repo and is not the governed worker. A generic build skill does not enforce the frontier, the safe-to-crawl view, same-domain scope, crawl policy, or run logging.
- Interactive CLI browser login is a local-exploration option only. It stores credentials on the operator's machine and must never be committed. A CLI run that is not logged in `public_source_crawl_runs` is not a KHG crawl run.
- The founder's Firecrawl key lives only in Muse's secure connector storage (`custom.firecrawl`) for verification. The worker reads only the `FIRECRAWL_API_KEY` environment variable; it never reads connector storage directly and never prints a key.

## 6. Test Source: Crossref Public Metadata

Already catalogued, verified live:

- `source_key`: `crossref-public-metadata`
- Name: Crossref Public Metadata REST API / Annual Data File
- `root_url`: `https://www.crossref.org/documentation/retrieve-metadata/`
- Domain: `crossref.org`; `source_type`: `professional_research_metadata`
- `access_mode`: `api_only`; `terms_status`: `allowed`; `scrapeability_score`: 95
- `min_delay_seconds`: 2; `max_pages_per_run`: 25
- Policy note begins: API/DATASET ONLY. Use the public REST/OAI/annual public data file within current rate limits.

Proof of life for this source must use the official Crossref API (`https://api.crossref.org`) through the same worker path, not Firecrawl scraping, and must be logged in `public_source_crawl_runs` with real counts. At the time of this build, no such run exists (0 runs, 0 frontier rows, 0 safe-to-crawl sources in the live tables), and the Firecrawl verification call is pending the founder-side connector confirmation. Do not claim a test crawl until that verification run is logged.

## 7. Environment

Required at run time, from the environment only:

- `FIRECRAWL_API_KEY` — Firecrawl Bearer key. Missing key means fail closed: no fetch, exit non-zero, and, if Supabase is configured, log a `blocked` run with 0 counts and an error summary naming the missing variable. A blocked run is never a completed run.
- `SUPABASE_URL` — KOLLECTIVE BOH Supabase URL.
- `SUPABASE_SERVICE_ROLE_KEY` — server-side key for the worker. Never commit it.

Example (key supplied by the environment, never written here):

```
python3 firecrawl_crawl_worker.py --source-key crossref-public-metadata --limit 1
```

## 8. Never

- Never bypass robots, terms, auth, paywalls, CAPTCHAs, anti-bot controls, or rate limits.
- Never crawl off-domain, never crawl Instagram with this skill (use `instagram-extractor`), and never treat a public page as automatically crawlable.
- Never weaken database fail-closed guards to make a crawl run.
- Never invent evidence, contact data, counts, or a run.
- Never write a key value anywhere.

Firecrawl Web Scraper — governed fetch engine only, fail-closed, evidence-logged.
