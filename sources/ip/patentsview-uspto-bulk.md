<!-- recovered from agent-a569e106a2dbfe13c.jsonl on 2026-08-06 after the original agent died on an API connection error (FailedToOpenSocket) following 100 tool calls at 2026-08-06T00:26:34 – 00:31:xx UTC -->

# PatentsView / USPTO Bulk & Open Patent Data — Technical Reference

**For:** rare-disease drug repurposing company screening off-patent and never-US-approved drugs.
**Date verified:** 2026-08-06 (newly verified fetches so noted).
**Relevance split:** Funnel A candidates (never-approved-in-US moiety, 505(b)(1), PRV-eligible) need
freedom-to-operate searches and prior-art dossiers. Funnel B candidates (US generic / 505(b)(2),
orphan-only) also need assignee and citation data for FTO and licensing.

---

## 1. Infrastructure Overview — The 2024–2026 Migration

### What happened

**PatentsView**, the NIH/USPTO-funded patent data platform, has been absorbed into the USPTO Open
Data Portal (ODP) at `data.uspto.gov`. The migration has three observable effects:

| Old address | Current state | Evidence |
|---|---|---|
| `api.patentsview.org/patents/query` | HTTP 301 → `data.uspto.gov/support/transition-guide/patentsview` | Verified 2026-08-06: `HTTP/2 301`, `location: https://data.uspto.gov/support/transition-guide/patentsview` |
| `patentsview.org/download/data-download-tables` | HTTP 301 → same ODP transition page | Verified 2026-08-06: `HTTP/2 301` via curl |
| `search.patentsview.org` | **NXDOMAIN** — dead | Verified 2026-08-06: `NXDOMAIN` from local resolver (128.103.1.1), Google (8.8.8.8), and Cloudflare (1.1.1.1) |
| `querytoolapi.patentsview.org` | **NXDOMAIN** — dead | Verified 2026-08-06 |
| `data.patentsview.org` (S3) | No response / 403 | Verified 2026-08-06: `s3.amazonaws.com/data.patentsview.org` → HTTP 403; bare domain → no response |
| `data.uspto.gov` | **Live** — resolves via CloudFront | Verified 2026-08-06: CNAME → `d16d88cv7ff8up.cloudfront.net`, IPs 13.33.82.x |
| `ped.uspto.gov` (PEDS) | **NXDOMAIN** | Verified 2026-08-06 |
| `bulkdata.uspto.gov` | **NXDOMAIN** | Verified 2026-08-06 |
| `ptabdata.uspto.gov` | No response (HTTP 000) | Verified 2026-08-06 |
| `developer.uspto.gov` | HTTP 301 → `data.uspto.gov:443/` | Verified 2026-08-06 |

**Key constraint:** `data.uspto.gov` is an Angular SPA protected by AWS WAF with a JS challenge
(`0dd6fc7fe1e2.edge.sdk.awswaf.com`). Every URL path — including `/api/v1/patent/`, `/data.json`,
`/datasets/patentsview/`, `/ptab-api/v2/trials` — returns the same 20,666-byte HTML shell to
non-browser clients. All curl-based automation of the ODP UI itself fails. The underlying REST
APIs must be accessed at their own base hosts or via documented SDK paths.

---

## 2. PatentSearch API (formerly PatentsView Search API)

### 2a. Current API host and key status

As of Wayback Machine CDX records (last capture: March 2026), the PatentSearch API was live at:

```
https://search.patentsview.org/api/v1/
```

Wayback CDX recorded **HTTP 403** responses from `search.patentsview.org/api/v1/` in
March 2026, which is the correct response when a valid `X-Api-Key` header is missing.
The host went **NXDOMAIN** between March 2026 and August 2026 (exact date not captured in CDX).

**Whether the API has migrated to a new host on data.uspto.gov is UNVERIFIED** — every path tested
on `data.uspto.gov` returns the SPA shell, and no successor hostname resolves. This is the most
important open question; see §8 (Unfinished).

### 2b. Authentication (verified from archived docs)

Source: Wayback snapshot of `search.patentsview.org/docs/docs/Search%20API/SearchAPIReference/`
captured 2024-04-16, confirmed still current in 2025-05-22 capture.

- **Required header:** `X-Api-Key: {your_key}`
- **How to obtain:** Submit request via the PatentsView Help Center
  (`https://patentsview.org/` → Help Center). One key per user/email. Keys do not expire
  (but documentation notes this policy may change with notice).
- **Rate limit:** **45 requests/minute** per key. HTTP 429 on excess; use `Retry-After` header.
- Keys cannot be shared or duplicated; multiple simultaneous keys → access revoked.
- Released in v2.1.2 (Aug 2024): "backend improvements to key-request workflow."
- License on API data: **Creative Commons Attribution 4.0** (explicitly applied in v2.3.2,
  April 2025).

### 2c. Request structure

Both `GET` and `POST` supported on all endpoints. Parameters:

| Parameter | Symbol | Notes |
|---|---|---|
| Query filter | `q` | Mandatory; JSON object; supports `_eq _neq _gt _gte _lt _lte _begins _contains _text_all _text_any _text_phrase _not _and _or` |
| Field list | `f` | Optional JSON array; defaults apply per endpoint |
| Sort | `s` | Optional JSON array of `{"field":"asc|desc"}` objects |
| Options/pagination | `o` | Optional; controls `per_page` (max 1,000), `page`, `after`, `pad_patent_id`, `exclude_withdrawn` |

Default page size: **100 records**. Maximum: **1,000 records per request**. Use `after`-based
cursor pagination for large result sets.

Response structure always:
```json
{
  "error": "boolean",
  "count": "integer",
  "total_hits": "integer",
  "<entity>": [...]
}
```

HTTP status codes: 200 success, 400 bad request (check `X-Status-Reason` header), 404 not found,
429 rate limit, 500 server error.

Example query (from archived docs — endpoint may no longer resolve):
```
GET https://search.patentsview.org/api/v1/patent/?q={"patent_id":"7861317"}
Header: X-Api-Key: {key}
```

### 2d. Endpoint inventory

Source: Wayback snapshot of Endpoint Dictionary page
(`search.patentsview.org/docs/docs/Search%20API/EndpointDictionary/`), captured 2025-06-20.
All at base path `/api/v1/`:

**Granted patent endpoints:**
- `GET/POST /api/v1/patent/` — granted patents; key fields: `patent_id`, `patent_title`,
  `patent_date`, `patent_type`, `patent_abstract`, `patent_num_times_cited_by_us_patents`,
  `gov_interest_statement`; nested: `applicants`, `application`, `assignees`, `attorneys`,
  `cpc_at_issue`, `cpc_current`, `examiners`, `inventors`, `ipcr`, `pct_data`, `us_term_of_grant`,
  `uspc_at_issue`, `wipo`
- `GET/POST /api/v1/patent/us_patent_citation/` — forward and backward US citations
- `GET/POST /api/v1/patent/us_application_citation/` — citations to pre-grant publications
- `GET/POST /api/v1/patent/foreign_citation/` — foreign patent citations
- `GET/POST /api/v1/patent/other_reference/` — NPL citations (corrected from `otherreference` in v2.2)
- `GET/POST /api/v1/patent/rel_app_text/` — related application text

**Pre-grant publication endpoints (added v2.0, Feb 2024):**
- `GET/POST /api/v1/publication/` — pregrant publication data
- `GET/POST /api/v1/publication/rel_app_text/` — related application data for pregrant

**Text endpoints (added v2.1.0; separated granted/pregrant in v2.2.0):**
- `GET/POST /api/v1/g_brf_sum_text/` — granted brief summary text
- `GET/POST /api/v1/g_claim/` — granted claims
- `GET/POST /api/v1/g_detail_desc_text/` — granted description text
- `GET/POST /api/v1/g_draw_desc_text/` — granted drawing description
- `GET/POST /api/v1/pg_brf_sum_text/` — pregrant brief summary text
- `GET/POST /api/v1/pg_claim/` — pregrant claims
- `GET/POST /api/v1/pg_detail_desc_text/` — pregrant description text
- `GET/POST /api/v1/pg_draw_desc_text/` — pregrant drawing description
- `GET/POST /api/v1/claim/` (beta) — claims endpoint
- `GET/POST /api/v1/brf_sum_text/` (beta) — brief summary
- `GET/POST /api/v1/detail_desc_text/` (beta) — detail description
- `GET/POST /api/v1/draw_desc_text/` (beta) — drawing description

**Common entity endpoints (lookup by ID supported):**
- `GET/POST /api/v1/assignee/{assignee_id}/`
- `GET/POST /api/v1/attorney/`
- `GET/POST /api/v1/inventor/{inventor_id}/`
- `GET/POST /api/v1/location/{location_id}/`

**Classification endpoints (500 errors fixed in v2.3.1):**
- `GET/POST /api/v1/cpc_class/`
- `GET/POST /api/v1/cpc_subclass/`
- `GET/POST /api/v1/cpc_group/`
- `GET/POST /api/v1/ipc/`
- `GET/POST /api/v1/uspc_mainclass/`
- `GET/POST /api/v1/uspc_subclass/`
- `GET/POST /api/v1/wipo/`

### 2e. Version history / data currency

| Version | Date | Data through | Key changes |
|---|---|---|---|
| 2.0 | Feb 2024 | 2023-12-31 | Pre-grant publication endpoints added |
| 2.1.0 | Mar 2024 | — | Text endpoints added |
| 2.1.1 | Apr 2024 | — | New publication fields |
| 2.1.2 | Aug 2024 | 2024-06-30 | API key workflow streamlined; renamed to PatentSearch API |
| 2.1.3 | Aug 2024 | — | Naming update only |
| 2.2.0 | Nov 2024 | 2024-09-30 | Text endpoints split granted/pregrant; classification bug fixes |
| 2.3.0 | Feb 2025 | 2024-12-31 | `pad_patent_id` option; `exclude_withdrawn` option; gender code; assignee/inventor location_id |
| 2.3.1 | Mar 2025 | — | Classification 500-error fixes (cpc_subclass, uspc_mainclass, uspc_subclass, wipo) |
| 2.3.2 | Apr 2025 | — | Endpoint Dictionary page added; CC BY 4.0 explicitly applied to API data |

API updated **quarterly** (data cut dates: 06/30, 09/30, 12/31, 03/31).

### 2f. Swagger UI

Archived at: `https://search.patentsview.org/swagger/` — returns ECONNREFUSED now (verified
2026-08-06). An archived Swagger UI was accessible as recently as 2025. The ODP transition guide
page (`data.uspto.gov/support/transition-guide/patentsview`) references the new location but the
page content cannot be read without a JS-rendering browser.

---

## 3. Bulk Download Files (PatentsView TSV tables)

### 3a. Old distribution infrastructure — dead

- Old S3 bucket: `s3.amazonaws.com/data.patentsview.org/` → **HTTP 403** (verified 2026-08-06)
- Old CDN: `data.patentsview.org/` → **no response** (verified 2026-08-06)
- Old URL pattern was: `https://data.patentsview.org/{YYYYMMDD}/g_patent.tsv.zip`

### 3b. New distribution — ODP datasets

The ODP transition page directs users to `data.uspto.gov/datasets`. The SPA cannot be read via
curl (all paths return the 20,666-byte WAF-challenge shell). The underlying file-download CDN
path is **UNVERIFIED** — no direct S3/CDN URL for bulk TSV files was confirmed in the transcript.

What is established from the migration context:

- The ODP "Open Data Portal" description from the SPA meta tag: *"USPTO's data platform that
  empowers you to discover and easily extract USPTO data in one place for free."*
- `developer.uspto.gov` redirects all paths (including `/datasets`, `/api-catalog`,
  `/ptab-api/`) to `data.uspto.gov:443/` (verified 2026-08-06).
- The bulk download table schema was historically at `patentsview.org/download/data-download-tables`
  — now redirected.

### 3c. Historical table inventory (UNVERIFIED for current ODP)

The following tables were available on the old PatentsView download system. Current availability
on ODP is **UNVERIFIED** — these schema names are from the PatentsView-DB GitHub repository
(github.com/PatentsView/PatentsView-DB) and are not confirmed against the current ODP.

Key tables relevant to rare-disease repurposing work:
- `g_patent` — granted patents core (patent_id, title, date, type, abstract)
- `g_inventor` — inventors with disambiguation IDs
- `g_assignee` — assignee names, types, locations
- `g_application` — application filing data, series codes
- `g_ipcr` — IPC classifications (A61K, A61P sections critical for pharma)
- `g_cpc_current` — current CPC classifications
- `g_uspc_current` — USPC classifications
- `g_patent_assignee` — join table patent ↔ assignee
- `g_patent_inventor` — join table patent ↔ inventor
- `g_us_patent_citation` — forward/backward citation network
- `g_wipo_technology` — WIPO technology fields
- `g_government_interest` — government interest statements (relevant for NIH-funded drugs)
- `pg_published_application` — pre-grant publications

File format was `.tsv.zip` (tab-separated, zip-compressed). File sizes for the main tables
(grant vintage ~2024): **UNVERIFIED** — the original agent could not reach any working bulk
download URL.

---

## 4. USPTO Patent Examination Data System (PEDS)

**Status: dead.** `ped.uspto.gov` → NXDOMAIN (verified 2026-08-06 from three DNS resolvers).

`ped.uspto.gov/api/queries` previously returned HTTP 301 → `data.uspto.gov:443/` (verified
2026-08-06 — the 301 response was captured before DNS went dark). The PEDS POST endpoint
returned `HTTP_STATUS:000` (connection refused) when directly tested.

PEDS was a Solr-based API accepting POST queries with Solr syntax. Its data is presumed to have
migrated to the ODP but no working replacement endpoint was verified.

---

## 5. USPTO Full-Text Bulk Data (bulkdata.uspto.gov)

**Status: dead.** `bulkdata.uspto.gov` → NXDOMAIN (verified 2026-08-06 from three DNS resolvers).

`bulkdata.uspto.gov` historically hosted:
- Weekly grant XML bundles (APS format, full text including claims)
- Weekly application publication XML bundles (US PGPub format)
- Assignment data (XML)
- Classification data
- Annual DVDs

The ODP transition page (inaccessible via curl) presumably redirects to ODP bulk files. The exact
new URLs for grant XML bundles are **UNVERIFIED**.

---

## 6. Patent Center API (patentcenter.uspto.gov)

`patentcenter.uspto.gov` resolves and returns HTTP 200 (verified 2026-08-06). However, it is also
an Angular SPA (`<title>Patent Center</title>`) behind a WAF. All paths including
`/retrieval/public/v1/applications/grants/10000000` return the SPA shell, not JSON.

The Patent Center public retrieval API (which historically returned document sections — claims,
drawings, etc. — for granted patents and pending applications) is **UNVERIFIED** as a working
REST endpoint accessible without a browser.

Scripts bundle found at `patentcenter.uspto.gov/main-CZBZIYUE.js` — size ~18,211 bytes
(another WAF-protected stub loader; actual application code is delivered post-challenge).

---

## 7. PTAB Data

### 7a. Old host

`ptabdata.uspto.gov` → no response / HTTP 000 (verified 2026-08-06).

`developer.uspto.gov/ptab-api/swagger/index.html` → HTTP 301 →
`data.uspto.gov:443/apis/ptab-trials/search-proceedings` (verified 2026-08-06).

`developer.uspto.gov/ptab-api/` → HTTP 301 → same ODP target (verified 2026-08-06).

### 7b. New ODP endpoint

`data.uspto.gov/apis/ptab-trials/search-proceedings` — path confirmed from redirect chain
but returns the 20,666-byte SPA shell when requested via curl (verified 2026-08-06). A
browsable PTAB trial search is present on the ODP; REST API parameters are **UNVERIFIED**.

The ODP PTAB tool covers IPR, PGR, CBM, and derivation proceedings. PTAB data is relevant for
identifying inter partes review challenges against pharma compound patents.

---

## 8. Patent Public Search (ppubs.uspto.gov)

**Not tested** in the original agent session. USPTO offers Patent Public Search at
`ppubs.uspto.gov` with a basic query API. **UNVERIFIED.**

---

## 9. Assignment Data

USPTO assignment data was historically at `bulkdata.uspto.gov/data/bib/assignee/`. That host is
dead (NXDOMAIN). The ODP presumably hosts assignment data but no working URL was verified.

The PatentSearch API `assignees` nested field and the `/api/v1/assignee/` endpoint provide
assignee data per-patent, which is usable for small-scale lookups if the API is accessible.
Bulk assignment data (for tracking all ownership transfers) is **UNVERIFIED**.

---

## 10. USPTO GitHub Resources

The following GitHub repositories are live and useful for understanding the data schema:

| Repo | URL | Status | Content |
|---|---|---|---|
| PatentsView-DB | github.com/PatentsView/PatentsView-DB | VERIFIED live | Pipeline code, schema (MySQL/Airflow) |
| PatentsView-API | github.com/PatentsView/PatentsView-API | VERIFIED live | Old API server setup instructions |
| PatentsView-Query | github.com/PatentsView/PatentsView-Query | VERIFIED live (master branch) | Old query builder UI; API URL was `querytoolapi.patentsview.org` (dead) |
| PatentPublicData | github.com/PatentsView/PatentPublicData | VERIFIED listed | "Utility tools to help download and parse patent data made available to the public" |
| PatentsView-APIWrapper | github.com/PatentsView/PatentsView-APIWrapper | VERIFIED listed | Python wrapper for bulk API calls |

From `PatentsView-Query/master/js/views/query/previewResultsView.js` (retrieved 2026-08-06):
- Old API base was `https://querytoolapi.patentsview.org/` (dead — NXDOMAIN verified)
- Export helpers: `https://querysupport.patentsview.org/tocsv.php` and `/toxml.php` (NXDOMAIN)

---

## 11. Data Licensing

From v2.3.2 release notes (2025-04-22, verified via Wayback):

> "PatentSearch API data content is licensed under a Creative Commons Attribution 4.0 License"

This license was "already advertised as applying to PatentsView Data accessed via bulk download
files" and was explicitly applied to API data in v2.3.2. CC BY 4.0 = free for commercial use
with attribution. No redistribution restrictions for a repurposing company's internal database.

---

## 12. Practical Guidance for a Small Team

### If PatentSearch API access is restored / migrated

1. Register at the PatentsView Help Center for a free API key (one per email).
2. Use `X-Api-Key: {key}` header on all requests to the API base URL.
3. Rate limit: 45 req/min — sufficient for screening; use exponential backoff on 429.
4. For pharma repurposing, filter on:
   - CPC codes: `A61K` (medicinal preparations), `A61P` (therapeutic activity)
   - IPC codes: same sections
   - `patent_type: "utility"` to exclude designs
   - `gov_interest_statement` field to identify NIH-funded patents (may affect licensing)
5. For Funnel A (never-US moiety, PRV-eligible): combine with Orange Book exclusivity data and
   FDA drug approvals data to confirm the active moiety has never been approved in the US.
6. For Funnel B (US generic): track assignee history and citation networks for FTO analysis.

### If bulk files are needed

Navigate to `data.uspto.gov/datasets` in a real browser (not curl) to locate current bulk
download files. The ODP is functional in a browser; the WAF blocks automated access.
Alternatively, use the PatentPublicData GitHub tools which are documented for parsing public
patent data files.

### If full-text XML is needed

USPTO grants XML (APS format) and application publications XML (US PGPub) are the gold standard
for full claim text. The old bulk host (`bulkdata.uspto.gov`) is dead. A browser session on the
ODP may expose the new download URLs. The `g_claim` and `pg_claim` API endpoints on the
PatentSearch API provide claim text per-patent without needing to download bulk XML.

---

## 13. Unfinished — Worth Re-Running

1. **New PatentSearch API host.** `search.patentsview.org` is dead. What is the successor
   hostname under `data.uspto.gov`? The ODP transition page cannot be read via curl. A
   browser-rendered fetch of `data.uspto.gov/support/transition-guide/patentsview` and
   `data.uspto.gov/apis/patentsearch` would answer this. One browser-tool fetch should suffice.

2. **Bulk download URLs.** Current TSV/ZIP download paths for the main PatentsView tables
   (g_patent, g_assignee, g_ipcr, g_cpc_current) are unknown. Fetch
   `data.uspto.gov/datasets` in a browser; find direct S3 or CDN URLs.

3. **PEDS replacement endpoint.** What replaced `ped.uspto.gov/api/queries` on the ODP?
   The ODP apparently hosts "Patent Examination Data" — the full endpoint URL needs a browser.

4. **PTAB REST API parameters.** `data.uspto.gov/apis/ptab-trials/search-proceedings` is
   the ODP page, but the underlying REST API path, parameters, and auth requirements are
   unknown.

5. **Bulk assignment data.** The replacement for `bulkdata.uspto.gov/data/bib/assignee/`
   is unknown.

6. **Patent Center public API.** Whether `patentcenter.uspto.gov/retrieval/public/v1/`
   works for REST access to document sections (claims, specs, drawings) in 2026 is unverified.

---

## 14. URL Ledger

### VERIFIED

| URL | Status | Verified finding |
|---|---|---|
| `https://api.patentsview.org/patents/query` | HTTP 301 | Redirects to `data.uspto.gov/support/transition-guide/patentsview` |
| `https://patentsview.org/download/data-download-tables` | HTTP 301 | Redirects to same ODP transition page |
| `https://search.patentsview.org` | NXDOMAIN | Dead — confirmed from 3 DNS resolvers (local, 8.8.8.8, 1.1.1.1) |
| `https://querytoolapi.patentsview.org` | NXDOMAIN | Dead |
| `https://querysupport.patentsview.org` | NXDOMAIN | Dead |
| `https://data.patentsview.org` | No response | Dead |
| `https://s3.amazonaws.com/data.patentsview.org/` | HTTP 403 | Bucket exists but access denied |
| `https://data.uspto.gov/` | HTTP 200 (20,666-byte SPA) | Live Angular SPA — WAF-protected, no curl access to API |
| `https://data.uspto.gov/support/transition-guide/patentsview` | HTTP 200 (SPA shell) | ODP page exists but unreadable via curl |
| `https://ped.uspto.gov` | NXDOMAIN | Dead |
| `https://bulkdata.uspto.gov` | NXDOMAIN | Dead |
| `https://ptabdata.uspto.gov` | HTTP 000 | No response |
| `https://patentcenter.uspto.gov/` | HTTP 200 (SPA shell) | Live — WAF-protected |
| `https://developer.uspto.gov/ptab-api/` | HTTP 301 → `data.uspto.gov:443/apis/ptab-trials/search-proceedings` | Dead host, ODP redirect confirmed |
| `https://developer.uspto.gov/api-catalog` | HTTP 301 → `data.uspto.gov:443/` | All developer.uspto.gov → ODP |
| `https://api.patentsview.org` (IPs) | 104.18.35.201 / 172.64.152.55 (Cloudflare) | DNS resolves; host is alive but 301s everything |
| `search.patentsview.org/api/v1/*` (via CDX) | HTTP 403 as of 2026-03 | Was live with API-key enforcement through at least March 2026 |
| `search.patentsview.org/docs/` | Last Wayback: 2025-06-20 200 OK | Docs site was live through mid-2025 |
| `https://github.com/PatentsView/PatentsView-DB` | Live | Schema and pipeline code |
| `https://github.com/PatentsView/PatentsView-API` | Live | Old API server code |
| `https://github.com/PatentsView/PatentsView-Query` | Live (master) | Old query builder; `querytoolapi.patentsview.org` was API host |
| Wayback: `search.patentsview.org/docs/docs/Search%20API/SearchAPIReference/` (2024-04-16) | 200 OK (archived) | Full API reference — auth, rate limits, query language, all endpoints |
| Wayback: `search.patentsview.org/docs/docs/Search%20API/EndpointDictionary/` (2025-06-20) | 200 OK (archived) | Full endpoint and field dictionary through v2.3.2 |

### UNVERIFIED

| Item | Why unverified |
|---|---|
| Current PatentSearch API hostname on ODP | `search.patentsview.org` dead; ODP SPA unreadable via curl; transition page inaccessible |
| Bulk TSV download URLs on ODP | Old S3/CDN dead; ODP SPA blocks curl; no working direct URL found |
| PEDS replacement endpoint | `ped.uspto.gov` dead; replacement path on ODP unknown without browser |
| PTAB REST API path/parameters on ODP | Redirects to ODP SPA; actual API parameters unknown |
| Patent Center public retrieval API | SPA-protected; `/retrieval/public/v1/` returns SPA shell |
| USPTO bulk assignment data location | `bulkdata.uspto.gov` dead; ODP replacement URL unknown |
| Full-text grant/application XML bulk location | `bulkdata.uspto.gov` dead; ODP replacement unknown |
| `ppubs.uspto.gov` Patent Public Search API | Not tested in this session |
| Current data currency / update schedule on ODP | Cannot read ODP; last verified data cut was 2024-12-31 via v2.3.0 release notes |
| Free API key registration URL post-migration | Old Help Center link may have changed with ODP move |
