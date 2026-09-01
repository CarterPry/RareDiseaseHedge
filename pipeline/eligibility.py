"""
FD&C Act s.529 (21 U.S.C. 360ff) rare pediatric disease PRV eligibility gate.

Encodes every statutory criterion separately and labels each by WHO can decide
it. The screening error that matters is not a missed candidate; it is a
candidate that looks eligible because a criterion nobody could evaluate was
quietly treated as satisfied.

Every criterion therefore returns one of PASS / FAIL / UNKNOWN / HUMAN, and the
overall verdict can never be ELIGIBLE while any criterion is UNKNOWN or HUMAN.
The best a machine can return is LIKELY_ELIGIBLE_PENDING_REVIEW.

Statutory text relied on, verified verbatim against 21 U.S.C. 360ff on
uscode.house.gov 2026-08-29. NOTE: Pub. L. 117-9 (2021) rewrote (a)(4)(A) and
(B); pre-2021 summaries of this program — including most law-firm explainers
still online — describe superseded law. The two substantive changes matter here:

  - (a)(4)(B)(i)(I)  for a DRUG, the application must contain "no active MOIETY
    (as defined by the Secretary in section 314.3 of title 21, Code of Federal
    Regulations)" previously approved in any other application under 505(b)(1),
    505(b)(2) or 505(j).  <- the criterion rdh_diff.py screens.
    It is NOT the older "active ingredient, including any ester or salt"
    formulation, and 351(a)/351(k) do NOT appear in the drug prong; they belong
    to the separate biologic prong at (a)(4)(B)(ii). Screening on active moiety
    — which is what the pipeline does — is therefore the correct standard.
  - (a)(4)(B)(i)(II)  the application must be "the subject of an application
    submitted under section 355(b)(1)", i.e. a full NDA under 505(b)(1) ONLY.
    A 505(b)(2) application is NOT eligible for a rare pediatric disease
    voucher. Vouchers awarded on 505(b)(2) applications predate Pub. L. 117-9.
    This does not sink a repurposing thesis — a 505(b)(1) may rest on published
    literature the sponsor did not generate — but it does mean the filing is a
    full NDA, with the cost and data burden that implies.

Remaining criteria:
  - (a)(3)(A) the disease is serious or life-threatening and its serious or
    life-threatening manifestations primarily affect individuals aged from birth
    to 18 years
  - (a)(3)(B) the disease is rare within the meaning of section 360bb (the
    orphan-drug definition: fewer than 200,000 persons in the US, or the
    not-cost-recoverable prong)
  - (a)(4)(A) the drug is for the prevention or treatment of that disease
  - (a)(4)(C) the Secretary deems the application eligible for priority review
  - (a)(4)(D) it relies on clinical data derived from studies examining a
    pediatric population and dosages intended for that population
  - (a)(4)(E) the original application does not seek an adult indication
  - (a)(4)(F) it is approved after 30 September 2016
  - (b)(5) "The Secretary may not award any priority review vouchers under
    paragraph (1) after September 30, 2029." The program had lapsed on
    20 December 2024 and was restored by the Consolidated Appropriations Act,
    2026 (Pub. L. 119-75, 3 February 2026), s.6604. There is no separate
    designation deadline.

FDA guidance further confirms that a drug approved and used abroad but never
submitted to FDA can qualify, while a new pediatric use or formulation of a
drug already US-approved cannot.

Data sources per criterion:
  - the exclusion test (1) is settled by rdh_diff.py (UNII/string/GSRS).
  - rarity (2) and primarily-pediatric (3) are settled by ORPHADATA when the
    disease resolves (orphadata.py — point prevalence + age of onset). Orphanet
    lists only rare diseases, so a match is itself rarity evidence and a
    common-disease drug correctly fails to match. Candidate.from_summary() pulls
    these straight off the row['orpha'] block enrich.py attaches.
  - seriousness (4), priority review (5) and the filing-design criteria (7-9)
    still require a human.

Usage against pipeline output:

    import json
    from eligibility import Candidate, assess
    row = json.load(open("data/out/summary.json"))["candidates"][0]
    # rarity + onset come from Orphadata (row['orpha']); the exclusion verdict is
    # NOT_IN_US because it is a funnelA candidate; the rest is diligence input.
    a = assess(Candidate.from_summary(row, us_exclusion_verdict="NOT_IN_US",
                                      serious_or_life_threatening=True,
                                      published_human_evidence=True,
                                      earliest_possible_approval=date(2029, 3, 1)))
    print(a.report())

Stdlib only.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from enum import Enum

SUNSET = date(2029, 9, 30)   # s.529(b)(5) — last date a voucher may be awarded
FLOOR = date(2016, 9, 30)    # s.529(a)(4)(F) — approval must be after this


class Status(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    UNKNOWN = "UNKNOWN"    # data exists but we do not hold it
    HUMAN = "HUMAN"        # no dataset can settle this; judgment required


class Decidability(str, Enum):
    MACHINE = "machine"    # a database join settles it
    DATA = "data"          # settled by a dataset we may or may not have loaded
    JUDGMENT = "judgment"  # requires a person, and often FDA
    DESIGN = "design"      # determined by how the sponsor chooses to file


@dataclass
class Criterion:
    key: str
    citation: str
    question: str
    decidability: Decidability
    status: Status = Status.UNKNOWN
    note: str = ""


@dataclass
class Candidate:
    name: str
    # from rdh_diff.py: "APPROVED_IN_US" | "NOT_IN_US" | "REVIEW"
    us_exclusion_verdict: str = "REVIEW"
    us_exclusion_note: str = ""
    foreign_regulators: list = field(default_factory=list)
    indication: str = ""
    disease: str = ""
    us_prevalence: int | None = None
    prevalence_note: str = ""                  # Orphadata evidence string
    pediatric_onset: bool | None = None       # primarily affects ages 0-18
    onset_class: str | None = None            # Orphadata: pediatric|adult|mixed|None
    onset_note: str = ""                       # Orphadata evidence string
    serious_or_life_threatening: bool | None = None
    us_therapy_exists: bool | None = None
    published_human_evidence: bool = False
    earliest_possible_approval: date | None = None

    @classmethod
    def from_summary(cls, row: dict, **overrides):
        """Build a Candidate from a summary.json row, pulling rarity and
        age-of-onset straight from the Orphadata block enrich.py attached
        (row['orpha']). Any field can be overridden by keyword — the exclusion
        verdict, seriousness and filing-design criteria still come from
        elsewhere. This is the wire between the pipeline output and the s.529
        criteria set."""
        o = row.get("orpha") or {}
        kw = dict(
            name=row.get("name", ""),
            indication=row.get("indication", ""),
            us_prevalence=o.get("us_prevalence_est"),
            prevalence_note=o.get("rarity_evidence", ""),
            onset_class=o.get("onset"),
            onset_note=o.get("onset_evidence", ""),
        )
        kw.update(overrides)
        return cls(**kw)


@dataclass
class Assessment:
    candidate: str
    criteria: list

    @property
    def failed(self):
        return [c for c in self.criteria if c.status is Status.FAIL]

    @property
    def open(self):
        return [c for c in self.criteria
                if c.status in (Status.UNKNOWN, Status.HUMAN)]

    @property
    def verdict(self) -> str:
        if self.failed:
            return "INELIGIBLE"
        if self.open:
            return "LIKELY_ELIGIBLE_PENDING_REVIEW"
        return "ELIGIBLE_ON_SCREENED_CRITERIA"

    def report(self) -> str:
        width = max(len(c.key) for c in self.criteria)
        lines = [f"{self.candidate}  ->  {self.verdict}", ""]
        for c in self.criteria:
            lines.append(f"  [{c.status.value:7}] {c.key:{width}}  "
                         f"({c.decidability.value})  {c.note}")
        return "\n".join(lines)


def assess(cand: Candidate, today: date | None = None) -> Assessment:
    today = today or date.today()
    crit: list[Criterion] = []

    # ---- 1. the exclusion test. The one a machine genuinely settles, and the
    #         one rdh_diff.py runs three layers deep (UNII variants, string
    #         keys, GSRS relationship graph).
    v = (cand.us_exclusion_verdict or "REVIEW").upper()
    if v == "APPROVED_IN_US":
        st, note = Status.FAIL, cand.us_exclusion_note or \
            "an active ingredient (or ester/salt of it) is already US-approved"
    elif v == "NOT_IN_US":
        st, note = Status.PASS, cand.us_exclusion_note or \
            "no US approval found across UNII variants, string keys and GSRS relatives"
    else:
        st, note = Status.HUMAN, cand.us_exclusion_note or \
            "screen could not settle it (see funnelA_review.csv flags)"
    crit.append(Criterion(
        "no_prior_us_active_moiety",
        "s.529(a)(4)(B)(i)(I) / 360ff(a)(4)(B)(i)(I)",
        "Has no active moiety (21 CFR 314.3) been previously approved in any "
        "other application under 505(b)(1), 505(b)(2) or 505(j)?",
        Decidability.MACHINE, st, note))

    # ---- 2. rarity. Orphadata point prevalence is the data source (orphadata.py):
    #         Orphanet lists only rare diseases, so a match is itself evidence,
    #         and the class refines it against the exact US 200,000 threshold.
    if cand.us_prevalence is not None:
        if cand.us_prevalence < 200_000:
            st, note = Status.PASS, (cand.prevalence_note or f"US prevalence {cand.us_prevalence:,}")
        else:
            st, note = Status.FAIL, (cand.prevalence_note or
                                     f"US prevalence {cand.us_prevalence:,} is not rare")
    elif cand.prevalence_note:
        # matched Orphanet but no numeric class (still a listed rare disease)
        st, note = Status.PASS, cand.prevalence_note
    else:
        st, note = Status.UNKNOWN, ("US prevalence not supplied; no Orphanet match "
                                    "(a common-disease drug will not match)")
    crit.append(Criterion(
        "rare_under_200k", "s.529(a)(3)(B)",
        "Does the disease affect fewer than 200,000 people in the US?",
        Decidability.DATA, st, note))

    # ---- 3. primarily pediatric. Orphadata age-of-onset is the data proxy
    #         (see orphadata.py); the statute's "primarily affects" is stricter
    #         than "onset", so a pediatric onset is PASS, an adult onset FAIL,
    #         and a mixed/all-ages onset stays HUMAN — a person must judge it.
    if cand.onset_class == "pediatric" or cand.pediatric_onset is True:
        st, note = Status.PASS, (cand.onset_note or "onset within birth-18")
    elif cand.onset_class == "adult" or cand.pediatric_onset is False:
        st, note = Status.FAIL, (cand.onset_note or "not primarily a pediatric population")
    elif cand.onset_class == "mixed":
        st, note = Status.HUMAN, (cand.onset_note or "onset spans pediatric and adult; "
                                  "'primarily affects 0-18' is a human call")
    else:
        st, note = Status.HUMAN, ("no age-of-onset data resolved; must be read "
                                  "from Orphadata (if the disease is listed) or "
                                  "the literature")
    crit.append(Criterion(
        "primarily_pediatric", "s.529(a)(3)(A)",
        "Does the disease primarily affect individuals aged from birth to 18?",
        Decidability.JUDGMENT, st, note))

    # ---- 4. seriousness
    if cand.serious_or_life_threatening is None:
        st, note = Status.HUMAN, "seriousness not assessed"
    elif cand.serious_or_life_threatening:
        st, note = Status.PASS, "asserted serious or life-threatening"
    else:
        st, note = Status.FAIL, "not serious or life-threatening"
    crit.append(Criterion(
        "serious_or_life_threatening", "s.529(a)(3)(A)",
        "Is the disease serious or life-threatening?",
        Decidability.JUDGMENT, st, note))

    # ---- 5. priority review. A documented share of real-world voucher denials
    #         turn on this, and it is the criterion most often assumed rather
    #         than tested (see sources/22-prv-denials-dataset.md).
    if cand.us_therapy_exists is None:
        st, note = Status.HUMAN, ("requires the US treatment landscape for this "
                                  "exact indication and a view on whether the "
                                  "drug is a significant improvement")
    elif cand.us_therapy_exists:
        st, note = Status.HUMAN, ("approved US therapy exists; must show "
                                  "significant improvement in safety or "
                                  "effectiveness to earn priority review")
    else:
        st, note = Status.HUMAN, ("no approved US therapy found, which helps, "
                                  "but FDA decides priority review at filing")
    crit.append(Criterion(
        "qualifies_for_priority_review", "s.529(a)(4)(C)",
        "Would the application qualify for priority review?",
        Decidability.JUDGMENT, st, note))

    # ---- 6. human evidence to build a 505(b)(2) on
    crit.append(Criterion(
        "human_evidence_exists", "505(b)(2) reliance",
        "Is there published or referenceable human evidence in this indication?",
        Decidability.DATA,
        Status.PASS if cand.published_human_evidence else Status.UNKNOWN,
        "published evidence located" if cand.published_human_evidence
        else "no published human evidence located"))

    # ---- 7-9. filing design. Not properties of the drug; choices the sponsor
    #           makes. Listed so they are never silently assumed satisfied.
    for key, cite, q, note in [
        ("filed_as_505b1", "s.529(a)(4)(B)(i)(II)",
         "Will the application be submitted under 505(b)(1)? A 505(b)(2) is "
         "NOT eligible for this voucher.",
         "sponsor's filing decision; note Pub. L. 117-9 (2021) narrowed this to "
         "505(b)(1) only, so a 505(b)(2) repurposing filing forfeits the voucher"),
        ("relies_on_pediatric_data", "s.529(a)(4)(D)",
         "Will it rely on clinical data from a pediatric population at "
         "pediatric dosages?",
         "sponsor's filing decision, not a drug property"),
        ("no_adult_indication_sought", "s.529(a)(4)(E)",
         "Does the original application avoid seeking an adult indication?",
         "sponsor's filing decision, not a drug property"),
    ]:
        crit.append(Criterion(key, cite, q, Decidability.DESIGN, Status.HUMAN,
                              note))

    # ---- 10. the clock
    if cand.earliest_possible_approval is None:
        st, note = Status.UNKNOWN, "no projected approval date supplied"
    elif cand.earliest_possible_approval <= SUNSET:
        margin = (SUNSET - cand.earliest_possible_approval).days
        st, note = Status.PASS, (f"projected approval "
                                 f"{cand.earliest_possible_approval} leaves "
                                 f"{margin} days of margin")
    else:
        over = (cand.earliest_possible_approval - SUNSET).days
        st, note = Status.FAIL, (f"projected approval "
                                 f"{cand.earliest_possible_approval} is "
                                 f"{over} days past the 30 Sep 2029 sunset; "
                                 f"reauthorisation would be required")
    crit.append(Criterion(
        "voucher_awardable_before_sunset", "s.529(b)(5)",
        "Can approval — and therefore the voucher award — land on or before "
        "30 September 2029?",
        Decidability.DATA, st, note))

    # ---- 11. the floor date. Trivially satisfied for anything filed now, but
    #          listed so the criterion set matches the statute rather than a
    #          remembered subset of it.
    if cand.earliest_possible_approval is None:
        st, note = Status.UNKNOWN, "no projected approval date supplied"
    elif cand.earliest_possible_approval > FLOOR:
        st, note = Status.PASS, f"approval would fall after {FLOOR}"
    else:
        st, note = Status.FAIL, f"approval on or before {FLOOR} cannot earn a voucher"
    crit.append(Criterion(
        "approved_after_30_sep_2016", "s.529(a)(4)(F)",
        "Is the approval after 30 September 2016?",
        Decidability.DATA, st, note))

    return Assessment(cand.name, crit)


if __name__ == "__main__":
    # worked example: everything passes except what a human must decide,
    # plus a sunset near-miss to show the FAIL path
    demo = Candidate(
        name="tiratricol", us_exclusion_verdict="NOT_IN_US",
        us_prevalence=1500, pediatric_onset=True,
        serious_or_life_threatening=True, us_therapy_exists=False,
        published_human_evidence=True,
        earliest_possible_approval=date(2029, 3, 1))
    print(assess(demo).report())
    print()
    late = Candidate(name="hypothetical-late-filer",
                     us_exclusion_verdict="NOT_IN_US",
                     earliest_possible_approval=date(2030, 3, 1))
    print(assess(late).report())
