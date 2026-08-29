# Funnel A candidate-discovery pipeline

Runnable implementation of `sources/00-CANDIDATE-DISCOVERY-METHOD.md`. It
enumerates the **PRV-eligible candidate universe** — active substances approved
by a foreign regulator whose active moiety has **never been approved in the US**
(population A1). Under 21 U.S.C. § 360ff that is the only route to a
transferable Priority Review Voucher for a repurposed molecule.

```
LEFT  (foreign approvals)   EMA centralised · Health Canada DPD · Swissmedic · PMDA(partial)
RIGHT (US exclusion set)    Drugs@FDA Products.txt  +  Orange Book products.txt
JOIN                        three layers, each measured against labeled cases:
                              1. UNII overlap across EVERY key variant (salt, base,
                                 spelling, INN-acid/USAN-ate) — moiety.py keys()
                              2. string-key overlap as backstop
                              3. GSRS relationship graph, 2 hops (prodrug / salt-parent /
                                 active-moiety; counterion edges are walls) — gsrs.py
DIFF                        LEFT − RIGHT, three-state: in_us / candidate / REVIEW
FILTER                      drop biologics/vaccines; split named-drug vs excipient noise
```

**The matcher is measured, not asserted.** `python3 pipeline/test_accuracy.py`
replays labeled known-answer drugs through the string layer (offline, seconds);
`--real` replays them through the exact production path against the real data
files. The hand-listed matcher this replaced silently passed 12/19 labeled
US-approved drugs (lapatinib, sunitinib, ibandronic acid, isavuconazole, ...);
the current one catches 19/19 with 19/19 true candidates retained. Run it
before and after any matcher change.

## Run it

```bash
python3 -m pip install --break-system-packages openpyxl   # only third-party dep
python3 pipeline/fetch.py       # (optional) refresh source files from live URLs
python3 pipeline/rdh_diff.py    # run the diff -> summary.json + CSVs
python3 pipeline/enrich.py      # (optional) add live PubMed/trials + competitor monitor
python3 pipeline/build_ui.py    # generate the dashboard
open pipeline/ui/index.html
```

## Live data

The dashboard is a static file, but it can be rebuilt from current data — "live"
happens at the build step, not in the browser (keeps it offline-safe & shareable).

- **`fetch.py`** — re-downloads the source bulk files from their live URLs (EMA
  publishes nightly; Drugs@FDA weekly; Orange Book, Canada, Swissmedic, UNII on
  their own cadences). Atomic + validated: a dead URL keeps the last good copy.
  `python3 pipeline/fetch.py ema fda` refreshes only named sources.
- **`enrich.py`** — at build time, adds real-world signal per candidate and a
  global competitor monitor, then embeds it. Cached in `data/cache/` (re-runs are
  instant), rate-limited, and fail-safe (a flaky API degrades to "—", never breaks
  the build):
  - **PubMed** hits in a rare/paediatric context (evidence signal)
  - **ClinicalTrials.gov v2** trial count (is anyone already developing it?)
  - **Federal Register** live PRV ledger + **SEC EDGAR** recent RPD-designation
    filers — the competitor early-warning channel (FDA publishes no RPD list)
  - US orphan designation is deliberately **not** asserted — FDA OOPD blocks
    automation, so it's surfaced as a manual-check, never a false "clear".

To refresh everything: `fetch.py` → `rdh_diff.py` → `enrich.py` → `build_ui.py`.

## The dashboard has two views

1. **Open & eligible** (top, plain-language) — the drugs that qualify for the
   voucher program *and* look freely available, with an off-patent-by-age read and
   an explicit warning that old candidates are exactly where "never US-approved"
   and freedom-to-operate are least certain. This is the "just show me what's
   available" view.
2. **Full analyst view** — all 105, promise-scored, filterable, with the detail
   drawer, triage state, and competitor monitor.

Outputs (written to `pipeline/data/out/`, ~7s runtime):
- `funnelA_candidates.csv` — named-drug (INN/USAN) never-US candidates, the headline list
- `funnelA_unnamed_excipients.csv` — never-US substances lacking an INN/USAN (excipients, antiseptics, sunscreen filters, reagents, vet-only) — kept for completeness, not repurposing candidates
- `funnel_report.md` — the funnel counts, top orphan candidates, and caveats
- `summary.json` — machine-readable version of all of the above (feeds the dashboard)

## The dashboard (what to actually look at)

Don't read the CSVs by hand. Generate and open the visual dashboard:

```bash
python3 pipeline/build_ui.py          # writes pipeline/ui/index.html
open pipeline/ui/index.html           # double-click also works — no server needed
```

It shows the headline numbers, a visual funnel, and every candidate as a card
with orphan/INN/USAN badges, source tags, and one-click lookup links (EMA,
PubMed, FDA GSRS). Search and filter chips ("Orphan only", by regulator). The
data is embedded in the file, so it works offline and is safe to share as a
single `index.html`. Re-run `rdh_diff.py` then `build_ui.py` to refresh it.

## Data

`pipeline/data/raw/` holds the inputs (~150 MB) and is git-ignored. The files
were already downloaded to the session scratchpad during research; the loaders
read them from `raw/`. To refresh from source, the verified URLs are in
`sources/00-CANDIDATE-DISCOVERY-METHOD.md` §1–2 and
`sources/_recovered/MINED-drug-data-sources.md`. Snapshot used:
UNII 26 Feb 2026 · Drugs@FDA 4 Aug 2026 · Orange Book Jul 2026 · EMA 5 Aug 2026.

## Why the join is the hard part

§ 360ff turns on active **moiety**, not active ingredient. `unii.py` therefore
canonicalizes every name — foreign and US — to a moiety UNII, which collapses
BOTH salt form AND synonym system. Worked example: US `MECHLORETHAMINE
HYDROCHLORIDE` (salt, USAN name) and EU `chlormethine` (base, INN name) both map
to UNII `50D9XSG0VR`, so the EU drug is correctly recognised as already
US-approved rather than surfacing as a false candidate. The measured EMA→UNII
match rate this relies on is 94.6% (see the method doc); the residual is
dominated by vaccines and complex biologics, which are not repurposing targets.

## Known limitations (also printed in every run's report)

1. **US exclusion set is NDA-based** — no OTC-monograph / pre-1938 / DESI drugs,
   so a monograph-only moiety (e.g. aspirin, sunscreen filters) can appear as a
   false candidate. This intersects the *Sun Pharma* A2 population, so treat as
   "investigate".
2. **Prodrug/conjugate exclusion runs via the live GSRS graph** (`gsrs.py`,
   cached in `data/cache/gsrs.json`) and catches the isavuconazole class, the
   edotreotide radiolabel class, and synonym islands (methylene blue). It is
   only as complete as GSRS's edges — a missing edge is a missing exclusion, so
   prodrug-looking candidate names still deserve a manual glance. If GSRS is
   unreachable for a row, that row lands in `funnelA_review.csv`, never in the
   candidate list.
3. **EMA is centralised-only**; nationally-authorised EU drugs are absent.
4. **Japan is under-covered** — only PMDA FY2025 loads and katakana names mostly
   fail to resolve without a transliteration layer. This is the highest-yield
   source, so the JP→UNII transliteration layer is the top next build.
5. This diff does **not** apply the § 360ff(a)(3) rare-pediatric gate, freedom
   to operate, or the orphan-exclusivity conflict check. `eligibility.py` walks
   all ten statutory criteria per candidate and labels which a machine settled,
   which a dataset could settle, and which need a human — it never returns
   "eligible", only "nothing has ruled it out yet".

## Files
- `moiety.py` — hardened string layer: generated salt vocabulary (multiplier ×
  counterion × spelling), INN-acid/USAN-ate bridge, ester-prodrug suffixes,
  key-SET matching, counterion walls; plus the standalone `StringExclusionSet`
- `unii.py` — UNII index; `collect()` gathers every UNII + key variant a name
  can resolve to (membership is tested on the full set, both sides)
- `gsrs.py` — live FDA GSRS relationship client (prodrug / salt-parent /
  active-moiety edges, two hops, counterion-walled), disk-cached
- `sources.py` — loaders for each regulator + the US exclusion set
- `rdh_diff.py` — the pipeline entry point (three-state verdicts)
- `eligibility.py` — the ten § 360ff criteria, labeled by decidability
- `test_accuracy.py` — labeled known-answer harness (offline + `--real`)
