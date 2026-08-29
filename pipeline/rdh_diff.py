#!/usr/bin/env python3
"""
RareDiseaseHedge — candidate-discovery diff (Funnel A enumeration).

Implements sources/00-CANDIDATE-DISCOVERY-METHOD.md end to end:

  LEFT  = active substances approved by foreign regulators (EMA, Canada,
          Swissmedic; PMDA best-effort)
  RIGHT = every active moiety ever approved in the US (Drugs@FDA + Orange Book)
  DIFF  = LEFT minus RIGHT, three layers deep:
            1. UNII overlap across every key variant (salt, base, spelling,
               acid/-ate) — moiety.py + UniiIndex.collect
            2. string-key overlap as backstop where UNII resolution is partial
            3. GSRS relationship graph (prodrug / salt-parent / active-moiety,
               two hops) for what no string can see — gsrs.py, cached
  FILTER= drop biologics/vaccines/unresolved; keep small molecules; flag orphan

Verdicts are three-state: in_us / candidate / REVIEW. A row lands in REVIEW when
the answer depends on data the run could not get (GSRS unreachable) or on a call
the statute leaves open (enantiomer of a US-approved racemate) — it is surfaced
in its own CSV, never silently kept or dropped.

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
from unii import UniiIndex, has_stereo_marker  # noqa: E402
from moiety import full_keys  # noqa: E402
from gsrs import GsrsClient  # noqa: E402
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
    # whether any source flagged it orphan. Membership is tested on the FULL
    # variant collection (all UNIIs + all key forms, both sides) — the single
    # canonical-key comparison this replaces measured 12/19 silent misses on
    # labeled US-approved drugs (see test_accuracy.py).
    log("resolving foreign substances and running anti-join...")
    by_moiety: dict[str, dict] = {}
    funnel = {"foreign_rows": len(foreign), "resolved": 0, "unmatched": 0,
              "biologic_or_mixture": 0, "in_us": 0, "in_us_string": 0,
              "in_us_gsrs": 0, "review": 0, "candidate_small_mol": 0,
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

        # every variant of the foreign name vs every variant the US ever approved
        f_uniis, f_keys = idx.collect(rec["substance"])
        hit_u = f_uniis & us_uniis
        hit_k = f_keys & us_moieties if not hit_u else set()
        in_us = bool(hit_u or hit_k)
        basis = (f"unii:{sorted(hit_u)[0]}" if hit_u
                 else f"key:{sorted(hit_k, key=len)[0]}" if hit_k else "")
        biologic = idx.is_biologic(cu)

        entry = by_moiety.setdefault(cu, {
            "unii": cu, "moiety_key": mk, "display": idx.unii2display.get(cu, ""),
            "inn": idx.unii2inn.get(cu, False), "usan": idx.unii2usan.get(cu, False),
            "subtype": idx.unii2type.get(cu, ""),
            "sources": set(), "orphan": False, "match_tier": tier,
            "in_us": in_us, "biologic": biologic, "examples": set(),
            "area": "", "atc": "", "indication": "", "approved": "",
            "flags": [], "excluded_by": basis, "verdict": "",
        })
        entry["sources"].add(rec["source"])
        entry["orphan"] = entry["orphan"] or rec["orphan"]
        entry["examples"].add(rec["substance"][:60])
        entry["in_us"] = entry["in_us"] or in_us
        if basis and not entry["excluded_by"]:
            entry["excluded_by"] = basis
        # keep the first non-empty enrichment (EMA carries these)
        for f in ("area", "atc", "indication", "approved"):
            if not entry[f] and rec.get(f):
                entry[f] = rec[f]

    # 4b) GSRS relationship sweep ------------------------------------------
    # What no string can see: prodrug pairs (isavuconazonium -> isavuconazole),
    # radiolabel conjugates (Ga-68 edotreotide -> edotreotide), synonym-system
    # islands (methylene blue vs methylthioninium). For each surviving small
    # molecule, walk the FDA's own substance-relationship graph two hops along
    # exclusion-grade edges (ACTIVE MOIETY / PRODRUG<->METABOLITE ACTIVE /
    # SALT|SOLVATE<->PARENT) and test every relative against the US record.
    # Enantiomer/racemate edges to a US-approved counterpart -> REVIEW (the
    # statute does not settle that case). GSRS unreachable -> REVIEW, never a
    # silent keep. Results are cached in data/cache/gsrs.json.
    survivors = [e for e in by_moiety.values() if not e["in_us"] and not e["biologic"]]
    log(f"GSRS relationship sweep over {len(survivors)} surviving moieties "
        f"(cached; first run makes ~2 API calls each)...")
    g = GsrsClient()

    def rel_hit(u, nm):
        """Is this GSRS relative in the US approval record?

        Matched on the relative's FULL identity only (its UNII, its unstripped
        name forms) — never on its salt-stripped moiety. A relative that is a
        salt of the candidate is 'candidate + counterion'; stripping it can
        expose the OTHER component and join two unrelated drugs (salicylic
        acid -> colchicine salicylate -> 'COLCHICINE' -> excluded, wrongly)."""
        if u in us_uniis:
            return f"gsrs-unii:{u}"
        for k in full_keys(nm):
            ru = idx.name2unii.get(k) or idx.moiety2unii.get(k)
            if ru and ru in us_uniis:
                return f"gsrs-unii:{ru}"
            if k in us_moieties:
                return f"gsrs-key:{k}"
        return ""

    wall = idx.is_counterion  # synonym-robust counterion wall for the traversal
    for n_done, e in enumerate(survivors, 1):
        res = g.relatives(e["unii"], wall=wall)
        if not res["ok"]:
            e["verdict"] = "review"
            e["flags"].append("GSRS_UNAVAILABLE: relationship graph could not be "
                              "fetched; prodrug/conjugate exclusion untested")
            continue
        hop2_queue = []
        for grade_, rtype, ru, rname in res["relatives"]:
            if grade_ == "exclude":
                basis = rel_hit(ru, rname)
                if basis:
                    e["in_us"] = True
                    e["excluded_by"] = basis
                    e["flags"].append(f"GSRS {rtype} -> {rname}")
                    break
                hop2_queue.append((ru, rname))
            elif grade_ == "review":
                basis = rel_hit(ru, rname)
                if basis:
                    e["verdict"] = "review"
                    e["flags"].append(f"STEREO_US_RELATIVE: {rtype} -> {rname} "
                                      f"is US-approved ({basis}); s.529 treatment "
                                      f"of enantiomer/racemate pairs is unsettled")
        if not e["in_us"]:
            # second hop: base -> its own salts/prodrugs -> the US spelling
            # (methylthioninium -> methylene blue cation -> methylene blue)
            for ru, rname in hop2_queue[:8]:
                r2 = g.relatives(ru, wall=wall)
                for grade_, rtype, ru2, rname2 in r2["relatives"]:
                    if grade_ != "exclude" or ru2 == e["unii"]:
                        continue
                    basis = rel_hit(ru2, rname2)
                    if basis:
                        e["in_us"] = True
                        e["excluded_by"] = basis
                        e["flags"].append(f"GSRS 2-hop via {rname}: {rtype} -> {rname2}")
                        break
                if e["in_us"]:
                    break
        if e["in_us"]:
            funnel["in_us_gsrs"] += 1
        elif e["verdict"] != "review" and has_stereo_marker(e["display"] or e["moiety_key"]):
            # caveat only — no US counterpart found, but a human should look
            e["flags"].append("STEREO_NAME: name carries an enantiomer/racemate "
                              "marker; check the counterpart's US status by hand")
        if n_done % 50 == 0:
            log(f"  ...{n_done}/{len(survivors)}")
            g.save()
    g.save()

    # 5) Classify ----------------------------------------------------------
    # A genuine 505(b)(1) repurposing candidate is a named drug substance (has an
    # INN or a USAN). Substances with neither are overwhelmingly excipients,
    # antiseptics, sunscreen filters, reagents and veterinary-only actives — real
    # foreign approvals, but not drug-repurposing candidates. Keep them, but in a
    # separate bucket so the headline number is meaningful. REVIEW rows go to
    # their own bucket regardless of naming — they are open questions, not
    # candidates.
    named, unnamed, review = [], [], []
    for e in by_moiety.values():
        if e["in_us"]:
            funnel["in_us"] += 1
            continue
        if e["biologic"]:
            funnel["biologic_or_mixture"] += 1
            continue
        if e["verdict"] == "review":
            funnel["review"] += 1
            review.append(e)
            continue
        funnel["candidate_small_mol"] += 1
        (named if (e["inn"] or e["usan"]) else unnamed).append(e)
    funnel["in_us_string"] = funnel["in_us"] - funnel["in_us_gsrs"]
    funnel["named_drug"] = len(named)
    funnel["unnamed"] = len(unnamed)

    sort_key = lambda e: (not e["orphan"], not (len(e["sources"]) > 1),
                          e["display"] or e["moiety_key"])
    named.sort(key=sort_key)
    unnamed.sort(key=sort_key)
    review.sort(key=sort_key)

    # 6) Write candidate CSVs ----------------------------------------------
    def write_csv(path, rows):
        with open(path, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["unii", "preferred_name", "moiety_key", "is_INN", "is_USAN",
                        "substance_type", "foreign_sources", "n_sources",
                        "orphan_flag", "therapeutic_area", "atc", "indication",
                        "approved_abroad", "match_tier", "flags",
                        "example_source_names"])
            for e in rows:
                w.writerow([e["unii"], e["display"], e["moiety_key"],
                            "Y" if e["inn"] else "N", "Y" if e["usan"] else "N",
                            e["subtype"], "|".join(sorted(e["sources"])),
                            len(e["sources"]), "Y" if e["orphan"] else "N",
                            e["area"], e["atc"], e["indication"], e["approved"],
                            e["match_tier"], " | ".join(e["flags"]),
                            " ; ".join(sorted(e["examples"])[:3])])

    csv_path = os.path.join(OUT, "funnelA_candidates.csv")
    write_csv(csv_path, named)
    write_csv(os.path.join(OUT, "funnelA_unnamed_excipients.csv"), unnamed)
    write_csv(os.path.join(OUT, "funnelA_review.csv"), review)
    candidates = named  # headline set

    # 7) Write funnel report ------------------------------------------------
    orphan_n = sum(1 for e in candidates if e["orphan"])
    inn_n = sum(1 for e in candidates if e["inn"])
    multi_n = sum(1 for e in candidates if len(e["sources"]) > 1)
    rep_path = os.path.join(OUT, "funnel_report.md")
    with open(rep_path, "w", encoding="utf-8") as fh:
        fh.write(_report_md(funnel, us_stats, candidates, review, orphan_n, inn_n,
                            multi_n, time.time() - t0))

    # 7b) Machine-readable summary for the dashboard UI --------------------
    import json
    def pack(e):
        return {"unii": e["unii"], "name": e["display"], "moiety": e["moiety_key"],
                "inn": e["inn"], "usan": e["usan"], "type": e["subtype"],
                "sources": sorted(e["sources"]), "orphan": e["orphan"],
                "tier": e["match_tier"], "examples": sorted(e["examples"])[:3],
                "area": e["area"], "atc": e["atc"], "indication": e["indication"],
                "approved": e["approved"], "flags": e["flags"]}
    summary = {
        "generated": time.strftime("%Y-%m-%d"),
        "snapshot": "UNII 26 Feb 2026 · Drugs@FDA 4 Aug 2026 · Orange Book Jul 2026 · EMA 5 Aug 2026 · GSRS live sweep",
        "funnel": funnel,
        "us_ingredient_rows": us_stats["ingredient_rows"],
        "counts": {"named": len(named), "unnamed": len(unnamed),
                   "review": len(review),
                   "orphan": orphan_n, "inn": inn_n, "multi_regulator": multi_n},
        "candidates": [pack(e) for e in named],
        "unnamed": [pack(e) for e in unnamed],
        "review": [pack(e) for e in review],
    }
    with open(os.path.join(OUT, "summary.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=1)

    log(f"DONE in {time.time()-t0:.1f}s")
    log(f"  candidates (small-molecule, never-US): {len(candidates):,}")
    log(f"  of which orphan-flagged: {orphan_n:,}")
    log(f"  needs-human-review rows: {len(review):,}")
    log(f"  excluded by GSRS relationship graph: {funnel['in_us_gsrs']:,}")
    log(f"  -> {csv_path}")
    log(f"  -> {rep_path}")


def _report_md(f, us, cands, review, orphan_n, inn_n, multi_n, secs):
    lines = []
    A = lines.append
    A("# Funnel A candidate-discovery run\n")
    A(f"_Generated by `pipeline/rdh_diff.py` in {secs:.0f}s. Data snapshot 2026-08 "
      "(UNII 26Feb2026, Drugs@FDA 04Aug2026, Orange Book Jul2026, EMA 05Aug2026, "
      "GSRS relationship graph queried live)._\n")
    A("**What this is:** active substances approved by a foreign regulator whose "
      "active moiety is absent from the entire US approval record — i.e. the "
      "population A1 (never approved in the US) that § 360ff makes PRV-eligible. "
      "This is a *screening list*, not a clearance; downstream filters "
      "(505(b)(1) fileability, rare-pediatric evidence, FTO, orphan-exclusivity "
      "conflict) still apply. The matcher is measured, not asserted: "
      "`python3 pipeline/test_accuracy.py --real` replays labeled known-answer "
      "drugs through this exact code path.\n")
    A("## Funnel\n")
    A("| Stage | Count |")
    A("|---|---|")
    A(f"| Foreign substance rows ingested | {f['foreign_rows']:,} |")
    A(f"| Resolved to a UNII | {f['resolved']:,} |")
    A(f"| Unresolved (mostly PMDA katakana — needs transliteration) | {f['unmatched']:,} |")
    A(f"| — of which PMDA/Japanese | {f['needs_translit_unmatched']:,} |")
    A(f"| Unique moieties, resolved | {len(cands)+f['in_us']+f['biologic_or_mixture']+f['review']+f.get('unnamed',0):,} |")
    A(f"| Dropped — moiety already approved in US | {f['in_us']:,} |")
    A(f"| — via string/UNII variant match | {f['in_us_string']:,} |")
    A(f"| — via GSRS relationship graph (prodrug/conjugate/synonym-island) | {f['in_us_gsrs']:,} |")
    A(f"| Dropped — biologic/vaccine/mixture (not a repurposing candidate) | {f['biologic_or_mixture']:,} |")
    A(f"| **Needs human review — cannot be settled by data on hand** | **{f['review']:,}** |")
    A(f"| Small-molecule, never-US | {f['candidate_small_mol']:,} |")
    A(f"| — unnamed (excipient/antiseptic/reagent/vet — appendix CSV) | {f.get('unnamed',0):,} |")
    A(f"| **Funnel A candidates — named drug (INN or USAN)** | **{f.get('named_drug',0):,}** |")
    A(f"| — INN-designated | {inn_n:,} |")
    A(f"| — flagged orphan by a foreign regulator | {orphan_n:,} |")
    A(f"| — approved in >1 foreign regulator | {multi_n:,} |\n")
    A("## US exclusion set\n")
    A(f"- {us['ingredient_rows']:,} active-ingredient rows from Drugs@FDA + Orange Book, "
      "expanded to every salt/spelling/acid-ate variant (moiety.py) and to GSRS "
      "prodrug/salt-parent/active-moiety relatives two hops out (gsrs.py)\n")
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
    if review:
        A("\n### Needs human review (funnelA_review.csv)\n")
        A("These rows are neither kept nor dropped: the data on hand cannot settle "
          "them. Each carries the specific open question.\n")
        A("| UNII | Name | Open question |")
        A("|---|---|---|")
        for e in review[:40]:
            A(f"| {e['unii']} | {e['display']} | {' / '.join(e['flags'])[:160]} |")
    A("\n### Known residual error classes (do not skip)\n")
    A("- **US exclusion set is NDA-based.** Drugs@FDA + Orange Book do NOT include "
      "OTC-monograph, pre-1938, or DESI-withdrawn drugs. So a moiety marketed in "
      "the US only under an OTC monograph (e.g. aspirin) can still surface as a "
      "false candidate. This is the § 2 completeness gap in the method doc. It "
      "also intersects the *Sun Pharma* A2 population, so treat these as "
      "'investigate', not 'discard'.\n")
    A("- **Prodrug/conjugate exclusion now runs via GSRS** (two hops along "
      "ACTIVE MOIETY / PRODRUG / SALT-PARENT edges) and catches the "
      "isavuconazole-class leaks the string layer measured. It depends on the "
      "GSRS graph being complete for the substance; a missing GSRS edge is a "
      "missing exclusion, so prodrug-looking names in the candidate list still "
      "deserve a manual glance.\n")
    A("- **EMA is centralised-only.** Nationally-authorised EU drugs are absent, "
      "so some 'never-US' calls may actually be approved via an EU member state.\n")
    A("- **Japan is under-covered.** Only PMDA FY2025 (~140 rows) is loaded and "
      "katakana names mostly fail to resolve without a transliteration layer. The "
      "true Funnel A pool is larger and concentrated in exactly this highest-yield "
      "source — building the JP→UNII transliteration layer is the top next step.\n")
    A("- This diff does NOT test the § 360ff(a)(3) rare-pediatric gate, FTO, or "
      "existing orphan exclusivity. `pipeline/eligibility.py` walks all ten "
      "statutory criteria per candidate and labels which a human must decide; it "
      "never returns 'eligible', only 'nothing has ruled it out yet'.\n")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
