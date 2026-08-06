<!-- RECOVERED from subagent transcript agent-a2ca18d1647ee5a9d.jsonl, session fd64561f-7c90-41a2-95cf-b4a133a8fe0f, research date 2026-08-05.
     Reference-regulator agent, UK MHRA.
     Verbatim agent deliverable — not re-edited. -->

# UK MHRA Machine-Accessible Drug Approval Data — Research Findings
*Research date: 2026-08-05. Every URL below marked VERIFIED was actually fetched in this session.*

---

## 1. products.mhra.gov.uk — the MHRA Products website

### 1.1 What it is
- **VERIFIED** `https://products.mhra.gov.uk/` — HTTP 200, `text/html`, 124,886 bytes.
- **Next.js static export** (`__NEXT_DATA__` present, `buildId: ufPgk6V6gc0hHc9abqxts`, `"nextExport": true, "autoExport": true`). **`pageProps` is `{}` on every route** — there is **zero server-side data**. 100% JS-rendered client side.
- Routes (from **VERIFIED** `https://products.mhra.gov.uk/_next/static/ufPgk6V6gc0hHc9abqxts/_buildManifest.js`): `/`, `/about`, `/search`, `/product`, `/substance`, `/substance-index`, `/medicine-levels-in-pregnancy`, `/medicine-levels-in-pregnancy/{search,substance,substance-index,reports/[report]}`.

### 1.2 URL patterns (all VERIFIED HTTP 200, but all return the same empty SPA shell)
- `https://products.mhra.gov.uk/search?search=sirolimus` → **200, 122,696 bytes, `query: {}`, `pageProps: {}`**. The query string is read client-side only. **Scraping this HTML returns nothing useful.**
- `https://products.mhra.gov.uk/product/?product=RAPAMUNE` → 200, 122,701 bytes (empty shell)
- `https://products.mhra.gov.uk/substance/?substance=SIROLIMUS` → 200, 121,259 bytes (empty shell)
- `https://products.mhra.gov.uk/substance-index/?letter=S` → 200, 120,746 bytes (empty shell)
- **VERIFIED** `https://products.mhra.gov.uk/robots.txt` → 200. Content is literally `User-agent: *` + `Sitemap: https://products.mhra.gov.uk/sitemap.xml`. **No Disallow directives.**
- **VERIFIED** `https://products.mhra.gov.uk/sitemap.xml` → 200, but contains **only the ~9 static route pages**, no product URLs. Useless for enumeration.

### 1.3 **THE ACTUAL API — undocumented public Azure Cognitive Search index**
There is no official MHRA API, **but the site's own frontend queries a public Azure Search service with a read-only query key hard-coded in shipped JavaScript.**

Source: **VERIFIED** `https://products.mhra.gov.uk/_next/static/chunks/843-012836701345ef2e.js` (fetched, 200) contains:
```js
new URL("https://mhraproducts4853.search.windows.net/indexes/" + index + "/docs")
r.searchParams.append("api-key","17CCFC430C1A78A169B392A35A99C49D")
r.searchParams.append("api-version","2017-11-11")
```

**VERIFIED live endpoint** (fetched, HTTP 200, real JSON results):
```
https://mhraproducts4853.search.windows.net/indexes/products-index/docs
  ?api-key=17CCFC430C1A78A169B392A35A99C49D
  &api-version=2017-11-11
  &search=sirolimus&$top=50&$count=true&queryType=full&searchMode=all
```

- **Auth:** the `api-key` is a **read-only query key publicly shipped to every browser**. No registration, no account. It is *not* documented or supported — MHRA can rotate it without notice. Re-scrape the JS chunk to self-heal.
- **Data format:** Azure Search OData JSON.
- **Index size (VERIFIED via `$count=true`, 2026-08-05):**

| doc_type | count |
|---|---|
| `Pil` (patient info leaflets) | **42,835** |
| `Spc` (summaries of product characteristics) | **24,582** |
| `Par` (public assessment reports) | **11,557** |
| **TOTAL** | **78,974** |

- **Territory counts (VERIFIED):** `UK` 63,650 · `GB` 8,607 · `NI` **48** · null 6,669.
- **Document schema (VERIFIED from live response):**
  `product_name`, `substance_name` (Collection), `pl_number` (Collection), `doc_type` (`Par`|`Pil`|`Spc`), `title`, `file_name`, `created` (ISO ts), `territory` (`UK`|`GB`|`NI`|null), `release_state`, `rev_label`, `keywords`, `facets`, `suggestions`, `metadata_storage_path` (blob URL to PDF), `metadata_storage_size`, `metadata_storage_name` (SHA-1-looking hash).

- **Capabilities tested (all VERIFIED):**
  - `$filter=doc_type eq 'Par'` ✅
  - `$filter=substance_name/any(s: s eq 'SIROLIMUS')` ✅ (14 docs)
  - `$filter=pl_number/any(p: p eq 'PL518080045')` ✅
  - `$filter=territory eq 'GB'` / `eq null` ✅
  - `$orderby=created desc` ✅ ← **this is your new-approvals feed**
  - `facet=doc_type` ✅ (returns exact counts)
  - `$top=1000` ✅ (Azure max page size), `$skip=78000` ✅, `$skip=100000` → 0 results (Azure hard cap 100k)
  - `POST /indexes/products-index/docs/search?api-version=2017-11-11` with `api-key` header ✅ 200
  - Newer API versions **also work**: `2020-06-30`, `2023-11-01`, `2024-07-01` all → 200 (use these for `search.score`/semantic features)
  - **`$filter` on `created` FAILS** — "`'created' is not a filterable field`" (and it's typed `Edm.String`, not `Edm.DateTimeOffset`). **Incremental sync must use `$orderby=created desc` + `$top=1000` and stop at your watermark.**
  - `/docs/suggest?suggesterName=sg` → **HTTP 400** (no suggester configured under that name)
  - `GET /indexes/products-index?api-version=...` → **HTTP 403** (query key can't read index definition)
  - `GET /indexes?api-version=...` → **HTTP 403**

- **Full enumeration is feasible:** 78,974 docs ÷ 1,000/page = **79 requests**. Under the 100k `$skip` ceiling. This is your de-facto bulk download.

- **Second index (VERIFIED):** `bmgf-index` — `https://mhraproducts4853.search.windows.net/indexes/bmgf-index/docs?...&search=*` → 200, **only 6 documents, and they are test data** (`"products":["PRODUCT TEST"], "pl_numbers":["PL 21111/0000"], "summary":"A New One"`). This backs "Medicine levels in pregnancy" (PBPK reports). Effectively empty — ignore.

### 1.4 PDF retrieval (bulk-ish)
- **VERIFIED** blob fetch: `https://mhraproducts4853.blob.core.windows.net/docs/21a92dd6603203b8f1b2caf5d897a6f4507e7800` → **HTTP 200, `application/pdf`, 882,108 bytes**. No auth, no referer check.
- Every search hit's `metadata_storage_path` is a directly downloadable PDF.
- **VERIFIED**: container listing is blocked — `https://mhraproducts4853.blob.core.windows.net/docs?restype=container&comp=list` → **HTTP 404**. You cannot enumerate blobs directly; you must go through the search index to get the hashes.

### 1.5 Dead endpoint
- **UNVERIFIED (fetch blocked — endpoint returns HTTP 503 on both GET and POST, including a trivial `{__typename}` query)**: `https://medicines.api.mhra.gov.uk/graphql`. This GraphQL URL is still referenced in shipped JS chunk `s_843`/`1957` module (`var i="https://medicines.api.mhra.gov.uk/graphql"`), but **the service is down/decommissioned**. Do not build on it.

---

## 2. Public Assessment Reports (UKPARs)

- **What you get:** the MHRA's scientific assessment (quality/non-clinical/clinical), the rationale for approval, and post-approval variation annexes. For repurposing work this is the closest UK analogue to an FDA review package or an EPAR.
- **Where they live:** inside the same Azure index. `$filter=doc_type eq 'Par'` → **11,557 PDFs**, each at a `mhraproducts4853.blob.core.windows.net/docs/<sha>` URL.
- **Format:** PDF only. No XML, no structured extract. Text-layer quality varies; older ones are scans.
- **Coverage (VERIFIED from `https://products.mhra.gov.uk/about`, HTTP 200):**
  - PARs exist for **new marketing authorisations granted after 30 October 2005**.
  - PARs are **also published for all MAAs that were REFUSED after 1 April 2019** — a rarely-used signal source for a repurposing shop (what MHRA rejected and why).
  - Non-safety variations of clinical significance are appended as **annexes at the end of each PAR**; minor variations (pack sizes, literature tweaks) are not.
  - Separate "Safety Public Assessment Reports" exist at **VERIFIED-by-reference** `https://www.gov.uk/guidance/safety-public-assessment-reports` (URL extracted from shipped JS; not independently fetched → treat as UNVERIFIED).
  - For EMA-centrally-authorised products, the assessment is an **EPAR at ema.europa.eu**, not a UKPAR.
- **Naming conventions — inconsistent, do NOT parse filenames as your primary key.** VERIFIED real examples:

| `title` (normalized, reliable) | `file_name` (raw, chaotic) |
|---|---|
| `PROGIT 50 MG FILM-COATED TABLETS - PL 37039/0005` | `FIN APPROVED_PUB_Progit 50 mg film-coated tablets (PL 37039_0005).pdf` |
| `CINACALCET 60 MG FILM-COATED TABLETS - PLGB 48259/0075` | `CINACALCET 30, 60 & 90 MG FILM-COATED TABLETS PLGB 48259_0074-5.pdf` |
| `WEZENLA 45 MG SOLUTION FOR INJECTION...` | `PAR WEZENLA 45mg solution... (PLGB 13832_0079-82) - final v2.pdf` |
| `BACLOFEN 2 MG/ML SOLUTION FOR INFUSION - PL 00142/1318` | `BACLOFEN 0.5 2 & 50 MG_ML SOLUTION FOR INFUSION (PL 00142_1316-18).pdf` |

  - **PAR `title` is reliably `<PRODUCT NAME> - <PL NUMBER>`.** Parse `title`, not `file_name`.
  - **One PAR PDF frequently covers a PL *range*** (`PL 00142_1316-18`, `PLGB 13832_0079-82`) but is indexed once per PL number → expect duplicate blob hashes across PL numbers. Dedupe on `metadata_storage_name`.
  - **SPC/PIL naming IS regular:** `spc-doc_PL 51718-0013.pdf`, `leaflet MAH BRAND_PL 51808-0045.pdf`, `leaflet MAH GENERIC_PLGB 00057-1613.pdf`. Note `/` in the PL becomes `-` in the filename, and the `pl_number` index field is the *unpunctuated* form (`PL517180013`).
- **Programmatic recipe:**
  ```
  GET .../products-index/docs?api-key=...&api-version=2024-07-01
      &search=*&$filter=doc_type eq 'Par'&$orderby=created desc&$top=1000&$skip=N
      &$select=title,pl_number,product_name,substance_name,created,metadata_storage_path
  ```
  then GET each `metadata_storage_path`.
- **Landing/guidance page:** **VERIFIED** `https://www.gov.uk/guidance/find-product-information-about-medicines` (HTTP 200, last updated 2026-07-10). ⚠️ **UNVERIFIED (404)** — `https://www.gov.uk/guidance/public-assessment-reports-for-medicines` does **not** exist; don't cite it.

---

## 3. The "MHRA approvals" list — **there is no official approvals register**

Plainly: **MHRA publishes no list, CSV, ODS, Excel or API of newly authorised products.** Verified negatives:

- **VERIFIED** `https://www.gov.uk/government/organisations/medicines-and-healthcare-products-regulatory-agency` → 200. Org type: `executive_agency`. Content API (**VERIFIED** `https://www.gov.uk/api/content/government/organisations/medicines-and-healthcare-products-regulatory-agency`, 200) contains no dataset links.
- **UNVERIFIED (404)** `https://www.gov.uk/government/organisations/medicines-and-healthcare-products-regulatory-agency/about/statistics` — that path does not exist.
- **VERIFIED** gov.uk Search API with `filter_content_store_document_type=statistics` + MHRA org → **`total: 0`. MHRA publishes zero official statistics releases.**
- **VERIFIED** `filter_content_store_document_type=transparency` + MHRA → 96 results, but they are **all spend/GPC/FOI/privacy** files. The only substantive one is MHRA Performance Data.
- **VERIFIED** `https://ckan.publishing.service.gov.uk/api/3/action/package_search?q=MHRA&rows=20` → 200, **`count: 8`**, and all 8 are: GPC transactions, recruitment exceptions, organogram, spend over £25k, adverse-incident reporting, SABRE, Yellow Card, COVID vaccine rollout. **No product/authorisation dataset on data.gov.uk.**

### What you can use instead

**(a) The Azure index as a de-facto approvals feed — best option.**
`$orderby=created desc` + `$filter=doc_type eq 'Par'` gives newest published PARs. VERIFIED live sample (fetched 2026-08-05):
```
REMSIMA 40 MG/ML ... - PL 51808/0045   created 2026-08-05T09:31:50Z  (infliximab)
NORTRIPTYLINE 25 MG FILM-COATED TABLETS - PL 20395/0438  created 2026-08-04T12:30:18Z
```
**Cadence: same-day.** The index was serving documents created hours before the fetch. This is the highest-frequency UK approval signal that exists.
⚠️ Gotcha: `created` = *document publication* timestamp, **not** the MA grant date. Re-published/re-versioned SPCs get new `created` values (`rev_label` field tracks revision). You will get churn, not just new approvals. Filter to `doc_type eq 'Par'` + `rev_label` = 1 to approximate genuinely new authorisations.

**(b) gov.uk Search API — structured JSON, free, no key. VERIFIED.**
```
https://www.gov.uk/api/search.json
  ?filter_organisations=medicines-and-healthcare-products-regulatory-agency
  &filter_content_store_document_type=press_release
  &order=-public_timestamp&count=100
  &fields=title,link,public_timestamp,content_store_document_type
```
VERIFIED: `total: 584` MHRA press releases. Every notable approval is announced as `MHRA approves <drug> (<Brand>) for <indication>` — VERIFIED live examples: *donidalorsen (Dawnzera) for hereditary angioedema* (2026-05-07), *olezarsen (Tryngolza) for familial chylomicronemia syndrome* (2026-04-10), *first medicine for rare immune disease APDS* (2024-09-27). **This is the only human-curated "new approvals" stream, and it is heavily skewed to rare/notable drugs — which suits your use case.** Not exhaustive: generics and most line extensions are never announced.

**(c) gov.uk Atom feed. VERIFIED:**
`https://www.gov.uk/search/news-and-communications.atom?organisations%5B%5D=medicines-and-healthcare-products-regulatory-agency` → HTTP 200, `application/atom+xml`, 14,397 bytes, `<updated>2026-08-04T09:56:29+01:00</updated>`.

**(d) gov.uk Content API for any page:** `https://www.gov.uk/api/content/<path>` → full JSON incl. `details.body` HTML, `details.attachments[]` (with `content_type`, `file_size`, asset URLs), and `details.change_history[]`. **VERIFIED repeatedly.** No auth. This is how you diff guidance changes programmatically.

**(e) MHRA Performance Data — VERIFIED** `https://www.gov.uk/government/publications/mhra-performance-data` and `.../mhra-performance-data/mhra-performance-data` (both 200; last updated 2026-07-30 with June 2026 data; **monthly**). **HTML tables only — no CSV/ODS/Excel attachment.** Gives KPI *percentages*, not counts. Relevant rows: National route **100% determined within 210 days**; **IRP Route A 98% within 60 days; IRP Route B 98% within 110 days**; national variations 98% within statutory timelines; scientific advice 95% meeting dates within 10 working days, 94% written advice within 30 working days. No application volumes.

---

## 4. International Recognition Procedure (IRP) — **TOP PRIORITY, full rules**

**Canonical URL — VERIFIED (HTTP 200 via both WebFetch and `https://www.gov.uk/api/content/government/publications/international-recognition-procedure/international-recognition-procedure`, 80,047 bytes JSON):**
`https://www.gov.uk/government/publications/international-recognition-procedure/international-recognition-procedure`
- `first_published_at: 2023-08-30` · `public_updated_at: 2026-07-14` · `updated_at: 2026-07-31`
- ⚠️ **UNVERIFIED (404)** — `https://www.gov.uk/guidance/international-recognition-procedure` does not exist. Common wrong citation.

### 4.1 Start date & what it replaced
- **"The International Recognition Procedure (IRP) was introduced on 1 January 2024."** It replaced the EC Decision Reliance Procedure (ECDRP) and complements the National Pathway.

### 4.2 ⚠️ **MAJOR RULE CHANGE — 13 July 2026 (verbatim from the page)**
> "Procedure developments will be introduced ... from 13 July 2026. Key updates include: A single opportunity to respond to Validation Correction Requests (VCRs) · Advance notice (8 weeks) required for new active substance submissions · **Reduction of the Route B reference approval window from 10 years to 5 years** (Route A remains unchanged at 2 years). A transition phase will be in place; therefore applicants can continue using the current process until **31 August 2026**."

**Anything written before July 2026 saying "Recognition B = 10 years" is now WRONG. It is 5 years.** As of today (2026-08-05) you are inside the transition window, which closes in 26 days.

### 4.3 Reference Regulators (RRs) — complete official table (VERIFIED verbatim)

| Country / jurisdiction | Regulatory authority |
|---|---|
| Australia | Therapeutic Goods Administration (TGA) |
| Canada | Health Canada |
| Switzerland | SwissMedic |
| Singapore | Health Science Authority Singapore (HSA) |
| Japan | Pharmaceuticals and Medical Devices Agency (PMDA) |
| United States | Food and Drug Administration (FDA) |
| European Union / EEA | European Medicines Agency (EMA) **and** Member State Competent Authorities of the EU, Norway, Iceland and Lichtenstein *(includes centralised, MRP/DCP and individual member state national routes)* |

**7 jurisdictions.** Critical constraint (verbatim): *"the RR authorisation must have undergone a full and standalone review. RR assessments based on reliance or recognition of authorisations in another territory cannot be used."* → **You cannot chain reliance.** An Australian TGA approval that itself relied on FDA is not a valid RR basis. **"Full unredacted assessment reports from the referencing authority will be required."** MHRA will not obtain them from the RR — the applicant must.

### 4.4 "Same product" definition (verbatim)
> "the same qualitative and quantitative composition (active substance(s) and excipients), the same pharmaceutical form and the same therapeutic use from Applicants belonging to the same company or group of companies or which are 'licensees'."

⚠️ **For a repurposing company this is the binding constraint.** Same *therapeutic use* is required — a **new indication** for an old drug is by definition not "the same product," so a repurposed indication cannot ride IRP on the strength of the original-indication foreign approval. IRP only helps you once *someone* (you, your group, or your licensor) already holds the repurposed indication at an RR.

### 4.5 Recognition A vs Recognition B — exact rules

| | **Recognition A** | **Recognition B** |
|---|---|---|
| Timetable | **60 calendar days** from successful validation | **110 calendar days** |
| Clock stops | **None** ("There is no clock stop") | **One, at day 70**, applicant gets **up to 60 days** to respond |
| RR approval age limit | **granted within the previous 2 years** | **granted within the previous 5 years** (was 10 yrs pre-13 Jul 2026) |
| Manufacturing | must be **same process as approved by RR**, with GMP compliance meeting MHRA requirements at time of submission | — |
| Entry rule | meets IRP criteria **and triggers none** of the Recognition B criteria | triggers **any one or more** of the 24 B-criteria |
| Failure mode | *"If major objections or concerns ... cannot be resolved within 60 days, the timetable will **revert to Recognition B** timeframe"* | *"If there are outstanding major objections or other concerns at day 110, formal advice on approvability will be sought from **CHM**, and the timetable will **revert to the national 210-day timetable**"* |
| Committee | — | Runs to a fixed monthly calendar to align with **CHM (Commission on Human Medicines)** meetings |

**Hard cap:** *"Authorisations more than 5 years old are not eligible for IRP."* An RR approval older than 5 years → **national route only** (210 days).

**Recognition B fixed calendar (VERIFIED verbatim, 2026 rows):** submissions are only accepted against monthly slots.

| Submission deadline | Procedure start | CHM meeting | Day 70 |
|---|---|---|---|
| 08/01/2026 | 22/01/2026 | 27/03/2026 | 02/04/2026 |
| 05/02/2026 | 19/02/2026 | 24/04/2026 | 30/04/2026 |
| 05/03/2026 | 19/03/2026 | 22/05/2026 | 28/05/2026 |
| 09/04/2026 | 23/04/2026 | 26/06/2026 | 02/07/2026 |
| 14/05/2026 | 28/05/2026 | 31/07/2026 | … |

⚠️ *"If the application fails validation or is not validated until after the corresponding procedure start date because of an outstanding validation correction request, the procedure start date will be **deferred to the following month**."* A validation slip costs you ~4 weeks.

### 4.6 The 24 Recognition B triggers (VERIFIED, complete verbatim list)
1. RR granted a **conditional or exceptional circumstances MA** (or international equivalent)
2. The application **seeks** a conditional/exceptional circumstances MA in UK
3. Additional manufacturing sites cited **not assessed by the RR** (except secondary packaging, labelling, QP release)
4. **Substantial changes in the manufacturing process or analytical methods** vs. RR
5. At least one manufacturing site **not yet GMP certified**
6. **Environmental risk assessment (ERA)** not assessed by the RR
7. **Risk management plan (RMP)** as proposed for UK not assessed by the RR
8. **UK-specific risk management activities** required
9. RR mandated one or more **post-authorisation safety studies (PASS)**
10. Product contains a **first-in-class new active substance**
11. Clinical efficacy/safety data available for a **later cutoff** than RR assessed
12. Pivotal clinical data are from **single-arm studies**
13. Pivotal clinical data include **real-world data**
14. Product is an **ATMP** (advanced therapy medicinal product)
15. Product is a **fractionated plasma product**
16. Application includes a **proposal for orphan drug designation**
17. Bioequivalence/therapeutic-equivalence **comparator sourced outside UK/EU/EEA** (generic/hybrid/biosimilar)
18. Product is **not subject to medical prescription** (OTC)
19. **Co-packaged medical device** components lacking CE or UKCA marking
20. Required **IVD** lacks CE or UKCA marking
21. Approved/notified body report unavailable for **integral medical device** components
22. RR assessment cites **guidelines not adopted by MHRA**
23. **Container closure system (incl. pack sizes), shelf life or storage conditions differ** from RR, and/or additional stability studies provided
24. Product includes an **excipient not previously used in authorised medicinal products in the UK**

⚠️ **For rare-disease repurposing, criteria 12, 13, 16 and 14 mean you are almost always in Recognition B (110 days), not A.** Single-arm pivotal + RWD + orphan proposal is the standard rare-disease evidence package. Budget 110 days + a 60-day clock-stop = up to **~170 days** worst case, not 60.

### 4.7 Scope (VERIFIED verbatim)
**In scope — Human Medicines Regulations 2012:**
- **Reg 50** — chemical & biological new active substances *and known active substances*
- **Reg 51B** — generics
- **Reg 52B** — hybrids
- **Reg 53B** — biosimilars
- **Reg 55** — new fixed combination products

**Post-authorisation (Section 6):** line extensions, **variations (Type IB, Type II)** and renewals (incl. annual renewal of conditional MAs, annual reassessment of exceptional-circumstance MAs). Type IA only if grouped with IB/II. Works for products originally authorised via direct national, MRDCRP or ECDRP routes. **A/B classification and the eligibility form do NOT apply to variations and renewals** — standard national post-auth timetables apply. Same RR recommended across the lifecycle; changing RR must be justified and flagged in the cover letter.

**Explicitly NOT in scope (verbatim):**
- Traditional herbal registrations
- Homoeopathic registrations (Simplified Registration Scheme)
- Homeopathic national rules authorisations (National Rules Scheme)
- **Well-established use bibliographic applications (Regulation 54 HMRs)** ← *directly relevant: the classic repurposing/bibliographic route is barred from IRP*
- **Cancelled authorisations** cannot support an IRP application
- **Emergency approvals** are not eligible
- Applications **previously submitted nationally and refused or withdrawn before determination** cannot be resubmitted via IRP — must go direct national, explicitly addressing prior objections

### 4.8 Process mechanics
- **Applicant/MAH must be established in the UK (GB or NI) or in the EU/EEA**, and be the same company/legal group as the RR MAH, or a demonstrable **licensee** with a written declaration covering Reg 74/75 HMR obligations. Third-party applications are possible with written assurance.
- **Eligibility form:** online eligibility checker, **completed at least 8 weeks before planned MAA submission** (was 6 weeks; raised to 8 in the July 2026 update). Outcome = Recognition A / Recognition B / **triage**.
  - Non-NAS + clear A or B → submit form **with** the MAA
  - Requires triage → email to **Recognition@mhra.gov.uk ≥6 weeks** before submission; MHRA responds **within 10 working days**
  - **New active substance** → mandatory advance notice, form to Recognition@mhra.gov.uk ≥6 weeks before (8 weeks under the new rules)
  - ⚠️ **UNVERIFIED (fetch blocked — DNS does not resolve)**: `https://irp-eligibility.mhra.gov.uk/` → `curl: (6) Could not resolve host`. The checker is reached from the guidance page, not at that guessed hostname.
- **PL number required before completing the eligibility form.** Need a 5-digit company number first (`Reference.Data@mhra.gov.uk`), then a PL via MHRA Submissions or `PLNumberAllocation@mhra.gov.uk`.
- **Pre-submission meeting (PSM) is optional**, not required; if wanted, request **≥3 months** ahead via `presubmission@mhra.gov.uk`.
- **Fees:** page says only *"Fees charged by MHRA can be found here: MHRA fees. Use the Fees calculator."* No IRP-specific fee schedule on this page. **UNVERIFIED** — I did not fetch the MHRA fees page.
- **Section 10** lists per-RR the exact assessment documents that constitute a complete package, with `**` marking mandatory items in all cases.
- **Urgent public health need → national fast track is preferred over IRP.** Pointer: `https://www.gov.uk/guidance/apply-for-a-licence-to-market-a-medicine-in-the-uk#fast-tracking-a-marketing-authorisation` (**UNVERIFIED** — extracted from the IRP body, not separately fetched).

---

## 5. ILAP — Innovative Licensing and Access Pathway (current 2026 state)

**VERIFIED** `https://www.gov.uk/government/publications/innovative-licensing-and-access-pathway-ilap` → HTTP 200, **`public_updated_at` 2026-08-05 (today)**.
**VERIFIED** `https://www.gov.uk/government/publications/innovative-licensing-and-access-pathway-ilap/ilap-application-guidance` → HTTP 200.

- **History:** original ILAP launched Jan 2021; **paused/reformed** — see **VERIFIED-by-search** `/government/publications/statement-of-policy-intent-relaunch-of-the-innovative-licensing-and-access-pathway` (2024-11-06). Relaunched integrated version announced 2025-01-30; first investigational products admitted 2025-10-14; latest passport cohort (cancer + dementia) announced **2026-08-04**.
- **The Innovation Passport still exists** and is *"the first step in the ILAP and the mandatory entry point."*
- **Innovation Passport eligibility — 7 criteria (VERIFIED):**
  1. Medicine or **drug-device combination** with a therapeutic aim
  2. **Not** an immunisation for prevention of infection/disease
  3. Applicant is a legal entity with rights to market in the UK
  4. Clinical stage: human safety pharmacology **preliminarily characterised**, safety in humans demonstrated, **confirmatory trials not yet started**
  5. Intention to obtain UK marketing authorisation
  6. Commitment to work with ILAP Partners on a **Target Development Profile (TDP)**
  7. Commitment to conduct feasibility for **opening clinical trial sites in the UK**
  - ⚠️ Criterion 4 is a **hard window for repurposing**: a well-characterised old drug where you're about to start (or have started) a confirmatory trial may be *too late*. Apply before confirmatory trials begin.
- **Application rounds — 4/year, 3-month windows (VERIFIED):**

  | Round | Window | Outcome date |
  |---|---|---|
  | R1 | 28 Apr – 30 Jul 2026 | 23 Oct 2026 |
  | R2 | **4 Aug – 4 Nov 2026** | 4 Feb 2027 |
  | R3 | 9 Nov 2026 – 11 Feb 2027 | 14 May 2027 |
  | R4 | 18 Feb – 20 May 2027 | 20 Aug 2027 |

  **Round 2 opened yesterday (4 Aug 2026).** Outcome lag ≈ 3 months after window close.
- **Partners (VERIFIED):** MHRA, NICE, SMC, AWTTC, NHS England, Department of Health Northern Ireland. Supporting: DHSC, HRA, NIHR, OLS, Scottish Government, Welsh Government. **The HTA bodies are inside the pathway** — this is the point of the relaunch.
- **Fees:** guidance says fees apply; **amount not stated on these pages (UNVERIFIED).**
- **Portal — VERIFIED** `https://applyforaninnovationpassport.mhra.gov.uk/` → HTTP 200. Contact `innovationpassport@mhra.gov.uk`.
- **Attachments (VERIFIED — the XLSX was downloaded and parsed):**
  - **Innovation Passport List — `https://assets.publishing.service.gov.uk/media/6a6cb3220ddb7e4831c62aef/Innovation_Passport_list_-_August_2026.xlsx` → HTTP 200, `application/vnd.openxmlformats-...sheet`, 17,958 bytes.** Columns: `Company Name*`, `Product Name`, `Therapeutic Indication`. **Only 6 products listed**, and they are overwhelmingly rare disease:
    - iECURE Inc — ECUR-506 — neonatal onset **ornithine transcarbamylase deficiency (OTCD)**
    - Solid Biosciences — SGT-003 — **Duchenne muscular dystrophy**
    - Orchard Therapeutics — OTL-201 — **MPS-IIIA (Sanfilippo A)**
    - CervoMed — Neflamapimod — **Dementia with Lewy bodies**
    - BeOne Medicines UK — BGB-B2033 — HCC after prior systemic treatment
    - ⚠️ **Publication is opt-in** — footnote: *"Only companies that have given permission ... are included ... it is optional for IP holders to consent to sharing information publicly."* **This list materially undercounts holders. Do not treat it as a census.**
  - Innovation Passport Application Form — `.../69ef67e820a498c16734aff3/Innovation_Passport_Application.docx` (MS Word, 523 KB)
  - ILAP Data Protection & Privacy — `.../68304197a599d03a16bff499/ILAP_Data_Protection_and_Privacy_Information.pdf` (89.4 KB)
  - HTML sub-pages: ILAP Application Guidance, What's on Offer in ILAP, Webinar/Video Recordings, **ILAP Performance Metrics**

---

## 6. Downloadable / bulk lists of UK authorised products

### 6.1 What does NOT exist (stated plainly)
- **No official MHRA API.** No REST, no OpenAPI, no developer portal, no keys.
- **No downloadable register of all UK marketing authorisations.** Nothing on gov.uk, nothing on data.gov.uk (VERIFIED: CKAN returns 8 MHRA datasets, none of them product data).
- **No MHRA bulk export** of SPC/PIL/PAR. The Azure index (§1.3) is the only route, and it is undocumented.
- **No public Azure blob container listing** (VERIFIED 404).
- **The `medicines.api.mhra.gov.uk/graphql` endpoint is dead** (VERIFIED 503).

### 6.2 What DOES exist — verified downloadable files

| File | URL | Format / size | Rows | Cadence |
|---|---|---|---|---|
| **Orphan Register** | `https://assets.publishing.service.gov.uk/media/6a5a43b45ca06bf11ccb4407/Orphan_Register_Ver._3_July_2026.csv` — **VERIFIED 200, `text/csv`, 68,679 B** | CSV | **192** | ad hoc, ~monthly |
| **Expired Orphan Register** | `https://assets.publishing.service.gov.uk/media/6a58cd8860a6e36813cb42f4/Expired_Orphan_Register_Ver._1_July_2026.csv` — **VERIFIED 200, 20,342 B** | CSV | **58** | ad hoc |
| **UK Additional Monitoring list** | `https://assets.publishing.service.gov.uk/media/6a4fc6732467584757371ca8/Additional_Monitoring_JUNE_2026.xlsx` — **VERIFIED 200, 285,786 B** | XLSX | ~1,587 shared strings | **monthly** |
| **Innovation Passport list** | see §5 | XLSX | 6 | per round |

**Orphan Register — parent page VERIFIED:** `https://www.gov.uk/government/publications/orphan-registered-medicinal-products` (200; `first_published 2021-02-09`, `public_updated_at 2026-07-17`).
- **Columns (VERIFIED, row 2 of the CSV — row 1 is a prose blurb, so `skiprows=1`):**
  `Product name | Active substance | Orphan Condition | OD Indication | Designation number | Orphan Market Exclusivity Expiry date`
- Expired register adds: `Date Orphan designation removed (if different to expiry)`
- **Real rows (VERIFIED):** `ABECMA | idecabtagene vicleucel | Multiple myeloma | ... | PLGB 15105/0191/OD1 | 23/06/2032`; `Adzynma | rADAMTS13 | Thrombotic thrombocytopenic purpura | ... | PL 16189/0148-0149/OD1 | 11/05/2037`
- ⚠️ **Encoding gotchas:** file is **not clean UTF-8** — mojibake in active-substance and designation-number cells (`idecabtagene vicleucel ���`, `�PL 16189/0148-0149/OD1`). Read with `encoding='cp1252'` or `errors='replace'` and strip. Header prose row contains smart quotes. Dates are `DD/MM/YYYY`.
- ⚠️ Designation numbers use the `/OD1`, `/OD2` suffix on the PL — one PL can carry multiple orphan designations.
- **`change_history` in the Content API gives you a free changelog** (VERIFIED): *"Added latest Orphan Register"* (2026-07-17), *"Addition of Reblozyl OD1 / Addition of Vyloy"* (2026-07-16), *"Addition of ZYNYZ"* (2026-07-07), *"Update to Lutathera Orphan Market Exclusivity Expiry date"* (2026-06-18). **This is the closest thing MHRA has to an orphan-approvals change feed — poll `https://www.gov.uk/api/content/government/publications/orphan-registered-medicinal-products` and diff.**

**Additional Monitoring list (XLSX) — VERIFIED columns:** `Active Substance | Brand name | MA number* | MAH* | Product category | Reason for inclusion | Date added to the list | Comments`. Includes a "New additions" marker and reason codes such as `New active substance`. Real rows verified (RADELUMIN `PL 27959/0001`, LIMAXETIN `PL 45726/0001`). **This is effectively a rolling list of recently-authorised NASs and conditional/PASS-bearing products with MAH names attached** — the single best structured proxy for "new UK approvals" that MHRA actually publishes as a file.

### 6.3 The real bulk source: NHS dm+d (not MHRA)
- **VERIFIED** `https://isd.digital.nhs.uk/trud/users/guest/filters/0/categories/6` → HTTP 200. NHS TRUD hosts the **dictionary of medicines and devices (dm+d)** — the authoritative machine-readable catalogue of every medicinal product available in the UK NHS, with AMP/VMP/VTM hierarchy, XML, weekly releases.
- **Auth:** free registration, then an API key. **VERIFIED** that the TRUD REST API exists and validates keys: `https://isd.digital.nhs.uk/trud/api/v1/keys/<KEY>/items/<ID>/releases?latest` → returned **HTTP 400** with a dummy key (i.e., the endpoint is live and rejecting the bad key, not 404). I did not register, so the authenticated call is **UNVERIFIED**.
- **Gotcha:** dm+d is a *supply/prescribing* catalogue, not a regulatory register. It carries no PAR link, no MA grant date, no orphan status. Join it to the Azure index on PL number.

---

## 7. Practical gotchas

### 7.1 Northern Ireland vs Great Britain — the Windsor Framework
**VERIFIED** `https://www.gov.uk/government/publications/uk-wide-licensing-for-human-medicines/uk-wide-licensing-for-human-medicines` (200) and **VERIFIED** `https://www.gov.uk/government/collections/mhra-windsor-framework` (200).

- **From 1 January 2025, MHRA licenses medicines across the whole UK.** GB-only MAs can no longer be applied for. IRP guidance confirms verbatim: *"applications for GB MAs covering Great Britain only will no longer be possible. All applications must be for UK-wide MAs."*
- **Existing PLGB MAs were auto-converted to UK-wide on 1 Jan 2025** unless cancelled by 31 Dec 2024. ⚠️ **The `PLGB` prefix was retained on conversion.** So **a `PLGB` number in 2026 does NOT mean Great-Britain-only** — it usually means a converted UK-wide licence. Do not infer territory from the prefix.
- **PLNI:** MAHs holding both PLNI and PLGB for the same product had to cancel the PLNI by **30 September 2024**; missing that deadline caused the GB authorisation to be cancelled instead.
- **From 1 January 2025 EU/EC union authorisations are no longer valid for Northern Ireland.** EMA centrally authorised products **no longer automatically cover NI**; MHRA now issues UK-wide authorisations covering NI.
- **Number prefixes you will encounter:** `PL` (new UK-wide from 1 Jan 2025), `PLGB` (legacy GB, mostly now UK-wide), `PLNI` (NI-only legacy), `PLPI` (parallel import), `THR` (traditional herbal). The regex in the site's own JS chunk `9276` (VERIFIED) is `(PL|PLGB|PLNI|PLPI|THR|...)`.
- **Index reality check (VERIFIED counts):** `territory` = `UK` 63,650 · `GB` 8,607 · `NI` **48** · null 6,669. The `territory` field is **stale and inconsistently populated** — 6,669 nulls and only 48 NI docs. **Do not use `territory` as a reliable jurisdiction filter.** Note the search JS builds its default filter as `(territory eq 'UK' or territory eq null)` — i.e. the site itself treats null as UK.

### 7.2 MHRA vs EMA post-Brexit / grandfathering
- **Yes, historic EU centrally-authorised products WERE grandfathered.** On 1 Jan 2021 all EU CAPs valid in the UK were automatically converted to GB MAs and given `PLGB` numbers ("grandfathered" MAs). Those then auto-converted again to UK-wide on 1 Jan 2025. **Two conversion events, two number regimes — historical PL-number joins across 2020/2021 and 2024/2025 boundaries will break.**
- ⚠️ **The MHRA products site does NOT hold everything.** VERIFIED verbatim from `https://products.mhra.gov.uk/about`: *"We hold data for medicines licensed at a national (UK) level. Some medicines are licensed by the European Medicines Agency (EMA). For product information on these medicines, use the EMA website."* → **You need EMA as a second source.** For older/EU-origin products the assessment is an **EPAR**, and *"For some medicines licensed at a European level, the PARs are prepared by either the EMA or the responsible authority of another EU member state."*
- ⚠️ **Cancelled products vanish on a timer.** VERIFIED verbatim: *"Once a marketing authorisation has been cancelled, the product information will stay on the website for a year."* (6 months to exhaust stocks + 6 months for patients at home.) **The index is a snapshot, not an archive. If you don't snapshot it yourself, withdrawn-product history is unrecoverable.** For a repurposing shop mining discontinued/withdrawn assets, this is the single most damaging gotcha — **start archiving now.**
- **Refused applications:** PARs published for all MAAs refused after 1 April 2019. Rare, but high signal.

### 7.3 Orphan designation — UK ≠ EU/US
- **VERIFIED** `https://www.gov.uk/guidance/orphan-medicinal-products-in-great-britain` (200, updated 2026-02-06).
- **There is no standalone pre-marketing orphan designation in the UK.** Orphan status is assessed **at the time of the MA or variation application** and decided **at the time of the approval decision**. You cannot bank a UK orphan designation early the way you can with FDA ODD or EMA OD. This changes the sequencing of any repurposing programme.
- Criteria: life-threatening/chronically debilitating; **prevalence in UK ≤ 5 in 10,000**; or unlikely that marketing would justify the investment; **and** no satisfactory existing method **or** the product offers **significant benefit**.
- Exclusivity: **up to 10 years**, +2 years with a completed PIP; MHRA can cut to **6 years** if criteria no longer met.
- ⚠️ Cross-reference with §4.6 criterion 16: **proposing orphan designation automatically forces IRP into Recognition B (110 days).** Orphan status and the fast IRP route are mutually exclusive.

### 7.4 Regulatory change in flight (2025–2026) — watch these
- **Draft rare disease therapies regulatory framework — VERIFIED** `https://www.gov.uk/api/content/government/consultations/draft-rare-disease-therapies-regulatory-framework` (200). Opened **21 May 2026**, **closed 30 July 2026** (6 days ago — outcome pending). Proposes a new **Investigational Marketing Authorisation (IMA)**: *"a single, flexible authorisation ... which would allow controlled early access to a therapy while further clinical and real-world evidence continues to be generated,"* covering eligibility, evidence requirements, patient engagement, lifecycle oversight, and transition to a full MA. Explicitly aimed at *"extremely small patient populations, limited natural history data, difficulties conducting randomised controlled trials, and ... individual- or family-specific genetic variants."* **This is the most consequential pending UK change for a rare-disease company. Attachments (VERIFIED URLs): `https://assets.publishing.service.gov.uk/media/6a0c189dc75cc34a8ff8f48e/draft_rare_disease_therapies_regulatory_framework.pdf` and `.../6a0dc2a25c3c79da61662e24/Rare_Disease_Therapies_survey_questions.pdf`.**
- Related, **VERIFIED-by-search-index only (UNVERIFIED page fetch)**: `/government/publications/rare-therapies-and-uk-regulatory-considerations` (2025-11-02), `/government/news/landmark-new-plans-bring-treatments-for-rare-diseases-a-step-closer` (2026-05-20).
- **EAMS (Early Access to Medicines Scheme) — VERIFIED** `https://www.gov.uk/government/collections/early-access-to-medicines-scheme-eams-scientific-opinions` (200, updated 2026-07-10). Each scientific opinion is a separate gov.uk publication → enumerable via the Search API. Relevant precedent found: *EAMS scientific opinion: Raxone to treat decline of respiratory function in Duchenne Muscular Dystrophy*.
- **National assessment procedure — VERIFIED** `https://www.gov.uk/guidance/national-assessment-procedure-for-medicines` (200) — the 210-day fallback when IRP is unavailable.

### 7.5 Engineering gotchas for the Azure index
- The `api-key` is **undocumented and rotatable**. Build a self-healing step: fetch `https://products.mhra.gov.uk/`, parse `__NEXT_DATA__` → `buildId`, fetch `_buildManifest.js` → chunk list, download the search chunk, regex `api-key","([0-9A-F]{32})"` and `https://(\w+)\.search\.windows\.net`.
- `created` is **`Edm.String` and NOT filterable** (VERIFIED error: *"'created' is not a filterable field"*). Sortable only. Incremental sync = `$orderby=created desc` + paginate until watermark.
- `$skip` hard limit **100,000**. Total corpus is 78,974, so full crawl works today — but if the corpus grows past 100k you must shard by `doc_type` or facet.
- `pl_number` and `substance_name` are `Collection(Edm.String)`; use `any(x: x eq '...')`. Values are **uppercase and unpunctuated** (`PLGB000571613`, `SIROLIMUS`) — normalize before querying.
- The site's own default filter is `(territory eq 'UK' or territory eq null)` plus optional `active_substances/any(...)` and `product_name eq '<UPPER>'` — note **`active_substances`** (plural, in the filter builder) vs **`substance_name`** (in returned docs). Both appear in the JS; `substance_name` is what the live `products-index` returns.
- `scoringProfile=preferKeywords` exists on the index and is what the UI uses — include it to reproduce site ranking.
- Rate limits: none observed across ~40 requests in this session, but this is an unmetered free tier someone else pays for. Throttle to be a good citizen; a full 79-page crawl should be spread out.

---

## 8. Verification ledger

**VERIFIED (fetched, HTTP 200, relevant content returned):**
`products.mhra.gov.uk/` · `/search?search=sirolimus` · `/product/?product=RAPAMUNE` · `/substance/?substance=SIROLIMUS` · `/substance-index/?letter=S` · `/about` · `/robots.txt` · `/sitemap.xml` · `/_next/static/ufPgk6V6gc0hHc9abqxts/_buildManifest.js` · `/_next/static/chunks/843-012836701345ef2e.js` (+4 other chunks) · `mhraproducts4853.search.windows.net/indexes/products-index/docs` (many query shapes, GET and POST) · `.../indexes/bmgf-index/docs` · `mhraproducts4853.blob.core.windows.net/docs/<sha>` (PDF, 882 KB) · `gov.uk/government/publications/international-recognition-procedure/international-recognition-procedure` · `gov.uk/api/content/...international-recognition-procedure` · `gov.uk/guidance/find-product-information-about-medicines` (+ Content API) · `gov.uk/government/publications/innovative-licensing-and-access-pathway-ilap` · `.../ilap-application-guidance` · `applyforaninnovationpassport.mhra.gov.uk/` · `assets.publishing.service.gov.uk/.../Innovation_Passport_list_-_August_2026.xlsx` (downloaded, parsed) · `.../Orphan_Register_Ver._3_July_2026.csv` (downloaded, parsed) · `.../Expired_Orphan_Register_Ver._1_July_2026.csv` (downloaded, parsed) · `.../Additional_Monitoring_JUNE_2026.xlsx` (downloaded, parsed) · `gov.uk/government/publications/mhra-performance-data` (+ `/mhra-performance-data`) · `gov.uk/government/organisations/medicines-and-healthcare-products-regulatory-agency` (+ Content API) · `gov.uk/api/search.json` (many query shapes) · `gov.uk/search/news-and-communications.atom?organisations[]=...` · `gov.uk/government/publications/uk-wide-licensing-for-human-medicines/uk-wide-licensing-for-human-medicines` · `gov.uk/guidance/orphan-medicinal-products-in-great-britain` · `gov.uk/government/publications/orphan-registered-medicinal-products` (+ Content API) · `gov.uk/government/collections/mhra-windsor-framework` · `gov.uk/government/collections/early-access-to-medicines-scheme-eams-scientific-opinions` · `gov.uk/guidance/national-assessment-procedure-for-medicines` · `gov.uk/api/content/government/consultations/draft-rare-disease-therapies-regulatory-framework` · `ckan.publishing.service.gov.uk/api/3/action/package_search?q=MHRA` · `data.gov.uk/search?q=MHRA` · `isd.digital.nhs.uk/trud/users/guest/filters/0/categories/6`

**VERIFIED NEGATIVE (fetched, got an error — the error IS the finding):**
- `https://www.gov.uk/guidance/international-recognition-procedure` — **HTTP 404** (does not exist)
- `https://www.gov.uk/guidance/public-assessment-reports-for-medicines` — **HTTP 404** (does not exist)
- `https://www.gov.uk/government/organisations/medicines-and-healthcare-products-regulatory-agency/about/statistics` — **HTTP 404**
- `https://medicines.api.mhra.gov.uk/graphql` — **HTTP 503** on GET and POST (decommissioned)
- `https://irp-eligibility.mhra.gov.uk/` — **DNS resolution failure** (guessed hostname; not real)
- `https://mhraproducts4853.blob.core.windows.net/docs?restype=container&comp=list` — **HTTP 404** (listing disabled)
- `https://mhraproducts4853.search.windows.net/indexes[/products-index]?api-version=...` — **HTTP 403** (query key cannot read index metadata)
- `.../docs/suggest?suggesterName=sg` — **HTTP 400**
- gov.uk Search API, MHRA + `document_type=statistics` — **`total: 0`**

**UNVERIFIED (not fetched in this session — cited from within verified page bodies, treat as unconfirmed):**
- `https://www.gov.uk/guidance/safety-public-assessment-reports`
- `https://www.gov.uk/guidance/apply-for-a-licence-to-market-a-medicine-in-the-uk#fast-tracking-a-marketing-authorisation`
- MHRA fees page / fees calculator
- `/government/publications/statement-of-policy-intent-relaunch-of-the-innovative-licensing-and-access-pathway`
- `/government/publications/rare-therapies-and-uk-regulatory-considerations`
- NHS TRUD authenticated API (`/trud/api/v1/keys/<KEY>/...`) — endpoint confirmed live via HTTP 400 on a dummy key, but no successful authenticated call was made

*Note: web search quota for this session was exhausted mid-research; all subsequent discovery was done via the gov.uk Search API (`https://www.gov.uk/api/search.json`) and gov.uk Content API, which are more authoritative anyway.*