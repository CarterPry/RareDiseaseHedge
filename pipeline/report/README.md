# State of Bio 2026 — the almanac report

A magazine-style, D3-driven presentation of the RareDiseaseHedge "Funnel A"
model. The visual design (hero scroll-dissolve, ticker, tabbed stacked bars,
bubbles, sunburst, marimekko, world map) is adapted from a data-almanac
template; the content is this project's rare-disease Priority Review Voucher
thesis.

Open `index.html` in a browser (it uses D3 from a CDN, so needs a connection for
the charts and the world map). Nothing to build for viewing — but the data is
generated.

## What's real vs. illustrative

Every chart carries a source pill that says which it is.

**Real (driven by `data.js`, generated from the pipeline):**
- **Ticker** — headline counts from `data/out/summary.json` (candidates,
  multi-regulator, orphan, months to sunset, …).
- **The Voucher Market** — annual PRV sale value, stacked by voucher type, from
  the SEC-8-K transaction table in `sources/18-prv-transaction-market.md`.
- **Candidates by Reach / Candidates** (bars + bubbles) — the 342 never-US
  candidates, sized by how many EEA countries authorise each (EMA Article 57).
- **Where They're Approved** — per-country candidate counts on a Europe-centred
  map.

**Illustrative (seeded synthetic, for the design only):**
- **Disease Areas** (sunburst) and **Modalities** (marimekko) — shaped to the
  layout, not pipeline output, because per-candidate area/class data is sparse in
  the source registers. Labelled "Illustrative" on the chart.

## Regenerating the data

```
python3 pipeline/report/build_report_data.py     # rewrites data.js from summary.json + the PRV table
```

Run this after `rdh_diff.py` produces a new `summary.json`. The chart code
(`app.js`) and design (`style.css`) do not need regenerating.
