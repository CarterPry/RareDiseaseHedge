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

**What survives.** Orphan designation and 7-year orphan exclusivity (§ 360bb / § 360cc) remain fully available on 505(b)(2) repurposing. And the "European Mucinex" pattern from the call — a drug approved in the EU or Japan that never entered the US because an incumbent owned the category — is *exactly* the shape that **does** qualify, because its active moiety has never been approved in the US. That leg of the thesis is intact and is now the whole PRV story.

**Program window.** The RPD PRV program lapsed after 2024-12-20 and was reauthorized by the **Consolidated Appropriations Act, 2026 (Pub. L. 119-75 § 6604(a)), enacted 2026-02-03**. § 360ff(b)(5) now reads: *"The Secretary may not award any priority review vouchers under paragraph (1) after September 30, 2029."* There is **no longer a separate designation-by deadline** — the binding constraint is **NDA/BLA approval on or before 2029-09-30**.

**Design consequence.** The screening pipeline needs a hard `active_moiety_previously_approved_in_US` boolean that routes every candidate into one of two disjoint funnels:

- **Funnel A — PRV funnel.** Never-approved-in-US active moiety → 505(b)(1) → RPD designation → PRV. Small, high-value, hard.
- **Funnel B — orphan funnel.** US-approved active moiety repurposed → 505(b)(2) → orphan designation → 7-year exclusivity. No voucher. Large, cheap, and where the international-registration revenue play lives.

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

**The PRV ledger lives in the Federal Register API, not on fda.gov.** `https://www.federalregister.gov/api/v1/documents.json`, no auth, JSON, daily. Live census on 2026-08-05: **73 RPD PRVs awarded** (2014-03-12 → 2026-05-11), 9 material-threat MCM PRVs, 32 redemption notices. Use `conditions[term]`, not `conditions[search]` — the latter is silently ignored and returns a null count. Title strings are not stable across years (including a literal typo, *"Notice of Approval of Product U nder Voucher"*), so match with a tolerant regex. Tropical-disease PRV issuances are **not** in the Federal Register at all.

**`"Rare Diseases"[MeSH]` is a near-useless recall filter.** 15,927 records across all of PubMed for a domain of ~7,000 diseases, applied inconsistently by indexers — and only ~25% of newly-entered records are MeSH-indexed at all (measured: 43,431 of 175,025 records entered 2026-07-01→2026-08-05). **Detection must run on `[tiab]` + `[pt]` + a disease-name dictionary expanded from Orphanet/MONDO; MeSH is a backfill layer, not a detection layer.**
