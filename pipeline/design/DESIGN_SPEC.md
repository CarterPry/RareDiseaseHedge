# RareDiseaseHedge Dashboard v2 — Design Specification

**Document owner:** Senior Product / UX Designer  
**Date:** 2026-08-07  
**Constraint:** Self-contained, single-file, vanilla JS, no build step, data embedded inline.  
**Honesty constraint (non-negotiable):** 105 candidates is a screening shortlist. ~7 are truly actionable. The UI must keep that truth visible at every level.

---

## 0. Design Foundation

### 0.1 Domain Exploration

**Who is this human?**  
A biotech analyst or deal-team principal, working at a desk, probably dual-monitor. They have 2–4 hours blocked for a focused triage session. They have read the feasibility memos. They know the program is hard. They are not being sold to — they are doing serious, consequential work and they know it.

**What must they accomplish?**  
Mark each of 105 candidates as Keep / Investigate / Reject with a note, starting from score-ranked order, finishing with a short list of 5–10 programs worth DD. The verb is: *triage*.

**What should this feel like?**  
A regulatory review file — not a startup dashboard. Dense and precise. Monochromatic with deliberate, meaningful color for signal only. The tone of a well-organized case binder: authoritative, legible, zero decoration. The aesthetic is the Bloomberg terminal crossed with a well-designed legal exhibit — cold and precise, not clinical-sterile.

### 0.2 Aesthetic Direction

**Not:** Soft gradients, rounded pill buttons, card shadows, purple accents, Inter + white cards.  
**Yes:** A dark-cream ground (#F5F2EC), hairline borders, tabular monospace data cells, a single teal accent used only for interactive states and CTAs, and a 4px left-rail color encoding triage state.

**Token naming that belongs to this domain:**

```css
--parchment:        #F5F2EC;   /* page ground */
--parchment-raised: #FDFCF9;   /* card surfaces */
--ink:              #0F1A20;   /* primary text */
--ink-secondary:    #3B4D58;   /* secondary text / labels */
--ink-tertiary:     #6E7E8A;   /* metadata / muted */
--ink-ghost:        #9DAAB4;   /* placeholders, disabled */
--rule:             rgba(15,26,32,.10);  /* hairline borders */
--rule-strong:      rgba(15,26,32,.18); /* section dividers */
--signal:           #0B6E75;   /* the ONE brand/interactive color */
--signal-dim:       #D5EEF0;   /* signal background tint */
--signal-ink:       #075056;   /* signal hover/active text */
--keep:             #2B7A3D;   /* triage: keep */
--keep-bg:          #EAF3EC;
--investigate:      #B06000;   /* triage: investigate */
--investigate-bg:   #FDF3E0;
--reject:           #A52828;   /* triage: reject */
--reject-bg:        #FAECEC;
--score-top:        #0B5A62;   /* score tier: high */
--score-mid:        #7A5C00;   /* score tier: medium */
--score-low:        #6B3838;   /* score tier: low */
--shadow-card:      0 1px 2px rgba(15,26,32,.04), 0 3px 8px rgba(15,26,32,.06);
```

### 0.3 Typography

**Fonts (both available on Google Fonts — load via @import in the file head):**

| Role | Family | Weights |
|------|--------|---------|
| Labels, nav, badges, scores | `IBM Plex Mono` | 400, 600 |
| Drug names, headings, body | `IBM Plex Sans` | 400, 500, 600 |

**Rationale:** IBM Plex is a single superfamily designed for information-dense regulatory/technical contexts (IBM R&D tooling). Plex Mono for all data cells and scores creates the "filing-system" register. Plex Sans for prose and names. Both share the same skeleton — no pairing tension.

**Type scale (px, at 16px root):**

| Token | Size | Weight | Use |
|-------|------|--------|-----|
| `--t-hero` | 28px | 600 Sans | Page title |
| `--t-section` | 11px | 600 Sans, uppercase, 0.8px tracking | Section labels |
| `--t-drug-name` | 15px | 600 Sans | Drug name in row |
| `--t-indication` | 13px | 400 Sans | Therapeutic area / indication |
| `--t-label` | 11px | 600 Mono, uppercase | Field labels in drawer |
| `--t-data` | 13px | 400 Mono | Data values in drawer |
| `--t-score-number` | 22px | 600 Mono | Promise Score display |
| `--t-badge` | 10.5px | 600 Mono | Badges (ORPHAN, INN, USAN) |
| `--t-body` | 13.5px | 400 Sans | Drawer prose |
| `--t-meta` | 12px | 400 Mono | Dates, UNIIs, sources |

**Line-height defaults:** 1.4 for UI text, 1.6 for prose (drawer indication text).

---

## 1. Enriched Candidate Card / Row

### 1.1 Layout

Each candidate is a **full-width row** (not a card grid). The list is a `<div role="list">` with `display:flex; flex-direction:column; gap:0` — rows are separated by hairline `border-bottom: 1px solid var(--rule)` only. No card box-shadow per row (shadow reserved for the page shell and drawer). This keeps the list readable as a filing manifest.

```
┌─ TRIAGE RAIL (4px) ─┬──────── ROW CONTENT ─────────────────────────────────────────────┬── SCORE COLUMN ──┐
│                     │ [DRUG NAME]              [ORPHAN] [INN] [USAN] [ATC class badge]  │    [score num]   │
│                     │ Therapeutic area · Indication (truncated to 1 line)               │   [tier label]   │
│                     │ [source chips]  [date]  [confidence dot + label]                  │   [score bar]    │
└─────────────────────┴──────────────────────────────────────────────────────────────────┴──────────────────┘
```

**Column widths:**
- Triage rail: 4px solid, no padding, left edge of row
- Row content: `flex:1`, `padding: 13px 16px 13px 20px`
- Score column: `width:96px`, `padding:13px 14px`, right-aligned, `border-left: 1px solid var(--rule)`

**Row hover:** `background: rgba(11,110,117,.04)` — a very faint signal tint. Cursor: `pointer`.  
**Row active (clicked):** `background: var(--signal-dim)`.

### 1.2 Information Hierarchy — Three Lines Maximum

**Line 1 (primary):** Drug name + badges  
**Line 2 (secondary):** Therapeutic area · Indication snippet  
**Line 3 (tertiary):** Source chips + abroad approval date + confidence

This reads in under 2 seconds because the eye path is: name → what it treats → where it came from. Score sits to the right as a persistent number — visible peripherally without demanding attention.

#### Line 1: Name + Badges

```
BARDOXOLONE METHYL           ★ ORPHAN   INN   USAN   C09AA
```

- Drug name: `IBM Plex Sans 600, 15px, var(--ink)`, `letter-spacing:-.1px`
- Name renders in ALL CAPS to distinguish from indication prose
- Badges inline, `margin-left:10px`, styled as tight monospaced pills

**Badge styles:**

| Badge | Background | Text | Border |
|-------|-----------|------|--------|
| `★ ORPHAN` | `#FDF3D7` | `#8A5A00` | `1px solid #D9C07A` |
| `INN` | `#EAF3EC` | `#2B7A3D` | `1px solid #A3CFAD` |
| `USAN` | `#E7F0FA` | `#1F5C99` | `1px solid #9DC0E6` |
| ATC code (e.g. `C09AA`) | `#F0EDFA` | `#5A3FA0` | `1px solid #C4B8E8` |
| caveat flag (e.g. `⚠ prodrug`) | `#FFF0E0` | `#8A4200` | `1px solid #EABD82` |

All badges: `font: 600 10.5px IBM Plex Mono`, `padding: 2px 7px`, `border-radius: 4px`.

#### Line 2: Therapeutic Area + Indication

```
Respiratory diseases · Chronic pulmonary insufficiency in patients with Leber…
```

- `IBM Plex Sans 400, 13px, var(--ink-secondary)`
- Therapeutic area in `IBM Plex Sans 500` (slightly heavier) then `·` separator then indication
- Indication truncated with CSS `white-space:nowrap; overflow:hidden; text-overflow:ellipsis`
- `max-width` clipped to prevent overflow into score column

#### Line 3: Sources + Date + Confidence

```
[EMA]  [Health Canada]    Approved 2019-04-12    ◉ High confidence
```

- Source chips: `background:var(--parchment); border:1px solid var(--rule-strong); font:600 10.5px IBM Plex Mono; padding:1px 6px; border-radius:3px; color:var(--ink-secondary)`
- Date: `font: 400 12px IBM Plex Mono; color:var(--ink-tertiary)`
- Confidence: colored dot (`◉`) + label — see confidence encoding below

**Confidence dot encoding:**

| Confidence | Dot color | Label |
|---|---|---|
| High | `#2B7A3D` | "High confidence" |
| Medium | `#B06000` | "Medium — review sources" |
| Low | `#A52828` | "Low — verify manually" |

### 1.3 Score Column

```
┌──────────────┐
│     78       │  ← IBM Plex Mono 600, 22px, color matches tier
│   STRONG     │  ← IBM Plex Mono 600, 9px uppercase, tier color
│ ████████░░   │  ← 10-segment bar, 8px tall, teal filled / ghost empty
└──────────────┘
```

**Score tiers:**

| Range | Tier label | Color |
|-------|-----------|-------|
| 75–100 | STRONG | `var(--score-top)` = #0B5A62 |
| 50–74 | MODERATE | `var(--score-mid)` = #7A5C00 |
| 25–49 | WEAK | `var(--score-low)` = #6B3838 |
| 0–24 | SCREEN OUT | `var(--ink-ghost)` = #9DAAB4 |

**Score bar:** 10 segments, each 7px wide × 8px tall, `border-radius:2px`, `gap:2px`. Filled = `var(--signal)` tinted by tier color. Empty = `rgba(15,26,32,.08)`. This gives a Bloomberg-style sparkline-like visual without needing SVG.

**Score column background:** Same as row (no contrast separation). The left hairline border of the score column is sufficient to group it visually.

### 1.4 Triage Rail (Left 4px)

The leftmost 4px of each row is a solid color strip, implemented as `border-left:4px solid <color>` on the row element:

| State | Color |
|-------|-------|
| Untriaged | `var(--rule-strong)` (neutral gray) |
| Keep | `var(--keep)` = #2B7A3D |
| Investigate | `var(--investigate)` = #B06000 |
| Reject | `var(--reject)` = #A52828 |

The rail is the **only** persistent color encoding of triage state in the row. No background fill changes — that would be too loud for 105 rows. The rail is readable in peripheral vision while reading a different row.

### 1.5 Row Height and Density

Target row height: **66–72px** at default content. This is dense enough to show ~10 rows above the fold at 900px viewport (important — user needs to see the ranked list without scrolling to understand the distribution). Rows with a caveat flag that wraps may grow to ~84px; that is acceptable.

---

## 2. Detail Drawer

### 2.1 Behavior

- **Trigger:** Click anywhere on a row (entire row is clickable; no separate "expand" button).
- **Animation:** Slide in from the right. `transform: translateX(100%) → translateX(0)`, `transition: transform 220ms cubic-bezier(0.22,1,0.36,1)`. The drawer overlays the list; the list does NOT re-flow. An `inset:0` overlay (`background: rgba(15,26,32,.25)`) dims the list behind the drawer. The overlay click dismisses.
- **Dismiss:** Click overlay, click ✕ button (top-right of drawer), or press `Esc`. Keyboard focus traps inside drawer while open.
- **Scroll:** Drawer has its own vertical scroll (`overflow-y:auto`). Page scroll does not propagate.
- **Width:** `min(520px, 92vw)`. On viewports <600px, drawer is full-width with a top drag handle.
- **Z-index stack:** overlay = 100, drawer = 101, focus trap sentinel = 102.
- **ARIA:** `role="dialog"`, `aria-modal="true"`, `aria-labelledby="drawer-drug-name"`. Overlay `aria-hidden="true"`.

### 2.2 Drawer Layout

```
┌─────────────────────────────────────────┐
│ [✕]  BARDOXOLONE METHYL         [KEEP ▼]│  ← Sticky header, 56px
├─────────────────────────────────────────┤
│ ★ ORPHAN   INN   USAN   C09AA           │
│ ─────────────────────────────────────── │
│ PROMISE SCORE                           │
│   78 / 100   STRONG tier                │
│   ████████░░  Breakdown →               │
│   [factor breakdown table]              │
├─────────────────────────────────────────┤
│ WHAT IT TREATS                          │
│ Respiratory Diseases                    │
│                                         │
│ Approved indication (full text):        │
│ "[Full EMA/Health Canada indication     │
│  text, wrapping, up to ~200 words]"     │
├─────────────────────────────────────────┤
│ ATC CLASSIFICATION                      │
│ C09AA · ACE inhibitors                  │
├─────────────────────────────────────────┤
│ REGULATORY DATES                        │
│ EMA approval    2019-04-12              │
│ HC approval     —                       │
├─────────────────────────────────────────┤
│ SOURCES & PROVENANCE                    │
│ EMA (centralised) · High confidence     │
│ UNII CEG1Q6OGU1                         │
│ Match tier: exact-moiety                │
│ [View on EMA]  [PubMed]  [DrugBank]     │
├─────────────────────────────────────────┤
│ CAVEAT FLAGS                            │
│ ⚠ prodrug — verify active moiety in US │
│ ⚠ possible OTC monograph overlap       │
├─────────────────────────────────────────┤
│ TRIAGE NOTE                             │
│ [textarea, placeholder "Add note…"]     │
└─────────────────────────────────────────┘
```

### 2.3 Drawer Header (Sticky)

`position:sticky; top:0; background:var(--parchment-raised); border-bottom:1px solid var(--rule-strong); z-index:10`

- ✕ button: `24×24px`, `font-size:18px`, left-aligned. Focus ring: `outline:2px solid var(--signal); outline-offset:2px`
- Drug name: `IBM Plex Sans 600 17px var(--ink)`, centered or left after ✕
- Triage dropdown: right side — button that opens a small positioned menu with Keep / Investigate / Reject / Clear. Styled like a segment control, not a `<select>`. Background color updates to match triage state when set.

### 2.4 Score Breakdown Table

Below the overall score bar, a compact breakdown table (collapsible by default, expand with "Breakdown ▾"):

| Factor | Weight | Your score | Contribution |
|--------|--------|-----------|-------------|
| Orphan designation | 25% | 100 | +25 |
| INN/USAN status | 15% | 100 | +15 |
| Source count | 15% | 50 | +8 |
| Match tier | 20% | 80 | +16 |
| Abroad approval age | 15% | 67 | +10 |
| Therapeutic area fit | 10% | 40 | +4 |
| **Total** | | | **78** |

Table: `font:400 12px IBM Plex Mono; border-collapse:collapse`. Header row: `background:rgba(15,26,32,.04); font-weight:600`. Each data row: `border-bottom:1px solid var(--rule)`. The Contribution column uses inline colored bars proportional to value.

**Score is analyst-assigned (0–100 integer).** The breakdown table explains the formula but the score field in `summary.json` is the final analyst value. The drawer does not let the user edit the score — it is read-only. The score field is owned by the pipeline.

### 2.5 Section Headings in Drawer

`IBM Plex Mono 600 10px UPPERCASE letter-spacing:.9px color:var(--ink-tertiary) border-bottom:1px solid var(--rule) padding-bottom:5px margin-top:22px margin-bottom:10px`

This creates a consistent "regulatory file" rhythm: labeled sections separated cleanly.

### 2.6 Full Indication Text

Block: `background:rgba(15,26,32,.025); border-left:3px solid var(--rule-strong); padding:10px 14px; font:400 13.5px IBM Plex Sans; line-height:1.6; color:var(--ink-secondary); border-radius:0 4px 4px 0`

Italicize the indication text to signal it is a quoted regulatory statement, not analyst commentary.

### 2.7 External Links

Row of text links (no button style): `font:600 12px IBM Plex Mono; color:var(--signal); text-decoration:underline; text-underline-offset:2px; gap:18px`

Links: "EMA product page", "PubMed", "DrugBank", "FDA UNII". Each opens in `target="_blank" rel="noopener"`.

### 2.8 Caveat Flags

Each flag is a row: `⚠ [flag text]` in `background:var(--investigate-bg); border:1px solid #EABD82; border-radius:4px; padding:6px 10px; font:400 12.5px IBM Plex Sans; color:var(--investigate)`. Stack vertically with `gap:6px`. If no flags, the CAVEAT FLAGS section is hidden entirely.

**Defined caveats (keyed per candidate in summary.json):**

| Key | Display text |
|-----|-------------|
| `prodrug` | "Prodrug — confirm active moiety eligibility before filing" |
| `otc_risk` | "Possible OTC monograph false positive — verify against 21 CFR Part 330" |
| `salt_form` | "Salt/ester form — moiety-base match only; verify no prior NDA on moiety" |
| `withdrawn` | "Withdrawn abroad — regulatory history may impair US filing" |
| `vet_only` | "Veterinary-only source — § 360ff human indication required" |

### 2.9 Triage Note

`<textarea>` full-width, `min-height:72px; resize:vertical; font:400 13px IBM Plex Sans; border:1px solid var(--rule-strong); border-radius:4px; padding:8px 10px; background:var(--parchment)`. On focus: `border-color:var(--signal); outline:none; box-shadow:0 0 0 3px var(--signal-dim)`.

Note auto-saves to `localStorage` on `input` event (debounced 400ms). No explicit save button.

---

## 3. Triage UX

### 3.1 State Model

Each candidate has one triage state: `"keep"`, `"investigate"`, `"reject"`, or `null` (untriaged).  
State stored in `localStorage` under key `rdh_triage_v2` as a JSON object `{ [unii]: { state, note, ts } }`.

UNII is the stable key (not the drug name, which could change across pipeline runs).

### 3.2 Setting Triage State

**In the drawer:** A segmented control in the sticky header with three labeled segments: `KEEP`, `INVESTIGATE`, `REJECT`. Clicking a segment sets that state and updates `localStorage`. Clicking the active segment again sets state back to `null` (clears it). Visual: active segment gets the triage color as background with white text; inactive segments are `background:var(--parchment); color:var(--ink-tertiary)`.

**In the row (right side of row):** A compact `3-icon dot-menu` or three small icon buttons (◆ = keep, ◎ = investigate, ✕ = reject) appears on row hover, to the left of the score column. Clicking one sets state without opening the drawer. This allows fast triage without reading the full drawer. Icons are 14px, colored when active.

Both controls are always in sync — changing one updates the other.

### 3.3 State Visibility in the List

1. **Triage rail** (4px left border — described in §1.4): always visible, all rows.
2. **Faded row opacity:** Rejected rows render at `opacity:0.55` unless the "show rejected" filter is active. This de-emphasizes without hiding, so the user retains spatial context.
3. **Row background tint (subtle):** Kept rows get `background: rgba(43,122,61,.03)` — barely perceptible but reinforces rail.

### 3.4 Triage Progress Summary

A sticky bar at the TOP of the candidate list (below the sort/filter controls, above the first row):

```
Triage progress    ●●●●●●●● ○○○○○○○○○○○○○○○○○○   8 / 105    Keep: 3  ·  Investigate: 2  ·  Reject: 3
```

- `●` = triaged (any state), `○` = untriaged. Render as a 105-segment mini progress bar using a `<div>` with inline `background:linear-gradient` or `clip-path` (not SVG — keep file simple).
- Font: `IBM Plex Mono 400 11px var(--ink-tertiary)`. Keep/Investigate/Reject counts use their respective colors.
- This bar is `position:sticky; top:0; z-index:5; background:var(--parchment); border-bottom:1px solid var(--rule); padding:8px 0`.

### 3.5 Filter: Show Only Kept / Investigate

A filter chip in the controls bar: `★ Kept only` and `? Investigate only`. When active, the list filters to matching rows only and the count label updates.

### 3.6 Export

A small `[Export triage]` text button at the top right of the page. On click, generates a JSON blob (all candidates with their triage states + notes) and triggers a browser download as `rdh_triage_YYYY-MM-DD.json`. Vanilla JS: `URL.createObjectURL(new Blob([json], {type:'application/json'}))`.

### 3.7 Import / Restore

A `[Restore]` link next to Export. Opens a `<input type="file">` picker, reads the JSON, merges it into `localStorage` (existing keys win on conflict unless file is newer per `ts`). This supports team handoff — analyst A can send triage state to analyst B.

---

## 4. Sort + Filter Controls & Overall Page Architecture

### 4.1 Above-the-Fold Layout (1280px desktop)

```
┌──────────────────────────────────────────────────────────────────────┐
│ HEADER (56px)                                                        │
│  Funnel A — PRV-eligible candidate universe          [Export] [?]   │
│  ...subtitle text...                           Generated: 2026-08-07│
├──────────────────────────────────────────────────────────────────────┤
│ HONESTY BAR (48px) — gold left border                               │
│ 105 candidates in screen · ~7 actionable after downstream filters   │
│ Approval deadline: 2029-09-30 · 37 months remaining                 │
├──────────────────────────────────────────────────────────────────────┤
│ STAT CARDS ROW (80px, 4 cards)                                      │
│  [105 Named] [15 Orphan-flagged] [~7 Actionable] [37 mo. remaining]│
├──────────────────────────────────────────────────────────────────────┤
│ FUNNEL (collapsible, default collapsed) — [▶ How the funnel narrows]│
├──────────────────────────────────────────────────────────────────────┤
│ SORT + FILTER CONTROLS (40px)                                        │
│ [Search]  [Sort ▼]  |  [Orphan] [INN] [EMA] [Canada] [Swiss]       │
│           [★ Kept] [? Investigate] [Untriaged]  [↑ count]           │
├──────────────────────────────────────────────────────────────────────┤
│ TRIAGE PROGRESS BAR (28px sticky)                                   │
├──────────────────────────────────────────────────────────────────────┤
│ CANDIDATE ROWS (score-ranked, default sort)                         │
│  ... 105 rows ...                                                    │
└──────────────────────────────────────────────────────────────────────┘
```

**Key above-fold principle:** At 900px viewport height, the user sees the honesty bar, stat cards, controls, progress bar, and the first ~8 ranked candidates before scrolling. The funnel is collapsed by default to not consume vertical real estate.

### 4.2 Header

`background:var(--ink)` (very dark blue-black). Text: `#EAFCFF`. Height: 56px.

- Left: title `IBM Plex Sans 600 20px` + subtitle `IBM Plex Sans 400 12px var(--ink-tertiary) on dark = #8ABDC2`
- Right: `[Export triage]` text button + `[?]` help popover trigger + generated timestamp

**No gradient.** The v1 teal gradient is replaced with a flat dark header — more authoritative, less startup.

### 4.3 Honesty Bar

This is mandatory and must appear immediately below the header, always visible, never collapsible.

`border-left:4px solid #C8990A; background:#FFFBF0; padding:10px 20px; font:400 13px IBM Plex Sans; color:#4A3800`

Text: "**105 candidates** in screening shortlist · **~7 estimated actionable** programs after orphan designation, pediatric-indication fit, and timeline filters · FDA PRV sunset: **2029-09-30** · Window remaining: **37 months**"

Bold the numbers. The tonal register is honest, not alarming. The bar is a standing disclaimer that the dashboard cannot make it disappear.

### 4.4 Stat Cards

Four cards in a row. **Not a grid of big numbers** (that would feel like vanity metrics). Instead: compact horizontal cards, each `height:72px`, `border:1px solid var(--rule-strong)`, `border-radius:6px`, `background:var(--parchment-raised)`.

Each card:
```
┌─────────────────────────┐
│ 105                     │  ← 28px 600 Mono, ink color
│ Named drug candidates   │  ← 11px 400 Sans, ink-tertiary
│ screening shortlist     │
└─────────────────────────┘
```

Card 1: `105` candidates (accent: neutral)  
Card 2: `15` orphan-flagged (accent: gold badge)  
Card 3: `~7` actionable est. (accent: signal teal — the optimistic number, but the `~` tilde must be present)  
Card 4: `37 mo.` to sunset (color: `#A52828` if <24 months remain, `#B06000` if 24–36, neutral otherwise — currently 37 months = neutral/amber)

### 4.5 Sort Controls

**Sort by dropdown** (custom, not `<select>`). Options:

| Label | Field | Default |
|-------|-------|---------|
| Score: High → Low | `score` desc | ✓ Default |
| Score: Low → High | `score` asc | |
| Name: A → Z | `name` asc | |
| Name: Z → A | `name` desc | |
| Abroad date: Newest | `abroad_date` desc | |
| Abroad date: Oldest | `abroad_date` asc | |
| Source count: Most | `source_count` desc | |
| Confidence: Highest | `confidence` desc | |

Sort control: a button `Sort: Score ▼` that opens a positioned list. Styled: `border:1px solid var(--rule-strong); background:var(--parchment-raised); border-radius:4px; padding:6px 12px; font:600 12px IBM Plex Mono`. Dropdown: `position:absolute; z-index:50; background:var(--parchment-raised); border:1px solid var(--rule-strong); border-radius:4px; box-shadow:var(--shadow-card); min-width:220px`.

### 4.6 Filter Chips

Two rows of chips:

**Row 1 — Data filters:**
`[★ Orphan only]` `[INN]` `[EMA]` `[Health Canada]` `[Swissmedic]` `[Japan]`

**Row 2 — Triage filters:**
`[Keep]` `[Investigate]` `[Untriaged]` `[All]` (All is default, others are exclusive-OR with All)

Chip style (off): `background:var(--parchment); border:1px solid var(--rule-strong); border-radius:4px; padding:5px 12px; font:600 11px IBM Plex Mono; color:var(--ink-secondary); cursor:pointer`

Chip style (on): `background:var(--ink); color:#FFF; border-color:var(--ink)`

Exception: triage filter chips when active use their semantic colors (Keep on = `background:var(--keep); color:#FFF`; Investigate on = `background:var(--investigate)...`; etc).

**Search:** `<input>` full-width or `flex:1; min-width:200px`. Placeholder: `"Search drug name or indication…"`. Searches `name`, `moiety`, and `indication` fields. Debounced 200ms. No search icon — label is the placeholder.

### 4.7 Count Label

Right-aligned after chips: `IBM Plex Mono 400 12px var(--ink-tertiary)` — `"Showing 23 of 105 candidates"`. Updates reactively.

### 4.8 Funnel Section

Collapsed by default. Toggle: `<details>/<summary>` element, styled:

Summary: `IBM Plex Mono 600 11px uppercase tracking .8px color:var(--ink-tertiary)` + `▶` rotates to `▼` on open.

When open, the funnel displays as a vertical list of steps with proportional bars (as in v1 but using the new color tokens). Each funnel step:
- Bar width proportional to count (max-width = widest step)
- Color: `var(--signal)` for the active funnel steps, `var(--rule-strong)` for filtered-out counts
- Text: `IBM Plex Mono 400 12px`

### 4.9 Empty State

When filters yield 0 results:

```
No candidates match current filters.
[Clear all filters]
```

Centered, `padding:60px 0`, `font:400 14px IBM Plex Sans; color:var(--ink-ghost)`. Link styled as signal color.

---

## 5. Accessibility Pass

### 5.1 Keyboard Navigation

- **Tab order:** Header controls → Sort → Filter chips → Search → Triage progress → First row. All interactive elements reachable by Tab.
- **Row keyboard activation:** Rows are `<div role="button" tabindex="0">`. `Enter` or `Space` opens the drawer.
- **Drawer Esc:** `document.addEventListener('keydown', e => { if(e.key==='Escape' && drawerOpen) closeDrawer(); })`.
- **Focus trap in drawer:** On drawer open, focus moves to the ✕ button. Tab cycles within the drawer only. On close, focus returns to the row that triggered it.
- **Triage icons in rows:** Each triage icon button has `aria-label="Mark as Keep"` etc.

### 5.2 ARIA Labels

- List container: `role="list" aria-label="PRV candidates, 105 total, sorted by score"`
- Each row: `role="listitem"` (inside the list role); the clickable div within: `role="button" aria-label="Open details for Bardoxolone Methyl" aria-expanded="false"`
- Drawer: `role="dialog" aria-modal="true" aria-labelledby="drawer-title"`
- Sort dropdown: `role="listbox" aria-label="Sort order"`
- Filter chips: `role="checkbox" aria-checked="true/false"`

### 5.3 Color Contrast

All text/background pairs target WCAG AA (4.5:1 minimum for body text, 3:1 for large text and UI components).

Verified pairs (approximate ratios):
- `var(--ink)` #0F1A20 on `var(--parchment)` #F5F2EC: **16.8:1** (AAA)
- `var(--ink-secondary)` #3B4D58 on `var(--parchment)`: **8.1:1** (AAA)
- `var(--ink-tertiary)` #6E7E8A on `var(--parchment)`: **4.7:1** (AA)
- `var(--signal)` #0B6E75 on `var(--parchment)`: **5.1:1** (AA)
- White `#FFFFFF` on `var(--keep)` #2B7A3D: **4.8:1** (AA)
- White on `var(--reject)` #A52828: **5.3:1** (AA)
- White on `var(--investigate)` #B06000: **4.5:1** (AA, verify with actual hex)
- Badge text `#8A5A00` on `#FDF3D7`: **4.6:1** (AA — verify)

All contrast ratios must be re-verified with a tool (e.g. `accessible-contrast` plugin or Colour Contrast Analyser) during implementation.

### 5.4 Motion

`@media (prefers-reduced-motion: reduce)` block must disable:
- Drawer slide transition → instant show/hide
- Score bar animation (if animated on load)
- Any staggered row entrance animations

```css
@media (prefers-reduced-motion: reduce) {
  .drawer { transition: none; }
  .score-bar-fill { animation: none; }
  .row { animation: none; }
}
```

### 5.5 Print Pass

`@media print` block:

```css
@media print {
  header.top { background: #000 !important; print-color-adjust: exact; }
  .drawer-overlay, .drawer { display: none !important; }
  .controls { display: none !important; }
  .triage-progress { display: none !important; }
  .item { break-inside: avoid; border: 1px solid #ccc; margin-bottom: 8px; }
  .score-bar { display: none; } /* bars don't print cleanly */
  .score-number { display: block; } /* show score number */
  a[href]::after { content: none; } /* suppress URL printing */
}
```

Print output: list of all visible (non-filtered) candidates with name, therapeutic area, score number, triage state rail color, and note. One candidate per print block, `break-inside:avoid`.

---

## 6. Data Contract — summary.json Enrichment

The following fields must be added to each `candidates[]` object in `summary.json` for the v2 dashboard. Fields marked † are analyst-supplied (not pipeline-generated); all others are pipeline-generated from EMA/source data.

| Field | Type | Source | Example |
|-------|------|--------|---------|
| `therapeutic_area` | string | EMA/pipeline | `"Respiratory diseases"` |
| `indication` | string | EMA/pipeline | `"Treatment of chronic pulmonary…"` |
| `atc_code` | string | EMA/pipeline | `"R03DC03"` |
| `atc_label` | string | EMA/pipeline | `"leukotriene receptor antagonists"` |
| `abroad_date` | string (ISO) | EMA/pipeline | `"2019-04-12"` |
| `confidence` | string enum | pipeline | `"high"` / `"medium"` / `"low"` |
| `score` | integer 0–100 | †analyst | `78` |
| `score_breakdown` | object | †analyst | `{ orphan:100, inn:100, source:50, ... }` |
| `caveats` | string[] | pipeline | `["prodrug","salt_form"]` |

**Non-EMA candidates** (Health Canada, Swissmedic) will have `therapeutic_area: null`, `indication: null`, `atc_code: null` — the UI must gracefully render these as `"—"` or simply omit those lines. Line 2 of the row collapses if both fields are null.

---

## 7. Component Interaction Map

```
Page load
  → parse summary.json inline
  → restore triage state from localStorage
  → render rows sorted by score desc
  → update triage progress bar

Row click
  → open drawer for that UNII
  → focus drawer ✕ button
  → overlay dims list

Drawer triage segment click
  → update state[unii]
  → update localStorage
  → update row rail color
  → update progress bar
  → re-evaluate filters if "Keep only" is active

Row hover triage icon click
  → same state update path as above
  → drawer not opened

Sort control change
  → re-sort visible array
  → re-render rows (virtual DOM: clear innerHTML, re-append)

Filter chip toggle
  → re-filter candidates array
  → re-render rows
  → update count label

Search input (debounced 200ms)
  → filter by name + indication
  → re-render rows
  → update count label

Export click
  → serialize localStorage triage state + candidate metadata
  → download JSON

Restore click
  → file picker → parse JSON → merge into localStorage → re-render
```

---

## 8. CSS Architecture (single-file constraints)

All CSS in a single `<style>` block. Order:

1. `@import` (Google Fonts — IBM Plex Sans + IBM Plex Mono)
2. `:root` custom properties (all tokens above)
3. Reset (`*, *::before, *::after { box-sizing: border-box }`, body margin 0)
4. Base elements (body, a, button, input, textarea)
5. Layout (`.wrap`, `header`, `.honesty-bar`, `.stat-cards`, `.controls`, `.list`)
6. Row (`.item`, `.triage-rail`, `.row-body`, `.row-score`)
7. Badges (`.badge`, `.badge--orphan`, `.badge--inn`, etc.)
8. Score bar (`.score-bar`, `.score-bar-fill`, `.score-tier`)
9. Drawer (`.drawer-overlay`, `.drawer`, `.drawer-header`, `.drawer-section`)
10. Triage controls (`.triage-segment`, `.triage-icon`)
11. Chips and sort (`.chip`, `.sort-btn`, `.sort-dropdown`)
12. Progress bar (`.triage-progress`)
13. States (`:hover`, `:focus`, `:focus-visible`, `[data-triage=keep]` etc.)
14. `@media (max-width:720px)` responsive
15. `@media (prefers-reduced-motion: reduce)`
16. `@media print`

**No CSS frameworks, no external CSS.** All tokens via CSS custom properties.

---

## 9. JavaScript Architecture (single-file)

All JS in a single `<script>` block at bottom of `<body>`. No modules, no bundler. Structure:

```js
// 1. DATA
const DATA = { /* summary.json embedded here */ };

// 2. STATE
const state = {
  sort: { field: 'score', dir: 'desc' },
  filters: { orphan: false, inn: false, sources: [], triage: null },
  search: '',
  triage: JSON.parse(localStorage.getItem('rdh_triage_v2') || '{}'),
  drawerUnii: null,
};

// 3. PURE HELPERS
function getScore(c) { return c.score ?? 0; }
function getTier(score) { /* returns 'strong'|'moderate'|'weak'|'screen-out' */ }
function getTriageClass(unii) { return state.triage[unii]?.state ?? null; }
function sortCandidates(arr, sort) { /* sort by field/dir */ }
function filterCandidates(arr, filters, search, triage) { /* returns filtered array */ }

// 4. RENDER
function renderRow(c) { /* returns HTMLElement */ }
function renderDrawer(c) { /* returns HTMLElement */ }
function renderProgressBar() { /* updates progress bar */ }
function renderAll() {
  const visible = filterCandidates(sortCandidates(DATA.candidates, state.sort), ...);
  document.getElementById('list').replaceChildren(...visible.map(renderRow));
  document.getElementById('count').textContent = `Showing ${visible.length} of ${DATA.candidates.length}`;
  renderProgressBar();
}

// 5. DRAWER
function openDrawer(unii) { /* set state.drawerUnii, render drawer, show overlay, trap focus */ }
function closeDrawer() { /* clear state.drawerUnii, remove overlay, return focus */ }

// 6. TRIAGE
function setTriage(unii, triageState) {
  if (state.triage[unii]?.state === triageState) {
    delete state.triage[unii]; // toggle off
  } else {
    state.triage[unii] = { state: triageState, note: state.triage[unii]?.note ?? '', ts: Date.now() };
  }
  localStorage.setItem('rdh_triage_v2', JSON.stringify(state.triage));
  renderAll(); // re-render rails + progress
  if (state.drawerUnii === unii) syncDrawerTriageUI(); // update drawer without closing
}

function setNote(unii, text) { /* debounced, update localStorage */ }

// 7. EXPORT / IMPORT
function exportTriage() { /* download JSON */ }
function importTriage(file) { /* parse and merge */ }

// 8. EVENTS
// Sort, filter chips, search, row click, drawer dismiss, Esc, overlay click, triage icons

// 9. INIT
renderAll();
```

**Performance note:** With 105 rows, `replaceChildren` on every filter/sort is acceptable (no virtualization needed). Each `renderRow` call is pure — no side effects, just DOM creation.

---

## 10. Spacing Scale

Base unit: **4px**.

| Token (conceptual) | Value | Use |
|--------------------|-------|-----|
| micro | 4px | Gap between badges |
| small | 8px | Padding within compact elements |
| component | 12–14px | Row padding vertical |
| section | 20px | Between sections in drawer |
| major | 32px | Between page sections |
| page-gutter | 22px | `.wrap` horizontal padding |

`max-width: 1120px` for `.wrap` — slightly wider than v1 (1080px) to accommodate the score column cleanly.

---

## 11. Responsive Breakpoints

| Breakpoint | Changes |
|------------|---------|
| `≤ 900px` | Stat cards: 2×2 grid. Sort + filter chips: wrap to 2 rows |
| `≤ 720px` | Stat cards: 2×2. Score column: hide bar, show number only. Badge truncation |
| `≤ 600px` | Drawer: full-width, slides up from bottom. Row score column: moves below row body |
| `≤ 480px` | Header title: single line, subtitle hidden |

---

## 12. Version Diff from v1

| v1 | v2 |
|----|-----|
| Card grid layout per candidate | Full-width row list (filing-manifest register) |
| Teal gradient header | Flat dark header `var(--ink)` |
| No therapeutic area / indication | Line 2 of row: area · indication |
| No score | Score column: number + tier + 10-segment bar |
| No detail drawer | Slide-in detail drawer with full provenance |
| No triage state | Keep / Investigate / Reject with 4px rail, localStorage |
| No triage progress | Sticky 105-segment progress bar |
| Basic chips (orphan/INN/source) | Enriched badges including ATC + caveat flags |
| No export/import | Triage JSON export + import/restore |
| Funnel always visible | Funnel collapsible (collapsed by default) |
| Inter/system font | IBM Plex Sans + IBM Plex Mono superfamily |
| White/card shadow aesthetic | Parchment ground, hairline borders, no card shadows |
| No honesty bar | Permanent honesty bar: 105 shortlist, ~7 actionable |

---

*End of specification. An engineer should be able to build directly from this document without further design input. All hex values, px sizes, and behavioral descriptions are implementation-complete.*
