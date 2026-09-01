"""
Source loaders for the candidate-discovery diff.

LEFT side (foreign approvals): EMA centralised, EMA Article 57 / xEVMPD (all
nationally-authorised EEA products — the largest source by far), Health Canada
DPD, Swissmedic, PMDA FY (best-effort — katakana needs a transliteration layer,
flagged).
RIGHT side (US exclusion set): Drugs@FDA + Orange Book active ingredients, plus
an optional flag-only layer from the openFDA NDC directory that distinguishes
real 505/351 approvals from OTC-monograph and bulk-ingredient marketing.

Each foreign loader yields dicts:
  {substance, source, status, orphan, raw, foreign_status[, countries]}
`foreign_status` is authorised / previously_authorised / never_authorised and is
what keeps a refused or withdrawn application from being counted as an approval.
The US loader returns (us_uniis:set, us_moiety_names:set, raw_ingredient_count).

Provenance and schemas verified live 2026-08-06 against the actual files;
see sources/00-CANDIDATE-DISCOVERY-METHOD.md and _recovered/MINED-drug-data-sources.md.
"""
from __future__ import annotations
import csv, io, os, re, zipfile
import openpyxl
from unii import UniiIndex, split_ingredients, moiety_key


def _resolve_cols(header, wanted):
    """Map logical field -> column index BY HEADER NAME, with a positional
    fallback that warns loudly. `wanted` is {field: (patterns, fallback_idx)};
    a column matches a field if its normalised header contains any pattern.
    Same defence as unii.py: a regulator that reorders/inserts a column silently
    corrupts every downstream field when columns are read positionally (this is
    exactly how the 2026-08 UNII column shift broke the biologic filter)."""
    def norm(s):
        return re.sub(r"[^a-z0-9]", "", (s or "").lower())
    hnorm = [norm(h) for h in header]
    idx, missing = {}, []
    for field, (patterns, fallback) in wanted.items():
        found = None
        for i, h in enumerate(hnorm):
            if any(norm(p) in h for p in patterns):
                found = i
                break
        if found is None:
            found = fallback
            missing.append(field)
        idx[field] = found
    if missing:
        print(f"[sources] WARNING: header lookup failed for {missing}; using "
              f"positional fallback {[wanted[m][1] for m in missing]}. Verify the "
              f"file layout has not changed.", flush=True)
    return idx


# --------------------------------------------------------------- US exclusion
def load_us_exclusion(idx: UniiIndex, raw: str):
    """Union of Drugs@FDA Products.txt ActiveIngredient, Orange Book Ingredient,
    and the openFDA NDC directory's application-approved products, canonicalized
    to ALL resolvable UNIIs plus ALL string key variants (see UniiIndex.collect).
    This is the set a foreign moiety must be ABSENT from to count as
    never-approved-in-US. Collecting every variant — salt UNII, base UNII,
    stripped key, canonicalised-counterion key, acid/-ate stem — on BOTH sides is
    what makes salt-vs-base, spelling-variant and INN-vs-USAN differences collapse
    correctly. The single-canonical-key version of this measured 12/19 silent
    misses on labeled US-approved drugs (test_accuracy.py).

    The NDC pass (marketing_category NDA/ANDA/BLA only) was added 2026-08-31 after
    Article 57 surfaced ~10 moieties — penicillamine, tetrofosmin, mebrofenin,
    selenium, L-tryptophan, methionine among them — that ARE in Drugs@FDA but
    under a spelling whose UNII did not intersect the foreign name's UNII. The NDC
    directory carries broader per-moiety name coverage, so ingesting its
    application-approved rows through the same collect() path closes that gap.
    NON-application NDC rows (OTC monograph, bulk, unapproved) are deliberately
    NOT ingested here — they are not a 505/351 approval and would introduce false
    negatives; they are surfaced as a separate flag by load_us_otc_marketing."""
    import json
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

    # openFDA NDC — only application-approved products (NDA/ANDA/BLA). Optional:
    # a missing file just means we fall back to the two bulk files above.
    ndc_path = os.path.join(raw, "openfda_ndc.zip")
    n_ndc = 0
    if os.path.exists(ndc_path):
        with zipfile.ZipFile(ndc_path) as z:
            mem = [n for n in z.namelist() if n.endswith(".json")][0]
            with z.open(mem) as fh:
                for rec in json.load(fh).get("results") or []:
                    if (rec.get("marketing_category") or "").upper() not in APPLICATION_CATEGORIES:
                        continue
                    for ai in rec.get("active_ingredients") or []:
                        for ing in split_ingredients(ai.get("name") or ""):
                            ingest(ing)
                            n_ndc += 1

    # Manual supplement: moieties with a real US approval that even Drugs@FDA +
    # Orange Book + the openFDA NDC application feed all miss — old withdrawn NDAs
    # from before the electronic record, and biologic-panel active ingredients the
    # NDC directory does not expose as a simple moiety. Each is a verified fact
    # with a primary-source citation, not a heuristic; kept small pending proper
    # 21 CFR 216.24/DESI and Purple Book feeds (see README limitations). A
    # withdrawn or diagnostic approval still disqualifies under s.529 — the moiety
    # was once approved in an application.
    US_WITHDRAWN_SUPPLEMENT = [
        "betahistine",    # Serc — FDA NDA approved 1966, withdrawn 1972 (DESI/efficacy)
        # Found by the 2026-08-31 Article-57 validation pass, both confirmed
        # against primary sources:
        "dimethindene",   # Forhistal — NDA 12-335/12-337/12-338 (Novartis),
                          # withdrawn 19 Apr 2000 (65 FR 54, doc 00-6722). Too old
                          # for the electronic bulk files.
        "tixocortol",     # tixocortol pivalate — allergen in T.R.U.E. TEST, an
                          # FDA BLA (STN 103738, US License 1888) marketed since
                          # 1994. A 351(a) biologic; NDC did not expose the panel
                          # component as a moiety.
    ]
    for ing in US_WITHDRAWN_SUPPLEMENT:
        ingest(ing)

    return us_moiety_uniis, us_moieties, {"ingredient_rows": n_ingredients,
                                          "unmatched": unmatched, "ndc_rows": n_ndc}


# --------------------------------------------------------------- US non-application marketing
# openFDA NDC marketing categories that are NOT an approval under 505(b)(1),
# (b)(2) or (j). A moiety sold in the US only under one of these is still
# PRV-eligible on the statutory test — s.529(a)(4)(B)(i)(I) bars a prior approval
# *in an application*, and an OTC monograph or a compounding bulk listing is not
# one. But it is commercially decisive: there is no exclusivity runway, supply
# already exists, and in practice these rows are usually excipients,
# antiseptics or supplements rather than repurposing candidates. So: flag, never
# exclude. (This is what identifies METHYLPARABEN as a US OTC-monograph
# preservative rather than a drug.)
NON_APPLICATION_CATEGORIES = {
    "OTC MONOGRAPH DRUG", "OTC MONOGRAPH FINAL", "OTC MONOGRAPH NOT FINAL",
    "UNAPPROVED DRUG OTHER", "UNAPPROVED HOMEOPATHIC", "UNAPPROVED MEDICAL GAS",
    "UNAPPROVED DRUG FOR USE IN DRUG SHORTAGE",
    "BULK INGREDIENT", "BULK INGREDIENT FOR HUMAN PRESCRIPTION COMPOUNDING",
    "DRUG FOR FURTHER PROCESSING", "EXPORT ONLY",
}
# ...and the ones that ARE an approval. Present for completeness and as a
# tripwire: if one of these ever matches a surviving candidate, the exclusion set
# missed a real US approval and the run should be treated as suspect.
APPLICATION_CATEGORIES = {"NDA", "ANDA", "BLA", "NDA AUTHORIZED GENERIC"}


def load_us_otc_marketing(idx: UniiIndex, raw: str):
    """openFDA NDC directory -> {UNII or moiety key: set(marketing_category)}.

    Optional: returns ({}, {}) if openfda_ndc.zip is absent, because this layer
    only ever adds flags and must never be able to change a verdict by being
    missing. Returns (by_unii, by_key)."""
    import json
    path = os.path.join(raw, "openfda_ndc.zip")
    if not os.path.exists(path):
        return {}, {}
    by_unii: dict[str, set[str]] = {}
    by_key: dict[str, set[str]] = {}
    with zipfile.ZipFile(path) as z:
        name = [n for n in z.namelist() if n.endswith(".json")][0]
        with z.open(name) as fh:
            records = json.load(fh).get("results") or []
    for rec in records:
        cat = (rec.get("marketing_category") or "").upper()
        if not cat:
            continue
        for ai in rec.get("active_ingredients") or []:
            for ing in split_ingredients(ai.get("name") or ""):
                uniis, keyset = idx.collect(ing)
                for u in uniis:
                    by_unii.setdefault(u, set()).add(cat)
                for k in keyset:
                    by_key.setdefault(k, set()).add(cat)
    return by_unii, by_key


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
    col = None
    for r in ws.iter_rows(values_only=True):
        vals = [("" if c is None else str(c)) for c in r]
        if col is None:
            if any("Active substance" in v for v in vals):
                # header row — resolve column indices by name (positional fallback)
                col = _resolve_cols(vals, {
                    "category": (["category"], 0),
                    "status": (["medicine status"], 3),
                    "inn": (["international non-proprietary", "inn"], 6),
                    "active": (["active substance"], 7),
                    "area": (["therapeutic area"], 8),
                    "atc": (["atc code (human)", "atc code"], 11),
                    "indication": (["therapeutic indication"], 15),
                    "orphan": (["orphan medicine"], 23),
                    "approved": (["marketing authorisation date"], 31),
                })
            continue
        need = max(col.values())
        if len(vals) <= need:
            continue
        g = lambda k: vals[col[k]].strip()
        category = g("category")
        status = g("status")
        inn = g("inn")
        active = g("active")
        area = g("area")
        atc = g("atc")
        indication = g("indication")
        approved = g("approved")
        orphan = g("orphan").lower() in ("yes", "true", "1")
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


# --------------------------------------------------------------- EMA Article 57 (EEA national)
# Countries that appear in the authorisation-country column for CENTRALISED
# products. Those are already loaded by load_ema from the medicines report, with
# real status and orphan data attached, so re-ingesting them here would
# double-count and would also overwrite a known status with a bare "authorised".
ART57_CENTRALISED = {"european union", "eu"}


def load_ema_art57(raw: str):
    """ema_art57.xlsx — EMA Article 57 / xEVMPD product data.

    The single biggest coverage gap this pipeline had. The medicines report loaded
    by load_ema covers CENTRALISED authorisations only, so a drug licensed in 30
    member states through national or mutual-recognition routes — etoricoxib,
    fusidic acid, sulthiame — was invisible and could read as "never approved
    abroad". This file is the register of everything authorised in the EEA:
    163,791 product rows, ~12,000 distinct active-substance strings.

    Layout (verified live 2026-08-29): header row begins with 'Product name';
    active substance col 1 ('|'-separated for combination products), route col 2,
    authorisation country col 3, marketing-authorisation holder col 4.

    Status semantics — the important caveat. Article 57 obliges
    marketing-authorisation holders to submit and maintain data for every medicine
    authorised in the EEA, so presence implies a live authorisation. But it is
    MAH-submitted data rather than a regulator's decision record, and it carries
    no status column: there is no "refused" or "withdrawn" to filter on the way
    load_ema now does. It is therefore reported under its own source label,
    'EU national (Art57)', so it can be discounted separately from a decision
    this pipeline has actually seen.

    Rows are aggregated to one record per substance with the set of authorising
    countries, because the country count is a real quality signal (a substance
    authorised in 25 member states is an established medicine) and because
    emitting 163,791 individual records would put the resolver through two orders
    of magnitude more work for the same answer.
    """
    path = os.path.join(raw, "ema_art57.xlsx")
    if not os.path.exists(path):
        return []
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb.active
    col = None
    by_sub: dict[str, set[str]] = {}
    for r in ws.iter_rows(values_only=True):
        vals = [("" if c is None else str(c)) for c in r]
        if col is None:
            if vals and vals[0].strip().startswith("Product name"):
                col = _resolve_cols(vals, {
                    "active": (["active substance"], 1),
                    "country": (["product authorisation country", "authorisation country"], 3),
                })
            continue
        if len(vals) <= max(col.values()):
            continue
        subs, country = vals[col["active"]].strip(), vals[col["country"]].strip()
        if not subs or country.lower() in ART57_CENTRALISED:
            continue
        for part in subs.split("|"):
            p = part.strip()
            if p:
                by_sub.setdefault(p, set()).add(country)
    wb.close()
    return [{"substance": s, "source": "EU national (Art57)",
             "status": "authorised", "orphan": False, "raw": s,
             "foreign_status": "authorised", "countries": sorted(c)}
            for s, c in by_sub.items()]


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
