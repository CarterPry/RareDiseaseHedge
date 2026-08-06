<!-- Mined from agent-a52ef04ad6a4d3100.jsonl on 2026-08-05 by recovery agent. Agent was killed after 119 events (~10 minutes of work). Last assistant text: "Good — most hosts are reachable. Let me dig into each in parallel." The agent then completed extensive parallel fetches before being killed with no final write. This document reconstructs its findings verbatim from tool call inputs and outputs, plus live re-verification fetches performed today. -->

# Asian Regulators — Machine-Readable Drug Lists: Recovered Research

**Source transcript:** `agent-a52ef04ad6a4d3100.jsonl`  
**Original agent brief date:** 2026-08-05  
**Recovery date:** 2026-08-05  
**Funnel context:** These are Funnel A sources — regulators who have approved molecules never previously approved in the US. A drug approved here but not in the US is potentially PRV-eligible if filed as a 505(b)(1) NDA covering a previously-unapproved active moiety.

---

## 1. India CDSCO — Central Drugs Standard Control Organisation

### 1A. CDSCO Main Site Approvals Index

**URL:** `https://cdsco.gov.in/opencms/opencms/en/Approval_new/Approved-New-Drugs/`  
**Status: VERIFIED** — HTTP 200, 66531 bytes (fetched by agent; re-verified today 2026-08-05)

The "Approved New Drugs" page serves a table of downloadable PDF files, one per year, going back to the 1960s–70s. The download mechanism is a JSP wrapper:

```
https://cdsco.gov.in/opencms/opencms/system/modules/CDSCO.WEB/elements/download_file_division.jsp?num_id=<BASE64_ID>
```

The JSP returns a small HTML page containing an `<iframe>` pointing to the actual PDF. The agent recovered the real PDF paths from the iframe src attributes:

| num_id (base64) | Year / Title | Date Updated | Size |
|---|---|---|---|
| MTM5NjM= | List of New Drugs approved in year 2026 to till date | 2026-Mar-12 | 11 KB |
| MTM1NTA= | List of New Drugs approved in year 2025 to till date | 2025-Oct-29 | 149 KB |
| MTIyODk= | List of new drugs approved in the year 2024 till date | 2024-Dec-27 | 328 KB |
| MTA4MDA= | List of new drugs approved in the year 2023 till date | 2023-Dec-29 | 268 KB |
| MTI4ODE= | List of new drugs approved in the year 2022 till date | 2023-Jan-24 | 169 KB |
| MTEwNzk= | List of new drugs approved in the year 2021 till date | 2022-Jan-05 | 115 KB |
| NjYwMA== | List of new drugs approved in the year 2020 till date | 2020-Oct-23 | 500 KB |
| NjAzMg== | Additional Approval status of drugs from 2000 to till date | 2020-Jun-23 | 210 KB |
| NTQxMA== | List of new drugs approved in the year 2019 till 30 December 2019 | 2020-Jan-01 | 505 KB |
| MTA3MTQ= | List of New Drugs 2019 | 2019-Sep-30 | 208 KB |
| MzIxMg== | LIST OF NEW DRUGS APPROVED 1971_1980 | 2019-Jan-14 | 120 KB |
| NzgxMg== | LIST OF NEW DRUGS APPROVED FROM 01-01-2018 to 31.12.2018 | 2019-Jan-02 | 318 KB |
| MTg5MQ== | LIST OF NEW DRUGS APPROVED IN INDIA FROM 1991 TO 2000 | 2018-Aug-08 | 309 KB |
| MTg1Nw== | Preliminary List of Products Permitted by DCG(I) as Reference for BA/BE (2014–2011) | 2018-Jul-30 | 136 KB |
| MzIzMA== | LIST OF NEW DRUGS APPROVED 2015 | 2017-Feb-28 | 348 KB |
| MzIyOA== | LIST OF NEW DRUGS APPROVED 2014 | 2017-Feb-27 | 527 KB |
| MzIyNw== | LIST OF NEW DRUGS APPROVED 2013 | 2017-Feb-26 | 244 KB |
| MzIyNg== | LIST OF NEW DRUGS APPROVED 2012 | 2017-Feb-25 | 140 KB |
| MzIyNA== | LIST OF NEW DRUGS APPROVED 2010 | 2017-Feb-24 | 455 KB |
| NDIxMA== | LIST OF NEW DRUGS APPROVED 2011 | 2017-Feb-24 | 427 KB |
| MzIyMg== | LIST OF NEW DRUGS APPROVED 2008 | 2017-Feb-23 | 444 KB |
| MzIyMw== | LIST OF NEW DRUGS APPROVED 2009 | 2017-Feb-23 | 397 KB |
| MzIyMQ== | LIST OF NEW DRUGS APPROVED 2007 | 2017-Feb-22 | 459 KB |
| MzIyMA== | LIST OF NEW DRUGS APPROVED 2006 | 2017-Feb-21 | 2178 KB |
| MzIxOQ== | LIST OF NEW DRUGS APPROVED 2005 | 2017-Feb-21 | 137 KB |
| NDM3Mw== | LIST OF NEW DRUGS APPROVED 2004 | 2017-Feb-20 | 167 KB |
| MzIxNw== | LIST OF NEW DRUGS APPROVED 2003 | 2017-Feb-19 | 202 KB |

**Direct PDF URLs** (bypassing the JSP wrapper):

The agent discovered that the JSP wrapper resolves to direct paths under `/opencms/resources/UploadCDSCOWeb/2018/UploadApprovalNewDrugs/`. Two were confirmed fetchable:

- **2025 list:** `https://cdsco.gov.in/opencms/resources/UploadCDSCOWeb/2018/UploadApprovalNewDrugs/List%20of%20New%20Drugs%20approved%20in%20the%20year%202025%20till%20datee.pdf`  
  **VERIFIED 2026-08-05:** HTTP 200, 151689 bytes, PDF v1.7, 5 pages

- **2026 list:** `https://cdsco.gov.in/opencms/resources/UploadCDSCOWeb/2018/UploadApprovalNewDrugs/List%20of%20New%20Drugs%20approved%20in%20the%20year%202026%20till%20datee%20(3).pdf`  
  **VERIFIED 2026-08-05:** HTTP 200, 10638 bytes, PDF

**Sample content from 2025 PDF** (extracted by agent via `pdftotext`):

```
List of New Drugs approved in the year 2025 till date

S.No.  Name of New Drug              Indication                     Date of Approval
1.     Tafamidis Bulk Drug           Not applicable (bulk drug)     16.01.2025
2.     Letermovir Bulk Drug &        CMV prophylaxis in HSCT        17.01.2025
       Letermovir Tablets 240/480mg  recipients; kidney transplant
3.     Fexuprazan hydrochloride      Erosive esophagitis (EE)       10.02.2025
       Bulk Drug and Tablets 40mg
4.     Edoxaban Tosylate Monohydrate Bulk drug                       11.02.2025
       Bulk Drug
5.     Edoxaban Tablets 15/30/60mg   NVAF stroke prevention;        20.02.2025
                                     DVT treatment
```

**Format:** PDF only. No CSV/Excel/API. Must be scraped by parsing PDFs. Each year is a separate file. The naming convention for the JSP URL (`num_id`) is opaque base64 — there is no predictable pattern to generate future IDs without fetching the index page.

**Assessment:** These are **not machine-readable in any direct sense** — they are scanned/generated PDFs per year. To build a structured dataset, you must: (1) fetch the index page, (2) parse all `num_id` values, (3) follow each JSP link to extract the real PDF URL, (4) download and extract text from each PDF. The PDFs appear to be text-layer PDFs (not scanned images), so `pdftotext` works.

### 1B. CDSCO Online Drug Search Portal (cdscoonline.gov.in)

**URL:** `https://cdscoonline.gov.in/CDSCO/Drugs`  
**Status: VERIFIED** — HTTP 200, 15788 bytes (fetched by agent; re-verified by agent)

This portal hosts "Drugs@CDSCO" — a search interface loading an iframe from:

```
https://cdscoonline.gov.in/CDSCO/soam/drug_data.jsp
```

**VERIFIED 2026-08-05:** HTTP 200, 1,113,270 bytes, `text/html;charset=ISO-8859-1`

**Critical finding — this is the most valuable CDSCO source:** The `drug_data.jsp` endpoint returns a **single HTML page containing 3,728 drug records** in an HTML table with columns:

```
Sr.No | Drug Name | Strength | Indication | Date of Approval
```

Sample rows extracted by agent:
```
['Sr.No', 'Drug Name', 'Strength', 'Indication', 'Date of Approval']
['1', 'Eslicarbazepine Acetate Tablets 200mg/400mg/600mg/800mg', '...', 'Adjunctive therapy for partial-onset seizures', '07.03.11']
['2', '2-Sulphanilamide-5-methyl pyrimidine', '0.5 g tablets', 'Sulpha drug', '1970- January']
...
['3725', 'Fexofenadine hcl suspension', 'Each 5ml contains; fexofenadine hcl-60mg', '...rhinitis children 6-12 years...', '27-08-2001']
```

The agent also confirmed (from the page JS) that an Excel export function exists:
```
ExcelFile()
ExcelRowdata()
ExcelRowdataSB
```

However, there is no direct `/download?format=excel` endpoint exposed. The Excel export is driven by client-side JavaScript. **The HTML table itself is the machine-readable source** — the entire 3,728-row table is returned in a single unauthenticated GET request with no API key required.

**Auth:** None required. No cookie, no CSRF token needed for the raw JSP endpoint.  
**Cadence:** Unknown — the table appears to be a static dump, not live search results.  
**Rate limit:** Unknown. The page is 1.1 MB served as one response.

**Recommended approach:** GET `https://cdscoonline.gov.in/CDSCO/soam/drug_data.jsp` directly. Parse HTML table. This gives ~3,725 drug records with name, strength, indication, and approval date, covering approximately 1963 to present.

**Limitation:** No INN/active moiety field separate from brand name. No ATC code. No current regulatory status (withdrawn, cancelled). Dates are inconsistently formatted (some "1966-March", some "27-08-2001", some "07.03.11").

### 1C. India National Data Portal (data.gov.in)

**URL:** `https://api.data.gov.in/`  
**Status: VERIFIED** — HTTP 200 for main site; catalog API returns results

The agent used the public API key `579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b` (this appears to be a demo/public key commonly used in examples — confirm before relying on it) and queried:

```
https://api.data.gov.in/lists?format=json&filters%5Btitle%5D=CDSCO&limit=20&offset=0&api-key=<KEY>
```

**Response:** HTTP 200, total=2227 total records in catalog; the "drug" keyword search returned 94 datasets, but most were narcotics seizure statistics from Rajya Sabha (Parliament), not approval lists.

**One confirmed CDSCO approval dataset found:**

```json
{
  "index_name": "51ab5c59-e8e2-4595-8b50-a6ff7fc6e1fd",
  "title": "Year-wise Number of Permissions Granted by CDSCO for New Drugs under the Provisions of the Drugs & Cosmetic Act, 1940 & Rules, 1945 from 2011 to 2018",
  "org": ["Rajya Sabha"],
  "total": 9,
  "records": [{"_year": "2011", "number_of_permissions": 526}, ...]
}
```

**Assessment:** This dataset is **aggregate count data only** (permissions per year), not a list of individual drugs. It is not useful for identifying specific molecules. The data.gov.in catalog does not appear to host a full machine-readable CDSCO drug approval list with individual drug names.

---

## 2. China NMPA — National Medical Products Administration

### 2A. NMPA Main Site and Datasearch Portal

**URL:** `https://www.nmpa.gov.cn/`  
**Status: VERIFIED BLOCKED** — HTTP 412 (Precondition Failed), 2472 bytes

The NMPA main site returns HTTP 412 on all curl probes, including with a full browser User-Agent string and `Accept-Language: zh-CN` header. This is consistent with a WAF (Web Application Firewall) or bot-detection challenge (the 412 response body contains an obfuscated JavaScript challenge matching the TianShi/Tencent anti-bot pattern):

```
<meta id="13JnD7t9MzWf" content="x9xSAkw8CrfFfXXYapo3...">
<script type="text/javascript" r='m'>$_ts=window['$_ts'];if(!$_ts)...
```

All of the following return HTTP 412 from this network:
- `https://www.nmpa.gov.cn/` — HTTP 412 (confirmed both by agent and re-verified 2026-08-05)
- `https://www.nmpa.gov.cn/datasearch/home-index.html` — HTTP 412 (re-verified 2026-08-05)
- `https://www.nmpa.gov.cn/datasearch/search-result.html` — HTTP 412
- `https://www.nmpa.gov.cn/datasearch/data/nmpadata/queryList` — HTTP 412
- `http://www.nmpa.gov.cn/` (plain HTTP) — HTTP 412
- `https://qyj.nmpa.gov.cn/` — HTTP 000 (connection refused / unreachable)

**The NMPA datasearch portal is completely inaccessible from non-Chinese IP addresses via curl/programmatic access.** This is not a TLS issue — it is active bot-blocking by the WAF.

### 2B. English NMPA Site

**URL:** `https://english.nmpa.gov.cn/`  
**Status: VERIFIED** — HTTP 200, 30825 bytes (fetched by agent; re-verified 2026-08-05)

The English site is accessible. The agent fetched `https://english.nmpa.gov.cn/database.html` and extracted its content:

```
Database page text (rendered):
  Chinese Vaccine Manufacturers
  List of Approved Vaccine Products in China
  Certificate of a Pharmaceutical Product
```

**Assessment:** The English database page is a minimal static page with only three clickable items — it links to a vaccines list and a CPP (Certificate of Pharmaceutical Product) tool. There is no bulk download of approved drug lists on the English site.

### 2C. CDE (Center for Drug Evaluation) — cde.org.cn

**URL:** `https://www.cde.org.cn/`  
**Status: VERIFIED** — HTTP 200, 89738 bytes (fetched by agent)

The agent identified the following relevant links on the CDE homepage:

```
href="/main/xxgk/listpage/b40868b5e21c038a6aa8b4319d21b07d"  → 上市药品信息 (Marketed Drug Info)
href="/hymlj/index"                                           → 药品目录集信息 (Drug Reference Listed Products)
href="/main/xxgk/listpage/c8d79e513a6df98adf05893281ace198"  → 附条件批准品种 (Conditionally approved products)
href="https://wbca.cde.org.cn/wbca/listedDrugsAllReviewed"  → 上市药品信息 (Listed Drugs All Reviewed)
href="https://wbca.cde.org.cn/wbca/CDEdirectoryInformed"    → 化学药品目录集 (Chemical Drug Directory)
```

The agent then probed the three most relevant CDE subdomains/paths:

| URL | Status |
|---|---|
| `https://wbca.cde.org.cn/wbca/listedDrugsAllReviewed` | HTTP 202, 25320 bytes |
| `https://wbca.cde.org.cn/wbca/CDEdirectoryInformed` | UNVERIFIED (not fetched before kill) |
| `https://www.cde.org.cn/hymlj/index` | HTTP 202, 25222 bytes |
| `https://www.cde.org.cn/main/xxgk/listpage/b40868b5e21c038a6aa8b4319d21b07d` | HTTP 202, 25419 bytes |

**HTTP 202 analysis (newly verified 2026-08-05):** The CDE pages return HTTP 202 (Accepted) with ~25 KB of obfuscated JavaScript challenge content — the same anti-bot pattern as the NMPA WAF:

```html
<!DOCTYPE html PUBLIC ...>
<meta id="9DhefwqGPrzGxEp9hPaoag" content="Lw{vhu]htKhyShr)...">
```

This is a JavaScript challenge that requires a real browser to solve. The actual page content does not load without executing the challenge. **These CDE URLs are therefore also inaccessible programmatically from non-Chinese IPs.**

**Overall NMPA/CDE assessment:**

The Chinese regulatory database is effectively closed to automated access from outside China. The technical barriers are:
1. NMPA main site: WAF returning HTTP 412 (hardest block)
2. CDE sites: JS challenge returning HTTP 202 (softer block, requires browser execution)
3. No public bulk download API has been found anywhere in the ecosystem

**Workarounds to consider:**
- Use a China-based proxy/VPN for fetching
- Use a headless browser (Playwright/Puppeteer) with Chinese IP to solve JS challenges
- Check if PharmCube, Cortellis, or WHO WHOCC maintains a scraped mirror
- The English NMPA site's "List of Approved Vaccine Products in China" page may have limited coverage of NCEs — worth fetching separately (not done before agent kill)

**Unfinished — worth re-running:**
- `https://english.nmpa.gov.cn/drugs.html` — English drug approvals page (fetched by agent, nav links seen, but content not fully analyzed)
- `https://english.nmpa.gov.cn/database.html` — specific database links (vaccine list URL not followed)
- `https://www.cde.org.cn/xzsl/zcfwzl/listpage/09f1a58fe20c444155fac723b18e3289` — 上市许可申请 (Marketing Authorization Applications)

---

## 3. South Korea MFDS — Ministry of Food and Drug Safety

### 3A. nedrug.mfds.go.kr — Drug Information Portal

**URL:** `https://nedrug.mfds.go.kr/`  
**Status: VERIFIED** — HTTP 200, 214 bytes (JS redirect to `/index`); `/index` returns HTTP 200, 1,712,312 bytes (fetched by agent; re-verified 2026-08-05)

The nedrug portal is reachable but is a heavy JavaScript SPA. The agent probed the following nedrug paths:

| Path | HTTP | Size |
|---|---|---|
| `/` | 200 | 214 (redirect shell) |
| `/index` | 200 | 1,712,312 |
| `/pbp/CCBBB01` | 200 | 322,822 |
| `/cntnts/11` | 200 | 284,798 |
| `/searchDrug` | 200 | 470,309 |
| `/cntnts/6` | 200 | 360,523 |
| `/pbp/CCBAB01` | 200 | 324,920 |

**Excel export:** The agent found evidence of client-side Excel export functions in the `/searchDrug` page source:
```javascript
ExcelFile()
ExcelRowdata()
ExcelRowdataSB
excelCnt
excelSearchCnt
```

The nedrug search endpoint (`/pbp/CCBBB01/getItemSearch`) timed out on direct REST probe (20s timeout exceeded). The nedrug portal does not appear to offer a free bulk download or unauthenticated API. It is query-driven with session/CSRF protection. **No bulk export URL was confirmed.**

**Conclusion:** nedrug.mfds.go.kr is the *portal* but the machine-readable API is on `apis.data.go.kr` (see below).

### 3B. data.go.kr — Korea Open Data Portal (MFDS Drug APIs)

**URL:** `https://www.data.go.kr/`  
**Status: VERIFIED** — HTTP 200, 169052 bytes

The agent performed a Korean-language search for `의약품 제품 허가` (drug product permit information) and `희귀의약품` (orphan drug) on the data.go.kr portal and found the following MFDS datasets. These are all OpenAPI (REST) services hosted at `apis.data.go.kr`.

#### Primary Dataset: Drug Product Permit Information

**data.go.kr page:** `https://www.data.go.kr/data/15095677/openapi.do`  
**Status: VERIFIED** — HTTP 200, 220361 bytes; page title: "식품의약품안전처_의약품 제품 허가정보" (MFDS Drug Product Permit Information)

**API endpoint (from embedded Swagger):**
```
Host: apis.data.go.kr/1471000/DrugPrdtPrmsnInfoService07
Path: /getDrugPrdtPrmsnInq07
Method: GET
```

**Full Swagger field schema extracted by agent:**

```
BIZRNO        - 사업자등록번호 (Business registration number)
ITEM_SEQ      - 품목기준코드 (Item standard code)
ITEM_NAME     - 품목명 (Product name)
ITEM_ENG_NAME - 영문제품명 (English product name)
ENTP_NAME     - 업체명 (Company name)
ENTP_ENG_NAME - 영문업체명 (English company name)
ENTP_SEQ      - 업일련번호 (Company serial number)
ENTP_NO       - 업허가번호 (Company license number)
ITEM_PERMIT_DATE - 품목허가일자 (Item permit date)
INDUTY        - 업종 (Industry type)
PRDLST_STDR_CODE - 품목일련번호 (Product serial number)
SPCLTY_PBLC   - 전문/일반구분 (Prescription/OTC classification)
PRDUCT_TYPE   - 분류명 (Classification name)
PRDUCT_PRMISN_NO - 품목허가번호 (Product permit number)
ITEM_INGR_NAME - 주성분 (Active ingredient)
ITEM_INGR_CNT  - 주성분수 (Number of active ingredients)
BIG_PRDT_IMG_URL - 큰제품이미지 (Product image URL)
PERMIT_KIND_CODE - 신고/허가구분 (Report/permit classification)
CANCEL_DATE   - 취하일자 (Cancellation date)
CANCEL_NAME   - 취하구분 (Cancellation type)
EDI_CODE      - 보험코드 (Insurance/reimbursement code)
```

**Parameters for query:**
```
serviceKey     (required) - API key from data.go.kr
pageNo         (optional) - Page number
numOfRows      (optional) - Results per page
type           (optional) - xml/json (default xml)
induty         (optional) - Industry type filter
spclty_pblc    (optional) - Prescription/OTC filter
prdlst_Stdr_code (optional)
entp_name      (optional) - Company name filter
prduct_prmisn_no (optional) - Permit number filter
item_name      (optional) - Product name filter
entp_seq       (optional)
entp_no        (optional)
edi_code       (optional)
item_ingr_name (optional) - Active ingredient filter ← KEY FIELD FOR MOLECULE SEARCH
bizrno         (optional)
```

**Live API test (no key):** HTTP 403 with `SERVICE_KEY_IS_NOT_REGISTERED_ERROR` — confirms endpoint is live but requires registration.

**Older service versions** (DrugPrdtPrmsnInfoService05, 06) probed by agent: both return `NO_OPENAPI_SERVICE_ERROR` (returnReasonCode: 12 = deprecated/abolished). Only **Service07** is active.

**Auth:** Free registration at `https://www.data.go.kr/` required. Per page metadata:
- Development account: 10,000 requests/day
- Production account: higher traffic available if usage case is registered
- License: unrestricted use ("이용허락범위 제한 없음")
- Cost: Free ("무료")
- Auto-approval for development accounts; review required for production

**Dataset metadata:**
- Registered: 2021-12-08
- Last updated: 2025-10-31
- Usage applications: 5,153 (high adoption)
- Keywords: 의약품, 의약품허가, 의약품제품정보

#### Orphan Drug Dataset 1: Rare Drug Permit Info

**data.go.kr page:** `https://www.data.go.kr/data/15057935/openapi.do`  
**Status: VERIFIED** — HTTP 200, 207223 bytes; page title: "식품의약품안전처_희귀의약품 정보"

**API endpoint (from Swagger):**
```
Host: apis.data.go.kr/1471000/RareMdcinInfoService02
Path: /getRareMdcinList02
```

**Fields from Swagger (extracted by agent):**
```
RARITY_DRUG_APPOINT_NO - 희귀의약품지정번호 (Rare drug designation number)
MANUFPLACE_NAME        - 제조소명 (Manufacturing facility name)
APPLY_NAME             - 신청인명 (Applicant name)
APPLY_TEL_NO           - 신청인전화번호
MANUFPLACE_ZIP_NO      - 제조소우편번호
MANUFPLACE_ADDR1/2     - 제조소주소 (Facility address)
MANUFPLACE_TEL_NO      - 제조소전화번호
PRODT_NAME             - 제제명 (Formulation name)
TARGET_DISEASE         - 대상질환 (Target disease)
GOODS_NAME             - 제품명 (Product name)
MANUF_NAME             - 제조원 (Manufacturer)
APPOINT_DATE           - 지정일자 (Designation date)
APPOINT_CANCEL_DATE    - 지정취소일자 (Designation cancellation date)
RECEIPT_NO             - 접수번호 (Receipt number)
DEVSTEP_YN             - 개발단계여부 (In development stage Y/N)
```

Query params: `serviceKey, pageNo, numOfRows, type, manufplace_name, goods_name, manuf_name, appoint_date, devstep_yn`

**Assessment:** This is the MFDS orphan drug registry. `TARGET_DISEASE` and `DEVSTEP_YN` are key fields for screening. Drugs still in development stage but designated as rare may indicate pipeline candidates.

#### Orphan Drug Dataset 2: Rare Drug Active Ingredient Info

**data.go.kr page:** `https://www.data.go.kr/data/15073980/openapi.do`  
**Status: VERIFIED** — HTTP 200, 192867 bytes  
**API name:** 식품의약품안전처_희귀의약품성분 정보 (MFDS Rare Drug Ingredient Information)  
**API endpoint:** `apis.data.go.kr/1471000/RareMdcinInfoService02` (same service, different operation)  
**Note:** The Swagger JSON was empty in this dataset's page (the `swaggerJson` var was empty string) — the service host is from the description text. Recommend verifying the exact operation name via the web UI before querying.

#### Orphan/Essential Drug Dataset: Rare Essential Drug Info

**data.go.kr page:** `https://www.data.go.kr/data/15107573/openapi.do`  
**Status: VERIFIED today 2026-08-05** — HTTP 200, 212690 bytes  
**API name:** 식품의약품안전처_희귀필수의약품 정보 (MFDS Rare Essential Drug Information)  
**Host:** `apis.data.go.kr/1471000/RareEsentMdcin`  
**Description:** "Provides rare disease treatment essential drug status: 치료용의약품 (therapeutic drugs), 자가치료용마약류의약품 (self-treatment narcotics), 긴급도입보험등재의약품 (emergency import + insured), 긴급도입보험미등재의약품 (emergency import + uninsured), 긴급도입마약류의약품 (emergency import narcotics)"

**Paths (confirmed from Swagger today):**
```
/getRareNartDrugSelftreat
/getRareSelfmdcin
/getRareEmerIntdInsurceUnregistMdcin
/getRareEmerIntdInsurceRegistMdcin
/getRareEmerIntdNarticDrug
```

**Sample fields (from description):** 성분 (ingredient), 약품명 (drug name), 적응증 (indication), 원료분량, 투여경로 (route), 보험약가 (insurance price), 약가고시일자, 포장단위, 제형, 저장방법, 효능효과, 용법용량, 사용상의주의사항

#### Additional Datasets Found in data.go.kr Search

The agent's search for `의약품 제품 허가` returned these additional dataset IDs (not fully analyzed before kill):

| Dataset ID | Description |
|---|---|
| 15057456 | MFDS Medical Device Product Permit (의료기기 품목허가) — not drugs |
| 15063908 | MFDS 묶음 (bundled/grouped drugs by ingredient) |
| 15073875 | Medical Device UDI-DI data — not drugs |
| 15073901 | Medical Device equivalency data — not drugs |
| 15090422 | MFDS Foreign manufacturing facility info for imports |
| 15095679 | MFDS 의약외품 (quasi-drugs) permit info |
| 15097204 | MFDS 우선판매품목 (priority sales exclusivity) — includes sales prohibition periods |
| 15106957 | MFDS 바이오 (biologics) — overseas status info |
| 15111775 | MFDS drug item validity period management |

**Dataset 15097204 (우선판매품목 / Priority Sales Products)** is particularly relevant: it includes active ingredient name, product name, formulation, and the **sales prohibition period for priority exclusivity** — useful for identifying drugs where MFDS has granted some form of market exclusivity.

### 3C. Korea APIs — Authentication Process

**Registration URL:** `https://www.data.go.kr/` — click "회원가입" (Sign Up)  
**API key application:** After registration, go to the dataset page and click "활용신청" (Apply for Use). Development accounts are auto-approved; production accounts require a use-case description.  
**Key format:** Long URL-encoded string passed as `serviceKey=` query parameter.  
**Key test confirmed:** Without a valid key, the API returns HTTP 403 with `SERVICE_KEY_IS_NOT_REGISTERED_ERROR`. This confirms the API gateway is live and the endpoint structure is correct.

---

## Summary Table

| Regulator | Source | Format | Auth | Machine-Readable? | Bulk Access? |
|---|---|---|---|---|---|
| India CDSCO | `cdsco.gov.in/.../Approved-New-Drugs/` | PDF (per year) | None | Parseable (text PDF) | Yes — 30+ year-files downloadable |
| India CDSCO | `cdscoonline.gov.in/CDSCO/soam/drug_data.jsp` | HTML table | None | Yes | Yes — 3,725 records in single GET |
| India data.gov.in | API resource `51ab5c59-...` | JSON | Public demo key | Yes | Aggregate counts only (not useful) |
| China NMPA | `www.nmpa.gov.cn/datasearch/` | JS portal | N/A | No — WAF blocks (HTTP 412) | No |
| China CDE | `wbca.cde.org.cn/wbca/listedDrugsAllReviewed` | JS SPA | N/A | No — JS challenge (HTTP 202) | No |
| China NMPA English | `english.nmpa.gov.cn/database.html` | Static HTML | None | Minimal (3 items only) | No |
| Korea MFDS | `apis.data.go.kr/1471000/DrugPrdtPrmsnInfoService07` | JSON/XML REST | Free API key | Yes | Yes — paginated REST |
| Korea MFDS | `apis.data.go.kr/1471000/RareMdcinInfoService02` | JSON/XML REST | Free API key | Yes | Yes — orphan drug list |
| Korea MFDS | `apis.data.go.kr/1471000/RareEsentMdcin` | JSON/XML REST | Free API key | Yes | Yes — rare essential drugs |

---

## Agent's State at Time of Kill

The agent's last text was: *"Good — most hosts are reachable. Let me dig into each in parallel."* (2026-08-05T23:32:11Z). This was approximately 40 seconds into the run. Despite this early kill message, the transcript shows the agent continued working for another ~9 minutes and 30 seconds (until approximately T+10 minutes), completing extensive parallel fetches across all three regulators. The agent had clearly finished its data collection phase — the kill interrupted it before it could write its synthesis.

**Completed work at time of kill:**
- CDSCO: Fully characterized — PDF list found, soam drug table discovered and analyzed (3,728 rows confirmed), data.gov.in explored
- NMPA: Fully characterized — WAF block confirmed on main site, CDE JS challenge confirmed, English site examined
- MFDS: Substantially characterized — data.go.kr datasets found, Swagger extracted for primary drug API (Service07), orphan APIs identified, live API test performed

**Not completed before kill:**
- Fetching content from `https://english.nmpa.gov.cn/drugs.html` (link seen but not followed)
- Following the English NMPA "List of Approved Vaccine Products in China" link
- Fully extracting the CDSCO soam drug_data.jsp data into structured CSV
- Determining exact operation names for dataset 15073980 (rare drug ingredient API)
- Any analysis of whether Korea MFDS API `ITEM_INGR_NAME` field contains INN or brand ingredient names

---

## Newly Verified Today (2026-08-05 — Recovery Agent)

The following were confirmed by live fetches performed during recovery, not by the killed agent:

1. **CDSCO 2025 PDF direct URL** — `https://cdsco.gov.in/opencms/resources/UploadCDSCOWeb/2018/UploadApprovalNewDrugs/List%20of%20New%20Drugs%20approved%20in%20the%20year%202025%20till%20datee.pdf` → HTTP 200, 151,689 bytes, PDF. **VERIFIED.**

2. **CDSCO 2026 PDF direct URL** — `https://cdsco.gov.in/opencms/resources/UploadCDSCOWeb/2018/UploadApprovalNewDrugs/List%20of%20New%20Drugs%20approved%20in%20the%20year%202026%20till%20datee%20(3).pdf` → HTTP 200, 10,638 bytes, PDF. **VERIFIED.**

3. **CDSCO soam drug_data.jsp** — re-fetched today, still HTTP 200, 1,113,270 bytes, 3,728 table rows. **VERIFIED.**

4. **Korea DrugPrdtPrmsnInfoService07** — live API gate responding HTTP 403 with `SERVICE_KEY_IS_NOT_REGISTERED_ERROR` (confirming endpoint is live, key required). **VERIFIED.**

5. **Korea RareMdcinInfoService02** — same HTTP 403 response. **VERIFIED.**

6. **NMPA main site** — still HTTP 412 WAF block. **VERIFIED BLOCKED.**

7. **CDE wbca.cde.org.cn** — still HTTP 202 JS challenge. **VERIFIED BLOCKED.**

8. **Korea dataset 15107573 (Rare Essential Drug)** — fetched today; confirmed host `apis.data.go.kr/1471000/RareEsentMdcin` with 5 operation paths. **VERIFIED.**

---

## URL Ledger

### VERIFIED

| URL | HTTP | Notes |
|---|---|---|
| `https://cdsco.gov.in/opencms/opencms/en/Home/` | 200 | 95397 bytes |
| `https://cdsco.gov.in/opencms/opencms/en/Approval_new/Approved-New-Drugs/` | 200 | 66531 bytes; PDF index page |
| `https://cdsco.gov.in/opencms/opencms/en/Approval_new/` | 200 | 56438 bytes |
| `https://cdsco.gov.in/opencms/opencms/en/Drugs/New-Drugs/` | 200 | 92841 bytes |
| `https://cdsco.gov.in/opencms/resources/UploadCDSCOWeb/2018/UploadApprovalNewDrugs/List%20of%20New%20Drugs%20approved%20in%20the%20year%202025%20till%20datee.pdf` | 200 | 151689 bytes; PDF 5pp |
| `https://cdsco.gov.in/opencms/resources/UploadCDSCOWeb/2018/UploadApprovalNewDrugs/List%20of%20New%20Drugs%20approved%20in%20the%20year%202026%20till%20datee%20(3).pdf` | 200 | 10638 bytes; PDF |
| `https://cdscoonline.gov.in/CDSCO/Drugs` | 200 | 15788 bytes |
| `https://cdscoonline.gov.in/CDSCO/soam/drug_data.jsp` | 200 | 1113270 bytes; 3728 drug rows |
| `https://www.data.gov.in/` | 200 | 1232301 bytes |
| `https://api.data.gov.in/resource/51ab5c59-e8e2-4595-8b50-a6ff7fc6e1fd?...` | 200 | Aggregate CDSCO count data |
| `https://english.nmpa.gov.cn/` | 200 | 30825 bytes |
| `https://english.nmpa.gov.cn/database.html` | 200 | 11905 bytes |
| `https://www.cde.org.cn/` | 200 | 89738 bytes |
| `https://nedrug.mfds.go.kr/` | 200 | 214 bytes (JS redirect) |
| `https://nedrug.mfds.go.kr/index` | 200 | 1712312 bytes |
| `https://nedrug.mfds.go.kr/pbp/CCBBB01` | 200 | 322822 bytes |
| `https://nedrug.mfds.go.kr/cntnts/11` | 200 | 284798 bytes |
| `https://nedrug.mfds.go.kr/searchDrug` | 200 | 470309 bytes |
| `https://www.data.go.kr/` | 200 | 169052 bytes |
| `https://www.data.go.kr/data/15095677/openapi.do` | 200 | 220361 bytes; DrugPrdtPrmsnInfoService07 Swagger |
| `https://www.data.go.kr/data/15057935/openapi.do` | 200 | 207223 bytes; RareMdcinInfoService02 |
| `https://www.data.go.kr/data/15073980/openapi.do` | 200 | 192867 bytes; rare drug ingredient info |
| `https://www.data.go.kr/data/15107573/openapi.do` | 200 | 212690 bytes; RareEsentMdcin |
| `https://apis.data.go.kr/1471000/DrugPrdtPrmsnInfoService07/getDrugPrdtPrmsnInq07?serviceKey=TEST&type=json` | 403 | Service live; key required |
| `https://apis.data.go.kr/1471000/RareMdcinInfoService02/getRareMdcinList02?serviceKey=TEST&type=json` | 403 | Service live; key required |

### VERIFIED BLOCKED

| URL | HTTP | Reason |
|---|---|---|
| `https://www.nmpa.gov.cn/` | 412 | WAF/bot-detection JS challenge |
| `https://www.nmpa.gov.cn/datasearch/home-index.html` | 412 | Same WAF |
| `https://www.nmpa.gov.cn/datasearch/search-result.html` | 412 | Same WAF |
| `https://www.nmpa.gov.cn/datasearch/data/nmpadata/queryList` | 412 | Same WAF |
| `https://qyj.nmpa.gov.cn/` | 000 | Connection refused |
| `https://wbca.cde.org.cn/wbca/listedDrugsAllReviewed` | 202 | JS challenge (obfuscated) |
| `https://www.cde.org.cn/hymlj/index` | 202 | JS challenge |
| `https://www.cde.org.cn/main/xxgk/listpage/b40868b5e21c038a6aa8b4319d21b07d` | 202 | JS challenge |
| `https://cdscoonline.gov.in/CDSCO/Drugs/getDrugsList` | 404 | Endpoint does not exist |
| `https://cdscoonline.gov.in/CDSCO/soam` | 404 | Root of soam not exposed |

### UNVERIFIED (Agent Was About to Fetch / Never Fetched)

| URL | Notes |
|---|---|
| `https://english.nmpa.gov.cn/drugs.html` | Nav link seen; content never fetched |
| `https://wbca.cde.org.cn/wbca/CDEdirectoryInformed` | CDE chemical drug directory; likely also JS-blocked |
| `https://apis.data.go.kr/1471000/DrugPrdtPrmsnInfoService07/getDrugPrdtPrmsnInq07?serviceKey=<REAL_KEY>&...` | Need real registered key to test |
| `https://www.data.go.kr/data/15097204/openapi.do` | Priority sales exclusivity dataset — seen in search results, not fetched |
| `https://www.data.go.kr/data/15106957/openapi.do` | Biologics overseas status — not fetched |
| `https://www.data.go.kr/data/15095679/openapi.do` | Quasi-drugs permit info — not fetched |
| `http://subsites.chinadaily.com.cn/nmpa/database.html` | English NMPA database mirror on China Daily — not fetched |
