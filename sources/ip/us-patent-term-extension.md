<!-- Recovered from agent-ab9aaeea3e50f9080.jsonl on 2026-08-06. The original agent completed 83
     tool calls across 35 CFR 156 / 37 CFR Subpart F / 21 CFR Part 60 / Federal Register API /
     Orange Book bulk download, then died on an API connection error (FailedToOpenSocket) before
     writing its report. All data below is derived from those tool results. Supplementary live
     fetches (marked "verified 2026-08-06") were made to close two gaps the dead agent left open:
     the 37 CFR 1.20 PTE application fee, and the USPTO FR grant-notice census. -->

# US Patent Term Extension (35 U.S.C. § 156)

**Relevance to funnel split.** PTE applies only to the patent holder — it is not part of the
exclusivity calculus for a repurposing company filing a new NDA. Its relevance here is negative
space: before selecting a Funnel-A candidate (never-US moiety, 505(b)(1)), confirm that no live PTE
certificate extends any US patent covering the target product. A PTE can add up to five years to a
US patent, meaning a molecule that naively looks off-patent in 2026 may actually be protected until
2030+. The Orange Book's `Patent_Expire_Date_Text` field already incorporates PTE and is the fastest
check for NDA-listed drugs.

---

## 1. Statutory Framework

**35 U.S.C. § 156 — Patent Term Extension (PTE)**
Source: https://www.law.cornell.edu/uscode/text/35/156 — VERIFIED (HTTP 200, content extracted)

PTE was created by the Drug Price Competition and Patent Term Restoration Act of 1984 (Hatch-Waxman,
Pub. L. 98-417) and extended to animal drugs by Pub. L. 100-670. It compensates patent holders for
regulatory review time consumed before a product could reach market.

### Eligibility — five conditions (§ 156(a))

1. The patent has not yet expired at the time of application.
2. The patent term has never previously been extended under § 156(e)(1).
3. The application is submitted within **60 days** of the date the product first received marketing
   permission.
4. The product was subject to a regulatory review period before its commercial marketing or use.
5. The marketing permission represents the **first** permitted commercial marketing or use (with
   limited exceptions for recombinant-DNA manufacturing and veterinary biologics).

### Duration formula (§ 156(c); implemented in 37 CFR 1.775)

For human drugs the extension equals the full regulatory review period (testing phase + approval
phase), then reduced by:
- Days that occurred before the patent was issued;
- Days during which the applicant did not act with "due diligence" (determined by HHS);
- One-half of the remaining testing-phase days.

The result is then subject to two caps:
- **Absolute cap:** 5 years maximum extension.
- **14-year rule:** The remaining patent life at approval plus the extension cannot exceed 14 years
  from the date of marketing approval. (37 CFR 1.775(d)(3): "By adding 14 years to the date of
  approval ... and comparing to the extended expiry; the lesser governs.")

**One-patent-per-product rule.** Only one patent per approved product may be extended (§ 156(c)(4)).
The applicant selects which patent to extend.

### What "regulatory review period" means for human drugs (§ 156(g)(1)(B))

Per 37 CFR 1.775(c) (eCFR verified):
- **Testing phase:** From the effective date of the IND (§ 505(i) exemption) through the date the
  NDA was initially submitted.
- **Approval phase:** From the date the NDA was initially submitted through the date FDA granted
  marketing approval.

The sum of both phases is the gross regulatory review period; FDA publishes this determination in
the Federal Register (see Section 4).

### VYALEV worked example (FR Doc 2026-13006, verified from raw text)

- IND effective: December 8, 2016
- NDA initial submission: May 19, 2022 → testing phase = 1,989 days
- NDA approval: October 16, 2024 → approval phase = 882 days
- **Total regulatory review period: 2,871 days**
- Patentee (AbbVie) seeking extension for US Patent Nos. 9,446,059; 10,174,061; and 10,730,895
- Orange Book shows all three expiring October 21, 2035 (NDA 216962, verified from OB patent.txt)
- The original 20-year term for US 9,446,059 (filed ~2015) would have expired ~2035; the PTE
  determination is still pending as of 2026-06-29.

---

## 2. PTE vs. PTA vs. European SPC

### Patent Term Adjustment (PTA) — 35 U.S.C. § 154(b)

PTA and PTE are completely separate mechanisms. PTA compensates for **USPTO prosecution delays**
(delays in examination exceeding the statutory timelines under AIA). It is calculated
automatically during prosecution and printed on the face of the issued patent. It is **not** the
same as PTE. Both can apply to the same patent (PTA adjusts the base 20-year term; PTE then runs
from the adjusted expiry date).

37 CFR Subpart F, §§ 1.701–1.705 govern PTA. §§ 1.710–1.791 govern PTE. The subpart heading is
"Adjustment and Extension of Patent Term." Source: eCFR API, verified (HTTP 200, 37 CFR § 1.710
and full Subpart F extracted).

### European Supplementary Protection Certificate (SPC)

The EPO page (https://www.epo.org/en/searching-for-patents/legal/spc) returned a 404 during the
original agent run (JS-rendered, not accessible via curl). UNVERIFIED from primary source in
the original run.

Key structural differences (from general knowledge, NOT verified from a primary source in this
session — mark UNVERIFIED):
- European SPCs are granted by **each individual national patent office**, not by the EPO centrally.
- The maximum SPC duration is 5 years (matching PTE), plus a 6-month paediatric extension if a
  Paediatric Investigation Plan has been completed.
- The calculation uses the date of first marketing authorisation in the European Economic Area, not
  the IND date — making the SPC period often shorter than the US PTE.
- There is no "one-SPC-per-product" rule equivalent; multiple SPCs can exist across member states
  for the same product covering different patents.

**For practical due diligence, use the SPC register at each relevant national office (EPO Espacenet
does index SPCs as a supplementary data layer).** See `spc-verification.md` in this directory.

---

## 3. USPTO Application Process (37 CFR §§ 1.720–1.791)

All CFR sections below were fetched from the eCFR API
(`https://www.ecfr.gov/api/versioner/v1/full/2024-01-01/title-37.xml?part=1&section=X.XXX`) —
all returned HTTP 200.

### Filing window

37 CFR § 1.720(f): The application must be submitted **within 60 days** of the date the product
first received permission for commercial marketing. Missing this window forfeits eligibility; there
is no late-filing provision.

### Who may apply (§ 1.730)

The owner of record of the patent, or its agent (e.g., a licensee). Must be submitted by a
registered practitioner unless the patent owner signs personally.

### Formal requirements (§ 1.740) — what the application must contain

- Complete identification of the approved product (chemical/generic name, structure/characteristics).
- The applicable Federal statute (for drugs: FFDCA § 505 or PHS Act § 351).
- The date of marketing approval.
- For drug products: identification of each active ingredient, with a statement that it has **not**
  been previously approved, or, if it has been, when and under what provision. (This is where the
  § 156 "first permitted commercial marketing" requirement is demonstrated.)
- Statement that the application is being submitted within the 60-day window.
- Complete patent identification (inventor, number, issue date, expiration date).
- A copy of the patent including specification, claims, and drawings.
- A copy of any disclaimer, certificate of correction, maintenance fee receipt, or reexamination
  certificate.
- A showing that at least one patent claim reads on the approved product, method of use, or method
  of manufacture.
- Relevant dates for the regulatory review period (IND effective date, NDA submission date, approval
  date).

### Application filing fees (37 CFR § 1.20(j)) — verified 2026-08-06

From eCFR § 1.20(j) (HTTP 200, full text fetched):

| Application type | Fee |
|---|---|
| Formal application for PTE (§ 1.740) | **$1,180** |
| Initial interim extension application (§ 1.790) | $440 |
| Subsequent interim extension application (§ 1.790) | $230 |

No small-entity or micro-entity discount is specified for PTE applications (the § 1.20(j) table
has no such reduction, unlike examination and maintenance fees).

### Interim extensions (§ 1.790)

If a patent is about to expire while the underlying regulatory review period is still ongoing (i.e.,
FDA has not yet approved the product), the patent owner may apply for interim extensions of up to
one year each. Requirements:
- Initial application: filed during the 6-month window ending 15 days before patent expiry.
- Subsequent applications: filed 60–30 days before the preceding interim extension expires.
- Each application must include all information required under §§ 1.740 and 1.741 appropriate to
  the current stage.
- Must certify that the regulatory review period described in § 156(g)(1)(B)(ii) (approval phase)
  has not yet been completed.

Note: Under § 1.790, interim extensions require electronic filing (USPTO patent electronic filing
system).

### Determination of eligibility (§ 1.750)

The Director (or designated USPTO officials) may determine eligibility solely from the
representations in the application. They may also request further information or make independent
inquiries. A notice of final determination is mailed to the applicant; a single request for
reconsideration may be filed within the time set in the notice (or one month if no time is set).

---

## 4. FDA Role: 21 CFR Part 60 and Federal Register Notices

Source: `https://www.govinfo.gov/content/pkg/CFR-2024-title21-vol1/xml/CFR-2024-title21-vol1-part60.xml`
— VERIFIED (HTTP 200, full XML returned; also confirmed via eCFR API: HTTP 200, 32.6 KB XML).

21 CFR Part 60 (source authority: 21 U.S.C. 348, 355, 360e, 360j, 371, 379e; 35 U.S.C. 156;
42 U.S.C. 262) was originally promulgated 53 FR 7305, Mar. 7, 1988, with nomenclature changes
at 68 FR 24879 (May 9, 2003) and 88 FR 45065 (July 14, 2023).

### FDA's statutory duties under 21 CFR Part 60

**Subpart B — Eligibility Assistance (§ 60.10):** Upon USPTO request, FDA verifies whether:
- the product underwent a regulatory review period (i.e., was subject to § 505 or equivalent);
- the approval represents first permitted commercial marketing;
- the PTE application was filed within 60 days of approval.

**Subpart C — Regulatory Review Period Determinations (§§ 60.20–60.28):**
- FDA consults its records and experts to verify dates and determine the length of the regulatory
  review period.
- **Publishing in the Federal Register:** FDA is required to publish its determination of the
  regulatory review period. This is the notice stream described below.
- **Timeline:** FDA must determine the period within **30 days** of USPTO's request (§ 60.28),
  with possible extensions.
- **Correction window:** Any person with knowledge that published dates are incorrect may submit
  comments within 60 days of the Federal Register publication; the applicant has 15 days to respond
  (§ 60.24).
- **Finality:** Determinations become final 180 days after publication unless a due diligence
  petition or revision request is filed (§ 60.26).

**Subpart D — Due Diligence Petitions (§ 60.30):** Any interested party (including a potential
generic competitor) may petition FDA within 180 days of the regulatory review period determination
publication to allege that the patentee did not act with "due diligence" during the review period.
A finding of lack of due diligence reduces the extension accordingly.

**FDA contact for PTE matters (from FR Doc 2026-13006 raw text):**
Patrick Clouser, Office of the Commissioner, Food and Drug Administration, 12420 Parklawn Drive,
Rockville, MD 20852, 240-402-5276.

---

## 5. Federal Register Notice Stream — Live Census

### Query parameters

The agent established that the `www.federalregister.gov` API domain works, while `api.federalregister.gov`
returns 302 redirects to `unblock.federalregister.gov` (and then 404). Use `www.federalregister.gov`
as the base URL.

**Broad query — all FDA documents mentioning "regulatory review period":**
```
https://www.federalregister.gov/api/v1/documents.json
  ?conditions[term]=regulatory+review+period
  &conditions[agencies][]=food-and-drug-administration
  &per_page=1
  &order=newest
```
- **count = 3,777** (as of 2026-08-05, verified from Bash curl output)
- Oldest: 1994-01-04 (doc 93-31812, Dietary Supplements — a false positive on "regulatory review
  period" from labeling context)
- Newest: 2026-08-05 (doc 2026-15920, Micro-Tracers response — another false positive)

This broad query is too noisy. Use the exact-phrase query below.

**Targeted query — exact phrase "determination of regulatory review period":**
```
https://www.federalregister.gov/api/v1/documents.json
  ?conditions[term]="determination+of+regulatory+review+period"
  &conditions[agencies][]=food-and-drug-administration
  &per_page=1
  &order=newest
```
(Note: use `conditions[term]` not `conditions[search]` — the agent confirmed this is the working
parameter; the `conditions[search]` variant was rejected by the API.)

- **count = 1,159** (verified 2026-08-05 from two separate curl calls with order=newest and
  order=oldest, both returning count=1159)
- **Oldest:** 1994-01-04, doc 94-36, "Determination of Regulatory Review Period for Purposes of
  Patent Extension; BetaseronRegister" (Betaseron = interferon beta-1b, first multiple sclerosis
  biological)
  URL: https://www.federalregister.gov/documents/1994/01/04/94-36/determination-of-regulatory-review-period-for-purposes-of-patent-extension-betaseronregister
  Abstract verified (HTTP 200, 2026-08-06): "The Food and Drug Administration (FDA) has determined
  the regulatory review period for Betaseron<Register> and is publishing this notice of that
  determination as required by law."
- **Newest:** 2026-06-29, doc 2026-13006, "Determination of Regulatory Review Period for Purposes
  of Patent Extension; VYALEV"
  URL: https://www.federalregister.gov/documents/2026/06/29/2026-13006/determination-of-regulatory-review-period-for-purposes-of-patent-extension-vyalev
- Document type: all 1,159 are type "Notice" (verified by sampling 3 most recent)
- Date range: January 4, 1994 — June 29, 2026

**Full-text URLs for individual notices (verified from doc 2026-13006):**
```
XML:  https://www.federalregister.gov/documents/full_text/xml/2026/06/29/2026-13006.xml
HTML: https://www.federalregister.gov/documents/full_text/html/2026/06/29/2026-13006.html
TXT:  https://www.federalregister.gov/documents/full_text/text/2026/06/29/2026-13006.txt
JSON: https://www.federalregister.gov/api/v1/documents/2026-13006?publication_date=2026-06-29
```
The TXT endpoint returned the full plain-text notice (HTTP 200). Pattern:
`https://www.federalregister.gov/documents/full_text/text/YYYY/MM/DD/{doc_number}.txt`

**Sample of recent notices (verified 2026-08-05):**
| Date | Doc number | Notes |
|---|---|---|
| 2026-06-29 | 2026-13006 | VYALEV (foscarbidopa/foslevodopa) — 2,871-day RRP |
| 2026-04-16 | 2026-07422 | — |
| 2026-04-03 | 2026-06483 | — |
| 2026-04-03 | 2026-06481 | — |
| 2026-04-03 | 2026-06480 | — |
| 2026-04-03 | 2026-06479 | — |
| 2026-04-03 | 2026-06478 | — |
| 2026-04-03 | 2026-06477 | — |
| 2026-04-03 | 2026-06476 | — |

(The April 3, 2026 cluster of seven notices in a single day is typical — FDA batches determinations.)

### USPTO grant notices in the Federal Register

When USPTO actually issues a PTE certificate or interim extension order, it too publishes in the
Federal Register. Query (verified 2026-08-06):
```
https://www.federalregister.gov/api/v1/documents.json
  ?conditions[term]="extension+of+the+term+of+U.S.+Patent"
  &conditions[agencies][]=patent-and-trademark-office
  &per_page=3
  &order=newest
```
- **count = 101** USPTO grant/order notices in the Federal Register
- Newest (2026-07-23, doc 2026-14941): "Grant of Interim Extension of the Term of U.S. Patent
  No. 8,461,196; Centanafadine Hydrochloride"
  Abstract: "The United States Patent and Trademark Office has issued an order granting a one-year
  interim extension of the term of U.S. Patent No. 8,461,196 (`196 patent)."

Note: The Federal Register only captures interim extensions and their orders under 35 U.S.C.
§ 156(d)(5) — 37 CFR § 1.780 requires this. Final PTE certificates are published only in the
**USPTO Official Gazette** (see Section 6).

---

## 6. Where PTE Certificates Are Published

Source: 37 CFR § 1.780 (verified from eCFR API, HTTP 200):

> "If a determination is made pursuant to § 1.750 that a patent is eligible for extension and that
> the term of the patent is to be extended, a certificate of extension, under seal, or an order
> granting interim extension under 35 U.S.C. 156(d)(5), will be issued to the applicant for the
> extension of the patent term. Such certificate or order will be recorded in the official file of
> the patent and will be considered as part of the original patent. **Notification of the issuance
> of the certificate or order of extension will be published in the Official Gazette of the United
> States Patent and Trademark Office.** Notification of the issuance of the order granting an
> interim extension under 35 U.S.C. 156(d)(5), including the identity of the product currently
> under regulatory review, will be published in the Official Gazette of the United States Patent
> and Trademark Office and in the Federal Register."

**Practical consequence:** Final PTE certificates are not indexed in the Federal Register. They
appear in the USPTO Official Gazette and are recorded on the face of the patent (visible in Patent
Center). The patent record in USPTO Patent Center will show the adjusted expiry date reflecting PTE.
The Orange Book `Patent_Expire_Date_Text` field also reflects the PTE-adjusted expiry.

**USPTO PTE list page:** Multiple URLs were attempted:
- `https://www.uspto.gov/patent/laws-and-regulations/patent-term-extension` → HTTP 404
- `https://www.uspto.gov/patent/laws-and-regulations/patent-term-extension/list-patent-terms-extended-35-usc-156` → HTTP 301 redirect → then 404
- `https://www.uspto.gov/patents/patent-term-extension` → HTTP 404
- `https://www.uspto.gov/patents/maintain/patent-term-extension` → HTTP 404

All USPTO PTE-specific landing pages returned 404 or redirect loops as of 2026-08-06. The Official
Gazette is the authoritative published record but is not easily queryable in bulk.

---

## 7. Orange Book Patent Fields and PTE

**Bulk download:** https://www.fda.gov/media/76860/download
- Verified 2026-08-06: HTTP 200, content-length 1,091,413 bytes, filename `EOBZIP_2026_06.zip`,
  last-modified Fri Jul 10 2026. Contains three files: `patent.txt` (1,223,277 bytes),
  `products.txt` (7,467,977 bytes), `exclusivity.txt` (75,337 bytes).

**patent.txt columns** (verified from header row):
```
Appl_Type ~ Appl_No ~ Product_No ~ Patent_No ~ Patent_Expire_Date_Text ~
Drug_Substance_Flag ~ Drug_Product_Flag ~ Patent_Use_Code ~ Delist_Flag ~ Submission_Date
```
Total rows (excluding header): **22,131** patent entries.

**Patent_Expire_Date_Text** — from OB documentation (https://www.fda.gov/drugs/drug-approvals-and-databases/orange-book-data-files, verified HTTP 200):
> "The date the patent expires as submitted by the applicant holder **including applicable
> extensions**."

This means the `Patent_Expire_Date_Text` **already incorporates PTE** where a PTE has been granted
and the applicant has submitted that date. It also incorporates pediatric exclusivity when a `*PED`
suffix is appended (6-month extension appears as a separate row with `Patent_No` = `NNNNNNN*PED`).

**Example — liraglutide (NDA 022341, Victoza), verified from OB patent.txt:**
```
N~022341~001~8114833~Aug 13, 2025~Y~Y~~~Mar 13, 2012
N~022341~001~8114833*PED~Feb 13, 2026~~~~~
N~022341~001~9968659~Jan 9, 2037~~~U-2313~~Jun 12, 2018
N~022341~001~9968659*PED~Jul 9, 2037~~~~~
```
US 8,114,833 expired Aug 13, 2025 (base patent term); the `*PED` row extends to Feb 13, 2026 via
6-month pediatric exclusivity.

**Example — VYALEV (NDA 216962, foscarbidopa/foslevodopa), verified from OB patent.txt:**
```
N~216962~001~12251365~Jun 10, 2040~~~U-4030~~Apr 10, 2025
N~216962~001~9446059~Oct 21, 2035~Y~Y~U-4030~~Nov 14, 2024
N~216962~001~10174061~Oct 21, 2035~~Y~U-4030~~Nov 14, 2024
N~216962~001~10730895~Oct 21, 2035~Y~~~~Nov 14, 2024
```
US 9,446,059; 10,174,061; and 10,730,895 all show Oct 21, 2035. The PTE determination was
published Jun 29, 2026 (FR Doc 2026-13006); the PTE certificate has not yet been issued as of that
date. When granted, the OB expiry date would be updated.

**Note on Gleevec/imatinib:** NDA 021335 (DISCN) and 021588 show no patent rows — these patents
have expired and were delisted from the OB. Gleevec is confirmed off-patent via OB products.txt.
The OB patent.txt only carries currently-listed (active) patents.

---

## 8. Computing Whether a Molecule's US Patents Have Expired

**Step 1 — Orange Book check (for NDA-listed drugs):**
Query `patent.txt` for any rows with a `Patent_Expire_Date_Text` in the future. If no rows exist
for the NDA, all OB-listed patents have either expired or been delisted. If rows exist, the date
shown already includes PTE if the patentee submitted a PTE-adjusted date. Note: Biologics (BLA)
are NOT in the Orange Book — they are in the Purple Book.

**Step 2 — USPTO Patent Center / PAIR check:**
Search by patent number at https://patentcenter.uspto.gov. The patent record shows the adjusted
expiry date incorporating PTA (automatically) and PTE (if a certificate has been issued). Patent
Center is a JS-rendered SPA; not curl-accessible.

**Step 3 — Federal Register PTE determination status:**
Check whether a FR determination notice exists for the product:
```
https://www.federalregister.gov/api/v1/documents.json
  ?conditions[term]="determination+of+regulatory+review+period"+"[DRUG NAME]"
  &conditions[agencies][]=food-and-drug-administration
  &per_page=5
  &order=newest
```
If a determination has been published but no certificate has been issued, the PTE is still pending.
If 180+ days have elapsed with no due diligence petition, the determination is final. The USPTO
then has discretion on whether and how much to grant (up to the 5-year / 14-year caps).

**Step 4 — Interim extension check:**
If the patent appears to have expired but the product was recently approved or is still in review,
check the USPTO FR notices:
```
https://www.federalregister.gov/api/v1/documents.json
  ?conditions[term]="interim+extension"+"[PATENT NUMBER]"
  &conditions[agencies][]=patent-and-trademark-office
```
Or search the Official Gazette.

**Quick formula — expected maximum extended expiry:**
```
max_expiry = max(
    approval_date + 14 years,
    original_patent_expiry + min(5 years, regulatory_review_period_reduced)
)
```
This gives an upper bound; the actual extension is usually less.

---

## 9. Interaction with PRV Eligibility (Funnel-A vs. Funnel-B)

PTE does not affect PRV eligibility directly, but it affects candidate selection:

- **Funnel A (never-US moiety, 505(b)(1), PRV-eligible):** If the target molecule is approved
  abroad but never in the US, there are no US OB patent listings and no US PTE to check. Check
  foreign patent filings directly (Espacenet, PATSTAT). If a US patent does exist (method of
  manufacture, composition), check whether a PTE application is pending.
- **Funnel B (US generic, 505(b)(2), no PRV):** The relevant question is whether any OB-listed
  patents remain that would trigger Paragraph IV litigation. PTE on a listed patent means the
  earliest ANDA entry date is later than the base expiry.

Both funnels benefit from confirming Gleevec-style off-patent status: OB has no listed patents,
no interim extension notices, and no pending PTE determination in the FR.

---

## 10. Unfinished — Worth Re-Running

The following were left incomplete when the agent died:

1. **USPTO Official Gazette bulk access.** The agent never found a machine-readable endpoint for
   the OG PTE certificate list. The OG is published weekly and available as XML at
   https://bulkdata.uspto.gov/ — but that hostname was unreachable (`bulkdata.uspto.gov` returned
   a DNS resolution failure during the agent run). Worth retrying; if it resolves, it provides a
   full list of PTE certificates granted.

2. **37 CFR 1.20(j) fee verification as of current fee schedule.** The 2024-01-01 eCFR snapshot
   shows $1,180 for formal PTE application. The USPTO publishes annual fee adjustments; the most
   recent fee schedule notice would be the authoritative source for 2026 fees. The FR fee query
   (conditions[term]="patent+term+extension+application+fee") returned 206 documents — the agent
   never drilled into the most recent one.

3. **European SPC primary source.** epo.org/en/searching-for-patents/legal/spc returned 404
   (page moved or JS-dependent). The SPC register is accessible per-country; `spc-verification.md`
   in this directory covers this.

4. **USPTO PTE granted-certificates list.** All USPTO PTE landing page URLs tried returned 404.
   The list of patents extended under 35 U.S.C. 156 may now be accessible only through Patent
   Center per-patent lookups or through the Official Gazette. Worth checking:
   `https://www.uspto.gov/patents/maintain` and related USPTO sitemap pages.

---

## URL Ledger

### VERIFIED

| URL | Status | Notes |
|---|---|---|
| `https://www.law.cornell.edu/uscode/text/35/156` | HTTP 200 | Full 35 U.S.C. § 156 text extracted |
| `https://www.govinfo.gov/content/pkg/CFR-2024-title21-vol1/xml/CFR-2024-title21-vol1-part60.xml` | HTTP 200 | 21 CFR Part 60 full XML |
| `https://www.ecfr.gov/api/versioner/v1/full/2024-01-01/title-21.xml?part=60` | HTTP 200 | 32.6 KB eCFR XML |
| `https://www.ecfr.gov/api/versioner/v1/full/2024-01-01/title-37.xml?part=1&section=1.710` | HTTP 200 | § 1.710 PTE-eligible products |
| `https://www.ecfr.gov/api/versioner/v1/full/2024-01-01/title-37.xml?part=1&subpart=F` | HTTP 200 | Full 37 CFR Subpart F (PTA + PTE) |
| `https://www.ecfr.gov/api/versioner/v1/full/2024-01-01/title-37.xml?part=1&section=1.720` | HTTP 200 | § 1.720 Conditions for extension |
| `https://www.ecfr.gov/api/versioner/v1/full/2024-01-01/title-37.xml?part=1&section=1.730` | HTTP 200 | § 1.730 Applicant requirements |
| `https://www.ecfr.gov/api/versioner/v1/full/2024-01-01/title-37.xml?part=1&section=1.740` | HTTP 200 | § 1.740 Formal application requirements |
| `https://www.ecfr.gov/api/versioner/v1/full/2024-01-01/title-37.xml?part=1&section=1.750` | HTTP 200 | § 1.750 Eligibility determination |
| `https://www.ecfr.gov/api/versioner/v1/full/2024-01-01/title-37.xml?part=1&section=1.775` | HTTP 200 | § 1.775 Calculation for human drugs |
| `https://www.ecfr.gov/api/versioner/v1/full/2024-01-01/title-37.xml?part=1&section=1.780` | HTTP 200 | § 1.780 Certificate publication (Official Gazette) |
| `https://www.ecfr.gov/api/versioner/v1/full/2024-01-01/title-37.xml?part=1&section=1.790` | HTTP 200 | § 1.790 Interim extensions |
| `https://www.ecfr.gov/api/versioner/v1/full/2024-01-01/title-37.xml?part=1&section=1.20` | HTTP 200 | § 1.20 Post-issuance fees (PTE = $1,180) |
| `https://www.federalregister.gov/api/v1/documents.json?conditions[term]="determination+of+regulatory+review+period"&conditions[agencies][]=food-and-drug-administration&per_page=1&order=newest` | HTTP 200 | count=1,159; newest=2026-06-29 (VYALEV) |
| `https://www.federalregister.gov/api/v1/documents.json?conditions[term]="determination+of+regulatory+review+period"&conditions[agencies][]=food-and-drug-administration&per_page=1&order=oldest` | HTTP 200 | count=1,159; oldest=1994-01-04 (Betaseron) |
| `https://www.federalregister.gov/api/v1/documents/2026-13006.json` | HTTP 200 | VYALEV notice metadata |
| `https://www.federalregister.gov/documents/full_text/text/2026/06/29/2026-13006.txt` | HTTP 200 | VYALEV notice full text (RRP = 2,871 days) |
| `https://www.federalregister.gov/api/v1/documents/94-36.json` | HTTP 200 | Betaseron notice metadata (2026-08-06) |
| `https://www.federalregister.gov/api/v1/documents.json?conditions[term]="extension+of+the+term+of+U.S.+Patent"&conditions[agencies][]=patent-and-trademark-office` | HTTP 200 | count=101 USPTO grant notices (2026-08-06) |
| `https://www.fda.gov/media/76860/download` | HTTP 200 | OB zip 1,091,413 bytes, EOBZIP_2026_06.zip |
| `https://www.fda.gov/drugs/drug-approvals-and-databases/orange-book-data-files` | HTTP 200 | OB field documentation |
| `https://api.fda.gov/drug/drugsfda.json?search=openfda.brand_name:GLEEVEC&limit=1` | HTTP 200 | Gleevec NDA021588 confirmed |

### UNVERIFIED (could not confirm from primary source)

| URL / Source | Status | Notes |
|---|---|---|
| `https://api.federalregister.gov/v1/documents.json` (api. subdomain) | HTTP 302 → unblock.federalregister.gov → 404 | Use `www.federalregister.gov` instead |
| `https://www.epo.org/en/searching-for-patents/legal/spc` | HTTP 404 (JS-rendered) | SPC system description — use national offices |
| `https://bulkdata.uspto.gov/` | DNS resolution failure | USPTO bulk data; retry |
| `https://www.uspto.gov/patent/laws-and-regulations/patent-term-extension` | HTTP 404 | USPTO PTE landing page — moved |
| `https://www.uspto.gov/patent/laws-and-regulations/patent-term-extension/list-patent-terms-extended-35-usc-156` | HTTP 301 → 404 | PTE list — URL no longer valid |
| `https://mpep.uspto.gov/RDMS/MPEP/print?version=r-08.2017.02&href=d0e302338.html` | HTTP 500 | MPEP Chapter 2750 print endpoint |
| `https://www.fda.gov/drugs/development-approval-process-drugs/patent-term-restoration` | HTTP 404 | FDA PTE guidance page — moved |
| `https://www.fda.gov/drugs/development-approval-process-drugs/patent-term-restoration-0` | HTTP 404 | Alternate FDA PTE URL — moved |
| `https://www.accessdata.fda.gov/scripts/cder/ob/index.cfm` | HTTP 404 | Old OB interactive interface |
| European SPC system details | UNVERIFIED | Not obtained from primary source in this session |
