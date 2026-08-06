# Recruitment Feasibility & Trial Cost Stress-Test
## Can 6–10 Simultaneous Rare Pediatric Trials Be Recruited and Run for $300–400k Each?

**Research date:** 2026-08-06. ClinicalTrials.gov API v2 queried live (data timestamp 2026-08-05T09:00:06). All ClinicalTrials.gov figures are measured, not recalled. Published benchmarks cited with URLs. VERIFIED / UNVERIFIED marked per methodology.

---

## 1. The Enrollment Funnel — Starting With Prevalence

### How many patients are actually available after eligibility filtering?

The disease prevalence math from source 10 (newborn screening) and source 03 (Orphanet) gives the total diagnosed US population. For a condition at 1:100,000 live births with 5-year life expectancy (untreated, severe pediatric), the survival-weighted prevalent US population is approximately **~180 patients** (3,600,000 births × 1/100,000 × 5 years). For a condition with 25-year treated life expectancy: **~900 patients**. The NewSTEPs 2018–2020 data shows actual case rates: MPS I at 0.14/10,000 implies ~48 new US diagnoses per year; propionic acidemia at 0.06/10,000 implies ~22. These are the diseases with a few hundred diagnosed US patients.

The funnel from **total diagnosed US population** to **realistically enrollable** passes through six successive cuts:

| Filter | Fraction Surviving | Basis |
|---|---|---|
| Age eligibility (e.g., 2–17 years) | ~0.40–0.60 | 5-to-25-year survival spread; only the window-eligible birth cohorts |
| Severity/stage criteria | 0.50–0.70 | Moderate/severe phenotype required; milder variants excluded |
| No prior approved therapy or stable on SOC (SOC exclusion) | 0.60–0.80 | Patients already on ERT, gene therapy, substrate reduction are excluded if the drug interacts |
| Geographic concentration and family travel burden | 0.30–0.50 | 5–8 academic centers hold >80% of known patients; families outside 150-mile radius often cannot travel |
| Competing trial enrollment | 0.70–0.90 | Each RDCRN consortium runs multiple concurrent studies; key patients are over-solicited |
| Parental consent / willingness | 0.60–0.80 | Estimated from advocacy group reports; fear of unknown, logistics, and distance all reduce consent rates |

**Compound product of all six:** 0.50 × 0.60 × 0.70 × 0.40 × 0.80 × 0.70 = **~0.047 to 0.14** of the diagnosed population.

**Applied to a disease with 300 diagnosed US patients:** 14 to 42 realistically enrollable patients. Targeting 20 patients for a trial means you need to approach essentially every known patient, and a single site refusing to participate or a slow consent rate collapses the trial below the floor of statistical relevance.

**This figure — 15–40% of the diagnosed population at best — is the single most load-bearing number in this analysis.** The $300–400k cost question is secondary to whether enrollment is physically achievable.

---

## 2. Measured ClinicalTrials.gov Benchmarks

All data queried live from ClinicalTrials.gov API v2 (`https://clinicaltrials.gov/api/v2`, data timestamp 2026-08-05T09:00:06). VERIFIED.

### 2.1 Enrollment Size — Small Rare Disease Trials

**Query:** Completed interventional LSD trials (mucopolysaccharidosis OR gaucher OR fabry), ACTUAL enrollment, all sponsors.
- **57 trials with ACTUAL enrollment data**
- **Median N: 19 patients**
- **56% had N ≤ 20; 70% had N ≤ 30**
- N range: 4–886 (886 is a stem-cell transplant registry study; the drug-intervention tail is uniformly small)

**Query:** Batten disease / NCL interventional trials, all statuses:
- 26 interventional trials identified
- Completed with ACTUAL enrollment: N ranges from 6 to 135 (the 135 is a stem-cell transplant trial, not drug-specific)
- Drug-specific trials: N = 6, 10, 12, 13, 14, 19, 23, 24 patients
- **Median duration (start to primary completion): 29 months** across LSD interventional trials
- 42% completed in <24 months; 60% in <36 months

### 2.2 Enrollment Duration for Ultra-Rare Disease Trials

**Measured from NCL/Batten disease interventional completed trials** (n=8 drug trials, excluding stem cell transplant registries):

| Trial | N | Sites | Total Duration | Pts/Month Overall |
|---|---|---|---|---|
| HuCNS-SC infantile NCL (NCT00337636) | 6 | 1 | 33 mo | 0.182 |
| Gene transfer CLN2 (NCT00151216) | 10 | 1 | 180 mo | 0.056 |
| RhAAV10 LINCL (NCT01161576) | 12 | 1 | 65 mo | 0.185 |
| Cellcept JNCL (NCT01399047) | 19 | 1 | 52 mo | 0.365 |
| Gene therapy CLN6 (NCT02725580) | 13 | 1 | 77 mo | 0.169 |
| AAVRh.10 LNCL (NCT01414985) | 8 | 1 | 67 mo | 0.119 |
| **Cerliponase alfa CLN2 (NCT01907087)** | **24** | **5** | **26 mo** | **0.923** |
| Open-label CLN5 (NCT05174039) | 6 | 1 | 26 mo | 0.231 |

**Median: 0.185 patients/month for the entire study.** The cerliponase alfa outlier (0.923/month) reflects BioMarin's international multi-site network across Nationwide Children's, Hamburg, Rome, and two London centers — a coordination infrastructure a bootstrapped sponsor does not have.

**88% of NCL drug trials ran at a single site.** This is because CLN2 disease (prevalence <1:100,000) concentrates its patient population at 3–5 expert centers globally, and those centers are the only investigators with the equipment and experience to run the trial.

**Enrollment duration projection:** At the typical 0.185 pts/month, enrolling 20 patients takes **108 months (9 years)**. This is not a planning target — it is evidence that NCL trials do not target N=20. They target N=6–24 because that IS the available population, and they use natural history controls to make the statistical case.

**The correct lesson:** target N equal to 10–15% of the total diagnosed US population, use a natural history control, and design for 24–48 months of active enrollment. Do not try to power a trial conventionally with a random-effects placebo arm.

### 2.3 Per-Site Per-Month Enrollment Rate

**Query:** Completed LSD interventional trials with actual enrollment AND reported site locations (n=11 with complete data):

| Trial | N | Sites | Duration | Pts/Site | Pts/Site/Month |
|---|---|---|---|---|---|
| MPS II ERT (NCT00069641) | 96 | 9 | 18 mo | 10.7 | 0.593 |
| AT2101 Gaucher extension (NCT00813865) | 8 | 4 | 36 mo | 2.0 | 0.056 |
| Phase 2 MPS (NCT05758922) | 13 | 3 | 12 mo | 4.3 | 0.361 |
| JR-141 MPS II (NCT03568175) | 28 | 19 | 18 mo | 1.5 | 0.082 |
| Velaglucerase bone (NCT02574286) | 21 | 15 | 53 mo | 1.4 | 0.026 |
| Velaglucerase children (NCT01685216) | 7 | 5 | 30 mo | 1.4 | 0.047 |
| SHP611 MLD (NCT03771898) | 36 | 30 | 46 mo | 1.2 | 0.026 |
| Miglustat NPC China (NCT03910621) | 17 | 2 | 23 mo | 8.5 | 0.370 |
| AT1001 Fabry (NCT00304512) | 9 | 6 | 20 mo | 1.5 | 0.075 |

**Measured median: 0.080 patients per site per month** (LSD multi-site trials)
**Range: 0.026 to 0.593** (the outlier at 0.593 is MPS II which has the largest diagnosed population of all LSDs; bottom end reflects trials with 30 sites for 36 patients — excessive site dilution)

**Planning benchmark for ultra-rare diseases (N<200 diagnosed US patients):** 0.04–0.08 patients/site/month. This is the real operating number for a bootstrapped sponsor.

**Implication:** To enroll 20 patients in 24 months at 0.05 pts/site/month, you need 20/(24×0.05) = **17 active sites**. Activating 17 pediatric specialty sites requires:
- 17 separate site initiation agreements and payments
- 17 IRB submissions (or one central IRB + 17 local reliances — local reliance often takes 2–4 months per site even for central IRB studies)
- 17 principal investigators, each requiring protocol training, regulatory binder preparation, and ongoing monitoring
- 17 sets of pharmacy approvals and drug shipment authorizations

This is not a back-of-envelope constraint. It is the dominant logistical burden.

**Key finding for site planning:** 0.08 pts/site/month means to enroll 20 patients in 24 months you need 20/(24×0.08) = **10.4 active sites**. Opening 10 pediatric specialty sites costs $65,000–$100,000 in initiation alone, plus ~$350/patient/monitoring-visit per site visit. Site number is a direct cost multiplier — each site added is $10,000–$25,000 in overhead regardless of whether it enrolls anyone.

**Cerliponase alfa provides the existence proof** for what good looks like: 24 patients, 5 sites across 3 countries, 26 months, industry sponsor with existing investigator relationships at each site. A bootstrapped company replicating this needs the investigator relationships first, the capital second.

### 2.4 Trial Termination and Accrual Failure Rate

**Query:** Inborn errors of metabolism trials, all statuses:
- Completed: **1,838**
- Terminated: **223**
- Withdrawn: **125**
- **Overall attrition rate (terminated + withdrawn / completed + terminated + withdrawn): 15.9%** VERIFIED

From MPS terminated interventional trials (n=23 terminated interventional): **17% terminated primarily for slow accrual or lack of enrollment** (4/23 with explicit accrual language in WhyStopped; others reflect sponsor business decisions partly driven by slow enrollment).

From rare pediatric disease terminated trials (n=2 from specific query): **100% of terminations cited accrual failure** ("slow enrolment," "Slow accrual and as a result, a strategic business decision was made to…").

The measured accrual failure rate for rare pediatric trials — roughly **15–25% of trials that start** — is not a tail risk. It is a routine expected outcome for any sponsor that does not have pre-existing patient relationships.

**Published benchmark (UNVERIFIED — secondary source):** A commonly cited analysis estimates ~30% of rare disease trials fail to meet enrollment targets, compared to ~19% for all-disease trials. The ClinicalTrials.gov-measured 16% formal termination/withdrawal rate from IEM trials is a floor — many trials labeled "business decision" terminate because accrual failure made the program commercially unviable, even when enrollment is not cited as the proximate reason.

---

## 3. Cost Stress-Test — Bottom-Up for a 20-Patient Pediatric Trial

### 3.1 Cost Element By Element

For a **single-arm, 20-patient, pediatric Phase 2 interventional trial** (single-arm with external/historical control arm, academic sites, central IRB, one indication, one country):

| Line Item | Low Estimate | Mid Estimate | High Estimate | Basis |
|---|---|---|---|---|
| **Site initiation and management** | | | | |
| Site initiation (per site, 8–12 sites) | $5,000–$8,000 | $6,500 | $8,000 | Industry standard; academic sites charge less than community |
| Site management / monitoring (per site-visit, 3–5 per site) | $2,500 | $3,500 | $5,000 | CRO monitoring rates 2024–2025 |
| Subtotal sites (10 sites × $6,500 init + 10×4 visits×$3,500) | $205,000 | $305,000 | $450,000 | |
| **CRO / study coordination** | | | | |
| Full-service CRO for 20-patient rare pediatric study | $150,000 | $250,000 | $400,000 | Quoted ranges from 2022–2024 peer publications; see §3.2 |
| OR: fractional CRO / in-house coordinator only | $40,000 | $80,000 | $120,000 | Self-managed with part-time CRA, no full-service |
| **Central IRB** | | | | |
| Initial review + annual continuation | $8,000 | $15,000 | $25,000 | WCG, ADVARRA, or Copernicus flat-fee schedules (UNVERIFIED exact figures) |
| **Data management / EDC** | | | | |
| REDCap (academic hosted, no-cost) | $0 | $0 | $5,000 | REDCap is free for academic sites; NIH-sponsored |
| Commercial EDC (Medidata Rave, Veeva Vault) | $20,000 | $40,000 | $80,000 | Per-study setup + per-patient fees; published tender prices |
| **Biostatistics** | | | | |
| SAP, analysis, clinical study report | $15,000 | $30,000 | $60,000 | Academic biostatistics consulting rates |
| **Pharmacovigilance / safety reporting** | | | | |
| Medical monitor (part-time) + SAE processing | $10,000 | $25,000 | $50,000 | DSMB meetings add $5–10K |
| **Drug supply** | | | | |
| Off-patent generic (20 patients × treatment period) | $2,000 | $10,000 | $30,000 | API often <$100/patient if sourced directly; GMP formulation and packaging dominate |
| GMP formulation / packaging / release testing | $20,000 | $50,000 | $120,000 | Pediatric formulation (liquid or dispersible tablet) requires batch manufacture; single batch can be $30–80K |
| Drug labeling and IND management | $5,000 | $10,000 | $20,000 | |
| **Comparator / external control** | | | | |
| Natural history data pull (RDCA-DAP, registry) | $0 | $5,000 | $15,000 | RDCA-DAP is free; patient registry data requires DUA |
| Matched cohort analysis (biostatistics hours) | $8,000 | $15,000 | $25,000 | |
| **Insurance / indemnity** | | | | |
| Clinical trial insurance (sponsor-side) | $10,000 | $20,000 | $40,000 | Annual premium for a small rare disease trial; UNVERIFIED exact figure |
| **Family travel reimbursement** | | | | |
| 20 patients × 4–8 visits × $500–$1,500/visit | $40,000 | $80,000 | $160,000 | Transportation + lodging; pediatric rare disease visits are frequently multi-day |
| **Regulatory (IND, FDA meetings)** | | | | |
| IND filing preparation + Type B meetings | $15,000 | $30,000 | $60,000 | Regulatory consultant or counsel; FDA PDUFA fees waived for small sponsors under certain conditions |
| **Overhead / misc** | $20,000 | $40,000 | $80,000 | |

**TOTAL (self-managed CRO, academic sites, REDCap, single-arm):**
- **Floor (absolute minimum, everything goes right):** ~$350,000–$450,000
- **Mid realistic (partial CRO, 10 sites, central IRB):** ~$650,000–$850,000
- **Full-service CRO, 12+ sites, commercial EDC:** ~$1,000,000–$1,500,000+

**The $300–400k figure is below even the floor estimate for a properly conducted 20-patient trial with drug supply and family reimbursement included.** See §3.3 for the specific conditions under which it can be approached.

### 3.2 Published Per-Patient Cost Benchmarks

**Medidata Acorn AI / Benchmarks Industry Data (UNVERIFIED — widely cited but behind a login wall):** Per-patient costs in rare disease Phase 2: $35,000–$80,000 per patient. At 20 patients, that is $700,000–$1.6M. These figures are for commercial sponsors and include full CRO.

**GlobalData Pharma Intelligence 2023 (UNVERIFIED — secondary source):** Pediatric Phase 2 median per-patient cost across all diseases: ~$19,000–$24,000. Applied to rare disease with site startup costs spread over 20 patients: $20,000–$50,000 per patient.

**NIH-funded investigator-initiated trials (most relevant comparator):** Rare pediatric NIH grants for ~20-patient studies run $200,000–$600,000 in direct costs over 2–4 years. These exclude indirect costs (F&A, typically 50–60% overhead at academic centers) and drug manufacture. The sponsor here would not receive indirect costs but would pay for drug supply that NIH grants often avoid by using IND Exemptions or NIH-supplied agents.

**Bottom-up cross-check from RDCRN:** The RDCRN DMCC at Cincinnati Children's (source 12) provides regulatory and data management support to consortium investigators, which effectively transfers $80,000–$200,000 of trial infrastructure cost to a federal grant. This is not available to a commercial sponsor unless embedded in a consortium study. Consortium embedding is slower (18+ months to negotiate) and involves IP co-ownership questions.

**Most honest benchmark:** For a genuinely stripped-down single-arm 15–20 patient trial with an off-patent drug, academic-site investigators waiving fees, REDCap, central IRB, self-manufactured drug, and advocates facilitating recruitment, total all-in cost is approximately **$500,000–$800,000**. Getting below $500,000 requires multiple concessions simultaneously (academic PI absorbs monitoring, no family travel reimbursement, free registry data for external control, no CRO). Getting to $300,000 requires academic sponsor status — i.e., the company would need to be embedded in an academic institution, which defeats the commercial structure.

### 3.3 Conditions Under Which $300–400k Is Plausible (And Where It Is Not)

**Achievable only if ALL of the following hold simultaneously:**
1. The drug is available as a generic tablet or liquid at pennies per dose with no custom formulation needed
2. The PI is an academic investigator who waives site fees and absorbs monitoring into their lab budget
3. The IRB is already familiar with the disease and approves in <60 days (academic IRB, not requiring central IRB fees)
4. REDCap is used (free), the academic medical center hosts it, and data management is handled by the PI's coordinator
5. No family travel reimbursement is offered (patients live near the single site, or advocates fund travel separately)
6. A single site enrolls all 20 patients (eliminating multi-site initiation costs entirely)
7. A natural history control arm exists in a public database (RDCA-DAP or RDCRN registry) requiring no paid data acquisition
8. The company's internal team handles all regulatory work (IND writing, FDA meeting prep) without outside consultants
9. No DSMB is required (or a volunteer DSMB is assembled)
10. Insurance is waived or minimal (investigator-initiated IND, academic center's institutional policy covers)

**This is the investigator-initiated single-site compassionate-use-adjacent model**, not a multi-site sponsor-initiated Phase 2. It can work — but it produces evidence that FDA will score as suggestive, not confirmatory, for a 505(b)(1) NDA.

**Where $300–400k is definitively not achievable:**
- Any trial requiring pediatric formulation development from scratch (+$50–150k minimum)
- Multi-site designs (>2 sites adds $100k+ in initiation and monitoring alone)
- Any disease where patients are geographically dispersed and travel reimbursement is ethically required
- Trials where FDA has required a REMS or a DSMB with independent chair
- Programs where the drug's supply chain does not already exist (manufacturing a small batch of an off-patent API in pediatric dosage form costs $30–80k for a single run)

---

## 4. Trial Design Approaches That Genuinely Cut Cost and Time

### 4.1 Single-Arm With External/Historical Control

**Mechanism:** Replace the concurrent control arm with a matched historical cohort from a natural history study or registry. Eliminates the need to randomize and enroll a control arm (which would double N and duration).

**FDA receptiveness:** Formally endorsed in FDA's 2019 guidance *"Rare Diseases: Common Issues in Drug Development"* (dead link at fda.gov as of 2026-08-06; referenced in RDEA FR materials) and the RDEA pilot program. FDA has approved drugs on single-arm data with external controls in rare diseases: **cerliponase alfa** (NCL/CLN2, approved April 2017 on N=24 single-arm with natural history control), nusinersen (SMA, approved December 2016), volanesorsen (familial chylomicronemia syndrome), and several lysosomal storage disease drugs. The critical requirement is that the natural history is **well-characterized and the external control is clearly comparable** — which requires a pre-existing natural history study, often with the same outcome measures.

**Cost savings:** Eliminates 50% of the enrolled patients and proportionally reduces site costs. More importantly, removes the ethical and logistical burden of withholding treatment from a control arm in a severe pediatric disease, which often makes randomization impossible anyway.

**Risk:** FDA can refuse to accept historical controls if the treated population differs systematically from the historical cohort, or if outcome measure definitions diverged over time. The PRV-focused programs most likely to succeed with this design are those where the disease's natural history is rapidly fatal and consistent (infantile-onset conditions, not variable-penetrance adult-onset forms).

### 4.2 Registry-Embedded Trials

**Mechanism:** Conduct the trial within an existing patient registry (e.g., an RDCRN consortium registry or a NORD IAMRARE registry). Registry already has enrolled patients, collected baseline data, and obtained consent for future contact. The trial adds a treatment arm to an ongoing registry observation.

**Cost savings:** Eliminates site initiation at the registry site (~$8–15k), pre-existing baseline data reduces visit burden, and existing advocacy relationships accelerate consent. Estimated savings: $100,000–$200,000 on a 20-patient trial.

**Reality check:** A bootstrapped sponsor cannot simply embed in an RDCRN registry. The sponsor must negotiate with the consortium PI, which involves IP sharing terms and can take 12–18 months. IAMRARE registries are controlled by patient organizations, not companies. The realistic path is to co-design the study with the patient organization and propose it to the consortium — which positions the trial as an academic study with commercial co-sponsorship, raising additional IP and rights questions.

### 4.3 Bayesian Borrowing

**Mechanism:** Use informative prior distributions derived from natural history or prior clinical data to reduce the required sample size. For a disease where the event rate in untreated patients is well-established, Bayesian methods can allow FDA approval on 10–12 patients with appropriate posterior probability thresholds.

**FDA receptiveness:** FDA has approved Bayesian borrowing in pediatric extrapolation (using adult data to support pediatric efficacy), and its 2023 guidance on Bayesian statistics in clinical trials confirms that this is acceptable. For rare pediatric diseases with no prior data, the approach is less proven but FDA's RDEA pilot explicitly invites discussion of novel statistical approaches.

**Practical limit:** Bayesian borrowing requires a credible prior — which requires existing natural history data. The approach is powerful when data exists (Friedreich ataxia, Pompe disease, Batten disease registries all have rich longitudinal data in RDCA-DAP). For a disease with <10 published cases, there is no prior to borrow from.

**Cost savings from N reduction:** Going from N=20 to N=12 via Bayesian borrowing saves approximately $200,000–$400,000 in per-patient site costs and drug supply, but adds $50,000–$100,000 in biostatistics complexity. Net savings: $150,000–$300,000 for a well-resourced statistical approach.

### 4.4 RDEA Pilot Program — FDA-Endorsed Early Engagement

**VERIFIED** from Federal Register 87 FR 65085–65088 (2022-10-27), Docket FDA-2022-N-2480:

The RDEA Pilot Meeting Program was established under PDUFA VII (FY2023–2027). Key features:
- Sponsors with an active IND or pre-IND can apply (natural history study sponsors also eligible)
- Maximum **3 proposals admitted per year** (one per quarter FY2024–2027), maximum 1 in FY2023
- Up to **4 focused meetings** with CDER/CBER on efficacy endpoint development
- FDA advice is **non-binding** and does not guarantee approval
- Accepted proposals will be disclosed publicly as case studies (negotiated disclosure)
- **Preference given to endpoints with broad applicability and novel methodologies**

**Contact for CDER:** Mary Jo Salerno, Division of Rare Diseases and Medical Genetics, 240-402-0420
**Deadline structure:** Rolling quarterly submissions (Dec 31, Mar 31, Jun 30, Sep 30); FDA responds within 60 days

**Value to a bootstrapped sponsor:** The RDEA pilot provides 4 structured FDA meetings that would otherwise require Type B or Type C meeting requests — which cost $2M+ in PDUFA fees for a large sponsor but are *free for small businesses* under the Small Business PDUFA fee waiver. The real value is **reducing endpoint development risk** before the trial starts, not reducing cost directly. A company that designs its endpoint in alignment with FDA's thinking before spending $500k on a trial is a fundamentally different risk profile from one that spends first and discovers FDA's endpoint preference later.

**Limitation relevant to this company:** The RDEA pilot requires an active IND or at minimum a pre-IND on file. An IND requires a drug formulation, manufacturing data, and preliminary safety justification. Preparing a pre-IND package (animal tox, formulation characterization, proposed protocol) costs $50,000–$150,000 in regulatory consultants and nonclinical work before the first clinical dollar is spent.

---

## 5. Assessment: One Bootstrapped Sponsor Running 6–10 Simultaneous Programs

### 5.1 The Concurrent Program Constraint

Running 6–10 programs simultaneously is not primarily a money problem. It is a **management bandwidth and regulatory correspondence problem** that cannot be solved by money alone at this stage.

Each active IND program requires:
- A designated regulatory contact who responds to FDA information requests (FDA information requests must be answered within 10 business days)
- An active pharmacovigilance system capable of processing SAEs within 7 calendar days (expedited SAE reporting to FDA)
- Ongoing site monitoring (quarterly at minimum for recruiting sites)
- A data safety monitoring board or equivalent safety review mechanism
- Protocol amendment management (any change to an active IND requires FDA notification or amendment)
- An active supply chain for drug shipment to each active site

A team of 2–3 people cannot manage this for 6 simultaneous INDs without systematic errors. Large CROs (Covance, ICON, Parexel) manage multiple programs simultaneously because they have dedicated program managers, safety officers, and regulatory staff for each program. A bootstrapped company does not.

**Coordination overhead per active program (beyond direct trial costs):** $80,000–$150,000 per year in regulatory staff time, safety monitoring infrastructure, and communication overhead. For 6–10 programs: $480,000–$1,500,000 per year in overhead alone, before any trial activity.

### 5.2 The Site Relationship Constraint

Rare pediatric disease trials compete for attention from a small number of investigators at a small number of sites. The US has approximately:
- **46 NORD Centers of Excellence** (source 12) with rare disease expertise
- **23 NIH UDN sites** with undiagnosed disease workup capability
- **~15–20 major academic medical centers** with dedicated IEM metabolic clinics

These overlap substantially. The true universe of pediatric metabolic disease sites capable of running a clinical trial in a rare IEM is approximately **20–30 institutions nationally**.

Six to ten simultaneous programs targeting the same disease space will compete for investigator attention at these same 20–30 sites. An investigator at Boston Children's who is already running two RDCRN consortium studies and a sponsor-initiated Batten trial is not going to accept a seventh study from an unknown company with no existing relationship and an offer of $5,000 per patient — particularly when the RDCRN consortium provides IRB coverage, data management, and advocacy relationships that the bootstrapped sponsor cannot.

**Site relationship capital is not fungible and not purchasable with cash alone.** The investigators who run rare pediatric trials are chosen for their patient relationships — they know every family with a given diagnosis in their region. Building that relationship from scratch takes 12–24 months of scientific engagement, conference presence, and advocacy community credibility. Running it across 6–10 disease areas simultaneously from a bootstrapped company with no published track record is not feasible.

### 5.3 The Advocacy Relationship Constraint

For each rare pediatric indication, the patient advocacy organization is the primary patient-finding channel (source 12). Building the trust of a patient advocacy organization requires:
- Demonstrating genuine scientific expertise (publishing, presenting at advocacy conferences)
- Offering transparency about the PRV/commercial motive (families are sophisticated and will ask)
- Proposing data-sharing terms that benefit the disease community, not just the sponsor
- Sustained engagement over 12–18 months before families will consent

Six to ten parallel advocacy relationships, each requiring sustained attention from the company's scientific leadership, are not manageable for a team of 2–3 people.

### 5.4 Financial Reality

**With ~$180k raised and a cost floor of ~$500k per program:**

| Scenario | Capital Required | Gap at $180k |
|---|---|---|
| 6 programs × $500k each | $3,000,000 | $2,820,000 |
| 10 programs × $500k each | $5,000,000 | $4,820,000 |
| 1 program × $500k (lean) | $500,000 | $320,000 |
| 1 program × $300k (absolute minimum) | $300,000 | $120,000 |

The current $180k covers:
- Regulatory consulting for 1 pre-IND package (if lean): ~$40–80k
- Legal (corporate, IP, FDA counsel retainer): ~$30–50k
- 6–9 months of a founder's below-market salary: ~$50–80k
- Travel and advocacy conference presence for 1 disease: ~$15–20k
- Drug supply feasibility assessment (sourcing, GMP quote): ~$10–20k

This is **pre-IND work for one program**. It does not fund a trial.

---

## 6. Minimum Viable Version

### The honest minimum viable program

**One program, done properly, with the following structure:**

**Step 1 (months 1–12, cost ~$80–120k):**
- Select one disease where: (a) a well-characterized external natural history control exists in RDCA-DAP or a published registry; (b) the off-patent drug is available as a generic without custom formulation; (c) a single academic center PI is interested and willing to serve as IND holder (investigator-IND) or co-sponsor
- Engage the patient advocacy organization and propose a registry-embedded study design
- File a pre-IND package and request an RDEA pilot meeting slot
- Negotiate a contract with one academic site (RDCRN consortium site preferred — they already have IRB coverage, DSMB infrastructure, and patient registry access)

**Step 2 (months 12–24, cost ~$200–350k):**
- Obtain RPD designation (IND required; RPD designation itself has no direct cost)
- Open IND, activate one site, begin enrollment
- Target N=12–15 patients with Bayesian borrowing from the external control arm
- REDCap for data management (free at the academic site)
- Central IRB reliance from the academic site's IRB (avoids $15–25k central IRB fee)

**Step 3 (months 24–36, cost ~$100–150k):**
- Complete enrollment, lock database, analyze
- File NDA (505(b)(1) with natural history external control if the moiety has no prior US approval)
- If approved, claim PRV

**Realistic all-in cost for this minimum viable design: $400,000–$620,000** across 30–36 months, assuming the academic site absorbs a substantial fraction of monitoring costs into their NIH-funded infrastructure and the PI is willing to negotiate a below-market site fee in exchange for authorship and disease community recognition.

**The gap from $180k to $400k is $220k.** This is a feasible fundraising target from a single rare disease foundation grant, an NCATS SBIR (max $2M Phase 2), or a disease-specific nonprofit. NIH SBIR/STTR Phase 1 for rare disease clinical programs goes up to $300,000 for 6 months (Phase 1) and $2M+ for Phase 2.

---

## 7. Verdict

**Can 6–10 simultaneous programs be recruited?** No — not from a standing start with one team, $180k, and no prior investigator or advocacy relationships. The enrollment funnel leaves 15–40 enrollable patients per disease, requiring approach of essentially every diagnosed patient, which in turn requires deep trust with the advocacy community and PI network. That trust takes 12–24 months to build per disease. Building it for 6–10 diseases simultaneously, with a small team, is not feasible.

**Can one program be recruited?** Yes, if the disease is chosen carefully (established natural history, existing registry, single-center concentration of patients, willing academic PI). The RDCRN consortium site list from source 12 is the PI-sourcing map. The RDCA-DAP platform from source 13 is the external control arm database. The RDEA pilot program provides FDA engagement that de-risks the endpoint before the trial starts.

**Can a trial be run for $300–400k?** Not for a properly powered, multi-site, industry-sponsored Phase 2. For a single-site, academically embedded, investigator-IND study with external historical control and borrowed biostatistical analysis: yes, at the extreme low end ($350–450k all-in if drug formulation is trivial and site absorbs overhead). This is the investigator-initiated model, not the commercial sponsor model. The distinction matters for PRV: FDA appears to accept investigator-IND submissions for RPD designation and PRV purposes (per the SEZABY precedent), but the legal and IP structure for an investigator-IND producing a commercially actionable PRV has not been definitively established — this is a material legal risk, not a solvable detail.

**The authentic minimum viable version:** One program, $500k total, one academic site, Bayesian external control, N=12–15, investigator-IND with commercial co-sponsor structure. This is fundable from an SBIR Phase 2 + one disease foundation grant. It is executable by a 2–3 person company with the right academic partner. Six programs done thinly, sharing the same fixed overhead without adequate site relationships or advocacy trust, produces six failed accruals and no PRVs.

**Critical calendar constraint (updated after adversarial review):** The PRV program sunsets September 30, 2029. FDA approval — not NDA filing — must precede that date. From August 2026, that is 37 months to approval. Under priority review (6 months), NDA filing must occur by March 2029 — 31 months from today. The 30–36 month path to NDA *filing* described in Section 6 puts approval at February 2029 (optimistic, zero-slip) to February 2030 (realistic 36-month path), the latter being five months past sunset. The minimum viable version as structured in Section 6 is not PRV-viable under its own "realistic" schedule. A PRV-eligible single program requires either compressing Steps 1–2 to a combined 22–25 months (removing SBIR sequencing as the funding vehicle for trial execution) or accepting that the economic thesis does not depend on PRV proceeds. See §8 (Adversarial Review) for the full analysis.

---

## 8. Adversarial Review (2026-08-06)

Two reviewers challenged this document from opposite directions. This section adjudicates each disputed claim by the quality of the evidence each reviewer brought, not by splitting the difference.

---

### Where the Analysis Survived

**The 6–10 simultaneous program conclusion is correct and well-supported (both reviewers concede this).** The site relationship constraint (§5.2), the advocacy trust-building timeline (§5.3), and the $480k–$1.5M annual coordination overhead figure (§5.1) are not contested by either reviewer and are grounded in structural arithmetic that survives scrutiny. The multi-program case is properly pessimistic.

**The 15.9% IEM attrition rate is adequately supported.** R2 challenged this figure but conceded that their own ClinicalTrials.gov session returned only the first 100 API records and explicitly acknowledged "the 15.9% figure from the full dataset may still hold." The document uses the full verified IEM dataset (1,838 completed + 223 terminated + 125 withdrawn = 2,186 total; 348 attritions / 2,186 = 15.9% VERIFIED). R2's partial pull does not constitute a refutation. The 15% floor for rare pediatric accrual failure holds.

**The enrollment funnel structure and the individual filter categories are correct.** The six filters — age eligibility, severity, SOC exclusion, geography, competing trials, parental consent — are each individually defensible. The table's ranges are honest.

**The per-site per-month planning benchmark of 0.04–0.08 pts/site/month for US ultra-rare indications is adequately supported** by the measured LSD/IEM trial data, even after removing the three non-US trials identified by R1 (see below). The remaining US/EU benchmark pool still produces a median in the 0.05–0.08 range.

**The RDEA pilot's 3-slots-per-year constraint is real.** Both reviewers confirm this from the verified FR 87 FR 65085 text. R1 correctly identifies the document soft-pedals the competitive nature of the program. R2 does not rebut this. The constraint stands.

**The cost floor for a multi-site sponsor-initiated Phase 2 is correctly placed at $500k–$800k.** R2 argues that a single-site IIT-adjacent structure embedded in RDCRN infrastructure can approach $350–500k total. This does not contradict the document — §3.2 already states $500k–$800k as "most honest benchmark" and §6 projects $400k–$620k for the minimum viable single-site design. The dispute here is with the document's framing ("The $300–400k figure is below even the floor"), which is accurate for multi-site designs and acknowledged as achievable only under a specific conjunction of conditions in §3.3. The document is correct on the cost question.

---

### Where the Analysis Was Genuinely Too Optimistic

**1. The PRV sunset omission is a material analytical failure. VERDICT: R1 is correct. (VERIFIED)**

The document's Section 6 lays out a 30–36 month path to NDA filing and presents this as "minimum viable" without applying the PRV sunset date of 2029-09-30 to that schedule. The math, using the document's own milestones from today (August 2026):

- Step 1 (disease selection, pre-IND, advocacy engagement): 12 months → August 2027
- Step 2 (IND open, enrollment of N=12–15, database lock): 12–24 months → August 2028–August 2029
- NDA filing: August 2028–August 2029
- FDA priority review (6 months): approval February 2029–February 2030

At the document's own "realistic" 36-month path to NDA filing: NDA filed August 2029, approval February 2030 — five months after the program ceases to issue PRVs. The 30-month optimistic path to NDA filing gives approval August 2029, which is one month before sunset with zero tolerance for any FDA hold, complete response letter, manufacturing deficiency, or information request. This is not a planning schedule; it is a no-margin scenario.

The PRV program requires *approval* before the sunset date, not merely filing. 21 U.S.C. § 360ff(a)(4)(B)(i) is unambiguous on this point (documented in project memory for this repository). The document's entire economic premise — PRV monetization at $100–150M — rests on reaching approval before September 30, 2029. The document never performs this calculation. R2 does not challenge or respond to this point at all. R1's evidence is live-verified statutory text plus the document's own milestone schedule. This finding stands at high confidence.

**The implication for the minimum viable version:** Starting today (August 2026), a PRV-viable program must reach NDA approval by September 30, 2029 — that is 37 months. Under priority review (6 months), the NDA must be filed no later than March 2029, which is 31 months from now. At the document's own enrollment timeline for the lean single-site design (12 months Step 1 + 12 months Step 2 enrollment), filing by March 2029 is barely achievable only if enrollment completes on time and the NDA preparation takes under 3 months. There is no margin for a single slip. The minimum viable version as written is therefore not viable for PRV purposes under most realistic execution sequences.

**2. Three benchmark trials in the per-site table are not US/EU pediatric comparators. VERDICT: R1 is correct. (VERIFIED)**

R1 verified live that JR-141 MPS II (NCT03568175) is Japan-only, velaglucerase children (NCT01685216) ran across Egypt, India, and Tunisia, and miglustat NPC China (NCT03910621) is China-only. These three trials are not comparable to a bootstrapped US pediatric IND. Their per-site enrollment rates — 0.082, 0.047, and 0.370 pts/site/month respectively — reflect patient registry density and physician-to-patient concentration in those markets. Removing them does not move the US/EU median dramatically (the remaining pool still centers around 0.05–0.08 pts/site/month), but the methodology is flawed and the benchmark pool should be characterized as containing non-comparable entries. The document's planning benchmark happens to survive the correction numerically, but the error should be acknowledged.

**3. SHP611 site count is incorrect. VERDICT: R1 is correct. (VERIFIED)**

R1's live ClinicalTrials.gov API query returned 26 location entries for NCT03771898, not the 30 used in the document. Using 30 sites for 36 patients understates the pts/site/month for that trial by approximately 15% (from 0.026 to ~0.031). This is a minor error that does not change any planning conclusion but is a factual inaccuracy in the VERIFIED section.

**4. The RDEA pilot program is described as a planning tool without quantifying admission probability. VERDICT: R1 is correct.**

The document treats RDEA pilot access as available to a bootstrapped sponsor without noting that at most 3 proposals are admitted per year across the entire US rare disease community. This should be characterized as a low-probability upside, not a baseline planning assumption. R2 does not rebut this.

**5. The internal contradiction on cerliponase and investigator-IND evidence quality. VERDICT: R2 is correct on this specific point.**

Section 4.1 correctly states that cerliponase alfa received full approval (not accelerated approval) on N=24 single-arm with natural history control. Section 3.3 then characterizes the investigator-IND single-site model as producing "evidence FDA will score as suggestive, not confirmatory, for a 505(b)(1) NDA." These two statements are in tension: the cerliponase precedent *is* the confirmatory approval case for a single-arm natural history-controlled N=24 trial. If cerliponase was confirmatory, the investigator-IND model aimed at similar N and design cannot be generically scored as merely suggestive. The SEZABY precedent footnote should not do all the work of establishing that investigator-IND can produce a PRV-eligible NDA — cerliponase itself, while a commercial sponsor trial, demonstrates FDA's acceptance of the design. The document's downgrading language in §3.3 is not adequately supported given what it says about cerliponase in §4.1.

---

### Where the Analysis Was Genuinely Too Pessimistic

**1. The enrollment funnel narrative anchors to the floor, not the central case. VERDICT: R2 is correct.**

The document's compound enrollment funnel produces a range of 4.7%–14% of the diagnosed population, but every paragraph following the table defaults to the 4.7% floor. R2 correctly computes the midpoint case: using the midpoint of each filter range produces approximately 8–10% reachable. For a disease with 300 diagnosed US patients, 8–10% means 24–30 enrollable patients — above the 20-patient target without requiring "approach of essentially every known patient." The document's statement that "targeting 20 patients means you need to approach essentially every known patient" is true at the floor (4.7% × 300 = 14 patients) but not at the central case (8–10% × 300 = 24–30 patients). The narrative should present the central case as representative and the floor as the stress case. The current framing is pessimistically biased in a way that is not supported by the document's own table.

**2. The competing-trial filter (0.70–0.90) is too generous for RDCRN-dependent diseases — but the correction is smaller than R1 implies.** R1 argues the realistic competing-trial survival fraction for RDCRN-dependent diseases is 0.50–0.70. This is likely correct for diseases where the RDCRN is the *only* investigator source. However, the correct remedy is better disease selection (choose a disease with an advocacy-led patient registry outside RDCRN, or where the RDCRN consortium is one of several investigator channels), not a global downgrade of the table. The document's §3.3 condition #5 ("no prior approved therapy") already partially captures this. R1's point is valid for the worst-case disease selection, not for the full universe the document is supposedly analyzing.

**3. The single-program case (Section 6) is understated relative to its own evidence base.** R2 correctly identifies that Sections 1–5 use NCL/CLN2 as the implicit prototype — the hardest enrollable disease globally (prevalence <1:100,000, <5-year survival, concentrated at 3–5 expert centers worldwide). The enrollment rate of 0.185 pts/month and the 88% single-site statistic are NCL-specific findings. For a disease like MPS I (0.14/10,000 diagnosed, well-characterized natural history, multiple US expert centers, multiple ERT trials completed), the per-site enrollment rates are materially higher — the MPS II ERT trial in the document's own table enrolled at 0.593 pts/site/month. The document correctly notes the MPS II trial is an outlier due to larger diagnosed population, but does not follow through by segmenting the disease selection universe by enrollment difficulty. Section 6's "one program done properly" should be framed as achievable for a mid-tier ultra-rare disease (100–500 diagnosed US patients, established natural history registry, willing academic PI) rather than as a heroic exception.

**4. The CLN2 gene transfer trial (NCT00151216) enrollment rate is mismeasured.** R1 correctly identifies that the 180-month denominator for this trial conflates the enrollment period with the long-term follow-up period required by gene therapy protocols. Using 180 months for 10 patients yields 0.056 pts/month, but actual enrollment at a single expert NCL center almost certainly occurred within the first 12–24 months (0.4–0.8 pts/month). This depresses the computed median from the NCL trial set. Paradoxically this error makes the pessimistic enrollment duration projection (108 months for 20 patients) worse than the data actually support — so it cuts against the document's own correct conclusion, not against it. The error should be corrected but the directional conclusion (enrollment is severely challenging for NCL-class diseases) remains valid.

---

### Conclusion After Both Reviews

The analysis is **appropriately pessimistic for the 6–10 simultaneous program question** and remains the correct answer there. It is **too pessimistic in framing the single-program case** — the enrollment and cost evidence, taken at central rather than floor values, supports a lean one-program scenario more readily than the document's narrative suggests. The Section 6 minimum viable design is sound in structure.

However, the document has **one unaddressed analytical failure that overrides the single-program optimism:** the PRV sunset makes the minimum viable timeline not minimum viable. The 30–36 month NDA filing schedule, taken from today (August 2026), puts approval at February 2029 (optimistic) to February 2030 (realistic). The PRV program closes September 30, 2029. Starting today, a team would need to compress the schedule to file NDA by March 2029 — leaving no margin for slippage — or accept that they are building non-PRV rare disease programs at a fraction of the projected economic value.

**The headline conclusion from §7 must be updated to reflect this finding:**

The single-program case was the one scenario this document found feasible. That finding survives the enrollment and cost challenges from R2. It does not survive the PRV sunset calendar check from R1. The economic thesis requires either (a) a faster execution path than the document's own 30–36 month minimum viable schedule — specifically, NDA approval before September 30, 2029 from a standing start in August 2026, which is 37 months at zero margin — or (b) a revised economic model that does not depend on PRV proceeds. R1's case on the sunset point is better supported, by the document's own milestone schedule versus a hard statutory deadline. R2's case on enrollment framing is also valid but does not rescue the economic thesis from the sunset constraint.

**Updated verdict (supersedes §7 for the single-program case):** A single lean program is operationally feasible but is not PRV-viable under a conventional 30–36 month development timeline starting today. To be PRV-viable, execution must compress Step 1 and Step 2 to a combined total under 25 months (filing by March 2029), which is at or beyond the boundary of what the SBIR/STTR funding timeline permits (NIH SBIR Phase 1 award ~9–12 months after submission + Phase 2 competition ~ another 9–12 months = earliest Phase 2 dollars late 2028, which does not fund a trial that has already filed). Either the funding structure must not depend on SBIR sequencing, or the PRV monetization assumption must be discounted substantially in the financial model.

---

## 9. URL Ledger

### VERIFIED

| URL | Source | Confirmed |
|---|---|---|
| `https://clinicaltrials.gov/api/v2/version` → `{"apiVersion":"2.0.5","dataTimestamp":"2026-08-05T09:00:06"}` | ClinicalTrials.gov API v2 | VERIFIED live 2026-08-06 |
| `https://clinicaltrials.gov/api/v2/studies?query.cond=mucopolysaccharidosis+OR+gaucher+OR+fabry&filter.overallStatus=COMPLETED` | LSD trial enrollment data | VERIFIED live 2026-08-06 |
| `https://clinicaltrials.gov/api/v2/studies?query.cond=batten+disease` | Batten disease trial inventory | VERIFIED live 2026-08-06 |
| `https://clinicaltrials.gov/api/v2/studies?query.cond=inborn+errors+metabolism` | IEM status counts (Completed:1838, Terminated:223, Withdrawn:125) | VERIFIED live 2026-08-06 |
| `https://www.federalregister.gov/documents/full_text/text/2022/10/27/2022-23383.txt` | RDEA Pilot Program FR Notice 87 FR 65085 | VERIFIED 2026-08-06; full text read |
| Sources 12, 10, 13, 03 in this repository | RDCRN, NewSTEPs, RWD platforms, Orphanet | VERIFIED per those files (research date 2026-08-05) |

### UNVERIFIED

| URL / Source | Issue |
|---|---|
| `https://www.fda.gov/drugs/development-resources/rare-disease-endpoint-advancement-pilot-program` | Returns 404 from automated fetcher; referenced in FR notice as the program web page |
| Medidata Acorn AI per-patient cost benchmarks | Behind commercial login; cited as $35–80k/patient for rare disease Phase 2; not independently confirmed |
| GlobalData per-patient cost $19–24k | Secondary citation; full report paywalled |
| Thomas et al. 2021 *Clinical and Translational Science* rare disease enrollment failure rate ~30% | Not directly fetched; widely cited in the literature |
| NCATS SBIR Phase 1 $300k cap | From memory of NIH program description; confirm at grants.nih.gov/funding/sbir |
| WCG/ADVARRA central IRB fee schedules | Proprietary; $8–25k range from informal industry reports |
| `https://www.fda.gov/media/151712/download` | PDUFA VII Performance Goals document; referenced in FR notice; not independently fetched |
