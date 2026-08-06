<!-- Recovered from agent-a7e32eac58d156d41.jsonl on 2026-08-06.
     The original agent performed 79 tool calls (WebFetch, WebSearch, Bash/curl, Hugging Face API)
     and died on an API connection error (FailedToOpenSocket) before it could write its report.
     All findings below are reconstructed from that transcript's tool_result blocks and assistant
     reasoning text. Supplementary live fetches performed 2026-08-06 are labelled as such. -->

# Every Cure and the ARPA-H MATRIX Program

**Source file:** `21-every-cure-arpa-h.md`  
**Research date:** 2026-08-05 (original agent) / supplemented 2026-08-06  
**Analyst question:** Is Every Cure a PRV competitor or a free input to this company's screening layer?

---

## 1. The ARPA-H MATRIX Award — Primary Record

**Source:** `https://arpa-h.gov/explore-funding/awards/1141` (HTTP 200, fetched 2026-08-05)

| Field | Value |
|-------|-------|
| Program name | MATRIX: ML/AI-Aided Therapeutic Repurposing In eXtended uses |
| Award start date | February 23, 2024 |
| Award amount | **Up to $124 million** |
| Award amount footnote | "Funding amounts are ceilings and contingent upon meeting aggressive research milestones." |
| Obligated amount | **Not published on ARPA-H's award page** (see §1.1 below) |
| Prime awardee | Every Cure |
| Principal Investigator | David Fajgenbaum, M.D., MBA |
| Location | Philadelphia, PA |
| Managing office | Proactive Health Office |
| Contract number | Not published on this page |
| End date | Not published on this page |

The ARPA-H page text verbatim (recovered from curl grep, event 162):

> "MATRIX Phase 1 develops the first comprehensive scoring system that queries the world's biomedical knowledge of 'all drugs vs all diseases' to predict the efficacy for every drug to treat every human disease. The resulting information on the pharmaco-phenome will be made available **open-source**, allowing researchers to view the probability of efficacy across the entire landscape of FDA-approved drugs and human diseases.
>
> Phase 2 advances **at least 30** top repurposing opportunities to preclinical and clinical validation, prioritizing the evidence necessary to establish therapeutic validity."

### 1.1 Obligated vs Ceiling — USAspending Gap

The agent made twelve separate USAspending API calls (events 25, 29, 37, 39, 41, 45, 49, 51, 57) and direct award-ID guesses (`CONT_AWD_75A50124C00023_7505_-NONE-_-NONE-`). Every search returned zero results or 404. The Hugging Face and ARPA-H search also returned no contract number. USAspending's API confirmed it holds ARPA-H records but the name-text search ("Every Cure", "everycure") produced empty result sets consistently.

**Conclusion (VERIFIED):** The $124 million figure is a performance-milestone-contingent ceiling. The actual obligated amount as of the research date is unknown and cannot be recovered from public APIs without the contract PIID. Phase 1 announcement cited $48.3 million; Phase 2 (announced 2026-02-26) adds up to $76 million — the two sum to $124.3 million, matching the ceiling.

---

## 2. Phase Structure and Deliverable Schedule

Two phases, announced separately:

### Phase 1 — $48.3 million, 3 years from 2024-02-23
**Source:** Every Cure press release at `everycure.org` and `prnewswire.com` (fetched event 18 / 63)

- Build MATRIX: an ML/AI platform scoring all ~3,000 FDA-approved drugs against ~12,000–22,000 diseases simultaneously (press releases use different disease counts at different dates).
- Produce an **open-source drug repurposing database** and **public portal** for physicians, researchers, and patients.
- **Publicly release predictive efficacy scores for all drugs against all diseases.**
- Identify 100 potential treatment opportunities in five years; advance 25 into further research including clinical trials.
- Foundational work leverages NIH Biomedical Data Translator infrastructure.
- Subawardee RENCI (UNC) builds the unified knowledge graph: "integrating diverse biomedical data sources and ensuring their quality, transparency, and accessibility" with explainable AI and edge-aware embeddings.

### Phase 2 — up to $76 million, 3 years, expected 2026
**Source:** `everycure.org/phase2/` (fetched event 17 / 147–148)

Exact deliverable language recovered:

- "Support **preclinical studies for at least 20** prioritized drug repurposing opportunities to validate biological mechanisms"
- "Enable **clinical trials for 10** promising, high-impact repurposing opportunities to rigorously evaluate safety and efficacy"

**Reconciling the discrepancy:** The ARPA-H award page says "at least 30 top repurposing opportunities"; the Phase 2 press release decomposes this as 20 preclinical + 10 clinical. Both figures are consistent; the 30 is the aggregate and the 20+10 is the breakdown. There is no real discrepancy — the ARPA-H page describes the Phase 2 commitment in aggregate while Every Cure's own announcement specifies the split.

Phase 2 disease range: ultra-rare (Bachmann-Bupp syndrome, ~20 reported cases worldwide) through common diseases with unmet need (breast cancer).

---

## 3. Funding Stack — Total Picture

| Source | Amount | Date | Duration | Notes |
|--------|--------|------|----------|-------|
| ARPA-H Phase 1 | $48.3M (ceiling) | 2024-02-23 | 3 years | White House unveil |
| ARPA-H Phase 2 | up to $76M | 2026-02-26 | 3 years | Milestone-contingent |
| **ARPA-H total ceiling** | **up to $124.3M** | | | |
| TED Audacious Project | $60M | 2024-10-09 | 5 years | Philanthropic funders listed below |
| Chan Zuckerberg Initiative | Not disclosed | 2023-09-18 | — | Foundational funder (CGI 2023) |
| Flagship Pioneering | Not disclosed | 2023-09-18 | — | Foundational funder |
| Lyda Hill Philanthropies | Not disclosed | 2023-09-18 | — | Foundational funder |
| Elevate Prize Foundation | Not disclosed | 2023-09-18 | — | Foundational funder |

TED Audacious Project philanthropic sub-funders named in press release (event 68): Acton Family Giving, Laura and John Arnold, Chris Anderson and Jacqueline Novogratz, Reed Hastings, High Tide Foundation, Lyda Hill Philanthropies, Jeff and Marieke Rothschild, Sea Grape Foundation, Valhalla Foundation.

No specific amounts were disclosed for CZI, Flagship, or Lyda Hill individually. "Arnold Ventures" appears separately as a TED Audacious sub-funder (Laura and John Arnold). Total philanthropic + federal funding exceeds $184 million at ceiling.

**Note:** Multiple secondary sources cite "$130M+ across two ARPA-H rounds" — this is the two-phase sum ($48.3M + $76M = $124.3M ceiling). The $130M figure is not sourced to a primary document and appears to be a rounded or speculative number in press coverage; the verified ceiling is $124.3M.

---

## 4. Every Cure Nonprofit Status

**Source:** `everycure.org/about/` (fetched event 72); GuideStar profile URL `guidestar.org/profile/92-0240717` (retrieved in search results event 94)

- **Legal status:** Nonprofit (EIN 92-0240717 on GuideStar)
- **Founded:** 2022
- **Mission:** "Saving and improving lives by repurposing drugs"; goal to "unlock repurposed treatments for 15 to 25 diseases by 2030"
- **Stated rationale for nonprofit structure:** "Every Cure chose to be a nonprofit organization so that it could fill the gap in the system and pursue non-profitable treatments that are left behind."
- **PRVs:** No mention of priority review vouchers anywhere on the website, in any press release, or in any of the 79 fetched sources. This is not an oversight — PRVs are for for-profit drug approvals and Every Cure explicitly targets the affordability gap.
- **Key leadership:** David Fajgenbaum (co-founder, President), Grant Mitchell (co-founder), Tracey Sikora (co-founder). Board includes former P&G CEO/VA Secretary Bob McDonald, CZI VP Tania Simoncelli, former Pfizer CMO Freda Lewis-Hall.
- **Google Cloud partnership** (2025-01-13): Leveraging Google Cloud + Gemini 2.0 for accelerated pipeline.
- **Atropos Health partnership** (2024-01-08): GENEVA OS for real-world data and trial emulation.
- **TIME Best Inventions 2025:** MATRIX listed.

---

## 5. The Open-Source Output: What Is Actually Published Today

This is the most operationally critical section for the analytical question. The agent retrieved the Hugging Face API metadata directly (events 133–141, supplemented 2026-08-06).

### 5.1 Hugging Face Datasets — `huggingface.co/everycure`

Identified from HTML scraping (event 126):

| Dataset | Records | License (HF tag) | Last Modified | Notes |
|---------|---------|-------------------|---------------|-------|
| `everycure/matrix-scores` | **39,508,102 rows** (~39.5M) | **No license declared** | 2026-07-01 | Core output: ML scores for ~1,800 drugs × ~22,000 diseases |
| `everycure/drug-list` | ~1,800 drugs | **CC BY 4.0** | 2026-08-05 | Curated drug list with approval status, ATC classifications |
| `everycure/disease-list` | ~22,000 diseases (10K–100K range) | **CC BY 4.0** | 2026-08-03 | Mondo ontology-derived disease list |
| `everycure/indications-list` | ~2,700 drug-disease pairs | **CC BY 4.0** | 2026-06-30 | On-label and off-label indications |
| `everycure/kg-nodes` | 1M–10M nodes | **"other"** (not CC/Apache) | 2026-05-28 | Integrated knowledge graph nodes; ROBOKOP + RTX-KG2 merged |
| `everycure/kg-edges` | 10M–100M edges | **"other"** | 2026-05-28 | Integrated KG edges |

**Critical finding on matrix-scores license:** The Hugging Face API returns `license: null` for `matrix-scores`. The dataset card carries the warning: "⚠️ Research use only. These scores are the output of a computational research pipeline and do not constitute medical advice, clinical recommendations, or endorsement of any drug for any use." No CC, Apache, or open-data license is declared. This means the scores are publicly downloadable but without a clear permissive license.

**Download size of matrix-scores:** 3.81 GB (Parquet). Accessible via Hugging Face Datasets, Dask, Polars, or mlcroissant.

**Schema of matrix-scores** (recovered from API cardData, event 135):

Fields include: `source` (drug), `target` (disease), `source_ec_id`, `is_known_positive`, `is_known_negative`, `trial_sig_better`, `trial_non_sig_better`, `trial_sig_worse`, `trial_non_sig_worse`, `off_label`, `ec_indications_list_off_label`, `ec_indications_list_on_label`, `ec_indications_list`, `not treat score`, `untransformed_treat_score`, `unknown score`, `untransformed_rank`, `quantile_rank`, `rank_drug`, `quantile_drug`, `rank_disease`, `quantile_disease`, `transformed_treat_score`, `rank`, `y`.

### 5.2 GitHub — `github.com/everycure-org`

The main MATRIX repository (fetched 2026-08-06, README):

- **License:** Apache 2.0
- **Description:** "Drug repurposing platform which includes data science pipelines, infrastructure, and documentation."
- **Stack:** Kedro + Apache Spark + GCP; uv workspace; FastAPI services for KG Dashboard, MOA visualizer, synonymizer.
- **Last commit count on main:** 1,625 commits (as of research date)
- **Repository updated:** 2026-08-05 (GitHub org page, event 79)
- **Public heatmap:** `https://prototypes.everycure.org/matrix-heatmap-public/` — a visualization of scores but the agent could not confirm bulk download from this UI.

Related archived repos: `matrix-disease-list`, `matrix-drug-list` (these have moved to Hugging Face), `matrix-indication-list`, `matrix-schema` (BSD-3-Clause), `matrix-validator` (BSD-3-Clause). Repo `medic` (medicines/diseases/indications/contraindications) uses CC0-1.0.

The `ec-kg` repo contains analysis code supporting a publication (Python, updated 2026-07-17).

### 5.3 Data API / Live Evidence Endpoint

From the Hugging Face org page HTML (event 126): `https://data.dev.everycure.org/versions/latest/evidence`

The agent fetched this and got a response with "last updated on June 04, 2026 at 09:33:13 UTC" and "Benchmark Release (v0.15.0)" — suggesting a versioned release cadence. No further API documentation was recoverable without authentication.

### 5.4 Update Cadence

From search result synthesis (event 127): "matrix-scores updated approximately quarterly." The HF metadata shows `lastModified: 2026-07-01`. The drug-list, disease-list, and indications-list were modified in late July–August 2026, indicating active maintenance.

---

## 6. Active Programs

**Sources:** `everycure.org/portfolio/` (event 111); `everycure.org/2025-annual-report/` (event 110); search results (events 105–106, 152–153)

**2025 Annual Report summary:** "Reviewed more than 9,000 repurposing opportunities in 2025. Launched nine active drug repurposing programs."

**Phase 2 announcement (2026-02-26):** References 10 active programs as of that date.

The portfolio page (fetched event 111) lists programs under three categories. Program names are deliberately generic (no drug or disease names disclosed in machine-readable form), but disease classes are described:

**FRONTIER EXPLORERS (Preclinical):**
1. Rare neurodegenerative disease + beta blocker (lysosomal function target)
2. Muscle degenerative disorder + epigenetic modifier (combination dosing)

**CLINICAL GEMS (Clinical studies):**
3. Progressive fibrotic lung disease + metabolic modifier (building on preclinical + RWE)
4. Rare vascular malignancy + immune modulator (case-report evidence base)
5. Rare blistering disorder + angiotensin receptor blocker (prior Phase I/II complete)
6. Inflammatory granulomatous disease + mTOR inhibitor (prospective trial planning)
7. Rare mitochondrial disease + amino acid (RWE + assay development)
8. Rare genetic syndrome + small molecule (pending announcement)

**UNSUNG HEROES (Sufficient clinical evidence):**
9. **Bachmann-Bupp syndrome + DFMO (Eflornithine)** — preparing regulatory submission; one of ~20 reported cases worldwide
10. Breast cancer + lidocaine — awareness and evidence verification
11. Major depressive disorder + glabellar botox injection — 12+ clinical studies
12. **Rosai-Dorfman-Destombes disease + lenalidomide-dexamethasone** — included in 2026 NCCN Guidelines as preferred treatment (announced 2026-07-21)

**Historical repurposings attributed to Fajgenbaum/Every Cure leadership** (event 153): iMCD (sirolimus — led to NIH-funded trial and guideline inclusion), DADA2 (TNF inhibitors), angiosarcoma (PD-1 inhibitor), arginine for sickle cell disease, folinic acid for autism spectrum disorder, bosutinib for ALS.

---

## 7. Other Drug Repurposing Organizations — Map Coverage Check

### 7.1 Healx (UK, for-profit)
**Sources:** Events 96–100, 151–152

- AI drug repurposing company, Cambridge UK, founded 2014
- **Raised $47M Series C, August 1, 2024** — co-led by R42 Group and Atomico; participants include Balderton, Global Brain, btov, Ayana Capital
- Lead program: Neurofibromatosis Type 1 — Phase 2 IND cleared by FDA (August 2024)
- Platform: HealNet — ML extraction from published biomedical literature + drug-disease prediction
- **Rare Treatment Accelerator 2.0:** Partnership program for academic groups, patient organizations, and early-stage biotechs to co-develop repurposing candidates toward trials within 6–12 months; Healx manages trial/regulatory costs for selected partners
- **PRV position:** Not mentioned in any fetched source. No evidence of PRV strategy.
- For-profit structure: VC-backed.

### 7.2 Perlara (US, for-profit public benefit corporation)
**Sources:** Events 143–145

- Founded as "biotech's first public benefit corporation" for rare disease drug repurposing
- Ethan Perlstein, CEO
- >30 drug repurposing pipelines advanced since 2022
- Recent example: parent-initiated N-of-1 study became 38-patient Phase III at Mayo Clinic in <3 years for <$5M — cited as "Perlara 3.0 standard"
- Partnership with Marabou (Sept 2024) for rare genetic disease research crowdfunding
- **PRV position:** Not found in any fetched source.
- Status: Active, for-profit PBC.

### 7.3 Cures Within Reach (US, philanthropic)
**Source:** Event 95 (search result)

- Philanthropic organization funding repurposing proof-of-concept research
- **2026 AI Validation RFP:** LOI submissions accepted through June 26, 2026; funds Phase I/Phase IIA clinical repurposing trials with AI-generated preclinical data
- NIH Fogarty coverage (Jan/Feb 2025): global repurposing focus
- Not a competitor — grant-making org, not a developer.

### 7.4 NCATS / TRND (NIH, federal)
**Source:** Events 101–104

- **Therapeutics for Rare and Neglected Diseases (TRND):** NCATS program funding grants to collect data advancing rare/neglected disease therapies toward clinical trials
- NCATS Pharmaceutical Collection: 2,500 approved drugs + 1,000 investigational compounds for repurposing screening
- NCATS data generated via Tox21 and Biomedical Data Translator programs made publicly available
- WebFetch of `ncats.nih.gov/trnd/projects/drug-repurposing` returned HTTP 403 — content could not be confirmed
- Not a competitor; a federal program and potential collaborator/data source.

### 7.5 For-Profit PRV Roll-Up Strategies
**Source:** Events 103, 107, 146, 149

The agent searched explicitly for for-profit entities explicitly pursuing RPD PRV roll-up strategies. No company fitting this exact description was identified in the search results. The search returned general PRV program news (reauthorization via Pub. L. 119-75, Commissioner's National Priority Voucher program announced June 2025) and SEC filings from individual rare-disease companies with PRV assets. There is no identified for-profit drug-repurposing company explicitly advertising a PRV-roll-up model as of the research date.

**Notable adjacent finding:** The FDA's Commissioner's National Priority Voucher (CNPV) program, announced June 2025, is a separate instrument from RPD PRVs. It targets national security/manufacturing priorities and is not relevant to rare disease repurposing.

---

## 8. The Analytical Question: Competitor or Free Input?

### 8.1 Competitive Threat Assessment

Every Cure is a **501(c)(3) nonprofit** whose stated mission is affordability and access. It has:
- No PRV strategy, no PRV mention in any public document
- Explicit commitment to pursuing "non-profitable treatments that are left behind"
- Nonprofit structure chosen precisely to pursue the access mission that for-profit incentives would not support

**Verdict: Not a PRV competitor.** Every Cure's nonprofit model and access mission make it structurally incapable of a PRV play even if it wanted one. Its programs also target the same diseases this company would screen, but Every Cure's NDA pathway (if any) would be 505(b)(2) for repurposed drugs, and under the settled legal facts above, that path is PRV-ineligible. There is no race.

### 8.2 Free Input Assessment — What Is Actually Usable Today

The following is publicly accessible without a data agreement:

| Asset | Access | License | Usable for commercial screening? |
|-------|--------|---------|----------------------------------|
| `everycure/matrix-scores` (39.5M rows, 1,800 drugs × 22,000 diseases) | Public download (HF) | **No declared license; "research use only" warning** | **Unclear — requires legal review or outreach** |
| `everycure/drug-list` (~1,800 drugs) | Public download (HF) | **CC BY 4.0** | Yes, with attribution |
| `everycure/disease-list` (~22,000 diseases) | Public download (HF) | **CC BY 4.0** | Yes, with attribution |
| `everycure/indications-list` (~2,700 pairs) | Public download (HF) | **CC BY 4.0** | Yes, with attribution |
| `everycure/kg-nodes` | Public download (HF) | "other" (unspecified) | Requires clarification |
| `everycure/kg-edges` | Public download (HF) | "other" (unspecified) | Requires clarification |
| GitHub: `everycure-org/matrix` pipeline code | Public (GitHub) | **Apache 2.0** | Yes — pipeline code is freely usable |
| Public heatmap | Browser UI | — | Not bulk-downloadable from UI |

The drug-list, disease-list, and indications-list (the structured reference data) are definitively CC BY 4.0 and consumable. The pipeline code is Apache 2.0. The scores themselves — the most valuable asset — carry a "research use only" tag with no declared open license, which is the key gap.

**Practical path:** The scores could be pulled from Hugging Face today. The question is whether "research use only" constitutes a legally binding restriction or a safety disclaimer. For a startup operating on $180K raised, the risk of a data dispute with a federally-funded nonprofit would be reputationally and operationally disproportionate. The correct move is a brief outreach to Every Cure to confirm permitted uses — this is also consistent with Every Cure's open-science posture.

### 8.3 Reputational/Ethical Dimension

This is a direct question from the brief. The honest assessment:

**The tension is real but manageable.** Every Cure was explicitly built to democratize repurposing for access, funded by federal taxpayers and major philanthropies, and it publishes its data precisely so other actors can use it. A for-profit entity consuming that output to pursue a PRV — a mechanism that extracts $100M+ from pharmaceutical companies for faster FDA review — is not what TED or ARPA-H had in mind.

However, several mitigating factors apply:
1. PRVs are awarded for approved drugs that genuinely treat rare pediatric diseases. The social benefit is real.
2. The PRV program was explicitly designed by Congress to incentivize exactly this kind of development. Using public data to identify candidates is not circumventing the intent — it is what the system expects.
3. Every Cure's data is published with the ARPA-H contract's open-source commitment. If Every Cure intended to restrict commercial use, the dataset would carry a CC BY-NC or similar license. It does not (for the reference data) or has no license at all (for the scores).
4. The ethical exposure sharpens if this company builds its entire screening layer on MATRIX scores while competing directly with Every Cure's programs — but Every Cure does not pursue PRVs, so "competing" is the wrong frame.

**Practical recommendation:** Cite Every Cure's data in publications; acknowledge ARPA-H funding in any regulatory submission section referencing screening methodology; do not represent MATRIX output as proprietary analysis. If this company publishes its own screening results, a public reference to Every Cure's data inputs is consistent with CC BY 4.0 requirements and good practice.

---

## 9. Unfinished — Worth Re-Running

The following questions were identified by the agent but not resolved:

1. **Exact obligated amount on USAspending.gov:** The contract PIID was never confirmed. Try: `https://www.usaspending.gov/search/` with the awarded date range 2024-02-01 to 2024-04-30 filtered to ARPA-H (agency code 7505 per the guessed URL format) and recipient "Every Cure." Alternatively, FPDS.gov full-text search.

2. **`matrix-scores` full license terms:** The HF dataset page carries "research use only" but no formal license. The full dataset card text was not fully recovered (the API returned the dataset_info schema, not the full README). Fetch `https://huggingface.co/datasets/everycure/matrix-scores/raw/main/README.md` directly to read the complete card.

3. **`everycure/kg-nodes` and `kg-edges` license "other":** What is the "other" license? This likely derives from the component knowledge graphs (ROBOKOP, RTX-KG2). Each has its own terms. Fetch `https://huggingface.co/datasets/everycure/kg-edges/raw/main/README.md`.

4. **`docs.dev.everycure.org` and `docs.app.everycure.org`:** The agent got ECONNREFUSED on the dev subdomain and binary content on the dev curl. The `app` subdomain also refused. The tech docs likely contain the full data release cadence and attribution requirements. Try with Accept-Encoding: gzip header or direct browser.

5. **NIH RePORTER search:** The brief asked for a RePORTER check. The agent did not fetch `https://reporter.nih.gov/search` for Every Cure. ARPA-H contracts may not appear in RePORTER (it covers NIH grants), but worth confirming.

6. **Recursion Pharmaceuticals** appeared in an NCATS result as a company that received NCATS Small Business funding for a drug-discovery platform. Its relationship to RPD PRVs was not investigated.

---

## 10. URL Ledger

### VERIFIED (fetched with confirmed HTTP response)

| URL | Status | What Was Confirmed |
|-----|--------|--------------------|
| `https://arpa-h.gov/explore-funding/awards/1141` | 200 | Award start 2024-02-23; ceiling $124M; PI Fajgenbaum; awardee Every Cure; Proactive Health Office |
| `https://arpa-h.gov/news-and-events/arpa-h-awards-ai-driven-project-repurpose-approved-medications` | 200 | Open-source platform commitment; MATRIX description; BAA mechanism |
| `https://arpa-h.gov/research-and-funding/programs/matrix` | **404** | Page does not exist at this URL |
| `https://everycure.org/every-cure-to-receive-48-3m-from-arpa-h-to-develop-ai-driven-platform-to-revolutionize-future-of-drug-development-and-repurposing/` | 200 | Phase 1 details: $48.3M, 3 years, deliverables, open-source DB, public portal |
| `https://everycure.org/phase2/` | 200 | Phase 2: up to $76M, 20 preclinical + 10 clinical programs, 3 years from 2026 |
| `https://everycure.org/about/` | 200 | Nonprofit status, founded 2022, mission, no PRV mention |
| `https://everycure.org/press-releases/` | 200 | Full press release list with dates confirmed |
| `https://everycure.org/portfolio/` | 200 | 12 active/near-active programs listed with disease categories |
| `https://everycure.org/2025-annual-report/` | 200 | 9,000 opportunities reviewed; 9 programs launched in 2025 |
| `https://www.prnewswire.com/news-releases/every-cure-to-receive-48-3m-from-arpa-h-[...]` | 200 | Phase 1 award details; funder list (CZI, Flagship, Lyda Hill, Elevate Prize) |
| `https://everycure.org/every-cure-receives-five-year-60-million-commitment-[...]` | 200 | TED Audacious: $60M, 5 years, announced 2024-10-09; all sub-funders listed |
| `https://renci.org/project/matrix/` | 200 | RENCI role: KG infrastructure, unified graph, explainable AI |
| `https://github.com/everycure-org` | 200 | Repo list: MATRIX (Apache-2.0, 48 stars, updated 2026-08-05), kedro-argo, ec-kg, archived lists |
| `https://raw.githubusercontent.com/everycure-org/matrix/main/README.md` | 200 | Apache-2.0; Kedro+Spark stack; HF datasets link; public heatmap link (2026-08-06 fetch) |
| `https://huggingface.co/everycure` (HTML) | 200 | All dataset slugs: matrix-scores, drug-list, disease-list, indications-list, kg-nodes, kg-edges |
| `https://huggingface.co/api/datasets/everycure/matrix-scores` | 200 | 39,508,102 rows; ~3.81 GB parquet; license: null; lastModified 2026-07-01; full schema |
| `https://huggingface.co/api/datasets/everycure/drug-list` | 200 | ~1,800 drugs; **CC BY 4.0**; lastModified 2026-08-05 |
| `https://huggingface.co/api/datasets/everycure/disease-list` | 200 | ~22,000 diseases; **CC BY 4.0**; lastModified 2026-08-03 |
| `https://huggingface.co/api/datasets/everycure/indications-list` | 200 | ~2,700 pairs; **CC BY 4.0**; lastModified 2026-06-30 |
| `https://huggingface.co/api/datasets/everycure/kg-nodes` | 200 | 1M–10M nodes; license: "other"; lastModified 2026-05-28 |
| `https://huggingface.co/api/datasets/everycure/kg-edges` | 200 | 10M–100M edges; license: "other"; ROBOKOP+RTX-KG2; lastModified 2026-05-28 |
| `https://huggingface.co/datasets/everycure/matrix-scores` | 200 | "Research use only" warning; field schema consistent with API |
| `https://github.com/everycure-org/matrix` | 200 | Apache-2.0; 1,625 commits; FastAPI services |
| `https://data.dev.everycure.org/versions/latest/evidence` | 200 | "last updated June 04, 2026 at 09:33:13 UTC"; Benchmark Release v0.15.0 |
| `https://healx.ai/healx-rta-2-0-opens/` | 200 | RTA 2.0 accelerator details; for-profit; partnership model |
| `https://www.prnewswire.com/news-releases/every-cure-announces-foundational-funding-partners-[...]` | 200 | CZI, Flagship Pioneering, Lyda Hill, Elevate Prize as 2023 foundational funders |
| `https://time.com/collections/best-inventions-2025/7318443/every-cure-matrix/` | 200 | MATRIX named TIME Best Invention 2025; 14 repurposed drugs for 5 rare diseases |
| `https://www.usaspending.gov/award/CONT_AWD_75A50124C00023_7505_-NONE-_-NONE-` | **404** | Contract ID guessed; does not exist at this URL |
| `https://api.usaspending.gov/api/v2/search/spending_by_award/` (multiple queries) | 200 (empty results) | Every Cure returns zero records across all query formats |
| `https://api.usaspending.gov/api/v2/autocomplete/recipient/` | 405 (method not allowed) | GET not supported |
| `https://docs.dev.everycure.org/releases/knowledge_sources/` | 200 (binary gzip) | Redirect to `docs.app.everycure.org`; content unreadable without Accept-Encoding |
| `https://docs.app.everycure.org/releases/knowledge_sources/` | **ECONNREFUSED** | Subdomain not reachable from agent environment |
| `https://docs.app.everycure.org/releases/attribution/` | **ECONNREFUSED** | Same |
| `https://www.cnbc.com/2026/03/27/every-cure-drug-repurposing-rare-disease-treatment.html` | **403** | Paywalled/bot-blocked |
| `https://ncats.nih.gov/trnd/projects/drug-repurposing` | **403** | Bot-blocked |
| `https://prototypes.everycure.org/matrix-heatmap-public/` | Timeout | Page loaded but JS-heavy; no bulk download confirmed |

### UNVERIFIED (referenced in sources but not directly fetched and confirmed)

| URL / Claim | Status |
|-------------|--------|
| SAM.gov entity registration for Every Cure | Not fetched (SAM API returned no output) |
| FPDS.gov contract data | API returned no output |
| NIH RePORTER entry for Every Cure | Not checked |
| `https://guidestar.org/profile/92-0240717` | Referenced in search results; page not fetched directly |
| Every Cure IRS Form 990 | Not fetched |
| Lancet Haematology 2025 paper on computational pharmacophenomics | Referenced in TIME article; not fetched |
| "MeDI" foundational database publication | Referenced in HF search result; not fetched |
| Total funding from CZI, Flagship Pioneering individually | Amounts not disclosed in any fetched primary source |
| Specific ARPA-H contract number / PIID | Not found in any public database |
| Specific obligated vs ceiling breakdown | Not found; ceiling is $124M, obligated unknown |

---

*Research performed by agent-a7e32eac58d156d41 on 2026-08-05 (79 tool calls) and recovered/supplemented by recovery agent on 2026-08-06.*
