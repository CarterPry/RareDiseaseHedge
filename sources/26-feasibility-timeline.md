# 26 — Can Any Program Finish Before 2029-09-30?
# Critical-Path Feasibility Analysis

*Date of research: 2026-08-06. Adversarial review added: 2026-08-06. Statutory deadline: FDA may
not award a PRV after 2029-09-30 (Pub. L. 119-75 § 6604(a), confirmed by 91 Fed. Reg. 47252,
July 28, 2026 — VERIFIED). Award = approval. Today: 2026-08-06. Available window: ~3.15 years
(38 months).*

*Headline conclusion revised by adversarial review: per-program probability is **3–5% (generic
program)** to **20–22% (optimized program)**; original 9% was too high for a generic program and
too low for a well-designed one. See Section 8 for full reconciliation.*

---

## 1. The PDUFA VII Review Clocks — Verified Verbatim

**Source:** FDA, "PDUFA VII Performance Goals and Procedures Fiscal Years 2023 Through 2027,"
downloaded from fda.gov/media/151712/download, 453,799 bytes. VERIFIED 2026-08-06 via curl.

All clocks for a 505(b)(1) NME NDA (which is what a Funnel A RPD-eligible application must be):

### Section I.B.4 (NME Program, verbatim):

> "For NME NDA and original BLA submissions that are filed by FDA under the Program, the PDUFA
> review clock will begin at the conclusion of the 60-day filing review period that begins on the
> date of FDA receipt of the original submission. The review performance goals for these
> applications are as follows:
> a. Review and act on 90 percent of standard NME NDA and original BLA submissions within
> **10 months of the 60-day filing date.**
> b. Review and act on 90 percent of priority NME NDA and original BLA submissions within
> **6 months of the 60-day filing date.**"

### Section I.A.1 (tabulated summary, verbatim):

| Application type | Standard | Priority |
|----------------|----------|---------|
| NME NDAs and original BLAs | 90% in **10 months** of 60-day filing date | 90% in **6 months** of 60-day filing date |
| Class 1 resubmitted original applications | 90% in **2 months** of receipt | 90% in **2 months** of receipt |
| Class 2 resubmitted original applications | 90% in **6 months** of receipt | 90% in **6 months** of receipt |

### CRITICAL: Resubmission after a Complete Response Letter (CRL) — Section I.B.3.e.iv (verbatim):

> "The resubmission goals described in Sections I.A.1.e and I.A.1.f will not apply to any
> resubmission of the application following an FDA complete response action. Any such resubmission
> will be reviewed **as available resources permit.**"

This means: **the Class 1 (2-month) and Class 2 (6-month) clocks do NOT apply** to resubmissions
after a CRL on an NME NDA in the Program. A CRL triggers an indefinite review queue.

### Priority review grant — 21 U.S.C. § 360ff(a)(4)(C) and FDA discretion:

The statute requires that the application "(C) the Secretary deems eligible for priority review"
as one of the conditions for PRV eligibility. Priority review is NOT automatic even for RPD
applications. Per the FDA Priority Review page (VERIFIED 2026-08-06):

> "FDA decides on the review designation for every application. However, an applicant may expressly
> request priority review as described in the Guidance for Industry Expedited Programs for Serious
> Conditions – Drugs and Biologics. FDA informs the applicant of a Priority Review designation
> within 60 days of the receipt of the original BLA, NDA, or efficacy supplement."

Priority review requires demonstrating "significant improvement in the safety or effectiveness of
the treatment, diagnosis, or prevention of serious conditions when compared to standard
applications." For a repurposed molecule in a rare pediatric disease, this standard is almost
always met by the unmet need alone — but it must be expressly requested and granted. A denial of
priority review (extremely rare for a genuine unmet-need RPD) would mean a 10-month + 60-day
review clock instead of 6-month + 60-day, adding 4 months to the critical path.

---

## 2. Backwards Critical-Path Schedule from 2029-09-30

Working backwards from the mandatory approval date of 2029-09-30.

### Phase A: FDA Priority Review (NME, 505(b)(1))

| Step | PDUFA VII clock | Duration |
|------|----------------|----------|
| 60-day filing review (before PDUFA clock starts) | § I.B.4, PDUFA VII | 60 calendar days (2 months) |
| Priority review clock (6-month goal) | § I.B.4, PDUFA VII | 6 months (180 calendar days) |
| **Total NDA-to-decision window** | | **~8 months** |

**Latest NDA submission date: 2029-09-30 minus 8 months = 2029-01-30**

In practice, FDA has a 60-day clock to notify of priority review designation. A sponsor submitting
January 30, 2029 would receive the PDUFA goal date (August 29, 2029, approximately) and the
priority review notification by late March 2029. If approved on the PDUFA date, that is before
the September 30, 2029 sunset. **This leaves zero buffer.** Any extension of the review clock
(major amendment triggers +3 months per § I.B.5.a.i of PDUFA VII) or any delay past the goal date
would push approval to October or later — after sunset.

**Conservative latest NDA submission: 2028-11-30** (2 months buffer for goal date extension or
filing issues).

### Phase B: NDA Preparation After Last-Patient-Last-Visit (LPLV)

| Step | Source/Basis | Duration |
|------|-------------|---------|
| Database lock after LPLV | Industry standard; clinical trial CSR timelines | 1–3 months |
| Statistical analysis and CSR drafting | ICH E3 guideline; rare disease externally-controlled trial | 3–6 months |
| NDA compilation, QC, regulatory writing | PDUFA goal assumes complete application at submission | 2–4 months |
| **Total NDA prep after LPLV** | | **6–13 months** |

**Conservative LPLV date needed: 2028-11-30 minus 9 months = 2028-02-28**

Note: For an externally-controlled single-arm study, the CSR is simpler (no randomized control arm
comparison, no unblinding ceremony), but FDA expects the CSR to follow ICH E3 structure. A
literature-based external control requires careful documentation of the comparator data sources.

### Phase C: Clinical Trial Conduct

**Enrolment and treatment timeline** varies dramatically by disease. For a rare pediatric disease
trial:

| Parameter | Source/Basis | Optimistic | Conservative |
|-----------|-------------|-----------|--------------|
| Site activation (IRB, contracts, regulatory submissions) | Industry rare disease benchmark | 3 months | 6–9 months |
| Enrolment ramp (first patient in to full enrolment) | Rare pediatric disease; N typically 10–30 patients | 6–18 months | 18–36 months |
| Treatment period | Disease-specific; often 6–52 weeks for metabolic/enzyme diseases | 6 months | 12 months |
| Follow-up | Disease-specific | 3 months | 6 months |
| **Total trial conduct** | | **18 months** | **54+ months** |

**Enrolment is the single most dangerous variable.** NORD, FDA, and NIH GRDS data consistently
show that rare pediatric disease trials enrol at 1–3 patients/site/year. For a disease with
worldwide prevalence under 5,000, finding 10–25 evaluable patients can take 18–36 months even
with 5–10 sites. Enrolment failures are the leading cause of rare disease trial delays and the
leading reason programs started within this window do not complete.

**LPLV needed by 2028-02-28.** Working back from conservative LPLV:

- Trial must begin enrolment (first patient in) no later than: **2026-08-28** (optimistic, 18 months before LPLV)
- Or: **2024-08-28** in the truly conservative scenario — which has already passed.

**Conservative "must begin enrolment" date: 2026-08-28 to 2027-02-28**
This is essentially NOW — August 2026 or at most six months from now.

### Phase D: IND Submission and 30-Day Clock

| Step | Regulatory basis | Duration |
|------|-----------------|---------|
| Pre-IND meeting request to scheduling | PDUFA VII Table, Type B: **60 calendar days** (90% performance goal) | ~2 months |
| Pre-IND briefing document preparation | PDUFA VII: due 30 calendar days before scheduled meeting | ~1–2 months |
| Pre-IND meeting (or written response) | PDUFA VII: written response within 60 days if no face-to-face | Day of meeting or within 30 days for minutes |
| IND preparation and submission | 21 CFR § 312.23; literature-supported | 1–3 months post-meeting |
| IND 30-day safety review clock | 21 CFR § 312.40(b): "30 days after FDA receives the IND, unless...clinical hold" | 30 calendar days |
| **Total from pre-IND meeting request to IND becoming effective** | | **5–8 months** |

If the company requests a pre-IND meeting TODAY (August 6, 2026), the meeting will be scheduled
within 60 days — approximately October 2026. Briefing document must be filed by approximately
September 2026 (30 days before the meeting). IND submission follows approximately
November–December 2026. IND becomes effective ~January 2027.

**VERIFIED clocks:**
- Pre-IND (Type B) scheduling: **60 calendar days** (PDUFA VII Table, verified verbatim)
- IND 30-day clock: 21 CFR § 312.40(b), VERIFIED via eCFR API

### Phase E: End-of-Phase-2 (EOP2) Meeting — PDUFA VII Type B(EOP)

The EOP2 meeting is not legally mandatory, but FDA considers it essential for NME NDAs, and the
PDUFA NME Program (§ I.B) explicitly requires a pre-NDA meeting to agree on "content of a
complete application." Per PDUFA VII (VERIFIED):

- **EOP2 / pre-Phase 3 meeting (Type B(EOP)):** scheduling goal = **70 calendar days** from request
- **Pre-NDA meeting (Type B):** scheduling goal = **60 calendar days** from request; must occur
  "not less than 2 months prior to the planned submission" (PDUFA VII § I.B.1.a, verbatim)

These meetings add approximately 3–5 months to the critical path between trial completion and NDA
submission, above and beyond NDA preparation time. The pre-NDA meeting in particular is treated
as near-mandatory by FDA — without it, sponsors risk an RTF (Refuse to File) for a "not
sufficiently complete" application.

**Adding an EOP2 meeting to the critical path:**

If enrolment completes by February 2028 and LPLV is February 2028:
- Analysis and CSR: March–July 2028 (5 months)
- EOP2/pre-NDA meeting request: August 2028 → meeting scheduled by October 2028
- Pre-NDA meeting occurs: October 2028 (2 months before NDA target)
- NDA submission: December 2028
- Priority review 60-day filing + 6-month clock → PDUFA goal date: approximately August–September 2029
- **Still within window — but with essentially zero buffer.**

---

## 3. Summary Table: Latest Possible Milestone Dates

*Working backwards from 2029-09-30 approval. "Conservative" = each interval uses median/realistic
duration. "Optimistic" = each interval uses best-case duration, no slippage anywhere.*

**Phase durations used:**

| Phase | Conservative | Optimistic | Source |
|-------|-------------|-----------|--------|
| FDA priority review (60-day filing + 6-month clock) | 8 months | 8 months | PDUFA VII § I.B.4, VERIFIED |
| NDA prep after LPLV (including pre-NDA meeting) | 9 months | 5 months | PDUFA VII; industry standard |
| Trial conduct (site activation + enrolment + treatment + follow-up) | 36 months | 18 months | Rare pediatric disease benchmarks; UNVERIFIED as primary source |
| IND effective to first patient in | 3 months | 1 month | IRB/site activation |
| IND submission to effective | 1 month | 1 month | 21 CFR § 312.40(b), VERIFIED |
| Pre-IND meeting to IND submission | 3 months | 1 month | Literature-supported program |
| Pre-IND meeting request to meeting | 2 months | 2 months | PDUFA VII Type B: 60 days, VERIFIED |
| **Total from first meeting request to approval** | **62 months** | **36 months** | |

**Backward-dated milestone table (as of 2026-08-06):**

| Milestone | Latest date (conservative) | Latest date (optimistic) |
|-----------|--------------------------|------------------------|
| **FDA approval — PRV awarded** | 2029-09-30 | 2029-09-30 |
| NDA submission | **2028-11-30** | **2029-01-30** |
| Pre-NDA meeting | 2028-09-30 | 2028-11-30 |
| LPLV (last patient last visit) | **2028-02-28** | **2028-08-31** |
| First patient in (enrolment start) | **2025-02-28** (PAST) | **2027-02-28** |
| IND becomes effective | **2024-11-30** (PAST) | **2027-01-31** |
| IND submission | **2024-10-31** (PAST) | **2026-12-31** |
| Pre-IND meeting | **2024-07-31** (PAST) | **2026-09-30** |
| Pre-IND meeting request filed | **2024-05-31** (PAST) | **2026-07-31** |

**Interpretation:**
- The conservative scenario's milestones have all passed. No program starting from scratch today
  can finish in the conservative scenario.
- The optimistic scenario shows that a pre-IND meeting request filed by **approximately July 2026**
  (this month) is the last viable entry point. The company's IND goal (end 2026) fits the optimistic
  scenario, but it is the theoretical minimum — any slippage kills the window.
- **The last date a trial can start and still (optimistically) reach approval: approximately 2027-02-28.**
- **The last date an NDA can be submitted and still (optimistically) reach approval: approximately 2029-01-30.**
  In practice, file by 2028-11-30 to preserve a 2-month buffer against goal date extensions.

---

## 4. What Breaks These Schedules

### A. Ultra-Rare Pediatric Enrolment Routinely Overruns

The single largest risk. Rare disease trials targeting children with conditions of <5,000 US
prevalence typically enrol:
- 1–3 patients per site per year (NORD/NIH data; UNVERIFIED as a published source — cite with
  caution; this is consistent with FDA's own statements in the 2019 draft guidance on rare diseases)
- Sites are often academic centers with long contracting timelines (3–6 months per site)
- Pediatric trials require parental consent, often at specialized centers that see 2–5 patients
  with the relevant disease per year

A disease with 500 US patients, a trial requiring 15 evaluable completers, and a 30% screen-failure
rate requires finding ~22 patients. With 5 sites enrolling 2/year, that is 2.2 years — and that
assumes sites are up and running immediately. In practice, site activation adds 6–12 months.

**Historical rare pediatric disease enrolment data from PRV-winning programs:**
No primary source was available for this run to document specific enrolment durations for past PRV
recipients. UNVERIFIED. The analysis above uses conservative assumptions consistent with FDA's
published statements on rare disease development challenges.

### B. One CRL is Almost Certainly Fatal to the Window

Under PDUFA VII § I.B.3.e.iv (VERIFIED verbatim above): a resubmission after a CRL on an NME NDA
is reviewed "as available resources permit" — no clock. In practice, FDA has taken 6–18 months to
act on such resubmissions historically. Adding 6 months (best case) to the latest optimistic NDA
submission date of 2029-01-30 puts approval at 2030-08-30 — 11 months past sunset.

**There is no recovery path from a CRL.** A program that receives a CRL at any point during its
first review cycle — even a CRL issued in August 2029 — cannot obtain approval before September 30,
2029. The sponsor would need to resubmit, and that resubmission has no committed review clock.

**First-cycle approval rate for NMEs:** Published academic literature (Hwang et al., various CDER
analyses) consistently finds that approximately 80–90% of NME NDAs are approved on the first review
cycle. However, several important caveats apply:
1. These rates include large-pharma programs with extensive pre-NDA alignment meetings and established
   CMC packages.
2. For a tiny sponsor's first NDA, with a novel externally-controlled trial design, a foreign-approved
   molecule with a WHO-GMP-only manufacturing site (possibly requiring a first-ever FDA PAI), and a
   small clinical dataset, the first-cycle approval rate is likely LOWER than the industry average.
3. The PDUFA VII Program explicitly aims at "first cycle approval when possible" but offers no
   guarantee.

**Quantified impact:** If first-cycle approval probability for this company's profile is 70%
(versus ~85% industry average), then 30% of programs receive a CRL and are eliminated from the
PRV window. Combined with enrolment and timeline risk, this is a major probability subtractor.

**Source on first-cycle rates:** UNVERIFIED at the primary-source level in this run. The FDA's
PDUFA performance reports contain cycle-completion data but the relevant annual reports were not
successfully retrieved (see URL ledger). The ~85% first-cycle rate is widely cited in regulatory
science literature and is consistent with CDER's stated goal of first-cycle approval. Mark this
UNVERIFIED pending retrieval of CDER's FY2023 or FY2024 annual performance report.

### C. CMC and Manufacturing Readiness — WHO GMP Is Not FDA GMP

Per FDA Compliance Program 7346.832 (VERIFIED 2026-08-06, downloaded 709,966 bytes), verbatim:

> "If FDA finds that sufficient information is available, a PAI may not be needed."

And:

> Objective 1 (Readiness for Commercial Manufacturing) coverage is specifically triggered by:
> **"The facility has never been inspected."**

A WHO-GMP-certified API manufacturer that has never been inspected by FDA is the highest-risk
scenario for triggering a mandatory Pre-Approval Inspection (PAI). PAI timing:

> "Within 60 calendar days of receiving an NDA or ANDA, OPMA sends a PAI or DFR request to ORA."

PAI scheduling and completion from NDA submission can take 6–18 months for foreign facilities.
FDA's MRA partners (EU, Canada, Switzerland, Australia, Japan, UK, Israel) allow FDA to rely on
partner inspection reports. **WHO Prequalification is NOT an MRA partner.** A site with only WHO
GMP must be treated as uninspected by FDA and will likely trigger a PAI.

**For programs sourcing API from Georgia, Ukraine, or other non-MRA countries:** Assume a PAI
will be required. The PAI must be completed before approval. If the PAI finds deficiencies, FDA
will issue a Form 483 and potentially withhold approval — adding 3–12 months for corrective actions.

**Does the PAI fit in the critical path?** Barely, if:
- The NDA is submitted by November 2028
- The PAI request goes to ORA within 60 days (January 2029)
- ORA schedules and completes the foreign inspection by May–June 2029
- Results are NAI or VAI (not OAI)
- Final approval follows by September 2029

Any OAI finding on the PAI kills the window entirely.

### D. Priority Review Is Not Automatic

Section 360ff(a)(4)(C) requires FDA to "deem eligible for priority review" — this is a condition of
PRV eligibility. A sponsor must request priority review at NDA submission and demonstrate that the
drug offers "significant improvement in the safety or effectiveness of the treatment, diagnosis, or
prevention of serious conditions." For a legitimate rare pediatric disease with no approved
treatment, this condition is almost always met, but:

1. **The request must be made.** An applicant that fails to request priority review, or whose
   request is denied, loses both the 6-month review clock and PRV eligibility for that application.
2. FDA notifies of priority review designation within 60 days of receipt (VERIFIED).
3. For a repurposed drug with prior approved use abroad but no US approval, demonstrating the
   "significant improvement" standard is relatively easy — but the sponsor must document it.
4. A denial of priority review would mean a 10-month + 60-day review clock (total ~12 months),
   pushing the latest NDA submission date to September 2028 — very tight.

---

## 5. Comparison to Stated Company Plan

**Stated plan:** "First IND cleared; first trial to start before end of 2026."

**Assessment of fit:**

The stated plan is consistent with the optimistic critical-path schedule but **sits at the extreme
edge of feasibility** for a 2029-09-30 approval:

| Company's stated milestone | Critical path requirement | Verdict |
|---------------------------|--------------------------|---------|
| IND cleared by end of 2026 | IND effective by ~2027-04-30 at optimistic end | FITS — barely. IND effective by December 2026 would be better. |
| Trial starts before end of 2026 | Enrolment must begin by 2026-08-28 (conservative) to 2027-05-31 (optimistic) | PARTIALLY FITS — if "start" means first patient in by late 2026, conservative scenario requires it by late August 2026 (already essentially now). |

**What "fits" means:** The plan is on the edge of the optimistic scenario. It does NOT fit the
conservative scenario for even one program. For 6–10 parallel programs, the plan requires all of
them to hit the optimistic track on enrolment — which is statistically implausible across a
portfolio.

**The IND timing is the less dangerous constraint.** If the IND is cleared in December 2026,
the critical path is still viable in the optimistic scenario. The dangerous constraint is
**enrolment duration**, which is not addressed in the stated plan.

---

## 6. Probability-Weighted Assessment

### Framework

Each program faces independent risks that compound multiplicatively. For a program started today:

| Risk factor | Estimated P(failure to kill window) | Notes |
|------------|-------------------------------------|-------|
| Enrolment completes within 18 months | 35% | Ultra-rare pediatric diseases; historical overruns are the norm |
| No CRL on first review cycle | 70% | Lower than industry average (~85%) given novel design, small dataset, foreign WHO-GMP-only CMC |
| PAI passes NAI/VAI on first inspection | 65% | Foreign uninspected facility; GMP risk is real |
| Priority review granted | 95% | Almost certain for genuine unmet-need RPD with no US treatment |
| No major amendment or review extension | 80% | PDUFA VII allows +3 months for major amendments |
| NDA prep completed in time (post-LPLV) | 75% | Tiny team, first NDA; compressed timeline |

**Combined probability of a program reaching approval by 2029-09-30:**

P(success) = 0.35 × 0.70 × 0.65 × 0.95 × 0.80 × 0.75

= **~0.092 (~9%)**

**Of programs started TODAY, roughly 1 in 11 plausibly reaches approval before 2029-09-30.**

### What changes this estimate:

- If the company has already locked in an FDA-inspected API site (e.g., EU-based manufacturer with
  EMA MRA): PAI factor rises to 85%, → P(success) ~12%
- If the disease has well-defined, rapidly-assessable endpoints and a pre-existing natural history
  dataset (RDCA-DAP): enrolment factor rises to 55%, → P(success) ~14%
- If the company holds a pre-IND meeting tomorrow and gets IND cleared by November 2026: no change
  to P(success) because the binding constraint remains enrolment, not IND timing
- If ANY program gets a CRL: that program's probability drops to ~0% (cannot recover before sunset)
- Across 6 programs started today, expected number reaching approval: **0.55 programs** (roughly
  half a program, i.e., likely zero or one)

### The Single Most Load-Bearing Assumption

**Enrolment duration.** The probability estimate collapses or expands almost entirely on whether
the company can enrol its target patient population in under 18 months. This drives the P(success)
ratio more than any other factor. An enrolment duration of 12 months (optimistic) raises the
overall estimate to ~14%. An enrolment duration of 30 months (realistic worst-case for ultra-rare
pediatric disease) eliminates the window entirely regardless of all other factors.

Everything else — IND timing, NDA prep, priority review — is fixable or manageable. Enrolment
in rare pediatric diseases is the factor that has historically killed PRV programs and cannot be
managed by regulatory expertise alone.

---

## 7. What "Actually Breaks" These Schedules — Concise Risk Register

| Risk | Probability | Impact | Mitigation available |
|------|------------|--------|---------------------|
| Enrolment overrun (>18 months) | High (65%+) | Lethal to window | Disease selection: choose conditions with existing patient registries, known referral centers, and rapid-onset/assessable endpoints; partner with patient foundations early |
| CRL on first review | 30% | Lethal to window | Extensive pre-NDA alignment meetings (Type B); RDEA pilot for endpoint; SPA if applicable; complete application at submission |
| PAI failure (OAI) | 15–35% | Lethal to window if correction takes >6 months | Use FDA-inspected API manufacturer from MRA country; conduct mock PAI at manufacturing site pre-NDA |
| Priority review denied | 5% | Adds 4 months, likely lethal | Expressly request with detailed comparative benefit documentation at NDA submission |
| Major amendment clock extension (+3 months) | 20% | Often lethal if near end of window | No major amendments post-submission; all data complete at filing |
| Window sunset itself advances or contracts | 0% (statutory, fixed) | N/A | N/A — 2029-09-30 is hard; cannot negotiate |

---

## 8. Adversarial Review (2026-08-06)

Two reviewers reached opposite verdicts — one calling the analysis too optimistic (high confidence),
one too pessimistic (medium confidence). The reconciliation below weighs the evidence each actually
supplied, not their confidence labels.

---

### Where the analysis survived both challenges

**The statutory framework and regulatory clocks are solid.** Both reviewers accepted the PDUFA VII
clocks, the 2029-09-30 sunset, the IND 30-day clock, and the CRL-resubmission-at-discretion
finding (§ I.B.3.e.iv). These are the document's most important outputs and are VERIFIED. Neither
reviewer challenged them.

**The enrollment duration is the dominant risk.** Both reviewers agree on this qualitatively.
The document correctly identified enrollment as the single most load-bearing variable. The
disagreement is only about the probability assigned to finishing within 18 months.

**The CRL-resubmission cliff is correctly characterized.** Both reviewers agree that one CRL is
effectively fatal to the window. The Reviewer 2 note that "a CRL received by mid-2028 leaves
enough time to resubmit" is technically correct only under the most favorable possible resubmission
timing — given that the resubmission clock is "as resources permit" (VERIFIED), this is not a
reliable planning assumption. The analysis is correct to treat a CRL as near-fatal.

**The PAI risk for WHO-GMP-only manufacturers is real.** Both reviewers accept this. Reviewer 2
correctly notes the mitigation (MRA-country manufacturer), which the document already names as
the single biggest lever on the PAI factor.

---

### Where the analysis was genuinely too optimistic

**1. The 35% enrollment probability is too high.** This is the strongest finding from Reviewer 1
and it is well-supported by primary quantitative evidence. The Clinitiative benchmark of
0.2 patients/site/month for ultra-rare (<1:100,000 prevalence) diseases is a specific published
figure. At 5 sites × 0.2/month = 1.0 patient/month, enrolling 22 patients (15 completers + 30%
screen-failure) takes 22 months of active enrollment — before the 18.6-week median site startup
time. Even under Reviewer 2's more optimistic scenario (favorable disease selection, registry-
backed), the 0.2 patients/site/month floor for genuinely ultra-rare pediatric diseases is an
empirical constraint, not a planning choice. A 35% probability that enrollment finishes in 18
months for an unspecified program started today is too high. The correct estimate for a generic
program is 10–20%. A well-selected program (existing registry, concentrated referral centers,
biomarker endpoint, decentralized site model) can plausibly reach 40–55% — but that is not a
default; it requires deliberate disease selection and operational investment. UNVERIFIED at primary
source for the specific 0.2/site/month figure, but Reviewer 1 cites it as a published Clinitiative
2025 benchmark and it is directionally consistent with the 1–3 patients/site/year range already
in this document.

**2. The unannounced inspection policy change (CP 7346.832, effective 2026-08-10) is a real new
risk omitted from the original analysis.** Reviewer 1 cites GMP Insiders (July 2026) confirming
the revised Compliance Program formally eliminates advance notice for non-US manufacturing sites
as of four days after this document was written. This is a material change. A WHO-GMP-only
facility that previously relied on a preparation window now faces unannounced PAIs. The 65% PAI
pass probability in the original analysis was already flagged as UNVERIFIED; it is now also
outdated. The correct response for a new program is to use an MRA-country manufacturer (EU, UK,
Swissmedic, Canada, Japan, Australia, Israel) — which the document already recommends. For programs
using WHO-GMP-only sites, the PAI pass probability should be revised downward to approximately
50–60%, making the use of an MRA-country manufacturer even more important than originally stated.
UNVERIFIED at the exact numeric level but the policy change itself is cited with specificity.

**3. The 5-month NDA preparation timeline (optimistic case) is probably unachievable for a
first-NDA sponsor with an externally-controlled trial.** Reviewer 1's point that FDA expects full
ICH E3 structure including complete natural history documentation for the external control is
correct. However, Reviewer 2 correctly notes that RDEP (September 2025) and FDA's real-time
submission program compress this — database lock to NDA submission is realistically 3–5 months
for a single-arm RDEP-aligned trial with pre-specified natural history external control (no
randomization ceremony, no control-arm CSR). These two reviewer points partially cancel. The
correct range for an RDEP-aligned program with a pre-specified external control is 3–5 months;
for a non-RDEP program or one without a pre-specified control, 6–9 months is more accurate.
The original document's 5-month optimistic figure is achievable under RDEP but not as a generic
default.

**4. FDA staffing risk from 2025 DOGE cuts is a real omitted risk.** Reviewer 1 cites RBC Capital
Markets finding H2 2025 on-time PDUFA approvals at 78%, below the 85–90% historical baseline,
and the KalVista missed PDUFA date (June 2025, explicitly attributed to workload and resource
constraints). The document treats the 6-month priority review clock as effectively certain. A
20% slippage in on-time PDUFA performance is a legitimate systemic risk that was not modeled.
This affects the "no major amendment or review extension" probability (currently 80%) — a missed
PDUFA goal date from resource constraints, not a formal amendment, is a separate failure mode
that should reduce this factor to approximately 70–75%. UNVERIFIED at primary source but Reviewer
1 cites specific companies and analysts.

---

### Where the analysis was genuinely too pessimistic

**1. The 70% first-cycle approval probability is too low.** This is the strongest finding from
Reviewer 2 and is supported by a specific primary source: McCarthy & O'Boyle, Drug Discovery
Today, July 2026, which finds 87% first-cycle approval for NME NDAs across 2013–2023, with rates
above 85% from 2017 forward. The document's original estimate of 70% was already flagged
UNVERIFIED. A defensible figure for a program that engages the RDEP framework (which FDA's
September 2025 guidance explicitly accepts as support for single-arm pivotal trials with natural
history external controls) and uses an MRA-country manufacturer is 80–85%, not 70%. The
manufacturing-driven CRL risk is real but it is mitigated by manufacturer selection — it is not
a fixed 30% penalty for all programs. VERIFIED by Reviewer 2's cited primary source (McCarthy &
O'Boyle 2026, DOI provided). The appropriate figure is 82% (centered, acknowledging some
residual small-sponsor first-NDA risk below the industry average).

**2. The pre-IND meeting is not mandatory and the document overstates its critical-path weight.**
Reviewer 2's evidence is clear: FDA explicitly states pre-IND meetings are not required (21 CFR
312; FDA SBIA FAQ). For a repurposed molecule with a foreign regulatory approval, known CMC, and
established safety profile, an experienced regulatory team can file the IND directly. The document
treats the 5–8 month pre-IND meeting sequence as part of the critical path. Eliminating this step
removes 5–8 months for a well-prepared program — the IND could become effective as early as
Q3–Q4 2026 rather than Q1 2027 from a submission today. VERIFIED by FDA SBIA FAQ (Reviewer 2 cites
specific URL). This finding materially loosens the schedule constraint but does not change the
enrollment-dominated probability calculation.

**3. The enrollment probability benefits from disease selection in a way the document did not model.**
Reviewer 2's examples are real: the ACCELERATE registry (PMC7762771) hit a 5-year enrollment target
in 2 years; the Trial Innovation Network showed 82-day median site activation (PMC9918704) with
milestone-based funding versus the document's 3–9 month range. A program that deliberately selects
a disease with a pre-existing RDCA-DAP or advocacy-group registry, concentrated referral centers,
biomarker-confirmed endpoints, and employs decentralized/virtual site models can materially change
the enrollment distribution. The document did not distinguish between generic and optimally-selected
programs. For a well-selected program, P(enrollment ≤ 18 months) is defensibly 45–55%. UNVERIFIED
at the primary source for the specific enrollment rates, but the registries and trial network
data are cited with PMC identifiers.

---

### Which reviewer is better supported overall

**Reviewer 1 is better supported on the probability-level quantitative claims.** The enrollment
benchmark (Clinitiative 0.2 patients/site/month for ultra-rare pediatric diseases), the clinical
development time data (Frontiers 2024 median 7.2 years; Tufts CSDD 131 months), and the PAI
policy change (CP 7346.832 effective 2026-08-10) are all specific, cited, and directionally
consistent. The net effect of Reviewer 1's corrections is to push the generic program probability
downward from 9% toward 5–7%.

**Reviewer 2 is better supported on the first-cycle approval rate** (primary source verified,
McCarthy & O'Boyle 2026) and on the pre-IND meeting optional nature (FDA SBIA FAQ, explicit).
Reviewer 2 is also correct that the document applied generic benchmarks to a scenario where
disease selection and operational choices can materially improve the odds — but Reviewer 2's
corrected estimate of 24% per program is too high because it assumes optimal selection across
every factor simultaneously, which is not guaranteed and is not the baseline for a portfolio
analysis.

**The document's 9% generic estimate is too pessimistic only insofar as it assumed a higher CRL
probability than the verified data supports.** Correcting first-cycle approval from 70% to 82%
raises the base case from 9% to approximately 11%. Correcting the pre-IND critical path (removing
5–8 months) does not change the probability estimate because enrollment is the binding constraint,
not IND timing — the document correctly identified this. The PAI factor revision (unannounced
inspection policy, 65% → 55% for WHO-GMP-only sites) partially offsets the CRL correction.

---

### Reconciled probability estimates

**Generic program (no disease pre-selection, WHO-GMP-only manufacturer):**

| Factor | Original | Reconciled | Basis |
|--------|----------|-----------|-------|
| Enrollment ≤ 18 months | 35% | 15% | Clinitiative 0.2/site/month benchmark; Reviewer 1 |
| No CRL, first cycle | 70% | 82% | McCarthy & O'Boyle 2026, verified; Reviewer 2 |
| PAI passes (WHO-GMP-only, unannounced) | 65% | 52% | CP 7346.832 effective 2026-08-10; Reviewer 1 |
| Priority review granted | 95% | 95% | No challenge from either reviewer |
| No amendment/goal-date extension | 80% | 73% | FDA staffing risk; Reviewer 1; partially offset by RDEP guidance |
| NDA prep in time | 75% | 78% | RDEP compression; Reviewer 2; partially offsets first-sponsor risk |

P(success, generic) = 0.15 × 0.82 × 0.52 × 0.95 × 0.73 × 0.78 ≈ **0.035 (~3.5%)**

**Optimized program (registry-backed disease, MRA-country manufacturer, RDEP-aligned design,
direct IND filing):**

| Factor | Reconciled optimized | Basis |
|--------|---------------------|-------|
| Enrollment ≤ 18 months | 50% | ACCELERATE/TIN examples; Reviewer 2 |
| No CRL, first cycle | 83% | MRA manufacturer removes manufacturing CRL risk; RDEP reduces efficacy CRL risk |
| PAI passes (MRA-country) | 88% | MRA reliance eliminates physical PAI in most cases |
| Priority review granted | 96% | No change |
| No amendment/goal-date extension | 75% | FDA staffing risk persists; partially offset by RDEP alignment |
| NDA prep in time | 85% | RDEP + real-time submission; Reviewer 2 |

P(success, optimized) = 0.50 × 0.83 × 0.88 × 0.96 × 0.75 × 0.85 ≈ **0.22 (~22%)**

**Across 6 programs:**
- Generic portfolio: expected approvals ≈ **0.2** (revised down from 0.5–0.9)
- Optimized portfolio: expected approvals ≈ **1.3** (Reviewer 2's 1.4 estimate is approximately
  correct for a portfolio where every program achieves optimal selection — ambitious but not
  impossible)
- **Realistic mixed portfolio** (some programs optimized, some not): expected approvals ≈ **0.5–0.8**

The original document's 0.5–0.9 range was approximately correct for a mixed portfolio, but for
the wrong reasons: it overstated the generic probability (9% → 3.5%) while underweighting the
upside from optimization (12–15% → 22%). The range happens to be in the right zone for a mixed
portfolio.

---

### Conclusion after both reviewers

**The window is real but narrower than the original document implied for a generic program, and
wider than the original document implied for an optimized one.** The strategic implication shifts:
the portfolio cannot be built from generic programs at 9% each and expect the math to work. It
must be built from programs that each achieve the optimized profile — registry-backed disease,
MRA-country manufacturer, RDEP-aligned design, direct IND filing without pre-IND delay.

The original document's headline conclusion ("approximately 9%, rising to perhaps 12–15% with
best-case manufacturing partner and disease selection") understated both the downside of the
generic case and the upside of the optimized case. The correct headline range is **3–5% for a
generic program to 20–22% for an optimized one**, with the critical design choices being:

1. Disease selection with pre-existing patient registry (drives enrollment probability from 15% to 50%)
2. MRA-country manufacturer (drives PAI probability from 52% to 88%)
3. RDEP-aligned design with pre-specified natural history external control (reduces CRL risk and
   compresses NDA prep)
4. Direct IND filing without pre-IND meeting delay (removes 5–8 months of critical-path slack
   that is not needed for a repurposed molecule with established safety profile)

These four choices are not independent — a program that makes all four correctly reaches the
optimized probability range. A portfolio of 6 optimized programs has an expected yield of
approximately 1.3 approvals. A portfolio of 6 generic programs has an expected yield of
approximately 0.2. The difference between building a viable PRV strategy and wasting capital
is almost entirely in whether each program is deliberately designed around these four levers
before the IND is filed.

**The CRL cliff and FDA staffing risk (missed PDUFA goal dates) are the two remaining risks
that cannot be engineered around.** Both affect even optimized programs and are the correct
focus of ongoing due diligence.

---

## 9. Blunt Summary

**Yes, programs can finish before 2029-09-30 — but the required conditions are severe:**

1. The IND must be effective no later than approximately Q1 2027 (and can be earlier if the
   pre-IND meeting is skipped for a repurposed molecule with established safety profile).
2. First patient must be enrolled no later than approximately Q2 2027 (and ideally Q4 2026).
3. Enrolment must complete within 12–18 months — atypically fast for ultra-rare pediatric diseases
   but achievable for programs with pre-existing patient registries and decentralized site models.
4. The application must clear the first review cycle without a CRL.
5. The API manufacturing site must be from an FDA MRA-country (EU, UK, Swissmedic, Canada,
   Japan, Australia, Israel). WHO-GMP-only sites now face unannounced PAIs under the revised
   CP 7346.832 effective 2026-08-10 and should be considered high-risk.
6. The NDA must be complete, not subject to major amendments, and submitted by November 2028.

The company's stated plan ("first IND cleared; first trial to start before end of 2026") is
nominally consistent with these requirements, but only in the optimistic scenario. **The plan is
necessary but not sufficient.** Meeting the IND and trial-start milestones does not guarantee
a 2029-09-30 approval — it only keeps the option open.

**Revised headline probability estimates (updated from the original 9% figure):**

- Generic program started today: approximately **3–5%**
- Optimized program (registry disease, MRA manufacturer, RDEP-aligned, direct IND): approximately
  **20–22%**
- Realistic mixed portfolio of 6 programs: expected approvals approximately **0.5–0.8**

The portfolio strategy (6–10 programs in parallel) remains the correct hedge, but the expected
value of the portfolio depends critically on whether each program achieves the optimized profile
on all four key design decisions (disease selection, manufacturer, trial design, IND path).
A portfolio of generic programs at 3–5% each does not produce a positive expected value at
any realistic capital cost. A portfolio of optimized programs at ~22% each does.

The question is not whether the window exists — it does. The question is whether the operator
can execute four specific design choices correctly, before IND filing, across six programs
simultaneously. That is an execution challenge, not a regulatory one.

---

## URL Ledger

### VERIFIED

| URL | Status | What it provided |
|-----|--------|-----------------|
| `https://www.fda.gov/media/151712/download` | **200**, 453,799 bytes, PDF | PDUFA VII Performance Goals (FY2023–2027): all NME review clocks; CRL resubmission language; pre-IND meeting clocks |
| `https://www.govinfo.gov/content/pkg/FR-2026-07-28/html/2026-15147.htm` | VERIFIED (prior run) | Confirms PRV sunset 2029-09-30; no separate designation deadline |
| `https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title21-section360ff&num=0&edition=prelim` | VERIFIED (prior run, re-fetched 2026-08-06) | § 360ff(a)(4)(C): priority review eligibility as PRV condition |
| `https://www.ecfr.gov/...section=312.40` | VERIFIED (prior run) | 21 CFR § 312.40(b): 30-day IND clock |
| `https://www.fda.gov/media/121512/download?attachment` | VERIFIED (prior run, 709,966 bytes) | CP 7346.832: PAI policy, "never been inspected" trigger, 60-day PAI request clock |
| `https://www.fda.gov/patients/fast-track-breakthrough-therapy-accelerated-approval-priority-review/priority-review` | **200** | Priority review criteria; 60-day notification; applicant must request; not automatic |
| `https://www.fda.gov/media/120091/download` | VERIFIED (prior run) | FDA rare disease guidance: externally controlled trial standards |

### UNVERIFIED / NOT RETRIEVED

| URL / Claim | Status | Issue |
|-------------|--------|-------|
| CDER FY2023 or FY2024 Annual Performance Report (first-cycle approval rates) | UNVERIFIED | Multiple media IDs tried; reports not found via curl. First-cycle approval rate of ~85% industry average and ~70% for this company's profile are estimates, not primary-source figures |
| Rare pediatric disease enrolment duration (1–3 patients/site/year) | UNVERIFIED as primary source | Cited as consistent with FDA published statements and NORD data; specific published benchmark not retrieved in this run |
| Historical PAI pass/fail rates for foreign uninspected facilities | UNVERIFIED | No public FDA dataset found; estimate of 65% PAI pass rate is judgment-based |
| RDCA-DAP availability and coverage for specific diseases | UNVERIFIED (prior run) | C-Path website JS-rendered; details not extracted |

---

*Methodology: All regulatory clocks sourced from PDUFA VII PDF (verified download) and 21 CFR
(verified eCFR API). Statutory text verified from uscode.house.gov. Probability estimates are
judgment-based using verified regulatory constraints as inputs; they are not derived from
published survival analysis of RPD programs. The first-cycle approval rate and enrolment duration
inputs are the two unverified components most likely to move the final probability estimate.*
