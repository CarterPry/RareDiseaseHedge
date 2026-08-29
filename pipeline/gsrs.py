"""
GSRS active-moiety relationship layer.

Prodrugs, radiolabel conjugates and synonym-system gaps are chemistry, not
string manipulation: isavuconazonium -> isavuconazole is invisible to any
tokenizer, and only the FDA's own substance-relationship graph (GSRS, the
system behind UNIIs) knows the two share an active moiety. The method doc
lists this as the § 2 completeness layer; this module implements it against
the live GSRS API with a persistent on-disk cache, so the pipeline works
offline after the first run and a flaky network can never silently produce a
candidate.

For each surviving candidate UNII we ask two questions:
  forward : what substances does THIS record point at?
            (a salt's record points at its base via ACTIVE MOIETY)
  reverse : what substances point AT this record?
            (isavuconazonium's record points at isavuconazole — the candidate
            — so only the reverse direction finds the US-approved prodrug)

Relationship types are classified, not trusted wholesale:
  EXCLUSION-grade  ACTIVE MOIETY / PRODRUG<->METABOLITE ACTIVE /
                   SALT|SOLVATE<->PARENT — these carry the s.529 "active
                   ingredient (including any ester or salt)" identity across.
  REVIEW-grade     ENANTIOMER / RACEMATE / STEREOISOMER — whether a single
                   enantiomer of an approved racemate is "an ester or salt of"
                   it is not settled by the statutory text; a human decides.
  ignored          targets, enzymes, impurities, ligands — biology, not
                   identity.

A fetch failure returns ok=False and the caller MUST route that row to REVIEW,
never to the candidate list.
"""
from __future__ import annotations
import json, os, ssl, time, urllib.parse, urllib.request

from moiety import is_counterion_substance

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE_PATH = os.path.join(HERE, "data", "cache", "gsrs.json")
BASE = "https://gsrs.ncats.nih.gov/api/v1"
UA = "RareDiseaseHedge/1.0 (research; carterpry@gmail.com)"
CTX = ssl.create_default_context()
THROTTLE_S = 0.15
RETRIES = 3

# relationship-type classification (substring tests on the GSRS type string)
def grade(rel_type: str) -> str | None:
    t = (rel_type or "").upper()
    if "ACTIVE MOIETY" in t:
        return "exclude"
    if "PRODRUG" in t and "METABOLITE" in t:
        return "exclude"
    if ("SALT" in t or "SOLVATE" in t) and "PARENT" in t:
        return "exclude"
    if "ENANTIOMER" in t or "RACEMATE" in t or "STEREOISOMER" in t:
        return "review"
    return None


class GsrsClient:
    def __init__(self, cache_path: str = CACHE_PATH, offline: bool = False):
        self.cache_path = cache_path
        self.offline = offline
        self._dirty = 0
        try:
            with open(cache_path, encoding="utf-8") as fh:
                self.cache = json.load(fh)
        except Exception:
            self.cache = {}

    # ---- plumbing ----------------------------------------------------------
    def _get_json(self, url: str):
        last = None
        for attempt in range(RETRIES):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": UA,
                                                           "Accept": "application/json"})
                with urllib.request.urlopen(req, timeout=30, context=CTX) as r:
                    time.sleep(THROTTLE_S)
                    return json.loads(r.read())
            except Exception as e:  # noqa: BLE001 — any failure means retry
                last = e
                time.sleep(0.6 * (attempt + 1))
        raise last

    def save(self):
        if not self._dirty:
            return
        os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)
        with open(self.cache_path, "w", encoding="utf-8") as fh:
            json.dump(self.cache, fh, indent=1)
        self._dirty = 0

    # ---- the two directions ------------------------------------------------
    @staticmethod
    def _rels_of(record: dict, only_pointing_at: str | None = None):
        """(type, related_unii, related_name) triples from a substance record."""
        out = []
        for rel in record.get("relationships") or []:
            rs = rel.get("relatedSubstance") or {}
            u = rs.get("approvalID") or ""
            nm = rs.get("refPname") or ""
            t = rel.get("type") or ""
            if only_pointing_at and u != only_pointing_at:
                continue
            out.append((t, u, nm))
        return out

    def relatives(self, unii: str, wall=None):
        """All graded relatives of a UNII, both directions, cached.

        Returns {"ok": bool, "relatives": [(grade, type, unii, name), ...]}.
        Forward: the record's own relationships (salt -> base).
        Reverse: substances whose relationships point at this UNII, with the
        pointing edge's type (prodrug -> this candidate). The relative reported
        for a reverse edge is the POINTING substance — that is the thing that
        may be US-approved.

        `wall` is the counterion test used to drop bridge-poisoning relatives;
        pass UniiIndex.is_counterion for the synonym-robust version. Defaults
        to the name-list check."""
        ent = self.cache.get(unii)
        if ent is None:
            if self.offline:
                return {"ok": False, "relatives": []}
            ent = {"ok": True, "forward": [], "reverse": []}
            # forward
            try:
                rec = self._get_json(f"{BASE}/substances({unii})?view=full")
                ent["forward"] = self._rels_of(rec)
                ent["name"] = rec.get("_name") or ""
            except Exception:
                ent["ok"] = False
            # reverse
            try:
                q = urllib.parse.quote(f'root_relationships_relatedSubstance_approvalID:"{unii}"')
                res = self._get_json(f"{BASE}/substances/search?q={q}&top=50&view=full")
                for sub in res.get("content") or []:
                    su = sub.get("approvalID") or ""
                    sname = sub.get("_name") or ""
                    if not su or su == unii:
                        continue
                    for t, _u, _nm in self._rels_of(sub, only_pointing_at=unii):
                        ent["reverse"].append((t, su, sname))
            except Exception:
                ent["ok"] = False
            self.cache[unii] = ent
            self._dirty += 1
            if self._dirty >= 25:
                self.save()

        wall = wall or is_counterion_substance
        rels = []
        for t, u, nm in list(ent.get("forward") or []) + list(ent.get("reverse") or []):
            g = grade(t)
            if not (g and u and u != unii):
                continue
            # a salt's graph also points at its bare counterion/solvent
            # (lasofoxifene tartrate -> tartaric acid). That edge is a wall,
            # not a bridge: following it would join every tartrate in the US
            # record to every foreign tartrate. Drop it here, centrally.
            if wall(nm):
                continue
            rels.append((g, t, u, nm))
        return {"ok": bool(ent.get("ok")), "relatives": rels}
