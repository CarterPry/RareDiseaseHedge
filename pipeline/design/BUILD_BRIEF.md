# Triage v2 — Prioritized Build Brief

**Date:** 2026-08-07
**Authority:** CREATIVE_DIRECTION.md (reconciliation decisions take precedence over DESIGN_SPEC.md and SCORING_MODEL.md where they conflict)
**Constraint:** Single-file, self-contained HTML (vanilla JS, no build step). Data embedded inline.
**Engineer note:** Items marked [ESSENTIAL] must ship in the initial build pass. Items marked [LATER] are deferred to a second pass after the essential build is user-tested.

---

## Item 1: Data Contract — verify and canonicalize summary.json fields [ESSENTIAL]

**What:** Before writing a line of UI, confirm the data shape the dashboard will consume. The current summary.json already contains `area`, `atc`, `indication`, and `approved` fields (confirmed in the live data). Map these to the design contract field names:

| summary.json field | Design contract name | Notes |
|---|---|---|
| `area` | `therapeutic_area` | May be semicolon-delimited; take first segment for display |
| `atc` | `atc_code` | Already present (e.g., "L01EX") |
| `indication` | `indication` | Already present; may be empty string |
| `approved` | `abroad_date` | Already present; may be empty string |
| `orphan` | `orphan` | Boolean — already present |
| `sources` | `sources` | Array — already present |
| `tier` | `tier` | String — already present |
| `unii` | `unii` | Stable key for localStorage triage |

**Add to summary.json header (pipeline-generated, not analyst-assigned):**
- `confidence`: derive from `tier` field: exact-moiety → "high"; moiety-base → "medium"; name-match or fuzzy → "low". Add this derivation in the JS layer if pipeline doesn't generate it — no pipeline change required for v2.

**Do not add yet:**
- `score`: computed client-side from the interim formula (see Item 2). Not stored in summary.json in the initial build.
- `score_breakdown`: computed client-side alongside the score.
- `caveats`: stub as empty array `[]` for all candidates in v2. The caveat-flag UI renders but shows nothing until the pipeline adds this field.

**Acceptance:** `DATA.candidates[0]` in the JS has all eight fields above with defined values or empty strings. No undefined access errors on first render.

---

## Item 2: Implement interim PROMISE score in client-side JS [ESSENTIAL]

**What:** Compute the PROMISE score for each candidate in JS at page load time, before rendering. Use the interim formula from SCORING_MODEL §7.2, adapted to the actual summary.json field names:

```js
function promiseScore(c) {
  // Interim: PED defaults to 0.2 (no validated indication scoring yet)
  const orph  = c.orphan ? 1.0 : 0.0;
  const reg   = c.sources.length >= 3 ? 1.0 : c.sources.length === 2 ? 0.6 : c.sources.length === 1 ? 0.2 : 0.0;
  const tierMap = {'exact-moiety': 1.0, 'moiety-base': 0.7, 'name-match': 0.4, 'fuzzy': 0.1};
  const match = tierMap[c.tier] ?? 0.3;
  const atcMap = {'A16':1,'A11':1,'A12':1,'N07':1,'V03':1,'S01':1,'L04':1,'B06':1,
                  'N06':.5,'A14':.5,'M09':.5,'D11':.5,'L01':.5,'G04':.5,'H04':.5};
  const atcKey = (c.atc_code || '').slice(0,3).toUpperCase();
  const atc = c.atc_code ? (atcMap[atcKey] ?? 0.1) : 0.3;
  const rec = (() => {
    if (!c.abroad_date) return 0.3;
    const y = parseInt(c.abroad_date.slice(0,4));
    if (y >= 2015) return 1.0;
    if (y >= 2005) return 0.7;
    if (y >= 1995) return 0.4;
    return 0.1;
  })();
  return Math.round(35*0.2 + 25*orph + 15*reg + 15*match + 5*atc + 5*rec);
}

function scoreBreakdown(c, score) {
  return {
    ped:   { weight:35, sub:0.2, contribution: Math.round(35*0.2), note:'Interim — awaiting indication data' },
    orphan:{ weight:25, sub:c.orphan?1:0, contribution: Math.round(25*(c.orphan?1:0)), note:'' },
    regcount:{ weight:15, sub: c.sources.length>=3?1:c.sources.length===2?.6:c.sources.length===1?.2:0,
               contribution: Math.round(15*(c.sources.length>=3?1:c.sources.length===2?.6:c.sources.length===1?.2:0)), note:'' },
    matchconf:{ weight:15, sub:({'exact-moiety':1,'moiety-base':.7,'name-match':.4,'fuzzy':.1}[c.tier]??0.3),
                contribution: Math.round(15*({'exact-moiety':1,'moiety-base':.7,'name-match':.4,'fuzzy':.1}[c.tier]??0.3)), note:'' },
    atc:   { weight:5, sub: /* same as above */ 0, contribution:0, note: c.atc_code ? '' : 'ATC unknown' },
    recency:{ weight:5, sub: /* same as above */ 0, contribution:0, note: c.abroad_date ? '' : 'Date unknown' },
    total: score,
    model: 'interim'
  };
}
```

Attach `c._score` and `c._breakdown` to each candidate object after parsing DATA but before any render. These are ephemeral (not persisted). When EMA enrichment lands and the pipeline adds full indication text, swap `35*0.2` for `35*ped_score(c.indication, c.therapeutic_area)` — a one-line change.

**Acceptance:** `DATA.candidates` sorted by `_score` descending shows the 15 orphan candidates clustering at the top with scores ~31–53, and non-orphan single-source exact-moiety candidates at ~28–36.

---

## Item 3: CSS token system and typography [ESSENTIAL]

**What:** Replace the v1 `--bg/#eef1f5` color system entirely. Implement all tokens from DESIGN_SPEC.md §0.2. Load IBM Plex Sans (400, 500, 600) and IBM Plex Mono (400, 600) via Google Fonts @import at the top of the `<style>` block.

**Key departures from v1:**
- Page ground: `#F5F2EC` (parchment), not `#eef1f5` (cool gray)
- Header: `background: var(--ink)` flat dark, not teal gradient
- Candidate layout: full-width rows with hairline borders, not card grid with box-shadows
- No `border-radius:12px` or `box-shadow` per candidate — shadow reserved for page shell and drawer only
- One accent color only: `var(--signal)` #0B6E75

**Implement the full CSS architecture from DESIGN_SPEC §8 in order.** This is a complete rewrite of the v1 styles, not a patch.

**Acceptance:** Screenshot of the page (even with placeholder data) matches the parchment/ink/hairline-border aesthetic described in DESIGN_SPEC §0.2. IBM Plex loads correctly; no system-font fallback visible.

---

## Item 4: Page layout — header, honesty bar, stat cards, collapsible funnel [ESSENTIAL]

**What:** Build the above-the-fold layout from DESIGN_SPEC §4.1 in order:

1. **Header (56px):** Dark ink background. Left: name "Triage" + subtitle "Funnel A PRV-Eligible Candidate Universe". Right: [Export] + generated timestamp.
   - Title does NOT say "105 Opportunities." It says "Funnel A Screening — 105 Candidates."

2. **Honesty bar (always visible, never collapsible):** Implement exactly as DESIGN_SPEC §4.3. The text must read: "**105 candidates** in screening shortlist · **~7 estimated actionable** programs after orphan designation, pediatric-indication fit, FTO, API sourcing, and timeline filters · FDA PRV sunset: **2029-09-30** · Window remaining: **37 months**"

3. **Stat cards (4 cards):**
   - Card 1: `105` / "Named drug candidates" / "screening shortlist" (last line mandatory per CREATIVE_DIRECTION §3 Attack 1)
   - Card 2: `15` / "Foreign orphan-flagged" / "rare-disease filter passed; pediatric, FTO, API, timeline filters remain" (sub-label from CREATIVE_DIRECTION §3 Attack 6)
   - Card 3: `~7` / "Estimated actionable" / "after FTO, orphan exclusivity, API sourcing, and timeline filters" (tilde mandatory)
   - Card 4: `37 mo.` / "To PRV sunset" / "2029-09-30" (color: ink-secondary at 37 months — NOT amber yet per CREATIVE_DIRECTION §3 Attack 5)

4. **Funnel:** Collapsed by default (`<details>`). Uses v1 funnel data from DATA.funnel. Bars use `var(--signal)` and `var(--rule-strong)` per DESIGN_SPEC §4.8. The funnel section is a visual reference — not interactive.

**Acceptance:** At 1280px viewport, honesty bar, all 4 stat cards, and the first 8 candidate rows are visible without scrolling. Funnel is collapsed.

---

## Item 5: Candidate row — full-width list with score column [ESSENTIAL]

**What:** Replace the v1 card grid with the row list from DESIGN_SPEC §1.1–§1.5. Implement all three lines:

- **Line 1:** Drug name (ALL CAPS) + badge row. Badges: ORPHAN (gold), INN (green), USAN (blue), ATC code (purple), caveat flag (amber). ATC badge shows the atc_code value from data (e.g., "L01EX").
- **Line 2:** Therapeutic area (Plex Sans 500) + `·` + indication truncated to 1 line. If both fields empty/null, omit line 2 entirely (row renders as 2-line only).
- **Line 3:** Source chips (EMA, Health Canada, etc.) + abroad date (formatted "Approved YYYY-MM-DD" or "—") + confidence dot + label.
- **Score column (96px, right side):** Number only (22px Plex Mono 600, score-tier color) + 10-segment bar. NO tier label in the row per CREATIVE_DIRECTION Decision 2.
- **Triage rail (4px left border):** Neutral gray by default, semantic color when triage state is set.

**Row hover:** On hover, show 3 inline triage icon buttons (◆ keep / ◎ investigate / ✕ reject) to the left of the score column. Click sets triage state without opening drawer.

**Acceptance:** 105 rows render. Row height 66–72px. Score column visible and distinct. Clicking a row (not an icon) opens the drawer. Triage icon clicks do not open the drawer.

---

## Item 6: Detail drawer [ESSENTIAL]

**What:** Implement the slide-in drawer from DESIGN_SPEC §2.1–§2.9 with the following modifications from CREATIVE_DIRECTION:

**Drawer sections in order:**
1. Sticky header: drug name + triage segmented control (KEEP / INVESTIGATE / REJECT) + ✕ dismiss
2. Badges (ORPHAN, INN, USAN, ATC)
3. **PROMISE SCORE (TRIAGE RANK ONLY)** — title uses this exact phrase per CREATIVE_DIRECTION Decision 2. Score number + tier label ("A — Worth diligence" / "B — Needs trigger" / "C — Screen level"). Inline note: "Ranks likelihood of surviving downstream diligence — not probability of regulatory approval." If model='interim': show amber "Score: interim — PED component (weight 35) unscored pending indication data." Breakdown table (collapsed by default).
4. **WHAT IT TREATS:** Therapeutic area + full indication text (quoted block, italicized).
5. **ATC CLASSIFICATION:** atc_code + label (derive human-readable ATC label from code in JS lookup table).
6. **REGULATORY DATES:** Abroad approval date or "—".
7. **RISK-ADJUSTED EV PROXY** (title in ink-tertiary, secondary visual weight): Show "P(success): 4% generic / up to 21% optimized" FIRST, then "Trial cost floor: ~$0.5M", then the range "$XM – $YM". For Tier C (score < 45), replace entire block with amber caveat: "EV proxy not shown — candidate requires stronger diligence basis before financial framing is appropriate." Add mandatory caveat block (amber, caveat-flag style) per CREATIVE_DIRECTION Decision 1.
8. **TIMELINE CHECK** (new section — add per CREATIVE_DIRECTION §3 Attack 5): Label "Latest viable first-patient-in: 2027-02-28". Two checkboxes (localStorage-persisted per UNII): "[ ] Patient registry or natural history dataset identified" and "[ ] Advocacy group contact made." These are analyst working notes, not pipeline data.
9. **SOURCES & PROVENANCE:** Source chips + confidence + UNII + match tier + external links (EMA, PubMed, DrugBank, FDA UNII).
10. **CAVEAT FLAGS:** Show if caveats array non-empty; hide section entirely if empty (most will be empty in v2 initial build).
11. **TRIAGE NOTE:** Textarea, auto-save to localStorage on input (debounced 400ms).

**ARIA:** role="dialog", aria-modal="true", Esc dismisses, focus trap, focus returns to triggering row on close.

**Acceptance:** Drawer opens on row click, shows correct data for that candidate, closes on Esc/overlay/✕. Triage state set in drawer updates row rail color. Note persists across page reloads.

---

## Item 7: Triage state management and progress bar [ESSENTIAL]

**What:** Implement the full triage state model from DESIGN_SPEC §3.1–§3.7.

- **State store:** localStorage key `rdh_triage_v2`. Schema: `{ [unii]: { state: 'keep'|'investigate'|'reject', note: string, ts: number } }`.
- **Progress bar:** Sticky, 105-dot display. Every session, all 105 dots are shown — never reduce to the filtered count. This preserves spatial awareness of incompleteness (CREATIVE_DIRECTION §3 Attack 4).
- **Rejected rows:** Render at `opacity:0.55` by default. Filter chip "[ ] Rejected" can include or exclude them.
- **Export / Import:** Per DESIGN_SPEC §3.6–§3.7.
- **Interim score banner:** Displayed below filter controls (dismissible per session, not permanently): "Score is interim — PED component (weight 35) unscored pending EMA enrichment. Rankings may shift materially when full scoring runs." See CREATIVE_DIRECTION §3 Attack 4. Dismiss stores `rdh_banner_dismissed_<date>` in localStorage (reappears next day).

**Acceptance:** Triage state survives page reload. Progress bar shows correct filled/hollow dots. Export downloads valid JSON. Import restores triage state.

---

## Item 8: Sort, filter, search controls [ESSENTIAL]

**What:** Implement the controls bar from DESIGN_SPEC §4.5–§4.7.

- **Sort:** 8 options per DESIGN_SPEC §4.5. Default: score descending.
- **Filter chips Row 1:** Orphan only / INN / EMA / Health Canada / Swissmedic / Japan
- **Filter chips Row 2:** Keep / Investigate / Untriaged / All
- **Search:** debounced 200ms, searches name + indication + therapeutic_area (note: `area` field in data)
- **Count label:** "Showing X of 105 candidates"
- **Orphan-only filter banner:** When "Orphan only" filter is active, show the banner from CREATIVE_DIRECTION §3 Attack 6 above the candidate list.

**Acceptance:** All 8 sort options work. Filter chips and search are composable (AND logic). Count updates reactively.

---

## Item 9: Accessibility pass [ESSENTIAL]

**What:** Implement all requirements from DESIGN_SPEC §5.1–§5.4.

- All rows: `role="button" tabindex="0"`, Enter/Space opens drawer
- Drawer: focus trap, Esc dismiss, focus return
- Chips: `role="checkbox" aria-checked`
- `@media (prefers-reduced-motion: reduce)`: no drawer slide, no bar animation
- `@media print`: hide controls, drawer, progress bar; show candidate list with score numbers

**Acceptance:** Tab navigation reaches every interactive element. Drawer keyboard interaction per §5.1. prefers-reduced-motion respected.

---

## Item 10: "Surprise me" sort + score tier color calibration [LATER]

**What:** Add a random-shuffle sort option ("Shuffle") to the sort dropdown. This forces exposure to non-top-ranked candidates and reduces score-rank anchoring (CREATIVE_DIRECTION §3 Attack 4). Low implementation cost (~3 lines of JS).

Also: once the EMA enrichment pipeline is validated and full PED scoring runs, update the score color thresholds. Currently with interim scoring, scores will cluster tightly (28–53) and tier colors may not differentiate well. After full scoring, recalibrate the tier breakpoints if needed.

**Acceptance:** Shuffle option appears in sort dropdown, randomizes display order. Score tier colors visually differentiate at least 3 distinct bands across the 105-row list.

---

## Item 11: EMA enrichment pipeline integration [LATER]

**What:** Run the full PROMISE score (six components) once `indication`, `therapeutic_area`, `atc_code`, and `abroad_date` are confirmed as populated and validated across all EMA candidates. Update the JS scoring function: replace `35*0.2` with `35*pedScore(c.indication, c.therapeutic_area)`. Update the drawer score model label from 'interim' to 'full'. Remove the interim score banner.

**Also at this point:**
- Validate that Tier A count is 5–15 (SCORING_MODEL §3 gate check). If > 15, tighten the PED_MODERATE keyword list.
- Run the calibration checks from SCORING_MODEL §6.

**Acceptance:** All 15 orphan candidates score above 55. The Tier A count is in the 5–15 range. The interim score banner is gone.

---

## Item 12: Caveat flag population [LATER]

**What:** Populate the `caveats` array in summary.json for candidates that are known to be prodrugs, salt forms, OTC monograph risks, withdrawn products, or vet-only sources. This requires manual analyst review or pipeline enhancement.

Display: per DESIGN_SPEC §2.8 — amber block, stack vertically, hidden if array empty.

**Acceptance:** At least the candidates with tier='moiety-base' display a "salt/ester form — moiety-base match only" caveat flag.

---

## Item 13: Timeline feasibility field in drawer [LATER — but architecture now]

**Note:** The two localStorage-persisted checkboxes in the drawer (Item 6, section 8) should be architected from the start even if the UI is minimal in v2. Use the same `rdh_triage_v2` localStorage schema, extending it: `{ [unii]: { state, note, ts, registry_identified: bool, advocacy_contact: bool } }`. This prevents a localStorage schema migration later.

**Acceptance:** The schema extension exists from day one. The checkbox UI can be minimal (plain `<input type="checkbox">`) in the initial build and styled later.

---

## Dependency order summary

```
Item 1 (data contract)
  → Item 2 (scoring)
    → Item 5 (rows)
      → Item 6 (drawer)
      → Item 7 (triage)
      → Item 8 (controls)
  → Item 3 (CSS)
    → Item 4 (header/honesty)
    → Item 5 (rows)
  → Item 9 (a11y — layered on top of 5, 6, 8)
```

Items 10–13 are independent of each other and can be added in any order after Items 1–9 ship.

---

## What is explicitly out of scope for v2

- Server-side rendering, build tools, npm dependencies
- API calls (all data embedded inline)
- Collaboration / multi-user sync (export/import covers team handoff)
- Patent search integration (FTO is a manual step — the drawer links to external search tools)
- OOPD search automation (still HTTP 403 from automated scripts per source 25 §9)
- Mobile-first layout (analysts are on desktop; responsive breakpoints from DESIGN_SPEC §11 are implemented but not the primary design target)

---

*This brief is implementation-complete. An engineer should execute Items 1–9 in one pass to produce the v2 dashboard. Items 10–13 are the second pass.*
