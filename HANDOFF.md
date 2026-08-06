# HANDOFF — session state, log, and what's left

**Session date:** 2026-08-05 (session 1), 2026-08-05 (session 2 — recovery)
**Working directory:** `/Users/carte/Downloads/RareDiseaseHedge` (was empty at session start; not actually a git repo despite the initial status snapshot — run `git init` if you want history)
**Stopped:** deliberately, at user request, mid-research. Nothing is broken; work is partitioned cleanly.

---

## 0. SESSION 2 — TRANSCRIPT RECOVERY (read this before §5)

**Large parts of §5 "What is NOT done" were, in fact, already done.** The work existed but had never been written to disk, because when a parent agent is interrupted its children's completed reports survive only inside the subagent transcripts.

Mining `…/subagents/agent-*.jsonl` (30 files) found that **25 of 30 agents produced complete final reports**. Five of those had already been synthesized into files 01/03/04 and `countries/armenia.md` / `botswana.md`. **The other 20 had never been written down.** All are now extracted verbatim into `sources/`, each with a provenance header naming its source transcript.

Recovered in full — every one of these was listed as a gap in §5.1:

| Now on disk | Was listed as |
|---|---|
| `countries/ukraine.md` (58.8 KB) | §5.1 "second priority — closing window" |
| `countries/georgia.md` (34.9 KB) | §5.1 "highest priority" |
| `countries/barbados-seychelles-albania-samoa.md` (46.7 KB) | §5.1 four separate unresearched markets |
| `countries/uk-mhra.md` (46.4 KB) | §5.1 reference regulators |
| `countries/switzerland-swissmedic.md` (27.0 KB) | §5.1 reference regulators |
| `06-reference-regulators.md` (46.0 KB) — PMDA, TGA, MHRA, Swissmedic | §5.1 reference regulators |
| `07-regional-multilateral.md` (59.8 KB) — ZAZIBONA, AMA, EAEU, CARPHA, Pacific, PIC/S, EU-M4all | §5.1 "multilaterals", all of it |
| `08-who-reliance.md` (40.4 KB) — WHO PQ, EML/EMLc, CRP, WLA | §5.1 WHO |
| `ip/google-patents-bigquery.md` (20.1 KB) | §3 row 5b: **"BigQuery findings lost"** — they were not lost |
| `ip/epo-ops-espacenet.md`, `ip/wipo-fto-aggregators.md`, `ip/spc-verification.md` | §5.2 IP sources |
| `09-cheminformatics-repurposing-dbs.md` (27.0 KB) | §5.2 PubChem/ChEMBL/DrugCentral/repoDB/Open Targets/Broad |
| `10`–`13`: newborn screening, NewSTEPs, patient-finding, RWD platforms | detail behind file 03 |

Also recovered:
- `countries/_crosscheck-ge-am-ua-bw.md` — a **second, independent pass** over Georgia/Armenia/Ukraine/Botswana by a different agent. Use it to cross-check the single-country files; disagreements are worth chasing.
- `_recovered/armenia-UNABRIDGED.md` (50.6 KB vs 38.3 KB on disk) and `_recovered/botswana-UNABRIDGED.md` (50.7 KB vs 41.6 KB). **The on-disk country files were abridged by the parent.** Diff before trusting the short versions.

**Substantive correction to a §5.1 premise.** The call assumed Ukraine was a now-or-never window ("10 business days now, 10 months starting January"). The recovered Ukraine file, read from the statute at `zakon.rada.gov.ua`, finds that Law No. 2469-IX is **набирає чинності 18.08.2022 but вводиться в дію 1 January 2027** (date set by Law No. 4239-IX of 12.02.2025) — and Розділ XII grandfathers existing registrations: unlimited-term MAs stay valid indefinitely and are re-papered as a free Register extract with no dossier changes. The real cliff is the dossier/labelling conformity obligation, not the MA. There *is* a flagged statutory ambiguity (the five-year clocks anchor to 18.08.2022, producing an 18 August 2027 date that falls after the law becomes operative) that needs Ukrainian counsel. **The urgency is real but differently shaped than assumed.**

**Methodology lesson, added to §7:** when a parent agent is interrupted, mine the child transcripts *before* re-running anything. Roughly 600 KB of finished, high-quality research was sitting unread. The §7 fix ("have children write their own files") prevents the problem going forward; transcript mining recovers it retroactively.

**Session 2 also ran a follow-up workflow** covering what remains genuinely unresearched after recovery: EMA, Health Canada, drug identity normalization, Orange Book patent/exclusivity, US PTE, PatentsView, the orphan/RPD conflict check, 505(b)(2) precedent mining, drug-knowledge licensing, PMDA deep-dive, Korea/Taiwan/China, all three manufacturing files, the PRV transaction market, competitor detection, FDA process mechanics — plus adversarial verification and a synthesis of the candidate-discovery diff method. See the file list in `README.md` for what landed.

> **Harness note for whoever resumes:** subagents fail instantly with `400 output_config.effort 'xhigh' is not supported when thinking is disabled` on opus-tier models in this configuration. Pin agents to `model: 'sonnet'` (which is what produced all of session 1's work anyway), or enable thinking / lower effort via `/config`.

---

## 0.1 SESSION 2 COMPLETE — final state (2026-08-06)

**All research tracks in §5 and §9 are now closed.** 59 files, ~2.5 MB, in a private GitHub repo
(`CarterPry/RareDiseaseHedge`) with continuous auto-push via `scripts/autosync.sh`.

**Two findings that changed the strategy since §0 was written:**

1. ***Sun Pharma Advanced Research Co. v. FDA* (D.D.C., 2025-12-02)** — a pre-1962 "deemed approved"
   NDA is NOT "previously approved" under § 360ff(a)(4)(B)(i). FDA awarded the SEZABY voucher
   2026-02-03 and did not appeal. Creates Funnel **A2** (1938–1962 grandfathered drugs). Narrow:
   any modern 505(b)(1)/(b)(2)/ANDA history still bars. See README and `sources/22-…`.

2. **The feasibility verdict** — Funnel A is ~7 globally actionable programs (range 2–15), not 6–10
   per sponsor; A2 adds 0–3. Per-program success 3–5% generic vs 20–22% optimized. **6–10 simultaneous
   programs is not viable at ~$180k; one optimized program is the correct strategy.** See README and
   `sources/25`–`27`, each adversarially reviewed from two opposed directions.

**Time-critical:** FDA CP 7346.832 (revised) takes effect **2026-08-10** — unannounced PAIs at non-US
sites; WHO-GMP-only drops PAI pass to ~50–60% vs ~88% for an MRA-country manufacturer. And enrollment
must start **now** (Aug 2026 conservative / Feb 2027 optimistic) to clear the 2029-09-30 sunset.

**Recovery statistics for this session** — the dominant lesson:
| Event | Agents | Outcome |
|---|---|---|
| Session 1 parents interrupted | 30 transcripts | 20 complete reports recovered that had never been written to disk |
| Session 2 workflows hit API socket exhaustion | 27 agents | 15 had done 60–124 tool calls each; **all 15 recovered by mining transcripts** |

**Operational lessons added to §7:**
- Mine child transcripts BEFORE re-running anything — ~600 KB of finished research was sitting unread
  after session 1, and 1,352 tool calls' worth after the session 2 failures.
- Cap workflow concurrency at ~4 agents. ~18 concurrent agents caused Anthropic API socket exhaustion
  (`FailedToOpenSocket` / `ConnectionRefused`) that killed 27 agents at once.
- Instruct agents to **Write their file early and refine it**, not to hold output in context until the
  end. The three agents that survived the socket failure were the ones that had already written.
- On this harness, opus-tier subagents fail with `400 output_config.effort 'xhigh' … thinking is
  disabled`. Pin `model: 'sonnet'` or enable thinking / lower effort via `/config`.

---

## 1. What was asked

Map every data source and *exact machine-access pathway* needed to build an automated screening and filing pipeline for a rare-disease drug repurposing company. Deliverable is the source map itself — topics and pathways laid out clearly enough to build from. The user is building the system; this is the reconnaissance layer.

### Business context driving the source selection

From a call transcript supplied as context. Summarized because it determines what counts as a relevant source:

- **Strategy leg 1 (US):** screen off-patent / generic drugs — and drugs approved abroad but never in the US — for published evidence in rare pediatric diseases. File FDA Rare Pediatric Disease designation + orphan designation + IND, run a small trial (~$300–400k), get approval, earn a transferable **Priority Review Voucher** (secondary market ~$150–250M). Parallelize across 6–10 programs. First IND cleared; first trial targeted to start before end of 2026.
- **Strategy leg 2 (international):** register the same generic in small/underserved markets for revenue and to absorb contract-manufacturer minimum order quantities. Named targets: **Georgia, Armenia, Ukraine, Botswana, Barbados, Seychelles, Albania, Samoa**. Georgia filed ~2 days before the call (7-business-day nominal). Rationale: the drug may be a normal commercial product elsewhere (the example given: a European mucolytic that will never be approved in the US because an incumbent owns the category) even while it is a rare-disease product in the US.
- **Constraints stated:** heavily agent-automated filing infrastructure; ~$180k raised April 2026, otherwise bootstrapped; manufacturing finalized or near-final for ~4 products; suppliers hold WHO certification with FDA GMP readiness planned but not current; no lab, no preclinical — candidates are decades-old drugs approved somewhere already; Japan flagged as a source of approved-but-never-commercialized-elsewhere drugs; Ukraine flagged as time-sensitive because of an EU/EMA regulatory transition with a possible grandfathering window.
- **Motivation:** family experience with off-label access and unaffordable IVIG; access is the stated mission, PRV economics are the financing mechanism.

### The instruction that shaped output quality

Every research agent was given this, and it is the single most important thing to preserve if you re-run any of them:

> Verify URLs actually resolve using WebFetch — do not rely on memory. Mark each as VERIFIED or UNVERIFIED. Flag anything dead, moved, paywalled, or that you could not confirm. Where you cannot verify something, say so explicitly rather than guessing — an honest "no public database, must contact the ministry directly, here's the ministry URL" is far more useful than a plausible-sounding fabrication.

This is why the output contains things like a transcribed misprint in the Botswana gazette (`"1 1600"`), an incomplete TLS chain on pharm.am, and a Federal Register API parameter that is silently ignored. Those are the findings that save weeks. **Do not relax this instruction on re-runs.**

---

## 2. The headline result

**The core PRV thesis is statutorily foreclosed for the generic-repurposing leg.** Full detail in `README.md`; the one-line version:

**21 U.S.C. § 360ff(a)(4)(B)(i)** requires that the drug contain **no active moiety previously approved** under 505(b)(1)/(b)(2)/(j) **and** be the subject of an application submitted under **505(b)(1)**. A repurposed US generic fails both prongs. A drug **approved abroad but never in the US**, filed as a full 505(b)(1), passes.

This was found by the FDA research agent and then **independently re-verified** by fetching the US Code directly (`uscode.house.gov`, prelim, 2026-08-05). Both readings agree. Treat it as settled unless FDA counsel says otherwise.

Downstream consequence for the pipeline: a hard `active_moiety_previously_approved_in_US` boolean splitting candidates into a PRV funnel (Funnel A) and an orphan-exclusivity funnel (Funnel B). These need different screening criteria, different filing playbooks, and different economics. Anything built before this branch exists will be built wrong.

**Program window is real and reauthorized:** Consolidated Appropriations Act, 2026 (Pub. L. 119-75 § 6604(a)), enacted 2026-02-03; PRVs may not be awarded after **2029-09-30**; no separate designation deadline any more.

---

## 3. Session log

| # | Agent / action | Status | Output |
|---|---|---|---|
| 0 | `WebSearch` — PRV reauthorization status | done | Confirmed CAA 2026, sunset 2029-09-30 |
| 1 | Agent: **FDA / US regulatory databases** | **completed** | `sources/01-fda-us-regulatory.md` (59.6 KB) |
| 2 | Agent: **International regulators + reliance pathways** | **interrupted** | Parent produced nothing; two children finished — see rows 2a/2b |
| 2a | ↳ child: Armenia | **completed** | `sources/countries/armenia.md` |
| 2b | ↳ child: Botswana / BOMRA | **completed** | `sources/countries/botswana.md` |
| 3 | Agent: **Disease prevalence, ontologies, patient-finding** | **completed** | `sources/03-disease-prevalence-patients.md` (86.3 KB) |
| 4 | Agent: **Literature + trial registry mining** | **completed** | `sources/04-literature-trials.md` (71.7 KB) |
| 5 | Agent: **Drug identity, IP/exclusivity, repurposing DBs** | **interrupted** | One child finished — row 5a; three children killed mid-run |
| 5a | ↳ child: SPC / patent term extension | **completed** | `sources/05-ip-exclusivity-PARTIAL.md` |
| 5b | ↳ child: "Verify patent and SPC data sources" | **killed** | last message: *"BigQuery is done. Let me close out PTE — Orange Book data files and the Federal Register PTE notice stream."* — BigQuery findings lost |
| 5c | ↳ child: "Verify foreign regulator drug lists" | **killed** | last message: *"Flags are HTML-escaped. Let me recount."* |
| 5d | ↳ child: "Verify Asia regulator drug lists" | **killed** | last message: *"Good — most hosts are reachable. Let me dig into each in parallel."* |
| 6 | `WebFetch` — independent verification of 21 U.S.C. § 360ff | done | Confirmed the blocking finding |
| 7 | Agent: **Manufacturing / API supply chain / GMP** | **never launched** | — |
| 8 | Agent: **PRV transaction market / financial intel** | **never launched** | — |

**Why 2 and 5 were interrupted:** they spawned many parallel children and were cut off at the parent level while children were still running. Children that finished before the cut returned complete, high-quality work; the parents never got to synthesize. This is the main structural lesson — see §7.

---

## 4. What is complete and trustworthy

### `sources/01-fda-us-regulatory.md`
FDA databases and APIs. 16 sections. Highlights beyond the § 360ff finding:
- **No public RPD designation list exists** — proven by sweeping all 43 fda.gov sitemap pages (85,349 URLs) for `rare-pediatric`: exactly 2 hits, neither a list. Competitor detection must run on SEC EDGAR + newswire. Usable proxy: § 360ff(d)(2) forces the RPD request to be filed simultaneously with an orphan/fast-track request, so new orphan designations for pediatric-onset serious diseases lead RPD requests, and the orphan DB *is* downloadable.
- **The PRV ledger is the Federal Register API**, not fda.gov. Live census: 73 RPD PRVs awarded 2014-03-12→2026-05-11, 9 MCM, 32 redemptions. Use `conditions[term]` not `conditions[search]`. Title strings unstable across years incl. a literal typo. Tropical PRV issuances never appear in the FR at all.
- Orphan Drug Designations database is fully downloadable — described as the workhorse.
- Sections on openFDA, Drugs@FDA bulk, Orange Book, Purple Book, DailyMed/NDC, shortages, a structured guidance feed, expanded access, unapproved-marketed-drugs lists, IND visibility, and a dead/moved URL ledger.

### `sources/03-disease-prevalence-patients.md`
Three architecture decisions stated up front and worth taking seriously:
- **MONDO is the hub ID**, not ICD and not OMIM — CC BY 4.0, monthly, diff files, 10,176 OMIM + 10,491 Orphanet + 15,947 GARD + 21,660 UMLS/MedGen xrefs.
- **Only 1,053 of 11,645 Orphanet disorders (9%) have their own ICD-10 code**; 6,768 carry a code Orphanet invented. Claims databases are ICD-10-only. This decides which real-world-data platform is worth buying.
- **OMIM requires a paid JHU licence** for a for-profit building a derivative database. Quarantine until signed; MONDO + HPO is the licence-clean substitute.
- Orphadata bulk endpoints verified by actual download. **`orpha.net` itself is bot-walled** (JS proof-of-work) — use `orphadata.com` / `api.orphadata.com` (free, unauthenticated JSON), never `orpha.net`, in a pipeline.
- Also covers GARD, HPO, ICD-11/10, ClinGen/ClinVar/MedGen, prevalence→US-patient-count methods, NORD/RDCRN/UDN patient infrastructure, N3C/All of Us/TriNetX/Truveta/Komodo, newborn screening (RUSP/NewSTEPs), and a ranked end-to-end workflow from "disease name in a case report" to "N diagnosed US patients + the 3 centers that treat them."

### `sources/04-literature-trials.md`
- **`"Rare Diseases"[MeSH]` is a near-useless recall filter** — 15,927 records in all of PubMed; only ~25% of newly-entered records are MeSH-indexed (43,431 of 175,025 measured over 2026-07-01→2026-08-05). Detection must run on `[tiab]` + `[pt]` + an Orphanet/MONDO-derived disease-name dictionary. MeSH is a backfill layer.
- Contains **six numbered, runnable, live-tested query strings** (Q1–Q6), including the two meant to be cron'd daily (Q5 detection, Q6 repurposing-vocabulary arm), with verified hit counts.
- PMC OA bulk via S3 with an ETag/last-modified diff recipe; commercial vs non-commercial licence buckets kept separate — **respect that split, it constrains redistribution**.
- Europe PMC, ClinicalTrials.gov API v2, ICTRP, CTIS/EudraCT, jRCT, CTRI, ChiCTR, ISRCTN, ANZCTR, medRxiv/bioRxiv, OpenAlex/Semantic Scholar/Crossref.

### `sources/countries/armenia.md` and `.../botswana.md`
Both unusually deep — statute-level, with fee schedules transcribed from primary gazetted sources, public-register API endpoints tested live, GMP reliance rules quoted verbatim, and explicit lists of what could not be verified plus the exact questions to email the regulator. Read the "Gotchas" and "Questions to put to…" sections before doing anything in either country.

Two items in there are time-sensitive and commercially material:
- **Botswana:** a declared assessment backlog (Stakeholder Notice 2026-07-08) pushes new applications to **January 2027**; the reliance pathway at 3 months is the only realistic route. And a **draft fee regulation would move international applicants from BWP to USD pricing** — an orphan registration is **BWP 1,000** today versus a USD-denominated regime with USD 800/yr retention under the draft. Filing under the current schedule is worth real money.
- **Armenia:** the national route legally closed 2021-07-01 and the EAEU conversion window closed 2025-12-31 — but Decision 78 §21(a) means a single-reference-state EAEU MRP *is* the national procedure, and Armenia's own 2024 fee law still prices "general" and "simplified" routes. Whether SCDMTE still accepts a "simplified national" filing (500,000 AMD / 31 days) versus EAEU reference-state (2,100,000 AMD / 140 working days) is a **~4× cost and time difference and is unresolved.** Ask them.

---

## 5. What is NOT done

### 5.1 International regulators — ~~the big gap~~ MOSTLY CLOSED BY TRANSCRIPT RECOVERY

> ⚠️ **This section is superseded — see §0.** Nearly everything below was recovered from subagent transcripts in session 2 and is now on disk: Ukraine, Georgia, Barbados, Seychelles, Albania, Samoa, UK MHRA, Swissmedic, PMDA, TGA, WHO (PQ/EML/CRP/WLA), ZAZIBONA, AMA, EAEU, CARPHA, Pacific, PIC/S, EU-M4all. EMA and Health Canada were the genuine remaining holes and were researched fresh in session 2. The original text is kept below for provenance and because its *framing* of what to look for in each market is still useful.

**Done:** Armenia, Botswana.
**Not done:** everything else. Specifically:

*Target markets from the call, all unresearched:*
- **Georgia** — recognition regime, reportedly ~7 business days. A filing is already in flight there. **Highest priority** because there's live exposure and no documentation.
- **Ukraine** — State Expert Center; the EU/EMA transition timeline, whether pre-transition filings are grandfathered, and what changes in January. Flagged in the call as time-critical: *"if it goes 10 business days now, but it will take 10 months starting January, then I might as well file everything right now."* **Second priority — this is a closing window.**
- **Albania** — National Agency for Medicines and Medical Devices (AKBPM/NAMMD)
- **Barbados** — Drug Service / Barbados Drug Formulary; reportedly permit-based rather than full registration. Verify permit vs registration.
- **Seychelles** — same permit-vs-registration question. Note: listed as a *non-active* ZAZIBONA member in the archived BoMRA page.
- **Samoa** — including the reported ~$7M government arrears to suppliers causing essential-medicine stockouts (metformin reportedly absent ~1 year). Unverified; verify before building any thesis on it.

*Reference regulators (needed as the basis for every reliance filing):*
- **Japan PMDA** — approval database, review reports, and the "approved in Japan only, never commercialized elsewhere" angle. Called out in the transcript as a specific bottleneck worth working on.
- **EMA** — medicine database, EPARs, orphan register, **Article 58 / EU-M4all**
- **Health Canada** DPD (has a documented API), **Australia TGA** ARTG + orphan register, **UK MHRA**, **Swissmedic**
- **WHO** — Prequalification list, **Collaborative Registration Procedure (CRP)**, EML + EMLc

*Multilaterals:*
- **ZAZIBONA** — reference/rapporteur assignment, submission windows, timelines. BoMRA removed its ZAZIBONA page in the 2026 redesign; this must come from the SADC/MCAZ secretariat.
- **African Medicines Agency** continental listing procedure
- **EAEU** common pharmaceutical market (partially covered in the Armenia file)
- **CARPHA / Caribbean Regulatory System** — does it do regional review? Relevant to Barbados.
- Pacific pooled procurement — relevant to Samoa
- **PIC/S membership list** — determines which GMP certificates are accepted where. Confirmed so far: Armenia not a member; Botswana not a member; SAHPRA is the only African member.
- **WHO-Listed Authority (WLA) list** — now the operative concept replacing "SRA" at BoMRA and probably elsewhere. Last updated 2025-12-22.

### 5.2 Drug identity, repurposing databases, and most of IP

**Done:** European SPCs, INPADOC event codes, national patent registers, paediatric extension, manufacturing waiver (`sources/05-ip-exclusivity-PARTIAL.md`).
**Not done:**
- **Identity normalization** — RxNorm/RxNav, FDA UNII + GSRS, WHO INN, ATC/DDD. *(Note: `UNII_Data.zip` (16.9 MB) and `UNIIs.zip` (14.6 MB) were downloaded to the scratchpad before the agent was killed — they're there, just unanalyzed.)*
- DrugBank (free vs licensed terms), ChEMBL, PubChem PUG-REST, DrugCentral, repoDB, Open Targets, SIDER, Drug Repurposing Hub
- DailyMed SPL API
- **Orange Book patent + exclusivity data files** — the single most important missing IP source
- **Checking whether someone already holds orphan designation or 7-year orphan exclusivity on a drug-disease pair** — the core conflict check
- PatentsView API, Google Patents BigQuery dataset (the killed agent had *finished* this and the result was lost), EPO OPS, WIPO PATENTSCOPE, Espacenet
- **US patent term extension** (the killed agent was about to do Orange Book + the Federal Register PTE notice stream)
- The practical "this compound is free to use" checklist and its failure modes — method-of-use patents, formulation patents, data vs patent exclusivity, NCE exclusivity, pediatric exclusivity add-ons
- **The "approved abroad but not in the US" diff method** — ⚠️ **this is now the highest-value single item in the entire project**, because § 360ff makes it the *only* PRV-eligible funnel. Concretely: diff PMDA/EMA/Health Canada/TGA approved-substance lists against FDA Orange Book / Drugs@FDA / UNII. Two killed child agents (5c, 5d) were working exactly this and got most of the way.
- 505(b)(2) precedent mining from Drugs@FDA

### 5.3 Manufacturing and supply chain — never started

Nothing exists. Needed: FDA Drug Establishment registration DB; **Type II API DMF list**; EDQM CEP database; EudraGMDP (GMP certs + non-compliance reports); WHO PQ API/FPP lists; CDSCO India and Indian API exporters; NMPA China; PIC/S membership; FDA inspection classification DB, warning letters, **import alerts (66-40 etc.)**, 483s; Pharmaoffer/CPHI directories; MOQ realities; and tender/price references — MSH International Medical Products Price Guide, Global Fund, UNICEF, PAHO, UNDP.

Directly relevant to stated facts from the call: suppliers currently hold WHO certification, not FDA GMP, with FDA readiness planned. Worth verifying the claim that FDA does not inspect a facility until the NDA stage — the Armenia and Botswana files both show foreign regulators *do* have GMP-recognition rules with hard expiry windows (Botswana: reliance capped at **two consecutive desk-assessment cycles** for non-WLA-jurisdiction sites, then a mandatory physical inspection at USD 5,000–7,000).

### 5.4 PRV transaction market and competitive intel — never started

Needed: verifiable PRV sale price history (the $150–250M figure is unverified); SEC EDGAR full-text search API for 8-K/10-K voucher-sale disclosure; press-release feeds; who else is running this playbook. Note the FDA file already established that **RPD designations are invisible on FDA's side**, so EDGAR + newswire is the *only* competitor-detection channel — which makes this section more important than it looks.

Also worth tracking: the **Commissioner's National Priority Voucher (CNPV) pilot**, a separate non-statutory program with 15+ pages on fda.gov and 7 approvals to date. Award announcements are press releases, not Federal Register notices.

---

## 6. Open questions requiring a human

These cannot be resolved by research — someone has to ask.

**FDA / counsel:**
1. Confirm the § 360ff(a)(4)(B)(i) reading with regulatory counsel before any further spend on the generic-repurposing PRV thesis. If it holds, re-plan around Funnel A / Funnel B.
2. Given (D) "clinical data derived from studies examining a pediatric population" and (E) "must not seek an adult indication" — do the currently planned trial designs satisfy both?

**SCDMTE Armenia** (info@ampra.am, +374 60 83-00-73) — full list of 9 questions in `sources/countries/armenia.md` §14. The two that matter most: which ICH member authorities qualify for the simplified route, and whether a national simplified filing is still accepted in 2026.

**BoMRA Botswana** (registration@bomra.co.bw) — full list in `sources/countries/botswana.md` §12.5. Most urgent: which Act is actually in force (2013 vs 2025 — the guidance cites the 2025 Act but no commencement Order was found), and the exact screening fee (the gazette contains a misprint).

**Unverified claims from the call worth checking before relying on them:**
- PRV secondary-market price of $150–250M
- Samoa's ~$7M supplier arrears and metformin stockout
- That FDA does not inspect a manufacturing facility until NDA stage
- That the PRV program was championed by Mark Wayne Mullin and Michael Bennet (the 2026 reauthorization rode on the Consolidated Appropriations Act; sponsorship of the underlying "Give Kids a Chance" effort is a separate question)

---

## 7. Methodology notes — what worked, what to do differently

**Worked:**
- The VERIFIED/UNVERIFIED discipline. It surfaced dead links in regulators' own menus, a gazette misprint, a bot-walled ontology host, a silently-ignored API parameter, and an incomplete TLS chain. All of these are things you'd otherwise discover during implementation, expensively.
- Telling agents "your final text IS the deliverable, no preamble." Output came back as usable reference documents rather than chat.
- Asking for a URL ledger split into VERIFIED and UNVERIFIED at the end of each report.
- Independently re-verifying the one finding that invalidates the business plan, rather than trusting a single agent.

**Do differently:**
- **Scope agents narrower.** The two that failed (international regulators, drug identity/IP) were the two broadest. They fanned out into many children and got cut off before synthesizing. Every completed agent had a tight, single-domain brief.
- **One country per agent.** Armenia and Botswana came back excellent precisely because they were single-country children. Run Georgia, Ukraine, Albania, Barbados, Seychelles, Samoa as six separate agents, not one "small markets" agent.
- **Have children write their own files.** When a parent is interrupted, its children's work is only recoverable from task notifications. Instruct each agent to `Write` its report to `sources/…` itself.

---

## 8. Where the raw material is

- **Agent reports (JSON-wrapped):** `/Users/carte/.claude/projects/-Users-carte-Downloads-RareDiseaseHedge/fd64561f-7c90-41a2-95cf-b4a133a8fe0f/tool-results/` — extract with `python3 -c "import json;print(''.join(b['text'] for b in json.load(open(F))))"`
- **Full subagent transcripts:** `.../subagents/agent-*.jsonl` — 60 files. **This is where the killed agents' partial work lives** (5b's Google Patents BigQuery findings, 5c/5d's foreign-regulator list work). Worth mining before re-running those.
- **Scratchpad — 349 files, ~730 MB of downloaded primary source:** `/private/tmp/claude-501/-Users-carte-Downloads-RareDiseaseHedge/fd64561f-7c90-41a2-95cf-b4a133a8fe0f/scratchpad/`
  Includes `UNII_Data.zip`, `UNIIs.zip`, `360ff_prelim.html` (the statute), NewSTEPs newborn-screening annual reports 2021/2022/2024, BoMRA site dumps, BRIMS JS bundle and JSON, KEGG BRITE extracts, an fda.gov URL sweep (`allurls.txt`, 6.6 MB), Orphanet XML (`ages.xml`), and more. **This is a temp directory — copy anything you want to keep into the repo.**

---

## 9. Suggested order of work when resuming

1. **Ukraine** — closing regulatory window, explicitly time-critical.
2. **Georgia** — live filing already in flight, zero documentation.
3. **The "approved abroad, never in the US" diff** — now the only PRV-eligible funnel, so it defines the whole candidate universe for leg 1. Mine agent 5c/5d transcripts first; they got most of the way.
4. **Orange Book patent + exclusivity files, and the orphan/RPD conflict check** — needed before any candidate can be cleared.
5. **PMDA** — the richest source of approved-abroad-only molecules, and independently called out in the call.
6. Remaining small markets (Albania, Barbados, Seychelles, Samoa), one agent each.
7. Manufacturing / API supply chain.
8. PRV transaction market + competitor detection via EDGAR.
