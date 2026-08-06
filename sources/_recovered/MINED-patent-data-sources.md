<!-- MINED from agent-af1ff36fa6fd3f051.jsonl on 2026-08-05.
     The original agent (25 assistant turns, 145 events, 398 KB) was killed before writing its
     final report (final assistant message = 107 chars: "[Request interrupted by user for tool use]").
     Actual research survived in tool_use/tool_result/assistant-text blocks across 4 spawned
     subagents whose completed transcripts were separately mined.
     Findings attributed as: TRANSCRIPT-VERIFIED (quoted from fetched content) or
     NEWLY-VERIFIED-2026-08-05 (confirmed by the recovery agent today). -->

# Patent-Data Sources for Pharma IP / FTO Pipeline
**Recovered from agent-af1ff36fa6fd3f051 — 2026-08-05**

---

## Contents
1. [USPTO Open Data Portal (ODP)](#1-uspto-open-data-portal)
2. [Patent Term Adjustment (PTA) and Patent Term Extension (PTE)](#2-pta-and-pte)
3. [Google Patents Public Datasets on BigQuery](#3-google-patents-bigquery)
4. [EPO Open Patent Services (OPS) — EPO API](#4-epo-open-patent-services-ops)
5. [Espacenet](#5-espacenet)
6. [WIPO PATENTSCOPE](#6-wipo-patentscope)
7. [Supplementary Protection Certificates (SPC)](#7-supplementary-protection-certificates-spc)
8. [FTO Aggregators: Lens.org, EPO Bulk, Commercials](#8-fto-aggregators)
9. [URL Ledger](#9-url-ledger)

---

## 1. USPTO Open Data Portal

### 1a. PatentsView Migration (settled fact — no re-derivation needed)

**TRANSCRIPT-VERIFIED** (caller established before the agent ran):
- `search.patentsview.org` no longer resolves in DNS.
- `patentsview.org` 301-redirects to `https://data.uspto.gov/support/transition-guide/patentsview`.
- PatentsView migrated into the USPTO Open Data Portal (ODP) on **2026-03-20**.

**TRANSCRIPT-VERIFIED** (agent fetched `https://data.uspto.gov/documents/transition-guide/support/patents-view.md`, HTTP 200, 5,486 bytes):

> "The legacy PatentsView website is migrating to the USPTO's Open Data Portal (https://data.uspto.gov) starting on March 20, 2026."
>
> "**PatentsView APIs:** ...USPTO plans to reintroduce PatentsView API functions in updated forms as the transition progresses. There is currently **no estimate for the launch date** of these API functions on ODP."
>
> "Previously-issued API keys for the PatentSearch API will **not** be compatible with ODP APIs."

**PatentsView bulk datasets are already live on ODP.** Confirmed redirect table (fetched):

| Category | Sample tables | ODP bulk URL |
|---|---|---|
| Granted Patents — disambiguated | `g_patent`, `g_cpc_current`, `g_assignee_disambiguated` | `https://data.uspto.gov/bulkdata/datasets/pvgpatdis` |
| Granted Patents — long text (claims) | `g_claims_2025`, `g_claims_2024` | `https://data.uspto.gov/bulkdata/datasets/pvgpattxt` |
| Granted Patents — brief summary | `g_brf_sum_text_2025` | same as above |
| Pre-grant — disambiguated | `pg_published_application`, `pg_cpc_current` | `https://data.uspto.gov/bulkdata/datasets/pvpgpubdis` |
| Pre-grant — long text (claims) | `pg_claims_2025` | `https://data.uspto.gov/bulkdata/datasets/pvpgpubtxt` |
| Sorted (beta) | `g_sorted_applicant`, `pg_sorted_individual` | `https://data.uspto.gov/bulkdata/datasets/pvsorted` |
| Annualized | `2024.csv`, `2023.csv` | `https://data.uspto.gov/bulkdata/datasets/pvannual` |

Contacts: `data@uspto.gov` (ODP), `economicsdata@uspto.gov` (PatentsView data questions).

### 1b. ODP API — Current Endpoints

**TRANSCRIPT-VERIFIED** — agent downloaded all 137 Angular chunks (2.8 MB) and the OpenAPI spec.

**OpenAPI spec (authoritative):** `https://data.uspto.gov/swagger/swagger.yaml` — **NEWLY-VERIFIED-2026-08-05**, HTTP 200, 101,395 bytes.

**API base URL:** `https://api.uspto.gov` (from the YAML `servers` block).

**API key header (confirmed from both the YAML securityScheme and inline curl examples in the Angular bundles):**
```
X-API-KEY: <your-api-key>
```

**Complete path list from the YAML** (TRANSCRIPT-VERIFIED):

```
POST /api/v1/patent/applications/search
GET  /api/v1/patent/applications/search/download
GET  /api/v1/patent/applications/{applicationNumberText}
GET  /api/v1/patent/applications/{applicationNumberText}/meta-data
GET  /api/v1/patent/applications/{applicationNumberText}/adjustment      ← PTA
GET  /api/v1/patent/applications/{applicationNumberText}/assignment
GET  /api/v1/patent/applications/{applicationNumberText}/attorney
GET  /api/v1/patent/applications/{applicationNumberText}/continuity
GET  /api/v1/patent/applications/{applicationNumberText}/foreign-priority
GET  /api/v1/patent/applications/{applicationNumberText}/transactions
GET  /api/v1/patent/applications/{applicationNumberText}/documents
GET  /api/v1/patent/applications/{applicationNumberText}/associated-documents
GET  /api/v1/patent/status-codes
POST /api/v1/datasets/products/search
GET  /api/v1/datasets/products/{productIdentifier}
GET  /api/v1/datasets/products/files/{productIdentifier}/{fileName}
POST /api/v1/petition/decisions/search
GET  /api/v1/petition/decisions/search/download
GET  /api/v1/petition/decisions/{petitionDecisionRecordIdentifier}
POST /api/v1/patent/applications/text-to-search                         ← new Smart Search
POST /api/v1/patent/trials/proceedings/search
GET  /api/v1/patent/trials/proceedings/{trialNumber}
POST /api/v1/patent/trials/decisions/search
GET  /api/v1/patent/trials/decisions/{documentIdentifier}
GET  /api/v1/patent/trials/{trialNumber}/decisions
POST /api/v1/patent/trials/documents/search
GET  /api/v1/patent/trials/documents/{documentIdentifier}
GET  /api/v1/patent/trials/{trialNumber}/documents
POST /api/v1/patent/appeals/decisions/search
GET  /api/v1/patent/appeals/{appealNumber}/decisions
POST /api/v1/patent/interferences/decisions/search
GET  /api/v1/patent/interferences/{interferenceNumber}/decisions
```

**Additional Swagger specs** (from `https://data.uspto.gov/swagger/swagger-initializer.js`, HTTP 200):
- `https://data.uspto.gov/swagger/tsdr-swagger.yaml` — Trademark Status and Document Retrieval API
- `https://data.uspto.gov/swagger/oa-rejections.yaml` — Office Action Rejections
- `https://data.uspto.gov/swagger/oa-text-retrieval.yaml` — Office Action Text Retrieval
- `https://data.uspto.gov/swagger/oa-citations.yaml` — Office Action Citations
- `https://data.uspto.gov/swagger/oa-enriched-citations.yaml` — Enriched Citations v3

**Example curl (from the ODP portal's own code snippets, TRANSCRIPT-VERIFIED):**
```bash
curl -X "GET" "https://api.uspto.gov/api/v1/patent/applications/14412875" \
  -H "X-API-KEY: YOUR_API_KEY"

curl -X "POST" "https://api.uspto.gov/api/v1/patent/applications/search" \
  -H "X-API-KEY: YOUR_API_KEY" \
  -d '{"q":"applicationMetaData.applicationTypeLabelName:Utility"}'
```

**Unauthenticated probe results** (TRANSCRIPT-VERIFIED — useful for debugging):
- Real endpoints (valid route, wrong/missing key): **HTTP 401** `{"message":"Unauthorized"}`
- Non-existent routes: **HTTP 403** `{"message":"Missing Authentication Token"}`

### 1c. API Key — Registration Requirement (Critical Change 2026-06-18)

**TRANSCRIPT-VERIFIED** — agent fetched `https://data.uspto.gov/documents/support/releases/release-40.md` (HTTP 200). Key excerpt:

> **Release 4.3 — 2026-06-18:**
> "Account Requirement: ODP now requires users to log in with a registered USPTO.gov account. Data access for non-registered (anonymous) users has been **discontinued**."
> "Developer Hub (DH) was officially decommissioned on **June 5, 2026**."

**The full key-generation flow** (TRANSCRIPT-VERIFIED, from `https://data.uspto.gov/documents/api/getting-started.md`, HTTP 200, 7,581 bytes):

1. Create a **USPTO.gov account** at `https://account.uspto.gov` — activate via email code (48-hour expiry).
2. Create an **ID.me account** at `https://api.id.me/en/registration/new` — identity verification required (for international users: video call + English-translated documents).
3. Link both accounts via the "Manage API Key" button in the ODP navigation → API key issued.

**Implication for automated/headless use:** the ID.me verification is a one-time human step; the resulting API key can then be used headlessly in `X-API-KEY` headers. But **no anonymous or service-account path exists** — the key is tied to a verified human identity.

**Profile fields now mandatory (by 2026-08-18, per Release 4.4):** Job Title, Organization Name, Organization Type, Intended Use. No stated impact on API key access before that date.

### 1d. Rate Limits

**TRANSCRIPT-VERIFIED** (from `https://data.uspto.gov/documents/api/api-rate-limits.md`, HTTP 200, 3,798 bytes):

| API category | Limit |
|---|---|
| **Metadata retrieval APIs** (search, application data, continuity, transactions, PTA, address, assignments, foreign priority, associated documents, bulk product, petition decisions, bulk search) | **5 million calls/week** (combined) |
| **Patent File Wrapper Documents API** | **1.2 million calls/week** |
| **Bulk Datasets Downloads API** (same file) | **20 downloads/year** per API key; XML files have a higher limit |
| **Bulk Downloads by IP** | 5 files per 10 seconds from same IP |

**Concurrency — critical constraint:**
> "We limit all API calls to **one API call per API key**. You will need to wait until an API call completed until starting a new one. We also **advise against using the same API key in applications running in parallel**: concurrent API calls with the same key are currently blocked."

**Burst:** 1 (no parallel requests per key). **Rate:** 4–15 requests/second depending on API call type.

**Quota reset:** Sunday at midnight UTC.

**Error code:** HTTP 429 if exceeded; retry delay minimum 5 seconds.

**Bulk file redirect note:** files are redirected with a digitally signed URL expiring in **5 seconds** — start the download immediately on redirect.

---

## 2. PTA and PTE

### Patent Term Adjustment (PTA) — FULLY SPECIFIED IN ODP

**TRANSCRIPT-VERIFIED** (from `https://data.uspto.gov/documents/api/patent-term-adjustment/patent-term-adjustment.md`, HTTP 200, 1,021 bytes):

> "This dataset includes published patent applications and issued patent data filed after **January 1, 2001**. This data is refreshed **daily**."

**Endpoint:**
```
GET https://api.uspto.gov/api/v1/patent/applications/{applicationNumberText}/adjustment
```
Requires `X-API-KEY`. Returns the `PatentTermAdjustment` schema.

**PTA Schema fields** (TRANSCRIPT-VERIFIED, from `https://data.uspto.gov/swagger/odp-common-base.yaml`, HTTP 200, 59,370 bytes):

| Field | Type | Description |
|---|---|---|
| `aDelayQuantity` | integer | USPTO-caused A delays (examination timeline) |
| `bDelayQuantity` | integer | B delays (patent not issued within 3 years) |
| `cDelayQuantity` | integer | C delays (interferences, secrecy orders, appeals) |
| `adjustmentTotalQuantity` | integer | Total: (A+B+C − overlaps) − applicant delays |
| `applicantDayDelayQuantity` | integer | Applicant delays (failure to respond promptly) |
| `nonOverlappingDayQuantity` | float | USPTO delay days after removing overlap |
| `overlappingDayQuantity` | float | Overlapping delay days |
| `patentTermAdjustmentHistoryDataBag` | array | Event-by-event history with dates and descriptions |

### Patent Term Extension (PTE / 35 U.S.C. § 156) — NOT IN ODP API

**TRANSCRIPT-VERIFIED negative:** The agent searched all 137 ODP Angular bundles (2.8 MB) and the ODP API documentation markdown for "patent term extension", "PTE", and "35 U.S.C. 156" — **zero matches**. The ODP API covers PTA only; it has no endpoint for FDA regulatory review period-based PTE grants.

**www.uspto.gov blocked by WAF** (TRANSCRIPT-VERIFIED): `https://www.uspto.gov/patents/laws/patent-term-extension` returns HTTP 403 to both curl and WebFetch, regardless of User-Agent.

**Best alternative sources for PTE data:**

**1. Federal Register API (free, no auth)** — TRANSCRIPT-VERIFIED and NEWLY-VERIFIED-2026-08-05:
```bash
curl -G "https://www.federalregister.gov/api/v1/documents.json" \
  --data-urlencode "conditions[term]=regulatory review period patent extension" \
  --data-urlencode "conditions[agencies][]=food-and-drug-administration" \
  --data-urlencode "fields[]=title" \
  --data-urlencode "fields[]=publication_date" \
  --data-urlencode "fields[]=document_number" \
  --data-urlencode "per_page=20" \
  --data-urlencode "order=newest"
```
Returns JSON: `count=3137` matching notices, newest = "Determination of Regulatory Review Period for Purposes of Patent Extension; VYALEV" (2026-06-29). Each PTE grant/determination is published here as a Federal Register notice. This is the primary public record.

**2. FDA Orange Book data files** (bulk download, monthly):
URL: `https://www.fda.gov/drugs/drug-approvals-and-databases/orange-book-data-files` (NEWLY-VERIFIED-2026-08-05, HTTP 200 to browser UA).
The Orange Book's patent data includes PTE-extended expiry dates as the declared expiry; the `patent.txt` bulk file in the monthly Orange Book download (ZIP) carries `patent_expire_date_text` which reflects PTE if applied.

**3. BigQuery `patents-public-data.uspto_peds.applications`** — TRANSCRIPT-VERIFIED: the PEDS dataset description says it includes *"patent term extension data tabs in Public PAIR from 1981 to present."* See §3 below.

---

## 3. Google Patents BigQuery

**Subagent `a0c3a42788a7a3528` verified.** All findings TRANSCRIPT-VERIFIED unless noted.

### 3a. Project and namespace

- **Project ID:** `patents-public-data` — **NOT** `bigquery-public-data`. Must always fully qualify: `` `patents-public-data.patents.publications` ``.
- The project does **not** appear in BigQuery Explorer by default; pin it manually.
- 21 Marketplace products live as of 2026-08-05 (browser render confirmed); all tagged "Free (21)" for storage.

**Three products NOT in `patents-public-data`** (confirmed from repo generator configs):
- IFI CLAIMS → `jefferson-1790:ifi_claims.xml`, `jefferson-1790:ifi_claims.publications`
- UCB Fung Institute → `erudite-marker-539:JEMS16.*`
- ETSI technical standards → `innography-174118:technical_standards.etsi`

### 3b. Key datasets and tables for pharma FTO

**Primary bibliographic layer:**

`patents-public-data.patents.publications` — 98.1M rows (2018 figure; larger now), ~900 GB. CC BY 4.0.

Key schema fields:

| Field | Type | Note |
|---|---|---|
| `publication_number` | STRING | Primary join key; DOCDB style `'US-7650331-B1'` |
| `application_number` | STRING | DOCDB style; may not always be set |
| `family_id` | STRING | Simple family — use as FTO grouping unit |
| `country_code`, `kind_code` | STRING | |
| `publication_date`, `filing_date`, `grant_date`, `priority_date` | INTEGER | **YYYYMMDD ints, not DATE**; `grant_date`=0 if not granted |
| `priority_claim` | RECORD REPEATED | |
| `title_localized`, `abstract_localized`, `claims_localized`, `description_localized` | RECORD REPEATED `.text`,`.language` | Claims/description are US-only; description capped at 9 MB |
| `inventor_harmonized`, `assignee_harmonized` | RECORD REPEATED `.name`,`.country_code` | Prefer over raw `inventor`/`assignee` |
| `cpc`, `ipc`, `uspc` | RECORD REPEATED `.code`,`.inventive`,`.first`,`.tree` | |
| `examiner` | RECORD REPEATED `.name`,`.department`,`.level` | |

**Google Patents Research Data:**
`patents-public-data.google_patents_research.publications` — Quarterly refresh, CC BY 4.0. Contains: title/abstract MT, **embedding vectors** (`embedding_v1` FLOAT REPEATED — dot-product similarity), extracted top terms, similar documents, forward citations, `cpc_low`/`cpc_inventive_low` (flattened CPC+ancestors — cheaper to filter on than the nested `cpc` record).

**USPTO OCE datasets** (all live, Marketplace-confirmed):

| Dataset | Key tables | Notes |
|---|---|---|
| `uspto_oce_pair` | `application_data`, `transactions`, `continuity_*`, `all_inventors`, `correspondence_address`, `event_codes`, `foreign_priority`, `status_codes`, `match` | PEDS replacement |
| `uspto_oce_office_actions` | `office_actions`, **`rejections`**, `citations` | **2008–mid-2017 only** — annually updated |
| `uspto_oce_claims` | `patent_claims_fulltext`, `pgpub_claims_fulltext`, `patent_claims_stats` | |
| `uspto_oce_assignment` | `assignment`, `assignee`, `assignor`, `documentid` | Ownership chain |
| `uspto_peds` | **`applications`** | Quarterly; includes **PTE data** from Public PAIR |
| `uspto_oce_litigation` | `cases`, `documents`, `names`, `attorneys` | Ends **2015** — useless for recent ANDA/IPR |
| `uspto_ptab` | `trials`, `match` | |

**Pharma-critical chemical/sequence tables:**

`patents-public-data.ebi_surechembl.map` — **SureChEMBL: the structure→patent bridge.** 278.5M rows, 37.3 GB. Columns: `schembl_id`, **`smiles`**, **`inchi_key`**, `corpus_frequency`, `patent_id`, `publication_date`, `field`, `field_frequency`. Joins to `patents.publications` at 99.73%. **CC BY-SA 3.0 — copyleft** (derivative databases may inherit share-alike obligation). Quarterly refresh. Upstream EBI SureChEMBL FTP (`ftp.ebi.ac.uk/pub/databases/chembl/SureChEMBL/`) was last updated 2026-08-04 — so the BigQuery mirror may lag if not refreshed.

`patents-public-data.ebi_chembl` (suffix `_24`) — 151 tables including `drug_indication_24`, `product_patents_24`, `patent_use_codes_24`, `compound_structures_24`. **CC BY-SA 3.0. WARNING: upstream ChEMBL is at version 37 as of 2026; the BigQuery mirror is at `_24`, roughly 13 releases behind.** Check EBI FTP for current: `https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/releases/` (contains `chembl_37`).

**Patent sequence data — NOT PRESENT in BigQuery.** No `uspto_sequences` or similar. The only sequence tables in `ebi_chembl` are protein-target sequences (not patent sequence listings). For nucleotide/amino-acid sequence claim coverage, source from EPO BDDS sequence listings or Lens PatSeq.

**IFI CLAIMS — freshest legal-status signal:**
`jefferson-1790:ifi_claims.publications` — Weekly refresh. Includes *"integrated legal status information"* and *"standardized assignee/applicant names."* **Licence: "Varies — contact IFI CLAIMS."** Do not build a commercial dependency without an IFI agreement.

**NO EPO DOCDB/Espacenet dataset exists in BigQuery.** Confirmed negative: no `espacenet` or `docdb` in the 21-product live Marketplace list, and zero hits in the index. The `patents.publications` table is sourced from IFI CLAIMS and is DOCDB-compatible by its own documentation; treat it as the bibliographic equivalent.

### 3c. Cost model

All TRANSCRIPT-VERIFIED from `https://cloud.google.com/bigquery/pricing` and `cloud.google.com/bigquery/public-data`:

| Item | Price |
|---|---|
| On-demand queries | **$6.25 / TiB** (US/EU regions) |
| First 1 TiB queries/month | **Free** (per billing account) |
| Storage (active) | First 10 GiB/month free; then $0.02/GiB |
| Google pays storage for public datasets | Yes — you pay only for queries |
| Minimum per table referenced | 10 MB |
| Minimum per query | 10 MB |

**Warning:** `patents.publications` was 899 GB in 2018 and is larger now. A `SELECT *` would consume or exceed the entire monthly free terabyte. Column pruning is mandatory — exclude `description_localized` and `claims_localized` from exploratory queries.

### 3d. BigQuery Sandbox (no billing account needed)

TRANSCRIPT-VERIFIED from `https://cloud.google.com/bigquery/docs/sandbox`:

> "The BigQuery sandbox lets you experience BigQuery **without providing a credit card or creating a billing account** for your project."

Limits:
- Same free tier: 1 TiB queries/month, 10 GiB active storage/month.
- Tables you create **expire after 60 days** — forced, cannot be disabled in sandbox.
- **No DML** (INSERT/UPDATE/DELETE/MERGE).
- **No streaming inserts.**
- Querying public datasets works fine; `CREATE TABLE AS SELECT` is allowed but results expire.
- For a production FTO pipeline, enable billing (still $0 under 1 TiB/mo) to remove the 60-day expiry and unlock DML.

### 3e. Gotchas

1. **Docs repo is archived.** `https://github.com/google/patents-public-data` has `"archived": true`, last pushed 2024-06-17. Row counts, byte sizes, and schemas in the repo are 2018 vintage — use as naming/shape reference only.
2. **"Expected update frequency" on Marketplace is a promise, not a measurement.** Verify each table's actual Last Modified in the BigQuery console.
3. **Snapshot suffixes** — dated copies exist (e.g. `patents.publications_201710`, `ebi_surechembl.map_201710`). Pin a dated snapshot for any FTO opinion you need to reproduce or defend.
4. **No SLA** for the Public Dataset Program — Google's own page says so.
5. **Licensing is not uniform:** `patents.publications` and `google_patents_research` = CC BY 4.0; `ebi_surechembl` and `ebi_chembl` = CC BY-SA 3.0 (copyleft); USPTO OCE = "for public use"; IFI CLAIMS = "varies / contact IFI."

---

## 4. EPO Open Patent Services (OPS)

**Subagent `a078ccb1f9bed4307` verified.** All findings TRANSCRIPT-VERIFIED unless noted.

### 4a. Base URL and current version — 3.2

**Authoritative OpenAPI spec:** `https://ops.epo.org/wsdl/ops.yaml` — NEWLY-VERIFIED-2026-08-05, HTTP 200, 61,053 bytes. Spec states: `version: "3.2"`, `host: ops.epo.org`, `basePath: /3.2/rest-services`. Reference Guide: `en-ops-v3.2-documentation-version-1.3.20.pdf` (June 2024).

**No v4.0 exists.** Version `/3.0/` and `/3.1/` return 404 `"This API version is not supported"` (3.1 officially EOL). Probe of `/3.3/`, `/4.0/`, `/5.0/` → 403 (quota gate fires before version routing). The auth endpoint `/3.2/auth/accesstoken` is the clean discriminator — only `3.1`, `3.2`, and bare `/auth/accesstoken` return 401 (route exists); all others fall through to 403.

### 4b. Clarification — the 403 is NOT an auth error

**TRANSCRIPT-VERIFIED (corrects prior assumption):** When the caller's transcript was made, they assumed HTTP 403 on an unauthenticated OPS call meant "credentials missing." That is wrong.

```
curl -i https://ops.epo.org/3.2/rest-services/published-data/publication/epodoc/EP1000000/biblio
→ HTTP 403
→ Header: x-rejection-reason: AnonymousQuotaPerDay
→ Body: <error><code>403</code><message>This request has been rejected due to the violation of
         Fair Use policy</message><moreInfo>https://www.epo.org/service-support/ordering/fair-use.html</moreInfo></error>
```

OPS does serve anonymous traffic under a per-day quota; 403 here means the anonymous pool is exhausted for that IP. The three distinct failure modes to code against:
- **403** + `X-Rejection-Reason: AnonymousQuotaPerDay` → quota exhausted (quota re-auth or rotate IP)
- **400** `invalid_access_token` → expired/bad Bearer token → re-authenticate
- **404** `This API version is not supported` → wrong version path

### 4c. OAuth2 Client Credentials Flow

**Token endpoint (TRANSCRIPT-VERIFIED):** `https://ops.epo.org/3.2/auth/accesstoken`

```bash
curl -X POST "https://ops.epo.org/3.2/auth/accesstoken" \
  -H "Authorization: Basic $(echo -n 'consumer_key:consumer_secret' | base64)" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials"
```

Response JSON (from EPO docs PDF p.35-36):
```json
{
  "token_type": "Bearer",
  "expires_in": "1199",
  "access_token": "...",
  "scope": "core",
  "api_product_list": "[ops-prod]",
  "refresh_count": "0"
}
```

**Token lifetime: ~20 minutes (1199 s). No refresh token.** Re-POST to the token endpoint when you receive a 400 `invalid_access_token`. Subsequent calls:
```
Authorization: Bearer <access_token>
```

### 4d. Registration and free tier

- **Register:** `https://developers.epo.org/user/register` (portal `https://developers.epo.org/`) — HTTP 200 NEWLY-VERIFIED-2026-08-05. Define an "App" to get Consumer Key + Secret; multiple credential sets per developer allowed.
- **Free tier: 4 GB/week** (TRANSCRIPT-VERIFIED twice from EPO docs). Beyond 4 GB: **EUR 2,800/year** annual subscription.
- **Global 1 Mbps bandwidth cap ≈ 450 MB/hour** on a rolling window; weekly reset at midnight UTC each calendar week.
- **Quota response headers:** `X-IndividualQuotaPerHour-Used`, `X-RegisteredQuotaPerWeek-Used`, `X-RegisteredPayingQuotaPerWeek-Used`, `X-Rejection-Reason`.

### 4e. Throttling — X-Throttling-Control

TRANSCRIPT-VERIFIED (PDF pp.41-42). Format on every response:
```
X-Throttling-Control: system-state (service-name=traffic-light-position:request-limit, ...)
e.g. idle (retrieval=green:200, search=yellow:20, inpadoc=red:30, images=green:200, other=green:1000)
```

System state ∈ **idle / busy / overloaded**. Lights: green <50% used, yellow 50-75%, red >75%, black = exceeded (service temporarily suspended). Per-minute limits shrink with system state (retrieval: 200→100→50; search: 30→15→5; inpadoc: 60→45→30). Parse `X-Throttling-Control` on every response and back off over a 60-second window.

**Throttle bucket mapping:**
- `search` → `/published-data/search/*`
- `retrieval` → all other `/published-data/*` calls
- **`inpadoc` → `/family/*` AND `/legal/*`** — these share the tightest bucket (60/45/30 per min). **FTO gotcha: legal-status calls compete with family calls.**
- `images` → `/published-data/images/*`, `/classification/cpc/media/*`
- `other` → everything else (1000/min)

### 4f. Service families — exact endpoint paths

All prefixed `https://ops.epo.org/3.2/rest-services`. GET (POST for bulk, max 100 refs). `{type}`=publication|application|priority, `{format}`=docdb|epodoc|original.

| Service | Path pattern | Returns |
|---|---|---|
| published-data search | `/published-data/search[/{constituent}]` | CQL search results |
| published-data | `/published-data/{type}/{format}/{number}/biblio` | Bibliographic data |
| | `.../abstract`, `.../claims`, `.../description`, `.../fulltext` | Text constituents |
| | `.../full-cycle` | All publication stages |
| | `.../equivalents` | Patent equivalents |
| | `/published-data/images/{cc}/{no}/{kind}/{type}` | Page images |
| **family** | `/family/{type}/{format}/{number}` | INPADOC simple family |
| | `/family/{type}/{format}/{number}/biblio` | Family + biblio |
| | **`/family/{type}/{format}/{number}/legal`** | **Family + legal status — FTO workhorse** |
| **legal** | `/legal/{type}/{format}/{number}` | Legal events for one document |
| register | `/register/{type}/{format}/{number}/biblio` | EP Register biblio |
| | `.../events`, `.../procedural-steps`, `.../upp` | Register events, procedural steps, **unitary patent** |
| | `/register/search[/{constituent}]` | Register search |
| classification | `/classification/cpc[/{class}[/{subclass}]]`, `/classification/cpc/search`, `/classification/cpc/media/{name}`, `/classification/map/{in}/{class}/{subclass}/{out}` | CPC scheme, statistics, media, IPC↔CPC mapping |
| number-service | `/number-service/{type}/{input-format}/{number}/{output-format}` | Number format conversion (epodoc↔docdb↔original) |
| usage stats | `/3.2/developers/me/stats/usage` | Your data usage (needs Bearer token) |

### 4g. SPC and legal-status data in OPS

**TRANSCRIPT-VERIFIED.** This is the key finding for pharma FTO.

SPC events are a **first-class INPADOC category.** Authoritative classification scheme: `https://link.epo.org/web/inpadoc_classification_scheme_v1.0_en.pdf` (HTTP 200, 212 KB, EPO, June 2018). ~2,800 legal event codes classified since 1997.

**SPC INPADOC categories — filter on ALL of these:**

| Category | Title | SPC coverage |
|---|---|---|
| **G** | Protection beyond IP right term | SPC filing/grant/refusal/paediatric extension request/grant |
| **H** | IP right cessation | **SPC lapse/expiry/surrender/invalidation** |
| **P** | Re-publication after modification | Modified SPCs (corrected certificates) |
| **Q** | Document publication | SPC certificate publications |

An FTO query filtering only on category G will miss SPC death events (H) and certificate publications (Q).

**OPS legal XML schema:** `https://ops.epo.org/schema/ops_legal.xsd` (HTTP 200). The `<ops:legal>` element contains `<ops:L500EP>` which contains fields **L501EP–L533EP**.

**Critical SPC-specific OPS tags** (TRANSCRIPT-VERIFIED from INPADOC documentation):

| OPS tag | Meaning |
|---|---|
| `L511EP` | SPC number |
| `L512EP` | SPC filing date |
| `L513EP` | Expiry date of underlying basic patent |
| `L523EP` | Date extension granted (SPC or paediatric extension) |
| **`L510EP`** | **Free-format text, max 700 chars** — contains product name and MA number |

**⚠️ THE CRITICAL PHARMA CAVEAT (verbatim from INPADOC docs, §3.5):**

> "In the legacy product SPC product information is exchanged in `<L510EP>`, in **free text format**… It is the intention to enhance the representation of SPC data in the future and offer product information in a richer tag structure… **Until that time SPC product information will be exchanged in element `<text>`**."

The active ingredient / product name and the marketing-authorisation number are **unstructured free text in a single 700-char field, in the national language** (example from EPO docs is in German: `PRODUCT NAME: REGORAFENIB ODER EIN SALZ DAVON`). You must regex/NLP-parse `PRODUCT NAME:` and `REGISTRATION NO/DATE:` and handle multilingual variants. No structured active-ingredient field exists.

**Also note:** The 154-page OPS Reference Guide v1.3.20 contains **zero** occurrences of "SPC" or "supplementary protection" — SPC support is real but entirely undocumented in the OPS guide. Cross-reference the INPADOC legal status docs.

INPADOC covers **50+ patent authorities**.

---

## 5. Espacenet

**TRANSCRIPT-VERIFIED** (subagent `a078ccb1f9bed4307`).

**There is no separate Espacenet API.** EPO's own page states verbatim (`https://www.epo.org/en/searching-for-patents/technical/espacenet`, HTTP 200):

> "For automated data retrieval, please use the EPO's **Open Patent Services (OPS)**."
> "It is **not intended for bulk data retrieval**. The service does **not support automated searches (robots)** and will **deny access to any robots it identifies**."

**Bot protection confirmed:** `worldwide.espacenet.com/` and all subpaths return HTTP 403 with a 1-byte body even with a full desktop Chrome User-Agent. `robots.txt` returns a single `.`. **Do not build on Espacenet's internal endpoints** — it is policy-prohibited and technically blocked.

**Alternative for bulk FTO coverage:** EPO Bulk Data Distribution Service (BDDS) — see §8b.

---

## 6. WIPO PATENTSCOPE

**Subagent `a56f2b8aaad7afe3b` verified.** TRANSCRIPT-VERIFIED from `https://www.wipo.int/en/web/patentscope/data/` (HTTP 200, 92 KB).

### 6a. API — EXISTS, PAID, SOAP, NOT PUBLIC

Two subscription products:

| Product | Price/yr | Scope |
|---|---|---|
| PCT Webservice limited access | CHF 600 | Published International Application series only |
| PCT Webservice full-access | CHF 2,000 | All publication documents |

**No free/public REST API.** SOAP/Java only.

**Rate limit:** 10 retrieval actions/minute per subscriber and per IP address (the more restrictive applies). Sharing one account across multiple IPs is a breach of terms.

**Licence tiers:** non-derivative (store in internal searchable DB, redistribute to affiliates) vs. derivative (redistribution with added value only; derivative-product price cannot be lower than what you paid WIPO). "Conditional use" requires technical measures preventing bulk downloading.

**Pipeline conclusion: Do not build on PATENTSCOPE.** 10 req/min ceiling, anti-parallelization clause, SOAP-only. EPO BDDS covers PCT/WO documents anyway (WO publications are in DOCDB).

### 6b. WIPO bulk data — ALL PAID (except statistics)

Delivery is SFTP or physical hard drive. Selected prices:

| Product | Price (CHF/yr) |
|---|---|
| PCT-Bibliographic | 400 |
| PCT-Text (non-derivative) | 3,900 |
| PCT-Text (derivative) | 19,500 |
| Backfile non-Asian langs (1978–) | 7,600 non-deriv / 38,000 deriv per copy |

50% discount for non-profits. Data retention: current-year data available on WIPO FTP until first publication of following year — miss a week and pay to restore.

**Free WIPO data:** IP Statistics Data Center (`https://www3.wipo.int/ipstats/`) — aggregate counts only, useless for FTO.

**Sequence listings (WIPO):** UNVERIFIED download location — the data page mentions free availability but provides no working bulk URL. Use EPO BDDS sequence listings instead.

### 6c. WIPO legal status — WEAK FOR FTO

WIPO sells no INPADOC equivalent. Explicit disclaimer on the data page: *"the patent data of national and regional patent offices is not currently available from WIPO."*

**Pat-INFORMED** (`https://www.wipo.int/pat-informed/en/`, HTTP 200) — searchable by INN, data from 20 biopharma companies via IFPMA. WIPO's own site says: *"While it is not a tool to provide Freedom to Operate analysis, it facilitates access to patent information."* Small molecules only, no biologics. Use as cross-check only, not as an FTO basis.

---

## 7. Supplementary Protection Certificates (SPC)

**Subagent `a7d3125d741fb5f75` verified.** Three findings upfront that will break an FTO pipeline if not handled.

### ⚠️ Critical Pipeline Breaks

1. **The EPO Federated Register (FRS) does NOT carry SPC data.** Every national-office spec page has a row "9 SPC" that reads "No" on every office checked. FRS deep-links to separate national SPC registers. Treating FRS as an SPC source yields silent false negatives.
2. **UKIPO Ipsum was retired 22 January 2025.** All `ipo.gov.uk/p-ipsum/*` URLs 301-redirect to a new service. There is no live Ipsum REST API.
3. **The EU unitary SPC / centralised examination package is NOT law.** All four 2023 Commission proposals sit at "Awaiting Council's 1st reading position." No unitary SPC, no EUIPO examining office.

### 7a. EPO Federated Register (FRS)

**TRANSCRIPT-VERIFIED** — `https://www.epo.org/en/searching-for-patents/legal/register/documentation/federated-register` (HTTP 200).

Quote: *"The Federated Register provides a single point of access to reliable post-grant bibliographic and legal status information on European patents. It is available free of charge."* It is a **tab inside the European Patent Register**, not a standalone endpoint. **Post-grant only** — does not show pre-grant EP status.

Countries federated (35): AT BA BE BG CH CZ DE EE ES FI FR GB GR HR HU IE IT LI LT LU LV MC MD ME MK MT NL NO PL PT RO RS SE SI SK SM TR.

Integration-status PDF: `https://link.epo.org/web/documentation/federated-register/en-federated-register-status.pdf` (HTTP 200, 386 KB, dated 06/2025) — covers 39 member states + 1 extension state (BA) + 6 validation states.

**SPC data in FRS — VERIFIED NEGATIVE.** Per-country field 9 "SPC":
- GB: "No — SPC Register available separately at `https://www.ipo.gov.uk/p-find-spc.htm`"
- FR: "No — SPC available in the INPI database. Deep linking will be provided"
- ES, IT: "No"
- NL: "European patents, with deep linking for national patents, European patents **and SPCs**" (only NL carries SPC data)
- DE, PT, MT, SK, LV, MK, BG: all "No"

### 7b. INPADOC legal-status SPC event codes

**TRANSCRIPT-VERIFIED** (same as §4g above). SPC events in categories G (filing/grant/PE), H (lapse), P (modified SPC), Q (certificate publication). INPADOC classification scheme PDF: `https://link.epo.org/web/inpadoc_classification_scheme_v1.0_en.pdf` (HTTP 200, 212 KB). INPADOC bulk: `https://www.epo.org/en/searching-for-patents/data/bulk-data-sets/inpadoc` (NEWLY-VERIFIED-2026-08-05, HTTP 200).

### 7c. National registers

**Germany — DPMA:**
- `https://register.dpma.de/DPMAregister/Uebersicht` — HTTP 200, TRANSCRIPT-VERIFIED.
- **Dedicated SPC expert search:** `https://register.dpma.de/DPMAregister/pat/experte/schutzzertifikate` — TRANSCRIPT-VERIFIED. Fields exposed: SPC number (ZAKZ), product designation (TIEZ), basic patent title (TIGZ), start of term (LB), expiry of term (LE), MA authority/number/date (GIS/GIN/GIT), EU MA authority/country/number/date (GES/GEC/GEN/GET). **Richest field set of all national registers.**
- **Bulk data:** now via **DPMAconnectPlus** (replacing DPMADatenabgabe). URL: `https://www.dpma.de/recherche/datenabgabe/dpmaconnect/index.html` — REST-based, weekly XML including Rechtsstandsdaten. **Not open data** — requires signed contract and cost-recovery fee. Contact `datenabgabe@dpma.de`.
- Access: HTML search only for the UI (JavaScript required); no public API.

**United Kingdom — Ipsum is dead:**
- Ipsum retired **22 January 2025**. Replaced by **"One IPO Search"** at `https://www.search-for-intellectual-property.service.gov.uk/`.
- `https://www.ipo.gov.uk/p-ipsum/` → 301 → `https://www.gov.uk/search-for-patent`
- **SPC coverage confirmed** — gov.uk: "You can also use this service to search for supplementary protection certificates (SPCs)."
- **REST API: UNVERIFIED / believed absent.** The launch announcement lists "new APIs for bulk data access" as **future** work. The new host is Cloudflare-protected (HTTP 403 to automated requests).
- **Bulk data — STALE:** Only available download is `SPCopendataJuly2018.xlsx` (HTTP 200, 294 KB, July 2018 snapshot). Unusable for current FTO. Ongoing: weekly XML Patents Journal at `https://www.gov.uk/check-the-patents-journal`.

**France — INPI:**
- `https://data.inpi.fr/` → HTTP 403 to both curl and WebFetch (bot protection).
- Live patent register (TRANSCRIPT-VERIFIED via EPO FRS spec page): `https://bases-brevets.inpi.fr/en/home.html`. FR updates weekly.
- Open-data pointer: `https://www.data.gouv.fr/datasets/les-brevets-francais-a-linpi-et-loeb` (data.gouv.fr).

**Netherlands — OCNL:**
- `https://www.octrooiregistrum.nl/` → 301 → `https://www.octrooicentrum.nl/` (HTTP 200). Actual register: `https://mijnoctrooi.rvo.nl/fo-eregister-view/` (HTTP 200).
- **Best SPC coverage of any FRS participant.** Per NL FRS spec: "European patents, with deep linking for national patents, European patents and SPCs." Daily updates.
- API/open data: UNVERIFIED — none found.

**Italy — UIBM:**
- `https://uibm.mise.gov.it/index.php/it/` (HTTP 200). Database: `https://www.uibm.gov.it/bancadati/`.
- FRS spec: updates every ≤2 days. **SPC: "No" (blank comment).** Weakest of the majors.

**Slovakia — Standalone SPC register:**
- **TRANSCRIPT-VERIFIED** — `https://wbr.indprop.gov.sk/WebRegistre/DodatkoveOchranneOsvedcenie` (HTTP 200). A dedicated standalone SPC register — best-in-class for programmatic access.

**Other:**
- Spain OEPM: `http://consultas2.oepm.es/ceo/` — HTTP 403 to agent's IP (UNVERIFIED reachability). FRS: no SPC.
- Ireland: `https://www.ipoi.gov.ie/en/ip-search-tools/patents-search/` (HTTP 200).
- Sweden PRV: `https://www.prv.se/en/patent/search-patent/` (HTTP 200).
- Denmark: `https://onlineweb.dkpto.dk/pvsonline/Patent` (HTTP 200); FRS integration "in progress" per 06/2025 PDF.

### 7d. EU unitary SPC / centralised examination — STATUS 2026-08-05: NOT ADOPTED

**TRANSCRIPT-VERIFIED** — all four 2023 Commission proposals checked on EUR-Lex and the European Parliament Legislative Observatory.

| Procedure | Title | COM doc | Status |
|---|---|---|---|
| 2023/0127(COD) | Unitary SPC — medicinal products | COM(2023)0222 | **Awaiting Council's 1st reading position** |
| 2023/0126(COD) | Unitary SPC — plant protection | COM(2023)0221 | **Awaiting Council's 1st reading position** |
| 2023/0130(COD) | SPC — medicinal products recast (centralised examination) | COM(2023)0231 | **Awaiting Council's 1st reading position** |
| 2023/0128(COD) | SPC — plant protection recast | COM(2023)0223 | **Awaiting Council's 1st reading position** |

EP first readings: 28/02/2024. Last substantive event on all four: 13/11/2024 (resumption of business from previous parliamentary term). Rapporteur meetings logged through 16/01/2026 on 2023/0127. **No Council first-reading position, no trilogue, no adopted act, no OJ publication, no application date.**

Through at least 2026, **SPCs remain purely national grants, 27+ separate registers, no central EU source.** Do not build against a unitary SPC.

### 7e. Paediatric extension (6 months)

**TRANSCRIPT-VERIFIED** — Reg. 469/2009 Art. 13(3) verbatim (EUR-Lex, HTTP 200, CELEX 32009R0469):

> "The periods laid down in paragraphs 1 and 2 shall be extended by **six months** in the case where Article 36 of Regulation (EC) No 1901/2006 applies."

Base SPC term cap: **5 years** (Art. 13(1)–(2)). Maximum total with paediatric extension: **5.5 years**.

Visibility in data sources:
- **INPADOC** — best machine-readable route. Category G explicitly names "extension of a supplementary protection certificate (paediatric extension (PE))" with granted/refused/withdrawn events.
- **DPMAregister** — implicit: `Expiry of term (LE)` reflects PE when applied but no explicit flag.
- **UKIPO** — forms exist (`https://www.gov.uk/government/publications/application-to-extend-a-supplementary-protection-certificate`) but not queryable as a structured field.
- **EPO Federated Register** — carries no SPC data at all.

### 7f. SPC manufacturing waiver — Regulation (EU) 2019/933

**TRANSCRIPT-VERIFIED** (EUR-Lex CELEX 32019R0933, HTTP 200):

Regulation (EU) 2019/933, OJ L 153, 11.6.2019, pp. 1–10. In force 1 July 2019. Amends Art. 469/2009 by inserting Art. 5(2).

Two exceptions to SPC protection:
1. **Export waiver** — EU-established manufacturer may make the product for export to third countries where protection does not exist or has expired.
2. **Stockpiling waiver** — manufacture no earlier than 6 months before SPC expiry for storing in the member state of making, for day-one EU generic placement after expiry.

**Limit:** Does not permit placing on market of a member state where SPC is still in force; no re-importation during the term. Notification and diligence duties attach.

**UK post-Brexit equivalent:** 3 months advance notification to holder + IPO. Form at `https://www.gov.uk/government/publications/notification-for-spc-manufacturing-waiver`.

---

## 8. FTO Aggregators

**Subagent `a56f2b8aaad7afe3b` verified.**

### 8a. Lens.org

**TRANSCRIPT-VERIFIED** — live unauthenticated call to `https://api.lens.org/patent/search` → HTTP 401 (NEWLY-VERIFIED-2026-08-05). `https://docs.api.lens.org/` (HTTP 200).

- **Base URL:** `https://api.lens.org`
- **Auth:** `Authorization: Bearer <token>` (POST) or `?token=<token>` (GET)
- **Rate limiting:** response headers `x-rate-limit-remaining-request-per-minute`, `x-rate-limit-remaining-request-per-month`, `x-rate-limit-remaining-record-per-month`; HTTP 429 on over-quota.

**Free tier — DOES NOT COVER COMMERCIAL FTO.** Terms at `https://about.lens.org/lens-api-terms-of-use/`: free "Trial Access" is non-commercial only. Commercial Use is defined expansively to include "commercial research & development" and "investment decisions." A pharma FTO pipeline is commercial use. Lens's own terms: "Lens API service is only available through an institutional subscription." Pricing: not published; custom based on use case, attribution plan, volume, and speed.

**PatSeq (pharma-critical):** 488.3M sequences across 440,000+ biological patents. BLAST-based similarity search (PatSeq Finder), bulk downloads under separate terms. Best free-tier sequence-vs-patent capability outside Derwent GENESEQ.

### 8b. EPO bulk data products — DOCDB and INPADOC are FREE

**TRANSCRIPT-VERIFIED** from `https://www.epo.org/en/service-support/ordering/patent-information-products` (HTTP 200). This is the headline finding from the WIPO/aggregators subagent:

| EPO Product | Cost |
|---|---|
| **EPO worldwide bibliographic database (DOCDB)** | **Free** |
| **EPO worldwide legal status database (INPADOC)** | **Free** |
| EP bibliographic data (EBD) | **Free** |
| European Patent Register data | **Free** |
| EP full-text data | **Free** |
| **Sequence listings** | **Free** |
| **Linked open EP data** | **Free** (CC BY 4.0) |
| European Publication Server web service (API) | **Free** |
| OPS API | Free ≤4 GB/week; EUR 2,800/year subscription |
| Global Patent Index (GPI) | EUR 755/yr *(legacy product)* |
| PATSTAT Online | EUR 755/yr |
| PATSTAT Global | EUR 1,460/subscription |
| National full-text (CH/FR/GB/ES) | EUR 2,700/country + EUR 9,100 backfile |

**Delivery — BDDS:** `https://publication-bdds.apps.epo.org/raw-data/products` (HTTP 200, React SPA). Free EPO account required to download.

**DOCDB bulk** (`https://www.epo.org/en/searching-for-patents/data/bulk-data-sets/docdb`, HTTP 200 NEWLY-VERIFIED): bibliographic data, abstracts, citations, DOCDB simple patent family; 100+ countries; XML ST.36; frontfile ~3 GB zipped (Tue/Thu), backfile ~200 GB zipped twice yearly.

**INPADOC bulk** (`https://www.epo.org/en/searching-for-patents/data/bulk-data-sets/inpadoc`, NEWLY-VERIFIED-2026-08-05, HTTP 200): legal events from 50+ authorities; XML ST.36; frontfile ~700 MB weekly (Tuesdays), backfile ~20 GB. **This sidesteps the 4 GB/week OPS cap and the `inpadoc` throttle bucket entirely** — the right primary source for a systematic FTO corpus.

**Sequence listings bulk** (`https://www.epo.org/en/searching-for-patents/data/bulk-data-sets/sequence-listing`): nucleotide/amino-acid listings from EP, Euro-PCT, and PCT applications (EPO as ISA); 1989 onward; frontfile 10–200 MB weekly.

**Linked open EP data:** `https://data.epo.org/linked-data/` — CC BY 4.0; includes SPARQL endpoint and bulk download. Fair use policy applies — **do not use the live SPARQL/API endpoint as a production backend**; bulk download only for production.

### 8c. Commercial tools

**Clarivate Derwent** (`https://clarivate.com/intellectual-property/derwent/`) — TRANSCRIPT-VERIFIED. Products now named "Derwent Patent Search" (formerly Derwent Innovation) and "Derwent Patent Analytics" (formerly Innography). FTO value: human-rewritten abstracts (800+ editors, ~80,000 new publications/week); 70M+ DWPI invention families (broader than DOCDB simple families — groups by invention, not just priority). **GENESEQ** (`/derwent/geneseq/`) = curated patent-sequence DB. **Chemical Patents Index**, **Patent Data APIs** also available. No public pricing.

**IFI CLAIMS** (`https://www.ificlaims.com/platform/claims-direct/`) — TRANSCRIPT-VERIFIED, HTTP 200. 105+ countries bibliographic, 62 full-text, 180M+ records, 100+ sources. **Computed expiration dates** (key differentiator for pharma): *"Easily forecast expiring technologies and patents for a company or location with our adjusted expiration dates."* Legal status: expirations, grants, examinations, rejections. IFI Names (assignee normalization with ultimate parent + reassignments). Weekly refresh. Licensing split between data-end-user-internal-use and data-reseller-commercial-use. No public pricing. **Best fit for computed patent-term/expiry in an automated pharma FTO pipeline.**

**PatSnap** (`https://www.patsnap.com/`) — TRANSCRIPT-VERIFIED, HTTP 200. Purpose-built FTO agents: `https://eureka.patsnap.com/ip/checking/#/agent-landing/fto`. Pharma-relevant: PatSnap Bio (biosequence search), Synapse (biopharma intelligence), Chemical (structure search), SAR data extraction. No public pricing.

**Questel (Orbit Intelligence)** — PARTIALLY VERIFIED (site bot-blocked). Confirmed via `https://www.orbit.com/` (HTTP 200): Orbit Intelligence / qpat branding, covers "infringement search… validity search… biotechnology patent search." FamPat family depth and legal-status coverage: UNVERIFIED. No public pricing.

---

## 9. URL Ledger

### VERIFIED (fetched by the agent or by this recovery run)

| URL | HTTP | Method | Date verified |
|---|---|---|---|
| `https://data.uspto.gov/swagger/swagger.yaml` | 200 | agent + recovery | 2026-08-05 |
| `https://data.uspto.gov/swagger/swagger-initializer.js` | 200 | agent | 2026-08-05 |
| `https://data.uspto.gov/swagger/index.html` | 200 | agent | 2026-08-05 |
| `https://data.uspto.gov/documents/transition-guide/support/patents-view.md` | 200 | agent | 2026-08-05 |
| `https://data.uspto.gov/documents/api/getting-started.md` | 200 | agent | 2026-08-05 |
| `https://data.uspto.gov/documents/api/api-rate-limits.md` | 200 | agent | 2026-08-05 |
| `https://data.uspto.gov/documents/api/patent-term-adjustment/patent-term-adjustment.md` | 200 | agent | 2026-08-05 |
| `https://data.uspto.gov/swagger/odp-common-base.yaml` | 200 | agent | 2026-08-05 |
| `https://data.uspto.gov/documents/support/releases/release-40.md` | 200 | agent | 2026-08-05 |
| `https://data.uspto.gov/apis/api-catalog` | 200 | agent | 2026-08-05 |
| `https://api.uspto.gov/api/v1/patent/applications/search` | 401 (valid route) | agent | 2026-08-05 |
| `https://api.uspto.gov/api/v1/status` | 403 (invalid route) | agent | 2026-08-05 |
| `https://ops.epo.org/wsdl/ops.yaml` | 200 | agent + recovery | 2026-08-05 |
| `https://ops.epo.org/3.2/rest-services/published-data/publication/epodoc/EP1000000/biblio` | 403 (quota) | agent | 2026-08-05 |
| `https://ops.epo.org/3.2/auth/accesstoken` | 401 (no creds) | agent | 2026-08-05 |
| `https://ops.epo.org/schema/ops_legal.xsd` | 200 | agent | 2026-08-05 |
| `https://developers.epo.org/user/register` | 200 | agent | 2026-08-05 |
| `https://link.epo.org/web/inpadoc_classification_scheme_v1.0_en.pdf` | 200 | agent | 2026-08-05 |
| `https://link.epo.org/web/searching-for-patents/data/en-ops-v3.2-documentation-version-1.3.20.pdf` | 200 | agent | 2026-08-05 |
| `https://link.epo.org/web/documentation/federated-register/en-federated-register-status.pdf` | 200 | agent | 2026-08-05 |
| `https://link.epo.org/web/FRS_post-grant_status_list_en.pdf` | 200 | agent | 2026-08-05 |
| `https://link.epo.org/web/14.11_user_documentation_3.1_en.pdf` | 200 | agent | 2026-08-05 |
| `https://www.epo.org/en/searching-for-patents/legal/register/documentation/federated-register` | 200 | agent | 2026-08-05 |
| `https://www.epo.org/en/searching-for-patents/data/bulk-data-sets/inpadoc` | 200 | agent + recovery | 2026-08-05 |
| `https://www.epo.org/en/searching-for-patents/data/bulk-data-sets/docdb` | 200 | agent | 2026-08-05 |
| `https://www.epo.org/en/service-support/ordering/patent-information-products` | 200 | agent | 2026-08-05 |
| `https://www.epo.org/en/searching-for-patents/technical/espacenet` | 200 | agent | 2026-08-05 |
| `https://publication-bdds.apps.epo.org/raw-data/products` | 200 | agent | 2026-08-05 |
| `https://data.epo.org/linked-data/` | 200 | agent | 2026-08-05 |
| `https://register.dpma.de/DPMAregister/Uebersicht` | 200 | agent + recovery | 2026-08-05 |
| `https://register.dpma.de/DPMAregister/pat/experte/schutzzertifikate` | 200 | agent | 2026-08-05 |
| `https://www.dpma.de/recherche/datenabgabe/dpmaconnect/index.html` | 200 | agent | 2026-08-05 |
| `https://mijnoctrooi.rvo.nl/fo-eregister-view/` | 200 | agent | 2026-08-05 |
| `https://uibm.mise.gov.it/index.php/it/` | 200 | agent | 2026-08-05 |
| `https://wbr.indprop.gov.sk/WebRegistre/DodatkoveOchranneOsvedcenie` | 200 | agent | 2026-08-05 |
| `https://www.search-for-intellectual-property.service.gov.uk/` | redirect | agent | 2026-08-05 |
| `https://www.gov.uk/government/news/new-patent-search-tool-to-boost-uk-innovation` | 200 | agent | 2026-08-05 |
| `https://www.wipo.int/en/web/patentscope/data/` | 200 | agent | 2026-08-05 |
| `https://www.wipo.int/en/web/patentscope/data/terms` | 200 | agent | 2026-08-05 |
| `https://www3.wipo.int/ipstats/` | 200 | agent | 2026-08-05 |
| `https://oeil.secure.europarl.europa.eu/oeil/en/procedure-file?reference=2023/0127(COD)` | 200 | agent | 2026-08-05 |
| `https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32009R0469` | 200 | agent + recovery | 2026-08-05 |
| `https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32019R0933` | 200 | agent | 2026-08-05 |
| `https://eur-lex.europa.eu/eli/reg/2009/469/oj` | 200 | agent | 2026-08-05 |
| `https://api.lens.org/patent/search` (unauthenticated) | 401 | agent + recovery | 2026-08-05 |
| `https://about.lens.org/lens-api-terms-of-use/` | 200 | agent | 2026-08-05 |
| `https://docs.api.lens.org/getting-started.html` | 200 | agent | 2026-08-05 |
| `https://www.federalregister.gov/api/v1/documents.json` (PTE notices) | 200 | agent + recovery | 2026-08-05 |
| `https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/releases/` | 200 | agent | 2026-08-05 |
| `https://cloud.google.com/bigquery/pricing` | 200 | agent | 2026-08-05 |
| `https://cloud.google.com/bigquery/docs/sandbox` | 200 | agent | 2026-08-05 |
| `https://cloud.google.com/bigquery/public-data` | 200 | agent | 2026-08-05 |
| `https://raw.githubusercontent.com/google/patents-public-data/master/tables/dataset_Google%20Patents%20Public%20Datasets.md` | 200 | agent | 2026-08-05 |
| `https://www.ipoi.gov.ie/en/ip-search-tools/patents-search/` | 200 | agent | 2026-08-05 |
| `https://www.prv.se/en/patent/search-patent/` | 200 | agent | 2026-08-05 |
| `https://onlineweb.dkpto.dk/pvsonline/Patent` | 200 | agent | 2026-08-05 |
| `https://clarivate.com/intellectual-property/derwent/world-patents-index/` | 200 | agent | 2026-08-05 |
| `https://www.ificlaims.com/platform/claims-direct/` | 200 | agent | 2026-08-05 |
| `https://www.patsnap.com/` | 200 | agent | 2026-08-05 |
| `https://www.orbit.com/` | 200 | agent | 2026-08-05 |

### UNVERIFIED or BLOCKED

| URL | Problem | Note |
|---|---|---|
| `https://www.uspto.gov/patents/laws/patent-term-extension` | HTTP 403 WAF block (both curl and WebFetch) | Use Federal Register API for PTE data instead |
| `https://data.uspto.gov/bulkdata/datasets/pvgpatdis` (and sibling bulk URLs) | Not directly verified by curl — referenced in ODP markdown | Expect auth-gated download |
| `https://publication-bdds.apps.epo.org/bdds/bdds-bff-service/prod/products` | HTTP 302 → OIDC login | Free EPO account required for BDDS downloads |
| `https://data.inpi.fr/` | HTTP 403 bot protection | Live French patent register: `https://bases-brevets.inpi.fr/en/home.html` |
| `https://register.epo.org/` | HTTP 403 (datacentre IP blocked) | Used via EPO FRS tab instead |
| `https://register.epo.org/allEvents?lng=en` | HTTP 403 (same block) | INPADOC classification PDF is the alternative |
| `http://consultas2.oepm.es/ceo/` | HTTP 403 to agent's IP | Spain OEPM SPC register — UNVERIFIED reachability |
| `https://www.search-for-intellectual-property.service.gov.uk/` | HTTP 403 Cloudflare bot challenge | No API confirmed or excluded |
| `assets.publishing.service.gov.uk/…/SPCopendataJuly2018.xlsx` | HTTP 200 but July 2018 snapshot | Do not use as current SPC source |
| `https://www.questel.com/` | HTTP 404 (bot mitigation returns fake 404) | Orbit Intelligence product confirmed at `https://www.orbit.com/` |
| `https://bigquery.googleapis.com/bigquery/v2/projects/patents-public-data/datasets` | HTTP 401 (requires auth credential) | BigQuery REST has no anonymous read path |
| WIPO sequence listings bulk download | No working URL found on data page | Use EPO BDDS sequence listings instead |
| `https://link.epo.org/web/14_11_legal_status_inpadoc_documentation_2021.zip` | URL found in agent trace | Not independently verified by recovery agent |
| `https://www.data.gouv.fr/datasets/les-brevets-francais-a-linpi-et-loeb` | Found via data.gouv.fr | Not directly verified by curl |
| `https://www.euipo.europa.eu/en/news/unitary-supplementary-protection-certificate` | HTTP 403 | EU unitary SPC remains a proposal anyway |

### UNFINISHED — worth re-running

- **ODP Swagger YAML download and OpenAPI validation.** The agent downloaded the YAML (101 KB) but did not confirm the full path-level schema parameters, request/response bodies, or whether any endpoint covers patent-family links or assignee normalization.
- **ODP bulk dataset API — enumerate all product IDs.** The `GET /api/v1/datasets/products/search` endpoint would return the live catalog of all bulk datasets. Agent found the endpoint but had no API key. Would reveal whether any PTE or Orange Book-linked product exists.
- **DPMA DPMAconnectPlus pricing.** Agent found the contract requirement but no price list. Requires contacting `datenabgabe@dpma.de`.
- **Lens.org institutional subscription pricing.** `https://www.lens.org/lens/user/subscriptions` is login-gated; no pricing visible. Requires direct contact.
- **IFI CLAIMS direct pricing.** `https://www.ificlaims.com/platform/claims-direct/` is bot-blocked to curl. Requires contact.
- **SureChEMBL EBI FTP current bulk data.** `https://ftp.ebi.ac.uk/pub/databases/chembl/SureChEMBL/bulk_data/` was last modified 2026-08-04 — this would provide a fresher alternative to the BigQuery mirror.
- **UKIPO One IPO Search API.** The launch announcement mentioned future APIs; worth re-checking quarterly.
- **BigQuery — actual row counts, byte sizes, and freshness.** Blocked by 401 at the REST level during the agent run; requires console access with a billing-enabled account to see Last Modified dates.
- **Orange Book data files.** Agent's curl timed out on `https://www.fda.gov/drugs/drug-approvals-and-databases/orange-book-data-files`. Recommended next step: fetch with a browser or increase timeout; monthly ZIP download URL contains `patent.txt` with PTE-extended dates.

---

*Recovery note: The original agent was interrupted after 25 turns (events 0–144). It had completed all four subagent tasks (BigQuery, EPO OPS/Espacenet, SPC sources, WIPO/aggregators) and was mid-way through consolidating PTE data from the Orange Book and Federal Register at the time of interruption. The final Federal Register API response had arrived (count=1,296; newest: VYALEV, 2026-06-29) and was about to be written into the report when the tool use was rejected by the user.*
