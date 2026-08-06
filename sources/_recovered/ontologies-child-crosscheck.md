<!-- RECOVERED from subagent transcript agent-a3587e443c4939c99.jsonl, session fd64561f-7c90-41a2-95cf-b4a133a8fe0f, research date 2026-08-05.
     Child of agent 3 (GARD/OMIM/MONDO/HPO). Synthesized into 03 but abridged; kept for detail + cross-check.
     Verbatim agent deliverable — not re-edited. -->

All four sources verified. Here is the technical reference.

---

# Rare-Disease Data Source Reference — Verified 2026-08-05

**Verification method:** `curl` (status + payload inspection), WebFetch, and Exa's fetcher for hosts that block automated agents. Files marked VERIFIED were actually downloaded and their contents inspected.

---

## 1. GARD — Genetic and Rare Diseases Information Center

### Status: home site VERIFIED, bulk CSV VERIFIED, **no API exists**

| URL | Status | Notes |
|---|---|---|
| `https://rarediseases.info.nih.gov/` | **VERIFIED** 200 | Current canonical home. NCATS/NIH branded. |
| `https://ncats.nih.gov/gard` | **VERIFIED** 301 | Redirects → `ncats.nih.gov/research/research-resources/gard` |
| `https://ncats.nih.gov/research/research-resources/gard` | **VERIFIED** 200 | NCATS landing page. No data links. |
| `https://rarediseases.info.nih.gov/about` | **VERIFIED** 200 | Where the CSV link is published |
| `https://rarediseases.info.nih.gov/?gard_id=0005528` | **VERIFIED** 200 | Current per-disease URL pattern |
| `https://rarediseases.info.nih.gov/diseases/6975/marfan-syndrome` | **UNVERIFIED** 404 | Legacy numeric path — **dead**, still embedded in MONDO |
| `https://rdas.ncats.nih.gov/` + `/about` | **VERIFIED** 200 | Rare Disease Alert System (separate resource) |

### The bulk download (the only one that exists)

**VERIFIED — downloaded, 3,638,571 bytes, `text/csv`, 16,215 lines = 16,214 diseases:**

```
https://ncats.file.force.com/sfc/dist/version/download/?oid=00Dt00000004XG2&ids=068SJ00001HZAaEYAX&d=%2Fa%2FSJ00000BC4Xl%2FUj7U9WuHII571Akz5AUBLe6WSCeelaMBynbjWybmhuA&asPdf=false
```

Filename served: **`GARD Rare Disease List Jun2026.csv`**. Exactly 4 columns, UTF-8 with BOM:

```
ID,DisplayName,Synonyms,URL
GARD:0027416,10p13-p14 deletion syndrome,,
GARD:0021052,10q22.3q23.3 microduplication syndrome,dup(10)(q22.3q23.3)|trisomy 10q22.3q23.3,https://rarediseases.info.nih.gov/?gard_id=0021052
```

- `Synonyms` is **pipe-delimited (`|`)**, lowercased, and quoted when it contains commas.
- `URL` is **frequently empty** (not every GARD entry has a live page).

### GARD ID system
`GARD:NNNNNNN` — 7-digit zero-padded. **Critical gotcha:** this is the *new* ID scheme. The legacy scheme was a short unpadded integer (e.g. `6975` for Marfan) used in the old `/diseases/{id}/{slug}` URLs. MONDO's SSSOM CURIE map still expands GARD as `https://rarediseases.info.nih.gov/diseases/` which **produces dead links**. Build your own resolver against `?gard_id=`.

### What you get
Disease name + synonym list + ID only. **No phenotypes, no genes, no drugs, no epidemiology, no text.** The narrative disease pages are website-only.

### API / bulk beyond the CSV — negative findings
- **No GARD REST API.** Nothing at `rarediseases.info.nih.gov/api`; NCATS publishes no GARD API docs.
- **No `ncats/gard-data` GitHub repo.** The NCATS org has `epi4GARD` (epidemiology NER from PubMed) and `RD-Clust` (rare-disease clustering for drug repurposing) — both research code, not data dumps.
- **Not on data.gov.** Queried the CKAN API (`catalog.data.gov/api/3/action/package_search`) for `GARD`, `rare+diseases`, `genetic+and+rare+diseases` → no GARD dataset. Same for healthdata.gov.
- **Not in NCATS Translator's SmartAPI registry.** `smart-api.info/api/query?q=GARD` → `"total":0`. GARD reaches Translator only indirectly, as MONDO xrefs inside the Monarch KG.
- **RDAS is a different product** — three Neo4j KGs (RDAS_SAKG from PubMed/PubTator, RDAS_CTKG from ClinicalTrials.gov, RDAS_GFKG from NIH grants). UI is an Angular SPA; no documented public REST API. Source at github.com/ncats.

### License / cadence
US federal government work → **public domain (17 U.S.C. §105)**, but NCATS publishes **no explicit license statement**. Cadence is **irregular** — versioned by month in the filename only.

> **Biggest gotcha:** the CSV URL is a Salesforce content-version link. The `ids=068SJ00001HZAaEYAX` token is bound to the *Jun2026* file. When NCATS publishes the next list, **this URL will serve stale data or break** — there is no `latest` alias. You must re-scrape `rarediseases.info.nih.gov/about` for the current link on each run.

**Recommendation:** don't build on GARD directly. Take GARD IDs from MONDO instead — MONDO carries **15,947 GARD xrefs** (below), which is 98% of the GARD list, already crosswalked to OMIM/Orphanet/HPO.

---

## 2. OMIM

### Status: VERIFIED (via Exa fetcher — `omim.org` returns **403 to WebFetch and curl**, including with a browser UA; it is behind bot protection. `api.omim.org` responded live.)

| URL | Status |
|---|---|
| `https://www.omim.org/downloads/` | **VERIFIED** — full content retrieved |
| `https://www.omim.org/api` | **VERIFIED** — API registration form |
| `https://www.omim.org/help/api` | **VERIFIED** — full API docs |
| `https://www.omim.org/help/agreement` | **VERIFIED** — the Use Agreement |
| `https://api.omim.org/api/entry?mimNumber=100100` | **VERIFIED** live — HTTP 400 with the exact message below |

The unauthenticated API call returned, verbatim:

> `org.omim.api.exceptions.BadRequestException: An API key is required to use the OMIM API, please go to https://omim.org/api to register for API access`

### ⚠️ Licensing — read this first, it is a hard blocker for a company

Exact text from **`https://www.omim.org/downloads/`** and **`https://www.omim.org/api`** (identical on both):

> "**For-profit companies or anyone planning to redisplay or incorporate OMIM data into software MUST secure a license** to obtain access to these files. Registering below will initiate this process, and you can expect to hear from the JHU licensing office within 2 business days."

And the click-through declaration on both forms:

> "Johns Hopkins University holds the copyright to OMIM including the collective data therein. I hereby declare that I will not use or share the data contained in OMIM for any commercial purposes, **will not develop a derivative database**, nor distribute the data to a third party without first obtaining a license from Johns Hopkins University to do so."

From **`https://www.omim.org/help/agreement`** (the Use Agreement):

> "Users at for-profit or commercial entities who want to download all or part of OMIM **must obtain a license by paying applicable licensing fees** to and entering into a license agreement with JHU... In addition, **if you access OMIM without a license, you agree to payment of penalties of double the standard license.**"

> "If OMIM data are downloaded in whole or part from the site or API servers and used in a database or analysis software, **the data must be refreshed at least weekly.**"

Additional binding terms verified:
- The agreement explicitly covers "the OMIM.org API, or downloads of OMIM data" — **the API is not a loophole around the download license.**
- Robots are bound by the agreement and `https://omim.org/robots.txt`.
- License is "non-exclusive, non-transferable and non-sub-licensable."
- **Registration rejects free-mail domains** (Gmail, Yahoo, Hotmail, Live, MSN, iCloud, 126.com, 163.com, qq.com) and rejects descriptions containing URLs. A `.com` address grants JHU Tech Ventures permission to contact you as a licensing lead.
- Commercial licensing contact: **`JHTV-OMIM@jhmi.edu`**.

**Bottom line for a drug-repurposing company:** a "derivative database" is precisely what a repurposing pipeline builds. You need a paid JHU license before OMIM data touches your pipeline. **Use MONDO/HPO as the OMIM-free substitute** — both carry OMIM *identifiers* (not OMIM copyrighted text) under permissive terms.

### Downloads — exactly what's available

| File | Access | Contents |
|---|---|---|
| **`mim2gene.txt`** | **No registration** — the only free file | MIM number ↔ NCBI Gene ID ↔ Ensembl Gene ID ↔ HGNC approved symbol |
| **`mimTitles.txt`** | Registration (free for single-user academic / non-profit / government) | MIM numbers + titles |
| **`genemap2.txt`** | Registration | Synopsis of the Human Gene Map + genomic coordinates + inheritance |
| **`morbidmap.txt`** | Registration | Same content as `genemap2.txt`, sorted alphabetically by disorder |

Registration page: **`https://www.omim.org/downloads/`**. Files "are updated **nightly**." After approval you receive a **set of personalized URLs** — there are no stable public download paths. Note `mim2gene.txt` is registration-free specifically "to help interconnectivity of MIM numbers among other data resources," i.e. it is an ID crosswalk, not content.

### API

- **Host:** `api.omim.org` (only host). Registration: **`https://www.omim.org/api`**. Docs: **`https://www.omim.org/help/api`**.
- **URL shape:** `/api/[handler]?[params]`, `/api/[handler]/[component]?[params]`, `/api/[handler]/[action]?[params]`
- **Handlers:** `entry`, `clinicalSynopsis`, `geneMap`, `search`, `status`, `apiKey`
- **Auth — three equivalent forms** (parameter name is **case-sensitive**):
  - Header `ApiKey: <key>`
  - Cookie `ApiKey=<key>`
  - Query `?apiKey=<key>`
- **Key must be renewed yearly**; JHU may revoke at discretion.
- **GET only** (except `apiKey` handler, which takes POST/DELETE to set/clear the cookie).
- **Formats:** `format=json` or `format=xml`. Data updated nightly.
- **Limits (per-request, not per-day):**
  - `entry` and `clinicalSynopsis`: **20 per request if any `include` is specified**, otherwise unlimited
  - `geneMap`: **100 per request**
  - Paginate with `start` and `limit`
  - **No published daily quota**, but HTTP **429 "Too Many Requests"** is documented as "the quota for the API key has been exceeded" — so a quota exists and is undocumented.
- **Status codes:** 200, 400 (bad URL), 401 (invalid/inactive key), 404, 429 (quota), 500
- **gzip supported** — send `Accept-Encoding: gzip`; docs claim 4–5× reduction. curl does *not* enable it by default.
- **`entry` includes:** `text`, `existFlags`, `allelicVariantList`, `clinicalSynopsis`, `seeAlso`, `referenceList`, `geneMap`, `externalLinks`, `contributors`, `creationDate`, `editHistory`, `dates`, `all`
- **Text sub-sections** (via `include=text:<section>`): `animalModel`, `biochemicalFeatures`, `clinicalFeatures`, `clinicalManagement`, `cloning`, `cytogenetics`, `description`, `diagnosis`, `evolution`, `geneFamily`, `geneFunction`, `geneStructure`, `geneTherapy`, `geneticVariability`, `genotype`, `genotypePhenotypeCorrelations`, `heterogeneity`, … — `clinicalManagement` and `geneTherapy` are the repurposing-relevant ones.
- Multiple MIMs: `?mimNumber=100100&mimNumber=100200` or `?mimNumber=100100,100200`

### MIM number system
6-digit integer with a **symbolic prefix that encodes entry type**:
- `*` gene
- `#` phenotype with known molecular basis (descriptive entry — **this is what you want for disease→gene**)
- `+` gene + phenotype combined (legacy)
- `%` phenotype, Mendelian, unknown molecular basis
- (none) phenotype with unclear Mendelian basis
- `^` moved or removed

Leading digit encodes historical inheritance/date-of-creation buckets (1–2 = autosomal pre-1994, 3 = X-linked, 4 = Y-linked, 5 = mitochondrial, 6 = autosomal post-1994). **`OMIMPS:` is a separate namespace** for Phenotypic Series (MONDO carries 615 of them) — do not conflate with `OMIM:`.

---

## 3. Monarch Initiative + MONDO

### 3a. Monarch API

| URL | Status |
|---|---|
| `https://monarchinitiative.org/` | **VERIFIED** 200 |
| `https://api.monarchinitiative.org/v3/docs` | **VERIFIED** 200 — FastAPI Swagger UI |
| **`https://api.monarchinitiative.org/openapi.json`** | **VERIFIED** 200 — **OpenAPI 3.1.0, 55 schemas** |
| `https://api.monarchinitiative.org/v3/openapi.json` | **UNVERIFIED** 404 |

> **Gotcha:** the Swagger UI lives at `/v3/docs` but its spec is served from the **root** `/openapi.json`, not `/v3/openapi.json`. Every operation path inside the spec is prefixed `/v3/api/...`. If you codegen a client, you must not double-prefix.

**Complete verified endpoint list** (all GET unless noted):

```
/v3/api/entity/{id}
/v3/api/entity/{id}/{category}
/v3/api/entity/{context_id}/case-phenotype-grid
/v3/api/entity/{context_id}/disease-phenotype-grid
/v3/api/entity/{context_id}/ortholog-phenotype-grid
/v3/api/entity-grid/{context_id}
/v3/api/entity-grid/traversable-associations/{entity_category}
/v3/api/association
/v3/api/case-phenotype-matrix/{disease_id}
/v3/api/histopheno/{id}
/v3/api/pathograph/{node_id}
/v3/api/search
/v3/api/autocomplete
/v3/api/mappings                     <-- the ID crosswalk endpoint
/v3/api/semsim/autocomplete
/v3/api/semsim/compare/{subjects}/{objects}
/v3/api/semsim/compare               (POST)
/v3/api/semsim/multicompare          (POST)
/v3/api/semsim/search/{termset}/{group}
/v3/api/semsim/search                (POST)
/v3/api/sources/versions
/v3/api/releases
/v3/api/version
/v3/api/annotate                     (GET, POST)
/v3/api/annotate/entities            (GET, POST)
/v3/api/ground                       (GET, POST)
```

**Auth: none.** No API key. Live-tested `entity/MONDO:0007947`, `search`, `mappings`, `releases`, `sources/versions` — all 200 JSON.

Live response for `/v3/api/entity/MONDO:0007947`:
```json
{"id":"MONDO:0007947","name":"Marfan syndrome","category":"biolink:Disease",
 "xref":["DOID:14323","GARD:0016535","ICD10CM:Q87.4","ICD9:759.82","MEDGEN:44287",
         "MESH:D008382","MedDRA:10026829","NANDO:1200644", ...]}
```

`/v3/api/mappings?entity_id=MONDO:0007947` returns **SSSOM-shaped rows** — the cleanest programmatic crosswalk:
```
subject_id, subject_label, predicate_id (skos:exactMatch),
object_id, object_label, mapping_justification (semapv:...), mapping_source (mondo.sssom)
```

The `semsim/*` endpoints (phenotype semantic similarity) and `annotate`/`ground` (free-text → HPO/MONDO) are the highest-value pieces for a repurposing pipeline — they give you patient-phenotype→disease ranking without you implementing Resnik/Phenodigm yourself.

### 3b. Monarch bulk downloads — Monarch KG

`https://data.monarchinitiative.org/` — **VERIFIED** 200. Top-level directories:
`dipper-kg`, `exomiser`, `hpo`, `mappings`, `monarch`, `monarch-gene-mapping`, **`monarch-kg`**, `monarch-kg-dev`, `phenologs`, `semantic-similarity`, `sri-reference-kg`, `upheno2`

**`https://data.monarchinitiative.org/monarch-kg/latest/`** — **VERIFIED**, complete file list:

| File | What it is |
|---|---|
| `monarch-kg.tar.gz` | **KGX** TSV nodes+edges (the canonical dump) |
| `monarch-kg.jsonl.tar.gz` | KGX JSON Lines |
| `monarch-kg.duckdb` | **DuckDB** database — best for analytics |
| `monarch-kg.db.gz` | SQLite |
| `monarch-kg.neo4j.dump` | Neo4j dump |
| `monarch-kg.neo4j.v5.dump` | Neo4j **v5** dump |
| `monarch-kg_nodes.neo4j.csv` / `monarch-kg_edges.neo4j.csv` | `neo4j-admin import` CSVs |
| `monarch-kg.nt.gz` | RDF N-Triples |
| `solr.tar.gz` | Prebuilt Solr index (powers the search API) |
| `phenio.db.gz` | **PHENIO** — merged phenotype/disease ontology (semsim backend) |
| `monarch-kg-schema.yaml`, `monarch-kg_schema_report.yaml` | LinkML schema |
| `metadata.yaml` | version + **sha256 per artifact** + full upstream source provenance |
| `merged_graph_stats.yaml`, `qc_report.yaml`, `connectivity_summary.yaml` | QC |
| `tsv/`, `data/`, `qc/`, `transform_output/` | subdirs |

**Verified current release: `2026-07-14`** (`metadata.yaml`: `biolink: 4.4.2`, `koza: 2.6.1`, `monarch-ingest: 0.8.0`).
**Verified scale** (`qc_report.yaml`): **1,582,279 nodes / 15,807,241 edges.**

> **Gotcha:** `qc_report.yaml` also reports **`dangling_edges: 2,951,148`** (~19% of edges) and `duplicate_nodes: 10,497`. You must filter dangling edges on load or your graph will have ~3M edges pointing at absent nodes.

Cadence: **monthly-ish, irregular** — verified dated dirs from `2023-09-28` through `2026-07-14`; sometimes two in a month (`2026-04-07`, `2026-04-14`), sometimes gaps (nothing between `2025-09-17` and `2025-11-18`). Use `/latest/` plus `/v3/api/releases` to pin.

> Note the `monarch-ingest` README still points at **`monarch-kg-dev/latest/`**. Use **`monarch-kg/latest/`** for production — `-dev` is the unstable build.

**Federated sources** (from `/v3/api/sources/versions` and `metadata.yaml`): Alliance of Genome Resources (MGI, RGD, ZFIN, WB, FB, SGD, XB), BGee, BioGrid, GO, HGNC, **HPOA**, NCBI Gene, Panther, **PHENIO** (which bundles **MONDO, HPO, Orphanet/ORDO, and MP/ZP/upheno**), PomBase, Reactome, STRING, ZFIN. **ClinVar and OMIM text are not directly ingested** — OMIM appears as identifiers via MONDO/HPOA only. That is deliberate and is exactly why Monarch is redistributable where OMIM is not.

**License:** `monarch-ingest` code is **BSD-3-Clause**. The KG is published as **CC BY 4.0** consistent with MONDO/PHENIO. `monarchinitiative.org/about/licensing` is **UNVERIFIED — 404**; there is no single authoritative license page, so for a commercial pipeline treat per-source licenses as governing (they are enumerated in `metadata.yaml`, which is the artifact to keep for compliance).

### 3c. MONDO — the ID crosswalk (the key resource)

**All PURLs VERIFIED 200** (they 302 to GitHub release assets):

| URL | Verified size |
|---|---|
| `https://purl.obolibrary.org/obo/mondo.owl` | 254,105,311 b |
| `https://purl.obolibrary.org/obo/mondo.json` | 107,497,863 b |
| `https://purl.obolibrary.org/obo/mondo.obo` | 53,086,111 b |
| `https://github.com/monarch-initiative/mondo/releases/latest` | 200 |

**Verified current release: `v2026-08-04`** (`data-version: releases/2026-08-04`). Cadence: **monthly, first Monday-ish** — verified `2026-08-04, 2026-07-06, 2026-06-02, 2026-05-05, 2026-04-07, 2026-03-03, 2026-02-03, 2026-01-06`. Far more regular than HPO.

**Verified scale:** **63,267 `[Term]` stanzas** in `mondo.obo`. ID format `MONDO:NNNNNNN` (7-digit).

**Release assets worth knowing** (verified from the GitHub API):
- `mondo.owl` / `.obo` / `.json` — full
- **`mondo-rare.owl` / `.obo` / `.json` + `mondo-rare_nodes.tsv` (15.4 MB) / `mondo-rare_edges.tsv` (3.8 MB)** — **rare-disease-only subset; start here**
- `mondo_nodes.tsv` (24.6 MB) / `mondo_edges.tsv` (22.1 MB) — **flat TSV, no OWL tooling needed**
- `mondo-base`, `mondo-simple`, `mondo-clingen`, `mondo-international`
- `mondo_release_diff_new_terms.tsv`, `mondo_release_diff_changed_terms.tsv` — **incremental delta files**, ideal for pipeline refresh
- `mondo_obsoletioncandidates.tsv`, `source-versions.tsv`

#### Cross-reference coverage — measured directly from `mondo.obo` (v2026-08-04)

| Prefix | xref count | | Prefix | xref count |
|---|---|---|---|---|
| UMLS | 21,660 | | MEDGEN | 21,660 |
| **GARD** | **15,947** | | DOID | 12,091 |
| **Orphanet** | **10,491** | | **OMIM** | **10,176** |
| SCTID (SNOMED) | 9,157 | | MESH | 8,211 |
| NCIT | 7,434 | | ICD9 | 5,658 |
| icd11.foundation | 4,637 | | OMIA | 3,196 |
| EFO | 2,400 | | NANDO | 2,345 |
| ICD10CM | 2,142 | | MedDRA | 1,488 |
| NORD | 911 | | ICDO | 769 |
| **OMIMPS** | **621** | | HP | 579 |

**SSSOM crosswalk file — VERIFIED, 13,111,988 bytes:**
```
https://raw.githubusercontent.com/monarch-initiative/mondo/master/src/ontology/mappings/mondo.sssom.tsv
```
> The release-asset path `releases/latest/download/mondo.sssom.tsv` is **UNVERIFIED — 404**. Only the `raw.githubusercontent.com` path works.

Columns: `subject_id | subject_label | predicate_id | object_id | object_label | mapping_justification`, preceded by a `#`-commented YAML `curie_map` block you must parse or skip.

**109,707 mappings**, of which **109,618 are `skos:exactMatch`** and only 88 are `skos:broadMatch`. Object breakdown: UMLS 21,660 · MEDGEN 21,660 · DOID 11,966 · **OMIM 10,045** · **Orphanet 9,785** · SCTID 9,123 · mesh 8,183 · NCIT 7,306 · icd11 4,635 · EFO 2,399 · ICD10CM 2,117 · OMIMPS 615.

> **Gotcha:** the SSSOM file **omits GARD** even though `mondo.obo` carries 15,947 GARD xrefs, and its `curie_map` maps GARD to the dead `/diseases/` URL prefix. **For GARD you must parse `mondo.obo`/`mondo.json` xrefs directly, not the SSSOM file.**

Also note in `mondo.obo`: xrefs carry `{source="MONDO:equivalentTo"}` vs `{source="MONDO:i2s"}` vs `{source="Orphanet:558/btnt"}` provenance qualifiers. **Only `MONDO:equivalentTo` is a true 1:1 equivalence** — `btnt` means "broader term maps to narrower term." Filtering on this is essential or you will silently merge distinct diseases. There is also a `gard_rare` subset tag (15,948 occurrences) for rare-disease filtering.

**License: CC BY 4.0** — VERIFIED from the OBO Foundry registry (`obofoundry.org/registry/ontologies.jsonld`: `{'label': 'CC BY 4.0', 'url': 'http://creativecommons.org/licenses/by/4.0/'}`). **Commercial use is permitted with attribution.** This makes MONDO the OMIM-safe substitute for disease identity and crosswalking.

---

## 4. HPO — Human Phenotype Ontology

### Downloads — all VERIFIED by download

| URL | Verified |
|---|---|
| `https://purl.obolibrary.org/obo/hp.obo` | 200, 11,222,341 b |
| `https://purl.obolibrary.org/obo/hp.json` | 200, 23,019,454 b |
| `https://purl.obolibrary.org/obo/hp/hpoa/phenotype.hpoa` | 200, 35,672,303 b |
| `https://github.com/obophenotype/human-phenotype-ontology/releases/latest/download/phenotype.hpoa` | 200, 35,672,303 b |
| `.../releases/latest/download/genes_to_phenotype.txt` | 200, 20,732,778 b |
| `.../releases/latest/download/phenotype_to_genes.txt` | 200, 66,907,216 b |
| `.../releases/latest/download/genes_to_disease.txt` | 200, 1,477,762 b |
| `https://hpo.jax.org/` | 200 (Angular SPA) |
| `https://hpo.jax.org/data/ontology`, `/data/annotations` | **UNVERIFIED — 404. These paths no longer exist.** |

> **Gotcha:** the old `hpo.jax.org/app/...` and `hpo.jax.org/data/...` download pages are gone. `hpo.jax.org` is now an Angular SPA whose only server routes are `/`, `/app`, `/browse` — every other path returns **HTTP 404 while still serving the SPA shell** (identical 60,203-byte body). A status-code health check on `hpo.jax.org/license` will report failure even though the page renders fine in a browser. **Fetch data from `purl.obolibrary.org` or GitHub releases, never from `hpo.jax.org`.**

**Verified current release: `2026-06-23`** (`data-version: hp/releases/2026-06-23`; 20,464 nodes in `hp.json`).

Cadence: **irregular, roughly every 1–3 months.** Verified tags: `v2026-06-23, v2026-06-06, v2026-02-16, v2026-01-08, v2025-11-24, v2025-10-22, v2025-09-01, v2025-08-11, v2025-05-06, v2025-03-03`. Note the 4-month gap Feb→Jun 2026 and the 17-day turnaround Jun 6→Jun 23. **Do not assume a fixed schedule** — poll the GitHub releases API.

Other release assets: `hp-base.{obo,owl,json}` (no reasoner), `hp-full.{obo,owl,json}` (reasoner-classified), `hp-international.*`, translations (`hp-fr.*`, etc.), `hp-simple-non-classified`.

### `phenotype.hpoa` — verified structure

Four `#`-comment lines, then a **tab-separated** header. Verified head of file:

```
#description: "HPO annotations for rare diseases [8574: OMIM; 47: DECIPHER; 4337 ORPHANET]"
#version: 2026-06-23
#tracker: https://github.com/obophenotype/human-phenotype-ontology/issues
#hpo-version: http://purl.obolibrary.org/obo/hp/releases/2026-06-23/hp.json
database_id	disease_name	qualifier	hpo_id	reference	evidence	onset	frequency	sex	modifier	aspect	biocuration
OMIM:619340	Developmental and epileptic encephalopathy 96		HP:0011097	PMID:31675180	PCS		1/2			P	HPO:probinson[2021-06-21]
```

**Exactly 12 columns:**

| # | Column | Notes |
|---|---|---|
| 1 | `database_id` | **CURIE: `OMIM:`, `ORPHA:`, `DECIPHER:`** |
| 2 | `disease_name` | accepted name only |
| 3 | `qualifier` | `NOT` = phenotype explicitly excluded. **Filter this or you invert the meaning.** |
| 4 | `hpo_id` | `HP:NNNNNNN` |
| 5 | `reference` | `PMID:...`, `OMIM:...`, `ORPHA:...`, `http...` |
| 6 | `evidence` | `IEA` (electronic), `PCS` (published clinical study), `TAS` (traceable author statement), `ICE` (individual clinical experience) |
| 7 | `onset` | HPO term from the Onset subontology |
| 8 | `frequency` | **three mixed encodings**: ratio `1/2`, percentage `30%`, or HPO CURIE `HP:0040283`. Must handle all three. |
| 9 | `sex` | `MALE` / `FEMALE` |
| 10 | `modifier` | HPO term(s) under Clinical modifier, **`;`-separated** |
| 11 | `aspect` | `P` phenotypic abnormality · `I` inheritance · `C` onset & clinical course · `M` clinical modifier |
| 12 | `biocuration` | e.g. `HPO:probinson[2021-06-21]` |

**Verified counts:** **285,598 annotation rows** over **12,958 diseases** — **OMIM 169,427 rows**, **ORPHA 115,875 rows**, **DECIPHER 296 rows**.

> **Gotcha:** `aspect` is not optional metadata. Rows with `aspect=I` are *inheritance modes* (e.g. `HP:0000007 Autosomal recessive inheritance`), not clinical signs. Failing to filter on `aspect='P'` pollutes phenotype similarity scoring with inheritance terms. Likewise `ORPHA:` here is a **bare numeric ORPHAcode** — MONDO writes the same thing as `Orphanet:` (capital O, different string). Normalize before joining.

### Gene/disease annotation files — verified headers

**`genes_to_phenotype.txt`** (6 cols):
```
ncbi_gene_id	gene_symbol	hpo_id	hpo_name	frequency	disease_id
10	NAT2	HP:0000007	Autosomal recessive inheritance	-	OMIM:243400
```
`frequency` uses `-` for missing (not empty). `ncbi_gene_id` is a **bare integer**.

**`phenotype_to_genes.txt`** (5 cols):
```
hpo_id	hpo_name	ncbi_gene_id	gene_symbol	disease_id
HP:3000004	Abnormal frontalis muscle physiology	60482	SLC5A7	ORPHA:98914
```

**`genes_to_disease.txt`** (5 cols):
```
ncbi_gene_id	gene_symbol	association_type	disease_id	source
NCBIGene:64170	CARD9	MENDELIAN	OMIM:212050	ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/mim2gene_medgen
```
> **Inconsistency to watch:** here `ncbi_gene_id` is prefixed **`NCBIGene:64170`**, whereas in the other two files it is a bare `64170`. `association_type` ∈ `MENDELIAN`, `POLYGENIC`, `UNKNOWN`.

### HPO API

**Base: `https://ontology.jax.org/api/`** — **VERIFIED live, no auth, no key.**

- `https://ontology.jax.org/api/hp/terms/HP:0001250` — **VERIFIED 200**, returns `{id, name, definition, comment, descendantCount, synonyms, ...}`
- `https://ontology.jax.org/api/hp/search?q=seizure&limit=2` — **VERIFIED 200**
- `https://ontology.jax.org/api/network/annotation/HP:0001250` — **VERIFIED 200** (gene/disease annotations for a term)
- `https://ontology.jax.org/api/hp/terms/{id}/genes`, `/api/hp/diseases/{id}` — **UNVERIFIED 404** (not the right paths)
- **No OpenAPI spec published** — `/api/openapi.json`, `/openapi.json`, `/v3/api-docs` all 404. You must discover endpoints empirically. `hpo.jax.org`'s own JS bundle confirms `https://ontology.jax.org/` is the only backend it calls.

> **Gotcha:** the API host is **`ontology.jax.org`**, not `hpo.jax.org`. There is no API on `hpo.jax.org`.

### ⚠️ HPO License — a custom license, **not** CC BY

This is the item most often gotten wrong. The **2026-06-23 `hp.json`** declares, verified from its own metadata:

```
http://purl.org/dc/terms/license = https://hpo.jax.org/app/license
http://purl.org/dc/elements/1.1/rights = Peter Robinson, Sebastian Koehler,
    The Human Phenotype Ontology Consortium, and The Monarch Initiative
```

The **OBO Foundry registry** confirms HPO is the odd one out — where MONDO is `{'label': 'CC BY 4.0'}`, HPO is `{'label': 'hpo', 'url': 'https://hpo.jax.org/app/license'}`. **HPO is not CC BY 4.0.** (Some secondary sources claim it is, because the *journal articles* about HPO are CC BY. Those are not the data license.)

The license page's canonical URL is now **`https://hpo.jax.org/license`** (SPA route; server returns 404 but it renders). I retrieved the authoritative text from the site's own source, `TheJacksonLaboratory/hpo-web/main/src/app/static/resources/license/license.component.html` — **VERIFIED**:

> "The HPO vocabularies, annotation files, tools and documentation are freely available. The HPO is copyrighted to protect the integrity of the vocabularies... anyone can download the HPO and use the ontologies or other HPO files **under three conditions**:
> 1. That the Human Phenotype Ontology Consortium is **acknowledged and cited** properly.
> 2. That any HPO Consortium file(s) displayed publicly **include the date(s) and/or version number(s)** of the relevant HPO file(s).
> 3. That **neither the content of the HPO file(s) nor the logical relationships embedded within the HPO file(s) be altered in any way.** (Content additions and modifications have to be suggested using our issue tracker.)"

Plus a required attribution string: *"This service/product uses the Human Phenotype Ontology (version information). Find out more at http://www.human-phenotype-ontology.org"* — and they request the HPO logo be displayed.

**Commercial use is permitted** (no for-profit carve-out, unlike OMIM), **but condition 3 is a real engineering constraint**: you may not ship an altered HPO or altered HPO logical relationships. Deriving, filtering, or extending in your own namespace is fine; redistributing something you call HPO with modified `is_a` edges is not. Surface the version string (`2026-06-23`) wherever HPO-derived output is displayed to satisfy condition 2.

---

## Cross-cutting notes for the pipeline

**ID normalization is the top source of silent bugs.** The same disease appears as: `OMIM:154700` · `ORPHA:558` (HPO's spelling) · `Orphanet:558` (MONDO's spelling) · `GARD:0016535` (new) vs `6975` (legacy) · `MONDO:0007947` · `UMLS:C0024796` · `MEDGEN:44287` · `DOID:14323`. **Make MONDO the hub** and normalize everything into `MONDO:` on ingest.

**Recommended license-clean stack for a commercial repurposing pipeline:**
- **MONDO** (CC BY 4.0) — disease identity + the full crosswalk, including 10,176 OMIM IDs and 15,947 GARD IDs *without* touching OMIM's copyrighted content
- **HPO** (custom, commercial-OK with attribution + no-modification) — phenotypes and `phenotype.hpoa`
- **Monarch KG** (BSD-3 code, CC BY data, per-source provenance in `metadata.yaml`) — the integrated graph, plus free semsim/annotate APIs with no key
- **GARD CSV** (US public domain) — only if you need GARD display names; otherwise take GARD IDs from MONDO
- **OMIM** — **quarantine until a JHU license is signed.** MIM *numbers* flowing through MONDO/HPOA are identifiers, not OMIM content; downloading `genemap2.txt`/`morbidmap.txt` or calling `api.omim.org` is what triggers the commercial-license requirement (with a stated double-fee penalty for unlicensed access, and a weekly-refresh obligation once licensed).

**Refresh cadences to encode:** MONDO monthly (regular, has diff files) · Monarch KG ~monthly (irregular) · HPO every 1–3 months (irregular) · GARD ad-hoc with an unstable URL · OMIM nightly but weekly-refresh is contractually mandatory if licensed.

**Two dead URLs still circulating in docs and code:** `hpo.jax.org/data/{ontology,annotations}` (404 — site restructured) and MONDO's SSSOM `curie_map` expansion of GARD to `rarediseases.info.nih.gov/diseases/` (produces 404s — the live pattern is `?gard_id=`).