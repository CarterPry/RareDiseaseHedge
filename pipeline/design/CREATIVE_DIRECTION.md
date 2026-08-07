# Triage — Creative Direction

**Document owner:** Creative Director / Head of Product
**Date:** 2026-08-07
**Supersedes:** Design intent in DESIGN_SPEC.md §0.1 and SCORING_MODEL.md §0 where they conflict

---

## 1. North Star

**Platform name: Triage**
**Positioning line:** A regulatory review file for 105 PRV candidates — ranked, annotated, and honestly scoped.

Triage is a single-session triage instrument for one analyst spending two to four hours determining which of 105 foreign-approved drug candidates is worth a real diligence week. Its one job — the only job it must do supremely well — is to surface the ~7 actionable programs without letting the 98 non-actionable ones waste analyst time or distort judgment. Every design and scoring decision serves that job. The platform must feel like a well-organized regulatory binder, not a biotech pitch deck.

---

## 2. Reconciliation Decisions

The following conflicts between DESIGN_SPEC.md and SCORING_MODEL.md are resolved here. These decisions are final and the BUILD_BRIEF enforces them.

### Decision 1: EV figures are drawer-only, never on the row

SCORING_MODEL §4.1 proposes three EV cells (conservative / base / ceiling). DESIGN_SPEC §1.2 specifies three lines maximum per row and reserves line 3 for sources + date + confidence. These are irreconcilable on a dense row.

**Ruling: EV figures go in the drawer only.** The row carries no dollar figures. Reason: displaying "$39M" on 105 rows next to a prominent score number will read as 105 investment opportunities, which contradicts the honesty constraint. Inside the drawer, the EV block is shown with its mandatory caveat in full view. The analyst who opens the drawer has already made the cognitive commitment to examine this candidate; the framing risk is contained.

One change to the EV display vs. SCORING_MODEL §4.1: display EV as a range only ("$6M – $47M risk-adjusted proxy"), never as a single base-case figure. Single-point EV implies precision this model does not have.

### Decision 2: Score bar tier labels use full words in the drawer but are suppressed in the row score column

DESIGN_SPEC §1.3 puts the tier label ("STRONG", "MODERATE", etc.) in the score column of every row. SCORING_MODEL §3 warns that a "STRONG" label on a non-orphan, uncharacterized candidate misleads about viability.

**Ruling: The score column shows the number and the 10-segment bar only — no tier label in the row.** The tier label ("A — Worth diligence", "B — Needs trigger", "C — Screen level") appears only in the drawer header, after the full disclaimer context. This prevents a row-level heuristic ("this one says STRONG") from short-circuiting the analyst's read of the indication and caveat flags.

### Decision 3: Interim scoring is mandatory for the initial build; full scoring deploys only after EMA enrichment is validated

SCORING_MODEL §7.2 defines an interim scoring path using only orphan, sources, and tier (the three fields already present in summary.json). DESIGN_SPEC assumes the full six-component score is available at build time.

**Ruling: Ship the interim score first.** The score column is live and functional — it just uses the interim formula. A persistent label reads "Score: interim (PED unscored)" in the drawer breakdown. When EMA enrichment fields (indication, therapeutic_area, atc_code, abroad_date) are populated and validated, the pipeline reruns the full formula and the label updates to "Score: full model." This prevents a false sense of analytical completeness during the window when PED — the 35-weight dominant component — is unscored. The interim score correctly clusters the 15 orphan candidates at ~49–53 and the rest at 28–36, which is the honest prior state of knowledge.

---

## 3. Honesty Audit

This section adversarially attacks the v2 design as if the goal were to stop a naive reader from over-reading the platform.

### Attack 1: "105 candidates" in the header implies a large, rich opportunity set

**Threat:** A new analyst reading the header "105 Named Drug Candidates" before reading the honesty bar will anchor on 105. Even a 5% skim rate feels like "5 real deals." The stat card showing `105` in 28px bold Mono reinforces this. If someone screenshots the dashboard header for a presentation, the honesty bar is below the fold.

**Guardrails:**
- The stat card for 105 must carry a sub-label "screening shortlist" in the card body, not just in the honesty bar. The number 105 must never appear alone without its qualifier.
- The header title must read "Funnel A Screening — 105 Candidates" (not "105 Opportunities" or "105 Programs").
- The ~7 actionable card uses a `~` tilde as the first character of the number display, and its sub-label reads "estimated actionable after FTO, orphan exclusivity, API sourcing, and timeline filters" — not just "actionable."
- Default sort is score descending, which shows the most charitable view first. This is unavoidable for triage utility, but the triage progress bar must always show the full 105-dot range so the analyst retains the sense of scale of what has not yet been reviewed.

### Attack 2: A score of 78 implies high probability of success

**Threat:** "78 / 100" in 22px monospace reads like a grade. A user unfamiliar with the model's 35-weight default PED=0.2 floor may interpret 78 as "78% viable." The tier label "STRONG" compounds this if it appears in the row.

**Guardrails:**
- No tier label in the row (see Decision 2 above).
- The drawer score block must be titled "PROMISE SCORE (triage rank only)" — not "Quality Score" or "Viability Score."
- Immediately below the score bar, before the breakdown table: a 1-line inline note in ink-tertiary: "Ranks likelihood of surviving downstream diligence — not probability of regulatory approval."
- The breakdown table must show the PED row prominently. If PED is scored at the interim default (0.2, "unscored"), the PED row renders in amber with the label "PED: unscored — awaiting indication data." This makes the incompleteness of the interim model visible at the point of decision, not buried in a footer.

### Attack 3: EV figures ($39M) create false precision and anchor on upside

**Threat:** Even range-format EV ("$6M – $47M") displayed on every row or in a prominent drawer position will anchor the analyst on the $47M ceiling rather than on P(success) = 4–21%. The denominator (trial cost, probability) disappears in the presence of large dollar numbers.

**Guardrails:**
- EV block in the drawer is titled "RISK-ADJUSTED EV PROXY" in ink-tertiary, not a primary heading.
- The two lines that precede the EV number: "P(success): 4% generic / up to 21% optimized" and "Trial cost floor: ~$0.5M." The probability appears before the dollar amount, not after.
- Below the EV range: the mandatory caveat from SCORING_MODEL §4.2 is quoted verbatim and rendered in the investigate-bg amber block style — same visual weight as a caveat flag. It cannot be a footnote.
- EV is not shown at all for Tier-C candidates (score < 45). For C-tier, the EV block is replaced with a single amber line: "EV proxy not shown — candidate requires stronger diligence basis before financial framing is appropriate."

### Attack 4: The default sort (score high to low) creates a false top-10 mental model

**Threat:** The analyst will naturally stop reading after the first 10–15 rows. If the top 10 are all ORPHAN-flagged candidates and score 49–53 (interim model), the analyst may conclude those are the actionable programs and deprioritize the rest. In reality, a non-orphan with strong indication text (not yet scored) could be a Tier-A candidate the interim model cannot see.

**Guardrails:**
- A banner below the sort/filter bar, displayed only when interim scoring is active: "Score is interim — PED component (weight 35) unscored pending EMA enrichment. Rankings may shift materially when full scoring runs." This banner is dismissed per session (localStorage flag) but reappears on next session load.
- The triage progress bar always shows all 105 dots. After the analyst marks 10 rows, 95 dots remain hollow — a persistent spatial reminder that the triage is incomplete.
- A "Surprise me" sort option (random shuffle) is a low-effort addition that forces the analyst to encounter the list in a non-ranked order occasionally, reducing anchoring on score-rank position.

### Attack 5: The sunset clock creates urgency that overrides quality filters

**Threat:** "37 months remaining" displayed in red-adjacent amber on a visible stat card may push analysts toward programs that look fastest to advance rather than programs that are genuinely viable. Speed and viability are not the same filter.

**Guardrails:**
- The sunset stat card color is neutral (ink-secondary) at 37 months, not amber. Amber threshold is 24 months, red is 12 months. The current state (37 months) does not warrant alarm coloring.
- The drawer timeline section (not specified in DESIGN_SPEC — add it) shows the latest viable first-patient-in date (2027-02-28) and asks "Is a patient registry or natural history dataset available?" as a labeled checkbox the analyst can check off per candidate. This converts the sunset pressure into a specific actionable question rather than a diffuse urgency signal.

### Attack 6: "15 Orphan-flagged" stat card implies 15 investable programs

**Threat:** The 15-orphan card sits next to the ~7-actionable card. A reader may perform quick mental division (15 ÷ 2 ≈ 8) and conclude that about half the orphan-flagged candidates are actionable — which is optimistic. The actual filter chain removes 50–80% of even orphan candidates on FTO, API sourcing, and timeline grounds.

**Guardrails:**
- The 15-orphan card sub-label: "foreign orphan designation (rare-disease filter passed; pediatric, FTO, API, timeline filters remain)."
- The 15 orphan-flagged candidates, when filtered to "Orphan only" view, display a filter-active banner: "Showing 15 orphan-flagged candidates. Foreign orphan status confirms rare-disease classification; it does NOT confirm pediatric indication fit, freedom to operate, or API sourcing."

---

*End of creative direction. The BUILD_BRIEF.md enforces these decisions as engineering requirements.*
