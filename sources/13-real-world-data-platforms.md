<!-- RECOVERED from subagent transcript agent-a5b2edbbc4e87517f.jsonl, session fd64561f-7c90-41a2-95cf-b4a133a8fe0f, research date 2026-08-05.
     RWD platforms for patient counting and external control arms.
     Verbatim agent deliverable — not re-edited. -->

I have what I need. Compiling the findings.

## Real-World Data Platforms for Rare Disease Patient Counting & External Control Arms

**Research date:** 2026-08-05. Every URL below was actually fetched; status marked VERIFIED / VERIFIED (JS app — resolves but content is client-rendered) / DEAD / BLOCKED (403 anti-bot, page exists).

---

### 0. First, the math that determines everything

For a **1-in-100,000** disease, US true prevalence ≈ **3,350 people**. In a database of N patients you'd naively expect `N/100,000` cases:

| Database | N | Naive expected cases |
|---|---|---|
| Komodo Healthcare Map | 330M | ~3,300 |
| Epic Cosmos | 310M | ~3,100 |
| HealthVerity | 270M+ | ~2,700 |
| Truveta (EHR) | 130M | ~1,300 |
| TriNetX US Collaborative | 117M | ~1,170 |
| Optum Clinformatics | 67–126M | ~670–1,260 |
| N3C | ~21M | ~210 |
| PCORnet | 50M/yr | ~500 |
| All of Us | 883K | **~9** |

**Three corrections that matter more than N:**

1. **The ICD-10 coding wall.** Only a few hundred of ~7,000+ rare diseases have specific ICD-10-CM codes. Pure-claims databases (Komodo, Optum, MarketScan, HealthVerity) are ICD-10-only — if your disease has no code, its 330M patients are worth nothing to you. **SNOMED-CT-coded EHR sources are dramatically better.** The N3C rare disease phenotyping work needed **12,081 SNOMED-CT codes vs only 357 ICD-10 codes** to cover 6,342 rare diseases — a ~34:1 ratio. This single fact should drive your platform choice more than N.
2. **Diagnosed ≠ prevalent.** For most rare diseases diagnosed prevalence is 10–50% of true prevalence.
3. **Denominator inflation.** TriNetX's 110M "Dataworks-USA" patients include duplicates across institutions; only ~72M had an encounter in the last 5 complete years. Truveta/Komodo counts are similarly cumulative.

**Practical floor:** below ~50M patients you cannot reliably count a 1-in-100,000 disease. **All of Us is disqualified for patient counting** (~9 expected cases, and the Data Browser rounds all counts up to 20, so 8 patients displays as 20).

---

### 1. N3C — National *Clinical* Cohort Collaborative

**URLs**
- `https://ncats.nih.gov/research/research-activities/n3c/overview` — VERIFIED
- `.../n3c/data-overview` — VERIFIED · `.../n3c/faqs` — VERIFIED
- `.../n3c/data-overview/access` — VERIFIED (5-step process) · `.../n3c/resources/data-access` — VERIFIED (DUA template)
- `https://n3c.ncats.nih.gov/` — VERIFIED (JS app) · `https://covid.cd2h.org/` → 301-redirects here
- ⚠️ `https://covid.cd2h.org/onboarding` and `/dur/` — **DEAD (404)**. Widely-cited old docs; don't send anyone there.

**🚩 It was renamed and restructured — this is the headline.** The August 2025 NCATS factsheet (VERIFIED, read directly) states N3C is *"currently available to support research on three diseases: cancer, renal disease and Long COVID."* Future expansion is planned into *"diabetes, Alzheimer's disease and chronic or rare pediatric diseases."* The old open ~21M-patient COVID enclave is now disease-specific tenants (N3C Cancer, N3C Renal, N3C Long COVID, N3C Education). **Unless your disease is renal, oncologic, or Long-COVID-adjacent, N3C is probably not currently open to your question.** Confirm directly with `NCATS_N3C@nih.gov`.

**Data:** OMOP CDM — demographics, labs, procedures, meds, conditions, physical measurements. Privacy-preserving linkage to CMS claims, cancer/kidney registries. Three levels: **Synthetic** (computationally derived, no real patients), **Limited Data Set** (real dates of service + patient ZIP), **De-identified** (date-shifted, 3-digit ZIP truncation).

**Industry access: YES — explicitly.** The FAQ (VERIFIED) names *"researchers from industry"* among eligible users, alongside nonprofits, health departments, and citizen scientists. Contributing data is **not** required to access.

**Process (VERIFIED, 5 steps):** (1) Institution executes a DUA with NCATS — signed by an Authorized Institutional Official, binds all users, one DUA covers unlimited projects; (2) register; (3) log in; (4) NIH infosec training (60–90 min) + human-subjects training for LDS/de-identified; (5) submit a Data Use Request → reviewed by the federal Data Access Committee.

**Timeline:** ~**15 business days** DUR→workspace (10 for DAC review + 3 for setup). The institutional DUA is the slow part (weeks–months of legal).

**Cost: FREE.** The FAQ states plainly: *"No fee will be charged."*

**Enclave constraint — hard:** *"Data cannot be downloaded from this enclave or be removed."* All analysis stays in the NCATS cloud. DURs valid 1 year, renewable.

**Rare disease:** No standing "N3C+RARE" domain team found under that name — N3C uses topic-based Domain Teams. But the rare disease work is real and published: a phenotyping workflow mapping GARD/ORPHANET→SNOMED-CT/ICD-10 produced **12,081 SNOMED-CT + 357 ICD-10 codes covering 6,342 rare diseases across 30 ORPHANET classes**, applied to **21M+ N3C patients**; **316,836 (6.55%)** of COVID-positive patients had a preexisting rare disease. That codeset is the single most reusable artifact here — **harvest it regardless of which platform you buy.**

---

### 2. All of Us Research Program

**URLs**
- `https://www.researchallofus.org/` — VERIFIED · `/data-tools/data-access/` — VERIFIED
- `https://www.researchallofus.org/institutional-agreements/` — VERIFIED
- `https://databrowser.researchallofus.org/` — VERIFIED (JS app) — **public, no login**
- `https://orau.org/allofus/documents/dura-process-infographic.pdf` — VERIFIED (read directly)
- `https://allofus.nih.gov/`, `support.researchallofus.org` — BLOCKED (403 anti-bot; pages exist)

**Scale:** ~**883,000** enrolled; **535,000+ whole genome sequences**, ~482,000 linked to EHR. Largest integrated genomics+health database in the world — and still **far too small for rare disease counting**.

**Tiers (VERIFIED):** **Public** (aggregate, Data Browser, no login) → **Registered** (individual-level EHR, wearables, surveys, physical measurements) → **Controlled** (adds genomic sequences/arrays, unsuppressed demographics, unshifted dates).

**🚩 The DURA gotcha — I found a genuine contradiction, flagging it honestly.** The official All of Us DURA infographic (hosted at orau.org/allofus, read directly) states verbatim: *"Currently, academic, not-for-profit, and health care organizations can enter into a DURA."* For-profits are **not** listed.

**But** the live registered-institutions page (1,457 institutions) demonstrably contains for-profit companies: **Eli Lilly, AstraZeneca, Biogen, Gilead, Google, Illumina, Abbott, AbbVie, Amgen, Bayer, Bristol Myers Squibb, Calico Life Sciences.**

Most likely reading: the infographic is stale (it references an era of ~556 institutions, ~Aug 2023; the list now shows 1,457) and industry access has since opened. **But every for-profit I could confirm is large-cap.** Treat this as: *submit a DURA request and find out; do not build a plan around it.* Individual researchers cannot self-sign — it requires an institutional signing official, routed through the Data and Research Center at Vanderbilt.

**Cost:** No fee to register. Compute in the Workbench is credit-based; heavy genomic work can incur real cloud cost.

**Verdict:** Useless for counting a 1-in-100,000 disease. **The Data Browser is still worth 20 minutes** — public, no login, no agreement — for a fast free sanity check on whether your condition's concept codes even appear in structured EHR data.

---

### 3. TriNetX — the actual answer for cohort counting

**URLs:** `https://trinetx.com/` — VERIFIED · `/data/` — VERIFIED · `/solutions/` — VERIFIED · `/solutions/trinetx-live/` — VERIFIED · `https://trinetx.com/real-world-data-network/` — **DEAD (404)**

Peer-reviewed corroboration: `https://pmc.ncbi.nlm.nih.gov/articles/PMC12414656/` (Dataworks-USA, *Pharmacoepidemiol Drug Saf* 2025) — VERIFIED; `https://www.frontiersin.org/journals/pharmacology/articles/10.3389/fphar.2025.1516126/full` — VERIFIED.

**Federated model:** *"Your query moves. Your patients' data doesn't."* Patient-level data stays behind each HCO's firewall; queries run locally and return aggregate counts. This is why cohort counting is instantaneous and needs no IRB.

**Networks (from the peer-reviewed review, Sept 2024 — more reliable than marketing pages):**

| Network | Patients | HCOs |
|---|---|---|
| Global Collaborative | 153.5M | 128 (17 countries) |
| **US Collaborative** | **117.2M** | **66** |
| LATAM Collaborative | 31.5M | 32 |
| EMEA Collaborative | 19.2M | 26 |
| APAC Collaborative | 5.1M | 14 |

**Dataworks-USA** (the licensable dataset product): **110M+ patients**, ~**72M** with an encounter in 2019–2023, **65 US HCOs**, ~75% academic medical centers. Mean **6.2 years** first-to-last encounter; ~75 diagnoses, ~150 medication records, 270+ labs/procedures per patient. Refreshed ~every 2 weeks. Population skews ~5 years older than US Census (43.9 vs 39.1) and 53% female. Also a **Linked** network tokenizing US EHR to closed claims + death data.

Homepage aggregate claims: 309M+ patient lives, 14,200+ clinical sites, 65M+ linkable patients, 99B+ data points, 4,000+ publications.

**🚩 Access model — the key asymmetry (VERIFIED in the Frontiers review):** *"Access to TriNetX is either by commercial licensing agreement (industry) or by collaboration agreement (academia)."* **TriNetX is free to academics and paid for you.** No published price. Signals gathered: dataset licenses grant rights for **1 year with quarterly refreshes**; pricing varies by therapeutic-area scope, network coverage, query volume, and AI modules. Expect **five to low-six figures** for a scoped rare-disease dataset license; the browse/count tier is far cheaper than a full extract.

**The workflow you actually want:** Query Builder → define cohort by ICD-10/SNOMED/RxNorm/LOINC/genomics → get **live patient counts globally, by region, and by individual HCO**. That last part is the trial-feasibility gold: it tells you *how many patients and at which sites*, which converts directly into a site list. Industry uses it precisely to *"challenge feasibility of in- and exclusion criteria."*

**⚠️ Export constraint:** data download capability varies by jurisdiction — GDPR/LGPD substantially restrict bulk extract outside the US. **Large-scale downloadable datasets are essentially a US-only capability.**

**Cheapest legitimate path:** partner with an academic collaborator at a TriNetX member AMC. They have free access and can run feasibility counts. This is common practice and can answer your counting question for ~$0.

---

### 4. Truveta

**URLs:** `https://www.truveta.com/` — VERIFIED · `/life-sciences/` — VERIFIED · `/members/` — VERIFIED · Azure Marketplace listing — BLOCKED (403; pricing below from search index, **UNVERIFIED**)

**Model:** Health-system-*owned* collective — **30 US health systems**, **900+ hospitals**, **~20,000 clinics**. Members: Providence, Trinity, Tenet, Advocate, CommonSpirit, Northwell, AdventHealth, Ochsner, Sanford, MedStar, Memorial Hermann, Novant, Sentara, Texas Health, Henry Ford, Inova, HealthPartners and others.

**Data:** **130M+ de-identified patients** (EHR), updated **daily**; **200M+ patients** of linked commercial/Medicare/Medicaid closed claims (added Feb 2025); **7B+ clinical notes**; **100M+ medical images**; plus SDOH, maternal-child, multiomics/genomics, mortality, device data. Notes + images are the real differentiator — for rare diseases lacking ICD codes, **NLP over clinical notes may be the only way to find patients**.

**Access:** Truveta Studio (analytics environment) + Truveta Embassy (bring-your-own sensitive data, SOC2, de-identified and linked to Truveta Data). A **Truveta Data subscription is required** to use Studio; health-system members are exempt. 60+ customers across life sciences, government, health systems, academia. Explicitly supports **regulatory submissions to FDA** with read-only verifiable regulatory exports — directly relevant to external control arms.

**💰 Pricing (best public figure found):** Azure Marketplace lists Truveta Studio/Embassy **usage reservations at $95,000 / $245,000 / $495,000**, valid one year — **and the underlying Truveta Data subscription is *not* included.** So realistic all-in is **well north of $100K/yr**. UNVERIFIED (403); treat as directional but it's the only public number that exists.

**Small company?** Technically yes, practically strained. Entry cost likely exceeds a small repurposing company's entire RWD budget.

---

### 5. Komodo Health

**URLs:** `https://www.komodohealth.com/` — VERIFIED · `/solutions/maplab/` — VERIFIED · MapEnhance press release — VERIFIED

**Healthcare Map:** **330M+ de-identified patients**, **1T+ linked records**, daily refresh. Primarily **closed + open claims**, patient-journey-linked across providers/payers.

**Products:** **MapLab** (analytics platform: MapView no-code, MapExplorer discovery, MapAI natural-language querying), **Sentinel** (custom high-code analytics in a compliant cloud), **Prism** (ML), **MapEnhance** (specialty data overlays: oncology, rare disease genomics, lab, SDOH, mortality), **Marmot** (AI layer).

**Rare disease — genuinely a marketed strength:** MapExplorer explicitly supports rare disease patient populations. MapEnhance integrates a **GeneDx** partnership contributing a de-identified rare disease genetic dataset from **600,000+ exomes and genomes** — meaningful, because genetic testing data can identify patients whose ICD-10 record is uninformative. Komodo also runs a program supplying Prism free to rare disease advocacy organizations in the CZI **Rare As One** Network.

**Access:** No published pricing anywhere; demo/sales-gated. Enterprise SaaS aimed at pharma commercial/RWE teams. Expect **six figures annually**. 

**💡 Non-obvious cheap path:** if a patient advocacy organization exists for your disease and is in the Rare As One network, they may already hold Komodo access. Partnering with them can be far cheaper than licensing.

---

### 6. The realistic cheap alternatives

**Optum Clinformatics Data Mart** — `optum.com/.../Clinformatics_for_Data_Mart.pdf` — VERIFIED (read directly). Commercial + Medicare Advantage claims. Product sheet confirms member/eligibility, medical claims (CPT-4, ICD-9/10, DRG), pharmacy (NDC), **lab results (LOINC, numeric + text)**, inpatient confinement, provider data, linked SSA Death Master File mortality; optional SDOH, 5-digit ZIP, **OMOP format**, and EHR linkage. Data from 2007. Size reports vary **63M–126M** depending on cumulative vs active. Licensed data — **you receive files** (not an enclave), which is a major advantage for building your own control arms. Academic site licenses exist and are far cheaper than commercial.

**Merative MarketScan** (formerly IBM/Truven) — Commercial Claims (2005–2023, **>200M cumulative lives**, ~350 payers, 20B+ service records) + Medicare Supplemental (**12.9M** retirees). The **longest longitudinal claims history available** — best value for characterizing multi-year disease natural history in a coded disease. Widely available through university site licenses. **Non-obvious cheap path:** many academic medical centers hold institutional MarketScan/Optum licenses; a collaboration can get you analyses for near-zero.

**HealthVerity** — `healthverity.com/marketplace/data-ecosystem/` — VERIFIED. **270M+** de-identified lives, **75+ data sources**, 10 data types (closed/open medical claims, pharmacy, EHR, lab — ~65% of the US lab market — consumer, SDOH, mortality). Marketplace model: license *only the slice you need* under a **single contract (IPGE)**, delivered in **<2 weeks**. **This à-la-carte structure is the single most small-company-friendly commercial model in this list** — you're not buying a whole enterprise platform.

**Datavant** — `datavant.com/` — VERIFIED. **Not a dataset — it's the plumbing.** Privacy-preserving tokenization for linking datasets without sharing PII. 1T records tokenized/yr, 80,000+ hospitals/clinics, **350+ RWD partners**, 75% of top-100 health systems, 100% of US payers. Relevant to you only if you need to link your own trial/registry data to external RWD — which is exactly what building an external control arm requires.

**Epic Cosmos** — `cosmos.epic.com/about/` — VERIFIED · `/request-access/` — VERIFIED (JS app). **310M patients**, **2,198 hospitals**, **49,300 clinics**, 594,000 physicians, **21.6B encounters**. Rich EHR incl. SDOH and birth records. **🚩 CONFIRMED CLOSED TO YOU.** Verbatim from Epic: access is limited to those *"affiliated with and approved by a Cosmos participating organization,"* and *"access to Cosmos and Cosmos data cannot be purchased."* Participation requires running Epic. Basic users get aggregate SlicerDicer analysis; line-level SQL access requires extensive Epic training. **The only route is a collaborator at an Epic health system** — and even then, no data leaves. Scientifically ideal (huge N + SNOMED-coded EHR), commercially inaccessible.

**PCORnet** — `pcornet.org/data/` — VERIFIED · `/front-door/` — VERIFIED. **50M+ people/yr** across **8 clinical research networks** (ADVANCE, GPC, INSIGHT, OneFlorida+, PaTH, PEDSnet, REACHnet, STAR), standardized Common Data Model. **🎯 Best-kept secret for a small budget.** The Front Door explicitly names *"industry scientists, sponsors"* as eligible requestors. Three services: Study Feasibility Review, Network Collaborator Request, **Data Network Request** (preliminary counts against the CDM). **Simple Data Network Requests are "generally completed without charge."** Timeline: weeks to months. PEDSnet is especially valuable for pediatric-onset rare disease.

**CMS / Medicare-Medicaid via ResDAC + VRDC** — `resdac.org/cms-fee-information-research-identifiable-data` — VERIFIED · `/virtual-research-data-center-vrdc-faqs` — VERIFIED · `/articles/rif-medicare-quarterly-data` — VERIFIED · ⚠️ `resdac.org/cms-data-file-availability-fees` — **DEAD (404)**.

*Costs — the concrete numbers:*
- VRDC: **~$35,000 first year** for a new project with one seat; **~$23,000/yr** thereafter. Additional seats **~$20,000** first year, **~$13,000/yr** after. (UNVERIFIED-exact — from indexed ResDAC/Brookings sources; the authoritative "CMS Fee List for CCW VRDC Cloud Environment" PDF 404'd on both the 2021 and 2025 paths I tried.)
- VERIFIED from the FAQ: extra storage in 1TB blocks at **$1,500**; 2,000 extra Databricks credits at **$1,500**; Researcher tier includes 2TB + 2,000 credits/yr, Innovator 5TB + 4,000.
- Physical (shipped) files: **four cohort-size tiers** (≤1M, 1–5M, 5–20M, 20M+), priced **per year of data**. Examples: MEDPAR $2,000/$2,500/$3,000/$5,000; Inpatient $2,000/$3,000/$6,000/$12,000. Initial project fee ~$20,000, renewal ~$10,000. Preliminary-file purchasers get mature files at 50%; quarterly extracts after the first at 50%.
- VRDC export: **aggregate statistics only**, minimum cell size **11 beneficiaries**, 3 output reviews/week up to 1GB. No PII/PHI leaves. Cannot access from outside the US.

*Fit:* excellent completeness for **65+ and disabled** populations only. **Wrong tool for pediatric-onset rare disease.** Multi-year, expensive, IRB + DUA heavy.

---

### 7. RDCA-DAP — the one built for exactly your problem

**URLs:** `https://c-path.org/programs/rdca-dap/` — VERIFIED · `/program/rare-disease-cures-accelerators-data-and-analytics-platform/` — VERIFIED · `/tools-platforms/rdca-dap/` — VERIFIED · `https://portal.rdca.c-path.org/` — VERIFIED (JS app) · `/contribute-data` — VERIFIED (JS app) · **DUA PDF `c-path.org/wp-content/uploads/2022/02/RDCA-DAP_DataUseAgreement.pdf` — VERIFIED, read all 8 pages** · `rarediseases.org/rdca-dap/` — BLOCKED (403)

**What it is:** FDA-funded (**Grant U18FD005320**), run by Critical Path Institute with NORD. Launched Sept 2021. Contact `rdcadap@c-path.org`.

**Holdings:** **111+ datasets** across **42–43+ rare diseases** — patient-level **clinical trial data, natural history studies, observational studies, real-world data, and patient registries**. Named diseases include Polycystic Kidney Disease, Duchenne Muscular Dystrophy, mitochondrial diseases, neurodevelopmental disorders, rare epilepsies, Friedreich ataxia (the largest FA database in existence), spastic paraplegia/PLS, and CF. Usage to date: **325 approved platform requests, 35 approved workspaces.**

**Access:** Register at the portal → agree to Terms → submit a Request for Access describing intended use, personnel, and publication plans → reviewed by a **5-member Data Use Committee** (C-Path, NORD, other rare disease stakeholders) on scientific merit / educational purpose / public interest, by majority vote → sign the DUA. Some datasets auto-approve; others need the original custodian's sign-off.

**Cost: FREE.** No fee appears anywhere in the program materials or in the 8-page DUA.

**Who:** *"qualified researchers in industry, government, regulatory agencies and academia."* **Industry is explicitly welcome** — no size or profit-status barrier. This is the most genuinely open door in this entire report.

**⚠️ DUA terms — read these before you commit (all VERIFIED from template v2.4_2026_05_04):**
- **🚩 IP license-back — the big one.** You retain ownership of Research Results and IP, **but you must grant each Data Custodian a "perpetual, non-exclusive, fully-paid up, royalty-free, irrevocable, worldwide, unrestricted license to any Intellectual Property derived from the Research Results."** For a **drug repurposing company whose entire value is a method-of-use patent, this is a material constraint.** Have counsel look at it before running anything patent-relevant on RDCA-DAP data. It may be fine (non-exclusive, and you keep ownership) — but it is not a nothing clause.
- **Publication:** submit to C-Path **30 days before** any journal submission or public disclosure. Custodians may review **for patentable subject matter** and demand deletion of their confidential information. Reference citation due within 3 months. Mandatory acknowledgment naming FDA Grant U18FD005320.
- **Export: permitted** — the DUA contemplates downloading processed data (warns results may change as data is added), subject to per-workspace conditions. Notably more permissive than N3C's absolute no-download rule.
- Use restricted to the approved Research Plan; **IRB/ethics approval required**; no re-identification; you indemnify C-Path and all custodians; either party may terminate on 60 days' notice, then you return or destroy the data; custodians are third-party beneficiaries; US sanctions and DOJ 28 CFR Part 202 bulk-sensitive-data restrictions apply.

**Contributing data:** via a Data Contribution Agreement. **Contributors retain ownership** and set access levels for their datasets. GDPR Standard Contractual Clauses available for EU transfers. Portal path: `portal.rdca.c-path.org/contribute-data`.

**Verdict:** For natural history and external control arms in a rare disease, **this is the highest value-per-dollar resource in existence** — *if your specific disease is among the 42–43.* Check the portal first; that's the entire question.

---

### Final ranking — practical accessibility on a small budget

| # | Platform | Cost | Realistic for you? | Best use |
|---|---|---|---|---|
| **1** | **RDCA-DAP** | **Free** | ✅ Yes — industry explicitly welcome | Natural history + external control arms. Check IP clause. |
| **2** | **PCORnet Front Door** | **Free** for simple requests | ✅ Yes — industry named as eligible | Free feasibility counts across 50M patients |
| **3** | **All of Us Data Browser** | **Free**, no login | ✅ Yes | 20-min free sanity check on concept coverage — *not* counting |
| **4** | **N3C** | **Free** | ⚠️ Only if renal / cancer / Long COVID | Enclave-only. Steal the 12,081-code rare disease codeset regardless. |
| **5** | **TriNetX via academic collaborator** | ~$0 to you | ✅ Yes, if you have a partner | **The best counting answer, cheapest** |
| **6** | **HealthVerity** | $$ à la carte | ✅ Most SMB-friendly commercial model | License only the slice you need, <2 weeks |
| **7** | **TriNetX direct license** | $$–$$$ | ⚠️ Maybe | Counts by site + licensable dataset |
| **8** | **Optum / MarketScan** | $$–$$$ (cheap via academic site license) | ⚠️ Via partner | Longest longitudinal claims; you get files |
| **9** | **Komodo** | $$$ | ❌ Unless via a Rare As One advocacy org | Largest N + genomics overlay |
| **10** | **Truveta** | $$$ ($95K–$495K + data subscription) | ❌ Likely out of reach | Notes + images + FDA-grade exports |
| **11** | **CMS VRDC** | $35K yr 1 / $23K after | ❌ Unless disease is geriatric | 65+/disabled only; slow; aggregate export only |
| **12** | **Epic Cosmos** | Cannot be purchased | ❌ **Structurally closed** | Only via an Epic-customer collaborator |
| **13** | **All of Us Workbench** | Free-ish | ❌ N far too small; DURA status ambiguous | Not for rare disease counting |
| — | **Datavant** | $$ | Infrastructure, not a dataset | Only if linking your own data |

### Recommended sequence

1. **Today, free:** search the RDCA-DAP portal for your disease. If it's there, everything else is secondary. **(30 min)**
2. **Today, free:** All of Us Data Browser + pull the N3C rare disease codeset (SNOMED-CT ≫ ICD-10) to build your phenotype definition. **(2 hrs)**
3. **Week 1, free:** submit a PCORnet Front Door Data Network Request. Genuinely free, industry-eligible, gives a real 50M-patient count.
4. **Week 1–2, ~free:** find an academic collaborator at a TriNetX member AMC. This is the cheapest path to a credible per-site patient count.
5. **Only then, paid:** HealthVerity first (à-la-carte), TriNetX direct second. Skip Truveta/Komodo/Cosmos/CMS unless a specific need justifies them.

**Two things to carry forward:** (a) your phenotype definition matters more than your database — SNOMED-coded EHR beats bigger ICD-10-only claims for rare disease; (b) have counsel review the RDCA-DAP IP license-back clause before you run patent-relevant analyses on it.