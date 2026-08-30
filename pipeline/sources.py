"""
Source loaders for the candidate-discovery diff.

LEFT side (foreign approvals): EMA centralised, Health Canada DPD, Swissmedic,
PMDA FY (best-effort — katakana needs a transliteration layer, flagged).
RIGHT side (US exclusion set): Drugs@FDA + Orange Book active ingredients.

Each foreign loader yields dicts:
  {substance, source, status, orphan, raw}
The US loader returns (us_uniis:set, us_moiety_names:set, raw_ingredient_count).

Provenance and schemas verified live 2026-08-06 against the actual files;
see sources/00-CANDIDATE-DISCOVERY-METHOD.md and _recovered/MINED-drug-data-sources.md.
"""
from __future__ import annotations
import csv, io, os, zipfile
import openpyxl
from unii import UniiIndex, split_ingredients, moiety_key


# --------------------------------------------------------------- US exclusion
def load_us_exclusion(idx: UniiIndex, raw: str):
    """Union of Drugs@FDA Products.txt ActiveIngredient and Orange Book Ingredient,
    canonicalized to ALL resolvable UNIIs plus ALL string key variants (see
    UniiIndex.collect). This is the set a foreign moiety must be ABSENT from to
    count as never-approved-in-US. Collecting every variant — salt UNII, base
    UNII, stripped key, canonicalised-counterion key, acid/-ate stem — on BOTH
    sides is what makes salt-vs-base, spelling-variant and INN-vs-USAN
    differences collapse correctly. The single-canonical-key version of this
    measured 12/19 silent misses on labeled US-approved drugs (test_accuracy.py)."""
    us_moiety_uniis: set[str] = set()
    us_moieties: set[str] = set()
    n_ingredients = 0
    unmatched = 0

    def ingest(ing):
        nonlocal n_ingredients, unmatched
        n_ingredients += 1
        uniis, keyset = idx.collect(ing)
        if uniis:
            us_moiety_uniis.update(uniis)
        else:
            unmatched += 1
        us_moieties.update(keyset)

    # Drugs@FDA — tab-delimited, ActiveIngredient is column index 6
    with zipfile.ZipFile(os.path.join(raw, "drugsatfda.zip")) as z:
        with z.open("Products.txt") as f:
            rd = csv.reader(io.TextIOWrapper(f, "utf-8", errors="replace"), delimiter="\t")
            header = next(rd, None)
            ai_col = header.index("ActiveIngredient") if header and "ActiveIngredient" in header else 6
            for row in rd:
                if len(row) <= ai_col:
                    continue
                for ing in split_ingredients(row[ai_col]):
                    ingest(ing)

    # Orange Book — '~'-delimited, Ingredient is column 0
    with zipfile.ZipFile(os.path.join(raw, "eob.zip")) as z:
        with z.open("products.txt") as f:
            rd = csv.reader(io.TextIOWrapper(f, "utf-8", errors="replace"), delimiter="~")
            header = next(rd, None)
            for row in rd:
                if not row:
                    continue
                for ing in split_ingredients(row[0]):
                    ingest(ing)

    # Manual supplement: moieties with a real US approval that the NDA-based bulk
    # files omit — withdrawn-before-electronic-record and pre-1938/DESI drugs.
    # Each is a verified fact, not a heuristic; kept small and cited pending a
    # proper 21 CFR 216.24 / DESI feed (see README limitations #1). A withdrawn
    # approval still disqualifies under s.529 (the moiety was once approved).
    US_WITHDRAWN_SUPPLEMENT = [
        "betahistine",   # Serc — FDA NDA approved 1966, withdrawn 1972 (DESI/efficacy)
    ]
    for ing in US_WITHDRAWN_SUPPLEMENT:
        ingest(ing)

    return us_moiety_uniis, us_moieties, {"ingredient_rows": n_ingredients, "unmatched": unmatched}


# --------------------------------------------------------------- EMA (EU centralised)
# EMA "Medicine status" values that mean the product NEVER held a marketing
# authorisation. The medicines report is an EPAR index, not an approval list: it
# also carries applications that were withdrawn before opinion, refused outright,
# or that only have a CHMP opinion pending an EC decision. Counting those as
# "approved abroad" is what made 33 of 67 headline candidates non-approvals
# (measured 2026-08-29).
EMA_NEVER_AUTHORISED = {
    "application withdrawn", "refused", "opinion",
    "withdrawn from rolling review", "opinion under re-examination",
}
# ...and the values that mean it WAS authorised and later lost the licence. A
# lapsed or withdrawn authorisation is still a real prior approval by a stringent
# regulator, so it stays in the approved-abroad population.
EMA_PREVIOUSLY_AUTHORISED = {
    "withdrawn", "lapsed", "expired", "revoked", "suspended",
}


def load_ema(raw: str):
    """ema_med.xlsx: header at row 9; active substance col 7, INN col 6,
    status col 3, orphan col 23, marketing-authorisation date col 31.
    Human medicines only.

    Each row is labelled with its true regulatory standing in `foreign_status`:
    authorised / previously_authorised / never_authorised. The textual status is
    authoritative; the marketing-authorisation date (col 31, the EC decision) is
    used only to classify a status value we do not recognise, so a future added
    status cannot silently become an "approval". The two measures agree on all but
    9 of 2,290 human rows, and every disagreement is a blank date on a genuinely
    authorised product rather than a layout change — so the date alone must not
    override an explicit status.

    Never-authorised rows are NOT discarded: a refused or withdrawn application
    still means a full dossier and human clinical data exist, which is the
    feasibility signal this pipeline is really after. They are carried with an
    honest label so rdh_diff.py can report them separately instead of counting
    them as foreign approvals.
    """
    path = os.path.join(raw, "ema_med.xlsx")
    if not os.path.exists(path):
        return []
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb.active
    out = []
    header_seen = False
    for r in ws.iter_rows(values_only=True):
        vals = [("" if c is None else str(c)) for c in r]
        if not header_seen:
            if any("Active substance" in v for v in vals):
                header_seen = True
            continue
        if len(vals) < 24:
            continue
        category = vals[0].strip()
        status = vals[3].strip()
        inn = vals[6].strip()
        active = vals[7].strip()
        area = vals[8].strip() if len(vals) > 8 else ""            # Therapeutic area (MeSH)
        atc = vals[11].strip() if len(vals) > 11 else ""           # ATC code (human)
        indication = vals[15].strip() if len(vals) > 15 else ""    # Therapeutic indication
        approved = vals[31].strip() if len(vals) > 31 else ""      # Marketing authorisation date
        orphan = vals[23].strip().lower() in ("yes", "true", "1")
        substance = active or inn
        # Only human medicines. The report also carries Veterinary and (rarely)
        # Herbal categories; neither is a 505(b)(1) repurposing candidate.
        if not substance or not category.lower().startswith("human"):
            continue

        s = status.lower()
        if s in EMA_NEVER_AUTHORISED:
            fstatus = "never_authorised"
        elif s in EMA_PREVIOUSLY_AUTHORISED:
            fstatus = "previously_authorised"
        elif s == "authorised":
            fstatus = "authorised"
        else:
            # unrecognised status — fall back to the EC decision date, and treat
            # "no date" as not-an-approval so a new status value cannot leak in
            fstatus = "authorised" if approved else "never_authorised"

        out.append({"substance": substance, "source": "EMA",
                    "status": status, "orphan": orphan, "raw": inn or active,
                    "area": area, "atc": atc, "indication": indication,
                    "approved": approved, "foreign_status": fstatus})
    wb.close()
    return out


# --------------------------------------------------------------- Health Canada DPD
def _canada_drug_meta(raw: str):
    """DRUG_CODE -> (class, product_categorization) from drug_ap.txt.
    class is Human / Veterinary / Disinfectant / Radiopharmaceutical;
    product_categorization exposes OTC-monograph buckets ('CAT IV - ...',
    'LS - ...'). Optional file: if absent, every row is treated as plain human."""
    path = os.path.join(raw, "drug_ap.zip")
    meta = {}
    if not os.path.exists(path):
        return meta
    with zipfile.ZipFile(path) as z:
        name = [n for n in z.namelist() if n.endswith(".txt")][0]
        with z.open(name) as f:
            for row in csv.reader(io.TextIOWrapper(f, "latin-1", errors="replace")):
                if len(row) > 2:
                    meta[row[0]] = (row[2].strip(), row[1].strip())
    return meta


def _is_otc_monograph(cat: str) -> bool:
    """Canadian OTC-monograph product categories: Category IV monographs and
    Labelling Standards (sunscreens, antiseptics, laxatives, OTC decongestants,
    athlete's-foot treatments, ...). Not 505/351-type approvals — they pollute
    the 'never US-approved' test and are not repurposing candidates."""
    c = cat.upper()
    return c.startswith("CAT ") or c.startswith("LS -") or c.startswith("LS-")


def load_canada(raw: str):
    """ingred_ap.txt (inside ingred_ap.zip): quoted CSV, DRUG_CODE in col 0,
    ingredient name in col 2. 'ap' = approved-products subset.

    Joined against the DPD drug table (drug_ap.zip) so we keep ONLY genuine human
    prescription approvals: a substance is retained iff it has at least one
    Human, non-OTC-monograph product row AND no OTC-monograph row at all. This
    drops (a) veterinary/disinfectant/radiopharmaceutical products and (b) the
    OTC-monograph noise (sunscreen filters, antiseptics, laxatives, decongestants)
    that otherwise appear as false 'never US-approved' candidates. If the drug
    table is missing, it degrades to the old behaviour (all rows kept)."""
    path = os.path.join(raw, "ingred_ap.zip")
    if not os.path.exists(path):
        return []
    meta = _canada_drug_meta(raw)
    contexts = {}   # substance -> list of (class, categorization)
    with zipfile.ZipFile(path) as z:
        name = [n for n in z.namelist() if n.endswith(".txt")][0]
        with z.open(name) as f:
            rd = csv.reader(io.TextIOWrapper(f, "latin-1", errors="replace"))
            for row in rd:
                if len(row) < 3:
                    continue
                ing = row[2].strip()
                if not ing:
                    continue
                cls, cat = meta.get(row[0], ("Human", "")) if meta else ("Human", "")
                contexts.setdefault(ing, []).append((cls, cat))
    out = []
    for ing, ctx in contexts.items():
        has_human_rx = any(cls == "Human" and not _is_otc_monograph(cat) for cls, cat in ctx)
        has_otc = any(_is_otc_monograph(cat) for _, cat in ctx)
        if not (has_human_rx and not has_otc):
            continue
        out.append({"substance": ing, "source": "Health Canada",
                    "status": "approved", "orphan": False, "raw": ing,
                    "foreign_status": "authorised"})
    return out


# --------------------------------------------------------------- Swissmedic
def load_swissmedic(raw: str):
    """sm_stoff.xlsx = 'Zugelassene Wirkstoffe' (approved active substances).
    Header row has 'Wirkstoff / Principe actif' in col 0, HAM (human) category in
    col 1, TAM (veterinary) in col 2. Names are Latin pharmacopoeial genitives
    ('abacaviri sulfas'), which resolve to UNII only partially — reported honestly
    in the funnel. Keep human rows (col 1 non-empty)."""
    path = os.path.join(raw, "sm_stoff.xlsx")
    if not os.path.exists(path):
        return []
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb.active
    out = []
    started = False
    for r in ws.iter_rows(values_only=True):
        vals = [("" if c is None else str(c)) for c in r]
        if not started:
            if vals and "wirkstoff" in vals[0].lower():
                started = True
            continue
        if not vals or not vals[0].strip():
            continue
        human = len(vals) > 1 and vals[1].strip() != ""
        if not human:
            continue  # skip veterinary-only substances
        ing = vals[0].strip()
        out.append({"substance": ing, "source": "Swissmedic",
                    "status": "approved", "orphan": False, "raw": ing,
                    "foreign_status": "authorised"})
    wb.close()
    return out


# --------------------------------------------------------------- PMDA (Japan, best-effort)
def load_pmda(raw: str):
    """pmda_fy2025.xlsx: active ingredient in Japanese katakana (col index 5,
    '成分名'). Katakana->Latin transliteration is not implemented, so these
    resolve to UNII only if the UNII Names index happens to carry the JP synonym.
    Returned so the funnel can report Japan coverage honestly, NOT as validated
    candidates. See method doc 1.1 (transliteration is the biggest single tax)."""
    path = os.path.join(raw, "pmda_fy2025.xlsx")
    if not os.path.exists(path):
        return []
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb.active
    out = []
    started = False
    for r in ws.iter_rows(values_only=True):
        vals = [("" if c is None else str(c)) for c in r]
        # header cell is '成  分  名' with full-width spaces -> strip them before matching
        if not started:
            if any("成分名" in v.replace("　", "").replace(" ", "") for v in vals):
                started = True
            continue
        if len(vals) < 6:
            continue
        ing = vals[5].split("\n")[0].strip().replace("　", " ")
        # drop the underline annotation marker for new active ingredients
        if ing:
            out.append({"substance": ing, "source": "PMDA-JP",
                        "status": "approved", "orphan": False, "raw": ing,
                        "needs_translit": True, "foreign_status": "authorised"})
    wb.close()
    return out
