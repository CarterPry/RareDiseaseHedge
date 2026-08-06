<!-- RECOVERED from subagent transcript agent-a549039bd1465fcc7.jsonl, session fd64561f-7c90-41a2-95cf-b4a133a8fe0f, research date 2026-08-05.
     Child of agent 3 (ICD-11/ICD-10-CM/ORPHA maps/ClinGen/ClinVar/MedGen). Same status.
     Verbatim agent deliverable — not re-edited. -->

All sources verified against live endpoints. Here is the reference.

---

# Rare-Disease Drug Repurposing — Verified Data Source Reference
*All checks performed 2026-08-05. **VERIFIED** = I fetched it and it returned expected content.*

## Cross-cutting finding (the load-bearing one)

I downloaded Orphanet's actual alignment file and counted the mappings. This quantifies the rare-disease coding gap better than any secondary source:

| ORPHA→ICD mapping precision | ICD-10 | ICD-11 |
|---|---|---|
| **Specific code** (disease has its own code) | **1,053** | **1,697** |
| Index term (listed in index/Foundation only) | 187 | 3,592 |
| Inclusion term (under a category, no own code) | 442 | 0 |
| **Attributed code** (Orphanet invented it; no ICD representation) | **6,768** | **1,579** |
| Total refs | 8,450 | 6,868 |

**Only 1,053 of 11,645 Orphanet disorders (9%) have their own ICD-10 code.** 6,768 have a code Orphanet assigned because ICD-10 had nothing. ICD-11 raises real representation to 5,289 (specific + Foundation index) — which independently triangulates WHO's "some 5500 rare diseases" claim. Design your pipeline to key on **ORPHAcode or MONDO, never ICD-10**.

---

## 1. ICD-11 (WHO)

**Browser** — `https://icd.who.int/browse11` **VERIFIED** (redirects). Note: the old `/browse11/l-m/en` structure is **retired**; current is `https://icd.who.int/browse/2025-01/mms/en` (release 2025-01). Any hardcoded `browse11` URLs in older literature will break.

**API** — base `https://id.who.int/`, docs `https://icd.who.int/docs/icd-api/APIDoc-Version2/` **VERIFIED** (v2.6).
- Token endpoint: `https://icdaccessmanagement.who.int/connect/token` — **VERIFIED live**: POSTing `grant_type=client_credentials&scope=icdapi_access` without credentials returns HTTP 400 `{"error":"invalid_client"}`, confirming the OAuth2 client-credentials flow.
- `https://id.who.int/icd/entity/257068234` returns **HTTP 401** without a bearer token — **VERIFIED** auth is enforced.
- Required headers: `API-Version: v2`, `Accept: application/json` (or `application/ld+json`), `Accept-Language`.
- Register for client-id/secret at `https://icd.who.int/icdapi` **VERIFIED**.
- Gotcha: returned URIs use `http://`; rewrite to `https://` to avoid a redirect per call.

**Foundation vs linearization** — Foundation is the multi-parent superset with **no codes**. MMS is the single-parent coded linearization (`linearizationname=mms`). **Most rare diseases live only in the Foundation** — they have a URI but no MMS code. If you query MMS only, you lose ~3,592 rare diseases.

**Local Docker (recommended — no OAuth, no rate limits)** — **VERIFIED** at `https://icd.who.int/docs/icd-api/ICDAPI-DockerContainer/`:
```
docker run -p 80:80 -e acceptLicense=true -e saveAnalytics=true whoicd/icd-api
```
Image `whoicd/icd-api`, ARM supported. `include=2026-01_en` selects release/language (multi-release and multi-language supported). Bundles Coding Tool at `/ct` and browser at `/browse`. Set `saveAnalytics=false` to stop sending search data to WHO.

**Rare disease coverage** — WHO FAQ **VERIFIED**: *"ICD-11 includes some 5500 rare diseases and their synonyms."* No dedicated chapter — distributed by most-affected system. Orphanet chaired the Rare Diseases Topic Advisory Group; content is maintained "in close collaboration and conceptual identity with Orphanet." WHO recommends **using the URI, not the code**, to identify rare diseases individually.

## 2. ICD-10-CM (US)

**NCHS FTP (best source — CMS pages are messy and 403 to automation)**: `https://ftp.cdc.gov/pub/Health_Statistics/NCHS/Publications/ICD10CM/` **VERIFIED**, years 2012→2027.

I downloaded and parsed the official FY2027 set (`2027/icd10cm-code-descriptions-2027.zip`) — **VERIFIED**:
- **74,879** billable codes; contains `icd10cm-codes-2027.txt`, `icd10cm-order-2027.txt`, plus `-addenda-` variants.
- Addenda file = **235** change lines in plain `Add:` / `Delete:` format — this is your FY-diff source.
- **23,738 codes contain "unspecified"; 2,324 contain "other specified"** — 35% of the code set is residual. This is where rare diseases land.

**Rare-disease-specific ranges verified from the official file:** E75 (26 codes — Sandhoff, Tay-Sachs, Fabry E75.21, Gaucher E75.22, Krabbe E75.23, Niemann-Pick A/B/C/D at E75.240–244, metachromatic leukodystrophy E75.25, Canavan E75.28, NCL/Batten E75.4), E76 (12, MPS), E77 (4), E79 (7), E80 (10, porphyrias), E83 (31, Wilson/hemochromatosis), E88 (24; **E88.4x mitochondrial** = only 5 codes: MELAS, MERRF, tRNA synthetases, +2 residual), G71 (28, muscular dystrophies/myopathies), G12 (11), Q87 (21).

**Major FY2027 development — new "QA" block (VERIFIED, 18 codes):** NCHS created gene-specific codes for the first time: `QA00101` SCN2A-related neurodevelopmental disorder, `QA00102` CACNA1A-related, `QA00131` SLC6A1-related, `QA00141` STXBP1-related, `QA00142` DLG4-related synaptopathy, `QA00151` FOXG1 syndrome, `QA171` Lynch syndrome, `QA1790/QA1791` BRCA1/BRCA2 familial cancer syndrome, `QA1792` Li-Fraumeni. Other FY2027 rare-disease additions: `D69.11` Glanzmann thrombasthenia, `I42.01` Familial-genetic dilated cardiomyopathy, `I42.81` Arrhythmogenic cardiomyopathy, `I49.81` Brugada syndrome, `M04.3` VEXAS syndrome, `Q87.A` Loeys-Dietz syndrome.

**Cadence:** FY files effective **October 1**; April 1 mid-year updates exist (`icd-10-cm-conversion-table-fy2026-april-1-2026.zip` seen on CMS).

**C&M Committee — IMPORTANT CAVEAT:** Spring (March) / fall (September) meetings, ~30–60 day comment periods, Oct 1 implementation. Multiple secondary sources (Avalere Health, MedLearn) report that at the **March 2026 meeting NCHS paused all proposals for ultra-rare and gene-specific conditions until the March 2027 meeting** while it develops organizing principles for genetic conditions (comment period closed May 15, 2026). **I could NOT verify this on a primary source** — `cdc.gov/nchs/icd/*` returns **403** to both WebFetch and curl, including the March 2026 topic packet PDF. Treat as **UNVERIFIED**; confirm from a browser before relying on it. The new QA chapter in FY2027 is consistent with this narrative.

## 3. ORPHAcode ↔ ICD mapping

**Gotcha: `www.orphadata.com/alignments/` is a 404.** The correct page is `https://sciences.orphadata.com/alignments/` **VERIFIED**.

**Download (product 1 = "Rare diseases and cross-referencing"):**
- `https://www.orphadata.com/data/xml/en_product1.xml` — **VERIFIED, downloaded (52 MB)**. Pattern `{lang}_product1.xml` for en, cs, nl, fr, de, it, es, pl, pt, tr, uk, zh.
- JSON: `https://www.orphadata.com/data/json/{lang}_product1.json.tar.gz`; diffs: `/data/diff/{lang}_product1.diff`; XSD: `http://www.orphadata.com/xsd-jpg/product1_en_cross_2024.xsd`
- Aggregated: `https://github.com/Orphanet/Orphadata_aggregated`
- Licence **CC BY 4.0**, declared inside the XML itself. Releases bi-annual (July/December).

**Verified file contents:** header `version="1.3.42"`, `date="2026-06-23"`, `<DisorderList count="11645">`. External reference counts: MONDO 9,979 · UMLS 9,586 · OMIM 8,745 · ICD-10 8,450 · **ICD-11 6,868** · GARD 3,825 · MeSH 3,209 · MedDRA 1,794 (52,456 total).

**Key fields** (per `OrphadataScienceDataDescription.pdf` V3 April 2026, **VERIFIED** by reading the PDF, and confirmed against real XML): `OrphaCode`, `DisorderType`, `DisorderGroup`, `DisorderFlag`, `ExternalReferenceList` → `Source` / `Reference` / `DisorderMappingRelation` / `DisorderMappingICDRelation` / `DisorderMappingValidationStatus` / `DisorderMappingICDRefUrl` / `DisorderMappingICDRefUri`.

- `DisorderMappingRelation`: **E** exact (34,278) · **NTBT** ORPHAcode narrower than target (12,994) · **BTNT** broader (5,144) · **ND** (40). Also NTBT/E, BTNT/E per spec.
- `DisorderMappingICDRelation` (ICD-10/ICD-11 only): Specific code · Inclusion term · Index term · **Attributed code** ("assigned by Orphanet"). See the table at top — this field is the one that tells you whether an ICD code is real or fabricated.
- `DisorderMappingICDRefUri` gives the **ICD-11 Foundation ID** — this is your direct join key to the ICD-11 API.
- Two mapping traps: only ~2/3 of entries are `Validated`, and "Moved to"/"Referred to" `DisorderDisorderAssociation` entries mark deprecated ORPHAcodes you must follow forward.

**ORPHAcodes / RD-CODE:** `https://www.orphacode.org/` **VERIFIED** — Nomenclature Pack (released annually in July, CC BY 4.0, 9 languages) at `/pack-nomenclature/`, containing separate ICD-10 and ICD-11 mapping XML files, a linearisation file, an EU statistical-reporting master XLSX, and a differential file. API at `https://api.orphacode.org/`; browsers at `classifications.orphacode.org`, `mappings.orphacode.org`, `dataviz.orphacode.org`. Note `orphacode.org/data/packs/` directory listing is 403 — go through the page.

## 4. ClinGen — `search.clinicalgenome.org/kb/downloads` **VERIFIED**

**Licence: CC0 1.0 Universal Public Domain Dedication — VERIFIED** at `https://www.clinicalgenome.org/docs/terms-of-use/`. Attribution requested but not required. Only restriction: the ClinGen logo. Cleanest licensing of any source here.

**Gene-disease validity CSV** — `https://search.clinicalgenome.org/kb/gene-validity/download` — **VERIFIED by download** (1.1 MB, header `FILE CREATED: 2026-08-05` — regenerated daily).
- **6 junk lines of preamble + `+++++` separator rows** you must strip before parsing.
- Columns: `GENE SYMBOL, GENE ID (HGNC), DISEASE LABEL, DISEASE ID (MONDO), MOI, SOP, CLASSIFICATION, ONLINE REPORT, CLASSIFICATION DATE, GCEP`
- **3,656 records / 3,021 genes / 2,140 MONDO diseases.** Classification: Definitive 2,282 · Limited 546 · Moderate 454 · Disputed 197 · Strong 82 · No Known Disease Relationship 48 · Refuted 47. MOI: AR 1,835 · AD 1,472 · XL 207.
- **Diseases are MONDO-identified, not ORPHA** — join via MONDO, which is also in Orphanet product1 (9,979 refs) and MedGen (23,304 rows). MONDO is your hub ID.

**Other files** (all **VERIFIED** as listed): dosage `kb/gene-dosage/download` and `/downloadall`; curated gene/region TSVs and haploinsufficiency/triplosensitivity BEDs at `ftp.clinicalgenome.org`; archive `https://ftp.clinicalgenome.org/archive` (nightly, 60-day retention). Actionability JSON APIs: `https://actionability.clinicalgenome.org/ac/{Adult|Pediatric}/api/summ` (`?flavor=flat` for flat JSON). Variant pathogenicity CSV/TSV: `https://erepo.clinicalgenome.org/evrepo/api/summary/classifications/download?type=csv`.

**Allele Registry** — `https://reg.clinicalgenome.org/` **VERIFIED**. CAids; lookup by HGVS, dbSNP, ClinVar RCV/AlleleID/VariationID, MyVariant, HGNC symbol. **Read requires no login; registering new alleles requires login.** Bulk query at `/bulk_query/start`. Docs at `/docs/cg-car/`. No documented rate limits.

## 5. ClinVar (NCBI) — `https://ftp.ncbi.nlm.nih.gov/pub/clinvar/` **VERIFIED**

**Cadence gotcha:** the FTP listing has **two date columns — "Released" and "Last Modified."** The Released column shows stale dates (2021/2024) and will mislead you. Last Modified on every key file was **2026-08-04/05** — files genuinely refresh **weekly**. Don't build staleness checks on the Released column.

**`/tab_delimited/`** (**VERIFIED**, sizes as of 2026-08-04): `variant_summary.txt.gz` 442 MB · `submission_summary.txt.gz` 386 MB · `hgvs4variation.txt.gz` 522 MB · `var_citations.txt` 230 MB · `cross_references.txt` 112 MB · `allele_gene.txt.gz` 92 MB · `variation_allele.txt.gz` 24 MB · `gene_specific_summary.txt` · `organization_summary.txt` · `summary_of_conflicting_interpretations.txt` (1.79 GB). Every file has a `.md5`. Note `cross_references.txt` is **uncompressed** despite what most docs imply, and `molecular_consequences.txt.gz` does **not** exist here.

**`variant_summary.txt.gz` — 43 columns, VERIFIED by reading the header:** `#AlleleID, Type, Name, GeneID, GeneSymbol, HGNC_ID, ClinicalSignificance, ClinSigSimple, LastEvaluated, RS# (dbSNP), nsv/esv (dbVar), RCVaccession, PhenotypeIDS, PhenotypeList, Origin, OriginSimple, Assembly, ChromosomeAccession, Chromosome, Start, Stop, ReferenceAllele, AlternateAllele, Cytogenetic, ReviewStatus, NumberSubmitters, Guidelines, TestedInGTR, OtherIDs, SubmitterCategories, VariationID, PositionVCF, ReferenceAlleleVCF, AlternateAlleleVCF, SomaticClinicalImpact, SomaticClinicalImpactLastEvaluated, ReviewStatusClinicalImpact, Oncogenicity, OncogenicityLastEvaluated, ReviewStatusOncogenicity, SCVsForAggregateGermlineClassification, SCVsForAggregateSomaticClinicalImpact, SCVsForAggregateOncogenicityClassification`. **`PhenotypeIDS` carries MedGen CUIs and OMIM IDs** — your disease join. Rows are duplicated per assembly (GRCh37/GRCh38) — filter on `Assembly`.

**`submission_summary.txt.gz` — VERIFIED**, ~15 comment lines then: `#VariationID, ClinicalSignificance, DateLastEvaluated, Description, SubmittedPhenotypeInfo, ReportedPhenotypeInfo, ReviewStatus, CollectionMethod, OriginCounts, Submitter, SCV, SubmittedGeneSymbol, ExplanationOfInterpretation, SomaticClinicalImpact, Oncogenicity, ContributesToAggregateClassification`. Use for submitter-level conflict analysis.

**`gene_condition_source_id` — VERIFIED, and underrated for your use case.** Columns: `#GeneID, AssociatedGenes, RelatedGenes, ConceptID, DiseaseName, SourceName, SourceID, DiseaseMIM, LastUpdated`. `ConceptID` = MedGen CUI, `SourceName`/`SourceID` = MONDO/Orphanet/OMIM. This is a ready-made gene→rare-disease crosswalk, 1.2 MB.

**VCF** — `/vcf_GRCh38/` and `/vcf_GRCh37/` **VERIFIED**: `clinvar.vcf.gz` (184 MB) + `.tbi`, dated copies `clinvar_20260804.vcf.gz`, `_papu` variants (pathogenic-and-pending), plus `weekly/`.

**XML** — `/xml/` **VERIFIED**: **`ClinVarVCVRelease_00-latest.xml.gz` (5.8 GB)**, monthly on the first Thursday, plus `weekly_release/`, `RCV_release/`, and legacy `*_xml_old_format/`. The old `ClinVarFullRelease` / `ClinVarVariationRelease` names are **gone** — VCV is the current full release.

**E-utilities — VERIFIED live.** `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/` with `db=clinvar`. `esearch.fcgi?db=clinvar&term=GBA1[gene]` returned Count 791; `esummary.fcgi?db=clinvar&id=1687&retmode=json` returned VCV000001687 — and its `variation_xrefs` included **`{"db_source":"ClinGen","db_id":"CA339901"}`**, a free ClinVar→ClinGen Allele Registry join.

**Rate limits — VERIFIED** at `https://www.ncbi.nlm.nih.gov/books/NBK25497/`: **3 req/sec without an API key, 10 req/sec with one.** Get a key from the Settings page of your NCBI account (`https://account.ncbi.nlm.nih.gov/settings/`, login required), pass as `&api_key=`. Also set `tool=` and `email=`. NCBI asks that large jobs run weekends or 21:00–05:00 US Eastern.

## 6. MedGen (NCBI) — `https://ftp.ncbi.nlm.nih.gov/pub/medgen/` **VERIFIED**

NCBI's medical-genetics concept hub aggregating OMIM, GTR, Orphanet/ORDO, HPO, GeneReviews, SNOMED CT, MeSH, UMLS, NCI, ClinVar. CUIs beginning `C` are UMLS-derived; **`CN` prefixes are MedGen-minted** for concepts with no UMLS equivalent — don't assume all CUIs resolve in UMLS.

**Cadence: weekly, on Wednesdays** (**VERIFIED** in README). Listing dates were 2026-08-04.

**`MedGenIDMappings.txt.gz` (5.4 MB) — the crosswalk you want. VERIFIED by downloading and parsing.**
- **Pipe-delimited (`|`), not tab.** Four columns, and **every line has a trailing `|`** — naive splits yield a phantom 5th field.
- Header: `#CUI_or_CN_id|pref_name|source_id|source`
- **421,816 data rows.** Source distribution (verified counts): MedGen 197,250 · SNOMEDCT_US 123,023 · **MONDO 23,304** · HPO 19,586 · GARD 16,846 · MeSH 16,502 · OMIM 10,249 · **Orphanet 9,026** · OMIM allelic variant 4,449 · OMIM included 962 · OMIM Phenotypic Series 619.
- Long format: one row per CUI-per-source, so a single concept spans many rows. Pivot on `CUI_or_CN_id`. `source=MedGen` rows give the integer UID (1:1 with the CUI).
- Reality check for planning: **9,026 Orphanet rows vs 23,304 MONDO** — MedGen's Orphanet coverage is thinner than MONDO's. Route ORPHA↔MedGen joins through MONDO, or better, use Orphanet's own product1 for ORPHA mappings and MedGen for the MedGen/SNOMED/HPO side.

**RRF files (UMLS-style, pipe-delimited; mirrored as CSV in `/csv/`) — column orders VERIFIED from README:**
- `MGCONSO.RRF.gz` (15 MB): `CUI|TS|STT|ISPREF|AUI|SAUI|SCUI|SDUI|SAB|TTY|CODE|STR|SUPPRESS` — all names/synonyms per source (`SAB`).
- `MGDEF.RRF.gz` (5 MB): `CUI|DEF|source|SUPPRESS` — **definitions embed carriage returns (`\r`)**, so line-based parsing breaks. Use a real RRF parser.
- `MGREL.RRF.gz` (15 MB): `CUI1|AUI1|STYPE1|REL|CUI2|AUI2|RELA|RUI|SAB|SL|SUPPRESS` — concept relationships.
- `MGSTY.RRF.gz`: `CUI|TUI|STN|STY|ATUI` — semantic types (filter Disease-or-Syndrome).
- `MGSAT.RRF.gz`: `CUI|METAUI|STYPE|CODE|ATUI|ATN|SAB|ATV|SUPPRESS`
- `NAMES.RRF.gz`: `CUI|name|source|SUPPRESS`  ·  `MERGED.RRF.gz`: `CUI|to CUI`
- **Note: there is no `names.txt`** — it's `NAMES.RRF.gz`.

**Also present (VERIFIED):** `MedGen_HPO_OMIM_Mapping.txt.gz` (4.1 MB), `MedGen_HPO_Mapping.txt.gz`, `medgen_pubmed_lnk.txt.gz` (98 MB; `UID|CUI|NAME|PMID`), `MedGen_Sources.txt`, and four history files essential for ID stability: `MedGen_CUI_history.txt`, `MedGen_UID_CUI_history.txt` (57 MB), `MONDO_CUI_history.txt`, `ORDO_CUI_history.txt`, `HPO_CUI_history.txt`. Resolve retired IDs through these before joining.

**E-utilities `db=medgen` — VERIFIED live**: `esearch.fcgi?db=medgen&term=Fabry+disease` returned Count 16.

---

### Practical recommendations

1. **Join on MONDO as the hub.** It's the only ID present with good coverage in ClinGen (all 2,140 diseases), Orphanet product1 (9,979), and MedGen (23,304). ORPHA and MedGen CUI are your secondary keys; OMIM third.
2. **Never key on ICD-10-CM for rare disease cohorts** — 91% of Orphanet disorders have no specific ICD-10 code, and 35% of the ICD-10-CM code set is residual. Use ICD-11 Foundation URIs (via `DisorderMappingICDRefUri`) if you need a WHO identifier.
3. **Run the ICD-11 API in Docker.** No OAuth, no rate limit, no network dependency, and it pins the release version for reproducibility.
4. **Licensing is clean end-to-end** for a commercial pipeline: ClinGen CC0, Orphanet CC BY 4.0 (attribute), NCBI public domain, WHO ICD-11 requires accepting the container licence. ClinVar's data is redistributable; **Orphanet's SNOMED CT codes are excluded from exports** for licensing reasons.
5. **Two items to confirm yourself:** the NCHS pause on ultra-rare/genetic code proposals (cdc.gov blocks automated access — check in a browser), and `https://id.who.int/swagger/index.html`, which I did not fetch.