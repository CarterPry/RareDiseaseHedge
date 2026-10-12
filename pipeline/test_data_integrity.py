#!/usr/bin/env python3
"""
Post-build integrity assertions against data/out/summary.json.

test_accuracy.py covers the MATCHER. This covers the OUTPUT and the enrichment/
scoring layers that the matcher harness never touched — the gaps the 2026-08
platform audit flagged as silently breakable on a data refresh. Run after
`enrich.py`. Exit non-zero on any regression so CI/`make check` catches it.
"""
from __future__ import annotations
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SUMMARY = os.path.join(HERE, "data", "out", "summary.json")


def main():
    d = json.load(open(SUMMARY))
    cands = d["candidates"]
    fails, notes = [], []

    def check(cond, msg):
        (notes if cond else fails).append(("ok  " if cond else "FAIL") + " " + msg)

    # ---- shape ----
    check(len(cands) > 0, f"candidate list is non-empty ({len(cands)})")
    check(d["counts"]["named"] == len(cands),
          f"counts.named ({d['counts']['named']}) == len(candidates) ({len(cands)})")

    # ---- every foreign register contributed a plausible row count ----
    # (a file that downloads but parses to 0 rows is otherwise only a WARNING;
    # 306/338 candidates come from Art57 alone, so an empty Art57 would publish
    # ~32 candidates with a green run). Floors are ~85% of the 2026-10 counts.
    rbs = (d.get("funnel") or {}).get("rows_by_source") or {}
    for src, floor in [("EMA", 2000), ("EU national (Art57)", 10000),
                       ("Health Canada", 600), ("Swissmedic", 2500), ("PMDA-JP", 200)]:
        check(rbs.get(src, 0) >= floor, f"{src} rows >= {floor} (got {rbs.get(src, 0)})")
    check("MISSING" not in (d.get("snapshot") or ""), f"no register MISSING in snapshot: {d.get('snapshot')}")

    # ---- every candidate is genuinely never-US (foreign_status not a non-approval) ----
    bad_status = [c["name"] for c in cands if c.get("foreign_status") == "never_authorised"]
    check(not bad_status, f"no candidate is 'never_authorised' (dossier-only leak): {bad_status[:5]}")

    # ---- scoring safety: the 'sma' substring bug must stay fixed ----
    # aumolertinib (adult NSCLC) must NOT read as pediatric via a substring hit
    aum = next((c for c in cands if c["name"] == "AUMOLERTINIB"), None)
    if aum:
        text = ((aum.get("indication") or "") + " " + (aum.get("area") or "") + " "
                + (aum.get("disease_terms") or "")).lower()
        # whole-word 'sma' must not be present (it was hitting 'non-small cell')
        check(not re.search(r"(^|[^a-z0-9])sma([^a-z0-9]|$)", text),
              "aumolertinib text has no whole-word 'sma' (NSCLC substring bug)")

    # ---- Phase 2: disease coverage materially above the pre-ChEMBL floor ----
    with_disease = sum(1 for c in cands
                       if c.get("area") or c.get("indication") or c.get("disease_terms"))
    check(with_disease >= 100,
          f"candidates with a disease name >= 100 (got {with_disease}; was ~24 pre-ChEMBL)")

    # ---- Orphadata precision: rare matches should be plausible, not zero/huge ----
    orpha_rare = [c["name"] for c in cands
                  if (c.get("orpha") or {}).get("rarity") == "rare"]
    check(0 < len(orpha_rare) <= 40,
          f"Orphanet 'rare' matches in a sane band 1-40 (got {len(orpha_rare)}: {orpha_rare[:6]})")

    # ---- Phase 3: eligibility present and never falsely 'eligible' ----
    have_elig = sum(1 for c in cands if c.get("eligibility"))
    check(have_elig == len(cands), f"every candidate has an eligibility assessment ({have_elig}/{len(cands)})")
    cleared = [c["name"] for c in cands
               if (c.get("eligibility") or {}).get("verdict") == "ELIGIBLE_ON_SCREENED_CRITERIA"]
    check(not cleared, f"no candidate is auto-'ELIGIBLE' (screen must never clear): {cleared[:5]}")
    # the exclusion criterion must be PASS for a candidate (it is never-US by construction)
    ex_fail = [c["name"] for c in cands
               if any(cr["key"] == "no_prior_us_active_moiety" and cr["status"] != "PASS"
                      for cr in (c.get("eligibility") or {}).get("criteria", []))]
    check(not ex_fail, f"exclusion criterion is PASS for all candidates: {ex_fail[:5]}")

    # ---- signals wired (Phase 1) ----
    check(any(c.get("eu_orphan_designation") for c in cands), "EU orphan designations wired")
    check(any(c.get("us_crl") for c in d["candidates"] + d.get("dossier_only", [])),
          "US CRL signal wired")

    print("\n".join(notes))
    if fails:
        print("\n" + "\n".join(fails))
        print(f"\nDATA INTEGRITY: FAIL ({len(fails)} issue(s))")
        return 1
    print(f"\nDATA INTEGRITY: PASS ({len(notes)} checks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
