#!/usr/bin/env python3
"""
RareDiseaseHedge — candidate-discovery diff (Funnel A enumeration).

Implements sources/00-CANDIDATE-DISCOVERY-METHOD.md end to end:

  LEFT  = active substances approved by foreign regulators: EMA centralised,
          EMA Article 57 (every NATIONALLY-authorised EEA product), Health
          Canada, Swissmedic; PMDA best-effort
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
from moiety import full_keys, norm, stereo_name_variants  # noqa: E402
from gsrs import GsrsClient  # noqa: E402
import sources  # noqa: E402

RAW = os.path.join(HERE, "data", "raw")
OUT = os.path.join(HERE, "data", "out")

# Regulatory standing, best-wins when several regulators list the same moiety.
# "never_authorised" means a dossier exists but no regulator ever granted a
# licence (EMA application-withdrawn / refused / opinion-only). Those rows are
# real repurposing leads but they are NOT foreign approvals, so they are counted
# and reported separately — conflating them overstated the 2026-08 candidate list
# by 33 of 67 rows.
STATUS_RANK = {"never_authorised": 1, "previously_authorised": 2, "authorised": 3}

# Authorisations this pipeline structurally cannot see, for moieties whose only
# LOADED record is a non-authorisation. The four registers loaded are EMA
# CENTRALISED, Health Canada, Swissmedic and PMDA-FY — so a drug licensed only in
# Japan, Australia, or via an EU national/mutual-recognition route reads as
# "never authorised" when it is in fact approved abroad. Without this table the
# status fix would trade one overclaim (calling refusals approvals) for another
# (calling real approvals refusals). Each entry is a cited fact, and the row is
# FLAGGED rather than promoted — the pipeline still has no machine evidence.
#   moiety_key -> (regulator, citation)
KNOWN_AUTHORISED_ELSEWHERE = {
    "ANAMORELIN":   ("PMDA Japan", "approved Jan 2021 (Adlumiz, cancer cachexia); "
                                   "EMA row is a refusal"),
    "GARENOXACIN":  ("PMDA Japan", "approved Jul 2007 (Geninax); EMA row is an "
                                   "withdrawn application"),
    # (PERFLUBUTANE was here until 2026-08-31; EMA Article 57 now carries it
    #  directly — Denmark/Norway/Sweden — so it lands as a real candidate and no
    #  longer needs a hand-correction.)
    "PLITIDEPSIN":  ("TGA Australia", "approved Dec 2018 (Aplidin, multiple "
                                      "myeloma); EMA row is a withdrawn application"),
    "LISURIDE":     ("EU national", "nationally authorised for Parkinson's disease "
                                    "and hyperprolactinaemia; the EMA row is a "
                                    "withdrawn RLS application"),
    "XIMELAGATRAN": ("EU mutual recognition",
                     "authorised via MRP before 2006 withdrawal; the EMA "
                     "centralised row is a withdrawn application"),
}

# The stereoisomer-partner vocabulary lives in moiety.py (INN_STEREO_PREFIXES /
# stereo_name_variants) so the harness can test it and there is exactly one
# definition of it in the codebase.

# Prodrugs whose active moiety IS US-approved but for which the GSRS graph holds
# no edge — typically because the substance is too new to have been curated.
# The GSRS sweep is the general mechanism; this is the acknowledged residual, so
# it stays small, cited, and VERIFIED at run time: each entry only excludes if
# the named parent is genuinely present in the US record, so a stale entry can
# never assert an approval that no longer exists.
#   moiety_key -> (US-approved active moiety, citation)
GSRS_GAP_PRODRUGS = {
    "TEGOMIL": ("monomethyl fumarate",
                "tegomil fumarate (Riulvy, EMA 2026) is two monomethyl-fumarate "
                "moieties joined by tetraethylene glycol and is cleaved in vivo "
                "to monomethyl fumarate + inactive PEG; MMF is US-approved as "
                "Bafiertam (NDA 210296). Verified 2026-08-29 — GSRS carries no "
                "relationship for UNII MXD6KMG2ZP."),
}


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def _newest_unii(prefix: str) -> str:
    """Newest date-stamped UNII flat file for a prefix, by embedded date.

    Sorting on the filename string would put 26Feb2026 after 4Aug2026, so the
    date is parsed. Raises with an actionable message rather than letting the
    run proceed on a file that is not there."""
    import datetime, glob, re
    best, best_d = None, None
    for p in glob.glob(os.path.join(RAW, prefix + "*.txt")):
        m = re.match(re.escape(prefix) + r"(.+)\.txt$", os.path.basename(p))
        if not m:
            continue
        try:
            d = datetime.datetime.strptime(m.group(1), "%d%b%Y").date()
        except ValueError:
            continue
        if best_d is None or d > best_d:
            best, best_d = p, d
    if not best:
        raise SystemExit(
            f"no {prefix}*.txt in {RAW}. Run: python3 pipeline/fetch.py unii unii_data")
    return best


def main():
    os.makedirs(OUT, exist_ok=True)
    t0 = time.time()

    # 1) Build the UNII join index -----------------------------------------
    # Filenames are date-stamped by FDA (UNII_Names_4Aug2026.txt), so pick the
    # newest present rather than hardcoding a date. The hardcoded 26Feb2026 path
    # meant a refreshed index was never actually used — the pipeline read a
    # six-month-old identity map while reporting a current snapshot.
    idx = UniiIndex()
    names_path = _newest_unii("UNII_Names_")
    recs_path = _newest_unii("UNII_Records_")
    log(f"loading UNII name index ({os.path.basename(names_path)}, ~1M synonyms)...")
    n_names = idx.load_names(names_path)
    log(f"  {n_names:,} synonym rows -> {len(idx.name2unii):,} normalized names")
    log(f"loading UNII records ({os.path.basename(recs_path)})...")
    n_rec = idx.load_records(recs_path)
    log(f"  {n_rec:,} UNII records")

    # 2) RIGHT side: US exclusion set --------------------------------------
    log("building US exclusion set (Drugs@FDA + Orange Book)...")
    us_uniis, us_moieties, us_stats = sources.load_us_exclusion(idx, RAW)
    log(f"  {us_stats['ingredient_rows']:,} ingredient rows -> "
        f"{len(us_uniis):,} US moiety-UNIIs, {len(us_moieties):,} US moiety keys "
        f"({us_stats['unmatched']:,} name rows unresolved to UNII)")

    # 2b) US non-application marketing (flag-only layer) -------------------
    # Optional and additive: it can add a flag but never change a verdict, so a
    # missing openfda_ndc.zip degrades to silence rather than to a wrong answer.
    ndc_unii, ndc_key = sources.load_us_otc_marketing(idx, RAW)
    if ndc_unii:
        log(f"  openFDA NDC marketing categories for {len(ndc_unii):,} UNIIs "
            f"(flag-only: OTC-monograph/bulk marketing does NOT disqualify)")

    # 3) LEFT side: foreign approvals --------------------------------------
    # Every loader returns [] when its file is absent. Silently, that turns a
    # missing download into a smaller candidate list that looks just as
    # confident — losing EMA alone would drop most of the headline set. So the
    # expected input file is named, and its absence is a loud warning.
    foreign = []
    missing = []
    for name, fn, fname in [
            ("EMA", sources.load_ema, "ema_med.xlsx"),
            ("EU national (Art57)", sources.load_ema_art57, "ema_art57.xlsx"),
            ("Canada", sources.load_canada, "ingred_ap.zip"),
            ("Swissmedic", sources.load_swissmedic, "sm_stoff.xlsx"),
            ("PMDA", sources.load_pmda, "pmda_fy2025.xlsx")]:
        recs = fn(RAW)
        if not recs:
            missing.append(f"{name} ({fname})")
            log(f"  !! WARNING: {name} contributed 0 rows — {fname} missing or "
                f"unreadable. Candidate list is INCOMPLETE for this regulator.")
        else:
            log(f"loaded {len(recs):,} substance rows from {name}")
        foreign.extend(recs)
    if missing:
        log(f"  !! {len(missing)} source(s) contributed nothing: {', '.join(missing)}")
        log(f"  !! run `python3 pipeline/fetch.py` before trusting these counts")

    # 4) Resolve + anti-join -----------------------------------------------
    # Collapse foreign rows to unique moiety, tracking which regulators and
    # whether any source flagged it orphan. Membership is tested on the FULL
    # variant collection (all UNIIs + all key forms, both sides) — the single
    # canonical-key comparison this replaces measured 12/19 silent misses on
    # labeled US-approved drugs (see test_accuracy.py).
    log("resolving foreign substances and running anti-join...")
    by_moiety: dict[str, dict] = {}
    unresolved_by_source: dict[str, int] = {}
    rows_by_source: dict[str, int] = {}
    funnel = {"foreign_rows": len(foreign), "resolved": 0, "unmatched": 0,
              "biologic_or_mixture": 0, "in_us": 0, "in_us_string": 0,
              "in_us_gsrs": 0, "review": 0, "candidate_small_mol": 0,
              "needs_translit_unmatched": 0}

    for rec in foreign:
        rows_by_source[rec["source"]] = rows_by_source.get(rec["source"], 0) + 1
        cu, mk, tier = idx.moiety_unii(rec["substance"])
        if cu:
            funnel["resolved"] += 1
        else:
            funnel["unmatched"] += 1
            if rec.get("needs_translit"):
                funnel["needs_translit_unmatched"] += 1
            # Per-source, because the aggregate is misleading: the report used to
            # blame "mostly PMDA katakana" when Japan is only ~140 rows and the
            # real mass is Swissmedic's Latin pharmacopoeial genitives.
            unresolved_by_source[rec["source"]] = \
                unresolved_by_source.get(rec["source"], 0) + 1
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
            "foreign_status": "never_authorised", "status_by_source": {},
            "countries": set(),
        })
        entry["sources"].add(rec["source"])
        entry["countries"].update(rec.get("countries") or ())
        entry["orphan"] = entry["orphan"] or rec["orphan"]
        entry["examples"].add(rec["substance"][:60])
        entry["in_us"] = entry["in_us"] or in_us
        if basis and not entry["excluded_by"]:
            entry["excluded_by"] = basis
        # Best regulatory standing across every source that lists this moiety. A
        # drug refused by EMA but licensed in Canada is approved abroad; a drug
        # only ever refused everywhere is not. Keeping the per-source detail means
        # the report can say WHICH regulator actually authorised it.
        fs = rec.get("foreign_status", "authorised")
        if STATUS_RANK.get(fs, 0) > STATUS_RANK.get(entry["foreign_status"], 0):
            entry["foreign_status"] = fs
        prev = entry["status_by_source"].get(rec["source"])
        if prev is None or STATUS_RANK.get(fs, 0) > STATUS_RANK.get(prev, 0):
            entry["status_by_source"][rec["source"]] = fs
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

    def stereo_partner(name):
        """A US-approved stereoisomer/geometric-isomer partner of this moiety.

        Candidate names come from moiety.stereo_name_variants; this function only
        decides which of them the US record actually contains. Returns
        (partner_key, basis) or None."""
        for c in sorted(stereo_name_variants(name)):
            u = idx.name2unii.get(c) or idx.moiety2unii.get(c)
            if u and u in us_uniis:
                return c, f"stereo-unii:{u}"
            if c in us_moieties:
                return c, f"stereo-key:{c}"
        return None

    def gsrs_gap_hit(e):
        """Cited prodrug exclusion for a pair GSRS does not link. Re-verifies the
        parent against the live US set rather than trusting the table."""
        ent = GSRS_GAP_PRODRUGS.get(e["moiety_key"])
        if not ent:
            return None
        parent, cite = ent
        puniis, pkeys = idx.collect(parent)
        if (puniis & us_uniis) or (pkeys & us_moieties):
            pu = sorted(puniis & us_uniis)
            return (f"prodrug-supplement:{pu[0] if pu else parent}", parent, cite)
        return None

    wall = idx.is_counterion  # synonym-robust counterion wall for the traversal
    for n_done, e in enumerate(survivors, 1):
        gap = gsrs_gap_hit(e)
        if gap:
            basis, parent, cite = gap
            e["in_us"] = True
            e["excluded_by"] = basis
            e["flags"].append(f"PRODRUG_OF_US_APPROVED: active moiety is {parent} "
                              f"— {cite}")
            funnel["in_us_gsrs"] += 1
            continue
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
            continue
        # Name-based stereo partner: the exclusion case GSRS structurally misses.
        # Whether a single enantiomer of an approved racemate (or vice versa)
        # shares the approved "active moiety" under 21 CFR 314.3 is not settled by
        # the statutory text, so this is REVIEW — never a silent keep or drop.
        sp = stereo_partner(e["display"] or e["moiety_key"])
        if sp:
            partner, basis = sp
            e["verdict"] = "review"
            e["flags"].append(
                f"STEREO_US_PARTNER: {partner} is US-approved ({basis}); "
                f"s.529 treatment of enantiomer/isomer pairs is unsettled and "
                f"GSRS carries no stereo edge for this pair")
        elif has_stereo_marker(e["display"] or e["moiety_key"]):
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
    # US marketing flags on everything that survived the exclusion test. Skip
    # rows already excluded or already biologic-dropped — flagging a biologic
    # about to be discarded is noise, and NDA/ANDA/BLA moieties are now folded
    # into the exclusion set so they carry in_us=True and never reach here (the
    # US_APPLICATION_FOUND branch is now a defensive should-never-fire tripwire).
    for e in by_moiety.values():
        if e["in_us"] or e["biologic"]:
            continue
        cats = set()
        cats |= ndc_unii.get(e["unii"], set())
        for k in (e["moiety_key"], e["display"]):
            if k:
                cats |= ndc_key.get(norm(k), set())
        hard = cats & sources.APPLICATION_CATEGORIES
        soft = cats & sources.NON_APPLICATION_CATEGORIES
        if hard:
            # Should be unreachable: an NDA/ANDA/BLA row means a real US approval
            # the exclusion set failed to see. Surface it as REVIEW, loudly.
            e["verdict"] = "review"
            e["flags"].append(
                f"US_APPLICATION_FOUND: openFDA NDC lists this moiety under "
                f"{sorted(hard)} — an application-based US approval the exclusion "
                f"set missed. Treat the whole run as suspect until explained.")
            log(f"  !! {e['display'] or e['moiety_key']}: NDC says {sorted(hard)}")
        elif soft:
            e["flags"].append(
                f"US_NON_APPLICATION_MARKETING: sold in the US under {sorted(soft)}. "
                f"Does NOT disqualify (s.529 bars a prior approval in a 505 "
                f"application, which these are not) but there is no exclusivity "
                f"runway and supply already exists — and rows like this are often "
                f"excipients or antiseptics rather than drugs.")

    named, unnamed, review, dossier_only = [], [], [], []
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
        if not (e["inn"] or e["usan"]):
            unnamed.append(e)
            continue
        # No authorisation in any register this pipeline LOADS — not the same as
        # "never authorised anywhere", since only EMA centralised, Health Canada,
        # Swissmedic and PMDA-FY are loaded. A dossier and human data exist (the
        # feasibility signal), but calling it "approved abroad" on this evidence
        # would be false. Its own bucket, never the headline number.
        if e["foreign_status"] == "never_authorised":
            known = KNOWN_AUTHORISED_ELSEWHERE.get(e["moiety_key"])
            if known:
                reg, cite = known
                e["flags"].append(f"AUTHORISED_ELSEWHERE ({reg}): {cite}. Not "
                                  f"visible to the registers loaded here.")
            dossier_only.append(e)
        else:
            named.append(e)
    funnel["in_us_string"] = funnel["in_us"] - funnel["in_us_gsrs"]
    funnel["named_drug"] = len(named)
    funnel["unnamed"] = len(unnamed)
    funnel["no_authorisation_in_loaded_registers"] = len(dossier_only)
    funnel["unresolved_by_source"] = dict(sorted(unresolved_by_source.items()))
    funnel["rows_by_source"] = dict(sorted(rows_by_source.items()))

    # EEA country count is a real quality signal from Article 57: a substance
    # authorised in 25 member states is an established medicine, not a curiosity.
    sort_key = lambda e: (not e["orphan"], not (len(e["sources"]) > 1),
                          -len(e["countries"]),
                          e["display"] or e["moiety_key"])
    named.sort(key=sort_key)
    unnamed.sort(key=sort_key)
    review.sort(key=sort_key)
    dossier_only.sort(key=sort_key)

    # 6) Write candidate CSVs ----------------------------------------------
    def write_csv(path, rows):
        with open(path, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["unii", "preferred_name", "moiety_key", "is_INN", "is_USAN",
                        "substance_type", "foreign_sources", "n_sources",
                        "n_eea_countries", "foreign_status", "status_by_source",
                        "orphan_flag", "therapeutic_area", "atc", "indication",
                        "approved_abroad", "match_tier", "flags",
                        "example_source_names"])
            for e in rows:
                w.writerow([e["unii"], e["display"], e["moiety_key"],
                            "Y" if e["inn"] else "N", "Y" if e["usan"] else "N",
                            e["subtype"], "|".join(sorted(e["sources"])),
                            len(e["sources"]), len(e["countries"]),
                            e["foreign_status"],
                            "|".join(f"{k}={v}" for k, v in
                                     sorted(e["status_by_source"].items())),
                            "Y" if e["orphan"] else "N",
                            e["area"], e["atc"], e["indication"], e["approved"],
                            e["match_tier"], " | ".join(e["flags"]),
                            " ; ".join(sorted(e["examples"])[:3])])

    csv_path = os.path.join(OUT, "funnelA_candidates.csv")
    write_csv(csv_path, named)
    write_csv(os.path.join(OUT, "funnelA_unnamed_excipients.csv"), unnamed)
    write_csv(os.path.join(OUT, "funnelA_review.csv"), review)
    write_csv(os.path.join(OUT, "funnelA_dossier_only.csv"), dossier_only)
    candidates = named  # headline set

    # 7) Write funnel report ------------------------------------------------
    orphan_n = sum(1 for e in candidates if e["orphan"])
    inn_n = sum(1 for e in candidates if e["inn"])
    multi_n = sum(1 for e in candidates if len(e["sources"]) > 1)
    rep_path = os.path.join(OUT, "funnel_report.md")
    with open(rep_path, "w", encoding="utf-8") as fh:
        fh.write(_report_md(funnel, us_stats, candidates, review, dossier_only,
                            orphan_n, inn_n, multi_n, time.time() - t0))

    # 7b) Machine-readable summary for the dashboard UI --------------------
    import json
    def pack(e):
        return {"unii": e["unii"], "name": e["display"], "moiety": e["moiety_key"],
                "inn": e["inn"], "usan": e["usan"], "type": e["subtype"],
                "sources": sorted(e["sources"]), "orphan": e["orphan"],
                "tier": e["match_tier"], "examples": sorted(e["examples"])[:3],
                "area": e["area"], "atc": e["atc"], "indication": e["indication"],
                "approved": e["approved"], "flags": e["flags"],
                "foreign_status": e["foreign_status"],
                "status_by_source": e["status_by_source"],
                "n_countries": len(e["countries"]),
                "countries": sorted(e["countries"])[:40]}
    summary = {
        "generated": time.strftime("%Y-%m-%d"),
        "snapshot": _snapshot_label(),
        "funnel": funnel,
        "us_ingredient_rows": us_stats["ingredient_rows"],
        "counts": {"named": len(named), "unnamed": len(unnamed),
                   "review": len(review), "dossier_only": len(dossier_only),
                   "orphan": orphan_n, "inn": inn_n, "multi_regulator": multi_n},
        "candidates": [pack(e) for e in named],
        "unnamed": [pack(e) for e in unnamed],
        "review": [pack(e) for e in review],
        "dossier_only": [pack(e) for e in dossier_only],
    }
    with open(os.path.join(OUT, "summary.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=1)

    log(f"DONE in {time.time()-t0:.1f}s")
    log(f"  candidates — approved abroad, never US: {len(candidates):,}")
    log(f"  of which orphan-flagged: {orphan_n:,}")
    log(f"  dossier-only (no authorisation in loaded registers): {len(dossier_only):,}")
    log(f"  needs-human-review rows: {len(review):,}")
    log(f"  excluded by GSRS relationship graph: {funnel['in_us_gsrs']:,}")
    log(f"  -> {csv_path}")
    log(f"  -> {rep_path}")


def _snapshot_label():
    """Provenance from the files actually on disk, not a hand-edited string.

    The previous label was a literal that drifted from reality (it claimed
    'EMA 5 Aug 2026' while naming no Health Canada file at all, and survived a
    refresh of drug_ap.zip). Deriving it from mtimes means the dashboard can
    never overstate how fresh the inputs are."""
    import datetime
    parts = []
    # the UNII index is date-stamped in its filename and picked by _newest_unii,
    # so report the file actually loaded rather than a hardcoded one
    try:
        parts.append("UNII " + os.path.basename(_newest_unii("UNII_Names_"))
                     .replace("UNII_Names_", "").replace(".txt", ""))
    except SystemExit:
        parts.append("UNII MISSING")
    for label, fn in [("Drugs@FDA", "drugsatfda.zip"),
                      ("Orange Book", "eob.zip"),
                      ("EMA", "ema_med.xlsx"),
                      ("Health Canada", "ingred_ap.zip"),
                      ("Swissmedic", "sm_stoff.xlsx"),
                      ("PMDA", "pmda_fy2025.xlsx")]:
        p = os.path.join(RAW, fn)
        if os.path.exists(p):
            d = datetime.date.fromtimestamp(os.path.getmtime(p))
            parts.append(f"{label} {d:%d %b %Y}")
        else:
            parts.append(f"{label} MISSING")
    return " · ".join(parts) + " · GSRS relationship graph"


def _report_md(f, us, cands, review, dossier_only, orphan_n, inn_n, multi_n, secs):
    lines = []
    A = lines.append
    A("# Funnel A candidate-discovery run\n")
    A(f"_Generated by `pipeline/rdh_diff.py` in {secs:.0f}s. Data snapshot: "
      f"{_snapshot_label()}._\n")
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
    A(f"| Unresolved to a UNII (cannot be diffed; dropped) | {f['unmatched']:,} |")
    for _src, _n in (f.get("unresolved_by_source") or {}).items():
        _tot = (f.get("rows_by_source") or {}).get(_src, 0)
        _pct = f"{100*_n/_tot:.0f}%" if _tot else "?"
        A(f"| — {_src} | {_n:,} of {_tot:,} rows ({_pct}) |")
    A(f"| Unique moieties, resolved | {len(cands)+f['in_us']+f['biologic_or_mixture']+f['review']+f.get('unnamed',0):,} |")
    A(f"| Dropped — moiety already approved in US | {f['in_us']:,} |")
    A(f"| — via string/UNII variant match | {f['in_us_string']:,} |")
    A(f"| — via GSRS relationship graph (prodrug/conjugate/synonym-island) | {f['in_us_gsrs']:,} |")
    A(f"| Dropped — biologic/vaccine/mixture (not a repurposing candidate) | {f['biologic_or_mixture']:,} |")
    A(f"| **Needs human review — cannot be settled by data on hand** | **{f['review']:,}** |")
    A(f"| Small-molecule, never-US | {f['candidate_small_mol']:,} |")
    A(f"| — unnamed (excipient/antiseptic/reagent/vet — appendix CSV) | {f.get('unnamed',0):,} |")
    A(f"| — named, but no authorisation in any register loaded here (dossier-only) | {f.get('no_authorisation_in_loaded_registers',0):,} |")
    A(f"| **Funnel A candidates — named drug (INN or USAN), genuinely approved abroad** | **{f.get('named_drug',0):,}** |")
    A(f"| — INN-designated | {inn_n:,} |")
    A(f"| — flagged orphan by a foreign regulator | {orphan_n:,} |")
    A(f"| — approved in >1 foreign regulator | {multi_n:,} |\n")
    A("## US exclusion set\n")
    A(f"- {us['ingredient_rows']:,} active-ingredient rows from Drugs@FDA + Orange Book "
      f"+ openFDA NDC ({us.get('ndc_rows', 0):,} NDA/ANDA/BLA rows), "
      "expanded to every salt/spelling/acid-ate variant (moiety.py) and to GSRS "
      "prodrug/salt-parent/active-moiety relatives two hops out (gsrs.py). The NDC "
      "pass covers moieties present in Drugs@FDA under a spelling whose UNII does "
      "not intersect the foreign name's.\n")
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
    if dossier_only:
        A("\n### Dossier-only — named, never-US, and no authorisation in any register "
          "loaded here (funnelA_dossier_only.csv)\n")
        A("These moieties reached a stringent regulator but the application was "
          "withdrawn, refused, or sits at opinion stage in every register this "
          "pipeline loads. They are **not** foreign approvals on this evidence and "
          "must never be counted as such. Two cautions, in opposite directions:\n")
        A("- **They may still be approved somewhere unseen.** Only EMA *centralised*, "
          "Health Canada, Swissmedic and PMDA-FY are loaded, so a drug licensed in "
          "Japan, Australia, or via an EU national/mutual-recognition route lands "
          "here wrongly. Known cases are flagged AUTHORISED_ELSEWHERE; that list is "
          "hand-built and certainly incomplete. Wiring in EMA Article 57 and a "
          "Japanese source is what actually fixes this.\n")
        A("- **A refusal is a real negative signal.** These are still genuine "
          "repurposing leads — a full dossier and human clinical data exist — but a "
          "refusal may reflect a safety or efficacy problem that would also sink a "
          "US filing. Read each one's refusal grounds before spending on it.\n")
        A("| UNII | Name | Regulator status | Orphan | Indication |")
        A("|---|---|---|---|---|")
        for e in dossier_only[:60]:
            st = "; ".join(f"{k}: {v.replace('_', ' ')}"
                           for k, v in sorted(e["status_by_source"].items()))
            A(f"| {e['unii']} | {e['display']} | {st} | "
              f"{'Y' if e['orphan'] else 'N'} | {(e['indication'] or '')[:70]} |")
    if review:
        A("\n### Needs human review (funnelA_review.csv)\n")
        A("These rows are neither kept nor dropped: the data on hand cannot settle "
          "them. Each carries the specific open question.\n")
        A("| UNII | Name | Open question |")
        A("|---|---|---|")
        for e in review[:40]:
            A(f"| {e['unii']} | {e['display']} | {' / '.join(e['flags'])[:160]} |")
    A("\n### Known residual error classes (do not skip)\n")
    A("- **US OTC-monograph marketing is NOT a disqualifying approval.** "
      "s.529(a)(4)(B)(i)(I) turns on a prior approval *in an application under "
      "505(b)(1), (b)(2) or (j)*. A drug marketed under an OTC monograph has no "
      "such application, so it does not bar a voucher. The exclusion set is "
      "therefore correctly NDA/ANDA-based, and adding OTC-monograph moieties to it "
      "would introduce false NEGATIVES. (The earlier version of this note claimed "
      "the opposite and used aspirin as the example; aspirin also holds NDAs, so "
      "it was doubly wrong.) What OTC status does change is commercial: no "
      "exclusivity runway and existing competition. openFDA `drug/ndc` "
      "`marketing_category` is the field that tells them apart.\n")
    A("- **Pre-1962 approvals may not count against a candidate.** In the "
      "*Sun Pharma* litigation over phenobarbital (SEZABY) the D.D.C. held that a "
      "pre-1962 NDA which became effective by FDA inaction and was later 'deemed "
      "approved' was never *approved* in the ordinary sense, so it did not bar a "
      "rare-pediatric voucher. 740 applications in this Drugs@FDA snapshot have an "
      "original approval before 10 Oct 1962, and 70 distinct active moieties are "
      "approved ONLY through them. This diff still excludes all 70. If that "
      "holding stands, they are a separate candidate population rather than "
      "exclusions — a district-court ruling, so treat it as a live legal theory, "
      "not settled law.\n")
    A("- **Pre-2000 US withdrawals are missing from the bulk files.** Of 30 "
      "hand-checked drugs with genuine FDA approvals later withdrawn, 13 are absent "
      "from Drugs@FDA + Orange Book — every one withdrawn before ~2000 (terfenadine, "
      "astemizole, mibefradil, temafloxacin, dexfenfluramine, encainide, "
      "flosequinan, zomepirac, benoxaprofen, ticrynafen, nomifensine, methaqualone, "
      "phenformin). Post-2000 withdrawals are retained. A withdrawn approval still "
      "disqualifies, so this is a real false-positive channel; measured 2026-08-29, "
      "none of the 13 currently appears in any loaded foreign register, so the hole "
      "is latent rather than active. `US_WITHDRAWN_SUPPLEMENT` patches one case "
      "(betahistine) and is not a substitute for a 21 CFR 216.24 feed.\n")
    A("- **Prodrug/conjugate exclusion runs via GSRS** (two hops along "
      "ACTIVE MOIETY / PRODRUG / SALT-PARENT edges) and catches the "
      "isavuconazole-class leaks the string layer measured. It depends on the GSRS "
      "graph being complete for the substance; a missing edge is a missing "
      "exclusion. Two such gaps are known and handled explicitly: the stereoisomer "
      "layer (GSRS holds no enantiomer/racemate edge for zopiclone/eszopiclone or "
      "enclomifene/clomifene) and `GSRS_GAP_PRODRUGS` (tegomil fumarate -> "
      "monomethyl fumarate). Newly-INN'd substances are the likeliest next gap, so "
      "prodrug-looking names still deserve a manual glance.\n")
    A("- **EEA national approvals are now loaded, with one caveat.** EMA Article 57 "
      "(xEVMPD) covers every nationally-authorised EEA product, closing the gap "
      "that made a drug licensed in 25 member states but never centrally read as "
      "'never approved abroad'. The caveat: unlike the centralised medicines "
      "report, Article 57 has **no status column** — it is marketing-authorisation-"
      "holder-submitted data, so presence is taken as authorisation and there is no "
      "'refused' or 'withdrawn' to filter. It is therefore labelled as its own "
      "source, 'EU national (Art57)', so it can be discounted separately from a "
      "regulator decision this pipeline has actually read.\n")
    A("- **Non-EEA approvals are still invisible.** A drug licensed only in Japan, "
      "Australia, Korea or Brazil whose sole EMA record is a refusal still lands in "
      "the dossier-only bucket. `KNOWN_AUTHORISED_ELSEWHERE` hand-corrects the "
      "cases found by audit (anamorelin, garenoxacin, plitidepsin, lisuride, "
      "ximelagatran — Article 57 now covers perflubutane on its own). That list is "
      "hand-built and certainly incomplete; KEGG DRUG and the MHLW price list are "
      "the cheapest routes into Japan, and TGA/MFDS/ANVISA remain unfetchable from "
      "this environment.\n")
    A("- **Japan is effectively absent, and Switzerland nearly so.** Only PMDA "
      "FY2025 (140 rows) is loaded and 139 of them fail to resolve, so Japan "
      "contributes 1 moiety. Swissmedic resolves 102 of 2,970 rows (3%) because the "
      "list is in Latin pharmacopoeial genitives ('abacaviri sulfas'). The unresolved "
      "mass is Swiss, not Japanese — 2,868 rows against 139. KEGG DRUG "
      "(rest.kegg.jp/list/drug) carries Japanese drugs under Latin-script names with "
      "JAN tags and is the cheapest route into Japan without building a katakana "
      "transliteration layer.\n")
    A("- This diff does NOT test the § 360ff(a)(3) rare-pediatric gate, FTO, or "
      "existing orphan exclusivity. `pipeline/eligibility.py` walks all ten "
      "statutory criteria per candidate and labels which a human must decide; it "
      "never returns 'eligible', only 'nothing has ruled it out yet'.\n")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
