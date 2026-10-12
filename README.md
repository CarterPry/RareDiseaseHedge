# RareDiseaseHedge — Data Source Map

Source inventory and machine-access pathways for a rare-disease drug repurposing pipeline. Every URL in these files was fetched live on **2026-08-05** and is marked **VERIFIED** or **UNVERIFIED**. Byte counts, record counts and HTTP statuses are measured, not remembered.

**Read `HANDOFF.md` first** — it has the full session log, what is finished, what is not, and the exact prompts to resume.

---

## ⚠️ The finding that changes the strategy

The thesis as described — *screen off-patent generics → 505(b)(2) approval → earn a transferable Priority Review Voucher, mass-produce vouchers at ~$300–400k per trial* — **is foreclosed by statute for the generic-repurposing leg.**

**21 U.S.C. § 360ff(a)(4)(B)(i) [FD&C Act § 529]**, verified independently against the US Code on 2026-08-05:

> (I) that contains **no active moiety** … **that has been previously approved in any other application under subsection (b)(1), (b)(2), or (j) of section 355**; and
> (II) **that is the subject of an application submitted under section 355(b)(1)**

Both prongs must hold. So:

| Route | RPD PRV eligible? | Why |
|---|---|---|
| Off-patent US generic repurposed via **505(b)(2)** | **NO — categorically** | Active moiety already approved under 505(b)(1)/(b)(2)/(j), *and* 505(b)(2) is not 505(b)(1) |
| Drug **approved abroad, never approved in the US**, via full **505(b)(1) NDA** | **YES** | Novel active moiety in the US |
| Biologic | 351(a) BLA, no previously approved active ingredient under 351(a)/351(k) | § 360ff(a)(4)(B)(ii) |

Three further statutory gates, all verified: the application must rely on **clinical data from a pediatric population** (D); must **not seek an adult indication** in the original RPD application (E); must be deemed **eligible for priority review** (C).

### ⚖️ MATERIAL CARVE-OUT — *Sun Pharma Advanced Research Co. v. FDA* (D.D.C. No. 1:24-cv-00946, Mehta, J., opinion entered 1 Dec 2025)

**Added 2026-08-06. This is the most important development since the original finding and it partially reopens the generic-repurposing route.**

**SEZABY** (phenobarbital sodium injection, for neonatal seizures) was approved November 2022. FDA **denied** the RPD voucher, citing **NDA 000597** (phenobarbital + atropine, submitted 1939) as a previously-approved active moiety. Sun/SPARC sued. **The court granted summary judgment for Sun**, holding that a pre-1962 *"deemed approved"* NDA is **not** *"previously approved"* under § 360ff(a)(4)(B)(i).

The court's reasoning — "approved" requires affirmative agency action:

> …to *"sanction officially," "confirm authoritatively," or "accept as satisfactory."* NDA 000597 became effective through FDA **inaction** rather than positive approval, and was withdrawn for lack of efficacy in 1982. **"In no ordinary sense then was NDA 000597 ever 'approved.'"**

The court further noted that Hatch-Waxman signalled any "previous approval" must have "successfully navigated" the modern approval process, and rejected a reading in which a drug "never able to show efficacy and ultimately pulled from the market" could block future pediatric treatments.

**Outcome:** FDA awarded the voucher on **2026-02-03**. The 60-day appeal window from the 2025-12-01 ruling had by then expired, which strongly implies **FDA did not appeal**. *(Checked 2026-10-11: no notice of appeal on the RECAP docket and no D.C. Circuit docket on CourtListener; PACER itself not queried.)* On **2026-04-30** SPARC signed a definitive agreement to sell the SEZABY voucher for **US$195M** to an undisclosed buyer (HSR-conditioned; closing not yet confirmed) — the A2 carve-out therefore has a realised market price.

**What this changes — this is the business-relevant part:**

> **Grandfathered 1938–1962 drugs may qualify for rare pediatric (or tropical) disease PRVs when repurposed.** That is a specific, enumerable class of decades-old molecules — precisely the class this company targets.

So Funnel A is **larger than originally stated**. It now has two sub-populations:

- **A1 — never approved in the US at all.** Approved abroad, filed as 505(b)(1). The original finding.
- **A2 — US drugs whose *only* prior "approval" was a pre-1962 deemed-approved NDA.** Newly available per *Sun*.

**Limits — do not over-read this:**
- It is a **district court** decision (D.D.C.), persuasive but not binding elsewhere, and unreviewed on appeal.
- The carve-out is **narrow**: it rescues only drugs whose *sole* prior approval was pre-1962 deemed-approved. **Any modern 505(b)(1), 505(b)(2) or ANDA approval still bars the voucher outright.** Most off-patent US generics have exactly that history and remain categorically excluded.
- The application must still clear every other gate — 505(b)(1) filing, priority-review eligibility, pediatric clinical data, no adult indication.
- Confirm with regulatory counsel before relying on it.

**Secondary implication flagged by commentators:** the ruling also undercuts FDA's practice of searching approval records back to 1938 when determining **new chemical entity (NCE)** status — so NCE exclusivity determinations resting on pre-1962 records may be similarly vulnerable.

**Precedent value for the whole thesis:** SEZABY is an ancient generic molecule, reformulated for a rare pediatric indication, that ultimately earned a transferable voucher. That is a near-exact instance of the model — and it shows both that the model can work *and* that FDA will fight it.

---

**What survives.** Orphan designation and 7-year orphan exclusivity (§ 360bb / § 360cc) remain fully available on 505(b)(2) repurposing. And the "European Mucinex" pattern from the call — a drug approved in the EU or Japan that never entered the US because an incumbent owned the category — is *exactly* the shape that **does** qualify, because its active moiety has never been approved in the US. That leg of the thesis is intact and is now the whole PRV story.

**Program window.** The RPD PRV program lapsed after 2024-12-20 and was reauthorized by the **Consolidated Appropriations Act, 2026 (Pub. L. 119-75 § 6604(a)), enacted 2026-02-03**. § 360ff(b)(5) now reads: *"The Secretary may not award any priority review vouchers under paragraph (1) after September 30, 2029."*

**There is no separate designation deadline — and this is now confirmed at the amendment-note level, not inferred.** *(Re-verified 2026-08-05 against the US Code amendment notes after an external audit flagged it as unconfirmed.)* The prior regime did have two dates. The 2026 amendment did not *collapse* them; it **deleted the entire conditional clause**:

> **2026** — Subsec. (b). Pub. L. 119–75, § 6604(a), substituted **"September 30, 2029."** for *"December 20, 2024, unless the rare pediatric disease product application— (A) is for a drug that, **not later than December 20, 2024, is designated** under subsection (d) as a drug for a rare pediatric disease; and (B) is, **not later than September 30, 2026, approved** under section 355(b)(1) of this title or section 351(a) of the Public Health Service Act."*

The designation-by prong (A) and the separate approval-by prong (B) were struck together and replaced with a flat award deadline. **The single binding constraint is award — i.e. approval — on or before 2029-09-30.** Designation timing is unconstrained by statute; it is constrained only by the practical need to have designation in hand before approval, and by § 360ff(d)(2), which forces the RPD request to be filed simultaneously with an orphan or fast-track request.

*Related, from the same amendment notes:* **Pub. L. 117-9 (2021)** is the amendment that replaced the old *"contains no active ingredient (including any ester or salt of the active ingredient)"* test in (a)(4)(A)–(B) with the current **active moiety** language. The moiety concept the whole eligibility analysis turns on is therefore a 2021 change, and pre-2021 commentary on § 360ff eligibility should not be relied on.

**Design consequence.** The screening pipeline needs a hard `active_moiety_previously_approved_in_US` boolean that routes every candidate into one of two disjoint funnels:

- **Funnel A — PRV funnel.** Never-approved-in-US active moiety → 505(b)(1) → RPD designation → PRV. Small, high-value, hard.
- **Funnel B — orphan funnel.** US-approved active moiety repurposed → 505(b)(2) → orphan designation → 7-year exclusivity. No voucher. Large, cheap, and where the international-registration revenue play lives.

---

## 🔴 The verdict (2026-08-06) — read before planning

Three feasibility analyses were run, each challenged by **two opposed reviewers** (one arguing too optimistic, one too pessimistic) and reconciled. Full detail in `sources/25`–`27` and `sources/00-CANDIDATE-DISCOVERY-METHOD.md`.

**Funnel A is ~7 globally actionable programs, not 6–10 for one sponsor.**

| Filter stage | Mid-case | Range |
|---|---|---|
| Distinct ex-US approved moieties, post-join | 700–1,800 (905 KEGG Japan-only is an empirical floor) | wide |
| …with published rare pediatric evidence | 50 | 15–120 |
| …qualifying under the § 360ff(a)(3) pediatric test | 15 | 5–35 |
| …after FTO / orphan exclusivity / API / trial feasibility | **~7** | **2–15** |

That is the *entire global inventory* meeting all conditions simultaneously — not a per-sponsor pipeline. The A2 (pre-1962 *Sun Pharma*) carve-out adds only **0–3** more, and rests on an unreviewed district-court holding, so treat it as opportunistic rather than foundational.

**Per-program probability of reaching approval before the sunset: 3–5% generic → 20–22% optimized.** Four choices drive the difference:
1. Pick a disease with a **pre-existing patient registry**
2. Use an **MRA-country API manufacturer** (EU, UK, Canada, Japan, Australia, Israel, Switzerland)
3. **RDEA-aligned design** with a pre-specified natural-history external control
4. **File the IND directly**, skipping the pre-IND meeting (not required for a repurposed molecule with an established safety profile; saves 5–8 months)

**Conclusion: 6–10 simultaneous programs is not viable on ~$180k. One program, with all four choices optimized, is the correct strategy.**

### ⏰ Two time-critical items

**1. Unannounced foreign pre-approval inspections are now FDA practice.** *(Corrected 2026-10-12: the earlier text attributed this to the revised Compliance Program 7346.832. That CP, effective 2026-08-10, adds risk-based PAI selection, MRA reliance and remote assessments and keeps a 60-day notification goal for original NDAs — the word "unannounced" does not appear in it. The unannounced policy comes from FDA's Office of Inspections and Investigations announcement of 2025-05-06; FDA reported India 87% / China 61% of inspections unannounced in FY2026 to date.)** A **WHO-GMP-only site drops to ~50–60% PAI pass probability**; an MRA-country manufacturer rises to **~88%**. Your suppliers currently hold WHO certification, not FDA GMP — this is the second-largest lever on program success after disease selection, and the policy lands in days.

**2. Enrollment must start essentially now.** 37 months remain to the 2029-09-30 sunset. Under priority review (6-month clock + 60-day filing), the NDA must be submitted by **~November 2028**, implying LPLV by Feb 2028 and **enrollment start between August 2026 (conservative) and February 2027 (optimistic)**. A program started from scratch today sits at the outer edge of the optimistic case, with no margin for slippage.

### Recruitment reality

Only **~4.7–14%** of a diagnosed population is realistically enrollable after six successive cuts (age, severity, standard-of-care exclusion, geography/travel, competing trials, parental consent). For a disease with 300 diagnosed US patients that is **14–42 patients** — so a 20-patient trial is feasible but tight, and running 6–10 such trials at once is not.

---

## Files

### Core

| File | Domain |
|---|---|
| [HANDOFF.md](HANDOFF.md) | Session log, todo, methodology, resume prompts — **start here** (see §0 on transcript recovery) |
| [sources/01-fda-us-regulatory.md](sources/01-fda-us-regulatory.md) | FDA databases and APIs — PRV ledger, orphan designations, openFDA, Drugs@FDA, Orange Book, DailyMed, shortages, guidance feed |
| [sources/03-disease-prevalence-patients.md](sources/03-disease-prevalence-patients.md) | Orphanet/Orphadata, MONDO, GARD, OMIM, HPO, ICD, prevalence→US-patient-count method |
| [sources/04-literature-trials.md](sources/04-literature-trials.md) | PubMed E-utilities, PMC OA bulk, Europe PMC, ClinicalTrials.gov v2, ICTRP, CTIS, jRCT/CTRI/ChiCTR, OpenAlex — with runnable detection queries |
| [sources/06-reference-regulators.md](sources/06-reference-regulators.md) | Japan PMDA, Australia TGA, UK MHRA, Swissmedic — machine-accessible approval data |
| [sources/07-regional-multilateral.md](sources/07-regional-multilateral.md) | ZAZIBONA, African Medicines Agency, EAEU, CARPHA/CRS, Pacific, PIC/S, EU-M4all |
| [sources/08-who-reliance.md](sources/08-who-reliance.md) | WHO Prequalification, EML/EMLc, Collaborative Registration Procedure, WHO-Listed Authority |
| [sources/09-cheminformatics-repurposing-dbs.md](sources/09-cheminformatics-repurposing-dbs.md) | PubChem, ChEMBL, Open Targets, DrugCentral, repoDB, Broad Drug Repurposing Hub |
| [sources/10-newborn-screening.md](sources/10-newborn-screening.md) · [11](sources/11-newsteps-detail.md) · [12](sources/12-patient-finding-infrastructure.md) · [13](sources/13-real-world-data-platforms.md) | RUSP/state panels, NewSTEPs deep dive, NORD/UDN/RDCRN/ERNs, RWD platforms |

### Countries and regulators

| File | Domain |
|---|---|
| [ukraine.md](sources/countries/ukraine.md) | State Expert Center, Law 2469-IX transition timeline, wartime provisions, drlz register, grandfathering |
| [georgia.md](sources/countries/georgia.md) | RAMA, recognition (7 working days / 500 GEL) vs national regime, the 36-country list, GMP gate |
| [armenia.md](sources/countries/armenia.md) | SCDMTE, EAEU transition, full fee schedule, well-established-use waiver |
| [botswana.md](sources/countries/botswana.md) | BoMRA, reliance pathway, gazetted fees, BRIMS public API, GMP reliance limits |
| [barbados-seychelles-albania-samoa.md](sources/countries/barbados-seychelles-albania-samoa.md) | The four remaining target markets |
| [uk-mhra.md](sources/countries/uk-mhra.md) · [switzerland-swissmedic.md](sources/countries/switzerland-swissmedic.md) | Reference regulators, incl. MHRA International Recognition Procedure |
| [_crosscheck-ge-am-ua-bw.md](sources/countries/_crosscheck-ge-am-ua-bw.md) | **Second independent pass** over Georgia/Armenia/Ukraine/Botswana — use to cross-check |

### IP and exclusivity

| File | Domain |
|---|---|
| [05-ip-exclusivity-PARTIAL.md](sources/05-ip-exclusivity-PARTIAL.md) | European SPCs, INPADOC event codes, national registers, paediatric extension, manufacturing waiver |
| [ip/spc-verification.md](sources/ip/spc-verification.md) | Unabridged SPC source verification |
| [ip/google-patents-bigquery.md](sources/ip/google-patents-bigquery.md) | Google Patents on BigQuery — tables, cost model, free-tier querying |
| [ip/epo-ops-espacenet.md](sources/ip/epo-ops-espacenet.md) | EPO Open Patent Services, OAuth2, SPC via the legal service |
| [ip/wipo-fto-aggregators.md](sources/ip/wipo-fto-aggregators.md) | WIPO PATENTSCOPE and commercial FTO aggregators |

### Provenance

`sources/_recovered/` holds verbatim agent output recovered from subagent transcripts, including **unabridged** Armenia and Botswana reports (the on-disk country files were shortened by the parent — diff before trusting the short versions) and the original parent outputs behind files 01/03/04.

---

## Three other findings worth surfacing now

**There is no public Rare Pediatric Disease designation list.** Confirmed, not assumed: a sweep of all 43 fda.gov sitemap pages (85,349 URLs) returns exactly two `rare-pediatric` hits — the program page and the guidance page. § 360ff(f)(1) requires Federal Register notice only for voucher *issuance* and for approval *under* a voucher; no publication duty attaches to designations. Competitor RPD intelligence must be built on SEC EDGAR full-text search and newswire, not on FDA. The usable proxy: § 360ff(d)(2) requires the RPD request to be filed *simultaneously* with an orphan or fast-track request, so **a new orphan designation for a pediatric-onset serious disease is a leading indicator of a concurrent RPD request** — and the orphan database is fully downloadable and daily-fresh.

**The PRV ledger lives in the Federal Register API, not on fda.gov.** `https://www.federalregister.gov/api/v1/documents.json`, no auth, JSON, daily. Live census on 2026-08-05: **73 RPD PRVs awarded** *(76 as of 2026-10-09: GENGLYCOS 2026-08-19, ZANVASTRO 2026-09-03, FAYUVI 2026-09-17 added — plus Emcitate/tiratricol, approved 2026-09-28 with a voucher, whose notice had not yet published)* (2014-03-12 → 2026-05-11), 9 material-threat MCM PRVs, 32 redemption notices. Use `conditions[term]`, not `conditions[search]` — the latter is silently ignored and returns a null count. Title strings are not stable across years (including a literal typo, *"Notice of Approval of Product U nder Voucher"*), so match with a tolerant regex. Tropical-disease PRV issuances are **not** in the Federal Register at all.

**`"Rare Diseases"[MeSH]` is a near-useless recall filter.** 15,927 records across all of PubMed for a domain of ~7,000 diseases, applied inconsistently by indexers — and only ~25% of newly-entered records are MeSH-indexed at all (measured: 43,431 of 175,025 records entered 2026-07-01→2026-08-05). **Detection must run on `[tiab]` + `[pt]` + a disease-name dictionary expanded from Orphanet/MONDO; MeSH is a backfill layer, not a detection layer.**
