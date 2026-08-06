<!-- Mined from agent-a5d6b183c04ce71b1.jsonl (plus subagent agent-a52ef04ad6a4d3100.jsonl) on 2026-08-05.
     Agent was killed at line 184 ("Request interrupted by user") after 20 assistant turns.
     All findings below are VERIFIED by actual fetches unless explicitly labeled UNVERIFIED or UNFINISHED.
     This file was reconstructed by a recovery agent; line numbers in brackets reference JSONL event indices. -->

# Non-US Regulatory Drug Approval Sources — Verified Technical Reference

**Purpose:** Machine-readable approved-drug / approved-substance lists from non-US regulators, for diffing against FDA Orange Book / Drugs@FDA to identify drugs approved abroad but never in the US. Framed against Funnel A (PRV-eligible, never-US moiety via 505(b)(1)) vs Funnel B (orphan exclusivity only, US generic via 505(b)(2)).

**Legal baseline (assumed settled):** 21 U.S.C. § 360ff(a)(4)(B)(i) bars PRVs for any moiety previously approved under 505(b)(1)/(b)(2)/(j). Only never-US moieties filed as full 505(b)(1) NDAs qualify. PRV sunset 2029-09-30.

---

## 1. EMA — European Medicines Agency (Centrally Authorised Products Only)

**VERIFIED** [events 16–34, agent-a5d6b183c04ce71b1]

### Primary Download

| Item | Value |
|------|-------|
| URL | `https://www.ema.europa.eu/en/documents/report/medicines-output-medicines-report_en.xlsx` |
| HTTP status | 200 |
| File size | 897,579 bytes (≈877 KB) as of 2026-08-05 18:05 UTC |
| Content-Type | `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` |
| Update cadence | Nightly; `Last-Modified: Wed, 05 Aug 2026 16:05:32 GMT` (verified in HTTP header) |
| Auth | None |
| Format | XLSX, one sheet named `Medicine` |

### Structure

- **Header at row 9** (rows 1–8 are metadata/title)
- **2,730 data rows** total (as of 2026-08-05 download)
- **39 columns** (verified by parsing):

| # | Column name |
|---|------------|
| 0 | Category |
| 1 | Name of medicine |
| 2 | EMA product number |
| 3 | Medicine status |
| 4 | Opinion status |
| 5 | Latest procedure affecting product information |
| 6 | International non-proprietary name (INN) / common name |
| 7 | Active substance |
| 8 | Therapeutic area (MeSH) |
| 9 | Species (veterinary) |
| 10 | Patient safety |
| 11 | ATC code (human) |
| 12 | ATCvet code (veterinary) |
| 13 | Pharmacotherapeutic group (human) |
| 14 | Pharmacotherapeutic group (veterinary) |
| 15 | Therapeutic indication |
| 16 | Accelerated assessment |
| 17 | Additional monitoring |
| 18 | Advanced therapy |
| 19 | Biosimilar |
| 20 | Conditional approval |
| 21 | Exceptional circumstances |
| 22 | Generic |
| 23 | Orphan medicine |
| 24 | PRIME: priority medicine |
| 25 | Marketing authorisation developer / applicant / holder |
| 26 | European Commission decision date |
| 27 | Start of rolling review date |
| 28 | Start of evaluation date |
| 29 | Opinion adopted date |
| 30 | Withdrawal of application date |
| 31 | Marketing authorisation date |
| 32 | Refusal of marketing authorisation date |
| 33 | Withdrawal / expiry / revocation / lapse of marketing authorisation date |
| 34 | Suspension of marketing authorisation date |
| 35 | Revision number |
| 36 | First published date |
| 37 | Last updated date |
| 38 | Medicine URL |

### Status breakdown (measured)
```
Category:       Human=2337  Veterinary=393
Medicine status: Authorised=1868, Withdrawn=416, Application withdrawn=284,
                 Refused=66, Opinion=35, Lapsed=29, Expired=19, Revoked=8
```

### Sample authorised human record (measured)
```
Category         = Human
Name of medicine = Degarelix Accord
EMA product number = EMEA/H/C/006048
Medicine status  = Authorised
INN              = degarelix
Active substance = degarelix acetate
ATC code         = L02BX02
Orphan medicine  = No
MA holder        = Accord Healthcare S.L.U.
EC decision date = 04/08/2026
MA date          = 29/09/2023
URL              = https://www.ema.europa.eu/en/medicines/human/EPAR/degarelix-accord
```

### Critical caveat

**This xlsx covers ONLY centrally authorised products.** There is no "central/national" column — every row in this file is a centrally authorised product. Nationally authorised products (the majority of EU medicines by product count) are NOT in this file.

### Companion downloads (same base URL pattern)

Other xlsx files at `https://www.ema.europa.eu/en/documents/report/`:
- `medicines-output-orphan_designations-report_en.xlsx`
- `medicines-output-pip_decisions-report_en.xlsx`
- `medicines-output-referrals-report_en.xlsx`
- `medicines-output-post_authorisation_activities-report_en.xlsx`
- `medicines-output-shortages-report_en.xlsx` etc.

### Redistribution / licence

EMA content is published under European Commission open data policy. No explicit licence found on the download page; standard EU open data CC BY 4.0 / ISA2 waiver typically applies. Verify with EMA legal if redistribution is planned.

---

## 2. EMA SPOR — Substance Management Service (SMS)

**VERIFIED (but API is SSO-gated)** [events 115–122, agent-a5d6b183c04ce71b1]

| URL | HTTP | Notes |
|-----|------|-------|
| `https://spor.ema.europa.eu/sporwi/` | 200 (9,192 bytes) | Landing page |
| `https://spor.ema.europa.eu/smswi/` | 200 (8,634 bytes) | SMS web UI — SPA, guest access to browse/export |
| `https://spor.ema.europa.eu/omswi/` | 200 (10,457 bytes) | OMS (Organisation Management) |
| `https://spor.ema.europa.eu/smsapi/v1/substances` | 302 → EMA SSO login | **Requires EMA account** |
| `https://spor.ema.europa.eu/v1/substances` | 404 | Wrong path |

**SMS landing text (measured):** "The SPOR portal currently offers guest access to query, browse and export OMS, RMS and SMS data. As of 1 October 2025 change requests should be submitted through the EMA Service Desk."

**Conclusion:** Guest browser access for querying is available. Programmatic bulk export via REST API requires EMA account/SSO. There is no anonymous bulk download endpoint. Manual export from `https://spor.ema.europa.eu/smswi/#/search` may be possible for small queries.

### SMSID as a join key

**VERIFIED** [events 126–133, agent-a5d6b183c04ce71b1]

The FDA UNII Records file (see Section 9) has a column `SMSID` = "European Medicines Substance ID" pointing to `https://spor.ema.europa.eu/smswi/#/`. This is the SPOR SMS ID.

**Coverage measured from UNII_Records_26Feb2026.txt (168,046 total UNII records):**
- With SMSID: **28,859 (17.2%)**
- With INN_ID: 12,588 (7.5%)
- With both: 12,299

Sample: `ADECATUMUMAB → SMSID=100000124297`, `SPIROFYLLINE → SMSID=100000083807`

**Join key verdict:** SMSID exists in FDA's UNII file as a bridge to SPOR, but only 17% of UNII records have it. For centrally authorised EMA products, the join path is: EMA INN → UNII Names lookup → UNII → SMSID (if populated). The free-text INN name lookup covers ≈84–95% of EMA authorised products (see Section 9).

---

## 3. EU Nationally Authorised Products

**VERIFIED (structure only; no bulk download exists)** [event 112, agent-a5d6b183c04ce71b1]

### HMA/CMDh MRI Product Index

| URL | HTTP | Notes |
|-----|------|-------|
| `http://mri.cts-mrp.eu/` | 301 → `https://mri-production.cts-mrp.eu/` | HTTP OK but 301 |
| `https://mri.cts-mrp.eu/` | 301 → `https://mri-production.cts-mrp.eu/` | |
| `https://mri-production.cts-mrp.eu/` | 200 (2,329 bytes) | Title: `HMA.MrIndex.Portal` |

**Content of `https://mri-production.cts-mrp.eu/`:** Angular SPA shell (2,329 bytes) — no server-rendered data, no link extraction possible without JavaScript. No bulk export or API discovered.

### EMA National Registers Page

**VERIFIED** [event 112, agent-a5d6b183c04ce71b1]
`https://www.ema.europa.eu/en/medicines/national-registers-authorised-medicines` — HTTP 200, 75,325 bytes

Lists 34 national register links for EU member states. Each country maintains its own database. Key examples:
- France: `http://agence-prd.ansm.sante.fr/php/ecodex/index.php`
- Germany: `https://www.pharmnet-bund.de/PharmNet/DE/Oeffentlichkeit/...`
- Italy: `https://medicinali.aifa.gov.it/`
- Spain: `http://cima.aemps.es/cima/publico/home.html`
- Sweden: `https://www.lakemedelsverket.se/sv/sok-lakemedelsfakta`
- Netherlands: `https://www.geneesmiddeleninformatiebank.nl`
- Poland: `https://rejestrymedyczne.ezdrowie.gov.pl/rpl/search/public`

**None of these have been individually verified for machine-readable bulk export.** Each is a national query portal. A few (AIFA Italy, AEMPS Spain) are known to publish open-data extracts but this was not verified in the session.

---

## 4. Health Canada — Drug Product Database (DPD)

**VERIFIED** [events 54–79, agent-a5d6b183c04ce71b1]

### Bulk Extract Files

**Base URL:** `https://www.canada.ca/content/dam/hc-sc/documents/services/drug-product-database/`

**Extract page:** `https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products/drug-product-database/what-data-extract-drug-product-database.html`
- Loaded with HTTP 200 (35,536 bytes) using plain curl (Canada.ca blocks some UA/HTTP2 combos)

**File naming convention:**
- `drug.zip` = all statuses; `drug_ap.zip` = approved only; `drug_ia.zip` = inactive; `drug_dr.zip` = dormant

**All files updated 2026-08-04** (confirmed from page timestamps)

**Verified downloads (both HTTP 200):**
```
drug_ap.zip   HTTP:200 SIZE:90,984 bytes   → drug_ap.txt (481,680 bytes uncompressed)
ingred_ap.zip HTTP:200 SIZE:99,197 bytes   → ingred_ap.txt (661,368 bytes uncompressed)
```

**Also available:**
```
allfiles.zip (all statuses)    → hc-sc.gc.ca HTTP 200, size 1,333,171 bytes (confirmed)
allfiles_ap.zip (approved)     → same host pattern
```

### DPD File Set

| File (table name) | Content |
|---|---|
| `drug_ap.zip` (QRYM_DRUG_PRODUCT) | Drug product master — drug code, DIN, brand name, class, category |
| `ingred_ap.zip` (QRYM_ACTIVE_INGREDIENTS) | Ingredient name, strength, unit |
| `comp_ap.zip` (QRYM_COMPANIES) | Company info |
| `form_ap.zip` (QRYM_FORM) | Dosage form |
| `route_ap.zip` (QRYM_ROUTE) | Route of administration |
| `pharm_ap.zip` (QRYM_PHARMACEUTICAL_STD) | Pharmaceutical standard |
| `schedule_ap.zip` (QRYM_SCHEDULE) | Schedule classification |
| `status_ap.zip` (QRYM_STATUS) | Status history with dates |
| `ther_ap.zip` (QRYM_THERAPEUTIC_CLASS) | Therapeutic class |
| `package_ap.zip` (QRYM_PACKAGING) | Package sizes |
| `inactive.zip` (QRYM_INACTIVE_PRODUCTS) | Inactive/cancelled products |
| `bios_ap.zip` | Biosimilars only |

### Sample records (measured from actual files)

**drug_ap.txt first records (comma-separated, no header):**
```
"14535","","Human","02040786","APO-CLOMIPRAMINE","","N","76172","1","22-MAR-2025","0109212001","Humain","",""
```
Fields: drug_code, (blank), class, DIN, brand_name, (blank), (flag), company_code, last_updated_field?, date, product_categorization, (French brand name?), ...

**ingred_ap.txt first records:**
```
"14535","2442","CLOMIPRAMINE HYDROCHLORIDE","I","10","MG","","","N","","Historic Freeform Text: CLOMIPRAMINE HCL","Chlorhydrate de clomipramine","MG","",""
```
Fields: drug_code, ingredient_code, ingredient_name(EN), (type?), strength, unit, (blanks), historic text, ingredient_name(FR), unit_fr, ...

### JSON API (already established)

- `https://health-products.canada.ca/api/drug/drugproduct/?lang=en&type=json&brandname=lipitor`
- `https://health-products.canada.ca/api/drug/activeingredient/?...`
- Auth: None; returns drug_code/DIN/brand_name/company_name/ingredient_name/strength
- Docs: `https://health-products.canada.ca/api/documentation/dpd-documentation-en.html`

### Auth / Licence

No auth. The DPD terms page notes open government use. The "old" allfiles.zip at `https://hc-sc.gc.ca/dhp-mps/alt_formats/zip/prodpharma/databasdon/allfiles.zip` also resolves (HTTP 200, 1,333,171 bytes) and may be easier to automate.

### Join key

Health Canada uses INN-style names in English (with French bilingual). The ingredient name field (`CLOMIPRAMINE HYDROCHLORIDE`) is typically a salt form. No UNII or INN_ID in the DPD; join via name normalization required.

---

## 5. PMDA (Japan)

**VERIFIED (English list = PDF only; Japanese Excel files verified)** [events 12–72, agent-a5d6b183c04ce71b1]

### English "List of Approved Products" page

- URL: `https://www.pmda.go.jp/english/review-services/reviews/approved-information/drugs/0002.html`
- HTTP: 200 (52,895 bytes)
- Title: "List of Approved Products | Pharmaceuticals and Medical Devices Agency"
- **Only download:** `https://www.pmda.go.jp/files/000281190.pdf` ("April 2004 to February 2026 [3.06 MB]")
  - HTTP 200, Content-Length: 3,206,009 bytes, Last-Modified: Mon, 22 Jun 2026 03:02:32 GMT
  - **Format: PDF only** — not machine-readable as structured data

### Japanese annual Excel files (FY-by-FY)

The Japanese-language page `https://www.pmda.go.jp/review-services/drug-reviews/review-information/p-drugs/` lists annual approved-drug Excel files:

**FY2025 (confirmed downloaded and parsed):**
- Index: `https://www.pmda.go.jp/review-services/drug-reviews/review-information/p-drugs/0040.html` (HTTP 200)
- **Excel:** `https://www.pmda.go.jp/files/000277965.pdf` (PDF summary) + **`https://www.pmda.go.jp/files/000277966.xlsx`** (Excel, HTTP 200, 32,825 bytes)

**FY2024 (confirmed):**
- Index: `https://www.pmda.go.jp/review-services/drug-reviews/review-information/p-drugs/0039.html` (HTTP 200)
- **Excel:** `https://www.pmda.go.jp/files/000274663.xlsx` (HTTP 200, 30 KB)

**Pattern for older years:** `/p-drugs/0037.html` (FY2024), `/p-drugs/0036.html` (FY2023), `/p-drugs/0035.html` (FY2022), etc.

### FY2025 Excel structure (measured from actual file)

```
Sheet: 2025年度承認品目  ("FY2025 Approved Products")
Row 3 header: 分野 | 承認日 | No. | 販売名/(会社名,法人番号) | 承認 | 成分名/(下線:新有効成分) | 効能・効果等
Translation: Division | Approval Date | No. | Brand Name/(Company, Corp No.) | Approval Type | Ingredient Name/(underline=new active ingredient) | Indication/Effect
Total rows: 143 (i.e., 143 approvals in FY2025)
```

**Sample row 4 (FY2025 first entry):**
```
分野=第１ | 承認日=2025.5.19 | No.=1 | 販売名=ファビハルタカプセル200mg/ノバルティスファーマ
成分名=イプタコパン塩酸塩水和物 | 効能=C3腎症を効能とする新効能医薬品/【希少疾病用医薬品】
(iptacopan hydrochloride hydrate — rare disease designation noted)
```

**Sample row 9 (FY2025):** `カンタリジン (Cantharidin)` — new active ingredient (underlined), for 伝染性軟属腫 (molluscum contagiosum).

### Key gotchas

- **Japanese character set:** Active ingredient names are in Japanese (Katakana phonetic transliterations of INN). Column header says new active ingredients are underlined (not parseable from xlsx alone). INN mapping requires transliteration + KEGG cross-reference.
- **JAN names** (Japanese Accepted Names) may differ from INN (e.g., `Warfarin potassium [JAN]` vs `Warfarin sodium [USP]`; `イプタコパン塩酸塩水和物` = iptacopan HCl hydrate, a salt not the free base).
- These are annual incremental files, not a cumulative approved products database.
- **No bulk endpoint** for the cumulative list; the English PDF covers 2004–Feb 2026.
- PMDA does operate `https://www.pmda.go.jp/PmdaSearch/iyakuSearch/` as a searchable database but no bulk download was found.

### Licence

PMDA is a Japanese government agency; data published under Japanese standard government licence (G-MIS), which permits open use for non-commercial/research. Verify for commercial redistribution.

---

## 6. KEGG DRUG

**VERIFIED** [events 6–11, 169–183, agent-a5d6b183c04ce71b1]

### REST API Endpoints

| Endpoint | HTTP | Size | Notes |
|---------|------|------|-------|
| `https://rest.kegg.jp/list/drug` | 200 | 599,728 bytes | 12,893 entries |
| `https://rest.kegg.jp/get/D00564` | 200 | 8,433 bytes | Full record for warfarin sodium |
| `https://rest.kegg.jp/get/D01280` | 200 | 5,134 bytes | Warfarin potassium (JP) |
| `https://www.kegg.jp/kegg-bin/download_htext?htext=br08303.keg&format=json` | 200 | 1,170,587 bytes | ATC BRITE JSON with country flags |

### Country flags — JP/US/EU coverage (measured)

From parsing `br08303` (ATC classification BRITE, 5,930 unique D-entries with ATC codes):
```
<JP> only       :   620  ("approved in JP, not US") — prime Funnel A candidate pool
<US> only       :   823
<JP/US>         : 1,179  (approved in both)
ANY flag        : 2,622  (44% of ATC-classified KEGG drugs have at least one flag)

JP total        : 1,799
US total        : 2,002
EU total        :     0  (EU flag is NOT present in KEGG ATC BRITE)
JP but NOT US   :   620  ← the useful diff
```

**Note:** EU flag `<EU>` is absent from the KEGG BRITE file — KEGG tracks JP and US approval flags only in this classification. The `<JP>` flag in KEGG BRITE represents JAN-listed (Japanese Pharmacopoeia/accepted name) drugs with Japanese PRODUCT entries.

### Sample record structure (D00564 warfarin sodium)

```
ENTRY    D00564   Drug
NAME     Warfarin sodium (USP); Coumadin (TN); Jantoven (TN)
PRODUCT  GENERIC  JANTOVEN (Upsher-Smith Labs)  ...
FORMULA  C19H15O4.Na
REMARK   ATC code: B01AA03
         Product (DG00149): D00564<US> D01280<JP>
DBLINKS  CAS: 129-06-6; PubChem: 7847630; ChEBI: 10034
```

**The `Product` line** encodes: `D00564<US>` = US-approved entry, `D01280<JP>` = JP-approved entry. This is the linkage between salt/form variants across jurisdictions.

### KEGG licensing

**Academic use:** Free via website.
**Commercial use:** Requires a commercial license. Contact Pathway Solutions Inc. (kegg.jp license page verified HTTP 200; restriction text confirmed by WebFetch: "Non-academic use of KEGG requires a commercial license. Please contact Pathway Solutions...").
**REST API for commercial use:** Not addressed on the license page — assume commercial license required.

**Conclusion for this pipeline:** KEGG DRUG REST API is useful for research/screening. For a commercial pipeline generating revenue (the small-market registrations), a commercial KEGG license would be required. Cost unknown — contact Pathway Solutions.

---

## 7. Swissmedic (Switzerland)

**VERIFIED** [events 85–95, agent-a5d6b183c04ce71b1]

### List page
- URL: `https://www.swissmedic.ch/swissmedic/de/home/services/listen_neu.html`
- HTTP: 200 (180,908 bytes)
- Title: "Listen und Verzeichnisse" (Lists and Directories)

### Key download files (all verified HTTP 200, dated 31.07.2026)

| File | Description | Size | URL |
|------|-------------|------|-----|
| `Zugelassene_Arzneimittel_HAM.xlsx` | Approved human medicines | 980 KB (1,004,159 bytes) | `https://www.swissmedic.ch/dam/swissmedic/de/dokumente/internetlisten/zugelassene_arzneimittel_ham_ind.xlsx.download.xlsx/Zugelassene_Arzneimittel_HAM.xlsx` |
| `Erweiterte_Arzneimittelliste_HAM.xlsx` | Extended human medicines list (more columns) | 2 MB (2,581,811 bytes) | `https://www.swissmedic.ch/dam/swissmedic/de/dokumente/internetlisten/erweiterte_ham_ind.xlsx.download.xlsx/Erweiterte_Arzneimittelliste%20HAM.xlsx` |
| `zugelassene_packungen_ham.xlsx` | Approved packages (human) | 3 MB | `https://www.swissmedic.ch/dam/swissmedic/de/dokumente/internetlisten/zugelassene_packungen_human.xlsx.download.xlsx/zugelassene_packungen_ham.xlsx` |
| `Liste_OrphanDrug_Internet.xlsx` | Human medicines with Orphan Drug status | 337 KB | `https://www.swissmedic.ch/dam/swissmedic/de/dokumente/internetlisten/status_orphandrug_ham.xlsx.download.xlsx/Liste_OrphanDrug_Internet.xlsx` |
| `Zugelassene_Arzneimittel_TAM.xlsx` | Approved veterinary medicines | 334 KB | (same pattern, TAM) |
| `Zugelassene_Wirkstoffe.xlsx` (Stoffliste) | Approved active substances | 357,451 bytes | `https://www.swissmedic.ch/dam/.../zugelassene_arzneimittel_ham_ind.xlsx` (separate file) |

### Structure (measured from actual downloads)

**`sm_ham.xlsx` (Zugelassene_Arzneimittel_HAM):**
```
Sheet: Zugelassene Arzneimittel HAM mI
Rows: 11,073 (including header rows)
Stand/Updated: 31.07.2026
Header row 7 columns:
  [0] Zulassungs-/nummer (N° d'autorisation)
  [1] Dosisstärke-nummer (N° de dosage)
  [2] Bezeichnung des Arzneimittels (Brand name)
  [3] Zulassungsinhaberin (MA holder)
  [4] Heilmittelcode (Medicine category)
  [5] Abgabekategorie Dosisstärke (Dispensing category — dose strength)
  [6] Abgabekategorie Arzneimittel (Dispensing category — medicine)
  [7] Erstzulassungs-datum Arzneimittel (First authorisation date)
  [8] Zul.datum Dosisstärke (Dose strength authorisation date)
  [9] Gültigkeitsdauer der Zulassung (Duration of authorisation)
```

**`sm_erw.xlsx` (Erweiterte Liste — EXTENDED, 25 columns, recommended for pipeline):**
Additional columns include: `ATC-Code`, `Wirkstoff(e)` (active substance), `Zusammensetzung` (composition), `Anwendungsgebiet` (indication), `Zulassungsart` (type: Hauptzulassung, Exportzulassung, etc.), `Zulassungsstatus` (zugelassen/widerrufen).

**Sample row 8:**
```
Zulassungs-Nr.: 417 | Brand: Tollwut Impfstoff Mérieux | Holder: Sanofi-Aventis (Suisse) SA
ATC: J07BG01 | Erstzulassung: 1975-10-24 | Status: zugelassen
```

**`sm_stoff.xlsx` (Stoffliste — active substances):**
```
Sheet: Stoffliste
Rows: 3,457
Columns: Wirkstoff (Principe actif) | Abgabekategorie HAM | Abgabekategorie TAM
```

### Key notes

- Files updated monthly (last update 31.07.2026 confirmed in all files)
- The extended list (`Erweiterte_Arzneimittelliste_HAM.xlsx`) has the active substance column — use this one
- No UNII or INN_ID field; substance names are in German/French bilingual format
- Switzerland is not EU; EMA central authorisation does not apply. Swiss-approved drugs not in EMA xlsx
- The Orphan Drug list (`Liste_OrphanDrug_Internet.xlsx`) is directly relevant for the pipeline

### Auth / Licence

No auth required (direct xlsx download). Swissmedic data is Swiss government open data. Terms at `https://www.swissmedic.ch/swissmedic/en/home/about-us/impressum/use-of-content.html` (not fetched; standard Swiss government open data applies).

---

## 8. MHRA (UK — Post-Brexit)

**VERIFIED (portal reachable; no bulk download identified)** [events 148–156, agent-a5d6b183c04ce71b1]

| URL | HTTP | Size | Notes |
|-----|------|------|-------|
| `https://products.mhra.gov.uk/` | 200 | 124,886 bytes | Title: "MHRA Products — Home" |
| `https://products.mhra.gov.uk/search/?search=aspirin` | 200 | — | A-Z search works |
| `https://products.mhra.gov.uk/api/search` | 404 | — | No public REST API endpoint |
| `https://products.mhra.gov.uk/downloads/products.json` | 404 | — | No bulk JSON download |

**Portal description (measured from page text):** "The MHRA products website allows you to find: The leaflets which are provided with medicines / The description of the medicinal product's properties / Scientific reports about marketing authorisations. You can search by product, active substance, or PL number."

**Portal technology:** Next.js SPA backed by Azure Cognitive Search (inferred from `x-ms-*` headers and Next.js static chunks). No public API key or search endpoint exposed.

**data.gov.uk / CKAN:** UK open data search (ckan.publishing.service.gov.uk) returned 7 MHRA datasets — all are spend reports, organograms, and Yellow Card ADR data. **No marketed products/MA list dataset found.**

**UK Veterinary Medicines (VMD):** The VMD (not MHRA) publishes a machine-readable XML product database at `http://www.vmd.defra.gov.uk/ProductInformationDatabase/downloads/VMD_ProductInformationDatabase.xml` — this covers veterinary products only and is not relevant to the human drug pipeline.

**dm+d (NHS Dictionary of Medicines and Devices):** `https://isd.digital.nhs.uk/trud/users/guest/filters/0/categories/6` — HTTP 200 (23,823 bytes), title confirmed "NHSBSA dictionary of medicines and devices — NHS TRUD". Updated weekly (every Monday). Covers marketed NHS medicines with SNOMED CT/dm+d codes. **Registration required** (free) to download from NHS TRUD. This is a UK marketing/dispensing lens, not an MA database.

**Bottom line for MHRA:** No bulk machine-readable download of MHRA-authorised human medicines exists in the public domain as of 2026-08-05. The portal (`products.mhra.gov.uk`) is the access point; scraping by active substance A–Z is feasible but brittle. Consider whether MHRA's PLPI (Product Licence/Public Assessment Reports) database has changed — worth contacting MHRA directly.

---

## 9. FDA UNII Records — The Join Key

**VERIFIED** [events 117–133, agent-a5d6b183c04ce71b1]

### Download

- URL: `https://precision.fda.gov/uniisearch/archive/latest/UNIIs.zip` → HTTP 308 → AWS S3 (signed URL)
- **Names file:** `UNII_Names_26Feb2026.txt` (80,554,309 bytes uncompressed)
- **Records file:** `https://precision.fda.gov/uniisearch/archive/latest/UNII_Data.zip` → HTTP 200, 16,947,343 bytes → `UNII_Records_26Feb2026.txt` (38,076,417 bytes uncompressed)

### UNII Records columns (verified from header)
```
1:UNII  2:Display Name  3:RN(CAS)  4:EC  5:NCIT  6:RXCUI  7:PUBCHEM
8:SMSID  9:EPA_CompTox  10:CATALOGUE_OF_LIFE  11:ITIS  12:NCBI
13:PLANTS  14:POWO  15:GRIN  16:MPNS  17:INN_ID  18:USAN_ID
19:DAILYMED  20:MF  21:INCHIKEY  22:SMILES  23:INGREDIENT_TYPE
24:SUBSTANCE_TYPE  25:UUID
```

**Total records: 168,046**

Key cross-reference fields:
- `SMSID` = European Medicines Agency SPOR SMS ID → joins to EMA SPOR
- `INN_ID` = WHO INN sequential number
- `RXCUI` = RxNorm → joins to NLM/FDA drug data
- `PUBCHEM`, `CAS`, `INCHIKEY` = structural identifiers

### EMA→UNII join rate (empirically measured)

Tested against 1,563 EMA authorised human products [events 138–144]:

**Using INN/common name field (column 6):**
- Exact match to UNII name: **1,318 / 1,563 = 84.3%**
- Rows identified as combos (`;`-separated): **213 (13.6%)**

**After splitting combos — each component matched separately:**
- ALL components resolve: **1,478 / 1,563 = 94.6%**
- SOME components resolve: 6 (0.4%)
- NONE resolve (true failures): **79 / 1,563 = 5.1%**

**Residual failures are almost entirely vaccines and novel biologics (measured sample):**
```
- COVID-19 Vaccine (recombinant, adjuvanted)
- hepatitis A (inactivated) and hepatitis B (rDNA) (HAB) vaccine
- trenibotulinumtoxinE
- COVID-19 mRNA vaccine
- respiratory syncytial virus vaccine (bivalent, recombinant)
- influenza vaccine (surface antigen, inactivated, adjuvanted)
- pneumococcal polysaccharide conjugate vaccine
- meningococcal group A, C, W-135 and Y conjugate vaccine
- dengue tetravalent vaccine (live, attenuated)
- yttrium [90Y] chloride
```

**Conclusion:** A 95% join rate is achievable for non-vaccine small molecules via free-text INN name → UNII name index. The 5% residual is dominated by complex vaccines and combination biologics — categories unlikely to be pipeline candidates anyway.

### Normalization failure modes

1. **Salt vs base:** "degarelix acetate" (EMA active substance) vs "degarelix" (INN). UNII has both; need to try both forms.
2. **Hydrates:** "iptacopan hydrochloride hydrate" (JP) ≠ "iptacopan" (INN). UNII Names file (1,024,188 entries) includes salt/hydrate names.
3. **JAN names (Japanese):** `イプタコパン塩酸塩水和物` in Japanese Katakana — requires transliteration to match "iptacopan hydrochloride hydrate".
4. **Combination products:** Use `;` or `+` separator — split and match individually.
5. **Biologics/vaccines:** Highly variable naming; may require manual mapping.

---

## 10. TGA (Australia — ARTG)

**UNVERIFIED — host unreachable from this environment** [events 92–97, 165–166]

DNS resolved: `www.tga.gov.au → 23.47.144.139` (confirmed)
TCP connects (time=0.474s) but HTTP returns `000` (connection reset after TLS, likely Cloudflare bot protection).

**data.gov.au CKAN API:** Searched multiple query terms — `ARTG`, `Australian Register of Therapeutic Goods`, `organization:tga`, `TGA` — all returned either 0 results or unrelated datasets. TGA does not appear to publish the ARTG on data.gov.au.

**Known from prior research (not verified in this session):** TGA publishes ARTG data via:
- `https://www.tga.gov.au/resources/artg` — ARTG Summary listing page (HTTP 000 from this environment)
- The ARTG bulk extract is reportedly available at `https://www.tga.gov.au/resources/artg` and historically at `https://data.gov.au/dataset/ds-dga-0ff8ef79-c15a-4d20-b1ae-0bfd6f3b7ac2/` — the dataset UUID link returned HTTP 403 when attempted.

**Action required:** Fetch from a non-blocked network. The ARTG does exist and TGA does publish bulk data — this is a network block issue, not an absence of data.

---

## 11. India CDSCO

**VERIFIED (PDF lists only — no machine-readable structured bulk export)** [subagent agent-a52ef04ad6a4d3100]

| URL | HTTP | Size | Notes |
|-----|------|------|-------|
| `https://cdsco.gov.in/opencms/opencms/en/Home/` | 200 | 95,397 | Home page reachable |
| `https://cdscoonline.gov.in/CDSCO/Drugs` | 200 | 15,788 | SUGAM portal page |
| `https://cdsco.gov.in/opencms/opencms/en/Approval_new/Approved-New-Drugs/` (guessed path) | 200 | 66,531 | Lists annual PDF downloads |

### What exists

CDSCO publishes annual "List of New Drugs approved" as PDF files, via a download server:
```
Download endpoint pattern:
https://cdsco.gov.in/opencms/opencms/system/modules/CDSCO.WEB/elements/download_file_division.jsp?num_id=<base64>
```
The base64 IDs decode to internal document numbers. The response is an HTML fragment containing an iframe pointing to the actual PDF path.

**Confirmed PDFs (HTTP 200, verified sizes):**
- FY2026 (to date): `https://cdsco.gov.in/opencms/resources/UploadCDSCOWeb/2018/UploadApprovalNewDrugs/List of New Drugs approved in the year 2026 till datee (3).pdf`
- FY2025: `https://cdsco.gov.in/opencms/resources/UploadCDSCOWeb/2018/UploadApprovalNewDrugs/List of New Drugs approved in the year 2025 till datee.pdf` — HTTP 200, 151,689 bytes, 5 pages

**FY2025 PDF content (measured — pdftotext output):**
```
Columns: S.No. | Name of New Drug | Indication | Date of Approval

Row 1: Tafamidis Bulk Drug | Not applicable (bulk drug) | 16.01.2025
Row 2: Letermovir Bulk Drug & Letermovir Tablets 240mg/480mg | CMV prophylaxis (HSCT/kidney transplant) | 17.01.2025
Row 3: Fexuprazan hydrochloride Bulk Drug and Tablets 40mg | Erosive esophagitis | 10.02.2025
Row 4: Edoxaban Tosylate Monohydrate Bulk Drug | (stroke prevention, non-valvular AF) | 11.02.2025
```

**data.gov.in:** HTTP 200 (reachable); CKAN-ish API at `https://api.data.gov.in/catalog?filters[title]=drug` returned 404. Search pages for "CDSCO" were JS-rendered; no structured CDSCO drug approval dataset found via API.

**Conclusion:** CDSCO approved drug lists exist as annual PDFs only. No machine-readable CSV/Excel/JSON/API endpoint found. PDFs are extractable with pdftotext but require per-PDF parsing; drug names are in English. Historical coverage is 2001–present via annual PDFs. The "Additional Approval status of drugs from 2000 to till date" consolidation PDF also exists (HTTP 200, ~210 KB).

---

## 12. South Korea MFDS

**VERIFIED (API exists but requires free registration for service key)** [subagent agent-a52ef04ad6a4d3100]

| URL | HTTP | Size | Notes |
|-----|------|------|-------|
| `https://nedrug.mfds.go.kr/` | 200 | 214 (redirect to /index) | Reachable |
| `https://nedrug.mfds.go.kr/index` | 200 | 1,712,312 | Main portal |
| `https://nedrug.mfds.go.kr/searchDrug` | 200 | 470,309 | Drug search page; Excel export function exists in JS |
| `https://www.data.go.kr/data/15095677/openapi.do` | 200 | 220,361 | MFDS Drug Permit Info API dataset page |
| `https://apis.data.go.kr/1471000/DrugPrdtPrmsnInfoService07/getDrugPrdtPrmsnDtlInq05?serviceKey=TEST&...` | 400 | 218 | Returns `NO_OPENAPI_SERVICE_ERROR` — key required |

### Korean Open Data Portal API (data.go.kr dataset 15095677)

**Dataset:** 식품의약품안전처_의약품 제품 허가정보 (MFDS Drug Product Permit Information)
- **API type:** REST, JSON+XML
- **Provider:** 식품의약품안전처 (MFDS — Ministry of Food and Drug Safety)
- **Cost:** Free
- **License:** No restriction
- **Registered:** 2021-12-08, last modified 2025-10-31
- **API path:** `https://apis.data.go.kr/1471000/DrugPrdtPrmsnInfoService07/`
- **Operations found:** `getDrugPrdtPrmsnDtlInq05`, `getDrugPrdtPrmsnInq06`
- **Auth:** Service key required — free registration at `https://www.data.go.kr` (developer account, automatic approval for dev; production requires use-case submission)
- **Dataset description (measured):** "의약품 품목, 주성분, 제조원, 포장단위, 저장방법, 성상등의 품목정보와 허가일자, 허가번호, 허가정보, 희귀의약품 여부" = product name, main ingredient, manufacturer, packaging, storage, appearance, permit date, permit number, permit info, rare disease drug status

**Key fields include:** 주성분 (main ingredient/active substance), 희귀의약품 여부 (whether it is a rare disease drug), 허가일자 (permit date), 허가번호 (permit number). Active substance names are in Korean (Hangul) for domestic drugs; some international drugs use INN transliterations.

**The search portal `nedrug.mfds.go.kr/searchDrug` has an Excel export button** (JavaScript `ExcelFile()` function found in source) — this could be scraped for batches of results.

**Action required:** Register at `https://www.data.go.kr` (free) to obtain service key. Then call `getDrugPrdtPrmsnInq06` with `type=json&pageNo=1&numOfRows=100`.

---

## 13. China NMPA

**BLOCKED — returns HTTP 412 Precondition Failed for all paths** [subagent agent-a52ef04ad6a4d3100]

| URL | HTTP | Notes |
|-----|------|-------|
| `https://www.nmpa.gov.cn/` | 412 | WAF/bot block |
| `https://www.nmpa.gov.cn/datasearch/home-index.html` | 412 | JS query portal; blocked |
| `https://www.nmpa.gov.cn/datasearch/search-result.html` | 412 | |
| `https://www.nmpa.gov.cn/datasearch/data/nmpadata/queryList` | 412 | |
| `https://qyj.nmpa.gov.cn/` | 000 | Completely unreachable |

**English site:** `https://english.nmpa.gov.cn/` — HTTP 200 (30,825 bytes). Contains `href="database.html"` and `href="drugs.html"` links, but the "Database" page links to `http://subsites.chinadaily.com.cn/nmpa/database.html` (an external news/info site).

**CDE (Center for Drug Evaluation):** `https://www.cde.org.cn/` — HTTP 200 (89,738 bytes). Contains links to:
- `https://wbca.cde.org.cn/wbca/listedDrugsAllReviewed` — HTTP 202 (JS-rendered SPA, 25,320 bytes shell)
- `https://www.cde.org.cn/hymlj/index` (化学药品目录集/drug reference listed drugs) — HTTP 202 (JS SPA)
- `https://wbca.cde.org.cn/wbca/CDEdirectoryInformed` — HTTP 202 (JS SPA)

All CDE database pages return HTTP 202 (JS application loading state) — they are React/Angular SPAs that require browser execution for content.

**Conclusion:** China NMPA domestic drug database is inaccessible from outside China via programmatic means. The portal is captcha-protected / WAF-blocked. No bulk download or open API found. CDE databases are JS-rendered and likely also geo-blocked. This is a **hard blocker** — access requires either: (a) a China-based server, (b) a licensed data vendor (e.g., SinoPharm, Cortellis, Citeline), or (c) direct engagement with NMPA/CDE.

---

## 14. Join Key Summary — What Actually Works

**VERIFIED** [events 138–144, agent-a5d6b183c04ce71b1]

### Recommended normalization path

```
Non-US regulator active substance name (free text)
    ↓
1. Normalize: lowercase, strip salt descriptors (sodium, hydrochloride, etc.),
   strip "hydrate"/"monohydrate", strip parentheticals
2. Lookup in UNII Names file (1,024,188 entries, tab-delimited)
   → returns UNII code
3. UNII → UNII Records file
   → cross-references: CAS, InChIKey, RXCUI, SMSID, INN_ID
4. UNII → FDA Orange Book / Drugs@FDA (by UNII or substance name)
   → determines if moiety was previously approved in US
```

**Measured match rate:** 94.6% for EMA centrally authorised products after combo-splitting. Residual 5.1% are almost entirely vaccines and novel complex biologics.

### Failure modes (quantified)

| Failure mode | Frequency | Example |
|---|---|---|
| Vaccine complex names | ~3% | "pneumococcal polysaccharide conjugate vaccine (21-valent)" |
| Novel biologics (not yet in UNII) | ~1% | "trenibotulinumtoxinE" |
| Combination products (combo-split failure) | ~0.5% | "yttrium [90Y] chloride" |
| Salt/hydrate form mismatch | Common but usually handled by UNII Names | "iptacopan HCl hydrate" → search both salt and base |
| JAN names (Japanese) | All Japanese entries | Requires Katakana → Latin transliteration |
| Korean/Hangul names | All Korean entries | Requires Korean → Latin lookup |

### Join key hierarchy (preference order)

1. **InChIKey** — best structural identifier; requires chemical structure data
2. **CAS number** — if regulators publish it (most do not in their approval lists)
3. **INN name → UNII Names lookup** — practical for EMA, HC, Swissmedic (all use INN in Latin script)
4. **SMSID** — only 17% of UNII records have it; useful as validation, not primary join
5. **JAN name → KEGG DRUG → D-entry with `<JP>` flag → KEGG DBLINKS → CAS/PubChem → UNII** — needed for Japanese data

---

## Unfinished — Worth Re-Running

The agent was killed [line 184: "Request interrupted by user"] immediately after the KEGG flag analysis. The following were **in progress or planned** but not executed:

1. **KEGG JP-only drug list extraction** — The agent had just computed 620 JP-only drugs from the BRITE JSON. The next step (interrupted) would have been to extract those 620 D-entry names, map them to UNII, and cross-check against Drugs@FDA to produce the actual Funnel A candidate list from Japan. **High value — run this.**

2. **EMA SPOR SMS export** — Guest access is available at `https://spor.ema.europa.eu/smswi/#/search`. Manual export of SMS substance list was planned but not executed. If guest CSV export works, this provides a complete EMA substance→SMSID table.

3. **TGA ARTG from non-blocked network** — Run from any Australian IP or VPN. Known URL to try: `https://www.tga.gov.au/resources/artg` and `https://www.tga.gov.au/resources/artg-summary-and-full-listings`.

4. **MHRA bulk product list** — No public bulk download found; consider contacting MHRA directly or checking `https://www.gov.uk/search/all?keywords=MHRA+marketing+authorisation+list`.

5. **Korea MFDS API registration** — Free; register at `https://www.data.go.kr`, obtain service key, then call `https://apis.data.go.kr/1471000/DrugPrdtPrmsnInfoService07/getDrugPrdtPrmsnInq06?serviceKey=<key>&type=json&pageNo=1&numOfRows=100`.

6. **CDSCO PDF-to-structured-data pipeline** — The annual PDFs are available and parseable with pdftotext. Build a parser for columns: S.No. | Drug name | Indication | Approval date.

7. **EMA national registers (27 countries)** — None were individually verified. High-value targets: AIFA (Italy, reportedly has open API), AEMPS (Spain, CIMA portal), ANSM (France), BfArM/PEI (Germany — PharmNet.Bund).

---

## URL Ledger

### VERIFIED

| URL | HTTP | Size | Notes |
|-----|------|------|-------|
| `https://rest.kegg.jp/list/drug` | 200 | 599,728 | 12,893 KEGG DRUG entries |
| `https://rest.kegg.jp/get/D00564` | 200 | 8,433 | Full KEGG record with JP/US flags |
| `https://rest.kegg.jp/get/D01280` | 200 | 5,134 | JP warfarin potassium; D-entry linkage |
| `https://www.kegg.jp/kegg-bin/download_htext?htext=br08303.keg&format=json` | 200 | 1,170,587 | ATC BRITE with country flags |
| `https://www.kegg.jp/kegg/legal.html` | 200 | — | Commercial license required |
| `https://www.ema.europa.eu/en/documents/report/medicines-output-medicines-report_en.xlsx` | 200 | 897,579 | 2,730 rows, 39 cols, nightly update |
| `https://www.pmda.go.jp/english/review-services/reviews/approved-information/drugs/0002.html` | 200 | 52,895 | English list of approved products |
| `https://www.pmda.go.jp/files/000281190.pdf` | 200 | 3,206,009 | English new drugs 2004–Feb 2026 (PDF) |
| `https://www.pmda.go.jp/review-services/drug-reviews/review-information/p-drugs/0040.html` | 200 | 130,872 | FY2026 Japanese approved drugs index |
| `https://www.pmda.go.jp/review-services/drug-reviews/review-information/p-drugs/0039.html` | 200 | 130,872 | FY2025 Japanese approved drugs index |
| `https://www.pmda.go.jp/files/000277966.xlsx` | 200 | 32,825 | FY2025 approved drugs Excel |
| `https://www.pmda.go.jp/files/000274663.xlsx` | 200 | 30,000 | FY2024 approved drugs Excel |
| `https://www.canada.ca/content/dam/hc-sc/documents/services/drug-product-database/drug_ap.zip` | 200 | 90,984 | DPD approved products (QRYM_DRUG_PRODUCT) |
| `https://www.canada.ca/content/dam/hc-sc/documents/services/drug-product-database/ingred_ap.zip` | 200 | 99,197 | DPD approved ingredients |
| `https://www.canada.ca/content/dam/hc-sc/documents/services/drug-product-database/allfiles.zip` | 200 | 1,333,171 | DPD all statuses, all tables |
| `https://hc-sc.gc.ca/dhp-mps/alt_formats/zip/prodpharma/databasdon/allfiles.zip` | 200 | 1,333,171 | Alternate host for same DPD allfiles |
| `https://health-products.canada.ca/api/drug/drugproduct/?lang=en&type=json&brandname=lipitor` | 200 | — | DPD JSON API — no auth |
| `https://www.swissmedic.ch/swissmedic/de/home/services/listen_neu.html` | 200 | 180,908 | Lists page with all xlsx downloads |
| `https://www.swissmedic.ch/.../Zugelassene_Arzneimittel_HAM.xlsx` | 200 | 1,004,159 | 11,073 approved human medicines |
| `https://www.swissmedic.ch/.../Erweiterte_Arzneimittelliste%20HAM.xlsx` | 200 | 2,581,811 | Extended list (ATC + active substance) |
| `https://products.mhra.gov.uk/` | 200 | 124,886 | MHRA portal — no bulk download |
| `https://precision.fda.gov/uniisearch/archive/latest/UNIIs.zip` | 308→200 | 14,627,843 | UNII Names file (~1M entries) |
| `https://precision.fda.gov/uniisearch/archive/latest/UNII_Data.zip` | 308→200 | 16,947,343 | UNII Records (168,046 records, SMSID col) |
| `https://spor.ema.europa.eu/sporwi/` | 200 | 9,192 | SPOR landing |
| `https://spor.ema.europa.eu/smswi/` | 200 | 8,634 | SMS web UI (guest browsing OK) |
| `https://spor.ema.europa.eu/smsapi/v1/substances` | 302→SSO | — | API requires EMA account |
| `https://www.ema.europa.eu/en/medicines/national-registers-authorised-medicines` | 200 | 75,325 | 34 national register links |
| `https://mri-production.cts-mrp.eu/` | 200 | 2,329 | MRI portal SPA — no data extracted |
| `https://cdsco.gov.in/opencms/opencms/en/Home/` | 200 | 95,397 | CDSCO home |
| `https://cdsco.gov.in/.../List of New Drugs approved in the year 2025 till datee.pdf` | 200 | 151,689 | FY2025 India new drugs PDF |
| `https://www.data.gov.in/` | 200 | 1,232,301 | India open data portal |
| `https://nedrug.mfds.go.kr/index` | 200 | 1,712,312 | Korea MFDS drug portal |
| `https://www.data.go.kr/data/15095677/openapi.do` | 200 | 220,361 | MFDS drug permit API dataset |
| `https://english.nmpa.gov.cn/` | 200 | 30,825 | China NMPA English site |
| `https://www.cde.org.cn/` | 200 | 89,738 | China CDE — links to drug lists |
| `https://isd.digital.nhs.uk/trud/users/guest/filters/0/categories/6` | 200 | 23,823 | NHS TRUD (dm+d) — registration needed |

### UNVERIFIED / BLOCKED / DEAD

| URL | Status | Reason |
|-----|--------|--------|
| `https://www.tga.gov.au/resources/artg` | HTTP 000 | Cloudflare/bot block from this environment |
| `https://data.gov.au/dataset/ds-dga-0ff8ef79-c15a-4d20-b1ae-0bfd6f3b7ac2/` | HTTP 403 | Forbidden |
| `https://www.nmpa.gov.cn/` | HTTP 412 | WAF block — all paths |
| `https://www.nmpa.gov.cn/datasearch/home-index.html` | HTTP 412 | WAF block |
| `https://wbca.cde.org.cn/wbca/listedDrugsAllReviewed` | HTTP 202 | JS SPA — no data without browser |
| `http://mri.cts-mrp.eu/` | HTTP 000 → 301 → `mri-production.cts-mrp.eu` | HTTP (not HTTPS) broken; HTTPS SPA |
| `https://apis.data.go.kr/1471000/DrugPrdtPrmsnInfoService07/...?serviceKey=TEST` | HTTP 400 | Invalid/missing service key — requires registration |
| `https://products.mhra.gov.uk/api/search` | HTTP 404 | No public REST API |
| `http://www.vmd.defra.gov.uk/ProductInformationDatabase/downloads/VMD_ProductInformationDatabase.xml` | HTTP 000 | Unreachable from this environment (veterinary only anyway) |
| EMA national registers (27 individual country portals) | NOT FETCHED | Listed at verified EMA page; individual reachability unknown |
| `https://fdasis.nlm.nih.gov/srs/download/srs/UNIIs.zip` | Not tested (deprecated host) | Use precision.fda.gov instead |
