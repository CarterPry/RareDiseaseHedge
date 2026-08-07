#!/usr/bin/env python3
"""
RareDiseaseHedge — candidate-discovery diff (Funnel A enumeration).

Implements sources/00-CANDIDATE-DISCOVERY-METHOD.md end to end:

  LEFT  = active substances approved by foreign regulators (EMA, Canada,
          Swissmedic; PMDA best-effort)
  RIGHT = every active moiety ever approved in the US (Drugs@FDA + Orange Book)
  DIFF  = LEFT minus RIGHT, resolved through FDA UNII with salt->moiety collapse
  FILTER= drop biologics/vaccines/unresolved; keep small molecules; flag orphan

The output is the PRV-eligible **Funnel A candidate universe** (population A1:
approved abroad, never approved in the US). It is a screening list, not a
clearance: § 360ff also requires a 505(b)(1) filing, published rare-pediatric
evidence, freedom to operate, and no prior orphan exclusivity — those are
downstream filters this diff feeds, not ones it applies.

Run:  python3 pipeline/rdh_diff.py
Deps: openpyxl (pip install --break-system-packages openpyxl); rest is stdlib.
"""
from __future__ import annotations
import csv, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from unii import UniiIndex  # noqa: E402
import sources  # noqa: E402

RAW = os.path.join(HERE, "data", "raw")
OUT = os.path.join(HERE, "data", "out")


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def main():
    os.makedirs(OUT, exist_ok=True)
    t0 = time.time()

    # 1) Build the UNII join index -----------------------------------------
    idx = UniiIndex()
    log("loading UNII name index (77MB, ~1M synonyms)...")
    n_names = idx.load_names(os.path.join(RAW, "UNII_Names_26Feb2026.txt"))
    log(f"  {n_names:,} synonym rows -> {len(idx.name2unii):,} normalized names")
    log("loading UNII records...")
    n_rec = idx.load_records(os.path.join(RAW, "UNII_Records_26Feb2026.txt"))
    log(f"  {n_rec:,} UNII records")

    # 2) RIGHT side: US exclusion set --------------------------------------
    log("building US exclusion set (Drugs@FDA + Orange Book)...")
    us_uniis, us_moieties, us_stats = sources.load_us_exclusion(idx, RAW)
    log(f"  {us_stats['ingredient_rows']:,} ingredient rows -> "
        f"{len(us_uniis):,} US moiety-UNIIs, {len(us_moieties):,} US moiety keys "
        f"({us_stats['unmatched']:,} name rows unresolved to UNII)")

    # 3) LEFT side: foreign approvals --------------------------------------
    foreign = []
    for name, fn in [("EMA", sources.load_ema), ("Canada", sources.load_canada),
                     ("Swissmedic", sources.load_swissmedic), ("PMDA", sources.load_pmda)]:
        recs = fn(RAW)
        log(f"loaded {len(recs):,} substance rows from {name}")
        foreign.extend(recs)

    # 4) Resolve + anti-join -----------------------------------------------
    # Collapse foreign rows to unique moiety, tracking which regulators and
    # whether any source flagged it orphan.
    log("resolving foreign substances and running anti-join...")
    by_moiety: dict[str, dict] = {}
    funnel = {"foreign_rows": len(foreign), "resolved": 0, "unmatched": 0,
              "biologic_or_mixture": 0, "in_us": 0, "candidate_small_mol": 0,
              "needs_translit_unmatched": 0}

    for rec in foreign:
        cu, mk, tier = idx.moiety_unii(rec["substance"])
        if cu:
            funnel["resolved"] += 1
        else:
            funnel["unmatched"] += 1
            if rec.get("needs_translit"):
                funnel["needs_translit_unmatched"] += 1
            # unresolved names cannot be diffed reliably; skip from candidates
            continue

        # canonical moiety UNII on both sides -> collapses salt/base and synonyms
        in_us = (cu in us_uniis) or (mk and mk in us_moieties)
        biologic = idx.is_biologic(cu)

        entry = by_moiety.setdefault(cu, {
            "unii": cu, "moiety_key": mk, "display": idx.unii2display.get(cu, ""),
            "inn": idx.unii2inn.get(cu, False), "usan": idx.unii2usan.get(cu, False),
            "subtype": idx.unii2type.get(cu, ""),
            "sources": set(), "orphan": False, "match_tier": tier,
            "in_us": in_us, "biologic": biologic, "examples": set(),
        })
        entry["sources"].add(rec["source"])
        entry["orphan"] = entry["orphan"] or rec["orphan"]
        entry["examples"].add(rec["substance"][:60])

    # 5) Classify ----------------------------------------------------------
    # A genuine 505(b)(1) repurposing candidate is a named drug substance (has an
    # INN or a USAN). Substances with neither are overwhelmingly excipients,
    # antiseptics, sunscreen filters, reagents and veterinary-only actives — real
    # foreign approvals, but not drug-repurposing candidates. Keep them, but in a
    # separate bucket so the headline number is meaningful.
    named, unnamed = [], []
    for e in by_moiety.values():
        if e["in_us"]:
            funnel["in_us"] += 1
            continue
        if e["biologic"]:
            funnel["biologic_or_mixture"] += 1
            continue
        funnel["candidate_small_mol"] += 1
        (named if (e["inn"] or e["usan"]) else unnamed).append(e)
    funnel["named_drug"] = len(named)
    funnel["unnamed"] = len(unnamed)

    sort_key = lambda e: (not e["orphan"], not (len(e["sources"]) > 1),
                          e["display"] or e["moiety_key"])
    named.sort(key=sort_key)
    unnamed.sort(key=sort_key)

    # 6) Write candidate CSVs ----------------------------------------------
    def write_csv(path, rows):
        with open(path, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["unii", "preferred_name", "moiety_key", "is_INN", "is_USAN",
                        "substance_type", "foreign_sources", "n_sources",
                        "orphan_flag", "match_tier", "example_source_names"])
            for e in rows:
                w.writerow([e["unii"], e["display"], e["moiety_key"],
                            "Y" if e["inn"] else "N", "Y" if e["usan"] else "N",
                            e["subtype"], "|".join(sorted(e["sources"])),
                            len(e["sources"]), "Y" if e["orphan"] else "N",
                            e["match_tier"], " ; ".join(sorted(e["examples"])[:3])])

    csv_path = os.path.join(OUT, "funnelA_candidates.csv")
    write_csv(csv_path, named)
    write_csv(os.path.join(OUT, "funnelA_unnamed_excipients.csv"), unnamed)
    candidates = named  # headline set

    # 7) Write funnel report ------------------------------------------------
    orphan_n = sum(1 for e in candidates if e["orphan"])
    inn_n = sum(1 for e in candidates if e["inn"])
    multi_n = sum(1 for e in candidates if len(e["sources"]) > 1)
    rep_path = os.path.join(OUT, "funnel_report.md")
    with open(rep_path, "w", encoding="utf-8") as fh:
        fh.write(_report_md(funnel, us_stats, candidates, orphan_n, inn_n, multi_n,
                            time.time() - t0))

    log(f"DONE in {time.time()-t0:.1f}s")
    log(f"  candidates (small-molecule, never-US): {len(candidates):,}")
    log(f"  of which orphan-flagged: {orphan_n:,}")
    log(f"  -> {csv_path}")
    log(f"  -> {rep_path}")


def _report_md(f, us, cands, orphan_n, inn_n, multi_n, secs):
    lines = []
    A = lines.append
    A("# Funnel A candidate-discovery run\n")
    A(f"_Generated by `pipeline/rdh_diff.py` in {secs:.0f}s. Data snapshot 2026-08 "
      "(UNII 26Feb2026, Drugs@FDA 04Aug2026, Orange Book Jul2026, EMA 05Aug2026)._\n")
    A("**What this is:** active substances approved by a foreign regulator whose "
      "active moiety is absent from the entire US approval record — i.e. the "
      "population A1 (never approved in the US) that § 360ff makes PRV-eligible. "
      "This is a *screening list*, not a clearance; downstream filters "
      "(505(b)(1) fileability, rare-pediatric evidence, FTO, orphan-exclusivity "
      "conflict) still apply.\n")
    A("## Funnel\n")
    A("| Stage | Count |")
    A("|---|---|")
    A(f"| Foreign substance rows ingested | {f['foreign_rows']:,} |")
    A(f"| Resolved to a UNII | {f['resolved']:,} |")
    A(f"| Unresolved (mostly PMDA katakana — needs transliteration) | {f['unmatched']:,} |")
    A(f"| — of which PMDA/Japanese | {f['needs_translit_unmatched']:,} |")
    A(f"| Unique moieties, resolved | {len(cands)+f['in_us']+f['biologic_or_mixture']:,} |")
    A(f"| Dropped — moiety already approved in US | {f['in_us']:,} |")
    A(f"| Dropped — biologic/vaccine/mixture (not a repurposing candidate) | {f['biologic_or_mixture']:,} |")
    A(f"| Small-molecule, never-US | {f['candidate_small_mol']:,} |")
    A(f"| — unnamed (excipient/antiseptic/reagent/vet — appendix CSV) | {f.get('unnamed',0):,} |")
    A(f"| **Funnel A candidates — named drug (INN or USAN)** | **{f.get('named_drug',0):,}** |")
    A(f"| — INN-designated | {inn_n:,} |")
    A(f"| — flagged orphan by a foreign regulator | {orphan_n:,} |")
    A(f"| — approved in >1 foreign regulator | {multi_n:,} |\n")
    A("## US exclusion set\n")
    A(f"- {us['ingredient_rows']:,} active-ingredient rows from Drugs@FDA + Orange Book\n")
    A("## How to read this\n")
    A("The **orphan-flagged, multi-regulator, INN** candidates are the highest-value "
      "rows: an INN exists (mature molecule), more than one stringent regulator "
      "approved it (real drug, real dossier), and at least one called it orphan "
      "(already in rare-disease territory). Start manual review there.\n")
    A("### Top orphan-flagged candidates\n")
    A("| UNII | Name | Foreign sources | INN |")
    A("|---|---|---|---|")
    for e in [c for c in cands if c["orphan"]][:40]:
        A(f"| {e['unii']} | {e['display']} | {'|'.join(sorted(e['sources']))} | "
          f"{'Y' if e['inn'] else 'N'} |")
    A("\n### Known residual error classes (do not skip)\n")
    A("- **US exclusion set is NDA-based.** Drugs@FDA + Orange Book do NOT include "
      "OTC-monograph, pre-1938, or DESI-withdrawn drugs. So a moiety marketed in "
      "the US only under an OTC monograph (e.g. aspirin) can still surface as a "
      "false candidate. This is the § 2 completeness gap in the method doc. It "
      "also intersects the *Sun Pharma* A2 population, so treat these as "
      "'investigate', not 'discard'.\n")
    A("- **Prodrugs still leak.** Salt/base collapse is handled via moiety-UNII, "
      "but a prodrug whose active moiety is US-approved under a different parent "
      "(e.g. isavuconazole vs US-approved isavuconazonium) is not caught without "
      "the GSRS active-moiety graph. A minority of rows; flag prodrug/ester names "
      "in manual review.\n")
    A("- **EMA is centralised-only.** Nationally-authorised EU drugs are absent, "
      "so some 'never-US' calls may actually be approved via an EU member state.\n")
    A("- **Japan is under-covered.** Only PMDA FY2025 (~140 rows) is loaded and "
      "katakana names mostly fail to resolve without a transliteration layer. The "
      "true Funnel A pool is larger and concentrated in exactly this highest-yield "
      "source — building the JP→UNII transliteration layer is the top next step.\n")
    A("- This diff does NOT test the § 360ff(a)(3) rare-pediatric gate, FTO, or "
      "existing orphan exclusivity. It narrows thousands of approvals to a "
      "hand-reviewable list; the human work starts here.\n")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
