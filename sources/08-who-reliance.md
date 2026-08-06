<!-- RECOVERED from subagent transcript agent-a0d83a17d545ed5b4.jsonl, session fd64561f-7c90-41a2-95cf-b4a133a8fe0f, research date 2026-08-05.
     WHO Prequalification, EML/EMLc, Collaborative Registration Procedure, WHO-Listed Authority framework.
     Verbatim agent deliverable — not re-edited. -->

## 1. WHO Prequalification of Medical Products (PQ)

### 1.1 Which site is current in 2026 — no public-site migration
- **`https://extranet.who.int/prequal/`** is still the live public PQ site as of Aug 2026 (Drupal). **VERIFIED** (HTTP 200). There has been **no migration of the public lists** to who.int.
- What *did* change: **ePQS** (Salesforce-based e-Prequalification System) is the **submission** portal, opened to external users 19 May 2025 and **mandatory from 11 May 2026**. Public read-only lists stayed on the extranet.
  - `https://extranet.who.int/prequal/epqs/epqs-portal` — **VERIFIED**
  - `https://extranet.who.int/prequal/epqs/ectd-portal` (eCTD submission) — **VERIFIED** (linked from site nav)
- Programme fact sheet (last updated **11 June 2026**): >1,700 health products WHO-listed across all streams as of end-2025; >40% of prequalified medicines and 50% of vaccines now made by LMIC manufacturers. `https://www.who.int/news-room/fact-sheets/detail/prequalification-of-medicines-by-who` — **VERIFIED**

### 1.2 Machine-readable list downloads (this is the good part — Drupal Views CSV export)

Every list page exposes a `.../export?page&_format=csv` endpoint. **No auth, no key, no rate limit observed. `_format=json` and `_format=xml` return HTTP 406 — CSV only.**

| Data | Endpoint | Status | Content |
|---|---|---|---|
| **Prequalified FPPs + biotherapeutics** | `https://extranet.who.int/prequal/medicines/prequalified/finished-pharmaceutical-products/export?page&_format=csv` | **VERIFIED** 200, `text/csv`, 131 KB | **656 products.** Cols: WHO Reference Number, INN/Dosage Form/Strength, Product Type, Therapeutic Area, Applicant, Dosage Form, **Basis of Listing**, **Basis of alternative listing**, Date of Prequalification |
| **Prequalified APIs** | `https://extranet.who.int/prequal/medicines/prequalified/active-pharmaceutical-ingredients/export?page&_format=csv` | **VERIFIED** 200, 23 KB | Cols: WHO Product ID (`WHOAPI-nnn`), INN, Grade, Therapeutic area, Applicant, Date of PQ, Confirmation of PQ Document Date |
| **Prequalified vaccines** | `https://extranet.who.int/prequal/vaccines/prequalified/export?page&_format=csv` | **VERIFIED** 200, 48 KB | **282 vaccine presentations.** Cols: Date of PQ, Vaccine Type, Commercial Name, Presentation, No. of doses, Manufacturer, Responsible NRA |
| **Prequalified QC labs** | `https://extranet.who.int/prequal/medicines/prequalified/quality-control-labs/export?page&_format=csv` | **VERIFIED** 200, 7.6 KB | 66 labs. Title, Applicant Org, Date of PQ, Country, Region |
| **Prequalified vector control products** | `https://extranet.who.int/prequal/vector-control-products/prequalified-product-list/export?page&_format=csv` | **VERIFIED** 200, 30 KB | PQT/VC Ref, Product Name, Applicant, Type, AI/Synergist, Date, Links |
| **Prequalified IVDs** | `https://extranet.who.int/prequal/vitro-diagnostics/prequalified-vitro-diagnostics` | **VERIFIED** page 200; **no CSV export link found** | Scrape only |

**HTML list pages** (all **VERIFIED**): FPPs `.../medicines/prequalified/finished-pharmaceutical-products`; APIs `.../medicines/prequalified/active-pharmaceutical-ingredients`; vaccines `https://extranet.who.int/prequal/vaccines/prequalified-vaccines` (alias `.../vaccines/list-prequalified-vaccines` also 200); index `https://extranet.who.int/prequal/medicines/prequalified-lists`.

**Server-side filters** (usable on both the HTML view and the CSV export): `field_sf_subtype_target_id`, `field_sf_date_prequalification_value`, `field_sf_therapeutic_areas_target_id`, `field_sf_generic_name_value`, `field_sf_assessment_procedure_target_id`, `page`.

**Gotchas:** CSV is a full-table dump regardless of `page`; dates are human-formatted with double spaces (`"27  May,  2014"`); vaccine dates are `DD/MM/YYYY` while API dates are `D Mon, YYYY` — parse per-file. `Basis of Listing` is the field that tells you whether a listing was full assessment vs. **"Alternative Listing"** via an SRA (e.g. `"USFDA - PEPFAR"`) — critical for CRP routing (see §3). **No update-cadence header, no ETag discipline, no changelog** — poll the CSV and diff. Updates are rolling (news items show FPP list updates several times per year).

### 1.3 WHOPARs (WHO Public Assessment Reports)
- Index: `https://extranet.who.int/prequal/medicines/prequalification-reports/whopars` — **VERIFIED** (4.1 MB single HTML page, **588 WHOPAR entries**, no pagination, no CSV export).
- Detail page pattern: `https://extranet.who.int/prequal/WHOPAR/{ref}` where `{ref}` is lowercase therapeutic-area code + number. **VERIFIED** on `ha060`. Prefix distribution: `ha` 177 (HIV), `tb` 132, `ma` 102 (malaria), `rh` 64, `cv` 20, `hp` 19, `bt-on` 18 (oncology biotherapeutics), `nt` 17, `in` 13, `di` 6, `bt-dm` 6, `td` 5, `ap` 3, `bt-eb`/`bt-cv` 2, `mr`/`bt-dx` 1.
- **PDF pattern:** `https://extranet.who.int/prequal/sites/default/files/whopar_files/{REF}part{N}v{V}.pdf` — e.g. `HA060part1v3.pdf` … `HA060part8v3.pdf`. **VERIFIED**. Version suffix `v{V}` is unpredictable per part — you must scrape the detail page for the exact filename; you cannot construct it.
- **Parts:** 1 Abstract · 2 All accepted presentations (incl. photo) · 3 WHO-PQ recommended PIL · 4 WHO-PQ recommended SmPC · 5 Label · 6 Discussion (status at time of PQ) · 7 Steps before PQ · 8 Steps following PQ.
- **WHOPIRs** (inspection reports): `https://extranet.who.int/prequal/inspection-services/whopirs` — **VERIFIED**, no CSV export. Posted only for sites that passed.
- **Gotcha for reliance filings:** WHOPARs/WHOPIRs are posted *after* listing (contents must be agreed with the manufacturer, redacting proprietary info). For products prequalified via the **abridged SRA route**, the SRA-approved product information is *not* rewritten — it goes into parts 3/4/5 verbatim, or part 1 just links to the reference SRA's website; WHO then adds *supplemental* PQT/MED-recommended clinical/preclinical text based on WHO treatment guidelines. Guidance note (19 Mar 2025): `https://extranet.who.int/prequal/sites/default/files/document_files/20250318_2-Note%20PQ%20Website%20for%20SRA-WHOPARs_0.pdf` — **VERIFIED**. That note also says: *when supplying a PQ'd medicine to a country, if the NMRA asks, the supplier should use WHO's recommended text as the basis for local product information.*

### 1.4 Expressions of Interest (EOI) — the hard gate for a rare-disease repurposer
Page: `https://extranet.who.int/prequal/medicines/fpps-apis-eligible-prequalification-eois` — **VERIFIED**.

> "The **first step** in the prequalification process of an FPP or API is its inclusion in an Invitation to Manufacturers to Submit an Expression of Interest (EOI). … **Generally, every product contained in an EOI is already included in the WHO Model List of Essential Medicines** … and/or in WHO treatment or other relevant guidelines."

**This is the structural blocker.** WHO PQ is scoped by disease-programme priority, not by unmet need. Exceptions are explicitly limited to public health emergencies. A repurposed rare-disease asset is essentially un-prequalifiable unless it lands on the EML or in a WHO guideline first (→ §2 is not a nice-to-have; it is the prerequisite). EOIs are issued by WHO after consultation with WHO disease programmes/clinical specialists — there is **no published applicant-initiated route to add a product to an EOI**; the practical channel is `prequalinfo@who.int` / the medicines key-contacts page and the relevant disease programme.

**Open EOIs for FPPs (18 therapeutic areas, current as of the page):** apnoea in preterm infants · bacterial infections in children · COVID-19 · diarrhoeal disease · Ebola · hepatitis B & C · HIV/AIDS · influenza · malaria · diabetes management · human insulin & insulin analogues · rituximab & trastuzumab · MDR bacterial infections · NTDs · reproductive health · TB · TB skin tests · tobacco use disorders · substance use disorders.

Key EOI PDFs (**VERIFIED via the page's link list**; URL-encode the spaces):
- API, 41st, 26 May 2026 — `https://extranet.who.int/prequal/sites/default/files/document_files/41st%20Invitation%20for%20API%20EOI%20v1.0.pdf`
- TB FPPs, 23rd, 24 Feb 2026 — `.../document_files/EOI_TB_v23_final2026-2-24%20%282%29.pdf`
- Malaria, 24th, 27 Feb 2026 — `.../document_files/EOI-MalariaV24_2.pdf`
- HIV/AIDS, 23rd, 9 Jul 2025 — `.../document_files/EOI_23rd%20HIV_9July_2025_clean_PQ.pdf`
- Diabetes, 3rd, 18 May 2026 — `.../document_files/EOI%20-%20medicines%20for%20managment%20of%20diabetes_18%20May%202026%20%28002%29-revised.pdf`
- Substance use disorders, 1st, 22 May 2026 — `.../document_files/EOI%20substanceusedisorders%2022%20May%202026%20%282%29.pdf`
- NTDs, 9th, 29 Oct 2024 — `.../document_files/Annex_EOI-NTD-v9_15Oct2024_minor%20revision.pdf`

No CSV/JSON index of EOIs; scrape the page (link text carries edition number + date). Documents A-Z (all medicines docs incl. EOIs): `https://extranet.who.int/prequal/key-resources/documents/medicines/all` — **VERIFIED**.

### 1.5 Abridged / reliance PQ pathway for SRA-approved products
- Overview: `https://extranet.who.int/prequal/medicines/sra-approved-multisource-generic-or-innovator-fpps` — **VERIFIED**
- Submission procedure: `https://extranet.who.int/prequal/medicines/submission-procedure-sra-approved-multisource-generic-or-innovator-fpps` — **VERIFIED**
- API equivalents: `.../medicines/abridged-assessment-api-accepted-previously-authority-applying-stringent-standards` (**VERIFIED**) and `.../medicines/abridged-assessment-apimf-assessed-previously-using-apimf-procedure`
- Mechanics: WHO does **not** re-assess the SRA's underlying data. Requires (a) SRA approval, (b) applicant willingness to let WHO obtain/share the SRA package, (c) **product must still be invited via an EOI**. Deliverables: **QIS-SRA** template, stability data for WHO climatic zones, and any extra data for WHO-relevant populations/settings.
  - Stability requirements (Mar 2016): `https://extranet.who.int/prequal/sites/default/files/document_files/48%20Stability%20data%20SRA%20FPPs_March2016_newtempl.pdf` — **VERIFIED**
- **Gotcha:** abridged-route products get a WHOPAR but the SRA product information is carried over unchanged (see §1.3). Products listed on an *alternative-listing* basis (e.g. USFDA-PEPFAR) are **not eligible for PQ CRP** — they must go through **SRA/WLA CRP** instead (CRP FAQ Q28).

### 1.6 Fees (from `https://extranet.who.int/prequal/medicines/prequalification-procedures-and-fees-fpps-apis-qcls` — **VERIFIED**)

| | Application (US$) | Annual (US$) | Major variation (US$) |
|---|---|---|---|
| FPP **full** assessment | 27,500 | 22,000 | 3,300 |
| FPP **abridged** assessment | **6,600** | **5,500** | n/a |
| API full assessment | 22,000 | 8,800 | — |
| API abridged assessment | 11,000 | 4,400 | — |
| APIMF | — | — | 3,300 |
| QCL | none | none | none |

- "Single product" = one strength + one dose form (multiple presentations allowed), or a co-packed combination. For APIs = one APIMF.
- Application fee invoiced **after screening/acceptance**, payable in 15 days. Annual fee invoiced on/before 1 Oct, due 30 Nov, applies to products prequalified ≥12 months as of 1 Sep.
- **Annual-fee waivers** available for low-profit products (must supply prior-year sales and net profit per product). No published effective date on the schedule — treat as current-as-of-fetch.
- **There are no WHO fees for CRP** (CRP FAQ Q4) — only the national regulatory fees.

---

## 2. WHO Model List of Essential Medicines (EML / EMLc)

### 2.1 Current edition as of Aug 2026: **24th EML / 10th EMLc (2025)**
Published **5 September 2025** by the 25th Expert Committee. Confirmed by the WHO essential medicines fact sheet **updated 26 January 2026** ("the 2025 edition"). The cycle is **biennial**; the next Expert Committee sits in 2027 → **no 2026 or 2027 list exists yet**. 523 medicines (adults) / 374 (children); 20 added to EML and 15 to EMLc in 2025.

### 2.2 Exact download URLs (all **VERIFIED**, HTTP 200, `application/pdf`)

| Item | URL | Size |
|---|---|---|
| **24th EML (2025), PDF** | `https://iris.who.int/server/api/core/bitstreams/17642505-ecd3-4940-a691-4f1dfa0d835a/content` (`B09474-eng.pdf`) | 1.36 MB |
| **10th EMLc (2025), PDF** | `https://iris.who.int/server/api/core/bitstreams/337edac2-d0aa-4e19-9d72-3acb11d09808/content` (`B09475-eng.pdf`) | 845 KB |
| **Full Expert Committee report** (contains both lists) | `https://iris.who.int/server/api/core/bitstreams/e1ba8eb2-28a4-49cb-8e97-4ae69d8af915/content` (`9789240119741-eng.pdf`) | 4.95 MB |

Landing pages: EML `https://www.who.int/publications/i/item/B09474`; EMLc `https://www.who.int/publications/i/item/B09475`; index `https://www.who.int/groups/expert-committee-on-selection-and-use-of-essential-medicines/essential-medicines-lists` — all **VERIFIED**. IRIS handles: `10665/382243` (EML), `10665/382242` (EMLc), `10665/384874` (report).

**IRIS has a real DSpace-7 REST API** and it is the reliable way to resolve any WHO publication to a stable bitstream (the `who.int/publications/i/item/...` pages are JS-rendered and unscrapeable):
- Search: `https://iris.who.int/server/api/discover/search/objects?query=<urlencoded>&size=10` (send `Accept: application/json`) — **VERIFIED**
- Bundles: `https://iris.who.int/server/api/core/items/{uuid}/bundles` → follow `_links.bitstreams.href` → `_links.content.href` is the download. **VERIFIED**
- Note: `https://iris.who.int/items/{uuid}` (the HTML item page) returns **403 to WebFetch** — use the API, not the page.
- **No official EML Excel/CSV on WHO.int or IRIS.** PDF only. The machine-readable path is the eEML (below).

### 2.3 eEML — `https://list.essentialmeds.org/` (**VERIFIED**)
- Content: **1,418 recommendations across 667 medicines + 156 therapeutic equivalents**, spanning 1977–2025. Structured by EML section hierarchy, with **ICD-11 codes, ATC codes, indication, list type (core/complementary), formulations, therapeutic alternatives, INN, medicine type, AWaRe antibiotic group, sex, age, age/weight restriction, patent information, and the Expert Committee decision justification**.
- **No JSON/REST API.** `/api`, `/api/medicines` → 404. The only XHR-ish endpoint in the JS bundle (`/build/assets/app-CimemzdQ.js`) is **`/filters`**, which returns an **HTML fragment**, not JSON. **UNVERIFIED that any JSON API exists — treat as none.**
- **Bulk export does work** — this is your machine-readable EML:
  - `https://list.essentialmeds.org/print?format=xlsx` → **VERIFIED** 200, `…spreadsheetml.sheet`, 83.7 KB
  - `https://list.essentialmeds.org/print?format=docx` → **VERIFIED** 200, 4.9 MB
  - `https://list.essentialmeds.org/print?format=pdf` → **VERIFIED** 200, 1.77 MB
  - `format=csv` → **200 but zero bytes. Not supported.**
- Real form is `POST https://list.essentialmeds.org/print?` with `format=pdf|xlsx|docx`, `preset=all|classic-layout`, and repeated `fields[]=` from: `indication, icd-11, atc-codes, list-type, formulations, therapeutic-equivalence, footnote, inn, medicine-type, antibiotic-groups, sex, age, age-restriction, weight-restriction, patent-information, justification`. **Gotcha:** a bare POST with a field subset returned the identical 83,715-byte file as the all-fields GET — field selection appears session/CSRF-bound, so **just take the full GET XLSX and filter locally**.
- Filtering in the UI (for building narrower exports): EML section, indication/diagnosis, first-added year, target population (age/sex), tags (e.g. "Cancer").
- Related: AWaRe `https://aware.essentialmeds.org/groups`; **`https://global.essentialmeds.org/` ("EMLs Around The World")** — **UNVERIFIED as a data source**: it is a SPA that returns the same 1.7 KB shell for every path (`/api/countries`, `/countries`, `/dashboard` all return the shell), and its JS bundle 404s to a plain fetch. Needs a headless browser; no documented export.

### 2.4 How EML listing propagates to national lists and procurement (why this matters in small markets)
- **>150 countries** maintain a national EML (NEML) derived from the WHO Model List (fact sheet, 26 Jan 2026). NEMLs drive **public-sector procurement, reimbursement/insurance schemes, donation acceptance, and local production priorities** — in many LMICs a medicine that is not on the NEML is effectively not purchasable with public money regardless of its marketing authorisation.
- The chain that actually matters for a repurposed rare-disease asset: **EML listing (or WHO guideline inclusion) → EOI issued → PQ eligible → PQ granted → CRP-eligible → fast national registrations across 69–71 countries → eligible for UN/donor procurement.** Skipping the first link breaks everything downstream.
- The Model List explicitly accepts applications from **researchers, NGOs, patient groups and pharmaceutical companies** — this is the one WHO gate a small company can actually walk up to unaided, and it is on a **fixed biennial cycle** (next Expert Committee 2027, so an application window in ~2026H2–2027H1).
- Procurement-side fallback if PQ is unreachable: the **Expert Review Panel (ERP)**, a time-limited risk-based clearance jointly run by WHO and the Global Fund for products that are neither PQ'd nor SRA-approved; principal users are the Global Drug Facility, the Global Fund, UNFPA, UNICEF and WHO procurement. Requires a WHO-GMP-compliant manufacturing site. `https://extranet.who.int/prequal/medicines/expert-review-panel` — **VERIFIED**. Note ERP is intended for products *en route to* PQ, and is generally invoked when fewer than three PQ'd products are on offer.

---

## 3. WHO Collaborative Registration Procedure (CRP)

Hub: `https://www.who.int/teams/regulation-prequalification/regulation-and-safety/facilitated-product-introduction/collaborative-registration-procedure` — **VERIFIED**. Contact **`crp@who.int`** (FPI Team; Team Lead Marie Valentin, `valentinm@who.int`). **Four pathways:** PQ CRP medicines & vaccines · PQ CRP IVDs · **SRA/WLA CRP medicines & vaccines** · PQ CRP vector control products.

### 3.1 PQ CRP (WHO-prequalified medicines & vaccines)
Page: `.../collaborative-registration-procedure/procedure-for-prequalified-med-vax` — **VERIFIED**
Legal basis: **WHO TRS 996, Annex 8 (2016)**. Landing `https://www.who.int/publications/m/item/trs996-annex08-crp-pq` — **VERIFIED**. PDF `https://cdn.who.int/media/docs/default-source/medicines/norms-and-standards/guidelines/prequalification/trs996-annex08-crp-pq.pdf?sfvrsn=791d2c89_4&download=true` — **VERIFIED** (225 KB).

**Mechanics.** The applicant submits a product that "in all essential features is the same as" the prequalified FPP/vaccine, using the same dossier WHO approved (updated for WHO-approved variations/requalification). WHO shares its **assessment, inspection and product-testing outcomes** with the NRA over a **secure platform**, accessible only to named CRP focal points under confidentiality undertakings.

**Timeline.** NRA commits to a decision **within 90 days** of receiving access to the assessment/inspection information, and to communicate the decision to WHO and the applicant **within a further 30 days**. The FAQ clarifies this is **90 *working* days**, the clock starts only once (a) the NRA has *accepted* use of CRP for that product, (b) national application requirements incl. the dossier are fulfilled, and (c) WHO's reports have been received — and the clock **stops** while the applicant answers NRA questions. **Post-approval variations: 30 working days.**

**Participating countries — 71 entries, dated 6 July 2026.** PDF: `https://cdn.who.int/media/docs/default-source/medicines/regulatory-updates/fpi/pq-crp---medicines-and-vaccines_-partcipating-countries_june-2024.pdf?sfvrsn=ff47ffb8_6` — **VERIFIED** (filename says "june-2024"; **contents are dated 6 July 2026** — do not trust the filename).
> Angola, Armenia, Azerbaijan, Bangladesh, Belarus, Benin, Bhutan, Botswana, Burkina Faso, Burundi, Cabo Verde, Cameroon, **CARICOM**, CAR, Chad, Comoros, Congo, Côte d'Ivoire, DRC, El Salvador, Eritrea, Ethiopia, Gabon, Gambia, Georgia, Ghana, Guinea, Honduras, Kazakhstan, Kenya, Kyrgyzstan, Lao PDR, Lesotho, Liberia, Madagascar, Malawi, Malaysia, Maldives, Mali, Mauritania, Mozambique, Namibia, Nepal, Nigeria, Oman, Pakistan, PNG, Philippines, Rep. of Moldova, Rwanda, São Tomé & Príncipe, Senegal, Serbia, Sierra Leone, South Africa, Sri Lanka, Sudan, Thailand, Timor-Leste, Togo, Tunisia, Türkiye, Uganda, Ukraine, Tanzania (Mainland), Tanzania (Zanzibar), Uzbekistan, Yemen (Sana'a), Yemen (Aden), Zambia, Zimbabwe.

**Forms** (all **VERIFIED** downloads under `https://cdn.who.int/media/docs/default-source/medicines/regulatory-updates/fpi/`):
- NRA side: **Appendix 1A** participation agreement `appendix1a_who_trs_996_2016_annex8.pdf?sfvrsn=285e4058_3`; **Appendix 1B** focal-point confidentiality undertaking `appendix1b_trs996_2016_annex8-(1).pdf?sfvrsn=53cdec00_3`; **Appendix 3B/3C** `appendix3_partb_who_trs_996_2016_annex8-(1).pdf?sfvrsn=95f15b90_3`, `appendix3_partc_who_trs_996_2016_annex8-(1).pdf?sfvrsn=18d5b085_3`
- **Manufacturer side: Appendix 2 = consent form** (`appendix2_trs996_2016_annex8-(2).pdf?sfvrsn=e7649f50_3`) — **one per country**, signed, emailed to `crp@who.int`, wet-ink originals couriered to WHO FPI Team, Room M431, 20 Avenue Appia, 1211 Geneva 27, Switzerland; **Appendix 3 Part A = expression of interest** (`appendix3_parta_who_trs_996_2016_annex8-(2).pdf?sfvrsn=6c003b2a_5`) — submitted to the NRA *and* copied to `crp@who.int`.

**Published registrations achieved:** `https://cdn.who.int/media/docs/default-source/medicines/regulatory-updates/fpi/pq-crp-registered-products.xlsx?sfvrsn=182b7b39_2` — **VERIFIED** (844 KB, **~1,292 registration records**). Columns: WHO PQ number, Notes, Product, Prequalification holder, Country of registration, Region, Registration date, Registration number. Caveat in the file: data come from the NMRAs and reflect WHO's best understanding at posting time.

### 3.2 SRA CRP / WLA CRP (products approved by an SRA/WLA)
Page: `.../collaborative-registration-procedure/crp-for-medicines-and-vaccines-approved-by-the-stringent-regulatory-authorities` — **VERIFIED**. **Note the page is now titled "Collaborative Registration Procedure for medicines and vaccines approved by WHO-Listed Authorities"** and its artefacts are named `wla-crp-*`, even though the URL and the FAQ still say SRA.
Legal basis: **WHO TRS 1010, Annex 11 (2018)**. Landing `https://www.who.int/publications/m/item/annex-11-trs-1010` — **VERIFIED**. PDF `https://cdn.who.int/media/docs/default-source/medicines/norms-and-standards/guidelines/regulatory-standards/trs1010-annex11.pdf?sfvrsn=b7c8b9c1_2&download=true` — **VERIFIED** (334 KB). Good-practice companion: **TRS 1019, Annex 6** (NRA good practices in implementing CRPs).

**Scope — much broader than PQ CRP.** Applies to **any FPP** — innovator, generic, vaccine, biotherapeutic, similar biotherapeutic — provided a WLA/SRA has assessed it and a positive scientific opinion exists that can be shared. **Explicitly includes EMA's EU-M4all (Article 58) opinions and Swissmedic's MAGHP** global-health procedures. **For a rare-disease repurposer this is the usable pathway — it has no EOI gate and no EML dependency.**

**Timeline.** Decision within **90 working days** of the NRA receiving all relevant documents; decision communicated to WHO and applicant (Appendix 9) within a further **30 working days**.

**Participating countries — 69 entries, dated 6 July 2026.** PDF: `https://cdn.who.int/media/docs/default-source/medicines/regulatory-updates/fpi/wla-crp-participating-countries.pdf?sfvrsn=c247bee4_7` — **VERIFIED**.
> Angola, Bangladesh, Benin, Bhutan, Botswana, Brunei Darussalam, Burkina Faso, Burundi, Cabo Verde, Cameroon, **CARICOM**, CAR, Chad, Comoros, Congo, Côte d'Ivoire, DRC, El Salvador, Eritrea, Ethiopia, Gabon, Gambia, Georgia, Ghana, Guinea, Honduras, **Jordan**, Kazakhstan, Kenya, Lao PDR, Lesotho, Liberia, Madagascar, Malawi, Malaysia, Maldives, Mali, Mauritania, **Montenegro**, Mozambique, Namibia, Nepal, **Niger**, Nigeria, Pakistan, PNG, **Paraguay**, Philippines, **Qatar**, Rwanda, São Tomé & Príncipe, Senegal, Serbia, Sierra Leone, South Africa, Sri Lanka, Thailand, Timor-Leste, Togo, Tunisia, Türkiye, Tanzania (Mainland), Tanzania (Zanzibar), Uganda, Ukraine, Yemen (Sana'a), Yemen (Aden), Zambia, Zimbabwe.
> *Delta vs PQ CRP:* WLA CRP **adds** Brunei, Jordan, Montenegro, Niger, Paraguay, Qatar; **lacks** Armenia, Azerbaijan, Belarus, Kyrgyzstan, Moldova, Oman, Sudan, Uzbekistan.

**Forms** (same cdn path, all **VERIFIED**):
- NRA: **Appendix 1** EN `crp_sra_who_trs_1010_2018_annex11_appendix_1_eng.pdf?sfvrsn=d4a8392c_1`; FR `..._fr.pdf?sfvrsn=a087902_1`; ES `..._sp.pdf?sfvrsn=7f5c95a1_1`
- Manufacturer: **Appendix 3a** (request WLA permission to share assessment + GMP inspection reports with NRAs and WHO) `sra-crp_who_trs1010_annex11_appendix3a.docx?sfvrsn=ae31b1e3_1`; **Appendix 3b** (grant WLA permission to share) `..._appendix3b.docx?sfvrsn=931e6f7_1`; **Appendix 4** QIS-SRA, WLA-validated `who_trs1010_annex11_appendix4_qis-sra.docx?sfvrsn=3313a9c5_1`; **Appendix 7** expression of interest to the NRA `sra-crp_who_trs1010_annex11_appendix7.docx?sfvrsn=893f801c_1`; **Appendix 8** agreement giving WHO access to data shared with NRAs `who_trs1010_annex11_appendix8.pdf?sfvrsn=2c9806d4_1`; **Appendix 9** NRA decision communication `who_trs1010_annex11_appendix9.pdf?sfvrsn=f0e3ae8b_1`.
- Signed originals couriered to WHO, attn. Marie Valentin, FPI Team Room M431, Geneva.

**Published registrations achieved:** `https://cdn.who.int/media/docs/default-source/medicines/regulatory-updates/fpi/wla-crp-registered-products.xlsx?sfvrsn=316083a7_8` — **VERIFIED**. Header: **"SRA/WLA CRP Registered Products as at 30 December 2025"**, **~262 records**. Columns: Applicant/MAH, Product, **Reference Authority**, Country. EMA dominates the Reference Authority column; MEB (Netherlands) also appears. Recent entries include Gilead's lenacapavir in Zimbabwe (EMA as reference).

### 3.3 CRP FAQ (v3, version date **March 2025**) — the gotcha list
`https://cdn.who.int/media/docs/default-source/medicines/regulatory-updates/fpi/faqs-crp-v3-march-2025_updated.pdf?sfvrsn=c6ebb65d_4` — **VERIFIED**, 7 pages.

- **Consent is mandatory and per-country.** PQ CRP: applicant signs **Appendix 2 consent per country**. WLA CRP: applicant must separately get the **WLA's** agreement to share (Appendix 3a/3b) plus give WHO data access (Appendix 8). Nothing moves without the manufacturer's signature.
- **The NRA must be a signatory.** Only NRAs that have signed the participation agreement (Appendix 1/1A) plus per-focal-point confidentiality undertakings (Appendix 1B) can receive reports. If your target country is not on the list, **you or the NRA can ask WHO FPI to invite it** (FAQ Q9) — that is a real, documented route, not a dead end.
- **CRP is opt-in per application, not automatic.** Submitting in a participating country does not trigger CRP. After the EOI, WHO asks the NRA to *accept* CRP for that specific product; reports are released only after a positive answer and confirmation of a complete national application — **that moment is the clock start** (Q14, Q16).
- **No exemption from local requirements.** Full national dossier, local requirements and **national fees still apply** (Q5, Q6). WHO charges nothing (Q4).
- **The applicant need not be the PQ/MA holder** — but the relationship must be declared in the EOI (Appendix 3a for PQ CRP, Appendix 7 for SRA CRP) (Q7).
- **Country-by-country staging is allowed** (Q10).
- **🚩 US FDA does not participate in SRA CRP** — "due to limitations with sharing reports." Participating reference authorities in practice: **EMA, MHRA (UK), TGA (Australia), FIMEA (Finland), MEB (Netherlands)**. **If your asset is FDA-only, SRA/WLA CRP is unavailable to you** — you would need an EMA/EU-M4all or other WLA route first.
- **Nominal SRA reference list for CRP (FAQ Q31, 35 authorities):** Australia, Austria, Belgium, Bulgaria, Canada, Croatia, Cyprus, Czech Republic, Denmark, Estonia, Finland, France, Germany, Greece, Hungary, Iceland, Ireland, Italy, Japan, Latvia, Liechtenstein, Lithuania, Luxembourg, Malta, Netherlands, Poland, Portugal, Romania, Slovenia, Slovakia, Spain, Sweden, Switzerland, UK, USA.
- **🚩 Live ambiguity:** FAQ Q32 (Mar 2025) says the procedure **still uses the SRA list**, and that guidelines will be revised for WLA "once the revision process begins." But the who.int page is already titled *WLA CRP*, the artefacts are named `wla-crp-*`, and the participating-countries PDF (6 Jul 2026) is titled *"Stringent Regulatory Authorities/WHO Listed Authorities (WLA CRP)"*. **Confirm the operative reference-authority list with `crp@who.int` before committing to a filing plan** — WLA-only authorities (e.g. Korea MFDS, Singapore HSA, Saudi SFDA, Indonesia BPOM) may or may not yet be accepted as CRP reference authorities.
- **De-registration / withdrawal / suspension all flow back:** NRAs notify WHO within 30 days of de-registration; WHO + manufacturer must notify all CRP-registering NRAs on PQ de-listing or SRA suspension (Q23–Q25).
- A product **prequalified via the abridged SRA route is not eligible for PQ CRP** — use SRA/WLA CRP with the original SRA as reference (Q28).

---

## 4. WHO-Listed Authority (WLA) framework

Initiative page: `https://www.who.int/initiatives/who-listed-authority-reg-authorities` — **VERIFIED**.

### 4.1 The official WLA list — **36 WLAs / 34 countries, as of December 2025**
- Landing: `https://www.who.int/publications/m/item/list-of-who-listed-authorities-wlas` — **VERIFIED**, published **22 December 2025**
- **PDF: `https://cdn.who.int/media/docs/default-source/medicines/regulatory-systems/wla/list_of_wla.pdf?sfvrsn=1f6c2140_49&download=true`** — **VERIFIED** (606 KB, 21 pp.)
- Structure: one row **per authority per product stream** (Medicines / Vaccines), with **listed functions** (registration & marketing authorization, vigilance, market surveillance, licensing establishments, regulatory inspection GMP/GSDP/GCP, laboratory testing, clinical trials oversight, RA lot release), date of first listing, and **renewal date** (listings are time-limited, ~5 yrs).
- **Non-EU entries (from the PDF):** **Australia TGA** (16 Dec 2025, renewal Jan 2031) · **Canada Health Canada** (21 Jul 2025, Aug 2030) · **Indonesia BADAN POM/BPOM** — vaccines only (16 Dec 2025) · **Japan MHLW/PMDA** (21 Jul 2025, Aug 2030) · **Republic of Korea MFDS** (26 Oct 2023, Nov 2028) · **Saudi Arabia SFDA** · **Singapore HSA** (26 Oct 2023, Nov 2028) · **Switzerland Swissmedic** (26 Oct 2023, Nov 2028) · **UK (Great Britain) MHRA** (21 Jul 2025, Aug 2030) · **US FDA** (13 May 2024, Jun 2029).
- **European Medicines Regulatory Network (EMRN)** is listed as a **regional regulatory system** (13 May 2024, renewal Jun 2029) — European Commission DG SANTE + EMA + the NRAs of Austria, Belgium, Bulgaria, Croatia, Cyprus, Czechia, Denmark, Estonia, Finland, France, Germany, Greece, Hungary, Iceland, Ireland, Italy, Latvia, Liechtenstein, Lithuania, Luxembourg, Malta, Netherlands, Norway, Poland, Portugal, Romania, Slovakia, Slovenia, Spain, Sweden; EDQM coordinates lab testing/lot release. Each of those 30 authorities also appears individually with a footnote "evaluated as part of the EMRN."
- Progression: three founding WLAs (Swissmedic, MFDS, HSA) Oct 2023 → expanded to 36 (adding US FDA, EMA/EMRN + 30 EU/EEA NRAs) → Australia and Indonesia added Dec 2025.
- Each row links to a per-authority **"listing summary"** (TGA-listing-summary, HC-listing-summary, US FDA-listing-summary, EMRN-listing-summary, etc.).

### 4.2 The transitional WLA (tWLA) list — the successor to the "SRA list"
- Landing: `https://www.who.int/publications/m/item/list-of-transitional-wlas` — **VERIFIED**, published **22 December 2025**
- **PDF: `https://cdn.who.int/media/docs/default-source/medicines/regulatory-systems/wla/list-of-transitional-wlas.pdf?sfvrsn=a3011e1e_21&download=true`** — **VERIFIED** (248 KB, 3 pp., "as of December 2025")
- **⏳ Hard deadline: the tWLA arrangement is valid five years from publication of the interim WLA Operational Guidance (31 March 2022) → it expires 31 MARCH 2027.** That is ~8 months from now. Any national law or tender that references "SRA" or the WHO interim list needs a migration answer before then.
- **18 tWLAs** (origin codes: A = ML3/ML4 NRA, B = SRA (medicines), C = highly performing NRA (vaccines), D = PAHO regional reference authority, E = functional NRA (vaccines)):
  | # | Country | tWLA | Origin | Scope |
  |---|---|---|---|---|
  |1|Argentina|ANMAT|D|Medicines, Vaccines|
  |2|Brazil|ANVISA|D, E|Medicines, Vaccines|
  |3|Chile|ISP|D|Medicines|
  |4|China|NMPA|A (ML3), E|Vaccines|
  |5|Colombia|INVIMA|D|Medicines|
  |6|Cuba|CECMED|D, E|Medicines, Vaccines|
  |7|Egypt|EDA|A (ML3)|Vaccines|
  |8|Ghana|FDA|A (ML3)|Medicines|
  |9|India|CDSCO|A (ML3)|Vaccines|
  |10|Iran|IFDA|E|Vaccines|
  |11|Japan|PMDA|E|Vaccines|
  |12|Mexico|COFEPRIS|D, E|Medicines, Vaccines|
  |13|Nigeria|NAFDAC|A (ML3)|Medicines|
  |14|Russian Federation|Ministry of Health|E|Vaccines|
  |15|Serbia|ALIMS|A (ML3)|Vaccines|
  |16|Thailand|Thai-FDA|A (ML3)|Vaccines|
  |17|Tanzania|TMDA|A (ML3)|Medicines|
  |18|Viet Nam|DAV|A (ML3)|Vaccines|
- **🚩 Critical read: no entry on the tWLA list carries origin code "B" (SRA-medicines).** Every classic SRA has already graduated to full WLA. So **as of Dec 2025 the tWLA list is *not* a "transitional SRA list"** — it is the on-ramp for emerging authorities. The classic-SRA universe now lives entirely in §4.1. Scope for tWLAs is provisional: "precise scope … will be further defined in agreement with each Regulatory Authority as part of the roadmap to listing."
- Legacy SRA definition still cited by CRP: **WHO TRS 1003** (ICH founding members + observers + MRA partners pre-2015).

### 4.3 GBT and the ML3/ML4 list
- **GBT Revision VI (2021)** is the current published revision: `https://www.who.int/publications/i/item/9789240020245` — **VERIFIED**. Benchmarking Manual (Mar 2024): `https://www.who.int/publications/i/item/9789240087637`. Maturity scale ML1 (some elements exist) → **ML3 (stable, well-functioning, integrated)** → **ML4 (advanced performance, continuous improvement)**. ML3 is the eligibility floor for WLA consideration.
- **List of NRAs at ML3/ML4 — "As of March 2026":** landing `https://www.who.int/publications/m/item/list-of-nras-operating-at-ml3-and-ml4` — **VERIFIED**; **PDF `https://cdn.who.int/media/docs/default-source/medicines/regulatory-systems/wla/list-of-nras-operating-at-ml3-and-ml4.pdf`** — **VERIFIED** (178 KB). Full contents (⚠️ WebFetch returns garbage on this PDF — pull with curl and run pdftotext):

| Country | Authority | ML | Scope | Year |
|---|---|---|---|---|
| China | NMPA | ML3 | Vaccines (producing) | 2022 |
| Egypt | EDA | ML3 | Medicines; Vaccines (producing) | 2024 / 2022 |
| Ethiopia | EFDA | ML3 | Medicines; Vaccines (non-producing) | 2025 |
| Ghana | FDA | ML3 | Medicines; Vaccines (non-producing) | 2020 / 2025 |
| India | CDSCO | ML3 | Vaccines (producing) | 2017, 2024 |
| Indonesia | BADAN POM | ML3 | Vaccines (producing) | 2019 |
| **Kazakhstan** | Cttee of Medical & Pharmaceutical Control / NCE | ML3 | Medicines; Vaccines (non-producing) | **2026** |
| Nigeria | NAFDAC | ML3 | Medicines; Vaccines (non-producing) | 2022 / 2025 |
| **Rep. of Korea** | **MFDS** | **ML4** | Medicines; Vaccines (producing) | 2022 |
| Rwanda | FDA | ML3 | Medicines; Vaccines (non-producing) | 2024 |
| **Saudi Arabia** | **SFDA** | **ML4** | Medicines; Vaccines (producing) | 2023 |
| Sénégal | ARP | ML3 | Medicines; Vaccines (non-producing) | 2024 |
| Serbia | ALIMS | ML3 | Vaccines (producing) | 2019 |
| **Singapore** | **HSA** | **ML4** | Medicines; Vaccines (non-producing); **Medical devices (2026)** | 2022 / 2026 |
| South Africa | SAHPRA | ML3 | Vaccines (producing) | 2022 |
| Thailand | FDA | ML3 | Vaccines (producing) | 2021 |
| Türkiye | TİTCK | ML3 | Medicines; Vaccines (producing) | 2023 |
| Tanzania | TMDA | ML3 | Medicines; Vaccines (non-producing) | 2018 / 2025 |
| Viet Nam | DAV + ASTT + NICVB + GDPM | ML3 | Vaccines (producing) | 2020 |
| Zimbabwe | MCAZ | ML3 | Medicines; Vaccines (non-producing) | 2024 |

### 4.4 Why this matters for reliance filings in small markets
- **The terminology mismatch is a live legal risk.** Many national medicines acts, registration regulations and tender specs hard-code **"Stringent Regulatory Authority"** or reference the WHO interim list. WHO has retired SRA as an operational concept in favour of WLA, but the CRP FAQ (Mar 2025) still runs the procedure off the **SRA list**, while the CRP web page and its artefacts are already branded **WLA CRP**. Expect per-country variance in what a dossier cover letter should cite. Practically: **cite both** ("approved by an authority that is both an SRA per WHO TRS 1003 and a WHO-Listed Authority for medicines, listing date X, renewal date Y") and attach the relevant listing summary from the WLA PDF.
- **The 31 March 2027 tWLA expiry** is the forcing function. Countries whose laws point at the transitional/interim list need to repoint at the WLA list; any authority you rely on that is only a tWLA (ANMAT, ANVISA, COFEPRIS, INVIMA, CECMED, NMPA, CDSCO, NAFDAC, TMDA…) may lose its transitional status if it hasn't completed full WLA listing.
- **WLA listings expire and renew** (renewal dates 2028–2031 in the current PDF). Reliance arguments should be re-verified per filing, not asserted once.
- **US FDA is a WLA but not a CRP reference authority.** A WLA-based *reliance* argument to a national NRA is different from — and available where — the *procedural* CRP route is not. For an FDA-only asset in a small market, the realistic sequence is: national reliance/abridged review citing FDA WLA status, or obtain an **EU-M4all (Art. 58)** scientific opinion to unlock WLA CRP across the 69 participating countries.

---

### Files worth pinning in a scraper
| Purpose | URL | Cadence |
|---|---|---|
| Prequalified FPPs | `extranet.who.int/prequal/medicines/prequalified/finished-pharmaceutical-products/export?page&_format=csv` | rolling, poll weekly + diff |
| Prequalified APIs | `.../medicines/prequalified/active-pharmaceutical-ingredients/export?page&_format=csv` | rolling |
| Prequalified vaccines | `.../vaccines/prequalified/export?page&_format=csv` | rolling |
| EML machine-readable | `list.essentialmeds.org/print?format=xlsx` | biennial (next 2027) |
| EML PDF (24th) | `iris.who.int/server/api/core/bitstreams/17642505-…/content` | biennial |
| PQ CRP countries | `cdn.who.int/…/pq-crp---medicines-and-vaccines_-partcipating-countries_june-2024.pdf?sfvrsn=ff47ffb8_6` | irregular; **content dated 6 Jul 2026** |
| WLA CRP countries | `cdn.who.int/…/wla-crp-participating-countries.pdf?sfvrsn=c247bee4_7` | **6 Jul 2026** |
| PQ CRP registrations | `cdn.who.int/…/pq-crp-registered-products.xlsx?sfvrsn=182b7b39_2` | ~1,292 rows |
| WLA CRP registrations | `cdn.who.int/…/wla-crp-registered-products.xlsx?sfvrsn=316083a7_8` | 262 rows, as at 30 Dec 2025 |
| WLA list | `cdn.who.int/…/wla/list_of_wla.pdf?sfvrsn=1f6c2140_49&download=true` | 22 Dec 2025 |
| tWLA list | `cdn.who.int/…/wla/list-of-transitional-wlas.pdf?sfvrsn=a3011e1e_21&download=true` | 22 Dec 2025; **expires 31 Mar 2027** |
| ML3/ML4 NRAs | `cdn.who.int/…/wla/list-of-nras-operating-at-ml3-and-ml4.pdf` | as of Mar 2026 |

**⚠️ cdn.who.int `?sfvrsn=` cache-buster tokens change when WHO republishes a file.** Resolve them by scraping the parent page rather than hard-coding; the bare path without `?sfvrsn` generally still resolves (verified on the ML3/ML4 PDF).

**Nothing was written to disk in the project directory.** Working files (downloaded PDFs/CSVs/XLSX used for verification) are in `/private/tmp/claude-501/-Users-carte-Downloads-RareDiseaseHedge/fd64561f-7c90-41a2-95cf-b4a133a8fe0f/scratchpad`.

**One caveat on sourcing:** the WHO ML3/ML4 and WLA figures above were read directly out of the official WHO PDFs via `pdftotext`, not from secondary reporting. The "36 WLAs / 34 countries" headline count comes from a Health Policy Watch article; the PDF itself does not state a total, so treat that number as journalist-derived while the per-authority rows are primary.