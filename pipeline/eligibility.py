"""
FD&C Act s.529 (21 U.S.C. 360ff) rare pediatric disease PRV eligibility gate.

Encodes every statutory criterion separately and labels each by WHO can decide
it. The screening error that matters is not a missed candidate; it is a
candidate that looks eligible because a criterion nobody could evaluate was
quietly treated as satisfied.

Every criterion therefore returns one of PASS / FAIL / UNKNOWN / HUMAN, and the
overall verdict can never be ELIGIBLE while any criterion is UNKNOWN or HUMAN.
The best a machine can return is LIKELY_ELIGIBLE_PENDING_REVIEW.

Statutory text and FDA guidance relied on:
  - a rare pediatric disease is serious or life-threatening, primarily affects
    individuals aged from birth to 18 years, and is rare (US prevalence under
    200,000, or the not-cost-recoverable prong)
  - no active ingredient, INCLUDING ANY ESTER OR SALT of the active ingredient,
    may have been approved in any other application under 505(b)(1), 505(b)(2),
    505(j), 351(a) or 351(k)  <- this is the criterion rdh_diff.py screens
  - the application must be submitted under 505(b)(1) or 505(b)(2)
  - it must rely on clinical data derived from studies in a pediatric
    population, at pediatric dosages
  - the original application must not seek approval of an adult indication
  - it must qualify for priority review, i.e. offer a significant improvement
    in safety or effectiveness over available therapy
  - a voucher cannot be awarded for an approval after 30 September 2029
    (the current statutory sunset)

FDA guidance further confirms that a drug approved and used abroad but never
submitted to FDA can qualify, while a new pediatric use or formulation of a
drug already US-approved cannot.

Usage against pipeline output:

    from eligibility import Candidate, assess
    # verdict/basis come from a funnelA row (rdh_diff.py already ran the
    # exclusion test three layers deep); everything else is diligence input
    a = assess(Candidate(name="tiratricol",
                         us_exclusion_verdict="NOT_IN_US",
                         us_prevalence=1500, pediatric_onset=True,
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

SUNSET = date(2029, 9, 30)


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
    pediatric_onset: bool | None = None       # primarily affects ages 0-18
    serious_or_life_threatening: bool | None = None
    us_therapy_exists: bool | None = None
    published_human_evidence: bool = False
    earliest_possible_approval: date | None = None


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
        "no_prior_us_active_ingredient",
        "s.529(a)(4)(A)(iv) / 360ff(a)(4)(A)(iv)",
        "Has no active ingredient, including any ester or salt of it, been "
        "approved in any other US application?",
        Decidability.MACHINE, st, note))

    # ---- 2. rarity
    if cand.us_prevalence is None:
        st, note = Status.UNKNOWN, "US prevalence not supplied"
    elif cand.us_prevalence < 200_000:
        st, note = Status.PASS, f"US prevalence {cand.us_prevalence:,}"
    else:
        st, note = Status.FAIL, f"US prevalence {cand.us_prevalence:,} is not rare"
    crit.append(Criterion(
        "rare_under_200k", "s.529(a)(3)(B)",
        "Does the disease affect fewer than 200,000 people in the US?",
        Decidability.DATA, st, note))

    # ---- 3. primarily pediatric. No dataset carries this as a field.
    if cand.pediatric_onset is None:
        st, note = Status.HUMAN, ("no database holds 'primarily affects ages "
                                  "0-18'; must be read from the literature")
    elif cand.pediatric_onset:
        st, note = Status.PASS, "asserted primarily pediatric"
    else:
        st, note = Status.FAIL, "not primarily a pediatric population"
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
        "qualifies_for_priority_review", "s.529(a)(4)(A)(v)",
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
    for key, cite, q in [
        ("filed_as_505b1_or_505b2", "s.529(a)(4)(A)(i)",
         "Will the application be submitted under 505(b)(1) or 505(b)(2)?"),
        ("relies_on_pediatric_data", "s.529(a)(4)(A)(ii)",
         "Will it rely on clinical data from a pediatric population at "
         "pediatric dosages?"),
        ("no_adult_indication_sought", "s.529(a)(4)(A)(iii)",
         "Does the original application avoid seeking an adult indication?"),
    ]:
        crit.append(Criterion(key, cite, q, Decidability.DESIGN, Status.HUMAN,
                              "sponsor's filing decision, not a drug property"))

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
        "approval_before_sunset", "statutory sunset",
        "Can approval land on or before 30 September 2029?",
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
