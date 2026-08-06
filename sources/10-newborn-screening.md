<!-- RECOVERED from subagent transcript agent-a61adf62890a232a5.jsonl, session fd64561f-7c90-41a2-95cf-b4a133a8fe0f, research date 2026-08-05.
     RUSP, state panels, NewSTEPs, CDC NSQAP, birth-prevalence math. Child of agent 3; fuller than the §-level summary in 03.
     Verbatim agent deliverable — not re-edited. -->

# US Newborn Screening — Patient-Finding Data Sources

**Headline:** The single most important finding is that **the RUSP governance model changed fundamentally in 2025**. ACHDNC was terminated April 1, 2025; HRSA now runs nominations directly via Federal Register notice-and-comment. Two conditions (DMD, MLD) were added December 16, 2025 under this new process. Most public references — including Baby's First Test and March of Dimes — are **stale** and still describe the old committee and old counts.

**Verification note:** `hrsa.gov`, `cdc.gov`, `hhs.gov`, `congress.gov`, and `wonder.cdc.gov` return **HTTP 403 to all automated fetchers** (bot-blocked, not dead). Where I say "VERIFIED via archive," I retrieved and read the actual content through the Wayback Machine or an alternate host. Pages marked LIVE-200 were confirmed by direct fetch.

---

## 1. RUSP (Recommended Uniform Screening Panel)

### Current count: 40 core + 26 secondary = 66 conditions

Confirmed against the **official HRSA RUSP table PDF, "As of December 2025"**, which I downloaded and parsed. Independently corroborated by NewSTEPs ("40 core disorders and 26 secondary disorders").

### URLs — note the canonical URL MOVED

| URL | Status |
|---|---|
| `https://newbornscreening.hrsa.gov/about-newborn-screening/recommended-uniform-screening-panel` | **NEW canonical.** VERIFIED via archive (403 to bots). This is the URL cited in the Dec 2025 Federal Register notices. |
| `https://www.hrsa.gov/advisory-committees/heritable-disorders/rusp` | **LEGACY/archival.** VERIFIED via archive. Now flagged as historical only. Don't build against this. |
| `https://mchb.hrsa.gov/programs/newborn-screening` | Landing page cited by the FR notices as where the updated RUSP lives. VERIFIED via archive. |
| `https://mchb.hrsa.gov/sites/default/files/mchb/programs-impact/recommended-uniform-screening-panel-table-december-15-2025.pdf` | **The downloadable RUSP table.** VERIFIED — I pulled and parsed the 3-page PDF (201 KB). |

**Downloadable format: PDF only. There is no official CSV, Excel, or API for the RUSP.** The date-stamped filename pattern means the URL changes on every revision — scrape the parent page for the link rather than hardcoding.

Best machine-readable substitute: **`https://www.newsteps.org/nbs-disorders`** (LIVE-200) — a structured HTML table of all core + secondary conditions with a **"Date Added" column** and time-criticality flags. Server-rendered, trivially scrapable.

### Recent additions (each = a newly created diagnosed cohort)

| Condition | Added | Core count after |
|---|---|---|
| SMA (homozygous SMN1 exon 7 deletion) | July 2018 | 35 |
| MPS II (Hunter) | Aug 2, 2022 | 36 |
| GAMT deficiency | Jan 2023 | 37 |
| Infantile Krabbe (low GALC + psychosine ≥10 nM) | July 1, 2024 | 38 |
| **Duchenne muscular dystrophy** | **Dec 16, 2025** | 39 |
| **Early-Onset Metachromatic Leukodystrophy** | **Dec 16, 2025** | **40** |

DMD and MLD appear on the official PDF as "Duchenne Muscular Dystrophy" and "Early-Onset Metachromatic Leukodystrophy" — note MLD is scoped to **early-onset** only.

### ACHDNC status: TERMINATED

- **Terminated April 1, 2025**, authority cited as "2025 Secretary Directive." Its charter had been renewed through 2026, but it was operating as a *discretionary* committee (statutory authority lapsed in 2019), so the agency head could terminate at will.
- Source: CRS Report R48757, *The Advisory Committee on Heritable Disorders in Newborns and Children* — **VERIFIED at `https://www.everycrsreport.com/reports/R48757.html`** (LIVE-200; congress.gov original is 403 to bots).
- The Dec 2025 Federal Register notices state plainly: *"The Advisory Committee on Heritable Disorders in Newborns and Children (ACHDNC), now inactive..."*
- HRSA's Heritable Disorders portfolio was **proposed for elimination** in the FY2026 Congressional Budget Justification for the proposed Administration for a Healthy America (AHA).
- **H.R. 4709** (introduced July 23, 2025) would reauthorize ACHDNC through 2030 as a statutory committee. No House action as of the CRS report.

### The NEW nomination pathway — this is the actionable part

The old process (nomination package → N&P Workgroup → Evidence Review Group → committee vote → Secretary within 120 days) **no longer exists as described.** For DMD and MLD, ACHDNC had already commissioned ERG evidence reviews but was terminated before voting. HRSA then improvised a replacement:

1. **HRSA publishes a Federal Register "Notice With Request for Comment"** proposing addition (Aug 14, 2025 for both DMD at 90 FR 39197 and MLD at 90 FR 39196).
2. **Public comment period.** DMD: 379 comments (366 support / 11 oppose). MLD: 98 comments (96 support / 1 oppose / 1 neutral).
3. **HRSA weighs comments + the ERG evidence review**, recommends to the Secretary.
4. **Secretary accepts** (Dec 16, 2025), published as a final FR notice Dec 22, 2025.

Verified Federal Register sources (all LIVE-200):
- DMD final: `https://www.federalregister.gov/documents/2025/12/22/2025-23573/addition-of-duchenne-muscular-dystrophy-to-the-recommended-uniform-screening-panel`
- MLD final: `https://www.federalregister.gov/documents/2025/12/22/2025-23574/addition-of-metachromatic-leukodystrophy-to-the-recommended-uniform-screening-panel`
- Full text API: `https://www.federalregister.gov/documents/full_text/text/2025/12/22/2025-23573.txt`
- **Federal Register JSON API works and is unblocked:** `https://www.federalregister.gov/api/v1/documents/2025-23573.json` — this is the reliable programmatic monitor for future RUSP changes.
- DMD evidence review (published in *Pediatrics*): `https://publications.aap.org/pediatrics/article/doi/10.1542/peds.2025-073192/...` (cited in the FR notice)

**How a company nominates today:** There is currently **no published standing nomination process.** The old preliminary/full nomination forms went to `achdnc@hrsa.gov` (a two-step process mandatory as of May 31, 2024 — Preliminary Nomination Form answering four gate questions: is there a screening test; is there case-definition agreement; has a prospective population-based pilot identified ≥1 infant; does pre-symptomatic identification enable effective therapy). That pipeline is dormant. The House Appropriations committee report explicitly "requests a plan regarding the new process for future recommendations." **Practical implication: the realistic levers right now are (a) generating population pilot data + an FDA-approved therapy so a condition is ERG-ready, (b) mobilizing public comment if/when HRSA publishes a notice, and (c) congressional pressure.** The archived nomination guidance is at `http://web.archive.org/web/20250110151753/https://www.hrsa.gov/advisory-committees/heritable-disorders/rusp/nominate` (VERIFIED).

### Commercially critical: the ACA coverage trigger

RUSP conditions are HRSA-supported preventive health guidelines under **§2713 of the Public Health Service Act**. Non-grandfathered group health plans and issuers **must cover the screening with no copay/coinsurance/deductible, for plan years beginning on or after one year from the Secretary's adoption.** For DMD and MLD (adopted Dec 16, 2025), that clock lands on **plan years beginning on or after December 16, 2026.**

---

## 2. State newborn screening panels

### Baby's First Test — `babysfirsttest.org` (Expecting Health / Genetic Alliance)

- State pages: `https://www.babysfirsttest.org/newborn-screening/states/<state-slug>` — **LIVE-200, VERIFIED** (checked California).
- Index pages: `/newborn-screening/states` (200), `/newborn-screening/conditions` (200), `/sitemap.xml` (200).
- **Structure:** static server-rendered HTML, conditions grouped by category (Amino Acid Disorders, Endocrine, Fatty Acid Oxidation, etc.) with condition name + abbreviation. Includes a headline count — e.g. *"California currently screens for 80 conditions."* Technically very easy to parse. **No JSON/API endpoint.**
- **There is no true side-by-side state comparison tool** — there's an interactive map and per-state pages, so a comparison matrix has to be assembled by scraping all 50 states + DC.
- **Scraping gotcha — read this before building anything:** `robots.txt` sets `Content-Signal: search=yes, ai-train=no, use=reference` and explicitly `Disallow: /` for **ClaudeBot, GPTBot, CCBot, Google-Extended, Amazonbot, Applebot-Extended, Bytespider, meta-externalagent**, plus `Crawl-delay: 10` for generic agents. Automated collection here carries a stated-terms problem. NewSTEPs is the cleaner source.
- **Staleness gotcha:** the site's own RUSP page still says *"35 core conditions and 26 secondary conditions"* and describes ACHDNC as actively meeting. It is roughly 5 conditions and one governance regime out of date. Do not use it for RUSP truth.

### NewSTEPs state profiles

`https://www.newsteps.org/data-resources/state-profiles` (LIVE-200) and `https://www.newsteps.org/view-state-profile` — state selector covering all 50 states, DC, and territories (Guam, Puerto Rico, American Samoa, CNMI). Profile data is **explicitly public**: *"Profile data is publicly available information... If you would like a different view or export of this data, please email newsteps@aphl.org."* **That email route for a bulk export is the highest-value, lowest-friction ask on this entire list.**

### The RUSP adoption lag — quantified

Authoritative source: **Sontag et al., "Implementation of Newborn Screening for Conditions in the United States First Recommended during 2010–2018," *Int J Neonatal Screen* — `https://pmc.ncbi.nlm.nih.gov/articles/PMC10123615/` (LIVE-200, VERIFIED).** Authored by APHL/NewSTEPs, covering 53 programs (50 states + DC + Guam + PR).

- **Full national adoption took 8.6 years for SCID and 6.8 years for CCHD.**
- **As of December 2022** — years after RUSP addition: Pompe (added 2015) 37 programs; MPS I (2016) 34; X-ALD (2016) 32; SMA (2018) 48.
- Pace, in additional programs per year: SMA 11.3, CCHD 7.8, SCID 6.2, MPS I 5.4, Pompe 4.9, X-ALD 4.7.
- The ramp is steep and slow. Companion paper Table 1 shows SMA went 5 → 15 → 29 programs across 2018 → 2019 → 2020; Pompe 16 → 21 → 25; MPS I 15 → 20 → 24; X-ALD 13 → 17 → 21.

**Modeling implication:** for a condition added in year 0, usable national diagnosed incidence does not arrive until roughly year 5–9, and the denominator of screened births ramps gradually. Any patient-finding forecast must apply a **time-varying screened-birth fraction**, not the full US birth count. For DMD/MLD (added Dec 2025), expect meaningful multi-state yield around 2028–2032.

**Texas confirms the mechanism** from the program side — its 2025 legislative report lists what adding a condition actually requires: modify lab space, install instruments, develop and validate tests, build algorithms, update the LIMS, and hire/train staff.

---

## 3. NewSTEPs — the best source for diagnosed US cases per condition

Run by **APHL** under HRSA cooperative agreement U22MC24078. All URLs below LIVE-200 VERIFIED.

| Resource | URL |
|---|---|
| Data Center | `https://www.newsteps.org/data-center` |
| Dashboards & Reports | `https://www.newsteps.org/data-center/dashboards-and-reports` |
| **Data Requests** | `https://www.newsteps.org/data-repository/data-requests` |
| State Profiles | `https://www.newsteps.org/data-resources/state-profiles` |
| Quality Indicators | `https://www.newsteps.org/data-resources/quality-indicators` |
| NBS Disorders (RUSP table) | `https://www.newsteps.org/nbs-disorders` |
| **Data API sign-up** | `https://www.newsteps.org/data-api/sign-up` |

### What the repository holds

Three data classes: **state/territory profile data, quality indicator data, and NBS confirmed cases.** Case data is **aggregate confirmed case counts by condition by state by year**, submitted voluntarily by 53 NBS programs. Collection runs on a **two-year lag** ("Case data collected are requested in the repository from two years prior") because diagnostic confirmation takes time.

### Access reality — this is the gating constraint

From the data-requests page, verbatim: *"NewSTEPs will in no event share state/territory-level quality indicator data or case data unless explicit permission has been granted by the NBS program."* Requests route to the NewSTEPs Data Manager; *"Sharing aggregate, unpublished data with investigators must be approved by the NewSTEPs Steering Committee."*

So: **profile data = public and exportable on request; case data = gated, per-state consent, Steering Committee approval, framed around "research and quality improvement purposes."** A for-profit requester is not excluded on its face but is not the intended audience. The Tableau dashboards — including a **"Confirmed Cases"** dashboard — are behind NewSTEPs account SSO with role-based permissions. There *is* a **data API sign-up**, which is the most promising programmatic route and worth pursuing directly.

### The published data — actual national case counts, no request needed

**Sontag et al., "Infants with Congenital Diseases Identified through Newborn Screening—United States, 2018–2020," *Int J Neonatal Screen* — `https://pmc.ncbi.nlm.nih.gov/articles/PMC10123626/` (LIVE-200, VERIFIED).** This is effectively the NewSTEPs repository published in the open, and it is the best free answer to "how many diagnosed US patients per year."

Headline: **overall birth prevalence of DBS-detected core RUSP diseases = 20.07 per 10,000** (2018–2020), up from 18.31 per 10,000 (2015–2017 restated). Applied to 2021 births (3,686,219), that is **~7,389 infants identified per year** via dried-blood-spot NBS. Total cases in the 2018–2020 window: **20,885**.

Selected per-condition results (2018–2020 cases / births screened / rate per 10,000):

| Condition | Cases | Births | Rate/10k |
|---|---|---|---|
| Primary congenital hypothyroidism | 7,421 | 11,086,342 | 6.69 |
| Sickle cell disease (SS + Sβthal + SC) | 5,517 | 11,086,342 | 4.98 |
| Cystic fibrosis | 2,518 | 10,983,899 | 2.29 |
| PAH deficiency (PKU) | 852 | 11,086,342 | 0.77 |
| Congenital adrenal hyperplasia | 781 | 11,086,342 | 0.70 |
| Biotinidase deficiency | 655 | 11,086,342 | 0.59 |
| MCAD deficiency | 651 | 11,086,342 | 0.59 |
| **X-linked adrenoleukodystrophy** | 345 | 5,125,176 | 0.67 |
| **Pompe disease** | 309 | 5,479,082 | 0.56 |
| Classical galactosemia | 216 | 11,086,342 | 0.19 |
| **SMA** | 219 | 3,185,560 | 0.69 |
| VLCAD deficiency | 204 | 11,086,342 | 0.18 |
| SCID | 185 | 10,947,551 | 0.17 |
| 3-MCC deficiency | 224 | 11,086,342 | 0.20 |
| Glutaric acidemia type I | 106 | 11,086,342 | 0.10 |
| **MPS I** | 71 | 5,121,441 | 0.14 |
| Citrullinemia type I | 69 | 11,086,342 | 0.06 |
| Propionic acidemia | 62 | 11,086,342 | 0.06 |
| Isovaleric acidemia | 67 | 11,086,342 | 0.06 |
| ASA aciduria | 57 | 11,086,342 | 0.05 |
| MSUD | 56 | 11,086,342 | 0.05 |
| MMA (mut) | 45 | 11,086,342 | 0.04 |
| Tyrosinemia type I | 39 | 11,086,342 | 0.04 |
| LCHAD deficiency | 32 | 11,086,342 | 0.03 |
| MMA (cobalamin) | 23 | 11,086,342 | 0.02 |
| Homocystinuria | 16 | 11,086,342 | 0.01 |
| β-Ketothiolase deficiency | 15 | 11,086,342 | 0.01 |
| 3-HMG aciduria | 8 | 11,086,342 | 0.01 |
| Trifunctional protein deficiency | 8 | 11,086,342 | 0.01 |
| Holocarboxylase synthase deficiency | 7 | 11,086,342 | 0.01 |

**Read the denominators carefully.** The newer conditions have much smaller denominators (Pompe 5.5M, MPS I 5.1M, SMA 3.2M vs. ~11.1M for legacy conditions) because only screening states/months are counted. The methodology is rigorous here — fractional-year analysis for mid-year implementations, and states excluded entirely for conditions they didn't universally screen.

Predecessor paper: the 2015–2017 analysis estimated **~6,646 babies/year** identified via DBS NBS.

### Data quality caveats to carry into any model

- Voluntary submission — data received from **49 states + 2 territories** (Mississippi and DC excluded from the prevalence analysis).
- **Aggregate counts only**, not individual-level. NewSTEPs explicitly states diagnostic data at case level "remains complicated"; they use total counts "rather than trying to obtain case information at an individual level."
- NewSTEPs has published **consensus public health surveillance case definitions** for RUSP diseases, but harmonization across programs is incomplete.
- Known artifacts: CF rates inflated by expanded molecular analysis picking up CRMS (inconclusive) cases; CH rates vary with TSH-vs-T4 algorithm choice and include transient cases; SCD trends track migration patterns.
- Excludes point-of-care conditions (hearing loss, CCHD) — DBS only.

---

## 4. CDC newborn screening — NSQAP

**Important negative finding: NSQAP is a laboratory quality-assurance program, not a patient or case-count data source.** Do not budget time expecting cohort data here.

NSQAP develops analytical methods for dried blood spots and produces certified DBS quality-control and reference materials. It serves **670+ NBS laboratories** worldwide — all US NBS labs, labs in 86+ countries, and 32 test manufacturers — shipping **~1 million DBS reference materials per year.** It holds ISO/IEC 17043 accreditation from A2LA (CDC's Newborn Screening and Molecular Biology Branch).

| Resource | URL | Status |
|---|---|---|
| About NBS Laboratories | `https://www.cdc.gov/newborn-screening/php/about/index.html` | VERIFIED via archive (403 to bots) |
| NSQAP program page | `https://www.cdc.gov/laboratory-quality-assurance/php/newborn-screening/index.html` | VERIFIED via archive |
| NSQAP resources | `https://www.cdc.gov/newborn-screening/php/resources/index.html` | VERIFIED via archive |
| NSQAP Participant Portal | `https://nbs.dynamics365portals.us/` | Participant-gated (labs only) |

Where NSQAP *is* useful: its **Program Reports** and proficiency-testing data quantify **assay performance and inter-laboratory variability** — directly relevant to false-positive rates and to how confident you can be that a given state's screening actually detects a target condition. The published harmonization work used QC/PT data from **302 laboratories in 2019**.

---

## 5. Birth prevalence → US patient count

### Authoritative annual US births

| Figure | Value | Source |
|---|---|---|
| **2025 provisional births** | **3,606,400** (−1% vs 2024) | NVSS Rapid Release Report No. 43, *Births: Provisional Data for 2025*, published April 2026 |
| 2025 general fertility rate | 53.1 per 1,000 women 15–44 | same |
| **2024 final births** | **3,628,934** (+1% vs 2023) | *Births: Final Data for 2024*, NVSR 75-02 |
| 2024 fertility rate | 53.8 per 1,000 | March of Dimes PeriStats (last updated March 2026) |
| 2021 births | 3,686,219 | used as denominator in the NewSTEPs paper |

The 2025 provisional data is based on **99.95% of birth records** as of Feb 3, 2026 — provisional here is essentially final for planning purposes.

**Recommended planning number: 3.6 million US live births/year**, trending down ~1%/year.

| Source | URL | Status |
|---|---|---|
| Births: Provisional Data for 2025 (full text) | `https://www.ncbi.nlm.nih.gov/books/NBK622025/` | **LIVE-200 VERIFIED** — use this mirror, it's unblocked |
| Births: Final Data for 2024 (NVSR 75-02) | `https://www.cdc.gov/nchs/data/nvsr/nvsr75/nvsr75-02.pdf` | Exists; 403 to bots |
| VSRR Report 43 PDF | `https://www.cdc.gov/nchs/data/vsrr/vsrr043.pdf` | Exists; 403 to bots |
| NVSS births hub | `https://www.cdc.gov/nchs/nvss/births.htm` | Exists; 403 to bots |
| **CDC WONDER Natality** | `https://wonder.cdc.gov/natality.html` | VERIFIED via archive; 403 to bots |
| CDC WONDER Expanded Natality (restricted) | `https://wonder.cdc.gov/natality-expanded-current.html` | VERIFIED via archive |
| NCHS Vital Stats Online (public-use micro-data) | `https://www.cdc.gov/nchs/data_access/vitalstatsonline.htm` | Exists; 403 to bots |

**On WONDER:** the standard **Natality** database is public and queryable by state/county/year/maternal characteristics. **Expanded Natality** adds finer geography and more variables but is **restricted-access** (requires agreeing to data use restrictions; some cells suppressed). WONDER has a programmatic POST/XML interface but it is brittle and rate-limited — for annual state birth counts, the **NCHS public-use natality files** (fixed-width annual micro-data, one record per birth) are the more reliable pipeline.

### The math — birth prevalence to prevalent population

The naive calculation everyone does wrong:

```
WRONG:  Prevalence × cumulative births over N years
```

This overcounts badly for severe pediatric conditions, because it assumes nobody dies. The correct calculation is a **survival-weighted birth-cohort sum**:

```
P(t) = Σ  B(t−a) × p(t−a) × S(a)
      a=0..A
```

where:
- `P(t)` = prevalent US population alive at time *t*
- `a` = age in years, summed 0 to max age `A`
- `B(t−a)` = US live births in the year that cohort was born
- `p(t−a)` = **birth prevalence** in that cohort (per live birth)
- `S(a)` = **probability of surviving from birth to age a** for an affected individual

**Steady-state simplification.** If births and prevalence are roughly constant, the sum collapses to:

```
P ≈ B × p × ê       where ê = Σ S(a) = life expectancy at birth (years) of affected individuals
                    (the area under the survival curve)
```

This is the formula worth internalizing: **prevalent population ≈ annual births × birth prevalence × life expectancy of the affected.**

**Worked example.** A condition at **1:100,000 live births**, with **treated life expectancy of 25 years**:

```
P ≈ 3,600,000 × (1/100,000) × 25 = 36 × 25 = 900 prevalent US patients
```

The same condition with an **untreated life expectancy of 5 years** (typical of early-onset MLD, infantile Krabbe, or infantile Pompe):

```
P ≈ 36 × 5 = 180 prevalent US patients
```

**A 5x swing driven entirely by the survival term.** This is why mortality adjustment is not a refinement — it dominates the answer for severe pediatric disease.

### Four corrections that must be layered on

1. **Screening coverage ramp.** Replace `B` with `B × c(a)`, where `c(a)` is the fraction of US births actually screened for that condition in the cohort's birth year. For anything added post-2015 this is well below 1.0 and rising — see the Section 2 adoption curves. Ignoring this overstates the NBS-ascertained cohort substantially.

2. **Pre-screening cohorts.** Patients born before screening existed were diagnosed clinically — later, incompletely, and with survivorship bias toward milder phenotypes. The NBS-identified cohort and the clinically-diagnosed prevalent cohort are **different populations with different severity distributions.** For a drug repurposing thesis, be explicit about which one you are targeting.

3. **Screening detects more, and milder, disease than clinical diagnosis.** NBS has low ascertainment bias by design, so **birth prevalence from NBS routinely exceeds historical clinical literature estimates.** Pompe is the canonical example — NBS-derived birth prevalence came in materially higher than pre-screening estimates because it catches late-onset cases that would not have presented for decades. Genotype-only estimates have their own problem: benchmarking against ~23 million NBS infants across 28 recessive disorders found allele-frequency models land within 10-fold of NBS truth for only ~90% of disorders. **NBS-derived rates are the gold standard; use them over carrier-frequency math wherever they exist.**

4. **Screen-positive ≠ diagnosed.** California's own data documentation warns: *"there is not a one-to-one relationship between a screen-positive test result and a disorder. A newborn can be screen-positive for more than one disorder. Conversely, a positive screen for one disorder can be associated with the diagnosis of a different disorder."* Always work from confirmed-case counts, never referral counts.

Methodology references (both LIVE-200 where noted):
- *Benchmarking genetic birth prevalence estimates against newborn screening data*, AJHG 2026 — `https://www.sciencedirect.com/science/article/pii/S0002929726001527` (cell.com mirror 403s to bots)
- *An analysis of Pompe newborn screening data: a new prevalence at birth* — `https://pmc.ncbi.nlm.nih.gov/articles/PMC10810242/`

---

## 6. March of Dimes PeriStats and state case-count reports

### March of Dimes PeriStats — `https://www.marchofdimes.org/peristats` (LIVE-200 VERIFIED)

Best free source for **US births by state and county**, plus fertility rates, preterm birth, birthweight, and demographics.

- URL pattern: `https://www.marchofdimes.org/peristats/data?reg=<region>&top=<topic>&stop=<subtopic>&lev=<level>&slev=<sublevel>&obj=<object>` — e.g. `reg=99&top=2&stop=1&lev=1&slev=1&obj=1` returns the US births page. **Parameterized and scrapable**; `reg` switches jurisdiction across all 50 states + DC + Puerto Rico. No public API.
- Confirmed current: *"In 2024, there were 3,628,934 live births in the United States"*, last updated March 2026.
- **Its newborn screening page is badly stale** — still says the RUSP has "32 core conditions and 26 secondary conditions" following "an update in March 2015," and notes state-level NBS detail is only planned "in future updates." Use PeriStats for **births**, never for RUSP or screening panels.

### States publishing confirmed case counts

**New York — the best per-condition public reporting.** Wadsworth Center publishes a one-page annual report with a **per-disorder "# Confirmed with Disease" column.**
- 2023 report: `https://www.wadsworth.org/sites/default/files/2025-04/2023%20Annual%20Report_Final.pdf` (LIVE-200 VERIFIED, parsed). Sample 2023 figures: 204,505 total newborns, 1,711 referrals; CAH 21-hydroxylase deficiency 8; primary congenital hypothyroidism 114; Hb SS disease 80; Hb SC 58; PKU 11; MCAD 6; VLCAD 5; homocystinuria 1; carnitine uptake defect 1; MSUD 0; tyrosinemia types I/II/III 0; LCHAD 0; TFP 0; CPT1 0; CPT2 0.
- 2024 topline: **671 infants diagnosed**, 1,866 screened positive, 246,895 specimens from 206,728 infants, panel of 50+ conditions. `https://www.health.ny.gov/press/releases/2025/2025-10-01_newborn_screening.htm` (LIVE-200 VERIFIED)
- Screened disorders list: `https://www.wadsworth.org/programs/newborn/screening/screened-disorders` (LIVE-200)

**California — the best machine-readable dataset.** CHHS Open Data Portal, `https://data.chhs.ca.gov/dataset/newborn-screening-disorders` (LIVE-200 VERIFIED).
- **Three downloadable CSVs**: counts statewide, by race/ethnicity, and by California region — plus XLSX data dictionaries and a county-to-region crosswalk.
- Covers **2009–2019**, counts of disorders **diagnosed** by the California NBS Program.
- **Caveats:** marked **ARCHIVED**; counts **suppressed for disorders with fewer than 6 cases** (which kills exactly the ultra-rare conditions of most interest); sickle subtypes collapsed into one "Sickle Cell Disease" group; SCID from March 2013, ALD from Feb 2016, Pompe and MPS I from Aug 2018 only. The `data.ca.gov` mirror 404s — use the CHHS URL.
- Program page: `https://www.cdph.ca.gov/Programs/CFH/DGDS/Pages/nbs/default.aspx` (LIVE-200). California detects **750+ newborns/year** with clinically significant disorders. Baby's First Test lists California at **80 conditions screened** — one of the broadest panels.

**Texas — annual reports plus a statutory RUSP-gap report.** All LIVE-200 VERIFIED:
- 2025 legislative report (HB 2478 / Health & Safety Code §33.020): `https://www.dshs.texas.gov/sites/default/files/legislative/2025-Reports/2025-HB-2478-Newborn-Screening-Report.pdf` — **statutorily required to identify RUSP conditions NOT on the Texas panel**, plus resource needs and implementation timelines. Unusually valuable for tracking adoption gaps.
- Annual reports: `https://www.dshs.texas.gov/sites/default/files/lab/NBS/NBS-Annual-Report/Annual%20Report%202022%20APPROVED%2008212023.pdf`, `.../Annual-Report-2020---072821.pdf`
- Program page: `https://www.dshs.texas.gov/newborn-screening-program`
- Scale: ~800,000 screens/year (Texas screens every newborn **twice**). 2024: 27,913 abnormal results, **1,089 newborns identified**. Panel = 59 lab-tested conditions + hearing loss + CCHD, after **adding four lysosomal storage diseases in August 2025** (including Pompe, MPS I). Texas statute mandates screening for RUSP conditions "as funding allows," with explicit carve-outs for galactoepimerase and galactokinase deficiency.

**Also known to publish:** North Carolina publishes a statutorily mandated annual NBS report (G.S. 130A-125(e)). Minnesota's Newborn Screening Advisory Committee publishes meeting minutes tracking RUSP adoption decisions.

---

## Recommended source hierarchy for patient counts

1. **NewSTEPs published IJNS papers** (PMC10123626, PMC10123615) — free, national, per-condition, methodologically sound. **Start here.**
2. **NewSTEPs profile data export** via `newsteps@aphl.org` — explicitly offered, public data, low friction. Gets you the screening-status matrix.
3. **NewSTEPs case data request** + data API sign-up — the real prize (case counts by condition by state by year), but gated behind per-state consent and Steering Committee approval.
4. **State reports** — NY (per-condition confirmed counts), CA (downloadable CSVs, ≥6-case suppression), TX (RUSP gap analysis).
5. **Federal Register JSON API** — the one unblocked, reliable programmatic monitor for RUSP changes.

## Three things that will bite you

1. **The RUSP URL moved and most secondary sources are stale.** Baby's First Test says 35 core; March of Dimes says 32 core; the truth is 40. Anchor on the December 2025 HRSA PDF or the NewSTEPs disorders table.
2. **RUSP addition ≠ diagnosed patients.** Historical lag to full national adoption is 7–9 years. DMD and MLD will not produce a meaningful national cohort until roughly 2028–2032.
3. **Never model prevalent population as cumulative births × prevalence.** The survival term dominates for severe pediatric disease — omitting it inflates estimates by 3–10x for exactly the conditions a rare-disease repurposing thesis targets.