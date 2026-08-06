<!-- RECOVERED from subagent transcript agent-a078ccb1f9bed4307.jsonl, session fd64561f-7c90-41a2-95cf-b4a133a8fe0f, research date 2026-08-05.
     EPO Open Patent Services + Espacenet, incl. SPC via the legal service.
     Verbatim agent deliverable — not re-edited. -->

Verification complete. All claims below were confirmed by direct HTTP fetches.

# EPO OPS & Espacenet — Verification Report

## 0. The 403 is NOT an auth error — caller's premise is wrong

**VERIFIED.** `curl -i https://ops.epo.org/3.2/rest-services/published-data/publication/epodoc/EP1000000/biblio` → **HTTP 403**, header **`x-rejection-reason: AnonymousQuotaPerDay`**, body:
```xml
<error><code>403</code><message>This request has been rejected due to the violation of Fair Use policy</message><moreInfo>https://www.epo.org/service-support/ordering/fair-use.html</moreInfo></error>
```
This is a **fair-use quota rejection on the anonymous tier**, not "credentials missing". OPS *does* serve anonymous traffic under a per-day quota; this IP's anonymous pool is exhausted. Contrast (**VERIFIED**): same URL with `Authorization: Bearer bogustoken123` → **HTTP 400**, `www-authenticate: Bearer realm="null",error="invalid_token",error_description="keymanagement.service.invalid_access_token"`, body `<code>400</code><message>invalid_access_token</message>`.

**Three distinct failure modes to code against:** 403 + `X-Rejection-Reason` = quota; 400 `invalid_access_token` = expired/bad token (re-auth); 404 `This API version is not supported` = wrong version path.

## 1. Base URL and current version — still 3.2 ✅

**VERIFIED** from EPO's own OpenAPI spec, `https://ops.epo.org/wsdl/ops.yaml` (HTTP 200): `version: "3.2"`, `host: ops.epo.org`, **`basePath: /3.2/rest-services`**. Confirmed by the current doc filename: `en-ops-v3.2-documentation-version-1.3.20.pdf` (Reference Guide v1.3.20, June 2024).

Probe results on `/rest-services/.../biblio` — **note the quota gate masks version routing**, so this is a weak discriminator:

| Path | Status | Body |
|---|---|---|
| `/3.0/`, `/3.1/` | **404** | `This API version is not supported` → `https://forums.epo.org/3-1-end-of-life-final-time-plan-7431` |
| `/3.2/`, `/3.3/`, `/4.0/`, `/9.9/`, `/foo/` | 403 | AnonymousQuotaPerDay (quota checked before version) |

**The clean discriminator is the auth endpoint** (VERIFIED): `POST /{v}/auth/accesstoken` returns **401** (route exists) only for `3.1`, `3.2`, and bare `/auth/accesstoken`; `3.3`, `4.0`, `5.0`, `2.0`, `xyz` all fall through to 403. Since 3.1 rest-services is explicitly EOL, **3.2 is the only live version. There is no 4.0.** Bare `/rest-services/` (no version) also 403s rather than 404s, and EPO's own docs use it in examples — but pin `/3.2/`.

## 2. OAuth2 client-credentials — fully verified

**Token endpoint: `https://ops.epo.org/3.2/auth/accesstoken`** — **VERIFIED** by probe *and* by the PDF (p.35).
- No creds → **401** `<message>Client identifier is required</message>`, `www-authenticate: Basic`
- Bogus Basic creds → **401** `<message>ClientId is Invalid</message>`
- `GET` instead of `POST` → **404** (POST only)

Mechanics (**VERIFIED**, PDF pp.35-36):
- `Authorization: Basic base64(consumer_key:consumer_secret)` — Base64 of colon-joined key:secret
- `Content-Type: application/x-www-form-urlencoded`, payload **`grant_type=client_credentials`**
- Response JSON: `"token_type": "Bearer"`, `"expires_in": "1199"`, `"access_token": "..."`, plus `issued_at`, `scope: "core"`, `api_product_list: "[ops-prod]"`
- **Lifetime ≈ 20 min** (1199 s). Docs: request a new token as soon as an invalid-token message is received (no refresh flow — `refresh_count: 0`).
- Subsequent calls: **`Authorization: Bearer <token>`**
- Only the Client Credentials flow is supported. Ref: RFC 6749.

## 3. Registration and free tier

- **Register: `https://developers.epo.org/user/register`** (login `/user/login`; portal `https://developers.epo.org/`) — **VERIFIED**, HTTP 200, linked as "Register"/"Log in" from the OPS page. You define an "App" to get Consumer Key + Secret; multiple credential sets per developer allowed.
- **Free tier = 4 GB/week.** **VERIFIED** twice: fair-use charter — "Open Patent Services (OPS, up to a weekly maximum of 4 GB) are available free of charge"; OPS page — `"Non-paying" users / Up to 4 GB of data per week / Free` vs `"Paying" users / More than 4 GB per week / Annual subscription: EUR 2 800`.
- **Global 1 Mbps rule enforced as ~450 MB/hour** (VERIFIED, PDF p.40). Hourly quota refreshes on a **rolling** window; **weekly quota resets each calendar week at midnight UTC**.
- Quota headers (VERIFIED): `X-IndividualQuotaPerHour-Used`, `X-RegisteredQuotaPerWeek-Used`, `X-RegisteredPayingQuotaPerWeek-Used`, `X-Rejection-Reason`.

**Throttling — `X-Throttling-Control`** (VERIFIED, PDF pp.41-42). Returned on **every** response, per-user-system. Format:
```
X-Throttling-Control: system-state (service-name=traffic-light-position:request-limit, ...)
e.g. idle (retrieval=green:200, search=yellow:20, inpadoc=red:30, images=green:200, other=green:1000)
```
System state ∈ **idle / busy / overloaded**. Lights: **green** <50% of limit used, **yellow** 50-75%, **red** >75%, **black** = exceeded, service temporarily suspended. Limits are per-service *and* shrink with system state (e.g. retrieval 200→100→50, search 30→15→5, inpadoc 60→45→30 per minute as idle→busy→overloaded). Self-throttle over a **60-second window** to the most negative value seen, or risk temporary/permanent suspension.

**Throttle bucket mapping (VERIFIED, Table 16):** `search`→`/published-data/search/*`; `retrieval`→`/published-data/*/`; **`inpadoc`→`/family/*` AND `/legal/*`**; `images`→`/published-data/images/*`, `/classification/cpc/media/*`; everything else→`other`. **Gotcha for FTO: legal-status calls share the `inpadoc` bucket with family calls, and it is the tightest non-search bucket (60/45/30).**

## 4. Service families — exact paths

**VERIFIED** — complete enumeration from `ops.yaml`. All prefixed `https://ops.epo.org/3.2/rest-services`. `{type}`=publication|application|priority, `{format}`=docdb|epodoc|original. GET (and POST for bulk, max 100 refs).

| Service | Path pattern | Returns |
|---|---|---|
| published-data | `/published-data/search[/{constituent}]` | Biblio search (CQL) |
| | `/published-data/{type}/{format}/{number}/biblio` | Bibliographic data |
| | `.../abstract`, `.../claims`, `.../description`, `.../fulltext` | Text constituents |
| | `.../full-cycle` | All publication stages |
| | `.../equivalents` | Equivalents |
| | `/published-data/images/{cc}/{no}/{kind}/{type}` | Page images |
| **family** | `/family/{type}/{format}/{number}` | **INPADOC simple family** |
| | `/family/{type}/{format}/{number}/biblio` | Family + biblio |
| | **`/family/{type}/{format}/{number}/legal`** | **Family + legal status — the FTO workhorse** |
| **legal** | `/legal/{type}/{format}/{number}` | Legal events for one doc |
| register | `/register/{type}/{format}/{number}/biblio` | EP Register biblio |
| | `.../events`, `.../procedural-steps`, `.../upp` | Register events, procedural steps, **unitary patent** |
| | `/register/search[/{constituent}]` | Register search |
| classification | `/classification/cpc[/{class}[/{subclass}]]`, `/classification/cpc/search`, `/classification/cpc/media/{name}`, `/classification/map/{in}/{class}/{subclass}/{out}` | CPC scheme, stats, media, IPC↔CPC mapping |
| number-service | `/number-service/{type}/{input-format}/{number}/{output-format}` | Number format conversion (epodoc↔docdb↔original) |

Also: `/3.2/developers/me/stats/usage` — data usage API (needs Bearer token).

## 5. SPC in the legal service — YES, confirmed end-to-end ✅ (with a major caveat)

This is the key finding. The chain is fully verified across three EPO documents.

**a) SPC events are a first-class INPADOC category. VERIFIED** — EPO INPADOC classification scheme page: "events related to applications for supplementary protection certificates are covered by the scheme in **category G (Protection beyond IP right term)**". Scheme = 21 categories A-Z, modelled on WIPO ST.27, ~2 800 legal event codes classified since 1997, new codes added monthly. PDF: `https://link.epo.org/web/inpadoc_classification_scheme_v1.0_en.pdf` (HTTP 200). Category G explicitly covers **SPC**, **SPC paediatric extension (PE)**, patent term adjustment (PTA), term extension — with events: requested / not requested / found admissible / refused / withdrawn / not granted / **granted or registered**. **Gotcha: SPC *discontinuation* is category H (cessation), not G**; modified SPCs are category P; SPC publication is category Q. An FTO query filtering only on G will miss SPC death events.

**b) OPS's own legal schema carries the SPC fields. VERIFIED** — `https://ops.epo.org/schema/ops_legal.xsd` (HTTP 200). `<ops:legal>` has attributes `code`, `desc`, `infl`, `dateMigr` and contains `<ops:L500EP>`, which contains **L501EP–L533EP**.

**c) Those exact L-codes are the SPC fields. VERIFIED** — EPO "Legal status tag definition" PDF (`https://link.epo.org/web/14.11_user_documentation_3.1_en.pdf`) and the INPADOC Legal Status user documentation (`https://link.epo.org/web/14_11_legal_status_inpadoc_documentation_2021.zip` → `T03.03_User Documentation Legstat_XML vs. 1.7.7.pdf`, §6.4):

| OPS tag | XML mapping | Meaning |
|---|---|---|
| `L511EP` | `<legal-event><spc><spc-number>` | **SPC number** |
| `L512EP` | `<spc><date-filing>` | SPC filing date |
| `L513EP` | `<spc><date-expiry-of-patent>` | Expiry date of underlying patent |
| `L523EP` | `<spc><date-extension-granted>` | **Date extension granted (SPC/PE)** |
| `L510EP` | `<spc><text>` | **Free-format text, max 700 chars** |

EPO's own worked example (event code `R067`, DE): `<spc-number>122013000086</spc-number>`, `<date-filing>20131107</date-filing>`, `<date-expiry-of-patent>20240723</date-expiry-of-patent>`, `<date-extension-granted>20280829</date-extension-granted>`, `<text>PRODUCT NAME: REGORAFENIB ODER EIN SALZ DAVON; REGISTRATION NO/DATE: EU/1/13/858 20130826</text>`.

**⚠️ THE CRITICAL FTO CAVEAT — VERIFIED verbatim (§3.5):** "In the legacy product SPC product information is exchanged in `<L510EP>`, in **free text format**… It is the intention to enhance the representation of SPC data in the future and offer product information in a richer tag structure… **Until that time SPC product information will be exchanged in element `<text>`**." So **the active ingredient / product name and the marketing-authorisation number — the two fields that actually matter for pharma FTO — are unstructured free text in a single 700-char field, in the national language** (the example is German). You must regex/NLP-parse `PRODUCT NAME:` / `REGISTRATION NO/DATE:` and handle multilingual variants. There is no structured active-ingredient field. Note this documentation is dated May 2018 / packaged 2021 and the "future enhancement" has not shipped.

**Also note:** the 154-page OPS Reference Guide v1.3.20 contains **zero** occurrences of "SPC" or "supplementary protection" — SPC support is real but entirely undocumented in the OPS guide itself; you must cross-reference the INPADOC legal status docs. INPADOC covers **50+ patent authorities**, gazettes and registers, incl. EPO and WIPO. **UNVERIFIED:** actual per-jurisdiction SPC coverage/completeness and live response payloads — I could not execute an authenticated call (no credentials; anonymous quota exhausted). Validate against known SPCs (e.g. EP + DE/FR/GB SPC families) once keyed.

## 6. Espacenet — no separate API; EPO says use OPS

**VERIFIED verbatim**, `https://www.epo.org/en/searching-for-patents/technical/espacenet` (HTTP 200):
> "For automated data retrieval, please use the EPO's **Open Patent Services (OPS)**."
> "It is **not intended for bulk data retrieval**. The service does **not support automated searches (robots)** and will **deny access to any robots it identifies**."

**Consistent with probing (VERIFIED):** `worldwide.espacenet.com/`, `/patent/search`, `/advancedSearch`, `/searchResults`, `/patent/` all return **HTTP 403 with a 1-byte body**, even with a full desktop Chrome User-Agent. `robots.txt` returns a single `.`. Bot protection is unconditional for non-browser clients. **Do not build on Espacenet's internal endpoints** — it violates the stated terms and is actively blocked. Classic vs new: "Open Espacenet" = `https://worldwide.espacenet.com/`, "Open classic Espacenet" = `https://worldwide.espacenet.com/?locale=en_EP`. **UNVERIFIED:** whether an internal JSON API exists behind the SPA — I could not load the app at all to observe XHRs, and probing further would mean evading bot detection.

**Bulk/FTP alternative — VERIFIED, and worth considering for FTO at scale.** EPO **Bulk Data Distribution Service (BDDS)**: `https://publication-bdds.apps.epo.org/raw-data/products` (HTTP 200, React SPA; JS bundle exposes only `/products` and `/oidc/login` → **OIDC login-gated**, no anonymous API). Product **EPO worldwide legal event data (INPADOC)**, `https://www.epo.org/en/searching-for-patents/data/bulk-data-sets/inpadoc`: **XML ST36**, **frontfile ~700 MB weekly** (usually Tuesdays), **backfile ~20 GB** twice a year, 50+ authorities, licensed under EPO database terms. Process backfile first, then weekly deltas. This sidesteps the 4 GB/week OPS cap and the `inpadoc` throttle bucket entirely — likely the right primary source for a systematic FTO corpus, with OPS for targeted/live lookups.

## Key gotchas for the pipeline

1. **Never treat 403 as "needs auth"** — check `X-Rejection-Reason`. 400 `invalid_access_token` is the re-auth signal.
2. **Token TTL ~20 min, no refresh token** — re-POST to `/3.2/auth/accesstoken` on 400.
3. **`/legal/*` and `/family/*` share the tightest `inpadoc` throttle bucket** (60/45/30 per min by system state). Parse `X-Throttling-Control` on every response and back off over 60 s.
4. **4 GB/week free; >4 GB = EUR 2 800/yr.** Weekly reset midnight UTC; hourly ~450 MB rolling.
5. **SPC product/active-ingredient data is free text in L510EP, multilingual** — the single biggest data-quality risk for pharma FTO.
6. **SPC lifecycle spans categories G/H/P/Q**, not G alone.
7. Bulk retrieval caps at **100 references** per POST; `SERVER.LimitedServerResources` means reduce range size.
8. Espacenet is off-limits for automation by EPO policy and technically blocked.

**Canonical URLs:** OPS docs PDF `https://link.epo.org/web/searching-for-patents/data/en-ops-v3.2-documentation-version-1.3.20.pdf` · OpenAPI `https://ops.epo.org/wsdl/ops.yaml` · legal XSD `https://ops.epo.org/schema/ops_legal.xsd` · tag definitions `https://link.epo.org/web/14.11_user_documentation_3.1_en.pdf` · INPADOC legal status docs `https://link.epo.org/web/14_11_legal_status_inpadoc_documentation_2021.zip` · classification scheme `https://link.epo.org/web/inpadoc_classification_scheme_v1.0_en.pdf` · fair use `https://www.epo.org/en/service-support/ordering/fair-use` · register `https://developers.epo.org/user/register`

Note: I wrote no files to the repo — all downloads went to `/tmp` as scratch.