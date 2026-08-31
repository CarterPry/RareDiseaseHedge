#!/usr/bin/env python3
"""
Build the data payload for the "State of Bio 2026" almanac (pipeline/report/).

Reads the pipeline's own summary.json and a compact, SEC-verified PRV
transaction table (from sources/18-prv-transaction-market.md) and writes
data.js — a single `window.BIO = {...}` object the report's charts consume.

The almanac reuses the visual design of a crypto data-almanac ("State of
Onchain"); the charts that CAN be driven by real pipeline output are (ticker,
voucher-market bars, candidate bubbles, approval map), and are labelled with a
real source. The remaining charts (stacked series, sunburst, marimekko) are
illustrative and labelled as such.

Run:  python3 pipeline/report/build_report_data.py
"""
import json, os, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
SUMMARY = os.path.join(HERE, "..", "data", "out", "summary.json")
OUT = os.path.join(HERE, "data.js")

# Approx lon/lat centroids for the regulators/countries Article 57 + the other
# loaders can surface. Only used to place bubbles on the world map.
CENTROIDS = {
    "Germany": (10.4, 51.2), "Italy": (12.6, 42.8), "France": (2.3, 46.8),
    "Portugal": (-8.2, 39.6), "Poland": (19.1, 52.1), "Spain": (-3.7, 40.2),
    "Austria": (14.5, 47.6), "Luxembourg": (6.1, 49.8), "Czech Republic": (15.5, 49.8),
    "Belgium": (4.5, 50.6), "Hungary": (19.5, 47.2), "Greece": (22.0, 39.1),
    "Netherlands": (5.3, 52.2), "Ireland": (-8.2, 53.4), "Denmark": (9.5, 56.0),
    "Sweden": (15.3, 62.0), "Finland": (25.7, 64.0), "Norway": (8.5, 61.0),
    "Slovakia": (19.7, 48.7), "Romania": (24.9, 45.9), "Bulgaria": (25.2, 42.7),
    "Croatia": (15.5, 45.1), "Slovenia": (14.8, 46.1), "Lithuania": (23.9, 55.2),
    "Latvia": (24.6, 56.9), "Estonia": (25.0, 58.6), "Cyprus": (33.4, 35.1),
    "Malta": (14.4, 35.9), "Iceland": (-18.6, 64.9), "Liechtenstein": (9.5, 47.2),
    "United Kingdom (Northern Ireland)": (-6.5, 54.6),
    "Canada": (-106.0, 56.0), "Switzerland": (8.2, 46.8), "Norway ": (8.5, 61.0),
}

# SEC-verified RPD/TD/MCM voucher sales, 2014–2026 (sources/18). Real prices.
PRV_DEALS = [
    (2014, 67.5, "RPD", "VIMIZIM", "MPS IVA"),
    (2014, 125.0, "TD", "Miltefosine", "leishmaniasis"),
    (2015, 150.0, "RPD", "CHOLBAM", "bile acid synthesis disorder"),
    (2015, 350.0, "RPD", "UNITUXIN", "neuroblastoma"),
    (2017, 125.0, "RPD", "EXONDYS 51", "Duchenne muscular dystrophy"),
    (2017, 125.0, "RPD", "BRINEURA", "CLN2 / Batten disease"),
    (2017, 130.0, "RPD", "MEPSEVII", "MPS VII / Sly syndrome"),
    (2018, 110.0, "RPD", "LUXTURNA", "RPE65 retinal dystrophy"),
    (2018, 80.0, "MCM", "TPOXX", "smallpox"),
    (2019, 105.0, "RPD", "EPIDIOLEX", "Dravet / LGS"),
    (2020, 95.0, "RPD", "ZOKINVY", "Hutchinson-Gilford progeria"),
    (2020, 105.0, "RPD", "DANYELZA", "refractory neuroblastoma"),
    (2021, 100.0, "RPD", "IMCIVREE", "POMC / LEPR obesity"),
    (2021, 110.0, "RPD", "LIVMARLI", "Alagille syndrome"),
    (2022, 110.0, "RPD", "VOXZOGO", "achondroplasia"),
    (2022, 110.0, "RPD", "ZTALMY", "CDKL5 deficiency"),
    (2022, 102.0, "RPD", "SKYSONA", "cerebral adrenoleukodystrophy"),
    (2023, 95.0, "RPD", "ZYNTEGLO", "beta-thalassemia"),
    (2023, 102.0, "RPD", "ELEVIDYS", "Duchenne muscular dystrophy"),
    (2023, 103.0, "RPD", "LYFGENIA", "sickle cell disease"),
    (2024, 158.0, "RPD", "IQIRVO", "primary biliary cholangitis"),
    (2024, 103.0, "TD", "IXCHIQ", "chikungunya"),
    (2024, 160.0, "TD", "VIMKUNYA", "chikungunya"),
    (2024, 105.0, "RPD", "XOLREMDI", "WHIM syndrome"),
    (2024, 108.0, "RPD", "OJEMDA", "pediatric low-grade glioma"),
    (2024, 150.0, "RPD", "DAYBUE", "Rett syndrome"),
    (2024, 150.0, "RPD", "KEBILIDI", "AADC deficiency"),
    (2025, 150.0, "RPD", "MIPLYFFA", "Niemann-Pick type C"),
    (2025, 155.0, "RPD", "ZEVASKYN", "recessive dystrophic EB"),
    (2025, 200.0, "RPD", "MODEYSO", "H3 K27M diffuse glioma"),
    (2026, 205.0, "RPD", "ZYCUBO", "Menkes disease"),
    (2026, 180.0, "RPD", "KRESLADI", "leukocyte adhesion deficiency-I"),
    (2026, 195.0, "RPD", "AVLAYAH", "MPS II / Hunter syndrome"),
]


def main():
    d = json.load(open(SUMMARY))
    cands = d["candidates"]
    f = d["funnel"]

    # --- per-country candidate counts (real, Article 57 + Canada/Swiss) --------
    ctry = {}
    for c in cands:
        for k in c.get("countries") or []:
            ctry[k] = ctry.get(k, 0) + 1
    countries = []
    for name, n in sorted(ctry.items(), key=lambda kv: -kv[1]):
        lon, lat = CENTROIDS.get(name, CENTROIDS.get(name.strip(), (None, None)))
        if lon is None:
            continue
        countries.append({"name": name.replace(" (Northern Ireland)", " (NI)"),
                          "n": n, "lon": lon, "lat": lat})

    # --- top candidates by EEA breadth (real) → bubbles -----------------------
    top = sorted(cands, key=lambda c: -c.get("n_countries", 0))[:40]
    bubbles = [{"name": c["name"].title(), "v": c.get("n_countries", 0) or 1,
                "orphan": c["orphan"], "area": (c.get("area") or "").split(";")[0]}
               for c in top]

    # --- EEA breadth histogram (real) → bars ----------------------------------
    buckets = [("1", 1, 1), ("2–4", 2, 4), ("5–9", 5, 9), ("10–14", 10, 14),
               ("15–19", 15, 19), ("20–24", 20, 24), ("25–30", 25, 30)]
    hist = []
    for label, lo, hi in buckets:
        n = sum(1 for c in cands if lo <= (c.get("n_countries", 0) or 0) <= hi)
        hist.append({"label": label, "n": n})

    # --- PRV market by year (real) → bars, stacked by voucher type ------------
    years = sorted({y for y, *_ in PRV_DEALS})
    types = ["RPD", "TD", "MCM"]
    prv_by_year = []
    for y in years:
        row = {"year": y}
        for t in types:
            row[t] = round(sum(p for yy, p, tt, *_ in PRV_DEALS if yy == y and tt == t), 1)
        prv_by_year.append(row)

    # headline PRV band from the most recent RPD deals
    recent = sorted([d for d in PRV_DEALS if d[2] == "RPD"], key=lambda x: -x[0])[:6]
    recent_prices = sorted(p for _, p, *_ in recent)

    today = datetime.date(2026, 8, 31)
    sunset = datetime.date(2029, 9, 30)
    months_to_sunset = (sunset.year - today.year) * 12 + (sunset.month - today.month)

    payload = {
        "generated": d.get("generated", ""),
        "snapshot": d.get("snapshot", ""),
        "headline": {
            "candidates": d["counts"]["named"],
            "orphan": d["counts"]["orphan"],
            "multi_regulator": d["counts"]["multi_regulator"],
            "dossier_only": d["counts"]["dossier_only"],
            "review": d["counts"]["review"],
            "foreign_rows": f["foreign_rows"],
            "in_us": f["in_us"],
            "months_to_sunset": months_to_sunset,
            "prv_low": recent_prices[0], "prv_high": recent_prices[-1],
            "deals": len(PRV_DEALS),
            "peak": max(p for _, p, *_ in PRV_DEALS),
        },
        "funnel": [
            {"label": "Foreign approval records", "n": f["foreign_rows"]},
            {"label": "Resolved to a UNII", "n": f["resolved"]},
            {"label": "Not in the US record", "n": f["resolved"] - f["in_us"]},
            {"label": "Small molecule, named", "n": f["named_drug"] + f.get("no_authorisation_in_loaded_registers", 0)},
            {"label": "Approved abroad, never US", "n": f["named_drug"]},
        ],
        "countries": countries,
        "bubbles": bubbles,
        "breadthHist": hist,
        "prvDeals": [{"year": y, "price": p, "type": t, "drug": dr, "disease": dz}
                     for y, p, t, dr, dz in PRV_DEALS],
        "prvByYear": prv_by_year,
        "prvTypes": types,
    }

    with open(OUT, "w") as fh:
        fh.write("/* Generated by build_report_data.py — do not edit by hand. */\n")
        fh.write("window.BIO = " + json.dumps(payload, indent=1) + ";\n")
    print(f"wrote {OUT}  ({len(countries)} countries, {len(bubbles)} bubbles, "
          f"{len(PRV_DEALS)} PRV deals, {d['counts']['named']} candidates)")


if __name__ == "__main__":
    main()
