#!/usr/bin/env python3
"""
Live enrichment for the candidate list. Adds, at build time, real-world signals
that the offline diff cannot see — then embeds them so the dashboard stays a
static file.

Per candidate (cached in data/cache/enrich.json, keyed by UNII):
  - pubmed   : PubMed hits for the drug in a rare/pediatric context (evidence signal)
  - trials   : ClinicalTrials.gov v2 study count (is anyone already trialing it?)
  - us_orphan: does the drug already hold a US FDA orphan designation? (a
               "someone may already have rights here" signal — best-effort;
               'unknown' on any failure, never a false 'clear')

Global competitor monitor (top-level 'monitor' block):
  - fedreg   : live Federal Register RPD-PRV ledger (count + most recent)
  - edgar    : recent SEC filers mentioning "rare pediatric disease designation"
               (the leading-indicator competitor channel from the research)

All network calls are wrapped, throttled and cached. A failure degrades to
'unknown'/empty and keeps going — the build never breaks on a flaky API.

Run:  python3 pipeline/enrich.py            # enrich all (uses cache)
      python3 pipeline/enrich.py --limit 5  # test on first 5
      python3 pipeline/enrich.py --fresh     # ignore cache
"""
import json, os, sys, time, ssl, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "data", "out")
SUMMARY = os.path.join(OUT, "summary.json")
CACHE_DIR = os.path.join(HERE, "data", "cache")
CACHE = os.path.join(CACHE_DIR, "enrich.json")
UA = "RareDiseaseHedge/1.0 (research; carterpry@gmail.com)"
CTX = ssl.create_default_context()

def get(url, headers=None, timeout=25):
    h = {"User-Agent": UA, "Accept": "application/json"}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
        return r.read()

def get_json(url, **kw):
    return json.loads(get(url, **kw))

def q(s):
    return urllib.parse.quote(s)

# ---------------------------------------------------------------- per-drug
def pubmed_count(name):
    """PubMed hits for the drug (clean moiety name) in a rare/pediatric context."""
    term = f'{name}[tiab] AND (rare disease[tiab] OR pediatric[tiab] OR paediatric[tiab] OR orphan[tiab] OR congenital[tiab])'
    url = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=json&retmax=0"
           f"&tool=raredduxhedge&email=carterpry@gmail.com&term={q(term)}")
    d = get_json(url)
    return int(d["esearchresult"]["count"])

def trials_count(name):
    """ClinicalTrials.gov v2 study count with the drug as INTERVENTION (query.intr
    is far more precise than query.term, which OR-matches salt tokens like
    'hydrochloride' into hundreds of unrelated trials)."""
    url = f"https://clinicaltrials.gov/api/v2/studies?query.intr={q(name)}&countTotal=true&pageSize=1"
    d = get_json(url)
    return int(d.get("totalCount", 0))

# NOTE: FDA OOPD (orphan designations) is NOT reliably machine-queryable — it
# returns 403/503/form pages to automation (confirmed 2026-08, matches sources
# 01/15/19). We therefore do NOT assert a US-orphan boolean, which would risk a
# false 'clear'. US-orphan-conflict is surfaced in the UI as a mandatory MANUAL
# check. This function is intentionally honest rather than wrong.
def us_orphan(name):
    return "unknown"

# ---------------------------------------------------------------- global monitor
def fedreg_prv():
    try:
        url = ("https://www.federalregister.gov/api/v1/documents.json?per_page=5&order=newest"
               "&conditions%5Bterm%5D=" + q("rare pediatric disease priority review voucher"))
        d = get_json(url)
        recent = [{"title": (x.get("title") or "")[:120], "date": x.get("publication_date")}
                  for x in (d.get("results") or [])[:5]]
        return {"count": d.get("count", 0), "recent": recent}
    except Exception as e:
        return {"count": None, "recent": [], "error": str(e)}

def edgar_competitors():
    try:
        url = ('https://efts.sec.gov/LATEST/search-index?q=%22rare+pediatric+disease+designation%22'
               '&forms=8-K,10-K,10-Q&dateRange=custom&startdt=2025-01-01&enddt=2026-12-31')
        d = get_json(url, headers={"Accept": "application/json"})
        hits = d.get("hits", {})
        total = hits.get("total", {}).get("value")
        filers = []
        seen = set()
        for h in hits.get("hits", [])[:25]:
            src = h.get("_source", {})
            for nm in src.get("display_names", []):
                nm = nm.split(" (")[0]
                if nm not in seen:
                    seen.add(nm)
                    filers.append({"name": nm, "form": src.get("root_form") or src.get("file_type"),
                                   "date": src.get("file_date")})
        return {"total": total, "filers": filers[:15]}
    except Exception as e:
        return {"total": None, "filers": [], "error": str(e)}

# ---------------------------------------------------------------- Orphadata
# Local, deterministic, no network: resolve each row's disease (EMA therapeutic
# area / indication text) to an Orphanet disorder and attach rarity + age-of-onset.
# This answers eligibility.py's rare_under_200k and primarily_pediatric criteria
# for the rows that carry a disease name. Coverage is intentionally low and
# precision-first — a NON-match is the correct answer for a common-disease drug.
def enrich_orphadata(data):
    try:
        from orphadata import OrphaIndex, rarity, onset
    except Exception as e:
        print(f"  [skip] orphadata: {type(e).__name__} {e}")
        return
    idx = OrphaIndex()
    n = idx.load(os.path.join(HERE, "data", "raw"))
    if not n:
        print("  [skip] orphadata: no XML in data/raw (run fetch.py orphadata_prev orphadata_ages)")
        return
    matched = 0
    buckets = ["candidates", "dossier_only", "review", "unnamed"]
    for b in buckets:
        for c in data.get(b, []):
            rec = idx.resolve(c.get("area"), c.get("indication"))
            if not rec:
                c["orpha"] = None
                continue
            rv, rev = rarity(rec)
            ov, oev = onset(rec)
            c["orpha"] = {"code": rec["orpha"], "name": rec["name"],
                          "rarity": rv, "rarity_evidence": rev,
                          "us_prevalence_est": rec.get("us_estimate"),
                          "onset": ov, "onset_evidence": oev}
            matched += 1
    data["orphadata"] = {"disorders_loaded": n, "candidates_matched": matched}
    print(f"  orphadata: {n:,} disorders loaded, {matched} rows matched to a disease")


# ---------------------------------------------------------------- EU orphan designations
# Local, no network. ema_orph.xlsx is the EMA orphan-designation register (fetched
# by fetch.py as ema_orph). A candidate carrying an EU orphan designation is a
# strong rare-disease signal AND a competitor signal (someone pursued it in the
# EU). Matched on normalised INN — orphan designations and candidate moieties are
# both INN-named, so exact-INN matching is high precision.
def _norm_name(s):
    import re
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def enrich_eu_orphan(data):
    try:
        import openpyxl
    except Exception:
        return
    path = os.path.join(HERE, "data", "raw", "ema_orph.xlsx")
    if not os.path.exists(path):
        print("  [skip] eu_orphan: ema_orph.xlsx not present")
        return
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb.active
    by_sub = {}
    started = False
    for r in ws.iter_rows(values_only=True):
        v = [("" if c is None else str(c)) for c in r]
        if not started:
            if v and v[0].strip() == "Medicine name":
                started = True
            continue
        if len(v) < 7:
            continue
        sub = _norm_name(v[2])
        if not sub:
            continue
        by_sub.setdefault(sub, {"use": v[4].strip(), "status": v[6].strip(),
                                "number": v[5].strip()})
    wb.close()
    matched = 0
    for b in ("candidates", "dossier_only", "review", "unnamed"):
        for c in data.get(b, []):
            hit = by_sub.get(_norm_name(c.get("moiety"))) or by_sub.get(_norm_name(c.get("name")))
            if hit:
                c["eu_orphan_designation"] = hit
                matched += 1
    print(f"  eu_orphan: {len(by_sub):,} EU designations, {matched} candidate rows flagged")


# ---------------------------------------------------------------- US Complete Response Letters
# Local, no network. openfda_crl.zip is FDA's CRL disclosure set. A candidate that
# already has a US CRL means a sponsor filed and FDA refused — the drug is not an
# untouched opportunity (found: govorestat, tolebrutinib). Whole-word name match
# against the letter text/company/application fields.
def enrich_crl(data):
    import re, zipfile
    path = os.path.join(HERE, "data", "raw", "openfda_crl.zip")
    if not os.path.exists(path):
        print("  [skip] crl: openfda_crl.zip not present")
        return
    with zipfile.ZipFile(path) as z:
        recs = json.load(z.open([n for n in z.namelist() if n.endswith(".json")][0])).get("results") or []
    blobs = [(json.dumps(r).lower(), r) for r in recs]
    matched = 0
    for b in ("candidates", "dossier_only", "review"):
        for c in data.get(b, []):
            nm = (c.get("moiety") or c.get("name") or "").lower()
            if len(nm) < 5:
                continue
            rx = re.compile(r"(^|[^a-z0-9])" + re.escape(nm) + r"([^a-z0-9]|$)")
            for blob, r in blobs:
                if rx.search(blob):
                    appl = r.get("application_number")
                    c["us_crl"] = {"application": appl[0] if isinstance(appl, list) else appl,
                                   "date": r.get("letter_date") or r.get("action_date")}
                    matched += 1
                    break
    print(f"  crl: {len(recs):,} letters, {matched} candidate rows flagged as already US-filed-and-refused")


# ---------------------------------------------------------------- driver
def main():
    fresh = "--fresh" in sys.argv
    limit = None
    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])

    with open(SUMMARY, encoding="utf-8") as fh:
        data = json.load(fh)
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache = {}
    if os.path.exists(CACHE) and not fresh:
        cache = json.load(open(CACHE, encoding="utf-8"))

    cands = data["candidates"]
    todo = cands[:limit] if limit else cands
    print(f"enriching {len(todo)} candidates (cache has {len(cache)})")
    n_fetched = 0
    for i, c in enumerate(todo, 1):
        key = c["unii"]
        if key in cache and not fresh:
            e = cache[key]
        else:
            # query on the CLEAN moiety name, not the salt form (the salt token
            # both misses PubMed and inflates trial counts)
            name = (c.get("moiety") or c["name"]).lower()
            e = {}
            try: e["pubmed"] = pubmed_count(name)
            except Exception: e["pubmed"] = None
            time.sleep(0.34)                       # NCBI: <=3 req/s
            try: e["trials"] = trials_count(name)
            except Exception: e["trials"] = None
            time.sleep(0.2)
            e["us_orphan"] = us_orphan(name)
            cache[key] = e
            n_fetched += 1
            if n_fetched % 10 == 0:
                json.dump(cache, open(CACHE, "w"), indent=1)   # checkpoint
                print(f"  {i}/{len(todo)}  {name[:28]:30} pm={e['pubmed']} ct={e['trials']} orph={e['us_orphan']}")
        c["pubmed"] = e.get("pubmed")
        c["trials"] = e.get("trials")
        c["us_orphan"] = e.get("us_orphan")
    json.dump(cache, open(CACHE, "w"), indent=1)

    if not limit:
        enrich_orphadata(data)
        enrich_eu_orphan(data)
        enrich_crl(data)
        print("fetching global competitor monitor...")
        data["monitor"] = {"fedreg": fedreg_prv(), "edgar": edgar_competitors(),
                           "as_of": time.strftime("%Y-%m-%d %H:%M")}
        json.dump(data, open(SUMMARY, "w"), indent=1)
        print(f"  Federal Register PRV docs: {data['monitor']['fedreg'].get('count')}")
        print(f"  EDGAR RPD-designation filers: {data['monitor']['edgar'].get('total')}")
        print(f"wrote enriched summary.json ({n_fetched} newly fetched, rest cached)")
    else:
        print(f"test run ({n_fetched} fetched) — summary.json NOT overwritten (use full run)")


if __name__ == "__main__":
    main()
