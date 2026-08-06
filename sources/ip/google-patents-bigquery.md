<!-- RECOVERED from subagent transcript agent-a0c3a42788a7a3528.jsonl, session fd64561f-7c90-41a2-95cf-b4a133a8fe0f, research date 2026-08-05.
     *** RECOVERED — HANDOFF §3 row 5b recorded these findings as LOST when the agent was killed. They were in the transcript. ***
     Verbatim agent deliverable — not re-edited. -->

# Google Patents Public Datasets on BigQuery — Verification Report
**Date of check: 2026-08-05. WebSearch unavailable; all findings from direct `curl` + a headless browser render of the Cloud Marketplace SPA.**

## 0. Method & the one hard limitation

- **No local tooling**: `which bq gcloud` → **`bq not found` / `gcloud not found`**; `~/.config/gcloud` does not exist. **No credentials of any kind on this machine.** No real query or dry-run was possible. I did not create a billing account or spend anything.
- **Unauthenticated BigQuery REST fails** — `curl "https://bigquery.googleapis.com/bigquery/v2/projects/patents-public-data/datasets"` → **HTTP 401**, `"Request is missing required authentication credential..."`, `"reason": "CREDENTIALS_MISSING"`. **BigQuery has no anonymous read path.** So *live* table-level existence/schema could not be confirmed by me.
- Consequently every claim below is one of: **VERIFIED-LIVE** (Google page fetched today), **VERIFIED-2018** (Google-authored table docs, but stale — see §5), or **UNVERIFIED**.

---

## 1. Project, datasets, tables

**`patents-public-data` is a real, distinct project — and it is NOT `bigquery-public-data`.**

- **VERIFIED-LIVE** — `https://cloud.google.com/bigquery/public-data` (HTTP 200): public datasets are *"available by default in BigQuery Studio in a project named `bigquery-public-data`"*. Patents data is **not** in that project; it has its own project, `patents-public-data`. You must always fully qualify: `` `patents-public-data.patents.publications` ``. It will **not** appear in the Explorer pane by default — you have to pin/add the project manually.
- **VERIFIED-LIVE** — the Marketplace SPA's own internal state on each product page renders the listing key as `patents-public-data:<product-slug>` (e.g. `patents-public-data:chembl`, `patents-public-data:uspto-oce-office-actions`), confirming the project ID is current and owns the listings.

### `patents-public-data.patents.publications` — EXISTS
**VERIFIED-2018** via `https://raw.githubusercontent.com/google/patents-public-data/master/tables/dataset_Google%20Patents%20Public%20Datasets.md` (HTTP 200):
> "Google Patents Public Data, provided by IFI CLAIMS Patent Services, is a worldwide bibliographic and US full-text dataset of patent publications." — Last updated 2018-11-26 | Rows 98,176,830 | **Size 899.4 GB**

**VERIFIED-LIVE** that the product still exists — Marketplace `.../product/google_patents_public_datasets/google-patents-public-data`: *"Cloud service: BigQuery / Expected update frequency: **Quarterly**"*.

Key schema fields (all VERIFIED-2018):

| Field | Type | Note |
|---|---|---|
| `publication_number` | STRING | **primary join key**, DOCDB style: `'US-7650331-B1'` |
| `application_number` | STRING | DOCDB style `'US-87124404-A'`; "may not always be set" |
| `family_id` | STRING | **simple family** — the correct FTO grouping unit |
| `country_code`, `kind_code`, `application_kind` | STRING | `A`=patent, `U`=utility, `P`=provisional, `W`=PCT, `F`=design, `T`=translation |
| `pct_number` | STRING | |
| `publication_date`, `filing_date`, `grant_date`, `priority_date` | INTEGER | **YYYYMMDD ints, not DATE**; `grant_date`=0 if not granted |
| `priority_claim` | RECORD REPEATED | |
| `title_localized`/`abstract_localized`/`claims_localized`/`description_localized` | RECORD REPEATED `.text`,`.language` | **claims & description are US-only**; description capped at first 9 MB |
| `inventor`, `assignee` | STRING REPEATED | raw |
| `inventor_harmonized`, `assignee_harmonized` | RECORD REPEATED `.name`,`.country_code` | use these for entity search |
| `cpc`, `ipc`, `uspc`, `fi` | RECORD REPEATED `.code`,`.inventive`,`.first`,`.tree` | |
| `examiner` | RECORD REPEATED `.name`,`.department`,`.level` | |

### Datasets inside `patents-public-data`
**VERIFIED-2018** — parsed from `tables/index.md` (HTTP 200, 61,959 bytes). **18 datasets**: `patents` (3), `google_patents_research` (3), `cpc` (2), `dsep` (1), `marec` (1), `usitc_investigations` (4), `worldbank_wdi` (1), `patentsview` (106), `uspto_oce_assignment` (14), `uspto_oce_cancer` (2), `uspto_oce_claims` (12), `uspto_oce_litigation` (10), `uspto_oce_office_actions` (5), `uspto_oce_pair` (20), `uspto_peds` (4), `uspto_ptab` (4), `ebi_chembl` (151), `ebi_surechembl` (4).

**VERIFIED-LIVE (today's authoritative list)** — browser render of `https://console.cloud.google.com/marketplace/browse?filter=partner:Google%20Patents%20Public%20Datasets` → **"21 results"**, filter facet **"Price: Free (21)"**. Product slugs extracted from the DOM: `chembl`, `cooperative-patent-classification`, `cpa-global-technical-standards-etsi`, `dsep`, `google-patents-public-data`, `google-patents-research-data`, `ifi-claims-patent-data-enrichments`, `marec`, `patentsview`, `surechembl`, `worldbank-wdi`, `ucb-fung-patent`, `usitc-investigations`, `uspto-oce-cancer`, `uspto-oce-office-actions`, `uspto-oce-assignment`, `uspto-oce-claims`, `uspto-oce-pair`, `uspto-oce-litigation`, `uspto-peds`, `uspto-ptab`.

⚠️ **Gotcha: 3 of the 21 products are NOT in the `patents-public-data` project.** **VERIFIED** from the repo's own generator configs (HTTP 200):
- `tools/dataset_ifi.json` → **`jefferson-1790:ifi_claims.xml`**, **`jefferson-1790:ifi_claims.publications`**
- `tools/dataset_berkeley_fung.json` → **`erudite-marker-539:JEMS16.*`**
- `tools/dataset_innography.json` → **`innography-174118:technical_standards.etsi`**

---

## 2. Tables that matter for pharma FTO

### Google Patents Research Data — **still alive**
`patents-public-data.google_patents_research.publications`
- **VERIFIED-LIVE** — Marketplace `.../google-patents-research-data`: *"...including machine translations of titles and abstracts from Google Translate, **embedding vectors**, extracted top terms, similar documents, and forward references."* / *"Expected update frequency: **Quarterly**"*. **This answers "is it still maintained": the listing is live and advertises quarterly refresh as of today.**
- **VERIFIED-2018** schema — the FTO-relevant fields: `publication_number` (joins 1:1, **100.00%, 98,176,830 rows** against `patents.publications`), `title`/`abstract` (English, possibly MT) + `*_translated` flags, `cpc` RECORD, **`cpc_low` / `cpc_inventive_low` STRING REPEATED** (flattened CPC+ancestors — much cheaper to filter on), **`top_terms` STRING REPEATED** ("top 10 salient terms"), **`similar` RECORD REPEATED**, **`cited_by` RECORD REPEATED** (forward citations), `url`, `country`, and **`embedding_v1` FLOAT REPEATED** — *"Machine-learned vector embedding... two documents that have similar technical content have a high dot product score... Trained on full text bag of words to predict CPCs using the WSABIE classification model."*

### EPO DOCDB / Espacenet — **DOES NOT EXIST**
- **VERIFIED (negative)**: no `espacenet`, `docdb`, or EPO product in the live 21-item Marketplace list; and `grep -oiE 'patents-public-data:[a-z0-9_]+\.[a-z0-9_]*(espacenet|docdb)...'` over `tables/index.md` returned **zero matches**. There is **no `patents-public-data.espacenet.*`**.
- Mitigation: `patents.publications` is *DOCDB-compatible* by construction (the `publication_number`/`application_number` docs both say "(DOCDB compatible)"), sourced from IFI CLAIMS. That is the DOCDB-equivalent bibliographic layer here.

### USPTO OCE — all five you asked about are REAL
**VERIFIED-LIVE** (each has a current Marketplace product) **+ VERIFIED-2018** (exact table names from `index.md`):

| Dataset | Tables | Live update freq / coverage |
|---|---|---|
| `uspto_oce_pair` | `application_data`, `transactions`, `continuity_parents`, `continuity_children`, `all_inventors`, `correspondence_address`, `event_codes`, `foreign_priority`, `status_codes`, `match` (+ `_2015` snapshots) | product = "USPTO OCE Patent Examination Research Data (PatEx)" |
| `uspto_oce_office_actions` | `office_actions`, **`rejections`**, `citations`, `match_app`, `match_pub` | **Annually**; *"4.4 million Office actions mailed during the **2008 to mid-2017** period... 2.2 million unique patent applications"* |
| `uspto_oce_claims` | `patent_claims_fulltext`, `pgpub_claims_fulltext`, `patent_claims_stats`, `patent_document_stats`, `pgpub_document_stats`, `match` (+ `_2014`) | |
| `uspto_oce_assignment` | `assignment`, `assignee`, `assignor`, `documentid`, `documentid_admin`, `assignment_conveyance`, `match` (+ `_2016`) | ownership chain |
| `uspto_peds` | `applications`, `match` (+ `_201710`) | **Quarterly**; *"bibliographic, published document and **patent term extension** data tabs in Public PAIR from 1981 to present"* |

`uspto_oce_litigation` (`cases`, `documents`, `names`, `attorneys`, `pacer_cases`) and `uspto_ptab` (`trials`, `match`) also exist.

### Chemical / sequence / bio
- **`ebi_surechembl`** — **the critical one for pharma.** Tables: **`ebi_surechembl.map`** and **`ebi_surechembl.match`** (+ `_201710`). **VERIFIED-2018**: `map` = 278,559,964 rows / 37.3 GB, columns `schembl_id`, **`smiles`**, **`inchi_key`**, `corpus_frequency`, `patent_id`, `publication_date`, `field`, `field_frequency`. `match` = 4,227,188 rows, columns `patent_id` → `publication_number`, joining to `patents.publications` at **99.73%**. That is your structure→patent bridge. **VERIFIED-LIVE**: *"Expected update frequency: **Quarterly**"*, license **CC BY-SA 3.0**.
- **`ebi_chembl`** — **version suffix is `_23` and `_24`** (e.g. `ebi_chembl.molecule_dictionary_24`, `compound_structures_24`, `activities_24`, `drug_indication_24`, **`product_patents_24`**, **`patent_use_codes_24`**, `target_dictionary_24`). **VERIFIED-2018** from `index.md` (151 tables, only `_23`/`_24` suffixes present). **VERIFIED-LIVE**: the ChEMBL Marketplace page still links documentation titled *"**ChEMBL 23 schema**"* / *"ChEMBL 23 schema diagram"* and says *"Expected update frequency: **Annually**"*. **Meanwhile upstream EBI is at `chembl_37`** — VERIFIED via `https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/releases/` (HTTP 200, listing `chembl_26`…**`chembl_37`**) and `.../latest/` (contains `chembl_37.sdf.gz`, `chembl_37_chemreps.txt.gz`). **So the BigQuery ChEMBL mirror is roughly 13 releases behind.** Whether a newer `_XX` suffix has quietly been added is **UNVERIFIED** (blocked by the 401).
- **Patent sequence data (DNA/protein) — NOT PRESENT.** **VERIFIED (negative)**: no `uspto_sequences` (or any sequence dataset) in the live 21-product list, and a regex for `*sequence*` over `index.md` returned **only** ChEMBL target-biology tables (`component_sequences_24`, `bio_component_sequences_24`, `variant_sequences_24`) — those are *protein target* sequences, **not** patent sequence listings. If your FTO pipeline needs sequence-listing claim coverage, **this data is not here** — source it elsewhere.

### Patent term / expiration / litigation
- **`uspto_peds.applications`** — best in-corpus source: **VERIFIED-LIVE** it carries the *"patent term extension data tabs in Public PAIR"*. PTE matters enormously for pharma.
- **`patentsview.us_term_of_grant`** (+ `_201708`) — **VERIFIED-2018** present in `index.md`.
- **`jefferson-1790:ifi_claims.publications`** — **VERIFIED-LIVE**: *"IFI CLAIMS Patent Data Enrichments includes standardized assignee/applicant names and **integrated legal status information**"*, *"Expected update frequency: **Weekly**"* — the freshest thing in the whole program, and the only real legal-status/alive-or-dead signal. ⚠️ but see licensing below.
- **`uspto_oce_litigation`** — **VERIFIED-LIVE**: *"74,623 unique district court cases filed during the period **1963-2015**"*. Ends in 2015; useless for recent ANDA/IPR activity. `uspto_ptab.trials` and `usitc_investigations` supplement it.
- **No Orange Book / Purple Book dataset exists** in this program (absent from the 21). `ebi_chembl.product_patents_24` is the nearest proxy and is ChEMBL-24 vintage.

---

## 3. Cost model
All **VERIFIED-LIVE** from `https://cloud.google.com/bigquery/pricing` (HTTP 200):

- **On-demand: `$6.25 / 1 tebibyte`**, quoted as *"Queries (on-demand) / 0 tebibyte to 1 tebibyte → **Free** per 1 month / account / 1 tebibyte and above → **$6.25 / 1 tebibyte**"*. Price is **per-region**; $6.25 is the US/EU-tier rate (appears 3× across region blocks). The `$9.125/TiB` figure on the page is **BigQuery Omni** (AWS/Azure regions) and `$312.50/TiB` is BigQuery ML contribution-analysis — neither applies to you.
- **Free tier: 1 TiB queries/month + 10 GiB storage/month.** *"Storage — The first 10 GiB per month is free. / Queries (analysis) — The first 1 TiB of query data processed per month is free."* Note it is **per billing account, not per project**.
- **Billing mechanics that will bite an FTO pipeline**: *"Charges are rounded up to the nearest MB, with a **minimum 10 MB data processed per table referenced** by the query, and with a minimum 10 MB per query"*; *"you're charged according to the data processed in the columns you select, **even if you set an explicit LIMIT**"*; cached results and errored queries are free; cancelling may still bill in full.
- **Public datasets are free to hold, not to read.** From `cloud.google.com/bigquery/public-data`: *"**Google pays for the storage of these datasets** and provides public access to the data using a project. **You pay only for the queries that you perform on the data.** The first 1 TB per month is free."* Also: *"You are charged for queries run against shared data. **The data owner is not charged** when their data is accessed."*
- **Egress**: batch `EXTRACT` to Cloud Storage is **free** (up to 50 TiB/day on the shared slot pool); Storage Read API streaming reads are **$1.10/TiB with the first 300 TiB/month free**; *"You are not charged for data extraction or data transfer when accessing query results in the Google Cloud console, BigQuery API, or any other clients."* Cross-region extracts bill under networking SKUs.

**Practical warning:** `patents.publications` was **899.4 GB in 2018** (≈0.878 TiB) and is certainly larger now. **A single `SELECT *` against it will consume — or exceed — your entire monthly free terabyte.** Column pruning is mandatory: `description_localized` / `claims_localized` are the bulk. Prefer `google_patents_research.cpc_low` for classification filters.

---

## 4. Can you query without a billing account? **YES.**
**VERIFIED-LIVE** from `https://cloud.google.com/bigquery/docs/sandbox` (HTTP 200):
> "The BigQuery sandbox lets you experience BigQuery **without providing a credit card or creating a billing account** for your project."

and from `cloud.google.com/bigquery/public-data`:
> "The first terabyte of data processed per month is free, so you can **start querying public datasets without enabling billing**."

Sandbox limits (verbatim):
- *"You are granted the same free usage limits as the BigQuery free tier, including **10 GB of active storage and 1 TB of processed query data each month**."*
- *"All BigQuery quotas and limits apply."*
- *"All tables, views, and partitions **automatically expire after 60 days**"* (default table expiration is forced on every dataset you create).
- **Unsupported**: *"Streaming data / **Data manipulation language (DML) statements** / BigQuery Data Transfer Service."*
- Explicitly supports querying public datasets (the doc's own walkthrough queries `bigquery-public-data.new_york.citibike_trips`).

**Implication for your pipeline:** read-only FTO queries against `patents-public-data` work fine in the sandbox. But **no DML** means no `INSERT`/`UPDATE`/`DELETE`/`MERGE` — you cannot incrementally maintain a results table. `CREATE TABLE AS SELECT` (DDL) is not on the unsupported list, but any table you materialize **self-destructs at 60 days**. For a production FTO pipeline you will want billing enabled (still $0 under 1 TiB/mo) purely to remove the 60-day expiry and unlock DML.

---

## 5. Gotchas

1. **The official docs repo is ARCHIVED.** **VERIFIED** — `https://api.github.com/repos/google/patents-public-data` → **`"archived": true`**, `pushed_at: 2024-06-17`. The last commit was **2024-03-13** ("Add Replicable Patent Indicators paper"), and **`tables/index.md` was last touched 2018-11-28**. Every row count, byte size and schema in §1–2 is **2018 vintage**. Treat it as a naming/shape reference, not as truth about current contents.
2. **Repo staleness ≠ dataset staleness — but verify per dataset.** The live Marketplace still advertises **Quarterly** for `patents`, `google_patents_research`, `surechembl`, `uspto_peds`; **Annually** for `chembl`, `uspto_oce_office_actions`, `uspto_oce_litigation`; **Weekly** only for `ifi_claims`. ⚠️ **VERIFIED-LIVE caveat from Google itself**: *"The **Last Updated date on a Cloud Marketplace dataset page indicates when the dataset page was last updated**. To find out when the data itself was last updated, see Accessing public datasets..."* — i.e. **"Expected update frequency" is a promise, not a measurement.** Once you have console access, check each table's **Last modified** field in its Details pane before trusting it.
3. **Hard evidence of real staleness in the pharma tables specifically**: ChEMBL mirror at `_24` vs upstream `chembl_37`; office actions end **mid-2017**; litigation ends **2015**. Meanwhile upstream SureChEMBL *is* actively maintained — `https://ftp.ebi.ac.uk/pub/databases/chembl/SureChEMBL/` (HTTP 200) shows `bulk_data/` **last modified 2026-08-04**, i.e. yesterday — so if the BigQuery SureChEMBL mirror has drifted, the fresh data is available directly from EBI's FTP as a fallback.
4. **Licensing is NOT uniform — this matters for a commercial FTO product.** All VERIFIED-LIVE from the respective Marketplace pages:
   - `patents.publications` → *"'Google Patents Public Data' by IFI CLAIMS Patent Services and Google is licensed under a **Creative Commons Attribution 4.0 International License**"* (CC BY 4.0 — permissive).
   - `google_patents_research.publications` → **CC BY 4.0**.
   - `ebi_surechembl` and `ebi_chembl` → *"used under **CC BY-SA 3.0**"* — **share-alike**. Derivative databases may inherit a copyleft obligation. Get counsel before shipping SureChEMBL-derived structures in a product.
   - USPTO OCE / PEDS / PTAB → *"by the USPTO, **for public use**"*.
   - `jefferson-1790:ifi_claims.*` → *"Terms of Service: **Varies, contact IFI CLAIMS for details.**"* — the freshest legal-status data is also the only one with **no open license**. Do not build a commercial dependency on it without an IFI agreement.
5. **`patents-public-data` vs `bigquery-public-data`**: different projects; patents data is only in the former; it won't auto-appear in Explorer; always fully qualify. Related: *"Public datasets are **not accessible by default from within a VPC Service Controls perimeter**"* and *"There is **no service-level agreement (SLA)** for the Public Dataset Program"* — both VERIFIED-LIVE. No SLA is a real consideration for a production pipeline.
6. **Snapshot-suffix convention**: dated copies sit beside the live table (`patents.publications_201710`, `publications_201802`, `uspto_peds.applications_201710`, `uspto_oce_pair.*_2015`, `ebi_surechembl.map_201710`). **Use a pinned dated snapshot for any FTO opinion you need to reproduce or defend later** — the unsuffixed table moves under you each quarter.
7. Dead links in the old docs: every "View in BigQuery" URL in the repo points at **`bigquery.cloud.google.com`**, which was retired years ago. Ignore them; use `console.cloud.google.com/bigquery`.

### What remains UNVERIFIED
- Current row counts, byte sizes, and live schemas of **every** table (blocked by HTTP 401 on the REST API; no `bq`/`gcloud`; no credentials).
- Whether `ebi_chembl` now carries a suffix newer than `_24`.
- Whether any sequence-listing or Espacenet/DOCDB dataset has been added since 2018 without a Marketplace listing (absence is verified only at the Marketplace-listing level, not the BigQuery-metadata level).
- IFI CLAIMS' own pages (`ificlaims.com`) returned **HTTP 403** to `curl` on all three URLs tried (bot protection), so their cadence/terms claims come from Google's Marketplace listing, not from IFI directly.