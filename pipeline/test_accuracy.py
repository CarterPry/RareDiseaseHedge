#!/usr/bin/env python3
"""
Accuracy harness for the s.529 exclusion matcher.

A screening pipeline with no labeled test set is unfalsifiable. This file holds
known-answer cases and reports recall and specificity, so a change to the
matcher can be shown to help rather than asserted to.

MUST_EXCLUDE
    The foreign-register spelling of a drug the FDA HAS approved. Every one of
    these must come back APPROVED_IN_US. A miss here is the expensive error: it
    puts an ineligible compound at the top of a review list. (The pre-2026-08
    hand-listed SALT_TOKENS matcher missed 12 of 19 of these against the real
    data files.)

MUST_KEEP
    Substances with no US approval on the record. These must not be excluded,
    or the screen throws away real candidates.

Two modes:

  python3 pipeline/test_accuracy.py
      Offline. Exercises the moiety.py string layer against a miniature US
      ingredient record spelled exactly as the FDA files spell it. No data
      files, no network. Fast enough to run on every change.

  python3 pipeline/test_accuracy.py --real
      Loads the real UNII flat files + Drugs@FDA + Orange Book from
      pipeline/data/raw/ and replays the same labeled cases through the SAME
      code path rdh_diff.py uses (UniiIndex.collect + us sets + GSRS cache).
      GSRS is consulted from the on-disk cache first; live only for uncached
      UNIIs. ~1-2 min, dominated by loading the 80MB names file.

Exit code 0 only when there are no silent misses and no false excludes.
"""
from __future__ import annotations
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from moiety import StringExclusionSet, Verdict, keys  # noqa: E402

# --------------------------------------------------------------------------
# Labeled cases. Spellings on the left are the FOREIGN-register form; the
# bracket note says why the case exists. Keep growing this list — every bug
# found in review should land here first.
# --------------------------------------------------------------------------

# (foreign spelling, why it must be excluded, class)
#   class: "string" — the string layer alone must catch it (hard fail if not)
#          "graph"  — needs the GSRS relationship graph; without it, REVIEW is
#                     acceptable (soft), silent NOT_IN_US is a hard fail
MUST_EXCLUDE = [
    ("ibandronic acid",             "Boniva 2003; INN acid vs USAN -ate",     "string"),
    ("lapatinib",                   "Tykerb 2007; US record has ditosylate",  "string"),
    ("fosaprepitant",               "Emend IV 2008; US has dimeglumine",      "string"),
    ("sunitinib",                   "Sutent 2006; US record has malate",      "string"),
    ("safinamide methanesulfonate", "Xadago 2017; mesylate spelling variant", "string"),
    ("infigratinib monophosphate",  "Truseltiq 2021 (withdrawn 2022 — still disqualifies)", "string"),
    ("aztreonam lysine",            "Cayston 2010; lysine salt",              "string"),
    ("zoledronate",                 "Reclast; -ate vs INN acid",              "string"),
    ("mycophenolic acid",           "Myfortic/CellCept; acid vs mofetil ester", "string"),
    ("amlodipine besilate",         "Norvasc; besilate/besylate spelling",    "string"),
    ("imatinib mesilate",           "Gleevec; mesilate/mesylate spelling",    "string"),
    ("pantoprazole sodium",         "Protonix; sesquihydrate on the US row",  "string"),
    ("quinidine",                   "US approved as the gluconate salt",      "string"),
    ("deflazacort",                 "Emflaza 2017 — itself a PRV earner",     "string"),
    ("cefpodoxime proxetil",        "Vantin; ester prodrug suffix",           "string"),
    ("isavuconazole",               "Cresemba 2015; US approved the prodrug isavuconazonium", "graph"),
    ("methylthioninium chloride",   "Provayblue 2016; synonym island (methylene blue)",       "graph"),
    ("edotreotide",                 "Ga-68 dotatoc 2019; radiolabel conjugate",               "graph"),
    # found BY this harness on real data 2026-08-28: originally mislabeled as a
    # keeper. Parecoxib is the injectable prodrug of valdecoxib (Bextra, FDA
    # 2001, withdrawn 2005) — active moiety already US-approved, mirror image
    # of the isavuconazole case.
    ("parecoxib sodium",            "prodrug of US-approved valdecoxib (Bextra)", "graph"),
    # found by the 2026-08-29 audit, using EMA Article 57 as an unseen test set.
    # Each was reading as never-US-approved against the real files.
    ("dabigatran",                  "Pradaxa 2010; US row is the ETEXILATE ester", "string"),
    ("cefalexin",                   "Keflex; INN cef- vs USAN ceph- spelling",     "string"),
    ("cefradine",                   "Velosef; INN cef- vs USAN ceph- spelling",    "string"),
    # found BY this harness on real data 2026-08-29, originally mislabeled as a
    # keeper — the same way parecoxib was. Mandol (cefamandole nafate, FDA 1978,
    # long discontinued) is on the record, so the moiety is disqualified.
    ("cefamandole",                 "Mandol; US row is the NAFATE ester",          "graph"),
]

# Substances whose US status the data CANNOT settle, where the only correct
# answer is REVIEW. Asserting either verdict would be a lie: for an enantiomer
# of an approved racemate (or vice versa) the statute does not say whether the
# approved "active moiety" carries across, and FDA's GSRS graph holds no edge
# between the pair — so no dataset on hand decides it. The harness checks that
# the stereo-partner layer still FINDS the pair; a human decides what it means.
MUST_REVIEW_STEREO = [
    ("zopiclone",    "ESZOPICLONE",  "Lunesta is the S-enantiomer of the racemate"),
    ("enclomifene",  "CLOMIFENE",    "Clomid is a mixture of en-/zu-clomifene"),
]

# Substances with no US approval. These must survive the screen.
MUST_KEEP = [
    ("idebenone",         "Raxone, EU only"),
    ("masitinib",         "EU review only, no US approval"),
    ("pridopidine",       "no US approval"),
    ("leriglitazone",     "no US approval"),
    ("tiratricol",        "Emcitate, EU 2025, no US approval"),
    ("ataluren",          "Translarna, EU only"),
    ("mifamurtide",       "Mepact, EU only"),
    ("gliclazide",        "widely marketed, never FDA approved"),
    ("bromazepam",        "never FDA approved"),
    ("delamanid",         "Deltyba, EU only"),
    ("plitidepsin",       "Aplidin, no US approval"),
    ("bardoxolone methyl", "no US approval; also guards TRIVIAL_BASES ('methyl')"),
    ("govorestat",        "no US approval"),
    ("eprodisate disodium", "no US approval; salt spelling"),
    ("catequentinib hydrochloride", "no US approval (anlotinib)"),
    # counterion-traversal regression guards, found on real data 2026-08-28:
    # a salt's GSRS graph points at its bare counterion (tartaric/maleic acid),
    # and walking through it joins every US drug sharing that counterion.
    ("lasofoxifene",          "Fablyn EU; FDA rejected — tartrate/tartaric-acid wall"),
    ("capromorelin",          "vet-only US (FDA CVM, s.512) — s.529 lists only 505/351"),
    ("cediranib maleate",     "never FDA approved — maleic-acid wall"),
    ("vinflunine ditartrate", "Javlor EU only — tartaric-acid wall"),
    # CEF-/CEPH- bridge regression guard: the variant must not over-fire.
    ("cefovecin",         "vet-only US (Convenia, FDA CVM) — s.529 lists only 505/351"),
]

# --------------------------------------------------------------------------
# Offline mode: miniature US record, spelled as the FDA files spell it
# --------------------------------------------------------------------------
US_INGREDIENT_RECORD = [
    "IBANDRONATE SODIUM",              # Boniva
    "LAPATINIB DITOSYLATE",            # Tykerb
    "FOSAPREPITANT DIMEGLUMINE",       # Emend for Injection
    "SUNITINIB MALATE",                # Sutent
    "SAFINAMIDE MESYLATE",             # Xadago
    "INFIGRATINIB PHOSPHATE",          # Truseltiq (withdrawn — still on record)
    "ISAVUCONAZONIUM SULFATE",         # Cresemba (prodrug of isavuconazole)
    "AZTREONAM",                       # Azactam / Cayston
    "METHYLENE BLUE",                  # Provayblue
    "ZOLEDRONIC ACID",                 # Reclast / Zometa
    "MYCOPHENOLATE MOFETIL",           # CellCept
    "AMLODIPINE BESYLATE",             # Norvasc
    "IMATINIB MESYLATE",               # Gleevec
    "PANTOPRAZOLE SODIUM SESQUIHYDRATE",
    "QUINIDINE GLUCONATE",
    "DEFLAZACORT",                     # Emflaza
    "CEFPODOXIME PROXETIL",            # Vantin
    "GALLIUM GA-68 EDOTREOTIDE",       # Ga-68 dotatoc (site-made kit approvals)
    "VALDECOXIB",                      # Bextra (withdrawn 2005 — still disqualifies)
    "DABIGATRAN ETEXILATE MESYLATE",   # Pradaxa
    "CEPHALEXIN",                      # Keflex (USAN ceph- spelling)
    "CEPHRADINE",                      # Velosef (USAN ceph- spelling)
    "CEFAMANDOLE NAFATE",              # Mandol (FDA 1978, discontinued)
]

# GSRS-style active-moiety edges for the graph class (offline stand-in; the
# real pipeline reads these live from the GSRS API with an on-disk cache)
MOIETY_LINKS = [
    ("ISAVUCONAZONIUM SULFATE", "ISAVUCONAZOLE"),
    ("ISAVUCONAZONIUM", "ISAVUCONAZOLE"),
    ("METHYLENE BLUE", "METHYLTHIONINIUM"),
    ("METHYLTHIONINIUM CHLORIDE", "METHYLTHIONINIUM"),
    ("GALLIUM GA-68 EDOTREOTIDE", "EDOTREOTIDE"),
    ("MYCOPHENOLATE MOFETIL", "MYCOPHENOLIC ACID"),
    ("PARECOXIB", "VALDECOXIB"),
    ("PARECOXIB SODIUM", "VALDECOXIB"),
    ("CEFAMANDOLE NAFATE", "CEFAMANDOLE"),
]


def run_offline(with_graph: bool):
    us = StringExclusionSet()
    for ing in US_INGREDIENT_RECORD:
        us.add_ingredient(ing)
    if with_graph:
        for form, moiety_name in MOIETY_LINKS:
            us.add_moiety_link(form, moiety_name)
        us.finalize()

    hard_miss, soft, fp = [], [], []
    caught = kept = 0
    for name, why, klass in MUST_EXCLUDE:
        r = us.check(name)
        if r.verdict is Verdict.APPROVED_IN_US:
            caught += 1
        elif r.verdict is Verdict.REVIEW and klass == "graph":
            soft.append(f"  soft  {name:30} -> REVIEW ({', '.join(r.flags)})")
        else:
            hard_miss.append(f"  MISS  {name:30} -> {r.verdict.value}  [{why}]")
    for name, why in MUST_KEEP:
        r = us.check(name)
        if r.verdict is Verdict.APPROVED_IN_US:
            fp.append(f"  FALSE-EXCLUDE {name:26} matched {r.matched_us_name!r} "
                      f"via key {r.matched_key!r}")
        else:
            kept += 1
    return caught, kept, hard_miss, soft, fp


# --------------------------------------------------------------------------
# Real mode: the production code path against the real files
# --------------------------------------------------------------------------
def run_real():
    from unii import UniiIndex
    from moiety import full_keys
    from gsrs import GsrsClient, grade  # noqa: F401
    import sources

    # Same date-stamped-file resolution rdh_diff.py uses. Hardcoding
    # UNII_Names_26Feb2026.txt here meant --real mode silently tested a
    # different (older) identity index than the pipeline it claims to replay.
    from rdh_diff import _newest_unii

    raw = os.path.join(HERE, "data", "raw")
    idx = UniiIndex()
    names_path = _newest_unii("UNII_Names_")
    recs_path = _newest_unii("UNII_Records_")
    print(f"loading UNII name index ({os.path.basename(names_path)})...", flush=True)
    idx.load_names(names_path)
    idx.load_records(recs_path)
    print("building US exclusion set...", flush=True)
    us_uniis, us_moieties, st = sources.load_us_exclusion(idx, raw)
    print(f"  {st['ingredient_rows']:,} rows -> {len(us_uniis):,} UNIIs, "
          f"{len(us_moieties):,} keys", flush=True)
    g = GsrsClient()

    def classify(name):
        """Same three layers as rdh_diff.py stage 4/4b."""
        f_uniis, f_keys = idx.collect(name)
        hit = (f_uniis & us_uniis) or (f_keys & us_moieties)
        if hit:
            return "APPROVED_IN_US", f"string/unii: {sorted(hit)[0]}"
        cu, _, _ = idx.moiety_unii(name)
        if not cu:
            return "REVIEW", "unresolvable to UNII"
        def rel_hit(u, nm):
            # full identity only — see rdh_diff.rel_hit for why stripping a
            # relative's name is unsafe (colchicine-salicylate bridge)
            if u in us_uniis:
                return True
            for k in full_keys(nm):
                ru = idx.name2unii.get(k) or idx.moiety2unii.get(k)
                if (ru and ru in us_uniis) or k in us_moieties:
                    return True
            return False

        res = g.relatives(cu, wall=idx.is_counterion)
        if not res["ok"]:
            return "REVIEW", "GSRS unavailable"
        hop2 = []
        for grade_, rtype, ru, rname in res["relatives"]:
            if grade_ != "exclude":
                continue
            if rel_hit(ru, rname):
                return "APPROVED_IN_US", f"gsrs: {rtype} -> {rname}"
            hop2.append((ru, rname))
        for ru, rname in hop2[:8]:
            r2 = g.relatives(ru, wall=idx.is_counterion)
            for grade_, rtype, ru2, rname2 in r2["relatives"]:
                if grade_ != "exclude" or ru2 == cu:
                    continue
                if rel_hit(ru2, rname2):
                    return "APPROVED_IN_US", f"gsrs 2-hop via {rname}: {rname2}"
        return "NOT_IN_US", ""

    hard_miss, soft, fp = [], [], []
    caught = kept = 0
    for name, why, klass in MUST_EXCLUDE:
        v, basis = classify(name)
        if v == "APPROVED_IN_US":
            caught += 1
            print(f"  OK    {name:30} {basis}")
        elif v == "REVIEW" and klass == "graph":
            soft.append(f"  soft  {name:30} -> REVIEW ({basis})")
        else:
            hard_miss.append(f"  MISS  {name:30} -> {v}  [{why}]")
    for name, why in MUST_KEEP:
        v, basis = classify(name)
        if v == "APPROVED_IN_US":
            fp.append(f"  FALSE-EXCLUDE {name:26} via {basis}")
        else:
            kept += 1
    g.save()
    return caught, kept, hard_miss, soft, fp


def main() -> int:
    real = "--real" in sys.argv
    print("=" * 74)
    print("s.529 EXCLUSION MATCHER — ACCURACY AGAINST LABELED CASES"
          + ("  [REAL DATA]" if real else "  [offline string layer]"))
    print("=" * 74)

    worst = 0
    runs = ([("production code path + real files + GSRS", None)] if real else
            [("string layer only", False), ("string layer + moiety graph", True)])
    for label, with_graph in runs:
        if real:
            caught, kept, hard_miss, soft, fp = run_real()
        else:
            caught, kept, hard_miss, soft, fp = run_offline(with_graph)
        n_ex, n_keep = len(MUST_EXCLUDE), len(MUST_KEEP)
        print(f"\n--- {label} ---")
        print(f"  must-exclude caught : {caught}/{n_ex}   (hard recall {caught/n_ex:.0%})")
        print(f"  deferred to review  : {len(soft)}   <- flagged, not resolved")
        print(f"  must-keep retained  : {kept}/{n_keep}   (specificity {kept/n_keep:.0%})")
        print(f"  silent misses       : {len(hard_miss)}   <- ineligible drugs reaching the list")
        print(f"  wrongly excluded    : {len(fp)}   <- real candidates thrown away")
        for line in hard_miss + soft + fp:
            print(line)
        worst = max(worst, len(hard_miss) + len(fp))

    # Stereoisomer-partner layer. Pure string generation, so it runs identically
    # in both modes and needs no data files.
    from moiety import stereo_name_variants, norm as _norm
    stereo_bad = []
    for name, partner, why in MUST_REVIEW_STEREO:
        if _norm(partner) not in stereo_name_variants(name):
            stereo_bad.append(f"  MISS  {name:22} -> {partner} not generated ({why})")
    print(f"\n--- stereoisomer-partner layer ---")
    print(f"  stereo pairs found  : {len(MUST_REVIEW_STEREO)-len(stereo_bad)}"
          f"/{len(MUST_REVIEW_STEREO)}   <- must reach REVIEW, never a silent keep")
    for line in stereo_bad:
        print(line)
    worst += len(stereo_bad)

    print("\n" + "=" * 74)
    if worst == 0:
        print("PASS — no silent misses and no candidates wrongly discarded.")
    else:
        print(f"FAIL — {worst} case(s) resolved incorrectly.")
    print("=" * 74)
    return 0 if worst == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
