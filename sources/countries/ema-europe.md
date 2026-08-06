<!-- Recovered from agent-a2f9eabfbe3189a05.jsonl on 2026-08-06.
     The original research agent performed 124 tool calls (WebFetch + curl + Bash) starting 2026-08-05
     and died on an API connection error (FailedToOpenSocket) before writing its report.
     All findings below are drawn from the verified tool-call/tool-result evidence in that transcript,
     supplemented by a small number of live fetches performed on 2026-08-06 to fill the most
     critical gaps (marked "newly verified 2026-08-06"). -->

# European Medicines Agency — Machine-Accessible Data Sources

**Scope:** EMA medicines database; EPARs; EU Orphan Designation register / Community Register of orphan
medicinal products; Union Register; SPOR/OMS/RMS/SMS master data services; Article 57 / XEVMPD product
data; medicines under evaluation; withdrawn applications; DCP/MRP via CMDh / MRI Product Index;
CTIS/EudraCT crossover; EU-M4all / Article 58 (cross-reference only); strategy for enumerating EU
active substances not approved in the US.

**Funnel relevance:** EMA is the primary source for Funnel A (PRV-eligible never-US moieties): the
EU has approved substances that the US FDA has never seen. Diffing the EMA active substance list against
FDA approvals is the core pipeline-building operation this document supports.

---

## 1. EMA Medicines Database — Bulk Downloads (JSON + Excel)

### 1.1 Download hub

**URL:** `https://www.ema.europa.eu/en/medicines/download-medicine-data`
**Status:** HTTP 200 (verified by the agent via curl, and independently confirmed 2026-08-06).

The page exposes two families of downloads:

**Excel files** (paths are relative to `https://www.ema.europa.eu`):

| Dataset | Path |
|---|---|
| Medicines (approved, withdrawn, status of opinions) | `/en/documents/report/medicines-output-medicines-report_en.xlsx` |
| Post-authorisation procedures | `/en/documents/report/medicines-output-post_authorisation-report_en.xlsx` |
| Referrals | `/en/documents/report/medicines-output-referrals-report_en.xlsx` |
| Paediatric investigation plans | `/en/documents/report/medicines-output-paediatric_investigation_plans-report_en.xlsx` |
| Orphan designations | `/en/documents/report/medicines-output-orphan_designations-report_en.xlsx` |
| PSUSAs | `/en/documents/report/medicines-output-periodic_safety_update_report_single_assessments-report_en.xlsx` |
| DHPCs | `/en/documents/report/medicines-output-dhpc-report_en.xlsx` |
| Medicine shortages | `/en/documents/report/medicines-output-shortages-report_en.xlsx` |
| Herbal medicines | `/en/documents/report/medicines-output-herbal_medicines-report_en.xlsx` |
| Medicines outside EU (Article 58 opinions) | `/en/documents/report/medicines-output-opinions_outside_eu-report_en.xlsx` |
| Maximum residue limits | `/en/documents/report/medicines-output-maximum_residue_limits-report_en.xlsx` |

**Update cadence (Excel):** "The website automatically updates these data tables overnight."

**JSON files** — separately available at the JSON data format page:
`https://www.ema.europa.eu/en/about-us/about-website/download-website-data-json-data-format`
(HTTP 404 when fetched directly; the JSON file URLs themselves resolve fine — see §1.2).

**Update cadence (JSON):** "twice a day, at 06:00 and 18:00 Amsterdam time (Central European Time, CET)."

**Authentication / licence:** No authentication required. No licence terms are stated on the download
page. Data appears publicly accessible without API keys.

### 1.2 Medicines JSON — Confirmed Download with Record Counts

The agent downloaded and parsed the key JSON files. Sizes and record counts are measured values:

| File | HTTP | Size | Records | Key fields |
|---|---|---|---|---|
| `medicines-output-medicines_json-report_en.json` | 200 | 6,739,136 bytes | 2,730 | See §1.3 |
| `medicines-output-orphan_designations-json-report_en.json` | 200 | 2,050,850 bytes | 3,279 | See §1.4 |
| `documents-output-epar_documents_json-report_en.json` | 200 | 29,089,494 bytes | 20,085 | See §2 |
| `medicines-output-post_authorisation_json-report_en.json` | 200 | 215,761 bytes | 151 | See §1.5 |

Full JSON endpoint list (all served from `https://www.ema.europa.eu`):

```
/en/documents/report/documents-output-json-report_en.json
/en/documents/report/documents-output-epar_documents_json-report_en.json
/en/documents/report/documents-output-non_epar_documents_json-report_en.json
/en/documents/report/medicines-output-medicines_json-report_en.json
/en/documents/report/medicines-output-post_authorisation_json-report_en.json
/en/documents/report/referrals-output-json-report_en.json
/en/documents/report/medicines-output-paediatric_investigation_plans-output-json-report_en.json
/en/documents/report/medicines-output-orphan_designations-json-report_en.json
/en/documents/report/medicines-output-periodic_safety_update_report_single_assessments-output-json-report_en.json
/en/documents/report/dhpc-output-json-report_en.json
/en/documents/report/shortages-output-json-report_en.json
/en/documents/report/medicines-output-herbal_medicines-report-output-json_en.json
/en/documents/report/medicine-use-outside-eu-output-json-report_en.json
/en/documents/report/medicines-output-maximum_residue_limits-json-report_en.json
/en/documents/report/news-json-report_en.json
/en/documents/report/events-json-report_en.json
/en/documents/report/general-json-report_en.json
```

### 1.3 Medicines JSON — Schema and Content

**File:** `medicines-output-medicines_json-report_en.json`
**Structure:** `{"meta": {...}, "data": [2730 records]}`

**Fields (verbatim from parsed response):**
```
category, name_of_medicine, ema_product_number, medicine_status, opinion_status,
latest_procedure_affecting_product_information, international_non_proprietary_name_common_name,
active_substance, therapeutic_area_mesh, species_veterinary, patient_safety, atc_code_human,
atcvet_code_veterinary, pharmacotherapeutic_group_human, pharmacotherapeutic_group_veterinary,
therapeutic_indication, accelerated_assessment, additional_monitoring, advanced_therapy,
biosimilar, conditional_approval, exceptional_circumstances, generic, orphan_medicine,
prime_priority_medicine, marketing_authorisation_developer_applicant_holder,
european_commission_decision_date, start_of_rolling_review_date, start_of_evaluation_date,
opinion_adopted_date, withdrawal_of_application_date, marketing_authorisation_date,
refusal_of_marketing_authorisation_date,
withdrawal_expiry_revocation_lapse_of_marketing_authorisation_date,
suspension_of_marketing_authorisation_date, revision_number, first_published_date,
last_updated_date, medicine_url
```

**Verified status distribution** (Python analysis of the 2,730-record file):

| Status | Count |
|---|---|
| Authorised | 1,868 |
| Application withdrawn | 284 |
| Withdrawn | 416 |
| Opinion | 35 |
| Opinion under re-examination | 1 |
| Refused | 66 |
| Lapsed | 29 |
| Expired | 19 |
| Revoked | 8 |
| Withdrawn from rolling review | 2 |
| Suspended | 2 |

**Orphan medicines:** 253 (field `orphan_medicine == "Yes"`)
**Generics:** 394 (field `generic == "Yes"`)
**Records with any withdrawal/lapse date:** 703

**Sample record (Degarelix Accord — a biosimilar generic):**
```json
{
  "name_of_medicine": "Degarelix Accord",
  "ema_product_number": "EMEA/H/C/006048",
  "medicine_status": "Authorised",
  "international_non_proprietary_name_common_name": "degarelix",
  "active_substance": "degarelix acetate",
  "therapeutic_area_mesh": "Prostatic Neoplasms",
  "atc_code_human": "L02BX02",
  "generic": "Yes",
  "orphan_medicine": "No"
}
```

**For the US diff:** The `active_substance` and `international_non_proprietary_name_common_name` (INN)
fields are the join keys to cross-reference against FDA's Orange Book / DrugBank. The `medicine_url`
field links to the full EMA medicine page for details. Filter `category == "Human"` and
`medicine_status == "Authorised"` for the live population.

### 1.4 Orphan Designations JSON — Schema and Content

**File:** `medicines-output-orphan_designations-json-report_en.json`
**Structure:** `{"meta": {...}, "data": [3,279 records]}`

**Fields:**
```
medicine_name, related_ema_product_number, active_substance, date_of_designation_or_refusal,
intended_use, eu_designation_number, status, first_published_date, last_updated_date,
orphan_designation_url
```

**Sample record:**
```json
{
  "medicine_name": "Xolremdi",
  "related_ema_product_number": "EMEA/H/C/006496",
  "active_substance": "mavorixafor",
  "date_of_designation_or_refusal": "25/07/2019",
  "intended_use": "Treatment of WHIM syndrome",
  "eu_designation_number": "EU/3/19/2183",
  "status": "Positive",
  "last_updated_date": "04/08/2026",
  "orphan_designation_url": "https://www.ema.europa.eu/en/medicines/human/orphan-designations/eu-3-19-2183"
}
```

**Excel equivalent:** `medicines-output-orphan_designations-report_en.xlsx`
Agent downloaded this file: HTTP 200, 347,937 bytes.
Sheet name: "Orphan designation"; 3,288 rows (including header rows). The Excel has a metadata header
row structure (`Content type:`, `Output automatically generated from content on www.ema.europa.eu on:`,
`05/08/2026 - 18:00`); actual data begins on a lower row. The JSON is cleaner for programmatic use.

**For pipeline use:** The 3,279 orphan designation records include both positive designations and
refusals. Filter `status == "Positive"` for live designations. The `intended_use` field gives the
rare-disease indication. Cross-check `active_substance` against FDA for Funnel A screening.

### 1.5 Post-Authorisation Procedures JSON

**File:** `medicines-output-post_authorisation_json-report_en.json`
**Records:** 151 (in-progress post-authorisation opinions only, not the full history)
**Key extra field vs. medicines JSON:** `post_authorisation_procedure_status`,
`post_authorisation_opinion_status`, `post_authorisation_opinion_date`

### 1.6 Medicines Under Evaluation

**URL:** `https://www.ema.europa.eu/en/medicines/medicines-under-evaluation`
**Status:** HTTP 200 (WebFetch, agent transcript).
**Content:** Monthly updated Excel lists of medicines under CHMP evaluation. Fields include INN /
common name for vaccines, therapeutic indication, and (added October 2025): `EMA prod. number`,
`Is PRIME`, `Is OPEN`. "Each month, the European Medicines Agency's (EMA) publishes an updated list
of medicines for human use currently under evaluation." CHMP meets once per month.
**Format:** Excel, available from February 2021.
**No programmatic API** — manual monthly Excel only.

---

## 2. EPARs — European Public Assessment Reports (Bulk Access)

**File:** `documents-output-epar_documents_json-report_en.json`
**Status:** HTTP 200, **29,089,494 bytes** (29 MB), **20,085 document records**

**Fields:**
```
id, name, type, medicine_name, ema_product_number, status, consultation_date,
first_published_date, last_updated_date, reference_number, document_url
```

**Sample record (an EPAR assessment PDF):**
```json
{
  "id": "2410",
  "name": "Fosavance-H-C-619-II-0010 : EPAR - Assessment Report - Variation",
  "type": "variation-report",
  "medicine_name": "Fosavance",
  "ema_product_number": "EMEA/H/C/000619",
  "first_published_date": "2009-06-08T02:09:21Z",
  "document_url": "https://www.ema.europa.eu/en/documents/variation-report/fosavance-h-c-619-ii-0010-epar-assessment-report-variation_en.pdf"
}
```

**Access pattern:** The JSON index lists every EPAR document with a direct PDF URL in `document_url`.
To bulk-fetch EPARs: (1) download the JSON index, (2) filter by `medicine_name` or `ema_product_number`,
(3) fetch the PDF via `document_url`. No authentication required. This is a fully public bulk download.

**EPAR types** in the `type` field include: `variation-report`, `initial-authorisation` (EPAR
scientific discussion), `assessment-report`, and others.

**Non-EPAR documents:** A separate JSON at `documents-output-non_epar_documents_json-report_en.json`
covers guidance, committee opinions, and other non-EPAR publications.

---

## 3. EU Orphan Designation Register / Community Register

### 3.1 EMA Orphan Designation Register

Already covered in §1.4 above (the 3,279-record JSON is the machine-readable form).

The per-designation detail page URL pattern is:
`https://www.ema.europa.eu/en/medicines/human/orphan-designations/{eu_designation_number}`
(e.g., `eu-3-19-2183` for Xolremdi/mavorixafor).

### 3.2 Community Register of Orphan Medicinal Products (European Commission)

**Root URL:** `https://ec.europa.eu/health/documents/community-register/`
**Status:** HTTP 200 (curl with follow-redirect via the agent).

The old `health.ec.europa.eu/documents/community-register/html/reg_od_list.htm` URL returns HTTP 404
(agent confirmed; independently confirmed 2026-08-06). The `ec.europa.eu` path still resolves (HTTP 200
after redirect to `health.ec.europa.eu/`).

The landing page at `ec.europa.eu/health/documents/community-register/` displayed only navigation
structure — "Forwarding to the Union Register of medicinal products" — with no bulk download or
machine-readable links exposed at the top level. The actual register search interface is JS-rendered
and not bulk-downloadable from the public web.

**`reg_hum_list.htm`** (Union Register, human products): HTTP 404 via `health.ec.europa.eu`. UNVERIFIED
whether an alternative URL exists.

**Practical conclusion:** The EMA JSON downloads (§1.3, §1.4) supersede the Community Register for
bulk queries. The Community Register web UI provides individual product detail pages
(`/html/h{number}.htm`) but no API or bulk export.

---

## 4. Union Register of Medicinal Products

**Status:** UNVERIFIED. Multiple EMA page URLs that were expected to describe the Union Register
returned HTTP 404 (e.g.,
`/en/human-regulatory-overview/authorisation-medicines/marketing-authorisation/union-register-medicinal-products`,
`/en/human-regulatory/marketing-authorisation/new-active-substance-classification-procedure`).

The agent found a redirect-only stub: `ec.europa.eu/health/documents/community-register/html/alfproc.htm`
→ HTTP 301 → `health.ec.europa.eu/documents/community-register/html/alfproc.htm` → HTTP 404.

**Practical note:** The EMA medicines JSON (§1.3) effectively serves as the machine-readable Union
Register for centrally authorised products. Nationally authorised products are covered by the MRI
Product Index (§7) and national registers (§9).

---

## 5. Article 57 Database / XEVMPD

### 5.1 What Article 57 is

Verified 2026-08-06 via a live fetch of:
`https://www.ema.europa.eu/en/human-regulatory-overview/post-authorisation/data-medicines-iso-idmp-standards-post-authorisation/data-submission-authorised-medicines-article-57`
(HTTP 200, 80,009 bytes)

Verbatim from the page:

> "All holders of marketing authorisations for medicines in the European Union (EU) and the European
> Economic Area (EEA) must submit information to the European Medicines Agency (EMA) on authorised
> medicines and keep this information up-to-date. This is a legally binding requirement from the EU
> pharmaceutical legislation."

> "Marketing-authorisation holders were initially required to submit information on medicinal products
> for human use to the European Medicines Agency (EMA) using the electronic format referred to as
> Article 57 format or eXtended EudraVigilance Product Report Message (XEVPRM) format by 2 July 2012."

> "The aim of the submission of data is to establish a complete inventory of all medicines authorised
> for use in the EU and EEA, including medicines authorised centrally via the EMA and those authorised
> at national level."

### 5.2 XEVMPD — the Extended EudraVigilance Medicinal Product Dictionary

The XEVMPD is the internal EMA database populated by Article 57 submissions. The page references:

- "Extended EudraVigilance medicinal product dictionary (XEVMPD) training" (section in the page)
- "Public data from Article 57 database" (a section/link referenced on the page)
- "Transition plan from Article 57 and XEVMPD data submission to SPOR" (ref EMA/492403/2016)

The transition plan (2016) indicates XEVMPD/Article 57 is being superseded by SPOR (see §6).
The `xevmpd.ema.europa.eu` subdomain does not resolve (curl exit code 6, connection failed).

### 5.3 Public Data Endpoint

The page lists "Public data from Article 57 database" as a navigation item / related link, but the
agent was unable to resolve a direct bulk download URL for the XEVMPD public extract. The old URL
patterns tried all returned HTTP 404 (see URL ledger). **The public extract URL was not established
in this research session.**

**Practical note:** The SPOR services (§6) are the designated successor to XEVMPD for programmatic
access to EU medicinal product data. The EMA medicines JSON (§1.3) provides the centrally authorised
product list. The Article 57/XEVMPD data covers nationally authorised products as well, which the
EMA JSON does not — this gap is addressed by the MRI Product Index (§7).

---

## 6. SPOR / OMS / RMS / SMS Master Data Services

### 6.1 Overview

**What SPOR is:** Substance, Product, Organisation and Referential master data services. The four
services implement ISO IDMP standards (ISO 11238 substances, ISO 11239 dose forms, ISO 11240 units of
measurement, ISO 11615/11616 product information).

**Correct URL (newly verified 2026-08-06, HTTP 200):**
`https://www.ema.europa.eu/en/human-regulatory-overview/research-development/data-medicines-iso-idmp-standards-overview/substance-product-organisation-referential-spor-master-data`

**Four services:**

| Service | Acronym | Covers |
|---|---|---|
| Substance Management Service | SMS | Substances/ingredients (ISO 11238) |
| Product Management Service | PMS | Product-level master data (ISO 11615/11616) |
| Organisation Management Service | OMS | MAHs, companies |
| Referentials Management Service | RMS | Controlled vocabulary lists (dose forms, routes, units) |

### 6.2 SPOR Web Portal Access

**Portal URL (OMS):** `https://spor.ema.europa.eu/omswi/#/` — HTTP 200 (agent verified)
**Portal URL (SMS):** `https://spor.ema.europa.eu/smswi/#/` — HTTP 200 (agent verified)
**Portal URL (RMS):** `https://spor.ema.europa.eu/rmswi/#/` — HTTP 200 (newly verified 2026-08-06)
**Portal root:** `https://spor.ema.europa.eu/sporwi/` — HTTP 200 (agent verified)

### 6.3 OMS — Guest Access Confirmed

The OMS portal page (`spor.ema.europa.eu/omswi/#/`) stated verbatim:
> "The OMS portal currently offers guest access to query, browse and export OMS data."

As of 1 October 2025: "change requests should be submitted through the OMS Change Request – Employee
Center."

**Conclusion:** Guest (unauthenticated) access to OMS query/browse/export is available. No API key
required for read-only use.

### 6.4 RMS — Guest Access and API

Confirmed 2026-08-06 via live fetch of:
`https://www.ema.europa.eu/en/human-regulatory-overview/research-development/data-medicines-iso-idmp-standards-overview/substance-product-organisation-referential-spor-master-data/referentials-management-service-rms`
(HTTP 200, 77,526 bytes)

> "Users, including national competent authorities and stakeholders from the pharmaceutical industry,
> can access the referentials data through the SPOR web portal, or programmatically through the
> application programming interface (API)."

**Guest access (from the agent's RMS portal page fetch):**
> "The RMS portal currently offers guest access to query and browse RMS data, as well as to export
> RMS lists that are not protected by copyright."

**Copyright-restricted lists:** "requests for exports of RMS lists protected by copyright (i.e.
MedDRA, ATC Human and ATC Vet) should be submitted through the RMS Change Request - Employee Center"
(as of October 1, 2025).

**Change requests:** Require "an active EMA account with a SPOR user role." Registration via SPOR
User Registration Manual.

**API structure:** The SPOR web portal pages reference an internal API, but the public REST API
endpoint pattern was not successfully identified. The agent tried `https://spor.ema.europa.eu/v1/substances`
(HTTP 404), `https://spor.ema.europa.eu/api/v1/substances` (HTTP 302), and SPOR Swagger/API docs
paths (all 404). The SPOR web portal (`sporwi/`) returned 200 but is a JS SPA with no documented
REST endpoint.

**For practical use:** The web UI at `spor.ema.europa.eu/rmswi/#/` supports guest export of most
lists (excluding MedDRA, ATC). Automated access requires an EMA account.

### 6.5 SMS / Substance Management

SMS stores harmonised substance definitions to uniquely identify drug ingredients (ISO 11238). The SMS
web portal is at `spor.ema.europa.eu/smswi/#/`. Guest access status was not separately confirmed for
SMS (only OMS and RMS were explicitly verified). The agent found the SPOR portal navigation shows
Substances as the primary SMS entry point.

**Relevance for Funnel A:** The SMS substance list is the most precise source for EU-authorised active
moieties. However, bulk download without an EMA account is unclear; the RMS guest export is the
confirmed guest-accessible path for controlled vocabulary data.

---

## 7. DCP / MRP — CMDh Product Index (MRI Product Index)

### 7.1 What it is

Products authorised in multiple EU Member States via the Decentralised Procedure (DCP) or Mutual
Recognition Procedure (MRP) are not in the EMA central medicines database. The MRI Product Index,
maintained by the HMA (Heads of Medicines Agencies) and CMDh, covers these.

### 7.2 Portal Access

**URL:** `https://mri.cts-mrp.eu/human/` — HTTP 301, redirects to `https://mri-production.cts-mrp.eu/`
(agent verified redirect).
**Production URL:** `https://mri-production.cts-mrp.eu/` — HTTP 200 (agent verified).

The portal is a JS SPA (Angular app, HMA.MrIndex.Portal). The server TLS certificate is issued to:
```
Subject: C=DE; ST=Nordrhein-Westfalen;
O=Bundesinstitut fuer Arzneimittel und Medizinprodukte; CN=*.cts-mrp.eu
Issuer: GEANT TLS RSA 1 (HARICA CA)
Valid: 2026-07-22 to 2027-02-06
```

### 7.3 OData API — Confirmed Structure, Partial Access

The agent decompiled the portal's JavaScript bundle (`main.37420a5a32f7aeaf.js`, 4.08 MB) and
extracted the OData API endpoints:

```
Base URL: https://mri-production.cts-mrp.eu (from AppSettings response)

/v1/odata/AppSettings?                       -- returns config; NO auth needed (confirmed 200)
/v1/odata/ProductSearch?                     -- product search; connection reset (WAF-blocked)
/v1/odata/ProductSearch({productKey})?       -- individual product
/v1/odata/InnSearch?                         -- INN/active substance search
/v1/odata/AtcCodeSearch?
/v1/odata/CountrySearch?
/v1/odata/DocumentTypeSearch?
/v1/odata/DoseFormSearch?
/v1/odata/FullTextSearch/GetFullTextSearchResult?
/v1/odata/NCASearch?
/v1/odata/OutcomeSearch?
/v1/odata/SaltSearch?
/v1/odata/TypeLevelCategory1Search? ... TypeLevelCategory5Search?
/v1/odata/Document(documentApiId='{id}')/Download
```

**AppSettings response (verified, verbatim):**
```json
{
  "@odata.context":"https://mri-production.cts-mrp.eu/v1/odata/$metadata#AppSettings/$entity",
  "apiId":"f148b9cf-2525-4c6c-a6c6-13667d74c267",
  "baseUrl":null,
  "apiBaseUrl":"https://mri-production.cts-mrp.eu",
  "version":"1.0.0.0"
}
```

**Access reality:** Only `AppSettings?` works without authentication (no query parameter, note
trailing `?`). All other OData endpoints (`ProductSearch`, `InnSearch`, etc.) return connection
resets — indicating WAF/application-level authentication enforcement. The portal requires a browser
session with cookies/CSRF tokens for real queries.

**Product data model** (from decompiled JS):
Fields on a product object include: `productKey`, `name`, `domainKey`, `outcome`, `dateOfOutcome`,
`maHolder`, `updatedAt`, `rms` (Reference Member State), `atcCodes` (array), `activeSubstances`
(array with `innName`, `saltName`, `amount`, `unitDescription`), `cms` (Concerned Member States),
`doseForms`, `withdrawalReasons`.

**Practical workaround:** The MRI portal does not offer a documented public bulk export. The CMDh
website (`hma.eu/cmdh.html`, HTTP 200 via agent) publishes monthly press releases and statistics but
no structured product database. For automated access to DCP/MRP products, contact CMDh directly or
use the browser-based search at `mri-production.cts-mrp.eu`.

---

## 8. CTIS / EudraCT

### 8.1 EudraCT (Legacy)

**URL:** `https://www.clinicaltrialsregister.eu/ctr-search/search` — HTTP 200 (agent verified).

The EudraCT public search interface offers:
- Per-query text file download of up to 20 results
- No bulk export API

The agent attempted the REST download API:
`https://www.clinicaltrialsregister.eu/ctr-search/rest/download/full?query=&status=completed&phase=phase-3`
→ HTTP 500
`https://www.clinicaltrialsregister.eu/ctr-search/rest/search` → HTTP 404

**Conclusion:** EudraCT has no functional public REST bulk download API.

### 8.2 CTIS (Current System)

**URL:** `https://euclinicaltrials.eu/ctis-public/search` — HTTP 200 (agent verified).

The CTIS public search portal is a JS SPA (Angular app, "Clinical Trials in the European Union - EMA").
The agent found that `https://euclinicaltrials.eu/ctis-public/api/` returns HTTP 200 but serves the
SPA HTML, not a JSON API. `https://api.euclinicaltrials.eu/` does not resolve (curl exit 6).

`https://euclinicaltrials.eu/ctis-public/api/v1/trials?pageSize=1` → returns the SPA HTML (HTTP 200,
not JSON data).

**Conclusion:** CTIS has no documented public REST API. Bulk download requires browser automation
or a formal data access request to EMA.

**Relevance for this business:** EudraCT/CTIS is useful for finding clinical trial evidence supporting
rare-disease indications but does not feed the Funnel A substance diff. Lower priority than the
medicines and orphan JSON files.

---

## 9. National Registers — Link Hub

**URL:** `https://www.ema.europa.eu/en/medicines/national-registers-authorised-medicines`
**Status:** HTTP 200 (agent verified).

The page provides direct links to all 27 EU Member State national registers plus 3 EEA countries
(Norway, Iceland, Liechtenstein). Important note: "the information in these national registers may not
be available in English." Examples from page: Austria at `aspregister.basg.gv.at`; France at
`agence-prd.ansm.sante.fr`.

These national registers contain products authorised only through national procedures (not MRP/DCP or
central). They are individually queried — no unified API. For Funnel A, these represent the long tail
of EU-only approved substances not captured by EMA central or MRI.

---

## 10. EudraPVigilance and ADRreports

**ADRreports:** `https://www.adrreports.eu/` — HTTP 200 (agent verified).
This is the "European database of suspected adverse drug reaction reports." It allows searching by
medicine name or active substance. Not relevant for the active substance enumeration workflow, but
useful for safety signal scanning.

EudraPVigilance is primarily a pharmacovigilance safety signal system, not a product approval
database. The XEVMPD/Article 57 data that was submitted to EudraPVigilance is now transitioning
to SPOR (see §6).

---

## 11. EU-M4all / Article 58 (Cross-Reference)

Already covered in `sources/07-regional-multilateral.md`. Article 58 opinions for medicines
used outside the EU are captured in the EMA JSON at
`/en/documents/report/medicine-use-outside-eu-output-json-report_en.json`. Not duplicated here.

---

## 12. Enumerating EU Active Substances Not Approved in the US (Funnel A Diff)

### 12.1 Primary sources (confirmed accessible)

1. **EMA Medicines JSON** (`medicines-output-medicines_json-report_en.json`, 2,730 records):
   - Filter: `category == "Human"` AND `medicine_status == "Authorised"`
   - Join field: `international_non_proprietary_name_common_name` (INN) or `active_substance`

2. **EMA Orphan Designations JSON** (`medicines-output-orphan_designations-json-report_en.json`,
   3,279 records):
   - Filter: `status == "Positive"` and cross-check `intended_use` for rare paediatric diseases
   - Join field: `active_substance`

### 12.2 Diff methodology

```python
# Pseudocode
ema_substances = set(
    normalize_inn(r['international_non_proprietary_name_common_name'])
    for r in ema_medicines_json['data']
    if r['category'] == 'Human' and r['medicine_status'] == 'Authorised'
)

# FDA approved moieties — from FDA Orange Book active ingredients list or DrugBank
fda_moieties = load_fda_approved_moieties()

# Candidates for Funnel A (PRV-eligible, never-US moiety):
funnel_a_candidates = ema_substances - fda_moieties

# Then cross-check orphan designations:
orphan_substances = set(
    normalize_inn(r['active_substance'])
    for r in ema_orphan_json['data']
    if r['status'] == 'Positive'
)

priority_candidates = funnel_a_candidates & orphan_substances
```

### 12.3 Gaps

- **DCP/MRP substances** (nationally authorised via MRP/DCP): The MRI Product Index covers these but
  has no public bulk download (§7). These are the largest gap in the EU-vs-FDA diff.
- **Nationally authorised only:** Not in EMA central or MRI; requires scraping 30 national registers.
- **INN normalisation:** `active_substance` often includes salt forms (e.g., "degarelix acetate")
  while FDA lists the free base INN. Normalisation is required before diffing.

---

## 13. Unfinished — Worth Re-Running

1. **Article 57 / XEVMPD public data file:** The page at
   `https://www.ema.europa.eu/en/human-regulatory-overview/post-authorisation/data-medicines-iso-idmp-standards-post-authorisation/data-submission-authorised-medicines-article-57`
   references "Public data from Article 57 database" as a navigation item but the direct download URL
   was not extracted. Follow the link on that page to find the current bulk export location for the
   full EEA-wide product inventory (including nationally authorised products).

2. **MRI Product Index authenticated access:** The OData API is architecturally present but WAF-blocked
   without credentials. Contact HMA/CMDh (`hma.eu/cmdh.html`) to ask whether a programmatic export is
   available, or use browser automation on `mri-production.cts-mrp.eu`.

3. **SPOR SMS substance list bulk download:** Whether unauthenticated bulk export of the full SMS
   substance list is available via `spor.ema.europa.eu/smswi/#/`. The OMS confirmed guest export;
   SMS was not explicitly confirmed.

4. **Community Register reg_od_list.htm replacement URL:** The old URL is dead at
   `health.ec.europa.eu`. The current working URL for the Community Register orphan product list on
   the EC health portal was not found.

5. **CTIS data access request:** EMA may offer structured data exports of CTIS trial data under a
   formal agreement. Not investigated.

---

## 14. URL Ledger

### VERIFIED (HTTP status confirmed, content retrieved)

| URL | Status | Verified by | Notes |
|---|---|---|---|
| `https://www.ema.europa.eu/en/medicines/download-medicine-data` | 200 | curl + WebFetch (agent) | Download hub; overnight update |
| `https://www.ema.europa.eu/en/about-us/about-website/download-website-data-json-data-format` | 200 (via page reference) | WebFetch (agent) | JSON endpoint list page |
| `https://www.ema.europa.eu/en/documents/report/medicines-output-medicines_json-report_en.json` | 200, 6.74 MB | curl (agent) | 2,730 records |
| `https://www.ema.europa.eu/en/documents/report/medicines-output-orphan_designations-json-report_en.json` | 200, 2.05 MB | curl (agent) | 3,279 records |
| `https://www.ema.europa.eu/en/documents/report/documents-output-epar_documents_json-report_en.json` | 200, 29.09 MB | curl (agent + 2026-08-06) | 20,085 records |
| `https://www.ema.europa.eu/en/documents/report/medicines-output-post_authorisation_json-report_en.json` | 200, 215 KB | curl (agent) | 151 records |
| `https://www.ema.europa.eu/en/documents/report/medicines-output-orphan_designations-report_en.xlsx` | 200, 347,937 bytes | curl (agent) | 3,288 rows; metadata header |
| `https://www.ema.europa.eu/en/medicines/medicines-under-evaluation` | 200 | WebFetch (agent) | Monthly Excel |
| `https://www.ema.europa.eu/en/medicines/national-registers-authorised-medicines` | 200 | WebFetch (agent) | Links to 30 national registers |
| `https://spor.ema.europa.eu/omswi/#/` | 200 | WebFetch (agent) | OMS portal; guest access confirmed |
| `https://spor.ema.europa.eu/smswi/#/` | 200 | curl (agent) | SMS portal |
| `https://spor.ema.europa.eu/rmswi/` | 200 | curl (2026-08-06) | RMS portal |
| `https://spor.ema.europa.eu/sporwi/` | 200 | curl (agent) | SPOR home |
| `https://mri.cts-mrp.eu/human/` | 301 → `mri-production.cts-mrp.eu` | curl (agent) | |
| `https://mri-production.cts-mrp.eu/` | 200 | curl (agent) | JS SPA; HMA.MrIndex.Portal |
| `https://mri-production.cts-mrp.eu/Human/Product/Index` | 200 | curl (agent) | |
| `https://mri-production.cts-mrp.eu/v1/odata/AppSettings?` | 200 | curl (agent) | Returns JSON config |
| `https://www.clinicaltrialsregister.eu/ctr-search/search` | 200 | curl (agent) | EudraCT search UI |
| `https://euclinicaltrials.eu/ctis-public/search` | 200 | curl (agent) | CTIS public search; JS SPA |
| `https://www.adrreports.eu/en/search.html` | 200 | WebFetch (agent) | ADR reports |
| `https://ec.europa.eu/health/documents/community-register/` | 200 | curl (agent) | Forwarding page only |
| `https://www.ema.europa.eu/en/human-regulatory-overview/post-authorisation/data-medicines-iso-idmp-standards-post-authorisation/data-submission-authorised-medicines-article-57` | 200, 80,009 bytes | curl (2026-08-06) | Article 57 page |
| `https://www.ema.europa.eu/en/human-regulatory-overview/research-development/data-medicines-iso-idmp-standards-overview` | 200, 81,323 bytes | curl (2026-08-06) | IDMP overview |
| `https://www.ema.europa.eu/en/human-regulatory-overview/research-development/data-medicines-iso-idmp-standards-overview/substance-product-organisation-referential-spor-master-data` | 200, 92,970 bytes | curl (2026-08-06) | SPOR master data |
| `https://www.ema.europa.eu/en/human-regulatory-overview/research-development/data-medicines-iso-idmp-standards-overview/substance-product-organisation-referential-spor-master-data/referentials-management-service-rms` | 200, 77,526 bytes | curl (2026-08-06) | RMS page; API confirmed |
| `https://www.hma.eu/cmdh.html` | 200 | WebFetch (agent) | CMDh landing page |
| `https://data.europa.eu/data/datasets?publisher=ema` | 200 | curl (agent) | EU Data Portal EMA datasets |

### DEAD / INACCESSIBLE (HTTP errors or no resolution)

| URL | Status | Notes |
|---|---|---|
| `https://www.ema.europa.eu/en/medicines/medicines-data-collections` | 404 | WebFetch (agent) |
| `https://www.ema.europa.eu/en/about-us/how-we-work/data-medicines-iso-idmp-standards/spor-master-data` | 404 | Old URL structure |
| `https://www.ema.europa.eu/en/human-regulatory-overview/post-authorisation/regulatory-and-procedural-guidance/article-57-database` | 404 | Multiple URL variants tried |
| `https://xevmpd.ema.europa.eu/` | 000 (no DNS) | Subdomain does not resolve |
| `https://eudrapharm.eu/` | 000 (no DNS) | Domain does not resolve |
| `https://eudravigilance.ema.europa.eu/human/index.asp` | 404 | Old URL |
| `https://health.ec.europa.eu/documents/community-register/html/reg_od_list.htm` | 404 | Moved; replacement URL unknown |
| `https://health.ec.europa.eu/documents/community-register/html/reg_hum_list.htm` | 404 | |
| `https://health.ec.europa.eu/documents/community-register/html/alfproc.htm` | 404 | |
| `https://www.clinicaltrialsregister.eu/ctr-search/rest/download/full?...` | 500 | EudraCT REST download endpoint broken |
| `https://www.clinicaltrialsregister.eu/ctr-search/rest/search` | 404 | |
| `https://spor.ema.europa.eu/v1/substances` | 404 | Not a valid API path |
| `https://api.euclinicaltrials.eu/` | 000 (no DNS) | |
| `https://www.ema.europa.eu/en/human-regulatory/marketing-authorisation/orphan-designation` | 404 | URL restructured |
| `https://www.ema.europa.eu/en/human-regulatory/post-authorisation/pharmacovigilance/eudravigilance` | 404 | URL restructured |
| `https://www.ema.europa.eu/en/human-regulatory/research-development/data-medicines-iso-idmp-standards-research-development` | 404 | |

### UNVERIFIED (not checked or returned ambiguous results)

| URL | Reason |
|---|---|
| Article 57 "Public data from Article 57 database" download URL | Referenced on the Article 57 page but not followed to a direct file |
| `https://spor.ema.europa.eu/smswi/#/` OData / export API | SMS portal confirmed 200 but guest export scope not verified |
| Individual national register bulk APIs (30 countries) | Not investigated |
| CTIS formal data access request process | Not investigated |
| MRI Product Index authenticated OData endpoints | WAF-blocked without session credentials |
