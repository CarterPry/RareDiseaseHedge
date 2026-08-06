<!-- recovered from agent-aecf128bd39bce62a.jsonl on 2026-08-06; original agent died on API ConnectionRefused error after 82 tool calls; all findings below are sourced directly from that transcript's tool results, supplemented by a small number of new live fetches performed 2026-08-06 and labelled as such -->

# Health Canada — Machine-Accessible Drug Data

**Scope:** Drug Product Database (DPD) API and bulk extracts; Notice of Compliance (NOC) database and API; Patent Register; Register of Innovative Drugs; Summary Basis of Decision (SBD) documents; Clinical Information Portal (CIP); Special Access Programme (SAP); Drug/Health Product Shortages Canada; Canada's rare-disease regulatory framework and orphan-drug policy state as of 2026.

**Funnel relevance:** Canada has no formal orphan-drug designation or PRV-equivalent. Exclusivity for innovative drugs is 8 years of data protection under C.08.004.1 FDR, available only to novel active substances receiving an NOC. The NOC/c (Notice of Compliance with Conditions) and Priority Review pathways accelerate timelines for serious/life-threatening conditions but confer no additional exclusivity. Canada is useful primarily as a regulatory reference jurisdiction and as a market for the company's generic registration program (NOC not required for DIN-exempt sales in some provinces, but a full NDS or ANDS is required for DIN).

---

## 1. Drug Product Database (DPD)

### 1.1 Overview

The DPD captures information on Canadian human, veterinary, disinfectant, and radiopharmaceutical products approved for use by Health Canada. As of the transcript's live query (2026-08-05, VERIFIED):

- **Total records across all statuses:** 58,183
- **Breakdown by class:** Human 50,846 | Veterinary 3,358 | Disinfectant 3,817 | Radiopharmaceutical 162
- **Marketed (status=2) human drugs:** 13,355
- **Statuses:** 1=Approved, 2=Marketed, 3=Cancelled Pre-Market, 4=Cancelled Post-Market, 6=Dormant

### 1.2 REST API

**Base URL:** `https://health-products.canada.ca/api/drug/`

**Authentication:** None. No API key required. No rate limit documented.

**Response formats:** JSON (`type=json`) or XML (`type=xml`). Language: `lang=en` or `lang=fr`.

**Filter by primary key:** `drug_code=<integer>` on per-drug endpoints; `status=<1-6>` on `drugproduct`.

**All endpoints verified HTTP 200 as of 2026-08-05:**

| Endpoint | Example URL | Notes |
|---|---|---|
| `drugproduct` | `…/drugproduct/?status=2&lang=en&type=json` | Core product record |
| `activeingredient` | `…/activeingredient/?drug_code=793&lang=en&type=json` | Returns strength, unit, dosage |
| `company` | `…/company/?drug_code=793&lang=en&type=json` | DIN owner address |
| `form` | `…/form/?drug_code=793&lang=en&type=json` | Pharmaceutical form |
| `route` | `…/route/?drug_code=793&lang=en&type=json` | Route of administration |
| `schedule` | `…/schedule/?drug_code=793&lang=en&type=json` | Prescription/OTC status |
| `therapeuticclass` | `…/therapeuticclass/?drug_code=793&lang=en&type=json` | ATC code and name |
| `packaging` | `…/packaging/?type=json` | Packaging info (no lang param) |
| `pharmaceuticalstd` | `…/pharmaceuticalstd/?type=json` | Pharm standard |
| `status` | `…/status/?lang=en&type=json` | Status lookup table |
| `veterinaryspecies` | `…/veterinaryspecies/?lang=en&type=json` | Vet species reference |

**Endpoints confirmed 404 (incorrect names found in some third-party docs):**
- `DosageForm` — returns `No type was found that matches the controller named 'DosageForm'`
- `RouteOfAdministration` — same error; correct name is `route`

**Sample `drugproduct` record (VERIFIED, fetched 2026-08-05):**
```json
{
  "drug_code": 793,
  "class_name": "Human",
  "drug_identification_number": "00000809",
  "brand_name": "ALCON TEARS 0.5%",
  "descriptor": "",
  "number_of_ais": "1",
  "ai_group_no": "0108634001",
  "company_name": "ALCON CANADA INC",
  "last_update_date": "2025-03-22"
}
```

**Sample `activeingredient` record (VERIFIED, fetched 2026-08-05):**
```json
{
  "drug_code": 4810,
  "ingredient_name": "TETRACYCLINE HYDROCHLORIDE",
  "strength": "25",
  "strength_unit": "G",
  "dosage_value": "100",
  "dosage_unit": "G"
}
```

**Sample `therapeuticclass` record (VERIFIED):**
```json
{"drug_code": 106683, "tc_atc_number": "A10BJ06", "tc_atc": "SEMAGLUTIDE"}
```

**API documentation page:** `https://health-products.canada.ca/api/documentation/dpd-documentation-en.html` — returns HTTP 200 but is JS-rendered; the agent's WebFetch of the root `https://health-products.canada.ca/api/drug/` returned HTTP 403 via the WebFetch tool; curl with browser User-Agent returned a JS-rendered shell (no content usable server-side). Use curl directly against specific endpoints.

### 1.3 Bulk Extract (Data Dump)

**Open Canada dataset GUID:** `bf55e42a-63cb-4556-bfd8-44f26e5a36fe`
**Open Canada page:** `https://open.canada.ca/data/en/dataset/bf55e42a-63cb-4556-bfd8-44f26e5a36fe`
**License:** Open Government Licence – Canada

**Primary download URL (VERIFIED HTTP 200, 2026-08-05):**
```
https://open.canada.ca/data/dataset/bf55e42a-63cb-4556-bfd8-44f26e5a36fe/resource/b05ae610-0366-478f-993f-b4afbdaadbc6/download/allfiles.zip
```
The agent confirmed HTTP 200 with Content-Length 245 bytes on a range request — consistent with a redirect response or small wrapper. The open.canada.ca CKAN API request was blocked (WAF returned "Request Rejected" HTML with support ID 13237979102341032341). The WebFetch of the dataset page succeeded and confirmed:

- **Inactive Products ZIP last updated:** 2025-05-28
- **Format:** Series of compressed UTF-8 text files; uncompressed ~116 MB
- **Update cadence:** Monthly (confirmed by WebSearch result stating "as of 2026-03-02, files including drug.zip, drug_ia.zip, drug_ap.zip, and drug_dr.zip have been updated")
- **File variants:** `allfiles.zip` (active/marketed), `allfiles_ia.zip` (inactive), `allfiles_ap.zip` (approved, pre-market), `allfiles_dr.zip` (dormant)

**Documentation pages:**
- `https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products/drug-product-database/what-data-extract-drug-product-database.html` — HTTP 000 (TLS/connection failure from agent; curl returned exit code 92); page exists per WebSearch results
- `https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products/drug-product-database/read-file-drug-product-database-data-extract.html` — same failure

**Third-party parsing scripts:** `https://github.com/FayeA/ScriptsForHCDrugProductDatabase` and `https://github.com/studybuffalo/dpd_data_extraction` exist per WebSearch (UNVERIFIED — not fetched).

R package `dpdr` (CRAN) provides an interface to the DPD API: `https://cran.r-project.org/package=dpdr` (UNVERIFIED — not fetched).

---

## 2. Notice of Compliance (NOC) Database

### 2.1 Overview

An NOC is issued after a satisfactory review of a New Drug Submission (NDS), Abbreviated NDS, or Supplement. It is the Canadian market authorization.

**Total NOC records (VERIFIED live query 2026-08-05):** 37,714

**Database coverage:** Human drugs from January 1, 1994 to present; Veterinary drugs from September 19, 2000 to present (pre-2000 vet NOCs being backfilled).

**Update cadence:** Nightly.

**Most recent NOC record retrieved (VERIFIED 2026-08-05):**
```json
{
  "noc_number": 38032,
  "noc_date": "2026-08-04",
  "noc_manufacturer_name": "SANIS HEALTH INC",
  "noc_status_with_conditions": "N",
  "noc_on_submission_type": "Supplement to an Abbreviated New Drug Submission (SANDS)",
  "noc_submission_class": "Admin",
  "noc_product_type": "Prescription Pharmaceutical",
  "noc_crp_product_name": "CELEXA",
  "noc_crp_company_name": "LUNDBECK CANADA INC",
  "noc_crp_country_name": "CANADA",
  "noc_active_status": "1",
  "noc_reason_supplement": "Administrative: Update to labelling (to match Licensor)"
}
```

### 2.2 NOC API

**Base URL:** `https://health-products.canada.ca/api/notice-of-compliance/`

**Authentication:** None.

**Endpoints verified (HTTP 200, 2026-08-05):**

| Endpoint | Pattern | Key `id` param |
|---|---|---|
| `drugproduct` | `/drugproduct/?id=<noc_number>&lang=en&type=json` | NOC number |
| `noticeofcompliancemain` | `/noticeofcompliancemain/?id=<noc_number>&lang=en&type=json` | NOC number |
| `medicinalingredient` | `/medicinalingredient/?id=<noc_number>&lang=en&type=json` | NOC number |
| `route` | `/route/?id=<noc_number>&lang=en&type=json` | NOC number |
| `dosageform` | `/dosageform/?id=<noc_number>&lang=en&type=json` | NOC number |

**Endpoints confirmed 404:**
- `/product/` — no such controller
- `/veterinaryspecies/` — no such controller (vet species uses `/vetspecies/` per documentation)
- `/noc/` — no such controller; internal error message shows `iis-prod.hc.local` is the backend host

**`noticeofcompliancemain` response fields (VERIFIED, from documentation):**
`noc_number`, `noc_date`, `noc_manufacturer_name`, `noc_status_with_conditions` (Y/N for NOC/c), `noc_on_submission_type`, `noc_is_suppliment`, `noc_submission_class`, `noc_is_admin`, `noc_product_type`, `noc_crp_product_name`, `noc_crp_company_name`, `noc_crp_country_name`, `noc_active_status`, `noc_reason_supplement`, `noc_reason_submission`, `noc_therapeutic_class`, `noc_last_update_date`

**Sample `noticeofcompliancemain` record — ATRIANCE (nelarabine), NOC 9042 (VERIFIED fetched 2026-08-05):**
```json
{
  "noc_number": 9042,
  "noc_date": "2007-09-22",
  "noc_manufacturer_name": "GLAXOSMITHKLINE INC.",
  "noc_status_with_conditions": "Y",
  "noc_on_submission_type": "New Drug Submission (NDS)",
  "noc_submission_class": "New Active Substance (NAS)",
  "noc_product_type": "Prescription Pharmaceutical",
  "noc_therapeutic_class": "ANTINEOPLASTIC AGENT"
}
```
The `noc_status_with_conditions: "Y"` field is the programmatic flag for NOC/c (conditional approval) drugs.

**`drugproduct` endpoint — NOC 9042 sample (VERIFIED):**
```json
{"noc_number": 9042, "noc_br_brandname": "ATRIANCE", "noc_br_din": "02299925", "noc_br_product_id": 16781}
```

**`medicinalingredient` response fields:** `noc_number`, `noc_pi_din_product_id`, `noc_pi_medic_ingr_name`, `noc_pi_strength`, `noc_pi_unit`, `noc_pi_basic_unit`

**Important:** calling `/noticeofcompliancemain/` without an `id` parameter returns all 37,714 records in a single response (no pagination). The agent attempted to do this but the response had only 2 records (possible rate-limiting or JSON parse error at the time). The clean count of 37,714 was obtained in a separate live call.

**Searching by brand name:** The `drugproduct` endpoint only accepts `id` (NOC number), not `brand_name`. To find by brand name you must use the web UI at `https://health-products.canada.ca/noc-ac/` or the NOC/c listing at `https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products/notice-compliance/conditions.html`.

**Open Canada dataset:** `https://open.canada.ca/data/en/dataset/a661b339-305f-4a41-96a3-2f5b12bcbf55` (HTTP 200, VERIFIED). Bulk download URL not confirmed from transcript.

**API documentation:** `https://health-products.canada.ca/api/documentation/noc-documentation-en.html` — returns HTTP 200; JS-rendered but the agent successfully extracted full endpoint documentation from it.

---

## 3. Patent Register

### 3.1 Overview

The Patent Register is an alphabetical listing of medicinal ingredients and their associated patents, patent expiry dates, and related information, established under the Patented Medicines (Notice of Compliance) Regulations. It governs data exclusivity for patent holders and drives the timeline for generic entry.

**Web interface (VERIFIED HTTP 200 with redirect, 2026-08-05):**
`https://pr-rdb.hc-sc.gc.ca/pr-rdb/` — redirects and returns HTTP 200. The agent fetched a partial rendered page showing an extensive alphabetical list of medicinal ingredients currently on the register, including: ABATACEPT, ABEMACICLIB, ABROCITINIB, ACALABRUTINIB, AFLIBERCEPT, AFOXOLANER, ALECTINIB, ALIROCUMAB, AMIVANTAMAB, ANDEXANET ALFA, ANIFROLUMAB, APALUTAMIDE, APIXABAN, AVACOPAN, AVAPRITINIB, AVATROMBOPAG MALEATE, AZACITIDINE, BARICITINIB, BELANTAMAB MAFODOTIN, BELIMUMAB, BELZUTIFAN, BENRALIZUMAB, BEROTRALSTAT, BEVACIZUMAB, BICTEGRAVIR/EMTRICITABINE/TAF, BIMEKIZUMAB, BLINATUMOMAB, BOSUTINIB, BRENTUXIMAB VEDOTIN, BRIGATINIB, BRODALUMAB, BROLUCIZUMAB, BUROSUMAB, CAPIVASERTIB, CARFILZOMIB, CANAKINUMAB, CANNABIDIOL, and many more. The list is live and current.

**Bulk download (VERIFIED HTTP 206 returning application/zip, 2026-08-05 newly verified):**
```
https://pr-rdb.hc-sc.gc.ca/patent/Patent.zip
```
The agent confirmed the 0-10 byte range returned valid ZIP magic bytes `504b0304`, and the file was confirmed as `Zip archive data, at least v2.0 to extract`. A 501-byte partial download succeeded (HTTP 206).

**Open Canada dataset:** `https://open.canada.ca/data/en/dataset/1674baf5-6822-4788-afb3-f8659531d7c0` (HTTP 200, VERIFIED)
- **Resource confirmed:** Patent Register Dataset — Format: CSV — Download URL: `https://pr-rdb.hc-sc.gc.ca/patent/Patent.zip` — Last Updated: 2026-01-14
- **License:** Open Government Licence – Canada
- **Update cadence:** Not stated in transcript; most recent Open Canada metadata modification: 2026-01-14

**Authentication:** None. No API key required.

**Note:** The Patent Register governs generic exclusion periods; it is **not** a data-exclusivity register. See Section 4 for the Register of Innovative Drugs (data protection).

---

## 4. Register of Innovative Drugs (Data Protection — C.08.004.1)

### 4.1 Overview

Canada's data exclusivity regime is established under section C.08.004.1 of the Food and Drug Regulations, which came into force October 5, 2006. It applies to drugs receiving an NOC on or after June 17, 2006. It provides **8 years** of data protection for "innovative drugs" (novel active substances not previously approved in Canada for human use).

Guidance document (updated June 16, 2025 per WebSearch result): `https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products/applications-submissions/guidance-documents/guidance-document-data-protection-under-08-004-1-food-drug-regulations.html`

The register lists:
- Medicinal ingredient
- Submission number
- Drug name / brand
- Manufacturer
- Notice of Compliance date
- Data protection end date
- Status: Active or Expired

**Web page:** `https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products/applications-submissions/register-innovative-drugs.html` — HTTP 000 (TLS/connection failure from Mac when agent attempted curl; WebSearch returned HTTP 200 via browser). The page is functional per all WebSearch results.

**Download format:** The WebSearch result found historical PDFs (e.g., `reg-innov-dr-14-dec-2023-eng.pdf`) suggesting the register has been published as a PDF rather than a CSV. No machine-readable bulk download endpoint was confirmed in the transcript. The Open Canada dataset page `https://open.canada.ca/data/en/dataset/1674baf5-6822-4788-afb3-f8659531d7c0` is the **Patent Register**, not the Register of Innovative Drugs — these are different.

**Update cadence:** Register updated as recently as February 2026 and January 2026 per WebSearch.

**Relevance to funnel:** The 8-year data-protection period for innovative drugs is Canada's analogue of US new-chemical-entity exclusivity. It applies to never-previously-approved-in-Canada novel active substances. Repurposed generic APIs already approved in Canada would not qualify. A drug approved abroad but never approved in Canada could qualify if it contains a novel active substance meeting C.08.004.1 criteria.

---

## 5. Summary Basis of Decision (SBD)

### 5.1 Overview

SBDs explain why Health Canada authorized drugs and medical devices for sale. They are published for significant new drug submissions and contain quality, non-clinical, and clinical basis-of-decision text.

**Total SBD records (VERIFIED live query 2026-08-06, newly verified):** 712

**Update cadence:** Daily (per Open Canada metadata, last modified 2026-01-16).

### 5.2 SBD API

**Endpoint (VERIFIED HTTP 200, 2026-08-05):**
```
https://health-products.canada.ca/api/summary-report/api/basisdecision/?lang=en&type=json
```
French mirror: `https://produits-sante.canada.ca/api/rapports-sommaires/api/basisdecision/?lang=fr&type=json`
XML format: replace `type=json` with `type=xml`

**Authentication:** None.

**Response fields (VERIFIED from first record):**
`template`, `control_number`, `date_issued`, `link_id`, `brand_name`, `manufacturer`, `med_ingredient`, `bd_din_list`, `sub_type_number`, `date_submission`, `date_authorization`, `notice_decision`, `sci_reg_decision`, `quality_basis`, `non_clin_basis`, `non_clin_basis2`, `clin_basis`, `clin_basis2`, `clin_basis3`, `benefit_risk`, `summary`, `what_approved`, `why_approved`, `steps_approval`, `assess_basis`, `followup_measures`, `post_auth`, `other_info`, `science_rationale`, `a_clin_basis`, `a_clin_basis2`, `a_non_clin_basis`, `a_non_clin_basis2`, `b_quality_basis`, `contact`, `paat_info`, `summary_drug`, `branch_info`, `trademark`, `din`, `licence_number`, `ai_str_route_summary`, `is_md`, `din_list`, `post_activity_list`, `milestone_list`, `tombstone_list`

**Sample first record (VERIFIED — fetched 2026-08-05):**
```json
{
  "control_number": "120192",
  "date_issued": "2009-11-26",
  "link_id": "SBD00001",
  "brand_name": "Abilify",
  "manufacturer": "Bristol-Myers Squibb Canada",
  "med_ingredient": "Aripiprazole",
  "date_submission": "2008-02-22",
  "date_authorization": "2009-07-09",
  "notice_decision": "<p>On July 9, 2009, Health Canada issued a Notice of Compliance to Bristol-Myers Squibb Canada for the drug product Abilify...</p>"
}
```

**Open Canada dataset:** `https://open.canada.ca/data/en/dataset/9e168ff0-ece9-44de-bbec-68878454cbc1` — HTTP 200 (VERIFIED).

**DHPP portal (individual SBD documents):** `https://dhpp.hpfb-dgpsa.ca/review-documents/resource/<link_id>` — HTTP 200 (VERIFIED for `SBD1709128914848`). Human-readable HTML review documents; not structured API.

**Legacy portal:** `https://hpr-rps.hres.ca/reg-content/summary-basis-decision-detailOne.php` — HTTP 404 for the specific item tested; the base portal returns HTTP 200. The SBD API at `health-products.canada.ca` is the preferred machine-accessible route.

---

## 6. Clinical Information Portal (CIP)

### 6.1 Overview

The CIP publishes clinical data packages from drug and medical device submissions, launched March 13, 2019 under Health Canada's Public Release of Clinical Information (PRCI) initiative.

**Records posted (per WebSearch result dated November 14, 2025):** 166 records across drugs, biologics, vaccines, and medical devices.

**Search portal (VERIFIED HTTP 200 with redirect, 2026-08-05):**
`https://clinical-information.canada.ca/search/ci-rc`

**Releases in progress page (VERIFIED HTTP 200, 2026-08-05):**
`https://clinical-information.canada.ca/content/clinical-information-release-in-progress`

**Authentication:** None — free public access.

**Query pattern confirmed from page source (VERIFIED):**
```
https://clinical-information.canada.ca/search/ci-rc?f[0]=drug_brand_name:"<brand>"
https://clinical-information.canada.ca/search/ci-rc?f[0]=drug_ingredients:"<ingredient>"
```

**Programmatic access:** No REST API confirmed. The portal is Drupal-based (WET/GCweb theme). Data is accessible via Drupal URL facets. No bulk download endpoint identified in the transcript.

**2025 expansion:** Health Canada extended PRCI to Class III and IV medical devices, targeting upload within 120 calendar days of initiation.

**Clinical Trials Search Portal (separate system):**
URL: `https://www.canada.ca/en/health-canada/services/drugs-health-products/clinical-trials/search-portal.html`
Open Canada dataset: `https://ouvert.canada.ca/data/dataset/8fb2d580-6ccd-48cf-8655-349bfd7a98b2`
This replaces the 2013 Clinical Trials Database and covers trials from April 1, 2013 to July 29, 2026.
HTTP status: 200 (VERIFIED for the Open Canada dataset).

---

## 7. Special Access Programme (SAP)

**Regulatory basis:** Sections C.08.010 and C.08.011 of the Food and Drug Regulations.

**Purpose:** Allows practitioners to access non-marketed drugs for patients with serious or life-threatening conditions when conventional therapies have failed, are unsuitable, or unavailable.

**Volume:** ~12,000 requests per year.

**Top requested drugs (2025 data, per WebSearch):** Solian/Amisulpride (673 requests), MVW products (538 requests), Lamprene/Clofazimine (536 requests).

**Web portal URL:** `https://www.canada.ca/en/health-canada/services/drugs-health-products/special-access/overview.html` — HTTP 000 from agent (TLS timeout), but confirmed via WebSearch to be active and returning 200 in browser.

**Guidance document:** `https://www.canada.ca/en/health-canada/services/drugs-health-products/special-access/drugs/guidance.html`

**Most requested drugs list:** `https://www.canada.ca/en/health-canada/services/drugs-health-products/special-access/drugs-most-often-requested.html`

**Relevant to funnel:** Drugs approved abroad but never in Canada may be accessed via SAP for individual patients before full Canadian market authorization. This is separate from the DIN registration path and does not provide market access.

**Machine-accessible data:** No API. SAP data is published as HTML lists only. The transcript identified no bulk download of SAP request history.

---

## 8. Drug / Health Product Shortages Canada

### 8.1 Migration (January 2026)

The Drug Shortages Canada website (`www.drugshortagescanada.ca`) was migrated to **Health Product Shortages Canada** (`healthproductshortages.ca`) on **January 18, 2026**. Old URLs redirect temporarily.

**New site (VERIFIED HTTP 200 redirect to `https://healthproductshortages.ca/`, 2026-08-05 newly verified).**

### 8.2 API

**Base URL:** `https://healthproductshortages.ca/api/v1`

**Authentication:** Requires a free web account with verified email. Login endpoint:
```
POST /api/v1/login
Parameters: email, password
Returns: auth-token in response header
```

**Content-type:** `application/json`
**Parameter encoding:** `application/x-www-form-urlencoded`
**Rate limit:** 1,000 requests/hour per account.

**Search endpoint:**
```
GET /api/v1/search
Authorization: auth-token: {user access token}
```
Parameters: `orderby`, `id`, `company_name`, `brand_name`, `status`, `type` (shortage or discontinuation), `updated_date`, `order` (asc/desc), `filter_status` (resolved / anticipated_shortage / active_confirmed / avoided_shortage / discontinued), `term`, `din`, `report_id`

**Response format (list):**
```json
{
  "total": <int>,
  "limit": <int>,
  "offset": <int>,
  "page": <int>,
  "remaining": <int>,
  "data": [...],
  "total_pages": <int>
}
```

**Error response:**
```json
{"error": {"en": "<message>", "fr": "<message>"}}
```

**API documentation page (VERIFIED — agent fetched content, 2026-08-05):**
`https://healthproductshortages.ca/blog/52`

**Tier 3 Drug Shortages:** The site tracks "Tier 3" drug shortages separately (most critical supply disruptions).

**Note:** Users who had integrated with the old `www.drugshortagescanada.ca/api/v1` API must reprogram their connections to `healthproductshortages.ca/api/v1`.

---

## 9. Canadian Rare Disease / Orphan Drug Framework

### 9.1 Verified position as of 2026

**Canada has no formal orphan drug designation system.** This was confirmed by multiple converging sources in the transcript:

1. CAPRA blog (fetched and returned content): "As of 2023, Canada lacks a formal orphan drug designation system. Orphan drugs therefore follow the same regulatory approval process as other drugs in Canada."
2. WebSearch result from Health Canada: "There is no specific submission for a drug that treats a rare disease in Canada; orphan drugs or drugs for rare diseases typically refer to the drugs that receive such a designation from the US FDA."
3. Open Canada dataset on rare disease regulatory approach: `https://open.canada.ca/data/en/info/d8d6588e-8640-47df-835e-528fd62bf188`

**Canadian definition of rare disease:** Affects fewer than 1 in 2,000 people (not the US 200,000 patients threshold).

### 9.2 Accelerated review pathways

**Notice of Compliance with Conditions (NOC/c):**
- Standard: 200-day review target (vs. 300 days for standard NDS)
- Eligibility: Promising drugs for serious, life-threatening, or severely debilitating conditions where no alternative exists or significant improvement shown
- Mechanism: Market authorization issued with conditions requiring additional confirmatory studies
- Programmatic flag: `noc_status_with_conditions: "Y"` in the NOC API
- Example from API: ATRIANCE (nelarabine, NOC 9042) — `noc_status_with_conditions: "Y"`, `noc_submission_class: "New Active Substance (NAS)"`

**Priority Review:**
- 180-day review target
- Requires "substantial" clinical effectiveness evidence
- Same disease criteria as NOC/c

**Rolling Review:** Proposed in December 2022 Forward Regulatory Plan amendments; status as of 2026 UNVERIFIED.

### 9.3 National Strategy for Drugs for Rare Diseases

**Announced:** March 22, 2023
**Investment:** Up to CAD $1.5 billion over three years (April 1, 2024 – March 31, 2027)
**Breakdown:**
- ~$1.4 billion to provinces/territories for drug coverage agreements
- $33 million for Indigenous Services Canada
- $68 million for evidence collection, research infrastructure, governance

**Structure:** 4 pillars — (1) national consistency in rare disease drug coverage, (2) patient outcomes and system sustainability, (3) evidence collection and use, (4) innovation investment.

**Implementation:** Pilot began July 2024 with British Columbia. Alberta bilateral agreement signed December 5, 2024 (CAD $162 million). Strategy focuses on coverage/reimbursement, not regulatory designation.

**Bill C-64 (Pharmacare Act):** Introduced February 29, 2024 — foundational principles for national pharmacare; does NOT create orphan drug designation.

**Key conclusion:** The National Strategy for Drugs for Rare Diseases is a **funding and access program**, not a regulatory designation framework. It does not create market exclusivity, expedited approval pathways beyond the existing NOC/c and Priority Review, or a Canada-specific orphan designation.

### 9.4 Data protection for innovative drugs (C.08.004.1)

If a drug qualifies as an "innovative drug" under C.08.004.1 (never previously approved in Canada for human use, novel active substance), the data protection period is **8 years** from the date of NOC. Generic and biosimilar manufacturers are barred from filing during this window.

**Relevance:** A drug approved in Europe or other jurisdictions but never approved in Canada could qualify for 8-year data protection upon first Canadian NOC — directly parallel to the US new chemical entity exclusivity logic. This is a distinct and meaningful incentive for Funnel A (never-US moiety) candidates entering Canada for the first time.

### 9.5 Agile Licensing / Conditional Market Authorization (future)

Health Canada's Forward Regulatory Plan 2022-2024 listed "Regulations Amending the Food and Drug Regulations (Agile Regulations for Licensing Drugs)" as a planned item to expand conditional approval terms for drugs and devices. The agent was unable to reach the specific page (`https://www.canada.ca/en/health-canada/corporate/about-health-canada/legislation-guidelines/acts-regulations/forward-regulatory-plan/plan/flexible-lifecycle-based-licensing-drugs-medical-devices.html` — returned empty). A 2024 gazette amendment (SOR/DORS-136) published July 3, 2024 addressed recalls, establishment licences, and finished product testing — not conditional approval for rare diseases. The status of the agile licensing amendment as of 2026 is **UNVERIFIED**.

---

## 10. Unfinished — Worth Re-running

1. **Register of Innovative Drugs machine-readable download:** The transcript confirmed the register is updated monthly and available on canada.ca, but no CSV/JSON bulk download URL was identified. The only confirmed format is interactive HTML table + historical PDFs. **Re-run:** Fetch `https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products/applications-submissions/register-innovative-drugs.html` with Playwright or equivalent JS-capable browser tool to extract the full table. Alternatively contact Health Canada's Office of Patented Medicines and Liaison.

2. **DPD extract documentation pages:** Both `what-data-extract-drug-product-database.html` and `read-file-drug-product-database-data-extract.html` returned HTTP 000 (connection failure). **Re-run:** These pages are accessible via browser (confirmed in WebSearch) and contain field-level documentation for the ZIP extract files. Fetch via Playwright.

3. **SBD record count and most-recent record from the ORIGINAL agent:** The agent's final bash call for the SBD count exited with code 1 before returning a result. The **newly verified count is 712 records** (2026-08-06 live fetch). The most recent record's date was not recovered — worth fetching to confirm freshness.

4. **Agile Licensing / Conditional Market Authorization regulations status:** The Forward Regulatory Plan 2026-2028 page (`https://www.canada.ca/en/health-canada/corporate/about-health-canada/legislation-guidelines/acts-regulations/forward-regulatory-plan/plan.html`) was fetched but returned empty content. **Re-run:** Use Playwright to determine whether the agile licensing amendment was finalized or is still planned.

5. **NOC bulk download URL:** The Open Canada NOC dataset page `https://open.canada.ca/data/en/dataset/a661b339-305f-4a41-96a3-2f5b12bcbf55` returned HTTP 200 but the agent did not extract individual resource download URLs from it. **Re-run:** CKAN API call `https://open.canada.ca/data/api/3/action/package_show?id=a661b339-305f-4a41-96a3-2f5b12bcbf55`.

6. **Clinical Trials Search Portal dataset:** The dataset at `https://ouvert.canada.ca/data/dataset/8fb2d580-6ccd-48cf-8655-349bfd7a98b2` was confirmed HTTP 200 but its download URL and field schema were not extracted.

---

## URL Ledger

### VERIFIED

| URL | Status | Notes |
|---|---|---|
| `https://health-products.canada.ca/api/drug/drugproduct/?status=2&lang=en&type=json` | HTTP 200 | Returns 13,355 marketed human drugs |
| `https://health-products.canada.ca/api/drug/activeingredient/?lang=en&type=json` | HTTP 200 | Ingredient data |
| `https://health-products.canada.ca/api/drug/company/?lang=en&type=json` | HTTP 200 | Company/DIN owner |
| `https://health-products.canada.ca/api/drug/form/?lang=en&type=json` | HTTP 200 | Dosage form |
| `https://health-products.canada.ca/api/drug/route/?lang=en&type=json` | HTTP 200 | Route of administration |
| `https://health-products.canada.ca/api/drug/schedule/?lang=en&type=json` | HTTP 200 | Rx/OTC schedule |
| `https://health-products.canada.ca/api/drug/therapeuticclass/?lang=en&type=json` | HTTP 200 | ATC codes |
| `https://health-products.canada.ca/api/drug/packaging/?type=json` | HTTP 200 | Packaging |
| `https://health-products.canada.ca/api/drug/pharmaceuticalstd/?type=json` | HTTP 200 | Pharm standard |
| `https://health-products.canada.ca/api/drug/status/?lang=en&type=json` | HTTP 200 | Status lookup |
| `https://health-products.canada.ca/api/drug/veterinaryspecies/?lang=en&type=json` | HTTP 200 | Vet species |
| `https://open.canada.ca/data/en/dataset/bf55e42a-63cb-4556-bfd8-44f26e5a36fe` | HTTP 200 | DPD bulk dataset page |
| `https://open.canada.ca/data/dataset/bf55e42a-63cb-4556-bfd8-44f26e5a36fe/resource/b05ae610-0366-478f-993f-b4afbdaadbc6/download/allfiles.zip` | HTTP 200 | DPD allfiles.zip download |
| `https://health-products.canada.ca/api/notice-of-compliance/drugproduct/?lang=en&type=json` | HTTP 200 | NOC drug product endpoint |
| `https://health-products.canada.ca/api/notice-of-compliance/noticeofcompliancemain/?lang=en&type=json` | HTTP 200 | NOC main endpoint; 37,714 records |
| `https://health-products.canada.ca/api/notice-of-compliance/medicinalingredient/?lang=en&type=json` | HTTP 200 | NOC medicinal ingredient |
| `https://health-products.canada.ca/api/notice-of-compliance/route/?lang=en&type=json` | HTTP 200 | NOC route |
| `https://health-products.canada.ca/api/notice-of-compliance/dosageform/?lang=en&type=json` | HTTP 200 | NOC dosage form |
| `https://health-products.canada.ca/api/documentation/noc-documentation-en.html` | HTTP 200 | NOC API documentation |
| `https://open.canada.ca/data/en/dataset/a661b339-305f-4a41-96a3-2f5b12bcbf55` | HTTP 200 | NOC dataset Open Canada |
| `https://pr-rdb.hc-sc.gc.ca/pr-rdb/` | HTTP 200 (redirect) | Patent Register web UI |
| `https://pr-rdb.hc-sc.gc.ca/patent/Patent.zip` | HTTP 206 (partial) | Patent Register ZIP — valid ZIP magic bytes confirmed |
| `https://open.canada.ca/data/en/dataset/1674baf5-6822-4788-afb3-f8659531d7c0` | HTTP 200 | Patent Register dataset Open Canada |
| `https://health-products.canada.ca/api/summary-report/api/basisdecision/?lang=en&type=json` | HTTP 200 | SBD API — 712 records |
| `https://open.canada.ca/data/en/dataset/9e168ff0-ece9-44de-bbec-68878454cbc1` | HTTP 200 | SBD dataset Open Canada |
| `https://dhpp.hpfb-dgpsa.ca/review-documents/resource/SBD1709128914848` | HTTP 200 | DHPP individual SBD document |
| `https://clinical-information.canada.ca/search/ci-rc` | HTTP 200 (redirect) | CIP search portal |
| `https://clinical-information.canada.ca/content/clinical-information-release-in-progress` | HTTP 200 | CIP releases in progress |
| `https://ouvert.canada.ca/data/dataset/8fb2d580-6ccd-48cf-8655-349bfd7a98b2` | HTTP 200 | Clinical Trials Database Open Canada |
| `https://healthproductshortages.ca/` | HTTP 200 | Health Product Shortages Canada (new site) |
| `https://healthproductshortages.ca/blog/52` | HTTP 200 | Shortages API documentation |
| `https://open.canada.ca/data/en/info/d8d6588e-8640-47df-835e-528fd62bf188` | Confirmed via WebSearch | HC regulatory approach to orphan drugs |

### UNVERIFIED (connection failures or not fetched)

| URL | Status / Reason | Notes |
|---|---|---|
| `https://health-products.canada.ca/api/drug/` | HTTP 403 (WebFetch) / JS-rendered HTML (curl) | API root; use specific sub-endpoints instead |
| `https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products/drug-product-database/what-data-extract-drug-product-database.html` | HTTP 000 / exit code 92 | DPD extract documentation; accessible in browser |
| `https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products/drug-product-database/read-file-drug-product-database-data-extract.html` | HTTP 000 / exit code 92 | DPD extract field definitions |
| `https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products/applications-submissions/register-innovative-drugs.html` | HTTP 000 | Register of Innovative Drugs; accessible in browser per WebSearch |
| `https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products/notice-compliance/database.html` | Not fetched | NOC database web UI |
| `https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products/notice-compliance/conditions.html` | Not fetched | NOC/c list |
| `https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products/summary-basis-decision.html` | HTTP 404 (via `sbd-smd` subdomain); HTTP 000 (canada.ca) | SBD landing page |
| `https://www.canada.ca/en/health-canada/services/drugs-health-products/special-access/overview.html` | HTTP 000 | SAP overview; accessible in browser |
| `https://www.canada.ca/en/health-canada/services/drugs-health-products/special-access/drugs.html` | HTTP 000 | SAP drugs page |
| `https://www.canada.ca/en/health-canada/services/health-care-systems/national-pharmacare/strategy-drugs-rare-diseases.html` | HTTP 403 (WebFetch) / empty (curl) | National Strategy for DRD |
| `https://www.canada.ca/en/health-canada/corporate/about-health-canada/legislation-guidelines/acts-regulations/forward-regulatory-plan/plan.html` | Empty response | Forward Regulatory Plan 2026-2028 |
| `https://capra.ca/en/blog/rare-diseases-and-orphan-drugs-regulatory-framework-in-canada-recent-initiatives-by-government-of-canada-2023-05-15` | Content extracted successfully by WebFetch | Used as source for no-formal-orphan-framework finding |
| `https://hpr-rps.hres.ca/reg-content/summary-basis-decision-detailOne.php` | HTTP 404 for specific item | Legacy SBD register portal |
| `https://github.com/FayeA/ScriptsForHCDrugProductDatabase` | Not fetched (WebSearch result only) | DPD extract parsing scripts |
| `https://cran.r-project.org/package=dpdr` | Not fetched | R package for DPD API |

---

*Recovered 2026-08-06 from agent-aecf128bd39bce62a.jsonl. SBD record count (712) and Patent.zip / healthproductshortages.ca HTTP status were newly verified on 2026-08-06 after transcript recovery.*
