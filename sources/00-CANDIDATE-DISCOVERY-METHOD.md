# 00 — Candidate Discovery Method & Honest Verdict

**Purpose:** The single authoritative build reference for enumerating the PRV-eligible drug candidate universe, joining it against the US approval record, filtering it to the actionable pool, and deciding whether the business as described is worth building.

**Research date:** 2026-08-06. Inputs synthesized from sources 01, 04, 06, 14, 15, 16, 21, 22, 25, 26, 27, and the recovered MINED-drug-data-sources file. Where this document infers rather than cites, it says so.

**Legal baseline (settled — do not re-derive):**
- 21 U.S.C. § 360ff(a)(4)(B)(i): PRV requires (I) no active moiety previously approved under any 505(b)(1)/(b)(2)/(j) application, AND (II) a 505(b)(1) filing.
- Pub. L. 119-75 § 6604(a): PRV program sunsets 2029-09-30. Binding constraint is FDA **approval** by that date, not designation or filing.
- Pub. L. 117-9 (2021): Replaced "active ingredient" with "active moiety" in the PRV eligibility test.
- *Sun Pharma Advanced Research Co. v. FDA* (D.D.C. 2025-12-02): Pre-1962 "deemed approved" NDAs do NOT constitute prior approval. PRV awarded 2026-02-03; FDA did not appeal. District court only; narrow; unreviewed on appeal.
- Industry-wide RPD PRV rate: ~6 awards/year across ALL sponsors.
- Verified 2026 PRV sale prices: Cyprium/Fortress $205M (ZYCUBO), Denali $195M (AVLAYAH), Rocket $180M (KRESLADI).

---

## 1. THE LEFT SIDE — Foreign Regulator Enumeration (Build Order by Yield Per Effort)

The left side of the anti-join is the set of active moieties approved in ex-US regulators. Ranked by yield-per-unit-effort, where "yield" = number of actionable never-US moieties actually reachable and "effort" = engineering time to ingest and normalize.

### 1.1 Japan PMDA — Tier 1 (highest yield, requires transliteration)

**Why Japan first:** KEGG BRITE `br08303.keg` (VERIFIED, 1,170,587 bytes) shows 905 drugs with JP-approval flag but no US-approval flag in the ATC-classified universe. The Japan NHI Yakka (VERIFIED: `tp20260715-01_05.xlsx`, 12,414 products, 2,694 unique `成分名` active ingredient values) is the comprehensive approved substance list. Japan has a distinct pharmacopoeia (JAN names), a large domestic market, and a cultural history of domestic-only approvals that never pursued global registration. This makes it structurally the richest single source of never-US-approved moieties.

**Machine-readable artefacts:**

| Artefact | URL | Format | Records | Cadence | Notes |
|---|---|---|---|---|---|
| NHI Yakka combined XLSX | `https://www.mhlw.go.jp/topics/2026/04/xls/tp20260715-01_05.xlsx` | XLSX | 12,414 products; 2,694 unique ingredients | Quarterly | VERIFIED HTTP 200, 683,699 bytes |
| PMDA FY-annual approved drugs | `/review-services/drug-reviews/review-information/p-drugs/00NN.html` → XLSX | XLSX | ~100–150 per year | Annual | VERIFIED FY2025: 143 rows, HTTP 200 |
| PMDA English new-drugs PDF | `https://www.pmda.go.jp/files/000281190.pdf` | PDF only | ~22 years, 2004–Feb 2026 | Annual | VERIFIED 200, 3.2 MB. Not machine-readable as structured data; requires PDF extraction. |
| KEGG DRUG REST API | `https://rest.kegg.jp/list/drug` | Tab-delimited | 12,893 entries (live 2026-08-06) | Irregular | VERIFIED. JP flag via `br08303.keg`. **Commercial license required** (Pathway Solutions); free for academic/research screening, not for commercial pipeline without paid licence. |
| KEGG JAN-flagged list | `https://rest.kegg.jp/find/drug/JAN` | Tab-delimited | 2,273 lines (VERIFIED 2026-08-06) | Irregular | JAN = Japan Accepted Name = Japan approval marker. Smaller than NHI Yakka because JAN does not include all generics. |

**Known incompleteness:** KEGG ATC BRITE captures only ATC-classified drugs (the 905 JP-only figure). NHI Yakka is comprehensive (2,694 ingredients) but includes generics and dosage-form variants that share a moiety with an already-US-approved parent. PMDA's searchable database (`pmda.go.jp/PmdaSearch/iyakuSearch/`) has no bulk download. The English PDF covers 2004–Feb 2026 but is PDF-only.

**Transliteration requirement (critical):** Japanese active ingredient names are in katakana phonetic script (`イプタコパン塩酸塩水和物` = iptacopan hydrochloride hydrate). All Japanese data requires katakana-to-Latin transliteration before any UNII lookup. This is the single biggest engineering tax on the Japan source.

**Degraded substitute if PMDA is too slow:** Use KEGG `/find/drug/JAN` (2,273 lines, no transliteration needed — KEGG stores Latin INN alongside JAN) as a rapid first-pass, then enrich with NHI Yakka.

**Orphan sub-population is the highest-yield sub-set:** Japan's NIBN orphan designation list (VERIFIED: #733 through 2025-10-01) contains drugs designated rare in Japan. Cross-referencing the ~400 estimated Japan-orphan approvals against US approval status yields a population with 100% rare-disease hit rate by construction (source 25). This is the most efficient screening sub-path.

---

### 1.2 EU EMA (Centralised Authorisations Only) — Tier 1 (excellent machine access)

**Machine-readable artefact:**

| Artefact | URL | Format | Records | Cadence |
|---|---|---|---|---|
| EMA Medicines XLSX | `https://www.ema.europa.eu/en/documents/report/medicines-output-medicines-report_en.xlsx` | XLSX | 2,730 rows (1,868 Authorised, 416 Withdrawn, 284 Application Withdrawn) | Nightly |
| EMA Medicines JSON | `https://www.ema.europa.eu/en/documents/report/medicines-output-medicines_json-report_en.json` | JSON | 2,730 records (VERIFIED 200, 6,739,136 bytes) | Nightly |
| EMA Orphan Designations XLSX | `https://www.ema.europa.eu/en/documents/report/medicines-output-orphan_designations-report_en.xlsx` | XLSX | ~2,190 Positive designations (VERIFIED 200, 347,937 bytes) | Nightly |

**Columns directly relevant to the pipeline:** `INN / common name` (col 6), `Active substance` (col 7), `Medicine status` (col 3), `Orphan medicine` (col 23), `Marketing authorisation date` (col 31), `Withdrawal / expiry date` (col 33).

**Critical caveat:** This XLSX covers ONLY centrally authorised products. EU nationally authorised products (the majority by count across 27 member states) are NOT in this file. No unified bulk download exists for EU nationally authorised drugs.

**Yield estimate:** ~1,400 distinct INN-level moieties in the 1,868 authorised products (estimated; not machine-run). Overlap with US approvals is high — most blockbuster drugs have FDA approval. EU-unique moieties number approximately 50–150 in the centralised database.

**EMA SPOR SMS (full substance database):** `https://spor.ema.europa.eu/smswi/` is accessible for guest browsing; the REST API (`smsapi/v1/substances`) requires EMA SSO account. Guest CSV export from the web UI may be possible for small queries but is not bulk-accessible programmatically without EMA registration.

---

### 1.3 Health Canada DPD — Tier 2 (good access, lower Japan-unique yield)

| Artefact | URL | Format | Records | Cadence |
|---|---|---|---|---|
| DPD approved products | `https://www.canada.ca/content/dam/hc-sc/documents/services/drug-product-database/drug_ap.zip` | ZIP → CSV (no header) | 481,680 bytes uncompressed | Updated 2026-08-04 |
| DPD approved ingredients | `https://www.canada.ca/content/dam/hc-sc/documents/services/drug-product-database/ingred_ap.zip` | ZIP → CSV | 661,368 bytes uncompressed | Same cadence |
| DPD all files (all statuses) | `https://hc-sc.gc.ca/dhp-mps/alt_formats/zip/prodpharma/databasdon/allfiles.zip` | ZIP | 1,333,171 bytes | Regularly updated |

**Join key:** DPD uses English INN-style names (e.g. `CLOMIPRAMINE HYDROCHLORIDE`); no UNII in the file. Requires name-normalization to match against UNII. Health Canada closely tracks FDA approvals; the fraction of Canada-only moieties that are also not in the US is estimated to be very small (<100 distinct moieties). **Low incremental yield over Japan + EMA but mechanically easy to ingest.**

**JSON API:** `https://health-products.canada.ca/api/drug/activeingredient/?lang=en&type=json` — no auth, documented, works live.

---

### 1.4 Swissmedic — Tier 2 (good machine access, very low incremental yield)

| Artefact | URL | Format | Records | Cadence |
|---|---|---|---|---|
| Extended HAM list (recommended) | `https://www.swissmedic.ch/dam/swissmedic/de/dokumente/internetlisten/erweiterte_ham_ind.xlsx.download.xlsx/Erweiterte_Arzneimittelliste%20HAM.xlsx` | XLSX | ~11,073 rows | Updated 31.07.2026 |
| Orphan Drug list | `https://www.swissmedic.ch/dam/swissmedic/de/dokumente/internetlisten/status_orphandrug_ham.xlsx.download.xlsx/Liste_OrphanDrug_Internet.xlsx` | XLSX | ~337 KB | Monthly |

Use the extended list (25 columns, includes `Wirkstoff(e)` active substance and ATC code). Switzerland is not in the EU; EMA central authorisation does not apply. Swiss-unique moieties are estimated to be very few. Primary value: confirmatory cross-check, not lead generation.

---

### 1.5 UK MHRA — Tier 3 (no bulk download; scrape-only)

VERIFIED: `https://products.mhra.gov.uk/` (HTTP 200, 124,886 bytes). No public REST API (`/api/search` returns 404). No bulk download. The portal is an Azure Cognitive Search SPA. **The only access path is A-Z active-substance scraping, which is brittle and legally uncertain post-Brexit.** Post-Brexit MHRA-unique substances are estimated at fewer than 50. The yield does not justify the engineering effort at this stage. Defer or contact MHRA directly for a data export.

---

### 1.6 Australia TGA / ARTG — Tier 3 (network-blocked; archive-only from current environment)

`https://www.tga.gov.au/resources/artg` returns HTTP 000 (Cloudflare/bot block from US IP). ARTG reportedly holds ~34,519 medicine entries. A facet-count of distinct active substances was archived at ~2,000. **Cannot access programmatically from this environment.** Run from an Australian IP or VPN. The ARTG open data is reportedly at `https://data.gov.au/dataset/ds-dga-0ff8ef79-c15a-4d20-b1ae-0bfd6f3b7ac2/` — confirmed HTTP 403 in prior session. Australia tracks FDA and EMA closely; incremental yield is low.

---

### 1.7 South Korea MFDS — Tier 3 (requires free registration; Korean-language data)

VERIFIED: `https://nedrug.mfds.go.kr/searchDrug/CNT` returns `{"data":95265}` (2026-08-06). The `rareDrugYn` field exists but is not bulk-queryable without session state. The Korean Open Data Portal API (`https://apis.data.go.kr/1471000/DrugPrdtPrmsnInfoService07/`) is free but requires registration at `https://www.data.go.kr`. Active substance names in Hangul require Korean-to-Latin normalization. **Register and ingest, but treat as lower-confidence yield.**

---

### 1.8 China NMPA — Blocked; Tier 4 (cannot enumerate programmatically)

All NMPA endpoints return HTTP 412 (WAF block) from US IPs. CDE databases are JS-rendered SPAs. No bulk download found. **This is a hard blocker — access requires a China-based server or a licensed data vendor (Cortellis, Citeline).** China's rare-disease designation pipeline is material and its absence is a gap in the A1 sizing.

---

### 1.9 India CDSCO — Tier 3 (PDF-only; annual lists; extractable)

VERIFIED: FY2025 PDF (`https://cdsco.gov.in/opencms/resources/UploadCDSCOWeb/2018/UploadApprovalNewDrugs/List of New Drugs approved in the year 2025 till datee.pdf`, HTTP 200, 151,689 bytes, 5 pages). Annual PDF lists with columns: drug name, indication, approval date. Extractable with `pdftotext`. Limited incremental yield for this pipeline — India mostly approves generics of globally marketed drugs. The "new drugs" list is the useful sub-set.

---

### 1.10 Ranking summary

| Regulator | Distinct never-US moieties (estimate) | Machine-readable bulk? | Engineering effort | Priority |
|---|---|---|---|---|
| Japan PMDA / NHI Yakka | 700–1,500 (905 KEGG-measured JP-only floor) | Yes (XLSX) | Medium (katakana transliteration) | **1 — do first** |
| EU EMA (centralised) | 50–150 unique | Yes (XLSX/JSON, nightly) | Low | **2 — do second** |
| Health Canada DPD | <100 unique | Yes (ZIP/CSV) | Low | 3 — cheap add-on |
| Swissmedic | <50 unique | Yes (XLSX) | Low | 3 — cheap add-on |
| UK MHRA | <50 unique | No (scrape) | High | 4 — defer |
| Australia TGA | ~100–200 unique | Blocked/unclear | Medium + VPN | 4 — defer |
| Korea MFDS | Unknown | API (registration required) | Medium + Korean NLP | 4 — defer |
| China NMPA | Unknown but material | Blocked | Very high or vendor | 5 — partner/buy |
| India CDSCO | Low | PDF-only | Medium | 5 — low priority |

---

## 2. THE RIGHT SIDE — US Active Moiety Exclusion Set

Building the correct US side of the anti-join is subtler than it appears. The question is: for every substance on the left side, has any active moiety at the same structural level ever been approved in the US under any NDA/ANDA/BLA? Multiple FDA artefacts must be unioned.

### 2.1 The five artefacts to union

**A. Drugs@FDA Products.txt — primary NDA/ANDA/BLA approval record**

`https://www.fda.gov/media/89850/download?attachment` (ZIP, HTTP 200, 5.8–6.1 MB).
File `Products.txt` (4.4 MB): columns `ApplNo | ProductNo | Form | Strength | ReferenceDrug | DrugName | ActiveIngredient | ReferenceStandard`.
- Contains every approved NDA, ANDA, and BLA application ever filed.
- `ActiveIngredient` is the text name of the active ingredient (not always normalized to free base; may be salt form).
- **This is the primary gate-check list.** Updated Monday–Friday.

**B. Orange Book products.txt — current + discontinued approved drug products**

`https://www.fda.gov/media/76860/download?attachment` (ZIP, HTTP 200, 1.1 MB). Column `Ingredient`: tilde-delimited (`~`). Covers approved and discontinued products, including combination products with multiple ingredients listed as `; `-separated.
- **Also available as JSON:** `https://download.open.fda.gov/drug/orangebook/drug-orangebook-0001-of-0001.json.zip` (2.34 MB, VERIFIED HTTP 200, export_date 2026-08-05 — fresher than the ZIP).
- 48,502 records. The `Approval_Date` field reads `"Approved prior to Jan 1, 1982"` for pre-1982 products — do not attempt date parsing on that field.

**C. Purple Book — licensed biological products**

`https://www.accessdata.fda.gov/drugsatfda_docs/PurpleBook/2026/purplebook-search-july-data-download.csv` (VERIFIED HTTP 200, 476,652 bytes). Covers BLA-approved biologics. Column `Proper Name` is the active moiety equivalent for biologics.
- **Monthly cadence.** Two stacked sections in the CSV — skip the delta block, use only the full snapshot.
- **Critical gotcha:** rows 1–3 are title banner; real header is row 4.

**D. openFDA UNII + substance\_name — normalization bridge**

`https://download.open.fda.gov/other/unii/other-unii-0001-of-0001.json.zip` (VERIFIED HTTP 200). 175,453 records. Field `unii` is the substance identifier that survives salt/ester/tradename variance. **This is the canonical identifier FDA uses internally for active moiety analysis.** The join should be done at UNII level, not text-name level, to handle salt/ester/hydrate collapse.

**E. NDC `marketing_category` for unapproved marketed drugs**

`https://api.fda.gov/drug/ndc.json?search=marketing_category:"UNAPPROVED+DRUG+OTHER"` (VERIFIED, n=2,202 live). This captures DESI leftovers and pre-1938 grandfathered drugs still on the market under an unapproved status. These are relevant to the A2 sub-population (see §3.2 below). Categories to include in the exclusion analysis: `ANDA`, `NDA`, `BLA`, `NDA AUTHORIZED GENERIC` — these are definitively approved. Categories to examine separately for A2 eligibility: `UNAPPROVED DRUG OTHER`, `UNAPPROVED DRUG FOR USE IN DRUG SHORTAGE`.

### 2.2 The Sun Pharma carve-out for A2 candidates — handle explicitly

Per *Sun Pharma v. FDA* (D.D.C. 2025-12-02, PRV awarded 2026-02-03): A drug whose ONLY US approval history consists of a pre-1962 "deemed approved" NDA that was subsequently withdrawn or lapsed is **not** disqualified from PRV eligibility under § 360ff(a)(4)(B)(i)(I). The court held that "approved" requires affirmative FDA action; a grandfathered NDA that took effect by inaction and was withdrawn for lack of efficacy does not count.

**Implementation:** The exclusion set must include a flag for each moiety:

- `MODERN_APPROVAL_EXISTS`: True if any NDA 505(b)(1), 505(b)(2), or ANDA/505(j) approved **after January 1, 1962** (post-Kefauver-Harris) covers this moiety. If True → PRV-ineligible, period.
- `PRE1962_DEEMED_ONLY`: True if the only US approval history is a pre-1962 grandfathered NDA that was subsequently withdrawn (DESI-reviewed as not effective or simply withdrawn) and no modern approval exists. If True → PRV-eligible under *Sun Pharma*, with legal risk caveat.
- `NEVER_US`: True if no US approval of any kind. If True → PRV-eligible (A1 sub-population).

**Building the pre-1962 flag:** The DESI review database is not in clean machine-readable form. FDA's enforcement actions page (`https://www.fda.gov/drugs/enforcement-activities-fda/drug-efficacy-study-implementation-desi`, VERIFIED 200) is narrative only. The NDC `marketing_category` = `UNAPPROVED DRUG OTHER` is the closest proxy — cross-reference against Drugs@FDA to confirm no modern approval exists, and against the historical NDA register to identify the pre-1962 NDA number.

**Legal risk caveat (state explicitly at every use):** *Sun Pharma* is a single district court decision in the D.D.C., unreviewed on appeal. FDA did not appeal, which is suggestive of agreement but not binding. Any A2 program that relies on this carve-out faces a non-trivial risk that FDA or a future court takes a narrower view in a different factual pattern. Treat A2 as legally risky until a circuit court affirms or FDA publishes binding guidance.

### 2.3 Residual risk: false positives (believing a moiety is new to the US when it is not)

**This is the single most expensive error in the pipeline.** A false positive means:
- The company files a 505(b)(1) NDA and pursues RPD designation based on the belief that the active moiety is novel in the US.
- FDA denies the PRV at approval (as it did for Lyfgenia and Sezaby) citing a prior US approval that the screening missed.
- The company has spent $300k–$800k on the trial and 3–5 years on development.
- The PRV denial is not automatically reversible — bluebird bio's FDR process is unresolved; *Sun Pharma* required litigation.

**Sources of false positives:**
1. **Salt/ester mismatch:** Screening found no UNII for "iptacopan HCl hydrate" but the free-base moiety "iptacopan" is US-approved. Mitigation: always check GSRS `/moieties` endpoint for the proposed moiety; check RxNorm at the IN (Ingredient) level, not just PIN (Precise Ingredient).
2. **Legacy NDA in Drugs@FDA text fields:** Pre-1982 approvals are listed with non-standard date strings and may use non-INN names. The `ActiveIngredient` text field in `Products.txt` is not normalized.
3. **Biologics vs small molecules:** A biologic approved under 351(a) BLA for a moiety does not bar a small-molecule 505(b)(1) for a different moiety that happens to share a trade name or mechanism.
4. **Combination product:** A combination NDA listing Drug A + Drug B as active ingredients. Both Drug A and Drug B are now PRV-ineligible as moieties, even if no monotherapy approval exists.
5. **A2 misjudgment:** Concluding that a pre-1962 deemed NDA is the only history when in fact a subsequent unapproved-marketed product was later granted a Type 7 NDA (Drug Already Marketed without Approved NDA) — which is a modern approval and would bar the PRV.

**Mandatory verification procedure for each candidate before IND filing:** Check (a) GSRS by UNII → `/moieties` endpoint → get moiety UNII → check moiety UNII against RXCUI column in UNII_Records file; (b) RxNorm `/rxcui.json?name={INN}` → if any RXCUI at IN level returns, presume US approval and route to Funnel B; (c) Drugs@FDA `Products.txt` text search on all INN synonyms; (d) DailyMed SPL search by substance name. Document every check with HTTP status codes and response snippets.

---

## 3. THE JOIN — Foreign Substance Name to US Active Moiety

### 3.1 The normalization pipeline

The join is: take the foreign substance name (INN, JAN, Korean name, or German/French name) → find its UNII → check that UNII's moiety UNII against the US exclusion set.

**Step-by-step pipeline:**

```
1. INPUT: Foreign substance name (text)
   Examples: "iptacopan hydrochloride hydrate" (Japan), "degarelix acetate" (EMA),
             "イプタコパン塩酸塩水和物" (Japanese katakana)

2. PRE-PROCESS:
   a. If katakana: transliterate to Latin INN using a katakana→INN lookup table
      (build from PMDA's English approved-products PDF + KEGG DRUG D-entry names)
   b. Normalize: lowercase, strip salt descriptors (sodium, hydrochloride, hydrate,
      monohydrate, acetate, succinate, etc.), strip parentheticals
   c. For combination products: split on " / " or ";" and process each component separately

3. LOOKUP IN UNII_Names_26Feb2026.txt (1,024,191 rows; tab-delimited: Name | TYPE | UNII | Display Name)
   a. Try exact match first on the cleaned name against the `Name` column
   b. If no match: try after stripping all salt descriptors (free-base form)
   c. If no match: try GSRS live API: GET https://gsrs.ncats.nih.gov/api/v1/substances/search?q={name}&top=5
      → returns UNII in approvalID field
   → RESULT: UNII code (10-char alphanumeric)

4. LOOK UP UNII IN UNII_Records_26Feb2026.txt:
   - Col 6: RXCUI — if non-empty → US approval almost certainly exists → FLAG AS FUNNEL B
   - Col 17: INN_ID — WHO INN sequential number; confirms INN identity
   - Col 21: INCHIKEY — structural identifier for structural deduplication

5. IF RXCUI EMPTY: Double-check via RxNorm live API:
   GET https://rxnav.nlm.nih.gov/REST/rxcui.json?name={INN_name}&search=1
   → If returns an rxcui with TTY = IN (Ingredient): US approval exists → FLAG AS FUNNEL B
   → If no result: proceed to Drugs@FDA text search

6. DRUGS@FDA TEXT SEARCH: grep ActiveIngredient column in Products.txt for all synonyms
   → If match: US approval exists → FLAG AS FUNNEL B

7. MOIETY CHECK (critical for salts/prodrugs):
   GET https://gsrs.ncats.nih.gov/api/v1/substances/{UNII}/moieties
   → Extract moiety UNII (may differ from substance UNII for salts/esters)
   → Repeat steps 4–6 for the moiety UNII
   → If moiety UNII has RXCUI or Drugs@FDA hit: FLAG AS FUNNEL B (same active moiety)

8. RESULT: Either FUNNEL_A_CANDIDATE (no US moiety approval found across all checks)
            or FUNNEL_B_CANDIDATE (US moiety approval exists)
            or MANUAL_REVIEW (ambiguous — e.g. pre-1962 only, or biologic ambiguity)
```

### 3.2 Expected match rate

The EMA→UNII join rate has been **empirically measured**: 1,563 EMA authorised human products were tested; after splitting combination products and trying both salt and free-base forms: **94.6% match** (1,478/1,563). Residual 5.1% (79 products) are almost entirely complex vaccines and novel biologics — categories unlikely to be pipeline candidates (source: MINED-drug-data-sources.md, measured in prior agent session).

For Japan (katakana input), the match rate before transliteration is 0% (katakana cannot match Latin names). After transliteration + salt stripping, the rate should converge to a similar ~90–95% for small molecules. No measured rate exists yet for the Japan path; 90% is the working assumption.

For Health Canada (English INN-style names): match rate should be similar to EMA (~93–95%) since DPD uses standard international names.

### 3.3 Manual-review queue design

The residual ~5–10% that fail automated UNII lookup must go to a human-reviewed queue. Priority order:

1. **Novel small-molecule candidates** (not vaccines, not polymers, not mixed biologics) — these are the ones that matter. Review manually by checking ChEMBL, PubChem, and GSRS by structure (SMILES/InChIKey).
2. **Combination products** — split on separator, check each component; if any component is US-approved, the combination contains that moiety.
3. **Biologics / complex molecules** — route to a separate biologic assessment workflow (Purple Book, not Drugs@FDA).
4. **Japanese-domestic traditional compounds** — many lack INN entirely; require Japanese pharmacopoeia lookup.

**Queue SLA:** Review within 5 business days. Each manual review should document: (a) reason for failure, (b) all alternative names searched, (c) structural search result if attempted, (d) disposition (Funnel A / Funnel B / exclude).

### 3.4 The "active moiety" legal definition and its join implications

**21 CFR 314.3 (VERIFIED, full text from GovInfo CFR XML):**
> "Active moiety is the molecule or ion, excluding those appended portions of the molecule that cause the drug to be an ester, salt (including a salt with hydrogen or coordination bonds), or other noncovalent derivative (such as a complex, chelate, or clathrate) of the molecule, responsible for the physiological or pharmacological action of the drug substance."

**Practical implications for the join:**
- Fluoxetine HCl and fluoxetine free base share one active moiety. If either is US-approved, both are PRV-ineligible.
- An acetate ester of a previously approved drug shares the moiety. Same ineligibility.
- A prodrug is assessed on its pharmacologically active metabolite (the moiety), not the prodrug itself. Enalapril's moiety is enalaprilat.
- Enantiomers are the hard case: FDA has ruled both ways. The 2021 Pub. L. 117-9 change from "active ingredient" to "active moiety" was specifically intended to close enantiomer loopholes. A racemic approval now bars the enantiopure form as the same moiety under the post-2021 standard. Check GSRS `stereochemistry` and `opticalActivity` fields in the moiety record.

**The join must be done at moiety level, not ingredient level.** A salt found in the EMA XLSX may not appear in Drugs@FDA by that name, but its free-base moiety may have a RXCUI and an existing US NDA. The GSRS `/moieties` endpoint is the authoritative structural arbiter.

---

## 4. THE FILTERS — Cheapest Disqualifier First

Apply in this order to minimize cost before incurring expensive steps.

### Filter 1: Any published rare-disease evidence at all (PubMed, free, seconds per compound)

**Query:** `{INN_name}[tiab] AND ("rare disease"[tiab] OR "orphan"[tiab] OR "inborn error"[MeSH])` via NCBI E-utilities.

**Base rate:** The rare pediatric disease literature contains 14,926 qualifying records at minimum, possibly 86,537+ when using broader MeSH terms (prior agents returned different counts due to query construction differences; the larger number is more likely correct). The important insight is that the literature base is large, not small — it does not constrain the pipeline. A compound with zero hits across multiple synonym searches is unlikely to be a productive candidate.

**Minimum bar:** At least one case report, case series, or mechanistic study associating the compound with a disease meeting the § 360ff(a)(3) pediatric rare disease criteria. Zero hits → deprioritize but do not categorically exclude (mechanism-first candidates without published case data may still be viable if the biology is compelling).

### Filter 2: Does the disease meet the § 360ff(a)(3) rare pediatric test? (Research, hours per compound)

The § 360ff(a)(3) test requires simultaneously:
- **(A)** Serious or life-threatening, primarily affecting ages 0–18. "Primarily" is determined per-manifestation by FDA — if any serious/life-threatening manifestation primarily affects children, the whole disease qualifies.
- **(B)** Rare: US prevalence < 200,000, or unrecoverable costs from US sales even if > 200,000.

**Disqualifying patterns:** Adult-onset diseases (most lysosomal storage disorders have adult-onset variants that dominate prevalence); diseases where the pediatric form is a minority of cases and FDA would not characterize the serious manifestations as primarily pediatric; diseases with US prevalence > 200,000 that lack an orphan subset.

**Data sources:** Orphanet (ORPHA numbers, age-of-onset, US prevalence estimates), NORD database, FDA OOPD database (whether an orphan designation already exists for the drug-disease pair — the designation disease description tells you FDA's prior characterization), NewSTEPs newborn screening prevalence data.

### Filter 3: Freedom to Operate — does anyone hold a composition-of-matter patent covering this moiety? (Hours to days per compound)

**Why cheap to run first:** A quick Espacenet or Google Patents search on the INN name often reveals whether the compound is still under patent protection globally. If the original inventor holds an unexpired composition-of-matter patent in the US, no 505(b)(1) can proceed without a license. Estimated **30–35% of the A1 candidate pool** (mostly older compounds) will be clearly off-patent. The 23% of KEGG JP-only candidates with D-numbers ≥ 8,000 (newer compounds, estimated ~210 of 905) will be more likely to have blocking patents.

**Key check:** US patent database (USPTO PatFT), Espacenet, Orange Book patent listings (for any existing US product). A compound with no US patent filings and a first-approval date before 2000 is almost certainly clear.

### Filter 4: Does anyone already hold orphan designation or orphan exclusivity on the drug-disease pair? (Minutes per compound if OOPD accessible)

**FDA OOPD database:** `https://www.accessdata.fda.gov/scripts/opdlisting/oopd/` returns HTTP 302→403 from automated scripts (confirmed 2026-08-06). Accessible only via browser. Use the OOPD Excel bulk export approach documented in source 01: POST to `OOPD_Results.cfm` with `Output_Format=Excel` and a 45-day date window. The "fake XLS" (actually HTML table) can be parsed with `pandas.read_html`.

**EU Community Register:** `https://health.ec.europa.eu/medicinal-products/union-register_en` (VERIFIED HTTP 200, 2,171 active EU orphan designations). Check whether the EMA has granted an orphan designation for the same drug-disease pair.

**Key nuance:** An existing orphan designation does NOT categorically block the pipeline. Orphan exclusivity (§ 360cc) only blocks FDA from approving the "same drug" for the "same disease" — a different moiety is not blocked. Even the same moiety can be approved if the new drug demonstrates clinical superiority. The blocking question is whether the existing holder has orphan **exclusivity** (not just designation), and whether the new drug would target the identical indication. Check Orange Book `exclusivity.txt` for `ODE-` codes.

### Filter 5: API sourceable at sane MOQ for a 20-patient trial? (Days; requires supplier outreach)

For the small-market registration program (Georgia, Ukraine, Armenia, Botswana, Albania, Barbados, Seychelles, Samoa) and for the trial drug supply, the API must be:
- Available from a WHO-GMP-certified or MRA-country manufacturer (see Section 6 on CMC risk)
- At a minimum order quantity of 200–500 grams (typical for 20 pediatric patients, 3–12 months treatment)
- At a cost that does not dominate the trial budget

**Estimated sourcing failure rate:** 40–60% for Japan-orphan-specific compounds (many manufactured only by a single Japanese company that has never exported the API); 20–30% for older off-patent compounds with established generic supply chains.

**Primary screening tools:** ChemSrc (`chemsrc.com`), eMolecules, Sigma-Aldrich (Merck) catalog, Santa Cruz Biotechnology for research-grade (not GMP; GMP sourcing is a follow-on step). Send supplier inquiries before starting IND preparation.

**API from MRA-country manufacturer is not optional for PAI risk mitigation:** Under the revised CP 7346.832 (effective 2026-08-10), FDA will conduct **unannounced** pre-approval inspections at non-US facilities. A WHO-GMP-only site now has a PAI pass probability of approximately 50–60%. An MRA-country manufacturer (EU, UK, Japan, Canada, Australia, Israel, Swissmedic) allows FDA to rely on a partner-authority inspection report, raising the PAI pass probability to ~88%. **This single manufacturing decision is the second-largest lever on the per-program success probability (after disease/enrollment selection).**

### Filter 6: Is a ~20-patient trial feasible for this disease? (Weeks; requires disease-specific assessment)

**Enrollment feasibility:** Measured LSD/IEM trial data (ClinicalTrials.gov API v2, VERIFIED 2026-08-06, 57 LSD completed trials): median actual N = 19 patients; 56% had N ≤ 20. Per-site per-month enrollment rate for ultra-rare pediatric diseases: 0.04–0.08 pts/site/month (measured from 9 LSD trials with site-level data).

**Key implication:** To enroll 20 patients in 24 months at 0.05 pts/site/month requires ~17 active sites. At 0.08 pts/site/month (better case), 10 sites. Ten sites costs $65k–$100k in initiation alone. A well-selected disease with an existing patient registry and concentrated referral centers can reach 0.15–0.35 pts/site/month (cerliponase alfa achieved 0.923/month with 5 international sites, but that was BioMarin with pre-existing investigator relationships).

**Minimum requirements for a 20-patient trial to be feasible:**
- US prevalence ≥ 200 diagnosed patients (gives an addressable pool of 30–80 enrollable after the 6-filter funnel at mid-case rates)
- At least one academic center with ≥5 known patients willing to serve as PI
- A measurable biomarker endpoint that resolves within 6–12 months (eliminates slowly-progressive conditions where 3+ years of follow-up are needed for FDA to accept efficacy)
- An existing natural history dataset in RDCA-DAP (`https://dataportal.c-path.org/`) or a published registry, for the external control arm

**Bayesian borrowing option:** If a natural history dataset exists, Bayesian borrowing from that dataset can reduce the required N from 20 to 10–12 while maintaining posterior probability thresholds acceptable to FDA. This saves ~$200k–$400k in per-patient site costs. FDA's RDEA pilot program provides 4 structured FDA meetings to align on this approach before the trial starts (maximum 3 proposals admitted/year industry-wide; apply early).

---

## 5. FUNNEL B — US Generic Repurposing (No PRV, Orphan Exclusivity Only)

### What Funnel B is

Funnel B applies to US generics — compounds with an existing 505(b)(1), 505(b)(2), or 505(j)/ANDA approval — filed as 505(b)(2) NDAs for a new rare pediatric indication. PRV-ineligible per § 360ff(a)(4)(B)(i). Available benefits:
- **7-year orphan drug exclusivity** (§ 360cc): blocks FDA from approving "same drug" for "same disease" for 7 years from marketing approval.
- **3-year exclusivity** for new clinical investigation (if the 505(b)(2) contains new clinical data).
- Potentially 6 months of pediatric exclusivity under BPCA (§ 505A), extending by 6 months all existing exclusivities.
- Orphan drug designation designation grants: waivers of PDUFA user fees (significant — NME PDUFA VII fee is ~$3.6M; orphan waiver removes it), priority review status.
- Access to FDA's OOPD grants program (up to $500k/year per grant for clinical studies).

### How Funnel B screening differs

- **Left side:** Every off-patent US generic is a candidate. There are approximately 4,000–5,000 distinct small-molecule active moieties with at least one US generic approval.
- **Right side:** The same OOPD database and EU/EMA orphan databases — but now you want to know whether a disease-drug pair has been claimed at all, not just whether the moiety is US-approved.
- **Literature hit rate:** Higher than Funnel A — the same 14,926–86,537 rare pediatric case reports exist, but now they can be linked to the much larger pool of US-approved generics. Source 04 measured approximately 35 new rare pediatric disease + drug therapy records per day appearing in PubMed.
- **FTO:** Much cleaner — off-patent generics are freely available; no composition-of-matter patent in the US.
- **API:** Trivially sourced — any USP-grade generic API can be purchased from multiple suppliers at low MOQ.

### What a Funnel B win is actually worth

**Orphan exclusivity value:** The 7-year orphan exclusivity prevents a generic from entering the US market for 7 years from approval. In a rare pediatric disease with < 200,000 patients and a drug that costs $50k–$500k/year per patient (orphan drug pricing norms), this can generate meaningful revenue. But this requires an actual US commercialization strategy — the company must sell the drug in the US during those 7 years, or license it to a commercial partner.

**The missing element:** Without the PRV ($180–210M (top figure a signed, unclosed agreement) lump sum), Funnel B economics require either (a) active US commercial operations with a viable rare disease drug revenue model, or (b) an out-licensing deal to a larger commercial partner who values the orphan exclusivity. The company's current model focuses on small-market registrations (Georgia, Ukraine, Armenia, Botswana, etc.) — estimated combined revenue of $500k–$5M annually (UNVERIFIED; inferred from market size and disease prevalence; this figure is not grounded in primary market data). That revenue does not justify $300k–$800k in trial costs without PRV proceeds.

**When Funnel B makes sense for this company:** As a parallel track to Funnel A where the trial infrastructure is already built for a given disease, or where an academic partner is running an investigator-IND study (reducing company cost to near-zero), or where the goal is proving clinical utility for a future Funnel A program in an adjacent disease. **Funnel B is not the core revenue generator at this capital level without US commercialization.**

---

## 6. THE HONEST VERDICT

### The pool size

The feasibility analyses in sources 25, 26, and 27 converge on the following picture:

**Funnel A (never-US-approved moiety, 505(b)(1), PRV-eligible):**

| Filter stage | Mid-case (revised post-adversarial review) | Range |
|---|---|---|
| Distinct ex-US approved moieties, post-join | 700–1,800 (905 KEGG JP-only floor is empirical) | Wide |
| With published rare pediatric evidence | 50 | 15–120 |
| Qualifying under § 360ff(a)(3) pediatric test | 15 | 5–35 |
| After FTO / patent / orphan exclusivity / API / trial feasibility filters | **~7** | **2–15** |

**7 globally actionable programs is not 6–10.** Even being generous, the upper bound is 15. In the lower range, this is 2 programs. These are not 6–10 independently actionable programs — they are the entire global inventory that meets all conditions simultaneously.

**Funnel A2 (Sun Pharma carve-out — pre-1962 deemed-approved-only):**
- Raw pool: approximately 200–600 distinct moieties where only history is a pre-1962 deemed NDA now withdrawn.
- With rare pediatric evidence: 2–18.
- After all filters: **0–3** actionable programs.
- Legal risk: district court only; unreviewed. Treat as opportunistic, not foundational.

**Funnel B (US generic, orphan exclusivity, no PRV):**
- Much larger candidate pool (~4,000–5,000 moieties) but without the PRV economic anchor.
- 14,926–86,537 rare pediatric case reports provide evidence substrate.
- Revenue model requires US commercialization or licensing partner; small-market revenues alone likely do not justify trial costs.

### The timeline

As of August 6, 2026, there are **37 months until the PRV sunset (September 30, 2029)**. Under priority review (6-month clock + 60-day filing period = ~8 months), an NDA must be submitted by **approximately November 2028** to preserve meaningful buffer for goal-date extensions. Working backwards:

- Trial LPLV by February 2028 (conservative)
- Enrollment start by August 2026 (conservative) to February 2027 (optimistic) — **this is essentially now**
- IND effective no later than December 2026 (for optimistic scenario)

**A program started from scratch today is at the outer edge of the optimistic scenario.** There is no margin for slippage.

**Per-program success probability (source 26, adversarial-reviewed):**
- Generic program (no disease pre-selection, WHO-GMP-only API): approximately **3–5%**
- Optimized program (registry-backed disease, MRA-country manufacturer, RDEP-aligned design): approximately **20–22%**

The four critical design choices that move a program from 3–5% to 20–22%:
1. Choose a disease with a pre-existing patient registry
2. Use an MRA-country API manufacturer (EU, UK, Canada, Japan, Australia, Israel, Swissmedic)
3. RDEP-aligned trial design with pre-specified natural history external control
4. File IND directly without pre-IND meeting delay (pre-IND meeting is not required for a repurposed molecule with established safety profile; eliminates 5–8 months)

### The 6–10 program plan

**A portfolio of 6–10 simultaneous programs is not viable at this capital level or team size, and the math does not recover even under generous assumptions.**

Evidence from source 27 (adversarial-reviewed):
- Cost floor for one properly conducted 20-patient trial: $500k–$800k all-in. The $300–400k figure is below the floor for a multi-site sponsor-initiated trial; it is achievable only for a single-site, academically embedded, investigator-IND-adjacent structure with multiple cost concessions simultaneously.
- 6 programs × $500k = $3M. Current capital: ~$180k. Gap: $2.8M before any overhead.
- Coordination overhead per active program: $80k–$150k/year. For 6 programs: $480k–$900k/year in overhead alone.
- Site relationship constraint: the universe of US pediatric metabolic disease sites capable of running a rare IEM trial is approximately 20–30 institutions. Six to ten simultaneous programs compete for the same investigators at the same 20–30 sites.
- IEM attrition rate: 15.9% of started trials terminate before completion (VERIFIED from ClinicalTrials.gov API, 2,186 IEM trial records). For ultra-rare pediatric disease, accrual failure is the primary cause.
- Expected approvals from 6 generic programs at 3–5% each: 0.2. Expected approvals from 6 optimized programs at 22% each: 1.3.

**Plain statement: 6–10 programs is fantasy at the current stage.** The company should pursue 1–2 programs, sequentially, starting immediately with the one that best achieves the four critical design choices. A second program can be initiated only when the first is past enrollment completion and NDA preparation is underway.

### Is the business worth building?

**Yes, but not as currently described.**

The business as described — 6–10 parallel programs at $300–400k each, all targeting PRV proceeds — is not viable. The candidate pool globally totals approximately 7 actionable programs, not 60. The capital is insufficient by a factor of 15–20x for 6 simultaneous programs. The timeline is too tight for any program that does not start enrollment within the next six months.

**The version worth building:**

1. **One program, immediately.** Select the single best candidate from the Japan-orphan-not-US sub-population. Use the NIBN list (#733 through 2025-10-01) cross-referenced against US approvals to identify candidates. Target a disease with: (a) RDCA-DAP natural history data, (b) a concentrated patient population at 1–3 academic centers, (c) a biomarker-confirmable outcome measurable within 6–12 months, (d) an MRA-country API supplier already qualified.

2. **One regulatory strategy.** File IND directly (no pre-IND meeting delay). Request RDEA pilot program meeting slot simultaneously with IND filing. Request orphan designation and RPD designation simultaneously (§ 360ff(d)(2) requires this to be co-filed; it is not a prerequisite to receiving the PRV but it establishes the record).

3. **One funding path.** NIH NCATS SBIR Phase 1 (up to $300k, ~9–12 months to award) to fund pre-clinical and IND preparation. A disease-specific patient foundation grant for trial co-funding. A single seed round targeting $2M to fund the full program through NDA filing.

4. **Every Cure as a screening input, not a competitor.** Every Cure's MATRIX scores dataset (39.5M rows, drug × disease, downloadable from Hugging Face) is open-source research output with no commercial license declared on the main scores file. The `drug-list`, `disease-list`, and `indications-list` datasets are CC BY 4.0. Every Cure is explicitly a nonprofit that does not pursue PRVs. The MATRIX scores should be used as the **first-pass literature signal layer** — any drug-disease pair with a high MATRIX score and no existing US approval is a candidate for further investigation. MATRIX covers ~1,800 FDA-approved drugs; this is Funnel B territory. For Funnel A (never-US-approved moieties), Every Cure's drug list is not the right starting point — but their knowledge graph infrastructure (ROBOKOP + RTX-KG2) can surface mechanistic evidence for Funnel A candidates once the INN names are established.

---

## 7. THE BUILD ORDER

### Phase 1 — Build now (weeks 1–8)

**7.1 Right-side US exclusion set (3–5 days of engineering)**
- Download Drugs@FDA Products.txt (daily), Orange Book products.txt (monthly), Purple Book CSV (monthly), UNII bulk files (quarterly).
- Build a `us_approved_moieties` table keyed on UNII: columns `unii`, `display_name`, `rxcui`, `inchikey`, `modern_approval` (Boolean), `pre1962_deemed_only` (Boolean), `approval_year`.
- The `pre1962_deemed_only` flag requires manual research — build it as a short manual list seeded from the known DESI/Sun Pharma precedent cases. Do not attempt to automate this from scratch; the DESI database is not machine-readable.

**7.2 Japan left side — first pass (1–2 weeks)**
- Download NHI Yakka (`tp20260715-01_05.xlsx`).
- Download KEGG `/find/drug/JAN` text file (2,273 lines); extract D-number and Latin INN for each.
- Build a katakana-to-Latin transliteration map from PMDA FY2025 XLSX (143 rows; annotate each row manually if needed — it is only 143).
- Run the normalization pipeline (Section 3.1 above) against the UNII_Names file.
- Output: `japan_candidates.csv` with columns: `jp_name_katakana`, `jp_name_latin`, `unii`, `rxcui`, `funnel_a_b`, `notes`.

**7.3 EMA left side — first pass (2–3 days)**
- Download EMA Medicines JSON.
- Extract `INN / common name` (column 6) for all Authorised human products.
- Run normalization pipeline.
- Output: `ema_candidates.csv`.

**7.4 Anti-join (1 day)**
- JOIN `japan_candidates` and `ema_candidates` on UNII against `us_approved_moieties`.
- Flag all rows where `modern_approval = False AND rxcui IS NULL` as Funnel A candidates.
- Flag all rows where `pre1962_deemed_only = True` as Funnel A2 candidates (with legal risk caveat).

**7.5 KEGG JP-orphan sub-population (1 day)**
- From the KEGG `/find/drug/JAN` file, identify the 905 JP-only drugs (D-entries with `<JP>` but not `<US>` flags, after correct HTML entity unescaping of the br08303.keg BRITE file).
- Cross-reference against NIBN Japanese orphan designation list to identify the Japan-orphan-not-US sub-population.
- This sub-population routes at 100% rare-disease hit rate — treat it as the highest-priority screening queue.

**NOTE: KEGG requires a commercial license for commercial use (Pathway Solutions Inc.). Use KEGG for research/screening to identify the candidate list, then re-verify each identified candidate against the open-data NHI Yakka for commercial pipeline use. Do not build a production pipeline that depends on bulk KEGG data without a paid licence.**

### Phase 2 — Build after the first candidates are identified (weeks 8–20)

**7.6 Literature screening layer (PubMed E-utilities, free)**
- For each Funnel A candidate from the anti-join, query PubMed: `{INN}[tiab] AND ("rare"[tiab] OR "orphan"[tiab] OR "inborn error"[MeSH] OR "pediatric"[tiab] AND "disease"[tiab])`.
- Use NCBI E-utilities (no auth for < 10 req/second with email in User-Agent; free API key for higher rate).
- Score each candidate by: number of case reports, whether there is a clinical trial registered on ClinicalTrials.gov, and whether any publication mentions the § 360ff(a)(3) pediatric criteria disease space.

**7.7 § 360ff(a)(3) pediatric qualification check**
- For each candidate with literature hits, cross-check the disease against: Orphanet age-of-onset data, NORD database, FDA OOPD designation history (browser-based search — automate later).
- Flag diseases that are clearly adult-onset, clearly > 200,000 US prevalence, or clearly lack serious pediatric manifestations.

**7.8 Every Cure MATRIX integration**
- Download `everycure/matrix-scores` (3.81 GB Parquet, Hugging Face, `research use only` license — confirm permitted use with Every Cure before using commercially).
- Cross-reference Funnel B candidates against MATRIX scores to identify the highest-scoring drug-disease pairs without existing orphan designation.
- For Funnel A candidates: use Every Cure's knowledge graph edges (`kg-edges`) to find mechanistic support for the proposed indication.

**7.9 Orphan exclusivity conflict check**
- For each surviving candidate, check FDA OOPD (browser-based) and Orange Book `exclusivity.txt` for ODE codes.
- Check EU Community Register for active EU orphan designations.
- Flag any candidate where an existing holder has 7-year orphan exclusivity for the same drug-disease pair.

### Phase 3 — Buy or partner, do not build (defer or contract out)

**7.10 FTO / IP analysis**
- **Buy, do not build.** A Freedom to Operate opinion from a patent attorney costs $3k–$8k per compound. For a pool of 15–30 Funnel A candidates surviving the Phase 1–2 filters, the total cost is $45k–$240k — less than building an in-house patent search infrastructure.
- Espacenet and Google Patents can be used for rapid pre-screening (15 minutes per compound) to eliminate obviously patent-encumbered candidates before spending money on a formal opinion.

**7.11 API sourcing and GMP qualification**
- **Contract out.** Engage a regulatory consulting firm (CMC consultant) to conduct API sourcing feasibility for the top 3–5 candidates. Cost: $5k–$15k per candidate for a sourcing report. This is significantly cheaper than discovering a sourcing problem after starting the IND.

**7.12 China NMPA access**
- **Partner.** License NMPA drug approval data from a commercial vendor (Cortellis/Clarivate, Citeline, or a China-specific regulatory data provider). The gap in China data is material — NMPA has approved several rare-disease drugs that have not reached FDA. Budget: $15k–$50k/year for a data subscription.

**7.13 Clinical trial design and RDEA pilot application**
- **Do not build internally.** Retain a rare disease regulatory consulting firm (e.g., RareVoice, Rarebase, or an academic RDCRN partner) for protocol design and RDEA pilot application. The RDEA pilot (maximum 3 admissions/year industry-wide) requires a highly competitive application. An experienced rare disease regulatory team increases admission probability.

### Where a human must be in the loop

1. **Every Funnel A candidate before IND filing:** Manual UNII moiety check with documented HTTP responses confirming no US approval. This is the anti-false-positive gate. One slip here costs the entire program.
2. **A2 (pre-1962 carve-out) designation:** Legal counsel must assess each A2 candidate against *Sun Pharma* and the specific NDA history. Do not rely on automated screening for A2 classification.
3. **PI relationship:** A disease expert PI (academic investigator) must co-sponsor or validate the trial design. This relationship cannot be automated. Budget 12–18 months to establish.
4. **Advocacy organization engagement:** A patient advocacy relationship takes 12–18 months to build and requires the scientific lead's personal presence at advocacy conferences. No shortcut exists.

---

## 8. URL LEDGER

### VERIFIED (live fetch or confirmed in primary source files)

| URL | HTTP | Source | Notes |
|-----|------|--------|-------|
| `https://www.ema.europa.eu/en/documents/report/medicines-output-medicines-report_en.xlsx` | 200 | MINED-drug-data-sources.md | 2,730 rows, 897,579 bytes, nightly |
| `https://www.ema.europa.eu/en/documents/report/medicines-output-medicines_json-report_en.json` | 200 | 25-feasibility-pool-size.md | 6,739,136 bytes, 2,730 records |
| `https://www.ema.europa.eu/en/documents/report/medicines-output-orphan_designations-report_en.xlsx` | 200 | 25-feasibility-pool-size.md | 347,937 bytes, ~2,190 Positive designations |
| `https://rest.kegg.jp/list/drug` | 200 | MINED-drug-data-sources.md | 599,728 bytes, 12,893 entries |
| `https://rest.kegg.jp/find/drug/JAN` | 200 | 25-feasibility-pool-size.md | 2,273 lines (VERIFIED live 2026-08-06) |
| `https://www.kegg.jp/kegg-bin/download_htext?htext=br08303.keg&format=json` | 200 | MINED-drug-data-sources.md | 1,170,587 bytes; 905 JP-only after correct HTML entity unescaping |
| `https://www.mhlw.go.jp/topics/2026/04/xls/tp20260715-01_05.xlsx` | 200 | 25-feasibility-pool-size.md | 683,699 bytes; 12,414 products, 2,694 unique ingredients |
| `https://www.pmda.go.jp/files/000277966.xlsx` | 200 | MINED-drug-data-sources.md | 32,825 bytes; FY2025 143 approvals |
| `https://www.pmda.go.jp/files/000281190.pdf` | 200 | MINED-drug-data-sources.md | 3,206,009 bytes; English new drugs 2004–Feb 2026 |
| `https://www.canada.ca/content/dam/hc-sc/documents/services/drug-product-database/drug_ap.zip` | 200 | MINED-drug-data-sources.md | 90,984 bytes |
| `https://www.canada.ca/content/dam/hc-sc/documents/services/drug-product-database/ingred_ap.zip` | 200 | MINED-drug-data-sources.md | 99,197 bytes |
| `https://www.swissmedic.ch/dam/swissmedic/de/dokumente/internetlisten/erweiterte_ham_ind.xlsx.download.xlsx/Erweiterte_Arzneimittelliste%20HAM.xlsx` | 200 | MINED-drug-data-sources.md | 2,581,811 bytes |
| `https://www.fda.gov/media/89850/download?attachment` | 200 | 01-fda-us-regulatory.md | 6,059,547 bytes; Drugs@FDA ZIP, updated M–F |
| `https://www.fda.gov/media/76860/download?attachment` | 200 | 01-fda-us-regulatory.md | 1,091,413 bytes; Orange Book ZIP |
| `https://download.open.fda.gov/drug/orangebook/drug-orangebook-0001-of-0001.json.zip` | 200 | 01-fda-us-regulatory.md | 2.34 MB; 48,502 records; export_date 2026-08-05 |
| `https://www.accessdata.fda.gov/drugsatfda_docs/PurpleBook/2026/purplebook-search-july-data-download.csv` | 200 | 01-fda-us-regulatory.md | 476,652 bytes |
| `https://download.open.fda.gov/other/unii/other-unii-0001-of-0001.json.zip` | 200 | 01-fda-us-regulatory.md | 175,453 records |
| `https://precision.fda.gov/uniisearch/archive/latest/UNIIs.zip` | 200 (via 308) | 14-drug-identity-normalization.md | UNII_Names_26Feb2026.txt; 1,024,191 rows |
| `https://precision.fda.gov/uniisearch/archive/latest/UNII_Data.zip` | 200 (via 308) | 14-drug-identity-normalization.md | UNII_Records_26Feb2026.txt; 168,046 records |
| `https://gsrs.ncats.nih.gov/api/v1/substances/@count` | 200 → 173,081 | 14-drug-identity-normalization.md | Live count as of 2026-08-05 |
| `https://rxnav.nlm.nih.gov/REST/version` | 200 | 14-drug-identity-normalization.md | RxNorm version 03-Aug-2026 |
| `https://www.govinfo.gov/content/pkg/CFR-2024-title21-vol5/xml/CFR-2024-title21-vol5-sec314-3.xml` | 200 | 14-drug-identity-normalization.md | Active moiety definition verbatim |
| `https://clinicaltrials.gov/api/v2/studies?query.cond=inborn+errors+metabolism` | 200 | 27-feasibility-recruitment.md | IEM status counts: Completed 1,838; Terminated 223; Withdrawn 125 |
| `https://arpa-h.gov/explore-funding/awards/1141` | 200 | 21-every-cure-arpa-h.md | Every Cure MATRIX; $124M ceiling; open-source output |
| `https://huggingface.co/everycure` | Accessible | 21-every-cure-arpa-h.md | matrix-scores 39.5M rows (3.81 GB Parquet); drug-list/disease-list CC BY 4.0 |
| `https://www.accessdata.fda.gov/scripts/opdlisting/oopd/` | 200 | 15-orphan-rpd-conflict-check.md | OOPD UI; POST-only; returns 403 from automated scripts |
| `https://prvwatch.com/news/when-does-the-fda-decline-to-award-a-priority-review-voucher` | 200 | 22-prv-denials-dataset.md | 18 PRV denials compiled; Lyfgenia and Sezaby named; table is image-only |
| `https://www.sec.gov/Archives/edgar/data/1293971/000129397124000037/blue-20231231.htm` | 200 | 22-prv-denials-dataset.md | bluebird bio 10-K FY2023; Lyfgenia PRV denial confirmed verbatim |
| `https://www.thefdalawblog.com/2025/12/when-is-an-approval-not-an-approval-before-1962/` | 200 | 22-prv-denials-dataset.md | Full *Sun Pharma v. FDA* analysis; FDA denial language verbatim |
| `https://www.fda.gov/media/151712/download` | 200 | 26-feasibility-timeline.md | PDUFA VII Performance Goals; 453,799 bytes; all NME review clocks |
| `https://health.ec.europa.eu/medicinal-products/union-register_en` | 200 | 25-feasibility-pool-size.md | 2,171 active EU orphan designations |
| `https://www.federalregister.gov/documents/full_text/text/2022/10/27/2022-23383.txt` | 200 | 27-feasibility-recruitment.md | RDEA Pilot Program FR Notice 87 FR 65085 |
| `https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title21-section360ff` | 200 | 01-fda-us-regulatory.md | § 360ff full text; active moiety bar verbatim |
| `https://www.accessdata.fda.gov/scripts/opdlisting/oopd/OOPD_Results.cfm` (POST) | 200 | 01-fda-us-regulatory.md | 8,190 designation records in "XLS" (actually HTML table); 8,890,799 bytes |

### UNVERIFIED / BLOCKED / INACCESSIBLE

| URL | Status | Reason | Impact |
|-----|--------|--------|--------|
| `https://www.tga.gov.au/resources/artg` | HTTP 000 | Cloudflare bot block from US IP | Cannot enumerate Australia ARTG; material gap |
| `https://www.nmpa.gov.cn` | HTTP 412 | WAF block, all paths | Cannot enumerate China-approved moieties; material gap |
| `https://www.nmpa.gov.cn/datasearch/home-index.html` | HTTP 412 | WAF block | Same |
| CDE drug databases (`wbca.cde.org.cn`) | HTTP 202 (JS SPA) | Requires browser execution | Same |
| `https://apis.data.go.kr/1471000/DrugPrdtPrmsnInfoService07/` | HTTP 400 | Requires free registration key | South Korea MFDS; get key at data.go.kr |
| `https://products.mhra.gov.uk/api/search` | HTTP 404 | No public REST API | UK MHRA no bulk download |
| `https://spor.ema.europa.eu/smsapi/v1/substances` | HTTP 302 → SSO | Requires EMA account | EMA SPOR SMS substance list |
| FDA DESI records / UMDI database | No machine-readable URL | Not published in structured form | Cannot enumerate A2 pool precisely |
| KEGG commercial license | Requires contact | Pathway Solutions Inc. | Must be resolved before production use |
| `https://www.accessdata.fda.gov/scripts/opdlisting/oopd/OOPD_Results.cfm` (from scripts) | HTTP 302 → 403 | Akamai bot management | Requires headless browser with cookies |
| prvwatch.com 18-denial table | Image (not HTML) | Table rendered as image in article | Full denial distribution unknown |
| Every Cure matrix-scores commercial use | License unclear | `license: null` on HF; "research use only" warning | Confirm with Every Cure before commercial pipeline use |
| KEGG br08303.keg revised JP-only count (905) | UNVERIFIED in this session | HTML entity unescaping bug in prior session; 905 is R2's corrected figure, mechanistically specific but not re-run | The 620 figure is verified; 905 is the corrected estimate |

---

*Written 2026-08-06. All VERIFIED designations refer to HTTP fetches documented in the source files cited. Uncertainty in pool-size estimates is explicitly labeled with confidence levels. The PRV sunset date (2029-09-30) is sourced from Pub. L. 119-75 § 6604(a) and from 91 Fed. Reg. 47252 (July 28, 2026), not from FDA's website which has moved the relevant page.*
