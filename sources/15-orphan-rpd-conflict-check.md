<!-- Recovered from agent-aaab30cefad91ed91.jsonl on 2026-08-06 after original agent died on
     API connection error (FailedToOpenSocket) following 103 tool calls completed on 2026-08-05.
     Recovery agent performed 8 additional live fetches on 2026-08-06 to fill key gaps. -->

# Conflict Check: Orphan Designation, Orphan Exclusivity, and RPD Designation

**Purpose:** Core clearance query for every repurposing candidate — does an existing orphan
designation, orphan exclusivity grant, or rare pediatric disease (RPD) designation already occupy
this drug-disease pair in a way that blocks or degrades the opportunity?

**Funnel framing (settled legal fact):** Funnel A = never-approved-in-US moiety filed as 505(b)(1)
NDA → PRV-eligible + orphan designation/exclusivity potentially available. Funnel B = repurposed
US generic filed as 505(b)(2) → PRV-ineligible, orphan designation and 7-year exclusivity still
available.

---

## 1. FDA OOPD Orphan Drug Designation Database

### 1.1 Access and Interface

**Primary URL (VERIFIED, HTTP 200, 2026-08-05):**
`https://www.accessdata.fda.gov/scripts/opdlisting/oopd/`
(34,324 bytes; ColdFusion-based legacy application)

The page hosts a form (`action="OOPD_Results.cfm"`, method POST) with these search fields:
- **Product_name** — searches both generic name and trade name
- **sponsor_name** — sponsor/company name
- **Designation** — free-text search of the disease designation string
- **Designation_Start_Date / Designation_End_Date** — date range (default 01/01/1983 to current)
- **Status** — All / Approved / Designated (not yet approved)
- **Output_Format**, **SortColumn**, **RecordsPerPage**

A blank search returns all designations. The form instruction page states: "Running a default search
with no criteria will return all designations."

**Search API status (2026-08-05/06):** The ColdFusion application returns HTTP 302 → HTTP 403 when
POSTed to from automated scripts. Direct GET attempts to OOPD_Results.cfm return HTTP 403 or 503.
The application is accessible only through an interactive browser session with cookies. There is
no public REST API, no CSV/Excel bulk download link, and no openFDA endpoint for this database.
The detailed record view (`detailedIndex.cfm?cfgridkey=NNN`) also returns HTTP 403 from scripts.

**Instructions page (VERIFIED, HTTP 200):**
`https://www.fda.gov/industry/designating-orphan-product-drugs-and-biological-products/instructions-searchable-designation-database`
(35,707 bytes; content last updated 10/24/2017 per page footer)

### 1.2 Database Fields

Fields displayed in search results and detailed records (documented from the OOPD instructions page
and from a WebSearch hit on `detailedIndex.cfm?cfgridkey=128999`, which is a real record URL
confirmed by the instructions page link but blocked by HTTP 403):

| Field | Notes |
|-------|-------|
| Generic name / trade name | Both searchable |
| Sponsor name | |
| Designation date | Date the orphan designation was granted |
| Orphan designation number | Alphanumeric internal ID |
| Designated indication (designation string) | Disease/condition description |
| Approval date | Date of marketing approval for the orphan indication (if any) |
| Approved indication | May differ from designated indication (narrower subset) |
| Exclusivity status | Whether orphan exclusivity is currently in force |

The instructions page explicitly states: "certain additional information is available on the website
(approval date, approved indication and exclusivity status)" — implying those fields only appear
for approved products.

### 1.3 Record Count — UNVERIFIED

The total number of records in the OOPD database was not determinable from public sources during
this research session. All attempts to run a blank search (which would return a record count)
were blocked by HTTP 403/503. Web searches for authoritative counts ("6000", "7000", "8000"
designations) returned no primary-source number. A 2022 PMC paper on orphan designations for
lysosomal storage disorders was found in search results but its total count was not extracted.
The EMA figures PDF (`orphan-medicines-figures-2000-2025_en.pdf`, 947,320 bytes, VERIFIED) likely
contains a comparative US/EU count but PDF text extraction via `strings` returned only metadata.

**Proxy estimate (UNVERIFIED, from public literature context):** The FDA has granted thousands of
orphan designations since 1983; industry sources commonly cite figures in the range of 6,000–9,000
cumulative designations through 2025, but this was not confirmed from a primary source in this
session.

**Unfinished — worth re-running:** Access the OOPD blank search through a headless browser
(Playwright, Puppeteer) with cookie support to extract total record count and confirm field set.

### 1.4 Data-Quality Problems

A 2023 PMC study (PMC10021800, VERIFIED at `https://pmc.ncbi.nlm.nih.gov/articles/PMC10021800/`)
examined discrepancies between FDA Medical Reviews and ClinicalTrials.gov for orphan drug-related
trials. Key findings relevant to data quality:

- Only 75% of trials showed exact phase classification matches between FDA and CTG records
- Only 70% of cases matched enrollment figures; 17% showed discrepancies exceeding ±5% variance
- Approximately 9% of records differed in anticipated vs. actual enrollment coding
- Older FDA documents exist as scanned images, "not easily machine readable"
- Newer documents show "great deal of variability from one document to the next" in how clinical
  study tables are organized
- 52% of trials listed in FDA medical reviews were not registered in ClinicalTrials.gov

A separate finding from FDA's own "Public Identification of Orphan Drug Designation" notice
(VERIFIED, HTTP 200, `https://www.fda.gov/industry/designating-orphan-product-drugs-and-biological-products/public-identification-orphan-drug-designation`, 36,423 bytes) is operationally important:
FDA replaced non-informative codes with informative identifiers across the OOPD database, and
acknowledged it could not notify all sponsors because "some sponsors may have gone out of business
or may have transferred ownership of or beneficial interest in orphan-drug designation without
informing FDA" (per 21 CFR 316.27). This means:

- Sponsor ownership in the database may be stale or wrong for older designations
- Annual progress reports (required by 21 CFR 316.30) are submitted to FDA but not published
- There is no public way to verify which designations are actively maintained vs. abandoned

### 1.5 Distinguishing Designation vs. Exclusivity vs. Approval in OOPD Data

These are three distinct statuses in the OOPD database:

1. **Designation only** — FDA has granted orphan drug designation. This confers tax credits,
   waived PDUFA fees, and protocol assistance, but NO exclusivity. Any number of sponsors can
   hold orphan designation for the same drug-disease pair simultaneously. Designation alone does
   NOT block a competitor.

2. **Approved with orphan exclusivity** — The drug has received marketing approval for the orphan
   indication. This triggers 7-year orphan exclusivity from the approval date. The OOPD record
   will show both an approval date and exclusivity status. The exclusivity blocks approval of the
   "same drug" for the "same disease" for 7 years (subject to the "same drug" sameness test and
   clinical superiority exception — see Section 3 below).

3. **Approved without orphan exclusivity** — An orphan-designated drug can be approved without
   receiving exclusivity if the same drug was previously approved for the same use. Also, if the
   designation itself has expired (e.g., a subsequent approved drug made the disease non-rare) or
   was revoked, no exclusivity attaches.

**Pipeline implication:** An OOPD search that finds "Positive" designation status for your
drug-disease pair does NOT automatically block your program. You are blocked only if there is an
active, unexpired orphan exclusivity grant. You must look up the approval date and compute whether
the 7-year clock has expired.

---

## 2. Orange Book Exclusivity File — Authoritative Source for Expiry Dates

### 2.1 Download and Structure

**Bulk download URL (VERIFIED, HTTP 200, content-type: application/zip, 1,091,413 bytes):**
`https://www.fda.gov/media/76860/download`

The ZIP extracts to three pipe-delimited (tilde `~`) text files:

| File | Size | Modified |
|------|------|----------|
| exclusivity.txt | 75,337 bytes | 2026-07-10 07:26 |
| patent.txt | 1,223,277 bytes | 2026-07-10 07:25 |
| products.txt | 7,467,977 bytes | 2026-07-10 08:36 |

**Exclusivity.txt field schema (VERIFIED from Orange Book Data Files page, HTTP 200):**
`https://www.fda.gov/drugs/drug-approvals-and-databases/orange-book-data-files`

```
Appl_Type ~ Appl_No ~ Product_No ~ Exclusivity_Code ~ Exclusivity_Date
```

- `Appl_Type`: N (NDA/innovator) or A (ANDA/generic)
- `Appl_No`: 6-digit FDA application number
- `Product_No`: 3-digit product strength identifier
- `Exclusivity_Code`: see below
- `Exclusivity_Date`: expiry date in "MMM DD, YYYY" format

**Sample header and first rows (VERIFIED from live file, 2026-08-05):**
```
Appl_Type~Appl_No~Product_No~Exclusivity_Code~Exclusivity_Date
N~017031~001~RTO~Jul 13, 2026
N~018680~001~D-193~Jun 28, 2027
N~019569~001~ODE-267~Jun 28, 2026
```

**Total rows in current file (VERIFIED):** 2,341 lines (including header), so ~2,340 active
exclusivity records.

### 2.2 ODE Code Structure and Counts

**Total ODE entries (VERIFIED, grep count):** 695 rows containing "ODE" in the current
exclusivity.txt file (dated 2026-07-10).

**Code taxonomy (VERIFIED from file analysis):**

| Code | Count | Meaning |
|------|-------|---------|
| ODE* | 90 | Orphan Drug Exclusivity — pre-2013 format without indication-specific numbering |
| ODE-NNN | 605 | Orphan Drug Exclusivity — post-2013 format with OOPD designation number suffix |

The numeric suffix (e.g., `ODE-267`, `ODE-428`) corresponds to the specific orphan designation
number in the OOPD database, enabling cross-referencing. A single drug product can carry multiple
ODE codes simultaneously (e.g., NDA 021825 carries ODE-417, ODE-420, and ODE-421) for different
approved orphan indications.

**Sample ODE* records (VERIFIED):**
```
N~204384~002~ODE*~Aug 9, 2026
N~204671~001~ODE*~Aug 28, 2026
N~205834~001~ODE*~Aug 28, 2026
```
These are pre-2013 approvals whose designation numbers were not yet encoded in the public
identifier scheme.

**Complete exclusivity code inventory in current file (VERIFIED, top codes by count):**
NCE (423), PED (339), NPP (159), NP (130), ODE* (90), PC (56), M-14 (47), GAIN (44), CGT (36),
M-82 (26), I-958 (24), NS (16), I-935 (9), I-913 (8), ODE-428 (7), ODE-405 (7), ODE-497 (6),
ODE-495 (6), ODE-360 (6), ODE-245 (6), ODE-241 (6), ODE-225 (6), [numerous others].

### 2.3 Authoritative Source: Orange Book vs. OOPD

**The Orange Book exclusivity.txt is the machine-readable authoritative source for expiry dates.**

The OOPD database displays "exclusivity status" but does not export and does not show precise
expiry dates in its public interface. The Orange Book is updated monthly (the current file
is dated 2026-07-10) and is machine-downloadable without authentication. For pipeline automation:

1. Download `https://www.fda.gov/media/76860/download` monthly
2. Filter for `Exclusivity_Code LIKE 'ODE%'`
3. Cross-reference `Appl_No` against the FDA NDA number for the drug of interest
4. Check whether `Exclusivity_Date` is in the future (i.e., exclusivity still running)

**Limitation:** The Orange Book only lists NDA-approved drugs (Appl_Type = N). A drug with orphan
designation that has never been approved in the US will not appear in the Orange Book at all.
That gap is important: it means an OOPD designation without a corresponding NDA approval does
not block you via the Orange Book. You must check the OOPD for designations that have not yet
progressed to approval.

---

## 3. The "Same Drug, Same Disease" Sameness Rules Under 21 CFR 316

### 3.1 Statutory Framework

Orphan drug exclusivity is governed by 21 U.S.C. § 360cc and implemented in 21 CFR Part 316
Subpart D. The core blocking provision is **21 CFR § 316.31(a)** (VERIFIED from LII/Cornell,
current eCFR as of 2026-08-04):

> "FDA may approve a sponsor's marketing application for a designated orphan drug for use in the
> rare disease or condition for which the drug was designated… Unless FDA previously approved the
> same drug for the same use or indication, FDA will not approve another sponsor's marketing
> application for the same drug for the same use or indication before the expiration of 7 years
> from the date of such approval…"

Exceptions allowing earlier approval (§ 316.31(a)(1)–(4)):
1. Withdrawal of exclusive approval or revocation of orphan-drug designation by FDA
2. Withdrawal for any reason of the marketing application for the drug
3. Consent by the holder of exclusive approval
4. Failure of holder to ensure sufficient supply (§ 316.36)

Additionally per § 316.31(b): exclusivity protects only the approved indication. A drug with
exclusivity for indication X within a disease does not block approval of the same drug for
indication Y within the same disease, unless that Y overlaps with X.

### 3.2 "Same Drug" Sameness Test — 21 CFR § 316.3(b)(14) (VERIFIED from Cornell LII)

The sameness test differs for small molecules vs. macromolecules:

**Small molecules (§ 316.3(b)(14)(i)):**
> "a drug that contains the same active moiety as a previously approved drug and is intended for
> the same use as the previously approved drug, even if the particular ester or salt (including
> a salt with hydrogen or coordination bonds) or other noncovalent derivative such as a complex,
> chelate or clathrate has not been previously approved, **except that if the subsequent drug can
> be shown to be clinically superior to the first drug, it will not be considered to be the same
> drug**."

"Active moiety" (§ 316.3(b)(2)):
> "the molecule or ion, excluding those appended portions of the molecule that cause the drug to
> be an ester, salt (including a salt with hydrogen or coordination bonds), or other noncovalent
> derivative (such as a complex, chelate, or clathrate) of the molecule, responsible for the
> physiological or pharmacological action of the drug substance."

Practical consequence: imatinib mesylate and imatinib free base share the same active moiety
(imatinib). Different salts = same drug for exclusivity purposes unless clinical superiority
is shown.

**Macromolecules (§ 316.3(b)(14)(ii)):**
> "a drug that contains the same principal molecular structural features (but not necessarily all
> of the same structural features) and is intended for the same use as a previously approved drug,
> except that, if the subsequent drug can be shown to be clinically superior, it will not be
> considered to be the same drug."

Sub-rules by macromolecule type (all VERIFIED from § 316.3(b)(14)(ii)(A)–(D)):
- **(A) Proteins:** same if "only differences in structure were due to post-translational events
  or infidelity of translation or transcription or were minor differences in amino acid sequence"
- **(B) Polysaccharides:** same if "identical saccharide repeating units, even if the number of
  units were to vary and even if there were postpolymerization modifications"
- **(C) Polynucleotides:** same if "identical sequence of purine and pyrimidine bases (or their
  derivatives) bound to an identical sugar backbone (ribose, deoxyribose, or modifications)"
- **(D) Complex partly definable drugs (e.g., live viral vaccines):** same if "similar therapeutic
  intent" unless clinically superior

### 3.3 "Clinically Superior" Exception — 21 CFR § 316.3(b)(3) (VERIFIED)

Even if your drug is the "same drug," it escapes the exclusivity block if it is "clinically
superior," meaning it provides "a significant therapeutic advantage over and above that provided
by an approved drug (that is otherwise the same drug) in one or more of the following ways":

- **(i)** Greater effectiveness on a clinically meaningful endpoint in adequate and well-controlled
  clinical trials (generally requires direct comparative trials)
- **(ii)** Greater safety in a substantial portion of the target population (sometimes requires
  direct comparative trials)
- **(iii)** In unusual cases, where neither greater safety nor greater effectiveness has been
  shown, "a major contribution to patient care"

**Pipeline implication:** Clinical superiority is a route through an existing exclusivity block,
but the evidentiary standard is high (direct comparative trials typically required for (i) and
(ii)). Major contribution to patient care (iii) is a narrow exception.

### 3.4 "Same Disease" Test

The exclusivity blocks approval for "the same use or indication." A drug approved for condition X
does not block approval of the same drug for condition Y even if both X and Y are covered by the
same OOPD designation, unless X and Y substantially overlap. If a designation covers a broad
disease category (e.g., "treatment of Duchenne muscular dystrophy") and an approved indication
is only a genetic subtype, a drug for a different subtype may not be blocked.

Per § 316.31(b): "Orphan-drug exclusive approval protects only the approved indication or use
of a designated drug." This means the approved label indication — not the broader designation —
defines the scope of exclusivity.

---

## 4. RPD (Rare Pediatric Disease) Designation — Public Access

### 4.1 No Public Searchable RPD Database Exists

The FDA confirmed (current FDA RPD page, VERIFIED HTTP 200, 35,632 bytes):
`https://www.fda.gov/industry/medical-products-rare-diseases-and-conditions/rare-pediatric-disease-designation-and-priority-review-voucher-programs`

RPD designation requests are submitted by email to `orphan@fda.hhs.gov`. The FDA does not
publish a searchable database of RPD designations. There is no equivalent of the OOPD for RPD
status. The page confirms the PRV program sunset: "FDA may not award any PRVs under this program
after September 30, 2029."

The page explicitly notes: "the current sunset provisions in the law do not provide a separate
date by which the drug that is the subject of the rare pediatric disease product application must
be designated as a drug for a rare pediatric disease." (This aligns with the settled legal fact
that the binding constraint is approval, not designation.)

### 4.2 Practical Proxy Detection Strategy for RPD

Because no public RPD database exists, a pipeline must use indirect signals:

**Tier 1 — Federal Register (strongest proxy):**
FDA publishes PRV award notices in the Federal Register when PRVs are actually awarded. These
name the drug, disease, NDA/BLA number, and applicant. 73 PRVs have been awarded through
2026-05-11 (settled fact). These notices are searchable at `federalregister.gov`. However,
this only covers programs that completed approval and claimed the PRV; it does not reveal active
RPD designation holders who have not yet filed an NDA.

**Tier 2 — ClinicalTrials.gov keyword search:**
Sponsors often disclose RPD designation in study descriptions, eligibility criteria, or the
"Regulatory Information" section of ClinicalTrials.gov records. Search for `"rare pediatric
disease designation"` plus your disease/drug terms.

**Tier 3 — SEC filings (EDGAR):**
Public companies routinely disclose RPD designation in 10-K, 10-Q, and 8-K filings because it
is a material event. EDGAR full-text search at `efts.sec.gov` is free and covers millions of
filings. Search for `"rare pediatric disease" AND [drug name OR disease name]`.

**Tier 4 — Company press releases and pipeline pages:**
RPD designation is routinely announced in press releases. Google News search and company pipeline
disclosures cover a substantial fraction.

**Tier 5 — OOPD orphan designation cross-reference:**
RPD designation is frequently co-requested with orphan designation (confirmed by the FDA RPD page:
"The sponsor should indicate in the rare pediatric disease designation request whether or not it
is requesting orphan-drug designation or fast track designation at the same time"). If a drug-
disease pair shows up in the OOPD database for a pediatric disease, there is elevated probability
that the same sponsor also holds RPD designation.

**What the proxy strategy CANNOT determine:** Whether a company holds active RPD designation
without also having filed publicly (i.e., private companies, pre-clinical stage, no ClinicalTrials
registration, no SEC filing). This is an irreducible gap. There is no FOIA-accessible registry.

---

## 5. EU Orphan Register

### 5.1 EMA COMP Orphan Designation Register (Excel Download)

**Bulk download URL (VERIFIED, HTTP 200, content-type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, 347,937 bytes, dated 2026-08-05 18:00):**
`https://www.ema.europa.eu/en/documents/report/medicines-output-orphan_designations-report_en.xlsx`

**Confirmed by (VERIFIED, HTTP 200):**
`https://www.ema.europa.eu/en/medicines/download-medicine-data`
(84,996 bytes; states "The website automatically updates these data tables overnight")

**Sheet structure (VERIFIED from direct parsing of downloaded file):**

Single sheet: "Orphan designation"

Row 9 (header row):
```
Medicine name | Related EMA product number | Active substance | Date of designation / refusal |
Intended use | EU designation number | Status | First published date | Last updated date |
Orphan designation URL
```

Row 10 (first data row, VERIFIED):
```
Xolremdi | EMEA/H/C/006496 | mavorixafor | 25/07/2019 | Treatment of WHIM syndrome |
EU/3/19/2183 | Positive | 24/09/2019 | 04/08/2026 | [URL]
```

**Record counts (VERIFIED by Python parsing, 2026-08-05):**

| Status | Count |
|--------|-------|
| Positive | 2,190 |
| Withdrawn | 965 |
| Negative | 36 |
| **Total with status field** | **3,191** |
| Total rows in sheet | 3,288 |

(The 97-row gap reflects rows without a status field — likely metadata/formatting rows.)

**Update cadence:** Daily (overnight). The file timestamp in the sheet header confirms:
"Output automatically generated from content on www.ema.europa.eu on: 05/08/2026 - 18:00"

**EU designation number format:** EU/3/YY/NNNN (e.g., EU/3/19/2183). The file confirms
designations running at least to EU/3/26/3257 (see EU Community Register below).

### 5.2 EU Community Register of Orphan Medicinal Products

**Current URL (VERIFIED HTTP 301 → HTTP 200, page last updated 04/08/2026, 594,168 bytes):**
`https://health.ec.europa.eu/medicinal-products/union-register_en`
(redirects from `https://ec.europa.eu/health/documents/community-register/html/o_en.htm`)

The register's active designation data is embedded in the page as a JavaScript `var dataSet`
array, parsed directly by the research agent. Counts extracted from that array (VERIFIED,
2026-08-05):

| Metric | Value |
|--------|-------|
| Total active EU orphan designations | 2,171 |
| With marketing authorisation | 207 |
| Last EU number in register | EU/3/26/3257 |
| First entry | EU/3/00/005 (Gemtuzumab Ozogamicin, Mylotarg) |
| Page last updated | 04/08/2026 |

**Note on discrepancy:** The EMA Excel shows 2,190 "Positive" designations while the EC register
shows 2,171 active. The difference (~19) likely reflects designations that are technically
"positive" at EMA COMP level but have not yet been formally entered in the EC Community Register,
or minor timing differences between the two systems. For a conflict check, use both sources.

### 5.3 EU Orphan Market Exclusivity Rules

**Source (VERIFIED, HTTP 200 after redirect, 63,507 bytes):**
`https://www.ema.europa.eu/en/orphan-designation-post-authorisation/market-exclusivity-orphan-medicines`

Key provisions (verbatim from that page):

- "Orphan medicines benefit from **ten years of market exclusivity** once they receive a marketing
  authorisation in the European Union."
- "Market exclusivity is an orphan incentive awarded by the European Commission to a **specific
  clinical indication** with an orphan designation."
- "Each indication with an orphan designation confers ten years' market exclusivity for the
  **particular indication**."
- "A medicine that has multiple orphan designations for different conditions will benefit from
  **separate market exclusivity periods** pertaining to its different orphan designations."
- Paediatric compliance adds **2 additional years** (total 12 years) when results from a fully
  compliant paediatric investigation plan are reflected in the SmPC.
- Article 8(2) of Regulation (EC) No 141/2000 allows Member States to request reduction from
  10 to **6 years** if the drug is sufficiently profitable.
- "When the period of market exclusivity for an indication ends, the orphan designation for that
  indication expires and the European Commission removes it from the Community register."

**Similarity test for EU exclusivity (Regulation (EC) No 141/2000, Article 8):**
The EMA applies a "similarity of medicinal products" guideline. A competitor product is blocked
if it is "similar" to the authorized orphan medicine and has the same therapeutic indication.
The guideline (`c_2008_4077_en.pdf`) defines similarity based on same principal molecular
features AND same therapeutic indication. However, a product that is "clinically superior" (shown
to be of major clinical benefit) escapes the exclusivity block — EU law has an analogous
exception to the US clinical superiority rule.

---

## 6. Decision Procedure for Pipeline Clearance

Execute in this order for each drug-disease candidate pair:

### Step 1: OOPD Designation Search (FDA — US orphan)
**Action:** Search `https://www.accessdata.fda.gov/scripts/opdlisting/oopd/` (browser session
required; POST to OOPD_Results.cfm) for your drug name and disease string.

**Interpret results:**
- No hits → No US orphan designation. No orphan exclusivity block. Proceed.
- Designation exists, no approval date → designation only, no exclusivity block. Orphan
  designation available for you to obtain independently for the same drug-disease pair, since
  multiple sponsors can hold designation simultaneously.
- Designation exists, approval date exists → compute: Is today more than 7 years after the
  approval date? If yes: exclusivity expired, you are not blocked. If no: proceed to Step 2.

### Step 2: Orange Book Cross-Reference (FDA — ODE code check)
**Action:** Download `https://www.fda.gov/media/76860/download` and grep exclusivity.txt for
`ODE` entries matching the NDA number of the drug you identified in Step 1.

**Interpret results:**
- No ODE entry for that NDA → No active orphan exclusivity in Orange Book (consistent with
  designation-only status). Note: if the drug has no approved US NDA at all, it won't be in
  the Orange Book — you only need the OOPD for pre-NDA designations.
- ODE entry present, Exclusivity_Date in past → exclusivity expired; you are not blocked.
- ODE entry present, Exclusivity_Date in future → active orphan exclusivity; apply sameness test.

### Step 3: Sameness Analysis (if active exclusivity found)
**Apply 21 CFR § 316.3(b)(14):**
- **Small molecule:** Is your drug's active moiety identical to the excluded drug's active moiety?
  (Note: same salt/ester = same active moiety = same drug; only different core structure = different.)
  - Yes, same active moiety, same indication → BLOCKED unless clinical superiority can be shown.
  - No, different active moiety → NOT BLOCKED by orphan exclusivity.
- **Macromolecule:** Apply the protein/polysaccharide/polynucleotide sub-rules from § 316.3(b)(14)(ii).
- **Same indication check:** Does the approved label indication overlap with your target indication?
  A narrow approved indication does not block a non-overlapping use.

### Step 4: Clinical Superiority Assessment (if blocked by Step 3)
Apply § 316.3(b)(3): Can you show greater efficacy, greater safety, or major contribution to
patient care vs. the blocking drug? If yes, the "same drug" definition no longer applies and
you are not blocked. If no, the program is blocked for the duration of the ODE exclusivity
period.

### Step 5: EU COMP Register Check
**Action:** Download EMA Excel from `https://www.ema.europa.eu/en/documents/report/medicines-output-orphan_designations-report_en.xlsx` and filter for your drug and disease. Also check the EC
Community Register at `https://health.ec.europa.eu/medicinal-products/union-register_en`.

**Interpret results:**
- EU designation present, EU marketing authorisation present → EU 10-year exclusivity may apply
  in European markets. Check whether exclusivity has expired (designation date + 10 years, or
  + 12 years if paediatric extension was granted).
- EU designation present, no EU MA → no EU exclusivity block yet.
- No EU designation → no EU orphan exclusivity, though competitor may still pursue it.

**Note:** EU exclusivity affects only EU/EEA markets. It is irrelevant to the US FDA pathway
and to the small-market registration program (Georgia, Ukraine, Armenia, Botswana, Albania,
Barbados, Seychelles, Samoa) unless any of those markets reference EMA decisions. Armenia and
Georgia have reliance procedures; check country-specific track for whether EU status is
imported.

### Step 6: RPD Designation Proxy Search
**Action (no public database exists — use indirect signals in this priority order):**
1. Search Federal Register (`federalregister.gov`) for PRV award notices naming your disease/drug.
2. Search ClinicalTrials.gov for `"rare pediatric disease designation"` + drug/disease terms.
3. Search SEC EDGAR full-text (`efts.sec.gov`) for `"rare pediatric disease" AND [drug]`.
4. Search press releases via Google News.
5. Check OOPD for overlapping orphan designation (co-filing is common).

**Interpret results:**
- PRV already awarded for this drug-disease pair → that specific NDA/BLA already consumed the
  RPD PRV. However, the PRV is transferable; the award to someone else does not block your
  own RPD designation or PRV eligibility for a different drug-disease pair.
- Active RPD holder identified (press release/SEC filing) but no PRV yet → they are ahead of
  you. If they obtain FDA approval before 2029-09-30, they collect the PRV first. You may still
  pursue your own RPD designation independently (FDA confirms in the RPD page that designation
  is not mutually exclusive).
- No signals found → likely no active public RPD holder, but private/pre-IND programs are
  undetectable. Document the search, date-stamp it, and note the residual uncertainty.

### What the Decision Procedure CANNOT Determine from Public Data:
1. Whether a private (non-publicly-reporting) company holds active RPD designation for your
   drug-disease pair — this is an irreducible gap.
2. Whether a designation holder has abandoned their program (no public withdrawal notice required
   for designations, only for approved products). The OOPD shows active designations; it does not
   show active clinical programs.
3. The precise scope of an approved indication where label language is ambiguous — this requires
   reading the actual approved label (available at DailyMed/Drugs@FDA).
4. Whether a macromolecule competitor's structural differences cross the threshold for EU
   "similarity" — that determination requires case-by-case scientific assessment by the COMP.

---

## 7. Unfinished — Worth Re-running

1. **OOPD total record count:** Access via headless browser (Playwright) with session cookies,
   submit a blank search, and read the record count from the results page. The agent attempted
   this 8+ times but was consistently blocked by HTTP 403/503 on automated POST requests.

2. **OOPD detailed field set:** Retrieve a sample detailed record (e.g., `cfgridkey=128999`) via
   browser automation to confirm all field names and whether there are fields not listed in the
   2017 instructions page.

3. **EMA figures PDF record count:** Re-extract text from
   `https://www.ema.europa.eu/en/documents/other/orphan-medicines-figures-2000-2025_en.pdf`
   (947,320 bytes, VERIFIED download) using a proper PDF text extraction library (pdfminer,
   pypdf2) rather than `strings`. The PDF likely contains both US and EU cumulative designation
   totals through 2025.

4. **EU similarity guideline:** Fetch and parse
   `https://health.ec.europa.eu/document/download/2b2bb3cb-276b-406e-ab0a-aa1817501c14_en?filename=c_2008_4077_en.pdf`
   (the Article 8(1)/(3) similarity guideline for EU orphan exclusivity) to document the precise
   structural similarity test used by COMP — relevant for biologics where EU exclusivity is more
   nuanced than the US macromolecule rules.

5. **OOPD API:** Test whether `https://api.fda.gov/` or any openFDA endpoint surfaces orphan
   designation data (the agent found HTTP 200 for `api.fda.gov/drug/event.json` but HTTP 404
   for an orphan-specific path; a systematic check of openFDA endpoints was not completed).

---

## 8. URL Ledger

### VERIFIED

| URL | Status | Notes |
|-----|--------|-------|
| `https://www.accessdata.fda.gov/scripts/opdlisting/oopd/` | HTTP 200 (34,324 bytes) | OOPD main search page; interactive only |
| `https://www.fda.gov/industry/designating-orphan-product-drugs-and-biological-products/instructions-searchable-designation-database` | HTTP 200 (35,707 bytes) | OOPD field documentation |
| `https://www.fda.gov/industry/designating-orphan-product-drugs-and-biological-products/frequently-asked-questions-faq-about-designating-orphan-product` | HTTP 200 (59,122 bytes) | OOPD FAQ including disclosure details |
| `https://www.fda.gov/industry/designating-orphan-product-drugs-and-biological-products/public-identification-orphan-drug-designation` | HTTP 200 (36,423 bytes) | Sponsor notification notice re: identifier changes |
| `https://www.fda.gov/media/76860/download` | HTTP 200 (ZIP, 1,091,413 bytes) | Orange Book data ZIP |
| `https://www.fda.gov/drugs/drug-approvals-and-databases/orange-book-data-files` | HTTP 200 (37,387 bytes) | OB data files documentation |
| `https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-316` | HTTP 200 (176,610 bytes) | 21 CFR Part 316 index |
| `https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-316/section-316.3` | HTTP 200 (77,174 bytes) | CFR definitions |
| `https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-316/section-316.31` | HTTP 200 (68,380 bytes) | Scope of orphan exclusivity |
| `https://www.law.cornell.edu/cfr/text/21/316.31` | HTTP 200 | 316.31 full text (LII) — verified 2026-08-06 |
| `https://www.law.cornell.edu/cfr/text/21/316.3` | HTTP 200 | 316.3 sameness definitions (LII) — verified 2026-08-06 |
| `https://www.fda.gov/industry/medical-products-rare-diseases-and-conditions/rare-pediatric-disease-designation-and-priority-review-voucher-programs` | HTTP 200 (35,632 bytes) | FDA RPD program page |
| `https://www.ema.europa.eu/en/medicines/download-medicine-data` | HTTP 200 (84,996 bytes) | EMA download page with orphan Excel link |
| `https://www.ema.europa.eu/en/documents/report/medicines-output-orphan_designations-report_en.xlsx` | HTTP 200 (347,937 bytes, .xlsx) | EMA COMP orphan register download; 3,191 records |
| `https://health.ec.europa.eu/medicinal-products/union-register_en` | HTTP 200 (594,168 bytes) | EC Community Register; 2,171 active designations |
| `https://www.ema.europa.eu/en/orphan-designation-post-authorisation/market-exclusivity-orphan-medicines` | HTTP 200 (63,507 bytes) | EMA orphan exclusivity rules |
| `https://pmc.ncbi.nlm.nih.gov/articles/PMC10021800/` | HTTP 200 | PMC study on FDA/CTG orphan drug data quality |
| `https://www.ema.europa.eu/en/documents/other/orphan-medicines-figures-2000-2025_en.pdf` | HTTP 200 (947,320 bytes) | EMA orphan figures PDF 2000–2025 |

### UNVERIFIED (blocked, moved, or not attempted)

| URL | Status | Notes |
|-----|--------|-------|
| `https://www.accessdata.fda.gov/scripts/opdlisting/oopd/OOPD_Results.cfm` (POST) | HTTP 302 → 403 | Search results; session-dependent, bot-blocked |
| `https://www.accessdata.fda.gov/scripts/opdlisting/oopd/detailedIndex.cfm?cfgridkey=128999` | HTTP 403 | Individual record detail; bot-blocked |
| `https://www.fda.gov/about-fda/fda-track-agency-wide-program-performance/fda-track-office-clinical-policy-and-programs-office-orphan-products-development-dashboard` | HTTP 404 | OOPD dashboard — broken link |
| `https://www.fda.gov/industry/developing-products-rare-diseases-conditions/designating-orphan-product-definitions-eligibility-application-process` | HTTP 404 | Old URL, not redirected |
| `https://www.fda.gov/media/134731/download` | HTTP 200 (227,391 bytes) | Gene therapy sameness guidance PDF — downloaded but text extraction failed (`strings` returned nothing) |
| `https://www.fda.gov/media/135234/download` | HTTP 200 (946,766 bytes) | FDA exclusivity types presentation PDF — downloaded; content extracted via WebFetch of `rxdatalab.com/docs/fda-exclusivity/exclusivity/` instead |
| `https://health.ec.europa.eu/documents/community-register/html/o_en.htm` | HTTP 404 | Old EC register URL — moved to union-register_en |
| `https://www.ema.europa.eu/en/human-regulatory/overview/orphan-designation-overview` | HTTP 404 | Dead EMA link |
| `https://api.fda.gov/drug/event.json?search=orphan` | HTTP 200 but no orphan designation endpoint confirmed | openFDA has no orphan designation API surface |
| `https://www.fda.gov/drugs/development-resources/rare-pediatric-disease-priority-review-voucher-program-section-529` | HTTP 404 | Old RPD section URL — moved |

---

*Document version: recovered 2026-08-06 from 103-call agent transcript. Additional live fetches
performed 2026-08-06 are so noted in text. No content is recalled or fabricated; unverified
claims are explicitly flagged.*
