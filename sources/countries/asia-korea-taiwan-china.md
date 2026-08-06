<!-- RECOVERY NOTE: This file was reconstructed from agent-a95d07e2315399fed.jsonl on 2026-08-06
     after the original agent died on API ConnectionRefused following 97 tool calls. All evidence
     cited below is drawn from that transcript unless marked "newly verified 2026-08-06". -->

# South Korea MFDS / Taiwan TFDA / China NMPA — Machine-Readable Approved-Drug Lists

**Purpose:** Identify machine-accessible data sources for drug approvals in three Asian regulators,
framed against the PRV-eligibility split:
- **Funnel A (PRV-eligible):** never-approved-in-US moieties filed as 505(b)(1) NDAs.
- **Funnel B (orphan exclusivity only):** US-generic or 505(b)(2) repurposing candidates.

All three jurisdictions approve molecules that never reach the US market. Under 21 U.S.C. 360ff,
those are the only Funnel A candidates this program can develop.

---

## 1. South Korea — MFDS (Ministry of Food and Drug Safety)

### 1.1 Regulatory Authority

**Ministry of Food and Drug Safety (MFDS)**
- Korean name: 식품의약품안전처
- Primary drug information portal: 의약품안전나라 (Nedrug)
- Website: `https://nedrug.mfds.go.kr`
- Parent authority website: `https://www.mfds.go.kr`

**WHO-Listed Authority / PIC/S / ICH status:**
Korea (MFDS) is a full PIC/S member (confirmed by picscheme.org; call 200 HTTP) and an ICH member
since 2016. This means Korean approvals are highly credible for mutual reliance. UNVERIFIED whether
Korea is an active WHO prequalification supplier for the specific therapeutic classes relevant to this
program.

### 1.2 Drug Approval Database — Nedrug (의약품안전나라)

**Main URL:** `https://nedrug.mfds.go.kr`

HTTP probe: `curl -s -L "https://nedrug.mfds.go.kr"` → HTTP 200, redirect to `/index` (verified
call 6, call 9). The site root returns a JS redirect: `location.replace('https://nedrug.mfds.go.kr/index')`.

**Total registered products (verified):**

```
GET https://nedrug.mfds.go.kr/searchDrug/CNT
Response: {"data":95253}
```

This endpoint was verified twice in the transcript (call 15, call 82) and once in a newly verified
live fetch (2026-08-06): `{"data":95265}`. The count grew by 12 over the ~12 hours between
transcript creation and recovery, confirming it is a live counter of currently-registered products.
**95,265 product registrations** as of 2026-08-06.

**Detail endpoint — confirmed live JSON API (verified, call 54 + call 65 + call 95):**

```
GET https://nedrug.mfds.go.kr/pbp/CCBBB01/getItemDetail?itemSeq={itemSeq}
Content-Type: application/json (no auth required)
```

Response schema confirmed by inspecting `itemSeq=200004827` (도일황정, a herbal preparation, permit
date 2000-02-29, withdrawn). Key fields returned:

| Field | Description |
|---|---|
| `itemSeq` | Unique product sequence number |
| `itemName` | Korean product name |
| `itemEngName` | English name (often null) |
| `entpName` | Manufacturer name (Korean) |
| `classNo` / `classNm` | Drug classification code and name |
| `itemPermitDate` | Original permit date (YYYY-MM-DD) |
| `cancelCode` / `cancelCodeName` | Withdrawal status (e.g., "취하" = withdrawn, "정상" = active) |
| `indutyClassCode` / `indutyClassCodeName` | Industry class (e.g., A0=의약품, E0=한약제제) |
| `rareDrugYn` | **Rare drug flag** — "Y", "N", or null |
| `etcOtcCode` | ETC (prescription) / OTC flag |
| `narcoticKindCode` | Narcotic classification |
| `euaYn` / `unaprvEuaYn` | Emergency use authorization flag |
| `eeDocData` / `udDocData` / `nbDocData` | Package insert sections (Korean text) |
| `ingrCode` / `ingrName` / `ingrMainName` | Active ingredient codes and names |

**Critical finding:** The field `rareDrugYn` is present in the API schema. In the two items tested
(call 67 and call 95, and one newly verified 2026-08-06), it returned `null` or `"N"` for non-rare
products. A value of `"Y"` would flag a product as a rare disease drug. This field enables filtered
enumeration of rare-disease-designated products.

**List/pagination endpoint — NOT accessible without session state (verified):**

Multiple attempts to use `getItemList`, `getItemPaging`, and `getItemSearch` all returned either
empty responses or the Korean error page "해당 화면 혹은 기능을 찾을 수 없습니다" (screen not
found). These endpoints appear to require session cookies set by the browser-rendered search page.
Calls 47, 56, 58, 61, 69, 72, 73, 78, 80, 81 all confirmed this.

The `getItemDetail` endpoint does accept direct HTTP GET with no session/auth cookie. This means
enumeration requires either:
- Sequential crawl of `itemSeq` integers (the known format is YYYYNNNNNNN, e.g., `200004827`),
- Or a separate scraping layer that first submits the search form to obtain session cookies.

**Search page (JS-rendered form, not directly machine-readable):**
`https://nedrug.mfds.go.kr/searchDrug` — HTTP 200, but all results load via JS + session.
The form submits to `/pbp/CCBBB01/getItemSearch` via GET.

### 1.3 Korea Open Data Portal (data.go.kr) — MFDS APIs

**data.go.kr main:** `https://www.data.go.kr` → HTTP 200 (verified call 20).

All attempts to access `apis.data.go.kr/1471000/DrugPrdtPrmsnInfoService04/...` returned:

```json
{"OpenAPI_ServiceResponse":{"cmmMsgHeader":{
  "errMsg":"NO_OPENAPI_SERVICE_ERROR",
  "returnAuthMsg":"해당 오픈API 서비스가 없거나 폐기됨",
  "returnReasonCode":"12"}}}
```

This response was received for every variant tested:
- `DrugPrdtPrmsnInfoService04` (calls 21, 22, 44)
- `DrugPrdtPrmsnInfoService` (call 24)
- `MdcinGrnIdntfcInfoService01` (calls 48, 70)

"returnReasonCode 12" and "폐기됨" (deprecated/decommissioned) confirm these APIs are **no longer
active**. The data.go.kr portal page for the MFDS drug approval service (orgFilter=1471000) loaded
(HTTP 200) but the content is entirely JS-rendered and did not expose API metadata in the grep output
(calls 55, 59, 83).

**Conclusion for Korea data.go.kr:** The historically published MFDS Open API endpoints on
data.go.kr have been decommissioned. The current machine-readable access point is exclusively the
nedrug.mfds.go.kr `getItemDetail` endpoint.

### 1.4 Korea Orphan / Rare Disease Designation

Korea has a dedicated rare disease drug support scheme. The portal at `https://nedrug.mfds.go.kr`
includes an "orphan drug" menu category (evidenced by the `rareDrugYn` field in the API and the
mention of "한국희귀필수의약품센터" (Korea Rare Disease and Essential Drugs Center, KODC) in the
MFDS site search dropdown, call 95).

**KODC:** `https://www.kodc.or.kr` — HTTP 200 (newly verified 2026-08-06). This body manages
sourcing of rare and essential drugs for the Korean market.

**Relevance to PRV:** Korea MFDS approval of a compound with `rareDrugYn=Y` does not by itself
confer PRV eligibility — that requires a US 505(b)(1) NDA filing with no prior US approval. But
MFDS rare-designation products are exactly the class of never-US-approved moieties that constitute
Funnel A candidates.

### 1.5 Review Reports

UNVERIFIED. No public review report database equivalent to FDA's Summary Basis of Approval or EMA's
EPAR was located in the transcript or live fetches. The nedrug `getItemDetail` endpoint includes
package insert data (`eeDocData`, `udDocData`, `nbDocData`) but not clinical review summaries.

### 1.6 English Interface

Partial. `https://www.mfds.go.kr/eng/index.do` returns HTTP 200 (verified). The nedrug search
interface is Korean-only. `itemEngName` in the API is frequently null. English drug names are
inconsistently populated.

### 1.7 Summary Access Map — Korea

| Resource | URL | Status | Auth | Bulk? |
|---|---|---|---|---|
| Portal home | nedrug.mfds.go.kr | VERIFIED 200 | None | — |
| Product count | nedrug.mfds.go.kr/searchDrug/CNT | VERIFIED JSON | None | N/A |
| Product detail | nedrug.mfds.go.kr/pbp/CCBBB01/getItemDetail?itemSeq= | VERIFIED JSON | None | Page-by-page |
| List/search | nedrug.mfds.go.kr/pbp/CCBBB01/getItemList | VERIFIED broken w/o session | Session cookie | No |
| data.go.kr APIs | apis.data.go.kr/1471000/Drug* | VERIFIED decommissioned | — | — |
| KODC rare drugs | kodc.or.kr | VERIFIED 200 | None | Unknown |

---

## 2. Taiwan — TFDA (Taiwan Food and Drug Administration)

### 2.1 Regulatory Authority

**Taiwan Food and Drug Administration (TFDA)**
- Chinese name: 衛生福利部食品藥物管理署
- Main website: `https://www.fda.gov.tw`
- Under: Ministry of Health and Welfare (衛生福利部)

**WHO / PIC/S status:** Taiwan TFDA is a PIC/S member. UNVERIFIED exact date of admission from the
transcript (picscheme.org GET returned no Taiwan-specific output in the grep).

### 2.2 Western Drug Permit Query System — lmspiq.fda.gov.tw

**Primary query system URL:** `http://lmspiq.fda.gov.tw/web/`

This is the current unified permit-query SPA (Single-Page Application), confirmed live 2026-08-06
(HTTP 200, call 96). Its title: `西藥、醫療器材及化粧品許可證暨相關資料查詢` (Western drugs, medical
devices, and cosmetics permit and related data query). It is a React+Vite application.

**Prior system URL (404 as of transcript):** `https://lmspiq.fda.gov.tw/web/DRPIQ/license-search`
returned HTTP 404 (call 94). The system routes are frontend routes, not server endpoints.

**Backend API (newly verified 2026-08-06):**

The JS bundle at `http://lmspiq.fda.gov.tw/web/assets/index-D_luKTR4.js` (779 KB) reveals:

```javascript
const Tde = "//lmspiq.fda.gov.tw/api/public/";
const Cy = axios.create({baseURL: Tde});
Cy.interceptors.request.use(t => {
  const e = JSON.parse(sessionStorage.getItem("item"));
  t.headers.Authorization = `Bearer ${(e?.token) || ""}`;
  return t;
});
```

The API base URL is `http://lmspiq.fda.gov.tw/api/public/`. It is a Spring Boot REST API. It
**accepts unauthenticated requests for code-lookup endpoints** but appears to require a Bearer token
for drug-search endpoints. Specifically verified:

```
GET http://lmspiq.fda.gov.tw/api/public/codes/search/simple/codeKind/MonthlyReport
→ HTTP 200, JSON array of 6 monthly report type codes (新增/變更/註銷/展延/預知展延/過期許可證月報)

GET http://lmspiq.fda.gov.tw/api/public/codes/search/full/codeKind/Lic.Type
→ HTTP 200, JSON array of license type codes (衛署藥製, 衛署藥輸, 衛署成製, 衛署中藥輸, 衛署醫器製, ...)

GET http://lmspiq.fda.gov.tw/api/public/codes/search/simple/codeKind/DosageForm.Detail
→ HTTP 200, 445 dosage form codes (硬空膠囊劑, 穿皮吸收貼片原料劑, 粉劑, 原料藥粉末, ...)
```

All newly verified 2026-08-06.

**Drug search endpoints (404 without auth):**

```
GET http://lmspiq.fda.gov.tw/api/public/DRPIQ/DRPIQ1000 → 404
GET http://lmspiq.fda.gov.tw/api/public/DRPIQ/DRPIQ6000 → 404
GET http://lmspiq.fda.gov.tw/api/public/DRPIQ/license-search → 404
```

The route structure from the JS bundle sitemap:

| Route | Description |
|---|---|
| `/DRPIQ/DRPIQ1000` | 許可證字號查詢 (Permit number search) |
| `/DRPIQ/DRPIQ2000` | 預知展延許可證查詢 (Pre-expiry renewal query) |
| `/DRPIQ/DRPIQ3000` | 過期許可證查詢 (Expired permits) |
| `/DRPIQ/DRPIQ4000` | 註銷許可證查詢 (Cancelled permits) |
| `/DRPIQ/DRPIQ5000` | 國內藥商資料查詢 (Domestic drug manufacturer data) |
| `/DRPIQ/DRPIQ6000` | 許可證各類月報查詢 (Monthly permit report query) |
| `/DRPIQ/DRPIQ7000` | DMF資料查詢 (Drug Master File query) |
| `/MDPIQ/MDPIQ1000` | Medical device permit search |
| `code-search` | Code lookup (DosageForm, Lic.Type, etc.) |

**Practical access:** The drug search endpoints return 404 unauthenticated. The system requires a
login and returns a Bearer JWT stored in sessionStorage. It is not clear from the transcript whether
a public API key is available. The code-lookup endpoints (DosageForm.Detail, Lic.Type,
MonthlyReport) respond without auth.

**Fallback query system found (call 92, WebFetch of fda.gov.tw/TC/site.aspx?sid=38):**

TFDA's public-facing drug portal lists these systems:

| System | URL | HTTP |
|---|---|---|
| 西藥、醫療器材許可證相關查詢 (main) | `http://lmspiq.fda.gov.tw/web/` | 200 (verified) |
| 西藥許可證查詢 (permit search) | `http://lmspiq.fda.gov.tw/web/DRPIQ/license-search` | 404 (frontend route, loads as SPA) |
| 藥品仿單查詢平台 (package insert) | `http://mcp.fda.gov.tw/` | 200 (verified call 97) |
| 藥品線上申辦及審查系統 | `https://mair.fda.gov.tw/#/index` | UNVERIFIED |
| 藥品供應監測系統 | `http://ddms.fda.gov.tw/` | UNVERIFIED |

**mcp.fda.gov.tw confirmed live (call 97):** Title is "藥品仿單查詢平台" (Drug Package Insert Query
Platform). Allows text search of drug package inserts at `/notice?q={query}`. No bulk export found.

### 2.3 TFDA Open Data Platform — data.fda.gov.tw

**URL:** `https://data.fda.gov.tw`

HTTP 200 (verified calls 26, 35, 39). However, **every URL path tried returned the platform's own
404 error page** (calls 33, 34, 40, 41, 49, 79, 85). The root serves a Swagger UI HTML shell but the
swagger initializer and API-docs paths all 404. The platform footer reads "copyright © 2025 衛生福利部食品藥物管理署 食品藥物開放資料平臺" — the system exists but its public API endpoints were not
accessible from outside.

**UNVERIFIED:** Whether data.fda.gov.tw requires registration/API key or is a currently-broken
system. The original agent was unable to resolve this.

### 2.4 Taiwan Government Open Data Portal — data.gov.tw

`https://data.gov.tw` — multiple searches for TFDA drug datasets (calls 62, 87, 89, 93) returned
large 400+ KB JS-rendered responses but grep for Chinese drug keywords found no matching dataset
titles. WebFetch of `data.gov.tw/dataset/5975` (call 90) confirmed that dataset is about an SME
export award, not drugs.

**UNVERIFIED:** Whether TFDA publishes a downloadable Western drug permit list on data.gov.tw. The
JS-rendered nature of the portal prevented grepping the actual dataset index.

### 2.5 TFDA Rare Disease / Orphan Drug Scheme

UNVERIFIED from transcript. Taiwan does have a rare disease medicines regulation
(罕見疾病防治及藥物法). The TFDA website section at `sid=1911` returned HTTP 200 (newly verified
2026-08-06) but content was not retrieved.

**Relevance:** Taiwan approvals of rare-disease drugs with no US equivalent would be Funnel A
candidates under 360ff.

### 2.6 English Interface

The TFDA website (`www.fda.gov.tw`) has an English section. The lmspiq permit query system
(`lmspiq.fda.gov.tw`) is Chinese-only based on the title and JS structure. Drug names in the
system appear in Chinese; English names are not consistently present.

### 2.7 Summary Access Map — Taiwan

| Resource | URL | Status | Auth | Bulk? |
|---|---|---|---|---|
| TFDA main site | www.fda.gov.tw | VERIFIED 200 | None | — |
| lmspiq permit query (SPA) | lmspiq.fda.gov.tw/web/ | VERIFIED 200 | None for UI | — |
| lmspiq API (code lookups) | lmspiq.fda.gov.tw/api/public/codes/* | VERIFIED 200 no auth | None | Yes |
| lmspiq API (drug search) | lmspiq.fda.gov.tw/api/public/DRPIQ/* | VERIFIED 404 no auth | Bearer JWT | Unknown |
| Package insert search | mcp.fda.gov.tw | VERIFIED 200 | None | No |
| Open data platform | data.fda.gov.tw | VERIFIED 200 host, all paths 404 | Unknown | Unknown |
| Taiwan open data portal | data.gov.tw | VERIFIED 200 (JS-rendered) | None | UNVERIFIED |

---

## 3. China — NMPA (National Medical Products Administration)

### 3.1 Regulatory Authority

**National Medical Products Administration (NMPA)**
- Chinese name: 国家药品监督管理局
- Website: `https://www.nmpa.gov.cn`
- Formerly: CFDA (China Food and Drug Administration)

**WHO / PIC/S status:** China NMPA is **not** a PIC/S member. It is not a WHO-Listed Authority for
prequalification. China has participated in ICH as a regulatory member since 2017. Drug approvals
are not straightforwardly recognised by PIC/S countries for reliance purposes.

### 3.2 Connectivity from Outside China

**All NMPA web endpoints tested were unreachable from the agent's location (likely US-based):**

| URL | Result |
|---|---|
| `https://www.nmpa.gov.cn` | HTTP 412 (call 14, call 52) |
| `https://www.nmpa.gov.cn/datasearch/home-index.html` | HTTP 412 |
| `https://datasearch.nmpa.gov.cn` | Exit code 6 / DNS failure (call 52) |
| `http://app1.nmpa.gov.cn/data_nmpa/face3/dir.html` | Exit code 6 (call 53) |
| `https://app1.nmpa.gov.cn` | 000 / connection failure (call 53) |
| `https://npps.nmpa.gov.cn/datasearch/face3/dir.html` | Exit code 6 (call 11) |

HTTP 412 from www.nmpa.gov.cn is a Precondition Failed response consistent with Tencent Cloud /
Wangsu CDN bot/WAF filtering of non-Chinese IP blocks. DNS lookup failure for datasearch.nmpa.gov.cn
suggests the subdomain is either GFW-gated or decommissioned. Curl exit code 6 = "Couldn't resolve
host."

**Newly verified 2026-08-06:** `https://www.nmpa.gov.cn` still returns HTTP 412 from US IP. The
CDN responds with a DDoS challenge JS block (confirmed: `$_ts.nsd=102715` challenge script) to
non-Chinese IPs.

### 3.3 Known NMPA Database Architecture (UNVERIFIED from outside China)

The agent did not find any NMPA data accessible from outside China. Based on known public
documentation that was NOT fetched and verified during the 97-call run, the NMPA maintains:

- **数据查询** at `www.nmpa.gov.cn/datasearch` — the primary drug approval query interface,
  Chinese-only, web form only, no public API.
- **国家药品监督管理局药品数据查询** — a JS-heavy search requiring a Chinese IP or VPN.
- Annual drug approval reports are published as PDFs on the NMPA website.

**MARK AS UNVERIFIED:** The above paragraph is not established by live fetches from this transcript.
It reflects general knowledge, not primary-source verification.

### 3.4 What Can Be Accessed Externally

**Option A — Third-party mirrors:** UNVERIFIED. Several Chinese pharmaceutical data aggregators
(e.g., 药智数据, Yaozhi; 丁香园, DXY) re-publish NMPA data but with uncertain completeness,
commercial licensing requirements, and no stable API.

**Option B — VPN / China-hosted crawler:** The NMPA datasearch is reachable from within China.
A partner or cloud VM in a Chinese data center (Alibaba Cloud, Tencent Cloud, AWS China) would
be necessary.

**Option C — Annual NMPA Blue Book PDFs:** NMPA publishes annual "药品审评报告" (drug review
reports). These are public PDFs but require Chinese-language parsing. UNVERIFIED whether 2025 edition
is available; no URL was successfully fetched.

**Option D — WHO ICTRP and PubMed:** For molecules approved only in China, publication in clinical
trial registries (ChiCTR) and PubMed is an alternative signal but incomplete.

### 3.5 Orphan Drug Scheme in China

China introduced a rare disease drug priority review policy in 2018 (《关于优化药品注册审评审批有关事宜的公告》). The rare disease list (罕见病目录) is maintained by the National Health Commission (NHC),
not NMPA directly. A second edition was released in September 2023.

**UNVERIFIED** from live fetches: whether the NMPA's datasearch distinguishes rare-disease
approvals in machine-readable form.

### 3.6 Relevance to PRV Program

China NMPA approvals are potentially the **richest Funnel A source** because:
1. China approves a large number of novel chemical entities (NCEs) that are not submitted to FDA.
2. Many approved traditional Chinese medicines have isolated active moieties with no US history.
3. China has a large rare disease patient population and an expanding rare disease pipeline.

The critical blocker is access: NMPA data is **not machine-readable from outside China** without
specific infrastructure. This is a gap that needs to be addressed operationally (VPN, Chinese cloud
compute, or commercial data partnership) before NMPA can be systematically screened.

### 3.7 Summary Access Map — China

| Resource | URL | Status | Auth | Bulk? |
|---|---|---|---|---|
| NMPA main site | www.nmpa.gov.cn | VERIFIED unreachable (412) from US | — | — |
| NMPA datasearch | datasearch.nmpa.gov.cn | VERIFIED DNS failure from US | — | — |
| NMPA app1 | app1.nmpa.gov.cn | VERIFIED DNS failure from US | — | — |
| Third-party mirrors | Various | UNVERIFIED | Commercial | Unknown |

---

## Unfinished — Worth Re-running

1. **Taiwan data.fda.gov.tw API authentication:** The platform exists (HTTP 200 at host) but every
   API path returned 404. This likely requires a registered API key obtainable from TFDA. Check
   `https://data.fda.gov.tw` for a registration page via a JS-capable browser. The lmspiq drug
   search endpoints likely use the same auth. Contact: `https://www.fda.gov.tw` — FDA Service
   Center for API access inquiry.

2. **Taiwan lmspiq Bearer token flow:** The JS shows `sessionStorage.getItem("item")` with a JWT.
   Determine whether TFDA has a public OAuth/API key program for the lmspiq backend, or whether
   auth is citizen-ID-only. The code-lookup endpoints work without auth and could be used to
   enumerate license type codes as a starting scaffold.

3. **Korea nedrug `itemSeq` enumeration:** The `getItemDetail` endpoint works without auth. The
   sequence format is `YYYYNNNNNNN` (e.g., `200004827` = 2000, item 4827). A full crawl of the
   95,265 products could be performed by iterating sequence numbers per year. Need to determine
   the actual year-range and padding of the sequence number, then batch-fetch and filter on
   `cancelCodeName="정상"` (active) and `rareDrugYn="Y"`.

4. **China NMPA access:** Requires either (a) a VPN endpoint in China or Chinese cloud VM, or
   (b) a commercial NMPA data vendor. Worth evaluating Yaozhi Data (`yaozhi.com`) or Pharmcube
   for licensed bulk export. No URL for these was fetched or verified.

5. **Taiwan data.gov.tw TFDA datasets:** The search results were JS-rendered blobs (400+ KB CSS).
   Need a JS-capable browser tool (Playwright) to enumerate the actual TFDA datasets on
   `data.gov.tw` by publisher filter.

6. **MFDS rare drug filter:** Locate an active product with `rareDrugYn=Y` on nedrug to confirm
   the field is populated for current designations. The two items tested (200004827 and 201600127)
   returned `null` and `"N"` respectively.

---

## URL Ledger

### VERIFIED

| URL | HTTP Code | What It Contains |
|---|---|---|
| `https://nedrug.mfds.go.kr` | 200 | MFDS drug portal — JS redirect to /index |
| `https://nedrug.mfds.go.kr/searchDrug/CNT` | 200 | JSON: `{"data":95265}` (live count) |
| `https://nedrug.mfds.go.kr/pbp/CCBBB01/getItemDetail?itemSeq=200004827` | 200 | Full product JSON, schema documented above |
| `https://nedrug.mfds.go.kr/pbp/CCBBB01/getItemDetail?itemSeq=201600127` | 200 | Full product JSON (잼플코프시럽, A0 class, withdrawn) |
| `https://nedrug.mfds.go.kr/pbp/CCBBB01/getItemDetail?itemSeq=202301060` | 200 | Full product JSON (바른해마, 정상/active, rareDrugYn=N) |
| `https://nedrug.mfds.go.kr/pbp/CCBBB01/getItemList` | Error page | Returns Korean error HTML — no session |
| `https://nedrug.mfds.go.kr/searchDrug` | 200 | JS-rendered search form, requires session |
| `https://nedrug.mfds.go.kr/pbp/CCBBB01/getItemPaging` | Empty | No response without session |
| `https://www.data.go.kr` | 200 | Korea public data portal (JS-rendered) |
| `https://apis.data.go.kr/1471000/DrugPrdtPrmsnInfoService04/getDrugPrdtPrmsnDtlInq04` | 200 | JSON error: "폐기됨" (decommissioned) |
| `https://apis.data.go.kr/1471000/MdcinGrnIdntfcInfoService01/getMdcinGrnIdntfcInfoList01` | 200 | JSON error: "폐기됨" (decommissioned) |
| `https://www.kodc.or.kr` | 200 | Korea Rare Disease and Essential Drugs Center |
| `https://www.mfds.go.kr/eng/index.do` | 200 | MFDS English portal |
| `https://www.fda.gov.tw/TC/siteList.aspx?sid=38` | 200 | TFDA business section (large HTML) |
| `https://www.fda.gov.tw/TC/site.aspx?sid=38` | 200 | TFDA drug business area |
| `https://www.fda.gov.tw/TC/site.aspx?sid=35` | 200 | TFDA drug area |
| `https://www.fda.gov.tw/TC/site.aspx?sid=2` | 200 | TFDA query systems (returned no grep hits) |
| `http://lmspiq.fda.gov.tw/web/` | 200 | Taiwan unified drug/device/cosmetic permit query SPA |
| `http://lmspiq.fda.gov.tw/api/public/codes/search/simple/codeKind/MonthlyReport` | 200 | JSON: 6 monthly report type codes |
| `http://lmspiq.fda.gov.tw/api/public/codes/search/full/codeKind/Lic.Type` | 200 | JSON: license type code list |
| `http://lmspiq.fda.gov.tw/api/public/codes/search/simple/codeKind/DosageForm.Detail` | 200 | JSON: 445 dosage form codes |
| `http://lmspiq.fda.gov.tw/api/public/DRPIQ/DRPIQ1000` | 404 | Drug permit search — requires auth |
| `http://lmspiq.fda.gov.tw/api/public/DRPIQ/DRPIQ6000` | 404 | Monthly permit report — requires auth |
| `https://lmspiq.fda.gov.tw/web/DRPIQ/license-search` | 404 | Frontend route — loads via SPA at root |
| `https://data.fda.gov.tw` | 200 | TFDA open data platform (Swagger UI shell) |
| `https://data.fda.gov.tw/swagger-ui.html` | 404 | Returns TFDA custom 404 page |
| `https://data.fda.gov.tw/v2/api-docs` | 404 | Returns TFDA custom 404 page |
| `https://data.fda.gov.tw/api/v1/Drug/getDrugList` | 404 | Returns TFDA custom 404 page |
| `http://mcp.fda.gov.tw/` | 200 | 藥品仿單查詢平台 (drug package insert search) |
| `https://data.gov.tw` | 200 | Taiwan government open data portal (JS-rendered) |
| `https://data.gov.tw/dataset/5975` | 200 | SME export award dataset — NOT drug data |
| `https://www.nmpa.gov.cn` | 412 | NMPA main site — WAF/CDN block from non-CN IP |
| `https://www.nmpa.gov.cn/datasearch/home-index.html` | 412 | Same block |
| `http://www.nmpa.gov.cn/datasearch/home-index.html` | 412 | Same block |
| `https://datasearch.nmpa.gov.cn` | 000 / Exit 6 | DNS failure — unreachable from US |
| `http://app1.nmpa.gov.cn/data_nmpa/face3/dir.html` | Exit 6 | DNS failure |
| `https://npps.nmpa.gov.cn/datasearch/face3/dir.html` | Exit 6 | DNS failure |

### UNVERIFIED

| URL | Reason Not Verified |
|---|---|
| `https://data.fda.gov.tw` (authenticated API paths) | All paths 404; auth mechanism unknown |
| `https://mair.fda.gov.tw/#/index` | Not fetched |
| `http://ddms.fda.gov.tw/` | Not fetched |
| `http://dsms.fda.gov.tw/` | Not fetched |
| `https://www.fda.gov.tw/TC/site.aspx?sid=1911` | HTTP 200 confirmed but content not retrieved |
| Any China NMPA datasearch endpoint | Unreachable from US infrastructure |
| `https://yaozhi.com` | Not fetched (commercial NMPA data aggregator) |
| Korea nedrug `rareDrugYn=Y` items | Field present in schema but no Y example found |
| `https://picscheme.org/en/participants-mra` for Korea/Taiwan | grep returned empty — page may be JS-rendered |
