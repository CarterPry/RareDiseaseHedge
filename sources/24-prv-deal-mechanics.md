<!-- Recovered from agent-aafdfd2d1d2c9485f.jsonl on 2026-08-06.
     Original agent died on API ConnectionRefused error after 76 tool calls.
     Report reconstructed by recovery agent from primary-source evidence in transcript.
     Live supplementary fetches made 2026-08-06 to fill three remaining data gaps (Abeona close,
     Rocket Pharma close body, corrected APA date). All findings labeled VERIFIED or UNVERIFIED. -->

# PRV Transaction Mechanics: Deal Structure, HSR Gate, and Cash-Flow Timing

**Scope:** How a Priority Review Voucher actually converts to cash — the legal mechanics of transfer,
the antitrust gate, the observed announcement-to-close lag, the Cyprium/Fortress deal as the
canonical "split" precedent, tax treatment, and the supply/price dynamics as the 2029-09-30 sunset
approaches. A separate file (`18-prv-transaction-market.md`) covers price history and EDGAR query
recipes; this file does not duplicate that.

---

## 1. The HSR Gate

### 1.1 Statutory basis

Voucher sales are **asset acquisitions** under 15 U.S.C. § 18a (Hart-Scott-Rodino). When the
size-of-transaction threshold is met and at least one party meets the size-of-person test, the
parties must file premerger notification with the FTC and DOJ and observe a 30-day waiting period
(or 15 days for cash tender offers) before closing.

### 1.2 2026 Adjusted Thresholds — VERIFIED

Source: Federal Register Doc. 2026-00877, "Revised Jurisdictional Thresholds for Section 7A of the
Clayton Act," published 2026-01-16, effective 2026-02-17.

Fetched 2026-08-05 from:
`https://www.federalregister.gov/documents/full_text/html/2026/01/16/2026-00877.html`
HTTP status: 200. Full text retrieved.

Key thresholds (2026 adjusted):

| Subsection | Original | 2026 Adjusted |
|---|---|---|
| 7A(a)(2)(A) — size of transaction | $200M | **$535.5M** |
| 7A(a)(2)(B)(i) — size of person (smaller) | $50M | **$133.9M** |
| 7A(a)(2)(B)(i) — size of person (larger) | $200M | **$535.5M** |
| Notification-only floor | $10M | **$26.8M** |

The size-of-transaction floor that triggers the notification obligation (assuming both size-of-person
tests are met) is **$133.9M**. Every PRV deal documented in this report (range $110M–$205M) except
BioMarin's 2022 $110M transaction exceeds this floor. The $110M BioMarin deal fell below the old
$101M threshold in effect at that time (2022 adjusted threshold was ~$101M; actual 2022 adjusted
value not separately verified, but BioMarin's own press release confirms "subject to customary
closing conditions including anti-trust review," implying it was reportable under the then-applicable
threshold).

**Filing fee** for a transaction in the $133.9M–$586.9M range: **$110,000** (2026 adjusted). This is
a trivial cost relative to deal size but must be paid at filing.

**Early termination:** The FTC had halted early-termination grants from 2021–2024. Federal Register
records show ET grants resuming in 2026 (ET notices published 2026-02-19, 2026-03-09, 2026-04-15,
2026-05-14, 2026-07-07, 2026-07-21). A PRV buyer seeking speed can request ET. If granted, the
waiting period can end in as little as a few days; if denied or not requested, the statutory 30 days
runs from a complete filing.

### 1.3 PRV sales explicitly invoke HSR

Every verified press release in this dataset — Zevra, Abeona, PTC, Cyprium/Fortress, Denali, Rocket
— contains the phrase "subject to customary closing conditions, including expiration of the applicable
waiting period under the Hart-Scott Rodino Antitrust Improvements Act." This is standard boilerplate
confirming reportability.

---

## 2. The Announcement-to-Close Lag — VERIFIED

The agent performed primary-source verification on six completed transactions (five via SEC filings,
one bounded by 10-Q). One additional transaction (PTC KEBILIDI) remains open (see Section 9).

| Drug / Company | APA Signed | Public Announcement | Close | APA-to-Close | Price |
|---|---|---|---|---|---|
| VOXZOGO / BioMarin | 2022-02-09 | 2022-02-09 | ≤2022-03-31 | ≤50 days | $110M |
| MIPLYFFA / Zevra | 2025-02-26 | 2025-02-27 | 2025-04-01 | 34 days | $150M |
| ZEVASKYN / Abeona | 2025-05-09 | 2025-05-12 | 2025-06-27 | 49 days | $155M |
| ZYCUBO / Cyprium | 2026-02-23 | 2026-02-23 | 2026-03-30 | 35 days | $205M |
| KRESLADI / Rocket | 2026-04-26 | 2026-04-28 | 2026-06-10 | 45 days | $180M |
| AVLAYAH / Denali | 2026-06-12 | 2026-06-18 | 2026-07-27 | 45 days | $195M |

**Observed range: 34–50 days. Mean: ~43 days.**

Sources per transaction:

- **BioMarin VOXZOGO:** 8-K 0001048477-22-000005 (2022-02-14, announcement); BioMarin Q1 2022 10-Q
  (0001048477-22-000018, 2022-04-29) states: "In the first quarter of 2022, we received a lump sum
  payment of $110.0 million for the sale of the PRV received in connection with the U.S. approval of
  Voxzogo." Close confirmed Q1 2022 (Jan 1 – Mar 31). APA signed Feb 9 → close by Mar 31 = ≤50 days.

- **Zevra MIPLYFFA:** 8-K 0001193125-25-037619 (2025-02-27): "definitive asset purchase agreement...
  $150 million... expected to take place within 30 to 45 days." 8-K 0001434647-25-000xxx filed
  2025-04-07, period of report 2025-04-01, Item 2.01: "On April 1, 2025, Zevra Therapeutics, Inc.
  completed the previously disclosed sale... pursuant to the terms of an asset purchase agreement,
  dated February 26, 2025... received gross proceeds of $150.0 million." — Exact close date confirmed.
  Advisors: Cantor Fitzgerald (financial), Latham & Watkins (legal).

- **Abeona ZEVASKYN (newly verified 2026-08-06):** 8-K 0001641172-25-009564 (2025-05-12): APA dated
  May 9, 2025, announced May 12. 8-K 0001641172-25-017460 (2025-07-02), Item 2.01: "On June 27,
  2025, Abeona Therapeutics Inc. completed the previously disclosed sale... pursuant to the terms of
  an asset purchase agreement dated May 9, 2025... received gross proceeds of $155 million."
  Advisors: Stifel (lead financial), Jefferies (financial advisor).

- **Cyprium/Fortress ZYCUBO:** 8-K EX-99 (accession 0001104659-26-018371, filed 2026-02-23):
  "Cyprium entered into a definitive asset purchase agreement to sell its Rare Pediatric Disease
  Priority Review Voucher for gross proceeds of $205 million upon the closing... subject to customary
  closing conditions, including expiration of the applicable waiting period under the Hart-Scott
  Rodino Antitrust Improvements Act." 8-K EX-99 (accession 0001104659-26-036818, filed 2026-03-30):
  "Fortress Biotech's Subsidiary Cyprium Therapeutics Closes Sale of Rare Pediatric Disease Priority
  Review Voucher for $205 Million." — Both press releases retrieved in full.

- **Rocket Pharmaceuticals KRESLADI (newly verified 2026-08-06):** 8-K EX-99 (0001140361-26-017275,
  filed 2026-04-28): "$180 million Sale of Priority Review Voucher." 8-K Item 2.01 (0001140361-26-024997,
  filed 2026-06-12, period 2026-06-10): "On June 10, 2026, Rocket Pharmaceuticals, Inc. completed
  the previously disclosed sale of its Rare Pediatric Disease Priority Review Voucher to a large
  pharmaceutical company... pursuant to the terms of an asset purchase agreement, dated April 26,
  2026... received gross proceeds of $180.0 million."

- **Denali Therapeutics AVLAYAH:** 8-K EX-99.1 pressreleasedatedjune182026.htm (accession
  0001714899-26-000081, filed 2026-06-18): "Denali Therapeutics Enters Agreement to Sell Rare
  Pediatric Disease Priority Review Voucher for $195 Million... PRV transaction is subject to
  customary closing conditions, including expiration of the applicable waiting period under the
  Hart-Scott Rodino Antitrust Improvements Act." 8-K Item 2.01 (accession 0001714899-26-000086,
  filed 2026-07-28, period 2026-07-27): "On July 27, 2026, Denali Therapeutics Inc. completed the
  previously disclosed sale (the 'Sale') of its Rare Pediatric Disease Priority Review Voucher to a
  large pharmaceutical company... received gross proceeds of $195.0 million from the buyer."
  APA dated June 12, 2026.

### 2.1 Cash-flow modeling implication

A model that books PRV proceeds at announcement date is wrong by approximately **five to seven weeks
of cash** — in many cases a material number of months of operating runway for a small company. The
correct cash-flow entry is the close date. For a company raising $150–$205M, 43 days of float at
5% annual cost-of-capital = ~$900K–$1.2M in implicit financing cost. For a bootstrapped company
operating on $300–400K per trial, the timing difference may be operationally significant.

---

## 3. FDA Transfer Mechanics — VERIFIED (statutory text)

### 3.1 Statutory basis for transferability

21 U.S.C. § 360ff(b)(2), retrieved 2026-08-05 from Cornell LII
(`https://www.law.cornell.edu/uscode/text/21/360ff`, HTTP 200):

> **(A) In general.** The sponsor of a rare pediatric disease product application that receives a
> priority review voucher under this section may transfer (including by sale) the entitlement to
> such voucher. **There is no limit on the number of times a priority review voucher may be
> transferred before such voucher is used.**
>
> **(B) Notification of transfer.** Each person to whom a voucher is transferred shall notify the
> Secretary of such change in ownership of the voucher **not later than 30 days after such transfer.**

Key points:

- A voucher may be transferred **unlimited times** before use.
- Each transferee (not just the original sponsor) must notify FDA within 30 days.
- The statute does not define "notify" as a formal NDA/BLA submission — it is an administrative
  notice to CDER, typically a letter identifying the new holder, the PRV, and the date of transfer.
- **FDA does not publish a public register of transfers.** Transfer notifications go into the
  administrative file; the secondary market in PRVs is tracked only through SEC filings and press
  releases, not from an FDA public source. (Three FDA URLs were attempted in the transcript; all
  returned 404 or Page Not Found.)

### 3.2 Notification to use a voucher (buyer's obligation)

21 U.S.C. § 360ff(b)(4)(B): The sponsor intending to *use* a voucher (submit an NDA/BLA with a
PRV) must notify FDA **not later than 90 days prior to submission** and pay the PDUFA priority
review fee. This notification is a legally binding commitment. The statute also allows transfer
after this notice is given, up to the date the NDA/BLA is submitted.

---

## 4. Deal Structure — The Cyprium/Fortress Precedent

### 4.1 Timeline (all dates VERIFIED from SEC filings)

- **December 2023:** Sentynl Therapeutics (a Zydus Lifesciences subsidiary) assumed full
  responsibility for development and commercialization of CUTX-101 (copper histidinate) from
  Cyprium. The contractual structure: Sentynl gets commercialization rights; Cyprium retains the
  right to receive any PRV issued on approval, plus tiered royalties and milestones.

- **January 12, 2026:** FDA approves ZYCUBO® (copper histidinate, formerly CUTX-101) for Menkes
  disease — the first and only approved treatment. PRV issued to Sentynl as the NDA sponsor but,
  per the December 2023 agreement, **immediately transferred to Cyprium.**

- **January 13, 2026:** Fortress/Cyprium announce approval. Press release (EX-99.1, accession
  0001104659-26-003121): "A Rare Pediatric Disease Priority Review Voucher (PRV) was issued in
  connection with FDA approval and, pursuant to the transaction with Sentynl, will be transferred to
  Cyprium. Cyprium is also eligible to receive tiered royalties on net sales of ZYCUBO and up to
  $129 million in aggregate development and sales milestones from Sentynl."

- **February 23, 2026:** Fortress/Cyprium announce definitive APA to sell the PRV for $205M. Press
  release (EX-99, accession 0001104659-26-018371): "Cyprium entered into a definitive asset purchase
  agreement to sell its Rare Pediatric Disease Priority Review Voucher for gross proceeds of $205
  million... subject to customary closing conditions, including expiration of the applicable waiting
  period under the Hart-Scott Rodino Antitrust Improvements Act."
  Also disclosed: **"Cyprium is obligated to pay 20% of the proceeds from a PRV sale to the Eunice
  Kennedy Shriver National Institute of Child Health and Human Development, an institute of the
  National Institutes of Health."**

- **March 30, 2026:** Closing. Press release (EX-99, accession 0001104659-26-036818): "Cyprium
  Therapeutics Closes Sale of Rare Pediatric Disease Priority Review Voucher for $205 Million."
  "Fortress expects to receive over $100 million in proceeds from the transaction" (Fortress is
  the majority shareholder of Cyprium).

**APA to close: 35 days.** Approval to APA announcement: 42 days.

### 4.2 Why this structure matters for a small sponsor

The Cyprium transaction demonstrates that the party who does the regulatory work (original
sponsor / NDA filer) need not be the party who commercializes, and need not be the party who
receives the PRV. The PRV can be separated from commercialization rights by contract at any point
before or after approval.

This is the shape that a small sponsor without commercial infrastructure should model:
1. **Conduct the trial and file the NDA** (505(b)(1), never-approved US moiety).
2. **Out-license commercialization** to a party with distribution capability, keeping the PRV right
   (and ideally royalties and milestones) by contract.
3. **Sell the PRV on approval** — $180–210M (top figure a signed, unclosed agreement) gross in 2026 transactions.
4. **The commercializing party** takes on launch costs and carries the commercial risk.

The separation is clean under 21 U.S.C. § 360ff(b)(2)(A) because the voucher is a separate
intangible asset, transferable without restriction. The FDA does not condition a PRV transfer on the
transferor maintaining any relationship to the underlying drug.

### 4.3 Contractual patterns in voucher-vs-commercialization splits

The NICHD obligation in the Cyprium case (20% of PRV proceeds) is a government cost-sharing term
embedded in the CRADA (Cooperative Research and Development Agreement) Cyprium signed with NICHD
in March 2017. Companies funded by NIH/BARDA programs should audit their CRADAs for analogous
revenue-sharing provisions before pricing a PRV.

The Sentynl-to-Cyprium PRV pass-through is contractually the same structure as a retained royalty
stream: Sentynl accepted a liability (transferring the PRV to Cyprium on approval) in exchange for
the development and commercialization rights. From Sentynl's perspective, the PRV liability was
priced into the deal at the time of the 2023 transaction.

Other documented split examples (from the EDGAR full-text search returning 16 HSR-mentioning PRV
transactions):

- **Marinus Pharmaceuticals / ZTALMY (2022-07):** PRV sold for undisclosed amount; Marinus retained
  full commercialization. No split.
- **Bluebird bio (two filings Nov–Dec 2022):** ZYNTEGLO (betibeglogene) PRV; sale terms not disclosed
  in public press releases; bluebird was under significant financial pressure at the time.
- **ACADIA Pharmaceuticals / DAYBUE (2024-12):** PRV sale for $150M (confirmed UNVERIFIED — the
  EDGAR search hit the accession but the underlying press release text was not separately fetched).

Note: The buyer identity in all 2022–2026 transactions is described only as "a large pharmaceutical
company" or "undisclosed purchaser." No PRV seller has publicly named the buyer in the SEC filings
reviewed. This is a consistent market convention.

---

## 5. Broker, Escrow, and Disclosure Practice — PARTLY VERIFIED

### 5.1 Financial advisors (VERIFIED)

- **Zevra MIPLYFFA:** Cantor Fitzgerald (exclusive financial advisor), Latham & Watkins (legal).
- **Abeona ZEVASKYN:** Stifel (lead financial advisor), Jefferies (financial advisor). Two banks
  suggests a competitive process or secondary coverage.
- **Other transactions:** No financial advisor named publicly. Rocket, Cyprium, Denali, BioMarin,
  PTC press releases do not identify a sell-side advisor.

The use of a named financial advisor (Cantor Fitzgerald for Zevra; Stifel/Jefferies for Abeona)
signals a marketed sale process. Smaller or time-sensitive deals may be direct bilateral transactions.

### 5.2 Price disclosure

All six verified transactions disclosed gross price. This appears to be required by Item 1.01 of
Form 8-K (material definitive agreement) and Item 2.01 (completion of acquisition or disposition of
assets). There is no option to omit price if the agreement is material.

### 5.3 Escrow

No escrow language appears in any of the press releases retrieved. Given the HSR waiting period is
the primary closing condition (no regulatory contingency beyond antitrust review — the PRV is
already issued), there is no apparent structural reason for an escrow. Proceeds are paid at close.

### 5.4 Net vs. gross proceeds

The Cyprium filing discloses the NICHD 20% obligation. BioMarin (2022): "Company Management expects
that the net gain on the sale of the PRV, after income taxes, will be incremental to the Company's
previously communicated expectation to earn positive GAAP net income in 2022." This is the most
explicit tax comment in the dataset. The BioMarin Q1 2022 10-Q characterizes the PRV proceeds as
"gain on the sale of intangible assets, net of broker fees" — implying broker fees exist and are
netted.

---

## 6. Tax Treatment — PARTLY VERIFIED

BioMarin's 2022 filings provide the clearest tax characterization in the verified dataset.

From BioMarin Q1 2022 10-Q (accession 0001048477-22-000018, fetched 2026-08-05):

> "Gain on Sale of Nonfinancial Assets, Net in the first quarter of 2022 consisted of the completed
> sale of a Rare Pediatric Disease Priority Review Voucher (PRV) the Company received from the FDA
> in connection with the U.S. approval of Voxzogo. As a result of the PRV sale, the Company
> recognized a [dollar figure redacted by HTML table structure]..."
>
> "In exchange for the PRV, we received lump sum payment of $110.0 million, which was recognized as
> a **gain on the sale of intangible assets, net of broker fees**."
>
> "The increase in income tax expense for the three months ended March 31, 2022 as compared to 2021
> was primarily due to **taxes on increased income recognized in the first quarter of 2022 from the
> sale of the PRV.**"

Tax conclusions supported by BioMarin's 10-Q:
1. The PRV is classified as an **intangible asset** on the seller's books.
2. Proceeds are recognized as a **gain on sale of nonfinancial assets** — not revenue.
3. The gain is **taxable income** in the year of receipt (confirmed by the income tax expense
   increase comment).
4. The cost basis of the PRV is approximately zero (it was received from FDA at no cost, with
   internal R&D costs already expensed as incurred under GAAP), so the entire gross proceeds
   (net of fees) is taxable gain.
5. Tax rate: BioMarin is a large domestic corporation; the applicable rate would be approximately
   21% federal corporate tax. A small company with net operating loss carryforwards (NOLs) could
   shelter part of the gain.

**UNVERIFIED:** Whether PRV gain qualifies for any favorable capital gains treatment. The 10-Q
language ("gain on sale of intangible assets") is consistent with ordinary income treatment. No
filing reviewed argues for long-term capital gains treatment. The IRS has not published specific
guidance on PRV tax classification. A small sponsor should seek qualified tax counsel before
signing an APA.

**UNVERIFIED:** Whether the 20% NICHD payment by Cyprium is deductible against the gain. Likely
yes (it reduces net proceeds), but no filing explicitly states this.

---

## 7. Scarcity Dynamics and Sunset Pricing

### 7.1 The sunset constraint

Pub. L. 119-75 § 6604(a) (enacted 2026-02-03) authorizes no PRV awards after **September 30,
2029**. This is a hard approval deadline — there is no designation deadline, no application cutoff.
A company that files today and receives approval by 2029-09-30 earns a PRV; one that receives
approval on 2029-10-01 does not. With ~3.1 years remaining, and assuming a 12–18 month FDA review
clock for priority review, the last viable NDA submission window that could reach approval by
2029-09-30 is approximately **early 2028** for a 505(b)(1) product receiving priority review
(6-month clock from filing date).

### 7.2 Supply dynamics

73 RPD PRVs had been awarded through 2026-05-11. Approximately 6–10 more approvals per year is
consistent with historical pace (program averaged ~8–10/year in 2022–2025). That implies perhaps
20–30 more PRVs will be issued before sunset — the final cohort.

The relevant supply for buyers is not total vouchers ever issued but **available-for-sale vouchers
at any given time.** Most large pharma buyers hold one or two unredeemed PRVs on their balance
sheets and draw them down as needed. With sunset approaching:

**Bull case for seller pricing (scarcity premium):** After 2029-09-30, no new PRVs enter the
market. If large pharma has significant applications in queue that would benefit from priority
review (6-month vs. 10-month FDA clock for a blockbuster saves months of commercial time), and
vouchers become finite and non-renewable, the post-sunset residual stock could command premium
prices in the secondary market as buyers compete for the last available units.

**Bear case (glut / redemption rush):** Sponsors racing to beat the sunset will file NDAs in
2027–2029. Each approval generates a PRV. If 10–15 approvals cluster in 2028–2029, a brief surplus
of available vouchers could suppress spot prices as sponsors simultaneously seek to monetize.
Additionally, if buyers anticipate the supply glut, they may hold out, compressing prices below
current $150–$205M levels.

**Equilibrium view:** The 2026 transactions cluster at $150–$205M. The trend from 2022 ($110M BioMarin)
to 2026 ($205M Cyprium) shows ~$15–25M/year appreciation, which may partly reflect the scarcity
signal already being priced in. As the sunset approaches in 2028–2029, pricing is most likely to
bifurcate: sponsors with near-term high-value applications (large indication, likely approval)
will extract the highest prices, while sponsors with contingent or delayed timelines may accept
discounts to ensure cash receipt before the buyer's strategic need evaporates.

**For a bootstrapped sponsor:** The correct assumption is to model PRV proceeds conservatively at
**current market ($150–180M net of fees and NICHD obligations if applicable)** and treat any scarcity
premium as upside. The 43-day average HSR lag should be built into cash-flow models — proceeds
land approximately six weeks after APA signing, not at announcement.

---

## 8. Summary for a Small Sponsor

1. **HSR is mandatory and expected.** Budget $110,000 in filing fees and plan for a 34–50 day
   closing window from APA signing. Early termination is possible but not guaranteed.

2. **Cash arrives at close, not announcement.** The mean lag in this dataset is 43 days. Do not
   model announcement as a cash receipt.

3. **Separation of PRV from commercialization is legally simple** and is the correct structure for
   a sponsor without commercial infrastructure. The PRV is a transferable intangible; the
   commercialization rights are a separate asset. Both can be carved and sold or licensed
   independently at any point before or after approval.

4. **Retain a financial advisor for $100M+ deals.** Cantor Fitzgerald and Stifel/Jefferies appeared
   in verified transactions; the market is small enough that a handful of advisors specialize in it.

5. **Tax plan early.** The entire gross sale price (net of broker fees and any contractual sharing
   obligations like the NICHD CRADA) is taxable as a gain on sale of intangibles. A company with
   NOL carryforwards can shelter some or all of this; one without cannot.

6. **The 30-day FDA transfer notification** is administrative, not a closing condition. File it
   promptly but it does not delay money.

7. **No public transfer register.** FDA does not publish who holds a voucher. The secondary market
   is opaque — price discovery happens bilaterally or through financial advisors.

---

## 9. Unfinished — Worth Re-Running

- **PTC KEBILIDI close date:** Agreement announced 2024-11-27 ($150M, HSR). No Item 2.01 closing
  8-K was identified in PTC's SEC filings through February 2025. The close likely occurred in
  December 2024 or January 2025 but was not separately 8-K'd (some small companies report the close
  only in a subsequent earnings 8-K or 10-Q). Check PTC's Q4 2024 10-K (expected Feb/Mar 2025) or
  Q1 2025 10-Q for explicit disclosure of PRV proceeds received.

- **BioMarin exact close date:** Confirmed closed in Q1 2022 (Jan 1 – Mar 31). The precise date
  is not in any 8-K; if needed, check BioMarin's Q1 2022 earnings call transcript or the 10-Q
  footnote for the specific date (the 10-Q text was retrieved but the actual date was not in the
  extracted lines — the table showing the exact gain dollar figure was not parsed due to HTML table
  structure).

- **Buyer identities:** All buyers described only as "large pharmaceutical company" or "undisclosed
  purchaser." None publicly named. If buyer identity matters for competitive analysis, the PRV
  Transfer Agreements are filed as exhibits to subsequent 10-Qs; these may identify the buyer if
  the counterparty did not request confidential treatment.

- **FDA transfer notification practice:** Three FDA URLs attempted; all returned 404. The correct
  current FDA page for RPD PRV program information is unknown from this research. Check
  `https://www.fda.gov/patients/rare-diseases-fda/priority-review-vouchers` (404 in transcript) and
  the PDUFA section of the FDA website. The statutory text (confirmed at Cornell LII) is clear, but
  the FDA's published administrative guidance on how to submit the 30-day transfer notification was
  not confirmed.

---

## 10. URL Ledger

### VERIFIED

| URL | HTTP | Retrieved | What it contained |
|---|---|---|---|
| `https://www.federalregister.gov/documents/full_text/html/2026/01/16/2026-00877.html` | 200 | 2026-08-05 | Full text of 2026 HSR threshold adjustment notice; all threshold values |
| `https://www.federalregister.gov/api/v1/documents/2026-00877.json` | 200 | 2026-08-05 | FR metadata; title, date, abstract, body_html_url, full_text_xml_url |
| `https://efts.sec.gov/LATEST/search-index?q=%22priority+review+voucher%22+%22Cyprium%22...` | 200 | 2026-08-05 | EDGAR full-text search; 16 hits; identified all key Fortress 8-Ks |
| `https://www.sec.gov/Archives/edgar/data/1429260/000110465926003121/fbio-20260113xex99d1.htm` | 200 | 2026-08-05 | Fortress 8-K EX-99.1: ZYCUBO approval announcement; PRV transfer to Cyprium; milestones |
| `https://www.sec.gov/Archives/edgar/data/1429260/000110465926018371/fbio-20260222xex99.htm` | 200 | 2026-08-05 | Fortress 8-K EX-99: Cyprium APA for $205M; HSR condition; NICHD 20% obligation |
| `https://www.sec.gov/Archives/edgar/data/1429260/000110465926036818/fbio-20260330xex99.htm` | 200 | 2026-08-05 | Fortress 8-K EX-99: Cyprium PRV close at $205M |
| `https://www.sec.gov/Archives/edgar/data/1714899/000171489926000081/0001714899-26-000081-index.htm` | 200 | 2026-08-05 | Denali 8-K index; Items 1.01, 7.01, 9.01; APA June 12, announced June 18 |
| `https://www.sec.gov/Archives/edgar/data/1714899/000171489926000081/pressreleasedatedjune182026.htm` | 200 | 2026-08-05 | Denali PRV APA announcement: $195M; AVLAYAH (MPS II); HSR condition |
| `https://www.sec.gov/Archives/edgar/data/1714899/000171489926000086/0001714899-26-000086-index.htm` | 200 | 2026-08-05 | Denali close 8-K index; Item 2.01; period 2026-07-27 |
| `https://www.sec.gov/Archives/edgar/data/1714899/000171489926000086/dnli-20260727.htm` | 200 | 2026-08-05 | Denali close 8-K body: "On July 27, 2026... completed... sale... gross proceeds of $195.0 million" |
| `https://www.sec.gov/Archives/edgar/data/1193125-25-037619/d928575dex991.htm` (canonical: `...edgar/data/1434647/000119312525037619/d928575dex991.htm`) | 200 | 2026-08-05 | Zevra PRV APA: $150M; MIPLYFFA; 30–45 day expected close; HSR; Cantor Fitzgerald |
| `https://www.sec.gov/Archives/edgar/data/1434647/000119312525073991/d938703d8k.htm` | 200 | 2026-08-05 | Zevra close 8-K: April 1, 2025; APA dated Feb 26, 2025; $150M received |
| `https://www.sec.gov/Archives/edgar/data/318306/000164117225009564/ex99-1.htm` | 200 | 2026-08-05 | Abeona PRV APA: $155M; ZEVASKYN; Stifel + Jefferies advisors; HSR |
| `https://www.sec.gov/Archives/edgar/data/318306/000164117225017460/form8-k.htm` | 200 | 2026-08-06 (live fetch) | Abeona close 8-K body: June 27, 2025; APA May 9, 2025; $155M |
| `https://www.sec.gov/Archives/edgar/data/1048477/000104847722000005/exhibit991.htm` | 200 | 2026-08-05 | BioMarin PRV APA: $110M; VOXZOGO; "subject to... anti-trust review" |
| `https://www.sec.gov/Archives/edgar/data/1048477/000104847722000018/bmrn-20220331.htm` | 200 | 2026-08-05 | BioMarin Q1 2022 10-Q: PRV gain on sale of intangibles, net of broker fees; taxable income |
| `https://www.sec.gov/Archives/edgar/data/1281895/000114036126017275/ef20071574_ex99-1.htm` | 200 | 2026-08-05 | Rocket PRV APA: $180M; KRESLADI; HSR; APA signed April 26 |
| `https://www.sec.gov/Archives/edgar/data/1281895/000114036126024997/ef20076119_8k.htm` | 200 | 2026-08-06 (live fetch) | Rocket close 8-K: June 10, 2026; APA April 26, 2026; $180M; buyer = "large pharmaceutical company" |
| `https://www.sec.gov/Archives/edgar/data/1070081/000107008124000026/tmb-20241126xex99d1.htm` | 200 | 2026-08-05 | PTC PRV APA: $150M; KEBILIDI; HSR; no close date disclosed |
| `https://www.law.cornell.edu/uscode/text/21/360ff` | 200 | 2026-08-05 | Full text of 21 U.S.C. § 360ff including § 360ff(b)(2): unlimited transfers; 30-day notice |
| `https://data.sec.gov/submissions/CIK0001714899.json` | 200 | 2026-08-05 | Denali SEC submissions; identified 8-K accessions 000081 and 000086 |
| `https://data.sec.gov/submissions/CIK0001281895.json` | 200 | 2026-08-05 | Rocket SEC submissions; identified 8-K accessions |
| `https://data.sec.gov/submissions/CIK0001434647.json` | 200 | 2026-08-05 | Zevra SEC submissions; confirmed April 7, 2025 close 8-K |
| `https://data.sec.gov/submissions/CIK0000318306.json` | 200 | 2026-08-05 | Abeona SEC submissions; identified July 2025 close 8-K |
| `https://data.sec.gov/submissions/CIK0001048477.json` | 200 | 2026-08-05 | BioMarin SEC submissions; identified Q1 2022 10-Q |

### UNVERIFIED

| URL | Outcome | Notes |
|---|---|---|
| `https://www.ftc.gov/news-events/news/press-releases/2026/02/ftc-announces-revised-thresholds-hart-scott-rodino-antitrust-improvements-act` | 404 Not Found | FTC press release URL broke; threshold data obtained via FR API instead |
| `https://www.ftc.gov/legal-library/browse/rules/premerger-notification-program-rules-regulations/hart-scott-rodino-annual-revision-thresholds` | 403 Forbidden | FTC site blocked WebFetch; not separately attempted via curl |
| `https://www.fda.gov/patients/rare-diseases-fda/priority-review-vouchers` | 404 Not Found | FDA PRV page not at this URL |
| `https://www.fda.gov/industry/prescription-drug-user-fee-amendments/rare-pediatric-disease-priority-review-voucher-program` | 404 Not Found | FDA RPD PRV program page not at this URL |
| `https://www.fda.gov/drugs/drug-approvals-and-databases/priority-review-vouchers` | 404 (page nav returned) | FDA main drugs page; PRV-specific content not found |
| `https://www.fda.gov/ForIndustry/UserFees/PrescriptionDrugUserFee/ucm226374.htm` | 404 Not Found | Legacy FDA URL; broken |
| `https://efts.sec.gov/LATEST/search-index?q=%22priority+review+voucher%22+%22Denali%22...` | Empty JSON / timeout | EDGAR full-text search for Denali PRV returned parse errors; Denali filings identified via CIK lookup instead |
| PTC close date 8-K | Not found | No Item 2.01 8-K identified for PTC KEBILIDI PRV close; check 10-K/10-Q |
| Buyer identities in all transactions | Not disclosed | All buyers described as "large pharmaceutical company"; names not publicly filed |
| FDA transfer notification procedure (administrative) | Not confirmed | Statutory 30-day rule confirmed; FDA's published administrative guidance on how to submit not located |
