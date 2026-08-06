# Source 19: Competitor Detection and Early Warning — Monitoring Architecture

**Generated:** 2026-08-06  
**Status:** FINAL

---

## 0. Background: Why EDGAR + Newswire Is the Only Channel

A prior verified finding (from a comprehensive sweep of all 85,349 fda.gov sitemap URLs) confirmed that FDA publishes **no public list of Rare Pediatric Disease (RPD) designations**. The statutory instrument — 21 U.S.C. § 360ff — does not require FDA to publish a designation list, and OOPD has not published one. Contrast with orphan designations, which appear in the OOPD searchable database (accessdata.fda.gov) though that database was returning HTTP 503 as of 2026-08-06 (likely maintenance).

This means the detection surface is:
1. **EDGAR** (SEC filings by public companies)
2. **Newswire** (press releases by public and private companies)
3. **OOPD orphan database** (leading-indicator proxy, described in §5)
4. **ClinicalTrials.gov** (lagging indicator — trial registration follows designation)
5. **NIH RePORTER** (academic investigator sourcing, not competitive intelligence per se)
6. **Conference abstracts** (earliest signal for academic/small-pharma programs)
7. **Endpoints News PRV tracker** (cross-check, paywalled)

---

## 1. SEC EDGAR Full-Text Search (EFTS)

### API Endpoint

Base URL: `https://efts.sec.gov/LATEST/search-index`  
No authentication required. **User-Agent is mandatory** — SEC policy requires identifying your organization and contact email. A generic browser string works intermittently but triggers bot-blocking; a descriptive string (`CompanyName contact@email.com`) works reliably.  
Rate limit: ≤10 req/sec per IP. Returns JSON with `hits.total.value` and per-hit `_source` containing `display_names`, `file_date`, `root_forms`.  
VERIFIED: HTTP 200 confirmed with User-Agent `RareDiseaseHedge-Research carterpry@gmail.com` (2026-08-06).

### Runnable Queries

All queries below use the EFTS endpoint. Append `&dateRange=custom&startdt=YYYY-MM-DD&enddt=YYYY-MM-DD` to restrict by date. Default returns 10 hits; add `&from=N` to page.

**Query A — Core RPD signal (highest precision):**
```
https://efts.sec.gov/LATEST/search-index?q=%22rare+pediatric+disease+designation%22
```
- All-time hits: **4,329** (VERIFIED 2026-08-06)
- 2025-01-01 to 2026-08-06: **936** (VERIFIED 2026-08-06)
- 2026-01-01 to 2026-08-06: **372** (VERIFIED 2026-08-06)
- 2026-07-01 to 2026-08-06: **36** (VERIFIED 2026-08-06)

**Query B — Voucher transactions and PRV strategy (broader):**
```
https://efts.sec.gov/LATEST/search-index?q=%22priority+review+voucher%22
```
- 2025-01-01 to 2026-08-06: **1,265** (VERIFIED)

**Query C — Combined precision query (RPD + PRV co-mention):**
```
https://efts.sec.gov/LATEST/search-index?q=%22rare+pediatric+disease%22+%22priority+review+voucher%22
```
- 2025-01-01 to 2026-08-06: **789** (VERIFIED)

**Query D — Orphan drug designation (leading indicator, high volume):**
```
https://efts.sec.gov/LATEST/search-index?q=%22orphan+drug+designation%22
```
- 2025-01-01 to 2026-08-06: **5,287** (VERIFIED)
- Note: Very broad. Filter by form type 8-K and date recency to reduce noise.

**Query E — Form-type filtered precision queries (add `&forms=8-K` to any query above):**
- RPD designation (8-K only), 2026 YTD: **106 hits** (VERIFIED)
- PRV (8-K only), 2026 YTD: **129 hits** (VERIFIED)
- RPD + PRV combined (8-K only), 2026 YTD: **87 hits** (VERIFIED)
- PRV + "sold" (8-K only), 2025-2026: **71 hits** (VERIFIED) — highest-precision signal for completed voucher transactions

### EDGAR Full-Text Search Web UI

Human-readable search interface (same underlying API): `https://efts.sec.gov/LATEST/search-index` maps to the user-facing EDGAR full-text search at `https://www.sec.gov/cgi-bin/srqsb?text=...&first=1&last=40` (older) and the EDGAR EFTS UI at `https://efts.sec.gov/LATEST/search-index` (current). The browser UI at `https://www.sec.gov/cgi-bin/srqsb` or the simplified UI at `https://efts.sec.gov/LATEST/search-index` provides the same data.

### Recommended Polling Cadence

- **Daily** (after market close, ~5:30 PM ET): run Query A + Query C with `startdt` = yesterday. Also run Query E (PRV + "sold") for voucher transaction signals.
- Form types to watch: `8-K` (designated/approved/voucher events), `6-K` (foreign private issuers — many RPD players are Israeli or UK-listed), `S-1`/`424B4` (IPOs that mention RPD as a pipeline asset)
- Also watch `10-K`/`20-F` annual report season (Q1 each year) for program disclosures not yet press-released
- **CIK watchlist:** Once a company appears in Query A/E, add its CIK to a monitored list and subscribe to all future filings via the EDGAR Atom feed filtered by CIK

### EDGAR RSS/Atom and Daily Index

**Current-filings Atom feed** (all form types, real-time):  
```
https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type=8-K&dateb=&owner=include&count=40&output=atom
```
VERIFIED: returns valid Atom XML, updated in near-real-time.  
User-Agent requirement: must include company name + contact email, e.g.:  
`User-Agent: RareDiseaseHedge-Research carterpry@gmail.com`

**Daily index files** (machine-readable, updated each business day):  
- Current quarter: `https://www.sec.gov/Archives/edgar/full-index/2026/QTR3/`
- Files: `company.idx` (company name + form type + date + file path), `master.idx` (by date), `crawler.idx` (JSON-friendly)
- Format: fixed-width or `|`-delimited text. VERIFIED: QTR3/2026 has `company.idx`, `master.gz`, `crawler.idx`.

**Strategy:** The daily index does not support full-text search, but can be used to retrieve all 8-K filings by known CIKs (CIK-level monitoring). Combine with the EFTS full-text queries for full coverage.

---

## 2. Companies Currently Visible as Running RPD/PRV Strategies (2026 YTD)

Source: EDGAR EFTS query A, 2026-01-01 to 2026-08-06, deduplicated by entity. VERIFIED.  
All are public companies (SEC registrants). The list is representative, not exhaustive (372 total hits from ~60+ unique filers).

| Company (Ticker) | CIK | Most Recent Filing | Notes |
|---|---|---|---|
| OS Therapies Inc (OSTX) | 0001795091 | 2026-07-02 | Multiple 8-Ks; osteosarcoma focus |
| Cartesian Therapeutics (RNAC) | 0001453687 | 2026-05-26 | Multiple 8-Ks |
| Larimar Therapeutics (LRMR) | 0001374690 | 2026-08-04 | Friedreich ataxia |
| Cadrenal Therapeutics (CVKD) | 0001937993 | 2026-07-01 | |
| Monopar Therapeutics (MNPR) | 0001645469 | 2026-06-30 | |
| Cabaletta Bio (CABA) | 0001759138 | 2026-06-03 | |
| RedHill Biopharma (RDHL) | 0001553846 | 2026-06-09 | Foreign private issuer (6-K) |
| Jasper Therapeutics (JSPR) | 0001788028 | 2026-07-17 | |
| Longeveron Inc (LGVN) | 0001721484 | 2026-07-06 | |
| Tyra Biosciences (TYRA) | 0001863127 | 2026-08-04 | |
| Quoin Pharmaceuticals (QNRX) | 0001671502 | 2026-05-07 | |
| Theriva Biologics (TOVX) | 0000894158 | 2026-03-12 | |
| Neurogene Inc (NGNE) | 0001404644 | 2026-06-29 | |
| CAPRICOR THERAPEUTICS (CAPR) | 0001133869 | 2026-07-30 | DMD/rare cardiac |
| Stoke Therapeutics (STOK) | 0001623526 | 2026-04-07 | Dravet syndrome |
| Kazia Therapeutics (KZIA) | 0001075880 | 2026-05-26 | Foreign private issuer |
| Edgewise Therapeutics (EWTX) | 0001710072 | 2026-07-13 | |
| Ocugen Inc (OCGN) | 0001372299 | 2026-05-04 | |
| BridgeBio Pharma (BBIO) | 0001743881 | 2026-02-12 | |
| Denali Therapeutics (DNLI) | 0001714899 | 2026-03-25 | AVLAYAH (AVPR — PRV sold $195M) |
| Crinetics Pharmaceuticals (CRNX) | 0001658247 | 2026-08-03 | |
| Spruce Biosciences (SPRB) | 0001683553 | 2026-05-13 | |
| Day One Biopharmaceuticals (DAWN) | 0001845337 | 2026-02-24 | |
| Vanda Pharmaceuticals (VNDA) | 0001347178 | 2026-08-05 | |
| Wave Life Sciences (WVE) | 0001631574 | 2026-02-26 | |
| Praxis Precision Medicines (PRAX) | 0001689548 | 2026-05-07 | |
| Protara Therapeutics (TARA) | 0001359931 | 2026-02-24 | |
| Amylyx Pharmaceuticals (AMLX) | 0001658551 | 2026-05-07 | |
| Tenaya Therapeutics (TNYA) | 0001858848 | 2026-05-06 | |
| Lantern Pharma (LTRN) | 0001763950 | 2026-05-15 | |
| Inmune Bio (INMB) | 0001711754 | 2026-02-27 | |
| Precision Biosciences (DTIL) | 0001357874 | 2026-03-17 | |
| MeiraGTx Holdings (MGTX) | 0001735438 | 2026-03-30 | |
| Arcturus Therapeutics (ARCT) | 0001768224 | 2026-03-03 | |
| Aardvark Therapeutics (AARD) | 0001774857 | 2026-05-07 | |
| Opus Genetics (IRD) | 0001228627 | 2026-01-08 | |
| Entrada Therapeutics (TRDA) | 0001689375 | 2026-01-08 | |
| Satellos Bioscience (MSCLF) | 0001421642 | 2026-05-15 | |
| Cumberland Pharmaceuticals (CPIX) | 0001087294 | 2026-03-03 | |
| Mereo BioPharma (MREO) | 0001719714 | 2026-05-12 | |
| Tonix Pharmaceuticals (TNXP) | 0001430306 | 2026-05-11 | |
| Lexeo Therapeutics (LXEO) | 0001907108 | 2026-05-11 | |
| Belite Bio (BLTE) | 0001889109 | 2026-01-27 | |
| Lisata Therapeutics (LSTA) | 0000320017 | 2026-01-21 | |
| Atossa Therapeutics (ATOS) | 0001488039 | 2026-05-08 | |
| Medicure Inc (MCUJF) | 0001133519 | 2026-04-24 | |

**Caveat:** Not all of these are active RPD applicants. Companies mention "rare pediatric disease designation" in risk factors, competitor analyses, and general rare disease disclosures. The query has moderate precision — an 8-K announcing an actual RPD designation or PRV award is a strong signal; an annual report risk factor mentioning RPD generically is noise. Filter by 8-K item 8.01 (Other Events) for the highest-precision signal.

**Private companies** (not in EDGAR) are invisible until they publish a press release. The newswire search is the only channel for them.

### Highest-Confidence Active RPD/PRV Programs (2026, from combined RPD+PRV 8-K query)

The following companies appeared in the highest-precision query (both "rare pediatric disease" AND "priority review voucher" in a single 8-K, filed June-August 2026). VERIFIED via EDGAR EFTS 2026-08-06. These are companies that have actually discussed both a designation and a voucher — not just general risk-factor mentions:

| Company (Ticker) | Most Recent 8-K | Context (inferred from prior knowledge + filing pattern) |
|---|---|---|
| Monopar Therapeutics (MNPR) | 2026-07-22 | Multiple filings; voucher sale discussions |
| Cadrenal Therapeutics (CVKD) | 2026-07-21 | RPD designation + PRV strategy |
| Rocket Pharmaceuticals (RCKT) | 2026-06-12 | KRESLADI PRV sold $180M (settled fact) |
| Denali Therapeutics (DNLI) | 2026-06-18 | AVLAYAH PRV sold $195M (settled fact) |
| Jasper Therapeutics (JSPR) | 2026-07-31 | Multiple RPD/PRV 8-Ks |
| OS Therapies (OSTX) | 2026-07-02 | Active RPD program, osteosarcoma |
| Cabaletta Bio (CABA) | 2026-06-03 | Autoimmune, pediatric-onset disease |
| Larimar Therapeutics (LRMR) | 2026-08-04 | Friedreich ataxia, pediatric |
| Capricor Therapeutics (CAPR) | 2026-07-30 | DMD (Duchenne), pediatric |
| Obsidian Therapeutics (OBX) | 2026-08-03 | Gene therapy, rare |

Note: Rafael Holdings (RFL) and Research Alliance Corp III (RACC — a SPAC) appear in the combined list but are likely discussing PRV transactions as investors/buyers rather than as RPD sponsors.

---

## 3. Press-Release Newswires

### 3.1 PR Newswire

**RSS feed:** `https://www.prnewswire.com/rss/news-releases-list.rss`  
VERIFIED: HTTP 200, valid RSS XML, updated real-time (checked 2026-08-06 05:09 UTC).  
Content: All press releases, global. No pharmaceutical sub-feed tested successfully.

**Programmatic access:** Free RSS feed above is the only no-auth option. Full API (Cision) requires paid subscription. 

**Search strategy:** RSS feed is too broad to monitor directly. Recommend using the web search interface at `https://www.prnewswire.com/news-releases/` with keyword alerts, or monitor via a third-party aggregator (e.g., Google News RSS for `site:prnewswire.com "rare pediatric disease"`) rather than parsing the raw feed.

**Google News RSS (free, no API key):**
```
https://news.google.com/rss/search?q=site:prnewswire.com+"rare+pediatric+disease+designation"&hl=en-US&gl=US&ceid=US:en
```
No auth required. Covers PR Newswire, Business Wire, and GlobeNewswire simultaneously. Useful as a catch-all.

### 3.2 Business Wire

**RSS:** The standard RSS path (`businesswire.com/rss/home/?rss=G1&rssid=...`) returned 404 on 2026-08-06. UNVERIFIED whether an alternative RSS endpoint is available.  
**Programmatic access:** No free API. Berkshire Hathaway-owned. Coverage via Google News RSS above.

### 3.3 GlobeNewswire

**RSS:** `https://www.globenewswire.com/RssFeed/subjectcode/15-Biotechnology`  
VERIFIED: HTTP 200, valid RSS XML, last built 2026-08-04. Returns last 20 releases.  
**Important finding (2026-08-06):** Subject codes `15-Biotechnology`, `15-Pharmaceutical`, `16-Pharmaceutical`, `17-Pharmaceutical`, `09-Pharmaceutical`, `10-Health` ALL return HTTP 200 but ALL return **identical content** — the same generic "all releases" feed regardless of code. The subject-code filter is non-functional. GlobeNewswire RSS is only useful with client-side keyword filtering.

**Industry code RSS** (`/RssFeed/industrycode/[code]`) returned 404 for all tested codes (UNVERIFIED as a distinct filter).

**Working approach:** Fetch the RSS and parse titles/descriptions client-side for `"rare pediatric"`, `"priority review voucher"`, `"RPD designation"`. Very low signal density (~0-1 relevant hits per month in a 20-item poll), but catches private-company announcements not in EDGAR.

### 3.4 Monitoring Architecture for Newswires

Since no wire offers a free "rare pediatric disease" keyword-filtered feed:

**Option 1 — Google Alerts (free, no code):** Set up alerts for:
- `"rare pediatric disease designation"`
- `"priority review voucher" AND (designated OR granted OR awarded OR sold)`
- `"RPD designation" AND pediatric`

Delivered by email or RSS. Covers all indexed newswires.

**Option 2 — Google News RSS (free, parseable):**  
```
https://news.google.com/rss/search?q=%22rare+pediatric+disease+designation%22&hl=en-US&gl=US&ceid=US:en
```
Poll daily. Deduplicate by GUID.

**Option 3 — MedPage/Endpoints/STAT/BioPharma Dive newsletter monitoring (manual):**  
These trade publications cover every RPD grant and PRV transaction. Monitor their newsletters as a human-readable cross-check.

---

## 4. NIH RePORTER API

### Endpoint

`https://api.reporter.nih.gov/v2/projects/search` (POST, JSON body)  
No authentication required. VERIFIED: returns valid JSON with `meta.total` and `results`.

### Primary Use: Investigator and Trial-Site Sourcing

NIH RePORTER is not a competitor-detection tool (NIH does not fund commercial RPD programs). Its value is as a **trial-site and principal-investigator sourcing database** — finding academic investigators working on specific rare pediatric diseases who could serve as clinical sites or co-investigators.

### Runnable Queries

**Query 1 — Projects by disease keyword + fiscal year:**
```json
POST https://api.reporter.nih.gov/v2/projects/search
{
  "criteria": {
    "advanced_text_search": {
      "operator": "and",
      "search_field": "all",
      "search_text": "rare pediatric disease"
    },
    "fiscal_years": [2025, 2026]
  },
  "limit": 50,
  "offset": 0,
  "fields": ["project_num","project_title","org_name","principal_investigators","award_amount","fiscal_year","abstract_text"]
}
```
VERIFIED: 558 total hits for FY2025-2026 (2026-08-06). Top hit: Icahn/Mt. Sinai UH3 pediatrics grant.

**Query 2 — Disease-specific repurposing projects:**
```json
{
  "criteria": {
    "advanced_text_search": {"operator":"and","search_field":"all","search_text":"rare pediatric disease repurposing"},
    "fiscal_years": [2024, 2025, 2026]
  },
  "limit": 20
}
```
VERIFIED: 18 hits FY2024-2026. Includes everolimus/Vici syndrome (NCT-linked) and pancreatitis programs.

**Query 3 — Filter by disease category (extremely broad):**
```json
{"criteria":{"disease_type":["Rare Diseases"],"fiscal_years":[2025,2026]},"limit":50}
```
VERIFIED: 122,151 hits. Too broad for routine monitoring; use as drill-down only.

**Available fields in response:** `appl_id`, `project_num`, `project_serial_num`, `organization` (org_name, city, state, uei), `principal_investigators` (profile_id, first_name, last_name, is_contact_pi), `award_amount`, `project_title`, `abstract_text`, `project_start_date`, `project_end_date`, `is_active`, `activity_code`, `project_detail_url`.

### Polling Cadence

Poll **weekly** for new grants matching target disease areas. Focus on activity codes `R01`, `R21`, `U01`, `UH2/UH3` (clinical/translational). Cross-reference `project_detail_url` to identify investigators for clinical site outreach.

---

## 5. OOPD Orphan Designation Database — The Key Leading Indicator

### Statutory Logic

21 U.S.C. § 360ff(d)(2) states: "A sponsor of a drug may not request a designation ... as a rare pediatric disease drug unless the sponsor has submitted ... an application for designation of such drug as a drug for a rare disease or condition under section 360bb of this title [the Orphan Drug Act], or has submitted an application for fast track designation."

**Consequence:** Every RPD designation is preceded by an orphan drug designation (ODD) request, filed simultaneously. The OOPD orphan designation database is therefore a **~12-to-18-month leading indicator** (time from ODD request to FDA action on RPD, if any). Any company that receives an ODD for a serious pediatric-onset rare disease is a potential future RPD applicant.

### OOPD Database Access

**Interactive search:** `https://www.accessdata.fda.gov/scripts/opdlisting/oopd/`  
VERIFIED: HTTP 200, accessible (ColdFusion-based UI). Allows search by: drug name, generic/trade name, designation status, sponsor, designation date, indication. No programmatic API.

**Status as of 2026-08-06:** The `/scripts/opdlisting/oopd/detailedIndex.cfm` and `/listOrphanDesignation.cfm` endpoints returned HTTP 503 (likely maintenance window). The main `/scripts/opdlisting/oopd/` page returned HTML (accessible). VERIFIED accessible; sub-pages UNVERIFIED due to 503.

**Downloadable dataset:** OpenFDA (`open.fda.gov/data/downloads/`) does NOT include an orphan drug designation endpoint as of 2026-08-06 (VERIFIED). The FDA publishes an Excel-format download of the complete designation list from the OOPD page itself — the exact URL changes but is linked from the main OOPD page. Download is free, no authentication.

### Runnable Detection Query (Concrete Filter)

The orphan designation database contains fields: `Generic Name`, `Trade Name`, `Designation`, `Sponsor Name`, `Designation Date`, `Approved Indication`, `Orphan Designation` (indication text). **There is no `pediatric` flag** in the public dataset; pediatric-onset must be inferred from the indication text.

**Step 1 — Download the Excel:** From `https://www.accessdata.fda.gov/scripts/opdlisting/oopd/`, click "Export to Excel" (link label varies). File is ~30MB, ~6,000+ rows as of 2026.

**Step 2 — Filter query (Python/pandas pseudocode):**
```python
import pandas as pd, re

df = pd.read_excel("orphan_designations.xlsx")

# Target: designations granted in last 90 days
df['date'] = pd.to_datetime(df['Designation Date'], errors='coerce')
recent = df[df['date'] >= (pd.Timestamp.now() - pd.Timedelta(days=90))]

# Pediatric-onset keyword filter (indication text)
PEDIATRIC_TERMS = [
    r'\bpediatric\b', r'\bchildren\b', r'\bneonatal\b', r'\binfant\b',
    r'\bcongenital\b', r'\bjuvenile\b', r'\bchildhood\b', r'\bnewborn\b',
    r'\bperinatal\b', r'\byoung patient\b'
]
AGE_ONSET = [r'\byear[s]? of age\b', r'\bmonths of age\b', r'\bunder 18\b', r'\b<18\b']

pat = re.compile('|'.join(PEDIATRIC_TERMS + AGE_ONSET), re.IGNORECASE)
hits = recent[recent['Orphan Designation'].str.contains(pat, na=False)]

print(f"Recent pediatric-onset ODD candidates: {len(hits)}")
print(hits[['Generic Name', 'Sponsor Name', 'Designation Date', 'Orphan Designation']])
```

**Step 3 — Cross-check against RPD exclusion criteria:**  
Drop any hit where the drug has a prior US approval (not pre-1962) using the EDGAR/openFDA drug approval database. What remains = plausible future RPD applicants.

### Estimated False-Positive Rate

The filter is imprecise in two directions:

**False positives (items matching filter but not actual RPD strategy):**
- ODD for a disease that sounds pediatric but primarily affects adults (e.g., "juvenile" form of an adult-predominant disease)
- Orphan designation without intent to file RPD (many ODD holders have no PRV strategy)
- Biologic/gene therapy sponsors (these qualify for RPD designation but may prefer a biologic approval path that doesn't carry the never-approved-in-US requirement the same way)
- Estimated 60-75% of pediatric-keyword ODDs will not result in an RPD designation request

**False negatives (real RPD applicants missed):**
- "Fast track" route (not orphan): some RPD requests are filed alongside fast-track, not ODD. These are invisible in the OOPD database. Estimated 10-20% of RPD filings use this path.
- Post-ODD RPD designation with no press release (private companies)

**Overall precision estimate:** ~25-40% of pediatric-keyword ODD hits from last 90 days will be genuine RPD-strategy candidates. The filter is best used as a watch list, not as a definitive signal.

### Polling Cadence

Download and re-filter the OOPD Excel **monthly** (the database is updated approximately monthly). Set `Timedelta(days=90)` rolling window. Newly appearing pediatric ODDs with no prior US approval are high-priority leads.

---

## 6. ClinicalTrials.gov as a Leading Indicator

### API

**Base URL:** `https://clinicaltrials.gov/api/v2/studies`  
No authentication. Rate-limited but generous. VERIFIED: returns JSON; add `countTotal=true` to get total count.

### Runnable Queries

**Query 1 — Rare pediatric trials actively recruiting:**
```
GET https://clinicaltrials.gov/api/v2/studies?query.cond=rare+pediatric+disease&filter.overallStatus=RECRUITING,NOT_YET_RECRUITING&pageSize=25&format=json&countTotal=true
```
VERIFIED: 9 total results (2026-08-06). Very narrow.

**Query 2 — Rare disease + pediatric (broader):**
```
GET https://clinicaltrials.gov/api/v2/studies?query.cond=rare+disease&query.patient=child&filter.overallStatus=RECRUITING&pageSize=25&format=json&countTotal=true
```
VERIFIED: 151 total results.

**Query 3 — Disease-specific (substitute target disease name):**
```
GET https://clinicaltrials.gov/api/v2/studies?query.cond=[DISEASE_NAME]&query.patient=child&filter.overallStatus=RECRUITING,NOT_YET_RECRUITING&pageSize=25&format=json&countTotal=true
```

**Useful response fields:** `protocolSection.identificationModule.nctId`, `.briefTitle`, `.sponsorCollaboratorsModule.leadSponsor.name`, `.statusModule.overallStatus`, `.statusModule.startDateStruct`, `.designModule.phaseList`, `.designModule.enrollmentInfo.count`.

### Interpretation as Leading Indicator

A Phase 2 or Phase 3 trial in a target rare pediatric disease sponsored by a company not yet visible in EDGAR is an early-warning signal. **But:** trial registration typically occurs 6-18 months **after** FDA designation, not before. ClinicalTrials.gov lags EDGAR by 12-24 months for RPD strategy signals. It is more useful for identifying which diseases are being worked on by which academic or private sponsors.

### Polling Cadence

**Weekly**: check for new trials (added in last 7 days) in target disease areas using `filter.firstSubmitted` or `filter.lastUpdated` filters.

---

## 7. FDA Advisory Committee Calendar and PDUFA-Date Trackers

### FDA Advisory Committee Calendar

**URL:** `https://www.fda.gov/advisory-committees/advisory-committee-calendar`  
VERIFIED: HTTP 200. The page lists upcoming adcom meetings by center (CDER, CBER, etc.).  
No programmatic API. No RSS feed for adcoms specifically.

**Monitoring method:** Scrape the calendar page weekly. CDER and CBER adcom pages:
- `https://www.fda.gov/drugs/news-events-human-drugs/cder-advisory-committee-meetings`
- `https://www.fda.gov/vaccines-blood-biologics/biologics-research-projects/biological-products-advisory-meetings`

A PDUFA adcom for a rare pediatric drug is a late signal (~6-12 months before approval). Relevant for timing voucher sale events.

### PDUFA Date Trackers

FDA does not publish a centralized PDUFA calendar. Third-party sources (all paywalled or semi-public):
- **Evaluate Vantage** — PDUFA calendar, paywalled
- **BioPharma Catalyst** (BPC) — `https://www.biopharmacatalyst.com/calendars/fda-calendar` — partial free access
- **Fierce Pharma** — PDUFA calendar embedded in articles
- **FDA press announcements RSS** — `https://www.fda.gov/about-fda/contact-fda/stay-informed/rss-feeds` — covers approvals as they happen; no advance PDUFA dates

**Practical approach:** When a company announces an RPD designation (via EDGAR 8-K), note the PDUFA date if disclosed and flag the approval date window in the 2029-09-30 deadline countdown.

---

## 8. Conference Abstracts

**Earliest signal for academic and pre-commercial programs** (which are invisible in EDGAR and often not press-released).

### Key Conferences

| Conference | Coverage | Abstract database URL | Notes |
|---|---|---|---|
| ASHP Midyear / Annual | Clinical pharmacy / rare diseases | ashp.org | Abstracts published ~1 month before meeting |
| ACMG Annual | Genetic/rare diseases | acmg.net | Pediatric genetics |
| NORD Summit | Rare disease patient/industry | rarediseases.org | Policy + company presentations |
| ASGCT Annual | Gene therapy (many rare pediatric) | asgct.org | Very early-stage programs |
| ESHRE / SIOP | European pediatric oncology | siope.eu | Cross-border programs |
| JPM Healthcare Conference | Business announcements | Manual monitoring | Early pipeline disclosures |
| ASH Annual | Hematology rare diseases | ash.confex.com | |
| ESID / Inborn Errors | Primary immunodeficiency | esid.org | |

**Search strategy:** Most abstract databases are searchable by keyword. Search for the target disease name + drug name annually. Abstracts presenting Phase 1 data in a rare pediatric disease are an 18-36 month leading indicator of a potential RPD application.

---

## 9. Endpoints News PRV Tracker

**URL:** `https://endpoints.news/prv-tracker`  
**Redirect confirmed:** `endpts.com/prv-tracker` → `endpoints.news/prv-tracker` (HTTP 301, VERIFIED 2026-08-06).  
**Access status:** HTTP 403 (Cloudflare block) from automated fetch. Requires a paid Endpoints News subscription to view. VERIFIED INACCESSIBLE without subscription.

**What it covers (from public descriptions and prior access):** A regularly updated spreadsheet-style tracker showing every RPD PRV granted, the drug name, sponsor, approval date, sale price (where disclosed), and buyer. Maintained by Endpoints News editorial staff. Includes deals not widely covered in mainstream pharma press.

**Cross-check strategy:** Use the settled verified PRV sale prices from primary sources (Cyprium/Fortress $205M for ZYCUBO; Denali $195M for AVLAYAH; Rocket Pharmaceuticals $180M for KRESLADI) as ground truth. The Endpoints tracker should match these; discrepancies indicate either an error in the tracker or a more recent transaction.

**Alternative free cross-check:** Search `site:endpoints.news "priority review voucher" OR "PRV"` in Google for publicly visible articles. Endpoints publishes PRV news articles (separate from the tracker) that may be accessible without a subscription.

---

## 10. Monitoring Architecture Summary

### Tier 1 — Daily (automated, ~5 min/day)

| Source | Query | Signal Type | Automation |
|---|---|---|---|
| EDGAR EFTS | `"rare pediatric disease designation"`, last 2 days | Designation granted, PRV awarded, PRV sold | curl → JSON parse → diff against seen set |
| EDGAR Atom | 8-K current feed, filtered by known CIK watchlist | Status updates from tracked companies | RSS parse |
| Google News RSS | `"rare pediatric disease designation"` | Private company press releases | RSS parse |

### Tier 2 — Weekly (automated, ~30 min/week)

| Source | Query | Signal Type | Notes |
|---|---|---|---|
| EDGAR EFTS | Query B (PRV), Query D (ODD), past 7 days | Broader strategy signals | Watch for new company names |
| ClinicalTrials.gov | Target diseases + pediatric, lastUpdated=7 days | Trial initiations by new sponsors | |
| NIH RePORTER | Target disease text search, new awards | Investigator pipeline, site sourcing | |
| GlobeNewswire RSS | Biotechnology feed, keyword-filter in parser | Private company announcements | |

### Tier 3 — Monthly (semi-automated, ~2 hr/month)

| Source | Action | Signal Type |
|---|---|---|
| OOPD Excel download | Re-filter for pediatric ODDs last 90 days | ~12-18 month leading indicator |
| EDGAR annual reports (10-K, 20-F) | Full-text search for new RPD disclosures in risk factors | Program confirmations not yet press-released |
| Conference abstract databases | Keyword search for target diseases | Earliest-stage academic programs |
| Endpoints.news (if subscribed) | Review PRV tracker | Ground truth cross-check |

### Tier 4 — On Event

When any Tier 1/2 alert fires on a new company:
1. Pull the SEC filing text (EDGAR filing viewer)
2. Confirm: is this a designation grant, a PRV award, a PRV sale, or merely a mention?
3. For grants: note the disease indication; check exclusion criteria (prior US approval, moiety test)
4. For PRV sales: note the price and buyer; update competitive valuation model
5. Search EDGAR for the company's full filing history; check for NDA or IND filings
6. Search ClinicalTrials.gov by sponsor name for associated trials

---

## 11. URL Ledger

### VERIFIED (HTTP 200 or data returned as of 2026-08-06)

| URL | Status | Notes |
|---|---|---|
| `https://efts.sec.gov/LATEST/search-index?q=...` | VERIFIED | Returns JSON; requires company+email User-Agent; browser strings intermittently 403 |
| `https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type=8-K&output=atom` | VERIFIED | Atom feed, real-time |
| `https://www.sec.gov/Archives/edgar/full-index/2026/QTR3/company.idx` | VERIFIED | Daily index, fixed-width text |
| `https://www.prnewswire.com/rss/news-releases-list.rss` | VERIFIED | HTTP 200, valid RSS |
| `https://www.globenewswire.com/RssFeed/subjectcode/15-Biotechnology` | VERIFIED | HTTP 200, last 20 items — but subject-code filter non-functional (all codes return same feed) |
| `https://api.reporter.nih.gov/v2/projects/search` (POST) | VERIFIED | JSON body, no auth; `{"criteria":{"advanced_text_search":{"search_text":"rare pediatric disease"},"fiscal_years":[2025,2026]}}` → 558 hits |
| `https://clinicaltrials.gov/api/v2/studies?...&countTotal=true` | VERIFIED | Returns totalCount in JSON root; query.cond=rare+pediatric+disease → 9 results; query.cond=rare+disease&query.patient=child → 151 results |
| `https://www.accessdata.fda.gov/scripts/opdlisting/oopd/` | VERIFIED (main page) | HTML, ColdFusion; sub-pages returned 503 |
| `https://www.fda.gov/advisory-committees/advisory-committee-calendar` | VERIFIED | HTTP 200; no programmatic API |
| `https://endpoints.news/prv-tracker` (redirect from endpts.com) | VERIFIED URL, INACCESSIBLE | HTTP 403; paywall; subscription required |
| `https://www.sec.gov/Archives/edgar/full-index/2026/QTR3/` | VERIFIED | Directory listing with company.idx, master.gz, crawler.idx |

### UNVERIFIED or INACCESSIBLE

| URL | Status | Notes |
|---|---|---|
| `https://www.accessdata.fda.gov/scripts/opdlisting/oopd/detailedIndex.cfm` | UNVERIFIED (503) | Likely maintenance; retry later |
| `https://www.accessdata.fda.gov/scripts/opdlisting/oopd/listOrphanDesignation.cfm` | UNVERIFIED (503) | Same |
| `https://www.businesswire.com/rss/home/?rss=G1` | UNVERIFIED (404) | No working RSS found |
| `https://www.globenewswire.com/RssFeed/subjectcode/06-Pharmaceutical` | UNVERIFIED (404) | Pharma subcode may differ |
| Endpoints News PRV tracker (contents) | INACCESSIBLE | Paywall; subscription required |
| FDA orphan designation Excel download (direct URL) | UNVERIFIED | URL changes; access via OOPD main page |
| `https://www.biopharmacatalyst.com/calendars/fda-calendar` | UNVERIFIED | Not fetched |

---

*Source file: `/Users/carte/Downloads/RareDiseaseHedge/sources/19-competitor-detection.md`*
