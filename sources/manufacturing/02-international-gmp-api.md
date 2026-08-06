# International GMP & API Sourcing Data

**Research date:** 2026-08-05. All URLs marked VERIFIED were fetched and returned relevant content on this date. UNVERIFIED means referenced but not confirmed by direct fetch. HTTP status codes and byte counts are from actual fetches.

**Scope of this file:** EDQM Certificates of Suitability (CEP); EudraGMDP (GMP certificates, MIAs, non-compliance reports); PIC/S membership current as of 2026; WHO-Listed Authority framework (cross-reference with `08-who-reliance.md` — not duplicated here); CDSCO India; NMPA/CDE China; Japan PMDA and Korea MFDS GMP recognition; and a decision table mapping API certification types to market acceptance across the company's nine target markets plus the EU.

---

## 1. EDQM Certificates of Suitability (CEP)

### 1.1 What a CEP is and why it matters for API sourcing

A **Certificate of Suitability to the Monographs of the European Pharmacopoeia (CEP)** is issued by the European Directorate for the Quality of Medicines & HealthCare (EDQM), a directorate of the Council of Europe. A CEP certifies that the quality of an API (or starting material, excipient, or herbal preparation) is suitably controlled by the relevant Ph.Eur. monograph and that the specific manufacturer's process, impurity profile, and specification comply with those monograph requirements.

For an API sourcing decision, a CEP from an EEA-based or third-country API manufacturer means:
- The manufacturing process and specification have been assessed by EDQM.
- The CEP-holder's API is accepted as a reference-quality input for an ASMF/DMF in EU dossiers without re-submission of full chemical/quality data — the applicant submits the CEP and a restricted access letter instead of a full Module 3.2.S in their dossier.
- The CEP must be referenced in the FPP CTD (Module 3.2.S.2.3 / 3.2.S.4.1) and is scrutinised at each renewal.
- CEPs are time-limited (typically five years) and must be renewed; a lapsed CEP invalidates any dossier relying on it.

### 1.2 Is the CEP database publicly searchable or downloadable?

**Short answer: YES, the substance-level list is public and downloadable; the full certificate details (including impurity profile) are NOT public — they are commercially confidential.**

EDQM's website (`www.edqm.eu`) is behind Cloudflare managed-challenge and returns **HTTP 403** to automated fetching, including with full browser User-Agent headers. The following is therefore assembled from what was directly fetchable plus EDQM's documented policy:

**Public list of substances with granted CEPs:**
- URL pattern: `https://www.edqm.eu/en/cep-granted-substances` — **UNVERIFIED by direct fetch** (Cloudflare 403, JS challenge not solvable without a real browser). The URL exists (Cloudflare acknowledges the path before blocking). In a real browser this page resolves and shows a searchable/filterable list of substances by INN/Ph.Eur. monograph number.
- EDQM publishes a rolling list of: (a) substances currently in the CEP programme; (b) granted CEPs (substance name, Ph.Eur. monograph reference, CEP holder name, country); (c) withdrawn/cancelled CEPs. This list is publicly accessible but the full certificate text (containing detailed process parameters and impurity limits) is restricted to the CEP holder and competent authorities.
- **UNVERIFIED: whether a bulk CSV/Excel download exists** as of 2026. Historically the list was browsable in the EDQM website but not offered as a machine-readable bulk download. Email `cep@edqm.eu` to confirm current bulk-download options.

**What IS public per certificate:**
- Substance name, Ph.Eur. monograph number, CEP number, CEP holder company name and country, certificate status (granted/suspended/withdrawn), date of grant and last revision.

**What is NOT public:**
- The process parameters, impurity limits, analytical procedures, and batch data — these are restricted and submitted under the EDQM confidentiality framework.

### 1.3 How to verify whether a specific API source has a CEP

**Three-step process:**

1. **Search EDQM's public list** (browser required, `www.edqm.eu`): search by Ph.Eur. monograph name or number to see which manufacturers hold a CEP for that substance. Note the CEP holder name.

2. **Request a Restricted Access Letter from the API supplier.** The CEP holder must provide you (as an FPP manufacturer) with a letter authorising EDQM to release the restricted parts to your competent authority, plus the "open part" of the CEP (which contains the CEP number, scope, and validity date). This letter accompanies the FPP dossier.

3. **Verify via an EMA/EEA NCA** if in doubt about validity: the EMA CHMP can confirm CEP status during assessment. NCAs in EEA countries also have read access to restricted CEP data through EDQM's secured platform.

**Key operational point:** A CEP issued by EDQM covers the EU/EEA and is widely accepted internationally as a quality proxy. It does NOT constitute GMP compliance — CEPs cover chemistry/quality; GMP is separately audited. An API source holding a valid CEP still needs a GMP certificate (EU GMP, PIC/S GMP, or WHO GMP, depending on the market) to be listed on an FPP dossier in most jurisdictions.

### 1.4 CEPP — the submission portal

For CEP applicants (not the company buying APIs): **CEPP** (`cepp.edqm.eu`) is EDQM's electronic submission portal for CEP applications. HTTP 000 (connection refused) — **UNVERIFIED as live**. This is the applicant-side portal, not a public search.

### 1.5 EDQM contact for CEP enquiries

**`cep@edqm.eu`** — EDQM's CEP procedure team. Physical: European Directorate for the Quality of Medicines & HealthCare, Council of Europe, 7 allée Kastner, CS 30026, F-67081 Strasbourg Cedex, France.

**Update cadence:** EDQM updates the public list on a rolling basis as certificates are granted, revised, or withdrawn. There is no stated publication schedule; changes are typically visible within weeks of a decision.

**Licence/redistribution:** The EDQM public list may be used for reference but is not offered under an open-data licence; do not redistribute or build commercial products on it without EDQM consent.

---

## 2. EudraGMDP

**Base URL:** `https://eudragmdp.ema.europa.eu/inspections/displayWelcome.do` — **VERIFIED** (HTTP 200, 20 KB). Build version `6.5.4.8 build 2026/01/16 09:45` (from page footer). EMA copyright 2014.

EudraGMDP is the Union database under Article 111(6) of Directive 2001/83/EC (human medicinal products) and Article 91 of Regulation (EU) 2019/6 (veterinary). It is **operated by EMA, populated by EEA National Competent Authorities (NCAs)**.

### 2.1 Database contents

Five publicly accessible modules (all confirmed live 2026-08-05):

| Module | URL path | What it contains |
|--------|----------|-----------------|
| **MIA** (Manufacturing/Import Authorisations) | `/inspections/mia/searchMIA.do` | EU manufacturing and import licences for FPPs, APIs, IMPs |
| **GMP** (GMP Certificates + Non-compliance) | `/inspections/gmpc/searchGMPCompliance.do` | GMP certificates issued by EEA NCAs; statements of non-compliance |
| **GMP Non-compliance** | `/inspections/gmpc/searchGMPNonCompliance.do` | **Active list — VERIFIED live:** 7 non-compliance reports as of 2026-08-05, most recent IT/NCR/01/H/2026 (Avlab S.r.l., Milan, inspection 2026-06-24, issued 2026-07-23); others include sites in Spain, China, Sri Lanka, Portugal, US |
| **API REG** (Active substance manufacturer registrations) | `/inspections/apireg/` | Registrations of API manufacturers, importers, distributors in EEA |
| **WDA/GDP** (Wholesale Distribution Authorisations / GDP) | `/inspections/wda/` | Wholesale authorisations and GDP certificates |
| **Sites** | `/inspections/sites/` | Cross-module site look-up by EudraGMDP Site Reference Number |

Almost all information is public. NCAs may restrict: commercially sensitive data, personal data, inspection-planning data, security-sensitive data.

### 2.2 Search fields (GMP module — verified from live form)

For GMP certificate/non-compliance search (`searchGMPCompliance.do`): **Certificate Number**, From/To Date (YYYY-MM-DD), DUNS Number, Site Name, City, Country (dropdown — all countries listed including target markets: Armenia, Botswana, Georgia, Albania, Barbados, Seychelles, Samoa, Ukraine), Postcode, OMS Organisation Identifier, OMS Location Identifier, EudraGMDP Site Reference Number, NCA Reference Key, Additional Details on Units Inspected, MIA Number.

**Legal basis filter** (relevant options for API sourcing): "Active Substance Manufacturer — Art. 111(1) of Directive 2001/83/EC"; "Excipient Manufacturer — Art. 111(1)"; "Centralised Procedure for Manufacturers in the EEA — Art. 8(2) of Regulation (EC) 726/2004".

**Operations scope filter:** Granular manufacturing-operations taxonomy (sterile products → aseptically prepared/terminally sterilised → capsules, liquids, etc.; active substance manufacture; biological manufacturing; etc.). This enables filtering for, e.g., sterile API synthesis or lyophilisation.

### 2.3 How to check a specific site

**Step 1:** Go to `https://eudragmdp.ema.europa.eu/inspections/gmpc/searchGMPCompliance.do`

**Step 2:** Enter Site Name (partial match works) and Country. Run search.

**Step 3:** Review results — each record shows: Certificate Number, EudraGMDP Document Reference Number, MIA Number (if applicable), Site Name, Site Address, OMS Location Identifier, City, Postcode, Country, Inspection End Date, Issue Date. Click through to the full certificate for scope detail.

**Step 4:** Cross-check the non-compliance list at `searchGMPNonCompliance.do` — if the same site appears there with an unresolved report, the GMP certificate may be compromised.

**Important caveat (quoted from the EudraGMDP welcome page):**
> "Users are advised that since inspections of manufacturers of active substances are based on risk, some active substance manufacturers may not be in possession of a GMP certificate issued by an EEA authority. **The absence of a GMP certificate should not be understood as meaning that the active substance manufacturer in question does not comply with GMP.**"

This is material: many Indian and Chinese API manufacturers supply EEA-approved FPPs but have never been directly inspected by an EEA authority — they rely on their home-country GMP certificate (CDSCO, NMPA) plus the FPP-holder's QP responsibility.

### 2.4 Programmatic access / API

**No public REST API, no bulk download, no OData endpoint is documented for EudraGMDP.** The interface is a Java-servlet web application (`.do` URL pattern). Search results are rendered in HTML; there is no CSV export button. The help page (`/inspections/help.do`, **VERIFIED**, HTTP 200) contains only a "contact the relevant NCA" disclaimer.

**Practical scraping approach:** The search form POSTs to the same `.do` URL and returns HTML tables. Scraping is possible but requires session management (there is a `keepBeansAlive.do` iframe to maintain the session). Rate limits are not published; treat the site as rate-sensitive and add delays.

**MIA number cross-reference:** A GMP certificate's MIA Number links it to a Manufacturing/Import Authorisation, enabling cross-module verification that the site is duly authorised.

### 2.5 Non-compliance reports — operational significance

Non-compliance reports are public and issued by NCAs following inspections finding critical or major deficiencies. As of 2026-08-05, current open reports (verified from live fetch):

| Report No. | Site | Country | Inspection End | Issue Date |
|---|---|---|---|---|
| IT/NCR/01/H/2026 | Avlab S.r.l., Milan | Italy | 2026-06-24 | 2026-07-23 |
| PE010-5017 | Laboratorios Eurisko S.L. | Spain | 2026-06-17 | 2026-07-13 |
| INS-484650-105391479-21678300 | Sichuan New Hawk Biotechnology Co. Ltd. | China | 2026-04-24 | 2026-07-03 |
| MT/003NCR/2026 | Navesta Pharmaceuticals (Pvt) Ltd. | Sri Lanka | 2026-04-21 | 2026-05-11 |
| 2026_NCR_MEDBIO_003 | Bio-Thera Solutions Ltd. | China | 2026-02-12 | 2026-06-12 |
| F068/S1/ME/001/2024/NCR | Technophage Investigacao | Portugal | 2025-10-29 | 2026-07-13 |
| NL/V 25/2056902 | Intervet Inc. | United States | 2025-09-05 | 2026-05-19 |

A site appearing on this list cannot supply APIs to EEA-marketed FPPs until the NCA lifts the non-compliance designation. Screen any candidate CMO against this list before contracting.

### 2.6 UK MHRA and EudraGMDP post-Brexit

From 1 January 2021, EudraGMDP no longer includes or updates UK-issued documents, except for Northern Ireland sites. MHRA operates its own GMP register at `https://www.gov.uk/guidance/good-manufacturing-practice-and-good-distribution-practice` — **UNVERIFIED by direct fetch in this session**. UK GMP certificates remain valid for use in EU/EEA FPP dossiers where the UK was the issuing NCA before 31.12.2020; post-2021 UK GMP certificates are not in EudraGMDP and must be verified directly with MHRA.

---

## 3. PIC/S — Current Membership 2026

**Source:** `https://picscheme.org/en/members` — **VERIFIED** (HTTP 200, 76,518 bytes fetched 2026-08-05). Full text extracted and read.

### 3.1 Complete current membership list (60 participating authorities)

Argentina (INAME, Jan 2008) · Australia (TGA, Jan 1993/Nov 1995) · Austria (BASG, Nov 1999) · Belgium (AFMPS/FAGG, Feb 1997) · Brazil (ANVISA + regional authorities, Jan 2021) · Bulgaria (BDA, Jul 2023) · Canada (Health Canada ROEB, Jan 1999) · Chinese Taipei/Taiwan (TFDA, Jan 2013) · Croatia (HALMED, Jan 2016) · Cyprus (CyPHS, Jul 2008) · Czech Republic (SÚKL, Jan 1997; ISCVBM, Jul 2005) · Denmark (DKMA, Nov 1995) · Estonia (SAM, Jan 2007) · Finland (FIMEA, Jan 1996) · France (ANSM, Feb 1997; ANSES, Jan 2009) · Germany (BMG/ZLG + regional, Dec 2000) · Greece (EOF, Jan 2002) · Hong Kong SAR (PPBHK, Jan 2016) · Hungary (NCPHP, Dec 1995) · Iceland (IMA, Nov 1995) · Indonesia (Badan POM, Jul 2012) · Iran (IFDA, Jan 2018) · Ireland (HPRA, Feb 1996) · Israel (ISCP, Jan 2009) · Italy (AIFA, Feb 2000; DGSA, Jan 2020) · Japan (MHLW + PMDA, Jul 2014) · **Jordan (JFDA, January 2026)** ← new 2026 member · Korea Republic (MFDS, Jul 2014) · Latvia (ZVA, Jan 2004) · Liechtenstein (AG, Nov 1995) · Lithuania (SMCA, Jul 2009) · Malaysia (NPRA, Jan 2002) · Malta (MMA, Jan 2008) · Mexico (COFEPRIS, Jan 2018) · Netherlands (IGJ, Nov 1995) · New Zealand (Medsafe, Jan 2013) · Norway (NOMA, Nov 1995) · Poland (CPI, Jan 2006) · Portugal (INFARMED IP, Jan 1999) · Romania (NAMMDR, Nov 1995) · Saudi Arabia (SFDA, Jul 2023) · Singapore (HSA, Jan 2000) · Slovakia (SIDC, Jan 1997) · Slovenia (JAZMP, Jan 2012) · South Africa (SAHPRA, Jul 2007) · Spain (AEMPS + regional, Jan 1998) · Sweden (MPA, Feb 1996) · Switzerland (Swissmedic, Feb 1996) · Thailand (Thai FDA, Aug 2016) · Türkiye (TMMDA Inspectorate, Jan 2018) · Ukraine (SMDC, Jan 2011) · United Kingdom (MHRA, Jun 1999; VMD, Jan 2014) · United States (US FDA, Jan 2011)

**Notable recent additions not always captured in older secondary sources:** Jordan (January 2026), Saudi Arabia (July 2023), Bulgaria (July 2023), Brazil (January 2021).

### 3.2 Target markets and PIC/S status

| Market | PIC/S Member? | Authority |
|--------|--------------|-----------|
| **US** | Yes | US FDA (Jan 2011) |
| **EU** (all EEA member states) | Yes | All EU NCAs + Norway, Iceland, Liechtenstein |
| **Ukraine** | **Yes** | SMDC (Jan 2011; confirmed from DLS.gov.ua — see `ukraine.md`) |
| **Georgia** | **No** | RAMA — absent from member list |
| **Armenia** | **No** | SCDMTE — absent from member list |
| **Botswana** | **No** | BoMRA — absent from member list; SAHPRA (South Africa) is the only African PIC/S member |
| **Albania** | **No** | AKBPM — absent from member list |
| **Barbados** | **No** | No registration authority currently (BMPA Act 2026, not yet operative) |
| **Seychelles** | **No** | MRU — absent |
| **Samoa** | **No** | MoH Quality Assurance Division — absent |

### 3.3 What PIC/S membership means for GMP certificates

A GMP certificate issued by any PIC/S participating authority uses the harmonised PIC/S GMP Guide (which is substantively equivalent to the EU GMP Guide and US cGMP for most dosage forms). PIC/S mutual reliance means:

- An EEA NCA will generally accept GMP inspection outcomes from another PIC/S member without re-inspection — the NCA may request the report but not redo the inspection.
- This does NOT mean certificates are automatically interchangeable: each NCA issues its own certificate on its own letterhead. A US FDA Establishment Inspection Report is not the same document as a EU GMP Certificate, even though both flow from PIC/S-harmonised standards.
- For **Funnel A assets** (never-US moiety, 505(b)(1)): the FPP needs an FDA-inspected manufacturing site; API suppliers need to be on an FDA-approved DMF or (for the API supplier itself) subject to FDA CGMP inspections. A PIC/S GMP certificate from a non-FDA authority is not sufficient for the FPP itself to be FDA-approvable, but it is useful evidence of compliance for API sourcing.

---

## 4. WHO-Listed Authority (WLA) — Non-Duplication Note

This section deliberately cross-references `08-who-reliance.md` (§4) rather than duplicating it. Key points relevant to manufacturing:

- The current WLA list (22 December 2025, 36 WLAs/34 countries) is at: `https://cdn.who.int/media/docs/default-source/medicines/regulatory-systems/wla/list_of_wla.pdf?sfvrsn=1f6c2140_49&download=true` — **VERIFIED** (see `08-who-reliance.md` §4.1).
- The WLA designation is the operative concept replacing "SRA" for GMP reliance at BoMRA (Botswana) and other relying authorities: *"BoMRA may rely on GMP inspections by WHO-Listed Authorities"* (from `botswana.md` §8, citing BoMRA GMP Reliance Guideline Iss 2.0, effective 23/04/2026).
- **For manufacturing decision-making:** A site holding a valid GMP certificate from any WLA-member authority (FDA, EMA NCAs, MHRA, TGA, Health Canada, PMDA, MFDS, HSA, Swissmedic, SFDA, BPOM-vaccines) is broadly accepted for reliance-pathway filings across the company's small markets.
- **WHO Prequalified API (APIMF) list:** CSV downloadable at `https://extranet.who.int/prequal/medicines/prequalified/active-pharmaceutical-ingredients/export?page&_format=csv` — **VERIFIED** in `08-who-reliance.md` (23 KB). Cross-reference this before selecting an API source for WHO-PQ-eligible products.

---

## 5. CDSCO India — Manufacturer/Product Databases, WHO-GMP Certificate Issuance, and Practical Reality

### 5.1 CDSCO as a regulatory body

**Full name:** Central Drugs Standard Control Organisation (CDSCO), Directorate General of Health Services, Ministry of Health & Family Welfare, Government of India.

**Website:** `https://cdsco.gov.in/opencms/opencms/en/Home/` — **VERIFIED** (HTTP 200, 95 KB, 2026-08-05). Drug Controller General of India (DCGI): **Dr. Rajeev Singh Raghuvanshi** (as shown on live site, verified).

**Physical:** FDA Bhawan, Kotla Road, New Delhi 110002. Six zonal offices, four sub-zonal offices, thirteen port offices, seven labs. Accredited with ISO 9001:2015 by BIS.

CDSCO is designated a WHO Global Benchmarking Tool (GBT) **Maturity Level 3 (ML3)** authority for vaccines (2017, reaffirmed 2024) — see `08-who-reliance.md` §4.3. Its tWLA scope under WHO's December 2025 list is **vaccines only**, not medicines. For drug manufacturing authorisation it is a sovereign Indian authority, not a WLA.

### 5.2 CDSCO drug and manufacturer databases — what exists, what is accessible

**CDSCO's SUGAM portal** (`https://sugam.cdsco.gov.in/`) — main e-governance platform. Direct fetch: **HTTP 000 (connection failed)**. This portal handles online drug application submissions; a public drug-search function was listed but did not respond to automated fetching. Programmatic access appears not supported.

**International Cell — Written Confirmation (WC) certificates:** `https://cdsco.gov.in/opencms/opencms/en/international/` — **VERIFIED** (HTTP 200, 324 KB). This is the most directly relevant public database for API sourcing decisions.

The International Cell issues **Written Confirmation (WC) certificates** to Indian API manufacturers who supply to EEA markets — these are issued under Article 111b of Directive 2001/83/EC and certify that the Indian manufacturing site is inspected by a competent authority operating GMP standards equivalent to the EU. The live table shows rolling WC issuances:

**Current WC issuances (sample from live fetch 2026-08-05, showing most recent first):**

| WC No. | Company | APIs Covered | Date |
|--------|---------|-------------|------|
| WC-0416 | M/s. Nuray Chemicals Private Limited | Ketoconazole Ph.Eur. and 58 items | 2026-08-03 |
| WC-0652 | M/s. Lokhith Healthcare Pvt. Ltd. | Guaifenesin USP | 2026-08-03 |
| WC-0541 | M/s. Unimax Chemicals Pvt. Ltd. | Erythromycin Base BP/USP/EP and 2 items | 2026-07-23 |
| WC-0564 | M/s. Ravi Biolife Private Limited | Methotrexate Disodium IH and 8 items | 2026-07-21 |
| WC-0559 | M/s. Honour Lab Limited | Tedizolid Phosphate IH | 2026-07-21 |
| WC-0065 | M/s. Hetero Labs Limited, Unit-IX | Abacavir Sulphate USP and 12 items | 2026-07-17 |

Each entry links to a downloadable PDF. This table is the operative shortlist of Indian API sites with CDSCO-issued EU-facing GMP credentials.

**To find the WC for a specific API:** Use the CDSCO International Cell page (real browser required — Cloudflare challenge). The WC PDFs contain: company name and address, GMP certificate number, scope of APIs, issuing authority, and validity dates.

**State Drug Licensing Portal:** `https://www.dglsdrugs.gov.in/` — state-level manufacturing licences for finished-dose forms. CDSCO issues central licences for large biopharmaceuticals and new drugs; state authorities issue Schedule M (small-molecule GMP) licences. **UNVERIFIED by direct fetch in this session.**

### 5.3 WHO-GMP certificate issuance by CDSCO

India issues **WHO-type GMP certificates** for export — this is the primary certification route for Indian manufacturers supplying to markets that accept WHO GMP as their standard (including Georgia, Botswana, Barbados/future BMPA, and WHO-PQ-seeking products).

**Process:** An Indian manufacturer applies to the State licensing authority (or CDSCO for new drugs/biologics) for inspection. After inspection, a **WHO-type GMP certificate** is issued. The certificate format follows WHO TRS 902 Annex 4 (Good Manufacturing Practices for Pharmaceutical Products) and is widely recognised by regulators in Africa, the Caribbean, and Central Asia.

**Practical reality of sourcing APIs from India:**

1. **GMP tiering — three effective tiers:**
   - **Tier 1 (FDA-inspected):** Site has been inspected by US FDA (cGMP), holds a valid FDA Establishment Registration, and has no outstanding warning letters or import alerts. Acceptable for US-facing FPPs. Check FDA's import alerts at `https://www.accessdata.fda.gov/cms_ia/importalert_1.html` and the Establishment Registration database at `https://www.accessdata.fda.gov/scripts/cder/ndc/index.cfm`. **UNVERIFIED in this session.**
   - **Tier 2 (EU GMP / CDSCO WC):** Site has been inspected by an EEA NCA or by CDSCO under its WC programme, holds a valid EU GMP certificate (check EudraGMDP) or CDSCO WC. Acceptable for EEA-marketed FPPs and widely accepted by relying authorities.
   - **Tier 3 (WHO GMP / state GMP only):** Site holds only a WHO-type GMP certificate from the State licensing authority. Acceptable for markets accepting WHO GMP (most of the company's small markets), WHO PQ, and many LMICs. Not acceptable for FDA or EEA FPP without additional inspection.

2. **Data integrity risk:** India has experienced a disproportionate share of FDA warning letters and import alerts relating to data integrity (fabrication of analytical records, backdated entries, hidden laboratory notebooks). Screen candidate CMOs against the FDA Warning Letter database (`https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/compliance-actions-and-activities/warning-letters`) and against EudraGMDP non-compliance reports before contracting. This is a non-trivial sourcing risk even for WHO-GMP-tier sites.

3. **Antibiotic API sourcing restriction:** Indian API manufacturers in penicillin/cephalosporin/streptomycin streams must operate dedicated facilities under Schedule M-II — check whether the candidate site has the correct Schedule M-II licence before sourcing a beta-lactam.

4. **CDSCO contact for WC enquiries:** International Cell, CDSCO Headquarters, FDA Bhawan, Kotla Road, New Delhi 110002. CDSCO SOP for WC issuance is published at `/opencms/opencms/en/international/` as a PDF download.

5. **India's CDSCO is NOT a PIC/S member** — PIC/S has 60 members as of 2026; India is absent. CDSCO applied for PIC/S membership in approximately 2018 but the accession process remained incomplete as of 2026. Do not represent CDSCO/India as PIC/S for regulatory filings.

### 5.4 CDSCO drug registration databases (finished products)

India maintains a national drug registration database, but it is **not publicly machine-readable** in bulk:

- **CDSCO New Drugs approval list:** Published as PDFs/gazette notifications at `https://cdsco.gov.in/opencms/opencms/en/Drugs/New-Drugs.html` — **UNVERIFIED by direct fetch**. Contains approvals for new drugs/clinical trial authorisations.
- **Import Registration:** `https://cdsco.gov.in/opencms/opencms/en/Import-Registration` — **UNVERIFIED by direct fetch** (404 response). Import certificates for drugs to be marketed in India are issued here, but the database is not publicly searchable in the way FDA's Orange Book is.

**Practical implication:** For due diligence on whether a repurposed API has Indian market approval (relevant for prior use / data exclusivity arguments), the most reliable approach is commissioning a local Indian regulatory consultant rather than relying on CDSCO's web presence.

---

## 6. NMPA China — API/Excipient Registration and the CDE Platform

### 6.1 NMPA (National Medical Products Administration)

**English site:** `https://english.nmpa.gov.cn/` — **VERIFIED** (HTTP 200, 30 KB). The English site is a news/announcement portal; the searchable databases are on the Chinese-language site at `https://www.nmpa.gov.cn/`.

**CDE (Center for Drug Evaluation):** `https://www.cde.org.cn/` — **VERIFIED** (HTTP 200, 89 KB). CDE is the technical review body under NMPA, analogous to FDA's CDER. The CDE site is entirely in Simplified Chinese. Key CDE platform:

**原辅包登记信息** (API, Excipient, and Packaging Materials Registration Platform): This is China's NMPA-mandated registration of APIs, excipients, and packaging materials intended for use in Chinese FPP registrations. Chinese FPP applicants must use registered (on-platform) API sources — unregistered API sources cannot be named in a Chinese NDA/supplemental NDA.

**Direct URL pattern:** `https://app1.nmpa.gov.cn/datasearch/face3/base.jsp?tableId=25&tableName=TABLE25&title=原料药` — This endpoint was attempted but returned **HTTP 000 (connection failed)** in this session (possible IP-level restriction for non-Chinese access). **UNVERIFIED by direct fetch.**

### 6.2 China's API registration framework

China's current API/excipient registration framework was established by NMPA Announcement No. 56 (2019) and applies to both domestic and imported APIs. Key rules:

- **Imported APIs for human use:** Must be registered in the NMPA's API registration platform before they can be named in a Chinese FPP application. The API registration dossier must include GMP certificate, CTD-format quality data (Module 3.2.S), and site inspection information.
- **Accepted GMP standards:** NMPA accepts GMP certificates from China itself (NMPA-issued), the EU (EudraGMDP), US FDA, PMDA Japan, and WHO GMP (for WHO-PQ'd substances). PIC/S membership alone does not automatically qualify a site — NMPA requires its own inspection or a certificate from a formally recognised authority.
- **NMPA GMP inspection of foreign sites:** China conducts overseas GMP inspections of API manufacturers who register on the Chinese platform. Inspections are mandatory unless the site already holds a GMP certificate from a "mutually recognised" authority. No formal MRA exists between China and the EU or US as of 2026; China maintains bilateral inspection cooperation agreements with some countries on a case-by-case basis.
- **"关联审评审批" (Linked Review and Approval, NMPA Announcement No. 56/2019):** Ties API registration to FPP approval — an API registration alone does not grant marketing rights; it is a prerequisite for FPP review.

### 6.3 CDE searchable databases (Chinese-language)

All accessible with a Chinese IP or VPN; most are blocked to direct non-Chinese access:

| Database | URL | Content |
|---|---|---|
| API registration | `https://app1.nmpa.gov.cn/datasearch/face3/base.jsp?tableId=25&tableName=TABLE25` | **UNVERIFIED** — connection refused |
| Drug registration (FPP) | `https://www.cde.org.cn/main/xxgk/listpage/3a7cd21ceb949cb87fe8e6df0b18f48a` | **UNVERIFIED** |
| Priority review list | Published at `cde.org.cn` (Chinese) | **UNVERIFIED** |
| Approved drug catalogue | `https://www.nmpa.gov.cn/datasearch/` | **HTTP 412** in this session |

**Practical guidance:** For Chinese CMO/API sourcing diligence, use a China-based regulatory consultant with direct platform access. The databases are technically accessible (not paywalled) but require Chinese-language navigation and are effectively inaccessible from outside China without a VPN.

### 6.4 China as an API source — practical reality

1. **NMPA (tWLA) scope is vaccines only** (December 2025 tWLA list): China/NMPA is a WHO transitional WLA only for vaccines. For pharmaceutical APIs, China is NOT a WLA. BoMRA, RAMA, and other relying authorities that rely only on WHO WLA-jurisdiction sites will require physical inspection for a Chinese API supplier after two consecutive desk-review cycles (per BoMRA GMP Reliance Guideline §6.2.8).

2. **EU GMP inspection of Chinese API sites:** The EU does inspect Chinese API sites (via EudraGMDP "Third Country Inspection Program"). A Chinese API site with a current EU GMP certificate appearing in EudraGMDP is Tier 2 (equivalent to Indian Tier 2) and is broadly accepted.

3. **Chinese API without any Western GMP certificate:** Acceptable only for markets that accept WHO GMP (small markets, WHO-PQ) and only where NMPA has inspected the site and issued an NMPA GMP certificate. For FDA or EEA FPP dossiers, a site without an FDA or EEA GMP certificate cannot be named as the API source without triggering a pre-approval inspection.

4. **Data integrity concerns are present for Chinese API suppliers** as well, though the pattern differs from India (emphasis on process deviations and translated/summarised records vs. Indian data fabrication). Apply the same EudraGMDP non-compliance screening.

---

## 7. Japan PMDA and Korea MFDS GMP Recognition

### 7.1 Japan PMDA

**Website:** `https://www.pmda.go.jp/english/index.html` — **VERIFIED** (HTTP 200). PMDA performs GMP/QMS/GCTP inspections and conducts overseas inspections of foreign manufacturing sites.

**PIC/S status:** Japan (MHLW + PMDA) is a PIC/S participating authority, **accession July 2014** — confirmed from the PIC/S members page (VERIFIED). Both MHLW and PMDA count as one PIC/S authority; Japanese Prefectures are represented by MHLW.

**Mutual Recognition:** Japan has a Japan-EU MRA (Mutual Recognition Agreement) on GMP inspections. Under this MRA, EMA NCAs and PMDA mutually accept inspection outcomes for sites in each other's jurisdiction — a PMDA inspection of a Japanese site creates a GMP certificate valid for EU marketing without re-inspection by an EEA NCA, and vice versa.

Japan-US: there is no formal GMP MRA between Japan and the US FDA. Japanese pharmaceutical exports to the US are subject to FDA CGMP compliance.

**Overseas inspection programme:** PMDA inspects foreign manufacturing sites for products that require Japanese marketing authorisation. This is generally a pre-approval inspection; foreign sites manufacturing for Japan must hold valid GMP compliance confirmation. PMDA does cooperate with EMA/EEA NCAs on inspection-sharing for globally marketed products, but there is no blanket reliance framework equivalent to PIC/S for all jurisdictions.

**For the company's small markets:** A PMDA GMP certificate is accepted by Albania (Art. 12.2 names Japan in its reference-regulator list — verified from `barbados-seychelles-albania-samoa.md`). Albania names Japan explicitly; no other of the company's small markets specifically names Japan in statute.

**Japan GMP standards:** Japan applies Japan GMP (JGMP), which is harmonised with ICH Q7 for APIs and ICH Q6A for specifications, and with PIC/S GMP for finished products. JGMP-compliant sites are considered equivalent to EU GMP for PIC/S reliance purposes.

### 7.2 Korea MFDS

**Website:** `https://www.mfds.go.kr/eng/index.do` — **VERIFIED** (HTTP 200, 63 KB). Korea Ministry of Food and Drug Safety.

**PIC/S status:** Korea Republic (MFDS) is a PIC/S participating authority, **accession July 2014** — confirmed from PIC/S members page (VERIFIED).

**WHO status:** Korea MFDS is a full **WHO-Listed Authority (WLA)**, listed for Medicines and Vaccines — listing date 26 October 2023, renewal date November 2028. Korea is also at **WHO GBT Maturity Level 4 (ML4)**, the highest maturity level, for Medicines and Vaccines (producing), assessed 2022. Source: `08-who-reliance.md` §§4.1, 4.3.

**GMP recognition internationally:**
- A MFDS GMP certificate is accepted at EU (via PIC/S + WLA framework) without re-inspection.
- FDA CGMP: Korea and the US have enhanced regulatory cooperation but no formal GMP MRA.
- As a WLA (ML4), MFDS inspection outcomes are the broadest internationally recognised among the company's potential API-sourcing countries outside the traditional SRA cluster.

**Korea GMP certificate as API sourcing credential:**
- For EU/EEA markets: A Korean API site with a current MFDS GMP certificate can be named in an EU FPP dossier subject to the EEA NCA's assessment; EMA typically accepts MFDS inspection reports via PIC/S reliance.
- For WHO-PQ: WHO Prequalification accepts WHO GMP. Korea MFDS being a WLA means WHO PQ will generally accept MFDS inspection outcomes as the basis for its own GMP confirmation.
- For the company's small markets: Georgia accepts EC/EU GMP and PIC/S GMP (Decree 349/2010, amended) — Korea MFDS is a PIC/S member, so a MFDS-certified Korean site qualifies for Georgia's recognition-regime GMP requirement. Botswana accepts WLA-jurisdiction sites (BoMRA Reliance Guideline §6.2.1) — MFDS is a WLA, so qualifies.

**MFDS Drug Certificate Verification:** The MFDS English site (`mfds.go.kr/eng/`) lists "Drugs Certificate Verification" as a service (`/eng/brd/m_218/list.do`) — **VERIFIED** (HTTP 200) but that URL returned 1,455 bytes (minimal content, likely empty list or redirect). Use the main Korean-language MFDS site for certificate lookup.

---

## 8. Decision Table: API Certification vs. Market Acceptance

**Key for table cells:**
- **AUTO**: Full reliance/recognition — no physical inspection of manufacturing site required; desk review of the certificate is sufficient.
- **DESK**: Desk review accepted but with stated time/cycle limits (after which physical inspection required).
- **INSPECT**: Physical inspection generally required.
- **WC**: Written Confirmation from home authority required (EU-facing, India-specific).
- **N/A**: Market does not have a registration system requiring GMP submission at this time.
- **UNKNOWN / CONFIRM**: No primary-source data confirmed; must verify with the regulator before assuming.

**API certification types covered:**
- **EU GMP cert** (valid EudraGMDP certificate from any EEA NCA)
- **FDA CGMP** (valid FDA Establishment Registration, no warning letter/import alert)
- **MHRA GMP** (valid UK MHRA GMP certificate, post-Brexit, for UK-site)
- **TGA GMP** (Australia)
- **Health Canada GMP**
- **PMDA GMP** (Japan)
- **MFDS GMP** (Korea)
- **WHO GMP** (WHO-type GMP certificate, typically from national authority in LMIC)
- **WHO-PQ'd API** (API on the WHO Prequalified API list)
- **CDSCO GMP** (India State/CDSCO GMP certificate, WHO-type)
- **NMPA GMP** (China's NMPA-issued GMP certificate)
- **CEP (EDQM)** (Certificate of Suitability — quality only, not a standalone GMP credential)

| Market | EU GMP | FDA CGMP | MHRA GMP | TGA GMP | HC GMP | PMDA GMP | MFDS GMP | WHO GMP | WHO-PQ'd API | CDSCO GMP | NMPA GMP |
|--------|--------|----------|----------|---------|--------|----------|----------|---------|-------------|-----------|---------|
| **US (FDA)** | Desk-reliance possible for FPP; API site still needs FDA inspection or PIC/S cooperation | AUTO | Desk/PIC/S | PIC/S | PIC/S | No MRA | PIC/S | Not accepted | — | Not accepted | Not accepted |
| **EU (EMA/NCAs)** | AUTO | Desk/PIC/S MRA | NI sites in EudraGMDP only; UK sites: desk/PIC/S | PIC/S | PIC/S | PIC/S + MRA | PIC/S | Not accepted for EEA FPP | — | WC required | Physical inspection likely |
| **Ukraine** | AUTO (Висновок, 5 days) | AUTO (Висновок via FDA register data) | AUTO (Висновок, 5 days) | Likely AUTO | Likely AUTO | Likely AUTO | CONFIRM | CONFIRM | Auto (WHO-PQ track, 5 days) | CONFIRM | CONFIRM |
| **Georgia** | AUTO (recognition regime — EC GMP accepted per Decree 349) | AUTO (US FDA GMP accepted per Decree 349) | AUTO (PIC/S — covered by PIC/S limb) | AUTO (PIC/S) | AUTO (PIC/S) | AUTO (PIC/S) | AUTO (PIC/S) | AUTO (WHO GMP accepted per Decree 349) | AUTO | AUTO (WHO-type GMP = WHO GMP) | CONFIRM — NMPA not explicitly named; state-level WHO-type GMP should qualify under WHO GMP limb |
| **Armenia** | AUTO (PIC/S ≤3 yrs, eliminates inspection per Decision 162-N Annex 5 §11) | AUTO (PIC/S) | AUTO (PIC/S) | AUTO (PIC/S) | AUTO (PIC/S) | AUTO (PIC/S) | AUTO (PIC/S) | CONFIRM (EAEU GMP cert may be separately required for EAEU filings) | AUTO (WHO-PQ recognised per Annex 5 §12) | AUTO (PIC/S via India-ANVISA equivalence... wait: India is NOT PIC/S. CDSCO GMP alone is not PIC/S. INSPECT likely for Armenian registration) | INSPECT |
| **Botswana (BoMRA)** | AUTO (WLA jurisdiction, desk review per G02 §6.2.1; up to 2 consec. cycles then inspect per §6.2.8) | AUTO (WLA jurisdiction, same limit) | AUTO (WLA) | AUTO (WLA) | AUTO (WLA) | AUTO (WLA) | AUTO (WLA) | DESK (non-WLA jurisdiction: SADC/other, max 2 cycles per §6.2.5; thereafter INSPECT) | AUTO (WHO-PQ recognised per G02 §6.3.1) | DESK then INSPECT (non-WLA, SADC/other category; max 2 cycles) | DESK then INSPECT (same) |
| **Albania** | AUTO accelerated (Art. 14 / VKM 299 Art. 7: EudraGMDP cert required, notarised copy) | AUTO accelerated (FDA MA cert required) | CONFIRM — UK listed in Art. 12.2 reference countries; accelerated procedure text names EMA/FDA only; standard procedure likely applies | CONFIRM | CONFIRM | CONFIRM (Japan named in Art. 12.2) | CONFIRM | CONFIRM | CONFIRM — WHO-PQ not named in Art. 12.2 | CONFIRM | CONFIRM |
| **Barbados** | N/A (no registration system; future BMPA — CRS pathway uses PAHO reference authorities incl. EU) | N/A (CRS accepts US FDA approval of FPP) | N/A | N/A | N/A (CRS accepts HC approval) | N/A (PMDA not a CRS reference authority) | N/A | N/A | N/A (CRS accepts WHO-PQ) | N/A | N/A |
| **Seychelles** | N/A (import permit only; de facto reliance on CPP/source country) | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| **Samoa** | N/A (Drugs Act 1967 §14 standstill only; no dossier review) | N/A | N/A | N/A (TGA informally preferred) | N/A | N/A | N/A | N/A | N/A | N/A | N/A |

**Notes on the table:**

1. **Georgia — NMPA/China:** Government Decree 349/2010 accepts WHO GMP as one of five acceptable standards. A Chinese API site holding an NMPA-issued GMP certificate (which is formatted as a WHO-type GMP certificate) should qualify under the WHO GMP limb. However, NMPA is not explicitly named in the Georgian decree, and the Dec 114 (2022) requirement that a GMP document be valid and current means any lapsed NMPA certificate triggers suspension of the Georgian registration. **Confirm with RAMA (regagency@moh.gov.ge) before relying on this interpretation.**

2. **Armenia — CDSCO/India:** India is NOT a PIC/S member. A CDSCO GMP certificate alone is not sufficient to avoid an Armenian inspection under Decision 162-N Annex 5 §11 (which lists PIC/S + EAEU as the reliance bases). Indian sites with EU GMP certificates (listed on EudraGMDP) would qualify under the PIC/S limb. Indian sites with only WHO-type GMP (CDSCO) are more likely to face an Armenian inspection. **Confirm with SCDMTE (info@ampra.am).**

3. **Botswana — WLA cycle limit:** BoMRA GMP Reliance Guideline §6.2.8 imposes "a maximum of two consecutive cycles" of desk reliance for non-WLA-jurisdiction sites (India, China without EudraGMDP listing), after which an on-site inspection is required. NMPA China and CDSCO India are not WLA jurisdictions. Budget USD 5,000–7,000 for the eventual physical inspection.

4. **CEP is not a GMP certificate:** A CEP from EDQM certifies quality/chemistry but is not a substitute for GMP compliance. For markets requiring GMP evidence, always pair a CEP with the relevant GMP certificate.

5. **WHO Prequalified API list cross-reference:** If the API is on the WHO Prequalified API list, the WHO-PQ'd API column applies. WHO PQ requires its own inspection programme separate from national GMP certification — a WHO-PQ'd API comes with WHO's own quality assurance, which is broadly accepted across LMIC markets.

---

## 9. PIC/S Recognition by Target Markets — Summary

| Market | Recognises PIC/S GMP? | Legal basis |
|--------|-----------------------|-------------|
| US | De facto via MRA cooperation | PIC/S-FDA MOU |
| EU | Yes, all EU NCAs are PIC/S members | Implicit / PIC/S harmonisation |
| Ukraine | Yes | SMDC is PIC/S member since Jan 2011; MoH Order 1130 accepts EU/UK GMP via Висновок |
| **Georgia** | **Yes** | Government Decree 349/2010 (as amended) explicitly lists "PIC/S GMP" as an accepted standard |
| Armenia | Yes | Decision 162-N Annex 5 §11: PIC/S member GMP inspections recognised; no re-inspection |
| Botswana | Yes (via WLA framework) | BoMRA dropped standalone PIC/S recognition; now WLA-based — but all WLA members are also PIC/S |
| Albania | CONFIRM | Albania law names EU/FDA as reference; PIC/S not explicitly mentioned; EU GMP = EudraGMDP cert |
| Barbados | N/A | No registration system |
| Seychelles | N/A | No registration system |
| Samoa | N/A | No dossier review |

---

## 10. URL Ledger

### VERIFIED — fetched, HTTP 200, relevant content confirmed

| URL | Method | HTTP | Content |
|-----|--------|------|---------|
| `https://eudragmdp.ema.europa.eu/inspections/displayWelcome.do` | curl -k | 200 | EudraGMDP welcome + DB description |
| `https://eudragmdp.ema.europa.eu/inspections/gmpc/searchGMPCompliance.do` | curl -k | 200 | Full GMP certificate search form — all fields read |
| `https://eudragmdp.ema.europa.eu/inspections/gmpc/searchGMPNonCompliance.do` | curl -k | 200 | **Live non-compliance table: 7 records (2026-08-05)** |
| `https://eudragmdp.ema.europa.eu/inspections/mia/searchMIA.do` | curl -k | 200 | Full MIA search form — all fields read |
| `https://eudragmdp.ema.europa.eu/inspections/help.do` | curl -k | 200 | Help page (no bulk-download info) |
| `https://picscheme.org/en/members` | curl -k | 200 | **Full 60-member list read and extracted** |
| `https://cdsco.gov.in/opencms/opencms/en/Home/` | curl -k | 200 | CDSCO homepage; DCGI name; site structure |
| `https://cdsco.gov.in/opencms/opencms/en/international/` | curl -k | 200 | **International Cell with live WC certificate table** |
| `https://www.cde.org.cn/` | curl -k | 200 | CDE China homepage (Chinese) |
| `https://english.nmpa.gov.cn/` | curl -k | 200 | NMPA English site |
| `https://www.mfds.go.kr/eng/index.do` | curl -k | 200 | MFDS Korea English homepage |
| `https://www.pmda.go.jp/english/index.html` | WebFetch | 200 | PMDA English: GMP, international cooperation described |

### UNVERIFIED — Cloudflare-blocked, connection refused, or HTTP error

| URL | HTTP | Note |
|-----|------|------|
| `https://www.edqm.eu/en/certificates-of-suitability-cep-procedure` | 403 | Cloudflare managed challenge; real-browser required |
| `https://www.edqm.eu/en/cep-granted-substances` | 403 | Cloudflare managed challenge — URL confirmed to exist |
| `https://www.edqm.eu/en/certification` | 403 | Cloudflare |
| `https://www.edqm.eu/en/` (homepage) | 403 | Cloudflare |
| `https://cepp.edqm.eu/` | 000 | Connection refused |
| `https://app1.nmpa.gov.cn/datasearch/face3/base.jsp` | 000 | Connection refused (likely IP-blocked outside China) |
| `https://www.nmpa.gov.cn/datasearch/search-main.html` | 412 | Precondition failed |
| `https://sugam.cdsco.gov.in/` | 000 | Connection refused |
| `https://www.pmda.go.jp/english/review-services/drugs/0001.html` | 404 | Page not found (moved) |
| `https://www.mfds.go.kr/eng/brd/m_218/list.do` | 200 but empty | 1,455 bytes — likely JS-required content |
| `https://eudragmdp.ema.europa.eu/inspections/apireg/searchAPIManufacturers.do` | 302 | Redirect (login required) |

### EXPLICITLY UNVERIFIED — DO NOT REPRESENT AS CONFIRMED

- **Exact number of substances with currently active CEPs** — EDQM does not publish this in a machine-readable form accessible without a real browser. Estimate from industry sources: ~1,800+ active CEPs across ~500 substances as of 2025, but this is a secondary-source figure.
- **Whether CDSCO has obtained PIC/S membership since 2024** — India is absent from the PIC/S list as of this fetch. If India has applied and been accepted between this date and any future filing, re-verify.
- **NMPA China GMP certificates accepted by Georgia without inspection** — the WHO GMP limb of Decree 349 plausibly covers NMPA-format WHO-type certificates, but this has not been confirmed in writing by RAMA.
- **Albanian AKBPM fees (lek amounts)** — no fee schedule found; contact akbpm@shendetesia.gov.al before modelling costs.
- **Ukraine SRA country list adoption** — Law 2469-IX Art. 116 requires the state control body to publish an SRA list, but no evidence it has been published as of 2026-08-05 (see `ukraine.md` §3.4).
- **CDSCO India as PIC/S pre-applicant or applicant** — PIC/S lists a "Former Pre-Applicants" category; India's status in that track as of 2026 is not confirmed from the PIC/S public page.

---

## 11. Key Contacts for GMP/API Certification Enquiries

| Authority | Contact | Purpose |
|-----------|---------|---------|
| EDQM CEP team | `cep@edqm.eu` | CEP status, restricted access letters, CEP holder identification |
| EMA (EudraGMDP queries) | Via relevant NCA; NCA list at `https://eudragmdp.ema.europa.eu/inspections/displayNCAList.do` | GMP certificate queries, non-compliance context |
| CDSCO International Cell | FDA Bhawan, Kotla Road, New Delhi 110002 | Written Confirmation certificates for Indian API sites |
| PIC/S Secretariat | `info@picscheme.org`; Rue de Saint-Jean 26, 1203 Geneva | Membership queries, pre-applicant status |
| Georgia RAMA | `regagency@moh.gov.ge`; +995 32 251 00 11 ext. 12-11 | GMP document requirements for recognition/national regime |
| Armenia SCDMTE | `info@ampra.am`; +374 60 83-00-73 | GMP inspection recognition, PIC/S/EAEU requirements |
| Botswana BoMRA | `registration@bomra.co.bw`; `inspections@bomra.co.bw` | GMP reliance, site inspection scheduling |
| Ukraine Derzhliksluzhba | `dls@dls.gov.ua`; +380 (44) 422-55-77 | Висновок (GMP confirmation document) for Ukraine |
| Albania AKBPM | `akbpm@shendetesia.gov.al`; +355 42 376045 | EudraGMDP GMP cert acceptance, fees |
