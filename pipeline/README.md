# Funnel A candidate-discovery pipeline

Runnable implementation of `sources/00-CANDIDATE-DISCOVERY-METHOD.md`. It
enumerates the **PRV-eligible candidate universe** — active substances approved
by a foreign regulator whose active moiety has **never been approved in the US**
(population A1). Under 21 U.S.C. § 360ff that is the only route to a
transferable Priority Review Voucher for a repurposed molecule.

```
LEFT  (foreign approvals)   EMA centralised · Health Canada DPD · Swissmedic · PMDA(partial)
RIGHT (US exclusion set)    Drugs@FDA Products.txt  +  Orange Book products.txt
JOIN                        FDA UNII, canonicalized to active-MOIETY UNII
DIFF                        LEFT − RIGHT
FILTER                      drop biologics/vaccines; split named-drug vs excipient noise
```

## Run it

```bash
pip install --break-system-packages openpyxl      # only third-party dep
python3 pipeline/rdh_diff.py
```

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
   so a monograph-only moiety (e.g. aspirin) can appear as a false candidate.
   This intersects the *Sun Pharma* A2 population, so treat as "investigate".
2. **Prodrugs still leak** — an active moiety US-approved under a different
   parent (isavuconazole vs US isavuconazonium) needs the GSRS active-moiety
   graph, not implemented.
3. **EMA is centralised-only**; nationally-authorised EU drugs are absent.
4. **Japan is under-covered** — only PMDA FY2025 loads and katakana names mostly
   fail to resolve without a transliteration layer. This is the highest-yield
   source, so the JP→UNII transliteration layer is the top next build.
5. This diff does **not** apply the § 360ff(a)(3) rare-pediatric gate, freedom
   to operate, or the orphan-exclusivity conflict check. It produces the
   screening list those downstream filters consume.

## Files
- `unii.py` — UNII index, normalization, salt→moiety canonicalization
- `sources.py` — loaders for each regulator + the US exclusion set
- `rdh_diff.py` — the pipeline entry point
