<!-- RECOVERED from agent-ac2d7a7b7114bd897.jsonl on 2026-08-06.
     Original agent died on API ConnectionRefused error after 90 tool calls.
     All evidence below is drawn from that transcript.
     New live fetches performed 2026-08-06 are marked NEWLY VERIFIED 2026-08-06. -->

# FDA Manufacturing and Inspection Data — Section 5.3

*Technical reference for rare-disease drug repurposing company (Funnel A: PRV-eligible 505(b)(1) never-US moieties; Funnel B: orphan exclusivity only, US generics via 505(b)(2)). Today: 2026-08-06.*

---

## 1. Drug Establishment Registration and Listing — DECRS

**What it is.** The Drug Establishments Current Registration Site (DECRS) is FDA's publication of all currently registered establishments that manufacture, prepare, propagate, compound, or process drugs distributed in or offered for import to the US. Registration is mandatory under 21 U.S.C. §510; it must be renewed annually (expiration dates appear in the data as 12/31/YYYY).

**Authoritative DECRS landing page.**
- Canonical URL (redirects to): `https://www.fda.gov/drugs/drug-approvals-and-databases/drug-establishments-current-registration-site-decrs`
- VERIFIED: HTTP 200 (curl, 2026-08-05). Page title: "Drug Establishments Current Registration Site (DECRS)". `datePublished` in schema.org metadata: `2026-02-05`. Maintained by Center for Drug Evaluation and Research.

**Interactive search system.**
- `https://www.accessdata.fda.gov/scripts/cder/drls/default.cfm`
- VERIFIED: HTTP 200 (curl, 2026-08-05). Serves HTML search interface.

**Bulk download — the two zip files linked from the DECRS page.**

| File | URL | HTTP | Size (compressed) | Last-Modified | Content |
|------|-----|------|--------------------|---------------|---------|
| `drls_reg.zip` | `https://www.accessdata.fda.gov/cder/drls_reg.zip` | **200** | 2,393,826 bytes | 2026-08-05 07:15 UTC | Active registered establishments |
| `drls_excluded.zip` | `https://www.accessdata.fda.gov/cder/drls_excluded.zip` | **200** | 5,305 bytes | 2026-08-05 07:15 UTC | Establishments with EXCLUSION_FLAG=E |

Both VERIFIED by curl HEAD request, 2026-08-05.

**Schema of `drls_reg.txt` (tab-delimited, UTF-8).**
Downloaded and inspected 2026-08-05. File contains **10,395 lines including the header row**, so approximately **10,394 establishment records**. Columns:

```
FEI_NUMBER  DUNS_NUMBER  FIRM_NAME  ADDRESS  EXPIRATION_DATE  OPERATIONS
ESTABLISHMENT_CONTACT_NAME  ESTABLISHMENT_CONTACT_EMAIL  AGENT_DETAILS
REGISTRANT_NAME  REGISTRANT_DUNS  REGISTRANT_CONTACT_NAME
REGISTRANT_CONTACT_EMAIL  EXCLUSION_FLAG
```

**Sample records (verbatim from downloaded file, 2026-08-05):**

```
FEI: 0000000360  DUNS: 271408412  DSP  Rue Grands Navoirs, Chauny, F-02300, France (FRA)
  Expires: 12/31/2026  Operations: API MANUFACTURE
  Agent: 139242874 - Registrar Corp - drugs@registrarcorp.com - 1-757-224-0177

FEI: 0000000405  DUNS: 986154341  VANTIVE MANUFACTURING LIMITED
  Moneen Road, Castlebar, County Mayo F23 XR63, Ireland (IRL)
  Operations: ANALYSIS; API MANUFACTURE; LABEL; MANUFACTURE; PACK; STERILIZE
```

**Key fields for this company's use:**
- `FEI_NUMBER` = FDA Establishment Identifier — the primary facility identifier in NDA/ANDA submissions and enforcement records. Cross-references IDS, warning letters, import alerts.
- `DUNS_NUMBER` = Dun & Bradstreet number — links to commercial databases.
- `OPERATIONS` — includes values such as `API MANUFACTURE`, `MANUFACTURE`, `ANALYSIS`, `LABEL`, `PACK`, `STERILIZE`. Use this field to filter to API manufacturers for a candidate compound.
- `AGENT_DETAILS` — for foreign establishments, shows the US Agent name, FEI, email, phone. Required by 21 U.S.C. §510(g)(1).
- `EXCLUSION_FLAG` — `N` = active registration; `E` = excluded (in the excluded zip). The excluded zip contains 21 records as of 2026-08-05 (NEWLY VERIFIED 2026-08-06: `drls_excluded.txt` = 22 lines including header = 21 exclusion records). Examples: Jiangsu Baozong & Baoda Pharmachem (China), Spencer Specialty Products (US), Wuhan Longke Biotechnology (China).

**How to use DECRS to screen API manufacturers:** Download `drls_reg.zip`, filter `OPERATIONS` for `API MANUFACTURE`, then match the API name or compound against known manufacturers in the `FIRM_NAME` or `ADDRESS` column. This tells you which sites have an active FDA registration — a prerequisite for being named in an NDA/ANDA. It does NOT confirm GMP compliance or a DMF.

**Update cadence.** The `last-modified` headers show 2026-08-05 07:15 UTC. The DECRS page `dateModified` in schema.org is `2026-02-05-00:00`. The zip files are regenerated more frequently than the page. Treat as refreshed at least monthly, practically closer to daily.

**Auth / licence.** Public domain, no key required, no stated rate limit on the zips. Redistribution not restricted (federal government open data).

---

## 2. Drug Master Files (DMFs) — Type II API

**What DMFs are.** A Drug Master File is a submission to FDA that may be used to provide confidential, detailed information about facilities, processes, or articles used in the manufacturing, processing, packaging, and storing of human drugs. The holder submits once; sponsors of NDAs/ANDAs then "reference" the DMF by its number in their application, granting FDA the right to review it. The DMF holder does not need to disclose proprietary process information to the applicant.

**Type II DMFs specifically.** Type II DMFs cover Drug Substance (API), Drug Substance Intermediate, and Material Used in Their Preparation, or Drug Product. For this company, Type II = the list of manufacturers who already hold an FDA-referenceable filing for a given API. Finding an existing Type II DMF holder for your candidate drug means you can name their site in your NDA without the holder having to re-submit.

**FDA's primary DMF information page.** Multiple URLs attempted; the canonical page URL at `https://www.fda.gov/drugs/drug-approvals-and-databases/drug-master-files-dmfs` returned **HTTP 404** on all attempts (2026-08-05). The alternate `https://www.fda.gov/drugs/development-approval-process-drugs/drug-master-files-dmfs` also returned **HTTP 404**. The eDMF page `https://www.fda.gov/drugs/electronic-regulatory-submission-and-review/electronic-drug-master-files` returned HTTP 200 but had no DMF list links.

**DMF searchable database (Drugs@FDA DAF).** URL `https://www.accessdata.fda.gov/scripts/cder/daf/index.cfm?event=dmflist.page` returned **HTTP 200** (NEWLY VERIFIED 2026-08-06). However, the page renders as a JavaScript-heavy application ("Drugs@FDA: FDA-Approved Drugs") and the agent could not extract DMF list content from the curl response — the actual list is rendered client-side. The URL `https://www.accessdata.fda.gov/scripts/cder/daf/index.cfm?event=drug.page` also returned HTTP 200.

**Quarterly bulk DMF list — not found.** The agent exhaustively tried the following URLs, all returning **HTTP 404**:
- `https://www.accessdata.fda.gov/cder/dmf.zip`
- `https://www.accessdata.fda.gov/cder/dmflist.zip`
- `https://www.accessdata.fda.gov/cder/dmf_list.zip`
- `https://www.accessdata.fda.gov/cder/dmf_list.txt`
- `https://www.accessdata.fda.gov/cder/dmflist.txt`
- `https://www.accessdata.fda.gov/cder/fo/dmfs_quarterly.zip`
- `https://www.accessdata.fda.gov/cder/dmfs_quarterly.zip`
- Multiple `https://www.fda.gov/media/{id}/download` attempts (75009, 75010, 121468, 121469, 121470, 112148 — all 404; 75647 = image, not DMF)
- `https://www.fda.gov/media/137303/download` returned **HTTP 200, content-type: application/pdf, 132,555 bytes** — but this is a COVID-19 EUA letter for SD BIOSENSOR (device), not a DMF list (NEWLY VERIFIED 2026-08-06).

**Practical access path.** No publicly downloadable bulk DMF list was found. Access is via:
1. The DAF search tool at `https://www.accessdata.fda.gov/scripts/cder/daf/index.cfm?event=dmflist.page` (requires a browser or JS-capable client). Search by DMF number, holder name, or subject (API name).
2. FDA's CDER FOIA Electronic Reading Room (`https://www.fda.gov/drugs/guidance-compliance-regulatory-information/cder-foia-electronic-reading-room`) — verified HTTP 200, `dateModified: 2026-04-17`. The FOIA route can produce lists of DMF holders for a specific API but requires submission of a request.
3. Commercial databases (e.g., Orange Book, Drugs@FDA, Citeline Pharma Intelligence) that aggregate DMF holder information.

**How to use it.** For a given candidate API, search the DAF DMF tool by the INN or chemical name. If a Type II DMF exists, the holder name, DMF number, and filing date are shown. You can then contact the holder to request a letter of authorization (LoA) to reference the DMF in your NDA. This is a major shortcut vs. compiling a full CMC package from scratch.

---

## 3. Inspection Classification Database (IDS)

**What it is.** FDA's Inspections Data Dashboard, updated weekly, showing final inspection classifications: No Action Indicated (NAI), Voluntary Action Indicated (VAI), Official Action Indicated (OAI) for each project area within each inspection.

**URL.** `https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/inspection-classification-database` — VERIFIED HTTP 200, 2026-08-05. Page `datePublished: 2024-10-02`, `dateModified: 2024-09-13`. Maintained by FDA's Office of Regulatory Affairs.

**Redirect note.** `https://datadashboard.fda.gov/ora/cd/inspections.htm` returns HTTP 301 redirecting to `http://datadashboard.fda.gov/oii/cd/inspections.htm` (VERIFIED 2026-08-05).

**Critical exclusions stated on the page (verbatim):**

> "This database does not represent a comprehensive listing of all conducted inspections and should not be used as a source to compile official data. **Inspections conducted by States, pre-approval inspections, mammography facility inspections, inspections waiting for a final enforcement action, and inspections of nonclinical labs are not included.**"

This means: **PAI outcomes are not visible in IDS.** For PAI-relevant compliance history, you must use EIRs (via FOIA) or enforcement letters.

**Classification definitions (from page text, verbatim):**
- **NAI**: facility in an acceptable state of compliance; usually not issued a Form FDA-483.
- **VAI**: objectionable conditions found, but facility can voluntarily correct without formal regulatory action.
- **OAI**: significant objectionable conditions found; FDA may take regulatory action (warning letters, import alerts, consent decrees).

**Update cadence.** Weekly.

**Auth / rate limit.** Public. No API documented; the dashboard is a web interface.

**Inspection fact sheet.** `https://www.fda.gov/media/181859/download` — VERIFIED HTTP 200, `content-type: application/pdf`, 136,320 bytes (2026-08-05). Filename: `oii_inspections_fact_sheet_-_091224.pdf`.

**How to use.** Search a facility FEI or firm name to see its historical compliance classifications. OAI on a foreign API site is a major red flag for naming that site in an NDA. An NAI or VAI history at a site that manufactures your candidate API is reassuring. Remember: PAIs are not in IDS — a clean IDS record does not mean the site passed its PAI.

---

## 4. Form FDA-483 Inspection Observations

**What they are.** Form FDA-483 is issued to a firm's management at the close of an inspection when an investigator observes conditions that may violate FDA requirements. It is not a regulatory determination — the firm has 15 working days to respond with a corrective action plan before FDA assigns a final classification.

**Access route — Inspection Observations summaries (aggregate data).**
- `https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/inspection-references/inspection-observations` — VERIFIED HTTP 200, 2026-08-05. `datePublished: 2025-12-16`. Maintained by Office of Inspections and Investigations.

From the page (verbatim): "FDA investigators may issue a Form FDA 483 when, in an investigator's judgment, the observed conditions or practices indicate that an FDA-regulated product may be in violation of FDA's requirements. Spreadsheets summarizing the areas of regulation cited on FDA's system-generated 483s are available by fiscal year on the menu links on this page."

**FY 2025 download (NEWLY VERIFIED 2026-08-06):**
- `https://www.fda.gov/media/190190/download?attachment`
- HTTP **200**, `content-type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`, 215,754 bytes
- Filename: `inspection_observations_fiscal_year_2025_0.xlsx`
- Tabs: Biologics, Drugs, Devices, Human Tissue for Transplantation, Radiological Health, Foods, Veterinary Medicine, Bioresearch Monitoring, Special Requirements, Total.

Note (verbatim from the page): "These spreadsheets are not a comprehensive listing of all inspectional observations but represent the area of regulation and the number of times it was cited as an observation on a Form FDA 483 during inspections conducted by FDA and its representatives. Inspectional observations reflect data pulled from FDA's electronic inspection tools. These tools are used to generate the Form FDA 483 when necessary. Not all Form FDA 483s are generated by these tools as some 483s are manually prepared."

**Access to individual 483 documents.** Individual 483s are available through:
1. **OII FOIA Electronic Reading Room** (`https://www.fda.gov/about-fda/office-inspections-and-investigations/oii-foia-electronic-reading-room`) — VERIFIED via redirect from `https://www.fda.gov/ora-foia-electronic-reading-room`, 2026-08-05. Contains records "redacted to remove non-public information (see 21 CFR Part 20)." Contact for accessibility issues: `OIIFOIAInquiries@fda.hhs.gov`.
2. **FOIA request** — formal FOIA to obtain specific 483s not yet in the reading room. Submit at `https://www.fda.gov/regulatory-information/freedom-information/how-make-foia-request`.

The OII page states: "For publicly available OII data sets, (such as lists of inspection classifications, 483 observations, etc.), please visit the data sets page."

---

## 5. Warning Letters

**Primary page.** `https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/compliance-actions-and-activities/warning-letters` — VERIFIED HTTP 200, 2026-08-05. `datePublished: 2025-09-25`. Maintained by Office of the Commissioner.

**Bulk download — XLSX (VERIFIED 2026-08-05):**
- `https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/compliance-actions-and-activities/warning-letters/datatables-data?page&_format=xlsx`
- HTTP **200**, `content-type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`, 53,121 bytes, filename `warning-letters.xlsx`

There is also a batch version linked from the page:
- `/inspections-compliance-enforcement-and-criminal-investigations/compliance-actions-and-activities/warning-letters/batch/datatables-data?page&_format=xlsx`

**How to use.** Warning letters referencing a specific FEI or firm name identify serious GMP deficiencies. A manufacturing site named in a warning letter that references CGMP violations is at high risk of Import Alert 66-40 placement and should be avoided until remediated (FDA typically requires demonstrated corrections before releasing from DWPE).

---

## 6. Import Alerts — Import Alert 66-40 (Drug GMP Detention Without Physical Examination)

**What Import Alert 66-40 is (NEWLY VERIFIED 2026-08-06).** Physical URL: `https://www.accessdata.fda.gov/cms_ia/importalert_189.html` (not the frequently cited but nonexistent `.../importalert_66.html`).

Full title: **"Detention Without Physical Examination of Drugs From Firms Which Have Not Met Drug GMPs"**

Published date shown on page: **2026-08-05** (updated continuously). Type: **DWPE** (Detention Without Physical Examination).

**Key text from the alert (verbatim, updated July 15, 2025 revision):**

> "As part of FDA's activities intended to protect the health and safety of US consumers, FDA performs foreign inspections and remote regulatory assessments of pharmaceutical establishments engaged in the manufacture, processing, packing, or holding of drugs or drug products intended for sale in the US. Detention without physical examination may be appropriate when information has revealed that a firm is not operating in conformity with current good manufacturing practice requirements (CGMP)."

> "Divisions may detain, without physical examination, the indicated drugs or drug products from the foreign establishments on the Red List of this Import Alert."

> "Detention without physical examination may be appropriate when an FDA inspection, remote regulatory assessment, or inspection conducted by foreign or other government authorities under a Memorandum of Understanding or other agreement reveals that an establishment is not operating in conformity with CGMPs."

> "Release of Articles Subject to Detention without Physical Examination under This Import Alert: In order to secure release of an entry detained pursuant to this Import Alert, the owner, consignee, and/or other responsible party for the affected goods should provide documentation to the FDA Division compliance office to demonstrate that [the violations have been corrected]."

**Companion alert (found at accessdata page 190):** Import Alert 66-41 covers a related but distinct category.

**URL disambiguation for import alerts.** The system at `https://www.accessdata.fda.gov/cms_ia/importalert_{N}.html` maps page numbers to alert IDs that do not match. Working URLs found:
- `importalert_189.html` = Import Alert 66-40 (DWPE for drug GMP non-compliance) — **200**
- `importalert_190.html` = Import Alert 66-41 — **200**
- `importalert_130.html` = Import Alert 53-06 — **200**
All other numbers tried (16, 17, 18, 66, 100, 140, 150, 160, 170, 200, 1) returned **404**.

The import alert search system at `https://www.accessdata.fda.gov/scripts/importalerts/importalert.cfm` returned **404** (2026-08-05).

**How to check if a site is on Import Alert 66-40.** Use the "Red List" link from the 66-40 page, which is a searchable table of firm names and FEI numbers. A site on the Red List cannot ship API to the US without providing evidence of GMP compliance to FDA — this effectively blocks it from being named in an NDA unless and until FDA removes it from the list.

---

## 7. openFDA Enforcement and Recall API

**API endpoint.** `https://api.fda.gov/drug/enforcement.json`

**Live test result (VERIFIED 2026-08-05):**
```json
{
  "disclaimer": "Do not rely on openFDA to make decisions regarding medical care...",
  "last_updated": "2026-07-29",
  "results": {
    "total": 17860
  }
}
```
Total drug enforcement/recall records as of last update: **17,860**.

**Available fields per record (from live API response):**
`status`, `city`, `state`, `country`, `classification` (Class I/II/III), `openfda`, `product_type`, `event_id`, `recalling_firm`, `address_1`, `address_2`, `postal_code`, `voluntary_mandated`, `initial_firm_notification`, `distribution_pattern`, `recall_number`, `product_description`, `product_quantity`, `reason_for_recall`, `recall_initiation_date`, `center_classification_date`, `termination_date`, `report_date`, `code_info`.

**Bulk download (VERIFIED 2026-08-05, from `https://api.fda.gov/download.json`):**

| Dataset | File | Records | Size |
|---------|------|---------|------|
| `drug/enforcement` | `https://download.open.fda.gov/drug/enforcement/drug-enforcement-0001-of-0001.json.zip` | 17,860 | 3.80 MB |
| `drug/drugsfda` | `https://download.open.fda.gov/drug/drugsfda/drug-drugsfda-0001-of-0001.json.zip` | 29,255 | 8.94 MB |
| `drug/orangebook` | `https://download.open.fda.gov/drug/orangebook/drug-orangebook-0001-of-0001.json.zip` | 48,502 | 2.34 MB |
| `drug/label` | 14 partitions, `https://download.open.fda.gov/drug/label/drug-label-{0001..0014}-of-0014.json.zip` | ~280,000 total | ~130–145 MB each |

Export date on all: **2026-08-05**.

**Auth.** No API key required for up to 1,000 requests/day per IP. For higher volume: register free key at `https://open.fda.gov/apis/authentication/`.

**Rate limit.** 40 requests/minute without key; 240/minute with key.

**Licence.** CC0 (public domain).

**How to use for manufacturing due diligence.** Query by `recalling_firm` or FEI (via the `openfda.manufacturer_name` field) to see whether a manufacturing site has had drug recalls. Combine with the enforcement XLSX from warning letters and IDS to build a compliance profile of a prospective API manufacturer.

---

## 8. Establishment Inspection Reports (EIRs) — FOIA Route

EIRs are the full written record of an inspection, created by the FDA investigator after completing an inspection. They contain far more detail than the IDS classification or a Form 483. They are not automatically public but can be obtained via FOIA.

**Access.** Submit a request at `https://www.fda.gov/regulatory-information/freedom-information/how-make-foia-request`. Specify the firm name, FEI, and approximate inspection date. Frequently requested EIRs may appear in the relevant center reading room.

**Reading rooms (VERIFIED 2026-08-05):**
- CDER FOIA Electronic Reading Room: `https://www.fda.gov/drugs/guidance-compliance-regulatory-information/cder-foia-electronic-reading-room` — HTTP 200, `dateModified: 2026-04-17`.
- OII FOIA Electronic Reading Room: `https://www.fda.gov/about-fda/office-inspections-and-investigations/oii-foia-electronic-reading-room` — VERIFIED via redirect from `/ora-foia-electronic-reading-room`, 2026-08-05. Contact: `OIIFOIAInquiries@fda.hhs.gov`.

**Division of Freedom of Information mailing address (from warning letters page, verbatim):** "Food and Drug Administration Division of Freedom of Information (HFI-35), 5630 Fishers Lane, Rockville, MD 20857."

**Practical note.** FOIA for a recent EIR can take weeks to months. For urgent due diligence on a prospective manufacturing partner, a faster path is to ask the site directly for copies of its most recent EIR and any 483 responses — sites with clean records typically share voluntarily.

---

## 9. Global Facility Identifiers: FEI and DUNS

**FDA Establishment Identifier (FEI).**
- Assigned by FDA to each manufacturing establishment.
- Appears in DECRS (`FEI_NUMBER` column), in NDA/ANDA submissions, in warning letters, import alerts, and the IDS.
- Format: 10-digit zero-padded number (e.g., `0000000360`).
- To look up an FEI for a facility, search DECRS or use the FDA's registration and listing system at `https://www.accessdata.fda.gov/scripts/cder/drls/default.cfm`.
- Cross-reference: FEI → IDS inspection history, warning letters, import alerts, openFDA enforcement records.

**DUNS Number.**
- Dun & Bradstreet global business identifier.
- Appears in DECRS (`DUNS_NUMBER` and `REGISTRANT_DUNS` columns).
- Enables cross-referencing FDA registrations with commercial databases (D&B, SAM.gov for US government contracts, etc.).
- From the sample DECRS records: Vantive Manufacturing Limited (Ireland) has DUNS 986154341; Alps Pharmaceutical Ind. (Japan) has DUNS 690535893.

---

## 10. FDA Compliance Programs Relevant to Manufacturing

The Compliance Program Manual at `https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/compliance-manuals/compliance-program-manual` (VERIFIED HTTP 200, 2026-08-05) lists all compliance programs. Programs most relevant to this company's manufacturing due diligence:

| Program | Title | PDF (from CDER compliance page) |
|---------|-------|-------------------------------|
| **7346.832** | Preapproval Inspections (PAIs) | `https://www.fda.gov/media/193382/download?attachment` (HTTP 200, 657,512 bytes) — new version; also `https://www.fda.gov/media/121512/download?attachment` (HTTP 200, 709,966 bytes) — earlier version |
| 7346.832M | Prelicense/Preapproval Inspections of CDER-Regulated Biological Product Manufacturers | — |
| 7356.002 | Drug Manufacturing Inspections | — |
| **7356.002F** | Active Pharmaceutical Ingredients | — |
| 7356.002A | Sterile Drug Process Inspections | — |
| 7356.002B | Drug Repackers and Relabelers | — |

VERIFIED from `https://www.fda.gov/drugs/guidance-compliance-regulatory-information/drug-compliance-programs` (HTTP 200, 2026-08-05). The page lists these programs verbatim.

---

## 11. Pre-Approval Inspections (PAIs): Policy Verification

**The claim to check:** "FDA does not inspect a manufacturing facility until the NDA stage."

**Verdict: FALSE as a blanket statement; TRUE in a narrow colloquial sense with important nuance.**

### What the primary source actually says

**Source: FDA Compliance Program 7346.832 — Preapproval Inspections**, issuance date 10/17/2022 (implementation version), downloaded from `https://www.fda.gov/media/121512/download?attachment`, 709,966 bytes. Downloaded and text-extracted 2026-08-05.

**When PAIs are triggered — verbatim from CP 7346.832 (Part II, Section A, "Risk-Based Determination for PAI"):**

> "This revised compliance program reinforces FDA's risk-based approach to determine whether inspections are needed using information provided in applications and information FDA may have regarding the facilities. **If FDA finds that sufficient information is available, a PAI may not be needed.** When a marketing application is submitted, CDER initiates the preapproval facility evaluation by assembling an IQA team to perform the quality assessment."

> "In performing the quality assessment, the IQA team determines the need for PAIs of facilities listed in the application by assessing: (1) Product risk and manufacturing (process and facility) risks; (2) The accuracy and reliability of the information provided in the application."

> "A PAI can be triggered when there is a need to confirm the accuracy and reliability of the quality data, which is critical in determining the safety, efficacy, and quality of the drug product. Additionally, a PAI can be triggered to confirm that a facility's operations match those proposed in the application."

**The "Scope" section (verbatim):**

> "Preapproval facility evaluations and inspections support the assessment of marketing applications by ensuring that any establishment named in or referenced in support of an application can perform the proposed manufacturing operations in conformance with CGMP requirements and that data submitted in the application are accurate and complete."

> "Preapproval facility evaluation: CDER, with ORA participation, considers information about each facility named in a marketing application, the drug being manufactured, and other information in the application to determine whether a PAI is needed before the application can be approved from a quality perspective."

> "Preapproval inspection: ORA, with CDER participation, evaluates the adequacy of the manufacturing processes and control strategy to ensure commercial product quality and conformance to application, facility, and CGMP requirements."

**When PAI is mandatory / likely triggered.** The "Inspection by Objective" section (Part II, Section B) lists four PAI objectives and states:

| Objective | Coverage trigger |
|-----------|-----------------|
| Objective 1: Readiness for Commercial Manufacturing | When determining whether to cover, consider: **"The facility has never been inspected."** Also: new building/equipment never inspected, major changes since last inspection, special containment required. |
| Objective 2: Conformance to Application | **Cover on every PAI.** |
| Objective 3: Data Integrity Audit | **Cover on every PAI.** |
| Objective 4: Commitment to Quality | Cover on initial PAI; periodically on subsequent PAIs. |

**The "never been inspected" factor is explicit.** A foreign API site that FDA has never previously inspected is a specific risk factor for triggering Objective 1 coverage.

**Timeline.** From the Program Management Instructions (Part II):

> "Within 60 calendar days of receiving an NDA or ANDA, OPMA sends a PAI or DFR request to ORA or enters a facility recommendation via Panorama."

> "A PAI should be requested and performed at the earliest opportunity, well before the user fee goal date."

**DFR = Decision to Forego Inspection.** OPMA can request a DFR (alternative to PAI request). ORA has 10 business days to respond: approve facility, withhold approval, or escalate to PAI. If ORA recommends withhold or PAI, OPMA makes the final recommendation.

**Summary of the correct characterization:**
- FDA does NOT routinely inspect facilities *before* an NDA is submitted.
- PAI is triggered *during* NDA review, typically within 60 days of application receipt.
- A PAI is not automatic: it is risk-based and may be foregone (DFR) if FDA has sufficient prior information.
- A facility that FDA has **never inspected** is a specific risk factor that makes a PAI likely.
- "Does not inspect until NDA stage" is approximately correct as a description of timing, but it does NOT mean "never inspects" — it means the inspection is triggered by the NDA submission.

### Can a foreign API site with only WHO GMP (not FDA) be named in an NDA?

**Directly addressed in CP 7346.832 (Part I background section, text extracted 2026-08-05):**

> FDA may rely on foreign regulatory partners through: "(1) requesting existing inspection reports from trusted foreign regulatory partners through mutual recognition agreements (MRAs) and other confidentiality agreements; and (2) conducting remote regulatory assessments (RRAs)..."

**The MRA point is critical.** FDA has MRAs with the EU, Canada, Switzerland, Australia, Japan, UK, Israel. Under these MRAs, FDA can request and rely on inspection reports from those regulators' GMP inspections. **WHO GMP certification (WHO Prequalification) is not an MRA partner — WHO is not in FDA's MRA network.** Therefore:

- A site with only WHO GMP certification can be named in an NDA, but FDA will not be able to rely on WHO's inspection to waive its own PAI.
- Such a site should be treated as "never been inspected" by FDA — triggering Objective 1 coverage and making a PAI highly likely.
- The acronym list in CP 7346.832 includes `MRA: mutual recognition agreement` but not WHO. WHO is not mentioned as a trusted inspection partner.

**ConOps Q&A page (VERIFIED 2026-08-05).** `https://www.fda.gov/drugs/pharmaceutical-quality-resources/questions-and-answers-integration-fda-facility-evaluation-and-inspection-program-human-drugs-concept` — HTTP 200, `datePublished: 2026-01-22`. The Q8 answer confirms: "Manufacturers are responsible for ensuring that their products are manufactured to meet all of the quality standards and in accordance with the current good manufacturing practice (CGMP) regulations. The ConOps promotes transparency and communication between the agency and industry for facilities involved in manufacturing human drugs."

**Bottom line for this company:** A foreign API manufacturer with only WHO GMP should be assumed to require a US FDA PAI before NDA approval. Plan for 6–18 months from NDA submission to PAI completion as a conservative estimate.

---

## 12. Pharmaceutical Inspections and Compliance — General

**FDA's CGMP inspections page.** `https://www.fda.gov/drugs/guidance-compliance-regulatory-information/pharmaceutical-inspections-and-compliance` — VERIFIED HTTP 200, 2026-08-05. `datePublished: 2024-12-05`. Text (verbatim from extracted content):

> "All Drugs Manufactured for the U.S. Market Must Meet FDA's Rigorous Standards... All drugs manufactured for the U.S. market, whether manufactured domestically or abroad, must meet the same rigorous standards."

**Types of FDA Inspections page.** `https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/inspection-basics/types-fda-inspections` — VERIFIED HTTP 200, 2026-08-05. `datePublished: 2024-09-13`.

---

## Unfinished — Worth Re-running

1. **Type II DMF quarterly list / bulk download.** The agent exhausted plausible direct-download URLs. No bulk-downloadable DMF list was found. **Re-run recommended:** Try loading `https://www.accessdata.fda.gov/scripts/cder/daf/index.cfm?event=dmflist.page` with a JavaScript-capable browser (Playwright/Puppeteer) to extract the actual DMF search results for specific APIs of interest. Alternatively, submit a FOIA to CDER for a list of Type II DMFs for the compound of interest.

2. **Import Alert 66-40 Red List.** The agent found the 66-40 alert page but died before extracting the full Red List of manufacturers. The Red List is embedded as a sortable table on `https://www.accessdata.fda.gov/cms_ia/importalert_189.html`. **Re-run recommended:** Load with latin-1 decoding (the page caused a UTF-8 decode error at 121,908 bytes), extract the firm name/FEI table to check whether any prospective manufacturing partners are blocked.

3. **CP 7356.002F (Active Pharmaceutical Ingredients) inspection program.** The link to this compliance program PDF was not verified — the CDER drug compliance programs page lists it but the PDF URL was not extracted. **Re-run recommended:** Fetch `https://www.fda.gov/drugs/guidance-compliance-regulatory-information/drug-compliance-programs`, extract the 7356.002F link, and retrieve the PDF to understand how FDA inspects API-only sites (which differ from finished drug manufacturers).

4. **IDS (Inspection Classification Database) downloadable datasets.** The IDS page mentions "data sets" but the agent did not find a direct bulk download URL. **Re-run recommended:** Locate the bulk download via `https://www.fda.gov/drugs/drug-safety-and-availability/fda-drug-safety-podcast` or the OII data sets page linked from the OII FOIA reading room.

5. **FY 2024 and FY 2023 inspection observation spreadsheets.** Only FY 2025 was confirmed. The pattern `https://www.fda.gov/media/{id}/download?attachment` was used for FY 2025 (id=190190). FY 2024 and FY 2023 URLs were not found — page scraping of the inspection observations index would yield prior-year media IDs.

---

## URL Ledger

### VERIFIED

| URL | HTTP | Notes |
|-----|------|-------|
| `https://www.fda.gov/drugs/drug-approvals-and-databases/drug-establishments-current-registration-site-decrs` | 200 | DECRS landing page |
| `https://www.accessdata.fda.gov/scripts/cder/drls/default.cfm` | 200 | DECRS interactive search |
| `https://www.accessdata.fda.gov/cder/drls_reg.zip` | 200 | DECRS bulk download (10,394 establishment records, 2.39 MB compressed, last-modified 2026-08-05) |
| `https://www.accessdata.fda.gov/cder/drls_excluded.zip` | 200 | DECRS excluded firms (21 records, 5.3 KB compressed, last-modified 2026-08-05) |
| `https://www.accessdata.fda.gov/scripts/cder/daf/index.cfm?event=dmflist.page` | 200 | DMF list search (JS-rendered; returns Drugs@FDA shell) |
| `https://www.accessdata.fda.gov/scripts/cder/daf/index.cfm?event=drug.page` | 200 | Drugs@FDA search |
| `https://www.fda.gov/drugs/guidance-compliance-regulatory-information/cder-foia-electronic-reading-room` | 200 | CDER FOIA reading room |
| `https://www.fda.gov/about-fda/office-inspections-and-investigations/oii-foia-electronic-reading-room` | 200 | OII FOIA reading room (483s and EIRs) |
| `https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/inspection-classification-database` | 200 | Inspection Classification Database / IDS |
| `https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/inspection-references/inspection-observations` | 200 | Form 483 observations index |
| `https://www.fda.gov/media/190190/download?attachment` | 200 | Inspection observations FY 2025 XLSX (215,754 bytes) |
| `https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/compliance-actions-and-activities/warning-letters` | 200 | Warning letters page |
| `https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/compliance-actions-and-activities/warning-letters/datatables-data?page&_format=xlsx` | 200 | Warning letters XLSX bulk download (53,121 bytes) |
| `https://api.fda.gov/drug/enforcement.json` | 200 | openFDA enforcement API (17,860 total records, last_updated 2026-07-29) |
| `https://download.open.fda.gov/drug/enforcement/drug-enforcement-0001-of-0001.json.zip` | — | openFDA enforcement bulk (17,860 records, 3.80 MB, export 2026-08-05) |
| `https://api.fda.gov/download.json` | 200 | openFDA download manifest |
| `https://www.accessdata.fda.gov/cms_ia/importalert_189.html` | 200 | Import Alert 66-40 (DWPE for drug GMP non-compliance), last updated 2026-08-05 |
| `https://www.accessdata.fda.gov/cms_ia/importalert_190.html` | 200 | Import Alert 66-41 |
| `https://www.accessdata.fda.gov/cms_ia/importalert_130.html` | 200 | Import Alert 53-06 |
| `https://www.fda.gov/media/193382/download?attachment` | 200 | CP 7346.832 PAI (new version, 657,512 bytes, implementing 2026-08-10) |
| `https://www.fda.gov/media/121512/download?attachment` | 200 | CP 7346.832 PAI (prior version, 709,966 bytes, issuance 2022-09-16, downloaded and text-extracted) |
| `https://www.fda.gov/media/181859/download` | 200 | OII Inspections fact sheet PDF (136,320 bytes) |
| `https://www.fda.gov/drugs/guidance-compliance-regulatory-information/pharmaceutical-inspections-and-compliance` | 200 | FDA CGMP inspections overview |
| `https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/inspection-basics/types-fda-inspections` | 200 | Types of FDA inspections |
| `https://www.fda.gov/drugs/guidance-compliance-regulatory-information/drug-compliance-programs` | 200 | CDER drug compliance programs (lists 7346.832, 7356.002F, etc.) |
| `https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/compliance-manuals/compliance-program-manual` | 200 | Compliance Program Manual index |
| `https://www.fda.gov/drugs/guidance-compliance-regulatory-information/electronic-drug-registration-and-listing-system-edrls` | 200 | eDRLS information page |
| `https://www.fda.gov/drugs/pharmaceutical-quality-resources/questions-and-answers-integration-fda-facility-evaluation-and-inspection-program-human-drugs-concept` | 200 | ConOps Q&A page (PAI/inspection integration, dated 2026-01-22) |
| `datadashboard.fda.gov/ora/cd/inspections.htm` | 301 → `http://datadashboard.fda.gov/oii/cd/inspections.htm` | IDS data dashboard (redirects) |

### UNVERIFIED / NOT FOUND

| URL | Status | Note |
|-----|--------|------|
| `https://www.fda.gov/drugs/drug-approvals-and-databases/drug-establishments-current-registration-site` | 404 | Old URL, use the -decrs version |
| `https://www.fda.gov/drugs/drug-approvals-and-databases/drug-master-files-dmfs` | 404 | Dead link |
| `https://www.fda.gov/drugs/development-approval-process-drugs/drug-master-files-dmfs` | 404 | Dead link |
| `https://www.accessdata.fda.gov/cder/dmf.zip` | 404 | No bulk DMF zip found |
| `https://www.accessdata.fda.gov/cder/dmflist.zip` | 404 | Not found |
| `https://www.accessdata.fda.gov/cder/dmf_list.zip` | 404 | Not found |
| `https://www.accessdata.fda.gov/cder/dmf_list.txt` | 404 | Not found |
| `https://www.accessdata.fda.gov/cder/dmflist.txt` | 404 | Not found |
| `https://www.accessdata.fda.gov/cder/fo/dmfs_quarterly.zip` | 404 | Not found |
| `https://www.fda.gov/media/75009/download` | 404 | Guessed DMF list media ID, incorrect |
| `https://www.fda.gov/drugs/drug-approvals-and-databases/searchable-database-type-ii-api-drug-master-files` | 404 | Not found |
| `https://www.fda.gov/drugs/drug-approvals-and-databases/drug-master-file-database` | 404 | Not found |
| `https://www.fda.gov/drugs/pharmaceutical-quality-resources/pre-approval-inspections` | 404 | Dead link — use ConOps Q&A and CP 7346.832 instead |
| `https://www.fda.gov/media/75209/download` | 404 | Guessed CP 7346.832 old URL, incorrect |
| `https://www.fda.gov/drugs/pharmaceutical-quality-resources/cder-manual-policies-and-procedures-mapp-5015-6` | 404 | Not found |
| `https://www.fda.gov/safety/import-alerts` | 404 | Dead link |
| `https://www.fda.gov/safety/import-alerts/drug-import-alerts` | 404 | Dead link |
| `https://www.accessdata.fda.gov/cms_ia/importalert_16.html` | 404 | Not Import Alert 66-40 |
| `https://www.accessdata.fda.gov/cms_ia/importalert_66.html` | 404 | Counter-intuitive: 66-40 is at page 189, not page 66 |
| `https://www.accessdata.fda.gov/scripts/importalerts/importalertlist.cfm` | 404 | Dead |
| `https://www.accessdata.fda.gov/scripts/importalerts/importalert.cfm?action=detail&alertNumber=66-40` | 404 (404 response body) | Dead |
| `https://www.fda.gov/food/import-alerts/import-alert-66-40` | 404 | Wrong center (food); drug alerts use accessdata |
| `https://www.fda.gov/media/148705/download` | 404 | Not found |
| `https://www.fda.gov/drugs/forms-submission-requirements/drug-master-files` | 404 | Dead link |
| `https://www.fda.gov/about-fda/about-center-drug-evaluation-and-research/frequently-requested-drug-information-cder` | 404 | Dead link |
