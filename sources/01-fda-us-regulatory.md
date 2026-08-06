# US FDA Regulatory Data Sources — Machine-Access Reference

All URLs below were fetched live on **2026-08-05**. Status codes, content types, byte sizes, record counts and file manifests are from actual responses, not memory.

---

## 0. BLOCKING FINDING — read before building the pipeline

Your stated strategy is **"screen off-patent/generic drugs → 505(b)(2) approval → earn a transferable PRV."** The statute forecloses that. **VERIFIED** against the current US Code (uscode.house.gov prelim, retrieved 2026-08-05).

**21 U.S.C. § 360ff(a)(4) [FD&C Act § 529(a)(4)]** — a "rare pediatric disease product application" must be one that:

> (B)(i) is for such a drug—
> (I) that contains **no active moiety** (as defined … in section 314.3 of title 21, CFR …) **that has been previously approved in any other application under subsection (b)(1), (b)(2), or (j) of section 355**; and
> (II) **that is the subject of an application submitted under section 355(b)(1)**

Consequences:

| Your leg | RPD PRV eligible? | Why |
|---|---|---|
| (a) US off-patent / generic repurposing via **505(b)(2)** | **NO — categorically** | Active moiety already approved under 505(b)(1)/(b)(2)/(j); and 505(b)(2) is not 505(b)(1) |
| (a') Drug **approved abroad, never approved in US** via **505(b)(1) NDA** | **YES** | Novel active moiety in the US; must be a full 505(b)(1) |
| Biologics analog | 351(a) BLA, no previously approved active ingredient under 351(a)/351(k) | § 360ff(a)(4)(B)(ii) |

Additional statutory gates in the same subsection, all **VERIFIED**:
- **(D)** application must rely on **clinical data derived from studies examining a pediatric population** and pediatric dosages.
- **(E)** must **not seek an adult indication** in the original RPD product application.
- **(C)** must be deemed **eligible for priority review** by FDA.
- **(F)** approved after Sept 30, 2016.

Orphan-drug designation + 7-year orphan exclusivity (§ 360bb / § 360cc) **do** remain available on 505(b)(2) repurposing — that path is intact. The PRV is not. Build the screening pipeline with a hard `active_moiety_previously_approved_in_US` boolean gate that routes candidates into two disjoint funnels.

**Program status (VERIFIED):** the RPD PRV program lapsed after Dec 20, 2024 and was **reauthorized by the Consolidated Appropriations Act, 2026 (Pub. L. 119-75, § 6604(a)), enacted Feb 3, 2026**. § 360ff(b)(5) now reads: *"The Secretary may not award any priority review vouchers under paragraph (1) after September 30, 2029."* The US Code amendment note explicitly records the substitution of "September 30, 2029" for the old Dec-20-2024 designation deadline / Sept-30-2026 approval deadline. **There is no longer a separate designation-by deadline** — FDA's own page confirms this in terms. Your effective window: NDA/BLA **approval** on or before 2029-09-30.

---

## 1. Statutory test for "rare pediatric disease"

**Codification:** FD&C Act § 529(a)(3) = **21 U.S.C. § 360ff(a)(3)**.
**VERIFIED source:** `https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title21-section360ff&num=0&edition=prelim` (200, 182 KB) and `https://www.govinfo.gov/content/pkg/USCODE-2023-title21/html/USCODE-2023-title21-chap9-subchapV-partB-sec360ff.htm` (200).

Exact text:

> **(3) Rare pediatric disease** — The term "rare pediatric disease" means a disease that meets **each** of the following criteria:
> **(A)** The disease is a **serious or life-threatening** disease in which the serious or life-threatening manifestations **primarily affect individuals aged from birth to 18 years**, including age groups often called neonates, infants, children, and adolescents.
> **(B)** The disease is a **rare disease or condition, within the meaning of section 360bb** of this title.

**Prevalence prong (§ 360bb / FD&C § 526), quoted from FDA's own draft guidance:** a rare disease or condition is one that affects **(1) fewer than 200,000 persons in the US**, or **(2) affects more than 200,000 and there is no reasonable expectation that US development/availability cost will be recovered from US sales**. An **"orphan subset"** of a ≥200,000-person disease also qualifies, but only if the orphan subset itself is serious/life-threatening and its serious/life-threatening manifestations primarily affect ages 0–18. Orphan-subset justification requires showing the drug would be inappropriate outside the subset due to toxicity, mechanism, or prior clinical experience — **21 CFR 316.3(b)(13)** and **21 CFR 316.20(b)(6)**.

**How FDA operationalizes "primarily affect" (VERIFIED, extracted from the guidance PDF text):**
- FDA decomposes the disease into individual manifestations and determines **per-manifestation** which primarily affect children vs. adults.
- Factors: *"timing and rate of disease progression (e.g., end-stage organ disease occurs in childhood), manifestations of abnormal growth or development, and whether the proportion of children is greater than the proportion of adults with the given manifestation."*
- **If ANY serious/life-threatening manifestation primarily affects children, FDA will consider the whole disease a rare pediatric disease.** Worked example given: cystic fibrosis qualifies even though impaired lung function primarily affects adults, because other manifestations primarily affect children.
- Prevalence estimation: **therapeutic drugs** → number of individuals **diagnosed**; **vaccines/diagnostics/preventive drugs** → number of persons of all ages to whom the drug would be administered in the US **annually**.

**Governing guidance:** *Rare Pediatric Disease Priority Review Vouchers, Guidance for Industry, DRAFT, July 2019 (Revision 1)*.
- Landing page: `https://www.fda.gov/regulatory-information/search-fda-guidance-documents/rare-pediatric-disease-priority-review-vouchers` — **VERIFIED 200**
- Direct PDF: `https://www.fda.gov/media/90014/download` — **VERIFIED 200, application/pdf, 313,761 bytes**
- Docket **FDA-2014-D-1461**. Still **Draft** as of today — never finalized.

**Designation mechanics — § 360ff(d), VERIFIED:** request is made by the sponsor; FDA must determine within **60 days**; the request **"shall be made at the same time a request for designation of orphan disease status under section 360bb or fast-track designation under section 356 is made"**; and critically — **"Requesting designation under this subsection is not a prerequisite to receiving a priority review voucher."** Submit to `orphan@fda.hhs.gov`.

---

## 2. Rare Pediatric Disease designation — IS THERE A PUBLIC LIST?

### **NO. There is no public RPD designation database, list, file, or feed. This is confirmed, not assumed.**

| Evidence | Result |
|---|---|
| FDA program page full-text + full link extraction | Contains **zero** links to any designation list. Only guidance, contacts, sunset text. Page "Content current as of: 04/29/2026". `https://www.fda.gov/industry/medical-products-rare-diseases-and-conditions/rare-pediatric-disease-designation-and-priority-review-voucher-programs` — **VERIFIED 200** |
| Full `www.fda.gov` sitemap sweep (43 sitemap pages, **85,349 URLs**) grepped for `rare-pediatric` | Exactly **2 hits**: the program page and the guidance page. No list page exists anywhere on fda.gov. |
| Statutory publication duty | § 360ff(f)(1) requires Federal Register notice **only** for (A) voucher *issuance* and (B) approval of a product *under* a voucher. **No FR/publication duty attaches to designations.** |
| Literature | The definitive decade-review (Orphanet J Rare Dis 2024, PMC10895788) analyzed RPD designations from an **internal FDA database**; RPD designations are stated to be **not publicly disclosable** and absent from any public FDA database (unlike orphan designations). |

**Implication for competitor monitoring:** RPD designation grants are only observable via **sponsor self-disclosure** — press releases, 8-K/10-K/S-1 filings, investor decks. Any RPD-designation intelligence layer must be built on SEC EDGAR full-text search + newswire + company IR feeds, **not** on FDA.

**Cross-signal that is public and highly correlated:** because § 360ff(d)(2) requires the RPD request to be filed *simultaneously* with an orphan or fast-track designation request, a **new orphan designation for a pediatric-onset serious disease is a leading indicator of a concurrent RPD request.** The orphan database (§4) is fully downloadable and daily-fresh — use it as the RPD proxy.

**Dead/renamed:** `https://www.fda.gov/industry/designating-orphan-product-drugs-and-biological-products/rare-pediatric-disease-designation-and-voucher-programs` → **404**. Old slug; content moved to the `medical-products-rare-diseases-and-conditions/` path.

---

## 3. Priority Review Vouchers — the authoritative machine-readable ledger

**FDA does not publish a consolidated PRV list page for any of the three programs.** Sitemap grep for `priority-review-voucher` across all 85,349 fda.gov URLs returns only 5 hits (one CDER tropical program page, one RPD program page, three guidance pages) — **no awarded/redeemed list exists on fda.gov**.

### The real source: **Federal Register API** — statutorily mandated, structured, free, no auth

§ 360ff(f)(1) (**VERIFIED text**): *"The Secretary shall publish a notice in the Federal Register … not later than 30 days after … (A) The Secretary issues a priority review voucher … (B) The Secretary approves a drug … for which the sponsor … used a priority review voucher."*

- **Endpoint:** `https://www.federalregister.gov/api/v1/documents.json` — **VERIFIED 200**
- **Auth:** none. **Format:** JSON. **Cadence:** daily (FR publication days).
- **Key params:** `conditions[agencies][]=food-and-drug-administration`, `conditions[term]="priority review voucher"`, `conditions[publication_date][gte]=YYYY-MM-DD`, `per_page=1000` (max), `order=newest`, `fields[]=title|publication_date|document_number|html_url|type|abstract`
- **Note:** use `conditions[term]`, **not** `conditions[search]` (the latter is silently ignored and returns a null count).

**Live census (retrieved 2026-08-05, 186 FDA documents matching the phrase):**

| Title pattern | Count | Range | Meaning |
|---|---|---|---|
| `Issuance of Priority Review Voucher; Rare Pediatric Disease Product; <DRUG>` | **73** | 2014-03-12 → 2026-05-11 | RPD PRV **awarded** |
| `Issuance of Priority Review Voucher; Material Threat Medical Countermeasure Product; <DRUG>` | **9** | → 2025-04-23 (EBANGA) | MCM PRV awarded |
| `Notice of Approval of Product Under Voucher: …` | **32** | 2019-05-03 → 2026-04-16 | PRV **redeemed** |
| `Fee Rate for Using a Priority Review Voucher in Fiscal Year <YYYY>` | 5+ | annual, ~Sept | Redemption fee |

Most recent issuances: `AVLAYAH (tividenofusp alfa-eknm)` 2026-05-11; `OTARMENI (lunsotogene parvec-cwha)` 2026-05-06. Most recent redemptions: `MNEXSPIKE` and `MRESVIA` both 2026-04-16.

**GOTCHAS (all observed in live data):**
1. **Title strings are not stable.** Historical variants include `Approval of Product Under Voucher: …` (2018-11-23), `Notice of Approval of Products Under Voucher: … Vouchers` (plural, 2018-04-10), `Use of Rare Pediatric Disease Priority Review Voucher; Approval of a Drug Product` (2015-08-24), and a literal typo `Notice of Approval of Product U nder Voucher` (2020-06-01). **Match with a tolerant regex, not exact prefixes.**
2. **Redemption notices only start 2019.** The § 360ff(f)(1)(B) publication practice began ~2019; earlier redemptions (2009–2018) are not in this series.
3. **Tropical disease PRV issuances are NOT published in the FR.** Query for `"Issuance of Priority Review Voucher; Tropical Disease Product"` returns **0**. § 524 contains no analogous notice requirement. Tropical PRV awards must be tracked from press releases / approval letters. Only *fee rates* and *disease-list designation orders* appear in the FR for the tropical program.
4. `conditions[term]` is **full-text**, so raw counts include documents merely *citing* the phrase. Post-filter on `title` regex.

### Program pages

| Program | URL | Status | What's on it |
|---|---|---|---|
| Rare Pediatric Disease | `https://www.fda.gov/industry/medical-products-rare-diseases-and-conditions/rare-pediatric-disease-designation-and-priority-review-voucher-programs` | **VERIFIED 200** | Sunset text, designation submission process, contacts. **No lists.** |
| Tropical Disease | `https://www.fda.gov/about-fda/center-drug-evaluation-and-research-cder/tropical-disease-priority-review-voucher-program` | **VERIFIED 200** | Full qualifying-disease list (28 diseases incl. Brucellosis, Opisthorchiasis, Paragonimiasis added 2020-07-15), docket **FDA-2008-N-0567-0011** for adding diseases. **HTML-scrape only, no file.** |
| Material Threat MCM | **NO program page exists** | — | Sitemap sweep found none. Only the draft guidance page. |

**Dead URLs found:** `fda.gov/about-fda/center-drug-evaluation-and-research-cder/tropical-disease-priority-review-vouchers` → 404 (note: `-voucher-program`, singular+program, is the live slug). `fda.gov/drugs/development-resources/tropical-disease-priority-review-vouchers` → 404. `fda.gov/about-fda/center-drug-evaluation-and-research-cder/material-threat-medical-countermeasure-priority-review-vouchers` → 404.

**Guidances:**
- Tropical Disease PRVs (Final, 2016-10-06, FDA-2008-D-0530): `https://www.fda.gov/regulatory-information/search-fda-guidance-documents/tropical-disease-priority-review-vouchers`
- Material Threat MCM PRVs (Draft, 2018-01-19, FDA-2017-D-6880): `https://www.fda.gov/regulatory-information/search-fda-guidance-documents/material-threat-medical-countermeasure-priority-review-vouchers-draft-guidance-industry`

**New adjacent program worth tracking:** the **Commissioner's National Priority Voucher (CNPV) pilot** now exists (sitemap shows 15+ pages, incl. `industry/commissioners-national-priority-voucher-cnpv-pilot-program` and press announcements for first/second batches and 7 approvals to date). Separate from statutory PRVs; award announcements are press releases, not FR notices.

---

## 4. Orphan Drug Designations & Approvals (OOPD) — **fully downloadable, this is your workhorse**

**Search UI:** `https://www.accessdata.fda.gov/scripts/opdlisting/oopd/` — **VERIFIED 200**
**Instructions page:** `https://www.fda.gov/industry/designating-orphan-product-drugs-and-biological-products/instructions-searchable-designation-database` — VERIFIED 200 (last updated 2017-10-24)

**There is no documented API, but there IS an undocumented full-corpus bulk export.** The search form exposes `Output_Format=Excel`, and the results endpoint honors it with no record cap.

```
POST https://www.accessdata.fda.gov/scripts/opdlisting/oopd/OOPD_Results.cfm
Content-Type: application/x-www-form-urlencoded
Referer: https://www.accessdata.fda.gov/scripts/opdlisting/oopd/

Product_name=&sponsor_name=&Designation=
&Designation_Start_Date=01/01/1983
&Designation_End_Date=08/05/2026
&Search_param=DESDATE          # DESDATE = all designations | EXCSTART = approved only
&Output_Format=Excel           # Short | Detailed | Excel
&Sort_order=Date_Order         # GENERIC_NAME | Date_Order | Date_Reverse_Order
&RecordsPerPage=25             # ignored for Excel output
&newSearch=Run Search
```

**VERIFIED live result:** `HTTP 200`, `Content-Type: application/msexcel;charset=UTF-8`, `Content-Disposition: attachment; FILENAME=Search_results.xls`, **8,890,799 bytes**, **8,190 designation records**, newest record dated **08/05/2026** (same-day fresh).

**GOTCHA: the ".xls" is a lie.** The payload is an **HTML `<table>`** with CRLF line endings, not a real XLS/XLSX. Parse with an HTML table parser (`pandas.read_html`, lxml), not openpyxl/xlrd.

**Columns (19, exact):**
`Generic Name | Trade Name | Date Designated | Orphan Designation | Orphan Designation Status | Date Designation Withdrawn or Revoked | FDA Orphan Approval Status | Approved Labeled Indication | Marketing Approval Date | Exclusivity End Date | Exclusivity Protected Indication * (Shown for approvals from Jan. 1, 2013, to the present) | Sponsor Company | Sponsor Address 1 | Sponsor Address 2 | Sponsor City | Sponsor State | Sponsor Zip | Sponsor Country | CF Grid Key`

**`CF Grid Key` is a stable integer primary key** — use it as the diff key. Example newest rows: `progranulin replacement therapy / 08/03/2026 / treatment of frontotemporal dementia / Denali Therapeutics / key 892822`; `bispecific ADC anti-MUC1/HER3 / 08/05/2026 / small cell lung cancer / Xadcera Biopharmaceutical (Suzhou) / key 1139626`.

**Incremental pull (VERIFIED):** setting `Designation_Start_Date=07/01/2026&Designation_End_Date=08/05/2026` returned **36 designations**, 39,090 bytes. Poll this daily — it is the cheapest competitor-filing tripwire on FDA's estate.

**Other gotchas:**
- `GET` on `OOPD_Results.cfm` returns **503**. POST only.
- Sponsor Zip is wrapped in literal quote-space padding: `"' 94080 '"`.
- Akamai bot management is active (`_abck`, `bm_sz` cookies). Send a real browser UA and a `Referer`; a bare curl UA may be challenged.
- No RPD field. No fast-track field. Orphan only.

**Related official pages:** `.../public-identification-orphan-drug-designation`, `.../orphan-drug-designation-disease-considerations`, `.../clinical-superiority-findings`, `.../orphan-drug-act-relevant-excerpts` — all under `https://www.fda.gov/industry/designating-orphan-product-drugs-and-biological-products/`.

**FDA-TRACK OOPD dashboard** (workload metrics, incl. an *RPD PRV Measures* section with request counts — aggregate only, no drug names):
- Page: `https://www.fda.gov/about-fda/fda-track-agency-wide-program-performance/fda-track-office-chief-medical-officer-office-orphan-products-development-dashboard` — VERIFIED 200, current as of 03/31/2026
- **Dataset (XLSX): `https://www.fda.gov/media/192479/download?attachment`** — **VERIFIED 200, xlsx, 28,531 bytes**

---

## 5. openFDA APIs

**Base:** `https://api.fda.gov` — HTTPS only, HTTP is rejected.
**Auth:** API key optional but strongly recommended. Pass as `?api_key=…` (place **before** `search=`) or as HTTP Basic username. Key signup: `https://open.fda.gov/apis/authentication/` — **VERIFIED 200**.

**Rate limits (VERIFIED, quoted from the authentication page):**
| | per minute | per day |
|---|---|---|
| No key | 240 / IP | **1,000 / IP** |
| With key | 240 / key | **120,000 / key** |

**Query params:** `search`, `sort`, `count`, `limit`, `skip`, `search_after`. Docs: `https://open.fda.gov/apis/query-parameters/` — VERIFIED 200.

**Hard limits (VERIFIED by triggering the errors):**
- `limit` max **1000** → `"Limit cannot exceed 1000 results for search requests. Use the skip or search_after param…"`
- `skip` max **25000** → `"Skip value must 25000 or less."` (applies even with a `search` filter)
- `search_after` exists but is arity-sensitive: `search_after=ANDA040012` with `sort=application_number:asc` returns `[illegal_argument_exception] search_after has 1 value(s) but sort has 2`. **For full-corpus extraction, use the bulk downloads (below), not pagination.**
- Field-name suffix `.exact` works on some fields and 400s on others (e.g. `count=marketing_category.exact` fails; `count=marketing_category` works). Test per field.

### Drug endpoints — all **VERIFIED 200**, live counts as of 2026-08-05

| Endpoint | Records | Bulk file | Export date | Why it matters to you |
|---|---|---|---|---|
| `/drug/drugsfda.json` | **29,255** | `https://download.open.fda.gov/drug/drugsfda/drug-drugsfda-0001-of-0001.json.zip` (8.94 MB, **VERIFIED 200**) | 2026-08-05 | Application-level truth: sponsor, submissions, review priority, **orphan flag** |
| `/drug/label.json` | **261,420** | 14 parts, `drug-label-0001-of-0014.json.zip` … (~131 MB each) | 2026-08-05 | Full SPL text: `indications_and_usage`, `pediatric_use`, `clinical_studies` — primary evidence-mining surface |
| `/drug/ndc.json` | **136,765** | `drug-ndc-0001-of-0001.json.zip` (26.69 MB) | 2026-08-05 | `marketing_category` = the unapproved-drug detector (see §12) |
| `/drug/event.json` | **20,692,690** | 1,767 parts, quarterly-partitioned from 2004q3 | 2026-08-03 | FAERS safety signal / pediatric AE screening |
| `/drug/enforcement.json` | **17,860** | `drug-enforcement-0001-of-0001.json.zip` (3.80 MB) | 2026-08-04 | Recalls |
| `/drug/shortages.json` | **1,651** | `drug-shortages-0001-of-0001.json.zip` (0.43 MB, **VERIFIED 200**) | 2026-08-05 | Market-gap detection (see §9) |
| **`/drug/orangebook.json`** | **48,502** | `drug-orangebook-0001-of-0001.json.zip` (2.34 MB, **VERIFIED 200**) | 2026-08-05 | **Undocumented on the main API index but live** — Orange Book as JSON |

### Non-drug endpoints you will want

| Endpoint | Records | Note |
|---|---|---|
| **`/transparency/crl.json`** | **457** | **Complete Response Letters, full OCR text.** Fields: `letter_date`, `letter_year`, `letter_type`, `approval_status`, `application_number[]`, `company_name`, `company_rep`, `text`. **VERIFIED 200.** Directly tells you why competitor applications failed. Bulk: `https://download.open.fda.gov/transparency/crl/transparency-crl-0001-of-0001.json.zip` (**VERIFIED 200**) |
| `/other/nsde.json` | 664,966 | NDC SPL Data Elements, 3 parts |
| `/other/unii.json` | 175,453 | Substance identifiers |
| `/other/substance.json` | 167,385 | GSRS substance records (316.93 MB) |

### The bulk download harness

**`https://api.fda.gov/download.json`** — **VERIFIED 200, application/json, 589,240 bytes.** This is the master manifest for every openFDA dataset: per-endpoint `export_date`, `total_records`, and a `partitions[]` array of `{file, size_mb, records, display_name}`.

**GOTCHA:** `https://download.open.fda.gov/download.json` returns **403**. The manifest lives on `api.fda.gov`, not the download host. The *files* live on `download.open.fda.gov`.

**Recommended harness:** poll `api.fda.gov/download.json` daily, diff `export_date` per endpoint, re-pull only changed partitions. This entirely sidesteps the 25,000-skip pagination cap.

### Key fields for your use case (verified against a live record, NDA021825 / FERRIPROX)

```
application_number                                    "NDA021825"
sponsor_name                                          "CHIESI"
submissions[].submission_type                         "ORIG" | "SUPPL"
submissions[].submission_status / _date               "AP" / "20210430"
submissions[].review_priority                         "PRIORITY" | "STANDARD" | "901 REQUIRED" | "901 ORDER" | "N/A" | "UNKNOWN"
submissions[].submission_class_code                   "EFFICACY" | "TYPE 1" | "TYPE 7" | ...
submissions[].submission_property_type[].code         "Orphan"        ← the ONLY value; 856 occurrences corpus-wide
submissions[].application_docs[].url                  → accessdata PDF (label / letter / review)
products[].marketing_status                           Prescription | Over-the-counter | Discontinued | None (Tentative Approval) | For Further Manufacturing Use
products[].te_code, reference_drug, reference_standard
openfda.*                                             unii, rxcui, spl_set_id, pharm_class_epc/moa, substance_name
```

`review_priority` distribution corpus-wide: STANDARD 19,281 / UNKNOWN 1,958 / **PRIORITY 1,727** / N/A 985 / 901 REQUIRED 530 / 901 ORDER 13.

---

## 6. Drugs@FDA bulk data files

- **Landing page:** `https://www.fda.gov/drugs/drug-approvals-and-databases/drugsfda-data-files` — **VERIFIED 200**, "Content current as of: 08/05/2026", page states *"Updated: August 5th, 2026"*.
- **Direct ZIP:** **`https://www.fda.gov/media/89850/download?attachment`** — **VERIFIED 200, application/zip, 6,059,547 bytes.** (Also works without `?attachment`.)
- **Cadence:** page states the underlying database is **"updated each morning, Monday through Friday."** ZIP members carried timestamp `08-04-2026 14:30`.
- **Auth:** none. **Format:** ZIP of **tab-delimited** `.txt` (note: TAB here, unlike Orange Book's tilde).
- **Interactive UI:** `http://www.accessdata.fda.gov/scripts/cder/daf/index.cfm`
- **Monthly approval reports** (HTML, scrape-only): `https://www.accessdata.fda.gov/scripts/cder/daf/index.cfm?event=reportsSearch.process&rptName=1&reportSelectMonth=7&reportSelectYear=2026` — **VERIFIED 200**

**ZIP manifest (12 files, 43,100,877 bytes uncompressed) — VERIFIED:**

| File | Bytes | Header |
|---|---|---|
| `Applications.txt` | 779,512 | `ApplNo ApplType ApplPublicNotes SponsorName` |
| `Products.txt` | 4,632,263 | `ApplNo ProductNo Form Strength ReferenceDrug DrugName ActiveIngredient ReferenceStandard` |
| `Submissions.txt` | 9,322,366 | `ApplNo SubmissionClassCodeID SubmissionType SubmissionNo SubmissionStatus SubmissionStatusDate SubmissionsPublicNotes ReviewPriority` |
| `SubmissionPropertyType.txt` | 9,211,091 | ← **carries the `Orphan` flag** |
| `ApplicationDocs.txt` | 11,066,569 | links to label/letter/review PDFs |
| `MarketingStatus.txt` | 731,130 | + `MarketingStatus_Lookup.txt` (5 codes) |
| `TE.txt` | 452,577 | therapeutic equivalence |
| `Join_Submission_ActionTypes_Lookup.txt` | 6,899,193 | |
| `ActionTypes_Lookup.txt`, `ApplicationsDocsType_Lookup.txt`, `SubmissionClass_Lookup.txt` | small | |

**`SubmissionClass_Lookup.txt` — high-value codes for your screen (VERIFIED):**

| ID | Code | Description |
|---|---|---|
| 7 | TYPE 1 | New Molecular Entity ← **the RPD-PRV-eligible class** |
| 9 | TYPE 2 | New Active Ingredient |
| 12 | TYPE 3 | New Dosage Form |
| 14 | TYPE 4 | New Combination |
| 15 | TYPE 5 | New Formulation or New Manufacturer |
| 16 | TYPE 6 | New Indication (no longer used) |
| **17** | **TYPE 7** | **Drug Already Marketed without Approved NDA** ← unapproved-drug-to-NDA conversions; your 505(b)(2) precedent set |
| 22 | TYPE 10 | New Indication Submitted as Distinct NDA — Not Consolidated |
| 24 | TYPE 9 | New Indication Submitted as Distinct NDA, Consolidated after Approval |

Query `TYPE 7` + `TYPE 10` historically to build the empirical base rate for "repurposed/unapproved drug wins its own NDA."

---

## 7. Orange Book (Approved Drug Products with Therapeutic Equivalence Evaluations)

- **Landing page:** `https://www.fda.gov/drugs/drug-approvals-and-databases/orange-book-data-files` — **VERIFIED 200** (page metadata stale: "Content current as of: 02/14/2025", but the file itself is current)
- **Direct ZIP:** **`https://www.fda.gov/media/76860/download?attachment`** — **VERIFIED 200, application/zip, 1,091,413 bytes**
- **Cadence:** **monthly.** ZIP members timestamped `07-10-2026`. Cumulative annual edition + monthly supplements.
- **Auth:** none. **Format:** ZIP → 3 ASCII files, **tilde (`~`) delimited**.
- **Search UI:** `https://www.accessdata.fda.gov/scripts/cder/ob/index.cfm` — VERIFIED 200
- **JSON alternative:** `https://api.fda.gov/drug/orangebook.json` (48,502 records) / `https://download.open.fda.gov/drug/orangebook/drug-orangebook-0001-of-0001.json.zip` — **both VERIFIED 200**, export_date 2026-08-05 (fresher than the ZIP)
- **Appendices (PDF):** A `media/71494`, B `media/71502`, C `media/71523` (all `/download?attachment`)

**Schemas (VERIFIED headers):**
```
products.txt    (7,467,977 B)  Ingredient~DF;Route~Trade_Name~Applicant~Strength~Appl_Type~Appl_No~
                               Product_No~TE_Code~Approval_Date~RLD~RS~Type~Applicant_Full_Name
patent.txt      (1,223,277 B)  Appl_Type~Appl_No~Product_No~Patent_No~Patent_Expire_Date_Text~
                               Drug_Substance_Flag~Drug_Product_Flag~Patent_Use_Code~Delist_Flag~Submission_Date
exclusivity.txt (   75,337 B)  Appl_Type~Appl_No~Product_No~Exclusivity_Code~Exclusivity_Date
```

**Exclusivity code census — VERIFIED live counts, this is your competitive-moat map:**

| Code | n | Meaning |
|---|---|---|
| **ODE** | **605** (+90 `ODE*`) | **Orphan Drug Exclusivity — 7 yr. Your primary defensible asset on the 505(b)(2) leg.** e.g. `N~019569~001~ODE-267~Jun 28, 2026` |
| NCE | 423 | New Chemical Entity — 5 yr |
| **PED** | **339** | **Pediatric Exclusivity — +6 mo (BPCA § 505A)** |
| I | 221 | New indication / clinical-investigation — 3 yr |
| M | 193 | New indication (misc. 3-yr) |
| NPP | 159 | New patient population |
| NP | 130 | New product |
| PC | 56 | Patient/pediatric-related |
| **GAIN** | **44** | **QIDP-derived +5 yr — the only public trace of QIDP designation (see §14)** |
| CGT | 36 | Competitive Generic Therapy — 180 day |
| D, NS, W, RTO, NDF | 44 total | misc. |

**Gotcha:** `Approval_Date` for pre-1982 products is the literal string `"Approved prior to Jan 1, 1982"`, not a date. `Patent_Expire_Date_Text` is `MMM DD, YYYY`. Applicant names in `Applicant` are truncated to a 20-char key; use `Applicant_Full_Name`.

---

## 8. Purple Book (licensed biological products)

- **Search UI:** `https://purplebooksearch.fda.gov/` — **VERIFIED 200**
- **Downloads page:** `https://purplebooksearch.fda.gov/downloads` — **VERIFIED 200**
- **File URL pattern:**
  `https://www.accessdata.fda.gov/drugsatfda_docs/PurpleBook/{YYYY}/purplebook-search-{month}-data-download.{csv|xlsx}`
  **VERIFIED:** `.../2026/purplebook-search-july-data-download.csv` → **200, 476,652 bytes**; `.../2026/purplebook-search-june-…csv` → **200, 457,261 bytes**
- **Cadence:** **monthly**, back to 2020. Every month is retained → full historical time series is downloadable, no scraping needed.
- **Auth:** none. **Format:** CSV and XLSX.
- **Patent list (BPCIA § 351(l)(9)(C)):** `https://purplebooksearch.fda.gov/index.cfm?event=patentlist` — **VERIFIED 200** (HTML only)
- **FDA landing page:** `https://www.fda.gov/drugs/therapeutic-biologics-applications-bla/purple-book-lists-licensed-biological-products-reference-product-exclusivity-and-biosimilarity-or` — VERIFIED 200

**CSV structure — VERIFIED.** Rows 1–3 are a title banner (`"Purple Book Monthly Historical Data Changes Report - July 2026"`), a blank row, and a section label. **The real header is on row 4.** 28 columns:

`N/R/U | Applicant | BLA Number | Proprietary Name | Proper Name | License Type | Strength | Dosage Form | Route of Administration | Product Presentation | Marketing Status | Licensure | Approval Date | Inter. Approval Date | Ref. Product Proper Name | Ref. Product Proprietary Name | Supplement Number | Submission Type | Inter. Supplement Number | License Number | Product Number | Center | Date of First Licensure | Exclusivity Expiration Date | First Interchangeable Exclusivity Exp. Date | Ref. Product Exclusivity Exp. Date | **Orphan Exclusivity Exp. Date** | Patent List Provided`

**Gotchas:** (1) Skip 3 rows on parse. (2) File is **two stacked sections** — a monthly-delta block (N=newly approved / R=added in release / U=updated) followed by the **full snapshot**; deduplicate or you will double-count. (3) UTF-8 BOM present. (4) Month casing in the URL is inconsistent on the index page (`january` lowercase, `February`–`June` capitalized) but **the server is case-insensitive** — lowercase works for all.

---

## 9. NDC Directory + Structured Product Labeling (DailyMed)

### FDA NDC Directory

- **Landing:** `https://www.fda.gov/drugs/drug-approvals-and-databases/national-drug-code-directory` — **VERIFIED 200**, current as of 03/04/2026. **Cadence: daily.**
- **Search UI:** `https://www.accessdata.fda.gov/scripts/cder/ndc/` (`https://dps.fda.gov/ndc` **redirects** here — VERIFIED)
- **Bulk files — all VERIFIED 200, `application/x-zip-compressed`, no auth:**

| File | URL | Bytes |
|---|---|---|
| Text (product+package) | `https://www.accessdata.fda.gov/cder/ndctext.zip` | 10,734,240 |
| Excel | `https://www.accessdata.fda.gov/cder/ndcxls.zip` | 10,734,240 |
| Unfinished drugs / APIs | `https://www.accessdata.fda.gov/cder/ndc_unfinished.zip` | 3,462,876 |
| Compounded (503B outsourcing) | `https://www.accessdata.fda.gov/cder/compounders_ndc_directory.zip` | 400,128 |
| **Excluded drugs** | `https://www.accessdata.fda.gov/cder/ndc_excluded.zip` | **31,326,642** |

- Field definitions: `.../ndc-product-file-definitions` and `.../ndc-package-file-definitions`
- API: `https://api.fda.gov/drug/ndc.json` (136,765 records)
- **Support files page:** `https://www.fda.gov/drugs/drug-approvals-and-databases/national-drug-code-directory-support-files`

**Gotchas (from FDA's own page text):** an NDC is **not** an approval marker; the directory **excludes** animal drugs, blood products, contract-manufactured drugs, and kit-only/inner-layer products; entries appear only between marketing start and end dates (future start dates are suppressed); compounded products only if reported within 2 years. **NDC format changes to a uniform 12 digits effective March 7, 2033** — build the parser accordingly now.

### DailyMed (NLM) — the SPL source of truth

- **API v2 base:** `https://dailymed.nlm.nih.gov/dailymed/services/v2/` — **no auth, JSON or XML**
  - `spls.json?pagesize=N&page=N` — **VERIFIED 200**
  - `drugnames.json` — **VERIFIED 200**
  - `rxcuis.json` — **VERIFIED 200**
  - `spls/{setid}.xml` — **VERIFIED 200** (286 KB for a real setid)
  - `spls/{setid}/ndcs.json` — **VERIFIED 200**
  - `spls/{setid}/packaging.json` — **VERIFIED 200**
  - **GOTCHA: `spls/{setid}.json` returns HTTP 415.** Individual SPL detail is **XML-only**; the `.json` variants exist only for the sub-resources.
- **Bulk downloads:** `https://dailymed.nlm.nih.gov/dailymed/spl-resources-all-drug-labels.cfm` — **VERIFIED 200**
  - Full release, human Rx: `https://dailymed-data.nlm.nih.gov/public-release-files/dm_spl_release_human_rx_part{1..6}.zip`
  - Human OTC: `..._human_otc_part{1..11}.zip`; also `..._homeopathic.zip`, `..._animal.zip`, `..._remainder.zip`
  - **Daily:** `.../dm_spl_daily_update_MMDDYYYY.zip` (latest observed `08042026`)
  - **Weekly:** `.../dm_spl_weekly_update_MMDDYY_MMDDYY.zip` (latest `072726_073126`)
  - **Monthly:** `.../dm_spl_monthly_update_{mon}{yyyy}.zip` (latest `jul2026`)
  - FTP mirror: `ftp://public.nlm.nih.gov/nlmdata/.dailymed/…`
  - Mapping files: `https://dailymed.nlm.nih.gov/dailymed/app-support-mapping-files.cfm` — VERIFIED 200
- **Cadence:** daily / weekly / monthly increments over a full base release. Ingest full release once, then apply daily deltas.

---

## 10. Drug Shortages

- **API (best option):** `https://api.fda.gov/drug/shortages.json` — **VERIFIED 200**, `meta.last_updated = 2026-08-05`, **total = 1,651**. Bulk: `https://download.open.fda.gov/drug/shortages/drug-shortages-0001-of-0001.json.zip` — **VERIFIED 200**, 453,583 bytes.
- **Search UI:** `https://www.accessdata.fda.gov/scripts/drugshortages/default.cfm` — VERIFIED 200. **`https://dps.fda.gov/drugshortages` now 301-redirects here** (the standalone DPS shortage app is gone).
- **FDA hub page:** `https://www.fda.gov/drugs/drug-safety-and-availability/drug-shortages` — VERIFIED 200
- **Annual Report to Congress (PDF):** `https://www.fda.gov/media/193637/download` — **VERIFIED 200, PDF, 548,793 bytes** (2025 report)

**Record shape (VERIFIED live):**
```json
{"update_type":"Revised","initial_posting_date":"04/28/2023","package_ndc":"0338-0004-03",
 "generic_name":"Sterile Water Irrigant","contact_info":"888-229-0001",
 "availability":"Limited Availability","related_info":"Estimated recovery: August 2026",
 "openfda":{"application_number":["NDA017428"],"brand_name":[...],"manufacturer_name":[...],
            "product_ndc":[...],"substance_name":[...],"rxcui":[...],"spl_set_id":[...]}}
```

Filterable on `status` (e.g. `search=status:"Current"` — VERIFIED 200). The `openfda` join block gives you free linkage to Drugs@FDA / NDC / SPL.

**Gotchas:** `https://open.fda.gov/apis/drug/shortages/` returns **403** (docs page blocked/absent while the API itself works). `initial_posting_date` is `MM/DD/YYYY` strings, not ISO. The accessdata UI exposes **no** CSV/Excel export — link extraction found zero download hrefs. Use the API. Also note this is **CDER-only**; CBER biologic shortages are tracked separately and are not in this feed.

---

## 11. Guidance documents — there IS a structured feed

**The documented search page is `https://www.fda.gov/regulatory-information/search-fda-guidance-documents` (VERIFIED 200), but it is a Drupal view backed by a static JSON file.**

**Feed: `https://www.fda.gov/files/api/datatables/static/search-for-guidance.json`**
**VERIFIED 200, `application/json`, 3,661,797 bytes, 2,786 guidance records. No auth.**

(The in-page reference is `datatables-json/search-for-guidance.json`; that path itself 404s / redirects to page-not-found — **the working prefix is `/files/api/datatables/static/`**. Same prefix serves `warning-letters.json`, VERIFIED 200, 3,278,544 bytes.)

**Fields (16):** `title` (HTML `<a>` — parse out href+text), `field_issue_datetime` (MM/DD/YYYY), `field_issuing_office_taxonomy`, `field_health_topics`, `term_node_tid`, `field_topics`, `topics-product`, **`field_final_guidance_1`** (`Final`|`Draft`), `open-comment`, `field_comment_close_date`, **`field_docket_number`** (HTML `<a>` to regulations.gov), `field_communication_type`, `field_center`, `field_regulated_product_field`, `changed` (HTML `<time datetime=…>`), `field_associated_media_2`.

**Gotcha:** several fields contain **escaped HTML**, not plain text. `title` and `field_docket_number` must be un-escaped and regex-parsed. Diff on `changed` to detect new/revised guidances.

### The guidances that govern your program (all extracted from the live feed; landing pages VERIFIED 200)

| Topic | Guidance | Status / Issued | Docket | URL slug under `/regulatory-information/search-fda-guidance-documents/` |
|---|---|---|---|---|
| **RPD + PRV** | Rare Pediatric Disease Priority Review Vouchers | **Draft** 2019-07-30 (Rev 1) | FDA-2014-D-1461 | `rare-pediatric-disease-priority-review-vouchers` |
| Tropical PRV | Tropical Disease Priority Review Vouchers | Final 2016-10-06 | FDA-2008-D-0530 | `tropical-disease-priority-review-vouchers` |
| MCM PRV | Material Threat Medical Countermeasure PRVs | Draft 2018-01-19 | FDA-2017-D-6880 | `material-threat-medical-countermeasure-priority-review-vouchers-draft-guidance-industry` |
| **Orphan / pediatric subset** | Clarification of Orphan Designation of Drugs and Biologics for **Pediatric Subpopulations of Common Diseases** | Final 2017-12-19 | FDA-2017-D-6380 | `clarification-orphan-designation-drugs-and-biologics-pediatric-subpopulations-common-diseases` |
| Orphan sameness | Interpreting Sameness of **Monoclonal Antibody** Products Under the Orphan Drug Regs | Final 2014-04-01 | FDA-1999-D-0178 | `interpreting-sameness-monoclonal-antibody-products-under-orphan-drug-regulations` |
| Orphan sameness | Interpreting Sameness of **Gene Therapy** Products Under the Orphan Drug Regs | Final 2021-09-29 | FDA-2019-D-5392 | `interpreting-sameness-gene-therapy-products-under-orphan-drug-regulations` |
| OOPD meetings | Meetings with the Office of Orphan Products Development | Final 2015-07-09 | FDA-2014-D-0313 | `meetings-office-orphan-products-development` |
| Orphan e-submission | Providing Regulatory Submissions in Electronic Format — Orphan-Drug and HUD Designation Requests | Draft 2006-02-01 | FDA-2006-D-0159 | `providing-regulatory-submissions-electronic-format-orphan-drug-and-humanitarian-use-device` |
| **505(b)(2)** | **Determining Whether to Submit an ANDA or a 505(b)(2) Application** | **Final 2019-05-10** | FDA-2017-D-5974 | `determining-whether-submit-anda-or-505b2-application` |
| 505(b)(2) | Applications Covered by Section 505(b)(2) | **Draft 1999-12-08** (never finalized — 27 years) | FDA-1999-D-0738 | `applications-covered-section-505b2` |
| **Rare disease dev** | **Rare Diseases: Considerations for the Development of Drugs and Biological Products** | **Final 2023-12-26** | FDA-2015-D-2818 | `rare-diseases-considerations-development-drugs-and-biological-products` |
| **Pre-IND** | **Rare Diseases: Early Drug Development and the Role of Pre-IND Meetings** | Draft 2018-10-16 | FDA-2018-D-3268 | `rare-diseases-early-drug-development-and-role-pre-ind-meetings` |
| Natural history | Rare Diseases: Natural History Studies for Drug Development | Draft 2019-03-25 | FDA-2019-D-0481 | `rare-diseases-natural-history-studies-drug-development` |
| Rare enzyme defects | Slowly Progressive, Low-Prevalence Rare Diseases with Substrate Deposition … Single Enzyme Defects | Final 2018-07-27 | FDA-2018-D-2456 | `slowly-progressive-low-prevalence-rare-diseases-substrate-deposition-results-single-enzyme-defects` |
| Pediatric rare model | Pediatric Rare Diseases — A Collaborative Approach … Gaucher Disease as a Model | Draft 2017-12-07 | FDA-2017-N-6476 | `pediatric-rare-diseases-collaborative-approach-drug-development-using-gaucher-disease-model-draft` |
| **PREA** | **Pediatric Study Plans: Content of and Process for Submitting iPSPs and Amended iPSPs** | Final 2020-07-31 | FDA-2013-D-0814 | `pediatric-study-plans-content-and-process-submitting-initial-pediatric-study-plans-and-amended` |
| PREA/oncology | FDARA Implementation Guidance for Pediatric Studies of **Molecularly Targeted Oncology Drugs** (§ 505B) | Final 2021-05-24 | FDA-2019-D-4751 | `fdara-implementation-guidance-pediatric-studies-molecularly-targeted-oncology-drugs-amendments-sec` |
| Pediatric clin pharm | General Clinical Pharmacology Considerations for Pediatric Studies | Draft 2022-09-07 | FDA-2013-D-1275 | `general-clinical-pharmacology-considerations-pediatric-studies-drugs-including-biological-products` |
| **Meetings (Type A/B/C/D)** | **Formal Meetings Between the FDA and Sponsors or Applicants of PDUFA Products** | **Draft 2023-09-22** | FDA-2017-D-6530 | `formal-meetings-between-fda-and-sponsors-or-applicants-pdufa-products` |
| Expanded access | **Expanded Access to Investigational Drugs for Treatment Use: Q&A** | **Final 2026-04-15** | FDA-2013-D-0446 | `expanded-access-investigational-drugs-treatment-use-questions-and-answers` |
| Expanded access | Individual Patient Expanded Access Applications: Form FDA 3926 | Final 2017-10-03 | FDA-2015-D-0268 | `individual-patient-expanded-access-applications-form-fda-3926` |
| Expanded access | IRB Review of Individual Patient Expanded Access Submissions | Final 2023-09-11 | FDA-2023-D-3452 | `institutional-review-board-irb-review-individual-patient-expanded-access-submissions-investigational` |
| **QIDP** | **Qualified Infectious Disease Product Designation Q&A** | Final 2021-05-11 | FDA-2017-D-7001 | `qualified-infectious-disease-product-designation-questions-and-answers` |
| Gene therapy | Human Gene Therapy for Rare Diseases | Final 2020-01-28 | FDA-2018-D-2258 | `human-gene-therapy-rare-diseases` |
| n-of-1 ASO | IND Submissions for Individualized Antisense Oligonucleotide Drug Products … | Draft 2021-12-07 | FDA-2021-D-1139 | `investigational-new-drug-application-submissions-individualized-antisense-oligonucleotide-drug` |
| Accelerated approval | Accelerated Approval — Expedited Program for Serious Conditions | Draft 2024-12-05 | FDA-2024-D-2033 | `accelerated-approval-expedited-program-serious-conditions` |
| BTD | Considerations for Rescinding Breakthrough Therapy Designation | Draft 2022-06-24 | FDA-2021-D-1152 | `considerations-rescinding-breakthrough-therapy-designation` |

Curated rare-disease guidance index: `https://www.fda.gov/drugs/guidances-drugs/guidance-documents-rare-disease-drug-development` — VERIFIED 200.

---

## 12. Expanded access / compassionate use

**FDA publishes no per-patient or per-protocol expanded-access registry.** What exists:

| Source | URL | Status | Content |
|---|---|---|---|
| **ClinicalTrials.gov API v2** | `https://clinicaltrials.gov/api/v2/studies?filter.advanced=AREA[StudyType]EXPANDED_ACCESS&countTotal=true` | **VERIFIED 200** | **1,063 expanded-access records.** JSON, no auth. **This is the only structured, per-program EA dataset in existence.** Sponsors are required to register EA programs under FDAAA 801. |
| FDA EA hub (industry) | `https://www.fda.gov/news-events/expanded-access/expanded-access-information-industry` | VERIFIED 200 | Narrative only |
| CDER EA IND activity | `https://www.fda.gov/drugs/ind-activity/expanded-access-inds-and-protocols` | VERIFIED 200 | **Aggregate receipt counts only, and STALE — page "current as of 02/22/2021", reports end at 2020.** Dead branch. |
| CDER single-patient eIND | `https://www.fda.gov/about-fda/cder-offices-and-divisions/requesting-expanded-access-single-patient-emergency-eind-or-non-emergency-investigational-new-drug` | in sitemap | Process only |

**Dead:** `fda.gov/drugs/development-approval-process-drugs/expanded-access-information-patients-caregivers-and-health-care-professionals` → **404**.

---

## 13. Unapproved marketed drugs & "approved abroad, not in US"

### 13a. Marketed unapproved drugs — **no FDA list exists; build it from NDC `marketing_category`**

`https://www.fda.gov/drugs/enforcement-activities-fda/unapproved-drugs` — **VERIFIED 200** (current as of 2024-05-09). FDA's own page explicitly says: *"Drugs marketed in the U.S., with or without FDA approval, can be identified in the following databases"* — and then points to **NDC Directory, Drugs@FDA, Orange Book**. There is no roster.

**The CPG that used to define the enforcement program, *Marketed Unapproved Drugs — Compliance Policy Guide* (CPG 440.100), was WITHDRAWN in November 2020** and FDA's own page now links to it only via **web.archive.org**: `https://web.archive.org/web/20230531051554/https://www.fda.gov/regulatory-information/search-fda-guidance-documents/marketed-unapproved-drugs-compliance-policy-guide`. Treat as dead.

**The machine-readable substitute — `marketing_category` on `/drug/ndc.json`. VERIFIED live census (2026-08-05):**

| marketing_category | n | Interpretation |
|---|---|---|
| ANDA | 50,318 | generic, approved |
| OTC MONOGRAPH DRUG | 35,497 | monograph, not NDA |
| BULK INGREDIENT | 13,748 | API |
| **UNAPPROVED HOMEOPATHIC** | **13,646** | unapproved |
| NDA | 7,404 | approved |
| DRUG FOR FURTHER PROCESSING | 5,914 | |
| BLA | 4,079 | approved |
| **UNAPPROVED DRUG OTHER** | **2,202** | ← **your primary marketed-unapproved-drug pool; DESI leftovers and pre-1938 grandfathered claims live here** |
| BULK INGREDIENT FOR HUMAN Rx COMPOUNDING | 1,893 | |
| NDA AUTHORIZED GENERIC | 1,183 | |
| **UNAPPROVED MEDICAL GAS** | **289** | |
| OTC MONOGRAPH FINAL / NOT FINAL | 220 / 166 | |
| EXPORT ONLY | 140 | |
| **UNAPPROVED DRUG FOR USE IN DRUG SHORTAGE** | **63** | ← **these are literally drugs FDA is permitting because there is no approved US supply — highest-signal 505(b)(2)/TYPE-7 targets** |
| EMERGENCY USE AUTHORIZATION | 3 | |

Query: `https://api.fda.gov/drug/ndc.json?search=marketing_category:"UNAPPROVED+DRUG+OTHER"&limit=1000` (+ bulk file for full extraction). Cross-reference the DESI program page: `https://www.fda.gov/drugs/enforcement-activities-fda/drug-efficacy-study-implementation-desi`. Enforcement actions: `https://www.fda.gov/drugs/enforcement-activities-fda/fda-activities-remove-unapproved-drugs-market`.

### 13b. "Approved abroad but never in the US" — **FDA publishes NO such list. Confirmed absent.**

An 85,349-URL sitemap sweep found no list, dataset, or feed of foreign-approved-but-not-US drugs. FDA has no statutory duty to compile one. **Flag: this must be built by anti-join against non-FDA sources.**

**FDA-side "known US universe" (the join's right-hand side) — all verified above:** Drugs@FDA `Products.txt` `ActiveIngredient` ∪ Orange Book `products.txt` `Ingredient` ∪ Purple Book `Proper Name` ∪ openFDA `openfda.unii` / `substance_name`. Normalize on **UNII** via `https://api.fda.gov/other/unii.json` (175,453 records) or `https://download.open.fda.gov/other/unii/other-unii-0001-of-0001.json.zip` — UNII is the only identifier that survives salt/ester/tradename variance and is the same identifier FDA uses in § 360ff's "active moiety" analysis.

**Left-hand side is out of the FDA domain** (EMA EPAR/Article 57, Health Canada DPD, PMDA, TGA, MHRA, Swissmedic, WHO EML/INN, ATC). Note there is one FDA-side partial signal: the **`UNAPPROVED DRUG FOR USE IN DRUG SHORTAGE` (n=63)** NDC category plus FDA's temporary-importation shortage notices (e.g. `fda.gov/drugs/drug-shortages/october-31-2023-temporary-importation-available-physostigmine-injection`) — these are, by construction, foreign-approved products FDA has admitted because there is no approved US equivalent. Small but pre-qualified list.

---

## 14. Pre-IND / Type B meetings, and IND visibility

### Meeting process

- **Governing guidance:** *Formal Meetings Between the FDA and Sponsors or Applicants of PDUFA Products* — **Draft, 2023-09-22, docket FDA-2017-D-6530.** VERIFIED 200. Defines Type A / **Type B (pre-IND, end-of-Phase-1, end-of-Phase-2, pre-NDA/BLA)** / Type B (end-of-phase) / Type C / **Type D** (new, narrow-issue, 50-day) and INTERACT.
- **Rare-disease-specific:** *Rare Diseases: Early Drug Development and the Role of Pre-IND Meetings* — Draft 2018-10-16, FDA-2018-D-3268. VERIFIED 200.
- **Division-level pre-IND contacts** (in sitemap, VERIFIED): `fda.gov/about-fda/cder-offices-and-divisions/division-anti-infectives-dai-information-pre-ind-submissions`, `…/division-antivirals-dav-information-pre-ind-submissions`.
- **OOPD meetings guidance:** Final 2015-07-09, FDA-2014-D-0313.
- **Sequencing note (statutory):** because § 360ff(d)(2) forces the RPD request to be simultaneous with orphan or fast-track, your pre-IND meeting must precede the joint orphan+RPD filing, not follow it.

### **CONFIRMED: INDs are not public.**

**21 CFR § 312.130(a)**, retrieved live from the eCFR API (`https://www.ecfr.gov/api/versioner/v1/full/2026-01-01/title-21.xml?part=312&section=312.130` — **VERIFIED 200**):

> **"(a) The existence of an investigational new drug application will not be disclosed by FDA unless it has previously been publicly disclosed or acknowledged."**

§ 312.130(b) routes drug-IND content confidentiality to **§ 314.430** and biologic-IND content to **§§ 601.50–601.51**. § 312.130(c) permits disclosure of an IND safety report only to the individual patient it concerns. § 312.130(d) sends § 50.24 exception-from-informed-consent material through FOIA.

**Therefore:** IND filings, IND numbers, pre-IND meeting requests, meeting minutes, designation requests, and designation grants are all **non-public unless the sponsor discloses them**. There is no FDA endpoint to diff. Competitor IND intelligence must come from **ClinicalTrials.gov registration** (the first mandatory public event), SEC filings, and press releases.

**eCFR API** is the right tool for regulatory text generally: `https://www.ecfr.gov/api/versioner/v1/full/{date}/title-21.xml?part=NNN[&section=NNN.NNN]` and `.../structure/{date}/title-21.json` (VERIFIED 200, 2.68 MB). No auth, XML/JSON, versioned by date — so you can diff regulations over time. Relevant parts: **21 CFR 312** (IND), **314** (NDA incl. 505(b)(2), § 314.3 active moiety, § 314.430 confidentiality), **316** (orphan designation/exclusivity), **320** (BA/BE), **601** (BLA).

---

## 15. Designation lists that CAN be diffed over time (competitor-filing detection)

| Designation | Public? | Machine-readable source | Diff key | Cadence | Verdict |
|---|---|---|---|---|---|
| **Orphan Drug** | **YES — full corpus** | OOPD POST-Excel export (§4), 8,190 records | `CF Grid Key` | **daily** | **BEST SIGNAL. Poll daily with a 30-day date window.** |
| **RPD** | **NO** | none — statutorily non-published | — | — | **Impossible from FDA. Proxy = new orphan designation on a pediatric-onset serious disease (statutorily co-filed).** |
| **PRV awarded** | **YES** | Federal Register API, `Issuance of Priority Review Voucher; …` (§3) | `document_number` | daily | **Excellent — mandated by § 360ff(f)(1)(A).** RPD n=73, MCM n=9. Tropical **not** published. |
| **PRV redeemed** | **YES** | Federal Register API, `Notice of Approval of Product Under Voucher…` | `document_number` | daily | Good, n=32, but only from 2019 forward. |
| **PRV transfers/sales** | **NO** | — | — | — | § 360ff(b)(2)(B) requires the transferee to notify FDA within 30 days, but **FDA publishes nothing.** Track via 8-K / press. |
| **Fast Track** | **designations NO; approvals YES** | `https://www.fda.gov/drugs/nda-and-bla-approvals/fast-track-approvals` (HTML); `https://www.fda.gov/drugs/ind-activity/fast-track-designation-requests` (aggregate counts) | — | irregular | **Approval-stage only — years too late for competitive intel. HTML-scrape.** |
| **Breakthrough Therapy** | **designations NO; approvals YES** | `https://www.fda.gov/drugs/nda-and-bla-approvals/breakthrough-therapy-approvals` — **VERIFIED 200**; CBER: `.../fdasia/cber-approvals-breakthrough-therapy-designated-drugs`; rescissions: `.../cder-breakthrough-therapy-designation-withdrawn-after-granting-wag-and-rescinded` | — | irregular | Approval-stage only. HTML-scrape. Note the **rescinded/WAG** pages are the only negative signal FDA publishes. |
| **QIDP** | **NO designation list** | **Sitemap grep for `qualified-infectious` across all 85,349 fda.gov URLs → 0 non-guidance hits.** Only public trace: **Orange Book `exclusivity.txt` code `GAIN` (n=44)** — appears only after approval. | `Appl_No~Product_No~GAIN` | monthly | Post-approval only. |
| **RMAT** | aggregate + negatives only | `.../cellular-gene-therapy-products/cumulative-cber-regenerative-medicine-advanced-therapy-rmat-designation-requests-received-fiscal`; `.../cber-regenerative-medicine-advanced-therapy-rmat-designations-withdrawn-after-granting-or-rescinded` | — | quarterly | Counts + rescissions. |
| **Orphan exclusivity clock** | **YES** | Orange Book `exclusivity.txt` `ODE-nnn` (605 + 90 `ODE*`); Purple Book `Orphan Exclusivity Exp. Date`; OOPD export `Exclusivity End Date` | `Appl_No~Product_No~Code` | monthly / daily | **Three independent sources — reconcile them.** |
| **Pediatric exclusivity** | **YES** | Orange Book `PED` (n=339); statistics XLSX `https://www.fda.gov/media/119732/download?attachment` — **VERIFIED 200, xls, 39,424 B** | | monthly | |
| **Pediatric labeling changes (PREA/BPCA outcomes)** | **YES — spreadsheets** | `https://www.fda.gov/media/175738/download?attachment` (**VERIFIED 200, xlsx, 396,434 B**) and Pediatric Descriptors `https://www.fda.gov/media/175739/download?attachment` (**VERIFIED 200, xlsx, 612,306 B**); page `https://www.fda.gov/science-research/pediatrics/pediatric-labeling-changes` | | irregular | **Best structured PREA/BPCA outcome dataset.** |
| **Orphan submission flag** | **YES** | openFDA `drugsfda` `submissions[].submission_property_type[].code == "Orphan"` — **856 corpus-wide, sole value** | `application_number+submission_number` | daily | Confirms orphan status at the *submission* level. |
| **Complete Response Letters** | **YES (new)** | `https://api.fda.gov/transparency/crl.json` — 457 records with full text | `file_name` | ~daily | **Underused. Read competitors' failure reasons verbatim.** |
| **Rare disease approvals (curated)** | HTML only | `https://www.fda.gov/about-fda/accelerating-rare-disease-cures-arc-program/rare-disease-drug-approvals` — VERIFIED 200 | — | ad hoc | **Scrape-only, no file.** Curated "select" approvals 2021–2026. |
| **CNPV (Commissioner's voucher)** | press releases only | `https://www.fda.gov/industry/commissioners-national-priority-voucher-cnpv-pilot-program` | — | ad hoc | New program, no FR ledger. |

**Recommended tripwire stack (daily cron, ~4 requests):**
1. `POST` OOPD Excel export, window = last 45 days → diff on `CF Grid Key` → alert on any new designation whose indication text matches your pediatric-serious-disease ontology.
2. `GET` Federal Register API, `conditions[term]="priority review voucher"`, `conditions[publication_date][gte]=T-7` → regex titles for issuance/redemption.
3. `GET` `https://api.fda.gov/download.json` → diff `export_date` per endpoint → trigger re-pull.
4. `GET` `https://www.fda.gov/files/api/datatables/static/search-for-guidance.json` → diff on `changed` → alert on new/revised rare-disease, pediatric, or PRV guidance (watch specifically for the RPD PRV draft finally going Final).

---

## 16. Status ledger — dead, moved, and scrape-only

**DEAD (404) — do not put these in your config:**
```
fda.gov/industry/designating-orphan-product-drugs-and-biological-products/rare-pediatric-disease-designation-and-voucher-programs
fda.gov/about-fda/center-drug-evaluation-and-research-cder/tropical-disease-priority-review-vouchers
fda.gov/about-fda/center-drug-evaluation-and-research-cder/material-threat-medical-countermeasure-priority-review-vouchers
fda.gov/drugs/development-resources/tropical-disease-priority-review-vouchers
fda.gov/drugs/development-approval-process-drugs/drug-shortages
fda.gov/drugs/drug-shortages/drug-shortages-api
fda.gov/drugs/guidance-compliance-regulatory-information/unapproved-drugs
fda.gov/drugs/enforcement-activities-fda/marketed-unapproved-drugs-compliance-guide   (CPG withdrawn Nov 2020; archive.org only)
fda.gov/drugs/nda-and-bla-approvals/cder-breakthrough-therapy-designation-approvals
fda.gov/drugs/development-resources/qualified-infectious-disease-product-designation-questions-and-answers
fda.gov/drugs/development-approval-process-drugs/expanded-access-information-patients-caregivers-and-health-care-professionals
fda.gov/drugs/development-approval-process-drugs/drug-and-biologic-approval-and-ind-activity-reports
fda.gov/media/163636/download
fda.gov/media/110805/download
fda.gov/datatables-json/search-for-guidance.json           (and /files/api/datatables-json/…)
download.open.fda.gov/download.json                        (403 — manifest is on api.fda.gov)
open.fda.gov/apis/drug/shortages/                          (403 — API itself works)
```

**MOVED / REDIRECTS:**
```
dps.fda.gov/drugshortages  →  accessdata.fda.gov/scripts/drugshortages/   (301)
dps.fda.gov/ndc            →  accessdata.fda.gov/scripts/cder/ndc/         (301)
```

**HTML-SCRAPE-ONLY (no API, no file) — budget for brittle parsers:**
- Tropical Disease PRV qualifying-disease list
- ARC "Rare Disease Drug Approvals" curated list
- Fast Track Approvals / Breakthrough Therapy Approvals / CBER BTD lists / RMAT withdrawn-rescinded lists
- Purple Book Patent List (`index.cfm?event=patentlist`)
- Drugs@FDA monthly approval reports (`daf/index.cfm?event=reportsSearch.process`)
- CDER IND activity / receipts pages (and EA IND page is stale to 2021)
- OOPD Excel export (an HTML table masquerading as `.xls`)

**INFRASTRUCTURE GOTCHAS:**
- `www.fda.gov` and `accessdata.fda.gov` sit behind **Akamai bot manager** (`_abck`, `bm_sz`, `AWSALB` cookies). WebFetch-style default UAs get **404s on pages that curl-with-browser-UA fetches at 200** — this was reproduced live on the RPD program page. **Always send a realistic browser User-Agent and, for POSTs, a matching `Referer`.**
- `accessdata.fda.gov` is ColdFusion on IIS; several endpoints are POST-only and return **503** on GET.
- FDA content pages carry a `Content current as of:` date that is frequently **stale relative to the file they link** (Orange Book page says 2025-02-14; its ZIP is 2026-07-10). **Trust the file's `Last-Modified` / internal timestamps, never the page.**
- Site inventory for discovery: `https://www.fda.gov/sitemap.xml` → 43 child sitemaps (`?page=1..43`) → **85,349 URLs**, `lastmod` 2026-08-05. Cheapest way to detect FDA page moves before your scrapers break.agentId: ad1577f28149d517a (use SendMessage with to: 'ad1577f28149d517a', summary: '<5-10 word recap>' to continue this agent)
<usage>subagent_tokens: 238790
tool_uses: 71
duration_ms: 1468201</usage>