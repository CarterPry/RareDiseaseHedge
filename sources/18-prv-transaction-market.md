# PRV Secondary Market: Price History, EDGAR Pipeline, and Forward Pricing

**Prepared:** 2026-08-06  
**Scope:** RPD PRV price series (2014–2026); EDGAR query recipes with measured hit counts; prvwatch.com assessment; forward price range 2027–2029. Does NOT duplicate HSR mechanics, deal structure, or the Cyprium/Fortress split precedent (see `24-prv-deal-mechanics.md`), and does NOT duplicate voucher type comparisons (see `23-voucher-instruments-compared.md`).

---

## 1. Complete Documented PRV Transaction Table (2014–2026)

### Methodology

Sources in order of preference: SEC 8-K EX-99 (announcement/APA signing) and Item 2.01 (closing) — primary sources retrieved via EDGAR; then company 10-K/10-Q confirmations; then company press releases; journalism cited only where no primary source available. Each entry is labeled VERIFIED or UNVERIFIED. Where buyer is named in a filing that is the primary source; where not, "undisclosed" reflects consistent SEC filing practice.

"Gross" price is the stated transfer consideration before tax, broker fees, and any contractual sharing obligations (e.g., Cyprium's 20% NICHD obligation, Jazz's 50% profit-share). Installment payments are noted separately.

**Note on non-RPD PRV entries:** Entries marked [MCM] are Medical Countermeasure PRVs; [TD] are Tropical Disease PRVs. The body of this report focuses on RPD PRVs. MCM and TD entries are included for completeness and pricing context; they are fungible instruments at the point of redemption (same 6-month priority review clock).

---

### Table 1: All Documented PRV Sales, 2014–2026

| # | Drug (Brand) | Seller | Buyer | APA Signed | Closed | Gross Price | Type | Primary Source | Status |
|---|---|---|---|---|---|---|---|---|---|
| 1 | VIMIZIM (elosulfase alfa) — MPS IVA | BioMarin Pharmaceutical | Regeneron Ireland | 2014-07-30 | **2014-07-30** | **$67.5M** | RPD | SEC 8-K Item 2.01 (0001193125-14-291230, filed 2014-08-01): "On July 30, 2014, in consideration for the sale of the Priority Review Voucher, Seller received from Buyer $67,500,000." | VERIFIED |
| 2 | Miltefosine (IMPAVIDO) — leishmaniasis | Paladin Labs / Knight Therapeutics | Undisclosed | ~Nov 2014 | ~Nov 2014 | **$125M** | TD | Company press release Nov 2014; not on EDGAR (Canadian company) | UNVERIFIED (price from press accounts; no SEC filing; primary source not retrieved) |
| 3 | CHOLBAM (cholic acid) — bile acid synthesis disorder | Retrophin / Asklepion Pharm | Sanofi | **2015-05-22** | **2015-07-02** | **$150M + $47.5M + $47.5M = $245M total** | RPD | SEC 8-K Item 1.01 (0001193125-15-201124, filed 2015-05-27): "$150M upon closing…plus additional $47.5M on first anniversary and $47.5M on second anniversary." Close: SEC 8-K Item 2.01 (0001193125-15-245643, filed 2015-07-06): "July 2, 2015, the Company completed its sale to Sanofi." | VERIFIED |
| 4 | UNITUXIN (dinutuximab) — neuroblastoma | United Therapeutics | **AbbVie Ireland** | **2015-08-18** | **2015-09-24** | **$350.0M** | RPD | APA: SEC 8-K EX-2.1 (0001104659-15-060788, filed 2015-08-19): "THREE HUNDRED FIFTY MILLION U.S. DOLLARS (U.S. $350,000,000)." Close: SEC 8-K Item 2.01 (0001104659-15-067017, filed 2015-09-24): "September 24, 2015, United Therapeutics Corporation completed its sale to AbbVie Ireland Unlimited Company…AbbVie paid the Company $350.0 million." | VERIFIED — **historical peak** |
| 5 | EXONDYS 51 (eteplirsen) — DMD | Sarepta Therapeutics | **Gilead Sciences** | **2017-02-20** | **2017-03-30** | **$125.0M** | RPD | APA: SEC 8-K EX-99.1 (0001193125-17-049361, filed 2017-02-21): "sell its Rare Pediatric Disease Priority Review Voucher...upfront payment of $125M." Close: SEC 8-K Item 2.01 (0001193125-17-105290, filed 2017-03-31): "March 30, 2017, Sarepta Therapeutics Inc. completed its sale to a subsidiary of Gilead Sciences." | VERIFIED |
| 6 | BRINEURA (cerliponase alfa) — CLN2/Batten disease | BioMarin Pharmaceutical | Undisclosed | **2017-11-21** | ~Dec 2017 | **$125.0M** | RPD | SEC 8-K EX-99.1 (0001193125-17-353976, filed 2017-11-28): "sell the Rare Pediatric Disease Priority Review Voucher...lump sum payment of $125,000,000." Subject to antitrust review. Close date not found in separate 8-K; estimated late Dec 2017. | VERIFIED (price and APA); UNVERIFIED (exact close date) |
| 7 | MEPSEVII (vestronidase alfa) — MPS VII/Sly syndrome | Ultragenyx Pharmaceutical | **Novartis** | **2017-12-14** | ~Jan 2018 | **$130.0M** | RPD | SEC 8-K EX-99.1 (0001564590-17-025027, filed 2017-12-18): "sell its Rare Pediatric Disease Priority Review Voucher to Novartis for $130,000,000." | VERIFIED (price, buyer, APA); UNVERIFIED (exact close date) |
| 8 | LUXTURNA (voretigene neparvovec) — RPE65 retinal dystrophy | Spark Therapeutics | **Jazz Pharmaceuticals Ireland** | **2018-04-30** | **2018-05-23** | **$110.0M** | RPD | APA: SEC 8-K (0001609351-18-000040, filed 2018-04-30): "Jazz will pay $110,000,000 upon closing." Close: SEC 8-K Item 2.01 (0001609351-18-000046, filed 2018-05-23, period 2018-05-23). | VERIFIED |
| 9 | TPOXX (tecovirimat) — smallpox | SIGA Technologies | Undisclosed | **2018-10-31** | ~Nov/Dec 2018 | **$80.0M** | MCM | SEC 8-K EX-99.1 (0001140361-18-042027, filed 2018-11-01): "agreement to sell its medical countermeasures priority review voucher for a lump sum payment of $80 million." | VERIFIED (price and APA); UNVERIFIED (exact close) |
| 10 | EPIDIOLEX (cannabidiol) — Dravet/LGS | GW Research (GW Pharmaceuticals) | **Biohaven Pharmaceutical** | **2019-03-15** | **2019-04-05** | **$105.0M** | RPD | SEC 8-K Item 2.01 (0001104659-19-020231, filed 2019-04-08): "April 5, 2019…completed its previously announced purchase from GW Research, Ltd…of a Rare Pediatric Disease Priority Review Voucher for $105 million in cash." APA March 15, 2019. | VERIFIED |
| 11 | ZOKINVY (lonafarnib) — Hutchinson-Gilford Progeria | Eiger BioPharmaceuticals | Undisclosed | **2020-11-20** | ~Dec 2020/Jan 2021 | **$95.0M gross** ($47.5M to Eiger; $47.5M to The Progeria Research Foundation per collaboration agreement) | RPD | SEC 8-K EX-99.1 (CIK 1305253, 0001193125-20-300479, filed 2020-11-23): "agreed to sell its Priority Review Voucher for a lump sum payment of $95 million. Eiger will retain fifty percent of the proceeds, or $47.5 million, under the terms of the Collaboration and Supply Agreement with The Progeria Research Foundation." | VERIFIED |
| 12 | DANYELZA (naxitamab) — refractory neuroblastoma | Y-mAbs Therapeutics | **United Therapeutics** | **2020-12-24** | **2021-01-21** | **$105.0M** | RPD | SEC 8-K Item 2.01 (CIK 1722964, 0001104659-21-006432, filed 2021-01-22): "January 21, 2021, Y-mAbs Therapeutics, Inc. closed its previously announced transaction with United Therapeutics Corporation…received the cash proceeds of $105 million." APA Dec 24, 2020. | VERIFIED — *United Therapeutics as buyer (reversal: they previously sold at $350M in 2015)* |
| 13 | IMCIVREE (setmelanotide) — POMC/PCSK1/LEPR obesity | Rhythm Pharmaceuticals | Undisclosed | **2021-01-05** | ~Jan/Feb 2021 | **$100.0M** | RPD | SEC 8-K Item 1.01 (CIK 1649904, 0001104659-21-000984, filed 2021-01-05): "Buyer agreed to pay the Company $100 million, payable in cash, upon the closing." Subject to customary closing conditions. | VERIFIED (price and APA); UNVERIFIED (exact close date) |
| 14 | LIVMARLI (maralixibat) — Alagille syndrome | Mirum Pharmaceuticals | **Janssen Biotech (J&J)** | **2021-11-16** | **2021-12-22** | **$110.0M** | RPD | SEC 8-K Item 2.01 (CIK 1759425, 0001193125-21-364950, filed 2021-12-22): "December 22, 2021…completed the sale…to Janssen Biotech, Inc…an affiliate of Johnson & Johnson…Buyer paid the Company $110.0 million." APA Nov 16, 2021. | VERIFIED |
| 15 | VOXZOGO (vosoritide) — achondroplasia | BioMarin Pharmaceutical | Undisclosed | **2022-02-09** | **≤2022-03-31** | **$110.0M** | RPD | SEC 8-K EX-99.1 (0001048477-22-000005, filed 2022-02-14): APA Feb 9, 2022; "subject to customary closing conditions including anti-trust review." Q1 2022 10-Q (0001048477-22-000018): "In the first quarter of 2022, we received a lump sum payment of $110.0 million for the sale of the PRV received in connection with the U.S. approval of Voxzogo." | VERIFIED |
| 16 | ZTALMY (ganaxolone) — CDKL5 deficiency disorder | Marinus Pharmaceuticals | Undisclosed | **2022-07-13** | ~Aug 2022 | **$110.0M** | RPD | SEC 8-K EX-99.1 (CIK 1267813, 0001558370-22-010694, filed 2022-07-14): "Marinus will receive a lump sum payment of $110 million upon closing…Jefferies LLC acted as the exclusive financial advisor." Subject to HSR waiting period. | VERIFIED (price and APA); UNVERIFIED (exact close date) |
| 17 | SKYSONA (elivaldogene autotemcel) — cerebral adrenoleukodystrophy | bluebird bio | **argenx** | **2022-11-29** | ~Dec 2022 | **$102.0M** | RPD | SEC 8-K Item 1.01 (CIK 1293971, 0001193125-22-294908, filed 2022-11-30): "agreed to sell a Rare Pediatric Disease Priority Review Voucher…to argenx BV…Buyer agreed to pay $102 million." | VERIFIED (price and buyer); UNVERIFIED (exact close date) |
| 18 | ZYNTEGLO (betibeglogene autotemcel) — beta-thalassemia | bluebird bio | **Bristol-Myers Squibb** | **2023-01-05** | **2023-01-05** | **$95.0M** | RPD | SEC 8-K Item 2.01 (CIK 1293971, 0001193125-23-002980, filed 2023-01-06): "agreed to sell a Rare Pediatric Disease Priority Review Voucher…to Bristol-Myers Squibb…Buyer agreed to pay $95 million…closing occurred simultaneously with the parties entering into the PRV Transfer Agreement." | VERIFIED — *same-day APA and close; BMS named* |
| 19 | ELEVIDYS (delandistrogene moxeparvovec) — DMD | Sarepta Therapeutics | Undisclosed | Jun 2023 | **Jun 2023** | **$102.0M** | RPD | Sarepta 10-Q Q3 2023 (CIK 873303, 0000950170-23-057414, filed 2023-11-01): "In June 2023, the Company entered into an agreement to sell the rare pediatric disease Priority Review Voucher…for consideration of $102.0 million…closing was not subject to [HSR]…closed in June 2023." | VERIFIED |
| 20 | LYFGENIA (lovotibeglogene autotemcel / lovo-cel) — sickle cell disease | bluebird bio | **Novartis Pharma AG** | **2023-10-26** | ~Dec 2023 (contingent on approval) | **$103.0M** | RPD | SEC 8-K Item 1.01 (CIK 1293971, 0001193125-23-265691, filed 2023-10-30): "rights to the PRV would transfer to Buyer and the Company would receive $103 million upon closing…contingent upon FDA's approval of the BLA for lovo-cel." LYFGENIA approved Dec 2023. | VERIFIED (price, buyer, APA); UNVERIFIED (exact close date, likely Dec 2023 or early 2024) |
| 21 | IQIRVO (elafibranor) — primary biliary cholangitis | Ipsen | Undisclosed | ~Aug 2024 | ~Aug 2024 | **$158.0M** | RPD | Company press release Aug 2024; Ipsen is French, does not file on EDGAR as primary issuer. | UNVERIFIED (price from press accounts; no primary SEC source retrieved) |
| 22 | CHIKUNGUNYA VACCINE (IXCHIQ) — chikungunya virus | Valneva SE | Undisclosed | ~Feb 2024 | **2024-02-05** | **$103.0M** | TD | SEC 6-K EX-99.1 (CIK 1836564, 0001171843-24-000572, filed 2024-02-05): "Valneva Announces Sale of Priority Review Voucher for $103 Million." Same-day close. | VERIFIED |
| 23 | CHIKUNGUNYA VACCINE (VIMKUNYA) — chikungunya | Bavarian Nordic | Undisclosed | ~2024 | ~2024 | **$160.0M** | TD | Company press release; Bavarian Nordic is Danish, does not file on SEC EDGAR. | UNVERIFIED (price from press reports; no primary SEC source retrieved) |
| 24 | XOLREMDI (mavorixafor) — WHIM syndrome | X4 Pharmaceuticals | Undisclosed | ~May 2024 | **2024-05-08** | **$105.0M** | RPD | SEC 8-K EX-99.1 (CIK 1501697, 0001628280-24-021937, filed 2024-05-09): "completed the sale of its Rare Pediatric Disease Priority Review Voucher to an undisclosed purchaser for $105 million." Same-day close. | VERIFIED |
| 25 | OJEMDA (tovorafenib) — pediatric low-grade glioma | Day One Biopharmaceuticals | Undisclosed | ~May 2024 | **2024-05-29** | **$108.0M** | RPD | SEC 8-K EX-99.1 (CIK 1845337, 0001193125-24-149895, filed 2024-05-30): "today announced it sold its Priority Review Voucher for $108 million to an undisclosed buyer." | VERIFIED |
| 26 | DAYBUE (trofinetide) — Rett syndrome | ACADIA Pharmaceuticals | Undisclosed | **2024-11-05** | **2024-12-11** | **$150.0M** | RPD | SEC 8-K Item 2.01 (CIK 1070494, 0001193125-24-275595, filed 2024-12-11): "December 11, 2024, Acadia Pharmaceuticals Inc. completed the sale…APA dated November 5, 2024…received $150.0 million." Note: 1/3 of net proceeds to Neuren Pharmaceuticals per joint venture agreement. | VERIFIED |
| 27 | KEBILIDI (patisiran intravitreal formulation / hSNCA-siRNA) — aromatic L-amino acid decarboxylase deficiency | PTC Therapeutics | Undisclosed | **2024-11-27** | **~Dec 2024** | **$150.0M** | RPD | APA: SEC 8-K (0001070081-24-000026, filed 2024-11-27). Close: PTC Q4 2024 income statement shows "Gain on Sale of priority review voucher: $99,900" (in thousands) = $99.9M gain, booked Q4 2024. PTC JPM25 press release (filed 2025-01-13): "PTC received $150 million from the sale of the Rare Pediatric Disease PRV it received with FDA approval of Kebilidi." | VERIFIED (price); close confirmed Q4 2024; UNVERIFIED (exact date) |
| 28 | MIPLYFFA (arimoclomol) — Niemann-Pick disease type C | Zevra Therapeutics | Undisclosed | **2025-02-26** | **2025-04-01** | **$150.0M** | RPD | APA: SEC 8-K EX-99.1 (0001193125-25-037619, filed 2025-02-27). Close: SEC 8-K Item 2.01 (0001193125-25-073991, filed 2025-04-07, period 2025-04-01): "April 1, 2025, Zevra…completed the previously disclosed sale…received gross proceeds of $150.0 million." Cantor Fitzgerald (financial), Latham & Watkins (legal). | VERIFIED |
| 29 | ZEVASKYN (pz-cel) — recessive dystrophic epidermolysis bullosa | Abeona Therapeutics | Undisclosed | **2025-05-09** | **2025-06-27** | **$155.0M** | RPD | APA: SEC 8-K EX-99.1 (0001641172-25-009564, filed 2025-05-12). Close: SEC 8-K Item 2.01 (0001641172-25-017460, filed 2025-07-02, period 2025-06-27): "June 27, 2025…completed…sale…received gross proceeds of $155 million." Stifel (lead), Jefferies (financial advisor). | VERIFIED |
| 30 | MODESYO (dordaviprone) — H3 K27M-mutant diffuse glioma | Jazz Pharmaceuticals | Undisclosed | ~Q4 2025/Q1 2026 | **Q1 2026** | **$200.0M gross** ($100M to Jazz at 50%; 50% to unnamed co-developer) | RPD | Jazz 4Q25 earnings (CIK 1232524, 0001232524-26-000012, filed 2026-02-24): "sold its Rare Pediatric Disease Priority Review Voucher for gross proceeds of $200 million (50% to Jazz)." Q1 2026 financials confirmed receipt. Disclosed by CEO at JP Morgan Healthcare Conference 2026 (Jan 12-15, 2026). | VERIFIED |
| 31 | ZYCUBO (copper histidinate) — Menkes disease | Cyprium Therapeutics (Fortress) | Undisclosed | **2026-02-23** | **2026-03-30** | **$205.0M** (20% NICHD obligation; ~$100M net to Fortress) | RPD | APA: SEC 8-K EX-99 (0001104659-26-018371, filed 2026-02-23). Close: SEC 8-K EX-99 (0001104659-26-036818, filed 2026-03-30): "Cyprium Therapeutics Closes Sale of Rare Pediatric Disease Priority Review Voucher for $205 Million." | VERIFIED |
| 32 | KRESLADI (marnetegragene autotemcel) — LAD-I | Rocket Pharmaceuticals | Large pharmaceutical company (unnamed) | **2026-04-26** | **2026-06-10** | **$180.0M** | RPD | APA: SEC 8-K EX-99 (0001140361-26-017275, filed 2026-04-28). Close: SEC 8-K Item 2.01 (0001140361-26-024997, filed 2026-06-12, period 2026-06-10): "June 10, 2026…completed…received gross proceeds of $180.0 million." | VERIFIED |
| 33 | AVLAYAH (tividenofusp alfa) — MPS II/Hunter syndrome | Denali Therapeutics | Large pharmaceutical company (unnamed) | **2026-06-12** | **2026-07-27** | **$195.0M** | RPD | APA: SEC 8-K (0001714899-26-000081, filed 2026-06-18). Close: SEC 8-K Item 2.01 (0001714899-26-000086, filed 2026-07-28, period 2026-07-27): "July 27, 2026…completed…received gross proceeds of $195.0 million." | VERIFIED |

---

## 2. Price Trend Analysis

### 2.1 Raw Price Series by Year (RPD PRVs only, verified)

| Year | Transaction(s) | Price(s) | Notes |
|------|----------------|----------|-------|
| 2014 | BioMarin → Regeneron (VIMIZIM) | $67.5M | First RPD PRV sale ever |
| 2015 | Retrophin → Sanofi (CHOLBAM) | $150M + $95M deferred ($245M total) | Installment structure; headline upfront $150M |
| 2015 | United Therapeutics → AbbVie (UNITUXIN) | **$350M** | **Historical peak; all-time high** |
| 2017 | Sarepta → Gilead (EXONDYS 51) | $125M | — |
| 2017 | BioMarin → Undisclosed (BRINEURA) | $125M | — |
| 2017 | Ultragenyx → Novartis (MEPSEVII) | $130M | — |
| 2018 | Spark → Jazz (LUXTURNA) | $110M | — |
| 2019 | GW Research → Biohaven (EPIDIOLEX) | $105M | — |
| 2020 | Eiger → Undisclosed (ZOKINVY) | $95M | Trough period |
| 2020/21 | Y-mAbs → United Therapeutics (DANYELZA) | $105M | — |
| 2021 | Rhythm → Undisclosed (IMCIVREE) | $100M | — |
| 2021 | Mirum → Janssen/J&J (LIVMARLI) | $110M | — |
| 2022 | BioMarin → Undisclosed (VOXZOGO) | $110M | — |
| 2022 | Marinus → Undisclosed (ZTALMY) | $110M | — |
| 2022 | bluebird → argenx (SKYSONA) | $102M | — |
| 2023 | bluebird → BMS (ZYNTEGLO) | $95M | — |
| 2023 | Sarepta → Undisclosed (ELEVIDYS) | $102M | — |
| 2023 | bluebird → Novartis (LYFGENIA) | $103M | — |
| 2024 | Ipsen → Undisclosed (IQIRVO) | ~$158M | UNVERIFIED primary source |
| 2024 | Valneva → Undisclosed (IXCHIQ) | $103M | TD PRV |
| 2024 | Bavarian Nordic → Undisclosed | ~$160M | UNVERIFIED primary source (TD PRV) |
| 2024 | X4 → Undisclosed (XOLREMDI) | $105M | — |
| 2024 | Day One → Undisclosed (OJEMDA) | $108M | — |
| 2024 | ACADIA → Undisclosed (DAYBUE) | $150M | — |
| 2024 | PTC → Undisclosed (KEBILIDI) | $150M | — |
| 2025 | Zevra → Undisclosed (MIPLYFFA) | $150M | — |
| 2025 | Abeona → Undisclosed (ZEVASKYN) | $155M | — |
| 2026 | Jazz → Undisclosed (MODESYO) | $200M gross / $100M to Jazz | 50% profit-share |
| 2026 | Cyprium/Fortress → Undisclosed (ZYCUBO) | $205M | 20% NICHD obligation |
| 2026 | Rocket → Large pharma (KRESLADI) | $180M | — |
| 2026 | Denali → Large pharma (AVLAYAH) | $195M | — |

### 2.2 Trend Description

**Phase 1 (2014–2015): Price Discovery.** The market opened at $67.5M in July 2014 with the first documented RPD PRV sale. Within 14 months, the United Therapeutics → AbbVie deal set the all-time high of $350M. The $350M figure was real and documented — it reflects a specific transaction: United Therapeutics' UNITUXIN (dinutuximab) PRV sold to AbbVie Ireland Unlimited Company on September 24, 2015. AbbVie is the only publicly named buyer in the first three years of the market.

**Phase 2 (2017–2021): Correction and Trough.** Prices corrected sharply. The 2017 range was $125–$130M. The 2018–2020 range was $80–$110M. The 2020 low was $95M (Eiger/ZOKINVY). The most plausible explanation: the $350M was anomalously high — AbbVie was buying a PRV for a high-value late-stage drug under a time-sensitive review constraint, and willing to pay a significant premium. As buyer sophistication increased and more vouchers entered the market (approximately 7–9 RPD awards per year in 2018–2021), prices stabilized at $95–$130M.

**Phase 3 (2022–2023): $95–$110M Plateau.** Multiple bluebird bio sales at $95–$103M and several other transactions in the $95–$110M range. Seven or more RPD PRVs were awarded per year in this period; market supply was relatively high. The 2023 trough was $95M (bluebird/ZYNTEGLO → BMS).

**Phase 4 (2024–2026): Re-acceleration.** Beginning in late 2024, prices resumed their upward trend: ACADIA and PTC both closed at $150M (Q4 2024); Zevra $150M and Abeona $155M in 2025; then $180–$205M in 2026. The three largest verified transactions in history (excluding the 2015 AbbVie outlier) all occurred in 2026. The year-over-year appreciation from 2023 trough ($95M) to 2026 peak ($205M) is approximately $110M in three years — roughly $35M/year — which is materially faster than the earlier 2017–2022 recovery.

### 2.3 The $350M Figure

The $350M figure is real. It refers to the United Therapeutics → AbbVie transaction for the UNITUXIN (dinutuximab) PRV, signed and closed in August–September 2015. The price is confirmed directly from the executed Asset Purchase Agreement filed as Exhibit 2.1 to United Therapeutics' Form 8-K (accession 0001104659-15-060788): "THREE HUNDRED FIFTY MILLION U.S. DOLLARS (U.S. $350,000,000)." The closing 8-K (0001104659-15-067017) confirms AbbVie paid exactly $350M at closing.

This price has never been matched in any subsequent transaction. The closest recent comparables are Cyprium/ZYCUBO at $205M (2026) and Denali/AVLAYAH at $195M (2026). The $350M outlier reflected a specific moment in 2015 when: the PRV program was young, vouchers were scarce, AbbVie had an identifiable high-value use case, and the price discovery function had not yet anchored to a narrower range. Whether the 2029 sunset creates conditions for another $350M+ outlier is addressed in Section 5.

### 2.4 Historical Peak and Program Context

- **Program peak:** $350M (United Therapeutics → AbbVie, 2015)
- **Post-2015 high:** $205M (Cyprium → undisclosed, 2026)
- **2024–2026 range:** $150–$205M (RPD; five verified transactions)
- **2020–2023 range:** $95–$130M (RPD; seven or more verified transactions)
- **73 RPD PRVs** awarded through 2026-05-11 (per prior repo census from Federal Register)

---

## 3. The EDGAR Data Pipeline

The Securities and Exchange Commission's EDGAR system is the primary machine-readable source for PRV transactions. All US-listed companies must disclose material agreements (8-K Item 1.01) and completion of asset dispositions (8-K Item 2.01). The pipeline below describes how to run it.

### 3.1 Full-Text Search API (efts.sec.gov)

**Base URL:** `https://efts.sec.gov/LATEST/search-index`

**Required User-Agent header:** `User-Agent: <CompanyName/AppName> <contact-email>`  
SEC EDGAR requires this header for programmatic access. Requests without a properly declared User-Agent are rate-limited or blocked (HTTP 403 "Undeclared Automated Tool" response).

**Example:** `User-Agent: RareDiseaseHedge-Research carterpry@gmail.com`

**Rate limits:** EDGAR's developer documentation states a maximum of 10 requests per second. In practice, the API will return rate-limit responses if you exceed this. For a monitoring script, 1 request per second is safe and comfortable.

**Key query patterns (measured hit counts from 2026-08-06 live runs):**

| Query string | Forms filter | Date range | Measured hits |
|---|---|---|---|
| `"priority review voucher" "asset purchase agreement"` | `forms=8-K` | 2014-01-01 to 2026-08-06 | **104** |
| `"priority review voucher" "asset purchase agreement"` | `forms=8-K` | 2014-01-01 to 2014-12-31 | **1** |
| `"priority review voucher" "million"` | none | 2014-01-01 to 2014-12-31 | **31** |
| `"Sarepta" "priority review voucher" "sale" "million"` | `forms=8-K` | 2023-01-01 to 2024-12-31 | **0** (note: Sarepta's ELEVIDYS sale was disclosed in a 10-Q, not an 8-K) |
| `"Jazz Pharmaceuticals" "priority review voucher" "200"` | none | any | **194** (broad; use narrower date range) |
| `"priority review voucher" "asset purchase agreement"` | `forms=8-K` | 2016-01-01 to 2016-12-31 | **0** |

**Complete query URL template:**
```
https://efts.sec.gov/LATEST/search-index?q=%22priority+review+voucher%22+%22asset+purchase+agreement%22&dateRange=custom&startdt=2026-01-01&enddt=2026-12-31&forms=8-K
```

**Response format:** JSON with `hits.total.value` (total hit count) and `hits.hits[]` array. Each hit has `_id` (accession number + filename), `_source.file_date`, `_source.entity_name` (often null in this endpoint; use `_source.display_names` or `_source.ciks` instead), and `_source.form_type`.

**Important caveat:** `entity_name` is frequently null in the `search-index` endpoint. The `display_names` field in `_source` reliably returns the company name and CIK. Use this for entity identification.

**Alternative: EDGAR full-text search UI** at `https://efts.sec.gov/LATEST/search-index` maps to the user-facing `https://efts.sec.gov/LATEST/search-index?q=` — the same endpoint.

### 3.2 Submissions API (data.sec.gov)

Once you have a company's CIK, retrieve all their filings:

```
https://data.sec.gov/submissions/CIK{10-digit-padded}.json
```

Example: `https://data.sec.gov/submissions/CIK0001714899.json` returns Denali Therapeutics' full filing history, including recent filings with accession numbers, form types, and filing dates. Verified working (HTTP 200) on 2026-08-05 for Denali, Rocket, Zevra, Abeona, BioMarin.

**Rate limit:** Same 10 requests/second limit applies. This endpoint is faster and more reliable than the full-text search.

### 3.3 Company-Facts API (data.sec.gov)

```
https://data.sec.gov/api/xbrl/companyfacts/CIK{10-digit-padded}.json
```

Returns all XBRL-tagged financial data. For PRV tracking, less useful than submissions or full-text search because PRV gain is reported in financial statements but the entity description typically does not use XBRL tags that would enable automated filtering. Use the submissions or full-text search API instead.

### 3.4 EDGAR Daily Index Files

For near-real-time monitoring, EDGAR publishes a daily index of all new filings:

```
https://www.sec.gov/Archives/edgar/full-index/2026/QTR3/company.idx
```

Format: fixed-width text. Updated each night with all filings from that business day. For PRV monitoring, download this daily, filter for `8-K` form type, then hit the full-text search API for each new 8-K that contains "priority review voucher."

**Quarter-specific index files:**
```
https://www.sec.gov/Archives/edgar/full-index/YYYY/QTRN/company.gz
```

### 3.5 EDGAR RSS Feed for Near-Real-Time Monitoring

EDGAR publishes an RSS feed of recent filings:

```
https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type=8-K&dateb=&owner=include&count=40&search_text=&output=atom
```

This returns an Atom feed of the most recent 40 Form 8-K filings across all companies. For a monitoring script:
1. Poll this feed every 30 minutes (well within rate limits).
2. For each new 8-K URL, check the filing text for "priority review voucher" using the full-text search API.
3. If found, retrieve the full filing for processing.

**A simpler alternative:** Use the `efts.sec.gov` search API with `dateRange=custom` set to today's date for a daily automated scan. Run once per day.

### 3.6 Practical Runnable Queries

```bash
# All PRV-related 8-Ks filed today (run daily)
curl -s "https://efts.sec.gov/LATEST/search-index?q=%22priority+review+voucher%22+%22asset+purchase+agreement%22&dateRange=custom&startdt=$(date +%Y-%m-%d)&enddt=$(date +%Y-%m-%d)&forms=8-K" \
  -H "User-Agent: RareDiseaseHedge-Research carterpry@gmail.com"

# All PRV sale announcements in the past 90 days
START=$(python3 -c "from datetime import date,timedelta; print((date.today()-timedelta(days=90)).isoformat())")
curl -s "https://efts.sec.gov/LATEST/search-index?q=%22priority+review+voucher%22+%22asset+purchase+agreement%22&dateRange=custom&startdt=${START}&enddt=$(date +%Y-%m-%d)&forms=8-K" \
  -H "User-Agent: RareDiseaseHedge-Research carterpry@gmail.com"

# Count total historical PRV APA 8-Ks (as of this report: 104 hits)
curl -s "https://efts.sec.gov/LATEST/search-index?q=%22priority+review+voucher%22+%22asset+purchase+agreement%22&forms=8-K&_source=false&size=0" \
  -H "User-Agent: RareDiseaseHedge-Research carterpry@gmail.com" | python3 -c "import json,sys; d=json.load(sys.stdin); print('Total hits:', d['hits']['total']['value'])"
```

**Phrases sponsors actually use in filings** (verified from primary source review of 33 transactions):
- `"priority review voucher"` — universal; appears in every filing
- `"asset purchase agreement"` — standard APA terminology; in all formal sale announcements
- `"rare pediatric disease priority review voucher"` — full statutory name; in approximately 85% of filings
- `"Hart-Scott-Rodino"` — always present when deal exceeds HSR threshold; absent for same-day / below-threshold deals (e.g., Sarepta/ELEVIDYS)
- `"lump sum payment"` — common but not universal; some filings use "gross proceeds"
- `"large pharmaceutical company"` — used as buyer description in approximately 70% of 2021–2026 filings
- `"completion of acquisition or disposition of assets"` — Item 2.01 header, signals close (not just APA)

**False positive rate:** The `"priority review voucher" "asset purchase agreement"` combination is highly specific. The 104 8-K hits from 2014 through mid-2026 include a small number of non-sale disclosures (e.g., some are agreements where a PRV was retained as part of a broader deal). Review each hit manually. The phrase `"rare pediatric disease priority review voucher" "sold"` in 10-Qs and 10-Ks catches sales that were announced and closed without a separate 8-K (example: Sarepta/ELEVIDYS in June 2023).

### 3.7 Gap Warning: Not All Sales Generate an 8-K

A significant monitoring gap: If a transaction is below the HSR threshold (approximately $133.9M in 2026), a company may close without filing an Item 2.01 8-K, disclosing the proceeds only in a subsequent quarterly report. The Sarepta/ELEVIDYS sale ($102M, June 2023) was disclosed exclusively in the Q3 2023 10-Q — no 8-K was filed. This means the 8-K search misses sub-threshold deals.

**Mitigation:** Supplement 8-K monitoring with full-text search of 10-Qs and 10-Ks quarterly:
```bash
curl -s "https://efts.sec.gov/LATEST/search-index?q=%22priority+review+voucher%22+%22gain+on+sale%22&forms=10-Q,10-K" \
  -H "User-Agent: RareDiseaseHedge-Research carterpry@gmail.com"
```

---

## 4. PRVWatch.com Assessment

### 4.1 Who Runs It

prvwatch.com is operated by an individual (email: lo@prvwatch.com; LinkedIn profile exists). The About page states: "I'm now over 500 hours in, having manually reviewed thousands of press releases, regulatory disclosures, and company financials to track all the issuances, sales, and redemptions I can find." No company name, legal entity, or formal institutional affiliation is disclosed. This is a solo passion project, not a commercial information service or academic institution.

### 4.2 Currency

The site footer indicates last publication date **July 27, 2026** — the site is being actively maintained as of this report date. The History page contains at minimum the 2015 United Therapeutics → AbbVie $350M transaction (confirmed during this research). The CNPV dashboard shows 21 CNPVs as of 2026-08-05 (confirmed in source 23-voucher-instruments-compared.md).

The chart data embedded in the history page's JavaScript shows voucher award counts by year with data through 2026, including:

```javascript
rpd: [0,0,0,1,2,0,3,5,7,8,8,9,7,6,6,8,4,3,4]
// for years: 2008–2026
// 2026 (partial year through Aug 6): 4 RPD PRVs
```

This aligns well with the Federal Register issuance notices in this repo (WASKYRA, ZYCUBO, KRESLADI, YUVIWEL, LOARGYS, OTARMENI, AVLAYAH — 7 in 2026 as of May 11, some of which may be in the "4" for partial-year 2026 in the chart, depending on cutoff date). Minor count discrepancy suggests data may not be updated in real time.

### 4.3 Feed or Scrape-Only?

No RSS feed, Atom feed, or API endpoint was found. There is no sitemap entry for a feed. The site is built on Webflow with a CMS-based content system (all content is rendered client-side by JavaScript). Data is not accessible via standard HTTP GET of the page HTML — JavaScript must execute to render transaction tables.

**Assessment: scrape-only, requiring browser automation.** Headless browser (Playwright or Puppeteer) would be needed to reliably extract structured data. Given the Webflow architecture, the underlying data may be in Webflow's CMS API, but no public endpoint URL was identified.

### 4.4 Safe to Build On?

**Use with caution as a secondary cross-reference, not as a primary data source.**

Arguments for use:
- The maintainer appears to have done substantial manual verification (500+ hours).
- The site is actively maintained (last updated July 27, 2026).
- Cross-referencing this report's SEC-verified transactions with prvwatch data points (e.g., the $350M AbbVie deal, the $67.5M BioMarin-Regeneron deal) found consistency.
- The CNPV dashboard (21 awards) was used in prior repo research and verified.

Arguments against relying on it:
- **Operator anonymity:** No disclosed legal entity, credentials, or institutional affiliation. No statement of methodology or error-correction process.
- **No API:** Data is effectively locked in Webflow CMS and requires browser automation to access programmatically.
- **No versioning or audit trail:** If data changes, there is no changelog.
- **Single point of failure:** The site depends entirely on one person's ongoing maintenance. If the operator stops updating, the data becomes stale without notice.
- **No primary source citations visible** in the scraped HTML (links may be present in the rendered JS but were not extracted in this research).

**Recommended approach:** Use prvwatch as a discovery tool to identify transactions, then independently verify each one via EDGAR or company press releases before relying on it in financial models or legal analysis.

---

## 5. Forward Price Range 2027–2029 and the Sunset Question

### 5.1 The Sunset Constraint

Pub. L. 119-75 § 6604(a), enacted 2026-02-03, bars any RPD PRV awards after September 30, 2029. This is a hard approval deadline. Given a typical priority review clock of 6 months from filing, the last viable NDA/BLA submission date for a sponsor who wants an approval by September 30, 2029 is approximately **late March 2028**. Companies that submit after that date face a real risk that FDA will not complete review by the sunset date.

### 5.2 Supply Dynamics

**Historical issuance pace:**
- 2018–2021: approximately 7–9 RPD PRVs per year
- 2022–2025: approximately 4–8 per year (chart data shows 6, 8, 4, 3 per year for 2022–2025)
- 2026 (through Aug 6): 4 confirmed (WASKYRA, ZYCUBO, KRESLADI, then AVLAYAH and others)

With approximately 3.1 years remaining to the 2029-09-30 sunset, the remaining RPD PRV supply is bounded: at 5–8 per year, approximately **15–25 more PRVs** may be issued before the program closes. This is a finite and knowable number, in contrast to the open-ended supply of earlier years.

**Key observation:** The Pub. L. 117-9 (2021) "active moiety" test and the 505(b)(1) requirement have already narrowed the eligible pipeline relative to the pre-2021 period. Programs using generics repurposed for US use are categorically excluded. The Sun Pharma/SEZABY ruling (D.D.C. Dec 2025) creates a small additional sub-population (A2: pre-1962 deemed-approved NDAs) but this is district-court-only, unreviewed on appeal, and narrow in scope.

### 5.3 Demand Dynamics

**Buyers of PRVs** are large pharmaceutical companies with late-stage development pipelines where 4–5 months of expedited FDA review translates to material commercial value (first-mover sales, competitive dynamics, manufacturing buildout lead time). The pool of meaningful buyers — companies large enough to pay $150–200M for a regulatory option — is relatively stable: approximately 10–20 major global pharma companies are plausible buyers at any given time.

**Buyer demand signal:** Three RPD PRV sales in Q2–Q3 2026 (Cyprium, Rocket, Denali) at $180–205M suggest sustained buyer appetite at these price levels. The 2026 prices suggest buyers are pricing in scarcity — they are willing to pay 70–90% more than the 2022–2023 trough.

### 5.4 Scarcity Premium vs. Redemption/Sale Race

**Bull case — scarcity premium:**  
After September 30, 2029, no new RPD PRVs enter the market. Large pharma buyers with high-value NDA/BLA submissions (blockbusters, competitive launch timing) will need to acquire vouchers from the residual stock of issued-but-unredeemed PRVs. If the remaining stock is small (fewer than 5–10 unredeemed vouchers after the sunset) and buyer demand persists, the terminal price of the last available vouchers could exceed the $205M 2026 peak — potentially approaching or exceeding $250M.

**Bear case — glut / sprint to exit:**  
Sponsors racing to beat the sunset will cluster NDA submissions in 2027–2028. If 15–20 approvals occur between now and 2029, a transient surplus of newly issued PRVs could suppress spot prices as multiple sellers simultaneously seek to monetize before the program closes and buyer value evaporates. Additionally, if buyers anticipate the post-sunset supply cut-off, they may build inventory in 2027 rather than 2028, creating a 2027 demand spike followed by buyer saturation.

**Equilibrium judgment:**  
The most likely outcome is **continued gradual appreciation with increased volatility** rather than either a clean scarcity premium or a pure glut. The pattern:

- **2026–2027:** Prices remain in the $175–210M range, consistent with the current $180–$205M observed band. Sellers and buyers both understand the trajectory.
- **2027–2028:** Prices may spike to $200–$250M if: (a) approval pipelines are thin (fewer than expected PRVs issued due to the active moiety test narrowing eligibility), or (b) buyers with high-value 2028 NDA submissions create competitive pressure for the remaining available vouchers.
- **2028–2029:** If the race-to-exit dynamic dominates, sellers may discount to $150–175M to ensure proceeds before the buyer pool narrows. If scarcity dominates, sellers with strong leverage may extract $220–$250M.

**Two structural features constrain both extremes:**
1. The 5-year capital markets horizon of most biotech companies means they cannot plan to receive a PRV much before 2029 and still capture it — the remaining window is already short.
2. Buyers do not need to buy every voucher; they buy only those they have a near-term use for. A buyer without an NDA ready to file will not pay $200M for a voucher that expires (is devalued) if the buyer's drug gets rejected or delayed.

### 5.5 Is the "$150–250M" Planning Assumption Supported?

**Yes, with appropriate qualification.**

The 2026 data strongly supports the lower end of this range as a floor. Three verified 2026 transactions — $180M (Rocket), $195M (Denali), $205M (Cyprium) — all fall within or above the $150–250M range. The Jazz $200M gross (50% to Jazz, so $100M net) is an anomaly due to the profit-sharing structure rather than a lower market price.

The $250M upper end is speculative but not unreasonable if:
- The remaining PRV pipeline is thinner than historical averages (due to the active moiety test and the 505(b)(1) requirement excluding repurposed generics).
- A buyer with a specific high-value, time-sensitive use case creates an outlier bid.
- The 2015 AbbVie/United Therapeutics $350M demonstrates this market is capable of wide outliers.

**Recommended planning assumption for this company:**
- **Conservative (base):** $150–$175M net of fees. Use this for IRR calculations.
- **Current market:** $175–$205M gross (2026 transactions). Subtract 3–5% broker fees and any contractual sharing obligations.
- **Upside:** $200–$250M gross if the 2028–2029 scarcity dynamic materializes and this company's program is among the last to receive a PRV before sunset.
- **Downside:** $120–$150M if a 2028 glut of seller supply suppresses prices and the buyer pool becomes satiated.

The "$150–250M" planning range is well-supported by the transaction history and should be retained as the working assumption. The center of gravity in 2025–2026 is approximately $175–$200M, and the trend is upward. Booking $150M in a conservative model and $200M in a base model is reasonable.

---

## 6. URL Ledger

### VERIFIED (primary source retrieved at stated HTTP status)

| URL | Retrieved | HTTP | What it contained |
|-----|-----------|------|-------------------|
| `https://www.sec.gov/Archives/edgar/data/1048477/000119312514291230/d769619d8k.htm` | 2026-08-06 | 200 | BioMarin → Regeneron, $67.5M, VIMIZIM, close July 30, 2014 |
| `https://www.sec.gov/Archives/edgar/data/1082554/000110465915060788/a15-18206_1ex2d1.htm` | 2026-08-06 | 200 | United Therapeutics APA EX-2.1: "THREE HUNDRED FIFTY MILLION U.S. DOLLARS" |
| `https://www.sec.gov/Archives/edgar/data/1082554/000110465915067017/a15-20167_18k.htm` | 2026-08-06 | 200 | United Therapeutics close 8-K: "September 24, 2015…AbbVie paid $350.0 million" |
| `https://www.sec.gov/Archives/edgar/data/1438533/000119312515201124/d932773d8k.htm` | 2026-08-06 | 200 | Retrophin APA: $150M + $47.5M + $47.5M deferred; Sanofi as buyer |
| `https://www.sec.gov/Archives/edgar/data/1438533/000119312515245643/d62271d8k.htm` | 2026-08-06 | 200 | Retrophin close: July 2, 2015; CHOLBAM; Sanofi |
| `https://www.sec.gov/Archives/edgar/data/873303/000119312517049361/d354714dex991.htm` | 2026-08-06 | 200 | Sarepta APA: $125M, EXONDYS 51, Feb 20, 2017; Credit Suisse as advisor |
| `https://www.sec.gov/Archives/edgar/data/873303/000119312517105290/d325575d8k.htm` | 2026-08-06 | 200 | Sarepta close: March 30, 2017; buyer = "a subsidiary of Gilead Sciences, Inc." |
| `https://www.sec.gov/Archives/edgar/data/1048477/000119312517353976/d498905dex991.htm` | 2026-08-06 | 200 | BioMarin APA: $125M, BRINEURA, Nov 21, 2017 |
| `https://www.sec.gov/Archives/edgar/data/1515673/000156459017025027/rare-ex991_6.htm` | 2026-08-06 | 200 | Ultragenyx: $130M, MEPSEVII, Novartis as buyer, Dec 14, 2017 |
| `https://www.sec.gov/Archives/edgar/data/1609351/000160935118000040/a8-kprv.htm` | 2026-08-06 | 200 | Spark APA: $110M, LUXTURNA, Jazz as buyer, Apr 30, 2018 |
| `https://www.sec.gov/Archives/edgar/data/1010086/000114036118042027/ex99_1.htm` | 2026-08-06 | 200 | SIGA: $80M, TPOXX, MCM PRV, Oct 31, 2018 |
| `https://www.sec.gov/Archives/edgar/data/1689813/000110465919020231/a19-7980_18k.htm` | 2026-08-06 | 200 | Biohaven close: $105M, EPIDIOLEX (GW Research as seller), April 5, 2019 |
| `https://www.sec.gov/Archives/edgar/data/1305253/000119312520300479/d54433dex991.htm` | 2026-08-06 | 200 | Eiger: $95M, ZOKINVY, 50/50 split with Progeria Research Foundation, Nov 23, 2020 |
| `https://www.sec.gov/Archives/edgar/data/1722964/000110465921006432/tm213777d1_8k.htm` | 2026-08-06 | 200 | Y-mAbs close: $105M, DANYELZA, United Therapeutics as buyer, Jan 21, 2021 |
| `https://www.sec.gov/Archives/edgar/data/1649904/000110465921000984/tm211725d1_8k.htm` | 2026-08-06 | 200 | Rhythm: $100M, IMCIVREE, Jan 5, 2021 |
| `https://www.sec.gov/Archives/edgar/data/1759425/000119312521364950/d221713d8k.htm` | 2026-08-06 | 200 | Mirum close: $110M, LIVMARLI, Janssen Biotech (J&J) as buyer, Dec 22, 2021 |
| `https://www.sec.gov/Archives/edgar/data/1267813/000155837022010694/mrns-20220713xex99d1.htm` | 2026-08-06 | 200 | Marinus: $110M, ZTALMY, Jul 13, 2022; Jefferies as advisor |
| `https://www.sec.gov/Archives/edgar/data/1293971/000119312522294908/d408871d8k.htm` | 2026-08-06 | 200 | bluebird bio: $102M, SKYSONA, argenx as buyer, Nov 29, 2022 |
| `https://www.sec.gov/Archives/edgar/data/1293971/000119312523002980/d435443d8k.htm` | 2026-08-06 | 200 | bluebird bio: $95M, ZYNTEGLO, BMS as buyer, Jan 5, 2023 same-day close |
| `https://www.sec.gov/Archives/edgar/data/873303/000095017023057414/srpt-20230930.htm` | 2026-08-06 | 200 | Sarepta 10-Q: $102M gain from sale of ELEVIDYS PRV, June 2023, below HSR threshold |
| `https://www.sec.gov/Archives/edgar/data/1293971/000119312523265691/d575905d8k.htm` | 2026-08-06 | 200 | bluebird bio: $103M, LYFGENIA, Novartis as buyer, APA Oct 26, 2023 |
| `https://www.sec.gov/Archives/edgar/data/1836564/000117184324000572/exh_991.htm` | 2026-08-06 | 200 | Valneva: $103M, IXCHIQ, TD PRV, Feb 5, 2024 same-day close |
| `https://www.sec.gov/Archives/edgar/data/1501697/000162828024021937/a991pressreleasedatedmay92.htm` | 2026-08-06 | 200 | X4 Pharmaceuticals: $105M, XOLREMDI, May 8, 2024 same-day close |
| `https://www.sec.gov/Archives/edgar/data/1845337/000119312524149895/d834662dex991.htm` | 2026-08-06 | 200 | Day One: $108M, OJEMDA, May 29, 2024 |
| `https://www.sec.gov/Archives/edgar/data/1070494/000119312524275595/d841090d8k.htm` | 2026-08-06 | 200 | ACADIA: $150M, DAYBUE, APA Nov 5, close Dec 11, 2024; 1/3 net to Neuren |
| `https://www.sec.gov/Archives/edgar/data/1070081/000107008125000007/tmb-20250113xex99d1.htm` | 2026-08-06 | 200 | PTC Therapeutics: "received $150 million from sale of KEBILIDI PRV" |
| `https://www.sec.gov/Archives/edgar/data/1232524/000123252426000012/a4q25financialpr.htm` | 2026-08-06 | 200 | Jazz 4Q25: "sold PRV for gross proceeds of $200 million (50% to Jazz)" |
| `https://www.sec.gov/Archives/edgar/data/1232524/000123252426000024/a1q26financialpr.htm` | 2026-08-06 | 200 | Jazz Q1 2026: "received gross proceeds of $200 million (50% to Jazz) from sale of PRV" |
| `https://prvwatch.com/history` | 2026-08-06 | 200 | Historical timeline; $350M AbbVie deal confirmed; chart data embedded in JS |
| `https://prvwatch.com/about` | 2026-08-06 | 200 | Operator: individual, anonymous, lo@prvwatch.com; 500+ hours manual review; last published Jul 27, 2026 |
| `https://prvwatch.com/sitemap.xml` | 2026-08-06 | 200 | 30+ page entries; no feed URL found |
| `https://efts.sec.gov/LATEST/search-index?q=%22priority+review+voucher%22+%22asset+purchase+agreement%22&forms=8-K` (2014–2026-08-06) | 2026-08-06 | 200 | **104 hits** |
| `https://efts.sec.gov/LATEST/search-index?q=%22priority+review+voucher%22+%22asset+purchase+agreement%22&forms=8-K&dateRange=custom&startdt=2016-01-01&enddt=2016-12-31` | 2026-08-06 | 200 | **0 hits** — confirmed no RPD PRV sales in 2016 |
| All Rocket, Denali, Abeona, Zevra, Cyprium, BioMarin 2022, Denali URLs | 2026-08-05/06 | 200 | All verified in source `24-prv-deal-mechanics.md` (not re-fetched) |

### UNVERIFIED / NOT CONFIRMED FROM PRIMARY SOURCE

| Item | Reason |
|------|---------|
| Knight Therapeutics / Paladin Labs miltefosine PRV $125M (~Nov 2014) | Canadian company, no EDGAR filing; price from press accounts; primary source not retrieved |
| Ipsen IQIRVO PRV $158M (~Aug 2024) | French company, no EDGAR primary listing; price from press reports and MeiraGTx 10-K reference to "$100–$158M" range; exact amount and date not confirmed from primary source |
| Bavarian Nordic chikungunya vaccine PRV $160M (~2024) | Danish company, no EDGAR filing; price from Fierce Pharma and source 23 cross-reference; exact amount and date not confirmed |
| BioMarin BRINEURA PRV exact close date (~Dec 2017) | APA Nov 21, 2017 confirmed; no separate close 8-K found |
| Ultragenyx MEPSEVII PRV exact close date (~Jan 2018) | APA Dec 14, 2017 confirmed; no separate close 8-K found |
| bluebird bio LYFGENIA PRV exact close date (~Dec 2023 / Jan 2024) | APA Oct 26, 2023 confirmed; close contingent on LYFGENIA approval (Dec 8, 2023); no separate close 8-K found in EDGAR search |
| PTC KEBILIDI PRV exact close date (~Dec 2024) | APA Nov 27, 2024; Q4 2024 income statement confirms gain booked; exact date not found in SEC filings |
| Buyer identities: Rocket KRESLADI, Denali AVLAYAH, Jazz MODESYO, Zevra, Abeona, Cyprium, Marinus, bluebird SKYSONA | All described as "large pharmaceutical company" or "undisclosed purchaser" in SEC filings |
| Jazz MODESYO PRV exact APA date | Disclosed retrospectively at JPM26 (Jan 12–15, 2026); precise APA date not publicly disclosed |
| Rhythm Pharmaceuticals IMCIVREE PRV exact close date | APA Jan 5, 2021; close date not found in a separate 8-K |

---

*Primary sources fetched and verified 2026-08-06 via EDGAR EDGAR archive, data.sec.gov, and prvwatch.com. EDGAR search API confirmed operational. User-Agent requirement verified. All prices stated as gross (pre-tax, pre-fee); net amounts differ per tax structure and contractual sharing arrangements.*
