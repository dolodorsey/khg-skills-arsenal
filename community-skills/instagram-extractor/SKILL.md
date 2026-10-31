---
name: instagram-extractor
description: Public Instagram profile, post, and audience extraction via the official Instagram connector into labeled audience tables and Black Book identity matches. Public data only; no login scraping, no credential sharing, and no bypass tooling.
metadata:
  version: 1.0.0
  owner: The Kollective Hospitality Group
  source_of_truth: KOLLECTIVE BOH Supabase
  execution_mode: connector_only
  engine: instagram-connector
  related_skills: khg-ig-lead-source
---

# Instagram Extractor

You extract public Instagram data through the official Instagram connector only, into KHG's labeled audience tables. You do NOT scrape Instagram by logging in, and you do NOT use Firecrawl for Instagram. Firecrawl does not do Instagram; this skill is its counterpart, not its duplicate.

## 1. Current Architecture Only

Use only:

- The connected Instagram connector (instagram-cli), the same route that produced the existing audience tables.
- `ig_audiences` — columns: username, audience, source, added_at. Baseline verified live: 1,098,324 handles across 33 audience labels. New rows keep the same shape: one handle, one audience label, one source, one added_at.
- Labeled audience tables in the same ig_audiences style. Do not invent a new audience schema without flagging it.
- `bb_identities` with kind='ig' for Black Book identity matches.
- `public_source_entity_matches` for matched leads, with entity_key and lead_archetype.
- `khg-ig-lead-source` for lead qualification and brand isolation. This skill extracts; that skill qualifies. Do not duplicate its qualification logic here.

## 2. Extraction Workflow

1. Confirm the request names an entity_key and a lead_archetype. Never extract for a generic, unscoped request.
2. Confirm the target is public and reachable through the official connector route. If the connector returns no public data, stop; do not fall back to login scraping, a browser session, or a third-party scraper.
3. Extract only public profile, post, and audience fields the connector returns. Do not collect private, non-public, or credential-protected data.
4. Normalize each handle to a single username, assign exactly one audience label per row, and record the connector source for every row.
5. Deduplicate by username plus audience before writing. Never double-count a handle in the same audience.
6. Match handles to Black Book identities (kind='ig') where an identity match exists, and record matches in `public_source_entity_matches` with a match score and reasons. Never present an unmatched handle as a qualified lead.
7. Report actual counts: handles extracted, new handles, duplicates skipped, labels used, and identity matches created. Never report a run that did not happen.

## 3. Governance Is Law

- Public data via official connector routes only.
- No login scraping, no shared credentials, no session-cookie reuse, no auth bypass, no CAPTCHA bypass, no proxy or stealth evasion.
- HTTP 429 means stop immediately. Do not retry, do not back off and continue the same run, do not switch routes to evade the limit.
- Respect Instagram's terms and rate limits, and the connector's own limits, whichever is stricter.
- Brand-isolated: an audience extracted for one KHG entity is never reused as a lead for another entity without a new, entity-scoped match.
- Never store a handle as a lead for every brand. Extraction is not qualification.

## 4. Output Shape

Audience row (ig_audiences style):

- username: the public Instagram handle, without '@'.
- audience: one of the existing 33 labels, or a new label explicitly approved for this extraction.
- source: the connector route and source name for this extraction.
- added_at: the timestamp the row was written.

Identity match (bb_identities, kind='ig'):

- The matched handle, the KHG identity it matches, and the evidence for the match.
- No match is created on a handle alone; it requires identity evidence recorded in the match row.

## 5. Relation to Firecrawl

- `firecrawl-web-scraper` handles public web sources through the governed crawl frontier. It never handles Instagram.
- `instagram-extractor` handles public Instagram through the official connector. It never handles general web crawling.
- A lead may need both: a web source from Firecrawl and an Instagram audience from this skill, joined only through `public_source_entity_matches` and Black Book identity matches, never by merging raw tables.

## 6. Never

- Never scrape Instagram with a login, a password, a session, or a bypass tool.
- Never use Firecrawl, a generic web scraper, or a third-party Instagram scraper as a fallback.
- Never evade a rate limit, a block, or a challenge.
- Never invent handles, audiences, counts, or matches.
- Never share credentials or write a credential value anywhere.

Instagram Extractor — official connector only, public data only, labeled and matched.
