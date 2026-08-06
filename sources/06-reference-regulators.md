<!-- RECOVERED from subagent transcript agent-aa5d9490a029a8c09.jsonl, session fd64561f-7c90-41a2-95cf-b4a133a8fe0f, research date 2026-08-05.
     Japan PMDA, Australia TGA, UK MHRA, Swissmedic — machine-accessible approval databases.
     Verbatim agent deliverable — not re-edited. -->

Both agents are back. Here are the consolidated findings.

---

### 1. Japan PMDA

**Verification note:** all PMDA/MHLW/NIBIOHN URLs below were fetched directly by me and returned real content unless marked otherwise.

#### 1a. The single best English asset — "List of Approved Drugs"
- **URL:** `https://www.pmda.go.jp/files/000281190.pdf` — **VERIFIED** (HTTP 200, `application/pdf`, 3,206,009 bytes, **207 pages**)
- **Parent page:** `https://www.pmda.go.jp/english/review-services/reviews/approved-information/drugs/0002.html` — **VERIFIED**
- **Content:** "List of Approved Drugs, April 2004 to February 2026". Fully **English**. Columns: Review Category | Approval Date | No. | Brand Name (Applicant Company) | New Approval / Partial Change | Active Ingredient (*underlined = new active ingredient*) | Notes.
- **Why it matters:** the Notes column carries inline designation tags. Counted by me across the extracted text: **`[Orphan drug]` × 457**, `[Priority review]` × 106, `[Expedited review]` × 72, `[Public knowledge-based application]` × 27, `[SAKIGAKE designation]` × 5, `[Notification of off-label use]` × 13. Case variants exist (`[Orphan Drug]` × 18, `[Priority Review]` × 7) — normalise case.
- **Structure:** newest entries are grouped by month (`New Drugs Approved in May 2025`), older ones collapse to fiscal-year blocks (`FY 2014` … `FY 2012`).
- **Auth:** none. **Cadence:** roughly monthly.
- **GOTCHA — the file ID rotates on every update.** I confirmed via Wayback that this page served `/files/000248626.pdf` (Feb 2023) → `/files/000250463.pdf` (Mar 2023) → `/files/000281190.pdf` (now). **Never hardcode the `/files/NNNNNNNNN.pdf` path** — scrape `0002.html` for the current link each run.
- **GOTCHA:** it is a PDF with multi-line wrapped table cells. Simple text extraction merges adjacent approval rows. Use `pdfplumber`/`camelot` table extraction with explicit column boundaries, not naive `extract_text()`.

#### 1b. Fiscal-year approval lists — **XLSX exists (Japanese only)**
- **Index:** `https://www.pmda.go.jp/review-services/drug-reviews/review-information/p-drugs/0010.html` — **VERIFIED** (新医薬品の承認品目一覧)
- Per-fiscal-year pages FY2004→FY2026 with **non-sequential IDs** (FY2025=`0039.html`, FY2024=`0037.html`, FY2023=`0036.html`, FY2016=`0026.html`, FY2011=`0001.html`). Scrape the index for the mapping; do not compute it.
- **Each FY page carries a PDF *and* an XLSX.** Verified download: `https://www.pmda.go.jp/files/000277966.xlsx` — **VERIFIED** (HTTP 200, correct XLSX MIME, 32,825 bytes). Sheet `2025年度承認品目`, 143 rows × 7 cols.
- **Columns:** 分野 (review category) | 承認日 (approval date, `YYYY.M.D`) | No. | 販売名（会社名、法人番号）| 承認 (`承認`=new / `一変`=partial change) | 成分名（下線:新有効成分）| 効能・効果等 (indication)
- **Orphan status is inline** in the indication cell as `【希少疾病用医薬品】`. Verified example: Fabhalta/iptacopan for C3 glomerulopathy.
- **Bonus:** includes 法人番号 (Japanese corporate number) — a clean legal-entity join key.
- **This is the most machine-readable PMDA approvals source and it is Japanese-only.**

#### 1c. Review reports (shinsa hokokusho) in English
- **URL:** `https://www.pmda.go.jp/english/review-services/reviews/approved-information/drugs/0001.html` — **VERIFIED** (267,105 bytes)
- **It is NOT a search interface — it is one static HTML page** containing the entire A–Z table. One GET gets everything. 476 table rows, **954 PDF links**.
- **Columns:** Brand Name | Non-proprietary Name | Approved In | Review Report (EN) | Review Report (JP)
- **Counts I measured: 448 English reports, 423 Japanese, spanning 2007–2025.**
- English PDFs: `https://www.pmda.go.jp/files/000273006.pdf` — **VERIFIED** (57pp, Acenobel/aceneuramic acid). Japanese PDFs use a different pattern that **embeds the approval number**: `https://www.pmda.go.jp/drugs/2024/P20240527004/620095000_30600AMX00133_A100_1.pdf` — the `30600AMX00133` segment is the Japanese marketing approval number, useful as a join key.
- **GOTCHA:** every English report carries a disclaimer that it is reference-only and *"the Japanese original shall take precedence."*
- **GOTCHA:** only ~448 of the ~1,000s of Japanese approvals get an English translation — selected for novelty/priority. Coverage is biased toward new active ingredients, which happens to suit rare-disease work.

#### 1d. Orphan drug (kishoyaku, 希少疾病用医薬品) designation lists
This is the highest-value find, and the English/Japanese gap is severe.

- **English list:** `https://www.nibiohn.go.jp/activities/promote/documents/orphan_drug_E.pdf` — **VERIFIED** (HTTP 200, 1,415,820 bytes, **35 pages**)
  - Columns: Fiscal year of designation (Heisei) | Fiscal year | Date of designation | Designation number | Grant period | Name of drug designated | Anticipated indications | Applicant receiving designation | **Indications approved for marketing** | Applicant obtaining approval | **Date of approval** | Product approved | Trade name | **General name of active ingredient** | Notes | Date of revocation `<Status>`
  - It links **designation → approval** in one table, in English. Exactly the join you want.
- **Japanese list:** `https://www.nibiohn.go.jp/activities/promote/documents/hp_orphanlist_drug.pdf` — **VERIFIED** (1,018,315 bytes, 29pp, *"令和7年10月1日現在"* = current as of **2025-10-01**)
- **⚠️ CRITICAL GOTCHA — the English version is ~6 years stale.** I parsed both: **English tops out at designation #415 with latest dates ~2019; Japanese runs to #733 (Aug 2025).** That is a **~318-designation gap**. If you build on the English file you silently miss every orphan designation since 2019 — including most of the modern gene/enzyme-replacement wave. **Use the Japanese file as the source of truth and machine-translate.**
- **MHLW's own list (2020-09-01 onward only):** `https://www.mhlw.go.jp/content/11120000/001701020.pdf` — **VERIFIED** (419,481 bytes, 7pp, Japanese). Columns: 指定年度 | 指定日 | 指定番号 | 医薬品の名称 | 予定される効能又は効果 | 指定を受けた者 | 住所 | 備考.
- **MHLW parent page:** `https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000068484.html` — **VERIFIED**
- Companion lists: orphan **devices** `https://www.mhlw.go.jp/content/11120000/001679247.pdf`, orphan **regenerative products** `https://www.mhlw.go.jp/content/11120000/001698413.pdf` — both **UNVERIFIED** (hrefs extracted from the verified MHLW page; not downloaded).

#### 1e. Search databases — Japanese only
- **Index:** `https://www.pmda.go.jp/english/search_index.html` — **VERIFIED**
- **Prescription drug package inserts:** `https://www.pmda.go.jp/PmdaSearch/iyakuSearch/` — **VERIFIED** (Japanese: 医療用医薬品 添付文書等情報検索). Struts-style **POST** to `/PmdaSearch/iyakuSearch` with `nameWord`, `howtoMatchRadioValue`, `ListRows`, `dispColumnsList[N]`. No JSON API.
- Sibling DBs (all Japanese): `otcSearch/`, `ivdSearch/`, `kikiSearch/`, `saiseiSearch/`.
- **⚠️ English package inserts are effectively nonexistent.** `https://www.pmda.go.jp/english/safety/info-services/drugs/package-inserts/0001.html` — **VERIFIED**, and it lists exactly **6 products** (three Abbott enteral nutrition products, two Bracco contrast agents, one gadoteridol). **Do not plan around English SmPC-equivalents from PMDA — they don't exist.** Only review reports are translated.
- Detail-page URL patterns: `https://www.pmda.go.jp/PmdaSearch/iyakuDetail/GeneralList/{YJ-base}` (JA) and `.../ResultDataSetPDF/{co}_{YJcode}_{n}_{n}E` (EN, trailing `E`).

#### 1f. **How to programmatically identify Japan-only approvals**
Concrete, verified-source recipe:

1. **Build the Japan side.** Backbone = per-FY **XLSX** (§1b) for machine-readability and currency; enrich with the English PDF (§1a) for English ingredient/indication strings; flag orphans from `【希少疾病用医薬品】` (XLSX) or `[Orphan drug]` (PDF). Filter to rows where the ingredient is **underlined / described as "a drug with a new active ingredient"** — I measured **70 approval blocks that are both orphan-tagged and new-active-ingredient** in the current PDF.
2. **Build the US side.** openFDA — `https://api.fda.gov/drug/drugsfda.json?search=openfda.generic_name:"<INN>"` — **VERIFIED** (HTTP 200, returns `application/json` with `meta.results.total`). No key needed for low volume. Bulk: `https://download.open.fda.gov/drug/drugsfda/drug-drugsfda-0001-of-0001.json.zip` — **VERIFIED** (HTTP 200, `application/zip`, 9,376,614 bytes).
3. **Build the EU side.** EMA bulk XLSX — `https://www.ema.europa.eu/en/documents/report/medicines-output-medicines-report_en.xlsx` — **VERIFIED** (HTTP 200, 897,579 bytes, sheet `Medicine`, **2,739 rows**, regenerated `05/08/2026 - 18:00`). Columns include `Name of medicine`, `EMA product number`, `Medicine status`, **`International non-proprietary name`**, `Active substance`, `Therapeutic area (MeSH)`. Orphan companion: `.../medicines-output-orphan_designations-report_en.xlsx`. **Header is on row 9** — rows 1–8 are metadata.
4. **Join on INN / active ingredient**, not brand name. Anti-join Japan against (FDA ∪ EMA) → Japan-only candidates.

**Gotchas that will break this join:**
- Japan uses **JAN (Japanese Accepted Names)**, not always INN. Expect `-um` Latin endings, `(genetical recombination)` suffixes on biologics, and hydrate/salt forms baked into the name (`iptacopan hydrochloride hydrate` vs INN `iptacopan`). Strip salt/hydrate/recombinant qualifiers before matching.
- EMA's national/decentralised approvals are **not** in the centralised XLSX — a drug absent from EMA may still be approved in individual EU member states. The EMA file alone will over-report "Japan-only."
- `Change` (一変) rows are new **indications** for already-approved drugs — for a repurposing shop these are often *more* interesting than new molecules, but they are not "new approvals." Keep the `承認`/`一変` flag.
- Worked example this surfaces: **Acenobel / aceneuramic acid** (GNE myopathy, approved Japan 2024-03, English review report at `/files/000273006.pdf`) — approved in Japan, not US/EU.

---

### 2. Australia TGA

**⚠️ Access caveat, stated up front:** `www.tga.gov.au` was **completely unreachable** from this environment — `curl` timed out with 0 bytes on every attempt (`https://www.tga.gov.au/`, `/resources/artg`, `/resources/datasets`), and WebFetch timed out twice. This is almost certainly geo/WAF filtering of non-AU or datacenter egress. **All `www.tga.gov.au` page content below is marked VERIFIED-VIA-ARCHIVE**, meaning I confirmed it from Wayback Machine snapshots (mostly Oct–Nov 2025), not from the live host. **Budget for an AU-resident IP or proxy in production.** By contrast `www.ebs.tga.gov.au` responded normally.

#### 2a. ⚠️ **The premise is wrong: there is NO bulk ARTG extract on data.gov.au**
I checked this exhaustively and it is a negative finding:
- `https://data.gov.au/data/api/3/action/package_search?q=ARTG` — **VERIFIED**, `count: 1`, and the single hit is *"Australian Museum Annual Report 1930-1931"* (fuzzy false positive).
- `organization_list` — **VERIFIED**, 1,138 orgs, **no Therapeutic Goods Administration org exists**.
- `fq=organization:department-of-health` — **VERIFIED**, 37 datasets, all workforce/geography/aged-care/PBS. **No ARTG, no product register.**
- Note the CKAN API moved: it is `https://data.gov.au/data/api/3/action/...`. The bare `/api/3/...` path returns a Drupal 11 404.
- **Conclusion: state plainly — no ARTG bulk download is published on data.gov.au.** The nearest adjacent dataset is APVMA PUBCRIS (agvet chemicals, CSV) which is irrelevant to human medicines.

#### 2b. ARTG public search
- **URL:** `https://www.tga.gov.au/resources/artg` — **VERIFIED-VIA-ARCHIVE**
- It is a **Drupal Views exposed form + facets**, JS-hydrated. Exact patterns confirmed from the page's own markup:
  - Keyword: `/resources/artg?keywords=<term>`
  - Facet: `/resources/artg?f%5B0%5D=artg_product_type%3A1303` (i.e. `f[0]=artg_product_type:1303`)
  - Year facet: `f[0]=published:1994`
- **Register size (facet counts, Oct 2025):** Medical devices **61,864** · Medicines **34,519** · Other therapeutic goods 284 · Biologicals 50 → **~96,717 entries**.
- **No JSON/REST API is exposed.** The archived HTML contains no `drupalSettings` search endpoint and no `/views/ajax` handle. Treat as scrape-only.
- **Export path:** the **ARTG Search Visualisation Tool** (`https://www.tga.gov.au/resources/artg/artg-search-visualisation-tool` — **VERIFIED-VIA-ARCHIVE**) supports CSV/Excel export, but **full ARTG requires four separate exports**, one per therapeutic type. That is the de-facto bulk route.

#### 2c. eBusiness Services — the reachable, genuinely scrapable backend
- `https://www.ebs.tga.gov.au/` — **VERIFIED live** (HTTP 200). Lotus Domino app; page footer showed *"last updated: Thursday, 06 August 2026"*.
- **PI/CMI repository, browse by letter — VERIFIED live:**
  `https://www.ebs.tga.gov.au/ebs/picmi/picmirepository.nsf/PICMI?OpenForm&t=PI&k=N&r=/`
  Returns a clean HTML table: **Trade Name | PI link | Active Ingredient(s)**. `t=PI|CMI|` (blank = both), `k=` is `0-9`/`A-Z`.
- **Keyword search — VERIFIED live** (POST): `POST .../PICMI?OpenForm&Seq=1` with `t=PI&q=<term>`; returned *"Search PI Trade Names and Active Ingredients containing nitisinone. 2 Documents available."*
- **Document IDs are stable and semantic:** `CP-2013-PI-02370-1` (NAGLAZYME/galsulfase), `CP-2020-PI-02477-1`. PDF endpoint: `.../picmirepository.nsf/pdf?OpenAgent&id=<ID>`.
- **⚠️ GOTCHA — click-through licence gate.** That PDF URL returns **HTML, not PDF** (verified: `text/html`, 12,918 bytes): a *"Product and Consumer Medicine Information Licence"* acceptance form (`POST .../pdf?OpenAgent&Seq=1&Id=<ID>`, with a hidden `Remote_Addr` field). **I did not auto-accept it** — accepting a licence agreement on your behalf is your call, not mine. Read the licence terms and decide whether programmatic acceptance is permitted before building a scraper on this.

#### 2d. Orphan drug designations + Priority/Provisional determinations
- **URL:** `https://www.tga.gov.au/resources/designations-determinations` — **VERIFIED-VIA-ARCHIVE** ("Last updated 21 November 2025")
- Same Drupal facet URL pattern as ARTG.
- **Facet counts:** Orphan drug **206** + Orphan Drug **15** · Priority review **79** + Priority Review **8** · Provisional approval **48** · Provisional determination **32**. Outcome dates **2017–2025**.
- **Row shape:** `Notice for <ingredient> (<Sponsor>)` | outcome date | type. Verified rare-disease rows: idebenone (Chiesi, 2025-11-24), Coagulation Factor X human, SKY-0515, **leniolisib** (Pharming, 2025-10-24), sparsentan (Seqirus), hydroxycarbamide (Norgine), odevixibat (Ipsen).
- **GOTCHA — case-variant duplication in the facet vocabulary** ("Orphan drug" vs "Orphan Drug", "Priority review" vs "Priority Review"). Normalise or you undercount by ~7%.
- **GOTCHA — one product yields multiple rows.** leniolisib appears twice: once Orphan Drug, once Priority review. Designations are not 1:1 with products.

#### 2e. Prescription medicines registrations (new approvals)
- **URL:** `https://www.tga.gov.au/resources/prescription-medicines-registrations` — **VERIFIED-VIA-ARCHIVE** ("Last updated 28 November 2025")
- **Facets:** New generic medicine **735** · EOI (extension of indications) **488** · NCE/NBE **276** + `NCE/ NBE` **55** *(note the stray space — same normalisation bug)* · New biosimilar **42** · Biologicals 19 · New combination 8. Decision date 2025: 229.
- **EOI = extensions of indications** — for repurposing this is the single most relevant TGA facet.
- Pre-2018 registrations live on separate legacy pages, not in this dataset.

#### 2f. AusPAR
- **URL:** `https://www.tga.gov.au/resources/auspar` — **VERIFIED-VIA-ARCHIVE**. Same Drupal facet pattern, faceted by sponsor.
- **GOTCHA — sponsor strings are not normalised.** Verified adjacent variants in the facet list: `A. Menarini Australia Pty Ltd` vs `A Menarini Australia Pty Ltd`; `Amgen Australia Pty. Ltd.` vs `Amgen Australia Pty Ltd`; `Abbott Australasia Pty Ltd` vs `Abbott Australasia Pty Ltd (AbbVie Pty Ltd)`; `Alexion Pharmaceuticals Australasia` vs `...Australia`. Entity resolution required.

#### 2g. Comparable Overseas Regulator (COR) + Priority/Provisional pathways
- **COR country list — VERIFIED-VIA-ARCHIVE:** `https://www.tga.gov.au/products/medicines/prescription-medicines/list-countries-and-jurisdictions-determined-be-comparable-overseas-regulators-cors` (page states "Last updated 24 October 2019"). Determined by the Secretary under **subregulation 16DA(3), Therapeutic Goods Regulations 1990**:

  | Jurisdiction | Authority |
  |---|---|
  | Canada | Health Canada |
  | Japan | PMDA |
  | Singapore | HSA |
  | Switzerland | Swissmedic |
  | United Kingdom | MHRA |
  | United States | FDA |
  | European Union | EMA — **centralised *and* decentralised** processes |

- Supporting COR pages (all **VERIFIED-VIA-ARCHIVE** as existing URLs, under `.../prescription-medicines/application-and-market-authorisation/supply-prescription-medicine/application-process-prescription-medicines/`): `comparable-overseas-regulators`, `.../cors-requirements-indications`, `.../cors-submission-requirements`, `.../cors-timeframes-and-milestones`.
- Pathways: `.../apply-prescription-medicine-priority-review-pathway` and `.../apply-prescription-medicine-provisional-registration-pathway` — **VERIFIED-VIA-ARCHIVE** (URLs confirmed present in the archive index; page bodies not individually fetched).

#### 2h. Access Consortium & Project Orbis
- **Access Consortium hub — VERIFIED-VIA-ARCHIVE (URL exists):** `https://www.tga.gov.au/about-us/international-engagements/australia-canada-singapore-switzerland-united-kingdom-access-consortium`
  - Members: **Australia, Canada, Singapore, Switzerland, UK** (the EU left on Brexit).
  - Work-sharing sub-pages confirmed in the archive index: `.../access-consortium-new-active-substance-nas-work-sharing-initiative`, `.../access-consortium-biosimilars-work-sharing-initiative`, `.../access-generic-medicines-work-sharing-initiative`, plus a NAS Q&A page.
  - Strategic plan PDF: `http://www.tga.gov.au/sites/default/files/2022-09/access-consortium-strategic-plan-2021-2024.pdf` — **UNVERIFIED** (archive index entry only).
  - **Note the URL churn:** this content has lived at `/about-tga/international-engagements/...`, `/about-tga/international/...`, and now `/about-us/international-engagements/...`. Old links redirect inconsistently.
- **Project Orbis:** no TGA-hosted Orbis page surfaced in the archive index under the prefixes I searched — **UNVERIFIED at TGA**. (Swissmedic does host one; see §4.) Orbis is FDA-led oncology work-sharing with TGA, Health Canada, Swissmedic, MHRA, HSA, ANVISA, INVIMA.

---

### 3. UK MHRA

#### 3a. products.mhra.gov.uk — and the undocumented API behind it
- `https://products.mhra.gov.uk/` — **VERIFIED** (HTTP 200, 124,886 bytes). It is a **Next.js static export**; `pageProps` is `{}` on every route. `?search=` is read **client-side only**.
- **Scraping the HTML gets you nothing** — `/search?search=sirolimus`, `/product/?product=RAPAMUNE`, `/substance/?substance=SIROLIMUS` all return the same ~122 KB empty shell (**VERIFIED**). `sitemap.xml` — **VERIFIED**, contains only ~9 static routes, no product URLs. `robots.txt` — **VERIFIED**, `User-agent: *` with **no Disallow**.
- **The site's own frontend queries a public Azure Cognitive Search index using a read-only query key shipped in client-side JS** (found in `https://products.mhra.gov.uk/_next/static/chunks/843-012836701345ef2e.js` — **VERIFIED**):
  ```
  https://mhraproducts4853.search.windows.net/indexes/products-index/docs
    ?api-key=17CCFC430C1A78A169B392A35A99C49D
    &api-version=2017-11-11
    &search=sirolimus&$top=50&$count=true&queryType=full&searchMode=all
  ```
  **VERIFIED live** (HTTP 200, real JSON). This is **undocumented and unsupported** — MHRA can rotate the key without notice; it is a query key delivered to every browser, not a credential you were issued. Build a self-healing step that re-scrapes the JS chunk. Throttle: this is someone else's unmetered tier.
- **Corpus (VERIFIED via `$count=true`, 2026-08-05):** PIL 42,835 · SPC 24,582 · **PAR 11,557** → **78,974 docs**.
- **Doc schema:** `product_name`, `substance_name` (Collection), `pl_number` (Collection), `doc_type`, `title`, `file_name`, `created`, `territory`, `rev_label`, `metadata_storage_path` (direct blob PDF URL), `metadata_storage_name`.
- **Verified query capabilities:** `$filter=doc_type eq 'Par'`; `substance_name/any(s: s eq 'SIROLIMUS')`; `pl_number/any(...)`; `$orderby=created desc`; `facet=doc_type`; `$top=1000`; POST `/docs/search`; api-versions `2020-06-30`/`2023-11-01`/`2024-07-01` all work.
- **GOTCHA:** `created` is `Edm.String` and **NOT filterable** (verified error). Incremental sync must be `$orderby=created desc` + paginate to a watermark. `$skip` caps at **100,000** (corpus is 78,974 — full crawl = 79 requests, works today).
- **PDFs:** `https://mhraproducts4853.blob.core.windows.net/docs/<sha>` — **VERIFIED** (HTTP 200, `application/pdf`, 882,108 bytes). Container listing is **blocked** (404) — you must go through the index for hashes.
- **Dead:** `https://medicines.api.mhra.gov.uk/graphql` — **HTTP 503** on GET and POST. Decommissioned; still referenced in shipped JS. Don't build on it.

#### 3b. Public Assessment Reports (UKPARs)
- Live inside the same index: `$filter=doc_type eq 'Par'` → **11,557 PDFs**. PDF only, no structured extract; older ones are scans.
- **Coverage (from `https://products.mhra.gov.uk/about`, VERIFIED):** PARs for new MAs granted **after 30 Oct 2005**; **also published for all applications REFUSED after 1 April 2019** — a rare, high-signal source. Clinically significant variations are appended as **annexes**.
- **Parse `title`, not `file_name`.** `title` is reliably `<PRODUCT NAME> - <PL NUMBER>`; filenames are chaotic (`FIN APPROVED_PUB_Progit 50 mg film-coated tablets (PL 37039_0005).pdf`).
- **GOTCHA:** one PAR PDF often covers a **PL range** (`PL 00142_1316-18`) but is indexed once per PL → duplicate blob hashes. Dedupe on `metadata_storage_name`.
- `https://www.gov.uk/guidance/find-product-information-about-medicines` — **VERIFIED**. `https://www.gov.uk/guidance/public-assessment-reports-for-medicines` — **404, does not exist**; don't cite it.

#### 3c. "MHRA approvals" list — **does not exist**
Verified negatives: no MHRA statistics path (404); gov.uk Search API with `document_type=statistics` + MHRA → **`total: 0`**; `ckan.publishing.service.gov.uk` `q=MHRA` → **count 8**, all spend/FOI/Yellow Card — **no product or authorisation dataset on data.gov.uk**.

**Usable substitutes:**
- **Azure index as an approvals feed:** `$filter=doc_type eq 'Par'&$orderby=created desc`. **Same-day freshness** — verified docs created hours before the fetch (REMSIMA `PL 51808/0045`, 2026-08-05T09:31:50Z). ⚠️ `created` = publication, **not MA grant date**; re-versioned docs churn. Filter `rev_label`=1 to approximate genuinely new authorisations.
- **gov.uk Search API (JSON, no key) — VERIFIED:** `https://www.gov.uk/api/search.json?filter_organisations=medicines-and-healthcare-products-regulatory-agency&filter_content_store_document_type=press_release&order=-public_timestamp&count=100`. **584 MHRA press releases.** Notable approvals appear as *"MHRA approves X for Y"* — verified: donidalorsen (Dawnzera) for **hereditary angioedema** (2026-05-07), olezarsen (Tryngolza) for **familial chylomicronemia** (2026-04-10), first medicine for **APDS** (2024-09-27). **Heavily skewed to rare/notable drugs — well suited to your use case**, but not exhaustive (generics never announced).
- **Atom feed — VERIFIED:** `https://www.gov.uk/search/news-and-communications.atom?organisations%5B%5D=medicines-and-healthcare-products-regulatory-agency`
- **Content API — VERIFIED:** `https://www.gov.uk/api/content/<path>` returns `details.attachments[]` and **`details.change_history[]`** — free changelogs for diffing.
- **MHRA Performance Data — VERIFIED** (`https://www.gov.uk/government/publications/mhra-performance-data`, monthly, June 2026 data). **HTML tables only, no CSV.** KPI percentages, not volumes: national 100% ≤210 days; **IRP Route A 98% ≤60 days; Route B 98% ≤110 days**.

#### 3d. International Recognition Procedure (IRP) — exact rules
- **Canonical URL — VERIFIED:** `https://www.gov.uk/government/publications/international-recognition-procedure/international-recognition-procedure` (first published 2023-08-30; `public_updated_at` **2026-07-14**). `https://www.gov.uk/guidance/international-recognition-procedure` is a **404** — common miscitation.
- **Started 1 January 2024**, replacing the EC Decision Reliance Procedure.
- **⚠️ RULE CHANGE, 13 JULY 2026 — verbatim:** *"Reduction of the Route B reference approval window from 10 years to 5 years"* (Route A unchanged at 2 years), plus a single opportunity to respond to Validation Correction Requests and **8 weeks** advance notice for NAS submissions. **Transition ends 31 August 2026** — 26 days from today. Anything written before July 2026 saying "Recognition B = 10 years" is now wrong.

**Reference Regulators (7) — verbatim table:** Australia (TGA) · Canada (Health Canada) · Switzerland (Swissmedic) · Singapore (HSA) · Japan (PMDA) · United States (FDA) · **EU/EEA** (EMA *and* member-state competent authorities of EU, Norway, Iceland, Liechtenstein — centralised, MRP/DCP and national routes).

- **No chained reliance — verbatim:** *"the RR authorisation must have undergone a full and standalone review. RR assessments based on reliance or recognition of authorisations in another territory cannot be used."* Full **unredacted** RR assessment reports required, supplied by the applicant.

| | **Recognition A** | **Recognition B** |
|---|---|---|
| Timetable | **60 calendar days** | **110 calendar days** |
| Clock stop | **None** | **One at day 70**, up to 60 days to respond |
| RR approval age | within previous **2 years** | within previous **5 years** (was 10 pre-13 Jul 2026) |
| Entry | meets IRP criteria, triggers **no** B-criterion | triggers **any** of 24 B-criteria |
| Failure | reverts to **Recognition B** timeframe | CHM advice sought; reverts to **national 210-day** |

- **Hard cap:** RR authorisations **>5 years old are not eligible for IRP** — national route only.
- **Recognition B runs on a fixed monthly calendar** aligned to CHM meetings (verified 2026 rows, e.g. submission 09/04/2026 → start 23/04/2026 → CHM 26/06/2026 → day 70 02/07/2026). A validation slip **defers you a full month**.
- **The 24 Recognition B triggers include (full list verified):** conditional/exceptional-circumstances MA at RR or sought in UK; manufacturing sites/processes not assessed by RR; ERA or RMP not assessed by RR; RR-mandated PASS; **first-in-class NAS**; **single-arm pivotal data (#12)**; **real-world data (#13)**; **ATMP (#14)**; fractionated plasma; **proposal for orphan drug designation (#16)**; non-UK/EU comparator; OTC; uncertified device/IVD components; guidelines not adopted by MHRA; differing container/shelf life; novel excipient.
- **⚠️ For rare-disease repurposing you are almost always Recognition B.** Single-arm + RWD + orphan proposal (#12, #13, #16) each independently forces B. Budget **110 days + up to 60-day clock stop ≈ 170 days**, not 60.
- **⚠️ "Same product" — verbatim:** *"the same qualitative and quantitative composition ... the same pharmaceutical form and **the same therapeutic use**."* **A new (repurposed) indication is by definition not "the same product"**, so it cannot ride IRP on the original indication's foreign approval. IRP only helps once you/your group/licensor already hold the *repurposed* indication at an RR.
- **Explicitly out of scope:** traditional herbal, homoeopathic, **well-established-use bibliographic applications (Reg 54 HMRs)** — the classic repurposing route is barred; cancelled authorisations; emergency approvals; and anything previously refused/withdrawn nationally.
- **In scope:** Reg 50 (NAS *and* known actives), 51B generics, 52B hybrids, 53B biosimilars, 55 fixed combinations; plus post-auth line extensions, Type IB/II variations and renewals (A/B classification does not apply to variations).
- **Eligibility form** via online checker ≥8 weeks pre-submission; triage/NAS → `Recognition@mhra.gov.uk` ≥6 weeks, response in 10 working days. PL number needed first. `https://irp-eligibility.mhra.gov.uk/` — **UNVERIFIED (DNS does not resolve)**; reach the checker from the guidance page.

#### 3e. ILAP
- **VERIFIED:** `https://www.gov.uk/government/publications/innovative-licensing-and-access-pathway-ilap` (`public_updated_at` **2026-08-05 — today**) and `.../ilap-application-guidance`.
- Original ILAP launched Jan 2021, **paused and reformed**; relaunch announced 2025-01-30, first investigational products admitted 2025-10-14, latest cohort 2026-08-04. **Innovation Passport remains the mandatory entry point.**
- **Eligibility criterion 4 is a hard gate for repurposing:** safety in humans demonstrated but **confirmatory trials not yet started**. An old drug about to enter (or already in) a confirmatory trial is too late.
- **Rounds (VERIFIED):** R1 28 Apr–30 Jul 2026 (outcome 23 Oct 2026); **R2 4 Aug–4 Nov 2026** (outcome 4 Feb 2027) — **open now**; R3 9 Nov 2026–11 Feb 2027; R4 18 Feb–20 May 2027.
- Partners include **NICE, SMC, AWTTC, NHS England** — HTA bodies are inside the pathway.
- **Innovation Passport list — VERIFIED downloaded & parsed:** `https://assets.publishing.service.gov.uk/media/6a6cb3220ddb7e4831c62aef/Innovation_Passport_list_-_August_2026.xlsx` (17,958 bytes). Columns: Company | Product | Therapeutic Indication. **Only 6 products**, overwhelmingly rare disease (iECURE ECUR-506 for **OTC deficiency**; Solid Biosciences SGT-003 for **DMD**; Orchard OTL-201 for **MPS-IIIA**; CervoMed neflamapimod for **DLB**; BeOne BGB-B2033). ⚠️ **Publication is opt-in — this materially undercounts holders. Not a census.**
- Portal: `https://applyforaninnovationpassport.mhra.gov.uk/` — **VERIFIED**.

#### 3f. Downloadable UK lists that actually exist
| File | URL | Format | Rows | Cadence |
|---|---|---|---|---|
| **Orphan Register** | `https://assets.publishing.service.gov.uk/media/6a5a43b45ca06bf11ccb4407/Orphan_Register_Ver._3_July_2026.csv` — **VERIFIED** 68,679 B | CSV | **192** | ~monthly |
| **Expired Orphan Register** | `.../6a58cd8860a6e36813cb42f4/Expired_Orphan_Register_Ver._1_July_2026.csv` — **VERIFIED** 20,342 B | CSV | **58** | ad hoc |
| **Additional Monitoring** | `.../6a4fc6732467584757371ca8/Additional_Monitoring_JUNE_2026.xlsx` — **VERIFIED** 285,786 B | XLSX | ~1,587 | **monthly** |

- Orphan Register columns: `Product name | Active substance | Orphan Condition | OD Indication | Designation number | Orphan Market Exclusivity Expiry date`. Parent page `https://www.gov.uk/government/publications/orphan-registered-medicinal-products` — **VERIFIED**; its Content API **`change_history`** is the closest thing to an orphan-approvals change feed (verified entries: *"Addition of Reblozyl OD1 / Addition of Vyloy"* 2026-07-16).
- **GOTCHAs:** row 1 is prose — use `skiprows=1`; file is **not clean UTF-8** (mojibake — read as `cp1252`); dates `DD/MM/YYYY`; designation numbers use `/OD1`,`/OD2` suffixes so one PL can carry several.
- **Additional Monitoring XLSX** columns include `Reason for inclusion` (e.g. `New active substance`) + `Date added` — **the best structured proxy MHRA publishes for "recently authorised NAS".**
- **⚠️ UK orphan status is granted at MA decision time — there is no standalone pre-marketing UK orphan designation** (`https://www.gov.uk/guidance/orphan-medicinal-products-in-great-britain` — **VERIFIED**). Prevalence ≤5/10,000; exclusivity up to 10 yrs (+2 with PIP), reducible to 6. And per §3d criterion #16, **proposing orphan designation forces IRP into Recognition B** — orphan status and the fast IRP route are mutually exclusive.
- **Real bulk source is NHS dm+d, not MHRA:** `https://isd.digital.nhs.uk/trud/users/guest/filters/0/categories/6` — **VERIFIED**. Free registration + API key; weekly XML. But it is a *supply* catalogue — no PAR link, no MA grant date, no orphan status. Join on PL number.

#### 3g. Post-Brexit gotchas
- **From 1 Jan 2025 MHRA licenses UK-wide**; GB-only MAs no longer possible. **Existing PLGB MAs auto-converted to UK-wide but KEPT the `PLGB` prefix** — **a `PLGB` number in 2026 does NOT mean GB-only.** Don't infer territory from prefix.
- EU centrally-authorised products **no longer automatically cover Northern Ireland** from 1 Jan 2025.
- **Two grandfathering events** (EU CAP→PLGB on 2021-01-01, then PLGB→UK-wide on 2025-01-01) — **PL-number joins across the 2020/21 and 2024/25 boundaries will break.**
- `territory` field in the index is **stale**: UK 63,650 · GB 8,607 · **NI 48** · null 6,669. The site's own default filter treats null as UK. Don't rely on it.
- **⚠️ Most damaging gotcha: cancelled products vanish.** Verbatim from the MHRA site: *"Once a marketing authorisation has been cancelled, the product information will stay on the website for a year."* **The index is a snapshot, not an archive.** For a repurposing shop mining withdrawn/discontinued assets, **start archiving now** — withdrawn-product history is otherwise unrecoverable.
- MHRA's site does **not** hold EMA-centrally-authorised product info — you need EMA as a second source.
- **Watch:** draft **rare disease therapies regulatory framework** consultation — **VERIFIED** `https://www.gov.uk/api/content/government/consultations/draft-rare-disease-therapies-regulatory-framework`, opened 2026-05-21, **closed 2026-07-30 (outcome pending)**. Proposes an **Investigational Marketing Authorisation (IMA)** for *"extremely small patient populations ... individual- or family-specific genetic variants."* **The most consequential pending UK change for your business.**

---

### 4. Swissmedic

#### 4a. No public API
No REST/GraphQL. `/api`, `/api/v1`, `/services/api.html` → **404 (VERIFIED)**. Everything is static file drops. The only queryable surface is **opendata.swiss CKAN** (`https://opendata.swiss/api/3/action/package_search?q=swissmedic` → **VERIFIED**, `count: 7`), which returns metadata pointing at the same static files. **No change feed, no webhook — you diff monthly snapshots yourself.**

#### 4b. **Best source — OGD bulk XML (not linked from the lists page)**
- **URL:** `https://ogd.swissmedic.cloud/ogd-arzneimittel/Daten/OGD.zip` — **VERIFIED** (HTTP 200, 2,873,492 bytes, `last-modified: Fri, 31 Jul 2026`). **No auth, no click-through.**
- 10 XML files, 75.7 MB uncompressed, `EXPORT_DATUM 2026-07-31`:

| File | Records |
|---|---|
| `OGD-Praeparate.XML` | **7,965** (human 7,207 / vet 758) |
| `OGD-Sequenzen.XML` | 12,631 |
| `OGD-Packungen.XML` | 20,048 |
| `OGD-Deklarationen.XML` | 54 MB, full composition |
| `OGD-ATC-Codes.XML` | 2,219 (**English** descriptions) |
| + Stoff-Synonyme, Adressen, User-Defined-Codes (7,121 rows, 4 languages), Applikationsarten | |

- `<PRAEPARAT>` fields: `ZULASSUNGSNUMMER`, `PRAEPARATENAME`, `ARZNEIFORM`, `ATC_CODE`, `ZULASSUNGSSTATUS`, `ZULASSUNGSKATEGORIE`, `ZULASSUNGSINHABERIN`, `ERSTZULASSUNGSDATUM`, `ANWENDUNGSGEBIET`, `ABLAUFDATUM`, etc.
- XSDs + **English docs** at `https://ogd.swissmedic.cloud/ogd-arzneimittel/Beschreibungen/Beschreibungen_OGD_EN.pdf` — **VERIFIED** (12pp, contains the ER diagram).
- **Cadence:** regenerated the **1st of each month**, reflecting the **last day of the prior month**.
- **⚠️ Historical archive — the single most valuable asset here:** `https://ogd.swissmedic.cloud/ogd-arzneimittel/Archiv/` — **VERIFIED**, browsable index, **53 monthly snapshots `202202`→`202607`, contiguous except `202505` is missing**. A 4.5-year time series lets you reconstruct first-authorisation and indication-change events without scraping.
- **⚠️ GOTCHA:** Swissmedic's own docs say the archive naming is `.ZIP` (uppercase). **Actual files are lowercase `.zip`** — `OGD_202607.ZIP` → 404, `OGD_202202.zip` → 200 (both verified).
- **⚠️ There is NO orphan field anywhere in the OGD export** (verified by grepping all 10 files — every `orphan*` hit is a false positive from *Dextromethorphan* / *orphanum*). Orphan status lives only in the Excel file below.

#### 4c. Authorised medicines Excel lists
- **Landing page:** `https://www.swissmedic.ch/swissmedic/en/home/services/listen_neu.html` — **VERIFIED**
- **⚠️ HOST GOTCHA: `dam.swissmedic.ch` DOES NOT EXIST** (DNS failure, verified). The pattern is `https://www.swissmedic.ch/dam/...`. Tools that rewrite the relative `/dam/...` href into a `dam.swissmedic.ch` origin produce dead URLs. Same trap: the XML `schemaLocation` points at `ogd.swissmedic.ch`, which also doesn't resolve — the live host is `ogd.swissmedic.cloud`.

**Use this one — extended list:**
- `https://www.swissmedic.ch/dam/swissmedic/en/dokumente/internetlisten/erweiterte_ham_ind.xlsx.download.xlsx/erweiterte_ham_ind.xlsx` — **VERIFIED** (HTTP 200, 2,581,811 bytes, real XLSX)
- Sheet `Erweiterte Liste HAM`, **header row 7**, **11,066 data rows × 25 columns**, `Stand 31.07.2026`.
- Key columns: A `Zulassungsnummer` · D `Zulassungsinhaberin` · **G `Verfahren nach Art. 14 Abs. 1 Bst. abis-quater HMG`** (reliance flag) · **I `ATC-Code`** (95.7% populated) · **J `Erstzulassungsdatum`** (100% parseable, **1933-09-13 → 2026-07-30**) · O `Wirkstoff(e)` (Latin INN) · **R `Anwendungsgebiet`** (indication) · X `Zulassungsstatus` · Y time-limited indications.
- **⚠️ Grain = dosage strength, not product:** 11,066 rows ↔ only **6,762 distinct authorisation numbers**. Dedupe before counting.
- The basic list (`zugelassene_arzneimittel_ham_ind.xlsx...`, **VERIFIED**, 10 cols) is a strict subset — **ignore it**.
- Also on that page (paths verified in raw HTML): authorised packagings, Stoffliste, temporarily authorised, co-marketing, **`unterlagenschutz.xlsx` (data exclusivity — directly relevant to repurposing)**, IBP vaccines/blood, gene-tech substances.
- **Stale/abandoned:** `Verfahren.xlsx` (**VERIFIED**, `Stand 01.09.2020`, 4 rows) and `Gesuchseingaenge` (filename dated 2021).
- **⚠️ `ATC-Liste.xlsx` is misleadingly named** — **VERIFIED** as *"Allocation of ATC code to Regulatory Assessment"*: 242 rows mapping ATC groups to **named Swissmedic reviewers**. It is an internal workload roster, **not** an ATC dictionary and **not** product↔ATC data.

#### 4d. Orphan Drug status list — the key file
- **URL:** `https://www.swissmedic.ch/dam/swissmedic/en/dokumente/internetlisten/status_orphandrug_ham.xlsx.download.xlsx/Liste_OrphanDrug_Internet.xlsx` — **VERIFIED** (HTTP 200, **345,547 bytes**, real XLSX)
- Sheet `Orphan`, **header row 4**, **726 data rows × 11 columns**, `Stand 31.07.2026`.
- Columns: `Wirkstoff(e)` | `Gesuchstellerin/Zulassungsinhaberin` | **designated indication (Art.14 Abs.1 Bst.f HMG)** | **`Status verliehen am`** | **`Status entzogen/verzichtet am`** | `Zulassungsstatus` | **`Zulassungsnummer`** (join key) | `Bezeichnung` | `Zulassungsdatum` | `Befristete Zulassung bis` | **`Zugelassenes Anwendungsgebiet`** (authorised indication)
- **Stats:** 459 distinct active substances, 320 distinct authorisation numbers, designations **2005-04-19 → 2026-07-17**, **53 rows carry a withdrawal date**.
- **⚠️ 265 rows have blank `Zulassungsstatus` — designations with no Swiss authorisation yet. That is your whitespace list.** (Zugelassen 442 / blank 265 / Befristet 19.)
- **⚠️ Grain = substance × designated indication × authorisation number** — acalabrutinib appears for both Waldenström and CLL/SLL under the same Zul.-Nr. Never count rows as "number of orphan drugs."
- **Columns 3 vs 11 diverge** — designated indication is often broader than what reached the label. For repurposing, col 3 = designation scope, col 11 = actual label.

#### 4e. SwissPAR
- **Index:** `https://www.swissmedic.ch/swissmedic/en/home/humanarzneimittel/authorisations/swisspar.html` — **VERIFIED** (231,924 bytes). **One static page, all A–Z sections, no pagination, no JS — one GET yields 388 SwissPAR PDF links.**
- **English only** — the only substantial natively-English Swissmedic assessment content.
- **Coverage:** human medicines with **new active substances**, transplant products, **both approved and rejected** applications, plus supplementary reports for **additional indications** (directly useful repurposing precedent).
- **Filename convention is fully machine-parseable** (355/388 parsed cleanly):
  `/dam/swissmedic/en/dokumente/zulassung/swisspar/{Zulassungsnummer}-{product}-{NN}-swisspar-{YYYYMMDD}.pdf.download.pdf/{free-form}.pdf`
  → authorisation number, **sequence (`01`=initial, `02`=indication extension)** and date without opening the PDF.
- 270 distinct authorisation numbers; by year 2019:2 · 2020:24 · 2021:35 · 2022:54 · 2023:38 · 2024:65 · 2025:79 · 2026:55.
- Verified download: `.../69592-reblozyl-01-swisspar-20260716.pdf.download.pdf/SwissPAR_Reblozyl.pdf` (726,551 bytes).
- **Gotchas:** trailing filename segment is free-form/inconsistently encoded; product slug case varies (`Cablivi`/`cablivi`); two entries have malformed dates (`2027xxxx`, `2408xxxx`) — validate.
- **Public Summary SwissPAR** (lay summaries) is separate and **HTML, not PDF**: `https://www.swissmedic.ch/swissmedic/en/home/humanarzneimittel/authorisations/public-summary-swisspar.html` — **VERIFIED**, 362 sub-page links, zero PDFs.

#### 4f. MAGHP
- **URL:** `https://www.swissmedic.ch/swissmedic/en/home/about-us/development-cooperation/marketing-authorisation-for-global-health-products.html` — **VERIFIED**. Note it sits under **about-us/development-cooperation**, not under authorisations — easy to miss.
- Accelerates access in **low- and middle-income countries** (World Bank definition), emphasis sub-Saharan Africa. Covers NAS, known actives and biosimilars. **NRAs of recipient countries participate in the assessment**; joint scientific advice with WHO available.
- Procedure guidance: `https://www.swissmedic.ch/dam/swissmedic/en/dokumente/stab/networking/maghp_procedure.pdf.download.pdf/maghp_procedure.pdf` — **VERIFIED** (623,725 bytes, 18pp, doc ID `ZL000_00_047e_WL`).
- **Relevance caveat: MAGHP is a global-health/LMIC instrument, not a rare-disease route and not a reliance shortcut. There is no published list of MAGHP-approved products.**

#### 4g. Reliance / foreign-decision routes — exposed as structured data
The extended list's column G quantifies Swiss reliance across 11,066 rows:

| Value | Rows |
|---|---|
| *(blank — ordinary full procedure)* | 10,947 |
| `Art. 14 Abs. 1 Bst. abis HMG` — authorised in **EU/EFTA** | **113** |
| `Bst. aquater` — cantonal authorisation | 4 |
| **`Bst. ater` — long-standing medical use abroad** | **2** |

- **`Bst. ater` is Switzerland's closest codified analogue to a well-established-use/repurposing route, and only 2 products currently carry it.** That scarcity is itself the finding.
- **Art. 13 TPA** (consideration of a foreign assessment) guidance: `https://www.swissmedic.ch/swissmedic/en/home/humanarzneimittel/authorisations/information/anpassung-wl-ham-art-13.html` — **VERIFIED** (updated 01.03.2026).
- **International procedures hub — VERIFIED:** `https://www.swissmedic.ch/swissmedic/en/home/humanarzneimittel/authorisations/internationale-zlverfahren-link.html`, linking Access Consortium, **Project Orbis**, EMA OPEN and MAGHP.

#### 4h. Other Swiss sources
- **New authorisations by year:** `https://www.swissmedic.ch/swissmedic/en/home/humanarzneimittel/authorisations/new-medicines.html` — **VERIFIED**. ~75 per-product HTML sub-pages, heavily rare-disease (Ezmekly, Agamree, Qalsody, Voxzogo, Filsuvez, Bylvay, Yorvipath). **HTML only, no export.**
- **AIPS full label text (SmPC + patient info) in bulk XML:** `https://download.swissmedicinfo.ch/` — **VERIFIED**. Operated by **Refdata, not Swissmedic**. **⚠️ Behind a click-through "Terms of use" consent interstitial** — a naive GET returns the landing page. **Refdata asserts copyright — clear licensing before redistribution.** Format changed 2025-08-28 to carry URLs rather than embedded text.
- **Swissmedic Journal:** monthly PDF, **German and French only**. Verified sample: `.../swissmedic-journal-2026-05.pdf.download.pdf/...` (735,898 bytes).
- **⚠️ opendata.swiss record declares `license_title: None`** — no licence stated. Genuine legal gotcha for commercial redistribution.

#### 4i. **⚠️ The biggest Swiss language trap**
The `/en/`, `/de/`, `/fr/`, `/it/` segment in `dam` URLs is **purely cosmetic for the XLSX files**. The orphan list was downloaded from all four language paths and all four returned **345,547 bytes with identical MD5 `da57a62ad3cc70d26c390fc95495cac1`**. **Fetching the `/en/` URL does not get you an English file.** Every Excel list is German/French regardless of path — headers are bilingual DE/FR *inside a single cell*, newline-separated, with soft hyphens. Only **SwissPAR** (and the OGD ATC codes / UDC labels) are genuinely English.

---

### Cross-cutting summary

**Where a real bulk download exists:** Swissmedic OGD XML (+53-month archive) · PMDA per-FY XLSX (JA) · MHRA Azure index (undocumented) · EMA XLSX · openFDA ZIP.
**Where it does not:** **no ARTG bulk extract on data.gov.au** (premise disproved) · no MHRA approvals register · no Swissmedic API · no PMDA API.
**Best orphan/rare-disease signals:** MHLW/NIBIOHN Japanese orphan list (733 designations) · Swissmedic orphan XLSX (**265 designated-but-unapproved**) · TGA designations (221 orphan) · MHRA Orphan Register CSV (192).
**Two things to act on now:** MHRA IRP Route B reference window drops 10→5 years when transition closes **31 Aug 2026**; and **start archiving the MHRA index immediately** — cancelled UK products are deleted after 12 months and are otherwise unrecoverable.

**Two caveats on my own coverage:** all `www.tga.gov.au` content is archive-verified, not live-verified, because the host is unreachable from this network; and I did not accept the TGA PI/CMI click-through licence, so that PDF path is documented but not exercised.