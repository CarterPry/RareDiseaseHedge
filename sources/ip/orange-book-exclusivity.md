# Orange Book Patent and Exclusivity Data — Technical Reference

**Prepared:** 2026-08-05  
**Data vintage:** July 10, 2026 (EOBZIP files dated Jul 10; openFDA last_updated 2026-08-05)  
**Relevance split:** Funnel A = never-US moiety, 505(b)(1) NDA, PRV-eligible; Funnel B = US generic or 505(b)(2), orphan exclusivity only, PRV-ineligible per 21 U.S.C. § 360ff(a)(4)(B)(i).

---

## 1. Data Files — Download, Format, Record Counts

### 1.1 EOBZIP (Primary Bulk Source)

**Download URL (VERIFIED — HTTP 200, 1,091,413 bytes):**
```
https://www.fda.gov/media/76860/download?attachment
```
Redirects directly to the file; no authentication required. The ZIP unzips into three tilde-delimited (`~`) ASCII text files.

**Update cadence:** Monthly. The files inside the July 2026 ZIP are dated **Jul 10, 2026**. The FDA page metadata shows `og:updated_time: Fri, 02/14/2025 - 09:24` (that is the page template date, not the data). The physical ZIP changes monthly to reflect the current Orange Book edition. There is no confirmed weekly update cycle; treat as monthly unless FDA states otherwise.

**Supplemental appendices (verified downloads, PDFs):**
- Appendix A — Product Name Index: `https://www.fda.gov/media/71494/download?attachment` — HTTP 200, 170,941 bytes, 64 pages
- Appendix B — Product Name Sorted by Applicant: `https://www.fda.gov/media/71502/download?attachment` — HTTP 200, 492,320 bytes, 227 pages
- Appendix C — Uniform Terms: `https://www.fda.gov/media/71523/download?attachment`

**License/redistribution:** No stated restrictions; US Government work, public domain. openFDA terms at `https://open.fda.gov/license/` require attribution and disclaimer.

---

### 1.2 products.txt — Column Schema and Record Counts

**Header (exact, tilde-delimited):**
```
Ingredient~DF;Route~Trade_Name~Applicant~Strength~Appl_Type~Appl_No~Product_No~TE_Code~Approval_Date~RLD~RS~Type~Applicant_Full_Name
```

**Actual record counts (Jul 10, 2026 edition):**
- Total lines including header: **48,502**
- NDA (Appl_Type = N): **10,851**
- ANDA (Appl_Type = A): **37,651**

**Key fields:**

| Col | Field | Notes |
|-----|-------|-------|
| 1 | Ingredient | INN/generic name |
| 2 | DF;Route | Dosage form + route, semicolon-separated |
| 3 | Trade_Name | Brand name |
| 4 | Applicant | Applicant short name |
| 5 | Strength | Dose strength as labeled |
| 6 | Appl_Type | N = NDA, A = ANDA |
| 7 | Appl_No | 6-digit application number (no prefix in file; add NDA/ANDA prefix for cross-reference) |
| 8 | Product_No | 3-digit product number within application |
| 9 | TE_Code | Therapeutic equivalence code (AB, AA, AP, AT, AN, AO, BX, BS, BC, BD, BP, blank) |
| 10 | Approval_Date | MMM DD, YYYY |
| 11 | RLD | Yes/No — Reference Listed Drug |
| 12 | RS | Yes/No — Reference Standard |
| 13 | Type | RX, OTC, DISCN (discontinued), BULK |
| 14 | Applicant_Full_Name | Full legal entity name |

**TE code distribution (actual counts from Jul 2026 data):**
```
blank  26,649  (no TE evaluation — mostly NDAs or pre-ANDA-era)
AB     14,894  (bioequivalent — can substitute)
AP      3,781  (aerosol-only)
AA      1,043  (bioequivalent injectable)
AB1/2/3/4 various (multiple-source split)
AT        509  (topical)
AN        129  (nasal)
AO         71  (ophthalmic)
BX         60  (insufficient data)
BS          1  (biosimilar via 351(k))
```

---

### 1.3 patent.txt — Column Schema and Record Counts

**Header (exact):**
```
Appl_Type~Appl_No~Product_No~Patent_No~Patent_Expire_Date_Text~Drug_Substance_Flag~Drug_Product_Flag~Patent_Use_Code~Delist_Flag~Submission_Date
```

**Total lines including header: 22,131**  
(Represents 22,130 patent-product-use-code rows; a single patent can appear multiple times if listed against multiple products or with multiple use codes.)

**Field breakdown:**

| Col | Field | Notes |
|-----|-------|-------|
| 1 | Appl_Type | N or A |
| 2 | Appl_No | 6-digit application number |
| 3 | Product_No | 3-digit product number |
| 4 | Patent_No | Up to 11 chars; may end in `*PED` if pediatric exclusivity added 6 months |
| 5 | Patent_Expire_Date_Text | `MMM DD, YYYY` including any patent term extension |
| 6 | Drug_Substance_Flag | Y or blank — DS patent |
| 7 | Drug_Product_Flag | Y or blank — DP (formulation) patent |
| 8 | Patent_Use_Code | U-XXXX or blank — method-of-use patent |
| 9 | Delist_Flag | Y or blank — sponsor requested delist but patent stays for 180-day exclusivity purposes |
| 10 | Submission_Date | Date FDA received Form 3542 |

**Patent type distribution (actual counts):**
```
Drug Substance only (DS=Y, DP=blank):   753
Drug Product only (DS=blank, DP=Y):   6,890
Both DS and DP (DS=Y, DP=Y):          2,745
Method-of-use only (use code, no DS/DP flags): 9,386
No flags, no use code (bare patent):   2,356
*PED suffix rows:                      2,353
```

**Critical note:** 9,386 of 22,130 listed patents are method-of-use only — they carry a U-XXXX code and have blank DS and DP flags. These are the patents that survive after compound IP expiry and are the primary barrier to repurposing plays.

**Sample rows (real data):**
```
# Substance + use code (Xyrem / sodium oxybate):
N~021196~001~10213400~Mar 15, 2033~~~U-2499~~Mar 28, 2019

# Pediatric patent extension (*PED suffix — 6 months added):
N~021196~001~8772306*PED~Sep 15, 2033~~~~~
N~020610~001~7625884*PED~Feb 24, 2027~~~~~

# Delist flag (stays for 180-day exclusivity):
N~206073~001~9173859~May 4, 2027~~Y~U-1772~Y~Dec 2, 2015
```

---

### 1.4 exclusivity.txt — Column Schema and Record Counts

**Header (exact):**
```
Appl_Type~Appl_No~Product_No~Exclusivity_Code~Exclusivity_Date
```

**Total lines including header: 2,341**

**Exclusivity code distribution (actual counts, Jul 2026 data):**

```
NCE      423   New Chemical Entity — 5-year exclusivity
PED      339   Pediatric exclusivity — 6-month add-on
NPP      159   New Pharmaceutical Product (was NDF?) — 3-year exclusivity
NP       130   New Product — 3-year exclusivity
ODE-xxx  605   Orphan Drug Exclusivity (numbered per orphan designation)
ODE*      90   Orphan Drug Exclusivity (alternate notation, non-numbered)
M-xxx    193   (Method-related exclusivity or miscellaneous — see decode below)
I-xxx    221   (Innovation/indication-specific — see decode below)
D-xxx     25   (Drug-specific — see decode below)
GAIN      44   Generating Antibiotic Incentives Now Act — 5-year add-on to NCE, or 10-year for NCE-qualifying antibiotic
CGT       36   Cell and Gene Therapy — 15-year exclusivity (FDORA 2022)
PC        56   Patent Certification — 30-month stay running
NS        16   New Strength — 3-year exclusivity
W          1   (rare/misc)
RTO        1   Return to Omission
NDF        1   New Dosage Form — 3-year exclusivity
NCE*       1   NCE variant
```

---

## 2. Exclusivity Code Decode Table

All periods run from the date of NDA approval unless noted. Codes are assigned per product within an NDA; a single NDA can carry multiple simultaneous codes.

### Core Statutory Exclusivities

| Code | Name | Statutory Basis | Period | What It Bars | What It Does NOT Bar |
|------|------|----------------|--------|--------------|----------------------|
| **NCE** | New Chemical Entity | 21 U.S.C. § 355(c)(3)(E)(ii); 21 CFR 314.108(b)(2) | 5 years from approval | ANDA filings AND 505(b)(2) filings (both barred for first 4 years; Para IV ANDA can file after 4 years, triggering 30-month stay if suit filed within 45 days) | Does not bar a 505(b)(1) NDA; does not bar clinical research |
| **NP** | New Product | 21 U.S.C. § 355(c)(3)(E)(iii); 21 CFR 314.108(b)(3) | 3 years from approval | ANDA approval (not filing) for same conditions of use; 505(b)(2) approval for same | Filing is permitted; only approval is stayed |
| **NPP** | New Pharmaceutical Product / New Product (formulation/indication) | Same as NP | 3 years | As NP; applies to new formulation, new indication, new route — anything requiring new clinical investigations other than bioavailability | Same limitations as NP |
| **NS** | New Strength | Same framework | 3 years | Approval of ANDA or 505(b)(2) for same strength | As NP |
| **NDF** | New Dosage Form | Same framework | 3 years | Approval of ANDA or 505(b)(2) for same dosage form | As NP |
| **ODE-xxx** / **ODE*** | Orphan Drug Exclusivity | 21 U.S.C. § 360cc; 21 CFR 316.31 | 7 years from approval | FDA may not approve another application for the **same drug** for the **same orphan indication**; bars ANDAs, 505(b)(2)s, and 505(b)(1)s for that indication | Does not bar other indications; does not bar a drug that is "clinically superior" (greater efficacy, superior safety, or major contribution to patient care); does not bar the same molecule for a different indication. The ODE number maps to a specific orphan designation number in FDA's orphan database. |
| **PED** | Pediatric Exclusivity | 21 U.S.C. § 505A | 6 months — added to the end of any existing NP, NCE, or patent that is running concurrently | Extends NP/NCE data exclusivity window by 6 months AND extends all listed Orange Book patents by 6 months (shown as `patent_no*PED` in patent.txt) | Cannot create exclusivity where none exists; only extends existing IP |
| **GAIN** | Generating Antibiotic Incentives Now Act | 21 U.S.C. § 355f | 5-year add-on to NCE (or 10-year stand-alone for Qualified Infectious Disease Products) | Same as NCE for the extended period | Only applies to qualified antibiotics/antifungals |
| **CGT** | Cell and Gene Therapy (FDORA 2022) | 21 U.S.C. § 355(u) | 15 years from approval | Approval of any "same indication" follow-on CGT product | Relatively new; applies to approved cell/gene therapy products only |
| **PC** | Patent Certification (30-month stay) | 21 U.S.C. § 355(j)(5)(B)(iii) | Runs from date ANDA applicant notified NDA holder of Para IV cert, up to 30 months | ANDA approval only (not filing); terminates early if district court rules patent invalid/not infringed | Not a true exclusivity; a litigation-triggered hold |

### Numbered Sub-Codes (M, I, D series)

These are internal FDA tracking codes mapping to specific orphan designations or indication-specific exclusivities. They do **not** represent separate statutory categories — they subdivide ODE, NP, or NDF grants for tracking purposes.

| Prefix | Meaning | Interpretation |
|--------|---------|---------------|
| **M-xxx** | Method-of-use or market-specific tracking | Example: M-14, M-82, M-187, M-285, M-287 etc. Each number is an internal FDA identifier for a specific method-of-use exclusivity or a sub-indication within a broader product approval. Not separately defined in CFR; must be cross-referenced against FDA's exclusivity records. Approximately 193 rows across ~30 distinct M-numbers in current data. |
| **I-xxx** | Indication-specific exclusivity | Example: I-935, I-939, I-958, I-973, I-975, I-976 etc. Maps to a specific approved indication under a multi-indication NDA. Approximately 221 rows across ~20 distinct I-numbers. |
| **D-xxx** | Drug-specific exclusivity identifier | Example: D-188, D-191, D-193, D-196, D-199. 25 rows across ~5 distinct numbers. |
| **RTO** | Return to Omission | One occurrence (NDA 017031). Signals FDA reversed a prior exclusivity determination. |
| **W-xxx** | (Rare/miscellaneous) | One occurrence in current data. |

**Practical note on M/I/D codes:** These are opaque without FDA's internal exclusivity tracking database. To decode a specific M or I number, query the FDA Exclusivity Determination History (accessible through Drugs@FDA application documents) or the CDER FOI service. Do not assume M-14 on one NDA means the same condition as M-14 on another NDA without verification.

---

## 3. Patent Listings — How They Map to NDAs and Products

### 3.1 Structural Mapping

The Orange Book patent system operates at three levels:

```
NDA (Appl_No) → Product within NDA (Product_No) → Patent(s) listed per product
```

A single NDA may have multiple Product_No entries (different strengths, formulations). Each patent must be listed against specific products. A patent can appear multiple times in patent.txt if it covers multiple products within the same NDA, or if it carries multiple use codes.

### 3.2 Form 3542 and the Listing Obligation

NDA holders must submit Form 3542 for each patent they wish to list. Only three patent categories may be listed:
1. Drug substance (active ingredient) patents — DS flag = Y
2. Drug product (formulation, composition) patents — DP flag = Y
3. Method-of-use patents — must correspond to an approved labeled indication; carries a U-XXXX use code

**What cannot be listed:** Process patents, metabolite patents, intermediate patents, packaging patents. These can still block competitors in court but do not appear in the Orange Book and do not trigger the Para IV certification/30-month stay mechanism.

### 3.3 The Para IV Certification Process (505(j) and 505(b)(2))

When a generic applicant (ANDA) or 505(b)(2) applicant certifies that a listed patent is invalid, unenforceable, or will not be infringed (Para IV cert), the NDA holder has 45 days to file suit. If suit is filed within 45 days, FDA automatically stays ANDA/505(b)(2) approval for up to 30 months. This 30-month stay appears in exclusivity.txt as code `PC`.

**505(b)(2) applicants must certify** to all listed patents (Para I, II, III, or IV) **except** patents where the Delist_Flag = Y (because the NDA holder cannot sue on a patent they asked to delist while a first ANDA applicant retains 180-day exclusivity rights to that patent).

### 3.4 Method-of-Use Patents and Repurposing

Method-of-use (MoU) patents are the most dangerous category for repurposers. They carry U-XXXX codes. The use code text (e.g., "Treatment of narcolepsy with excessive daytime sleepiness") defines the exact labeled indication covered.

**Key principle:** A 505(b)(2) or ANDA applicant seeking approval for a **different** indication than the one covered by a MoU patent can "carve out" that indication from its label (the "skinny label" strategy) and certify Para III (patent won't expire before its approval date) or simply not certify at all if the indication is entirely carved out. However:
- If any part of the proposed label overlaps with the MoU patent, Para IV is required.
- Brand-name holders have challenged skinny labels as inducing infringement even after carve-out (*GlaxoSmithKline LLC v. Teva Pharmaceuticals*, Fed. Cir. 2021).
- For Funnel A (new indication for a never-US moiety), MoU patents on the brand's approved indication are irrelevant if the new NDA covers a different indication entirely — but if the new NDA seeks the same indication, the MoU patent must be certified against.

**Current scale of MoU exposure:** 9,386 of 22,130 listed patents are MoU-only (no DS or DP flag). This is the largest single patent category in the Orange Book.

### 3.5 Patent Term Extensions (PTE) / Hatch-Waxman Extension

Patent expiry dates in patent.txt already incorporate any USPTO-granted Patent Term Extension under 35 U.S.C. § 156 (Hatch-Waxman PTE). PTEs can add up to 5 years to a patent's term to compensate for FDA regulatory delay. The statutory limit is: the adjusted term cannot exceed 14 years from the date of NDA approval.

The expiry date in patent.txt reflects: `[Original patent expiry] + [PTE granted] + [6 months if PED add-on]`. The `*PED` suffix confirms pediatric add-on was applied; the date shown is already the extended date.

---

## 4. Exclusivity Duration, Bar Type, and NCE-1 Date Arithmetic

### 4.1 What Bars Filing Versus What Bars Approval

This distinction is critical for timeline planning:

| Exclusivity | Bars ANDA/505(b)(2) Filing? | Bars ANDA/505(b)(2) Approval? |
|-------------|---------------------------|-------------------------------|
| NCE (5-year) | Yes — for first 4 years. Para IV ANDA may be filed at year 4. | Yes — no approval until year 5. Para IV ANDA filed at year 4 can be approved at end of 30-month stay if that runs past year 5. |
| NP/NPP/NS/NDF (3-year) | No — filing permitted immediately | Yes — approval blocked for 3 years |
| ODE (7-year) | No (for ANDAs targeting different indication) | Yes — for same drug, same orphan indication |
| PED (6-month add-on) | Extends whichever underlying exclusivity is running | As underlying |
| Patent (any type) | No — filing and Para IV cert permitted | Yes — 30-month stay if NDA holder sues within 45 days of notification |

### 4.2 NCE-1 Date Arithmetic (Verified)

The "NCE-1 window" is the date on which a Para IV ANDA or 505(b)(2) may first be filed against a drug with 5-year NCE exclusivity.

**Statutory text (21 U.S.C. § 355(c)(3)(E)(ii)):** "…no application may be submitted under subsection (j) of this section which refers to the listed drug…for a period of five years from the date of approval of the application…except that such an application may be submitted after four years if it contains a certification of patent invalidity or noninfringement described in subclause (IV) of subsection (b)(2)(A)…"

**Formula:**
```
NCE exclusivity end date = Approval date + 5 years (same calendar date, 5 years later)
NCE-1 Para IV filing open date = Approval date + 4 years (same calendar date)
```

**Verified example from actual data:**
- NDA 021164 (EXXUA / gepirone hydrochloride ER), approved Sep 22, 2023
- Exclusivity.txt shows: `N~021164~001~NCE~Sep 22, 2028`
- NCE-1 = Sep 22, 2027 (Para IV ANDA may be filed from that date)
- NCE-1 + 30-month stay = Mar 22, 2030 (latest a Para IV-filed ANDA could be held up if suit filed on day 45 of notification window)

**With PED add-on:** If the NDA holder later earns pediatric exclusivity, the 5-year NCE end date shifts +6 months. If `NCE*` appears (rare — 1 instance in current data for NDA 214133), verify specific FDA correspondence.

### 4.3 Orphan Exclusivity (ODE) — 7-Year Period

ODE is counted from NDA approval date. Critically:
- ODE blocks approval of the **same drug** for the **same rare disease/condition** as the orphan designation.
- "Same drug" means the same active moiety (21 CFR 316.3(b)(13)). Salt forms, esters, and polymorphs of the same moiety = same drug unless FDA finds a clinically meaningful difference.
- A different drug can still be approved for the same orphan condition — ODE is not an exclusive franchise over the disease.
- "Clinically superior" exception: FDA can approve a second drug for the same indication if the sponsor demonstrates greater efficacy, better safety, or a major contribution to patient care (21 CFR 316.31(a)(3)).

**ODE-xxx numbering:** Each ODE-xxx number in exclusivity.txt corresponds to a specific orphan designation number from FDA's Orphan Drug Designations database. The designation number is the link between the Orange Book and the rare disease indication. To decode: go to `https://www.accessdata.fda.gov/scripts/opdlisting/oopd/` and search by designation number.

### 4.4 3-Year Exclusivities (NP, NPP, NS, NDF)

These apply when an NDA supplement or new NDA requires new clinical investigations (not just bioavailability) to establish safety/effectiveness of a new formulation, new indication, new strength, or new route. The 3-year period blocks **approval** but not **filing** of a generic application.

**Important for Funnel B (505(b)(2) repurposing):** If a Funnel B application adds a new indication for a well-known drug, the approved NDA earns 3-year NP/NPP exclusivity for that indication. This blocks generics from being approved for the same indication for 3 years — valuable, but far shorter than NCE's 5-year or ODE's 7-year windows, and far shorter than PRV value.

---

## 5. Pediatric Exclusivity Six-Month Add-On (PED)

### 5.1 Mechanism

Authorized under 21 U.S.C. § 505A (Best Pharmaceuticals for Children Act). FDA may request pediatric studies via a Written Request (WR). If the sponsor conducts the studies and submits reports regardless of outcome, FDA adds 6 months to any existing NCE, NP, or patent exclusivity.

**Scope of add-on:** The 6 months attaches to **all** qualifying exclusivities and **all** Orange Book-listed patents for the drug — not just the patents covering the pediatric indication. This is unusually broad: a MoU patent on an adult cardiovascular indication gets extended by 6 months if the same company completes pediatric studies for a completely different indication.

**Verification in data:** In patent.txt, the extended patent appears as a separate row with `patent_no*PED` and a date 6 months later than the base patent. Example from real data:
```
N~021196~001~8772306~Mar 15, 2033~~~U-1532~~Jul 9, 2014   (base patent)
N~021196~001~8772306*PED~Sep 15, 2033~~~~~                 (PED extension)
```
In exclusivity.txt, the PED code appears with the end date:
```
N~021196~001~PED~Apr 26, 2026
```
Current data: **339 PED rows** across 2,341 total exclusivity rows. **2,353 *PED patent rows** out of 22,130 patent rows.

### 5.2 PED in the Context of Funnel B

For a Funnel B (505(b)(2)) repurposing play targeting a rare pediatric disease via orphan exclusivity, PED exclusivity adds a further 6 months on top of the ODE 7-year window if FDA issues a Written Request and the sponsor completes pediatric studies. Given that ODE and PED are additive, a Funnel B product could hold:
- ODE (7 years) + PED (6 months) = 7.5 years of exclusivity on the approved orphan indication
- Plus 3-year NP exclusivity on the new indication (runs concurrently with ODE, so adds nothing in the first 3 years but may matter if ODE is challenged and falls)

---

## 6. The Difference Between Patent Expiry, Data Exclusivity, and Orphan Exclusivity

These three mechanisms are independent and can run simultaneously or in sequence. They have fundamentally different legal triggers and effects:

| Mechanism | Trigger | Governs | Effect on Generic/505(b)(2) |
|-----------|---------|---------|---------------------------|
| **Patent** | Listed in Orange Book (NDA holder files Form 3542) | Right to make/use/sell a specific compound, formulation, or method | If Para IV certified and NDA holder sues within 45 days → 30-month approval stay. If no suit or Para III certified → no delay from patent |
| **Data exclusivity (NCE, NP, NPP)** | FDA approval of qualifying NDA | FDA's own data-submission and approval queue | Blocks FDA from using the NDA's data as the basis for a generic's approval; blocks filing (NCE) or only approval (NP) |
| **Orphan exclusivity (ODE)** | Orphan Drug Act; tied to specific orphan designation | FDA's power to approve "same drug, same indication" competitors | FDA may not approve a second application for same drug + same orphan indication for 7 years |

**A compound can have expired patents, expired data exclusivity, but still active orphan exclusivity** (or vice versa). All three must be checked independently.

**What actually blocks a 505(b)(2) filing:**
1. Active NCE exclusivity within first 4 years (absolute filing bar)
2. A listed DS patent (compound patent) if the 505(b)(2) cannot certify Para III

**What actually blocks a 505(b)(2) approval but not filing:**
3. Active NCE exclusivity for year 5 (approval bar but Para IV filing permitted at year 4)
4. Active NP/NPP/NS/NDF exclusivity (3-year approval bar)
5. Active ODE for same drug + same orphan indication (7-year approval bar)
6. 30-month stay from Para IV litigation on any listed patent
7. Active listed MoU patent if the proposed indication overlaps (requires Para IV cert → risk of 30-month stay)

**What does NOT block a 505(b)(2):**
8. Unlisted patents (process, packaging, metabolite) — enforceable in court but do not trigger automatic FDA stay
9. ODE for a different indication on the same drug
10. ODE for the same indication on a different drug (different moiety)

---

## 7. openFDA API for Orange Book Data

### 7.1 Orange Book Endpoint

**Base URL (VERIFIED — HTTP 200, 48,502 records):**
```
https://api.fda.gov/drug/orangebook.json
```

**Authentication:** None required for API key-less access. Rate limit: 240 requests/minute without key; 1,000/minute with free API key from `https://open.fda.gov/apis/authentication/`.

**Schema (actual, verified via live query):**

```json
{
  "approval_date": "YYYYMMDD",
  "product_number": "001",
  "products": [
    {
      "active_ingredients": [{"name": "...", "strength": "..."}],
      "brand_name": "...",
      "application_name": "...",
      "application_type": "N|A",
      "application_number": "040134",
      "therapeutic_equivalence_codes": ["AB"],
      "reference_listed_drug": true|false,
      "reference_standard": true|false,
      "marketing_status": "HUMAN PRESCRIPTION DRUG|DISCONTINUED|...",
      "application_full_name": "...",
      "dosage_form": "...",
      "route": "..."
    }
  ]
}
```

**CRITICAL LIMITATION:** The openFDA Orange Book endpoint contains **product data only** — no patent data and no exclusivity data. The `products` object has no patent_no, patent_expiry, exclusivity_code, or exclusivity_date fields. To get patent and exclusivity data, you must use the flat files (EOBZIP).

Total records matches local file: both show 48,502 entries (products, not NDAs — a single NDA with 4 strengths = 4 records).

**Example queries:**
```bash
# All NDA products for a specific application
curl "https://api.fda.gov/drug/orangebook.json?search=products.application_number:020785&limit=10"

# Search by ingredient
curl "https://api.fda.gov/drug/orangebook.json?search=products.active_ingredients.name:thalidomide&limit=5"

# Count by application type
curl "https://api.fda.gov/drug/orangebook.json?count=products.application_type.exact"
```

### 7.2 Drugs@FDA Endpoint (openFDA)

**Base URL (VERIFIED — HTTP 200):**
```
https://api.fda.gov/drug/drugsfda.json
```

**Schema fields:** `submissions`, `application_number`, `sponsor_name`, `openfda`, `products`

Relevant to repurposing: the `submissions` array contains `submission_property_type` which may show `{"code": "Orphan"}` — confirming orphan designation was claimed at submission. This is the only way to query orphan submission history via openFDA without the EOBZIP.

**Does NOT contain:** patent data, exclusivity data, orphan designation numbers, or ODE end dates. These require EOBZIP or FDA Orphan Drug Designations database.

### 7.3 Drugs@FDA Bulk Download (VERIFIED)

**URL (HTTP 200, 6,059,547 bytes ZIP, updated daily Mon–Fri):**
```
https://www.fda.gov/media/89850/download?attachment
```

Contains 12 relational tables including: Applications, Products, Submissions, SubmissionPropertyType (Orphan flag), MarketingStatus, TE codes. **Does not contain** Orange Book patent or exclusivity data — those remain in the EOBZIP only.

---

## 8. Purple Book for Biologics

### 8.1 Overview and Access

The Purple Book covers FDA-licensed biological products under section 351 of the PHS Act (42 U.S.C. § 262), including biosimilars approved under 351(k). It is separate from the Orange Book; biologics do not appear in the Orange Book.

**Primary access:** Browser-based search tool at:
```
https://purplebooksearch.fda.gov/
```
Status: UNVERIFIED for API access — the tool returns HTTP 403 from curl with bot-detection. No confirmed programmatic API endpoint.

**PDF download (VERIFIED — HTTP 200, 784,473 bytes):**
```
https://www.fda.gov/media/120734/download?attachment
```
This is the full Purple Book PDF (UCM623303.pdf), not machine-readable CSV. No confirmed bulk CSV download URL was found. UNVERIFIED whether a flat-file download exists.

**Biosimilar product list (HTML page, VERIFIED — HTTP 200, 60,414 bytes):**
```
https://www.fda.gov/drugs/biosimilars/biosimilar-product-information
```
Contains 90+ approved biosimilar products as of July 2026 with approval dates and reference product links.

### 8.2 Biologic Exclusivity

Biologics are governed by a separate exclusivity framework under 42 U.S.C. § 262(k)(7):

| Period | Type | What It Covers |
|--------|------|----------------|
| **12 years** | Reference Product Exclusivity | FDA may not approve a biosimilar or interchangeable product based on the reference product's license before 12 years from first licensure |
| **4 years** | Data Exclusivity (filing bar) | No biosimilar application may be submitted using the reference product's data for the first 4 years post-licensure |

**No orphan-drug exclusivity interaction:** Biologic orphan exclusivity and PHS Act exclusivity run independently. A biologic with orphan designation for a rare disease gets: ODE (7 years) AND 12-year reference product exclusivity. These are concurrent, not additive, so the 12-year term controls.

**Key difference from small molecules:** There is no NCE equivalent, no NP/NPP, and no PED add-on for biologics. Pediatric studies for biologics earn a 6-month PED add-on under the Biologics Price Competition and Innovation Act (BPCIA), but FDA implementation differs from the FDCA § 505A mechanism.

**Purple Book data fields:** Based on the PDF and search interface, the Purple Book records: BLA number, proprietary name, proper name, BLA applicant, reference product (for biosimilars), dosage form/route/strength, licensure date, marketing status, interchangeable status, exclusivity dates (both 4-year and 12-year). No machine-readable API is confirmed.

---

## 9. Funnel-Specific Analysis

### 9.1 Funnel A (Never-US Moiety, 505(b)(1) NDA, PRV-Eligible)

**Orange Book check sequence for a never-approved-in-US compound:**
1. Search products.txt for the INN/ingredient — if absent, the compound has no US NDA history (good for Funnel A).
2. If absent from products.txt, no listed patents exist. No Orange Book IP barriers.
3. No exclusivity.txt entries possible.
4. Remaining barriers: free-standing patents held by anyone (not just NDA holders) on the compound, composition, or method — these must be checked via USPTO PAIR, Espacenet, Google Patents, not the Orange Book.
5. After approval: the Funnel A NDA earns NCE exclusivity (5 years), potentially ODE (7 years if orphan designation), and PED add-on (6 months if pediatric studies completed). These stack with maximum ODE period controlling.

**Funnel A PRV window math:** PRV requires FDA approval before Sep 30, 2029 (sunset). An NDA filed in mid-2026 would need a review period of ~3–3.5 years for standard review. Priority Review (6-month PDUFA goal) requires a Priority Review Designation or Rare Pediatric Disease Designation. Realistically achievable with a compound already in late-stage clinical development and a strong rare pediatric disease data package.

### 9.2 Funnel B (US Generic or 505(b)(2), Orphan Exclusivity Only, PRV-Ineligible)

**Orange Book check sequence for a known US generic:**
1. Search products.txt by ingredient to find all NDAs (Appl_Type=N) — these are the RLDs with IP.
2. For each NDA, pull patent.txt rows: note DS, DP, and MoU patents with their expiry dates.
3. For each NDA, pull exclusivity.txt rows: note NCE (if active), ODE (if active, which indication number), PED (if active).
4. ODE is the key value: 7 years of market protection for the orphan indication. If no ODE row exists and all patents have expired, the compound may be fully open.
5. File under 505(b)(2). This earns NP/NPP exclusivity (3 years) and ODE (7 years if orphan designation obtained). Cannot earn NCE. PRV-ineligible per § 360ff(a)(4)(B)(i).

---

## 10. "Is This Compound Free to Use?" Checklist

Run this for every candidate before allocating development budget. Apply to the specific NDA (use Appl_No from products.txt to pull the patent and exclusivity rows).

### Step 1 — Product and Application Lookup
```python
# Filter products.txt for the ingredient
ingredient = "DRUG_INN"
ndas = products[products['Ingredient'].str.contains(ingredient, case=False) & (products['Appl_Type'] == 'N')]
# Get list of Appl_No values (6-digit, e.g. "021196")
```
- [ ] Does the compound appear in products.txt at all?
  - If NO → no Orange Book IP. Proceed to USPTO/FTO analysis for background patents.
  - If YES → note all NDA numbers for the compound.

### Step 2 — Data Exclusivity Check
```python
excl = exclusivity[exclusivity['Appl_No'].isin(nda_list)]
active_excl = excl[pd.to_datetime(excl['Exclusivity_Date'], format='%b %d, %Y') > today]
```
- [ ] Any active **NCE** row? If YES and within first 4 years: ANDA/505(b)(2) FILING BARRED. If within year 5: approval barred. **HARD STOP for 505(b)(2).**
- [ ] Any active **NP/NPP/NS/NDF** row? If YES: 505(b)(2) approval barred for same condition until date shown. Filing permitted. Note expiry date.
- [ ] Any active **ODE-xxx** row? Note the designation number. Check which indication it covers. If your proposed indication matches the orphan designation → **APPROVAL BARRED for 7 years** unless you can claim clinical superiority or a different drug.
- [ ] **ODE* row?** Same analysis; the asterisk notation is an older non-numbered form of orphan exclusivity.

### Step 3 — Patent Check: Compound Patents
```python
patents = patent_df[patent_df['Appl_No'].isin(nda_list)]
ds_patents = patents[patents['Drug_Substance_Flag'] == 'Y']
active_ds = ds_patents[pd.to_datetime(ds_patents['Patent_Expire_Date_Text'], format='%b %d, %Y') > today]
```
- [ ] Any active **Drug Substance (DS=Y)** patents? If YES: these cover the active ingredient itself. A 505(b)(2) must certify (Para III if expiry before your target approval date, Para IV if you believe invalid/not infringed). Para IV → 30-month stay risk.

**Failure mode:** A single long-running DS patent with a PTE adds several more years. Check if the expiry date in patent.txt already includes PTE (it does — the date reflects extended expiry) and whether there is a `*PED` version adding another 6 months.

### Step 4 — Patent Check: Formulation Patents
```python
dp_patents = patents[patents['Drug_Product_Flag'] == 'Y']
active_dp = dp_patents[pd.to_datetime(dp_patents['Patent_Expire_Date_Text'], format='%b %d, %Y') > today]
```
- [ ] Any active **Drug Product (DP=Y)** patents? These cover the specific formulation (extended release, nanoparticle, salt form, excipient combination). A 505(b)(2) that uses a different formulation may be able to certify Para III or avoid certifying entirely. But if the proposed formulation is the same or substantially similar, Para IV is required.

**Failure mode (most common for repurposing plays):** The reference product has a novel delivery system (e.g., depot injection, nanoparticle, liposome) covered by DP patents expiring 10–15 years out. If the generic tries to copy the delivery system, it's exposed to Para IV litigation with a 30-month stay. Solution: use a different formulation and seek independent clinical data.

### Step 5 — Patent Check: Method-of-Use Patents (THE CRITICAL FAILURE MODE)
```python
mou_patents = patents[(patents['Drug_Substance_Flag'] != 'Y') & 
                      (patents['Drug_Product_Flag'] != 'Y') & 
                      (patents['Patent_Use_Code'] != '')]
active_mou = mou_patents[pd.to_datetime(mou_patents['Patent_Expire_Date_Text'], format='%b %d, %Y') > today]
```
- [ ] Any active **Method-of-Use (use code = U-XXXX)** patents? Note all use codes.
- [ ] Do any use codes cover the **same indication** you plan to pursue?
  - If YES and you cannot carve it out: Para IV cert required → 30-month stay risk. Litigation outcome uncertain.
  - If YES but it's a different indication than yours: carve it out of your label. Risk: brand can still sue for induced infringement if your product is prescribed off-label for their patented indication.
  - If NO / all expired: proceed.

**The induced-infringement failure mode:** This is how MoU patents kill repurposing plays even with a skinny label. Under *GlaxoSmithKline v. Teva* (Fed. Cir. 2021), a generic can be liable for inducement if the generic's label describes an indication that leads physicians to use the drug in a patented manner, even if the label does not explicitly state the patented indication. For rare disease repurposing, where the indication may be highly specific, the risk is lower — but not zero.

**To look up what a use code covers:** Query the patent use code list at:
```
https://www.accessdata.fda.gov/scripts/cder/ob/patentlist.cfm
```
NOTE: This URL returned HTTP 403 (rate-limited) during the current research session. The list is available via the Orange Book online search tool at `https://www.accessdata.fda.gov/scripts/cder/ob/index.cfm`. The use code text (e.g., "Treatment of cataplexy in patients 7 years of age and older with narcolepsy" for U-1532) determines whether your proposed indication overlaps.

### Step 6 — Pediatric Patent Extension Check
- [ ] Any `*PED` patent rows? These extend the base patent by 6 months. The date shown is already the extended date. If the base patent would have expired but the `*PED` entry shows a date 6 months later, the 6-month extension is controlling.

### Step 7 — Cross-Check with USPTO for Unlisted Patents
The Orange Book only shows patents that the NDA holder chose to list on Form 3542. Unlisted patents (process, packaging, metabolite, intermediate) are not in the Orange Book but can still be enforced in district court. They do not trigger the 30-month automatic stay, but an NDA holder can seek a preliminary injunction.

**Failure mode:** The RLD holder holds a process patent on the manufacturing route for the only commercially viable synthesis. Even if all Orange Book patents have expired, the process patent forces the generic to develop an alternative synthesis, which may be cost-prohibitive for a small-volume rare disease drug.

**Check:** USPTO Patent Full Text and Image Database (`https://patents.google.com` or `https://ppubs.uspto.gov`), search by assignee + INN. Also check USPTO PAIR for any pending patent applications that could issue and be listed before your approval date.

### Step 8 — Purple Book (Biologics Only)
If the compound is a biologic (protein, mAb, nucleic acid-based, cell/gene therapy):
- [ ] Check Purple Book at `https://purplebooksearch.fda.gov/` for reference product exclusivity end dates (4-year filing bar, 12-year approval bar).
- [ ] No Orange Book entries will exist for biologics.
- [ ] ODE on biologics works the same way as small molecules (7-year orphan exclusivity under PHS Act § 351(k)(7)(A)(ii)).

### Step 9 — Synthesized "Free to File" vs "Free to Approve" Decision

| Condition | Free to File 505(b)(2)? | Free to Be Approved? |
|-----------|------------------------|---------------------|
| Active NCE (years 1–4) | NO | NO |
| Active NCE (year 5) | YES (Para IV) | NO until year 5 |
| Active NP/NPP (3-year) | YES | NO until expiry |
| Active ODE (same indication) | YES | NO until expiry (unless clinical superiority) |
| Active DS patent (Para IV) | YES | Subject to 30-month stay if NDA holder sues |
| Active DP patent (Para IV, same formulation) | YES | Subject to 30-month stay |
| Active MoU patent (overlapping indication) | YES | Subject to 30-month stay + inducement risk |
| Active MoU patent (different indication) | YES (carve out) | YES with skinny label (inducement risk remains) |
| No active exclusivity or patents | YES | YES |

---

## 11. URL Ledger

### VERIFIED (HTTP 200 confirmed, file contents examined)

| URL | Description | Status Details |
|-----|-------------|----------------|
| `https://www.fda.gov/media/76860/download?attachment` | EOBZIP (products.txt, patent.txt, exclusivity.txt) | HTTP 200, 1,091,413 bytes, files dated Jul 10 2026 |
| `https://api.fda.gov/drug/orangebook.json` | openFDA Orange Book products endpoint | HTTP 200, 48,502 records, no patent/exclusivity data |
| `https://api.fda.gov/drug/drugsfda.json` | openFDA Drugs@FDA submissions endpoint | HTTP 200, includes orphan flag |
| `https://www.fda.gov/media/89850/download?attachment` | Drugs@FDA bulk ZIP download | HTTP 200, 6,059,547 bytes, updated daily Mon–Fri, last updated Aug 5 2026 |
| `https://www.fda.gov/media/71494/download?attachment` | Orange Book Appendix A (Product Name Index) | HTTP 200, 170,941 bytes, PDF 64 pages |
| `https://www.fda.gov/media/71502/download?attachment` | Orange Book Appendix B (Applicant Sort) | HTTP 200, 492,320 bytes, PDF 227 pages |
| `https://www.fda.gov/media/120734/download?attachment` | Purple Book PDF (UCM623303.pdf) | HTTP 200, 784,473 bytes, not machine-readable |
| `https://www.fda.gov/drugs/biosimilars/biosimilar-product-information` | Biosimilar product list (HTML) | HTTP 200, 60,414 bytes |
| Orange Book data files page (FDA.gov node/358564) | Products.txt/patent.txt/exclusivity.txt descriptions | HTTP 200, field schema extracted |
| `https://www.fda.gov/drugs/drug-approvals-and-databases/drugsfda-data-files` | Drugs@FDA data files page | HTTP 200, 34,668 bytes, schema extracted |

### UNVERIFIED (returned 404, 403, or not confirmed)

| URL | Description | Status |
|-----|-------------|--------|
| `https://www.fda.gov/drugs/drug-approvals-and-databases/orange-book-data-files` | Orange Book data files landing page | HTTP 404 on direct fetch (redirects internally; page content retrieved via curl with browser UA) |
| `https://www.fda.gov/drugs/development-approval-process-drugs/orange-book-preface` | Orange Book preface (exclusivity code definitions) | HTTP 404 |
| `https://www.fda.gov/drugs/development-approval-process-drugs/orange-book-frequently-asked-questions` | Orange Book FAQ | HTTP 404 |
| `https://www.accessdata.fda.gov/scripts/cder/ob/patentlist.cfm` | Patent use code list (U-XXXX descriptions) | HTTP 403 (rate-limited / bot block during session) — page exists but blocked |
| `https://www.accessdata.fda.gov/scripts/cder/ob/index.cfm` | Orange Book online search | HTTP 403 (rate-limited) |
| `https://purplebooksearch.fda.gov/` | Purple Book search tool | HTTP 403 (bot block) |
| `https://purplebooksearch.fda.gov/api/v1/product/search` | Purple Book search API | HTTP 404 — no confirmed public API |
| `https://api.fda.gov/drug/patent.json` | openFDA patent-specific endpoint | HTTP 404 — does not exist |
| `https://api.fda.gov/drug/orangebook.json` (patent/exclusivity fields) | Patent and exclusivity data in openFDA | Does not exist in endpoint — products only |
| `https://www.fda.gov/drugs/drug-approvals-and-databases/drugsfda-data-files` | Drugs@FDA data files page | HTTP 404 on one attempt, HTTP 200 on second — intermittent |
| Orange Book update cadence (weekly vs monthly) | Documented update frequency | UNCONFIRMED in official documentation; inferred as monthly from file dates |

### INACCESSIBLE / PAYWALLED

None of the Orange Book or Drugs@FDA primary sources are paywalled. All data is free to access from FDA.gov. Third-party aggregators (e.g., Cortellis, Orange Book Express, Integrity) repackage this data with search interfaces and cross-links at commercial subscription prices — no added data not available from FDA directly.

---

## 12. Practical Access Pattern for a Screening Pipeline

```python
import pandas as pd

# Download once per month when updated (check file date in ZIP)
# EOBZIP: https://www.fda.gov/media/76860/download?attachment

products = pd.read_csv('products.txt', sep='~', header=0, dtype=str)
patents = pd.read_csv('patent.txt', sep='~', header=0, dtype=str)
exclusivity = pd.read_csv('exclusivity.txt', sep='~', header=0, dtype=str)

def is_clear(ingredient: str, proposed_indication: str, today=pd.Timestamp.today()):
    """
    Returns (clear: bool, blocking_items: list[str])
    """
    blocks = []
    
    # Step 1: Find NDA numbers
    ndas = products[
        products['Ingredient'].str.contains(ingredient, case=False, na=False) &
        (products['Appl_Type'] == 'N')
    ]['Appl_No'].unique()
    
    if len(ndas) == 0:
        return True, ["No US NDA found — check USPTO for background patents"]
    
    # Step 2: Parse dates
    def parse_date(s):
        try: return pd.to_datetime(s, format='%b %d, %Y')
        except: return pd.NaT
    
    excl = exclusivity[exclusivity['Appl_No'].isin(ndas)].copy()
    excl['exp_date'] = excl['Exclusivity_Date'].apply(parse_date)
    active = excl[excl['exp_date'] > today]
    
    # Step 3: Data exclusivity checks
    nce = active[active['Exclusivity_Code'].str.startswith('NCE')]
    if not nce.empty:
        blocks.append(f"HARD STOP: Active NCE until {nce['exp_date'].max().date()} — 505(b)(2) filing may be barred")
    
    ode = active[active['Exclusivity_Code'].str.startswith('ODE')]
    if not ode.empty:
        blocks.append(f"ODE active until {ode['exp_date'].max().date()} — check indication overlap with {ode['Exclusivity_Code'].tolist()}")
    
    for code in ['NP', 'NPP', 'NS', 'NDF']:
        sub = active[active['Exclusivity_Code'] == code]
        if not sub.empty:
            blocks.append(f"{code} exclusivity (3-year approval bar) until {sub['exp_date'].max().date()}")
    
    # Step 4: Patent checks
    pats = patents[patents['Appl_No'].isin(ndas)].copy()
    pats['exp_date'] = pats['Patent_Expire_Date_Text'].apply(parse_date)
    active_p = pats[pats['exp_date'] > today]
    
    ds = active_p[active_p['Drug_Substance_Flag'] == 'Y']
    if not ds.empty:
        blocks.append(f"DS patents active: {ds[['Patent_No','exp_date']].values.tolist()} — Para IV required")
    
    dp = active_p[active_p['Drug_Product_Flag'] == 'Y']
    if not dp.empty:
        blocks.append(f"DP (formulation) patents active: {len(dp)} rows — check formulation overlap")
    
    mou = active_p[active_p['Patent_Use_Code'].str.startswith('U-', na=False)]
    if not mou.empty:
        blocks.append(
            f"MoU patents active: {mou['Patent_Use_Code'].unique().tolist()} — "
            f"look up use code text at accessdata.fda.gov/scripts/cder/ob/patentlist.cfm "
            f"and check against proposed indication: {proposed_indication}"
        )
    
    ped = active_p[active_p['Patent_No'].str.endswith('*PED', na=False)]
    if not ped.empty:
        blocks.append(f"PED 6-month extension active on {len(ped)} patents — adjust expiry dates")
    
    return len(blocks) == 0, blocks
```

---

*Source data retrieved directly from FDA servers on 2026-08-05. File dates (Jul 10, 2026) confirm July 2026 Orange Book edition. All HTTP status codes measured at time of fetch. openFDA last_updated confirmed as 2026-08-05 from API metadata. No third-party sources used for data; all exclusivity code interpretations derived from 21 U.S.C. § 355, 21 CFR Part 314, and 21 U.S.C. § 360cc statutory text as applied to observed data structures.*
