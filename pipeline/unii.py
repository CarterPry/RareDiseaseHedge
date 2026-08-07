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
foreign substance is only called "never approved in the US" when BOTH its UNII
is absent from the US UNII set AND its moiety key is absent from the US moiety
set.

Pure stdlib + the two UNII flat files. No pandas.
"""
from __future__ import annotations
import csv, io, os, re, sys, zipfile

# --- salt / hydrate / ester counter-ions stripped to approximate active moiety.
# Not exhaustive; it is the pragmatic set that covers the large majority of
# marketed small-molecule salts. GSRS /moieties is the authoritative source and
# is listed as a future refinement in the method doc.
SALT_TOKENS = {
    "HYDROCHLORIDE", "HCL", "DIHYDROCHLORIDE", "HYDROBROMIDE", "HYDROIODIDE",
    "SODIUM", "DISODIUM", "POTASSIUM", "CALCIUM", "MAGNESIUM", "ZINC", "LITHIUM",
    "SULFATE", "SULPHATE", "BISULFATE", "HEMISULFATE",
    "ACETATE", "DIACETATE", "TRIHYDRATE", "DIHYDRATE", "MONOHYDRATE", "HYDRATE",
    "MESYLATE", "MESILATE", "MALEATE", "CITRATE", "DIHYDROGEN", "TARTRATE",
    "BITARTRATE", "PHOSPHATE", "DIPHOSPHATE", "BESYLATE", "BESILATE",
    "FUMARATE", "HEMIFUMARATE", "SUCCINATE", "BROMIDE", "CHLORIDE", "IODIDE",
    "NITRATE", "PAMOATE", "EMBONATE", "GLUCONATE", "LACTATE", "STEARATE",
    "SALICYLATE", "OXALATE", "TOSYLATE", "TOSILATE", "XINAFOATE", "VALERATE",
    "PROPIONATE", "DECANOATE", "ENANTATE", "ENANTHATE", "PALMITATE", "PIVALATE",
    "DIMALEATE", "HYDROGEN", "SESQUIHYDRATE", "MONOHYDROCHLORIDE", "AXETIL",
    "TROMETAMOL", "TROMETHAMINE", "MEGLUMINE", "ARGININE", "CHOLINE", "OLAMINE",
    "ETHANOLATE", "SOLVATE", "ANHYDROUS", "BASE", "FREE",
}
# tokens that are pure noise in names
NOISE_TOKENS = {"AND", "OF", "THE", "USP", "BP", "EP", "PH", "EUR"}


def norm(s: str) -> str:
    """Uppercase, drop punctuation, collapse whitespace."""
    if s is None:
        return ""
    s = str(s).upper()
    # unify various dashes / quotes to space, drop other punctuation
    s = re.sub(r"[^A-Z0-9 ]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def moiety_key(s: str) -> str:
    """Strip trailing salt/hydrate/ester tokens to approximate the active moiety."""
    toks = norm(s).split()
    # peel salt/noise tokens from the end (they follow the moiety name)
    while toks and (toks[-1] in SALT_TOKENS or toks[-1] in NOISE_TOKENS):
        toks.pop()
    return " ".join(toks)


class UniiIndex:
    """name -> UNII, plus UNII -> descriptive info."""

    def __init__(self):
        self.name2unii: dict[str, str] = {}      # normalized synonym -> UNII
        self.moiety2unii: dict[str, str] = {}     # moiety-key -> a representative UNII
        self.unii2display: dict[str, str] = {}
        self.unii2type: dict[str, str] = {}       # SUBSTANCE_TYPE (chemical/protein/...)
        self.unii2inn: dict[str, bool] = {}
        self.unii2usan: dict[str, bool] = {}      # has a USAN (US Adopted Name)

    # ---- loaders -----------------------------------------------------------
    def load_names(self, path: str) -> int:
        """UNII_Names file: Name<TAB>TYPE<TAB>UNII<TAB>Display Name."""
        n = 0
        with open(path, encoding="utf-8", errors="replace", newline="") as fh:
            rd = csv.reader(fh, delimiter="\t")
            header = next(rd, None)
            for row in rd:
                if len(row) < 4:
                    continue
                name, _type, unii, display = row[0], row[1], row[2], row[3]
                if not unii:
                    continue
                nm = norm(name)
                if nm and nm not in self.name2unii:
                    self.name2unii[nm] = unii
                    mk = moiety_key(name)
                    if mk and mk not in self.moiety2unii:
                        self.moiety2unii[mk] = unii
                n += 1
        return n

    def load_records(self, path: str) -> int:
        """UNII_Records: UNII, Display Name, ... INN_ID(16), ... SUBSTANCE_TYPE(23)."""
        n = 0
        with open(path, encoding="utf-8", errors="replace", newline="") as fh:
            rd = csv.reader(fh, delimiter="\t")
            header = next(rd, None)
            for row in rd:
                if len(row) < 24:
                    continue
                unii, display = row[0], row[1]
                inn_id = row[16] if len(row) > 16 else ""
                usan_id = row[17] if len(row) > 17 else ""
                subtype = row[23] if len(row) > 23 else ""
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
                mk = moiety_key(display)
                if mk and mk not in self.moiety2unii:
                    self.moiety2unii[mk] = unii
                n += 1
        return n

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


def split_ingredients(field: str):
    """FDA/foreign active-ingredient fields pack combos and dual name/salt forms
    with ';', '+', or '/' (e.g. 'CEFADROXIL/CEFADROXIL HEMIHYDRATE'). Split on all
    three so each component resolves cleanly."""
    if not field:
        return []
    parts = re.split(r"[;+/]", field)
    return [p.strip() for p in parts if p.strip()]
