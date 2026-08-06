<!-- RECOVERED from subagent transcript agent-ad0737720557a6a24.jsonl, session fd64561f-7c90-41a2-95cf-b4a133a8fe0f, research date 2026-08-05.
     PubChem, ChEMBL, Open Targets, DrugCentral, repoDB, Broad Drug Repurposing Hub.
     Verbatim agent deliverable — not re-edited. -->

All eight verified. Report below.

---

# Cheminformatics / Drug-Repurposing Source Verification
Verified 2026-08-05 by live HTTP/psql calls. Three sources have **breaking changes** vs. the assumptions in the brief.

---

## 1. PubChem PUG-REST — **VERIFIED**

**Base:** `https://pubchem.ncbi.nlm.nih.gov/rest/pug/`

**Grammar** (from `https://pubchem.ncbi.nlm.nih.gov/pcfe/docs/markdown/pug-rest.md`):
```
/rest/pug/<input>/<operation>/[<output>][?<options>]
<input> = <domain>/<namespace>/<identifiers>
<domain> = substance | compound | assay | gene | protein | pathway | taxonomy | cell
compound <namespace> = cid | name | smiles | inchi | sdf | inchikey | formula
                     | <structure search> | <xref> | <mass> | listkey | <fast search> | identifier
<xref> = xref/{RegistryID|RN|PubMedID|MMDBID|ProteinGI|NucleotideGI|TaxonomyID|MIMID|GeneID|ProbeID|PatentID}
substance <namespace> = sid | sourceid/<source id> | sourceall/<source name> | name | <xref> | listkey
compound <operation> = record | property/<tags> | synonyms | sids | cids | aids
                     | assaysummary | classification | xrefs/<tags> | description | conformers
<output> = XML | ASNT | ASNB | JSON | JSONP | SDF | CSV | PNG | TXT
```
Gotcha: source names containing `/` → replace with `.` in URL; `&` → `%26`.

**Working examples (actual responses):**

| URL | Response |
|---|---|
| `/compound/name/aspirin/cids/JSON` | `{"IdentifierList":{"CID":[2244]}}` |
| `/compound/name/sirolimus/property/MolecularFormula,MolecularWeight,ConnectivitySMILES,InChIKey/JSON` | CID 5284616, `C51H79NO13`, MW 914.2, InChIKey `QFJCIRLUMZQUOT-HPLJOQBZSA-N` |
| `/compound/cid/5284616/synonyms/JSON` | `rapamycin, Sirolimus, 53123-88-9, Rapamune, AY-22989, FYARRO, HYFTOR, W36ZG6FT64, L04AA10, CHEBI:9168…` |
| `/compound/inchikey/QTBSBXVTEAMEQO-UHFFFAOYSA-N/cids/TXT` | `176 / 21980959 / 160748163` |
| `/compound/cid/2244,5284616,5090/property/InChIKey,MolecularWeight/CSV` | CSV table, 3 rows |
| `/compound/xref/RegistryID/W36ZG6FT64/cids/JSON` | `{"CID":[5284616]}` ← **UNII resolves directly** |
| `/substance/sourceid/FDA%20Global%20Substance%20Registration%20System%20%28GSRS%29/W36ZG6FT64/cids/JSON` | `{"SID":175268272,"CID":[5284616]}` |

**Rate limits — read carefully.** The *only* limit currently published is:
> "not make more than **5 requests per second**… We cannot offer API keys or whitelists to exceed these limits."

The classic **400 req/min and 300 s/min running-time limits are NOT in the current docs** — I searched `pug-rest.md`, `programmatic-access.md`, `pug-rest-tutorial.md`, `dynamic-request-throttling.md` and got zero matches. Treat those numbers as **UNVERIFIED / no longer published**. PUG-REST requests time out at **30 s** (server default). Excess → **HTTP 503** (may return HTML, not JSON), then IP blocking with growing duration.

**Throttling header (live, confirmed):**
```
x-throttling-control: Request Count status: Green (0%), Request Time status: Green (0%), Service status: Green (17%)
```
Count/Time: Green <50%, Yellow 50–75%, Red >75%, Black = blocked. Service: Idle/Moderate/Busy/Overloaded. Load-balanced across instances — **moderate to the worst-case reading you see**, not the average.

**PUG-View — VERIFIED.** `https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/5284616/JSON` → 568 KB, `RecordType: CID`, 19 top sections. **UNII and ATC both present:**
- `Names and Identifiers > Other Identifiers > UNII` → `W36ZG6FT64`
- `Pharmacology and Biochemistry > ATC Code` → `L04AA10` (+ hyperlinked level breakdown)
- `Classification > WHO ATC Classification System` and `> ATCvet Classification`

ATC links in PUG-View point to `https://atcddd.fhi.no/atc_ddd_index/` (the new WHOCC domain — see §8).

---

## 2. ChEMBL — **VERIFIED**

**Release:** `ChEMBL_37`, released **2026-05-01** (`/api/data/status.json`): 24,527,044 activities · 2,921,148 distinct compounds · 18,552 targets · 101,100 publications.

**FTP:** `https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/latest/` — actual listing:

| File | Size |
|---|---|
| `chembl_37_sqlite.tar.gz` | **5.4 G** |
| `chembl_37_mysql.tar.gz` | 2.0 G |
| `chembl_37_postgresql.tar.gz` | 1.9 G |
| `chembl_37.sdf.gz` | 888 M |
| `chembl_37_chemreps.txt.gz` | 279 M |
| `chembl_37.fps.gz` | 168 M |
| `chembl_37.h5` | 314 M |
| `chembl_37.fa.gz` / `_bio.fa.gz` / `_blast.fa.gz` / `_hmmr.fa.gz` | 4.6 M / 215 K / 4.6 M / 4.7 M |
| `chembl_uniprot_mapping.txt` | 1.2 M |
| `chembl_37_monomer_library.xml` | 3.7 M |
| plus `LICENSE`, `README`, `REQUIRED.ATTRIBUTION`, `checksums.txt` (SHA256), `chembl_37_release_notes.txt`, `chembl_37_schema.pdf`, `schema_documentation.{html,txt}` |

**License — gotcha:** the `LICENSE` file is **CC BY-SA 3.0 Unported**, *not* 4.0 (I read the file header directly). `REQUIRED.ATTRIBUTION` asks you to cite Mendez et al. 2019 (*NAR* 47(D1):D930-40, doi:10.1093/nar/gky1075) and to **preserve ChEMBL IDs and display the release number** in derived works.

**Repurposing endpoints — all live:**

| Endpoint | Verified result |
|---|---|
| `/molecule/CHEMBL413.json` | `max_phase: 4.0`, `first_approval: 1999`, `atc_classifications: ["S01XA23","L04AH01","L01EG04"]`, `black_box_warning: 1`, `usan_stem: -imus`, `withdrawn_flag`, `oral/parenteral`, `cross_references` (EMA, DailyMed) |
| `/drug.json` | Adds `applicants`, `atc_classification` (code+description), `drug_type`, `first_in_class`, `molecule_properties`, `helm_notation` |
| `/drug_indication.json?efo_term__icontains=Duchenne` | Returns `efo_id: MONDO:0010679`, `mesh_id: D020388`, `max_phase_for_ind: "4.0"`, `indication_refs` with NCT ID lists + EMA EPAR links |
| `/drug_indication.json?efo_id=MONDO:0010679` | **55** indication records |
| `/mechanism.json?molecule_chembl_id=CHEMBL413` | `action_type: INHIBITOR`, `mechanism_of_action: "FK506-binding protein 1A inhibitor"`, `target_chembl_id: CHEMBL1902`, DailyMed refs |
| `/molecule_form.json?parent_chembl_id=CHEMBL413` | parent/salt form mapping |
| `/atc_class.json?level5=L04AH01` | Full L→L04→L04A→L04AH→L04AH01 hierarchy + `who_name: sirolimus` |
| `/drug_warning.json` | `warning_class` (e.g. hepatotoxicity), `warning_country`, `efo_id_for_warning_class`, DailyMed/FDA refs |

**`atc_class` gotcha:** `/atc_class/L04AH01.json` (path lookup) **fails** — you must filter: `/atc_class.json?level5=L04AH01`.

**`max_phase` — VERIFIED as float.** Live counts: `-1`→2,499 · `0.5`→25 · `1`→1,613 · `2`→9,054 · `3`→1,892 · `4`→4,225. Meaning: `4.0` approved, `3.0/2.0/1.0` Phase 3/2/1, `0.5` Early Phase 1, `-1.0` unknown, `null` preclinical. Note `/drug_indication` returns `max_phase_for_ind` as a **string** `"4.0"` while `/mechanism` returns an **int** `4` — inconsistent typing across endpoints.

**Pagination gotcha:** `limit` silently caps at **1000** (`?limit=1001` returns `"limit": 1000`). Follow `page_meta.next`.

---

## 3. Open Targets — **VERIFIED, with breaking changes**

**Bulk:** `https://ftp.ebi.ac.uk/pub/databases/opentargets/platform/latest/output/` (= `26.06/`, dated 2026-06-25). Also `croissant.json` (626 K), `manifest.json` (20 M), `metrics.parquet`, `disk_images/`, `input/`, `intermediate/`, `view/`.

**⚠ The dataset names in the brief are all obsolete.** Traced across releases:

| Brief's name | 24.09 (`output/etl/parquet/`) | 25.09 (`output/`) | **26.06 (latest)** |
|---|---|---|---|
| `known_drug` | `knownDrugsAggregated/` | `known_drug/` | **REMOVED** |
| `molecule`/`drug` | `molecule/` | `drug_molecule/` | `drug_molecule/` |
| `indication` | `indication/` | `drug_indication/` | **`clinical_indication/`** |
| `mechanismOfAction` | `mechanismOfAction/` | `drug_mechanism_of_action/` | `drug_mechanism_of_action/` |
| `associationByDatasourceDirect` | camelCase | — | `association_by_datasource_direct/` |

Two renames happened: **snake_case + singular in 25.03**, then **`known_drug`/`drug_indication` replaced in 26.03** by `clinical_indication/`, `clinical_report/`, `clinical_target/`, and `evidence_clinical_precedence/`. Also present: `drug_warning/`, `openfda_significant_adverse_drug_reactions/`, `pharmacogenomics/`, `evidence_orphanet/` (rare-disease relevant), plus ~20 other `evidence_*` datasets.

**Parquet layout — two shapes coexist:**
- `clinical_indication/clinical_indication.parquet` — single file, 4.7 M
- `drug_molecule/` — Spark-style: `_SUCCESS` + `part-00000-<uuid>-c000.snappy.parquet` (14 M)

Format is **parquet only** — the pipeline no longer emits JSON. Open Targets ships `p2j` for parquet→NDJSON.

**GCS mirror — VERIFIED, with a cost gotcha:** `gs://open-targets-data-releases/`. Listing returns:
> `Bucket is a requester pays bucket but no user project provided.`

You must supply a billing project and **you pay egress**. No BigQuery dataset is documented.

**License:** **CC0 1.0** (public domain dedication) for the Platform. Caveat: individual upstream datasources retain their own licenses (Ensembl/UniProt/Reactome CC BY 4.0; ClinVar/Gene2Phenotype under EMBL-EBI terms; Cancer Gene Census, Genomics England PanelApp, Project Score carry "commercial use for Open Targets" notes).

**GraphQL rate limits:** **none documented, none advertised.** No API key needed. Response headers carry no `RateLimit-*`/`Retry-After` (only `server: nginx/1.31.3`, HSTS, `x-content-type-options`). Treat as best-effort fair use.

**⚠ `knownDrugs` is gone from the GraphQL schema too.** `Disease.knownDrugs` → `Cannot query field 'knownDrugs' on type 'Disease'`. Replacement is **`drugAndClinicalCandidates`** (type `clinicalIndicationsFromDiseaseImp`, no args). Also renamed on `Drug`: `isApproved` removed, `maximumClinicalTrialPhase` → **`maximumClinicalStage`**.

**Working query + real response:**
```graphql
query kd($efoId: String!) {
  disease(efoId: $efoId) {
    id name
    drugAndClinicalCandidates {
      count
      rows {
        id maxClinicalStage
        drug { id name drugType maximumClinicalStage }
        clinicalReports { id trialPhase clinicalStage trialOverallStatus source year }
      }
    }
  }
}
# variables: {"efoId": "MONDO_0010679"}
```
```json
{"disease": {"id":"MONDO_0010679","name":"Duchenne muscular dystrophy",
 "drugAndClinicalCandidates": {"count": 62, "rows": [
  {"maxClinicalStage":"APPROVAL","drug":{"id":"CHEMBL4297762","name":"GOLODIRSEN","drugType":"Oligonucleotide"},
   "clinicalReports":[{"id":"label/2019/211970s000lbl.pdf","clinicalStage":"APPROVAL","source":"FDA"}]},
  {"maxClinicalStage":"PHASE_3","drug":{"id":"CHEMBL2109377","name":"PAMREVLUMAB","drugType":"Antibody"},
   "clinicalReports":[{"id":"nct04371666","trialPhase":"PHASE3","trialOverallStatus":"TERMINATED","source":"AACT"}]},
  {"maxClinicalStage":"PHASE_1","drug":{"id":"CHEMBL5095171","name":"BOCIDELPAR","drugType":"Small molecule"},
   "clinicalReports":[{"id":"nct04184882","trialPhase":"PHASE1","trialOverallStatus":"TERMINATED","source":"AACT"}]}]}}}
```
Note `clinicalStage` is now an enum string (`APPROVAL`, `PHASE_3`…), not a number. `trialOverallStatus: TERMINATED` gives you failure signal directly — useful as a repoDB substitute.

---

## 4. DrugCentral — **VERIFIED (connected live)**

**Public postgres works.** Connected with `psql`:
```
host=unmtid-dbs.net  port=5433  user=drugman  password=dosage  dbname=drugcentral
```
→ `PostgreSQL 14.8 (Ubuntu 14.8-0ubuntu0.22.04.1)`. Confirmed by drugcentral.org: *"available via public instance at drugcentral:unmtid-dbs.net:5433, username="drugman", password="dosage""*.

**Release:** `select * from dbversion` → **version 54, 2023-11-01**. Matches the site's "Download Database dump 11/01/2023 (Postgres v14.5)". **DrugCentral 2023 is still the current release** — no 2024/2025/2026 update.

Full dump: `https://unmtid-dbs.net/download/drugcentral.dump.11012023.sql.gz` — **1,400,714,190 bytes (~1.4 GB)**, confirmed via range request.

**License:** **CC BY-SA 4.0** (drugcentral.org/privacy). Cite *NAR* doi:10.1093/nar/gkw993.

**Repurposing tables (live row counts):**

| Table | Rows | Key columns |
|---|---|---|
| `omop_relationship` | 42,307 | `struct_id, concept_id, relationship_name, concept_name, umls_cui, snomed_full_name, cui_semantic_type, snomed_conceptid` |
| `active_ingredient` | 288,489 | `struct_id, active_moiety_unii, substance_unii, substance_name, ndc_product_code, quantity, unit` |
| `identifier` | 82,230 | `identifier, id_type, struct_id, parent_match` |
| `faers` | 364,935 | `struct_id, meddra_name, meddra_code, level, llr, llr_threshold, drug_ae, drug_no_ae, no_drug_ae, no_drug_no_ae` |
| `act_table_full` | 20,978 | bioactivity |
| `atc` | 5,372 | `code, chemical_substance, l1..l4_code/_name` |
| `struct2atc` | 5,148 | structure↔ATC bridge |
| `structures` | 4,995 | `id, name, smiles, inchi, inchikey, cas_reg_no, stem, status, fda_labels, molfile` |
| `approval` | 3,915 | `struct_id, approval, type, applicant, **orphan**` |

**`omop_relationship.relationship_name` distribution** — this is the repurposing goldmine:
`contraindication` 27,731 · **`indication` 12,047** · **`off-label use` 2,525** · `symptomatic treatment` 2 · `reduce risk` 1 · `diagnosis` 1

**`approval.orphan`** = `t` 618 / `f` 130 / null 3,167 → direct orphan-drug filter for rare disease.

**`identifier.id_type`** cross-map coverage: `ChEMBL_ID` 7,129 · `UNII` 5,185 · `PUBCHEM_CID` 5,013 · `DRUGBANK_ID` 4,368 · `CHEBI` 4,302 · `INN_ID` 4,232 · `RXNORM` 3,525 · `MESH_*`, `SNOMEDCT_US`, `UMLSCUI`, `KEGG_DRUG`, `IUPHAR_LIGAND_ID`.

**Live repurposing query that works:**
```sql
select s.id, s.name, o.concept_name, o.relationship_name, a.approval, a.type
from structures s
join omop_relationship o on o.struct_id = s.id
left join approval a on a.struct_id = s.id and a.type='FDA'
where o.concept_name ilike '%pulmonary arterial hypertension%'
  and o.relationship_name = 'indication';
-- → ambrisentan (2007-06-15), beraprost, bosentan (2001-11-20), epoprostenol (1995-09-20),
--   iloprost, macitentan, riociguat, selexipag (2015-12-21)
```

**⚠ Gotcha:** the `public` schema is **polluted with third-party junk** — the `drugman` account apparently has write access and unrelated users have created ~60+ tables (`DEMO_PHARMACOVIGILANCE_*`, `NURSESCHEDULINGDEMO_*`, `OBJECTDETECTION_YOLO_*`, `GENAIFIERCEPHARMA_*`…). Never do `select * from information_schema.tables` and assume it's DrugCentral; whitelist the real table names. Also treat the instance as untrusted-writable and non-authoritative — pull the 1.4 GB dump for anything reproducible.

---

## 5. repoDB — **VERIFIED**

**URL:** `https://unmtid-shinyapps.net/shinyapps/repodb/` → **404 (confirmed)**. Working: **`https://unmtid-shinyapps.net/shiny/repodb/`** → 200 (also `https://unmtid-shinyapps.net/repodb/` → 200). Shiny app, R 1.7.4 / Bootstrap 3.4.1.

**Contents (from live app text):** **2,381 approved drugs** (curated from DrugCentral), **1,462 diseases/indications**, all mapped to **UMLS CUIs**. Drugs listed with **DrugCentral and DrugBank IDs**.

**Download:** no static file URL — it's a Shiny `downloadHandler`. Filenames: **`full.csv`** (full DB, comma-separated), `drugsearch.tsv`, `diseasesearch.tsv` (filtered subsets). Requires clicking the Download tab in a browser session.

**Columns (verified in `R/repodb/app.R`, all three handlers):**
```
drug_name, drugbank_id, ind_name, ind_id, NCT, status, phase, DetailedStatus
```
Status values: `Approved`, `Terminated`, `Withdrawn`, `Suspended`. Phases: `Phase 0`–`Phase 3`.

**License:** **CC BY 4.0** (`https://creativecommons.org/licenses/by/4.0/`, linked in-app). Source versions stated in-app: **AACT (2023-06-14) and UMLS (2023AA)** + DrugCentral. GitHub `unmtransinfo/DrugRepoDB` has **no LICENSE file** (`license: None` via GitHub API); last push **2023-06-15** — the repo is code-only (R scripts), not the data.

**⚠ The "failed" caveat, verified in source.** `R/clinicaltrials_gov.R` derives failures purely from AACT overall_status:
```r
clin <- clin[phase %in% c("Phase 0","Early Phase 1","Phase 1","Phase 1/Phase 2",
                          "Phase 2","Phase 2/Phase 3","Phase 3")]
# Failed Only
clin <- clin[overall_status %in% c("Suspended","Terminated","Withdrawn")]
clin <- clin[, .(nct_id, phase, overall_status, why_stopped)]
```
So a "failure" means **the trial registration stopped**, not that the drug failed on efficacy. Trials are terminated for enrollment shortfalls, funding, business decisions, sponsor bankruptcy — `why_stopped` is free text and often blank. Treating these as negative labels injects substantial label noise. Also: Phase 4 is excluded, and the dataset is frozen at **2023-06-14** — three years stale.

---

## 6. Broad Drug Repurposing Hub — **VERIFIED**

Both files live at `https://repo-hub.broadinstitute.org/public/data/`:

| File | Bytes | Data rows |
|---|---|---|
| `repo-drug-annotation-20250818.txt` | 661,900 | **7,540** (7,550 lines − 9 meta − 1 header) |
| `repo-sample-annotation-20250818.txt` | 4,072,927 | **22,612** |

Tab-separated, 9 `!`-prefixed metadata lines, `File_date 8/18/2025`.

**Drug annotation columns:** `pert_iname, clinical_phase, moa, target, disease_area, indication`
**Sample annotation columns:** `broad_id, pert_iname, qc_incompatible, purity, vendor, catalog_no, vendor_name, expected_mass, smiles, InChIKey, pubchem_cid, deprecated_broad_id`

**Field contents (verified distributions):**
- **`clinical_phase`** (7,540 rows): `Launched` 2,718 · `Preclinical` 2,381 · `Phase 2` 915 · `Phase 1` 655 · `Phase 3` 500 · `Withdrawn` 126 · `Phase 1/Phase 2` 97 · `Phase 2/Phase 3` 53 · blank 95
- **`moa`** — free-text mechanism, e.g. `c-Myc inhibitor`, `sterol demethylase inhibitor`, `glucocorticoid receptor agonist`
- **`target`** — pipe-delimited HGNC symbols: `AR | CYP1A2 | CYP2B6 | CYP3A5 | ESR1 | ESR2 | NR1H4 | NR1I2 | NR3C1 | PGR`
- **`disease_area`** — broad therapeutic area: `infectious disease` 377 · `neurology/psychiatry` 364 · `oncology` 180 · `cardiology` 171 · `endocrinology` 141 · `gastroenterology` 114 · `dermatology` 112 · `pulmonary` 93 · `hematologic malignancy` 71 · `ophthalmology` 54 · `rheumatology` 46
- **`indication`** — specific conditions, comma-separated inside quotes: `"ulcerative colitis, rheumatoid arthritis, psoriasis, joint inflammation, eczema"`

**⚠ License: NOT open.** From the `!Restrictions` line:
> "The Drug Repurposing Hub data is provided for **non-commercial use only**."

`!Disclaimer`: research use only, no clinical treatment decisions, no accuracy warranty. Cite Corsello SM et al., *Nature Medicine* 2017;23(4):405-408, doi:10.1038/nm.4306. Contact `repurposing@broadinstitute.org`.

**⚠ Serious gotcha:** the server returns **HTTP 200 with a 36,590-byte HTML page** for files that don't exist. I probed `repo-drug-annotation-20260818.txt`, `-20260218`, `-20251118`, and even `-99999999` — all returned **200**, all HTML. You **cannot** discover newer releases by probing status codes. Validate by checking the body starts with `!Source` and/or size > 500 KB. `20250818` is the only real drug-annotation file I could confirm.

Multi-value fields use ` | ` — and note the data quirk where `disease_area` sometimes repeats itself (`infectious disease | infectious disease`, 61 rows), so dedupe after splitting.

---

## 7. WHO INN — **VERIFIED, with a dead URL in the brief**

**⚠ `https://mednet.edqm.eu/` is DEAD — the hostname does not resolve** (`Could not resolve host: mednet.edqm.eu`; `edqm.eu` itself resolves fine at 193.164.228.50, so it's not a network issue). MedNet-INN has been **migrated to the WHO's own infrastructure and renamed "School of INN (SoINN)"**.

Confirmed from `https://www.who.int/teams/health-product-and-policy-standards/inn`, which reads *"Request access to MedNet-INN (now School of INN - SoINN)"*:
- **SoINN portal:** `https://extranet.who.int/soinn/` → **200** (Moodle-based; access request required)
- Member deep link: `https://extranet.who.int/soinn/mod/page/view.php?id=49`
- INN online application: `https://extranet.who.int/tools/inn_online_application/` → 200

**Proposed / Recommended INN lists — free, PDF only:**
- Index: `https://www.who.int/teams/health-product-and-policy-standards/inn/inn-lists`
- Proposed: `https://www.who.int/publications/m/item/inn-pl-<N>` — latest **PL 135, 19 July 2026** (134 = 2026-01-29, 133 = 2025-07-10)
- Recommended: `https://www.who.int/publications/m/item/inn-rl-<N>` — verified 200 for rl-93/94/95
- Mirrored in WHO IRIS: `https://iris.who.int/` (DSpace 7 REST API at `/server/api/discover/search/objects?query=…` works unauthenticated and is the practical way to enumerate them)
- Lists go back to 1955; also published in *WHO Drug Information*

**Machine-readable cumulative INN list: NO free public download.** Searching WHO IRIS for cumulative INN lists returns only *"Cumulative list of proposed international nonproprietary names… lists 1-25"* (**1971**) and the radicals/groups comprehensive lists (1997, 2004). No modern cumulative list is publicly downloadable. The current cumulative INN data + search tool sits **behind SoINN registration** at `https://extranet.who.int/soinn/`.

**Licensing:** WHO publications are typically **CC BY-NC-SA 3.0 IGO** and INN itself is explicitly non-proprietary/public-domain by design ("their use is normally required by national or… international legislation"). But **no bulk machine-readable INN file is offered under any open license** — I could not verify an explicit data license for a cumulative INN dataset. **UNVERIFIED: any open-licensed bulk INN download.** Practical path: parse the PL/RL PDFs, or use DrugCentral's `identifier` table (`INN_ID`, 4,232 rows) / ChEMBL `pref_name` + `usan_stem` as proxies.

---

## 8. WHOCC ATC/DDD Index — **VERIFIED: no free bulk download, no API**

**⚠ Domain moved:** `https://www.whocc.no/atc_ddd_index/` now **301-redirects to `https://atcddd.fhi.no/atc_ddd_index/`** (Norwegian Institute of Public Health). Update any hardcoded whocc.no URLs.

**Code lookup URL pattern (verified live):**
```
https://atcddd.fhi.no/atc_ddd_index/?code=<ATC_CODE>
```
`?code=L04AH01` returns the full hierarchy with Guidelines text: `L` ANTINEOPLASTIC AND IMMUNOMODULATING AGENTS → `L04` IMMUNOSUPPRESSANTS → `L04A` IMMUNOSUPPRESSANTS → `L04AH` Mammalian target of rapamycin (mTOR) kinase inhibitors → `L04AH01`. Plain server-rendered XHTML (scrapeable), but there is **no JSON/REST API** — one HTTP request per code.

**Bulk access (verbatim from `atcddd.fhi.no/atc_ddd_index_and_guidelines/atc_ddd_index/`, last updated 2026-01-28):**
> "The ATC index is available in **electronic format (Excel or XML)** and can be downloaded from a **registered user account**. Access is provided via the ordering portal Orders ATC/DDD… **printed copies of the ATC Index and the ATC/DDD Guidelines are no longer provided**. Access to a searchable version of the ATC Index with DDDs (including text from the Guidelines) is available **free of charge** on this website (ATC/DDD Index 2026)."

- Ordering portal: `https://orders.atcddd.fhi.no/` (Angular SPA; `/api/products` and `/api/publications` return 200 but empty without auth — **UNVERIFIED: exact prices**, registration required)
- **Free:** "Lists of new ATC codes, DDDs and alterations, normally made available in November/December, can be accessed and downloaded **free of charge**" from the same portal — i.e. the *deltas* are free, the *full index* is not.

**Copyright (from `https://atcddd.fhi.no/copyright_disclaimer/`):**
> "Use of all or parts of the material requires reference to the WHO Collaborating Centre for Drug Statistics Methodology." … "**Copying and distribution for commercial purposes is not allowed. Changing or manipulating the material is not allowed.**"

Required citation: *WHO Collaborating Centre for Drug Statistics Methodology, ATC classification index with DDDs, 2026. Oslo, Norway 2026.*

**Practical read:** you may use ATC codes internally with attribution, but **redistributing the ATC index (or a derived table that reconstitutes it) commercially is prohibited**, and "changing or manipulating" arguably covers remapping. For a commercial pipeline, source ATC from a permissively-licensed proxy instead.

**Free ATC proxies — verified:**

| Source | License | Coverage | Notes |
|---|---|---|---|
| **ChEMBL `atc_class`** | CC BY-SA 3.0 | full L1–L5 + `who_name` | `?level5=L04AH01` (see §2) |
| **ChEMBL `molecule.atc_classifications`** | CC BY-SA 3.0 | per-molecule L5 list | `["S01XA23","L04AH01","L01EG04"]` |
| **DrugCentral `atc` + `struct2atc`** | CC BY-SA 4.0 | 5,372 codes / 5,148 links | `l1..l4_code/_name` columns |
| **SIDER `drug_atc.tsv`** | CC BY-SA 4.0 | 32,760 bytes, live (HTTP 200) | frozen at SIDER 4.1, 2015-10-21 |
| **DrugBank open vocabulary** | CC0 (open subset) | drugbank_id + name + ATC | full DrugBank needs a license |
| **RxClass (RxNorm)** | US public domain / NLM | ATC1–4 classes | see below |

**RxClass ATC — VERIFIED live:**
```
https://rxnav.nlm.nih.gov/REST/rxclass/class/byRxcui.json?rxcui=35302&relaSource=ATC
→ sirolimus (rxcui 35302, tty IN): L01EG "Mammalian target of rapamycin (mTOR) kinase inhibitors" (classType ATC1-4),
  L04AH (same), S01XA "Other ophthalmologicals"

https://rxnav.nlm.nih.gov/REST/rxclass/classMembers.json?classId=L04AH&relaSource=ATC
→ 2 members: everolimus (141704, nodeAttr SourceId=L04AH02), sirolimus (35302, SourceId=L04AH01)
```
**⚠ RxClass gotcha:** `classType` is **`ATC1-4`** — RxClass only exposes ATC **levels 1–4** as classes. Level-5 codes appear only as a `nodeAttr` `SourceId` on `classMembers` results. To get L5 codes you must enumerate L4 classes and read `nodeAttr`, or use ChEMBL/DrugCentral instead. Also RxNorm is US-centric, so ATC codes for non-US drugs will be missing.

---

## Summary of changes vs. the brief

| # | Issue | Impact |
|---|---|---|
| 3 | OT `known_drug` **removed** in 26.03; `indication` → `clinical_indication`; GraphQL `knownDrugs` → `drugAndClinicalCandidates` | **Breaking** — pipeline must be rewritten |
| 7 | `mednet.edqm.eu` **DNS-dead**; now `https://extranet.who.int/soinn/` | **Breaking** |
| 8 | `whocc.no` → `atcddd.fhi.no` | Breaking (301 redirect saves you) |
| 2 | ChEMBL license is CC BY-SA **3.0**, not 4.0 | Compliance |
| 6 | Broad Hub is **non-commercial only**; server returns 200+HTML for missing files | Compliance + silent-failure risk |
| 1 | PubChem 400/min + 300 s/min limits **no longer published**; only 5 req/s | Plan for 5 req/s + header backoff |
| 3 | OT GCS bucket is **requester-pays** | Cost |
| 4 | DrugCentral `public` schema polluted by third-party writes; frozen at 2023-11-01 | Whitelist tables; use the 1.4 GB dump |
| 5 | repoDB "failures" = AACT `Suspended/Terminated/Withdrawn` only; frozen 2023-06-14; no static download URL | Label noise; manual download |

**Cleanest licensing for a commercial repurposing pipeline:** Open Targets (CC0) → DrugCentral (CC BY-SA 4.0) → ChEMBL (CC BY-SA 3.0) → PubChem (public domain). Avoid Broad Hub (non-commercial) and raw WHOCC ATC (no commercial redistribution); get ATC from ChEMBL/DrugCentral/RxClass instead.