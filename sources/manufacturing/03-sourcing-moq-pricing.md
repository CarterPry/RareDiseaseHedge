<!-- RECOVERED from agent-a814ddd28437598da.jsonl on 2026-08-06.
     Original agent completed 92 tool calls (WebFetch, WebSearch, Bash curl) then died on
     an API socket connection error before it could write this file.
     All findings below are recovered from that transcript; a small number of additional
     live fetches were performed on 2026-08-06 to fill gaps and are labelled accordingly. -->

# API/CMO Sourcing, Minimum Order Quantities, and Reference Pricing

**Scope:** Commercial reality layer for a rare-disease drug repurposing company sourcing off-patent
APIs and drugs approved abroad but never in the US. Covers supplier discovery platforms, trade
intelligence, CMO/MOQ strategies, documentation requirements, and reference pricing databases.
Funnel A = PRV-eligible (never-US moiety, 505(b)(1)); Funnel B = orphan exclusivity only
(505(b)(2)). Pricing data relevant to both funnels; CMO/MOQ strategies equally applicable.

---

## 1. Supplier Discovery Platforms

### 1.1 Pharmaoffer

- **URL:** https://pharmaoffer.com
- **Type:** Global B2B API/excipient sourcing marketplace, headquartered Netherlands, offices India
  and China.
- **Scale (from WebSearch, verified against search-result snippets):** >5,000 suppliers worldwide;
  4,000+ GMP-verified manufacturers; >1 million buyer-sessions/year; active in 200+ countries;
  100,000+ API SKUs searchable.
- **Free tier:** Buyer registration and supplier contact appear free. The "Raw Materials Directory"
  (listing, certificates, direct contact) is described as free-of-charge.
- **Paid intelligence product — Pharmaoffer Intelligence / Sourcing Intelligence:**
  URL https://pharmaoffer.com/intelligence and https://pharmaoffer.com/api-price-intelligence-tool/
  — both returned HTTP 403 (Cloudflare bot-wall) when fetched directly (events 18, 128).
  Search results describe: analytics dashboard, price benchmarks (avg API price/kg by market/origin),
  transaction insights (real transactions: price/kg, quantities, dates, counterparties), backed by
  "4 million verified deals" from customs-verified data from 40+ countries. Monthly subscription
  with 15% annual-plan discount; specific price not publicly displayed.
- **Pricing page:** https://pharmaoffer.com/pricing/ — returned Cloudflare challenge (5,536 bytes,
  event 137); not scraped. Subscription detail page
  https://pharmaoffer.com/dashboard/trade-data/subscription exists per search results.
- **Direct fetch status:** All Pharmaoffer pages return HTTP 403 (Cloudflare managed challenge).
  Must use a real browser session or contact sales for pricing.

### 1.2 PharmaCompass

- **URL:** https://www.pharmacompass.com
- **Type:** Pharmaceutical intelligence platform — API pricing, DMF/CEP search, CDMO finder,
  supplier listings.
- **Access:** All direct fetches (root, /price/metformin, /find-suppliers, /manufacturers-suppliers-exporters)
  returned HTTP 403 (events 9, 21, 110, 122). Not machine-accessible without a browser session.
- **What search results confirm:** "API Reference Price" derived from Indian Trade (Import/Export)
  data. Database includes USFDA DMFs, CEP/COS, Japanese DMFs, Written Confirmations. Prospector
  product covers pharma/biotech/API/CDMO/FDF globally. Specific subscription price not public.
- **Key sub-pages (URLs from search, unverified by direct fetch):**
  - Supplier search: https://www.pharmacompass.com/find-suppliers
  - DMF/supplier directory: https://www.pharmacompass.com/manufacturers-suppliers-exporters
  - Price lookup pattern: https://www.pharmacompass.com/price/{INN} (e.g. /price/resveratrol,
    /price/apixaban confirmed in search results)
  - Small-batch CMO finder: https://www.pharmacompass.com/pharma-services/api-manufacturing-services/small-scale-batch
  - CDMO/API finder: https://www.pharmacompass.com/dashboard/pharma-biotech-api-cdmo-fdf-find-prospects

### 1.3 CPHI Online

- **URL:** https://www.cphi-online.com
- **Type:** Informa-operated directory tied to the CPHI trade show franchise. Company profiles,
  product listings, show participation records.
- **Access:** All direct fetches returned Cloudflare block (4,548 bytes, event 139). Not
  machine-accessible without a browser session.
- **Scale (from WebSearch):** Generic APIs category covers 750+ generic products from 150+
  suppliers. Also covers innovative APIs, CDMOs/CMOs, excipients, intermediates.
- **Auth:** Search results do not confirm whether a login is required to view supplier details;
  likely registration-gated for contact information. Contact CPHI directly at cphi-online.com.
- **Key sub-pages (URLs from search, not directly verified):**
  - Generic APIs: https://www.cphi-online.com/category/generic-apis/
  - CDMOs/data services: https://www.cphi-online.com/category/cdmos-and-cmos/data-services/
  - Innovative APIs: https://www.cphi-online.com/innovative-apis-code007586.html

### 1.4 ChemBK / ChemicalBook

- **URLs:** https://www.chembk.com/en/ (ChemBK); https://www.chemicalbook.com (ChemicalBook)
- **Type:** Chemical/pharmaceutical property databases with some supplier listings.
- **Access:** ChemBK homepage fetched (event 108): confirmed loading, "Powerful Online Chemical
  Database for PC, Pad and Phone" — minimal content in visible HTML, no supplier price data in
  page content returned by WebFetch. Not primarily a pharma-supplier sourcing platform; more
  useful for CAS lookup, molecular data, and as a secondary cross-reference for supplier names.
- **ChemicalBook.in** (India-specific index) appears in search results as a separate domain.
- **Utility:** Low for direct API sourcing; useful for CAS number disambiguation and basic
  property lookup. Supplier listings sparse compared to Pharmaoffer/PharmaCompass.

---

## 2. Trade Intelligence / US Import Data Sources

### 2.1 Panjiva (S&P Global Market Intelligence)

- **URL:** https://panjiva.com / https://www.spglobal.com/market-intelligence/en/solutions/products/panjiva-supply-chain-intelligence
- **Type:** Commercial trade intelligence database. Now branded under S&P Global Market Intelligence.
- **Coverage:** 2+ billion shipment records; 9 million companies; data from US (maritime only),
  Brazil, Central/South America, China, India, Indonesia, Pakistan, Philippines, Sri Lanka, Turkey,
  Vietnam — 20 countries total. US data from 2007 onward.
- **Data source:** Government-required customs declarations / Bills of Lading.
- **Access:** Subscription only. Pricing not published; reported by Reddit users as >$1,000/month.
  Institutional access available through some university library systems (e.g. Stanford GSB;
  WRDS/Wharton).
- **Pharma utility:** Search by company name, HS code (Chapter 30 = pharmaceutical products;
  Chapter 29 = organic chemicals/APIs), shipper/consignee. Reveals who actually ships specific
  APIs to the US and in what volumes — directly relevant to verifying that a supplier is an
  established exporter.
- **Panjiva root URL fetch (event 147):** Page loaded but returned only navigation/footer;
  body content blocked without login. Status confirmed reachable (HTTP 200 from headers).

### 2.2 ImportGenius

- **URL:** https://www.importgenius.com
- **Type:** Commercial trade intelligence — global import/export at bill-of-lading level.
- **Pricing (fetched by WebFetch, event 171-172, HTTP 200, VERIFIED):**
  - **USA Essentials Flex:** $229/month (or $183/month annual)
    — 1 seat, 25 searches/day, 1,000 rows/month download, most recent 12 months of US import data
  - **USA Pro Flex:** $449/month (or $359/month annual)
    — up to 3 seats, 50 searches/day, 150,000 rows/month download (50k/seat), US data 2006–present,
    AI-powered search
  - **Global Enterprise:** $1,999+/month
    — unlimited encrypted searches, custom download limits, shipment data from 21+ countries,
    dedicated research team
  - Global trade data (Mexico, India, Vietnam, etc.) available as add-ons starting $183/month
- **Coverage:** 25+ countries, 8 million US businesses, BL-level records.
- **Pharmaceutical utility:** Search by shipper, consignee, product description, HS code. Identify
  which Indian or Chinese API manufacturers ship to specific US buyers, and at what volumes.

### 2.3 ImportYeti (Free alternative)

- **URL:** https://www.importyeti.com
- **Type:** Free US customs manifest search tool.
- **Access:** Direct fetch returned HTTP 403 (bot-wall), but service confirmed operational via
  search results and Bellingcat description (events 153-156).
- **Coverage (from WebSearch):** 70+ million US customs sea shipment records; Bills of Lading
  from January 2015 onward, obtained via FOIA to US CBP. No login required. Air and truck freight
  not covered. 60+ fields per result: HS codes, shipping lanes, carriers, BOL numbers, trading
  partners, contact info.
- **Limitation:** Covers ocean freight inbound to US ports only. Designed for B2B lead generation
  and competitive intelligence; useful for pharma supplier discovery at no cost.
- **URL to use:** https://www.importyeti.com (confirmed domain; site reachable but bot-blocked
  to headless curl — requires browser).

### 2.4 FDA Import Refusals Dashboard

- **URL:** https://datadashboard.fda.gov/oii/cd/imprefusals.htm
- **Fetch result (event 39, HTTP 200, WebFetch VERIFIED):** Dashboard tracks import refusals with
  weekly updates; covers "final actions" only. Eight product categories filterable including
  "Drugs and Biologics." Geographic filters: 5 import divisions, 15 import districts.
- **Export options:** Full dataset download or filtered results available. API access exists but
  requires credentials from "OII Unified Logon application."
- **Curl head check (2026-08-06):** Returned HTTP 403 Forbidden (the dashboard uses IIS and
  requires browser authentication). The WebFetch result above (event 39) was from a rendered
  page fetch.
- **Utility:** Verify that a specific API supplier or country of origin has a history of FDA
  import refusals — critical due-diligence step before qualifying a CMO.
- **Caveat:** "Datasets are updated weekly and only include final actions." Real-time or more
  complete data requires FOIA request to Division of Freedom of Information.

### 2.5 US Census Bureau USA Trade Online

- **URL:** https://usatradeonline.census.gov/
- **Fetch status:** HTTP 200 confirmed (curl head, events 55 and 2026-08-06 live check). Site
  served over Cloudflare. Last-Modified: 2026-08-05.
- **What it provides (from WebSearch, event 46):** Official US Census platform for import/export
  data. Free service. Datasets: District Data (10-digit HS detail), Port Data (6-digit HS),
  State Export/Import Data (6-digit HS). Updated monthly with international trade report releases.
- **Registration:** Based on WebFetch result (event 52), the homepage returned only the title
  "U.S. Census Bureau - USA Trade Online" — body content behind JavaScript rendering. Registration
  requirements could not be confirmed from the fetch. Historically this service has been free
  without registration.
- **Key HS codes for pharma:**
  - Chapter 30: Pharmaceutical Products (finished dosage forms)
  - Chapter 29: Organic Chemicals (includes most APIs)
  - HS 2941: Antibiotics specifically
- **Utility:** Aggregate-level data by HS code and country; not shipper/consignee level (that
  requires Panjiva/ImportGenius/ImportYeti). Use to quantify total import volumes for a given API
  and identify dominant origin countries.

---

## 3. CoA Requirements and Documentation Package

### 3.1 Certificate of Analysis — Required Fields

Source: GMP Compliance website (https://www.gmp-compliance.org/gmp-news/gmp-requirements-for-certificates-of-analysis-coa), fetched via WebFetch (event 115, 118, HTTP 200 VERIFIED).

Per EU GMP Guide Part II Section 11.4, an authentic CoA must include:
- Name of the intermediate or API
- Batch number
- Release date
- Expiry date (where applicable)
- List of tests performed including acceptance limits
- Numerical results for each test
- Dated signature by authorised personnel
- Name of the company or laboratory

Regulatory frameworks governing CoA content:
1. EU GMP Guide Part I Chapters 4 & 6, Part II Section 11.4
2. EMA Guideline on batch certification
3. WHO Annex 10 — Model Certificate of Analysis
4. USP General Chapter <1080> — Bulk Pharmaceutical Excipients
5. IPEC CoA Guide for Pharmaceutical Excipients

ICH Q7 (GMP Guide for APIs) Section 7.2 additionally requires specifications for starting
materials: identity tests (at minimum one specific test per shipment), purity requirements,
impurity limits (based on process capability), and physical properties where relevant.

### 3.2 Full Documentation Package to Demand from a CMO/API Supplier

The following documentation items should be requested in a supplier qualification package.
Note: the transcript established CoA requirements from primary sources; the broader documentation
list below reflects industry standard practice — the specific items beyond CoA were not
individually verified by primary-source fetch in the original transcript.

**Verified by primary source (CoA):**
- Certificate of Analysis per EU GMP / ICH Q7 requirements above

**Standard package (industry practice — not individually primary-source verified in transcript):**
- Drug Master File (DMF) number (US FDA Type II for APIs) or EU CEP/COS certificate
- GMP certificate issued by a recognised authority (EMA, US FDA, PMDA, Health Canada, TGA, WHO-PQ)
- Written Confirmation (WC) for EU export
- Stability data (ICH Q1A) demonstrating shelf-life under relevant storage conditions
- Impurity profile against ICH Q3A
- Residual solvents report per ICH Q3C
- Heavy metals / elemental impurities per ICH Q3D
- Method validation summaries for all release tests
- Process flow diagram and description of synthesis route
- Vendor audit right or third-party audit report (BSI, SGS, Intertek)

**Verification strategy:** Per ICH Q7, a supplier's CoA may not align with your specifications.
Best practice: periodic independent testing (quarterly to semi-annually depending on criticality)
to verify supplier data. Do not rely on CoA alone for specification-critical batches.

---

## 4. MOQ Strategies for Low-Volume Orphan Products

### 4.1 The MOQ Problem

Typical commercial API batch sizes from Indian or Chinese manufacturers run 100 kg to several
metric tons. A small-market orphan product registering in Georgia, Ukraine, Armenia, Botswana,
Albania, Barbados, Seychelles, Samoa may consume 1–10 kg/year total. At $5,000–$50,000/kg
(illustrative — not a verified figure), even a 25 kg MOQ represents a multi-year supply
commitment that may be difficult to finance or store.

### 4.2 Campaign Manufacturing

Source: PubMed abstract 31850487 (https://pubmed.ncbi.nlm.nih.gov/31850487/), fetched via WebFetch
(event 161, HTTP — content confirmed in event 163, VERIFIED).

Campaign manufacturing = producing different pharmaceutical products sequentially in the same
facility between cleaning validations rather than dedicating a line. Key regulatory findings:

- **Health Canada, EMA, PIC/S, FDA** allow campaign manufacturing "after an appropriate risk
  evaluation has been performed."
- **CFDA (China) and WHO** permit it "only in exceptional circumstances" (without clear definition).
- **COFEPRIS (Mexico):** allowed "for certain classes of drugs."
- **CDSCO (India):** regulations contain "no mention of campaign manufacturing."
- Classes typically eligible: highly active APIs, hormones, immunosuppressants, cytotoxic agents,
  biological preparations, steroids, sensitizing materials, antibiotics, cephalosporins,
  penicillins, carbapenems, beta-lactam derivatives.
- Key concern: cross-contamination and mix-ups — requires appropriate cleaning validation.
- Significant regulatory inconsistency internationally; GMP harmonization unmet priority.

**Strategic implication:** An Indian or Chinese CMO subject to CDSCO regulations may not
explicitly permit campaign manufacturing; verify in the Quality Agreement. A European CMO
under EMA/PIC/S may be more straightforwardly available for campaign batches.

Source: DCATVCI Roundtable (https://www.dcatvci.org/features/cdmo-roundtable-managing-orphan-drug-projects/),
fetched via WebFetch (event 78, HTTP 403 — NOT directly retrieved). Content recovered from
WebFetch event 82 (tool_result) which returned the page via a different path. Key strategies
confirmed VERIFIED:

- **Multi-year campaign manufacturing:** "Manufacturing sites can plan to manufacture in
  multi-year campaigns to decrease production costs and maximize efficiency" when accurate
  forecasting is available.
- **Intermediate banking:** Maximise batch volumes at early synthesis steps and hold as
  intermediates; release to final API in smaller sub-campaigns.
- **Equipment optimisation:** Work within optimal ranges of equipment, perhaps at smaller
  batch sizes made more often, to improve robustness without significant cost increase.
- **Excipient standardisation:** Align non-functional excipients with those in common use to
  ensure freshly cycled material availability rather than specialised specs that may go stale.
- **Registration batch size:** For low-volume products, set the registration batch size the same
  as the commercial batch size — enables early identification of critical process parameters.

### 4.3 Shared Campaigns / Multi-Tenant CMOs

Not directly verified by primary-source fetch in the transcript. The concept (multiple sponsors
sharing a campaign to split costs) is referenced in industry practice. PharmaCompass lists
small-scale batch CMO services at:
https://www.pharmacompass.com/pharma-services/api-manufacturing-services/small-scale-batch
(URL confirmed in search results; direct fetch returned 403).

### 4.4 Acquiring an Existing Registered Dossier

Source: PMC (https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10229127/) and WebSearch results
(events 107, VERIFIED via search summary). A core regulatory dossier established for multiple
marketing authorization applications can be adapted across markets, with the core dossier used in
submissions to multiple regulatory authorities. This approach results in accelerated submission
timelines. For the target markets (Georgia, Ukraine, Armenia, Botswana, Albania, Barbados,
Seychelles, Samoa), several have reliance pathways on WHO-PQ, EMA, or FDA approvals
(covered in file 06-reference-regulators.md and 08-who-reliance.md) — an existing WHO-PQ dossier
may be adapted for multiple small-market registrations simultaneously, dramatically reducing
per-market dossier cost.

**Acquiring a dossier outright:** Buying or licensing a registered generic dossier from an
existing holder (e.g. a generic company with EMA/WHO-PQ registration for an API you need) is
a recognised strategy. This eliminates the cost of generating the bioequivalence/analytical
development package from scratch. No specific primary-source quote was recovered from the
transcript for this tactic; noted as standard practice.

### 4.5 Contract Packaging and Toll Manufacturing

The pharmaceutical contract packaging market was valued at USD 17.1 billion in 2024; the
broader CDMO market expected to reach $159.94 billion in 2026 (WebSearch event 160). Flexible,
modular, rapid-response packaging lines are increasingly available for small-batch orphan and
investigational product production. "Toll manufacturing" (supplying API to a CMO for formulation
and packaging only) is an option that separates the API sourcing constraint from the finished
dosage form manufacturing constraint.

---

## 5. Reference Pricing Sources

### 5.1 MSH International Medical Products Price Guide — DISCONTINUED

- **URL:** https://www.msh.org/resources/international-medical-products-price-guide
  (now redirects to https://msh.org/resources/international-medical-products-price-guide-2/)
- **Redirect confirmed:** HTTP 301 then HTTP 200 on the new URL (2026-08-06 live check, VERIFIED).
- **Status (fetched via WebFetch, event 10-11, VERIFIED):** The guide is **retired and no longer
  an active resource.** MSH's own page states the website "will no longer be accessible after
  June 30th, 2024" and the decision was made "because the most recent data being 9-years old."
  Last data year is 2015 (final edition). PDF versions for 1996–2015 were made available for
  download before retirement.
- **WHO/HAI impact:** WHO/HAI methodology manuals were updated in late 2024 specifically because
  MSH prices could no longer be used as international reference prices (confirmed via WebSearch
  event 59).
- **Conclusion:** Do not rely on MSH Price Guide for current business case pricing. Use the
  alternatives below.

### 5.2 Global Fund Price & Quality Reporting (PQR)

- **URL:** https://pqr.theglobalfund.org/
- **Page fetch (event 27, VERIFIED):** Login required. The landing page presents a login interface
  for username (email) and password. Registration is possible for new users.
- **Public access:** Per the theglobalfund.org description page (event 56-58, WebFetch HTTP 200,
  VERIFIED), two reports are available without login:
  - **Price Reference Report:** International reference prices and market data
  - **Transaction Summary:** Complete or filtered transaction listing
  However, direct navigation to sub-URLs /pqr/PriceReference and /pqr/TransactionSummary returned
  HTTP 404 (2026-08-06 live check) — URL paths may have changed. Access via the main portal
  login is the reliable path.
- **Product scope:** ARVs, anti-malarials, anti-TB, anti-hepatitis medicines; insecticidal nets,
  indoor spraying insecticides, condoms; diagnostic tests for HIV, TB, malaria, syphilis, HBV,
  HCV. **Orphan/rare-disease medicines not covered** unless they overlap with the above disease
  areas.
- **API access:** No API access mentioned in documentation.
- **Data entry:** Only Principal Recipients and Local Fund Agents can enter data; public users
  are read-only for published reports.
- **Utility for this company:** Useful for any candidates that overlap with HIV, TB, malaria or
  hepatitis treatment — for those, transaction-level procurement prices are visible and show
  genuine market prices paid by Global Fund grantees. Not relevant for most rare-disease
  repurposing candidates.

### 5.3 UNICEF Supply Division

- **Primary URL:** https://www.unicef.org/supply/price-data
  — returned HTTP 403 (event 31). Not directly machine-accessible.
- **Supply Catalogue:** https://supply.unicef.org/
  — returned HTTP 403 on both original fetch (event 97) and 2026-08-06 live check.
- **What is confirmed via WebSearch (events 28):**
  - UNICEF publishes prices of essential and strategic products procured under multiyear supply
    agreements. Prices reflect ceiling price per product per supplier per calendar year, including
    discount ranges and scaled pricing; highest and lowest spot prices shown.
  - Pricing not available for some products in some countries due to patent/licensing restrictions.
  - Sub-pages confirmed in search index: antimalarials price data
    (https://www.unicef.org/supply/documents/antimalarials-price-data), medicines tender calendar,
    vaccines pricing data.
- **Access in practice:** The UNICEF Supply Catalogue (supply.unicef.org) is intended to be
  browsable and exportable but is behind Cloudflare bot protection from headless access. Use a
  browser. No login reported to be required for browsing.
- **Utility:** UNICEF procures at very large scale; prices are below commercial market rates.
  Useful as a floor reference for what a very-large buyer pays, particularly for essential
  medicines on the WHO EML. Not representative of orphan/rare-disease APIs.

### 5.4 PAHO Strategic Fund

- **Primary URL:** https://www.paho.org/en/paho-strategic-fund
  — HTTP 200 confirmed (event 32, 34, and 2026-08-06 live check, VERIFIED).
- **Reference price document:** https://www.paho.org/en/documents/strategic-funds-reference-prices-eligible-products
  — HTTP 200 confirmed (events 37, 40, and 2026-08-06 live check, VERIFIED). Last updated
  per page content: 7 April 2025. The PAHO overview page states the document was updated
  "June 10, 2026" (event 34 content).
- **Format:** HTML page with downloadable PDF ("Strategic Fund's Catalogue for eligible products").
- **Access:** Freely accessible on PAHO's public website. No login required.
- **Caveat quoted from source:** "Prices are not guaranteed and do not constitute a formal price
  proposal." Member States advised to add 20–25% to listed prices to reflect freight and insurance
  to port of delivery. FCA Incoterm.
- **Scope:** Essential medicines and health supplies for the Americas. Products procured through
  PAHO's pooled procurement mechanism for Latin American and Caribbean member states.
- **Utility:** Relevant for candidate drugs already on the PAHO product list. Prices reflect
  pooled-procurement rates for the Americas, typically significantly below commercial tender
  prices. Useful as a low-end benchmark and as evidence that a product has an established
  procurement market.

### 5.5 WHO/HAI Medicine Price Methodology and Database

- **WHO source index:** https://www.who.int/teams/health-product-and-policy-standards/medicines-selection-ip-and-affordability/pricing-financing/med-price-info-source
  — WebFetch (event 61, 65) confirmed page loads, returns an Excel spreadsheet (latest version:
  July 2026) containing medicine registries, clinical trial registries, "Medicine Price Information
  Sources," and medical device price sources. Email contact: hps@who.int.
- **HAI database:** https://haiweb.org/what-we-do/price-availability-affordability/price-availability-data/
  — HTTP 200 confirmed (events 63, and 2026-08-06 live check, VERIFIED). HAI states:
  "Medicine Prices, Availability, Affordability & Price Components Database...freely available...
  data can be viewed, printed and exported to an Excel spreadsheet."
- **HAI methodology download:** https://haiweb.org/publication/measuring-medicine-prices-availability-affordability-and-price-components-2nd-ed/
  — Free. Two Excel workbooks (Part 1: prices/availability/affordability; Part 2: price
  components). Available in English, French, Spanish, Russian.
- **Methodology:** Standardised survey methodology capturing government procurement prices and
  patient out-of-pocket prices. Not a real-time commercial price feed — results are periodic
  surveys. Countries covered not specified on the landing page; contact info@haiweb.org for
  geographic coverage.
- **Update note:** 2024 minor revision to 2nd-edition manual to remove MSH reference prices
  as the comparator (MSH retired; see §5.1 above).
- **Utility:** Most useful for understanding price components (manufacturer price, distributor
  margin, pharmacy markup, taxes) in a specific country. Relevant for pricing strategy in the
  small target markets (Georgia, Ukraine, Armenia, Botswana, Albania, Barbados, Seychelles, Samoa)
  if a country-level survey has been conducted. Check the HAI database for those countries.

### 5.6 UNDP Procurement / Global Health Procurement

- **UNDP sustainable pharma procurement guide:**
  https://www.undp.org/sites/g/files/zskgke326/files/2025-09/sustainable_procurement_of_pharmaceuticals.pdf
  — HEAD returned HTTP 403 (2026-08-06 live check). URL was surfaced in WebSearch results (event
  53) but content could not be retrieved. URL appears to be from a 2025 UNDP publication.
- **No dedicated UNDP "Global Price Reporting Mechanism" was found:** WebSearch (events 51, 53)
  returned results about pharmaceutical pricing broadly but no UNDP-branded price reporting
  mechanism comparable to the Global Fund PQR. A dedicated UNDP price database does not appear
  to be publicly accessible based on this research.
- **UNDP procurement prices** are reported through individual country procurement records and
  occasionally through the Global Fund PQR for jointly-funded programmes. No standalone machine-
  accessible UNDP pharmaceutical price database was found.

### 5.7 DrugPatentWatch

- **URL:** https://www.drugpatentwatch.com
- **API page:** https://www.drugpatentwatch.com/api.php — HTTP 200, WebFetch (event 102, 105,
  VERIFIED). Page confirmed four API tiers: Lite, Plus, Advanced, Select — all display "Inquire"
  buttons; no public pricing listed. Trial access referenced.
- **Delivery formats:** SQL, REST API, XML/JSON/CSV, HTML/iframe, custom solutions.
- **What the platform provides:** Drug patents, generic entry projections, regulatory exclusivity,
  505(b)(2) reformulation tracking, royalty/settlement terms, CDMO pricing guides (editorial
  content). Covers small-molecule drugs, 1.3 million global patents.
- **Utility for this company:** Strong for Funnel A (never-US moiety) — identify whether a
  candidate API has active patents, exclusivities, or known generic entry that would disrupt the
  business case. CDMO guide content (editorial, not transaction data) useful for framing CMO
  negotiations.

---

## 6. Target-Market Procurement Price Databases

### 6.1 Georgia (Country Code GE)

- **eProcurement portal:** https://tenders.procurement.gov.ge/
  — Curl HEAD returned HTTP 302 → redirect to login.php (event 113, VERIFIED). The tender search
  portal requires login. The State Procurement Agency main site (https://procurement.gov.ge/en/)
  returned HTTP 200 with content (event 72, 75, VERIFIED).
- **Open data:** http://opendata.spa.ge/ and http://charts.procurement.gov.ge/ — referenced on
  the procurement agency site as structured/downloadable resources. Not directly fetched; existence
  confirmed from WebFetch result of main site (event 75).
- **Market Research portal:** https://research.spa.ge/ka — referenced but not fetched.
- **Contact:** info@procurement.gov.ge
- **Conclusion:** Georgia has a functioning e-procurement system. Medicine-specific procurement
  data appears available through the eProcurement portal but requires login/registration. Open
  data export may provide bulk access. Manual search of tender records is likely necessary for
  pharmaceutical price benchmarking.

### 6.2 Ukraine

- **National Drug Price Catalogue:**
  URL: https://moz.gov.ua/uk/nacionalnij-katalog-cin (found in WebSearch, event 164).
  Curl HEAD returned HTTP 403 (event 166). The site uses Cloudflare bot protection; requires
  a browser session.
- **Legal basis:** Government Resolution No. 439, 4 April 2025. Administered by Ministry of
  Health / State Expert Centre. The catalogue:
  - Sets maximum wholesale prices for most medicines
  - Listed price cannot exceed arithmetic average of three lowest prices for the same drug in
    reference countries defined by the Ministry of Health
  - Updated monthly; prices reviewed every six months
  - Pharmacies must stock at least one of the cheapest options per INN/form/dosage
  - Generics and biosimilars wholesale prices capped at 75% of declared maximum for originator
- **Transparency requirement:** Manufacturers and importers must declare maximum wholesale prices.
- **Public access:** Catalogue is described as publicly available but the URL is Cloudflare-
  protected from headless access. A browser session should work.
- **Additional context:** Medical Procurement of Ukraine (MPU, USAID-supported) achieved
  >$200M central budget savings Oct 2018–Jun 2024. Ukraine law simplifies state registration
  of medicines procured by MPU that are registered in UK, in the PEPFAR database, with temporary
  FDA approval, or on WHO prequalification lists.

### 6.3 Armenia

- No dedicated public pharmaceutical procurement price database found. WebSearch (events 76, 131)
  returned information about electronic prescription rollout (January 2025: all prescriptions
  electronic; 2,566 items on electronic prescription list) but no price database.
- Armenia pharmaceutical imports: USD 86,362,244 (December 2024 per CEIC data).
- Armenia has a drug registration body (pharm.am per search results).
- **Recommendation:** Contact the Armenian Ministry of Health directly or consult CEIC Data
  (subscription) for import price data. No public machine-accessible price database found.

### 6.4 Botswana

- **BoMRA (Botswana Medicines Regulatory Authority):**
  - URL: https://www.bomra.co.bw/ — HTTP 200 confirmed (events 90, 93, and 2026-08-06 live check,
    VERIFIED). WordPress-based site.
  - WebFetch (event 93) confirmed: site provides regulatory services, product registration,
    pharmacovigilance, clinical trial oversight, lab testing. Maintains "Registers" in Resource
    Centre; SmPC/PIL Repository; BRIMS system (https://brims.bomra.co.bw/). Fee schedules
    published in Resource Centre.
  - Legal basis: Medicines and Related Substances Act 2013 (updated 2025).
  - No public pharmaceutical procurement price database found at BoMRA or through WebSearch.
- **Pooled procurement:** Seychelles (and context suggests Botswana may participate) is involved
  in African island states joint medicines procurement initiative per WHO/AFRO (event 117 content).
- **Recommendation:** BoMRA for registration/regulatory. For procurement prices, contact the
  Ministry of Health directly. Botswana may participate in regional pooled procurement mechanisms.

### 6.5 Albania

- **Open Procurement Albania (health sector):**
  URL: https://openprocurement.al/en/health/index — HTTP 200 confirmed (events 96, 100, and
  2026-08-06 live check, VERIFIED).
  WebFetch (event 100) returned detailed content (VERIFIED):
  - **28,164 total tenders** listed in health sector
  - **1,075 economic operators**
  - Award and contract amounts visible in tables (ranges from under 1,000 to ~1.9 billion,
    currency unspecified in content — likely ALL, Albanian Lek)
  - Searchable by tenderer/contracting institution, successful bidders, tender numbers
  - Excel export option confirmed (Excel icon markers throughout page)
  - Successful bidders include: Megapharma, Incomed, Edna-Farma (pharmaceutical distributors)
  - Regional health institutions across Albania as contracting authorities
- **National Agency of Pharmaceuticals and Medical Devices:** Regulates pharmaceutical
  registration. Compulsory Health Insurance Fund administers a List of Reimbursable
  Pharmaceuticals.
- **Utility:** Albania's Open Procurement portal is the most machine-accessible of the target
  markets found in this research. 28,164 health tenders with award prices and Excel download
  make it a direct source of tender price benchmarking for Albania.

### 6.6 Barbados

- No public pharmaceutical procurement price database found. Barbados is part of CARICOM;
  pharmaceutical procurement research for CARICOM exists in academic literature (PMC8132958).
  Tender aggregators list 12,812+ tenders for Barbados (Tenderinfo.org per search results,
  event 83) but these are general government tenders, not a pharmaceutical price database.
- **Recommendation:** Contact the Barbados Drug Service (Ministry of Health) directly. Consider
  PAHO Strategic Fund prices as a reasonable proxy for CARICOM region procurement costs.

### 6.7 Seychelles

- **Seychelles pooled procurement:** WHO/AFRO confirmed (event 117, WebSearch VERIFIED) that
  Seychelles received its first pharmaceutical consignment through the pooled procurement
  mechanism and anticipates ≥50% cost savings over 5 years across 67 essential medicine
  formulations. The Medicine Procurement Unit is responsible for procuring medicines with
  objectives for cost-effectiveness, transparency, affordable prices, and quality assurance.
- **Ministry of Health pharmaceutical services:**
  URL: https://www.health.gov.sc/health-care-agency/pharmaceutical-services/ — not directly
  fetched. Exists per WebSearch results (event 117).
- No public machine-accessible price database found for Seychelles.
- **Recommendation:** Contact Seychelles Medicine Procurement Unit via the Ministry of Health.
  Given pooled procurement participation, prices may be available through regional reporting.

### 6.8 Samoa

- No dedicated public pharmaceutical procurement price database found. Tender aggregators list
  2,846 records for Samoa (Tenderinfo.org per event 83) but no pharmaceutical-specific database.
- **Recommendation:** Contact Samoa Ministry of Health. Samoa may participate in Pacific regional
  pooled procurement arrangements.

---

## 7. WHO Prequalification and EML as Sourcing Signals

- **WHO Prequalified Medicines List:**
  URL: https://extranet.who.int/prequal/medicines/prequalified-lists-medicines
  — HTTP 200 confirmed (event 120, 124, and 2026-08-06 live check, VERIFIED).
  Freely accessible. Lists finished pharmaceutical products assessed as acceptable in principle
  for procurement by UN agencies (HIV/AIDS, TB, malaria, other diseases, reproductive health).
  Also lists prequalified APIs (sources acceptable for use in pharmaceutical products) and
  quality control laboratories. Manufacturer information and country data available in the lists.
  Over 1,700 health products prequalified as of end-2025.
- **WHO EML (24th edition, September 2025):**
  URL: https://www.who.int/groups/expert-committee-on-selection-and-use-of-essential-medicines/essential-medicines-lists
  — Confirmed active (WebSearch, event 119). Freely accessible online database (eEML).
- **Utility for this company:** If a candidate API is WHO prequalified, it signals established
  supply chain, quality-assured suppliers, and acceptance in UN procurement. WHO-PQ status is
  also frequently accepted as a reliance pathway in the target markets.

---

## 8. Unfinished — Worth Re-running

The following research threads were initiated or identified but not completed before the original
agent died:

1. **UNICEF Supply Catalogue prices in-browser:** supply.unicef.org is Cloudflare-protected from
   headless access. A browser-based fetch of the medicines section and price data would establish
   actual product coverage and price ranges. Relevant URL:
   https://www.unicef.org/supply/price-data (403 from headless); try
   https://www.unicef.org/supply/documents/antimalarials-price-data and similar product pages.

2. **PAHO Strategic Fund PDF download and product list:** The PDF at
   https://www.paho.org/en/documents/strategic-funds-reference-prices-eligible-products was
   identified (HTTP 200 confirmed) but its actual product list and price ranges were not extracted.
   Download and check whether any target candidate APIs are listed.

3. **Pharmaoffer Intelligence subscription pricing:** The pricing page (pharmaoffer.com/pricing/)
   is Cloudflare-protected. A browser session would reveal actual tier pricing. The search results
   confirmed the page exists and has monthly/annual options with a 15% annual discount.

4. **Ukraine National Drug Price Catalogue:** moz.gov.ua/uk/nacionalnij-katalog-cin returns
   HTTP 403 to headless access. A browser session would reveal the actual catalogue content,
   which would give declared maximum wholesale prices for any candidate drugs registered in Ukraine.

5. **Georgia eProcurement pharmaceutical tenders:** tenders.procurement.gov.ge requires login.
   Registration and authenticated search for pharmaceutical tender awards would reveal historical
   medicine prices paid in Georgia.

6. **Armenia price database:** No public database found. The pharm.am regulatory body and
   Armenian Ministry of Health should be contacted directly. Phone/email not recovered from
   the transcript.

7. **UNDP sustainable procurement PDF:**
   https://www.undp.org/sites/g/files/zskgke326/files/2025-09/sustainable_procurement_of_pharmaceuticals.pdf
   returned HTTP 403. A browser or Wget with appropriate headers may retrieve the PDF.

8. **PharmSource (That's Nice LLC) CDMO intelligence subscription:** Search results confirm
   this service exists and compiles transaction-level CDMO pricing and capacity data, but
   subscription cost was not found in any public source. Contact sales directly.

9. **Specific CMO small-batch API sourcing prices:** Typical price/kg for small-batch (1–25 kg)
   GMP API synthesis from a European CMO versus Indian or Chinese CMO was not established in the
   transcript. This requires direct RFQ outreach rather than public database lookup.

---

## URL Ledger

### VERIFIED (URL fetched and content confirmed by the original agent or 2026-08-06 live check)

| URL | Status | Key Finding |
|---|---|---|
| https://www.msh.org/resources/international-medical-products-price-guide | 301 → 200 | Guide retired; data stopped 2015; no longer active |
| https://msh.org/resources/international-medical-products-price-guide-2/ | 200 | Retirement notice confirmed; PDF download 1996–2015 only |
| https://pqr.theglobalfund.org/ | Login wall (200) | PQR portal requires login; registration available |
| https://www.theglobalfund.org/en/sourcing-management/price-quality-reporting/ | 200 | Public Price Reference and Transaction Summary reports exist; no API |
| https://www.paho.org/en/paho-strategic-fund | 200 | Strategic Fund overview confirmed |
| https://www.paho.org/en/documents/strategic-funds-reference-prices-eligible-products | 200 | Price catalogue PDF, last updated 7 Apr 2025 / Jun 10 2026 |
| https://datadashboard.fda.gov/oii/cd/imprefusals.htm | 403 (IIS auth) | Dashboard confirmed; 8 product categories; weekly updates; API needs OII login |
| https://usatradeonline.census.gov/ | 200 | US Census trade data; free service; monthly updates |
| https://www.bomra.co.bw/ | 200 | BoMRA site confirmed; registers, fee schedules, BRIMS system |
| https://openprocurement.al/en/health/index | 200 | Albania: 28,164 health tenders, 1,075 operators, Excel export, award prices visible |
| https://www.importgenius.com/pricing | 200 | Essentials $229/mo, Pro $449/mo, Enterprise $1,999+/mo |
| https://extranet.who.int/prequal/medicines/prequalified-lists-medicines | 200 | WHO PQ list free, >1,700 products, APIs and FPPs listed |
| https://haiweb.org/what-we-do/price-availability-affordability/price-availability-data/ | 200 | HAI medicine price database freely accessible, Excel export |
| https://haiweb.org/what-we-do/price-availability-affordability/collecting-evidence-on-medicine-prices-availability/ | 200 | WHO/HAI methodology workbooks free download |
| https://www.gmp-compliance.org/gmp-news/gmp-requirements-for-certificates-of-analysis-coa | 200 | CoA required fields per EU GMP Part II §11.4 confirmed |
| https://pubmed.ncbi.nlm.nih.gov/31850487/ | 200 | Campaign manufacturing paper; regulatory agency positions confirmed |
| https://www.dcatvci.org/features/cdmo-roundtable-managing-orphan-drug-projects/ | 403 (content recovered from tool_result) | Orphan CMO strategies: multi-year campaigns, intermediate banking confirmed |
| https://procurement.gov.ge/en/ | 200 | Georgia State Procurement Agency; eProcurement at tenders.procurement.gov.ge |
| https://tenders.procurement.gov.ge/ | 302 → login.php | Login required to access Georgian tender database |
| https://www.drugpatentwatch.com/api.php | 200 | 4 API tiers (Lite/Plus/Advanced/Select); pricing on inquiry only; trial available |
| https://panjiva.com/import-export/United-States | 200 (content blocked) | Login required; 2B+ shipment records; 2007–present; 20 countries |

### UNVERIFIED (URL identified in search results or brief but not confirmed by any direct fetch)

| URL | Source | Notes |
|---|---|---|
| https://pharmaoffer.com/ (and subpages) | WebSearch | All fetch attempts returned HTTP 403 Cloudflare; site confirmed active from search results but no page content retrieved |
| https://pharmaoffer.com/pricing/ | WebSearch | Cloudflare challenge; 5,536 bytes of challenge JS returned |
| https://pharmaoffer.com/intelligence | WebSearch | HTTP 403 |
| https://pharmaoffer.com/api-price-intelligence-tool/ | WebSearch | HTTP 403 |
| https://www.pharmacompass.com/ (and subpages) | WebSearch | All fetch attempts HTTP 403 |
| https://www.cphi-online.com/ (and subpages) | WebSearch | All fetch attempts Cloudflare-blocked |
| https://supply.unicef.org/ | WebSearch | HTTP 403 both original and 2026-08-06 check |
| https://www.unicef.org/supply/price-data | WebSearch | HTTP 403 |
| https://moz.gov.ua/uk/nacionalnij-katalog-cin | WebSearch | HTTP 403; URL identified from search results; login or browser needed |
| https://www.health.gov.sc/health-care-agency/pharmaceutical-services/ | WebSearch | Not fetched; Seychelles MOH pharmaceutical services |
| https://www.importyeti.com | WebSearch | HTTP 403 from headless; confirmed free, 70M+ US customs records, no login |
| https://www.undp.org/sites/g/files/zskgke326/files/2025-09/sustainable_procurement_of_pharmaceuticals.pdf | WebSearch | HTTP 403 on 2026-08-06 check |
| https://www.paho.org/sites/default/files/2025-07/prices-vac-2025-eng-2-july-2025-v3.pdf | WebSearch | Not fetched; vaccines price list July 2025 |
| https://research.spa.ge/ka | WebFetch of main site | Market Research portal referenced on Georgian SPA site; not directly fetched |
| http://opendata.spa.ge/ | WebFetch of main site | Open data portal referenced; not fetched |
| https://brims.bomra.co.bw/ | WebFetch of BoMRA site | BRIMS medicine information system referenced on BoMRA site |
| https://www.pharmacompass.com/pharma-services/api-manufacturing-services/small-scale-batch | WebSearch | Small-batch CMO finder; not fetched (403) |
| https://pharmj.org.ua/index.php/journal/article/view/1486 | WebSearch | Ukrainian pharmacy journal on National Catalogue implementation |
