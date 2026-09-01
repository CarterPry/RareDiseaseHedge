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
import os, re, sys, ssl, zipfile, urllib.request, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "data", "raw")
UA = "RareDiseaseHedge/1.0 (research; carterpry@gmail.com)"

# name -> (url, local filename, kind)   kind in {zip, xlsx, bin}
#
# Every URL below was re-verified live on 2026-08-29. The UNII entries that used
# to live here are NOT here any more: see MANUAL_SOURCES.
SOURCES = {
    "ema":       ("https://www.ema.europa.eu/en/documents/report/medicines-output-medicines-report_en.xlsx",
                  "ema_med.xlsx", "xlsx"),
    "ema_orph":  ("https://www.ema.europa.eu/en/documents/report/medicines-output-orphan_designations-report_en.xlsx",
                  "ema_orph.xlsx", "xlsx"),
    # Article 57 / xEVMPD: NATIONALLY-authorised EEA products, i.e. everything
    # the centralised medicines report cannot see. 163,791 product rows,
    # 11,932 distinct active substances (measured 2026-08-29).
    "ema_art57": ("https://www.ema.europa.eu/en/documents/other/article-57-product-data_en.xlsx",
                  "ema_art57.xlsx", "xlsx"),
    "fda":       ("https://www.fda.gov/media/89850/download", "drugsatfda.zip", "zip"),
    "orangebook":("https://www.fda.gov/media/76860/download", "eob.zip", "zip"),
    "canada":    ("https://www.canada.ca/content/dam/hc-sc/documents/services/drug-product-database/ingred_ap.zip",
                  "ingred_ap.zip", "zip"),
    "canada_drug":("https://www.canada.ca/content/dam/hc-sc/documents/services/drug-product-database/drug_ap.zip",
                  "drug_ap.zip", "zip"),
    # Swissmedic renamed this list: the old zugelassene_wirkstoffe_ham /
    # Zugelassene_Wirkstoffe_HAM.xlsx path has returned 404 for some time, so
    # every "refresh" silently kept the stale local copy. Current path scraped
    # from the published list index 2026-08-29; file is "Stand vom 31.07.2026".
    "swissmedic":("https://www.swissmedic.ch/dam/swissmedic/de/dokumente/internetlisten/zugelassen_wirkstoffe.xlsx.download.xlsx/Stoffliste.xlsx",
                  "sm_stoff.xlsx", "xlsx"),
    # openFDA bulk exports, refreshed daily. marketing_category on the NDC
    # directory separates a real 505/351 approval from an OTC-monograph or
    # unapproved-marketed product; the CRL set names drugs FDA has already
    # reviewed and refused, which is both a competitor signal and proof a US
    # dossier exists.
    "openfda_ndc":("https://download.open.fda.gov/drug/ndc/drug-ndc-0001-of-0001.json.zip",
                  "openfda_ndc.zip", "zip"),
    "openfda_crl":("https://download.open.fda.gov/transparency/crl/transparency-crl-0001-of-0001.json.zip",
                  "openfda_crl.zip", "zip"),
    # Orphadata: rare-disease epidemiology. prev = point prevalence by disorder;
    # ages = average age of onset. Together they answer eligibility.py's
    # rare_under_200k and primarily_pediatric criteria for any candidate whose
    # disease resolves to an Orphanet disorder.
    "orphadata_prev":("https://www.orphadata.com/data/xml/en_product9_prev.xml",
                  "orphadata_prev.xml", "bin"),
    "orphadata_ages":("https://www.orphadata.com/data/xml/en_product9_ages.xml",
                  "orphadata_ages.xml", "bin"),
    # The UNII identity index — the join layer the whole diff depends on.
    # These are served through an AWS API Gateway that 308->302-redirects to a
    # presigned S3 URL and accepts GET ONLY: a HEAD request (curl -I) gets a
    # 403 MissingAuthenticationToken, which is easy to misread as "blocked".
    # A plain GET works. Verified 2026-08-29: 20.3 MB and 14.5 MB.
    "unii":      ("https://precision.fda.gov/uniisearch/archive/latest/UNIIs.zip",
                  "UNIIs.zip", "zip"),
    "unii_data": ("https://precision.fda.gov/uniisearch/archive/latest/UNII_Data.zip",
                  "UNII_Data.zip", "zip"),
}

# Zips whose payload must be EXTRACTED, because rdh_diff.py reads the flat files
# and not the archives. Downloading without extracting is why a fresh UNII
# release never reached the pipeline: fetch.py wrote UNIIs.zip while the diff
# went on reading a date-stamped .txt that fetch.py never produced.
#   source name -> filename prefixes to extract
EXTRACT_MEMBERS = {
    "unii":      ("UNII_Names_",),
    "unii_data": ("UNII_Records_",),
}


def _parse_unii_date(s):
    """'26Feb2026' (local filename form) or '2026-08-04' (archive form) -> date."""
    import datetime
    for fmt in ("%d%b%Y", "%Y-%m-%d"):
        try:
            return datetime.datetime.strptime(s, fmt).date()
        except (ValueError, TypeError):
            pass
    return None


ARCHIVE_LISTING = "https://precision.fda.gov/uniisearch/archive"


def unii_staleness():
    """Newest UNII release advertised on the archive page vs what is on disk.

    Kept even though the download is automated, because the diff reads whatever
    date-stamped file is present: if a refresh is skipped or fails, this is what
    turns a silently stale identity index into a visible warning.
    Returns (newest_remote:str|None, local_dates:list[str])."""
    local = sorted({m.group(1) for f in os.listdir(RAW)
                    for m in [re.match(r"UNII_(?:Names|Records)_(.+)\.txt$", f)] if m})
    newest = None
    try:
        req = urllib.request.Request(ARCHIVE_LISTING, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as r:
            html = r.read().decode("utf-8", "replace")
        dates = re.findall(r"archive/(\d{4}-\d{2}-\d{2})/UNIIs_", html)
        newest = max(dates) if dates else None
    except Exception as e:
        print(f"  [warn] could not read UNII archive listing: {type(e).__name__} {e}")
    return newest, local


def fetch_one(name):
    url, fn, kind = SOURCES[name]
    dest = os.path.join(RAW, fn)
    # Full TLS verification. The previous CERT_NONE/check_hostname=False was
    # justified in a comment as "some regulator hosts have incomplete chains";
    # re-tested 2026-08-29, all seven hosts (ema.europa.eu, fda.gov, canada.ca,
    # swissmedic.ch, precision.fda.gov, gsrs.ncats.nih.gov, download.open.fda.gov)
    # verify cleanly. Disabling verification on the inputs to an investment
    # thesis bought nothing and allowed silent substitution of every file.
    ctx = ssl.create_default_context()
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
    for member in _extract(name, dest):
        print(f"         extracted {member}")
    return True


def _extract(name, zip_path):
    """Extract the flat files rdh_diff.py actually reads. Returns member names."""
    prefixes = EXTRACT_MEMBERS.get(name)
    if not prefixes:
        return []
    out = []
    with zipfile.ZipFile(zip_path) as z:
        for m in z.namelist():
            base = os.path.basename(m)
            if not base.startswith(prefixes):
                continue
            target = os.path.join(RAW, base)
            with z.open(m) as src, open(target + ".tmp", "wb") as dst:
                while chunk := src.read(1 << 20):
                    dst.write(chunk)
            os.replace(target + ".tmp", target)
            out.append(base)
    return out


def main():
    os.makedirs(RAW, exist_ok=True)
    which = sys.argv[1:] or list(SOURCES)
    unknown = [w for w in which if w not in SOURCES]
    if unknown:
        print("unknown sources:", unknown, "\navailable:", list(SOURCES))
        return
    print(f"refreshing {len(which)} source(s) into {RAW}")
    ok = sum(fetch_one(n) for n in which)
    print(f"done — {ok}/{len(which)} refreshed.")

    newest, local = unii_staleness()
    print("\nUNII identity index (the join layer the whole diff depends on):")
    print(f"  on disk : {', '.join(local) if local else 'NONE'}")
    print(f"  newest  : {newest or 'unknown'}")
    have = max((d for d in (_parse_unii_date(x) for x in local) if d), default=None)
    want = _parse_unii_date(newest) if newest else None
    if have and want and want > have:
        print(f"  [STALE] by {(want - have).days} days — release {newest} exists. "
              f"Run: python3 pipeline/fetch.py unii unii_data")
    elif have and want:
        print("  [ok]    index is current")
    print("\nNow run: python3 pipeline/rdh_diff.py")


if __name__ == "__main__":
    main()
