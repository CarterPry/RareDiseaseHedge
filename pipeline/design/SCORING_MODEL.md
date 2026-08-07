# PROMISE-SCORE MODEL — RareDiseaseHedge Candidate Ranking

**Author:** Buy-side biotech analyst perspective  
**Date:** 2026-08-07  
**Data contract version:** summary.json as of 2026-08-07  
**Legal basis:** 21 U.S.C. § 360ff; PRV program sunset 2029-09-30 (Pub. L. 119-75 § 6604(a))

---

## 0. Honesty Preamble (Non-Negotiable)

The pipeline outputs 105 named-drug candidates. That is a screening shortlist — names that passed the anti-join against the full US approval record. **Approximately 7 of those 105 are truly actionable** after applying the downstream filters documented in sources 25–27. This model ranks 105 candidates as risk-adjusted assets; it does NOT manufacture more investable programs than reality supports. An A-tier score means "worth a real diligence week." It does not mean "viable business." The score is a triage tool, not a valuation.

---

## 1. Economic Ground Truth (From Primary Sources)

Before constructing any formula, the real numbers must be fixed:

| Parameter | Value | Source |
|---|---|---|
| PRV secondary market value (2026 verified) | $180–205M gross | sources/18-prv-transaction-market.md (Rocket $180M, Denali $195M, Cyprium $205M — all SEC-verified) |
| PRV planning range (conservative / base / upside) | $150M / $190M / $225M | sources/18-prv-transaction-market.md §5.5 |
| Per-program P(approval by 2029-09-30), generic program | 3–5% | sources/26-feasibility-timeline.md §8 reconciled |
| Per-program P(approval by 2029-09-30), optimized program | 20–22% | sources/26-feasibility-timeline.md §8 reconciled |
| Globally actionable A1+A2 programs (mid-case) | ~7 (range 2–15) | sources/25-feasibility-pool-size.md §10 |
| Trial cost floor (single-site, academic, lean) | $400–620k | sources/27-feasibility-recruitment.md §3.2 |
| Time to sunset from Aug 2026 | ~37 months | sources/26-feasibility-timeline.md §3 |
| Latest viable first-patient-in date (optimistic) | 2027-02-28 | sources/26-feasibility-timeline.md Table §3 |
| CRL is effectively fatal to the PRV window | Yes | sources/26-feasibility-timeline.md §4.B |

**Risk-adjusted expected value per candidate (base case):**

```
EV_candidate = P(success) × PRV_value − cost

Generic program:    EV = 0.04 × $190M − $0.5M ≈ $7.1M  (pre-probability of selection)
Optimized program:  EV = 0.21 × $190M − $0.5M ≈ $39.4M
```

These are per-program figures before capital constraints. They are the ceiling on what a candidate can be worth as a PRV play.

---

## 2. The Scoring Formula

### 2.1 Formula Statement (One Line)

```
PROMISE = 35·PED + 25·ORPHAN + 15·REGCOUNT + 15·MATCHCONF + 5·ATC + 5·RECENCY
```

All sub-scores are normalized 0–1 before applying weights, yielding a 0–100 final score. Each component and weight is derived from the research and tied to a specific risk driver.

---

### 2.2 Component Definitions and Rationale

#### Component 1: PED — Pediatric-Rare Disease Signal (weight 35)

**What it measures:** Likelihood the candidate's indication qualifies under 21 U.S.C. § 360ff(a)(3) — primarily affects individuals under 18, serious or life-threatening, US prevalence under 200,000.

**Why weight 35:** This is the single biggest real filter in the entire funnel. Source 25 (§2d) documents that even after a compound passes the rare-disease filter, only 25–35% qualify under the pediatric restriction. Source 26 confirms this is the binding gate for PRV eligibility. No other factor eliminates candidates faster or more absolutely. A drug for a common adult disease scores zero here regardless of how good everything else looks.

**How to compute (keyword heuristic from indication text + therapeutic_area field):**

The field `indication` and `therapeutic_area` (to be added from EMA enrichment) are scanned. Score is 0, 0.5, or 1.0:

**Score 1.0 — Strong pediatric-rare signal (any of the following):**

Primary pediatric rare disease keywords (indication text contains):
```python
PEDIATRIC_RARE_STRONG = [
    # Disease groups with known pediatric onset
    "pediatric", "paediatric", "children", "child", "infant", "neonatal",
    "congenital", "inherited", "inborn", "lysosomal", "mucopolysaccharid",
    "gaucher", "fabry", "pompe", "niemann-pick", "krabbe", "batten",
    "neuronal ceroid", "spinal muscular atrophy", "sma", "duchenne",
    "friedreich", "hunter syndrome", "hurler", "sanfilippo",
    "glycogen storage", "fatty acid oxidation", "organic acidemia",
    "maple syrup urine", "phenylketonuria", "pku", "urea cycle",
    "galactosemia", "biotinidase", "homocystinuria", "tyrosinemia",
    "propionic acidemia", "methylmalonic", "isovaleric",
    "adrenoleukodystrophy", "adrenomyeloneuropathy", "ald",
    "metachromatic leukodystrophy", "mld", "globoid",
    "lesch-nyhan", "wilson disease", "menkes",
    "epidermolysis bullosa", "progeria", "hutchinson",
    "angelman", "rett syndrome", "cdkl5", "dravet",
    "tuberous sclerosis", "neurofibromatosis",
    "cystinosis", "nephropathic cystinosis",
    "transthyretin", "ttr amyloidosis",   # often pediatric forms
    "methylation disorder", "cobalamin", "cblc",
    "bile acid synthesis", "peroxisomal",
]
```

**Score 0.5 — Partial pediatric-rare signal (any of the following, absent strong signals):**

```python
PEDIATRIC_RARE_MODERATE = [
    # Rare disease, may be adult or pediatric
    "orphan", "rare disease", "rare disorder",
    "autoinflammatory", "familial", "hereditary", "genetic",
    "muscular dystrophy", "myopathy", "mitochondrial",
    "metabolic disorder", "enzyme deficiency", "enzyme replacement",
    "ataxia", "neuropathy", "leukodystrophy",
    "retinal dystrophy", "leber", "stargardt",
    "haemophilia", "hemophilia", "thrombotic thrombocytopenic",
    "paroxysmal nocturnal hemoglobinuria", "pnh",
    "primary biliary", "alagille", "cholestasis",
    "systemic mastocytosis", "myelofibrosis",  # rare, may adult
    "amyloidosis",
    "epidermolysis", "ichthyosis",
    "pulmonary hypertension", "pah",  # rare, pediatric forms exist
    "cystic fibrosis",  # often overlap with adult programs
    "sickle cell",  # pediatric trials exist
]
```

**Score 0 — Adult-predominant or common disease (disqualifiers take priority):**

```python
ADULT_COMMON_DISQUALIFIERS = [
    "prostatic", "prostate", "alzheimer", "parkinson", "dementia",
    "type 2 diabetes", "hypertension", "coronary artery",
    "atrial fibrillation", "chronic obstructive pulmonary",
    "obesity", "overweight", "erectile dysfunction",
    "osteoporosis", "rheumatoid arthritis",  # common adult
    "major depressive", "schizophrenia", "bipolar",
    "breast cancer",  # unless pediatric subtype specified
    "prostate cancer", "lung cancer", "colorectal cancer",
    "hepatitis b", "hepatitis c",  # common viral diseases
    "hiv", "antiretroviral",
    "insomnia", "anxiety disorder", "dementia",
    "benign prostatic", "hair loss", "alopecia",
]
```

**Scoring logic:**
```python
def ped_score(indication: str, therapeutic_area: str) -> float:
    text = (indication + " " + therapeutic_area).lower()
    if any(k in text for k in ADULT_COMMON_DISQUALIFIERS):
        return 0.0
    if any(k in text for k in PEDIATRIC_RARE_STRONG):
        return 1.0
    if any(k in text for k in PEDIATRIC_RARE_MODERATE):
        return 0.5
    # No signal — unknown, but not explicitly adult
    return 0.2  # small non-zero for optionality
```

**PED sub-score:** `PED_sub = ped_score(indication, therapeutic_area)`  
**Weighted contribution:** `35 × PED_sub`

**IC challenge response:** An IC would ask "why 35 and not 50?" The answer: because even a zero-pediatric signal candidate can score on other dimensions, and those other dimensions represent real optionality (the orphan flag, multi-regulator, and match confidence all reduce downstream development risk even if the pediatric gate is uncertain). Collapsing everything into PED would make the score a binary gate, not a continuous ranker. The 35 weight is high enough that no candidate with a zero PED score can reach Tier A, which is the correct behavior.

---

#### Component 2: ORPHAN — Foreign Orphan Designation (weight 25)

**What it measures:** Whether the candidate carries an orphan designation from at least one foreign regulator (captured in the `orphan` boolean from summary.json).

**Why weight 25:** Source 25 (§2c, §10) establishes that the Japan-orphan-not-US sub-population has a 100% rare-disease hit rate by construction. An orphan designation is not proof of pediatric qualification, but it is proof of rare-disease status under a foreign regulator's criteria. Source 25 (§2e) notes that 15 of 105 named candidates already carry a foreign orphan flag. For those 15, the rare-disease filter (the step that eliminates ~92–97% of non-orphan candidates) has already been passed. The residual filter is pediatric qualification, for which PED provides signal. The 25 weight is high because this binary field provides the sharpest prior probability update: orphan candidates are ~12x more likely to survive the rare-disease step than non-orphan candidates (100% vs. 3–8% hit rate per source 25).

**How to compute:**
```python
ORPHAN_sub = 1.0 if orphan == True else 0.0
```

**Weighted contribution:** `25 × ORPHAN_sub`

**IC challenge response:** "Why not a hard gate?" Because some non-orphan candidates may have published rare pediatric evidence not captured by a foreign designation (e.g., a Japan-domestic compound for a metabolic disease that was approved pre-orphan-designation-system). The 25 weight rewards orphan status without eliminating non-orphan candidates entirely.

---

#### Component 3: REGCOUNT — Number of Foreign Regulatory Approvals (weight 15)

**What it measures:** How many distinct foreign regulators have approved this compound (count of entries in the `sources` list).

**Why weight 15:** Source 25 (§2c) and source 26 (§3, manufacturing section) establish two distinct risk-reduction mechanisms from multi-regulator status. First, each foreign approval comes with a dossier (CMC, nonclinical, clinical summary) — a compound approved in EMA + Health Canada + Swissmedic has a richer evidence base than one approved only by Health Canada. Second, source 26 (§4.C) shows that FDA MRA agreements with EU, Canada, Swissmedic, Australia, UK, Japan, Israel mean a compound already inspected by an MRA-partner regulator faces a lower PAI risk — and PAI failure is a lethal event for the PRV timeline. Multi-regulator status is therefore a direct proxy for dossier richness and manufacturing GMP credibility.

**Current data limitation:** As of the current summary.json, `counts.multi_regulator = 0` because the pipeline only fully joins EMA and Health Canada with high confidence. The `sources` list does carry the regulator names, but many candidates show only 1 source. As enrichment expands, this dimension becomes more discriminating.

**How to compute:**
```python
n = len(sources)
if n >= 3:
    REGCOUNT_sub = 1.0
elif n == 2:
    REGCOUNT_sub = 0.6
elif n == 1:
    REGCOUNT_sub = 0.2
else:
    REGCOUNT_sub = 0.0
```

**Weighted contribution:** `15 × REGCOUNT_sub`

**IC challenge response:** "Why 15 and not 20?" Because regulator count is highly correlated with the source regulator coverage of this pipeline (which is primarily EMA and Health Canada). Most candidates have n=1 through pipeline artifact rather than true single-country approval. Until broader regulator coverage is integrated, this dimension has lower discriminating power. Weight 15 is proportional to its current practical utility.

---

#### Component 4: MATCHCONF — Match Confidence Tier (weight 15)

**What it measures:** The confidence with which the foreign drug was matched to an FDA UNII-resolved active moiety through the anti-join. Higher confidence means lower risk that the compound is actually already in the US under a different name, or that the anti-join result is a false positive.

**Why weight 15:** Source 25 (§8, data quality notes) confirms the EMA-to-UNII join rate is 94.6% with the residual 5.1% concentrated in complex biologics. The `tier` field in summary.json encodes match quality. A candidate at "exact-moiety" tier carries essentially zero risk of being a false-positive anti-join result. A candidate at "moiety-base" tier (salt or prodrug resolved to base moiety) has a slightly higher false-positive risk because some prodrug/salt forms may have different active moiety interpretations. A false-positive means the compound is not actually PRV-eligible — it is wasted diligence.

**How to compute (from `tier` field):**
```python
TIER_MAP = {
    "exact-moiety": 1.0,    # UNII match at exact moiety level
    "moiety-base":  0.7,    # matched via salt stripping; slightly higher false-positive risk
    "name-match":   0.4,    # matched by INN name rather than UNII; needs manual verification
    "fuzzy":        0.1,    # low-confidence name match; high manual verification burden
}
MATCHCONF_sub = TIER_MAP.get(tier, 0.3)
```

**Weighted contribution:** `15 × MATCHCONF_sub`

**IC challenge response:** "Why not make low-confidence tiers score zero?" Because a fuzzy-matched candidate with a strong orphan + pediatric signal still deserves to surface for manual review — the score ranks for triage, not for elimination. A low MATCHCONF with high PED + ORPHAN will score in Tier B and trigger verification, which is the correct behavior.

---

#### Component 5: ATC — ATC Drug Class PRV Proximity (weight 5)

**What it measures:** Whether the ATC class of the compound (to be added via EMA enrichment) is historically associated with rare pediatric disease programs that have earned PRVs. Candidates in enzyme replacement, gene therapy support, or rare metabolic drug classes have a more established regulatory path.

**Why weight 5:** ATC class is a useful but noisy signal. Source 26 establishes that the fundamental drivers of success are disease selection and manufacturing, not drug class per se. A small-molecule in the right orphan rare metabolic indication beats a biologic in a vague autoimmune indication. Weight 5 captures the signal without letting it dominate.

**How to compute (from `atc_code` field, first two characters = ATC Level 2):**

```python
# ATC codes associated with PRV-winning programs in the 2014–2026 transaction history
# Derived from: cerliponase alfa (N07), miglustat (A16), vestronidase (A16), copper histidinate (V03),
# voretigene (S01), lonafarnib (L01), setmelanotide (A08), patisiran intravitreal (S01)
HIGH_ATC = {
    "A16",  # Other alimentary tract and metabolism — enzyme replacement, metabolic rare disease
    "A11",  # Vitamins — cofactor replacement (thiamine, pyridoxine for IEM)
    "A12",  # Mineral supplements — copper (Menkes), zinc (Wilson)
    "N07",  # Other nervous system drugs — neuronal ceroid lipofuscinosis, rare neurological
    "V03",  # All other therapeutic products — orphan enzyme therapies
    "S01",  # Ophthalmologicals — retinal dystrophies (voretigene precedent)
    "L04",  # Immunosuppressants — rare autoinflammatory
    "B06",  # Other hematological agents — rare coagulation disorders
}
MEDIUM_ATC = {
    "N06",  # Psychoanaleptics — pediatric neurological forms
    "A14",  # Anabolic agents — rare muscle disorders
    "M09",  # Other drugs for musculoskeletal — rare muscle/bone diseases
    "D11",  # Other dermatologicals — epidermolysis bullosa, ichthyosis
    "L01",  # Antineoplastics — pediatric oncology (Dravet, CDKL5 precedents)
    "G04",  # Urologicals — rare urological pediatric
    "H04",  # Pancreatic hormones — rare metabolic
}
# Everything else: LOW_ATC (no special signal)

def atc_score(atc_code: str) -> float:
    if not atc_code:
        return 0.3  # unknown: small non-zero credit, enrichment needed
    prefix = atc_code[:3].upper()
    if prefix in HIGH_ATC:
        return 1.0
    prefix2 = atc_code[:2].upper()
    if prefix2 in {a[:2] for a in MEDIUM_ATC}:
        return 0.5
    return 0.1  # common disease class
```

**Weighted contribution:** `5 × ATC_sub`

**IC challenge response:** "Why only 5 when ATC is actually informative?" Because the ATC enrichment field does not yet exist in summary.json — it is to be added. Until the enrichment pipeline is validated, giving this dimension 5 weight (vs. zero if it were excluded) preserves the structure for when the data arrives, while not letting an unvalidated field distort rankings. When EMA enrichment is fully integrated, consider raising to 8–10 and reducing MATCHCONF to 12.

---

#### Component 6: RECENCY — Abroad-Approval Date (weight 5)

**What it measures:** How recently the foreign approval was granted. More recent approvals signal: (a) the compound is still commercially active in its home market (less likely to be withdrawn for safety), (b) more modern clinical data exists, and (c) the drug likely has a more established manufacturing infrastructure than 1980s approvals.

**Why weight 5:** Source 25 (§2e) establishes that API sourcing is a 40–80% block depending on the compound's vintage. Older compounds (pre-1990) are more likely to have a Japan-exclusive manufacturer with no exported supply chain. More recent approvals (post-2015) are more likely to have GMP manufacturing accessible outside the home country, and in an MRA-partner country. Source 26 (§4.C) confirms the MRA-country manufacturer is the single biggest lever on PAI pass probability (52% → 88%).

**How to compute (from `abroad_date` field, ISO date string, to be added via EMA enrichment):**

```python
from datetime import date

def recency_score(abroad_date_str: str) -> float:
    if not abroad_date_str:
        return 0.3  # unknown: moderate credit
    try:
        d = date.fromisoformat(abroad_date_str[:10])
        year = d.year
        if year >= 2015:
            return 1.0   # modern: CMC data likely current
        elif year >= 2005:
            return 0.7   # recent: reasonable CMC currency
        elif year >= 1995:
            return 0.4   # aging: supply chain scrutiny needed
        else:
            return 0.1   # old: high API sourcing risk
    except (ValueError, TypeError):
        return 0.3
```

**Weighted contribution:** `5 × RECENCY_sub`

---

### 2.3 Complete Python Implementation (Engineer-Ready)

```python
from typing import Optional

# --- keyword lists (see Component 1 above for full lists) ---

def ped_score(indication: Optional[str], therapeutic_area: Optional[str]) -> float:
    """Returns 0.0–1.0 pediatric-rare signal score."""
    text = ((indication or "") + " " + (therapeutic_area or "")).lower()
    if any(k in text for k in ADULT_COMMON_DISQUALIFIERS):
        return 0.0
    if any(k in text for k in PEDIATRIC_RARE_STRONG):
        return 1.0
    if any(k in text for k in PEDIATRIC_RARE_MODERATE):
        return 0.5
    return 0.2  # no text signal, but not disqualified

def orphan_score(orphan: bool) -> float:
    return 1.0 if orphan else 0.0

def regcount_score(sources: list) -> float:
    n = len(sources)
    if n >= 3: return 1.0
    if n == 2: return 0.6
    if n == 1: return 0.2
    return 0.0

TIER_MAP = {"exact-moiety": 1.0, "moiety-base": 0.7, "name-match": 0.4, "fuzzy": 0.1}
def matchconf_score(tier: Optional[str]) -> float:
    return TIER_MAP.get(tier or "", 0.3)

def atc_score(atc_code: Optional[str]) -> float:
    HIGH_ATC  = {"A16","A11","A12","N07","V03","S01","L04","B06"}
    MEDIUM_ATC= {"N06","A14","M09","D11","L01","G04","H04"}
    if not atc_code: return 0.3
    if atc_code[:3].upper() in HIGH_ATC: return 1.0
    if atc_code[:3].upper() in MEDIUM_ATC: return 0.5
    return 0.1

def recency_score(abroad_date_str: Optional[str]) -> float:
    from datetime import date
    if not abroad_date_str: return 0.3
    try:
        year = date.fromisoformat(abroad_date_str[:10]).year
        if year >= 2015: return 1.0
        elif year >= 2005: return 0.7
        elif year >= 1995: return 0.4
        else: return 0.1
    except (ValueError, TypeError):
        return 0.3

def promise_score(candidate: dict) -> float:
    """
    PROMISE = 35·PED + 25·ORPHAN + 15·REGCOUNT + 15·MATCHCONF + 5·ATC + 5·RECENCY
    Returns float in [0, 100].
    """
    ped   = ped_score(candidate.get("indication"), candidate.get("therapeutic_area"))
    orph  = orphan_score(candidate.get("orphan", False))
    reg   = regcount_score(candidate.get("sources", []))
    match = matchconf_score(candidate.get("tier"))
    atc   = atc_score(candidate.get("atc_code"))
    rec   = recency_score(candidate.get("abroad_date"))
    return round(
        35 * ped + 25 * orph + 15 * reg + 15 * match + 5 * atc + 5 * rec,
        1
    )
```

---

## 3. Tiering System

| Tier | Score Range | Plain-English Meaning | Expected N of 105 | Reconciliation |
|------|-------------|----------------------|-------------------|----------------|
| **A** | 70–100 | Worth a real diligence week. Has a foreign orphan designation AND strong pediatric-rare signal AND solid match confidence. These are the candidates closest to the ~7 actionable programs. Full FTO search, API sourcing assessment, and OOPD exclusivity check are all warranted. | **~5–12** | Must be consistent with the ~7-actionable reality (source 25). An A-tier score does not confer viability — it confers priority for the downstream filters (FTO, API, orphan exclusivity) that the score cannot see. Expect 5–12 to score A; expect ~7 to survive those downstream checks. |
| **B** | 45–69 | Interesting but needs a specific trigger. May have orphan OR pediatric signal, but not both. Or has both but low match confidence (needs verification). Suitable for a half-day desk review to confirm or eliminate. | **~20–30** | Wider band because many candidates have one strong signal and one weak or unknown signal (e.g., orphan flag but no indication text yet, pending EMA enrichment). |
| **C** | 0–44 | Screen-level only. Lacking orphan status, lacks pediatric-rare signal (or has adult-disease disqualifiers), or is a low-confidence match. Not worth analyst time until A+B tiers are exhausted. | **~60–80** | The majority of 105 candidates will fall here. Many are EMA-approved drugs for common adult diseases that happen to have no formal US NDA — agomelatine (depression), isavuconazole (fungal), and similar. These are not PRV plays. |

**Reconciliation with the ~7-actionable reality:**

The score ranks; it does not promise. The ~7-actionable figure from source 25 is the result of applying downstream filters (FTO/patent, orphan exclusivity block, API sourcing, 20-patient trial feasibility) that the score cannot see from summary.json fields alone. The A tier surface area of ~5–12 candidates is designed to be slightly larger than 7 so that the ~7 actionable programs are almost certainly inside the A tier, while a manageable analyst workload (5–12 candidates, not 105) is required to identify them. If the A tier consistently produces more than 15 candidates, the score thresholds should tighten.

---

## 4. Expected-Value Framing Per Candidate

### 4.1 The Formula to Display in the Dashboard

For each candidate, display three EV cells:

```
EV_conservative = P_generic  × $150M − $0.5M  =  0.04 × $150M − $0.5M  = $5.5M
EV_base         = P_optimized × $190M − $0.5M  =  0.21 × $190M − $0.5M  = $39.4M (if optimized program)
EV_ceiling      = P_optimized × $225M − $0.5M  =  0.21 × $225M − $0.5M  = $46.8M
```

More precisely, let the PROMISE score drive a continuous probability interpolation:

```python
def p_success(promise: float) -> tuple[float, float]:
    """
    Returns (p_generic, p_optimized) based on PROMISE score.
    Scores 70+ are treated as optimized-program candidates.
    Scores 45–69 are intermediate.
    Scores <45 use generic probability.
    These are ordinal guides, not actuarial probabilities.
    """
    if promise >= 70:
        return (0.04, 0.21)
    elif promise >= 45:
        frac = (promise - 45) / 25.0  # 0 at score=45, 1 at score=70
        p_opt = 0.04 + frac * (0.21 - 0.04)
        return (0.04, round(p_opt, 3))
    else:
        return (0.03, 0.04)

def ev_range(promise: float) -> dict:
    p_gen, p_opt = p_success(promise)
    prv_values = {"conservative": 150e6, "base": 190e6, "ceiling": 225e6}
    cost = 0.5e6  # $500k trial cost floor (source 27)
    return {
        "p_generic":   p_gen,
        "p_optimized": p_opt,
        "ev_generic_base_usd":   round(p_gen * prv_values["base"] - cost),
        "ev_optimized_base_usd": round(p_opt * prv_values["base"] - cost),
        "ev_optimized_ceil_usd": round(p_opt * prv_values["ceiling"] - cost),
    }
```

### 4.2 Display Guidance

Show EV figures to one significant figure (e.g., "$7M" not "$7,100,000") to avoid false precision. Always display the range ($5–$47M for an A-tier candidate) rather than a single point. Label the EV as "risk-adjusted EV proxy" — not "valuation."

Add a mandatory visible caveat on every candidate card:

> "EV is a risk-adjusted screen proxy. It does NOT account for FTO/patents, existing US orphan exclusivity, API sourcing, trial feasibility, or regulatory path risk. ~7 of the 105 candidates shown are estimated to be truly actionable after those filters."

---

## 5. What the Score CANNOT See — Mandatory Caveats

Every user of this model must understand the following blind spots. These are not disclaimers — they are the real filters that determine which of the ~7 actionable candidates a program is:

### 5.1 Freedom-to-Operate (FTO) / Composition Patents

The score has zero visibility into the patent landscape. Source 25 (§2e) estimates 30–35% of candidates have relevant blocking patents (reduced from the original 50% estimate after KEGG vintage analysis; many Japan-only candidates are pre-1990 and off-patent). For newer candidates (abroad_date post-2010), the FTO risk is substantially higher. **A Tier-A score on a 2019-approved EMA orphan drug is meaningless without a patent search.**

### 5.2 Existing US Orphan Drug Exclusivity

FDA's OOPD database (which is not bulk-accessible — HTTP 403 from automated scripts per source 25 §9 URL ledger) contains designations that would create a "same drug, same indication" exclusivity block. A candidate can score Tier A and still be completely blocked by an existing FDA orphan designation granted to a competitor for the same disease/drug pair. **OOPD manual search is mandatory before any A-tier candidate advances.**

### 5.3 API Sourcing and Manufacturing (MRA vs. Non-MRA)

Source 26 (§4.C) and source 27 (§3.3) establish that a WHO-GMP-only manufacturing site now faces unannounced PAIs (CP 7346.832, effective 2026-08-10) with a ~48–52% pass probability, versus 88% for MRA-country sites. Japan-orphan compounds specifically have a 50–80% API sourcing failure rate (source 25 §10). The score does not know where the API is manufactured. **Sourcing assessment is a first-day diligence action for any A-tier candidate.**

### 5.4 Prodrug / Salt / Monograph False-Positive Risk

The `moiety-base` tier candidates were matched by stripping salts and prodrugs. Some of these may represent a moiety that IS already in the US Orange Book under a related active ingredient or prodrug formulation. The match confidence scoring (MATCHCONF component) penalizes this, but does not eliminate the risk. **All moiety-base tier candidates require a manual UNII / Orange Book check before declaring them PRV-eligible.**

### 5.5 The 37-Month Sunset Clock

The score assigns no time-decay penalty. A candidate that would require 5 years of development does not score lower than one that could be ready for an IND by Q4 2026. In practice, the sunset is the binding constraint: programs that cannot plausibly reach approval by 2029-09-30 have PRV EV = $0 regardless of their promise score. **Diligence must include a timeline feasibility check: does a natural history dataset exist? Is there an existing patient registry? Can enrollment begin within 6 months?**

### 5.6 What "Abroad Approved" Does Not Prove

A foreign approval proves safety and efficacy in the approved indication for the approved population in that jurisdiction. It does NOT prove: (a) pediatric efficacy (many foreign approvals are adult labels), (b) that the foreign clinical data is sufficient for a 505(b)(1) NDA without additional US trials, or (c) that FDA would grant the same indication. Source 26 (§8) documents that SEZABY succeeded because phenobarbital had 100 years of safety data plus a clear neonatal biomarker endpoint — exceptional conditions. The general case requires fresh US clinical data.

---

## 6. Score Calibration Checks

Run these checks whenever the scoring model or underlying data is updated:

1. **Orphan base rate check:** All 15 current candidates with `orphan=True` must score > 55 (since they get 25 raw points from ORPHAN alone, plus at least 3 from REGCOUNT + 3 from MATCHCONF for an EMA single-source exact-moiety match = 31 baseline). Any orphan candidate below 35 signals a data error (indication text triggering an adult-common disqualifier on a known rare disease drug).

2. **Non-orphan ceiling check:** A non-orphan candidate with no indication text (ORPHAN=0, PED=0.2, REGCOUNT single=0.2, MATCHCONF exact=1.0, ATC unknown=0.3, RECENCY unknown=0.3) should score: 35×0.2 + 25×0 + 15×0.2 + 15×1.0 + 5×0.3 + 5×0.3 = 7+0+3+15+1.5+1.5 = **28**. This is a correct Tier-C baseline for an uncharacterized candidate.

3. **Maximum possible score (best case):** 35×1.0 + 25×1.0 + 15×1.0 + 15×1.0 + 5×1.0 + 5×1.0 = **100**. A candidate scoring 100 would be: strong pediatric-rare indication text, foreign orphan designation, 3+ regulators, exact-moiety match, high-PRV ATC code, and approved after 2015. This is the theoretical ceiling.

4. **Tier-A count gate:** If the model produces > 15 Tier-A candidates on the first run, reduce the PED 0.5-level keywords to require stronger text evidence before granting 0.5. The A tier should not exceed 15% of the 105-candidate universe (~16 candidates) — the ~7-actionable reality makes any larger A tier implausible.

5. **Reconciliation sanity:** `count(Tier A) × P_optimized_avg ≈ 7 × ~15% ≈ 1.0` expected approval. This is consistent with "expected approvals ≈ 0.5–0.8 for a realistic mixed portfolio" (source 26 §8). If the A tier count and P_optimized are calibrated correctly, the model implicitly encodes the portfolio math from the feasibility research.

---

## 7. Integration Roadmap for summary.json

### 7.1 Fields required before scoring goes live

| Field name | Source | Status | Priority |
|---|---|---|---|
| `indication` | EMA EPAR / product label | TO ADD via EMA enrichment | Critical — drives 35-weight PED component |
| `therapeutic_area` | EMA EPAR | TO ADD | Critical — secondary PED signal |
| `atc_code` | EMA ATC classification | TO ADD | Medium — 5-weight ATC component |
| `abroad_date` | EMA EPAR approval date | TO ADD | Low — 5-weight RECENCY component |
| `orphan` | Already in summary.json | Exists | None |
| `sources` | Already in summary.json | Exists | None |
| `tier` | Already in summary.json | Exists | None |

### 7.2 Immediate interim scoring (with current data)

Until EMA enrichment lands, compute a degraded score using only the currently available fields:

```python
def promise_score_interim(candidate: dict) -> float:
    """
    Interim score using only fields available in current summary.json.
    PED defaults to 0.2 (no text available), ATC defaults to 0.3, RECENCY defaults to 0.3.
    Result is a flat prior with orphan + regcount + matchconf as differentiators.
    """
    orph  = orphan_score(candidate.get("orphan", False))
    reg   = regcount_score(candidate.get("sources", []))
    match = matchconf_score(candidate.get("tier"))
    return round(
        35 * 0.2          # PED: no data, use floor
        + 25 * orph
        + 15 * reg
        + 15 * match
        + 5  * 0.3        # ATC: unknown
        + 5  * 0.3,       # RECENCY: unknown
        1
    )
```

With interim scoring, all 15 orphan candidates will cluster at ~49–53 (Tier B), and non-orphan candidates will spread 28–36 (Tier C) based on REGCOUNT and MATCHCONF variation. This is the correct behavior: the interim score surfaces the orphan candidates as higher priority without making false claims about pediatric qualification.

---

## 8. Model Limitations Summary (IC Presentation Version)

**What this model is:** A risk-adjusted screening tool that ranks 105 anti-join candidates by their estimated prior probability of surviving the downstream diligence filters that determine PRV eligibility and trial feasibility.

**What this model is not:** A valuation, a probability of regulatory approval, or a guarantee that any candidate is actionable.

**The most important number this model does not compute:** Whether the program can begin enrollment before 2027-02-28 (the latest first-patient-in date consistent with PRV eligibility per source 26). That determination requires a disease-specific assessment of patient registry existence, advocacy group readiness, and site investigator availability — none of which is in summary.json.

**The most dangerous number this model produces:** The EV figures ($5M–$47M range). These are mathematically correct given the input assumptions but look large relative to trial costs. An IC should be reminded that the PRV EV is multiplied by P(success) which is 3–22%, and that the ~7-actionable pool size means most of the 105 candidates have PRV EV ≈ $0 regardless of their score.

**Recommended use:** Sort by PROMISE score descending. Conduct manual diligence on all Tier-A candidates (expected ~5–12). Apply the five blind-spot filters (FTO, OOPD, API sourcing, prodrug/monograph, timeline) before any program advances to IND discussion. The score tells you where to look; it does not tell you what you will find.

---

*Model version: 1.0. Grounded in: sources/25-feasibility-pool-size.md, sources/26-feasibility-timeline.md, sources/27-feasibility-recruitment.md, sources/18-prv-transaction-market.md, sources/24-prv-deal-mechanics.md. All probability and EV figures derived from adversarially reconciled primary-source research conducted 2026-08-06.*
