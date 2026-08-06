<!-- RECOVERED from subagent transcript agent-ad56cfbdebba24850.jsonl, session fd64561f-7c90-41a2-95cf-b4a133a8fe0f, research date 2026-08-05.
     NewSTEPs (APHL) deep dive incl. scrapable state-profile JSON API.
     Verbatim agent deliverable — not re-edited. -->

I have everything needed. Here are the findings.

---

# NewSTEPs (APHL) — Research Findings

**Bottom line for your use case:** NewSTEPs holds exactly the data you want — confirmed case counts by condition by state — but the state-level layer is **not public and not purchasable**. What *is* freely available is (a) **national** case counts by condition (published in annual reports + peer review), and (b) a **fully open, unauthenticated JSON API** for which conditions each state screens. State-by-state case counts require a data request plus **per-state written permission**, and "Rule of 5" suppression destroys most rare-disease cells at the state level.

---

## 1. The NewSTEPs Data Repository

**Primary URLs**
| URL | Status |
|---|---|
| `https://www.newsteps.org/` | **VERIFIED** (200) |
| `https://www.newsteps.org/data-center` | **VERIFIED** (200) |
| `https://www.newsteps.org/data/login` | **VERIFIED** (200) |
| `https://www.aphl.org/programs/newborn_screening/Pages/data-repository.aspx` | **UNVERIFIED** — returns HTTP 200 but the body renders APHL's **"Not Found"** page. This URL is widely cited (incl. in search results) but is **dead**. Do not cite it. |

**Does it hold case-level data on confirmed cases by condition by state? — YES.** Three data strata, per the official policy document:

1. **NBS Program Profiles** — public.
2. **Quality Indicators** — restricted (8 QIs, monthly/annual).
3. **Cases** — restricted. Two sub-types:
   - **Individual (infant-level) case data** — de-identified; demographics, time to diagnosis, time to medical intervention, final diagnosis details.
   - **Aggregate case data** — total confirmed case counts **per disorder, stratified by birth year**, per program.

Direct quote from the policy page: cases *"provide confirmed case counts for each newborn screening disorder, stratified by birth year."*

**Access control is verifiable in the HTML.** On both the Data Center nav and the dashboards page, the case entries are rendered as non-clickable locked spans, not links:
```html
<li class="li-level-second "><span class="locked locked--white">NBS Cases</span></li>
...
<li><span class="locked">Quality Indicators</span></li><li><span class="locked">Confirmed Cases</span></li>
```

**Years covered**
- Aggregate case counts published: **2015 → 2022** (2019 report covers 2015–2017; 2022 report covers 2018–2020; 2024 report covers 2020–2022).
- Individual-level cases: birth years **2006–2020** were present as of Aug 2020 (per the Omari 2022 usability study).
- **Two-year reporting lag** is structural: a 2020 birth is submitted by 2022. So as of Aug 2026, ~2023–2024 births are the practical frontier.

**How many states submit — and it is declining for cases**

| Layer | Programs |
|---|---|
| Repository total | **56** programs (50 states + DC + American Samoa, CNMI, Guam, Puerto Rico, USVI) |
| Programs with data actually in repository (IJNS) | **53** |
| Aggregate cases, 2020 births | **n=51** |
| Aggregate cases, 2021 births | **n=44** |
| Aggregate cases, 2022 births | **n=42** (report notes 2022 is still *"pending"*) |
| Individual-level cases (as of 31 Aug 2020) | **45 states**, 24,129 cases across 34 disorders |
| Screened Conditions Report rows | sum to **54** (page claims 56 — minor inconsistency) |

Mississippi and DC did not report aggregate cases for 2018–2020.

---

## 2. Public Dashboards and Visualizations

**Landing pages**
| URL | Status |
|---|---|
| `https://www.newsteps.org/data-center/dashboards-and-reports` | **VERIFIED** (200) |
| `https://www.newsteps.org/data-visualizations` | **VERIFIED** (200) — redirects to the same page |

**Is there a public dashboard showing case counts? — NO.** The dashboard page has three tabs. Exactly one is public:

| Tab | Public? |
|---|---|
| State Profiles | **Yes** — `href="/quicktabs/nojs/data_visualizations/0"` |
| Quality Indicators | **No** — `<span class="locked">` |
| **Confirmed Cases** | **No** — `<span class="locked">` |

Tableau access is gated by SSO tied to your NewSTEPs user role. Case/QI dashboards need an authorized (state NBS program) account.

**Publicly embedded Tableau workbooks** (all **VERIFIED**, embedded from `public.tableau.com`, none contain case counts):

| Page (all VERIFIED 200) | Tableau workbook/view |
|---|---|
| `/resources/data-visualizations/newborn-screening-status-all-disorders` | `NewbornScreeningStatusforAllDisorders/NBSStatusforAllDisordersStory` |
| `/resources/data-visualizations/operating-days-and-hours` | `OperatingDaysandHours/OperatingDaysandHours` |
| `/resources/data-visualizations/newborn-screening-fees` | `NewbornScreeningFees/NBSFees` |
| `/resources/data-visualizations/newborn-screening-information-management-systems` | `InformationManagementSystems/InformationManagementSystems` |
| `/resources/data-visualizations/newborn-screening-electronic-messaging` | `NewbornScreeningElectronicMessaging/NewbornScreeningElectronicMessaging` |
| `/resources/data-visualizations/newborn-screening-advisory-committees` | `NewbornScreeningAdvisoryCommittee/AdvisoryCommittee` |

`https://public.tableau.com/views/NewbornScreeningStatusforAllDisorders/NBSStatusforAllDisordersStory` — **VERIFIED** (200).

**Most useful public report — `Screened Conditions Report`** — **VERIFIED** (200)
`https://www.newsteps.org/data-center/reports/screened-conditions-report`
Plain server-rendered HTML `<table>`, trivially scrapable. Gives **number of programs per screening status per condition**. Live values:

| Condition | Not Screened | Universally Screened |
|---|---|---|
| MPS I | 6 | **48** |
| MPS II | 30 | **24** |
| Pompe | 4 | **50** |
| Infantile Krabbe | 32 | **22** |
| MLD | 53 | **3** |
| GAMT | 32 | **22** |
| SMA | 3 | **51** |
| X-ALD | 4 | **50** |
| DMD | 53 | **3** |
| SCID | 1 | 53 |
| CF / PKU / MCAD / GA1 | 0 | 54 |

Other public reports (all **VERIFIED** 200): `/data-resources/reports/` + `nbs-fees-report`, `screening-methodologies-and-targets-report`, `lims-system-report`, `dbs-retention-report`, `courier-system-report`, `data-retention-report`.

---

## 3. Annual Reports — WITH ACTUAL CASE COUNTS

**Index:** `https://www.newsteps.org/resource-library/newsteps-annual-reports` — **VERIFIED** (200). Four reports exist (no 2021 or 2023 edition).

| Report | PDF URL (all **VERIFIED** 200) | Size | Case years |
|---|---|---|---|
| **2024** (pub. July 2025, 27pp) | `https://www.newsteps.org/sites/default/files/resources/download/NewSTEPs-2024-Annual-Report_0.pdf` | 5.5 MB | 2020–2022 |
| **2022** (pub. July 2023) | `.../NewSTEPS-2022-Annual-Report.pdf` | 1.5 MB | 2018–2020 |
| **2020** | `.../NewSTEPs%20Annual%20Report%209%2022%2021.pdf` | 2.2 MB | 2018 |
| **2019** | `.../nbs-newsteps-2019-annual-report.pdf` | 6.1 MB | 2015–2017 |

### Latest national case counts — 2024 Report, Table 17 (data as of 17 Mar 2025)

Confirmed cases reported to NewSTEPs, core RUSP disorders, **by birth year**:

| Disorder | 2022 (n=42) | 2021 (n=44) | 2020 (n=51) |
|---|---|---|---|
| **CH** (congenital hypothyroidism) | **2,105** | 2,052 | 2,512 |
| **Presence of Hb S** (sickling hemoglobinopathies) | **1,327** | 1,247 | 1,675 |
| **CF** | **607** | 655 | 761 |
| **PKU** | **170** | 206 | 240 |
| **SMA** | **164** | 156 | 141 |
| **CAH** | **163** | 134 | 267 |
| **BIOT** | **162** | 186 | 198 |
| **MCAD** | **157** | 176 | 178 |
| **X-ALD** | **131** | 132 | 145 |
| **Pompe** | **119** | 109 | 132 |
| **GALT** | **109** | 99 | 69 |
| 3-MCC | 69 | 69 | 68 |
| SCID | 56 | 48 | 71 |
| VLCAD | 54 | 55 | 76 |
| MSUD | 28 | 18 | 21 |
| IVA | 26 | 31 | 22 |
| CUD | 25 | 25 | 34 |
| **MPS I** | **23** | 25 | 24 |
| PROP | 20 | 19 | 24 |
| CIT I | 19 | 17 | 16 |
| ASA | 18 | 11 | 15 |
| GA I | 16 | 31 | 27 |
| LCHAD | 11 | ● | 15 |
| **MPS II** | **9** | NA | NA |
| Cbl A,B | 8 | 7 | ● |
| TYR I | 7 | 15 | 16 |
| MUT | 6 | 9 | 16 |
| HCY, TFP, BKT, HMG, MCD | ● | ● | ● |
| **TOTAL** | **5,617** | **5,543** | **6,781** |

● = suppressed under the **Rule of Five** (≤5 newborns in a cell). Excludes CCHD, hearing loss, GAMT, Infantile Krabbe.

### 2022 Report, Table 14 — *unsuppressed*, n=51, and therefore more useful for rare conditions

This table has **no Rule-of-5 masking**, so you get real integers for ultra-rare disorders:

| Disorder | 2018 | 2019 | 2020 |
|---|---|---|---|
| CH | 2,402 | 2,430 | 2,542 |
| Presence of Hb S | 1,891 | 1,885 | 1,759 |
| CF | 917 | 809 | 768 |
| PKU & Hyperphe | 316 | 271 | 260 |
| CAH | 272 | 241 | 260 |
| MCAD | 237 | 227 | 180 |
| BIOT | 215 | 235 | 202 |
| X-ALD | 90 | 106 | 149 |
| Pompe | 79 | 98 | 134 |
| SMA | 11 | 79 | 135 |
| 3-MCC | 87 | 72 | 64 |
| GALT | 73 | 65 | 77 |
| SCID | 57 | 55 | 68 |
| VLCAD | 57 | 75 | 71 |
| GA I | 40 | 39 | 27 |
| CUD | 39 | 33 | 35 |
| **MPS I** | 15 | 29 | 27 |
| **MPS II** | **0** | **0** | **0** |
| **TFP** | **1** | **4** | **3** |
| **HMG** | **4** | **3** | **1** |
| **BKT** | **3** | **7** | **5** |
| **MCD** | **2** | **3** | **2** |
| **HCY** | **8** | **3** | **5** |
| Cbl A,B | 8 | 6 | 8 |
| MUT | 19 | 13 | 13 |
| PROP | 21 | 17 | 24 |
| IVA | 19 | 25 | 23 |
| MSUD | 17 | 18 | 21 |
| TYR I | 20 | 4 | 14 |
| CIT I | 26 | 26 | 16 |
| ASA | 12 | 30 | 15 |
| LCHAD | 8 | 9 | 15 |
| **TOTAL** | **6,966** | **6,917** | **6,923** |

### 2019 Report, Table 12 — 2015–2017 (n=51)
CH 2,224 / 2,252 / 2,179 · Hb S 1,957 / 1,836 / 2,026 · CF 755 / 692 / 682 · PKU&Hyperphe 241 / 228 / 229 · CAH 272 / 272 / 282 · MCAD 253 / 231 / 206 · BIOT 183 / 144 / 157 · SCID 71 / 78 / 71 · X-ALD 5 / 17 / 61 · Pompe 14 / 17 / 31 · MPS I <5 / <5 / 6. **Totals 6,507 / 6,237 / 6,543.**

---

## 4. Data Access — Request Process and Eligibility

**No public bulk download of case data.** Profile data only is public.

| URL | Status |
|---|---|
| `https://www.newsteps.org/data-repository/data-requests` | **VERIFIED** (200) |
| `https://www.newsteps.org/data-repository/data-requests/newsteps-data-request-policies-and-procedures` | **VERIFIED** (200) |
| `https://www.newsteps.org/data-repository/data-requests/cases-data` — the case request webform | **VERIFIED** (200) |
| `https://www.newsteps.org/data-repository/data-requests/quality-indicator-data` | **VERIFIED** (200) |

**Mechanism: not a signed DUA — a webform with click-through terms.** The form requires ticking *"I confirm that I have read and agree to all policies and procedures…"*; on submission the investigator **automatically agrees** to the provisions. Verified form fields include `requestors_organization`, `sponsor_of_the_project`, `funding_y_n`, `name_of_project_that_will_utilize_this_data`, `why_do_you_need_this_data` (research questions, hypotheses, objectives, design, cohort, analysis method), optional mock tables/figures upload, plus `disorder_type`, `years`, `hrsa_region`, `number_of_annual_births`, `number_of_required_screens` on page 2.

**Steps**
1. Read policies & procedures; complete the Cases Data webform.
2. Acknowledged and logged; NewSTEPs "respects the order received," prioritization at their discretion.
3. **NewSTEPs Data Manager** reviews; may schedule a call to discuss limitations.
4. **Depending on the request, the NewSTEPs Steering Committee reviews.** Sharing *aggregate unpublished* data with investigators **must be approved by the Steering Committee**.
5. Timeline provided if granted.

**Timelines (stated):** ≥**3 weeks** for profile data and **national-level** QI/case data. **~8 weeks** for **state-level** QI/case data, because *"we will need to get permission from the NBS Programs."*

**Can a for-profit company request it? — Yes, nothing prohibits it, but expect friction.** There is **no stated eligibility restriction** anywhere in the policy or the form — no non-profit/academic/IRB requirement, and the form explicitly captures organization and funding sponsor. The policy says only that NewSTEPs *"encourages data requests for research and quality improvement purposes."* Practical constraints that will bite a commercial requester:

- **State-level data is blocked by default.** *"NewSTEPs will in no event share state/territory-level quality indicator data or case data unless explicit permission has been granted by the NBS program."* That is up to **50+ separate approvals**.
- **Rule of Five** — no sharing where a cell has ≤5 newborns. For most rare conditions × 50 states × single year, nearly every cell dies.
- Results restricted to aggregate; no identification of any individual, institution, or firm.
- Data may only be used for the stated purpose; no onward sharing to third parties not on the form.
- Data are **provisional** — programs can modify or delete past data at any time.
- Publications must acknowledge NewSTEPs + carry a non-endorsement disclaimer.
- Approval is **discretionary** — Steering Committee is composed of the state NBS programs whose data you'd be commercializing.

**Precedent that requests do get granted:** Omari et al. (Univ. of Michigan) obtained **individual-level** data — 24,129 cases, 34 disorders, 45 states, birth years 2006–2020. States were **not identified** in the released dataset "owing to confidentiality restrictions."

**Governance:** MOUs between APHL and each NBS program govern QI and infant-level entry. Colorado IRB and HHS OHRP deemed the project **Non-Human Subject Research** (`https://www.newsteps.org/about-newsteps/frequently-asked-questions` — **VERIFIED** 200).

**Contact:** `newsteps@aphl.org`

---

## 5. State Profiles — Conditions Screened, and YES it's scrapable via a public JSON API

**Human-facing pages** (all **VERIFIED** 200):
- `https://www.newsteps.org/data-resources/state-profiles`
- `https://www.newsteps.org/view-state-profile?state=Colorado&year=2024`
- `https://www.newsteps.org/data-center/state-profiles?state=Colorado&year=2024`

These are **JS-rendered shells** — HTML scraping returns an empty template. But I located the backing module `aphl_data_api` and extracted the endpoints from
`https://www.newsteps.org/modules/custom/aphl_data_api/modules/aphl_state_profile/assets/js/aphl_state_profile.scripts.js` (**VERIFIED** 200).

### Public, unauthenticated JSON API — **VERIFIED working**

| Endpoint | Params | Verified result |
|---|---|---|
| `GET /data-api/state/profile` | `institution`, `year` | **200**, 723 KB JSON (Colorado 2024) |
| `GET /data-api/state/profile/annual` | `state`, `year` | **200** → `{"institutionName":"Colorado","year":2024,"count":64277}` |
| `GET /data-api/state/profile/external/disorders` | none | **200**, 409 KB — full disorder taxonomy |
| `GET /data-api/state/profile/download` | — | **200** |

Example (verified):
```
https://www.newsteps.org/data-api/state/profile?institution=Colorado&year=2024
https://www.newsteps.org/data-api/state/profile/annual?state=Colorado&year=2024
```

**No API key, no cookie, no referer check, no rate limiting observed.** Verified across Texas / California / New York / Wyoming for years 2019 and 2024 — all 200. **Year coverage: 2016–2026 return 200; 2012 and 2014 return HTTP 500.**

**Payload:** 26 top-level keys — `screeningStatuses` (**83 condition records**), `nbsPolicies` (57 fields), `programStructure` (34), `hitElements` (37), `itInfrastructure` (24), `screeningFeeDetails`, `testAdditionDetails`, `advisoryCommitteeDetails`, `responsibleLaboratories`, `contacts` (16), `labOperatingHours`, `followUpOperatingHours`, `requiredScreenCount`, `region`, `website`, `year`.

Each `screeningStatuses` record: `condition.name`, `primaryStatus`/`secondaryStatus`/`tertiaryStatus`, `statusMonth`, `statusYear`, plus 1st/2nd/3rd-tier test methods and targets for first and second screens, and `equipment`.

Colorado 2024 verified distribution: **48 Universally Screened**, 33 Not Screened, 1 Offered to select populations, 1 null. `requiredScreenCount` = "Two Screen".

**Crucially: `screeningStatuses` contains NO case counts.** I searched the full payload — zero incidence/case-count fields. This API answers *"does state X screen for condition Y, since when, by what method"* — not *"how many patients."*

**Recommended scrape:** 56 institutions × 11 years (2016–2026) ≈ **616 requests** for a complete panel of who-screens-what-when. Plus the plain-HTML Screened Conditions Report for national rollups.

---

## 6. Peer-Reviewed Literature with National Case Counts

I ran a PubMed E-utilities query (`NewSTEPs AND newborn screening`) returning 14 PMIDs. The load-bearing ones:

**★ Primary source for national case counts by condition**
> Gaviglio A, McKasson S, Singh S, Ojodu J. **Infants with Congenital Diseases Identified through Newborn Screening—United States, 2018–2020.** *Int J Neonatal Screen.* 2023 Apr 13;9(2):23. doi:10.3390/ijns9020023. PMID 37092517. PMC10123626.
> - `https://pmc.ncbi.nlm.nih.gov/articles/PMC10123626/` — **VERIFIED** (200)
> - `https://pubmed.ncbi.nlm.nih.gov/37092517/` — **VERIFIED** (200)
> - `https://www.mdpi.com/2409-515X/9/2/23` — **UNVERIFIED** (403 to scripted fetch; MDPI bot-blocks. DOI is valid; use the PMC mirror.)

**Table 2** — 3-year national totals and birth prevalence (2018–2020), the single most useful published table for market sizing:

| Disease | Cases 2018–20 | Rate/10,000 | Denominator births |
|---|---|---|---|
| Primary congenital hypothyroidism | **7,421** | 6.69 | 11,086,342 |
| SCD (S,S + S,β-thal + S,C) | **5,517** | 4.98 | 11,086,342 |
| Cystic fibrosis | **2,518** | 2.29 | 11,086,342 |
| PAH deficiency (PKU) | **852** | 0.77 | 11,086,342 |
| CAH | **781** | 0.70 | 11,086,342 |
| Biotinidase deficiency | **655** | 0.59 | 11,086,342 |
| MCAD | **651** | 0.59 | 11,086,342 |
| **X-ALD** | **345** | **0.67** | **5,125,176** ← partial |
| **Pompe** | **309** | 0.56 | 11,086,342 |
| 3-MCC | 224 | 0.20 | 11,086,342 |
| **SMA** | **219** | **0.69** | **3,185,560** ← partial, first-ever estimate |
| Classical galactosemia | 216 | 0.19 | 11,086,342 |
| VLCAD | 204 | 0.18 | 11,086,342 |
| SCID | 185 | 0.17 | 10,947,551 |
| CUD | 107 | 0.10 | 11,086,342 |
| Glutaric acidemia I | 106 | 0.10 | 11,086,342 |
| **MPS I** | **71** | 0.14 | 11,086,342 |
| Citrullinemia I | 69 | 0.06 | 11,086,342 |
| Isovaleric acidemia | 67 | 0.06 | 11,086,342 |
| Propionic acidemia | 62 | 0.06 | 11,086,342 |
| ASA | 57 | 0.05 | 11,086,342 |
| MSUD | 56 | 0.05 | 11,086,342 |
| MMA (mutase) | 45 | 0.04 | 11,086,342 |
| Tyrosinemia I | 39 | 0.04 | 11,086,342 |
| LCHAD | 32 | 0.03 | 11,086,342 |
| MMA (cobalamin) | 23 | 0.02 | 11,086,342 |
| Homocystinuria | 16 | 0.01 | 11,086,342 |
| β-Ketothiolase | 15 | 0.01 | 11,086,342 |
| HMG | 8 | 0.01 | 11,086,342 |
| TFP | 8 | 0.01 | 11,086,342 |
| Holocarboxylase synthase | 7 | 0.01 | 11,086,342 |
| **TOTAL DBS** | **20,885** | **20.07** | — |

Note the **partial denominators** for X-ALD and SMA — rates are computed on screened births only, not all US births. Do not multiply those rates by the full birth cohort without adjusting.

**Predecessor (the 2015–2017 baseline)**
> Sontag MK, Yusuf C, Grosse SD, Edelman S, et al. **Infants with Congenital Disorders Identified Through Newborn Screening — United States, 2015–2017.** *MMWR Morb Mortal Wkly Rep.* 2020 Sep 11;69(36):1265–1268. doi:10.15585/mmwr.mm6936a6. PMID 32915168. PMC7499833.
> - `https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7499833/` — **VERIFIED** (200)
> - `https://pubmed.ncbi.nlm.nih.gov/32915168/` — **VERIFIED** (200)
> - `https://www.cdc.gov/mmwr/volumes/69/wr/mm6936a6.htm` — **UNVERIFIED** (403 to scripted fetch; CDC bot-blocks)
> - State-level heat map supplement: `https://stacks.cdc.gov/view/cdc/93107` — **UNVERIFIED** (403)
>
> Key figures: overall 34.0/10,000 incl. hearing loss → **~12,900 infants/yr** (6,646 DBS + 6,259 hearing loss). DBS-only 17.5/10,000. CH 6.0, SCD 4.9, CF 1.8 per 10,000 — those three = **73% of all DBS cases**. First report using cases from all 50 states.

**★ Essential read before you request data — tells you exactly how usable the infant-level file is**
> Omari A, Reeves SL, Prosser LA, et al. **Usability of NewSTEPs Data for Assessing the Characteristics of Infants with Newborn Screening Disorders.** *Int J Neonatal Screen.* 2022 Jul 19;8(3):42. doi:10.3390/ijns8030042. PMID 35892472. PMC9326755.
> - `https://pmc.ncbi.nlm.nih.gov/articles/PMC9326755/` — **VERIFIED** (200)
>
> 24,129 cases, 34 disorders, 45 states, birth years 2006–2020. **Missingness: sex 3.8%, birth weight 7.0%, gestational age 31.7%, race/ethnicity 39.7%.** After dropping 21 states with ≥50% missing race/ethnicity, only **16,010 cases from 24 states** remained. **States were not identified in the released dataset.** Findings: Hb S 71.0% Black/non-Hispanic; MPS I 70.3% Black/non-Hispanic; MMA 48.7% Hispanic; MSUD 45.7% Hispanic.

**Case-definition harmonization**
> Sontag MK, Sarkar D, Comeau AM, et al. **Case Definitions for Conditions Identified by Newborn Screening Public Health Surveillance.** *Int J Neonatal Screen.* 2018;4(2):16. doi:10.3390/ijns4020016. PMID 29862374. PMC5978752.
> `https://pmc.ncbi.nlm.nih.gov/articles/PMC5978752/` — **VERIFIED** (200)

**Program/infrastructure background**
> Ojodu J, Singh S, Kellar-Guenther Y, et al. **NewSTEPs: The Establishment of a National Newborn Screening Technical Assistance Resource Center.** *Int J Neonatal Screen.* 2018;4(1):1. doi:10.3390/ijns4010001. PMID 33072927. PMC7510199 — **VERIFIED** (200)

> Yusuf C, Sontag MK, Miller J, et al. **Development of National Newborn Screening Quality Indicators in the United States.** *Int J Neonatal Screen.* 2019;5(3):34. doi:10.3390/ijns5030034. PMID 33072993. PMC7510218 — **VERIFIED** (200)

**Other verified NewSTEPs-derived papers**
- Jones E, Singh S, McKasson S, et al. *Learning Collaborative to Support CQI in Newborn Screening.* IJNS 2025 Aug 27;11(3):70. doi:10.3390/ijns11030070. PMID 40981301. PMC12452637 — **VERIFIED** (200). 36 QI projects funded 2019–2024.
- Singh S, Caggana M, Johnson C, et al. *COVID-19 Pandemic-Related Impacts on NBS Public Health Surveillance.* IJNS 2022;8(2):28. PMC9036218 — **VERIFIED** (200)
- Edelman S, Desai H, Pigg T, et al. *Landscape of CAH Newborn Screening in the US.* IJNS 2020;6(3):64. PMC7569894 — **VERIFIED** (200). (`https://www.mdpi.com/2409-515X/6/3/64` — **UNVERIFIED**, 403)
- Sontag MK, Miller JI, McKasson S, et al. *NBS timeliness QI initiative.* PLoS One 2020;15(4):e0231050. PMC7117765
- Hale K, Kellar-Guenther Y, McKasson S, et al. *Expanding NBS for Pompe Disease in the US.* IJNS 2020;6(2):48. PMC7423006
- Kellar-Guenther Y, Sontag MK, Linder E, et al. *Analyzing Patterns in NewSTEPs Site Review Recommendations.* IJNS 2019;5(1):13. PMC7510203

---

## 7. Data Quality Caveats

**Self-reported and non-authoritative.** Official language: *"due to the self-reporting, voluntary nature of data collection, the data could be subject to errors or inaccuracies."*

**Provisional and retroactively mutable.** *"Newborn screening programs can modify or delete past data at any time, even months or years after they are initially entered."* **Demonstrated:** birth-year 2020 total was **6,923** in the 2022 report and **6,781** in the 2024 report — same n=51, revised down 142 (−2.1%). Individual conditions moved more: 2020 CF 768→761, SMA 135→141, GALT 77→69.

**Reporting completeness is *declining*, not improving.** n=51 (2020) → n=44 (2021) → **n=42 (2022)**. The 2024 report flags 2022 as *"pending."* The apparent drop in totals (6,781 → 5,543 → 5,617) is substantially an **artifact of fewer reporting programs**, not falling incidence. Do not read these as a trend line.

**Rule of Five suppression.** Blocks any cell with ≤5 newborns. In the 2024 national table this already erased **HCY, TFP, BKT, HMG, MCD** entirely and partially erased LCHAD and Cbl A,B. At *state* level this will suppress nearly every rare condition. **This is the single biggest obstacle to your per-condition-per-state goal.**

**Two-year lag** by design. As of Aug 2026, expect ~2023 births as the newest reasonably complete year.

**Case definitions are not harmonized.** The report is explicit: *"variations may exist depending on the case definitions utilized within the program… (e.g., for PKU some programs may have included cases of hyperphe, while others only include classical PKU)."* Also flagged: some programs may have counted **hemoglobinopathy trait** (carriers) inside sickle-cell case counts. Milder/later-onset phenotypes are inconsistently classified. **NewSTEPs states it is "currently working on standardizing case definitions."**

**Active harmonization effort:** the *Outcomes Following a Screen Positive* survey contains standardized case definitions to be integrated into case collection, after which historical case data **will be restated**. The instrument is the NewSTEPs Case Worksheets / **"Diagnostic Form Templates for Newborn Screening," Version 2.0, July 2026** — `https://www.newsteps.org/media/5/download?inline` — **VERIFIED** (200, 76 pages, PDF). Covers 30 condition-specific worksheets with structured final-outcome fields (*Affected / Carrier-Heterozygote / False Positive-Unaffected / Other*), biochemical confirmatory results, and molecular genetics (genes tested, variants). Also collects **Infant's Name, DOB, Mom's Name, State Unique ID** — i.e., the source records are identifiable at the state level even though NewSTEPs receives de-identified data.

**Denominator problem.** Case counts are not incidence. *"Not all states and territories offered universal screening for all disorders during the reporting period; therefore, case counts may not be representative of the true national birth prevalence."* Recently-added conditions (SMA, X-ALD, Pompe, MPS I/II, Krabbe, GAMT, MLD, DMD) have partial and *time-varying* denominators — you must join to the state-profile API's `statusYear`/`statusMonth` implementation dates and do fractional-year weighting, exactly as the IJNS authors did.

**Internally inconsistent national estimates — be careful which you quote.** The same IJNS 2023 paper gives **7,389** (results, = 20.07/10,000 × 3,686,219 births), **8,180** (discussion), and **">8,500"** (conclusion). The 2022 Annual Report cites 8,180. The **2024 Annual Report claims "over 14,000 newborns are detected for the core RUSP disorders" citing that same paper** — that figure only reconciles if hearing loss (~6,300/yr) and CCHD are included, which the paper's DBS-only analysis excludes. **Treat "14,000" as all-RUSP-including-point-of-care, and ~7,400–8,500 as DBS-only.**

**Coverage scope mismatch for your use case.** NewSTEPs covers ~60 screened conditions (RUSP core + secondary + state additions) and counts **incident newborns only** — not prevalent diagnosed patients, not late-onset diagnoses, not conditions outside newborn screening. For a repurposing thesis you would be sizing *annual birth incidence in screened states*, then modeling forward.

**Excluded from all case tables:** CCHD, hearing loss, GAMT, Infantile Krabbe (newest RUSP additions, 2023–2024).

---

## Practical Recommendation

1. **Free and immediate:** scrape `/data-api/state/profile?institution={state}&year={year}` across 56 programs × 2016–2026 to build the definitive screening-coverage matrix (which state screens what, since when, by what method). Combine with the plain-HTML Screened Conditions Report. This is unauthenticated and needs no permission.
2. **Free and immediate:** national case counts by condition for **birth years 2015–2022** are already published across the four annual report PDFs plus the IJNS/MMWR papers — the 2022 report's Table 14 is the best single source because it is unsuppressed at n=51.
3. **For state-level counts:** submit the Cases Data webform, but budget **~8 weeks minimum** and expect the Rule of Five plus per-state consent to gut the rare-condition cells. Consider requesting **HRSA-region-level** rather than state-level aggregation (the form has an `hrsa_region` parameter) — 10 regions will survive suppression far better than 50 states.
4. **Alternative for state-level rare disease counts:** individual state NBS program annual reports (published independently by many state health departments) are often more granular than what NewSTEPs will release centrally.