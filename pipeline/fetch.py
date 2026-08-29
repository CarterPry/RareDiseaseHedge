#!/usr/bin/env python3
"""
Refresh the pipeline's source inputs from their live URLs.

Downloads current versions of each bulk source into pipeline/data/raw/. Every
download is atomic and validated: it fetches to a .tmp file, checks it is
non-trivial and (for zips) a valid archive, and only then replaces the existing
file. A failed or dead URL leaves the previous good copy untouched — so a bad
refresh never corrupts the working data.

URLs verified in sources/00-CANDIDATE-DISCOVERY-METHOD.md and
sources/_recovered/MINED-drug-data-sources.md.

Run:  python3 pipeline/fetch.py            # refresh all
      python3 pipeline/fetch.py ema fda    # refresh only named sources
"""
import os, sys, ssl, zipfile, urllib.request, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "data", "raw")
UA = "RareDiseaseHedge/1.0 (research; carterpry@gmail.com)"

# name -> (url, local filename, kind)   kind in {zip, xlsx, bin}
SOURCES = {
    "ema":       ("https://www.ema.europa.eu/en/documents/report/medicines-output-medicines-report_en.xlsx",
                  "ema_med.xlsx", "xlsx"),
    "ema_orph":  ("https://www.ema.europa.eu/en/documents/report/medicines-output-orphan_designations-report_en.xlsx",
                  "ema_orph.xlsx", "xlsx"),
    "fda":       ("https://www.fda.gov/media/89850/download", "drugsatfda.zip", "zip"),
    "orangebook":("https://www.fda.gov/media/76860/download", "eob.zip", "zip"),
    "canada":    ("https://www.canada.ca/content/dam/hc-sc/documents/services/drug-product-database/ingred_ap.zip",
                  "ingred_ap.zip", "zip"),
    "canada_drug":("https://www.canada.ca/content/dam/hc-sc/documents/services/drug-product-database/drug_ap.zip",
                  "drug_ap.zip", "zip"),
    "unii":      ("https://precision.fda.gov/uniisearch/archive/latest/UNIIs.zip", "UNIIs.zip", "zip"),
    "unii_data": ("https://precision.fda.gov/uniisearch/archive/latest/UNII_Data.zip", "UNII_Data.zip", "zip"),
    "swissmedic":("https://www.swissmedic.ch/dam/swissmedic/de/dokumente/internetlisten/zugelassene_wirkstoffe_ham.xlsx.download.xlsx/Zugelassene_Wirkstoffe_HAM.xlsx",
                  "sm_stoff.xlsx", "xlsx"),
}


def fetch_one(name):
    url, fn, kind = SOURCES[name]
    dest = os.path.join(RAW, fn)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE  # some regulator hosts have incomplete chains
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    try:
        with urllib.request.urlopen(req, timeout=60, context=ctx) as r:
            data = r.read()
    except Exception as e:
        print(f"  [skip] {name}: {type(e).__name__} {e} — kept existing")
        return False
    if len(data) < 2000:
        print(f"  [skip] {name}: response too small ({len(data)}b) — kept existing")
        return False
    tmp = dest + ".tmp"
    with open(tmp, "wb") as fh:
        fh.write(data)
    if kind == "zip" or (kind == "xlsx"):  # xlsx is a zip container too
        if not zipfile.is_zipfile(tmp):
            os.remove(tmp)
            print(f"  [skip] {name}: not a valid archive — kept existing")
            return False
    os.replace(tmp, dest)
    print(f"  [ok]   {name}: {len(data)//1024} KB -> {fn}")
    return True


def main():
    os.makedirs(RAW, exist_ok=True)
    which = sys.argv[1:] or list(SOURCES)
    unknown = [w for w in which if w not in SOURCES]
    if unknown:
        print("unknown sources:", unknown, "\navailable:", list(SOURCES))
        return
    print(f"refreshing {len(which)} source(s) into {RAW}")
    ok = sum(fetch_one(n) for n in which)
    print(f"done — {ok}/{len(which)} refreshed. Now run: python3 pipeline/rdh_diff.py")


if __name__ == "__main__":
    main()
