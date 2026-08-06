# Literature & Clinical Trial Registry Data Pathways
### Reference for continuous detection of "off-patent drug X benefited rare pediatric disease Y"

**Verification status legend**

- **VERIFIED** — I issued a live request during this session (2026-08-05) and confirmed the response shape.
- **VERIFIED (blocked)** — endpoint exists and responded, but returns an auth/WAF error from this network.
- **UNVERIFIED** — documented but not confirmed live, or confirmed only via docs page.

All HTTP checks were run 2026-08-05. Byte counts and record counts below are actual measured values, not estimates.

---

## 0. The single most important finding first

Before the source-by-source detail, the fact that should drive your entire architecture:

**PubMed MeSH indexing lags publication by weeks-to-months, so MeSH-based queries cannot be your detection layer.** Measured live:

| Query | Count |
|---|---|
| `"Rare Diseases"[mh]` — all time, entire PubMed | **15,927** |
| `"Rare Diseases"[mh] AND 2026/07/01:2026/08/05[edat]` | **26** |
| `"Case Reports"[pt] AND 2026/07/01:2026/08/05[edat]` | **6,290** |
| All PubMed records entered 2026/07/01–2026/08/05 | **175,025** |
| ...of which `publisher[sb]` (not yet MEDLINE-indexed) | **75,333** |
| ...of which `pubmednotmedline[sb]` | **49,004** |
| ...of which `inprocess[sb]` | **7,256** |
| ...of which `medline[sb]` (fully MeSH-indexed) | **43,431** |

Two conclusions:

1. `"Rare Diseases"[MeSH]` is a near-useless recall filter. 15,927 records total across all of PubMed, for a domain with ~7,000 diseases and a literature in the hundreds of thousands. It is applied inconsistently by indexers. **Never use it as your primary rare-disease gate.** Use a disease-name dictionary expanded from Orphanet/MONDO, matched against title/abstract.
2. Only ~25% of newly-entered records are MeSH-indexed. **Detection runs on `[tiab]` + `[pt]` + `[ti]`; MeSH is a backfill/enrichment layer that arrives later and lets you re-score.**

`"Case Reports"[pt]` *is* usable fresh (6,290 in a 5-week window) because many publishers supply the publication type at deposit — but it will still miss the ~43% of the firehose sitting in `publisher[sb]`. Plan a re-scan of every record 60–120 days after first sight, when MeSH lands.

---

## 1. PubMed E-utilities

**VERIFIED.** Base URL: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/`

### Auth, rate limits, etiquette

| Item | Value |
|---|---|
| Without API key | **3 requests/sec** per IP |
| With API key | **10 requests/sec** by default (higher on request to NLM) |
| Key parameter | `api_key=` (query string) |
| Key registration | NCBI account → Settings page → API Key Management. Free, instant. |
| Required identifiers | `tool=` (no spaces) and `email=` on every request |
| Large-job window | NLM asks that bulk jobs run **weekends or 21:00–05:00 US Eastern** on weekdays |
| Formats | `retmode=json` or `xml`; `efetch` for PubMed is **XML-only** (`retmode=xml`), no JSON |

### The four calls you need

```bash
# esearch — get PMIDs. Always use usehistory for anything >200 hits.
curl -sG 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi' \
  --data-urlencode 'db=pubmed' \
  --data-urlencode 'term="Case Reports"[pt] AND cystinosis' \
  --data-urlencode 'usehistory=y' --data-urlencode 'retmode=json' \
  --data-urlencode 'api_key=YOURKEY' --data-urlencode 'tool=rdh' --data-urlencode 'email=you@co.com'
# VERIFIED -> {"count":"411","querykey":"1","webenv":"MCID_6a73c3d606eeeb1475024e38"}
```

```bash
# Incremental polling — THIS is your cron query shape. datetype=edat + reldate.
curl -sG 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi' \
  --data-urlencode 'db=pubmed' \
  --data-urlencode 'term="Case Reports"[pt] AND (rare[tiab] OR orphan[tiab])' \
  --data-urlencode 'datetype=edat' --data-urlencode 'reldate=2' \
  --data-urlencode 'retmode=json' --data-urlencode 'retmax=500'
# VERIFIED -> count 204, translated to "2026/08/03:2026/08/05[Date - Entry]"
```

```bash
# efetch — full record incl. abstract, MeSH, PublicationType, chemicals
curl -s 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=42290712&retmode=xml&rettype=abstract'
# VERIFIED -> <ArticleTitle>, <Abstract>, <PublicationType> x3

# esummary — cheap metadata for ranking without the abstract payload
curl -s 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=39000000&retmode=json'
# VERIFIED

# elink pubmed -> pmc  (does this PMID have free full text?)
curl -s 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&db=pmc&id=39000000&retmode=json'
# VERIFIED -> linkname "pubmed_pmc" -> ["11241611"]

# elink pubmed -> pubmed (related citations; use for candidate expansion)
curl -s 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&db=pubmed&linkname=pubmed_pubmed&id=42290712&retmode=json'
# VERIFIED (200)
```

For >10k PMIDs, POST to `efetch` with `WebEnv`/`query_key` from the `usehistory=y` esearch and page with `retstart`/`retmax` (500 per efetch is the practical ceiling for PubMed XML).

### Publication-type and MeSH filters that isolate small studies

PubMed publication types relevant here (exact strings, `[pt]`):

- `"Case Reports"` — the workhorse. **There is no "Case Series" publication type**; case series are only findable as `"case series"[tiab]`.
- `"Clinical Trial, Phase I"`, `"Clinical Trial, Phase II"`, `"Controlled Clinical Trial"`, `"Observational Study"`, `"Comparative Study"`, `"Multicenter Study"`, `"Evaluation Study"`, `"Twin Study"`
- `"Randomized Controlled Trial"` — useful as an *exclusion* signal for the "small study" tier, or as a "someone got serious" escalation signal.
- `"Letter"`, `"Editorial"`, `"Comment"` — exclude (but note: many n-of-1 reports publish as Letters; consider `"Letter"[pt] AND "case"[ti]` as a separate low-confidence stream).

MeSH descriptors, with measured counts:

| MeSH | Value for this use case |
|---|---|
| `"Rare Diseases"[mh]` | 15,927 total. Low recall. Precision-only. |
| `"Genetic Diseases, Inborn"[mh]` | Broad tree, good recall for the pediatric genetic space |
| `"Metabolism, Inborn Errors"[mh]` | Best single high-yield rare-pediatric tree |
| `"Orphan Drug Production"[mh]` | Orphan designation discourse |
| `"Off-Label Use"[mh]`, `"Drug Repositioning"[mh]` | The repurposing signal itself |
| `"Compassionate Use Trials"[mh]`, `"N-of-1 Trials as Topic"[mh]` | High-precision access-pathway signal |
| Age gates: `infant[mh]`, `child[mh]`, `adolescent[mh]`, `"Infant, Newborn"[mh]` | Standard pediatric filter |
| Subheadings: `"drug therapy"[sh]`, `"therapeutic use"[sh]` | Attaches to disease/drug terms |

### Working query examples (counts measured live)

```
# Q1 — HIGH PRECISION, retrospective corpus build (MeSH available)
"Case Reports"[pt] AND ("drug therapy"[sh] OR "therapeutic use"[sh])
  AND ("Rare Diseases"[mh] OR "Genetic Diseases, Inborn"[mh] OR "Metabolism, Inborn Errors"[mh])
  AND (infant[mh] OR child[mh] OR adolescent[mh])
-> 14,926 records
```

```
# Q2 — publication-type ladder over IEM, pediatric
("Case Reports"[pt] OR "Clinical Trial, Phase I"[pt] OR "Clinical Trial, Phase II"[pt]
  OR "Observational Study"[pt] OR "Multicenter Study"[pt] OR "Comparative Study"[pt])
  AND "Metabolism, Inborn Errors"[mh] AND (infant[mh] OR child[mh])
-> 21,947 records
```

```
# Q3 — benefit language (the "positive result" half of your signal)
"Case Reports"[pt] AND ("Metabolism, Inborn Errors"[mh] OR "Genetic Diseases, Inborn"[mh])
  AND (improv*[tiab] OR resolution[tiab] OR remission[tiab] OR "response to treatment"[tiab]
       OR normaliz*[tiab] OR "clinical benefit"[tiab])
-> 15,908 records
```

```
# Q4 — access pathway signal (compassionate/n-of-1/expanded access), pediatric
("N-of-1 Trials as Topic"[mh] OR "n-of-1"[tiab] OR "compassionate use"[tiab]
  OR "Compassionate Use Trials"[mh] OR "expanded access"[tiab] OR "named patient"[tiab])
  AND (infant[mh] OR child[mh] OR adolescent[mh])
-> 921 records
```

```
# Q5 — DETECTION QUERY (MeSH-free, runs daily). This is the one you cron.
(rare[tiab] OR ultra-rare[tiab] OR orphan[tiab] OR "inborn error"[tiab] OR syndrome[ti])
  AND ("case report"[tiab] OR "case series"[tiab] OR "we report"[tiab] OR "we describe"[tiab])
  AND (child*[tiab] OR infant*[tiab] OR pediatric[tiab] OR paediatric[tiab]
       OR neonat*[tiab] OR adolescen*[tiab] OR "years old"[tiab] OR "month-old"[tiab])
-> 487 records in the 2026/07/01–2026/08/05 window
```

```
# Q6 — DETECTION QUERY, repurposing-vocabulary arm (runs daily, no disease gate)
("off-label"[tiab] OR "off label"[tiab] OR repurpos*[tiab] OR "compassionate use"[tiab]
  OR "n-of-1"[tiab] OR "drug repositioning"[tiab])
-> 738 records in the same window
```

Q5 ∪ Q6 ≈ **1,200 records per 5 weeks ≈ 35/day.** That is a tractable LLM-extraction volume. Do not try to run the full 5,000/day firehose through an LLM.

### Gotchas

- `"Rare Diseases"[MeSH]` recall problem (above). Fatal if you build on it.
- `[dp]` (date of publication) is the *journal* date and is wrong for detection — an article can publish with a 2027 date today. Use `[edat]` (Entrez date, when it entered PubMed) or `[crdt]`. Only `edat`/`crdt` are monotonic.
- Wildcards (`repurpos*`) are capped at 600 term expansions and silently truncate.
- Ahead-of-print records get re-dated when the final version posts; dedupe on PMID, not on date.
- E-utilities is stateful via `WebEnv` but History server entries expire; don't hold them across a long job.

### PubMed bulk (annual baseline + daily deltas)

**VERIFIED.** `https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/` and `https://ftp.ncbi.nlm.nih.gov/pubmed/updatefiles/`
File pattern `pubmed26nNNNN.xml.gz` (latest observed: `pubmed26n1563.xml.gz`). Baseline is refreshed each December; `updatefiles/` posts daily deltas including **deletions and revisions**. If you keep a local mirror, you must process `<DeleteCitation>` blocks or your corpus rots. Use `ftp.ncbi.nlm.nih.gov` over HTTPS — plain FTP is flaky.

---

## 2. PubMed Central Open Access subset — full text

**This changed in 2026 and most tooling in the wild is now broken. Read carefully.**

Per `https://ftp.ncbi.nlm.nih.gov/pub/pmc/readme.txt` (**VERIFIED**, updated 2026-04-10) and the NCBI Insights announcement of 2026-02-12:

- All legacy PMC dataset files were moved to a temporary `deprecated/` directory and **will be removed from the FTP service in August 2026** — i.e., now.
- `https://ftp.ncbi.nlm.nih.gov/pub/pmc/` today contains only `deprecated/`, `PMC-ids.csv.gz` (240 MB), and `readme.txt`. **VERIFIED.**
- `https://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/` → **404. VERIFIED.**
- `https://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_file_list.csv` → **404. VERIFIED.**
- **The OA Web Service API (`oa.fcgi`) is being retired.** It still answers today (**VERIFIED**, returns an `ftp://` tarball link for `PMC5543364`), but NLM has announced it "will no longer be available." Do not build on it.
- The old S3 prefixes `oa_comm/`, `oa_noncomm/`, `author_manuscript/`, `phe_timebound/` are retained only "for a transition period of 6 months." `oa_comm/xml/all/` already lists **zero keys. VERIFIED.**

### The go-forward path: `s3://pmc-oa-opendata`

**VERIFIED.** Anonymous, no credentials, no requester-pays. Add `--no-sign-request` to all `aws` commands. Also reachable over plain HTTPS at `https://pmc-oa-opendata.s3.amazonaws.com/<key>`.

New unified layout — one prefix per **article version**, ~8 million of them:

```
s3://pmc-oa-opendata/
├── PMC10009416.1/
│   ├── PMC10009416.1.xml      # JATS Z39.96-2015
│   ├── PMC10009416.1.txt      # plain text extracted from the XML
│   ├── PMC10009416.1.json     # core metadata
│   ├── PMC10009416.1.pdf      # when license permits
│   └── NPR2-43-85-g001.jpg    # figures/supplementary when license permits
├── metadata/
│   └── PMC10009416.1.json     # every metadata object, flat
├── inventory-reports/pmc-oa-opendata/metadata/   # daily S3 inventory, CSV
└── README.txt
```

**VERIFIED live**, e.g. `PMC10000000.1/` contains `.json`, `.pdf`, `.txt`, `.xml` plus 11 JPEGs.

The per-article JSON carries exactly the fields you need for filing triage: `pmcid`, `version`, `pmid`, `doi`, `title`, `citation`, `is_pmc_openaccess`, `is_manuscript`, `is_historical_ocr`, **`is_retracted`**, `license_code` (CC code, or `TDM` for author manuscripts), `xml_url`, `pdf_url`, `media_urls`, `text_url`. Every S3 URL in the JSON embeds an `md5` query param, so you get change detection for free.

### Incremental full-text sync — the pattern to implement

```bash
# 1. Find the latest daily inventory
aws s3 ls --no-sign-request \
  s3://pmc-oa-opendata/inventory-reports/pmc-oa-opendata/metadata/ \
  | awk '{print $2}' | grep -v hive | grep -v data | sort | tail -1
# -> e.g. 2026-01-18T01-00Z/

# 2. Read its manifest to get the CSV key
aws s3 cp --no-sign-request \
  s3://pmc-oa-opendata/inventory-reports/pmc-oa-opendata/metadata/2026-01-18T01-00Z/manifest.json - \
  | jq -r '.files[].key'

# 3. Pull the CSV: bucket, key, last-modified, ETag.
#    Diff ETag/last-modified against your local table -> exactly the changed articles.
```

Inventory regenerates **daily**, is retained **30 days**, and lags the live bucket slightly. Copy it out if you need history.

### Targeted retrieval (ESearch → S3), the NLM-blessed pattern

```bash
# Everything deposited in PMC on a given day that is in the OA/manuscript dataset
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pmc\
&term=2026/07/01:2026/08/05[pmcrdat]+AND+(open_access[Filter]+OR+author_manuscript[Filter])\
&retmode=json&retmax=10000&usehistory=y"

# then, per PMCID, resolve version(s):
aws s3api list-objects-v2 --no-sign-request --bucket pmc-oa-opendata \
  --prefix "PMC12810641." --delimiter "/" --query "CommonPrefixes[].Prefix" --output text
# -> PMC12810641.1/

# then fetch just the text (cheapest for LLM extraction):
aws s3 cp --no-sign-request s3://pmc-oa-opendata/PMC12810641.1/PMC12810641.1.txt -
```

License filters usable in that `esearch`, straight from the NLM README:

```
# commercial reuse permitted
(cc0_license[Filter] OR cc_by_license[Filter] OR cc_by-sa_license[Filter] OR cc_by-nd_license[Filter])
  AND (open_access[Filter] OR author_manuscript[Filter])

# non-commercial only  -- keep these in a separate bucket; they constrain what you may redistribute
(cc_by-nc_license[Filter] OR cc_by-nc-nd_license[Filter] OR cc_by-nc-sa_license[Filter])
  AND (open_access[Filter] OR author_manuscript[Filter])
```

### ID conversion

**VERIFIED.** Old `https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/` → **301**. New:
`https://pmc.ncbi.nlm.nih.gov/tools/idconv/api/v1/articles/?ids=42290712&format=json&tool=rdh&email=you@co.com`
All IDs in one call must be the **same type** (all PMIDs, or all DOIs — mixing errors out). Warns if `tool`/`email` are missing.

### Gotchas

- OA subset ≈ 20–25% of PMC and PMC ≈ a fraction of PubMed. **Full text will be missing for most of your candidate signals** — especially older case reports in small clinical journals, which is exactly your target stratum. Budget for abstract-only extraction plus publisher-permitted retrieval for the top-ranked candidates.
- COVID-era `phe_timebound` content had licenses expire; some PMCIDs were removed from bulk distribution. Track the removal list at `https://pmc.ncbi.nlm.nih.gov/about/covid-19-faq/#removed`.
- `is_retracted` is in the metadata JSON — check it before a filing decision, not after.
- Redistribution terms: acknowledge NLM, only redistribute what is licensed for redistribution, keep current or disclose staleness.

---

## 3. Europe PMC REST API

**VERIFIED.** Base: `https://www.ebi.ac.uk/europepmc/webservices/rest/`
No API key. No auth. No rate-limit headers returned (**VERIFIED** — none present). EBI's stated fair-use guidance is roughly 1 request/sec sustained; be polite and set a real User-Agent.

### Why it beats PubMed for this specific use case

1. **It searches full text, not just abstracts.** Your core problem is that "the abstract omits the drug/dose." Europe PMC indexes the body of every OA article. A PubMed `[tiab]` query structurally cannot find "the patient was started on sirolimus 0.8 mg/m² BID" if that sentence is in the Methods.
2. **It is a superset of PubMed** — MEDLINE plus preprints, patents, NHS guidelines, Agricola, and (critically) **conference abstracts and non-MEDLINE journals**.
3. **The Annotations API gives you free, pre-computed named-entity recognition** with ontology IDs — chemicals mapped to ChEBI, diseases, gene/proteins, organisms. This is a drug-name normalization layer you would otherwise have to build.
4. **`cursorMark` deep pagination** with no 10,000-record ceiling.
5. It exposes `PUB_TYPE`, and it exposes publisher-supplied types like `case-report` that PubMed sometimes lacks.

### Search

```bash
# Verified working: 171 hits
curl -sG 'https://www.ebi.ac.uk/europepmc/webservices/rest/search' \
  --data-urlencode 'query=sirolimus AND "lymphatic malformation" AND PUB_TYPE:"Case Reports"' \
  --data-urlencode 'format=json' --data-urlencode 'pageSize=25' --data-urlencode 'resultType=core'
```

```bash
# Incremental window — FIRST_PDATE range. Verified: 23 hits.
curl -sG 'https://www.ebi.ac.uk/europepmc/webservices/rest/search' \
  --data-urlencode 'query=(FIRST_PDATE:[2026-07-01 TO 2026-08-05]) AND PUB_TYPE:"Case Reports" AND "rare disease"' \
  --data-urlencode 'format=json' --data-urlencode 'resultType=core' --data-urlencode 'cursorMark=*' \
  --data-urlencode 'pageSize=1000'
```

Response gives `hitCount`, `nextCursorMark`, `nextPageUrl`. Loop on `nextCursorMark` until it stops changing.

Fields worth knowing: `PUB_TYPE`, `FIRST_PDATE`, `FIRST_IDATE`, `JOURNAL`, `ISSN`, `AUTH`, `AFF`, `GRANT_AGENCY`, `GRANT_ID`, `HAS_FT:Y`, `OPEN_ACCESS:Y`, `SRC:MED|PMC|PPR|AGR|CBA`, `IN_EPMC:Y`, `ABSTRACT:`, `TITLE:`, `METHODS:`, `RESULTS:` (section-scoped full-text search — **this is the killer feature**, e.g. `METHODS:"sirolimus"`).

`SRC:PPR` isolates preprints. `SRC:MED` is the PubMed-equivalent slice.

### Full text

```bash
curl -s 'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13260515/fullTextXML'   # VERIFIED 200
curl -s 'https://www.ebi.ac.uk/europepmc/webservices/rest/MED/42290712/references/1/json'
curl -s 'https://www.ebi.ac.uk/europepmc/webservices/rest/MED/42290712/citations/1/json'
curl -s 'https://www.ebi.ac.uk/europepmc/webservices/rest/MED/42290712/supplementaryFiles'
```

### Annotations API — use this for drug/disease extraction

```bash
curl -s 'https://www.ebi.ac.uk/europepmc/annotations_api/annotationsByArticleIds?articleIds=PMC%3APMC13260515&type=Chemicals&format=JSON'
```
**VERIFIED.** Returns, for a real pediatric lymphatic-malformation case report, annotations including:

```json
{"prefix":"by prolonged oral","exact":"sirolimus","postfix":"therapy for 2",
 "tags":[{"name":"sirolimus","uri":"http://purl.obolibrary.org/obo/CHEBI_9168"}],
 "type":"Chemicals","section":"Abstract","provider":"Europe PMC"}
```

That is your drug mention, with a ChEBI ID, with surrounding context, for free. Types available: `Chemicals`, `Diseases`, `Gene_Proteins`, `Organisms`, `Cell_Types`, `Accession Numbers`, `Gene Ontology`, `Experimental Methods`. ID format: `MED:<pmid>` or `PMC:PMC<id>`, semicolon-separated for batches (up to 8 IDs per call). There is also `annotationsByArticleIds` sibling `annotationsBySectionAndOrType` for whole-corpus sweeps.

Note: annotations exist only for articles Europe PMC has full text or a mined abstract for. `MED:28815119` returned an **empty** annotation array — absence is normal, not an error.

### Grants / funder data — GRIST

**VERIFIED**, but the URL form matters. Path-style works; query-string style 404s.

```bash
# WORKS
curl -s 'https://www.ebi.ac.uk/europepmc/GristAPI/rest/get/query=cystinosis&format=json&resultType=core'
# -> {"HitCount":"6", "RecordList":{"Record":[{"Person":{...},"Grant":{"Funder":{"Name":"Telethon Italy",...

# 404s
curl -s 'https://www.ebi.ac.uk/europepmc/webservices/rest/grantfinder?query=cystinosis&format=json'
```

Why you care: a Telethon/NIH/Wellcome grant on a rare disease is a **leading indicator** — grant awarded now, case report publishes in 18–36 months. GRIST lets you watch the funding pipeline for diseases in your portfolio and pre-position. You can also filter search results by `GRANT_AGENCY:"..."` in the main search API.

### Gotchas

- Europe PMC's `PUB_TYPE` includes publisher-supplied lowercase variants (`case-report`) alongside MEDLINE's (`Case Reports`). Query both.
- Field names are case-sensitive uppercase.
- `synonym=true` expands using MeSH/UniProt synonyms — very useful for drug name variants, but it inflates hit counts unpredictably. Turn it on deliberately, not by default.
- `resultType=lite` is the default and omits abstracts. You want `core`.

---

## 4. ClinicalTrials.gov API v2

**VERIFIED.** Base: `https://clinicaltrials.gov/api/v2`
Live check: `GET /api/v2/version` → `{"apiVersion":"2.0.5","dataTimestamp":"2026-08-05T09:00:06"}`. Data refreshes daily. No API key, no auth, no registration. Rate limits are not published; NLM throttles abusive clients — keep to a few requests/sec and set a User-Agent.

### Endpoints (all VERIFIED 200)

| Endpoint | Purpose |
|---|---|
| `GET /api/v2/studies` | Search. Paginated via `nextPageToken`. |
| `GET /api/v2/studies/{nctId}` | Single record, full protocol + results |
| `GET /api/v2/studies/metadata` | Complete field dictionary — generate your schema from this |
| `GET /api/v2/studies/search-areas` | Which fields each `query.*` param actually searches |
| `GET /api/v2/studies/enums` | Legal enum values (status, phase, sex, etc.) |
| `GET /api/v2/stats/size` | Corpus size stats |
| `GET /api/v2/version` | API version + data timestamp |
| `GET /api/rss?cond=...` | RSS feed of new/updated studies for a condition |

### Search syntax

```bash
curl -sG 'https://clinicaltrials.gov/api/v2/studies' \
  --data-urlencode 'query.cond=Rett Syndrome' \
  --data-urlencode 'query.intr=trofinetide' \
  --data-urlencode 'pageSize=100' --data-urlencode 'countTotal=true' \
  --data-urlencode 'fields=NCTId,BriefTitle,OverallStatus,Phase,EnrollmentCount,LeadSponsorName,Condition,InterventionName'
```
**VERIFIED** — returns nested `protocolSection` with exactly the requested modules:
```json
{"studies":[{"protocolSection":{
  "identificationModule":{"nctId":"NCT04988867","briefTitle":"An Open-Label Study of Trofinetide..."},
  "statusModule":{"overallStatus":"TERMINATED"},
  "sponsorCollaboratorsModule":{"leadSponsor":{"name":"ACADIA Pharmaceuticals Inc."}},
  "conditionsModule":{"conditions":["Rett Syndrome"]},
  "designModule":{"phases":["PHASE2","PHASE3"],"enrollmentInfo":{"count":15}},
  "armsInterventionsModule":{"interventions":[{"name":"Trofinetide"}]}}}],
 "nextPageToken":"ZVdj7o2Elu8o3lp2Wsy8sLL2mpOQJJxuZ_at2_IckA"}
```

**Incremental polling — the advanced filter is the important one:**

```bash
curl -sG 'https://clinicaltrials.gov/api/v2/studies' \
  --data-urlencode 'filter.advanced=AREA[LastUpdatePostDate]RANGE[2026-08-01,MAX]' \
  --data-urlencode 'query.cond=rare disease' \
  --data-urlencode 'countTotal=true' --data-urlencode 'pageSize=100' \
  --data-urlencode 'fields=NCTId,LastUpdatePostDate'
# VERIFIED -> {"totalCount":13,...,"lastUpdatePostDateStruct":{"date":"2026-08-03"}}
```

`AREA[...]` accepts any field from `/studies/metadata`. `RANGE[a,b]`, `MAX`, `MIN`, `EXPANSION[None|Term|Concept|Relaxation]`, `COVERAGE[FullMatch|StartsWith|EndsWith|Contains]`. Boolean `AND`/`OR`/`NOT` work inside `filter.advanced`. Other useful params: `filter.overallStatus=`, `filter.geo=distance(lat,lon,50mi)`, `filter.ids=`, `sort=LastUpdatePostDate:desc`, `postFilter.*`.

### Fields that matter for your signal

| Field | Why |
|---|---|
| `InterventionName`, `InterventionType`, `InterventionOtherName` | `InterventionOtherName` holds synonyms/brand names — essential for RxNorm mapping |
| `Condition`, `ConditionBrowseLeafName`, `ConditionBrowseBranchName` | CTG's own MeSH-mapped condition tree |
| `Phase` (`NA`, `EARLY_PHASE1`, `PHASE1`..`PHASE4`) | `NA` + drug intervention often = investigator-initiated repurposing |
| `EnrollmentCount` + `EnrollmentType` (`ACTUAL`/`ESTIMATED`) | Enrollment ≤ 30 + `ACTUAL` = your small-study stratum |
| `OverallStatus`, `WhyStopped` | `WhyStopped` free text is under-mined and very informative |
| `LeadSponsorName`, `LeadSponsorClass` (`OTHER`/`NIH`/`INDUSTRY`) | **`OTHER` = academic-sponsored = classic repurposing tell** |
| `StudyType` (`INTERVENTIONAL`/`OBSERVATIONAL`/`EXPANDED_ACCESS`) | **`EXPANDED_ACCESS` is a direct off-label-use signal** |
| `MinimumAge`/`MaximumAge`, `StdAge` (`CHILD`/`ADULT`/`OLDER_ADULT`) | Pediatric gate |
| `LocationCountry`, `LocationFacility` | Jurisdiction for filing |
| `HasResults`, `ResultsFirstPostDate`, `OutcomeMeasure*`, `PrimaryOutcome*` | Posted results = hard evidence |
| `IsFDARegulatedDrug`, `IsUnapprovedDevice`, `OrgStudyIdInfo` | Regulatory posture |
| `ReferencePMID`, `ReferenceType` (`BACKGROUND`/`RESULT`/`DERIVED`) | **Direct join key to your literature graph** |
| `LastUpdatePostDate`, `StudyFirstPostDate` | Watermarks for incremental sync |

### Bulk download

**VERIFIED.** Exactly one format is accepted:

```bash
curl -O -J 'https://clinicaltrials.gov/api/v2/studies/download?format=json.zip'
# -> HTTP 200, content-type: application/zip
# -> content-disposition: attachment; filename=ctg-studies.json.zip
# -> 1,108,562,183 bytes  (~1.11 GB), measured
```

**Any other parameter is rejected.** Measured error bodies:
- `format=csv` → `400 Allowed values for parameter 'format' are 'json.zip'`
- `format=json.zip&query.cond=Rett+Syndrome` → `400 Invalid prefix in parameter name: query.cond`
- `format=json.zip&filter.overallStatus=RECRUITING` → `400`

So: **the bulk endpoint is all-or-nothing.** Download the 1.11 GB zip weekly for a full local mirror; use `filter.advanced=AREA[LastUpdatePostDate]RANGE[...]` against `/studies` for daily deltas.

Legacy XML dump (**VERIFIED**, 301 → 200 `application/zip`):
`https://clinicaltrials.gov/AllPublicXML.zip` → redirects to `https://clinicaltrials.gov/api/legacy/public-xml?format=zip`

### Gotchas

- Response is deeply nested modules; `fields=` returns a *pruned tree*, not a flat object. Write a flattener once.
- `nextPageToken` is opaque and expires. Don't persist it across runs; re-query with a date watermark instead.
- Registered ≠ conducted ≠ published. Roughly half of registered trials never publish. Cross-reference `ReferencePMID` and, where absent, match on sponsor+intervention+condition against PubMed.
- Only "applicable clinical trials" are legally required to post results; a `HasResults=false` on an academic phase-2 means nothing.

---

## 5. WHO ICTRP

**VERIFIED (portal reachable).** `https://trialsearch.who.int/`

**What it is:** a metaregistry that harmonizes records from **19 primary registries** into one schema. Confirmed on the portal, data files imported **2026-08-03**. Feeder registries include: ANZCTR, ChiCTR, ClinicalTrials.gov, CTIS, EU-CTR, ISRCTN, ReBEC (Brazil), CTRI (India), CRiS (Korea), RPCEC (Cuba), DRKS (Germany), IRCT (Iran), jRCT/JPRN (Japan), PACTR (Pan-African), SLCTR (Sri Lanka), TCTR (Thailand), REPEC (Peru), LBCTR (Lebanon), ITMCTR (traditional medicine).

**Why it matters to you specifically:** ICTRP is the *only* practical single door to ANZCTR (which blocks direct scraping — see §7) and to the smaller registries. Its weekly harmonized export is worth more than any individual small registry integration.

**Access:**

| Route | Status |
|---|---|
| Web search portal, per-trial pages `/Trial2.aspx?TrialID=<ID>` | Free, **VERIFIED reachable** |
| Search-result **XML export** from the portal UI | Documented on the portal. UNVERIFIED programmatically. |
| **ICTRP Search Portal Web Service** (XML, real-time) | **Paid / on request.** WHO: "The cost charged by ICTRP for accessing the ICTRP web service can be provided upon request." Eligible users include research institutions; you apply and negotiate. **UNVERIFIED** (no public endpoint). |
| **ICTRP Crawling Service** | **Currently not available** (stated on the portal). |
| Full weekly dataset export | Exists via the "Downloading records from the ICTRP database" process under the WHO data-set docs; requires request/agreement. **UNVERIFIED** — I could not confirm a public file URL or the `ICTRPWeek*.zip` naming that circulates in older tooling. |

**Practical recommendation:** email ICTRP for the web service / dataset agreement (it is the correct legal path and the pricing is reportedly modest for research use). In the meantime, cover ~90% of ICTRP's value by integrating ClinicalTrials.gov + CTIS + EudraCT + ISRCTN + jRCT directly, and treat ICTRP as the gap-filler for ANZCTR/ChiCTR/CTRI/IRCT/DRKS.

**Gotcha:** ICTRP records are *snapshots* of the source registry, refreshed weekly, and are often staler and thinner than the source. Never treat ICTRP as authoritative if you can reach the primary registry.

---

## 6. EU CTIS and legacy EudraCT

### CTIS (Clinical Trials Information System) — the current EU system

**VERIFIED — and there is an undocumented-but-public JSON API that works.**

Public UI: `https://euclinicaltrials.eu/ctis-public/search`

**Search (POST only):**

```bash
curl -s -X POST 'https://euclinicaltrials.eu/ctis-public-api/search' \
  -H 'Content-Type: application/json' \
  -d '{"pagination":{"page":1,"size":50},
       "sort":{"property":"decisionDate","direction":"DESC"},
       "searchCriteria":{"medicalCondition":"asthma"}}'
```
**VERIFIED.** Returns `{"pagination":{"totalRecords":116,...},"data":[{"ctNumber":"2025-523307-29-00","ctStatus":2,"ctTitle":"...","shortTitle":"..."}]}`.
An empty `searchCriteria:{}` returns **12,156 total records** — the whole public CTIS corpus, walkable by pagination.

Criteria keys confirmed by probing: `medicalCondition` filters correctly (asthma → 116). `containAll` / `containAny` / `trialTitle` did **not** filter in my tests (`trialTitle:"asthma"` returned all 12,156 — i.e. silently ignored). **Validate every criteria key you use against a known-answer query; unknown keys fail open, not closed.** That is a serious silent-bug hazard.

**Retrieve a single trial:**
```bash
curl -s 'https://euclinicaltrials.eu/ctis-public-api/retrieve/2022-500014-26-00'
```
**VERIFIED 200.** Top-level keys: `ctNumber`, `ctStatus`, `startDateEU`, `decisionDate`, `publishDate`, `ctPublicStatusCode`, `authorizedApplication`, `events`, `results`, `documents`, `trialRegion`, `trialRegionCode`, `correctiveMeasures`. `authorizedApplication` contains the full protocol including products, conditions, sponsors, and per-member-state sites. `documents` links to public protocol/lay-summary PDFs.

**GET on `/search` returns `403 {"message":"Missing Authentication Token"}`. VERIFIED.** It must be POST. This is why most people conclude "CTIS has no API."

**Cadence:** CTIS publishes on a rolling basis with regulatory delays. Poll weekly, sort by `decisionDate` or `publishDate` descending, and watermark.

**Gotcha / posture:** this API backs the public portal and is not formally documented as a public API. It is unauthenticated public data, but it can change without notice and it has no SLA. Rate-limit yourself hard (≤1 req/sec), set an identifying User-Agent with a contact address, cache aggressively, and be prepared for schema drift. Check the portal's terms of use before scaling.

### EudraCT / EU-CTR — the legacy register

**VERIFIED.** `https://www.clinicaltrialsregister.eu/`

- Search UI: `https://www.clinicaltrialsregister.eu/ctr-search/search?query=cystinosis` → **200**
- **Bulk text export (this is the useful one):**
  `https://www.clinicaltrialsregister.eu/ctr-search/rest/download/full?query=cystinosis&mode=current_page` → **200 VERIFIED**
  `mode=all` pulls the whole result set. Output is a structured plain-text dump, one block per trial per member state. Parseable with a line-oriented parser; no JSON.
- No JSON/REST API. No API key.

**Why still bother:** EudraCT holds all EU trials registered **before 31 Jan 2023**, and legacy trials transitioned into CTIS only through 30 Jan 2025. Historical repurposing precedent for a rare pediatric indication in Europe lives here and nowhere else. Do a one-time full harvest, then check quarterly for results postings on old records.

**Gotcha:** one trial produces one record *per member state*, all sharing the EudraCT number. Deduplicate on the EudraCT number or you will 20x-count multinational trials.

---

## 7. Japan jRCT, India CTRI, China ChiCTR, ISRCTN, ANZCTR

### jRCT (Japan) — highest strategic value on this list

**VERIFIED.** `https://jrct.mhlw.go.jp/`

You are right that Japan matters disproportionately. Japan's Sakigake/orphan pathway and its domestic-approval-without-global-commercialization pattern means jRCT and the PMDA approval list contain drug–indication pairs that have *regulatory validation* and *zero Western commercial presence*. That is precisely the arbitrage.

| Item | Status |
|---|---|
| Search page | `https://jrct.mhlw.go.jp/search?language=en` → **200 VERIFIED** |
| Detail (Japanese) | `https://jrct.mhlw.go.jp/latest-detail/jRCT2031200153` → **200 VERIFIED** |
| Detail (English) | `https://jrct.mhlw.go.jp/en-latest-detail/jRCT2031200153` → **200 VERIFIED** |
| REST API | **None.** `/download` and `/search/csvdownload` both **404 VERIFIED** |
| CSV export | **Yes, via POST form.** The search form exposes `execDownload`, `download-count`, `in_download-count` fields (**VERIFIED** by parsing the form). It is a CakePHP form with CSRF: you must GET the search page, extract `_Token[fields]` and `_Token[unlocked]`, then POST with `button_type`/`execDownload`. |

Other form fields you can filter on (**VERIFIED** from the live form): `reg_plobrem_type` (condition), `reg_inter_contents_type` (intervention), `reg_recruitment[]`, `reg_classification[]`, `reg_is_specific[]`, `is_clinical_specific[]`, `reg_medical_product_type`, `reg_inclusion_criteria_type`, `reg_region`, `reg_research_num`, `count_start`/`count_end`, `language`.

ID prefixes: `jRCT1…` (specified regenerative medicine), `jRCT2…` (specified clinical trials, incl. off-label/unapproved use — **this is your bucket**), `jRCTs…` (studies with investigational products, `jRCTs0…` regenerative, `jRCTs1/2/3…` by region), `jRCTc…` (contract). Pre-2019 records live in the retired UMIN-CTR (`https://www.umin.ac.jp/ctr/`), JapicCTI, and JMACCT — mirrored into ICTRP as "JPRN".

**Recommended approach:** implement the CSRF-aware form POST for the CSV (stable, low volume, ~weekly), plus per-trial fetches of the `/en-latest-detail/` pages for the English text. English coverage is partial — many records have Japanese-only condition and outcome fields, so budget for JA→EN translation in your extraction step. Also mirror **PMDA** approval data separately; jRCT alone will not tell you a drug is already approved in Japan.

### CTRI (India)

**VERIFIED reachable.** `https://ctri.nic.in/Clinicaltrials/login.php` → 200; `https://ctri.nic.in/Clinicaltrials/advsearch.php` → 200.
No API. ASP-style form POST search; trial pages at `https://ctri.nic.in/Clinicaltrials/pmaindet2.php?EncHid=<hash>&Enc=&userName=`. The `EncHid` is an opaque encoded ID, so you must crawl from search results rather than enumerate. Site is slow and periodically down. **Recommendation: pull CTRI via ICTRP rather than scraping.** Value for your use case is moderate (large volume of generic-drug academic trials, but poor structure and inconsistent English).

### ChiCTR (China)

**VERIFIED reachable.** `https://www.chictr.org.cn/` → 200. `https://www.chictr.org.cn/searchproj.html?...` via GET → **405 Not Allowed (VERIFIED)** — search is POST-only.
No API. Bilingual records (Chinese + English). Registration numbers `ChiCTR<NNNNNNNNNN>`, detail at `/showproj.html?proj=<id>`. Heavy anti-bot posture and frequent layout changes. **Recommendation: ICTRP for coverage; direct scrape only if a specific disease shows Chinese-only evidence.** Value: real — a lot of pediatric generic-drug work publishes only in Chinese journals — but the retrieval cost is high and evidentiary weight for a filing is variable.

### ISRCTN (UK/international)

**VERIFIED — has a genuine, free, unauthenticated REST API.** Best-engineered registry on this list after CTGov.

```bash
curl -s 'https://www.isrctn.com/api/query/format/default?q=cystinosis&limit=100'
```
**VERIFIED** — returns XML: `<allTrials totalCount="1"><fullTrial><trial lastUpdated="2023-09-21T12:57:21Z" version="36" ...><isrctn>15626850</isrctn><trialDescription>...<title>Improvement of physical abilities in patients with cystinosis</title>...`

Query syntax supports fielded Lucene-ish terms and date ranges, e.g.
`?q=condition:cystinosis%20AND%20lastUpdated%20GT%202026-07-01T00:00:00Z&limit=100&offset=0`
Formats: `default`, `compact`, `full`, plus `/format/csv`. `lastUpdated` + `version` give you clean incremental sync. **Integrate directly — it's cheap.**

### ANZCTR (Australia/New Zealand)

**VERIFIED (blocked).** Every path returned **403** from this network, including `https://www.anzctr.org.au/`, `https://anzctr.org.au/`, `https://www.anzctr.org.au/TrialSearch.aspx?searchTxt=cystinosis&isBasic=True`, `https://www.anzctr.org.au/WebServices/AnzctrWebService.svc`, and even `/robots.txt` (which returned a styled HTML block page, i.e. a WAF interstitial, not a robots file).

ANZCTR historically exposed a SOAP web service at `/WebServices/AnzctrWebService.svc` and a per-trial page at `/Trial/Registration/TrialReview.aspx?id=<n>`. Both are behind the block from here — plausibly geo-fencing or a bot-mitigation rule. **UNVERIFIED whether the SOAP service still functions.**

**Recommendation: route ANZCTR through ICTRP.** If you need it directly, contact ANZCTR (they do grant data access for research) rather than fighting the WAF.

---

## 8. medRxiv / bioRxiv API

**VERIFIED.** Base: `https://api.biorxiv.org/` — free, no key, no auth.

```bash
# Details by date interval. 30 records per call; page with the cursor.
curl -s 'https://api.biorxiv.org/details/medrxiv/2026-07-01/2026-07-02/0'
# VERIFIED -> {"messages":[{"status":"ok","interval":"2026-07-01:2026-07-02","cursor":0,
#   "count":30,"count_new_papers":"170","total":"189"}], "collection":[{...}]}
```

Each record: `doi`, `title`, `authors`, `author_corresponding`, `author_corresponding_institution`, `date`, `version`, `type` (`new results` / `PUBLISHAHEADOFPRINT`), `license`, `category`, `jatsxml` (URL to full JATS XML), `abstract`, `published` (journal DOI once published).

| Endpoint | Pattern | Page size | Status |
|---|---|---|---|
| Details | `/details/{server}/{start}/{end}/{cursor}` | 30 | **VERIFIED** |
| Details by DOI | `/details/medrxiv/10.1101/2020.09.09.20191205` | — | **VERIFIED 200** |
| Preprint→published links | `/pubs/{server}/{start}/{end}/{cursor}` | 100 | **VERIFIED 200** |
| Published articles (bioRxiv) | `/pub/{interval}/{cursor}/{format}` | 100 | UNVERIFIED |
| By publisher prefix | `/publisher/{prefix}/{interval}/{cursor}` | 100 | UNVERIFIED |
| By funder ROR | `/funder/{server}/{interval}/{rorID}/{cursor}/{format}` | 100 | UNVERIFIED; data only from **2025-04-10** onward |
| Content stats | `/sum/{m\|y}/{format}` | — | UNVERIFIED |
| Usage stats | `/usage/{m\|y}/{server}/{format}` | — | UNVERIFIED |

Servers accepted: `biorxiv`, `medrxiv`. Interval forms: `YYYY-MM-DD/YYYY-MM-DD`, `N` (N most recent), `Nd` (last N days). Formats: `json`, `xml` (OAI-PMH), `html`, and `csv` on some endpoints. No published rate limits — be polite, ~1/sec.

**Gotchas**

- **The API has no keyword search.** You can only page by date/category. For a keyword-driven pipeline, either (a) ingest all medRxiv daily (~150–200/day, trivial) and index locally, or (b) search preprints via Europe PMC with `SRC:PPR`, which does support full-text query.
- Versions: the same DOI reappears with incremented `version`. Dedupe on `(doi, version)` and keep only the latest for scoring.
- `type: PUBLISHAHEADOFPRINT` records are journal-published; use `/pubs/` to link preprint DOI → published DOI so you don't double-count the same evidence.
- **medRxiv is the higher-value server for you** (clinical case reports and small trials); bioRxiv is mostly preclinical. But medRxiv explicitly discourages case reports in its screening policy, so yield is lower than you'd hope — treat it as a secondary stream and a leading indicator, not a primary one.
- Preprints are unrefereed. Weight accordingly in ranking, but do not discard: for ultra-rare diseases, a preprint may be the only public record for 18 months.

---

## 9. Cochrane Library

**VERIFIED (partially).** `https://www.cochranelibrary.com/` → 302 → 200. `https://www.cochranelibrary.com/en/search?q=cystinosis` → 302 → 200.

**There is no public API.** Wiley (the publisher) offers the **Cochrane Library API / CDSR content feeds under a commercial licence**; access is via Wiley's content-licensing team, not self-service. **UNVERIFIED** (no public endpoint to test).

What is accessible without a licence:

- **Abstracts and Plain Language Summaries of CDSR reviews are free worldwide.** Full reviews are free in many countries via national provisions (UK, Australia, India, most LMICs) and paywalled elsewhere.
- **Cochrane review DOIs are in Crossref** (prefix `10.1002/14651858.CD*`), so you can enumerate and monitor new/updated reviews via the Crossref API without touching Cochrane's site.
- **CDSR reviews are indexed in PubMed** — `"Cochrane Database Syst Rev"[ta]` — and in Europe PMC.
- **CENTRAL** (the Cochrane Central Register of Controlled Trials) is the genuinely unique asset: ~2M records including **hand-searched conference abstracts and trial reports that are not in PubMed**. CENTRAL is **not** freely downloadable in bulk and **not** available via API. It is licensed through Wiley.

Note: searching Crossref's journal endpoint for ISSN `1469-493X` returned only 3 works (**VERIFIED**) — the ISSN-based route is unreliable for Cochrane; use the DOI prefix `10.1002/14651858` instead.

**Recommendation.** Do not build on Cochrane for detection — it is a synthesis layer, not a primary-signal layer, and reviews lag primary literature by years. Its real value to you is twofold: (1) a Cochrane review of drug X in disease Y is strong *negative* evidence that the pair is novel/unclaimed; (2) **CENTRAL's conference-abstract coverage is the single best commercial answer to your §12 problem.** If you license one commercial dataset, license CENTRAL — it does the conference-abstract hand-searching you would otherwise have to do yourself.

---

## 10. OpenAlex, Semantic Scholar, Crossref, Lens.org

### OpenAlex — **it became metered in 2026. Check this before you build.**

**VERIFIED.** Base: `https://api.openalex.org`

Live response headers measured today on an unauthenticated request:
```
x-ratelimit-limit: 1000
x-ratelimit-limit-usd: 0.1
x-ratelimit-cost-usd: 0.0001
x-ratelimit-credits-used: 1
x-ratelimit-remaining: 989
x-ratelimit-reset: 2804
```
And from `https://developers.openalex.org/llms.txt` (**VERIFIED**):
```
Auth: api_key parameter (free at openalex.org/settings/api)
Rate limit: $1/day free usage with key, $0.01/day without
```

So, concretely, at $0.0001 per standard request:

| Tier | Effective daily budget |
|---|---|
| No key | ~**100 requests/day** |
| Free key (`api_key=`) | ~**10,000 requests/day** |
| Paid plan | higher limits + **monthly** snapshots |

**Get the free API key on day one.** The old "unlimited 100k/day polite pool with `mailto`" era is over; any tutorial telling you otherwise predates 2026.

Bulk snapshot — **VERIFIED**: `s3://openalex/` is public and anonymously listable; top level contains `LICENSE.txt`, `README.txt`, `RELEASE_NOTES.txt`, `browse.html`, `data/`, `legacy-data/`.
```bash
aws s3 sync --no-sign-request s3://openalex/data/works/ ./openalex/works/
```
CC0-licensed. **Quarterly** refresh on the free tier; monthly requires a paid plan.

Query example (**VERIFIED**, returns 18 hits):
```bash
curl -sG 'https://api.openalex.org/works' \
  --data-urlencode 'filter=type:review|article,from_publication_date:2026-07-01' \
  --data-urlencode 'search=sirolimus lymphatic malformation' \
  --data-urlencode 'per-page=200' --data-urlencode 'api_key=YOURKEY'
```
`search=` runs against **full text where available** (the response echoes `"fulltext.search"` in the query plan — confirmed live). Filters you'll use: `concepts.id`, `topics.id`, `referenced_works`, `cited_by_count`, `is_retracted`, `type`, `authorships.institutions.country_code`, `from_publication_date`, `from_updated_date` (for incremental sync). `cursor=*` for deep pagination; `group_by=` for facets.

**What OpenAlex is uniquely good for here:** the citation graph. Given a seed case report, `referenced_works` + `cited_by` gives you the local citation neighborhood, which is how you find the other 4 case reports of the same drug–disease pair scattered across 4 languages and 4 journals. That clustering is what converts a single anecdote into a filable pattern.

### Semantic Scholar

**VERIFIED.** Base: `https://api.semanticscholar.org/graph/v1`

- Unauthenticated is aggressively throttled: I got **`429 Too Many Requests`** on the 1st and again on a retry after 5s (**VERIFIED**). Practically ~1 req/sec shared across all anonymous users — unusable for production.
- API key: request at `https://www.semanticscholar.org/product/api#api-key-form`. Passed as the **`x-api-key` header**. Typical granted limits are 1 req/sec for the general pool, higher on justification. **UNVERIFIED** (I have no key).
- Bulk search: `GET /graph/v1/paper/search/bulk?query=...&fields=...` → **VERIFIED 200**. Returns up to 1,000/page with a continuation `token`, up to 10M matches. This is the endpoint to use, not `/paper/search`.
- **Datasets API — this is the real answer.** `https://api.semanticscholar.org/datasets/v1/release/latest` → **VERIFIED**, current release **`2026-07-28`**. Provides full downloadable corpus dumps (`papers`, `abstracts`, `citations`, `s2orc` full text, `tldrs`) with weekly incremental diffs. Requires an API key for the download links. Governed by AI2 Terms of Use.

**Distinctive value:** `s2orc` gives parsed full text with **inline citation contexts** (the sentence around each citation), and `tldrs` gives model-generated one-line summaries. Citation *context* is genuinely useful for your ranking — "cited as evidence of efficacy" reads differently from "cited as a counterexample."

### Crossref

**VERIFIED.** Base: `https://api.crossref.org` — free, no key, no registration.

```bash
curl -sG 'https://api.crossref.org/works' \
  --data-urlencode 'query.bibliographic=sirolimus lymphatic malformation case report' \
  --data-urlencode 'rows=1000' --data-urlencode 'select=DOI,title,type,created,container-title,ISSN' \
  --data-urlencode 'mailto=you@yourco.com'
# VERIFIED
```

- **Polite pool:** add `mailto=` (query param) or a `User-Agent` containing your contact. Puts you on faster infrastructure with better limits. Anonymous is best-effort with no guarantees. Crossref Plus (paid) gives a guaranteed pool and a token.
- Pagination: `rows` up to 1000; deep paging via `cursor=*` and `next-cursor` (offset is capped at 10,000).
- Incremental: `filter=from-index-date:2026-08-01` — indexes when Crossref *received* it, which is the right watermark for detection.
- Journal-scoped: `https://api.crossref.org/journals/{ISSN}/works` (**VERIFIED**).
- Bulk: public data file torrents (annual) plus the Metadata Plus subscription for monthly/real-time snapshots.

**Distinctive value:** Crossref sees a DOI **at deposit**, often days-to-weeks before PubMed indexes it, and it covers journals PubMed never indexes at all. For "small non-indexed literature," Crossref plus Europe PMC is the pairing that gets you there.

### Lens.org

**VERIFIED (blocked).** `POST https://api.lens.org/scholarly/search` → `401 {"message":"Missing/Incorrect Authorization Header","code":401}`. Endpoint confirmed live; requires `Authorization: Bearer <token>`.

- Access: free-for-non-commercial via institutional/academic application; **commercial use requires a paid subscription**, negotiated. Given you are a commercial entity filing IP, assume paid.
- **Why it may still be worth it for you specifically:** Lens is the only one of these four that unifies **scholarly works with patent records** in one query surface, including patent-to-literature citation links. For a repurposing-IP business, "has anyone already claimed drug X for disease Y, and what non-patent literature did the examiner cite" is a first-class question, and Lens answers it in one place. That is a different job from the other three.
- Query language is Elasticsearch-style JSON. Scholarly and patent indexes are separate endpoints (`/scholarly/search`, `/patent/search`).

---

## 11. Case-report-specific sources

The systematic answer: **case reports are identifiable by publication type and by journal, and both routes are queryable.**

### Route A — publication type, across all journals

```
PubMed:      "Case Reports"[pt]                    -> 6,290 in a 5-week window (VERIFIED)
Europe PMC:  PUB_TYPE:"Case Reports" OR PUB_TYPE:"case-report"   (VERIFIED)
```
Europe PMC's `core` result for a real BMJ Case Reports article returned `"pubTypeList":{"pubType":["Journal Article","Case Reports","case-report"]}` (**VERIFIED**) — note both the MEDLINE-cased and publisher-cased variants are present. Query both or you lose the publisher-supplied ones on non-MEDLINE journals.

### Route B — dedicated case-report journals, enumerated by ISSN

| Journal | ISSN | Verified access |
|---|---|---|
| **BMJ Case Reports** | **`1757-790X`** (NLM ID `101526291`) | **VERIFIED**: Europe PMC `JOURNAL:"BMJ Case Reports" AND (FIRST_PDATE:[2026-01-01 TO 2026-08-05])` → **1,011 records**, `isOpenAccess: Y` |
| **Journal of Medical Case Reports** | `1752-1947` | **VERIFIED**: Crossref `from-pub-date:2026-01-01` → **609 works**. Springer Nature, fully OA, in PMC. |
| *Cureus* | `2168-8184` | Fully OA, in PMC, enormous case-report volume |
| *Clinical Case Reports* (Wiley) | `2050-0904` | OA |
| *American Journal of Case Reports* | `1941-5923` | OA, in PMC |
| *Case Reports in Genetics / Pediatrics / Endocrinology* (Hindawi/Wiley) | various | OA series, IEM-heavy |
| *JIMD Reports* | `2192-8312` | **The single highest-yield journal for inborn errors of metabolism case reports.** OA, in PMC. |
| *Molecular Genetics and Metabolism Reports* | `2214-4269` | OA, IEM-focused |

**Trap I hit, so you don't:** Crossref returns **0 works** for BMJ Case Reports under ISSN `1757-1626` (**VERIFIED**) — that ISSN is stale/wrong and it appears in a lot of published tooling. The live ISSN is **`1757-790X`**. Always resolve a journal's ISSN from a live Europe PMC `resultType=core` record's `journalInfo.journal` block rather than from a reference list.

**Access posture:** BMJ Case Reports is **subscription/fellowship-based for reading** on bmj.com, but the great majority of its content is deposited in **PMC and Europe PMC as open access** (confirmed `isOpenAccess: Y` on the record I pulled). So harvest it from Europe PMC/PMC, not from bmj.com. JMCR, Cureus, AJCR, JIMD Reports are all fully OA and in the PMC S3 bucket — meaning **full text, not just abstracts**, which is exactly what you need for drug and dose extraction.

### Route C — the harvest query

```bash
# Systematic daily case-report harvest, full text where available, no MeSH dependency
curl -sG 'https://www.ebi.ac.uk/europepmc/webservices/rest/search' \
  --data-urlencode 'query=(PUB_TYPE:"Case Reports" OR PUB_TYPE:"case-report")
       AND (FIRST_PDATE:[2026-08-01 TO 2026-08-05])
       AND (HAS_FT:Y OR OPEN_ACCESS:Y)' \
  --data-urlencode 'resultType=core' --data-urlencode 'cursorMark=*' \
  --data-urlencode 'pageSize=1000' --data-urlencode 'format=json'
```
Then for each `pmcid`, pull `s3://pmc-oa-opendata/{PMCID}.1/{PMCID}.1.txt` — no rate limit, no throttling, plain text ready for the extractor.

---

## 12. Preprints and conference abstracts

You are right that this is where the only evidence often lives, and it is the weakest-covered layer. Honest assessment: **there is no comprehensive structured feed for rare-disease meeting abstracts.** Here is what actually exists, verified.

### What IS structured and harvestable

**ASH (American Society of Hematology) — fully solved.** ASH annual meeting abstracts publish as a *Blood* supplement with real DOIs and are in Crossref. Measured live via `https://api.crossref.org/journals/0006-4971/works` with November date filters:

| Year | Works dated November |
|---|---|
| 2023 | **7,507** |
| 2024 | **8,029** |
| 2025 | **8,332** |

DOI pattern `10.1182/blood-YYYY-NNNNNN` (**VERIFIED**, e.g. `10.1182/blood-2020-136763`, "COVID-19 Outcomes in Individuals with Sickle Cell Disease..."). So: harvest the November slice of ISSN `0006-4971` annually, ~8,000 abstracts, structured, free. That covers the hematology rare diseases (sickle cell, thalassemia, HLH, PNH, aHUS, congenital cytopenias, storage disorders with heme manifestations).

**SSIEM — mostly solved.** Abstracts publish as a supplement to the *Journal of Inherited Metabolic Disease* (ISSN `1573-2665`, **VERIFIED** via Crossref — 247 works since 2025 on the online ISSN). Harvest the annual supplement issue. This is your highest-value single conference for inborn errors of metabolism.

**ACMG — partially solved.** Abstracts appear in *Genetics in Medicine* (ISSN `1098-3600`, **VERIFIED**, 6,224 works in Crossref) and increasingly in *Genetics in Medicine Open* (`2949-7744`). Note ISSN `1530-0366` returns only 9 works (**VERIFIED**) — wrong ISSN, don't use it.

**The general pattern:** *most society meeting abstracts publish as a supplement issue of the society's journal, with DOIs, and are therefore in Crossref.* Build a table of `(society, journal ISSN, meeting month)` for your ~20 target societies and run a scheduled Crossref journal-scoped harvest against the supplement window. This is unglamorous but it works and it is the only scalable approach.

Societies worth putting in that table: SSIEM (JIMD), ACMG (Genet Med), ASH (Blood), SIMD, ICIEM, ESID/CIS (J Clin Immunol), WORLDSymposium (Mol Genet Metab — lysosomal, extremely high value), ASGCT (Mol Ther), ESHG (Eur J Hum Genet), AAN (Neurology), CNS/ICNA (Pediatr Neurol), ENDO/ESPE (Horm Res Paediatr), ASN/ERA (kidney), NORD and EURORDIS summits, FDA rare-disease workshops.

Also: **Orphanet Journal of Rare Diseases** (`1750-1172`, OA, in PMC) publishes many meeting-proceedings supplements — a single high-yield ISSN covering many small conferences.

**Crossref `type:proceedings-article`** — 919,155 records since 2025-01-01 (**VERIFIED**), but this is dominated by engineering/CS conferences and is a poor filter for biomedicine. Journal-supplement harvesting beats it.

### What is NOT structured

- Abstracts published only as a conference PDF booklet with no DOI (very common for smaller patient-organization and disease-foundation meetings — and these are often the ones with the single-patient n-of-1 result you most want).
- Poster content, which frequently contains dose and response detail absent from the 250-word abstract.
- Society meeting platforms behind member login.

**Realistic options for that tail:**
1. **License Embase.** Embase indexes ~2.9M conference abstracts from ~7,000 conferences and is the only comprehensive commercial source. Elsevier offers an API/data feed. This is the single highest-leverage purchase for your §12 gap.
2. **License Cochrane CENTRAL** (see §9) — its hand-searched trial reports include many conference abstracts PubMed lacks.
3. **Targeted crawl** of 15–25 disease-foundation and society sites, per-meeting PDF booklets, with a PDF-to-text and abstract-segmentation step. Perfectly tractable at that scale; do not attempt it generically.
4. **Preprints** via Europe PMC `SRC:PPR` (verified searchable, full text) and the medRxiv API.

Set your expectations: this layer will always be lower-recall and lower-structure than the journal layer. Treat it as a **precision-boost input** that raises confidence on candidate pairs surfaced elsewhere, not as an independent detection stream — with the exception of ASH/SSIEM/WORLDSymposium, which are structured enough to be primary.

---

# THE PIPELINE

## Design principle

Do not try to answer "did drug X help disease Y" with a query. **Queries produce a candidate stream; an extractor produces structured (drug, disease, outcome) triples; a scorer ranks them; a human decides.** The query layer's only job is to shrink 5,000 records/day into ~50/day of LLM-worthy candidates without losing the true positives.

The four measured constraints that shape everything:

1. **175,025 new PubMed records per 5 weeks** (~5,000/day) — too many to extract from.
2. **~75% of new records have no MeSH** — so the shrinking must be lexical, not ontological.
3. **Case reports are ~4% of the firehose** (6,290/175,025) — the `[pt]` filter alone is a 25x reduction.
4. **OA full text exists for a minority** — so the extractor must degrade gracefully to abstract-only.

## Layer 0 — Reference data, built once, refreshed monthly

Build these before writing a single crawler. Everything downstream keys off them.

**Disease dictionary → ORPHAcode.**
Source: Orphadata. **VERIFIED**: `https://api.orphadata.com/rd-cross-referencing/orphacodes/558?lang=en` → 200, CC-BY-4.0. Pull the full ORPHAcode set with all synonyms and cross-references (ICD-10/11, OMIM, UMLS, MeSH, MedDRA, GARD). ~6,500 rare diseases, ~30,000 synonym strings after expansion. Supplement with MONDO via OLS4 (**VERIFIED**: `https://www.ebi.ac.uk/ols4/api/search?q=Rett%20syndrome&ontology=mondo` → 200) for the cross-ontology mappings Orphanet lacks.
Store: `orphacode, canonical_name, synonyms[], mesh_ui, omim[], icd10[], prevalence_class, inheritance, age_of_onset[]`.
The `age_of_onset` field is your pediatric gate at the *disease* level — far more reliable than trying to infer patient age from text.

**Drug dictionary → RxCUI + UNII.**
**VERIFIED**: `https://rxnav.nlm.nih.gov/REST/rxcui.json?name=sirolimus` → `{"idGroup":{"rxnormId":["35302"]}}`; `https://rxnav.nlm.nih.gov/REST/rxcui/35302/allrelated.json` → all TTYs including brand names (`Rapamune`). Also **VERIFIED**: FDA GSRS `https://gsrs.ncats.nih.gov/api/v1/substances/search?q=sirolimus` → 200 (UNII, the FDA's authoritative substance identifier); openFDA `https://api.fda.gov/drug/ndc.json?search=generic_name:sirolimus` → 200.
Store: `rxcui, unii, canonical_name, brand_names[], atc[], chebi_id, is_generic_available, num_anda_holders, orange_book_patent_expiry, first_approval_date`.

**Critical: precompute the off-patent flag.** From the FDA Orange Book (patent and exclusivity files) plus openFDA NDC (count of distinct ANDA labelers). A drug with ≥3 ANDA holders and no unexpired Orange Book patent is unambiguously generic. **This flag is a hard pre-filter, not a ranking feature** — it eliminates the majority of drug mentions before they ever reach the extractor and it is the cheapest filter you have.

**ChEBI ↔ RxNorm bridge.** Europe PMC's annotations return ChEBI URIs (`CHEBI_9168` for sirolimus, verified). You need ChEBI→RxCUI to use them. Get it from UniChem or ChEMBL.

## Layer 1 — Ingestion (the actual cron schedule)

| # | Source | Endpoint | Cadence | Volume | Watermark |
|---|---|---|---|---|---|
| 1 | PubMed detection | `esearch` Q5 ∪ Q6, `datetype=edat&reldate=2` | **6h** | ~35/day | `edat` |
| 2 | PubMed firehose | `esearch` `"Case Reports"[pt]`, `reldate=2` | **daily** | ~180/day | `edat` |
| 3 | PubMed hydrate | `efetch` XML for new PMIDs | daily | — | — |
| 4 | Europe PMC full-text | `search` `PUB_TYPE` + `FIRST_PDATE` window, `resultType=core`, cursorMark | **daily** | ~300/day | `FIRST_PDATE` |
| 5 | EPMC annotations | `annotationsByArticleIds` batch of 8 | daily | — | — |
| 6 | PMC full text | `s3://pmc-oa-opendata/{PMCID}.{v}/{...}.txt` | on demand | — | md5 |
| 7 | PMC bulk sync | S3 daily inventory CSV diff | **daily** | ~4k changed/day | ETag |
| 8 | ClinicalTrials.gov | `filter.advanced=AREA[LastUpdatePostDate]RANGE[<wm>,MAX]` | **daily** | ~400/day | `LastUpdatePostDate` |
| 9 | CTGov full mirror | `/studies/download?format=json.zip` (1.11 GB) | **weekly** | — | — |
| 10 | CTIS | `POST /ctis-public-api/search` sorted `decisionDate` desc | **weekly** | ~50/wk | `publishDate` |
| 11 | EudraCT | `/ctr-search/rest/download/full?query=<disease>&mode=all` | **monthly** | — | — |
| 12 | ISRCTN | `/api/query/...&q=lastUpdated GT <wm>` | **weekly** | ~30/wk | `lastUpdated` |
| 13 | jRCT | CSRF form POST → CSV; then `/en-latest-detail/{id}` | **weekly** | ~100/wk | `jRCT` ID + update date |
| 14 | ICTRP | portal XML export (or licensed web service) — covers ANZCTR, ChiCTR, CTRI, IRCT, DRKS | **weekly** | — | import date |
| 15 | medRxiv | `/details/medrxiv/{N}d/0` | **daily** | ~180/day | `date` + `version` |
| 16 | Crossref | `filter=from-index-date:<wm>` + per-ISSN journal harvest | **daily** | — | `index-date` |
| 17 | OpenAlex | graph expansion on Tier-1 hits only (budget-metered) | **on demand** | ≤10k req/day | — |
| 18 | Conference | Crossref per-ISSN supplement harvest | **per meeting** | ~8k/yr ASH | — |
| 19 | PubMed backfill | Re-`efetch` every record 90d after first sight, to capture MeSH | **daily batch** | — | `first_seen + 90d` |

Job 19 is not optional. It is how you recover the 75% of records that arrive un-indexed, and it is what lets your recall improve retroactively.

## Layer 2 — Candidate reduction (lexical, cheap, before any LLM)

For each incoming record, in order, cheapest first:

1. **Disease gate.** Aho-Corasick match of the 30,000-string ORPHAcode synonym set against title + abstract + (full text if available). Require ≥1 hit. Rejects ~85% of the firehose. Prefer full-text matches in Title/Abstract/Discussion; ignore matches occurring only in the reference list.
2. **Pediatric gate.** Any of: ORPHAcode `age_of_onset` ∈ {neonatal, infancy, childhood, adolescence}; or `child[mh]`/`infant[mh]`/`adolescent[mh]`; or regex on age expressions (`\b\d+[- ](year|month|week|day)[- ]old\b`, `neonat`, `p[ae]ediatric`). Note the age regex is your workhorse pre-MeSH.
3. **Drug gate.** Match against the RxNorm/UNII dictionary (canonical + brand + synonym), **restricted to the `is_generic_available = true` subset**. Also accept ChEBI IDs from the Europe PMC annotation payload, bridged via UniChem. Require ≥1 hit.
4. **Study-type gate.** `"Case Reports"[pt]` OR `case-report` OR title/abstract match on `case report|case series|we report|we describe|n-of-1|compassionate use|expanded access|open-label|pilot study|retrospective (cohort|review)`.
5. **Outcome-language gate.** `improv|resolv|remission|normaliz|reduction in|response|benefit|efficac|amelior|stabiliz|reversal|cessation of (seizures|crises)` — deliberately loose. This gate exists to *rank*, not to reject; keep near-misses in a lower tier.

Measured expectation: 5,000/day → ~50–80/day reaching Layer 3.

## Layer 3 — Extraction (LLM, structured output, one record at a time)

Input: full text if in the PMC S3 bucket, else abstract + any Europe PMC annotations. Emit strict JSON, and **require a verbatim `evidence_span` for every field** — this is your defense against hallucinated dose/outcome data, which in your business is a filing-quality risk, not a nuisance.

```json
{
  "pmid": "42290712", "pmcid": "PMC13260515", "doi": "10.3389/fped.2026.1836317",
  "study_design": "case_report|case_series|open_label_trial|rct|retrospective_cohort|n_of_1",
  "n_patients": 1,
  "patients": [{"age_value": 7, "age_unit": "years", "sex": "F"}],
  "disease": {"text_as_written": "lymphatic malformation", "orphacode": null, "mesh_ui": null},
  "drugs": [{
     "text_as_written": "sirolimus", "rxcui": "35302", "unii": "W36ZG6FT64",
     "route": "oral", "dose_text": "0.8 mg/m2 BID", "duration_text": "2 years",
     "is_investigational_here": false,
     "evidence_span": "treated by prolonged oral sirolimus therapy for 2 years"
  }],
  "outcome": {
     "direction": "benefit|no_benefit|harm|mixed|unclear",
     "measure_text": "near-complete regression of the malformation on MRI",
     "quantified": true,
     "followup_text": "7-year follow-up",
     "adverse_events_text": null,
     "evidence_span": "..."
  },
  "off_label_stated": true,
  "prior_therapies_failed": ["bleomycin sclerotherapy"],
  "confidence": 0.0
}
```

Two hard rules: (a) any field without a verbatim `evidence_span` present in the source is dropped, not kept with low confidence; (b) `n_patients` must be extractable or the record goes to manual review — it is the single biggest driver of the score.

## Layer 4 — Normalization and deduplication

**Normalize.** `text_as_written` → RxCUI via RxNav `approximateTerm` (handles misspellings and non-US names — essential for Japanese and Chinese sources) → UNII via GSRS. Disease text → ORPHAcode via exact synonym match, then MONDO via OLS4, then embedding-nearest-neighbor over the ORPHAcode synonym set with a similarity floor and a human-review queue below it. **Log every unresolved string.** Your unresolved-string log is the highest-value input to improving the dictionary; review it weekly.

**Deduplicate at three levels.**

1. *Document:* union-find over `{PMID, PMCID, DOI, medRxiv DOI, NCT ID}`. Edges from: PMC ID converter (**VERIFIED** at `https://pmc.ncbi.nlm.nih.gov/tools/idconv/api/v1/articles/?ids=<pmids>&format=json&tool=&email=`), Europe PMC `fullTextIdList`, medRxiv `/pubs/` preprint→published links, CTGov `ReferencePMID`, Crossref DOI. One preprint + one published article + one registered trial + one conference abstract = **one** evidence node, not four.
2. *Patient:* the same patient is frequently reported in a case report and again in a later case series from the same center. Cluster on `(orphacode, rxcui, first_author_last_name OR institution, age±1, sex)`. Flag, don't auto-merge — surface it as "possible patient overlap" for human review. Getting this wrong inflates your n and corrupts the score.
3. *Pair:* collapse to the `(rxcui_or_unii, orphacode)` candidate pair. **The pair is the unit of decision, not the paper.**

## Layer 5 — Ranking

Score each `(drug, disease)` pair, not each paper:

```
score =  3.0 * log(1 + total_patients_with_benefit)
       + 2.0 * n_independent_centers            # independent replication dominates volume
       + 1.5 * has_quantified_objective_outcome
       + 1.5 * is_generic AND n_anda_holders >= 3
       + 1.5 * mechanistic_plausibility         # target-pathway link, ChEMBL/OpenTargets
       + 1.0 * pediatric_onset_disease
       + 1.0 * has_active_or_completed_registered_trial   # CTGov/CTIS/jRCT/ISRCTN join
       + 1.0 * orphan_prevalence < 1/100,000    # from Orphadata prevalence_class
       + 0.5 * recency_decay(most_recent_publication)
       + 0.5 * approved_in_JP_or_EU_not_US      # the jRCT/PMDA arbitrage
       - 3.0 * existing_approved_therapy_for_indication
       - 3.0 * prior_patent_claims_pair         # Lens/Google Patents check
       - 2.0 * contradicted_by_negative_report
       - 2.0 * n_patients == 1 AND n_centers == 1 AND no_followup
       - 5.0 * any_source_retracted             # PMC metadata is_retracted flag
```

Weights are a starting point. **Calibrate them against your own outcomes.** Once you have 50–100 human decisions logged (filed / didn't file / filed and it was already claimed), fit a logistic regression on the features and replace the hand-weights. Until then, hand-weights with a human in the loop.

**The two negative terms that matter most** are `prior_patent_claims_pair` and `existing_approved_therapy`. Both are cheap to check and both are the reason most high-scoring pairs are not filable. Check them *before* human review, not after — otherwise your reviewers spend their time on pairs that were dead on arrival.

## Layer 6 — Alerting

Emit a daily digest of pairs crossing a threshold, and — separately — **emit on state transitions**, which is where the real alpha is:

- A pair that had 1 report now has 2 from **independent centers** → sharp confidence jump.
- A pair that had only case reports now has a **registered trial** (any registry) → someone else noticed; clock is running.
- A pair with a trial that just posted **results**.
- A drug in your dictionary that just went generic (Orange Book patent expiry) where prior rare-disease case reports already exist → a pair that was unfilable yesterday and is filable today. **This is a scheduled re-scan of your existing corpus against a changed drug status, not a literature query at all** — and it is the highest-yield job in the whole system, because the corpus is already built and the signal is a calendar event.

## Build order

1. Layer 0 dictionaries + the off-patent flag. Nothing works without these.
2. PubMed + Europe PMC ingestion, jobs 1–5. Two weeks of data before you tune anything.
3. Lexical reduction (Layer 2). Measure the funnel at each gate against a hand-labeled set of 200 records; if any single gate is rejecting >95%, it's miscalibrated.
4. PMC S3 full-text sync (job 7) — this is what makes extraction good rather than mediocre.
5. LLM extraction + normalization + dedup.
6. ClinicalTrials.gov, then CTIS, then ISRCTN, then jRCT. In that order — that is descending order of (value ÷ integration cost).
7. Scoring, alerting, transition detection.
8. Only then: conference abstracts, Embase/CENTRAL licensing, Lens patent cross-check.

---

## Things that will break, ranked by likelihood

1. **PMC FTP legacy files are removed this month (August 2026).** Anything using `oa_bulk/`, `oa_file_list.csv`, or `oa_package/` tarballs is already broken. `oa.fcgi` is announced for retirement. Build on `s3://pmc-oa-opendata` with the new per-version prefix layout and the daily S3 inventory.
2. **OpenAlex is metered as of 2026** — $0.01/day without a key (~100 requests), $1/day with a free key (~10,000). Register the key.
3. **`"Rare Diseases"[MeSH]` has 15,927 records total.** Building recall on it is the most common and most fatal mistake in this domain.
4. **MeSH lags ~75% of new records.** Detection must be lexical; schedule the 90-day re-fetch.
5. **CTGov `/studies/download` accepts only `format=json.zip`** — no filters, 1.11 GB, all-or-nothing.
6. **CTIS search is POST-only** (GET → 403) **and unknown `searchCriteria` keys fail open**, silently returning the full corpus. Validate every key against a known-answer query.
7. **ANZCTR blocks direct access (403 on everything, including robots.txt).** Route via ICTRP.
8. **ICTRP's web service is paid and its crawling service is currently offline.** Don't design around free bulk ICTRP access without confirming terms first.
9. **BMJ Case Reports' ISSN is `1757-790X`.** The widely-copied `1757-1626` returns zero from Crossref.
10. **Europe PMC's GRIST grants API only works in path-style** (`/GristAPI/rest/get/query=...`); the query-string form 404s.
11. **Semantic Scholar returns 429 immediately without a key.** Get one, or use the Datasets API dumps.
12. **EudraCT emits one record per member state per trial.** Deduplicate on the EudraCT number.agentId: a43b1bd4526e0e262 (use SendMessage with to: 'a43b1bd4526e0e262', summary: '<5-10 word recap>' to continue this agent)
<usage>subagent_tokens: 186782
tool_uses: 81
duration_ms: 1132227</usage>