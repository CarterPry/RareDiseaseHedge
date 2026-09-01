"""
Orphadata rare-disease epidemiology: prevalence + age of onset.

Answers the two eligibility.py criteria that were structurally UNKNOWN/HUMAN
before — s.529(a)(3)(B) "rare (US < 200,000)" and s.529(a)(3)(A) "primarily
affects individuals aged birth-18" — for any candidate whose disease resolves to
an Orphanet disorder.

Two facts make this a good fit:
  1. Orphanet lists ONLY rare diseases (EU threshold < 5 / 10,000). So a match is
     itself strong rarity evidence, and a NON-match for a common-disease drug
     (vildagliptin -> type-2 diabetes) is the correct answer: it is not a
     rare-disease candidate. Orphadata therefore both confirms rarity AND helps
     narrow the Article-57 expansion, which is dominated by common-disease drugs.
  2. Age-of-onset classes (Neonatal / Infancy / Childhood / Adolescent vs Adult /
     Elderly) map directly onto the pediatric-population question.

Source files (data/raw/, fetched by fetch.py):
  orphadata_prev.xml  = en_product9_prev  (prevalence)
  orphadata_ages.xml  = en_product9_ages  (natural history / onset)
Schemas verified live 2026-08-31. product9 carries no synonyms, so matching is
on the disorder Name only (normalised); coverage is reported honestly rather
than asserted.

Stdlib only (xml.etree).
"""
from __future__ import annotations
import os, re
import xml.etree.ElementTree as ET

US_POPULATION = 335_000_000
RARE_THRESHOLD = 200_000   # s.529 / orphan-drug definition

# Point-prevalence class -> (per-N, N) midpoint used to estimate a US headcount.
# Only used as a coarse comparator against the 200,000 threshold; the class
# string itself is carried as the real evidence.
_CLASS_MID = {
    "<1 / 1 000 000": 0.5 / 1_000_000,
    "1-9 / 1 000 000": 5 / 1_000_000,
    "1-9 / 100 000": 5 / 100_000,
    "1-5 / 10 000": 3 / 10_000,
    "6-9 / 10 000": 7.5 / 10_000,
    ">1 / 1000": 1.5 / 1000,
}
_PEDIATRIC_ONSET = {"Antenatal", "Neonatal", "Infancy", "Childhood", "Adolescent"}
_ADULT_ONSET = {"Adult", "Elderly"}


def _norm(s: str) -> str:
    """Lowercase, strip punctuation and a few stop/descriptor words, collapse
    spaces — so 'Leber hereditary optic neuropathy' and
    'Optic Atrophy, Hereditary, Leber' have a chance of meeting on tokens."""
    s = (s or "").lower()
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


# Only truly generic words are dropped. Disease-distinguishing modifiers
# (hereditary, familial, congenital, neonatal, primary, ...) are KEPT as tokens:
# "hereditary atrial fibrillation" (rare) must NOT collapse onto "atrial
# fibrillation" (common), and that distinction lives entirely in those words.
_STOP = {"disease", "disorder", "syndrome", "of", "the", "and", "with",
         "treatment", "for", "in", "a", "an", "to"}


def _tokens(s: str) -> frozenset:
    return frozenset(t for t in _norm(s).split() if t not in _STOP and len(t) > 2)


class OrphaIndex:
    def __init__(self):
        self.by_orpha: dict[str, dict] = {}
        self.name2orpha: dict[str, str] = {}       # normalised name -> orpha
        self._token_index: list[tuple[frozenset, str]] = []

    # ---- load --------------------------------------------------------------
    def load(self, raw: str):
        prev = os.path.join(raw, "orphadata_prev.xml")
        ages = os.path.join(raw, "orphadata_ages.xml")
        if os.path.exists(prev):
            self._load_prev(prev)
        if os.path.exists(ages):
            self._load_ages(ages)
        for orpha, rec in self.by_orpha.items():
            n = _norm(rec["name"])
            if n:
                self.name2orpha.setdefault(n, orpha)
                self._token_index.append((_tokens(rec["name"]), orpha))
        return len(self.by_orpha)

    def _rec(self, orpha, name):
        return self.by_orpha.setdefault(orpha, {
            "orpha": orpha, "name": name, "prev_class": "", "prev_geo": "",
            "us_estimate": None, "onset": [], "onset_class": ""})

    def _load_prev(self, path):
        for _, d in ET.iterparse(path, events=("end",)):
            if d.tag != "Disorder":
                continue
            oc = d.findtext("OrphaCode")
            nm = d.findtext("Name")
            if not oc:
                d.clear(); continue
            rec = self._rec(oc, nm)
            best = None  # prefer US geo, then Worldwide; prefer a real class
            for p in d.iter("Prevalence"):
                if (p.findtext("PrevalenceType/Name") or "") != "Point prevalence":
                    continue
                cls = p.findtext("PrevalenceClass/Name") or ""
                geo = p.findtext("PrevalenceGeographic/Name") or ""
                if cls in ("", "Unknown", "Not yet documented"):
                    continue
                score = (2 if geo == "United States" else 1 if geo == "Worldwide" else 0)
                if best is None or score > best[0]:
                    best = (score, cls, geo)
            if best:
                _, cls, geo = best
                rec["prev_class"], rec["prev_geo"] = cls, geo
                mid = _CLASS_MID.get(cls)
                rec["us_estimate"] = int(mid * US_POPULATION) if mid else None
            d.clear()

    def _load_ages(self, path):
        for _, d in ET.iterparse(path, events=("end",)):
            if d.tag != "Disorder":
                continue
            oc = d.findtext("OrphaCode")
            nm = d.findtext("Name")
            if not oc:
                d.clear(); continue
            rec = self._rec(oc, nm)
            onset = [a.findtext("Name") for a in d.iter("AverageAgeOfOnset")]
            onset = [o for o in onset if o and o not in ("No data available",)]
            rec["onset"] = onset
            rec["onset_class"] = _classify_onset(onset)
            d.clear()

    # ---- resolve -----------------------------------------------------------
    def resolve(self, *texts):
        """Best Orphanet disorder for any of the given free-text disease strings.

        Precision over recall: an exact normalised-name match, else a token match
        that requires near-identity (Jaccard >= 0.8, >= 2 shared tokens). The
        looser 0.6 threshold produced real false matches — vildagliptin's
        'diabetes mellitus type 2' onto 'neonatal diabetes mellitus' — so a
        confident answer for the clearly-rare diseases is worth more here than
        coverage bought with noise. Returns the disorder record or None."""
        cands = [t for t in texts if t and t.strip()]
        for t in cands:
            n = _norm(t)
            if n in self.name2orpha:
                return self.by_orpha[self.name2orpha[n]]
        best, best_score = None, 0.0
        for t in cands:
            tt = _tokens(t)
            if len(tt) < 2:
                continue
            for toks, orpha in self._token_index:
                if len(toks) < 2:
                    continue
                inter = len(tt & toks)
                if inter < 2:
                    continue
                jac = inter / len(tt | toks)
                if jac > best_score:
                    best, best_score = orpha, jac
        return self.by_orpha[best] if best and best_score >= 0.8 else None


def _classify_onset(onset: list[str]) -> str:
    s = set(onset)
    if not s:
        return ""
    if "All ages" in s:          # explicitly spans pediatric and adult
        return "mixed"
    ped = bool(s & _PEDIATRIC_ONSET)
    adult = bool(s & _ADULT_ONSET)
    if ped and not adult:
        return "pediatric"
    if adult and not ped:
        return "adult"
    return "mixed"


def rarity(rec) -> tuple[str, str]:
    """(verdict, evidence). verdict in rare / possibly_not_rare / unknown.
    A match to Orphanet is itself rarity evidence (Orphanet lists only rare
    diseases); the class refines it against the exact US 200,000 threshold."""
    est, cls, geo = rec.get("us_estimate"), rec.get("prev_class"), rec.get("prev_geo")
    if est is None:
        if cls:
            return "rare", f"Orphanet point prevalence {cls} ({geo}); listed as a rare disease"
        return "unknown", "matched an Orphanet disorder but it carries no point-prevalence class"
    if est < RARE_THRESHOLD:
        return "rare", f"Orphanet {cls} ({geo}) ≈ {est:,} in the US, under 200,000"
    return "possibly_not_rare", (f"Orphanet {cls} ({geo}) ≈ {est:,} in the US — the "
                                 f"class midpoint exceeds 200,000; verify the exact figure")


def onset(rec) -> tuple[str, str]:
    """(verdict, evidence). verdict in pediatric / mixed / adult / unknown."""
    cls = rec.get("onset_class")
    ol = ", ".join(rec.get("onset") or [])
    if not cls:
        return "unknown", "matched an Orphanet disorder but it carries no age-of-onset data"
    if cls == "pediatric":
        return "pediatric", f"Orphanet age of onset: {ol} — within birth-18"
    if cls == "adult":
        return "adult", f"Orphanet age of onset: {ol} — adult/elderly"
    return "mixed", f"Orphanet age of onset: {ol} — spans pediatric and adult"


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    idx = OrphaIndex()
    n = idx.load(os.path.join(here, "data", "raw"))
    print(f"loaded {n:,} Orphanet disorders")
    for q in ["Leber hereditary optic neuropathy", "Alagille syndrome",
              "Duchenne muscular dystrophy", "chronic kidney disease",
              "Huntington disease", "Menkes disease"]:
        rec = idx.resolve(q)
        if rec:
            print(f"\n{q!r} -> {rec['name']} (ORPHA:{rec['orpha']})")
            print("   rarity:", rarity(rec))
            print("   onset :", onset(rec))
        else:
            print(f"\n{q!r} -> no Orphanet match (not a listed rare disease)")
