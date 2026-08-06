<!-- RECOVERED from agent-a7e10a62c64973ab1.jsonl on 2026-08-06.
     Original agent died on an API connection error after 110 tool calls.
     All findings below are reconstructed verbatim from that transcript's
     tool_result payloads and assistant analysis blocks. Newly-verified
     items (live fetches performed during recovery on 2026-08-06) are
     labelled [NEWLY VERIFIED 2026-08-06]. -->

# Drug Knowledge Bases — Licence Terms and Commercial Use

**Scope:** Resources NOT covered in `09-cheminformatics-repurposing-dbs.md` (which handled PubChem, ChEMBL, Open Targets, DrugCentral, repoDB, Broad Repurposing Hub). This document covers: DrugBank, SIDER 4.1, OFFSIDES/TWOSIDES, FAERS/openFDA adverse events, DailyMed SPL API, WHO VigiBase/VigiAccess, CTD (Comparative Toxicogenomics Database), NCATS Inxight Drugs, and supplementary repurposing resources.

**Legal framing:** Funnel A candidates are never-approved-in-US moieties filed as 505(b)(1) NDAs (PRV-eligible). Funnel B are US generics or existing-approval extensions filed as 505(b)(2) (orphan exclusivity only, no PRV). For any database noted as relevant to Funnel A, verifying that the moiety's approval status in the US is absent is essential — NCATS Inxight Drugs and DailyMed are the primary authoritative sources for this check.

**Verification standard:** All numbers, HTTP status codes, file sizes, and quoted text are drawn directly from live HTTP responses obtained during the original agent's 110 tool calls (2026-08-06 ~00:26–00:35 UTC). Items verified during recovery on 2026-08-06 are labelled [NEWLY VERIFIED 2026-08-06].

---

## 1. DrugBank — VERIFIED

**Home:** `https://go.drugbank.com/`
**Current release:** v5.1.22 (released 2026-06-27)

### Licence architecture — three tiers

**Tier 1 — Academic (CC-BY-NC 4.0), currently SUSPENDED**

Confirmed from live fetch of `https://go.drugbank.com/releases/latest`:

> "These DrugBank datasets are released under a Creative Common's Attribution-NonCommercial 4.0 International License"

Eligibility criteria quoted verbatim:
> "The Academic License is free and available for researchers who meet the following criteria: You're a student, professor, or research associate with an academic institution. Your research is not primarily for the benefit of a commercial third party. You're building a tool solely for academic purposes."

**Status as of 2026-08-06:** Suspended. Quoted notice:
> "All Academic DrugBank dataset downloads are temporarily paused while we update how we distribute DrugBank data. We know these datasets matter to your work, and we'll restore access as soon as the updated program is in place."

Downloads affected: Full XML (204 MB), all SDF structures. A notification sign-up is available.

**Commercial-use verdict on Tier 1:** A for-profit building a derivative commercial database CANNOT use this tier. CC-BY-NC explicitly prohibits primary commercial use. The academic eligibility criteria add a second prohibition ("not primarily for the benefit of a commercial third party"). Even if the suspension lifts, a for-profit entity is barred.

**Tier 2 — CC0 "Open Data" (freely usable including commercially)**

Two datasets, confirmed live from `https://go.drugbank.com/releases/latest#open-data`:

> "The DrugBank Open Data datasets are public domain datasets that can be used freely in your application or project (including commercial use). It is released under a Creative Common's CC0 International License. To the extent possible under law, the person who associated CC0 with the DrugBank Open Data has waived all copyright and related or neighboring rights to the DrugBank Open Data."

| Dataset | Format | Size | Version |
|---|---|---|---|
| DrugBank Vocabulary (identifiers, names, synonyms) | CSV | 1.12 MB | 5.1.22 / 2026-06-27 |
| DrugBank Structures (structures, names, synonyms) | SDF | 5.16 MB | 5.1.22 / 2026-06-27 |

**Note:** Direct download URL pattern `https://go.drugbank.com/releases/5-1-22/downloads/all-drugbank-vocabulary` returns HTTP 403 without authentication (verified). Files are served from the authenticated DrugBank portal even for CC0 content; an account is needed but no licence fee applies for these two files.

**Commercial-use verdict on Tier 2:** YES — CC0 explicitly permits commercial use, derivative databases, and redistribution without attribution. These two files (identifiers + structures) are the only commercially-clean DrugBank data.

**Tier 3 — Commercial licence**

Requires contacting DrugBank sales. No pricing published. Covers all data not in Tiers 1–2 (pharmacology, drug interactions, ADMET, targets, pathways, clinical data, etc.).

**For-profit bottom line:** Only the two CC0 Open Data files (Vocabulary + Structures) may be incorporated into a commercial derivative database without a paid licence. The full therapeutic database requires a commercial agreement.

---

## 2. SIDER 4.1 — VERIFIED

**Home:** `https://sideeffects.embl.de/`
**Download page:** `https://sideeffects.embl.de/download/`

### Database contents (verified from live page fetch)

- 1,430 marketed medicines
- 5,868 distinct adverse reactions
- 139,756 drug-side effect associations
- Frequency data for ~40% of pairs
- MedDRA dictionary classifications (version 16.1)
- Drug-target relations and cross-references

### Licence — split by file type

All files verified with HEAD requests returning HTTP 200:

**Identifiers and mapping files — CC0 (commercial use permitted):**

| File | Size | Licence |
|---|---|---|
| `drug_names.tsv` | 34,759 bytes | CC0 |
| `drug_atc.tsv` | 32,760 bytes | CC0 |
| README | 3.2 KB | CC0 |

**MedDRA-derived files — CC-BY-SA 4.0 (ShareAlike — commercial use permitted with conditions):**

| File | Size | Licence |
|---|---|---|
| `meddra_all_indications.tsv.gz` | 344,689 bytes | CC-BY-SA 4.0 |
| `meddra_all_se.tsv.gz` | 2,381,171 bytes | CC-BY-SA 4.0 |
| `meddra_freq.tsv.gz` | 2,058,445 bytes | CC-BY-SA 4.0 |
| `meddra_all_label_indications.tsv.gz` | 5.6 MB | CC-BY-SA 4.0 |
| `meddra_all_label_se.tsv.gz` | 40.6 MB | CC-BY-SA 4.0 |
| `meddra.tsv.gz` | 1.0 MB | CC-BY-SA 4.0 |

Page states verbatim: "We used the MedDRA dictionary to extract side effects from drug labels. The results of this mapping are available under a Creative Commons Attribution-Share Alike 4.0 License."

**Historical FTP:** `ftp://xi.embl.de/SIDER/` — returned 404 during agent's fetch (HTTP 404). Files are served at HTTPS URLs above, not the old FTP.

### Update status

**Frozen.** Last update: 2015-10-21. Quoted from page: "no longer actively maintained due to lack of funding." EBI announced plans to develop a successor beginning in 2026. No EBI successor URL is live yet.

**Commercial-use verdict:**
- CC0 files (drug_names.tsv, drug_atc.tsv): YES, fully commercial-clean.
- CC-BY-SA files (MedDRA-derived): Permitted for commercial use, BUT derivatives must be released under CC-BY-SA 4.0 — a copyleft/ShareAlike condition. A for-profit may build a commercial product using these data, but any derivative database incorporating them must itself be CC-BY-SA licensed. Consult counsel before building a closed proprietary database on top of these files.

---

## 3. OFFSIDES and TWOSIDES — VERIFIED

**Source:** Tatonetti Lab (Columbia University)
**Download page:** `https://tatonettilab.org/offsides/`
**Direct file URLs (S3, verified HTTP 200):**
- `https://tatonettilab-resources.s3.us-west-1.amazonaws.com/nsides/OFFSIDES.csv.gz` — 68,762,346 bytes (last modified 2024-03-30)
- `https://tatonettilab-resources.s3.us-west-1.amazonaws.com/nsides/TWOSIDES.csv.gz` — 738,463,578 bytes (last modified 2024-03-30)

### Column schema (from README.txt, verified [NEWLY VERIFIED 2026-08-06])

**OFFSIDES.csv.gz** — drug single-agent off-label side effect signals:
```
drug_rxnorm_id       RxNORM identifier for the drug
drug_concept_name    RxNORM name string
condition_meddra_id  MedDRA identifier for the side effect
condition_concept_name  MedDRA name string
A    Reports for the drug that report the side effect
B    Reports for the drug that do not report the side effect
C    Reports for PSM-matched control drugs that report the side effect
D    Reports for PSM-matched controls without the side effect
PRR  Proportional reporting ratio = (A/(A+B)) / (C/(C+D))
PRR_error            Error estimate of the PRR
mean_reporting_frequency  A/(A+B)
```

**TWOSIDES.csv.gz** — drug-drug interaction safety signals (same PRR model, pairs):
Same schema extended with `drug_1_rxnorm_id`, `drug_1_concept_name`, `drug_2_rxnorm_id`, `drug_2_concept_name`.

**Methodology:** Propensity score matching (PSM) against FAERS, focusing on signals NOT already listed on structured product labels — hence "off-label" signals. Generates more reliable PRR estimates by controlling for confounders.

### Successor: OnSIDES / NSIDES (nsides.io)

The agent found `https://nsides.io/` resolving with an OnSIDES project listing. OnSIDES is extracted from structured product labels (complementary to OFFSIDES). OFFSIDES and TWOSIDES remain the primary off-label signal sources.

### Licence

**No explicit open licence is stated in the README.txt or on the download page.** The page is hosted under the Tatonetti Lab (academic). The README ends: "Please contact Dr. Nicholas Tatonetti for questions regarding these data."

**Commercial-use verdict:** UNVERIFIED — no published licence found in any checked location (README.txt, tatonettilab.org/offsides, nsides.io). Default copyright applies: no licence = all rights reserved. A for-profit must contact the lab for a licence before incorporating these data commercially. Email: use the Tatonetti Lab contact form or reach Nicholas Tatonetti at Columbia.

**Note for Funnel A/B screening:** OFFSIDES is a signal generator, not a regulatory source. Off-label signals from FAERS can surface indications in rare pediatric populations that were never formally studied — but they are hypotheses requiring clinical validation, not evidence of prior regulatory approval.

---

## 4. FAERS / openFDA Adverse Events — VERIFIED

### API endpoint and authentication

**Base URL:** `https://api.fda.gov/drug/event.json`

**Rate limits (verified from `https://open.fda.gov/apis/authentication/`):**
- Without API key: 240 requests/minute, 1,000 requests/day (per IP)
- With API key: 240 requests/minute, 120,000 requests/day (per key)
- API keys are free, obtained at `https://open.fda.gov/apis/`

**Authentication:** Pass `?api_key=YOUR_KEY` as query parameter, or `Authorization: Basic` header.

### Data coverage and scale

Live call to `https://api.fda.gov/drug/event.json?limit=1`:
- `meta.results.total`: **20,692,690** records
- `meta.last_updated`: 2026-07-30
- Coverage: FAERS reports from 2004 Q3 through 2026 Q2

### Record structure (verified from live API response)

Top-level keys: `safetyreportid`, `transmissiondate`, `receivedate`, `receiptdate`, `serious`, `seriousnessdeath`, `fulfillexpeditecriteria`, `companynumb`, `primarysource`, `sender`, `receiver`, `patient`

Under `patient`:
- `patientonsetage`, `patientonsetageunit`, `patientsex`, `patientdeath`
- `reaction[].reactionmeddrapt` — MedDRA preferred term
- `drug[]` containing: `drugcharacterization`, `medicinalproduct`, `drugauthorizationnumb`, `drugadministrationroute`, `drugindication`

**Paediatric PAH query test:** `search=patient.drug.drugindication:"pulmonary arterial hypertension"` → 215,018 matching reports (verified).

### Bulk download

From `https://api.fda.gov/download.json` (verified):
- `export_date`: 2026-08-03
- `total_records`: 20,692,690
- Quarters covered: 2004 Q3 through 2026 Q2 inclusive (1,767 partitions)
- 2026 Q2 has 36 parts, each ~90–107 MB as `.json.zip`
- Full URL pattern: `https://download.open.fda.gov/drug/event/{YEAR}q{Q}/drug-event-{NNN}-of-{TTT}.json.zip`
- Example verified: `https://download.open.fda.gov/drug/event/2026q2/drug-event-0001-of-0036.json.zip` (~91.99 MB)
- Note: Direct HEAD to these S3 URLs returns HTTP 403 from CloudFront; download via `api.fda.gov/download.json` manifest, not direct URL.

DailyMed monthly update confirmed available: `https://dailymed-data.nlm.nih.gov/public-release-files/dm_spl_monthly_update_jul2026.zip` (1,758,077,987 bytes, verified HTTP 200).

### Licence

From `https://open.fda.gov/license/` (verified):

> "FDA has waived all rights to the work worldwide under copyright law, including all related and neighboring rights, to the extent allowed by law. You can copy, modify, distribute, and perform the work, even for commercial purposes, all without asking permission."

This is a CC0 1.0 Universal dedication.

**Exception — GMDN content:** "Any data/information suppliers who wish to extract GMDN Content from this site in order to use it as a basis for creating and supporting commercial services such as alternative categorization, alternative GMDN Term assignment, mapping to other categorizations or ontologies, or for AI training purposes, must first obtain an appropriate license from The GMDN Agency." GMDN affects medical device event records; drug event records are not affected.

**Commercial-use verdict:** YES — openFDA drug adverse event data (FAERS) is CC0 and fully commercial-clean. The GMDN carve-out does not affect drug event records.

---

## 5. DailyMed SPL API — VERIFIED (Full Detail)

**Home:** `https://dailymed.nlm.nih.gov/`
**API base:** `https://dailymed.nlm.nih.gov/dailymed/services/v2/`
**Database size:** 158,361 drug labels (verified from API metadata, 2026-08-05)

### Full endpoint catalogue (verified from app-support page)

| Endpoint | Purpose | Formats |
|---|---|---|
| `/spls` | All SPL documents (paginated, 100/page) | XML, JSON |
| `/spls/{SETID}` | Specific SPL by SET ID (UUID) | XML, JSON |
| `/spls/{SETID}/history` | Version history for label | XML, JSON |
| `/spls/{SETID}/media` | Media links for label | XML, JSON |
| `/spls/{SETID}/ndcs` | NDC codes for label | XML, JSON |
| `/spls/{SETID}/packaging` | Packaging descriptions | XML, JSON |
| `/applicationnumbers` | All NDA/ANDA numbers | XML, JSON |
| `/drugclasses` | All drug classes from index | XML, JSON |
| `/drugnames` | All drug names | XML, JSON |
| `/ndcs` | All NDC codes | XML, JSON |
| `/rxcuis` | Product-level RxCUIs | XML, JSON |
| `/uniis` | All UNIIs | XML, JSON |

**Pagination:** Default 100 records/page. 158,361 labels = 1,584 pages. `next_page_url` provided in metadata.

**Query parameters (from live test):** `drug_name=aspirin` returns 1,072 labels. Filter by drug name supported.

**Response structure (verified from live JSON):**
```json
{
  "data": [
    {"spl_version": "3", "published_date": "Aug 05, 2026",
     "title": "MEDLINE (ASPIRIN) TABLET, DELAYED RELEASE [MEDLINE INDUSTRIES, LP]",
     "setid": "4b0c569a-ed7a-e104-e063-6394a90a6d54"}
  ],
  "metadata": {
    "db_published_date": "Aug 05, 2026 07:57:24PM EST",
    "total_elements": 158361,
    "total_pages": 1584,
    "current_page": 1,
    "next_page_url": "...?limit=1&page=2&pagesize=100"
  }
}
```

### SPL XML structure for indications and dosage extraction

SPL files are HL7 v3 CDA XML (`urn:hl7-org:v3` namespace). Verified by downloading and parsing a live label (aspirin SETID `4b0c569a-ed7a-e104-e063-6394a90a6d54`).

**Section codes for programmatic extraction:**

| LOINC code | Section |
|---|---|
| `34067-9` | INDICATIONS AND USAGE |
| `34068-7` | DOSAGE AND ADMINISTRATION |
| `34070-3` | CONTRAINDICATIONS |
| `34071-1` | WARNINGS |
| `43685-7` | WARNINGS AND PRECAUTIONS |
| `34073-7` | DRUG INTERACTIONS |
| `34084-4` | ADVERSE REACTIONS |
| `55106-9` | OTC ACTIVE INGREDIENT |
| `55105-1` | OTC PURPOSE |
| `50570-1` | OTC DO NOT USE |

**Live parse of aspirin label (verified):**
```
[55106-9] ACTIVE INGREDIENT: ['Aspirin 81 mg (NSAID)']
[55105-1] PURPOSE:           ['Pain reliever']
[34067-9] INDICATIONS AND USAGE: ['for the temporary relief of minor aches and pain...']
[34071-1] WARNINGS:         ["Reye's syndrome: Children and teenagers..."]
```

**Extraction approach for at-scale processing:**
1. Page through `/spls.json` (1,584 pages at 100/page)
2. For each SETID, fetch ZIP: `https://dailymed.nlm.nih.gov/dailymed/downloadzipfile.cfm?setId={setid}`
3. Unzip, parse XML, extract sections by LOINC code `34067-9` (indications) and `34068-7` (dosage)
4. For batch/incremental updates, use monthly ZIP releases via FTP or HTTPS

### Bulk download

HTTPS bulk: `https://dailymed-data.nlm.nih.gov/public-release-files/dm_spl_monthly_update_jul2026.zip` — 1,758,077,987 bytes (verified HTTP 200).
FTP bulk: `ftp://public.nlm.nih.gov/nlmdata/.dailymed/` — verified accessible; contains archival parts and daily/monthly/weekly update files.

Individual label ZIP: `https://dailymed.nlm.nih.gov/dailymed/downloadzipfile.cfm?setId={setid}`
Individual label PDF: `https://dailymed.nlm.nih.gov/dailymed/downloadpdffile.cfm?setId={setid}`
Older version ZIP: `https://dailymed.nlm.nih.gov/dailymed/getFile.cfm?type=zip&setid={setid}&version={versionnumber}`

**HTTP method:** GET only. No authentication required.

### Licence

NLM is a US Government agency. From `https://www.nlm.nih.gov/web_policies.html`:

> "Works produced by the U.S. government are not subject to copyright protection in the United States. Any such works found on National Library of Medicine (NLM) Web sites may be freely used or reproduced without permission in the U.S. Please acknowledge NLM as the source of the information by including the phrase 'Courtesy of the National Library of Medicine' or 'Source: National Library of Medicine.'"

The DailyMed metadata tag `<meta name="DC.Rights" content="Public Domain" />` was verified on NLM pages.

**Commercial-use verdict:** YES — US government work, public domain in the US. Attribution encouraged but not required by law. Non-US copyright considerations exist for abstracts from third-party publications embedded in some labels, but the SPL label text itself (authored by manufacturers, submitted to FDA) is regulatory filing content not subject to copyright protection by NLM.

**Relevance for Funnel A/B:** DailyMed is one of the two authoritative sources to confirm whether an active moiety has been previously approved under any NDA/ANDA in the US. Query `/applicationnumbers` or search drug names to confirm "never previously approved" status. Cross-reference with NCATS Inxight Drugs.

---

## 6. WHO VigiBase / VigiAccess — VERIFIED

**WHO Uppsala Monitoring Centre (UMC):** `https://who-umc.org/`
**VigiBase access page:** `https://who-umc.org/vigibase-data-access/`
**VigiAccess (public portal):** `https://www.vigiaccess.org/`

### VigiBase — the core database

VigiBase is the WHO global database of individual case safety reports. Coverage: 99% of world population (134 member countries). Verified from live page:

> "VigiBase data are available free of charge to member organisations in the WHO Programme for International Drug Monitoring, and for a fee to marketing authorisation holders, software providers, research organisations, and universities."

**Access tiers:**

| Tier | Who | Cost |
|---|---|---|
| Free | National pharmacovigilance centres (WHO PIDM members) | Free |
| VigiBase Extract | MAHs, CROs, research organisations, universities | Annual subscription, cost-recovery basis |
| VigiBase Search Services | As above | Annual subscription |
| VigiAccess (limited) | Public | Free (no registration) |

**VigiBase Extract specifics** (from `https://who-umc.org/vigibase-data-access/vigibase-extract/`, verified):
- "Aggregated and regularly updated case-level data available on request"
- "Already coded and structured to WHODrug and MedDRA standards"
- Confidential details excluded (narratives, medical history, lab data)
- Age and country generalised into groups/regions
- Pricing: "fees for all VigiBase Services are set on a cost recovery basis" — exact price requires contacting UMC

**Contact for pricing:** `https://who-umc.org/contact-information/` (no email or phone published on the access page).

### VigiAccess — public API

**API page:** `https://who-umc.org/vigibase-data-access/vigiaccess-api/` (verified resolving, HTTP 200)

Quoted from page: "VigiAccess provides a summarised view of VigiBase, grouping certain categories of data. The VigiAccess API enables connection to VigiAccess, allowing other systems to incorporate VigiAccess requests and perform functions not available on the VigiAccess website."

- Target users: "software vendors and developers integrating VigiAccess search functions into their products and systems"
- Data: statistical/aggregated only — "The full VigiBase data set contains information that is subject to strict data access conditions"
- Note: `https://www.vigiaccess.org/` loads JavaScript only (confirmed `Loading...` state with no scraped content)

### Licence

No publicly stated open licence for VigiBase data. Access is contractual. The VigiAccess public portal's aggregate statistics are freely viewable but no API terms are published without engagement.

**Commercial-use verdict:** No bulk commercial use without a paid subscription agreement with UMC. The VigiAccess API is available to vendors — contact UMC directly. Full VigiBase data requires an Extract agreement. For-profits must budget for an annual subscription.

---

## 7. CTD (Comparative Toxicogenomics Database) — VERIFIED

**Home:** `https://ctdbase.org/` — redirects (HTTP 302) and is bot-walled by a CAPTCHA for web browser access.
**Downloads directory:** `https://ctdbase.org/reports/` — **directly accessible via HTTP without captcha** (verified, returns Apache directory listing, HTTP 200).

### Database contents and key files (verified from directory listing)

All files in `https://ctdbase.org/reports/` — compressed as `.tsv.gz`, `.csv.gz`, and `.xml.gz`:

| File | Notes |
|---|---|
| `CTD_chemicals_diseases.tsv.gz` | 161,580,117 bytes (verified HEAD, last-modified 2026-07-30) |
| `CTD_curated_chemicals_diseases.tsv.gz` | Human-curated subset |
| `CTD_chem_gene_ixns.tsv.gz` | Chemical-gene interactions |
| `CTD_genes_diseases.tsv.gz` | Gene-disease associations |
| `CTD_curated_genes_diseases.tsv.gz` | Human-curated subset |
| `CTD_chemicals.tsv.gz` | Chemical dictionary |
| `CTD_diseases.tsv.gz` | Disease dictionary |
| `CTD_genes.tsv.gz` | Gene dictionary |
| `CTD_genes_pathways.tsv.gz` | Gene-pathway associations |
| `CTD_diseases_pathways.tsv.gz` | Disease-pathway associations |
| `CTD_chem_go_enriched.tsv.gz` | Chemical-GO enrichment |
| `CTD_chem_pathways_enriched.tsv.gz` | Chemical-pathway enrichment |
| `pc_CTD_genes_diseases.csv.gz` | Predicted (computational) gene-disease |
| `CTD_pheno_term_ixns.tsv.gz` | Phenotype-term interactions |
| `CTD_exposure_events.tsv.gz` | Exposure data |
| `CTD_anatomy.tsv.gz` | Anatomy ontology |
| `CTD_UniProtToCTDIdMapping.txt.gz` | UniProt mapping |

**CTD_chemicals.tsv.gz header** — verified [NEWLY VERIFIED 2026-08-06] by streaming decompression of first 50 KB:

```
# The Comparative Toxicogenomics Database (CTD) - http://ctdbase.org/
#   Copyright 2002-2012 MDI Biological Laboratory. All rights reserved.
#   Copyright 2012-2026 NC State University. All rights reserved.
#
# Use is subject to the terms set forth at http://ctdbase.org/about/legal.jsp
# These terms include:
#   1. All forms of publication (e.g., web sites, research papers, databases,
#      software applications, etc.) that use or rely on CTD data must cite CTD.
#   2. All electronic or online applications must include hyperlinks from
#      contexts that use CTD data to the applicable CTD data pages.
#   3. You must notify CTD, and describe your use of our data.
#   4. For quality control purposes, you must provide CTD with periodic
#      access to your publication of our data.
# Report created: Thu Jul 30 13:48:35 EDT 2026
#
# Fields:
# ChemicalName  ChemicalID  CasRN  PubChemCID  PubChemSID  DTXSID  InChIKey  Definition ...
```

The web access to `https://ctdbase.org/about/legal.jsp` is blocked by CAPTCHA; however the full licence text is reproduced verbatim in the file header above.

**CTD Batch Query API** (`https://ctdbase.org/tools/batchQuery.go`): Returns CAPTCHA page for both GET and POST requests — not programmatically accessible without browser session.

### Update cadence

Verified: `CTD_chemicals_diseases.tsv.gz` last-modified 2026-07-30, confirming monthly or near-monthly updates.

### Licence

Proprietary, all rights reserved (MDI Biological Laboratory 2002–2012; NC State University 2012–2026). Four conditions apply, the most operationally significant being:

1. Citation required in all publications
2. Hyperlinks to CTD data pages required in all online applications
3. Must notify CTD and describe use
4. Must provide CTD periodic access for QC

**There is no open licence (no CC, no CC0).** All use is "subject to the terms at http://ctdbase.org/about/legal.jsp".

**Commercial-use verdict:** RESTRICTED. The licence requires notification, hyperlinks, citation, and QC access — conditions unusual for a commercial proprietary database. This is not a standard commercial or academic open licence; it is a custom access agreement with obligations. A for-profit building a closed derivative database would need to negotiate with NC State University, as the hyperlink and notification requirements are difficult to satisfy in an enclosed commercial product. Contact: `ctd-feedback@ctdbase.org`.

---

## 8. NCATS Inxight Drugs — VERIFIED

**Home:** `https://drugs.ncats.io/`
**API base:** `https://drugs.ncats.io/api/v1/`
**Count endpoint:** `https://drugs.ncats.io/api/v1/substances/@count` → `167131` (verified live, HTTP 200)

### Database contents (verified from home page and API)

| Category | Count |
|---|---|
| All substances | 167,131 |
| US Approved Drugs | 2,638 |
| Marketed Drugs | 13,227 |
| Investigational Drugs | 10,302 |

Data includes: marketing/regulatory status, FDA UNII identifiers, rigorous chemical structure definitions (SMILES, InChI, formula, stereochemistry), biological activity, clinical use, pharmacokinetics, adverse events, drug-drug interactions (from March 2025 dataset update).

The FDA Global Substance Registration System (GSRS) at `https://gsrs.ncats.nih.gov/` has 173,081 substances (live API verified).

### API endpoints (verified from `https://drugs.ncats.io/api/v1/`)

All accessible at `https://drugs.ncats.io/api/v1/{endpoint}`:

| Endpoint | Description |
|---|---|
| `substances` | Main resource — GInAS substances |
| `substances/{UUID}` | Single substance by UUID |
| `substances?q={query}` | Full-text / field search |
| `substances/@count` | Total count |
| `structures` | Chemical structure records |
| `codes` | Identifier codes (UNII, CAS, RxCUI, etc.) |
| `names` | Substance names |
| `references` | Citation records |
| `relationships` | Substance relationships |
| `vocabularies` | Controlled vocabularies |
| `xrefs` | Cross-references |

**Key query patterns:**
- By UNII: `https://drugs.ncats.io/api/v1/substances?q=approvalID:{UNII}`
- By name: `https://drugs.ncats.io/api/v1/substances?q=names.name:{NAME}&substanceClass=chemical`
- Chemical + approved: `?q=substanceClass:chemical+AND+status:approved` → 167,131 total (query returns all substances, approved filter appears to be a display filter rather than a strict data filter)

**JSON record structure (verified from live substance record):**
Top-level: `id`, `version`, `created`, `etag`, `uuid`, `deprecated`, `substanceClass`, `status`, `approvalID` (= UNII), `_name`, `names[]`, `codes[]`, `relationships[]`, `references[]`, `structure{}`, `moieties[]`

Code systems present in sample records: `EVMPD`, `CAS`, `RXCUI`, `FDA UNII`, `ECHA (EC/EINECS)`, `EPA CompTox`, `DAILYMED`, `EMA ASSESSMENT REPORTS`

**Downloads page:** `https://drugs.ncats.io/downloads` returned HTTP 401 Unauthorized during agent's fetch — bulk file download requires authentication or a different access path. The home page referenced downloads available as of March 2025; exact URLs unconfirmed.

### Licence

Quoted verbatim from home page (verified live):

> "All facts appearing in these datasets are in the public domain and may be reproduced or copied without NCATS permission. If you use Inxight in your work, please cite our manuscript: Vishal B. Siramshetty, Ivan Grishagin, [...] Nucleic Acids Research..."

**Commercial-use verdict:** YES — explicitly public domain. No restriction on commercial use, derivative databases, or redistribution. API is unauthenticated for read access.

**Critical Funnel A application:** The `approvalID` field is the FDA UNII. Checking whether a UNII exists in this database with `status: approved` and cross-referencing with DailyMed `/applicationnumbers` is the most reliable automated method to confirm "never previously approved in the US" for Funnel A eligibility.

---

## 9. Drug Repurposing-Specific Curated Resources

### 9.1 DrugCentral (not duplicated from prior report — licence clarification)

Covered in `09-cheminformatics-repurposing-dbs.md`. Noted here: DrugCentral data is openly available at `https://drugcentral.org/` under CC BY 4.0, permitting commercial use with attribution.

### 9.2 OnSIDES / NSIDES (nsides.io) — VERIFIED

**URL:** `https://nsides.io/` (verified resolving, HTTP 200)
OnSIDES is the successor project to OFFSIDES for label-based adverse event extraction, using NLP on FDA structured product labels rather than spontaneous reports. Listed resources include OnSIDES, OFFSIDES/TWOSIDES, AwareDX, ManySIDES.

**Licence:** No explicit licence stated on nsides.io. Same situation as OFFSIDES — contact the Tatonetti Lab.

### 9.3 repoDB (not duplicated — licence note)

Covered in `09-cheminformatics-repurposing-dbs.md`. CC0.

---

## Summary: Licence Cleanliness for Commercial Use

| Database | Licence | Commercial Derivative DB? | Conditions |
|---|---|---|---|
| **DrugBank — CC0 Open Data** (Vocabulary + Structures only) | CC0 | YES | Two small files only (identifiers + SMILES) |
| **DrugBank — Full DB (academic)** | CC-BY-NC 4.0, SUSPENDED | NO | For-profits excluded; downloads paused |
| **DrugBank — Full DB (commercial)** | Proprietary | YES (with licence) | Contact sales; price undisclosed |
| **SIDER 4.1 — drug_names, drug_atc** | CC0 | YES | Frozen 2015 data |
| **SIDER 4.1 — MedDRA files** | CC-BY-SA 4.0 | YES (with conditions) | Derivatives must be CC-BY-SA; copyleft |
| **OFFSIDES / TWOSIDES** | No stated licence | UNCLEAR | Contact Tatonetti Lab before commercial use |
| **FAERS / openFDA** | CC0 | YES | GMDN carve-out (medical devices only, not relevant here) |
| **DailyMed SPL** | US Gov public domain | YES | Attribution encouraged, not required |
| **WHO VigiBase / VigiAccess** | Contractual | YES (with paid subscription) | Annual fee; contact UMC |
| **CTD** | Custom / all rights reserved | RESTRICTED | Notify CTD, hyperlink, cite, QC access required; needs negotiation |
| **NCATS Inxight Drugs** | US Gov public domain | YES | Cite NAR paper (strongly encouraged) |

---

## Unfinished — Worth Re-Running

**CTD legal.jsp full text:** The page `https://ctdbase.org/about/legal.jsp` returns a CAPTCHA wall for all automated fetches. The file header provides the four key terms but the full legal text including any commercial-use carve-outs, fee schedules, or sublicensing provisions was not obtained. If building anything commercial on CTD, obtain the full terms via a browser session or contact `ctd-feedback@ctdbase.org`.

**DrugBank commercial pricing:** `https://go.drugbank.com/legal/terms_of_use` returned HTTP 403 Forbidden. The commercial licence pricing is not published anywhere on the public site. A for-profit must contact DrugBank sales directly.

**NCATS Inxight bulk download:** `https://drugs.ncats.io/downloads` returned HTTP 401. The agent could not determine the exact URLs or format for bulk substance export. An authenticated session or NLM/NCATS API key may be required.

**OFFSIDES column header structure:** Range-based fetches of the `.csv.gz` files returned incomplete gz blocks (file too large for partial range decompression). The schema was recovered from README.txt but the actual column headers were not directly confirmed from the file.

**WHO VigiAccess API terms and pricing:** The VigiAccess API page at `https://who-umc.org/vigibase-data-access/vigiaccess-api/` describes the API but its full terms, any cost-recovery fee, and rate limits are not published — only available after contact with UMC.

---

## URL Ledger

### VERIFIED

| URL | Status | What was confirmed |
|---|---|---|
| `https://go.drugbank.com/releases/latest` | 200 | CC0 open data, CC-BY-NC full DB, academic suspension notice, v5.1.22 |
| `https://go.drugbank.com/releases/latest#open-data` | 200 | CC0 Vocabulary (1.12 MB) + Structures (5.16 MB), 2026-06-27 |
| `https://go.drugbank.com/releases/5-1-22/downloads/all-drugbank-vocabulary` | 403 | Returns 403 without auth (expected for authenticated download) |
| `https://sideeffects.embl.de/` | 200 | SIDER 4.1 contents, CC-BY-SA 4.0 licence, EBI successor announcement |
| `https://sideeffects.embl.de/download/` | 200 | Full file listing with sizes and per-file licences |
| `https://sideeffects.embl.de/media/download/drug_names.tsv` | 200 | 34,759 bytes, CC0 |
| `https://sideeffects.embl.de/media/download/meddra_all_se.tsv.gz` | 200 | 2,381,171 bytes, last-modified 2026-06-12, CC-BY-SA 4.0 |
| `https://tatonettilab.org/offsides/` | 200 | OFFSIDES.csv.gz + TWOSIDES.csv.gz S3 links |
| `https://tatonettilab-resources.s3.us-west-1.amazonaws.com/nsides/OFFSIDES.csv.gz` | 200 | 68,762,346 bytes, last-modified 2024-03-30 |
| `https://tatonettilab-resources.s3.us-west-1.amazonaws.com/nsides/TWOSIDES.csv.gz` | 200 | 738,463,578 bytes, last-modified 2024-03-30 |
| `https://tatonettilab-resources.s3.us-west-1.amazonaws.com/nsides/README.txt` | 200 | Column schema, no licence statement [NEWLY VERIFIED 2026-08-06] |
| `https://api.fda.gov/drug/event.json?limit=1` | 200 | 20,692,690 records, last_updated 2026-07-30, record structure |
| `https://open.fda.gov/apis/authentication/` | 200 | Rate limits: 240/min, 1,000/day without key; 120,000/day with key |
| `https://open.fda.gov/license/` | 200 | CC0, GMDN exception for medical devices |
| `https://open.fda.gov/terms/` | 200 | CC0 verbatim, GMDN licence text |
| `https://api.fda.gov/download.json` | 200 | export_date 2026-08-03, 20,692,690 records, 2004–2026 Q2, 1,767 partitions |
| `https://dailymed.nlm.nih.gov/dailymed/services/v2/spls.json?limit=1` | 200 | 158,361 labels, pagination structure, 2026-08-05 |
| `https://dailymed.nlm.nih.gov/dailymed/services/v2/spls.json?drug_name=aspirin` | 200 | 1,072 aspirin labels |
| `https://dailymed.nlm.nih.gov/dailymed/app-support-web-services.cfm` | 200 | Full endpoint catalogue |
| `https://dailymed.nlm.nih.gov/dailymed/spl-resources-all-drug-labels.cfm` | 200 | Monthly/daily update ZIP links |
| `https://dailymed-data.nlm.nih.gov/public-release-files/dm_spl_monthly_update_jul2026.zip` | 200 | 1,758,077,987 bytes |
| `https://dailymed.nlm.nih.gov/dailymed/downloadzipfile.cfm?setId={setid}` | 200 | Returns SPL ZIP with XML + media |
| `ftp://public.nlm.nih.gov/nlmdata/.dailymed/` | 200 | FTP directory listing confirmed |
| `https://www.nlm.nih.gov/web_policies.html` | 200 | US Gov public domain, attribution encouraged |
| `https://www.nlm.nih.gov/databases/download.html` | 200 | NLM download/copyright policy |
| `https://who-umc.org/vigibase-data-access/` | 200 | Access tiers, free for PIDM members, fee for others |
| `https://who-umc.org/vigibase-data-access/vigibase-extract/` | 200 | Annual subscription, cost-recovery, exclusions |
| `https://who-umc.org/vigibase-data-access/vigiaccess-api/` | 200 | API for vendors, statistical data only |
| `https://ctdbase.org/reports/` | 200 | Apache directory listing, all files accessible |
| `https://ctdbase.org/reports/CTD_chemicals_diseases.tsv.gz` (HEAD) | 200 | 161,580,117 bytes, last-modified 2026-07-30 |
| `https://ctdbase.org/reports/CTD_chemicals.tsv.gz` (stream, 50KB) | 200 (206) | Licence header verbatim [NEWLY VERIFIED 2026-08-06] |
| `https://drugs.ncats.io/api/v1/substances/@count` | 200 | `167131` |
| `https://drugs.ncats.io/api/v1/` | 200 | Full endpoint list |
| `https://drugs.ncats.io/api/v1/substances?format=json&limit=1` | 200 | Record structure, code systems |
| `https://drugs.ncats.io/` | 200 | Public domain statement, 167,131 substances |
| `https://gsrs.ncats.nih.gov/api/v1/substances/@count` | 200 | `173081` |
| `https://nsides.io/` | 200 | OnSIDES project listing [NEWLY VERIFIED 2026-08-06] |

### UNVERIFIED

| URL | Status | Reason |
|---|---|---|
| `https://go.drugbank.com/legal/terms_of_use` | 403 | Blocked without authentication |
| `https://go.drugbank.com/commercial` | Bot-blocked | Cloudflare JS challenge |
| `https://ctdbase.org/about/legal.jsp` | Captcha | Bot wall; full terms not retrieved |
| `https://ctdbase.org/` | 302 redirect | Redirects to captcha wall |
| `https://ctdbase.org/tools/batchQuery.go` | Captcha | Batch API behind captcha for all attempts |
| `https://drugs.ncats.io/downloads` | 401 | Unauthorized |
| `https://drugs.ncats.io/substances/download` | 404 | Not found |
| `https://ftp.ebi.ac.uk/pub/databases/sider/2015_10_21/` | 404 | Old SIDER FTP path no longer valid |
| `https://vigiaccess.org/` | JS-only | Renders `Loading...`; no machine-readable content |
| `https://www.who.int/teams/regulation-prequalification/medicines/pharmacovigilance` | 404 | WHO URL restructured |
| `https://download.open.fda.gov/drug/event/2025q4/drug-event-0001-of-0001.json.zip` | 403 | CloudFront; use download.json manifest |
| DrugBank commercial pricing | Not published | No public price list; contact sales |
| WHO VigiAccess API pricing/terms | Not published | Requires UMC engagement |
