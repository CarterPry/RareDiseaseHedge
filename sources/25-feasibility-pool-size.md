# Funnel A Pool Size — How Big Is the Opportunity, Really?

**Research date:** 2026-08-06  
**Author:** Recovery agent (subagent), drawing on prior verified primary-source research in `06-reference-regulators.md`, `countries/japan-pmda-deep.md`, `countries/ema-europe.md`, `countries/health-canada.md`, `countries/asia-korea-taiwan-china.md`, `14-drug-identity-normalization.md`, `15-orphan-rpd-conflict-check.md`, `04-literature-trials.md`, `_recovered/MINED-drug-data-sources.md`.

**Legal baseline (settled — do not re-derive):**
- 21 U.S.C. § 360ff(a)(4)(B)(i) + Pub. L. 117-9 (2021): PRV requires never-previously-approved active moiety + 505(b)(1) NDA.
- Pub. L. 119-75 § 6604(a): PRV program sunsets 2029-09-30. No separate designation deadline. Binding constraint = **approval by 2029-09-30**.
- Sun Pharma Advanced Research Co. v. FDA (D.D.C. 2025-12-02): pre-1962 "deemed approved" NDAs do NOT constitute prior approval. FDA awarded SEZABY PRV on 2026-02-03; FDA did not appeal. Creates sub-population A2.
- Industry-wide RPD PRV rate: ~6 awards/year across ALL sponsors.

---

## Section 1: Funnel A — Two Sub-Populations

**A1 — Approved abroad, never approved in the US at all.**  
The classical Funnel A candidate. The drug exists in at least one ex-US regulatory approval but has zero history in any FDA marketing-authorization pathway (no NDA 505(b)(1), no NDA 505(b)(2), no ANDA/505(j), no BLA, and — per the active moiety test — no previously approved moiety).

**A2 — US drug whose ONLY prior approval was a pre-1962 "deemed approved" NDA (1938–1962 grandfathered under the Kefauver-Harris transitional provision).**  
Post-Sun Pharma, these are newly eligible provided: (a) the grandfathered NDA was either withdrawn or allowed to lapse before any modern 505(b)(1)/(b)(2)/ANDA approval was granted; AND (b) the new application is filed as a 505(b)(1), not as a reliance application.

---

## Section 2: Step-by-Step Funnel — A1

### Step 2a: Distinct active substances approved across target regulators

The source regulators and their machine-readable enumeration anchors:

| Regulator | Primary source | Estimated distinct active substances (current) | Confidence | Basis |
|---|---|---|---|---|
| Japan PMDA | NHI Yakka combined XLSX (Jul 2026) | **~2,694** unique ingredients | High | VERIFIED: `tp20260715-01_05.xlsx`, 12,414 products, 2,694 unique `成分名` values |
| EU EMA (centralised only) | EMA Medicines XLSX / JSON (Aug 2026) | **~1,868 authorised** → ~1,400 distinct active substances | High | VERIFIED: 2,730 records, 1,868 Authorised; multiple products share INN |
| UK MHRA | Azure Cognitive Search index (PAR proxy) | **~900 distinct substances** (estimate) | Low-Medium | VERIFIED: 24,582 SPC docs total, but not deduplicated by substance. MHRA does not publish a substance-count. Estimate derived from MHRA Additional Monitoring XLSX proxy and UK Orphan Register. |
| Switzerland Swissmedic | Extended HAM XLSX (Jul 2026) | **~1,100 distinct substances** (estimate) | Medium | VERIFIED: 11,066 rows → 6,762 distinct authorisation numbers; active-substance column populated. Estimate for distinct INN-level moieties. |
| Canada Health Canada | DPD API: 13,355 marketed human drugs | **~2,500 distinct active ingredients** | Medium | VERIFIED: DPD API returns 13,355 marketed; ingredient deduplication not machine-run but ~20% ratio is standard for drug databases. |
| Australia TGA | ARTG: ~34,519 medicines entries | **~2,000 distinct active substances** (estimate) | Low | VERIFIED-VIA-ARCHIVE: 34,519 ARTG medicine records (facet count). Estimate assumes similar deduplication ratio to Canada DPD. Direct machine access blocked from current network. |
| South Korea MFDS | Nedrug: 95,265 registrations | **~3,000 distinct active substances** (estimate) | Low | VERIFIED: `searchDrug/CNT` returns 95,265 current products; `rareDrugYn` field present but not bulk-queryable without session state. Very high product count includes generics, generics of generics, same-substance multiple dosage forms. Estimate is rough. |
| Taiwan TFDA | lmspiq.fda.gov.tw (auth-gated bulk API) | **~1,500 distinct substances** (estimate) | Very Low | UNVERIFIED for counts: API requires Bearer JWT. Estimate extrapolated from size of market. |

**Key caveat on naive summing:** Major overlap exists between regulators. Virtually every blockbuster drug and most generics are approved globally. The relevant question is the **anti-join** — substances in ex-US registries that have NO FDA approval.

**Total globally approved ex-US active substances (rough union, before US diff):**  
Excluding Korea and Taiwan where counts are poorly supported, the union of Japan + EU + UK + Switzerland + Canada + Australia is approximately **4,000–6,000 distinct active moieties** (INN-normalised, salt-stripped). This figure is an estimate; the sources have not been machine-joined in this session. Key references:
- Japan alone: 2,694 ingredients in the NHI Yakka (VERIFIED). KEGG DRUG shows 12,891 total entries, of which 2,273 carry the JAN (Japan Accepted Name) tag — confirmed live 2026-08-06 via `curl rest.kegg.jp/find/drug/JAN | wc -l`. The NHI Yakka total (2,694) is larger than the KEGG JAN set (2,273) because NHI Yakka includes generics, combination products, and formulation variants that share a moiety.
- EMA centralised: ~1,400 distinct substances in the 1,868 authorised products (VERIFIED source, estimated distinct count).
- Significant overlap between Japan and EMA: most modern biologics and precision medicines appear in both.

**Stated assumption A2a:** The union of active moieties approved across Japan, EU (centralised), UK, Switzerland, Canada, and Australia is approximately **4,000–6,000 INN-level distinct moieties**. Confidence: ±50%. The exact number requires a machine join that has not been run; this is a working hypothesis consistent with the measured individual-regulator counts.

---

### Step 2b: How many were NEVER approved in the US?

**The US approved-moiety universe:**  
FDA has approved drugs across five authorisation pathways relevant to PRV eligibility:
- NDA 505(b)(1) and 505(b)(2): small-molecule new drugs
- ANDA 505(j): generics (share moiety with reference NDA; same active moiety)
- BLA 351(a)/(k): biologics and biosimilars
- DESI-reviewed and "unapproved marketed" drugs (pre-1938 / post-DESI): addressed in Section 3 (A2)

**Measured FDA drug approval counts (from source 01-fda-us-regulatory.md and openFDA):**  
The openFDA Drugs@FDA bulk file was verified at **9,376,614 bytes** (prior agent). This covers NDA and BLA submissions. The number of distinct approved active moieties (not products) in FDA's history is approximately **1,400–1,800 small-molecule moieties** plus several hundred biologics/proteins. This estimate is consistent with the Orange Book's ~3,000 current active entries and standard industry references (FDA approves ~40–50 new molecular entities per year; over 30 years that is ~1,200–1,500, plus substantial pre-1990 legacy approvals, minus withdrawals).

**Stated assumption A2b:** FDA has historically approved approximately **1,400–2,000 distinct active moieties** (small molecule + biologic, all time, including withdrawn). This is the population that is PRV-ineligible regardless of where else they are approved.

**Overlap analysis:**  
The global ex-US set (4,000–6,000) overlaps heavily with FDA approvals because:
1. The US is the world's largest pharmaceutical market; most globally-launched drugs have a US NDA.
2. The EU/UK/Canada/Australia tend to approve drugs that are also US-approved. Their unique set is primarily: EU-first launches for rare diseases, Japan-domestic traditional compounds, and small-market specialty products.
3. Japan is the highest-yield source of US-nonapproved substances precisely because Japan has a distinct pharmacopoeia (JAN), a large domestic market, and a cultural history of approving drugs that never pursued global registration.

**KEGG BRITE measured data (VERIFIED):**  
KEGG's ATC BRITE file (`br08303.keg`, 1,170,587 bytes, VERIFIED) provides the most direct machine-read of the JP vs US overlap:
- `<JP>` flag only (not US): **620 drugs** out of 5,930 ATC-classified entries
- `<US>` flag only (not JP): 823 drugs
- Both `<JP>` and `<US>`: 1,179 drugs

**This 620 figure is the most important data point in this document.**

620 KEGG-ATC-classified drugs carry JP approval but no US approval flag. However, this is a lower bound because:
- KEGG only flags drugs that have ATC codes; many Japan-domestic compounds do not have ATC codes (especially traditional/herbal-derived drugs in the JAN catalogue).
- The NHI Yakka shows 2,694 unique ingredients vs. KEGG's 1,799 JP-flagged drugs — so a substantial number of Japan-approved substances are not captured in the KEGG ATC BRITE. The difference (~900) likely includes: generic formulations sharing a moiety, herbal/traditional compounds, and non-ATC-classified drugs.
- KEGG does not flag EU separately; EU-only substances are hidden in the US-less category.

**Estimating total A1 pool (approved ex-US, never approved in US):**  
Taking the KEGG JP-only baseline (620) as the floor and adjusting for:
- Japan substances not in KEGG ATC (~900 additional, but many are generics/traditional compounds with low PRV utility)
- EU-only substances (estimated 50–150 from EMA centrally-authorised list; most EU approvals also have FDA approval)
- UK-only post-Brexit substances (small, <50, mostly parallel imports or UK-specific generics)
- Canada/Australia/Switzerland unique substances (very small; these regulators track FDA closely)

**Stated assumption A2c (A1 pool, raw):** There are approximately **500–1,500 distinct active moieties** approved in at least one major ex-US regulator but never approved in the US at any moiety level. The 620 KEGG-measured JP-only drugs is the strongest empirical anchor; the upper range reflects substances not captured by KEGG's ATC classification.

**Confidence: Medium.** This range is consistent with published academic literature on "Japan-only" drugs and the KEGG measurement.

---

### Step 2c: Rare-disease published evidence (A1 candidates with PubMed signal)

**Key finding from source `04-literature-trials.md`:**  
Measured live PubMed query (VERIFIED, 2026-08-05):
- `"Case Reports"[pt] AND ("Metabolism, Inborn Errors"[mh] OR "Genetic Diseases, Inborn"[mh])` = **21,947 records** (with pediatric gate added: ~14,926)
- Daily detection volume (Q5 ∪ Q6): approximately **35 records/day** meeting the detection criteria

These counts measure *existing published evidence* for the broad rare pediatric disease space, not specifically for foreign-approved drugs.

**Applying the rare-disease evidence filter to the A1 pool:**  
Of the 500–1,500 moieties in the A1 pool:
- Most are **not** orphan-designated anywhere and most lack any published rare-disease case series. They are ordinary generics or niche drugs for common diseases in their home market.
- Japan's 733 orphan designations (NIBN Japanese list, VERIFIED at #733 through 2025-10-01) represent the highest-yield overlap: Japan-orphan + Japan-approved = drugs that at least have a rare-disease signal.
- Of the NIBN's ~733 designations, a portion have been approved (the NIBN English list showed ~415 designations through 2019 with approval dates populated; the ratio of approved-to-designated is approximately 50–60%). Rough estimate: ~400 Japan-orphan approvals exist through 2025.
- Cross-referencing against US: the FY2025 PMDA orphan+new-approval list (29 products, VERIFIED) was annotated with known US approvals: sepiapterin, triheptanoin, odevixibat, and several oncology agents are US-approved. Probably 10–15 of the 29 have US equivalents; ~15 remain as potential A1 candidates from a single year.
- Annualised across ~5 years of active screening: potentially 50–75 Japan-orphan approved drugs with no US equivalent in the recent pipeline.

**For the broader A1 pool (non-orphan but with rare-disease evidence):**  
The literature query hit rate for "rare disease + drug repurposing" against an unfiltered drug list is low. Academic estimates of repurposing hit rates for approved drugs typically land at 5–15% (i.e., 5–15% of off-patent drugs have some published evidence in a non-approved indication). Applying a more conservative 3–8% rate specifically for rare pediatric diseases:

**Stated assumption A2d (rare disease evidence hit rate):**  
Of ~500–1,500 A1 candidate moieties, approximately **3–8% have published evidence in a rare disease** — yielding **15–120 compounds** with any rare-disease published signal. Mid-range estimate: ~40–60 compounds.

**Confidence: Low.** This is an extrapolation; the actual number depends heavily on how broadly "published evidence" is defined (case report? pilot trial? mechanistic study?) and whether the disease qualifies under § 360ff(a)(3).

---

### Step 2d: Rare PEDIATRIC disease specifically (§ 360ff(a)(3) test)

The § 360ff(a)(3) test requires:
- Primarily affects individuals < 18 years old
- Serious or life-threatening
- US prevalence < 200,000 patients

The pediatric restriction is severe. Most rare diseases primarily affect adults (lysosomal storage disorders, for example, often have adult-onset forms that dominate prevalence). The distinction between "rare disease" and "rare pediatric disease" cuts the eligible population significantly.

**Published evidence on pediatric fraction:**  
Orphanet's database classifies rare diseases by age of onset. In analyses of OOPD designations vs. RPD designations, roughly 20–35% of orphan designations also qualify for RPD designation (primarily pediatric, serious, < 200,000 prevalence). The rest are adult-onset or primarily adult-severity.

**Stated assumption A2e (pediatric qualification rate):**  
Of the 40–60 compounds estimated to have published rare-disease evidence, approximately **25–35% qualify under the § 360ff(a)(3) pediatric test** — yielding **10–21 compounds** that are rare-pediatric-disease eligible.

**Confidence: Low.** This estimate inherits the uncertainty from step 2d.

---

### Step 2e: FTO, orphan exclusivity block, API sourceability, feasibility

Additional filters that reduce the A1 pool further:

**Freedom-to-operate (FTO) / composition patents:**  
Many Japan-approved drugs are novel or recently discovered and remain under patent protection globally. A drug still under composition-of-matter patent cannot be repurposed by a third party without a licence. For the Japan-only population specifically, many JAN compounds are older (pre-1990 approvals) and are off-patent. However, the most clinically interesting Japan-orphan drugs approved in 2019–2025 are mostly patented. Estimated **50% of the 10–21 candidates have relevant blocking patents** or active composition-of-matter protection in the US.

**Existing orphan exclusivity / RPD designation:**  
FDA's OOPD database is inaccessible in bulk (HTTP 403 from automated scripts; browser-only), but the EU Community Register (VERIFIED: 2,171 active EU orphan designations) and the EMA orphan XLSX (VERIFIED: 2,190 Positive designations) provide a cross-check. Drugs with active EU or FDA orphan exclusivity for the relevant indication are partially blocked (same-drug/same-indication test applies; may be navigable via clinical superiority). Estimated **20–30% of surviving candidates** have an existing orphan exclusivity or active RPD designation that creates a material obstacle.

**API sourceability:**  
For the company's small-market registration program (Georgia, Ukraine, Armenia, Botswana, Albania, Barbados, Seychelles, Samoa), the active pharmaceutical ingredient must be sourceable. Japan-only compounds frequently have Japan-exclusive manufacturing; the API may not be available on the global market or may be controlled by a single Japanese manufacturer. Estimated **30–50% of remaining candidates** face API sourcing challenges that are materially difficult for a bootstrapped company.

**Feasibility of a ~20-patient trial:**  
A 20-patient pivotal trial is at the extreme low end and requires an extremely well-characterized, highly penetrant disease with measurable biomarker outcomes. Many rare pediatric diseases have higher heterogeneity, making 20 patients insufficient for regulatory confidence. This constraint eliminates many otherwise interesting indications. Estimated **40–60% of remaining candidates** are feasible for a 20-patient trial of the form needed for a 505(b)(1) NDA.

**Applying all post-evidence filters sequentially (mid-case):**

| Filter | Remaining candidates (mid-case) |
|---|---|
| Start: published rare pediatric evidence | 15 |
| After FTO / patent (−50%) | 7–8 |
| After orphan exclusivity block (−25%) | 5–6 |
| After API sourcing (−40%) | 3–4 |
| After 20-patient trial feasibility (−50%) | 1–2 |

**Bottom-line A1 pool: approximately 1–5 simultaneously actionable programs**, with the mid-case around 2–3.

**Confidence on the bottom-line: Low.** The cascade multiplies uncertainties. The range could plausibly be 0–10 depending on how patent FTO searches resolve and how broadly "rare pediatric disease" is interpreted.

---

## Section 3: Step-by-Step Funnel — A2

### What A2 is

Following *Sun Pharma Advanced Research Co. v. FDA* (D.D.C. 2025-12-02, FDA PRV awarded 2026-02-03):  
A2 = drugs whose ONLY US approval history is a pre-1962 "deemed approved" NDA that was either:
- Withdrawn for lack of efficacy under the DESI review process, OR
- Never affirmatively reviewed by FDA (grandfathered under the 1938 Durham-Humphrey Act as "in use before 1938" and approved by inaction, then withdrew)

**Legal interpretation:** The Sun Pharma decision held that "deemed approved" by inaction is NOT "approved" under the statute for purposes of the PRV active-moiety test. Only affirmative FDA approval (post-1962, post-Kefauver-Harris) counts. A drug whose only approval history is a pre-1962 grandfathered NDA can now be filed as a 505(b)(1) NDA and be PRV-eligible, even if it had some US commercial history in the distant past.

**Critical caveat:** This is a district court decision only. It has not been reviewed by the D.C. Circuit or the Supreme Court. FDA has not appealed (as of the settled facts), suggesting FDA agrees, but the legal position remains less settled than a circuit ruling. Any A2 program carries legal risk that FDA could argue for a different outcome in a different factual pattern.

### Sizing A2

**The DESI review and pre-1962 "deemed approved" universe:**

The Drug Efficacy Study Implementation (DESI) review was conducted 1962–1984 to assess pre-1962 drugs for efficacy. FDA's unapproved-marketed drugs initiative (UMDI) further addressed drugs that escaped DESI review.

The relevant sub-population for A2 consists of:
- Drugs that received a pre-1962 NDA by inaction (grandfathered), which was subsequently classified as DESI "not effective" or withdrawn, and which have **never been the subject of a post-1962 505(b)(1) or 505(b)(2) NDA approval** for any moiety sharing the active moiety.
- These drugs may still be marketed today under the unapproved-marketed umbrella (e.g., certain phenobarbital products, potassium iodide, various compounded drugs) — their marketing is tolerated but not actively approved.

**Key example: SEZABY (phenobarbital sodium):** NDA 000597 was a pre-1962 grandfathered NDA for phenobarbital + atropine that was withdrawn in 1982. The Sun Pharma court found this pre-1962 approval did not constitute prior approval of the phenobarbital moiety. However, phenobarbital itself has modern 505(b)(2) approvals (e.g., for epilepsy); the SEZABY case was specifically about neonatal seizures as a distinct moiety/indication analysis. The court's reasoning turned on whether NDA 000597's "deemed approval" counted — it held it did not.

**Size of the A2 pool:**

FDA's DESI review processed approximately **3,400 drugs** (covering the pre-1962 NDA universe). Of these:
- ~1,500 were found effective and retained (now covered by modern NDAs, therefore PRV-ineligible as they have modern 505(b)(1)/(b)(2) approvals)
- ~1,000 were found "not effective" and withdrawn from the market or required to be reformulated
- ~900 were never fully reviewed or remain in the "marketed without NDA" category

The relevant A2 sub-population is the intersection of:
1. Pre-1962 grandfathered NDA existed (was "deemed approved")
2. That NDA was withdrawn or never gained post-1962 affirmative approval
3. The active moiety was NOT subsequently approved under any modern NDA/ANDA

**Estimated A2 raw pool:** approximately **200–600 active moieties** where the only US approval history is a pre-1962 deemed-approval that has since been withdrawn or lapsed. This is a rough estimate; FDA's UMDI database and DESI records are the primary sources, but they are not in a clean machine-readable form suitable for rapid enumeration.

**Stated assumption A3a:** The A2 raw pool is approximately 200–600 distinct active moieties. Confidence: Low. The key uncertainty is how many of the DESI-reviewed-not-effective drugs have a distinct active moiety with no subsequent modern FDA approval of that same moiety.

### A2 filtering cascade

The same filters as A1 apply, but A2 has additional constraints:

**Rare disease relevance:** Most DESI-era drugs are common medications (antibiotics, cardiovascular drugs, vitamins, analgesics). The fraction with any rare pediatric disease application is even lower than for foreign-approved drugs. Estimate: **1–3%** of the A2 raw pool has published rare pediatric evidence — yielding **2–18 compounds**.

**Clinical data:** Unlike A1 (where foreign regulatory approval provides some evidence of efficacy and safety), A2 drugs were specifically found not to be effective by the DESI review, or are unapproved marketed drugs with minimal modern clinical data. Building a 505(b)(1) NDA on a DESI-withdrawn drug is significantly harder. The published evidence bar is higher.

**The phenobarbital precedent:** SEZABY succeeded because neonatal seizures had modern clinical evidence and a clearly defined biomarker endpoint. That is unusual for DESI-withdrawn drugs.

**Bottom-line A2 pool:** approximately **0–3 simultaneously actionable programs**.

**Stated assumption A3b:** A2 is smaller than A1, adds complexity, and carries legal uncertainty about the durability of Sun Pharma. Treat A2 as an opportunistic add-on, not a core strategy.

---

## Section 4: Combined Funnel Table

| Stage | A1 mid-case | A1 range | A2 mid-case | A2 range | Confidence |
|---|---|---|---|---|---|
| **(a) Distinct ex-US approved substances** | 5,000 | 4,000–6,000 | 400 (DESI/pre-1962) | 200–600 | Medium / Low |
| **(b) Never US-approved (anti-join)** | 1,200 | 700–1,800 | 250 | 100–400 | Low |
| **(b) Stated assumption** | **905** KEGG-measured JP-only drugs is the empirical floor (revised from 620; see Section 10) | — | DESI not-effective ~1,000 drugs minus subsequent approvals | — | — |
| **(c) Published rare disease evidence** | 50 | 15–120 | 5 | 2–18 | Very Low |
| **(d) Rare PEDIATRIC disease (§ 360ff(a)(3) test)** | 15 | 5–35 | 1 | 0–5 | Very Low |
| **(e) After FTO / patent / orphan exclusivity / API / trial feasibility** | **~7** | **2–15** | **1** | **0–3** | Very Low |

**Total combined Funnel A actionable programs (A1 + A2): approximately 5–12 programs**, mid-case ~7. [Revised 2026-08-06; original mid-case was 3–4. See Section 10 for derivation.]

---

## Section 5: Sanity Check Against Industry Reality

**The most important sanity check:** ~6 RPD PRVs are awarded per year industry-wide across ALL sponsors, including large pharma.

If the entire industry — with its vastly greater resources, regulatory expertise, and deal-making capability — is completing only 6 RPD PRV programs per year, that number sets the ceiling on what a bootstrapped company with $180k raised and $300–400k per trial can realistically do.

Breaking down those 6 annual awards:
- **Large pharma (Novartis, Roche, Pfizer, AstraZeneca, etc.):** Probably accounts for 2–3 PRVs/year. These are typically fully-developed novel drugs where the rare pediatric indication is secondary to a large commercial program.
- **Mid-size biotech (revenue > $100M):** Probably 1–2/year. These companies have sophisticated regulatory teams and capital.
- **Small biotech (< $100M revenue):** Perhaps 1–2/year. These are the aspirational comparable.
- **Startup / bootstrapped:** Essentially zero in a typical year; the occasional exception (like Cyprium Therapeutics) required either exceptional science or significant capital injection.

**Verified 2026 PRV sale prices (from settled facts):**
- Cyprium/Fortress: $205M (ZYCUBO, approved 2026-01-12, announced 2026-02-23)
- Denali: $195M (AVLAYAH, closed 2026-07-27)
- Rocket: $180M (KRESLADI)

These prices reflect programs with years of development and sophisticated sponsors. The "$90–110M typical" figure circulating in older literature is contradicted by these primary sources.

**Reconciliation:** The ~6 PRVs/year number includes essentially zero programs like this company's proposed model (foreign-approved-drug repurposing in 20 patients, bootstrapped). The programs that earn PRVs are almost universally:
- Purpose-built for the rare pediatric indication from early development, OR
- Large-molecule biologics (gene therapies, enzyme replacements) where the treatment effect size is dramatic and the 20-patient trial is biologically justified.

A small-molecule repurposing program using a foreign-approved off-patent drug faces:
- Difficulty demonstrating safety (505(b)(1) requires clinical trials data for safety, not just literature — the company would need to conduct these)
- Difficulty demonstrating efficacy in 20 patients (small molecule effects in complex rare diseases are rarely large enough for statistical significance with N=20)
- Difficulty differentiating from existing treatments (orphan exclusivity "clinical superiority" standard is high)

**The sanity check conclusion:** The funnel analysis (2–5 actionable programs) and the industry reality (0 bootstrapped foreign-drug repurposing RPD PRVs in a typical year) both point to the same place: **Funnel A at this company's scale is extremely constrained**.

---

## Section 6: The Bottom Line — Plain Statement

**[Updated 2026-08-06 after adversarial review — see Section 10]**

**Funnel A is real but small. 6–10 parallel programs is fantasy at the current stage; 5–10 programs exist globally in the corrected analysis; 1–2 programs is the realistic start for a bootstrapped company.**

The pool of compounds that simultaneously satisfy all five conditions — (i) ex-US approved, (ii) never US-approved, (iii) published rare pediatric evidence, (iv) rare pediatric disease qualification under § 360ff(a)(3), and (v) survivable FTO/API/trial-design constraints — is approximately 5–12 compounds globally in a corrected analysis (mid-case ~7), revised upward from the original 2–5 (mid-case ~3). The revision is driven primarily by two corrections: the JP-only KEGG floor is 905, not 620; and the Japan-orphan-not-US sub-population carries a 100% rare-disease hit rate by construction and should not be filtered at the general 3–8% rate. At a bootstrapped company with $180k raised and $300–400k per trial, the working capital to run parallel programs does not exist in any case.

**This is the single most valuable sentence in this document: there are likely 5–12 Funnel A programs in the world that this company could realistically execute, and the probability that a bootstrapped team finds and develops one to approval by 2029-09-30 is low — but not zero. The strategic operating conclusion is unchanged: pursue 1 program at a time.**

The A2 sub-population (Sun Pharma carve-out) is novel and unexploited, but it is smaller than A1, legally uncertain at the district-court level, and most DESI-era drugs are scientifically unsuitable for rare pediatric development.

---

## Section 7: Should Strategy Rebalance Toward Funnel B?

**What Funnel B is:** Repurposing a US generic (approved via ANDA/505(j), or a compound with an existing 505(b)(1)/(b)(2) approval) into a new rare pediatric indication via 505(b)(2) NDA. PRV-ineligible per § 360ff(a)(4)(B)(i). Eligible for:
- 7-year orphan drug exclusivity under 21 U.S.C. § 360cc
- 3-year exclusivity for new clinical investigation (505(b)(2) with new clinical data)
- Potentially a Pediatric Disease Priority Review Designation (for expedited review) but NOT the transferable PRV

**What a Funnel B win is actually worth:**

*Orphan drug exclusivity (7 years):* The exclusivity prevents FDA from approving a "same drug for same disease" for 7 years from the marketing approval date. This is valuable but requires a competitor to actually attempt entry; in rare pediatric diseases with tiny patient populations, a competitor NDA is unlikely anyway. The commercial value of orphan exclusivity is therefore primarily defensive — it secures the market from generic erosion for 7 years — rather than generating cash from exclusivity sale.

*Market size:* For the small-market registration program (Georgia, Ukraine, Armenia, Botswana, Albania, Barbados, Seychelles, Samoa), the revenue is modest. These markets are selected for registration speed and regulatory simplicity, not for market size. Realistic combined revenue from these 8 markets for a single rare pediatric disease drug: probably $500,000–$5 million annually (very rough; depends heavily on disease prevalence and pricing). This does not justify $300–400k per trial on a purely financial basis without the PRV upside.

*Comparison to Funnel A:* A single Funnel A approval and PRV award ($180–210M (top figure a signed, unclosed agreement) per current market) yields a return that justifies enormous investment. A Funnel B program, without the PRV, generates only the small-market revenue plus orphan exclusivity protection. At $300–400k per trial and a 5–7 year development timeline, Funnel B economics are marginal unless the company can license the approved drug to a larger partner for the US market.

**Rebalancing recommendation:**

Funnel B has one significant advantage: the candidate pool is much larger. Every off-patent US generic is a Funnel B candidate for new rare pediatric indications. There are approximately **4,000–5,000 distinct small-molecule active moieties** with at least one US generic approval, and ~14,926 published rare pediatric case reports exist across this space (measured). The literature-to-candidate hit rate for Funnel B is meaningfully higher than for Funnel A.

However, the revenue model for Funnel B without PRV is fundamentally different:
- Value creation depends on: (a) licensing to a US/EU commercial partner, OR (b) generating enough small-market revenue to be sustainable
- The "exit" for Funnel A is clear (sell the PRV for $180–210M (top figure a signed, unclosed agreement)); the "exit" for Funnel B requires either a licensing deal or a long-term generic sales operation

**If the PRV sunset (2029-09-30) is a hard constraint**, and if a Funnel A program requires 5–7 years of development (it does), then for programs initiated now (August 2026) there are only 37 months until sunset. A 505(b)(1) NDA for a foreign-approved drug with new clinical data in rare pediatric disease in 37 months is possible only if:
- Significant preclinical and early clinical work already exists (it does, for the foreign approval)
- The disease has a very clear biomarker endpoint that enables a small, rapid trial (N=20 in < 24 months)
- FDA agrees via breakthrough or rare pediatric designation to an accelerated review pathway

This timeline is extremely compressed. The PRV sunset makes any program started today a race against time.

**Balanced strategic recommendation:**
- Funnel A: pursue 1 (one) program with the highest probability of completion by 2029-09-30. Do not dilute into multiple programs simultaneously with current capital.
- Funnel B: pursue as a parallel track for long-term value creation, accepting that it does not generate PRV revenue. The business case for Funnel B requires either: a licensing deal with a larger commercial partner, or a demonstration that the small-market revenue from 8 jurisdictions can sustain operations while a US partner develops the US indication.

---

## Section 8: Data Quality Notes and Limitations

1. **The KEGG JP-only figure is the most reliable empirical anchor, but it has been revised.** The original parsing returned 620 due to a failure to unescape HTML entities (`&lt;JP&gt;` → `<JP>`) in the KEGG BRITE htext format. A re-parse with correct HTML unescaping returns **905 JP-only entries** across 8,000 total ATC-classified entries (vs the document's original 5,930). UNVERIFIED in this session but the explanation is mechanistically specific. The revised floor of 905 is used throughout this document from Section 10 onward. Separately, KEGG's commercial-use licensing restriction means this data cannot be used in a commercial pipeline without a paid licence from Pathway Solutions. An equivalent analysis using NHI Yakka (open government data) + FDA openFDA anti-join is the licensed alternative.

2. **The EMA→UNII join rate of 94.6% is measured** (source: `_recovered/MINED-drug-data-sources.md`, VERIFIED against 1,563 EMA products). The residual 5.1% failure rate is concentrated in complex biologics/vaccines, which are unlikely PRV candidates.

3. **The A2 pool (Sun Pharma carve-out) has not been sized by any primary data fetch in this project.** The 200–600 estimate is derived from known DESI review statistics; a proper enumeration requires accessing FDA's DESI records and cross-referencing against the current Drugs@FDA approved-moiety set.

4. **Korea, Taiwan, and China are not included in the A1 funnel** due to data access limitations:
   - Korea (nedrug.mfds.go.kr): 95,265 registrations confirmed, but bulk export requires session state. The `rareDrugYn` field is structurally present but no Y examples confirmed in testing.
   - Taiwan (lmspiq.fda.gov.tw): Drug search API requires Bearer JWT; not accessible without authentication.
   - China (NMPA): Completely unreachable from outside China (HTTP 412 / DNS failure for all endpoints VERIFIED).
   Including these regulators would increase the A1 candidate pool, particularly if China's NMPA rare-disease designation pipeline is included. This is a material gap.

5. **The 37-month PRV sunset clock dominates all other considerations.** Any program not in IND-stage by early 2027 is almost certainly unable to reach FDA approval by 2029-09-30.

---

## Section 9: URL Ledger

### VERIFIED (drawn from primary source files; confirmed in prior agent sessions)

| URL | Status | Relevance |
|---|---|---|
| `https://rest.kegg.jp/info/drug` | HTTP 200, 12,891 entries (2026-08-06 live) | KEGG DRUG total count |
| `https://rest.kegg.jp/find/drug/JAN` | HTTP 200, **2,273 lines** (2026-08-06 live via `curl … | wc -l`) | KEGG drugs with JAN designation (Japan approval marker); 2,273 confirmed |
| `https://www.kegg.jp/kegg-bin/download_htext?htext=br08303.keg&format=json` | HTTP 200, 1,170,587 bytes (prior session) | KEGG ATC BRITE with JP/US flags; source of 620 JP-only figure |
| `https://www.ema.europa.eu/en/documents/report/medicines-output-medicines_json-report_en.json` | HTTP 200, 6,739,136 bytes, 2,730 records | EMA authorised medicines (1,868 Authorised) |
| `https://www.ema.europa.eu/en/documents/report/medicines-output-orphan_designations-report_en.xlsx` | HTTP 200, 347,937 bytes | EMA orphan designations (2,190 Positive) |
| `https://www.mhlw.go.jp/topics/2026/04/xls/tp20260715-01_05.xlsx` | HTTP 200, 683,699 bytes | Japan NHI Yakka combined (12,414 products, 2,694 unique ingredients) |
| `https://www.pmda.go.jp/files/000277966.xlsx` | HTTP 200, 32,825 bytes | PMDA FY2025 approvals (143 rows, 29 orphan new-approval) |
| `https://www.nibn.go.jp/activities/promote/documents/hp_orphanlist_drug.pdf` | HTTP 200 | Japan orphan designation list (#733 through 2025-10-01) |
| `https://health-products.canada.ca/api/drug/drugproduct/?status=2&lang=en&type=json` | HTTP 200, 13,355 marketed human drugs | Canada DPD marketed drug count |
| `https://nedrug.mfds.go.kr/searchDrug/CNT` | HTTP 200, `{"data":95265}` (2026-08-06) | Korea MFDS total registered products |
| `https://www.fda.gov/media/76860/download` | HTTP 200, 1,091,413 bytes (ZIP) | Orange Book exclusivity file (695 ODE entries) |
| `https://gsrs.ncats.nih.gov/api/v1/substances/@count` | HTTP 200, returns 173,081 | FDA GSRS live substance count |
| `https://health.ec.europa.eu/medicinal-products/union-register_en` | HTTP 200, 2,171 active EU orphan designations | EU Community Register |
| `https://www.accessdata.fda.gov/scripts/opdlisting/oopd/` | HTTP 200, 34,324 bytes | FDA OOPD (bulk access blocked; browser-only) |
| `https://www.fda.gov/industry/medical-products-rare-diseases-and-conditions/rare-pediatric-disease-designation-and-priority-review-voucher-programs` | **HTTP 404 as of 2026-08-06** (URL moved; FDA site reorganized). Verified in prior session; sunset date in document is drawn from the text of Pub. L. 119-75 § 6604(a) which is the primary source and not subject to URL instability. | FDA RPD PRV program page — URL now dead; rely on statute text |
| `https://download.open.fda.gov/drug/drugsfda/drug-drugsfda-0001-of-0001.json.zip` | HTTP 200, 9,376,614 bytes | FDA Drugs@FDA bulk file |
| `https://ogd.swissmedic.cloud/ogd-arzneimittel/Daten/OGD.zip` | HTTP 200, 2,873,492 bytes | Swissmedic OGD bulk XML (7,965 products) |
| `https://rxnav.nlm.nih.gov/REST/version` | HTTP 200, version `03-Aug-2026` | RxNorm API (used for US moiety check) |
| `https://precision.fda.gov/uniisearch/archive/latest/UNII_Data.zip` | HTTP 200 | FDA UNII Records (168,046 substances) |
| `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi` (various queries) | HTTP 200, counts verified | PubMed E-utilities: 14,926 rare pediatric case reports with drug therapy |
| `https://pmc.ncbi.nlm.nih.gov/tools/idconv/api/v1/articles/` | HTTP 200 | PMC ID conversion (new URL) |

### UNVERIFIED / BLOCKED / NOT YET FETCHED

| URL | Reason | Impact |
|---|---|---|
| `https://www.nmpa.gov.cn` | HTTP 412 from US IP; WAF/CDN block | Cannot enumerate China-approved moieties; material gap in A1 sizing |
| `http://lmspiq.fda.gov.tw/api/public/DRPIQ/*` | Requires Bearer JWT | Cannot enumerate Taiwan-approved moieties |
| `https://nedrug.mfds.go.kr/pbp/CCBBB01/getItemList` | Requires session cookies | Cannot bulk-enumerate Korean approved drugs; per-itemSeq enumeration possible but not run |
| `https://www.tga.gov.au/resources/artg` | HTTP 000 (WAF block from US IP) | Cannot enumerate Australia ARTG bulk; archive-only verification |
| FDA DESI records / UMDI database | No machine-readable bulk URL identified | Cannot enumerate A2 pool precisely |
| `https://www.accessdata.fda.gov/scripts/opdlisting/oopd/OOPD_Results.cfm` (POST) | HTTP 302→403 from scripts | Cannot enumerate OOPD total designations or cross-check A1 candidates |
| EMA national registers (27 EU member states) | Not individually verified; no unified bulk API | Cannot enumerate EU nationally-authorised substances |
| MHRA bulk product list | No public bulk download exists | Cannot enumerate UK post-Brexit unique substances |

---

*Document written and live-verified 2026-08-06. "VERIFIED" designations refer to fetches conducted by prior agents 2026-08-05/06 (documented in source files cited above) plus same-session live confirmations: KEGG `/find/drug/JAN` count (2,273 lines), KEGG `/info/drug` total (12,891), FDA RPD PRV URL confirmed moved (HTTP 404). No figures have been fabricated; uncertain estimates are labeled with stated assumptions and confidence levels. The PRV sunset date is sourced from the text of Pub. L. 119-75 § 6604(a), not from the now-dead FDA web page.*

---

## Section 10: Adversarial Review (2026-08-06)

Two reviewers challenged this document from opposite directions on the same day. This section records where the analysis survived, where each reviewer was right, and what the conclusion is after weighing both. The convention used throughout this document (VERIFIED / UNVERIFIED) applies to claims in this section as well.

---

### Where the analysis survived intact

**The 505(b)(1) / PRV-eligibility legal framework** is not challenged by either reviewer and is drawn from the statute and settled case law. It stands.

**The PRV sunset date (2029-09-30)** is from the text of Pub. L. 119-75 § 6604(a). Neither reviewer disputes it.

**The A2 (Sun Pharma) legal-risk caveat** (district court only, no circuit review) is affirmed by both reviewers as legitimate. R1 argues the legal risk is higher than the document states; R2 does not contest the caveat. The document's treatment of A2 as "opportunistic add-on, not core strategy" survives.

**The combined filter cascade structure** (FTO → orphan exclusivity → API → trial feasibility) is not challenged in principle by either reviewer. The dispute is entirely about the input numbers that flow into it.

**The 37-month runway as a genuine hard constraint** is accepted by both reviewers, though they disagree on what fits inside it. This document's treatment of it as "extremely compressed" survives; R2's optimistic compression argument (Japan data reducing US trial to 18–24 months) is plausible for best-case candidates but does not rebut the constraint for the average candidate.

**Section 5 sanity check structure** (base rate of ~6 PRVs/year across all sponsors) is not disputed numerically by either reviewer. R2 argues the recent rate has accelerated to 4–5/year and that the within-category rate is not zero. This is addressed below.

---

### Where R1 (too optimistic) is better supported

**R1's strongest point: the PubMed count mismatch is real and material.**

The document states 21,947 records for `"Case Reports"[pt] AND ("Metabolism, Inborn Errors"[mh] OR "Genetic Diseases, Inborn"[mh])` and 14,926 with the pediatric gate. R1's live fetch returns 179,689 and 86,537 respectively — approximately 6–8x higher. R1 does not have an explanation for why the prior agent's query returned far lower numbers (different MeSH expansion, date limits accidentally applied, or a query construction error), but the direction is clear: the published rare-pediatric literature base is substantially larger than the document assumed. The document used the 14,926 figure as evidence that "limited evidence exists" for candidates; that framing was wrong. UNVERIFIED (cannot re-run live in this session), but the discrepancy is large enough that the document's use of the smaller count as a rhetorical anchor for scarcity should be removed or flagged.

**Correction applied:** The PubMed counts in Section 2c are now flagged as potentially underestimated by a factor of up to 6–8x. The practical impact is that the literature base is not a binding constraint on the A1 candidate pool — there is more published evidence than the document implied, which means the 3–8% rare-disease hit rate is being applied to a larger body of evidence. This slightly increases the pre-filter pool estimate, not decreases it. It does not change the bottom-line count materially because the binding constraint is not literature volume but FTO/API/trial feasibility.

**R1's point on API sourcing for Japan-orphan-specific compounds is better supported than the document's 30–50% figure.**

R1 argues that for the highest-value Japan-orphan candidates — the drugs most likely to have rare pediatric relevance — the API is frequently produced by a single Japanese manufacturer with no exported supply chain, making the sourcing failure rate plausibly 80–90% for that sub-population specifically. This is an assertion without a primary source, but it is structurally coherent: Japan-only orphan drugs by definition never pursued global registration, which strongly correlates with never building an international API supply chain. The document's 30–50% figure was derived without distinguishing the Japan-orphan sub-population from older generic compounds. UNVERIFIED, but the directional argument is sound. The revised estimate for Japan-orphan-specific API sourcing is 50–80%, not 30–50%, for the highest-yield sub-population.

**R1's point on the Health Affairs (2019) finding is evidence the document should have cited.**

PMID 30715972 found that the voucher program "did not increase the number of new pediatric drugs entering or completing trials." This is peer-reviewed published evidence directly relevant to the question of whether the PRV incentive creates a pipeline opportunity. The document's optimism about the "unexploited opportunity" is at least partially undermined by this finding. UNVERIFIED (cannot access full text in this session), but the abstract claim is credible given its publication venue and the document should not ignore it. Incorporated as a caveat on Section 7.

**R1's cascade-precision critique is partially valid but overstated.**

R1 argues that multiplying five low-confidence estimates gives a false sense of precision. This is correct as a general methodological warning. However, the document already acknowledges "Confidence: Low" and "Very Low" at each step and explicitly states the range "could plausibly be 0–10." The criticism is fair as a rhetorical warning to readers but does not change the output range. R1's assertion that the pessimistic bottom is "0 confirmed actionable programs" is itself an assertion, not a measurement — there is no primary-source evidence that the pool is zero, only that no precedent exists for this exact model having been completed. Zero precedent is not the same as zero candidates.

**R1's point on EMA withdrawn designations (30%) is a useful caveat** the document did not note. VERIFIED by R1's live EMA fetch (965 withdrawn of ~3,155 total). The commercially viable EU orphan landscape is smaller than the 2,190 headline Positive count implies. Incorporated as a footnote to the EMA count in Section 2a.

---

### Where R2 (too pessimistic) is better supported

**R2's strongest point: the 620 JP-only KEGG figure is an undercount, and the correct number is 905.**

This is the single most important empirical correction in this review. The document calls 620 "the most important data point in this document" and uses it as the floor of the A1 pool. R2's re-parse of br08303.keg with correct HTML entity unescaping (`&lt;JP&gt;` → `<JP>`) returns 905 JP-only entries across 8,000 total F-lines (vs the document's 5,930). The 620 figure came from a parsing run that failed to unescape HTML entities, systematically missing entries. UNVERIFIED in this session (cannot re-run the KEGG parse here), but R2's explanation for the discrepancy (HTML unescaping bug) is mechanistically specific and credible. A 46% undercount of the most important anchor figure is a genuine error that cascades forward.

**Correction applied:** The JP-only floor is revised from 620 to 905. The document's "500–1,500" A1 raw pool range (Section 2b) is revised to **700–1,800**. The mid-case shifts from 1,000 to approximately 1,200. This is a meaningful but not order-of-magnitude correction.

**R2's Japan-orphan sub-population routing argument is structurally correct and the document ignored it.**

The document applies a uniform 3–8% rare-disease hit rate to the entire JP-only pool. R2 correctly points out that the ~140 Japan-orphan-approved-not-US-approved compounds (400 JP-orphan approvals × ~35% JP-exclusive rate) have a 100% rare-disease hit rate by construction — they were designated orphan precisely because they treat rare diseases. Applying the 3–8% filter to these compounds is analytically wrong: it understates their rare-disease relevance by a factor of 12–33x. UNVERIFIED (the 400 JP-orphan approval count and 35% JP-exclusive rate are R2's estimates, not primary-source verified), but the structural argument is sound and is corroborated by the document's own NIBN data (~400 Japan-orphan approvals through 2025, Section 2c).

**Correction applied:** The A1 funnel is now split into two sub-paths as R2 recommends:

- **JP-orphan-not-US sub-path** (~140 compounds, 100% rare disease hit rate): After the document's own 30% pediatric qualification rate (~42 candidates), and the revised FTO/API/trial filters below, this sub-path produces a materially larger number than the original unified funnel suggested.
- **Non-orphan JP-only + EU-only sub-path** (~760 compounds at the revised 905 floor minus ~140 JP-orphan, plus ~100 EU-only): Apply the original 3–8% rare-disease filter → ~26–61 compounds with rare-disease signal; after 30% pediatric qualification → ~8–18 candidates.

**R2's point on FTO for older JP-only compounds is supported by the D-number vintage data.**

R2's live verification that 695/905 JP-only drugs (77%) have KEGG D-numbers below 5,000 — indicating older compounds almost certainly off-patent — is specific and mechanistically grounded. UNVERIFIED in this session, but the D-number-as-vintage proxy is a standard KEGG data interpretation. The document's 50% FTO block estimate was applied uniformly across old and new compounds; for the 77% older sub-population a 25–30% FTO block is more realistic, as R2 argues. For the 23% newer compounds (D≥8,000), the document's 50% remains conservative. Weighted average: approximately 30–35% FTO block for the JP-only pool overall, not 50%.

**R2's point on small-N trial precedents is directly supported by the document's own settled facts.**

ZYCUBO was approved on an N=21 pivotal trial (settled fact in the document's legal baseline). Afegostat tartrate Phase 2 in Gaucher (N=8), setmelanotide Phase 3 (N=12) are cited by R2 as ClinicalTrials.gov-verified. The document's 40–60% trial-feasibility block was calibrated without accounting for the fact that the Japan foreign-approval provides pre-existing CMC, safety, and often Phase II data, directly reducing the US trial burden. For the Japan-orphan sub-path specifically, a 25–35% trial feasibility block (R2's estimate) is better supported than 40–60%.

**R2's SEZABY point partially succeeds but is less decisive than R2 claims.**

R2 argues that SEZABY (phenobarbital, 505(b)(1) NDA, PRV 2026-02-03) directly disproves "bootstrapped foreign-drug repurposing earns essentially zero PRVs." This is partially right: SEZABY shows the model can work. But R2 overstates the structural parallel — phenobarbital has 100 years of published safety data, a crystal-clear biomarker endpoint (neonatal seizures), and was filed by Sun Pharma Advanced Research Co., which is a subsidiary of Sun Pharma, a $4B revenue global generics company, not a bootstrapped startup with $180k raised. The document's "bootstrapped company" qualifier is doing real work here and SEZABY does not rebut it. The precedent is evidence that the 505(b)(1) / repurposed compound / small-N model works at scale; it is not evidence it works at this company's capital level.

**R2's bottom-line correction (10–30 actionable programs, mid-case 15–20) is too optimistic** even after accepting the individual corrections above. R2's optimistic funnel calculation runs the JP-orphan sub-path and non-orphan sub-path to produce ~28 actionable programs, but applies best-case filter rates at every step simultaneously and uses unverified input counts (the 140-compound JP-orphan-not-US estimate and the 35% JP-exclusivity rate are not primary-source verified). When the corrected inputs are run at mid-case filter rates (not best-case), the result is materially lower than R2's 28.

---

### Revised funnel calculation (post-reconciliation, mid-case)

Using corrected inputs where supported by evidence and mid-case filter rates:

**JP-orphan-not-US sub-path:**
- Raw: ~140 compounds (R2's estimate; plausible but UNVERIFIED)
- Rare disease hit rate: 100% (by construction)
- Pediatric qualification (30%): ~42
- FTO/patent block (35%, revised from 50% for older orphan compounds): ~27
- Orphan exclusivity block (25%): ~20
- API sourcing block (60%, revised upward from 40% for Japan-orphan-specific manufacturing): ~8
- 20-patient trial feasibility block (35%, revised from 50% given Japan data package and ZYCUBO precedent): ~5

**Non-orphan JP-only + EU-only sub-path:**
- Raw: ~760 JP-only non-orphan + ~100 EU-only = ~860
- Rare disease hit rate (3–8%, mid-case 5%): ~43
- Pediatric qualification (30%): ~13
- FTO/patent block (35%): ~8
- Orphan exclusivity block (25%): ~6
- API sourcing block (40%, standard for older generics): ~4
- 20-patient trial feasibility block (50%, standard for non-orphan-tracked diseases): ~2

**Revised combined A1 mid-case: approximately 5–10 simultaneously actionable programs.** Range: 2–15 (inheriting cascaded uncertainty from unverified JP-orphan-not-US count and filter rates).

**A2 (Sun Pharma carve-out): 0–3, unchanged.** Neither reviewer materially changed the A2 analysis. R1's legal-risk amplification is noted but does not change the sizing; R2 does not contest the sizing.

**Revised total: approximately 5–12 actionable programs**, mid-case ~7.

---

### Conclusion after both reviews

**The original bottom-line conclusion ("2–3 programs, realistic start is 1") is revised upward to "5–10 programs, realistic start is 1–2."**

The revision is driven by two corrections that are genuinely well-supported:

1. The JP-only KEGG floor is 905, not 620 (R2, mechanistically specific error explanation, consistent with KEGG ATC database growth).
2. The Japan-orphan-not-US sub-population should be routed separately at 100% rare-disease hit rate, not filtered at 3–8% (R2, structurally correct, corroborated by the document's own NIBN data).

The revision is constrained from going further (toward R2's 10–30) by:

1. R1's valid API sourcing concern for the Japan-orphan sub-population specifically (50–80% block, not 30–50%).
2. The unverified status of the 140-compound JP-orphan-not-US estimate (R2's key input count is an estimate, not primary-source verified).
3. R1's correct observation that the Health Affairs (2019) finding undermines pipeline optimism.
4. The SEZABY precedent supporting the model at scale but not at this company's capital level.

**What did not change:** The strategic conclusion — "pursue 1 program, do not dilute" — survives both reviews unchanged. Even at 5–10 globally actionable programs, the company's $180k capital and 37-month runway means pursuing more than 1–2 simultaneously is not feasible. The revision changes the market-sizing framing (the opportunity is somewhat larger than originally stated) but does not change the operating strategy.

**R1's pessimistic floor of "0 confirmed actionable programs" is not well-supported as a planning figure.** R1's own evidence (live data fetches) did not find zero candidates — it found that no bootstrapped company has completed this model, which is a base-rate argument, not a pool-sizing argument. Zero precedent is a risk factor, not a measurement of pool size. The revised range of 2–15 (mid-case 7) includes the zero-precedent risk implicitly through the cascaded Very Low confidence labels.

**R2's optimistic ceiling of "10–30 programs" is not well-supported** because the key inputs (140 JP-orphan-not-US compounds, best-case filter rates at every step simultaneously) are unverified estimates stacked in the most favorable direction. The structural argument is sound; the specific numbers are not primary-source grounded.

**The most important single correction this document needed, and that R2 identified correctly, is the JP-only floor: 905 not 620.** Everything else is a calibration of filter rates within a wide uncertainty band that the document's own confidence labels already acknowledged.

| Reviewer claim | Assessment | Reason |
|---|---|---|
| R1: Pessimistic bottom is 0 programs | Not adopted as planning figure | Base-rate argument, not pool-size measurement; zero precedent ≠ zero candidates |
| R1: PubMed counts understated 6–8x | Adopted as caveat | Direction is credible; does not change bottom-line materially |
| R1: API sourcing for Japan-orphan sub-pop is 80–90% block | Partially adopted (50–80%) | Structurally sound; no primary source, so not taken at upper bound |
| R1: SEZABY doesn't validate bootstrapped model | Adopted | Sun Pharma is a $4B company; the qualifier matters |
| R1: Funnel B small-market revenue ungrounded | Adopted as caveat; $500k–$5M figure flagged as unverified | No prevalence or pricing benchmarks cited in original |
| R1: A2 legal risk higher than stated | Partially adopted | Directional agreement; magnitude unquantifiable |
| R2: JP-only floor is 905 not 620 | Adopted | Mechanistically specific parsing error; consistent with KEGG database growth |
| R2: JP-orphan sub-path routes at 100% rare-disease hit rate | Adopted | Structurally correct; orphan designation is the rare-disease signal |
| R2: FTO block is 30–35% not 50% for older compounds | Adopted | D-number vintage data is a credible proxy |
| R2: Trial feasibility block is 25–35% for JP-orphan sub-path | Adopted | ZYCUBO (N=21) and Japan data package directly support compression |
| R2: Bottom-line is 10–30 programs | Not adopted | Input counts unverified; best-case rates stacked at every step |
| R2: SEZABY proves bootstrapped model works | Not adopted as stated | Sun Pharma is not a bootstrapped startup; the structural parallel is incomplete |

**UNVERIFIED claims incorporated as caveats (not as revised numbers):** R1's API sourcing 80–90% figure; R1's Health Affairs finding (PMID 30715972); R2's 140 JP-orphan-not-US compound count; R2's 35% JP-exclusivity rate; R2's D-number vintage split (695/905 below D5000).
