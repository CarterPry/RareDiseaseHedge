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
    canonicalized to MOIETY UNIIs (plus moiety-name keys as a backstop). This is
    the set a foreign moiety must be ABSENT from to count as never-approved-in-US.
    Using moiety UNIIs — not raw UNIIs — is what makes salt-vs-base and INN-vs-USAN
    differences collapse correctly (see UniiIndex.moiety_unii)."""
    us_moiety_uniis: set[str] = set()
    us_moieties: set[str] = set()
    n_ingredients = 0
    unmatched = 0

    def ingest(ing):
        nonlocal n_ingredients, unmatched
        n_ingredients += 1
        cu, mk, tier = idx.moiety_unii(ing)
        if cu:
            us_moiety_uniis.add(cu)
        else:
            unmatched += 1
        if mk:
            us_moieties.add(mk)

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

    return us_moiety_uniis, us_moieties, {"ingredient_rows": n_ingredients, "unmatched": unmatched}


# --------------------------------------------------------------- EMA (EU centralised)
def load_ema(raw: str):
    """ema_med.xlsx: header at row 9; active substance col 7, INN col 6,
    status col 3, orphan col 23. Human medicines only."""
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
        orphan = vals[23].strip().lower() in ("yes", "true", "1")
        substance = active or inn
        if not substance or category.lower().startswith("veterinary"):
            continue
        out.append({"substance": substance, "source": "EMA",
                    "status": status, "orphan": orphan, "raw": inn or active})
    wb.close()
    return out


# --------------------------------------------------------------- Health Canada DPD
def load_canada(raw: str):
    """ingred_ap.txt (inside ingred_ap.zip): quoted CSV, ingredient name in col 3
    (index 2). 'ap' = approved-products subset."""
    path = os.path.join(raw, "ingred_ap.zip")
    if not os.path.exists(path):
        return []
    seen = set()
    out = []
    with zipfile.ZipFile(path) as z:
        name = [n for n in z.namelist() if n.endswith(".txt")][0]
        with z.open(name) as f:
            rd = csv.reader(io.TextIOWrapper(f, "latin-1", errors="replace"))
            for row in rd:
                if len(row) < 3:
                    continue
                ing = row[2].strip()
                if not ing or ing in seen:
                    continue
                seen.add(ing)
                out.append({"substance": ing, "source": "Health Canada",
                            "status": "approved", "orphan": False, "raw": ing})
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
                    "status": "approved", "orphan": False, "raw": ing})
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
                        "needs_translit": True})
    wb.close()
    return out
