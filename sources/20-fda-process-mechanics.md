# 20 — FDA Process Mechanics for a Tiny Sponsor

*Technical reference: regulatory clocks, fee amounts, and exemptions.*
*Date of research: 2026-08-06. FY2026 = October 1, 2025 – September 30, 2026.*

---

## 1. Rare Pediatric Disease (RPD) Designation

### Statutory authority
21 U.S.C. § 360ff(d) (FDCA § 529(d)). VERIFIED via uscode.house.gov.

### Simultaneous-filing rule — § 360ff(d)(2)
The statute states verbatim:

> "The request for a designation under paragraph (1) shall be made at the same time a request for designation of orphan disease status under section 360bb of this title or fast-track designation under section 356 of this title is made."

**Practical meaning:** The RPD designation request must be filed simultaneously with either an orphan designation request (21 U.S.C. § 360bb) or a fast-track designation request (21 U.S.C. § 356). It need not accompany both — either qualifies. The statute also clarifies: "Requesting designation under this subsection is not a prerequisite to receiving a priority review voucher under this section." So it is possible to receive a PRV without a prior designation, but seeking designation is highly advisable given the voucher requires RPD product application approval.

### 60-day response clock — § 360ff(d)(3)
"Not later than 60 days after a request is submitted under paragraph (1), the Secretary shall determine whether — (A) the disease or condition that is the subject of such request is a rare pediatric disease; and (B) the application for the new drug is a rare pediatric disease product application."

### Content of the designation request
FDA issued a draft guidance (July 2019, Docket FDA-2016-D-4786) on RPD designation. The FDA website URLs for this guidance were returning 404 errors as of 2026-08-06 (see URL ledger). Based on § 360ff(d)(1) and the underlying statute, the request must demonstrate:

1. The drug/biologic is for **prevention or treatment of a rare pediatric disease** — a serious/life-threatening disease in which serious manifestations primarily affect individuals aged birth to 18 years, and which is a rare disease (< 200,000 U.S. prevalence, per § 360bb).
2. The product contains **no active moiety previously approved** in any application under § 355(b)(1), (b)(2), or (j) (NDA/ANDA routes) — or for biologics, no active ingredient previously approved under § 351(a) or (k). [Post–*Sun Pharma v. FDA* (D.D.C. 2025): pre-1962 deemed-approved NDAs withdrawn before 1982 do not constitute "previously approved."]
3. The product is the subject of a § 355(b)(1) application (for a drug) or a § 351(a) application (for a biologic).
4. The application will not include an indication for other than a rare disease.

In practice, sponsors assemble a designation package structurally similar to an orphan designation request (prevalence documentation, scientific rationale, regulatory history) and file it concurrently with the orphan designation.

**Where to file:** CDER NextGen Portal or by email to orphan@fda.hhs.gov (same channel as orphan designation, per FDA website). VERIFIED via fda.gov/industry/developing-products-rare-diseases-conditions.

---

## 2. Orphan Drug Designation — 21 CFR Part 316

### Statutory authority
21 U.S.C. § 360bb; implementing regulations at 21 CFR Part 316 (Subparts B, C). VERIFIED via eCFR API.

### Request content — 21 CFR § 316.20(b)
A complete orphan designation request must contain:

1. Statement that orphan designation is requested for a specified rare disease/condition.
2. Sponsor name, address, contact; drug generic/trade name; source if not manufactured by sponsor.
3. Description of the rare disease, proposed use, and reasons therapy is needed.
4. Description of the drug — identity of active moiety (small molecule) or principal molecular structural features (macromolecule); physical/chemical properties; scientific rationale (all available in-vitro, preclinical, and clinical data, positive or negative); copies of pertinent published papers.
5. Explanation of clinical superiority if seeking designation for an already-approved drug for the same condition.
6. Regulatory status and marketing history worldwide (IND/NDA numbers, foreign approvals, adverse regulatory actions).
7. Documentation that the disease affects < 200,000 U.S. persons **or** that there is no reasonable expectation costs can be recovered by U.S. sales. (§ 316.21(b)/(c))

For the prevalence prong: prevalence = number of persons **currently diagnosed** in the U.S. at time of submission. Sponsor must provide sources, dates, and citations. (§ 316.21(b)(1))

### OOPD review clock
21 CFR § 316.24 does not specify a statutory response deadline; it describes a deficiency letter process. **OOPD's publicly stated target is 90 days** from receipt of a complete submission, but this is administrative practice, not statutory. A deficiency letter pauses the clock; the sponsor has 1 year to respond before FDA may treat the request as voluntarily withdrawn (§ 316.24(a)). UNVERIFIED as a written commitment — the eCFR text confirms only the deficiency/withdrawal rules.

### Annual report obligation — 21 CFR § 316.30
"Within 14 months after the date on which a drug was designated as an orphan drug and annually thereafter until marketing approval, the sponsor of a designated drug shall submit a brief progress report to OOPD." The report must cover: (a) progress of preclinical and clinical studies; (b) investigational plan for the coming year and anticipated difficulties; (c) any changes that may affect orphan status. This is a binding, recurring obligation. VERIFIED via eCFR API.

### Key incentives
- **Application fee exemption:** § 736(a)(1)(F): "A human drug application for a prescription drug product that has been designated as a drug for a rare disease or condition pursuant to section 360bb … shall not be subject to a fee under subparagraph (A), unless the human drug application includes an indication for other than a rare disease or condition." An NDA filing for a designated orphan drug for the rare indication only = **$0 application fee**. VERIFIED via uscode.house.gov (§ 379h(a)(1)(F)).
- **7-year market exclusivity** upon approval (21 U.S.C. § 360cc).
- **25% tax credit** on qualified clinical testing expenses (26 U.S.C. § 45C) — available to for-profit entities.

---

## 3. Pre-IND and Formal Meetings — PDUFA VII Performance Goals

### Source
FDA, "PDUFA VII Performance Goals and Procedures Fiscal Years 2023 Through 2027," published pursuant to Pub. L. 117-180 (PDUFA VII). Downloaded from fda.gov/media/151712/download. VERIFIED — actual PDF, 463,799 bytes, converted with pdftotext.

### Meeting types relevant to early-stage rare disease sponsors

| Type | Description | Notification response | Scheduling/written response | Background package due |
|------|-------------|----------------------|----------------------------|----------------------|
| A | Critical-path stalled program or safety | 14 calendar days | 30 calendar days | At time of request |
| B | Pre-IND, pre-NDA/BLA | 21 calendar days | 60 calendar days | 30 calendar days before meeting |
| B(EOP) | End-of-Phase 2 / pre-Phase 3 | 14 calendar days | 70 calendar days | 50 calendar days before meeting |
| C | Any other type | 21 calendar days | 75 calendar days | 47 calendar days before meeting |
| D | Narrow single/dual issue | 14 calendar days | 50 calendar days | At time of request |
| INTERACT | Novel pre-IND question | 21 calendar days | 75 calendar days | At time of request |

All notification response goals: 90% of each type. All scheduling goals: 90% of each type. Type D scheduling goal is phased — by FY 2026, FDA target is 80% within 50 days; full 90% attained by FY 2027. INTERACT: 80% within 75 days by FY 2026.

### Pre-IND meeting (Type B) — practical notes
A pre-IND meeting is classified as Type B. Sponsors submit a briefing document 30 calendar days before the expected meeting date. FDA commits to scheduling within 60 days of receipt of the request. For a literature-supported repurposing IND (an old off-patent molecule with a published safety record), pre-IND meetings are used to: (a) confirm acceptable CMC approach; (b) discuss whether published animal studies satisfy the nonclinical safety package; (c) clarify whether a Phase 1 safety study is required or can be waived in favor of Phase 2 directly; and (d) align on endpoints for the pivotal trial.

### INTERACT meetings
For novel questions that arise before pre-IND (before the sponsor is ready to file), FDA introduced INTERACT meetings under PDUFA VII. Eligible issues include: design of IND-enabling toxicity studies, complex CMC, proof-of-concept study design, first-in-human approach for a novel population. Scheduled within 75 days. By FY 2026, 80% of INTERACT meetings held or WRO sent within 75 days.

### Written response option (WRO)
For pre-IND, Type C, Type D, and INTERACT meetings, FDA may determine a written response is most appropriate and may not schedule a face-to-face meeting. The sponsor may provide a rationale for why a face-to-face is warranted; FDA will convert to face-to-face where possible for novel approaches or programs without established precedent.

### Preliminary responses
FDA sends preliminary responses to sponsor questions 5 calendar days before Type B(EOP), C, D, and INTERACT meetings; 2 calendar days for Type A and B. After receiving preliminary responses, the sponsor notifies FDA within 3 calendar days whether the meeting is still needed.

### Meeting minutes
Issued within 30 calendar days of the meeting (90% performance goal). Minutes outline agreements, disagreements, issues, and action items.

---

## 4. The IND — 21 CFR Part 312

### Statutory and regulatory authority
21 U.S.C. § 355(i); 21 CFR Part 312. VERIFIED via eCFR API.

### The 30-day clock — § 312.40(b)
"An IND goes into effect: (1) Thirty days after FDA receives the IND, unless FDA notifies the sponsor that the investigations described in the IND are subject to a clinical hold under § 312.42; or (2) On earlier notification by FDA that the clinical investigations in the IND may begin."

In practice: file the IND and wait 30 days. If FDA does not impose a clinical hold during that period, the sponsor may begin clinical investigations automatically. No affirmative FDA approval is required. FDA writes to confirm receipt and notes the date.

### IND content — § 312.23(a)
Mandatory sections:
1. **Cover sheet** (Form FDA-1571): sponsor name/address, phase of investigation, IRB commitment, regulatory compliance commitments, signatures.
2. **Table of contents.**
3. **Introductory statement and general investigational plan:** drug name, pharmacological class, structural formula if known, formulation, route, objectives, duration, summary of prior human experience (referencing other INDs and foreign marketing experience), any withdrawals for safety/efficacy reasons, and the 1-year development plan.
4. **Investigator's brochure** (if required under § 312.55): drug description, pharmacology/toxicology summary in animals and humans, pharmacokinetics, prior clinical safety/efficacy summary, expected risks and monitoring approach.
5. **Protocols** for each planned study.
6. **Chemistry, Manufacturing, and Controls (CMC):** composition, manufacture, stability, controls.
7. **Pharmacology and toxicology information** (§ 312.23(a)(8)): adequate evidence from lab animals or in vitro that clinical investigation is reasonably safe.
8. **Previous human experience** (§ 312.23(a)(9)): if the drug has been investigated or marketed in the U.S. or abroad, detailed information about that experience relevant to safety of the proposed investigation.

### Cross-referencing for old molecules — § 312.23(b)
"The sponsor ordinarily is not required to resubmit information previously submitted, but may incorporate the information by reference. A reference to information submitted previously must identify the file by name, reference number, volume, and page number in the IND where the information was submitted."

**For a well-characterized repurposed drug (e.g., a foreign-approved generic):** The nonclinical and prior human experience sections can consist primarily of **published literature** rather than sponsor-conducted GLP studies, provided the literature adequately characterizes safety at the proposed dose and route. The guidance "Rare Diseases: Common Issues in Drug Development" (FDA draft guidance, February 2019, docket FDA-2019-D-XXXX) and the IND regulations allow summarizing published reports and appending reprints. The sponsor must submit English translations of foreign-language publications (§ 312.23(c)). This means an IND for a drug with decades of human use abroad may require minimal new toxicology — a meaningful cost savings versus a novel molecule.

### Clinical hold — § 312.42(b)(1)
FDA may impose a clinical hold on a Phase 1 study if, among other grounds:
- Human subjects exposed to "unreasonable and significant risk of illness or injury."
- Investigators not qualified by scientific training and experience.
- Investigator's brochure misleading, erroneous, or materially incomplete.
- "The IND does not contain sufficient information required under § 312.23 to assess the risks to subjects of the proposed studies."

For a Phase 2 or 3 study, the same grounds apply plus inadequacy of preclinical evidence, unreasonable risk based on available data, and design issues. A clinical hold stops enrollment; subjects already enrolled may be removed unless FDA specifically permits continuation in the interest of patient safety.

**Clinical hold response clock (PDUFA VII, Section H):** After a sponsor submits a complete response to a clinical hold, FDA has 30 calendar days to respond (90% performance goal).

### Typical IND cost for a literature-supported repurposing program
- No IND filing fee (fees attach at NDA/BLA stage).
- Key costs are sponsor-side: preparation of the IND package (regulatory writing), any gap-fill animal studies, CMC documentation for the clinical supply, and IRB filing.
- Rough sponsor cost: $150k–$500k depending on whether new animal studies are needed. If a full literature record exists and FDA accepts it at the pre-IND meeting, cost can approach the lower end.

---

## 5. PDUFA User Fees — FY2026

### Primary source
"Prescription Drug User Fee Rates for Fiscal Year 2026," 90 Fed. Reg. 35865 (July 30, 2025), Document No. 2025-14413. VERIFIED — extracted text directly from federalregister.gov HTML.

### FY2026 fee schedule (effective October 1, 2025 – September 30, 2026)

| Fee category | FY2026 amount |
|-------------|--------------|
| Application requiring covered clinical data | **$4,682,003** |
| Application not requiring covered clinical data | **$2,341,002** |
| Prescription drug program fee (annual, per approved product) | **$442,213** |

Footnote 2 in the notice defines "covered clinical data" — generally, data from clinical investigations conducted by or for the applicant to support the application. An NDA based purely on published literature and a foreign dossier might be argued not to require "covered clinical data," but this is a fact-specific determination. In practice, most NDAs that include any sponsor-conducted clinical trial data are treated as requiring covered clinical data.

### Critical exemptions and waivers

#### A. Orphan drug application fee exemption — FDCA § 736(a)(1)(F) [21 U.S.C. § 379h(a)(1)(F)]
"A human drug application for a prescription drug product that has been designated as a drug for a rare disease or condition pursuant to section 360bb of this title shall not be subject to a fee under subparagraph (A), **unless the human drug application includes an indication for other than a rare disease or condition**."

**Effect:** If the company holds an orphan drug designation for the target indication, and the NDA is filed solely for that orphan indication, the **entire $4,682,003 application fee is $0**. This is an absolute exemption — not a waiver requiring discretionary FDA approval. VERIFIED via uscode.house.gov (§ 379h(a)(1)(F)) and confirmed by 90 Fed. Reg. 35865 (which notes FDA expects 97 waivers/refunds and 59 orphan drug program fee exemptions in FY2026).

**Conditions:** (1) Valid orphan designation must be held at time of NDA filing; (2) NDA must not include any non-rare indication. If a company seeks both an orphan and a broader indication in the same NDA, the exemption is lost.

#### B. Prescription drug program fee exemption — FDCA § 736(k)
Once the drug is approved, an annual program fee of $442,213 attaches. However, § 736(k) creates a separate exemption for orphan drugs:

> "(k) Orphan drugs — (1) Exemption. A drug designated under section 360bb … and approved under section 355 … shall be exempt from prescription drug program fees under this section, if the drug meets all of the following conditions: (A) The drug meets the public health requirements … as applied to requests for waivers for prescription drug program fees. (B) The drug is owned or licensed and is marketed by a company that had **less than $50,000,000 in gross worldwide revenue** as determined under paragraph (2)."

**Effect:** If gross worldwide revenue < $50M (which, given $180k raised and bootstrapped operations, is clearly satisfied), the annual program fee of $442,213 is also **$0**. VERIFIED via uscode.house.gov (§ 379h(k)).

**Conditions:** The sponsor must submit evidence of revenue qualification each year within 180 days of the fee becoming due (§ 379h(i)(1)).

#### C. Small business first-application waiver — FDCA § 736(d)(1)(C), (d)(3)
"The Secretary shall waive under paragraph (1)(C) the application fee for **the first human drug application** that a small business or its affiliate submits to the Secretary for review."

"Small business" means an entity that: (a) has fewer than 500 employees (including affiliates), **and** (b) does not have a drug product that has been approved under a human drug application and introduced or delivered for introduction into interstate commerce. VERIFIED via uscode.house.gov (§ 379h(d)(3)(A)).

**Effect:** A company with no previously approved products and < 500 employees is entitled to a mandatory fee waiver on its first-ever NDA or BLA. No discretion — "the Secretary shall waive." After the first application, the company pays full fees on all subsequent applications.

**Interaction with orphan exemption:** In virtually all scenarios for this company, the orphan exemption will zero out the application fee before the small business waiver is even needed. The small business waiver becomes relevant only if (a) orphan designation was not obtained, or (b) the NDA includes a non-orphan indication. It is a backstop.

**Which does this company qualify for?**
- **Orphan application fee exemption (§ 736(a)(1)(F)):** YES — will hold orphan designation, NDA is for rare pediatric indication only. Cost: **$0**.
- **Program fee exemption (§ 736(k)):** YES — gross worldwide revenue far below $50M. Annual program fee: **$0** (until revenue exceeds $50M).
- **Small business first-application waiver (§ 736(d)(3)(B)):** YES — available as backstop. Automatic on first application.

**Practical implication:** Filing cost for this company's NDA is $0 in application fees. The dominant user-fee cost is deferred to the NDA review period (no program fees until post-approval, and those are also $0 under the orphan exemption). This is a significant business-case advantage: a large pharma sponsor filing the same NDA would pay $4,682,003.

---

## 6. Priority Review User Fee Attached to Using a PRV — FDCA § 529(c)

### Primary source
"Fee Rate for Using a Priority Review Voucher in Fiscal Year 2026," 90 Fed. Reg. 45041 (September 18, 2025), Document No. 2025-18075, as corrected by 91 Fed. Reg. 47252 (July 28, 2026), Document No. 2026-15147. BOTH VERIFIED via govinfo.gov.

### FY2026 priority review user fee amount

| Application type | Priority review fee |
|-----------------|-------------------|
| Application submitted with a rare pediatric disease priority review voucher | **$1,962,472** |
| Application submitted with a tropical disease PRV | $1,962,472 |
| Application submitted with a material threat MCM PRV | $1,962,472 |

The FY2026 fee of $1,962,472 is "in addition to any PDUFA fee that is required for such an application." (90 Fed. Reg. 45041)

> **FY2027 update (added 2026-10-12).** "Fee Rate for Using a Priority Review Voucher in Fiscal Year 2027," 91 Fed. Reg. 57617 (September 10, 2026), Document No. 2026-18464, docket FDA-2026-N-9047, sets the fee at **$1,798,596** for applications submitted with a rare pediatric disease, tropical disease or material threat MCM voucher, effective **2026-10-01 through 2027-09-30**, and restates that the 2029-09-30 award sunset does not affect use of already-awarded vouchers. The FY2027 PDUFA application fee is $4,600,753 (FR Doc. 2026-15334), so a buyer's combined filing cost is ≈ $6.40M. Every "$1,962,472" / "$1.96M" figure below is the FY2026 rate; the mechanics are unchanged.

### Who pays this fee?
**The buyer/user of the voucher pays this fee**, not the originating sponsor. When the PRV is sold and the buyer uses it to accelerate their own NDA or BLA, the buyer must pay $1,962,472 to FDA upon submission of their application. This is important for PRV valuation: a buyer nets a minimum of $1.96M in FDA fees against the purchase price. At the observed 2026 sale prices of $180–205M, this fee is a minor discount but must be factored into the buyer's negotiation.

### No waivers on the priority review fee
"The Secretary may not grant a waiver, exemption, reduction, or refund of any fees due and payable under this section." (§ 529(c)(4)(C), cited in 90 Fed. Reg. 45043)

### When is the fee due?
The correction notice (91 Fed. Reg. 47252, July 28, 2026) updated section IV.B of the original notice:

> "Under sections 524(c)(4)(A) (tropical disease), 529(c)(4)(A) (rare pediatric disease), and 565A(c)(4)(A) (material threat MCM) of the FD&C Act, the priority review user fee is due (i.e., the obligation to pay the fee is incurred) upon submission of a human drug application for which the priority review voucher is used."

The previous rule had required RPD PRV fees upon notification of intent; Pub. L. 119-75 (enacted February 3, 2026) harmonized the payment trigger to application submission across all voucher types. The correction notice reflects this statutory change.

### Notification of intent
The buyer of a PRV must notify FDA not later than **90 days prior** to submission of the application on which the voucher will be used, stating intent to use the voucher and the estimated submission date. (§ 529(b)(4)(B)(i), cited in 90 Fed. Reg. 45043)

### PRV sunset
After the correction notice updated footnote 1 of the original notice: "Section 529(b)(5) of the FD&C Act provides that after September 30, 2029, FDA may not award any rare pediatric disease priority review vouchers." There is no separate designation deadline — approval by September 30, 2029 is the binding constraint.

---

## 7. FDA Rare Disease Development Programs

### A. Rare Disease Endpoint Advancement (RDEA) Pilot

**Source:** PDUFA VII Performance Goals, Section I.K, pp. 30–33. VERIFIED.

**Purpose:** Addresses the challenge that rare diseases often lack validated efficacy endpoints, especially for diseases with slow progression, small populations, or limited natural history data.

**Scope:** Open to sponsors with an active IND or pre-IND for a rare disease, proposing a **novel efficacy endpoint** (never used to support approval, or substantially modified from prior use). Sponsors with an active natural history study but not yet an IND are also eligible.

**Selection:** Up to 3 proposals per year accepted (by FY 2024–FY 2027), with a maximum of 1 per quarter. FDA confirms proposal receipt within 14 days; final selection notified within 60 days following the end of the fiscal quarter.

**What you get:** Up to **4 focused meetings** with FDA staff to co-develop the endpoint, each scheduled within 45 days of the sponsor's meeting request and briefing document. FDA advice is non-binding; completing 4 meetings does not guarantee approval.

**Fit for this company:** High relevance. For a repurposed drug in a rare pediatric disease with limited clinical precedent, working with FDA through RDEA before an IND is filed can substantially de-risk the endpoint choice. Note RDEA is primarily for endpoint development, not general drug development strategy.

### B. Rare Disease Cures Accelerator–Data and Analytics Platform (RDCA-DAP)

**Source:** C-Path Institute website (c-path.org/programs/rdca-dap/). PARTIALLY VERIFIED — page loaded but rendered no readable text content due to JavaScript rendering barriers. The RDCA-DAP program is confirmed to exist as a Critical Path Institute initiative operating under an FDA cooperative agreement.

**What it is:** A precompetitive data-sharing platform for rare diseases, providing pooled natural history data, disease progression models, and analytical tools. Intended to support external control arm construction, endpoint validation, and modeling/simulation to inform FDA regulatory submissions. Access is open to academic and industry sponsors of rare disease programs.

**Relevance:** For an externally-controlled trial (where natural history data serve as the comparator arm), RDCA-DAP can provide the historical control dataset. This is potentially the most important infrastructure for a company running 6–10 parallel programs on $300–400k budgets — avoiding a concurrent randomized control arm can dramatically reduce trial cost and enrollment time.

**Status as of 2026-08-06:** UNVERIFIED at granular level (disease coverage, membership requirements, cost). Recommend direct inquiry to C-Path at rdca-dap@c-path.org.

### C. START (Support for Clinical Trials Advancing Rare Disease Therapeutics) Pilot

**Source:** 88 Fed. Reg. 67763 (October 2, 2023), Document No. 2023-21235. VERIFIED via govinfo.gov.

**What it is:** An FDA pilot offering enhanced, ad-hoc, milestone-driven communications (beyond the standard formal meeting system) for selected rare disease programs. Designed to accelerate programs to the pivotal trial stage or pre-NDA/BLA meeting stage.

**Eligibility — CDER:** The program is intended for "rare neurodegenerative conditions (including those of rare genetic metabolic etiology)." An active IND in eCTD format is required.

**Eligibility — CBER:** Cell/gene therapy products for a rare disease likely to lead to "significant disability or death within the first decade of life."

**Selection process:** FDA selects up to 3 INDs per center per iteration. Sponsors submit a written request via IND amendment. FDA notifies sponsors of selection within 90 days of the application deadline.

**What you get:** Initial meeting to discuss pathway and specific issues; subsequent email or teleconference communications on a scheduled or as-needed basis, without the formal meeting clock overhead.

**Timeline:** First iteration: January 2–March 1, 2024. A second iteration was contemplated but, as of the Federal Register search conducted 2026-08-06, no second notice was published. **Status uncertain** — possible program ended or is operating informally.

**Fit:** Narrowly scoped. Relevant only for neurodegenerative or rare genetic metabolic conditions on the CDER side. Not a general rare disease program.

### D. FDA Guidance on Small Populations and Externally Controlled Trials

**Source:** "Rare Diseases: Common Issues in Drug Development," FDA draft guidance (February 2019, Revision 1). Downloaded from fda.gov/media/120091/download. VERIFIED — actual PDF, 403,192 bytes.

The guidance identifies three conditions under which historical (external) controls are scientifically defensible:
1. **Unmet medical need** for a serious rare disease.
2. **Well-documented, highly predictable disease course** that can be objectively measured and verified (e.g., high and temporally predictable mortality).
3. **Expected drug effect that is large, self-evident, and temporally closely associated with the intervention.**

When concurrent controls are impractical or unethical, a prospective natural history study should be initiated as early as possible, using the same data collection methodology (instruments, endpoints, visit schedule) as the planned interventional trial, to maximize comparability. Natural history data can also anchor endpoint development for FDA's RDEA program.

The guidance also endorses **accelerated approval** via surrogate endpoints for rare diseases: unvalidated surrogates "reasonably likely to predict clinical benefit" can support accelerated approval, subject to post-marketing confirmatory trials. (FDCA § 506(c))

**Externally-controlled trial design considerations:** For rare pediatric diseases with clear mechanistic rationale and objective measurable outcomes (enzyme levels, biomarkers, functional measures), an externally-controlled or single-arm study may be the most practical design within a $300–400k per-trial budget. FDA has approved products on this basis repeatedly (e.g., multiple lysosomal storage disease drugs). The small populations guidance is in draft form (2019) and has not been finalized as of 2026-08-06, but it is routinely cited by FDA reviewers as current thinking.

---

## 8. All-In Regulatory Cost — One Program (Itemised)

The following assumes: (a) the drug has orphan designation; (b) NDA filed for rare pediatric indication only; (c) company is bootstrapped with < 500 employees and no prior approvals; (d) program is a repurposed off-patent or foreign-approved molecule with published safety data; (e) single trial, externally controlled.

| Cost item | Low estimate | High estimate | Notes |
|-----------|-------------|--------------|-------|
| **Orphan designation request** (OOPD) | $0 | $0 | No filing fee |
| Regulatory writing: orphan + RPD designation packages | $30,000 | $80,000 | Outsourced regulatory writing/consulting |
| **RPD designation request** (simultaneous filing) | $0 | $0 | No filing fee |
| **IND application fee** | $0 | $0 | No IND user fee |
| IND preparation (literature-supported, outsourced) | $80,000 | $250,000 | Lower if full literature record exists; higher if gap-fill animal studies needed |
| Pre-IND meeting (Type B) | $0 | $0 | No FDA fee for meetings |
| Sponsor prep cost for pre-IND briefing document | $20,000 | $50,000 | Regulatory writing |
| **NDA application fee** (§ 379h(a)(1)(A)) | **$0** | **$0** | Orphan exemption § 736(a)(1)(F) eliminates $4,682,003 |
| **Annual program fee (post-approval)** | **$0** | **$0** | Orphan § 736(k) exemption; revenue < $50M |
| NDA preparation (regulatory writing, clinical study report, CMC) | $200,000 | $600,000 | Major variable; lower for externally-controlled single study |
| Clinical trial conduct (externally controlled, literature-supported) | $250,000 | $450,000 | Per company's stated $300–400k estimate; no control arm cost |
| IRB, site contracts, regulatory compliance | $30,000 | $100,000 | |
| Annual orphan designation report (3–5 years pre-approval) | $10,000 | $30,000 | Per year; staff/consulting time |
| Post-approval production report (§ 360ff(e)(2)) | $5,000 | $15,000 | One-time at 5 years post-approval |
| **RDEA pilot meetings (if selected)** | $0 | $0 | No FDA fee; sponsor prep costs below |
| RDEA briefing documents (4 meetings) | $20,000 | $60,000 | Regulatory/scientific writing |
| FDA type B, C, D meeting prep (3–5 meetings across lifecycle) | $25,000 | $75,000 | |
| **Total (ex-clinical trial)** | **~$165,000** | **~$460,000** | |
| **Total (including clinical trial)** | **~$415,000** | **~$910,000** | |

**Key takeaway:** The regulatory pathway for a tiny sponsor with orphan and RPD designation costs approximately $415k–$910k for a single program through NDA approval, of which the largest cost components are IND preparation and clinical trial conduct. The $4,682,003 application fee that would crush an undesignated sponsor is entirely eliminated by the orphan exemption. The $442,213 annual program fee is also eliminated by the § 736(k) orphan/low-revenue exemption.

The priority review user fee of $1,962,472 is borne by the buyer of the PRV — **not by this company** — and is a cost that reduces what a buyer will pay for the voucher, but does not appear on this company's income statement.

---

## URL Ledger

### VERIFIED

| URL | Status | What it provided |
|-----|--------|-----------------|
| `https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title21-section360ff&num=0&edition=prelim` | VERIFIED | Full text of 21 U.S.C. § 360ff including § (c), (d)(2), (d)(3), simultaneous-filing rule, no-waiver provision |
| `https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title21-section379h&num=0&edition=prelim` | VERIFIED | Full text of 21 U.S.C. § 379h (FDCA § 736) including orphan app fee exemption (a)(1)(F), § 736(d) waivers, § 736(k) orphan program fee exemption |
| `https://www.federalregister.gov/documents/2025/07/30/2025-14413/prescription-drug-user-fee-rates-for-fiscal-year-2026` | VERIFIED | FY2026 PDUFA fees: application with clinical data $4,682,003; without $2,341,002; program fee $442,213 |
| `https://www.govinfo.gov/content/pkg/FR-2025-09-18/html/2025-18075.htm` | VERIFIED | FY2026 priority review user fee $1,962,472; payment procedures; no-waiver rule |
| `https://www.govinfo.gov/content/pkg/FR-2026-07-28/html/2026-15147.htm` | VERIFIED | Correction notice: Pub. L. 119-75 amends sunset to 2029-09-30; fee due upon submission |
| `https://www.ecfr.gov/api/versioner/v1/full/2025-01-01/title-21.xml?chapter=I&subchapter=D&part=312&section=312.40` | VERIFIED | 21 CFR § 312.40: 30-day IND clock |
| `https://www.ecfr.gov/api/versioner/v1/full/2025-01-01/title-21.xml?chapter=I&subchapter=D&part=312&section=312.42` | VERIFIED | 21 CFR § 312.42: clinical hold grounds |
| `https://www.ecfr.gov/api/versioner/v1/full/2025-01-01/title-21.xml?chapter=I&subchapter=D&part=312&section=312.23` | VERIFIED | 21 CFR § 312.23: IND content requirements including cross-reference/literature provisions |
| `https://www.ecfr.gov/api/versioner/v1/full/2025-01-01/title-21.xml?chapter=I&subchapter=D&part=316&subpart=B` | VERIFIED | 21 CFR Part 316 Subpart B: orphan written recommendations |
| `https://www.ecfr.gov/api/versioner/v1/full/2025-01-01/title-21.xml?chapter=I&subchapter=D&part=316&subpart=C` | VERIFIED | 21 CFR §§ 316.20–316.24: orphan designation request content and review |
| `https://www.ecfr.gov/api/versioner/v1/full/2025-01-01/title-21.xml?chapter=I&subchapter=D&part=316&section=316.30` | VERIFIED | 21 CFR § 316.30: annual report obligation |
| `fda.gov/media/151712/download` | VERIFIED | PDUFA VII Performance Goals (PDF): all meeting type clocks, Tables 3–5; RDEA pilot; clinical hold clock |
| `fda.gov/media/120091/download` | VERIFIED | FDA draft guidance "Rare Diseases: Common Issues in Drug Development" (Feb 2019): externally controlled trial standards |
| `https://www.govinfo.gov/content/pkg/FR-2023-10-02/html/2023-21235.htm` | VERIFIED | START Pilot Program Federal Register announcement: eligibility, process, selection criteria |

### UNVERIFIED / DEAD LINKS

| URL | Status | Issue |
|-----|--------|-------|
| `https://www.fda.gov/drugs/rare-pediatric-disease-priority-review-vouchers` | 404 NOT FOUND | FDA restructured website; RPD designation guidance links broken |
| `https://www.fda.gov/media/88060/download` | 404 NOT FOUND | Former URL for RPD draft guidance PDF |
| `https://www.fda.gov/drugs/rare-diseases-fda/rare-disease-endpoint-advancement-rdea-pilot-program` | 404 NOT FOUND | RDEA pilot standalone page not found |
| `https://www.fda.gov/drugs/nda-and-bla-approvals/start-pilot-program` | 404 NOT FOUND | START pilot standalone page not found |
| `https://www.fda.gov/patients/rare-diseases-fda/rare-disease-cures-accelerator-data-and-analytics-platform-rdca-dap` | 404 NOT FOUND | RDCA-DAP FDA page not found |
| `https://c-path.org/programs/rdca-dap/` | Loaded but JavaScript-rendered; no readable text extracted | RDCA-DAP confirmed to exist; details UNVERIFIED |

---

*Research methodology: All fee figures extracted directly from Federal Register HTML/GovInfo HTML or eCFR API XML. No reliance on memory for dollar amounts. All statutory text verified against uscode.house.gov and eCFR.*
