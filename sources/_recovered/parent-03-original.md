<!-- RECOVERED from subagent transcript agent-a10c11ad412d23e0d.jsonl, session fd64561f-7c90-41a2-95cf-b4a133a8fe0f, research date 2026-08-05.
     Provenance copy: verbatim parent output that became 03-disease-prevalence-patients.md.
     Verbatim agent deliverable — not re-edited. -->

# Rare Disease Prevalence, Ontology & Patient-Finding — Source Reference

*Verified 2026-08-05. **VERIFIED** = URL fetched and content inspected. **UNVERIFIED** = referenced but not confirmed (404, bot-blocked, or secondary source only).*

---

## 0. Architecture decision before anything else

Three facts should drive the whole pipeline design:

1. **MONDO is your hub ID, not ICD and not OMIM.** It is CC BY 4.0, monthly, has diff files, and carries 10,176 OMIM + 10,491 Orphanet + 15,947 GARD + 21,660 UMLS/MedGen xrefs.
2. **Only 1,053 of 11,645 Orphanet disorders (9%) have their own ICD-10 code.** 6,768 carry a code Orphanet invented because ICD-10 had nothing. Claims databases are ICD-10-only. This single fact decides which RWD platform is worth buying.
3. **OMIM requires a paid JHU license for a for-profit building a derivative database.** Quarantine it until signed; use MONDO + HPO as the license-clean substitute.

---

## 1. Orphanet / Orphadata — the prevalence source

### 1.1 Hosts, and the one that matters

| Host | Status | Note |
|---|---|---|
| `https://www.orphadata.com/` | **VERIFIED** | Bulk file host. **Scrapable.** |
| `https://sciences.orphadata.com/` | **VERIFIED** | Product documentation pages |
| `https://api.orphadata.com/` | **VERIFIED** | **Free, unauthenticated JSON API** |
| `https://www.orphacode.org/` | **VERIFIED** | Nomenclature Pack (coding/implementation) |
| `https://api.orphacode.org/` | **VERIFIED** — returns **401** | Requires API key |
| `http://www.orphadata.org/...` | **VERIFIED** | Legacy host still serves files |
| `https://www.orpha.net/` | ⚠️ **BOT-WALLED** | Serves a JS proof-of-work challenge ("Vérification de la connexion…", `haphash`). **Do not put orpha.net in a pipeline.** All legacy `orpha.net/pdfs/orphacom/cahiers/...` Report Series PDFs now return this 5,349-byte HTML shim instead of a PDF. |

### 1.2 Bulk XML products — all VERIFIED by download

Pattern: `https://www.orphadata.com/data/xml/{lang}_{product}.xml` — langs `en, fr, de, nl, it, es, pt, pl, cs` (+ `tr, uk, zh` on some products). Diffs at `/data/diff/{file}.diff`.

| File | Size | Content | Release date in file |
|---|---|---|---|
| `en_product1.xml` | 54.0 MB | **Cross-references / alignments** — 11,645 disorders | 2026-06-23 |
| `en_product3_{hchid}.xml` | 9 KB–15.7 MB | **Classifications**, one file per hierarchy (34 of them) | 2026-06-23 |
| `en_product4.xml` | 47.9 MB | **Phenotypes** (HPO annotations) — 4,357 disorders, 116,664 annotations | 2026-06-23 |
| `en_product6.xml` | 22.6 MB | **Genes** | 2026-06-23 |
| `en_product7.xml` | 12.8 MB | **Linearisation** — 10,101 entries, preferential parent | 2026-06-23 |
| `en_product9_prev.xml` | 16.2 MB | **⭐ Epidemiology / prevalence** — 6,728 disorders, 17,108 records | 2026-06-23 |
| `en_product9_ages.xml` | 6.9 MB | **Natural history** — 7,790 disorders | 2026-06-23 |
| `en_funct_consequences.xml` | 18.6 MB | Disability / functional consequences | 2026-06-23 |

Licence declared **inside every file**: `CC-BY-4.0`. Commercial use permitted with attribution. Releases **bi-annual, July and December**. Historical versions since April 2020 on GitHub; aggregated flat versions at `https://github.com/Orphanet/Orphadata_aggregated`. Data description PDF: `https://www.orphadata.com/docs/OrphadataScienceDataDescription.pdf` (**VERIFIED**, 1.0 MB, V3 April 2026).

> ⚠️ **JSON bulk files do not exist at the documented paths.** `/data/JSON/en_product9_prev.json` and `/data/json/...` both **404**. The docs claim JSON; only `{lang}_product1.json.tar.gz` appears to exist. **Use XML for bulk, the API for JSON.**

### 1.3 `en_product9_prev.xml` — the prevalence file, field by field

```xml
<Disorder id="17601">
  <OrphaCode>166024</OrphaCode>
  <Name lang="en">…</Name>
  <DisorderType id="21394"><Name>Disease</Name></DisorderType>
  <DisorderGroup id="36547"><Name>Disorder</Name></DisorderGroup>
  <PrevalenceList count="2">
    <Prevalence id="8323">
      <Source>ORPHANET_11389160[PMID]_9689990[PMID]</Source>
      <PrevalenceType id="23669"><Name>Point prevalence</Name></PrevalenceType>
      <PrevalenceQualification id="23704"><Name>Class only</Name></PrevalenceQualification>
      <PrevalenceClass id="23760"><Name>&lt;1 / 1 000 000</Name></PrevalenceClass>
      <ValMoy>0.0</ValMoy>
      <PrevalenceGeographic id="23844"><Name>Worldwide</Name></PrevalenceGeographic>
      <PrevalenceValidationStatus id="25958"><Name>Validated</Name></PrevalenceValidationStatus>
    </Prevalence>
  </PrevalenceList>
</Disorder>
```

**Controlled vocabularies — measured from the live file (17,108 records):**

| `PrevalenceType` | n | | `PrevalenceQualification` | n |
|---|---|---|---|---|
| Point prevalence | 8,304 | | Value and class | 7,131 |
| Cases/families | 3,619 | | Class only | 6,358 |
| Annual incidence | 3,068 | | Case(s) | 3,251 |
| Prevalence at birth | 2,070 | | Family(ies) | 368 |
| Lifetime Prevalence | 47 | | | |

| `PrevalenceClass` | n | → US count range @ 341.8M |
|---|---|---|
| `<1 / 1 000 000` | 4,998 | 0 – 342 |
| *(empty)* | 3,624 | — |
| `1-9 / 100 000` | 2,835 | 3,418 – 30,761 |
| `1-9 / 1 000 000` | 2,232 | 342 – 3,076 |
| **`Unknown`** | **1,999** | **unusable** |
| `1-5 / 10 000` | 1,204 | 34,178 – 170,892 |
| `6-9 / 10 000` | 113 | 205,071 – 307,606 |
| `>1 / 1000` | 97 | 341,785+ |
| `Not yet documented` | 6 | unusable |

`PrevalenceValidationStatus`: Validated 15,232 / Not yet validated 1,873.
`PrevalenceGeographic`: **140 distinct values.** Worldwide 9,518 · Europe 1,675 · **United States 449** · United Kingdom 362 · France 274 · Italy 261 · … · `Specific population` 105.

**Critical semantics:**
- `ValMoy` is **per 100,000**, and is only meaningful when `PrevalenceQualification = "Value and class"`. Otherwise it is `0.0` — a sentinel, not a zero prevalence.
- `Source` embeds `NNNNNNNN[PMID]` tokens joined by `_`, plus `[EXPERT]` and `ORPHANET`. **This is your bridge from a prevalence figure to the underlying paper, its authors, and their institutions** — a free lead into site-finding.
- `Cases/families` + `Case(s)` records are literal published case counts (`ValMoy=4.0` = four reported cases). For ultra-rare diseases this is often the only number that exists, and it is a *literature* count, not a patient count.

### 1.4 ⚠️ How much of this is actually usable — measured

Of 6,728 disorders in the prevalence file:

| Outcome | n | % |
|---|---|---|
| Class-bounds only (a **5–10× wide** range) | 3,881 | **57.7%** |
| Point prevalence present but class = `Unknown` | 1,780 | 26.5% |
| **Usable numeric point prevalence** | **878** | **13.0%** |
| No point prevalence at all | 189 | 2.8% |

**Only 138 disorders (2.1%) have a US-specific point-prevalence record.** Plan for the 87% case, not the 13% case.

### 1.5 `en_product9_ages.xml` — natural history (the pediatric test)

Contains **only** `AverageAgeOfOnsetList` and `TypeOfInheritanceList`. **`AverageAgeOfDeath` is empty in the current release** — the tag does not appear at all. Do not build a survival model on this file.

`AverageAgeOfOnset` vocabulary (7,790 disorders): Neonatal 3,192 · Infancy 2,693 · Childhood 1,724 · Adult 1,572 · Antenatal 973 · All ages 873 · Adolescent 870 · Elderly 365 · No data 50.

`TypeOfInheritance`: Autosomal recessive 2,690 · Not applicable 2,026 · Autosomal dominant 2,017 · Unknown 432 · X-linked recessive 394 · Multigenic 210 · X-linked dominant 110 · Mitochondrial 40 · Semi-dominant 5 · Y-linked 4 · Oligogenic 4.

> **For the FDA "primarily affects 0–18" screen:** onset ∈ {Antenatal, Neonatal, Infancy, Childhood, Adolescent} with **no** Adult/Elderly value is a good first-pass filter, but it is onset, not age *distribution*. FDA wants >50% of the affected US population aged 0–18, which requires survival. See §8.

### 1.6 `en_product1.xml` — cross-references

11,645 disorders, 52,456 external references:

| Source | n | | Source | n |
|---|---|---|---|---|
| MONDO | 9,979 | | ICD-11 | 6,868 |
| UMLS | 9,586 | | GARD | 3,825 |
| OMIM | 8,745 | | MeSH | 3,209 |
| ICD-10 | 8,450 | | MedDRA | 1,794 |

`DisorderMappingRelation`: **E** exact 34,278 · **NTBT** (ORPHA narrower than target) 12,994 · **BTNT** (ORPHA broader) 5,144 · **ND** 40.

`DisorderMappingICDRelation` — **this is the field that tells you whether an ICD code is real**:

| | ICD-10 | ICD-11 |
|---|---|---|
| **Specific code** (own code) | **1,053** | **1,697** |
| Index term (index / Foundation only) | 187 | 3,592 |
| Inclusion term | 442 | 0 |
| **Attributed code** (Orphanet invented it) | **6,768** | **1,579** |

`DisorderMappingICDRefUri` carries the **ICD-11 Foundation ID** — your direct join key into the WHO ICD API. `DisorderMappingICDRefUrl` gives the browser URL.

> **Traps:** ~⅓ of mappings are `Not yet validated`. `DisorderDisorderAssociation` entries of type "Moved to"/"Referred to" mark deprecated ORPHAcodes — follow them forward or you'll silently drop diseases.

### 1.7 Orphadata REST API — free, no key, 32 endpoints

Base `https://api.orphadata.com`. **OpenAPI 3.1 spec: `https://api.orphadata.com/openapi.json`** (**VERIFIED**, 84 KB, title "Orphadata APIs"). No `securitySchemes`, no auth. Every response embeds the CC-BY-4.0 licence object and the source file's extraction date.

```
/rd-cross-referencing/orphacodes/{orphacode}      /rd-cross-referencing/orphacodes/names/{name}
/rd-cross-referencing/icd-10s/{icd}               /rd-cross-referencing/icd-11s/{icd}
/rd-cross-referencing/omims/{omim}                /rd-epidemiology/orphacodes/{orphacode}
/rd-natural_history/orphacodes/{orphacode}        /rd-phenotypes/orphacodes/{orphacode}
/rd-phenotypes/hpoids/{hpoids}                    /rd-associated-genes/genes/symbols/{symbol}
/rd-classification/hchids                         /rd-classification/hchids/{hchid}/orphacodes
/rd-classification/orphacodes/{orphacode}/hchids  /rd-medical-specialties/orphacodes/{orphacode}
```
All take `?lang=en`. Each family also has a bare `/orphacodes` listing endpoint (enumerate everything).

> ⚠️ **Two gotchas.** (1) The natural-history path uses an **underscore**: `/rd-natural_history/`, not `-natural-history-`. Everything else uses hyphens. (2) There is **no `/docs` or `/swagger`** — both 404. The spec is only at `/openapi.json`.

**34 classifications** (`/rd-classification/hchids`), e.g. `150` rare inborn errors of metabolism, `156` rare genetic diseases, `181` rare neurological diseases, `199` rare bone diseases, `231` rare systemic and rheumatological diseases **of childhood**, `202` rare neoplastic diseases.

### 1.8 Orphanet Nomenclature Pack — best single artifact for a coding pipeline

`https://www.orphacode.org/data/packs/Orphanet_Nomenclature_Pack_EN.zip` — **VERIFIED**, 8.5 MB. Also `_CS _NL _FR _DE _IT _ES _PL _PT`. **CC BY 4.0, updated annually in July.**

Contents (**VERIFIED** by extraction):
```
ORPHAnomenclature_en_2026.xml            ORPHA_ICD10_mapping_en_2026.xml
ORPHAnomenclature_MasterFile_en_2026.xlsx  (sheets: ICD10, ICD11)
ORPHAnomenclature_diff_en_2026.xlsx      ORPHA_ICD11_mapping_en_2026.xml
ORPHAlinearisation_en_2026.xml           ORPHA_OMIM_mapping_en_2026.xml
List_of_rare_diseases_en_2026.xlsx       OrphanetNomenclaturePackDescription.pdf
  sheets: Read_me | List_active_alphabethical_order
        | List_active_by_ORPHAcode | List_deprecated_obsoleted   ← ⭐ retired-code handling
Classifications/ORPHAclassification_{hchid}_{slug}_en_2026.xml   (34 files)
```
The **`List_deprecated_obsoleted` sheet and `ORPHAnomenclature_diff`** are what you need to keep a pipeline from silently rotting across releases.

### 1.9 ORDO ontology

`https://www.orphadata.com/data/ontologies/ordo/last_version/ORDO_en_4.9.owl` — **VERIFIED**, 52.5 MB, **v4.9 released 1 July 2026**. Also `_fr _de _es _cs _nl _it _pl _pt`. Previous versions under `/previous_versions/` back to v1.0 (Jan 2014). Mirrors: BioPortal `ontologies/ORDO`, EBI OLS `ebi.ac.uk/ols4/ontologies/ordo` (**VERIFIED**). SPARQL: `https://www.orphadata.com/ordo-sparql-endpoint`, HOOM (HPO-ORDO module) at `/hoom-sparql-endpoint`. FAIR data point: `http://fairdatapoint.orphadata.com`.

> ⚠️ `http://purl.obolibrary.org/obo/ordo.owl` **404s** — ORDO is not an OBO PURL.

### 1.10 Orphanet Expert Resources — ⚠️ NOT free

Centres of expertise, diagnostic labs, patient organisations, research projects, clinical trials, registries, biobanks, orphan drugs. `https://www.orphadata.com/expert-resources/` (**VERIFIED**).

**Academia/public: Data Transfer Agreement minimum. For-profit: a specific paid contract with Orphanet-AISBL** (`https://www.orphanet-aisbl.com`). Coverage is Europe-centric. This is the one Orphanet product that is not CC BY, and it is exactly the patient-finding piece — budget for it or substitute ClinicalTrials.gov + ERN directories (§9).

### 1.11 Phenotypes (`en_product4.xml`)

4,357 disorders, 116,664 HPO annotations. `HPOFrequency` vocabulary: Occasional (29-5%) 43,064 · Frequent (79-30%) 39,975 · Very frequent (99-80%) 25,662 · Very rare (<4-1%) 6,602 · Excluded (0%) 733 · Obligate (100%) 628. Each association carries `HPOId`, `HPOTerm`, `HPOFrequency`, `DiagnosticCriteria`.

---

## 2. GARD (NCATS)

| URL | Status |
|---|---|
| `https://rarediseases.info.nih.gov/` | **VERIFIED** — current canonical home |
| `https://ncats.nih.gov/gard` | **VERIFIED** 301 → `/research/research-resources/gard` |
| `https://rarediseases.info.nih.gov/?gard_id=0005528` | **VERIFIED** — current per-disease URL pattern |
| `https://rarediseases.info.nih.gov/diseases/6975/marfan-syndrome` | **404 — legacy path, dead** |
| `https://rdas.ncats.nih.gov/` | **VERIFIED** — Rare Disease Alert System (separate product) |

**The only bulk download** — a Salesforce content link published on `/about`, **VERIFIED** at 3,638,571 bytes / 16,214 diseases, served as `GARD Rare Disease List Jun2026.csv`:

```
https://ncats.file.force.com/sfc/dist/version/download/?oid=00Dt00000004XG2&ids=068SJ00001HZAaEYAX&d=%2Fa%2FSJ00000BC4Xl%2FUj7U9WuHII571Akz5AUBLe6WSCeelaMBynbjWybmhuA&asPdf=false
```

Four columns, UTF-8 **with BOM**: `ID,DisplayName,Synonyms,URL`. Synonyms are **pipe-delimited and lowercased**; `URL` is frequently empty.

> ⚠️ **The `ids=` token is bound to the June 2026 file. There is no `latest` alias.** Re-scrape `rarediseases.info.nih.gov/about` for the current link on every run.

**Negative findings (all confirmed):** no GARD REST API · no `ncats/gard-data` GitHub repo (only `epi4GARD` and `RD-Clust`, which are research code) · not on data.gov or healthdata.gov (CKAN API queried) · not in the NCATS Translator SmartAPI registry (`smart-api.info/api/query?q=GARD` → `total:0`).

**ID system:** `GARD:NNNNNNN`, 7-digit zero-padded. The legacy scheme was a short unpadded integer. **MONDO's SSSOM curie_map still expands GARD to the dead `/diseases/` prefix** — build your own resolver against `?gard_id=`.

Licence: US federal work, public domain (17 U.S.C. §105), but **no explicit licence statement is published**. Cadence irregular, versioned by month in the filename only.

**Recommendation: don't build on GARD.** Take GARD IDs from MONDO, which carries 15,947 of them (98% coverage) already crosswalked.

---

## 3. OMIM — ⚠️ commercial licence required

`omim.org` **returns 403 to curl and WebFetch** (bot protection). Content below verified through an alternate fetcher; `api.omim.org` confirmed live.

### The licensing blocker, quoted

From `https://www.omim.org/downloads/` and `https://www.omim.org/api`:

> "**For-profit companies or anyone planning to redisplay or incorporate OMIM data into software MUST secure a license.**"

Click-through declaration on both forms:

> "…I will not use or share the data contained in OMIM for any commercial purposes, **will not develop a derivative database**, nor distribute the data to a third party without first obtaining a license from Johns Hopkins University."

From `https://www.omim.org/help/agreement`:

> "Users at for-profit or commercial entities who want to download all or part of OMIM **must obtain a license by paying applicable licensing fees**… if you access OMIM without a license, you agree to payment of **penalties of double the standard license**."
> "If OMIM data are downloaded… and used in a database or analysis software, **the data must be refreshed at least weekly**."

The agreement explicitly covers "the OMIM.org API, **or** downloads" — **the API is not a loophole**. Registration rejects free-mail domains. Commercial licensing: **`JHTV-OMIM@jhmi.edu`**.

A repurposing pipeline *is* a derivative database. **Quarantine OMIM until licensed.**

### Downloads (`https://www.omim.org/downloads/`)

| File | Access | Content |
|---|---|---|
| `mim2gene.txt` | **No registration** | MIM ↔ NCBI Gene ID ↔ Ensembl ↔ HGNC symbol — an ID crosswalk, deliberately free |
| `mimTitles.txt` | Registration | MIM numbers + titles |
| `genemap2.txt` | Registration | Gene map synopsis + coordinates + inheritance |
| `morbidmap.txt` | Registration | Same, sorted by disorder |

Updated **nightly**. After approval you get **personalized URLs** — there are no stable public paths.

### API (`https://api.omim.org`, docs `https://www.omim.org/help/api`)

Confirmed live: an unauthenticated call returns `BadRequestException: An API key is required…`.

- Handlers: `entry`, `clinicalSynopsis`, `geneMap`, `search`, `status`, `apiKey`
- Auth: header `ApiKey: <key>` / cookie `ApiKey=<key>` / query `?apiKey=<key>` — **parameter name is case-sensitive**
- **Key must be renewed yearly.** GET only (except `apiKey`). `format=json|xml`. gzip via `Accept-Encoding`.
- Limits: `entry`/`clinicalSynopsis` **20 per request when any `include` is set**; `geneMap` **100**. Paginate with `start`/`limit`. **429 = undocumented daily quota exceeded.**
- Repurposing-relevant text sections: `include=text:clinicalManagement`, `text:geneTherapy`.

**MIM prefixes:** `*` gene · `#` phenotype, known molecular basis (what you want) · `+` gene+phenotype (legacy) · `%` Mendelian, unknown basis · *(none)* unclear · `^` moved/removed. **`OMIMPS:` (Phenotypic Series) is a separate namespace** — do not conflate with `OMIM:`.

---

## 4. Monarch Initiative + MONDO

### 4.1 Monarch API — free, no key

`https://api.monarchinitiative.org/v3/docs` (**VERIFIED**, FastAPI Swagger). **Spec is at the root: `https://api.monarchinitiative.org/openapi.json`** (**VERIFIED**, OpenAPI 3.1, 55 schemas). `/v3/openapi.json` **404s**. Paths inside the spec are prefixed `/v3/api/…` — don't double-prefix when codegen'ing.

```
/v3/api/entity/{id}          /v3/api/search        /v3/api/autocomplete
/v3/api/association          /v3/api/mappings      ← SSSOM crosswalk
/v3/api/semsim/compare       /v3/api/semsim/search/{termset}/{group}
/v3/api/annotate             /v3/api/ground        ← free text → HPO/MONDO
/v3/api/histopheno/{id}      /v3/api/releases      /v3/api/sources/versions
/v3/api/entity/{id}/disease-phenotype-grid   …and ~15 more
```

`GET /v3/api/entity/MONDO:0007947` returns Marfan syndrome with `xref: ["DOID:14323","GARD:0016535","ICD10CM:Q87.4","MEDGEN:44287","MESH:D008382",…]`.

The `semsim/*` (phenotype semantic similarity) and `annotate`/`ground` endpoints give you Resnik/Phenodigm-grade phenotype→disease ranking **for free, with no key** — the highest-leverage free API in this whole reference.

### 4.2 Monarch KG bulk

`https://data.monarchinitiative.org/monarch-kg/latest/` (**VERIFIED**). Current release **2026-07-14**, biolink 4.4.2. **1,582,279 nodes / 15,807,241 edges** (from `qc_report.yaml`).

Artifacts: `monarch-kg.tar.gz` (KGX TSV) · `.jsonl.tar.gz` · **`.duckdb`** · `.db.gz` (SQLite) · `.neo4j.dump` / `.neo4j.v5.dump` · neo4j-admin CSVs · `.nt.gz` (RDF) · `solr.tar.gz` · **`phenio.db.gz`** (merged phenotype/disease ontology, powers semsim) · `metadata.yaml` (sha256 per artifact + full upstream provenance — **keep this for licence compliance**).

> ⚠️ `qc_report.yaml` reports **2,951,148 dangling edges (~19%)** and 10,497 duplicate nodes. Filter on load.
> ⚠️ Cadence is **irregular** (two releases in April 2026; a two-month gap in late 2025). Pin via `/v3/api/releases`.
> ⚠️ Use `monarch-kg/latest/`, **not** `monarch-kg-dev/latest/` (which the ingest README still points at).

Federates: Alliance of Genome Resources, BGee, BioGrid, GO, HGNC, **HPOA**, NCBI Gene, Panther, **PHENIO** (bundles MONDO + HPO + ORDO + MP/ZP/upheno), PomBase, Reactome, STRING, ZFIN. **OMIM text and ClinVar are not ingested** — deliberately, which is why Monarch is redistributable where OMIM is not. Code BSD-3; data CC BY 4.0 per-source (`monarchinitiative.org/about/licensing` **404s** — there is no single licence page).

### 4.3 MONDO — ⭐ the crosswalk

All PURLs **VERIFIED** (302 → GitHub release assets):

| URL | Size |
|---|---|
| `https://purl.obolibrary.org/obo/mondo.owl` | 254.1 MB |
| `https://purl.obolibrary.org/obo/mondo.json` | 107.5 MB |
| `https://purl.obolibrary.org/obo/mondo.obo` | 53.1 MB |

Current release **v2026-08-04**. Cadence **monthly, first-Monday-ish** — far more regular than HPO. **63,267 terms.**

**Release assets worth knowing:**
- **`mondo-rare.owl/.obo/.json` + `mondo-rare_nodes.tsv` (15.4 MB) / `mondo-rare_edges.tsv`** — rare-disease-only subset, **start here**
- `mondo_nodes.tsv` / `mondo_edges.tsv` — flat TSV, no OWL tooling
- **`mondo_release_diff_new_terms.tsv` / `..._changed_terms.tsv`** — incremental deltas for refresh
- `mondo_obsoletioncandidates.tsv`, `mondo-clingen`, `mondo-base`, `mondo-simple`

**Xref coverage measured from `mondo.obo`:** UMLS 21,660 · MEDGEN 21,660 · **GARD 15,947** · DOID 12,091 · **Orphanet 10,491** · **OMIM 10,176** · SNOMED 9,157 · MeSH 8,211 · NCIT 7,434 · ICD9 5,658 · icd11.foundation 4,637 · EFO 2,400 · ICD10CM 2,142 · MedDRA 1,488 · NORD 911 · OMIMPS 621.

**SSSOM file** (**VERIFIED**, 13.1 MB, 109,707 mappings, 109,618 `skos:exactMatch`):
```
https://raw.githubusercontent.com/monarch-initiative/mondo/master/src/ontology/mappings/mondo.sssom.tsv
```
> ⚠️ The release-asset path `releases/latest/download/mondo.sssom.tsv` **404s**. Only `raw.githubusercontent.com` works.
> ⚠️ **The SSSOM file omits GARD entirely** despite `mondo.obo` carrying 15,947 GARD xrefs. For GARD, parse the OBO/JSON xrefs directly.
> ⚠️ In `mondo.obo`, xrefs carry provenance qualifiers: `{source="MONDO:equivalentTo"}` vs `{source="MONDO:i2s"}` vs `{source="Orphanet:558/btnt"}`. **Only `MONDO:equivalentTo` is true 1:1.** Filtering on this is mandatory or you will silently merge distinct diseases. There is also a `gard_rare` subset tag (15,948 uses).

**Licence: CC BY 4.0** (confirmed from the OBO Foundry registry JSON-LD). Commercial use permitted with attribution. **This is what makes MONDO the OMIM-safe substitute.**

---

## 5. HPO (Human Phenotype Ontology)

### Downloads — all VERIFIED by download

| URL | Size |
|---|---|
| `https://purl.obolibrary.org/obo/hp.obo` | 11.2 MB |
| `https://purl.obolibrary.org/obo/hp.json` | 23.0 MB |
| `https://purl.obolibrary.org/obo/hp/hpoa/phenotype.hpoa` | 35.7 MB |
| `https://github.com/obophenotype/human-phenotype-ontology/releases/latest/download/genes_to_phenotype.txt` | 20.7 MB |
| `…/releases/latest/download/phenotype_to_genes.txt` | 66.9 MB |
| `…/releases/latest/download/genes_to_disease.txt` | 1.5 MB |

Current release **2026-06-23**, 20,464 terms.

> ⚠️ **`hpo.jax.org/data/ontology` and `/data/annotations` are gone (404).** `hpo.jax.org` is now an Angular SPA whose only real server routes are `/`, `/app`, `/browse` — everything else returns 404 while still serving a 60,203-byte SPA shell. **Fetch from `purl.obolibrary.org` or GitHub releases, never `hpo.jax.org`.**
> ⚠️ Cadence is **irregular, 1–3 months** (4-month gap Feb→Jun 2026; 17 days Jun 6→Jun 23). Poll the GitHub releases API; don't assume a schedule.

### `phenotype.hpoa` — 12 columns, tab-separated

Header comment: `#description: "HPO annotations for rare diseases [8574: OMIM; 47: DECIPHER; 4337 ORPHANET]"`

```
database_id  disease_name  qualifier  hpo_id  reference  evidence
onset  frequency  sex  modifier  aspect  biocuration
```

**285,598 rows / 12,958 diseases** — OMIM 169,427 · ORPHA 115,875 · DECIPHER 296.

- `qualifier` = `NOT` means the phenotype is **explicitly excluded**. Filter it or you invert the meaning.
- `evidence`: `IEA` · `PCS` (published clinical study) · `TAS` · `ICE`
- **`frequency` has three mixed encodings** in one column: ratio `1/2`, percentage `30%`, or HPO CURIE `HP:0040283`. Handle all three.
- `modifier` is `;`-separated.
- **`aspect`: `P` phenotypic abnormality · `I` inheritance · `C` onset & clinical course · `M` modifier.** Rows with `aspect=I` are *inheritance modes*, not signs — **failing to filter `aspect='P'` pollutes every similarity score you compute.**
- `database_id` uses **`ORPHA:`** (bare numeric). MONDO writes the same thing as **`Orphanet:`**. Normalize before joining.

`genes_to_phenotype.txt` (6 cols, `-` for missing frequency, **bare integer** gene ID) · `phenotype_to_genes.txt` (5 cols) · `genes_to_disease.txt` (5 cols, `association_type` ∈ MENDELIAN/POLYGENIC/UNKNOWN — and here gene ID is prefixed **`NCBIGene:64170`**, inconsistent with the other two files).

### API — `https://ontology.jax.org/api/` (no auth)

- `GET /api/hp/terms/HP:0001250` — **VERIFIED** 200
- `GET /api/hp/search?q=seizure&limit=2` — **VERIFIED** 200
- `GET /api/network/annotation/HP:0001250` — **VERIFIED** 200 (gene/disease annotations)
- **No OpenAPI spec** — `/api/openapi.json`, `/openapi.json`, `/v3/api-docs` all 404. Discover empirically.

> ⚠️ **The API host is `ontology.jax.org`, not `hpo.jax.org`.** There is no API on `hpo.jax.org`.

### ⚠️ Licence — custom, NOT CC BY

`hp.json` declares `dcterms:license = https://hpo.jax.org/app/license`. The OBO Foundry registry lists HPO's licence as `{'label': 'hpo'}` where MONDO's is `{'label': 'CC BY 4.0'}`. **HPO is not CC BY 4.0** — sources that say otherwise are citing the *journal articles*, not the data licence.

Three binding conditions:
1. HPO Consortium acknowledged and cited
2. **Publicly displayed HPO files must include the date/version number**
3. **"Neither the content… nor the logical relationships embedded within… be altered in any way."**

Commercial use *is* permitted (no for-profit carve-out, unlike OMIM), but **condition 3 is a real engineering constraint**: you may derive, filter, and extend in your own namespace, but you may not redistribute something called HPO with modified `is_a` edges. Surface `2026-06-23` wherever HPO-derived output appears.

---

## 6. ICD-11, ICD-10-CM, and ORPHA↔ICD

### 6.1 ICD-11 (WHO)

- **Browser:** `https://icd.who.int/browse11` (**VERIFIED**, redirects). ⚠️ The `/browse11/l-m/en` structure is **retired**; current is `https://icd.who.int/browse/2025-01/mms/en`.
- **API:** base `https://id.who.int/`, docs `https://icd.who.int/docs/icd-api/APIDoc-Version2/` (**VERIFIED**, v2.6). Register at `https://icd.who.int/icdapi` (**VERIFIED**).
- **OAuth2 client-credentials, confirmed live:** POST to `https://icdaccessmanagement.who.int/connect/token` with `grant_type=client_credentials&scope=icdapi_access`; without creds returns `400 {"error":"invalid_client"}`. `https://id.who.int/icd/entity/257068234` returns **401** without a bearer token.
- Required headers: `API-Version: v2`, `Accept: application/json`, `Accept-Language`. ⚠️ Returned URIs use `http://` — rewrite to `https://` or eat a redirect per call.
- **Foundation vs MMS:** Foundation is the multi-parent superset with **no codes**; MMS is the coded linearization. **Most rare diseases exist only in the Foundation** (3,592 index-term-only vs 1,697 with MMS codes). Querying MMS alone loses them.
- **⭐ Local Docker — recommended.** No OAuth, no rate limits, reproducible version pinning:
  ```
  docker run -p 80:80 -e acceptLicense=true -e saveAnalytics=true whoicd/icd-api
  ```
  Image `whoicd/icd-api`, ARM supported, `include=2026-01_en` selects release/language, bundles Coding Tool at `/ct`. Set `saveAnalytics=false` to stop sending your searches to WHO.
- **Rare disease coverage:** WHO FAQ states ICD-11 includes **~5,500 rare diseases and synonyms**, distributed by system (no dedicated chapter). Orphanet chaired the Rare Diseases Topic Advisory Group; content is maintained "in conceptual identity with Orphanet." **WHO recommends using the URI, not the code**, to identify rare diseases individually.

### 6.2 ICD-10-CM (US)

**Best source — NCHS FTP** (CMS pages 403 to automation): `https://ftp.cdc.gov/pub/Health_Statistics/NCHS/Publications/ICD10CM/` (**VERIFIED**, years 2012→2027).

FY2027 set downloaded and parsed: **74,879 billable codes**. Files: `icd10cm-codes-2027.txt`, `icd10cm-order-2027.txt`, plus `-addenda-` variants (**235 change lines** in `Add:` / `Delete:` format — your FY-diff source).

> **35% of the code set is residual: 23,738 codes contain "unspecified", 2,324 "other specified".** This is where rare diseases go to disappear.

**Rare-disease-relevant ranges** (counts from the official FY2027 file): E75 (26 — Fabry E75.21, Gaucher E75.22, Krabbe E75.23, Niemann-Pick E75.240–244, MLD E75.25, Canavan E75.28, NCL/Batten E75.4) · E76 (12, MPS) · E77 (4) · E79 (7) · E80 (10, porphyrias) · E83 (31, Wilson/hemochromatosis) · **E88 (24; E88.4x mitochondrial = only 5 codes)** · G71 (28, muscular dystrophies) · G12 (11) · Q87 (21).

**⭐ FY2027 introduces gene-specific codes for the first time — a new "QA" block, 18 codes:** `QA00101` SCN2A-related neurodevelopmental disorder · `QA00102` CACNA1A · `QA00131` SLC6A1 · `QA00141` STXBP1 · `QA00142` DLG4 synaptopathy · `QA00151` FOXG1 syndrome · `QA171` Lynch · `QA1790/QA1791` BRCA1/2 · `QA1792` Li-Fraumeni. Other FY2027 additions: `D69.11` Glanzmann · `I42.01` familial DCM · `I42.81` arrhythmogenic cardiomyopathy · `I49.81` Brugada · `M04.3` VEXAS · `Q87.A` Loeys-Dietz.

**Cadence:** effective **October 1** each FY; April 1 mid-year updates exist.

**C&M Committee:** Spring (March) / Fall (September) meetings, ~30–60 day comment, Oct 1 implementation.
> ⚠️ **UNVERIFIED but important:** multiple secondary sources (Avalere, MedLearn) report NCHS **paused all ultra-rare and gene-specific code proposals at the March 2026 meeting until March 2027** while developing organizing principles for genetic conditions. `cdc.gov/nchs/icd/*` returns 403 to all automated fetchers, so this could not be confirmed on a primary source. The new QA chapter is consistent with the narrative. **Check in a browser before relying on it.**

### 6.3 ORPHA ↔ ICD mapping

> ⚠️ `www.orphadata.com/alignments/` is a **404**. Correct page: `https://sciences.orphadata.com/alignments/` (**VERIFIED**).

Use `en_product1.xml` (§1.6) or, for coding implementations, the dedicated Nomenclature Pack files `ORPHA_ICD10_mapping_en_2026.xml` / `ORPHA_ICD11_mapping_en_2026.xml` (§1.8) plus the `ORPHAnomenclature_MasterFile.xlsx` with `ICD10` and `ICD11` sheets. XSD: `http://www.orphadata.com/xsd-jpg/product1_en_cross_2024.xsd`.

EU implementation: browsers at `classifications.orphacode.org`, `mappings.orphacode.org`, `dataviz.orphacode.org`. Helpdesk: `github.com/OD4RD/Main-Help-Desk`.

---

## 7. ClinGen / ClinVar / MedGen

### 7.1 ClinGen — cleanest licensing of anything here

**Licence: CC0 1.0 Universal Public Domain Dedication** (**VERIFIED** at `https://www.clinicalgenome.org/docs/terms-of-use/`). Attribution requested, not required. Only restriction is the logo.

**Gene-disease validity CSV** — `https://search.clinicalgenome.org/kb/gene-validity/download` (**VERIFIED** by download, 1.1 MB, regenerated **daily**, header `FILE CREATED: 2026-08-05`):

> ⚠️ **6 junk preamble lines + `+++++` separator rows** — strip before parsing.

Columns: `GENE SYMBOL, GENE ID (HGNC), DISEASE LABEL, DISEASE ID (MONDO), MOI, SOP, CLASSIFICATION, ONLINE REPORT, CLASSIFICATION DATE, GCEP`

**3,656 records / 3,021 genes / 2,140 MONDO diseases.** Classification: Definitive 2,282 · Limited 546 · Moderate 454 · Disputed 197 · Strong 82 · No Known Disease Relationship 48 · Refuted 47. MOI: AR 1,835 · AD 1,472 · XL 207.

**Diseases are MONDO-identified, not ORPHA** — another reason MONDO is the hub.

Other files (**VERIFIED**): dosage `kb/gene-dosage/download` and `/downloadall` · haploinsufficiency/triplosensitivity BEDs at `ftp.clinicalgenome.org` · nightly archive `https://ftp.clinicalgenome.org/archive` (60-day retention) · actionability JSON `https://actionability.clinicalgenome.org/ac/{Adult|Pediatric}/api/summ?flavor=flat` · variant pathogenicity `https://erepo.clinicalgenome.org/evrepo/api/summary/classifications/download?type=csv`.

**Allele Registry** `https://reg.clinicalgenome.org/` (**VERIFIED**) — CAids, lookup by HGVS/dbSNP/ClinVar RCV/AlleleID/VariationID/HGNC. **Read requires no login.** Bulk at `/bulk_query/start`. No documented rate limits.

### 7.2 ClinVar

`https://ftp.ncbi.nlm.nih.gov/pub/clinvar/` (**VERIFIED**).

> ⚠️ **The FTP listing has two date columns — "Released" and "Last Modified."** The Released column shows stale dates (2021/2024) and will mislead your staleness checks. Last Modified on every key file was 2026-08-04/05 — files genuinely refresh **weekly**.

**`/tab_delimited/`** (sizes 2026-08-04): `variant_summary.txt.gz` 442 MB · `submission_summary.txt.gz` 386 MB · `hgvs4variation.txt.gz` 522 MB · `var_citations.txt` 230 MB · `cross_references.txt` 112 MB (**uncompressed**, despite what most docs imply) · `allele_gene.txt.gz` 92 MB · `variation_allele.txt.gz` 24 MB · `summary_of_conflicting_interpretations.txt` 1.79 GB. Every file has a `.md5`. `molecular_consequences.txt.gz` does **not** exist here.

**`variant_summary.txt.gz` — 43 columns**, header verified. **`PhenotypeIDS` carries MedGen CUIs and OMIM IDs** — that's your disease join. ⚠️ Rows are duplicated per assembly; filter on `Assembly`.

**⭐ `gene_condition_source_id`** — underrated, 1.2 MB, a ready-made gene→rare-disease crosswalk: `#GeneID, AssociatedGenes, RelatedGenes, ConceptID, DiseaseName, SourceName, SourceID, DiseaseMIM, LastUpdated`. `ConceptID` = MedGen CUI; `SourceName`/`SourceID` = MONDO/Orphanet/OMIM.

**VCF:** `/vcf_GRCh38/clinvar.vcf.gz` (184 MB) + `.tbi`, dated copies, `_papu` variants, `weekly/`.
**XML:** **`/xml/ClinVarVCVRelease_00-latest.xml.gz` (5.8 GB)**, monthly first Thursday, plus `weekly_release/` and `RCV_release/`. ⚠️ The old `ClinVarFullRelease` / `ClinVarVariationRelease` names are **gone**.

**E-utilities** (`db=clinvar`) — verified live. `esummary` returns `variation_xrefs` including `{"db_source":"ClinGen","db_id":"CA339901"}`, a free ClinVar→ClinGen Allele Registry join.

**Rate limits** (`https://www.ncbi.nlm.nih.gov/books/NBK25497/`): **3 req/sec without a key, 10 with.** Key from `https://account.ncbi.nlm.nih.gov/settings/`; pass `&api_key=`, and set `tool=` and `email=`. NCBI asks that large jobs run weekends or 21:00–05:00 ET.

### 7.3 MedGen

`https://ftp.ncbi.nlm.nih.gov/pub/medgen/` (**VERIFIED**). **Weekly, Wednesdays.** CUIs starting `C` are UMLS-derived; **`CN` prefixes are MedGen-minted** and won't resolve in UMLS.

**`MedGenIDMappings.txt.gz` (5.4 MB) — the crosswalk. Verified by parsing:**
> ⚠️ **Pipe-delimited (`|`), not tab. Every line has a trailing `|`** — naive splits yield a phantom 5th field.

Header `#CUI_or_CN_id|pref_name|source_id|source`. **421,816 rows.** Source distribution: MedGen 197,250 · SNOMEDCT_US 123,023 · **MONDO 23,304** · HPO 19,586 · GARD 16,846 · MeSH 16,502 · OMIM 10,249 · **Orphanet 9,026** · OMIM allelic variant 4,449 · OMIMPS 619.

Long format — one row per CUI-per-source; pivot on `CUI_or_CN_id`. **MedGen's Orphanet coverage (9,026) is much thinner than MONDO's (23,304)** — route ORPHA↔MedGen joins through MONDO, or use Orphanet's own product1.

**RRF files** (pipe-delimited; CSV mirrors in `/csv/`): `MGCONSO.RRF.gz` (names/synonyms per `SAB`) · `MGDEF.RRF.gz` (⚠️ **definitions embed `\r`** — line-based parsing breaks; use a real RRF parser) · `MGREL.RRF.gz` · `MGSTY.RRF.gz` (semantic types — filter Disease-or-Syndrome) · `MGSAT.RRF.gz` · **`NAMES.RRF.gz`** (there is no `names.txt`) · `MERGED.RRF.gz`.

Also: `MedGen_HPO_OMIM_Mapping.txt.gz`, `medgen_pubmed_lnk.txt.gz` (98 MB, `UID|CUI|NAME|PMID`), and **four history files essential for ID stability**: `MedGen_CUI_history.txt`, `MedGen_UID_CUI_history.txt`, `MONDO_CUI_history.txt`, `ORDO_CUI_history.txt`, `HPO_CUI_history.txt`.

---

## 8. Prevalence → US patient count

### 8.1 The FDA screen you're actually computing

**Rare pediatric disease** = (a) **serious or life-threatening**, (b) **primarily affects individuals aged 0 through 18** — FDA interprets this as **>50% of the affected US population aged 0–18** — and (c) fewer than 200,000 in the US (or the "no reasonable expectation of recovering costs" prong).

`https://www.fda.gov/industry/medical-products-rare-diseases-and-conditions/rare-pediatric-disease-designation-and-priority-review-voucher-programs` — **VERIFIED** (200 with a browser UA; WebFetch gets 404). Designation requests to **`orphan@fda.hhs.gov`**. Per FDA, as of Feb 3, 2026 (Consolidated Appropriations Act, 2026) **the RPD PRV program sunsets after September 30, 2029.**

Note criterion (b) is about the **prevalent age distribution**, not onset. A neonatal-onset disease with normal life expectancy fails it; a neonatal-onset disease with 5-year survival passes it decisively. This is why survival modeling is load-bearing, not optional.

### 8.2 Denominators

| Quantity | Value | Source |
|---|---|---|
| US resident population, 1 Jul 2025 | **341,784,857** | Census Vintage 2025 |
| US live births, 2024 final | **3,628,934** | NVSS *Births: Final Data for 2024*, NVSR 75-02 |
| US live births, 2025 provisional | **3,606,400** (−1%) | NVSS VSRR No. 43, Apr 2026, 99.95% of records |
| Planning number | **~3.6M births/yr**, trending −1%/yr | |

Access: Census API needs a free key (`https://api.census.gov/data/key_signup.html` — **VERIFIED**; unkeyed calls returned empty in testing). `census.gov` QuickFacts **403s** to automation. CDC WONDER Natality (`https://wonder.cdc.gov/natality.html`) exists but **403s to bots** and its POST/XML interface is brittle — prefer the **NCHS public-use natality micro-data files**. Unblocked mirrors of the NVSS reports: `https://www.ncbi.nlm.nih.gov/books/NBK622025/` (2025 provisional), `NBK623381` (2024 final). March of Dimes **PeriStats** (`https://www.marchofdimes.org/peristats`, **VERIFIED**) is the best free births-by-state/county source — parameterized URLs, scrapable, no API. ⚠️ **Use PeriStats for births only — its newborn screening content is years out of date.**

### 8.3 The canonical Orphanet-based method

Nguengang Wakap et al., *Eur J Hum Genet* 2020 — `https://pmc.ncbi.nlm.nih.gov/articles/PMC6974615/` (**VERIFIED**). Their rules, which you should copy:

- Numeric values → assign to the matching Orphanet class.
- **Class-only records → compute both a minimum and a maximum** (e.g. `1-9/100,000` → 1/100,000 and 9/100,000). For `<1/1,000,000`, set both bounds to 1/1,000,000.
- **Single cases/families → assume <1/1,000,000 individually**, but compute an aggregate indirect prevalence as (sum of all case/family reports) ÷ global population.
- **Exclude** rare cancers, infectious diseases, and acute/subacute poisonings (incidence-driven, not prevalence-driven). **Exclude birth prevalence and lifetime prevalence** from a point-prevalence rollup.
- Headline: 6,172 diseases; 3,585 analyzed (67.6% of those where prevalence applies); **cumulative 3.5–5.9%** = 263–446M globally; **69.9% exclusively pediatric onset**; 71.9% genetic.

### 8.4 The estimator, in order of defensibility

**Tier 1 — a US-specific point prevalence exists** (only 138 disorders, 2.1%). Take `ValMoy` where `PrevalenceQualification = "Value and class"` and `PrevalenceGeographic = "United States"`:
```
N_US = (ValMoy / 100,000) × 341,784,857
```
Worked, from the live file: **ORPHA:558 Marfan syndrome**, US point prevalence `ValMoy=10.0`, Validated → **34,178**.

**Tier 2 — Europe or Worldwide point prevalence, numeric.** Same formula, but flag the geographic transfer as an assumption. Adjust for known ancestry-specific founder effects.

**Tier 3 — class-only.** Emit a range, never a point estimate. `1-9/100,000` → **3,418–30,761**. A 9× range is honest; a midpoint is not.

**Tier 4 — birth prevalence only** (583 disorders). This is where the real work is. **Do not multiply birth prevalence by cumulative births.**

### 8.5 ⭐ The survival-weighted formula

```
P(t) = Σ   B(t−a) · p(t−a) · c(t−a) · S(a)
      a=0..A
```
- `P(t)` = prevalent US population alive at time *t*
- `B(t−a)` = US live births in the cohort's birth year
- `p(t−a)` = birth prevalence per live birth
- `c(t−a)` = **fraction of US births actually screened** for the condition that year (newborn-screened conditions only; see §11)
- `S(a)` = probability an affected individual survives from birth to age *a*

**Steady-state collapse** (roughly constant births and prevalence):
```
P ≈ B × p × ê          where ê = Σ S(a) = life expectancy at birth of affected individuals
                                        (the area under the survival curve)
```

**Worked, 1:100,000 birth prevalence, 3.6M births:**

| Treated life expectancy | Prevalent US patients |
|---|---|
| 25 years | 3.6M × 1e-5 × 25 = **900** |
| 5 years (untreated infantile MLD, Krabbe, Pompe) | **180** |

**A 5× swing driven entirely by the survival term.** For severe pediatric disease, omitting it inflates estimates 3–10×. It also *helps* your FDA case: short survival is precisely what makes >50% of the prevalent population aged 0–18.

### 8.6 The five corrections that separate a defensible number from a bad one

1. **Prevalent ≠ diagnosed.** For most rare diseases, diagnosed prevalence is 10–50% of true prevalence. Your recruitable pool is the diagnosed one.
2. **Screening coverage ramp.** For anything added to the RUSP post-2015, `c(a)` is well below 1.0 and rising. Full national adoption historically takes **7–9 years**.
3. **NBS-derived birth prevalence routinely exceeds pre-screening clinical estimates** because screening has low ascertainment bias and catches late-onset cases. Pompe is the canonical example. **Prefer NBS rates over carrier-frequency math** — benchmarking allele-frequency models against ~23M screened infants across 28 recessive disorders found agreement within 10× for only ~90% of disorders (`https://www.sciencedirect.com/science/article/pii/S0002929726001527`).
4. **Screen-positive ≠ diagnosed.** Always work from confirmed-case counts.
5. **Pre-screening vs screened cohorts are different populations** with different severity distributions. Be explicit about which you're recruiting.

### 8.7 Corroborating sources for a specific number

- **FDA orphan drug designation database** — `https://www.accessdata.fda.gov/scripts/opdlisting/oopd/` (**VERIFIED**, title "Search Orphan Drug Designations and Approvals", **exports to Excel**). Every designation contains a sponsor's US prevalence estimate that FDA already accepted. If a competitor has a designation in your disease, their number is your best defensible anchor.
- **PMIDs in the Orphanet `Source` field** — go read the primary study.
- **Claims-based studies** and NBS-derived rates (§11) — the two empirical alternatives to literature synthesis.

---

## 9. Patient-finding infrastructure

### 9.1 ⭐ ClinicalTrials.gov API v2 — the one thing to automate today

`https://clinicaltrials.gov/api/v2/studies` — **VERIFIED live. No key, no auth, full pagination, no rate-limit wall encountered.**

```
https://clinicaltrials.gov/api/v2/studies?query.cond=Pompe+disease
   &filter.overallStatus=RECRUITING&pageSize=50&countTotal=true
   &fields=NCTId,BriefTitle,LocationFacility,OverallOfficialName
```
Verified: `query.cond=Pompe disease` → `totalCount: 176`. Response gives `protocolSection.contactsLocationsModule.locations[]` (facility, city, country) and **`.overallOfficials[]` (named PIs with credentials)**, plus `nextPageToken`.

**The method:** enumerate every `LocationFacility` across every trial ever run in your disease → rank facilities by trial count → **that ranking is your patient-volume proxy**, and `overallOfficials` gives you the names to email.

### 9.2 Two more free PI-finding APIs — both verified live

- **NIH RePORTER** `POST https://api.reporter.nih.gov/v2/projects/search` — no key. Verified: `"Batten disease"` → 461 projects, returning `organization.org_name` and `principal_investigators[].full_name` (e.g. Michelle L Hastings / University of Michigan; Susan Lynn Cotman / MGH). **This finds the PIs who have money and mice but no trial yet** — often more receptive than a PI already running three industry studies.
- **PubMed E-utilities** `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=...&retmode=json` — no key needed at 3 req/sec. Verified: `Batten disease` → 3,195. Affiliation fields on recent case reports = the clinicians who currently have the patient.

### 9.3 NIH RDCRN — the highest-yield single channel

`https://www.rarediseasesnetwork.org/` · consortia directory `/consortia-directory` (**VERIFIED**) · registry `/registry` · DMCC `/data-management-and-coordinating-center` · data sharing `/data-sharing-resources`.

**19 consortia, 280+ diseases, 170+ patient advocacy partners. Cycle 5 began FY2025 (~$26M).** URL pattern `https://rdcrn.org/<slug>`.

| Consortium | Disease area |
|---|---|
| ACT | Syndromic craniosynostosis |
| ARDVARC | Vascular malformations |
| ARISEN | Autoimmune encephalitis, Rasmussen, NORSE |
| BDCRC | Neuronal ceroid lipofuscinoses (Batten) |
| BBDC | Osteogenesis imperfecta, bone disorders |
| CReATe | ALS and related |
| CPIC | Congenital CMV, neonatal HSV |
| CEGIR | Eosinophilic GI disorders |
| DSC | TSC, PTEN hamartoma, Phelan-McDermid |
| GLIA-CTN | Leukodystrophies |
| IMPACT | Thrombotic microangiopathies |
| MGNet | Myasthenia gravis |
| NASCARR | Sex chromosome aneuploidy |
| NAMDC | Mitochondrial diseases |
| PFN-STRIDE | Invasive fungal disease in immunocompromised children |
| PHEFREE | PKU, phenylalanine metabolism |
| RBDC | PCD, alpha-1 antitrypsin, humoral immunodeficiencies |
| ROAR (`roar.rarediseasesnetwork.org`) | PA, MMA, GA-1, IVA |
| SP-CERN | Hereditary spastic paraplegia |

**Every consortium site publishes its own clinical sites list and PI roster** — 19 pre-built, disease-indexed site maps.

**Contact Registry: 4,553 participants across 95 countries.** ⚠️ **A company cannot query or license it.** Access runs through a consortium investigator. Its significance is as proof that a consented, re-contactable pool exists — the PI is the key. Note the **87.6% White** skew; that's a diversity-plan problem for your FDA submission.

**DMCC:** Cincinnati Children's, co-PIs Maurizio Macaluso and Michael Wagner. Its **Clinical Research Core provides regulatory guidance, protocol review, and FDA submission support**. Contact **`support@rdcrn.org`**.

Data goes to the **RDCRN Data Repository** on NCATS servers (not primarily dbGaP); external access needs DAR + ethics training + IRB + DUA. Consent language explicitly permits sharing with "companies to make new medicines or products, which may generate profit" — **commercial use is contemplated, but there is no published industry partnership pathway.**

### 9.4 NORD

⚠️ **`rarediseases.org` returns 403 to plain HTTP (Cloudflare Bot Management).** You need a headless browser with a real UA.

| Resource | URL |
|---|---|
| **Member org list** | `https://rarediseases.org/nord-member-list/` |
| Patient org directory | `https://rarediseases.org/organizations/` |
| Rare Disease Database | `https://rarediseases.org/rare-diseases/` |
| Centers of Excellence | `https://rarediseases.org/center-of-excellence/` |
| IAMRARE registry | `https://rarediseases.org/advancing-research/iamrare-patient-registry-platform/` |

**`/nord-member-list/` is a flat, alphabetical, fully-rendered HTML list — the most scrapable asset NORD has.** Two tiers: **Platinum** (orgs with research infrastructure, registries, and a Medical Advisory Board — *your targets*) and **Gold** (support only). The Platinum/Gold split is the filter that matters.

**Rare Disease Database:** ~1,324 disease reports. **No API, no bulk export.** Each report's "Organizations" block maps disease → advocacy group.

**IAMRARE:** patient organizations launch registries; NORD provides platform + IRB + instruments. **You cannot buy access.** You sponsor or co-design a registry with the disease's patient org, which controls the data.

**Centers of Excellence:** launched Nov 2021, page states **46 centers across 28 states + DC**, 350+ volunteer clinicians (press releases suggest ~49 — **UNVERIFIED**). List and Map views with a state filter in the HTML, so the roster is extractable per-state. The network's stated goal to "Increase the Number of Multi-Site Clinical Trials" is an explicit invitation.

**Engagement:** the Corporate Council (`/corporate-council/`) is the formal paid door, but for a 20-patient trial the higher-yield path is **direct to the Platinum member org**. NORD's value is the directory, not the introduction.

### 9.5 Global Genes / RARE-X

Merger confirmed — RARE-X lives entirely under `globalgenes.org` paths. `/rare-x-for-researchers/` and `/rare-x-research-data-access/` both **VERIFIED**.

De-identified patient-level PROs, molecular/genomic, and structured study data organized into disease communities. **No participant count or disease count is published** — you must ask.

**Three tiers. Tier 3 is the one that matters:** Level 1 aggregate ("coming soon") · Level 2 de-identified patient-level · **Level 3: "support for identifying and recruiting patients for clinical trials."** ⚠️ Level 3 is advertised on the researcher page and **completely undocumented on the access page** — no process, no terms, no fee. It is a conversation, not a form.

**Level 2 process:** DAR → Data Access Committee → DUA via DocuSign (PI + Institutional Signatory) → register for **Terra** (`terra.bio`) → configure GCP billing. No application fee; compute only. 3-year term. **Timeline: "at least a couple of months" — DAC weeks, DUA negotiation 1–8 months.**

⚠️ **Commercial eligibility risk:** listed eligible applicants are academic, clinical, and patient advocacy — **for-profits are not explicitly addressed**, and individual participants can restrict their data to **non-commercial research only**. Confirm eligibility before investing in the DUA cycle.

The **Global Advocacy Alliance is members-only with no public directory** — strictly worse than NORD's open list. Use NORD for directory work.

### 9.6 Europe: ERDERA, RD-Connect GPAP, and the ERNs

**EJP RD (2019–2023) is finished. ERDERA is the successor** — `https://erdera.org/` (**VERIFIED**), 170+ organisations across 37 countries, coordinated by INSERM, Horizon Europe grant 101156595. Its **Clinical Research Network** (`/clinical-research/`) has an *Innovative Therapies* pillar explicitly covering **"N-of-few trials."** ⚠️ No published sponsor-engagement pathway and no site counts — entry is `/contact-us/` or a funding call.

**RD-Connect:** `rd-connect.eu` states "The content of this website is no longer updated." **The GPAP survived and migrated to CNAG-CRG Barcelona: `https://portal.gpap.cnag.eu/`** (**VERIFIED**). Docs still at `https://platform.rd-connect.eu/gpap_doc/`. Support `help@rd-connect.eu`.
⚠️ **GPAP is "free to all noncommercial members of the RD research community."** A for-profit cannot get access directly — **you need an academic collaborator as PI.** Not negotiable.

**⭐ The ERN Service Directory is the highest-value European asset:** `https://webgate.ec.europa.eu/ernsd/cgi-bin/ern_public.cgi?npage=ern_portal.html` (**VERIFIED**, JS SPA). Searches by ERN, country, and clinical centre, and offers **bulk downloads: "ERN members per network" and "ERN members per country"** — a downloadable roster of every ERN-designated European centre.

**24 ERNs** (`https://health.ec.europa.eu/rare-diseases-and-european-reference-networks/european-reference-networks_en`, **VERIFIED**): Endo-ERN (endocrine) · ERKNet (kidney) · ERN BOND (bone) · CRANIO · EpiCARE (epilepsies) · EURACAN (adult solid cancers) · eUROGEN · **EURO-NMD (neuromuscular)** · GENTURIS · GUARD-Heart · **PaedCan** · RARE-LIVER · ReCONNET · **RITA (immunodeficiency, autoinflammatory, paediatric rheumatic)** · **TRANSPLANT-CHILD** · EuroBloodNet · ERN-EYE · **ITHACA (malformation syndromes & neurodevelopmental)** · ERN-LUNG · ERN-RND (neurological) · ERN-Skin · ERNICA · **MetabERN (hereditary metabolic)** · VASCERN.

### 9.7 UDN / UDNI

`https://undiagnosed.hms.harvard.edu/` (**VERIFIED**), `/udn-sites/`, `/research/data-availability/`. Contact `UDN@hms.harvard.edu`.

**23 clinical sites:** Baylor · CHOP/UPenn · Cincinnati Children's · Duke · Harvard-affiliated · Mount Sinai · Indiana · Johns Hopkins · Mayo · MCW/Children's Wisconsin · NIH UDP · Sanford · Stanford · UAB · UC Irvine/CHOC · UCLA · Miami · Utah · Washington/Seattle Children's · Wisconsin–Madison · Vanderbilt · WashU · Yale. Biorepository Vanderbilt; DMCC Harvard; Sequencing Baylor.

Data → **dbGaP phs001232 annually**; variant classifications → **ClinVar quarterly (submitter 505999)** with HPO terms.

⚠️ **Weak as a recruitment channel** — no participant re-contact mechanism, no collaborative recruitment pathway, dbGaP data is de-identified. **Its real value is PI-finding**: it tells you which of 23 institutions has a clinician who personally worked up your ultra-rare phenotype.

**UDNI** (`https://www.udninternational.org/`, **VERIFIED**, run from Istituto Superiore di Sanità, `udni@iss.it`) is the more approachable of the two — it has an **open membership application** (clinical membership requires 5 undiagnosed cases). Active: 15th Conference Siena Oct 16–17 2026.

### 9.8 NCATS DRDRI (formerly ORDR)

ORDR was transitioned in **April 2022** to the **Division of Rare Diseases Research Innovation (DRDRI)**. ⚠️ `ncats.nih.gov/research/research-activities/ordr` **404s** — searching for "ORDR" leads to dead links. Programs: GARD, RDCRN, **RaDaR** (Rare Diseases Registries Program), and the NCATS Toolkit for Patient-Focused Therapy Development.

---

## 10. Real-world data platforms

### 10.1 The math that decides the platform

For a **1-in-100,000** disease, US true prevalence ≈ **3,350**. Naive expected cases = N/100,000:

| Platform | N | Expected cases |
|---|---|---|
| Komodo Healthcare Map | 330M | ~3,300 |
| Epic Cosmos | 310M | ~3,100 |
| HealthVerity | 270M+ | ~2,700 |
| Truveta | 130M | ~1,300 |
| TriNetX US Collaborative | 117M | ~1,170 |
| Optum Clinformatics | 63–126M | ~630–1,260 |
| PCORnet | 50M/yr | ~500 |
| N3C | ~21M | ~210 |
| **All of Us** | **883K** | **~9** |

**But coding beats N.** The N3C rare disease phenotyping work needed **12,081 SNOMED-CT codes vs only 357 ICD-10 codes** to cover 6,342 rare diseases — a **34:1 ratio**. Pure-claims databases (Komodo, Optum, MarketScan, HealthVerity) are ICD-10-only; if your disease has no code, their 330M patients are worth nothing. **SNOMED-coded EHR sources are dramatically better for rare disease.** Also correct for denominator inflation — TriNetX's 110M "Dataworks-USA" includes duplicates; only ~72M had an encounter in the last 5 complete years.

**Practical floor: below ~50M patients you cannot reliably count a 1-in-100,000 disease.** All of Us is disqualified for counting (the Data Browser also rounds counts up to 20).

### 10.2 ⭐ RDCA-DAP — free, rare-disease-specific, industry-eligible

`https://c-path.org/programs/rdca-dap/` (**VERIFIED**) · portal `https://portal.rdca.c-path.org/` · contribute `/contribute-data` · **DUA PDF `c-path.org/wp-content/uploads/2022/02/RDCA-DAP_DataUseAgreement.pdf`** (**VERIFIED**, all 8 pages read).

FDA-funded (**Grant U18FD005320**), run by Critical Path Institute with NORD. Launched Sept 2021. Contact **`rdcadap@c-path.org`**.

**111+ datasets across 42–43 rare diseases** — patient-level clinical trial, natural history, observational, RWD, and registry data. Named: PKD, DMD, mitochondrial diseases, neurodevelopmental disorders, rare epilepsies, **Friedreich ataxia (largest FA database in existence)**, spastic paraplegia/PLS, CF. Usage: 325 approved platform requests, 35 workspaces.

**Access:** register → Request for Access → **5-member Data Use Committee** (scientific merit / educational purpose / public interest, majority vote) → sign DUA. **Cost: FREE.** Eligibility: *"qualified researchers in industry, government, regulatory agencies and academia"* — **industry explicitly welcome, no size barrier. The most genuinely open door in this report.**

⚠️ **DUA terms to have counsel read first (template v2.4_2026_05_04):**
- **IP license-back:** you retain ownership of Research Results and IP, **but must grant each Data Custodian a "perpetual, non-exclusive, fully-paid up, royalty-free, irrevocable, worldwide, unrestricted license to any Intellectual Property derived from the Research Results."** **For a repurposing company whose entire value is a method-of-use patent, review this before running anything patent-relevant.**
- **Publication:** submit to C-Path **30 days before** any disclosure; custodians may review **for patentable subject matter**.
- **Export permitted** (unlike N3C) subject to per-workspace conditions.
- IRB required; no re-identification; you indemnify C-Path and all custodians; 60-day termination.

**For a 20-patient trial, this is how you build an external/historical control arm and justify a single-arm design to FDA.** Check the portal for your disease first — that's the whole question.

### 10.3 N3C — ⚠️ renamed and restructured

`https://ncats.nih.gov/research/research-activities/n3c/overview` (**VERIFIED**), `/data-overview/access`, `/faqs`. `https://n3c.ncats.nih.gov/` (JS app). ⚠️ `covid.cd2h.org/onboarding` and `/dur/` are **DEAD (404)** — widely-cited stale docs.

**Headline:** the Aug 2025 NCATS factsheet states N3C is *"currently available to support research on three diseases: cancer, renal disease and Long COVID,"* with future expansion planned into *"diabetes, Alzheimer's disease and chronic or rare pediatric diseases."* The old open ~21M-patient enclave is now disease-specific tenants. **Unless your disease is renal, oncologic, or Long-COVID-adjacent, N3C is probably not open to your question.** Confirm with `NCATS_N3C@nih.gov`.

OMOP CDM; three levels (Synthetic / Limited Data Set / De-identified). **Industry access explicitly allowed** per the FAQ. Process: institutional DUA (Authorized Official signs, covers unlimited projects) → register → NIH infosec training → DUR → federal Data Access Committee. **~15 business days DUR→workspace**; the institutional DUA is the slow part. **Cost: free.** ⚠️ **"Data cannot be downloaded from this enclave or be removed."**

**Steal the codeset regardless of platform choice:** the N3C rare disease phenotyping workflow mapped GARD/ORPHANET → SNOMED-CT/ICD-10, producing **12,081 SNOMED-CT + 357 ICD-10 codes covering 6,342 rare diseases across 30 ORPHANET classes**, applied to 21M+ patients (316,836 / 6.55% of COVID-positive patients had a preexisting rare disease). **This is the single most reusable artifact in the RWD landscape.**

### 10.4 All of Us

`https://www.researchallofus.org/` · `/data-tools/data-access/` · `/institutional-agreements/` · **`https://databrowser.researchallofus.org/` — public, no login** (all **VERIFIED**).

~**883,000** enrolled; **535,000+ WGS**, ~482,000 with linked EHR. Tiers: Public (Data Browser) → Registered → Controlled (genomics).

⚠️ **DURA contradiction, flagged honestly:** the official DURA infographic (`https://orau.org/allofus/documents/dura-process-infographic.pdf`, **VERIFIED**) states *"Currently, academic, not-for-profit, and health care organizations can enter into a DURA"* — **for-profits are not listed.** But the live registered-institutions page (1,457 institutions) contains **Eli Lilly, AstraZeneca, Biogen, Gilead, Google, Illumina, Abbott, AbbVie, Amgen, Bayer, BMS, Calico.** Most likely the infographic is stale. **But every confirmable for-profit is large-cap.** Submit and find out; don't build a plan on it.

**Verdict: useless for counting a 1-in-100,000 disease (~9 expected). But the Data Browser is worth 20 minutes** — public, no login, no agreement — as a free sanity check on whether your concept codes appear in structured EHR data at all.

### 10.5 TriNetX — the actual answer for cohort counting

`https://trinetx.com/` · `/data/` · `/solutions/trinetx-live/` (**VERIFIED**). ⚠️ `/real-world-data-network/` is **404**.

**Federated:** "Your query moves. Your patients' data doesn't." Patient-level data stays behind each HCO's firewall; queries run locally, return aggregate counts. This is why counting is instant and needs no IRB.

Networks (from the peer-reviewed review, more reliable than marketing pages): Global Collaborative 153.5M / 128 HCOs · **US Collaborative 117.2M / 66 HCOs** · LATAM 31.5M · EMEA 19.2M · APAC 5.1M. **Dataworks-USA** (the licensable dataset): 110M+ patients, ~72M with an encounter 2019–2023, 65 US HCOs, ~75% AMCs, mean **6.2 years** longitudinality, refreshed ~biweekly. Skews ~5 years older than Census, 53% female.

⚠️ **The key asymmetry:** *"Access to TriNetX is either by commercial licensing agreement (industry) or by collaboration agreement (academia)."* **Free to academics, paid for you.** No published price; expect **five to low-six figures** for a scoped rare-disease license, with the browse/count tier far cheaper than a full extract. Export is substantially restricted outside the US by GDPR/LGPD.

**The workflow you want:** Query Builder → define cohort by ICD-10/SNOMED/RxNorm/LOINC/genomics → **live patient counts globally, by region, and by individual HCO.** That last part converts directly into a site list.

**⭐ Cheapest legitimate path: partner with an academic collaborator at a TriNetX member AMC.** They have free access and can run feasibility counts. Common practice, ~$0.

### 10.6 The rest, briefly

- **PCORnet** — `pcornet.org/data/` · `/front-door/` (**VERIFIED**). **50M+ people/yr**, 8 networks (incl. **PEDSnet**, valuable for pediatric-onset), standardized CDM. **Front Door explicitly names "industry scientists, sponsors" as eligible.** Simple Data Network Requests are **"generally completed without charge."** Weeks to months. **Best-kept secret for a small budget.**
- **HealthVerity** — `healthverity.com/marketplace/data-ecosystem/` (**VERIFIED**). 270M+ lives, 75+ sources, 10 data types (incl. ~65% of the US lab market). **Marketplace model: license only the slice you need under a single contract, delivered <2 weeks. The most SMB-friendly commercial model in this list.**
- **Truveta** — 30 health systems, 900+ hospitals, **130M+ EHR patients** (daily) + 200M+ linked claims, **7B+ clinical notes, 100M+ images**. Notes+images matter because **NLP over notes may be the only way to find patients for an uncoded disease.** Supports FDA regulatory exports. 💰 Azure Marketplace lists Studio/Embassy reservations at **$95K / $245K / $495K** and **the underlying data subscription is not included** (**UNVERIFIED** — 403). Likely out of reach.
- **Komodo** — Healthcare Map **330M+ patients, 1T+ records**, daily. MapLab / Sentinel / MapEnhance / Marmot. **Rare disease is a marketed strength**, with a **GeneDx** partnership contributing de-identified data from **600,000+ exomes and genomes** — genetic data finds patients whose ICD record is uninformative. Six figures. 💡 **Non-obvious cheap path: Komodo supplies Prism free to advocacy orgs in the CZI Rare As One network** — partnering with your disease's org may be far cheaper than licensing.
- **Optum Clinformatics** — commercial + Medicare Advantage claims from 2007, **lab results (LOINC)**, SSA mortality, optional OMOP format. **You receive files, not an enclave** — a major advantage for building control arms. Academic site licenses are far cheaper.
- **Merative MarketScan** — Commercial Claims 2005–2023, >200M cumulative lives, 20B+ service records, + 12.9M Medicare Supplemental. **Longest longitudinal claims history available.** 💡 Many AMCs hold institutional MarketScan/Optum licenses — a collaboration gets you analyses for near-zero.
- **Datavant** — **not a dataset, it's the plumbing.** Privacy-preserving tokenization; 350+ RWD partners. Relevant only if you need to link your own trial/registry data to external RWD — which is exactly what an external control arm requires.
- **Epic Cosmos** — 310M patients, 2,198 hospitals, 21.6B encounters, SNOMED-coded EHR. ⚠️ **CONFIRMED CLOSED.** Verbatim: access is limited to those *"affiliated with and approved by a Cosmos participating organization,"* and *"access to Cosmos and Cosmos data cannot be purchased."* Scientifically ideal, commercially inaccessible. Only route is a collaborator at an Epic health system, and no data leaves.
- **CMS via ResDAC / VRDC** — `resdac.org/cms-fee-information-research-identifiable-data` (**VERIFIED**; ⚠️ `resdac.org/cms-data-file-availability-fees` is **404**). VRDC ~**$35,000 first year**, ~**$23,000/yr** after (**UNVERIFIED-exact**; the authoritative CMS fee PDF 404'd). **VERIFIED from the FAQ:** +1TB storage $1,500, +2,000 Databricks credits $1,500. Physical files priced per year of data across four cohort tiers (MEDPAR $2,000–$5,000; Inpatient $2,000–$12,000), ~$20,000 initial project fee. Export is **aggregate only, minimum cell size 11**. **Wrong tool for pediatric-onset rare disease** — 65+ and disabled only.

### 10.7 Ranked by practical accessibility on a small budget

| # | Platform | Cost | Viable? | Best use |
|---|---|---|---|---|
| 1 | **RDCA-DAP** | Free | ✅ industry explicitly welcome | Natural history + external control arm. Check IP clause. |
| 2 | **PCORnet Front Door** | Free (simple requests) | ✅ industry named eligible | Free feasibility counts across 50M |
| 3 | **All of Us Data Browser** | Free, no login | ✅ | 20-min concept-coverage sanity check |
| 4 | **TriNetX via academic collaborator** | ~$0 | ✅ with a partner | **Best counting answer, cheapest** |
| 5 | **N3C** | Free | ⚠️ renal/cancer/Long COVID only | Steal the 12,081-code rare disease codeset regardless |
| 6 | **HealthVerity** | $$ à la carte | ✅ most SMB-friendly | License only what you need, <2 weeks |
| 7 | **TriNetX direct** | $$–$$$ | ⚠️ | Counts by site + licensable dataset |
| 8 | **Optum / MarketScan** | $$–$$$ (cheap via academic license) | ⚠️ via partner | Longest longitudinal claims; you get files |
| 9 | **Komodo** | $$$ | ❌ unless via a Rare As One org | Largest N + genomics overlay |
| 10 | **Truveta** | $95K–$495K + subscription | ❌ | Notes + images + FDA-grade exports |
| 11 | **CMS VRDC** | $35K yr1 / $23K after | ❌ unless geriatric | 65+/disabled only |
| 12 | **Epic Cosmos** | Cannot be purchased | ❌ structurally closed | Only via an Epic-customer collaborator |
| 13 | **All of Us Workbench** | Free-ish | ❌ N far too small | Not for rare disease counting |

---

## 11. Newborn screening

**Headline: the RUSP governance model changed fundamentally in 2025.** ACHDNC was terminated April 1, 2025; HRSA now runs nominations directly via Federal Register notice-and-comment. **Most public references — Baby's First Test, March of Dimes — are stale** and still describe the old committee and old counts.

⚠️ `hrsa.gov`, `cdc.gov`, `hhs.gov`, `congress.gov`, `wonder.cdc.gov` all **403 to automated fetchers**. Items below marked VERIFIED were read through the Wayback Machine or an alternate host.

### 11.1 RUSP: 40 core + 26 secondary = 66 conditions

Confirmed against the **official HRSA RUSP table PDF "As of December 2025"** (downloaded and parsed), corroborated by NewSTEPs.

| URL | Status |
|---|---|
| `https://newbornscreening.hrsa.gov/about-newborn-screening/recommended-uniform-screening-panel` | **NEW canonical** (VERIFIED via archive) |
| `https://www.hrsa.gov/advisory-committees/heritable-disorders/rusp` | **LEGACY/archival** — don't build against it |
| `https://mchb.hrsa.gov/sites/default/files/mchb/programs-impact/recommended-uniform-screening-panel-table-december-15-2025.pdf` | **The downloadable table** (VERIFIED, 3pp, 201 KB) |

**PDF only — there is no official CSV, Excel, or API for the RUSP**, and the date-stamped filename changes on every revision. **Best machine-readable substitute: `https://www.newsteps.org/nbs-disorders`** (LIVE-200) — server-rendered HTML table of all core + secondary conditions with a **"Date Added" column** and time-criticality flags.

**Recent additions** (each creates a newly identifiable diagnosed cohort): SMA Jul 2018 (→35) · MPS II Aug 2, 2022 (→36) · GAMT Jan 2023 (→37) · infantile Krabbe Jul 1, 2024 (→38) · **Duchenne muscular dystrophy Dec 16, 2025 (→39)** · **Early-Onset Metachromatic Leukodystrophy Dec 16, 2025 (→40)**. Note MLD is scoped to **early-onset only**.

### 11.2 ACHDNC terminated — and the new nomination path

**Terminated April 1, 2025** under a Secretary Directive; its statutory authority had lapsed in 2019 so it was a discretionary committee. Source: **CRS Report R48757**, readable at `https://www.everycrsreport.com/reports/R48757.html` (LIVE-200; congress.gov 403s). The Dec 2025 Federal Register notices state: *"The Advisory Committee on Heritable Disorders in Newborns and Children (ACHDNC), now inactive…"* HRSA's Heritable Disorders portfolio was proposed for elimination in the FY2026 CBJ. **H.R. 4709** (Jul 23, 2025) would reauthorize ACHDNC through 2030 as a statutory committee; no House action as of the CRS report.

**The replacement process, as actually executed for DMD and MLD:**
1. HRSA publishes a Federal Register **"Notice With Request for Comment"** (Aug 14, 2025 — DMD at 90 FR 39197, MLD at 90 FR 39196)
2. Public comment — DMD: 379 comments (366 support / 11 oppose); MLD: 98 (96/1/1)
3. HRSA weighs comments + the existing Evidence Review Group review, recommends to the Secretary
4. Secretary accepts Dec 16, 2025; final notice Dec 22, 2025

**⭐ The Federal Register JSON API is unblocked and is your reliable RUSP-change monitor:**
```
https://www.federalregister.gov/api/v1/documents/2025-23573.json
https://www.federalregister.gov/documents/full_text/text/2025/12/22/2025-23573.txt
```

**How a company nominates today:** ⚠️ **there is no published standing nomination process.** The old two-step path (Preliminary Nomination Form to `achdnc@hrsa.gov`, gated on four questions: is there a screening test; case-definition agreement; has a prospective population-based pilot identified ≥1 infant; does pre-symptomatic identification enable effective therapy) is dormant. House Appropriations "requests a plan regarding the new process." **Realistic levers: (a) generate population pilot data + an approved therapy so the condition is ERG-ready, (b) mobilize public comment when HRSA publishes a notice, (c) congressional pressure.** Archived guidance: `http://web.archive.org/web/20250110151753/https://www.hrsa.gov/advisory-committees/heritable-disorders/rusp/nominate`.

**💰 Commercially critical — the ACA trigger:** RUSP conditions are HRSA-supported preventive guidelines under **PHS Act §2713**. Non-grandfathered plans **must cover the screening with no cost-sharing for plan years beginning one year after Secretary adoption.** For DMD and MLD, that is **plan years beginning on or after December 16, 2026.**

### 11.3 State panels and the adoption lag

**Baby's First Test** — `https://www.babysfirsttest.org/newborn-screening/states/<state-slug>` (LIVE-200). Static server-rendered HTML, conditions grouped by category, with a headline count (e.g. *"California currently screens for 80 conditions"*). No API. **No true side-by-side comparison tool** — a matrix requires scraping all 51 jurisdictions.

⚠️ **Two problems.** (1) `robots.txt` sets `Content-Signal: ai-train=no` and explicitly `Disallow: /` for **ClaudeBot, GPTBot, CCBot, Google-Extended, Amazonbot, Applebot-Extended, Bytespider, meta-externalagent**, plus `Crawl-delay: 10`. Automated collection carries a stated-terms problem. (2) Its RUSP page still says *"35 core conditions and 26 secondary"* and describes ACHDNC as actively meeting — **~5 conditions and one governance regime out of date.**

**Use NewSTEPs instead:** `https://www.newsteps.org/data-resources/state-profiles` and `/view-state-profile` (LIVE-200) cover all 50 states, DC, and territories. **Profile data is explicitly public**, and the page invites *"If you would like a different view or export of this data, please email newsteps@aphl.org."* **That email is the highest-value, lowest-friction ask in this entire section.**

**⚠️ The adoption lag, quantified.** Sontag et al., *Int J Neonatal Screen* — `https://pmc.ncbi.nlm.nih.gov/articles/PMC10123615/` (LIVE-200, APHL/NewSTEPs authors, 53 programs):

- **Full national adoption took 8.6 years for SCID and 6.8 years for CCHD.**
- **As of Dec 2022**, years after RUSP addition: Pompe (2015) 37 programs · MPS I (2016) 34 · X-ALD (2016) 32 · SMA (2018) 48.
- Pace (programs added per year): SMA 11.3 · CCHD 7.8 · SCID 6.2 · MPS I 5.4 · Pompe 4.9 · X-ALD 4.7.

**Modeling implication:** for a condition added in year 0, usable national diagnosed incidence does not arrive until roughly **year 5–9**. Apply a **time-varying screened-birth fraction `c(a)`** (§8.5), never the full US birth count. For DMD/MLD (added Dec 2025), expect meaningful multi-state yield around **2028–2032**.

### 11.4 ⭐ NewSTEPs — the best source for diagnosed cases per condition

Run by **APHL** under HRSA cooperative agreement U22MC24078. All LIVE-200 VERIFIED: `/data-center` · `/data-center/dashboards-and-reports` · **`/data-repository/data-requests`** · `/data-resources/quality-indicators` · **`/data-api/sign-up`**.

Holds state/territory profile data, quality indicators, and **NBS confirmed cases — aggregate counts by condition by state by year**, submitted voluntarily by 53 programs. Runs on a **two-year lag** because diagnostic confirmation takes time.

⚠️ **Access reality, verbatim:** *"NewSTEPs will in no event share state/territory-level quality indicator data or case data unless explicit permission has been granted by the NBS program,"* and *"Sharing aggregate, unpublished data with investigators must be approved by the NewSTEPs Steering Committee."* So: **profile data public and exportable on request; case data gated behind per-state consent + Steering Committee approval**, framed around "research and quality improvement." A for-profit is not excluded on its face but is not the intended audience. The Tableau **"Confirmed Cases"** dashboard is behind account SSO. **The `/data-api/sign-up` route is the most promising programmatic path — pursue it directly.**

**⭐⭐ The published data — national case counts, free, no request needed.** Sontag et al., *"Infants with Congenital Diseases Identified through Newborn Screening—United States, 2018–2020"* — `https://pmc.ncbi.nlm.nih.gov/articles/PMC10123626/` (LIVE-200). This is effectively the NewSTEPs repository published in the open, and it is **the best free answer to "how many diagnosed US patients per year."**

Overall birth prevalence of DBS-detected core RUSP diseases = **20.07 per 10,000** (2018–2020), up from 18.31 (2015–2017). Applied to 2021 births → **~7,389 infants/year**. Total 2018–2020: **20,885 cases.**

Selected results (cases / births screened / per 10,000):

| Condition | Cases | Births screened | Rate/10k |
|---|---|---|---|
| Primary congenital hypothyroidism | 7,421 | 11,086,342 | 6.69 |
| Sickle cell disease (SS+Sβthal+SC) | 5,517 | 11,086,342 | 4.98 |
| Cystic fibrosis | 2,518 | 10,983,899 | 2.29 |
| PAH deficiency (PKU) | 852 | 11,086,342 | 0.77 |
| CAH | 781 | 11,086,342 | 0.70 |
| MCAD deficiency | 651 | 11,086,342 | 0.59 |
| **X-linked adrenoleukodystrophy** | 345 | **5,125,176** | 0.67 |
| **Pompe disease** | 309 | **5,479,082** | 0.56 |
| **SMA** | 219 | **3,185,560** | 0.69 |
| SCID | 185 | 10,947,551 | 0.17 |
| **MPS I** | 71 | **5,121,441** | 0.14 |
| Propionic acidemia | 62 | 11,086,342 | 0.06 |
| MSUD | 56 | 11,086,342 | 0.05 |
| MMA (mut) | 45 | 11,086,342 | 0.04 |
| Tyrosinemia type I | 39 | 11,086,342 | 0.04 |
| LCHAD deficiency | 32 | 11,086,342 | 0.03 |
| Homocystinuria | 16 | 11,086,342 | 0.01 |
| TFP deficiency | 8 | 11,086,342 | 0.01 |

⚠️ **Read the denominators.** Newer conditions have much smaller ones (Pompe 5.5M, MPS I 5.1M, SMA 3.2M vs ~11.1M for legacy conditions) because only screening states/months count. Methodology is rigorous — fractional-year analysis for mid-year implementations.

**Quality caveats:** voluntary submission (49 states + 2 territories; MS and DC excluded from the prevalence analysis) · **aggregate only, not individual-level** · harmonization incomplete despite published consensus case definitions · known artifacts (CF inflated by CRMS pickup; CH varies with TSH-vs-T4 algorithm and includes transient cases) · **DBS only** — excludes hearing loss and CCHD.

### 11.5 CDC NSQAP — important negative finding

**NSQAP is laboratory quality assurance, not a patient or case-count source.** Do not budget time expecting cohort data. It develops DBS methods and ships ~1M reference materials/year to 670+ labs in 86+ countries, with ISO/IEC 17043 accreditation. `https://www.cdc.gov/laboratory-quality-assurance/php/newborn-screening/index.html` (VERIFIED via archive; 403 to bots). Participant portal `https://nbs.dynamics365portals.us/` is lab-gated.

Where it *is* useful: **Program Reports and proficiency-testing data quantify assay performance and inter-laboratory variability** — relevant to false-positive rates and to how much you trust a given state's detection.

### 11.6 States publishing confirmed case counts

- **New York — best per-condition public reporting.** Wadsworth Center annual report with a **"# Confirmed with Disease" column per disorder.** `https://www.wadsworth.org/sites/default/files/2025-04/2023%20Annual%20Report_Final.pdf` (LIVE-200, parsed). 2023: 204,505 newborns, 1,711 referrals; CAH 8 · congenital hypothyroidism 114 · Hb SS 80 · Hb SC 58 · PKU 11 · MCAD 6 · VLCAD 5 · homocystinuria 1 · MSUD 0 · tyrosinemia I/II/III 0 · LCHAD 0 · TFP 0. 2024 topline: **671 infants diagnosed**, 206,728 infants, 50+ conditions.
- **California — best machine-readable dataset.** `https://data.chhs.ca.gov/dataset/newborn-screening-disorders` (LIVE-200). **Three downloadable CSVs** (statewide, by race/ethnicity, by region) + XLSX dictionaries + county-region crosswalk. Covers **2009–2019**, counts of disorders **diagnosed**. ⚠️ Marked **ARCHIVED**; **counts suppressed below 6 cases** — which kills exactly the ultra-rare conditions you care about. SCID from Mar 2013, ALD from Feb 2016, Pompe and MPS I from Aug 2018. The `data.ca.gov` mirror 404s. California detects **750+ newborns/year** and screens ~80 conditions.
- **Texas — annual reports plus a statutory RUSP-gap report.** `https://www.dshs.texas.gov/sites/default/files/legislative/2025-Reports/2025-HB-2478-Newborn-Screening-Report.pdf` (LIVE-200) is **statutorily required to identify RUSP conditions NOT on the Texas panel**, with resource needs and timelines — unusually valuable for tracking adoption gaps. ~800,000 screens/year (Texas screens twice). 2024: 27,913 abnormal, **1,089 newborns identified**. Panel = 59 lab conditions + hearing + CCHD after **adding four lysosomal storage diseases in Aug 2025**.
- Also publishing: **North Carolina** (statutory annual report, G.S. 130A-125(e)); **Minnesota** NBS Advisory Committee minutes tracking RUSP adoption.

---

## 12. The ranked workflow: "disease name in a case report" → "N diagnosed US patients + the 3 centers that treat them"

### Stage 0 — Resolve the name (minutes, free, fully automatable)

Case reports use eponyms, gene-based names, and obsolete synonyms interchangeably. Never key on a string.

1. `GET https://api.monarchinitiative.org/v3/api/search?q=<name>` → candidate MONDO IDs. Or `/v3/api/ground` for free text.
2. `GET /v3/api/entity/MONDO:xxxxxxx` → the full xref set in one call: ORPHA, OMIM, GARD, UMLS, MedGen, ICD10CM, MeSH, DOID.
3. Resolve retired IDs through MedGen's `*_CUI_history.txt` files and Orphanet's `List_deprecated_obsoleted` sheet.
4. **Output: a canonical `MONDO:` + the ORPHAcode.** Everything downstream keys on these two.

### Stage 1 — Rare-pediatric eligibility triage (minutes, free, automatable)

5. `GET https://api.orphadata.com/rd-natural_history/orphacodes/{code}?lang=en` → `AverageAgeOfOnset`. **Gate: onset ⊆ {Antenatal, Neonatal, Infancy, Childhood, Adolescent} with no Adult/Elderly.**
6. `GET /rd-epidemiology/orphacodes/{code}` → prevalence records. Apply the §8.4 tiering.
7. `GET /rd-cross-referencing/orphacodes/{code}` → check `DisorderMappingICDRelation`. **If ICD-10 is "Attributed code," flag the disease as claims-invisible** — that decides your RWD strategy in Stage 3.
8. **Cheap corroboration: search the FDA orphan designation database** (`accessdata.fda.gov/scripts/opdlisting/oopd/`, Excel export). If a competitor holds a designation, their accepted US prevalence estimate is your best anchor and costs nothing.

### Stage 2 — Get a defensible N (hours to days)

9. **Is it newborn-screened?** Check `newsteps.org/nbs-disorders`. If yes → the Sontag 2018–2020 IJNS table gives you a real per-condition US rate with a real denominator. **This is the single best free number that exists.** Multiply by 3.6M births, apply the screening-coverage ramp `c(a)`.
10. **Otherwise, run the survival-weighted estimator**: `P ≈ B × p × ê`. Source `ê` (life expectancy of affected individuals) from GeneReviews, the natural history literature, or a registry — **not from Orphanet, which no longer publishes age of death.**
11. **Free empirical corroboration, in this order:** RDCA-DAP portal (is your disease among the 42?) → PCORnet Front Door Data Network Request (free, industry-eligible, 50M patients) → TriNetX counts via an academic collaborator at a member AMC (~$0, and gives you per-HCO breakdown).
12. **Report a range with the method attached**, never a bare point estimate. Record which Orphanet tier the number came from — that provenance is what makes the number defensible to FDA and to investors.

### Stage 3 — Find the centers and the PIs (hours, free, automatable)

13. **ClinicalTrials.gov API v2** — enumerate every `LocationFacility` across all trials in the disease, rank by trial count, extract `overallOfficials[]`. **This is your primary site ranking.**
14. **NIH RePORTER API** — `"disease name"` in title/abstract → the PIs with grants but no trial yet. Often more available than a PI already running three industry studies.
15. **RDCRN** — is your disease among the 280+ covered by the 19 consortia? If so, **the consortium PI is the single highest-leverage human in this entire map**: sites, patients, IRB relationships, and Contact Registry access, all in one relationship.
16. **NORD member list** — find the **Platinum-tier** org for your disease (Platinum = already runs research infrastructure and a Medical Advisory Board).
17. **NORD Centers of Excellence (46) + ERN Service Directory bulk downloads (Europe)** — cross-reference against your ClinicalTrials.gov ranking.

**Your top 3 centers = the institutions that appear in all of: ClinicalTrials.gov facility ranking ∩ RDCRN consortium site list ∩ NORD COE.** Where fewer than three overlap, fall back to RePORTER PI institutions plus the affiliations on the PMIDs in Orphanet's prevalence `Source` field.

### Stage 4 — Make contact (weeks to months — start the legal work in parallel)

18. Approach the **RDCRN consortium PI** with a collaboration proposal. `support@rdcrn.org` / the DMCC Clinical Research Core is the institutional door if you also want protocol and regulatory help.
19. Approach the **Platinum patient org**. For a 20-patient trial this is often faster than any institutional route.
20. **RDCA-DAP for the external control arm** — free, industry-eligible, but have counsel read the IP license-back clause first.
21. **RARE-X Level 3** if it exists for your disease — the only channel that explicitly advertises trial recruitment support, but undocumented; budget 2+ months and confirm for-profit eligibility before starting the DUA.

### The four things that will cost you the most time

1. **No registry sells you patients.** RDCRN Contact Registry, IAMRARE, RARE-X, GPAP — every one routes through an intermediary (consortium PI, patient org, DAC). These are relationships, not transactions.
2. **DUA negotiation is the hidden critical path.** RARE-X states **1–8 months** for institutional DUA execution alone. Start legal in parallel with everything else, not after.
3. **Your phenotype definition matters more than your database.** SNOMED-coded EHR beats a bigger ICD-10-only claims set for rare disease by a factor of ~34 in code coverage. Harvest the N3C rare disease codeset regardless of which platform you buy.
4. **GPAP is non-commercial only, and Epic Cosmos cannot be purchased at any price.** Both require an academic or Epic-customer collaborator. Plan for that or write them off.

---

### Licence summary for a commercial pipeline

| Source | Licence | Commercial |
|---|---|---|
| Orphanet scientific knowledge files, ORDO, Nomenclature Pack | **CC BY 4.0** | ✅ with attribution |
| Orphanet **Expert Resources** | Contract required | ❌ paid contract with Orphanet-AISBL |
| MONDO, Monarch KG | **CC BY 4.0** (per-source in `metadata.yaml`) | ✅ |
| HPO | **Custom** — cite, show version, **do not alter logical relationships** | ✅ with conditions |
| ClinGen | **CC0 1.0** | ✅ unrestricted |
| ClinVar, MedGen, GARD, NCBI | US public domain | ✅ |
| **OMIM** | JHU proprietary | ❌ **paid licence required; double-fee penalty for unlicensed access; weekly refresh mandatory once licensed** |
| WHO ICD-11 | Accept container licence | ✅ |
| RDCA-DAP | DUA with **IP license-back to data custodians** | ⚠️ counsel review |