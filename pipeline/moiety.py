"""
Hardened active-moiety string normalization for the s.529 (21 U.S.C. 360ff)
"never approved in the US" test.

WHY THIS EXISTS
---------------
s.529 excludes any drug "no active ingredient (including any ester or salt of
the active ingredient) of which has been approved in any other application"
under 505(b)(1), 505(b)(2), 505(j), 351(a) or 351(k).

The expensive error is a FALSE NEGATIVE ON THE EXCLUSION SET: believing a
moiety is new to the US when it is not. That builds a program on an ineligible
drug. Measured against a labeled set on 2026-08-28, the previous hand-listed
SALT_TOKENS matcher let 12 of 19 known US-approved drugs (lapatinib, sunitinib,
ibandronic acid, ...) through to the candidate list. This module fixes the
string-resolvable part of that:

  1. Salt/hydrate tokens are GENERATED combinatorially (multiplier x counterion
     x spelling variant) instead of hand-listed. A hand-list will always have
     TOSYLATE while missing DITOSYLATE, MEGLUMINE while missing DIMEGLUMINE.

  2. Counterion spelling variants collapse to one canonical form, so
     "mesilate", "mesylate" and "methanesulfonate" are the same thing.

  3. The INN-vs-USAN acid/-ate convention is bridged. Europe writes
     "ibandronic acid", the US writes "ibandronate sodium". No salt-stripping
     connects those strings; a stem transformation in both directions does.

  4. Ester-prodrug suffixes (axetil, proxetil, mofetil, ...) are stripped,
     because the statute explicitly reaches "any ester or salt".

  5. keys() returns a SET of candidate forms per name and matching is set
     intersection, rather than reducing to one string and comparing. One key
     cannot represent a molecule that is legitimately written several ways.

WHAT IT DELIBERATELY WILL NOT DO
--------------------------------
Prodrug and enantiomer relationships are chemistry, not string manipulation.
isavuconazonium -> isavuconazole is invisible to any tokenizer. Those cases are
handled by the GSRS relationship layer (pipeline/gsrs.py) and, failing that,
surfaced as REVIEW — never silently passed.

This module is pure stdlib and has no dependency on the UNII index; unii.py
builds on top of it. StringExclusionSet at the bottom is the standalone
string-only matcher used by test_accuracy.py's offline mode.
"""
from __future__ import annotations
import re
from dataclasses import dataclass, field
from enum import Enum

# --------------------------------------------------------------------------
# Counterion vocabulary, generated rather than listed
# --------------------------------------------------------------------------

# Counterion stems whose spelling varies. Synonyms map to a single canonical
# spelling so "mesilate", "mesylate" and "methanesulfonate" collapse together.
COUNTERION_SYNONYMS = {
    "MESYLATE": "MESYLATE", "MESILATE": "MESYLATE",
    "METHANESULFONATE": "MESYLATE", "METHANESULPHONATE": "MESYLATE",
    "METHANSULFONATE": "MESYLATE",
    "TOSYLATE": "TOSYLATE", "TOSILATE": "TOSYLATE",
    "TOLUENESULFONATE": "TOSYLATE", "TOLUENESULPHONATE": "TOSYLATE",
    "PTOLUENESULFONATE": "TOSYLATE",
    "BESYLATE": "BESYLATE", "BESILATE": "BESYLATE",
    "BENZENESULFONATE": "BESYLATE", "BENZENESULPHONATE": "BESYLATE",
    "ESYLATE": "ESYLATE", "ESILATE": "ESYLATE", "ETHANESULFONATE": "ESYLATE",
    "SULFATE": "SULFATE", "SULPHATE": "SULFATE", "BISULFATE": "SULFATE",
    "HYDROGENSULFATE": "SULFATE",
    "MALEATE": "MALEATE",
    "MALATE": "MALATE",          # distinct from maleate; both are common
    "MALONATE": "MALONATE",
    "TARTRATE": "TARTRATE", "BITARTRATE": "TARTRATE",
    "HYDROGENTARTRATE": "TARTRATE",
    "PHOSPHATE": "PHOSPHATE", "DIHYDROGENPHOSPHATE": "PHOSPHATE",
    "HYDROGENPHOSPHATE": "PHOSPHATE",
    "MEGLUMINE": "MEGLUMINE",
    "TROMETAMOL": "TROMETAMOL", "TROMETHAMINE": "TROMETAMOL",
    "OLAMINE": "OLAMINE", "ETHANOLAMINE": "OLAMINE",
    "PAMOATE": "PAMOATE", "EMBONATE": "PAMOATE",
    "XINAFOATE": "XINAFOATE",
    "ISETIONATE": "ISETIONATE", "ISETHIONATE": "ISETIONATE",
    "NAPADISYLATE": "NAPADISYLATE", "NAPADISILATE": "NAPADISYLATE",
    "NAPSYLATE": "NAPSYLATE", "NAPSILATE": "NAPSYLATE",
    "EDISYLATE": "EDISYLATE", "EDISILATE": "EDISYLATE",
    "CAMSYLATE": "CAMSYLATE", "CAMSILATE": "CAMSYLATE",
    "GLUCEPTATE": "GLUCEPTATE", "GLUCOHEPTONATE": "GLUCEPTATE",
    "ENANTATE": "ENANTHATE", "ENANTHATE": "ENANTHATE", "HEPTANOATE": "ENANTHATE",
}

SIMPLE_COUNTERIONS = {
    # cations
    "SODIUM", "POTASSIUM", "CALCIUM", "MAGNESIUM", "ZINC", "LITHIUM",
    "ALUMINIUM", "ALUMINUM", "AMMONIUM", "CHOLINE", "ARGININE", "LYSINE",
    "DIETHYLAMINE", "DIETHYLAMMONIUM", "PIPERAZINE", "BENZATHINE",
    "PROCAINE", "DIOLAMINE",
    # anions
    "CHLORIDE", "BROMIDE", "IODIDE", "FLUORIDE",
    "HYDROCHLORIDE", "HCL", "HYDROBROMIDE", "HYDROIODIDE", "HYDROFLUORIDE",
    "NITRATE", "CITRATE", "ACETATE", "LACTATE", "GLUCONATE", "FUMARATE",
    "SUCCINATE", "OXALATE", "BENZOATE", "SALICYLATE", "STEARATE",
    "PALMITATE", "PROPIONATE", "BUTYRATE", "VALERATE", "DECANOATE",
    "UNDECYLENATE", "HEXANOATE", "CAPROATE", "CYPIONATE", "PIVALATE",
    "ADIPATE", "ASPARTATE", "GLUTAMATE", "CARBONATE", "BICARBONATE",
    "BORATE", "TANNATE", "THIOCYANATE", "TRIFLUOROACETATE", "FORMATE",
    # ester-prodrug suffixes — the statute reaches "any ester or salt".
    # ETEXILATE was missing and cost a measured false positive: EU/Article-57
    # "dabigatran" did not meet US "DABIGATRAN ETEXILATE MESYLATE" (Pradaxa),
    # so a US-approved active moiety read as never-approved (found 2026-08-29).
    "AXETIL", "PROXETIL", "PIVOXIL", "DIPIVOXIL", "MEDOXOMIL", "CILEXETIL",
    "ETABONATE", "FOSAMIL", "MOFETIL", "ETEXILATE",
    # hydrate / solvate / state descriptors
    "HYDRATE", "SOLVATE", "ETHANOLATE", "METHANOLATE", "ANHYDROUS",
    # bare qualifiers seen trailing real names
    "HYDROGEN", "DIHYDROGEN", "BASE", "FREE", "ACID", "SALT",
}

# Stoichiometric prefixes. Generating these is the whole point: a hand-written
# list reliably contains TOSYLATE and omits DITOSYLATE.
MULTIPLIERS = ["", "MONO", "DI", "TRI", "TETRA", "PENTA", "HEXA", "HEPTA",
               "OCTA", "DECA", "HEMI", "SESQUI", "SEMI", "BIS", "TRIS"]

NOISE_TOKENS = {"AND", "OF", "THE", "USP", "BP", "EP", "PH", "EUR", "NF",
                "JP", "PHEUR", "FOR", "INJECTION", "ORAL", "AS", "IN"}

# If salt-stripping reduces a name to one of these fragments, the "salt" token
# was actually half the ester's name (methyl salicylate, ethyl chloride, benzyl
# benzoate). Do not emit the stripped form — it would join unrelated esters.
TRIVIAL_BASES = {
    "METHYL", "ETHYL", "PROPYL", "ISOPROPYL", "BUTYL", "ISOBUTYL", "AMYL",
    "BENZYL", "PHENYL", "CETYL", "STEARYL", "LAURYL", "GLYCERYL", "VINYL",
    "MONO", "DI", "TRI",
}

# Free acids/bases/solvents that exist in GSRS as substances in their own right
# and appear as SALT/SOLVATE->PARENT relatives of every salt that contains them.
# Walking the relationship graph THROUGH one of these joins unrelated drugs
# ("lasofoxifene tartrate -> tartaric acid -> <every US tartrate>"), so the
# traversal must treat them as walls, not bridges. Names, not UNIIs, because
# GSRS carries several records per acid (anhydrous/hydrate/isomer forms).
COUNTERION_SUBSTANCES = {
    # acids (incl. the irregular stems the -ATE rule cannot derive: TARTARIC)
    "TARTARIC ACID", "MALEIC ACID", "MALIC ACID", "CITRIC ACID", "FUMARIC ACID",
    "SUCCINIC ACID", "ACETIC ACID", "LACTIC ACID", "GLUCONIC ACID",
    "BENZOIC ACID", "SALICYLIC ACID", "OXALIC ACID", "MALONIC ACID",
    "STEARIC ACID", "PALMITIC ACID", "PAMOIC ACID", "EMBONIC ACID",
    "METHANESULFONIC ACID", "ETHANESULFONIC ACID", "BENZENESULFONIC ACID",
    "TOLUENESULFONIC ACID", "P TOLUENESULFONIC ACID", "CAMPHORSULFONIC ACID",
    "NAPHTHALENESULFONIC ACID", "NAPADISILIC ACID", "EDISILIC ACID",
    "ISETHIONIC ACID", "GLUCOHEPTONIC ACID", "XINAFOIC ACID",
    "1 HYDROXY 2 NAPHTHOIC ACID", "HYDROCHLORIC ACID", "HYDROBROMIC ACID",
    "HYDRIODIC ACID", "HYDROIODIC ACID", "SULFURIC ACID", "PHOSPHORIC ACID",
    "NITRIC ACID", "CARBONIC ACID", "BORIC ACID", "ADIPIC ACID",
    "GLUTAMIC ACID", "ASPARTIC ACID", "DECANOIC ACID", "TRIFLUOROACETIC ACID",
    "FORMIC ACID", "PROPIONIC ACID", "BUTYRIC ACID", "VALERIC ACID",
    "HEPTANOIC ACID", "HEXANOIC ACID", "UNDECYLENIC ACID", "THIOCYANIC ACID",
    "TANNIC ACID",
    # bases / cations / amines
    "SODIUM HYDROXIDE", "POTASSIUM HYDROXIDE", "CALCIUM HYDROXIDE",
    "MAGNESIUM HYDROXIDE", "ZINC HYDROXIDE", "LITHIUM HYDROXIDE",
    "ALUMINUM HYDROXIDE", "ALUMINIUM HYDROXIDE", "AMMONIA",
    "AMMONIUM HYDROXIDE", "MEGLUMINE", "TROMETAMOL", "TROMETHAMINE",
    "LYSINE", "ARGININE", "CHOLINE", "BENZATHINE", "PROCAINE", "PIPERAZINE",
    "ETHANOLAMINE", "AMINOETHANOL", "MONOETHANOLAMINE", "OLAMINE",
    "DIETHANOLAMINE", "TRIETHANOLAMINE", "ETHYLENEDIAMINE",
    "DIETHYLAMINE", "SODIUM", "POTASSIUM", "CALCIUM", "MAGNESIUM", "ZINC",
    "LITHIUM",
    # solvate edges point at the solvent
    "WATER", "ETHANOL", "METHANOL", "ISOPROPYL ALCOHOL",
}


def is_counterion_substance(name: str) -> bool:
    """True when a GSRS substance is a bare salt-former/solvent, i.e. a wall
    for relationship-graph traversal (see COUNTERION_SUBSTANCES). Locant
    digits are ignored — GSRS says '2-Aminoethanol' where the wall list says
    'AMINOETHANOL'."""
    n = norm(name)
    if n in COUNTERION_SUBSTANCES:
        return True
    stripped = " ".join(t for t in n.split() if not t.isdigit())
    return bool(stripped) and stripped in COUNTERION_SUBSTANCES


# Enantiomer / stereochemistry markers. Presence only FLAGS a name for caveat;
# whether a single enantiomer of an approved racemate is "an ester or salt of"
# that racemate is not settled by the statutory text, so it is surfaced, not
# decided. (Single letters D/L are excluded — "VITAMIN D" is not a stereo call.)
STEREO_PREFIXES = ["LEVO", "DEXTRO", "RAC"]
STEREO_MARKERS = {"DL", "RS", "SR", "RACEMIC", "RACEMATE"}

# WHO INN stereochemical and geometric-isomer prefixes, fused into the stem
# rather than written as a "(R)-"/"(±)-" marker. Used to find a US-approved
# stereoisomer PARTNER of a candidate — the one exclusion class FDA's own GSRS
# substance graph provably cannot see: verified live 2026-08-29, GSRS carries no
# enantiomer/racemate edge between zopiclone and eszopiclone (Lunesta) nor
# between enclomifene and clomifene (Clomid). Broader than STEREO_PREFIXES
# above, which answers the different question "does this NAME look stereo".
INN_STEREO_PREFIXES = ["ES", "LEVO", "LEV", "DEXTRO", "DEX", "AR", "RAC",
                       "EN", "ZU", "CIS", "TRANS", "MESO", "ALLO", "EPI"]


# Trailing stereo descriptors as they survive norm(): UNII writes the single
# enantiomer as "ZOPICLONE, (R)-" and norm() reduces that to "ZOPICLONE R".
# Which UNII record claims a moiety key is not stable across UNII releases — the
# 4 Aug 2026 file made "ZOPICLONE" resolve to the (R)- record rather than the
# racemate — so the descriptor has to be stripped before looking for a partner,
# or the pair silently stops being found.
STEREO_SUFFIXES = {"R", "S", "RS", "SR", "E", "Z", "D", "L", "DL",
                   "1R", "1S", "2R", "2S", "ALPHA", "BETA"}
LEADING_ISOMER_PREFIXES = {"D", "L", "DL"}


def stereo_name_variants(name: str) -> set[str]:
    """Candidate names for a stereoisomer/geometric-isomer partner of `name`.

    Both directions, because either name may carry the descriptor:
      add    ZOPICLONE   + ES -> ESZOPICLONE   (US-approved: Lunesta)
      strip  ENCLOMIFENE - EN -> CLOMIFENE     (US-approved: Clomid)
    and a trailing descriptor is removed first, so "ZOPICLONE, (R)-" is treated
    as ZOPICLONE. A stripped prefix stem must keep >= 6 characters so short words
    cannot collide. Pure string generation — the caller decides which variants
    are US-approved. Measured over the full survivor set this yields only real
    pairs (zopiclone/eszopiclone, enclomifene/clomifene, levomenthol/menthol)
    and raises no false alarms."""
    n = norm(name)
    if not n:
        return set()
    bases = {n}
    toks = n.split()
    if len(toks) > 1 and toks[-1] in STEREO_SUFFIXES:
        stem = " ".join(toks[:-1])
        if len(stem) >= 4:
            bases.add(stem)
    out = set()
    for b in bases:
        out |= {p + b for p in INN_STEREO_PREFIXES}
        out |= {b[len(p):] for p in INN_STEREO_PREFIXES
                if b.startswith(p) and len(b) - len(p) >= 6}
        out.add(b)
    return {v for v in out if v and v != n}


def _build_salt_vocabulary() -> set[str]:
    vocab: set[str] = set()
    stems = set(COUNTERION_SYNONYMS) | SIMPLE_COUNTERIONS
    for stem in stems:
        for mult in MULTIPLIERS:
            vocab.add(mult + stem)
    return vocab


SALT_TOKENS = _build_salt_vocabulary()

_MULTS_BY_LEN = sorted((m for m in MULTIPLIERS if m), key=len, reverse=True)


def _canonical_counterion(tok: str) -> str:
    """Strip a stoichiometric prefix and map spelling variants to one form."""
    stem = tok
    for mult in _MULTS_BY_LEN:
        if tok.startswith(mult):
            candidate = tok[len(mult):]
            if candidate in COUNTERION_SYNONYMS or candidate in SIMPLE_COUNTERIONS:
                stem = candidate
                break
    return COUNTERION_SYNONYMS.get(stem, stem)


# --------------------------------------------------------------------------
# Normalization
# --------------------------------------------------------------------------

def norm(s: str) -> str:
    """Uppercase, drop punctuation, collapse whitespace."""
    if s is None:
        return ""
    s = str(s).upper()
    s = re.sub(r"[^A-Z0-9 ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def _strip_salts(tokens: list[str]) -> list[str]:
    """Peel counterion / hydrate / noise tokens from the end of a token list.
    Returns [] when stripping would leave nothing or a trivial ester fragment
    (the caller then falls back to the full name)."""
    out = list(tokens)
    while out and (out[-1] in SALT_TOKENS or out[-1] in NOISE_TOKENS):
        out.pop()
    if len(out) == 1 and (out[0] in TRIVIAL_BASES or len(out[0]) < 3):
        return []
    return out


def moiety_key(s: str) -> str:
    """Single canonical salt-stripped key (counterion spellings canonicalised
    before stripping). This is the drop-in successor of the old hand-listed
    moiety_key and is what the UNII moiety index is keyed on. keys() below is
    the richer set used for exclusion-set membership."""
    toks = [_canonical_counterion(t) for t in norm(s).split()]
    return " ".join(_strip_salts(toks))


def _acid_ate_variants(stem: str) -> set[str]:
    """
    Bridge the INN 'X-ic acid' / USAN 'X-ate' convention, both directions:

        ibandronic acid  <-> ibandronate      (Boniva)
        zoledronic acid  <-> zoledronate      (Reclast)
        mycophenolic acid<-> mycophenolate    (CellCept/Myfortic)
    """
    out: set[str] = set()
    if stem.endswith("IC"):
        base = stem[:-2]
        if len(base) >= 4:
            out.add(base + "ATE")
            out.add(base + "IC ACID")
    if stem.endswith("IC ACID"):
        base = stem[:-7]
        if len(base) >= 4:
            out.add(base + "ATE")
            out.add(base + "IC")
    if stem.endswith("ATE"):
        base = stem[:-3]
        if len(base) >= 4:
            out.add(base + "IC")
            out.add(base + "IC ACID")
    return out


def _orthographic_variants(n: str) -> set[str]:
    """INN-vs-USAN spelling variants that UNII records as SEPARATE substances.

    UNII's synonym table already unifies almost every INN/USAN divergence —
    paracetamol/acetaminophen, salbutamol/albuterol, ciclosporin/cyclosporine,
    rifampicin/rifampin all resolve to one UNII. Measured over 26 known pairs
    (2026-08-29) exactly one class does not: the cephalosporin CEF-/CEPH- rule,
    where INN 'cefalexin' and USAN 'cephalexin' carry different UNIIs and
    different keys. That let EU cefalexin and cefradine read as never-US-approved
    while cephalexin and cephradine are both US-approved.

    Restricted to a leading CEF/CEPH so it cannot fire mid-word or on unrelated
    names, and applied in both directions."""
    out = set()
    if n.startswith("CEPH"):
        out.add("CEF" + n[4:])
    elif n.startswith("CEF"):
        out.add("CEPH" + n[3:])
    return out


def keys(name: str) -> set[str]:
    """
    Every plausible canonical form of a substance name.

    Two substances are the same moiety when their key sets intersect.
    Returning a set rather than one string is what lets 'ibandronic acid'
    and 'ibandronate sodium' meet.
    """
    n = norm(name)
    if not n:
        return set()

    out: set[str] = {n}
    tokens = n.split()

    # Leading D-/L-/DL- isomer prefix (Art57 "D-Penicillamine", "L-Tryptophan"):
    # the US record names the same substance without it (PENICILLAMINE,
    # TRYPTOPHAN) and UNII gives the prefixed spelling its own record, so neither
    # UNII nor key intersected and both sat in REVIEW. Found 2026-10-11. Stem
    # must keep >= 4 chars so a bare "D"/"L" token cannot collide.
    if len(tokens) > 1 and tokens[0] in LEADING_ISOMER_PREFIXES \
            and len(" ".join(tokens[1:])) >= 4:
        out |= keys(" ".join(tokens[1:]))

    # counterion spellings canonicalised in place, unstripped
    canon = [_canonical_counterion(t) for t in tokens]
    canon_joined = " ".join(canon)
    out.add(canon_joined)

    # salt-stripped forms (raw and canonicalised)
    for toks in (tokens, canon):
        stripped = _strip_salts(toks)
        if stripped:
            base = " ".join(stripped)
            out.add(base)
            # acid/-ate stem variants on the stripped base
            out |= _acid_ate_variants(base)

    # acid/-ate variants on the full name, for cases where nothing strips
    out |= _acid_ate_variants(n)

    # INN/USAN spelling variants UNII keeps as separate substances (CEF-/CEPH-)
    for k in list(out):
        out |= _orthographic_variants(k)

    return {k for k in out if k}


def full_keys(name: str) -> set[str]:
    """UNSTRIPPED key forms only: the normalized name and its counterion-
    canonicalised spelling. This — not keys() — is what a GSRS RELATIVE must be
    matched on. A relative that is a salt of the candidate is 'candidate +
    counterion'; stripping it can expose the OTHER component and join two
    unrelated drugs (found live: salicylic acid -> colchicine salicylate ->
    stripped 'COLCHICINE' -> US-approved colchicine)."""
    n = norm(name)
    if not n:
        return set()
    canon = " ".join(_canonical_counterion(t) for t in n.split())
    return {n, canon}


def has_stereo_marker(name: str) -> bool:
    """True when a name carries an enantiomer/racemate marker. Caveat signal
    only — never decides an exclusion by itself."""
    toks = norm(name).split()
    if any(t in STEREO_MARKERS for t in toks):
        return True
    first = toks[0] if toks else ""
    return any(first.startswith(p) and len(first) > len(p) + 3
               for p in STEREO_PREFIXES)


def split_ingredients(field_value: str):
    """Ingredient fields pack combination products and dual name/salt forms
    with ';', '+', '/' or ' AND ' (e.g. 'CEFADROXIL/CEFADROXIL HEMIHYDRATE').
    Split on all so each component resolves on its own."""
    if not field_value:
        return []
    parts = re.split(r"[;+/]|\bAND\b", str(field_value).upper())
    return [p.strip() for p in parts if p.strip()]


# --------------------------------------------------------------------------
# Verdicts — three-state on purpose. REVIEW is returned whenever the answer
# depends on information the matcher does not hold, so an unresolvable case
# can never be silently reported as a candidate.
# --------------------------------------------------------------------------

class Verdict(str, Enum):
    APPROVED_IN_US = "APPROVED_IN_US"   # excluded by s.529, definite
    NOT_IN_US = "NOT_IN_US"             # candidate, definite on available data
    REVIEW = "REVIEW"                   # a human must decide


@dataclass
class MatchResult:
    verdict: Verdict
    reason: str
    matched_us_name: str = ""
    matched_key: str = ""
    flags: list = field(default_factory=list)


class StringExclusionSet:
    """
    String-only US exclusion set: the moiety.py layer with no UNII index.

    Used by test_accuracy.py's offline mode and usable standalone when the
    UNII flat files are not on disk. The production path (sources.py /
    rdh_diff.py) wraps the same keys() logic around the UNII join, which
    additionally collapses synonym systems (chlormethine vs mechlorethamine).
    """

    def __init__(self) -> None:
        self._key_to_name: dict[str, str] = {}
        self._moiety_graph: dict[str, str] = {}   # any form -> canonical moiety
        self._raw_ingredients: list[str] = []
        self.n_ingredients = 0
        self._finalized = True

    def add_ingredient(self, name: str) -> None:
        self._raw_ingredients.append(name)
        for k in keys(name):
            self._key_to_name.setdefault(k, name)
        self.n_ingredients += 1

    def add_moiety_link(self, form: str, moiety: str) -> None:
        """GSRS-style active-moiety edge: a specific substance (salt, ester,
        prodrug) -> its canonical active moiety."""
        mk = norm(moiety)
        for k in keys(form):
            self._moiety_graph[k] = mk
        self._moiety_graph.setdefault(mk, mk)
        self._finalized = False

    @property
    def has_moiety_graph(self) -> bool:
        return bool(self._moiety_graph)

    def finalize(self) -> None:
        """Re-index every US ingredient under its canonical active moiety.

        Call after both the ingredient record and the moiety graph are loaded.
        Without this the graph is useless in the direction that matters: the
        US record holds ISAVUCONAZONIUM SULFATE, the foreign register holds
        isavuconazole, and only resolving the US side down to its moiety makes
        the two meet."""
        for name in self._raw_ingredients:
            for k in keys(name):
                canon = self._moiety_graph.get(k)
                if not canon:
                    continue
                for ck in keys(canon):
                    self._key_to_name.setdefault(ck, name)
        self._finalized = True

    def check(self, foreign_name: str) -> MatchResult:
        """Is this foreign substance's active moiety already approved in the US?"""
        if not self._finalized:
            raise RuntimeError("finalize() must be called after add_moiety_link()")
        flags: list[str] = []
        fkeys = keys(foreign_name)
        if not fkeys:
            return MatchResult(Verdict.REVIEW, "unparseable name", flags=["EMPTY"])

        for k in fkeys:
            if k in self._key_to_name:
                return MatchResult(Verdict.APPROVED_IN_US,
                                   "active ingredient matches a US approval",
                                   self._key_to_name[k], k)

        if self.has_moiety_graph:
            for k in fkeys:
                canon = self._moiety_graph.get(k)
                if not canon:
                    continue
                for ck in keys(canon):
                    if ck in self._key_to_name:
                        return MatchResult(
                            Verdict.APPROVED_IN_US,
                            "active moiety matches a US approval via moiety graph",
                            self._key_to_name[ck], ck)
        else:
            flags.append("NO_MOIETY_GRAPH")

        if has_stereo_marker(foreign_name):
            flags.append("STEREOISOMER")

        if flags:
            return MatchResult(
                Verdict.REVIEW,
                "no string match, but not fully resolvable: " + ", ".join(flags),
                flags=flags)

        return MatchResult(Verdict.NOT_IN_US,
                           "no US approval found for this active moiety",
                           flags=flags)
