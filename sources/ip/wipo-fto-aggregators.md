<!-- RECOVERED from subagent transcript agent-a56f2b8aaad7afe3b.jsonl, session fd64561f-7c90-41a2-95cf-b4a133a8fe0f, research date 2026-08-05.
     WIPO PATENTSCOPE and commercial FTO aggregators.
     Verbatim agent deliverable — not re-edited. -->

All items verified. Here are the findings.

---

# Data-source verification — WIPO & FTO aggregators
Fetched 2026-08-05. Method: `curl` with browser UA + WebFetch. **Note:** `patentscope.wipo.int` and `www.epo.org` return **403 to a default curl UA**; a browser `User-Agent` header is required. `www.questel.com` blocks both.

## PART A — WIPO

### A1. PATENTSCOPE API — EXISTS, PAID, SOAP, NOT PUBLIC ✅ VERIFIED
Source: `https://www.wipo.int/en/web/patentscope/data/` (HTTP 200, 92 KB)

Two subscription products, both flagged **"(conditional use)"**:

| Product | Price/yr | Scope |
|---|---|---|
| **PCT Webservice limited access** | **CHF 600** | Only docs in the "Published International Application" series |
| **PCT Webservice full-access** | **CHF 2,000** | All publication documents in the document tab |

Exact quote: *"Programmatic access via a set of Java API, based on SOAP protocol, to all publication documents available in the document tab of the PATENTSCOPE search engine… to retrieve the International Application Status Report (IASR) and to parse it on the fly and to download… documents by batch."*

**Rate limit ✅ VERIFIED** — `https://www.wipo.int/en/web/patentscope/data/terms` (HTTP 200): *"(i) 10 retrieval related actions per minute from an individual IP address of a subscriber. The limit of 10 retrieval-related actions per minute applies to each subscriber account and IP address, whichever is more restrictive."* Sharing one account across multiple IPs to raise throughput *"shall constitute a breach of these General Conditions."*

**No free/public REST API.** REST/JSON access is not offered at any tier. It is SOAP/Java only. This is the single most important constraint for a pipeline: **PATENTSCOPE cannot be used as a programmatic FTO backend at 10 req/min.**

**Licence tiers** (same terms page): basic → **non-derivative** (may store in searchable DB, redistribute internally to affiliates) → **derivative** (bulk redistribution allowed only with *"added value"* i.e. substantial modification, and *"the price of the added value product should not be lower than the price of the PCT data product paid by the Customer to WIPO"*). "Conditional use" additionally requires the subscriber to *"take the necessary technical measures to prevent the complete and easy bulk downloading of the data 'as is'"* and to redistribute *"only… to identified users."*

### A2. WIPO bulk data — ALL PAID (except statistics) ✅ VERIFIED
Same URL. Delivery is **SFTP or physical hard drive** — no S3/HTTP bulk endpoint.

| Product | Price (CHF/yr unless noted) | Delivery |
|---|---|---|
| PCT-Bibliographic | 400 | SFTP |
| ISA documents (ISR, Written Opinion, Art. 17.2) | 2,000 | SFTP |
| PCT-Text | 3,900 non-deriv / **19,500 deriv** | SFTP |
| PCT-Images | 3,900 | SFTP |
| PCT-FATE (machine-translated full text) | 6,000 non-deriv / **30,000 deriv** | FTP |
| Backfile, non-Asian langs (1978→) | 7,600 / **38,000 deriv** per copy | Hard drive |
| Backfile, Asian langs (1979→) | 1,600 / 8,000 deriv per copy | Hard drive |
| Backfile XML | 1,600 per copy | Hard drive |
| Backfile Bibliographic snapshot | 1,600 per copy | Hard drive |
| PCT images on demand | 100/order + CHF 100/GB (max 32 GB or 10k apps) | Hard drive |
| Missed weekly downloads | 50/wk in-subscription, 150/wk otherwise | — |
| **COPPA V2** parallel corpus (1990–2014) | **Free for translation research**; 1,100 otherwise | DVD |

**"A 50% discount is offered to non-profit organizations."** Data retention warning: *"PCT data of the current year will be available on the WIPO ftp server until the first publication of PCT data of the following year"* — miss a week and you pay to restore it.

**Free WIPO data:**
- **IP Statistics Data Center** — `https://www3.wipo.int/ipstats/` HTTP 200, `<title>WIPO IP Statistics Data Center</title>`. Described as *"a free online service."* **Aggregate counts only — not document-level. Useless for FTO.**
- **Sequence listings** — ⚠️ **UNVERIFIED download location.** The data page says *"Sequence listings in machine-readable format as filed by the applicant for all applicable PCT international applications. All sequence listings are published together for convenient download"* but carries **no download hyperlink** (the only adjacent link goes to `https://www.wipo.int/pct/en/texts/`, the PCT regulations). I could not locate a working bulk URL. **Use EPO's free sequence listings instead (A6/B6).**

### A3. WIPO Standards ✅ VERIFIED
`https://www.wipo.int/en/web/standards` (HTTP 200) — ST.96 is the XML schema standard (alongside ST.36/ST.66/ST.86); **ST.26 is the mandatory XML standard for nucleotide/amino-acid sequence listings**; ST.3 country codes, ST.16 kind codes, ST.9 INID. Relevance: schema/normalization only, not a data source. WIPO also launched an **IP API Catalog** (`https://www.wipo.int/en/web/standards/catalog-api/` → 200 at `.../standards/ip-api-catalog/index`) — an index of *other offices'* APIs, not a WIPO data API.

### A4. WIPO legal status — WEAK FOR FTO ✅ VERIFIED
- WIPO sells **no INPADOC equivalent**. The only national-phase artifact on the data page is a **DTD for offices submitting data to WIPO** (`/documents/d/patentscope/docs-en-data-documents-wo-national-phase-information-v1-5.dtd`), not a consumable dataset.
- Explicit disclaimer on the data page: *"the patent data of national and regional patent offices is not currently available from WIPO."*
- **Pat-INFORMED** (`https://www.wipo.int/pat-informed/en/`, HTTP 200) — free, medicines-specific, searchable by **INN**, data supplied directly by 20 biopharma companies via IFPMA. **Critical caveat, quoted verbatim: *"While it is not a tool to provide Freedom to Operate analysis, it facilitates access to patent information."*** Covers HIV/AIDS, cardiovascular, diabetes, hep C, oncology, respiratory + all WHO EML small molecules. **Small molecules only — no biologics.** Useful as a cross-check, not as an FTO basis.
- Also flagged on that page: **MedsPaL** (Medicines Patent Pool) and the FDA **Orange Book** as non-WIPO medicine/patent databases.

## PART B — Aggregators

### B5. Lens.org ✅ VERIFIED (base URL + auth proven by live calls)
- **Base URL: `https://api.lens.org`** — confirmed by live requests.
- **Unauthenticated call** → `POST https://api.lens.org/patent/search` returns **HTTP 401**:
  `{"reference":"b5cdbe51-...","message":"Missing/Incorrect Authorization Header","code":401}`
- **Invalid Bearer token** → distinct **HTTP 401**:
  `{"reference":"72d25f05-...","message":"Unable to authorize user to this resource.","code":401}`
  Two different messages confirm the header is parsed → **Bearer auth is the real mechanism.**
- **Auth format** (`https://docs.api.lens.org/getting-started.html`, HTTP 200): POST → `Authorization: Bearer your-access-token`; GET → `?token=your-access-token`.
- **Rate limiting**: response headers `x-rate-limit-remaining-request-per-minute`, `x-rate-limit-remaining-request-per-month`, `x-rate-limit-remaining-record-per-month`; over-quota → `429 - Too many requests`. **Numeric quota values are plan-specific and not published.**
- **Free tier — heavily qualified.** `https://about.lens.org/lens-api-terms-of-use/` (HTTP 200): free option is **"Trial Access"**, *"for non-commercial use only"*, evaluation-only, *"Trial access does not include commercial permissions."* Commercial Use is defined expansively: *"any use of Lens data that results in a business or corporate outcome – financial or otherwise,"* explicitly naming *"commercial research & development… investment decisions."* **A pharma FTO pipeline is unambiguously Commercial Use — the free tier does not cover it.** Also: *"Lens API service is only available through an institutional subscription."*
- **Pricing: ⚠️ NOT PUBLISHED.** `https://www.lens.org/lens/user/subscriptions` returns HTTP 200 but is login-gated and shows no figures. Custom Access pricing is *"determined by use case, attribution plan and API volume and speed requirements."*
- **PatSeq (pharma-critical)** — `https://about.lens.org/patseq-exploring-biological-sequences-in-patents/`: **488.3M sequences** across **440,000+ biological patents** (394M in applications, 94M in grants). Tools: PatSeq Finder (**BLAST-based similarity search**), Explorer, Analyzer, Data, Text Search. Bulk downloads under separate terms (`https://about.lens.org/patseq-bulk-download-tou/`). This is the strongest free-ish sequence-vs-patent capability outside Derwent GENESEQ.

### B6. EPO — THE HEADLINE FINDING: DOCDB + INPADOC ARE NOW FREE ✅ VERIFIED
Price list: `https://www.epo.org/pricelist` → **`https://www.epo.org/en/service-support/ordering/patent-information-products`** (HTTP 200). Verbatim from that table:

| Product | Cost |
|---|---|
| **EPO worldwide bibliographic database (DOCDB)** | **Free** |
| **EPO worldwide legal status database (INPADOC)** | **Free** |
| EP bibliographic data (EBD) | **Free** |
| European Patent Register data | **Free** |
| EP full-text data | **Free** |
| **Sequence listings** | **Free** |
| **Linked open EP data** | **Free** |
| European Publication Server web service (API) | **Free** |
| **Open Patent Services (OPS)** API | **Free ≤ 4 GB/week**; subscription **EUR 2,800** |
| Global Patent Index (GPI) | EUR 755/yr (bi-annual 490, quarterly 250) — *"a legacy product"* |
| PATSTAT Online | EUR 755/yr (bi-annual 490, quarterly 250) |
| PATSTAT Global | EUR 1,460 subscription / EUR 975 single edition |
| PATSTAT EP Register | EUR 1,460 subscription / EUR 1,420 single edition |
| National full-text (CH, FR, GB, ES) | EUR 2,700/country + EUR 9,100 backfile/country |

**Delivery — Open Bulk Data Download Service (BDDS): `https://publication-bdds.apps.epo.org/raw-data/products`** (HTTP 200; React SPA). Its backend `https://publication-bdds.apps.epo.org/bdds/bdds-bff-service/prod/products` returns **HTTP 302** unauthenticated → **a free EPO account is required to download.** Landing page: `https://www.epo.org/en/searching-for-patents/data/bulk-data-sets` (HTTP 200).

Product specifics (both HTTP 200):
- **DOCDB** `.../bulk-data-sets/docdb` — *"bibliographic data, abstracts, citations and the DOCDB simple patent family, but no full text or images"*; 100+ countries, back to the 1830s; **XML ST.36**; frontfile ~3 GB zipped (Tue/Thu), backfile **~200 GB zipped**, twice yearly. *"DOCDB data is the backbone of many commercial products and services."*
- **INPADOC** `.../bulk-data-sets/inpadoc` — **the legal-status layer WIPO does not sell.** *"legal events from over 50 international patent authorities worldwide"*; XML ST.36; frontfile ~700 MB weekly (Tuesdays), backfile ~20 GB. Lets you *"link legal events to your existing bibliographic records."*
- **Sequence listings** `.../bulk-data-sets/sequence-listing` — nucleotide/amino-acid listings from **EP, Euro-PCT and PCT publications where the EPO is ISA**; 1989 onward; txt; frontfile 10–200 MB weekly, backfile 6 GB. Caveat: *"the data has been re-formatted and marked up. It is not the version as filed by the applicant."*
- Licence: *"The terms and conditions for licensing of EPO databases apply"* — a click-through licence, not CC.

**Linked open EP data ✅ VERIFIED and it is genuinely open** — `https://www.epo.org/en/searching-for-patents/data/linked-open-data` (HTTP 200; the endpoint `https://data.epo.org/linked-data/` is a JS SPA). *"Linked open EP data is a free-of-charge service and is governed by a fair use policy."* Licence: **"Creative Commons Attribution 4.0 International Public" (CC BY 4.0)** — the only genuinely open licence found anywhere in this review. Offers URIs, RDF, a **SPARQL endpoint**, and bulk download. Explicit fair-use limit: the browser/API/SPARQL endpoint *"are not designed to provide a backend database service for production applications. For these uses, please download the data in bulk."*

**Bottom line for the pipeline: EPO, not WIPO, is the viable free backbone.** DOCDB (bibliographic + families) + INPADOC (legal status) + sequence listings, all free bulk, covers WIPO/PCT documents anyway.

### B7. Commercial FTO tools

**Clarivate Derwent** ✅ VERIFIED `https://clarivate.com/intellectual-property/derwent/world-patents-index/` (HTTP 200). ⚠️ **Products were renamed** — Clarivate's own login index lists *"Derwent Patent Search (formerly **Derwent Innovation**)"* and *"Derwent Patent Analytics (formerly Innography)."* DWPI's FTO value is **human-rewritten abstracts**: *"abstracts that clearly describe an invention's novelty, use and advantage"* by *"800+ editors"* covering *"nearly 80,000 new patent publications every week"*; **135m+ publications → 70m+ DWPI invention families**, where families *"go beyond priority relationships and group patents by invention, including non-convention equivalents"* — better recall than DOCDB simple families. **GENESEQ** (`/derwent/geneseq/`, HTTP 200) is the curated patent-sequence DB, the direct pharma counterpart to Lens PatSeq. Also `/derwent/sequence-search/`, `/derwent/chemical-patents-index/`, `/derwent/patent-data-apis/` (all linked from the IP hub). **No public pricing.**

**IFI CLAIMS** ✅ VERIFIED `https://www.ificlaims.com/platform/claims-direct/` and `/platform/data-coverage/` (both HTTP 200). Paid REST/data platform; **105+ countries bibliographic, 62 full-text, 180M+ records, 100+ sources.** Confirms the hypothesis verbatim — **"Calculated expiration dates"**: *"Easily forecast expiring technologies and patents for a company or location with our adjusted expiration dates"*; and **Legal status**: *"Available status information includes expirations, grants, examinations, rejections, and more."* Plus IFI Names (assignee normalization incl. ultimate parent + reassignments), Citation/Family/Attachment services, English MT one day after original, and a MaxVal-based litigation add-on. Licensing is explicitly split **`/usage/data-end-user-internal-use/` vs `/usage/data-reseller-commercial-use/`**. **No public pricing.** *This is the best fit for computed patent-term/expiry in an automated pharma FTO pipeline.*

**PatSnap** ✅ VERIFIED `https://www.patsnap.com/` (HTTP 200). Ships **purpose-built FTO agents**: `https://eureka.patsnap.com/ip/checking/#/agent-landing/fto` (FTO Search) and `/novelty` , plus Design FTO. Pharma-relevant modules: **Bio** (`/products/bio/`, biosequence search), **Synapse** (`/products/synapse/`, biopharma intelligence), **Chemical** (structure search), and SAR data extraction from patents. **No public pricing.**

**Questel (Orbit Intelligence)** ⚠️ **PARTIALLY VERIFIED.** `www.questel.com` is bot-blocked: curl returns **HTTP 404 with a 380 KB body** for *every* path (including `/sitemap.xml`), and WebFetch returns **HTTP 402**. I could not fetch a Questel product page and **will not invent one**. Verified indirectly via the Questel-operated login portal **`https://www.orbit.com/` (HTTP 200)**, whose meta tags read: description *"Questel new portal for patent, design, and legal professionals looking for a comprehensive coverage and powerful tool"*, keywords including **"orbit, Orbit Intelligence, qpat"**, *"infringement search… validity search… biotechnology patent search."* Confirms the product exists and is Questel's; FamPat family depth and legal-status coverage remain **unverified**. **No public pricing.**

---

## Recommendation for the pipeline

1. **Do not build on PATENTSCOPE.** SOAP-only, CHF 600–2,000/yr, and a hard **10 requests/minute** ceiling with an anti-parallelization clause. It is a document-retrieval service, not an FTO backend.
2. **Build the free layer on EPO**: DOCDB (biblio + families) + **INPADOC (legal status)** + sequence listings via BDDS (free account), with **Linked open EP data under CC BY 4.0** where an open licence is required. This subsumes PCT/WO documents, so WIPO's paid PCT products are largely redundant.
3. **Budget for one commercial layer.** The genuine gaps are (a) **computed patent term/expiry incl. PTA/PTE** → **IFI CLAIMS Direct**; (b) **curated abstracts + invention-level families** → **DWPI**; (c) **patent sequence search** → Derwent GENESEQ, Lens PatSeq, or PatSnap Bio.
4. **Lens's free tier will not cover you.** "Trial Access" is non-commercial-only and Lens defines commercial use to include *"commercial research & development"* and *"investment decisions."* An institutional subscription is required; no pricing is published, so budget an unknown.
5. **Two licence traps to route past legal:** WIPO's **derivative licence** forbids redistributing at a price below what WIPO charged you; EPO's Linked-open-data **fair use policy** forbids using the live SPARQL/API endpoint as a production backend (bulk download instead).
6. **Pat-INFORMED is not an FTO source** — WIPO says so on the page. Small molecules only, voluntary company-submitted data. Treat as a cross-check.