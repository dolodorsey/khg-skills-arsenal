"""KHG Firecrawl crawl worker — governed fetch engine for KOLLECTIVE BOH.

Reads an approved source from public_source_catalog, works only from
public_source_crawl_frontier, fetches with Firecrawl (or, for api_only
sources, with the official API), and logs every run in
public_source_crawl_runs with real counts.

Secrets: all from the environment only. Never hardcode a key.
  FIRECRAWL_API_KEY          Firecrawl Bearer key (env placeholder only)
  SUPABASE_URL               e.g. https://<project-ref>.supabase.co
  SUPABASE_SERVICE_ROLE_KEY  server-side key for the worker

Usage:
  python3 firecrawl_crawl_worker.py --source-key crossref-public-metadata --limit 1
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

FIRECRAWL_BASE = "https://api.firecrawl.dev"
UA = "KHG-Firecrawl-Worker/1.0"
HANDLE_RE = re.compile(r"@[A-Za-z0-9_.]{2,30}")
STOP_STATUSES = {401, 403, 429}


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def http_json(method, url, headers=None, body=None, timeout=60):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    if body is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", "replace")
            return resp.status, json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        try:
            return e.code, json.loads(raw) if raw else {"error": raw}
        except ValueError:
            return e.code, {"error": raw}


class Supabase:
    def __init__(self):
        self.url = os.environ.get("SUPABASE_URL", "").rstrip("/")
        self.key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
        self.enabled = bool(self.url and self.key)

    def headers(self):
        return {"apikey": self.key, "Authorization": f"Bearer {self.key}"}

    def get(self, table, query):
        url = f"{self.url}/rest/v1/{table}?{query}"
        status, data = http_json("GET", url, self.headers())
        if status >= 300:
            raise RuntimeError(f"Supabase GET {table} failed: {status} {data}")
        return data

    def post(self, table, row):
        url = f"{self.url}/rest/v1/{table}"
        status, data = http_json("POST", url, self.headers(), row)
        if status >= 300:
            raise RuntimeError(f"Supabase POST {table} failed: {status} {data}")
        return data

    def patch(self, table, query, row):
        url = f"{self.url}/rest/v1/{table}?{query}"
        status, data = http_json("PATCH", url, self.headers(), row)
        if status >= 300:
            raise RuntimeError(f"Supabase PATCH {table} failed: {status} {data}")
        return data


def same_domain(url, domain):
    host = urllib.parse.urlparse(url).netloc.lower().split(":")[0]
    return host == domain.lower() or host.endswith("." + domain.lower())


def robots_allows(url, domain):
    robots_url = f"https://{domain}/robots.txt"
    try:
        with urllib.request.urlopen(robots_url, timeout=15) as resp:
            text = resp.read().decode("utf-8", "replace")
    except Exception:
        return True
    path = urllib.parse.urlparse(url).path or "/"
    in_star = False
    for line in text.splitlines():
        line = line.strip()
        if line.lower().startswith("user-agent:"):
            in_star = line.split(":", 1)[1].strip() in ("*", "")
        elif in_star and line.lower().startswith("disallow:"):
            rule = line.split(":", 1)[1].strip()
            if rule and path.startswith(rule.rstrip("*")):
                return False
    return True


def firecrawl_scrape(api_key, url):
    headers = {"Authorization": f"Bearer {api_key}", "User-Agent": UA}
    status, data = http_json("POST", f"{FIRECRAWL_BASE}/v2/scrape", headers,
                             {"url": url, "formats": ["markdown", "links"]})
    if status in STOP_STATUSES:
        raise RuntimeError(f"Firecrawl stopped with HTTP {status}; aborting run.")
    if status >= 300 or not data.get("success", True):
        raise RuntimeError(f"Firecrawl scrape failed: {status} {data}")
    payload = data.get("data", data)
    return payload.get("markdown", ""), payload.get("links", [])


def crossref_fetch(limit):
    url = f"https://api.crossref.org/works?rows={limit}&select=DOI,title,author"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode())
    items = data.get("message", {}).get("items", [])
    return len(items)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-key", required=True)
    ap.add_argument("--limit", type=int, default=1)
    ap.add_argument("--entity-key", default=None)
    ap.add_argument("--lead-archetype", default=None)
    args = ap.parse_args()
    started = now_iso()
    sb = Supabase()
    firecrawl_key = os.environ.get("FIRECRAWL_API_KEY", "")
    counts = {"pages_discovered": 0, "pages_fetched": 0, "pages_skipped": 0,
              "usernames_found": 0, "unique_usernames": 0}
    usernames = set()
    errors = []
    source = None
    status = "completed"
    mode = "firecrawl"
    start_url = None
    try:
        if not sb.enabled:
            print("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are required.", file=sys.stderr)
            return 2
        rows = sb.get("public_source_catalog",
                      f"source_key=eq.{urllib.parse.quote(args.source_key)}&select=id,source_key,root_url,domain,access_mode,terms_status,min_delay_seconds,max_pages_per_run")
        if not rows:
            raise RuntimeError(f"Source not found in public_source_catalog: {args.source_key}")
        source = rows[0]
        start_url = source.get("root_url")
        delay = float(source.get("min_delay_seconds") or 2)
        cap = int(source.get("max_pages_per_run") or args.limit)
        limit = min(args.limit, cap)
        safe = sb.get("v_public_sources_safe_to_crawl", f"id=eq.{source['id']}&select=id")
        api_only = source.get("access_mode") == "api_only" and source.get("terms_status") == "allowed"
        if not safe and not api_only:
            raise RuntimeError("Source is not in v_public_sources_safe_to_crawl and is not an allowed api_only source; refusing to crawl.")
        if api_only:
            mode = "api"
            fetched = crossref_fetch(limit)
            counts["pages_fetched"] = fetched
            counts["pages_discovered"] = fetched
            counts["usernames_found"] = 0
            counts["unique_usernames"] = 0
            print(f"api_only fetch: {fetched} items from Crossref official API (metadata, not usernames).")
        else:
            if not firecrawl_key:
                status = "blocked"
                errors.append("FIRECRAWL_API_KEY is not set; no fetch attempted.")
                print("FIRECRAWL_API_KEY is not set; failing closed.", file=sys.stderr)
            else:
                frontier = sb.get("public_source_crawl_frontier",
                                  f"source_id=eq.{source['id']}&status=eq.pending&order=available_at.asc&limit={limit}&select=id,url,canonical_url")
                if not frontier:
                    sb.post("public_source_crawl_frontier", {
                        "source_id": source["id"], "url": start_url,
                        "canonical_url": start_url, "discovered_from": "catalog",
                        "depth": 0, "status": "pending"})
                    frontier = sb.get("public_source_crawl_frontier",
                                      f"source_id=eq.{source['id']}&status=eq.pending&limit={limit}&select=id,url,canonical_url")
                for row in frontier:
                    url = row["url"]
                    if not same_domain(url, source["domain"]) or not robots_allows(url, source["domain"]):
                        counts["pages_skipped"] += 1
                        sb.patch("public_source_crawl_frontier", f"id=eq.{row['id']}", {"status": "skipped"})
                        continue
                    time.sleep(delay)
                    markdown, links = firecrawl_scrape(firecrawl_key, url)
                    found = HANDLE_RE.findall(markdown or "")
                    usernames.update(found)
                    counts["pages_fetched"] += 1
                    sb.patch("public_source_crawl_frontier", f"id=eq.{row['id']}",
                             {"status": "fetched", "last_http_status": 200})
                    seen = sb.get("public_source_crawl_frontier",
                                  f"source_id=eq.{source['id']}&select=canonical_url")
                    known = {r.get("canonical_url") for r in seen}
                    for link in links or []:
                        if same_domain(link, source["domain"]) and link not in known:
                            sb.post("public_source_crawl_frontier", {
                                "source_id": source["id"], "url": link,
                                "canonical_url": link, "discovered_from": url,
                                "depth": 1, "status": "pending"})
                            counts["pages_discovered"] += 1
                            known.add(link)
                counts["usernames_found"] = len(usernames)
                counts["unique_usernames"] = len(usernames)
    except Exception as exc:
        status = "failed" if status == "completed" else status
        errors.append(str(exc))
        print(f"Run failed: {exc}", file=sys.stderr)
    finally:
        if sb.enabled and source:
            row = {
                "source_id": source["id"], "entity_key": args.entity_key,
                "lead_archetype": args.lead_archetype, "start_url": start_url,
                "crawl_mode": mode, "status": status,
                "pages_discovered": counts["pages_discovered"],
                "pages_fetched": counts["pages_fetched"],
                "pages_skipped": counts["pages_skipped"],
                "usernames_found": counts["usernames_found"],
                "unique_usernames": counts["unique_usernames"],
                "started_at": started, "completed_at": now_iso(),
                "error_summary": "; ".join(errors)[:1000] if errors else None,
                "metadata": {"engine": "firecrawl", "worker": "firecrawl_crawl_worker.py"},
            }
            try:
                sb.post("public_source_crawl_runs", row)
            except Exception as exc:
                print(f"Could not log run: {exc}", file=sys.stderr)
    print(json.dumps({"source_key": args.source_key, "status": status, **counts}))
    return 0 if status == "completed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
