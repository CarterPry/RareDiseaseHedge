"""
UNII normalization and name->moiety resolution.

This is the join layer the whole candidate-discovery diff depends on. Every
substance name — foreign or US — is resolved to (a) a FDA UNII and (b) a
salt/hydrate-stripped "moiety key". Section 3 of
sources/00-CANDIDATE-DISCOVERY-METHOD.md is the spec; the measured EMA->UNII
match rate that motivates this approach was 94.6%.

The two-key design is deliberate. 21 U.S.C. 360ff turns on active *moiety*, not
active *ingredient*: "hydroxyamphetamine hydrobromide" (a salt, its own UNII)
and "hydroxyamphetamine" (the base moiety, a different UNII) must be treated as
the SAME thing for the "previously approved in the US" test. Matching on UNII
alone would miss that and produce false positives — the single most expensive
error in the pipeline (believing a moiety is new to the US when it is not). So a
foreign substance is only called "never approved in the US" when its UNIIs, its
key variants, AND its GSRS relatives (rdh_diff.py) are all absent from the US
record.

String normalization (generated salt vocabulary, counterion canonicalisation,
acid/-ate bridging, key sets) lives in moiety.py; this module layers the UNII
join on top. The old hand-listed SALT_TOKENS matcher measured 12/19 silent
misses against labeled US-approved drugs (2026-08-28); see
pipeline/test_accuracy.py for the harness that keeps this measured.

Pure stdlib + the two UNII flat files. No pandas.
"""
from __future__ import annotations
import csv, io, os, re, sys, zipfile

# normalization layer — re-exported so sources.py / rdh_diff.py keep importing
# from unii
from moiety import (norm, moiety_key, keys, split_ingredients,  # noqa: F401
                    has_stereo_marker, SALT_TOKENS, NOISE_TOKENS)


class UniiIndex:
    """name -> UNII, plus UNII -> descriptive info."""

    def __init__(self):
        self.name2unii: dict[str, str] = {}      # normalized synonym -> UNII
        self.moiety2unii: dict[str, str] = {}     # moiety-key -> a representative UNII
        self._moiety_claim: dict[str, int] = {}   # key -> quality of current claim
        self.unii2display: dict[str, str] = {}
        self.unii2type: dict[str, str] = {}       # SUBSTANCE_TYPE (chemical/protein/...)
        self.unii2inn: dict[str, bool] = {}
        self.unii2usan: dict[str, bool] = {}      # has a USAN (US Adopted Name)

    def _claim_moiety(self, mk: str, nm: str, unii: str):
        """Representative UNII for a moiety key. An exact base name ('SUNITINIB'
        for key 'SUNITINIB') beats a stripped derivative ('SUNITINIB ACID'),
        and among derivatives the shortest name wins ('SALICYLIC ACID' beats
        'SALICYLIC ACID MONOETHANOLAMINE' for key 'SALICYLIC') — else whatever
        salt the names file lists first becomes the moiety's face: wrong
        display name, wrong INN/USAN flags, wrong substance type. Membership
        testing is unaffected (collect() checks every variant); this is about
        which record represents the group."""
        if not mk:
            return
        score = 0 if nm == mk else len(nm)
        prev = self._moiety_claim.get(mk)
        if prev is None or score < prev:
            self.moiety2unii[mk] = unii
            self._moiety_claim[mk] = score

    # ---- loaders -----------------------------------------------------------
    @staticmethod
    def _cols(header, wanted, legacy):
        """Map logical field -> column index BY HEADER NAME, not by position.

        FDA changes this schema without notice. The 4 Aug 2026 UNII_Records
        release inserted UTF8_DISPLAY_NAME at index 23, shifting SUBSTANCE_TYPE
        from 23 to 24 — so the previously-correct row[23] began returning a
        display name. is_biologic() then matched almost nothing and the
        biologic/mixture filter silently collapsed from 204 rows to 4, leaking
        ~200 proteins and mixtures into the candidate list. Positional indices
        are only a fallback for a file with no recognisable header.

        Also tolerates the header renaming seen in the same release
        ('Display Name' -> 'DISPLAY_NAME'): comparison is case- and
        separator-insensitive.
        """
        idx = {}
        if header:
            norm = {re.sub(r"[^a-z0-9]", "", (h or "").lower()): i
                    for i, h in enumerate(header)}
            for key, aliases in wanted.items():
                for a in aliases:
                    j = norm.get(re.sub(r"[^a-z0-9]", "", a.lower()))
                    if j is not None:
                        idx[key] = j
                        break
        missing = [k for k in wanted if k not in idx]
        for k in missing:
            idx[k] = legacy[k]
        if missing:
            print(f"[unii] WARNING: no header match for {missing}; falling back to "
                  f"legacy positions {[legacy[k] for k in missing]}. Verify the "
                  f"UNII schema has not changed again.", flush=True)
        return idx

    def load_names(self, path: str) -> int:
        """UNII_Names file: NAME, TYPE, UNII, DISPLAY_NAME (columns by header)."""
        n = 0
        with open(path, encoding="utf-8", errors="replace", newline="") as fh:
            rd = csv.reader(fh, delimiter="\t")
            header = next(rd, None)
            c = self._cols(header,
                           {"name": ["NAME", "Name"], "unii": ["UNII"],
                            "display": ["DISPLAY_NAME", "Display Name"]},
                           {"name": 0, "unii": 2, "display": 3})
            i_name, i_unii, i_disp = c["name"], c["unii"], c["display"]
            need = max(i_name, i_unii, i_disp)
            for row in rd:
                if len(row) <= need:
                    continue
                name, unii, display = row[i_name], row[i_unii], row[i_disp]
                if not unii:
                    continue
                nm = norm(name)
                if nm and nm not in self.name2unii:
                    self.name2unii[nm] = unii
                    self._claim_moiety(moiety_key(name), nm, unii)
                n += 1
        return n

    def load_records(self, path: str) -> int:
        """UNII_Records: UNII, DISPLAY_NAME, INN_ID, USAN_ID, SUBSTANCE_TYPE.

        Columns are resolved by header name — see _cols for why that is not
        optional here."""
        n = 0
        with open(path, encoding="utf-8", errors="replace", newline="") as fh:
            rd = csv.reader(fh, delimiter="\t")
            header = next(rd, None)
            c = self._cols(header,
                           {"unii": ["UNII"],
                            "display": ["DISPLAY_NAME", "Display Name"],
                            "inn": ["INN_ID"], "usan": ["USAN_ID"],
                            "subtype": ["SUBSTANCE_TYPE"]},
                           {"unii": 0, "display": 1, "inn": 16, "usan": 17,
                            "subtype": 23})
            need = max(c.values())
            for row in rd:
                if len(row) <= need:
                    continue
                unii, display = row[c["unii"]], row[c["display"]]
                inn_id = row[c["inn"]]
                usan_id = row[c["usan"]]
                subtype = row[c["subtype"]]
                if not unii:
                    continue
                self.unii2display[unii] = display
                self.unii2type[unii] = subtype
                self.unii2inn[unii] = bool(inn_id.strip())
                self.unii2usan[unii] = bool(usan_id.strip())
                # ensure the display name itself is resolvable
                nm = norm(display)
                if nm and nm not in self.name2unii:
                    self.name2unii[nm] = unii
                self._claim_moiety(moiety_key(display), nm, unii)
                n += 1
        self._check_subtypes(path)
        return n

    def _check_subtypes(self, path: str):
        """Belt-and-braces guard on the SUBSTANCE_TYPE column.

        Header-name lookup fixes the known 2026-08 schema shift, but the failure
        mode it protects against is silent and expensive — a mis-read column made
        is_biologic() return False almost everywhere and leaked ~200 proteins and
        mixtures into the candidate list, while every count still looked
        plausible. So assert the shape of the data too: this column is a small
        controlled vocabulary dominated by 'chemical'. Anything else means the
        schema moved again."""
        types = {}
        for t in self.unii2type.values():
            types[t] = types.get(t, 0) + 1
        if not types:
            return
        n = sum(types.values())
        chem = types.get("chemical", 0)
        if len(types) > 25 or chem < 0.25 * n:
            top = sorted(types.items(), key=lambda kv: -kv[1])[:5]
            print(f"[unii] WARNING: SUBSTANCE_TYPE in {os.path.basename(path)} "
                  f"looks wrong — {len(types):,} distinct values, 'chemical' is "
                  f"{chem:,}/{n:,}. Expected a handful of values dominated by "
                  f"'chemical'. The biologic/mixture filter is probably reading "
                  f"the wrong column; top values: {top}", flush=True)

    # ---- resolution --------------------------------------------------------
    def resolve(self, name: str):
        """Return (unii, moiety_key, tier). tier in exact|salt-stripped|moiety|unmatched."""
        mk = moiety_key(name)
        nm = norm(name)
        if nm in self.name2unii:
            return self.name2unii[nm], mk, "exact"
        if mk and mk in self.name2unii:
            return self.name2unii[mk], mk, "salt-stripped"
        if mk and mk in self.moiety2unii:
            return self.moiety2unii[mk], mk, "moiety"
        return None, mk, "unmatched"

    def moiety_unii(self, name: str):
        """Canonical active-moiety UNII for set-membership comparison.

        This is what makes the diff correct across BOTH salt form AND synonym
        system. Example: US "MECHLORETHAMINE HYDROCHLORIDE" (a salt, USAN name)
        and EU "chlormethine" (base, INN name) both canonicalize here to the
        same base UNII 50D9XSG0VR, so the EU drug is correctly recognised as
        already US-approved. Salt/base pairs also collapse, de-duplicating
        e.g. MASITINIB + MASITINIB MESYLATE.

        Preference order: base UNII for the moiety key > direct UNII of the
        full name. Returns (canonical_unii|None, moiety_key, tier).
        """
        mk = moiety_key(name)
        nm = norm(name)
        base = self.moiety2unii.get(mk) if mk else None
        if base:
            tier = "moiety-base" if nm != mk else "exact-moiety"
            return base, mk, tier
        direct = self.name2unii.get(nm)
        if direct:
            return direct, mk, "direct"
        return None, mk, "unmatched"

    def is_biologic(self, unii: str) -> bool:
        t = (self.unii2type.get(unii) or "").lower()
        return any(k in t for k in ("protein", "nucleic", "polymer", "structurally", "mixture"))

    def is_counterion(self, name: str) -> bool:
        """Synonym-robust counterion test for GSRS graph walls. The name list
        alone is bypassable — GSRS says '2-Aminoethanol' where the wall list
        says 'ETHANOLAMINE' — so also resolve the name and test the display
        names of everything it resolves to. (Found live: fosfosal was excluded
        through 2-aminoethanol -> ethanolamine oleate before this check.)"""
        from moiety import is_counterion_substance
        if is_counterion_substance(name):
            return True
        uniis, _ = self.collect(name)
        return any(is_counterion_substance(self.unii2display.get(u, ""))
                   for u in uniis)

    def collect(self, name: str):
        """All UNIIs and all key variants a substance name can legitimately
        resolve to. THIS — not a single canonical key — is what exclusion-set
        membership is tested on, on both sides symmetrically.

        Why a set: one string cannot represent a molecule that is written
        several ways. US "LAPATINIB DITOSYLATE" collects {salt UNII, base UNII,
        'LAPATINIB DITOSYLATE', 'LAPATINIB'}; foreign "lapatinib" collects the
        base UNII and 'LAPATINIB'; the intersection is the match the old
        single-key comparison missed. Returns (uniis:set, keyset:set)."""
        keyset = keys(name)
        uniis = set()
        for k in keyset:
            u = self.name2unii.get(k)
            if u:
                uniis.add(u)
            b = self.moiety2unii.get(k)
            if b:
                uniis.add(b)
        return uniis, keyset
