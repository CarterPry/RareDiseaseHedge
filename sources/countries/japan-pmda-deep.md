<!-- RECOVERED from agent-a5ee041e6c67215aa.jsonl on 2026-08-06 after the original agent died on an
     API connection error (ConnectionRefused) following 69 tool calls of live primary-source research.
     All "VERIFIED" findings below were confirmed by the original agent's fetches on 2026-08-05;
     findings marked "newly verified 2026-08-06" were confirmed by a recovery pass on 2026-08-06. -->

# Japan PMDA — Deep Dive: Approved-Drug Enumeration for Rare-Disease Repurposing

**Why Japan is the primary PRV-eligible funnel.** Under 21 U.S.C. 360ff(a)(4)(B)(i) as interpreted post-Pub. L. 117-9 (2021), the only candidates that can earn a Priority Review Voucher are those containing an active moiety **never previously approved** in the US under 505(b)(1)/(b)(2)/(j), filed as a full 505(b)(1) NDA. Japan approves hundreds of drugs, including many traditional JAN (Japanese Accepted Name) compounds and novel biologics, that have never entered US regulatory review. It is therefore the single richest source of Funnel A (PRV-eligible) candidates. This document is a technical reference for enumerating those candidates in machine-readable form.

**Prior coverage.** The survey-level PMDA section in `06-reference-regulators.md` (recovered from agent-aa5d9490a029a8c09.jsonl) covers the overview and the join recipe against the FDA and EMA. This document does not repeat that content; it goes deeper on each source, adds measured record counts, and documents the NHI Yakka as the completeness anchor.

---

## 1. PMDA Approved-Products Sources

### 1a. English "List of Approved Drugs" PDF

| Field | Value |
|---|---|
| URL | `https://www.pmda.go.jp/english/review-services/reviews/approved-information/drugs/0002.html` |
| Status | **VERIFIED** HTTP 200, 52,895 bytes (2026-08-05; re-confirmed 2026-08-06) |
| Current PDF | `https://www.pmda.go.jp/files/000281190.pdf` |
| PDF size | 3,206,009 bytes, 207 pages |
| Coverage | April 2004 → February 2026 (as of last update) |
| Language | English throughout |
| Auth | None |
| Update cadence | Roughly monthly; file path rotates on each update |

**Columns:** Review Category | Approval Date | No. | Brand Name (Applicant Company) | New Approval / Partial Change | Active Ingredient (underlined = new active ingredient) | Notes

**Designation tags in the Notes column (measured across the full extracted text by the agent):**

| Tag | Count |
|---|---|
| `[Orphan drug]` | 457 |
| `[Orphan Drug]` (case variant) | 18 |
| `[Priority review]` | 106 |
| `[Priority Review]` (case variant) | 7 |
| `[Expedited review]` | 72 |
| `[Public knowledge-based application]` | 27 |
| `[SAKIGAKE designation]` | 5 |
| `[Notification of off-label use]` | 13 |

Normalise case before counting; the two `[Orphan drug]`/`[Orphan Drug]` variants are the same designation.

**Critical operational gotchas:**

1. **The file ID rotates on every update.** Historical path progression confirmed: `/files/000248626.pdf` (Feb 2023) → `/files/000250463.pdf` (Mar 2023) → `/files/000281190.pdf` (current). Never hardcode the numeric ID. On each pipeline run, fetch `0002.html` and scrape the PDF link dynamically.

2. **Multi-line table cell extraction.** This PDF uses multi-line wrapped table cells. Naive `pdfplumber` `extract_text()` merges adjacent approval rows. Use table-extraction mode with explicit column boundaries (`pdfplumber` `extract_tables()` or `camelot`).

3. **Coverage gap.** The PDF covers FY2004 onward. Pre-2004 approvals are not in this file. For historical depth use the MHLW printed supplements (not machine-readable) or the NHI Yakka (§3 below), which carries the full historical marketed universe.

---

### 1b. Per-Fiscal-Year Approval XLSX (Japanese-language primary source)

| Field | Value |
|---|---|
| Index URL | `https://www.pmda.go.jp/review-services/drug-reviews/review-information/p-drugs/0010.html` |
| Index status | **VERIFIED** HTTP 200, 126,752 bytes (2026-08-05) |
| Coverage | FY2004 → FY2026 (current fiscal year) |
| Language | Japanese |

Per-fiscal-year detail pages have **non-sequential** IDs; do not compute them. Verified mapping (from agent inspection of the index page):

| Fiscal Year | Page |
|---|---|
| FY2025 | `0039.html` |
| FY2024 | `0037.html` |
| FY2023 | `0036.html` |
| FY2016 | `0026.html` |
| FY2011 | `0001.html` |

Scrape `0010.html` to get the full current mapping. Each FY page carries both a PDF and an XLSX.

**Verified FY2025 XLSX download:**

- URL: `https://www.pmda.go.jp/files/000277966.xlsx` — **VERIFIED** HTTP 200, correct XLSX MIME, 32,825 bytes
- Sheet: `2025年度承認品目`
- Dimensions: 143 rows × 7 columns (3 header rows + 140 data rows)

**Columns (verified by agent inspection):**

| Col | Japanese | English |
|---|---|---|
| 0 | 分野 | Review category (第１＝pharmaceuticals, etc.) |
| 1 | 承認日 | Approval date (format `YYYY.M.D`) |
| 2 | No. | Serial number |
| 3 | 販売名（会社名、法人番号） | Brand name (company, corporate number) |
| 4 | 承認 | Approval type |
| 5 | 成分名（下線:新有効成分） | Active ingredient (underlined = new) |
| 6 | 効能・効果等 | Indication |

**Approval type values (col 4):** The field uses full-width space (U+3000) between 承 and 認. Values verified:
- `承　認` = new approval (new drug or new indication)
- `一　変` = partial change (e.g., new formulation, dose, or route for existing product)
- Mixed strings exist: a single row can have multiple products with different approval types concatenated by newline

**FY2025 counts (verified by agent):**
- Total data rows: 140
- Rows with `承認` (new approval): 70
- Rows tagged orphan (`【希少疾病用医薬品】` in col 6): 45
- Rows that are BOTH orphan-tagged AND new-approval: **29**

**Orphan new approvals FY2025 (complete enumeration from agent, verified):**

| Date | Active Ingredient (JAN) | Brand Name | Indication |
|---|---|---|---|
| 2025-05-19 | ベランタマブ マホドチン | ブーレンレップ点滴静注 | Relapsed/refractory multiple myeloma |
| 2025-06-24 | シパグルコシダーゼ アルファ | ポムビリティ点滴静注 | Late-onset Pompe disease (combo w/ miglustat) |
| 2025-06-24 | ミグルスタット | オプフォルダカプセル | Late-onset Pompe disease (combo w/ cipaglucosidase) |
| 2025-06-24 | ソタテルセプト | エアウィン皮下注 | Pulmonary arterial hypertension |
| 2025-06-24 | ジアゼパム | スピジア点鼻液 | Status epilepticus (new route) |
| 2025-06-24 | ベルズチファン | ウェリレグ錠 | Renal cell carcinoma |
| 2025-06-24 | フェドラチニブ塩酸塩水和物 | インレビックカプセル | Myelofibrosis |
| 2025-06-24 | トアルクエタマブ | タービー皮下注 | Relapsed/refractory multiple myeloma |
| 2025-08-25 | パロペグテリパラチド | ヨビパス皮下注 | Hypoparathyroidism |
| 2025-09-19 | オデビキシバット水和物 | ビルベイ顆粒 | PFIC (progressive familial intrahepatic cholestasis) pruritus |
| 2025-09-19 | ケノデオキシコール酸 | フジケノン粒状錠 | Cerebrotendinous xanthomatosis (new indication) |
| 2025-09-19 | ニポカリマブ | アイマービー点滴静注 | Generalized myasthenia gravis |
| 2025-09-19 | セルメチニブ硫酸塩 | コセルゴ顆粒 | Neurofibromatosis type 1 (new dose/form) |
| 2025-09-19 | ヌシネルセンナトリウム | スピンラザ髄注 | Spinal muscular atrophy (new dose) |
| 2025-09-19 | ボラシデニブ | ボラニゴ錠 | IDH1/IDH2-mutant glioma |
| 2025-09-19 | ゾンゲルチニブ | ヘルネクシオス錠 | HER2-mutant NSCLC |
| 2025-09-19 | タレトレクチニブ | イブトロジーカプセル | ROS1-positive NSCLC |
| 2025-12-22 | セピアプテリン | セピエンス顆粒 | Phenylketonuria |
| 2025-12-22 | フェニル酪酸グリセロール | ラヴィクティ内用液 | Urea cycle disorders |
| 2025-12-22 | セベトラルスタット | エクテリー錠 | Hereditary angioedema (acute attacks) |
| 2025-12-22 | マシテンタン (小児) | オプスミット小児用分散錠 | Pulmonary arterial hypertension (pediatric dose) |
| 2025-12-22 | レチファンリマブ | ジニイズ点滴静注 | Squamous cell carcinoma of anal canal |
| 2025-12-22 | タグラキソフスプ | エルゾンリス点滴静注 | Blastic plasmacytoid dendritic cell neoplasm |
| 2025-12-22 | タファシタマブ | ミンジュビ点滴静注 | Relapsed/refractory follicular lymphoma |
| 2026-02-19 | パロバロテン | ソホノスカプセル | Fibrodysplasia ossificans progressiva |
| 2026-03-06 | ドラビリン／イスラトラビル水和物 | イドビンソ配合錠 | HIV-1 infection |
| 2026-03-23 | オデビキシバット水和物 | ビルベイ顆粒 | (second listing) |
| 2026-03-23 | レニオリシブリン酸塩 | ジョエンジャ錠 | Activated PI3K-delta syndrome |
| 2026-03-23 | トリヘプタノイン | ドジョルビ内用液 | Long-chain fatty acid oxidation disorders |
| 2026-03-23 | リソバリシブメシル酸塩水和物 | ハイツエキシン錠 | PIK3CA-mutant ovarian clear cell carcinoma |

**Note for Funnel A screening:** Several of these (sepiapterin, triheptanoin, parobarotene, léniolisib, odevixibat, sevtralstat) are approved or in late development in the US or EU — cross-check against FDA Drugs@FDA and EMA before treating as Japan-only. The join methodology is in `06-reference-regulators.md` §1f.

**Why this XLSX is the preferred machine-readable source:**
- The 法人番号 (corporate registration number) embedded in the brand-name cell is a clean join key to Japanese company records
- Orphan designation is machine-parseable from the indication cell (`【希少疾病用医薬品】`)
- The approval type (`承認` vs `一変`) is structured and parseable once the full-width-space is handled
- Dimensions are small enough to hold in memory (140 rows/FY), allowing per-FY download and concat

---

### 1c. English Review Reports (Shinsa Hokokusho)

| Field | Value |
|---|---|
| URL | `https://www.pmda.go.jp/english/review-services/reviews/approved-information/drugs/0001.html` |
| Status | **VERIFIED** HTTP 200, 267,105 bytes (prior agent; same parent domain confirmed 2026-08-06) |
| Structure | One static HTML page (not a search interface) |
| Total table rows | 476 |
| PDF links | 954 total (448 English, 423 Japanese) |
| Coverage | 2007–2025 |

This page is a complete A–Z table, obtained in a single GET. It is not paginated. Columns: Brand Name | Non-proprietary Name | Approved In | Review Report (EN) | Review Report (JP).

**URL patterns:**
- English PDF: `https://www.pmda.go.jp/files/000273006.pdf` (example: Acenobel/aceneuramic acid, GNE myopathy)
- Japanese PDF: `https://www.pmda.go.jp/drugs/2024/P20240527004/620095000_30600AMX00133_A100_1.pdf` — the segment `30600AMX00133` is the Japanese marketing approval number (承認番号), a useful join key

**Selection bias:** Only ~448 of the thousands of Japanese approvals receive English translation. Selection is biased toward new active ingredients and priority designations — which happens to suit rare-disease screening well, but is **not** a complete list of Japan-approved drugs.

---

## 2. KEGG DRUG Database

### 2a. REST API and data inventory

| Field | Value |
|---|---|
| Info endpoint | `https://rest.kegg.jp/info/drug` |
| Status | **VERIFIED** HTTP 200 (2026-08-05, re-confirmed 2026-08-06) |
| Total entries | 12,891 (as of 2026-08-05 per API response: `dr  12,891 entries  Last update 2026/08/05`) |
| List endpoint | `https://rest.kegg.jp/list/drug` |
| List status | **VERIFIED** HTTP 200, Content-Type `text/plain; charset=utf-8` |

**Downloaded file stats (verified by agent, files downloaded 2026-08-05):**
- `kegg_drug.txt`: 12,893 lines × ~45 bytes avg = 586 KB. Last entry: D13366 `Palacaparib (USAN/INN)`. The 2-line discrepancy vs the API count reflects a blank terminal line.
- `brite.txt` (KEGG BRITE `br:br08303`): 14,214 lines, 450 KB — hierarchical drug classification with DGroup nodes
- `kegg_d00564.txt` (warfarin sodium, single-entry detail): 203 lines, 8.2 KB — shows full ENTRY/NAME/PRODUCT/REACTION/ENZYME/DBLINKS/ATOM/BOND structure

**Japan-approval markers in `kegg_drug.txt` (measured by agent):**

| Tag | Count |
|---|---|
| `JAN` (Japanese Accepted Name) | 2,267 entries |
| `JP18` or `JP19` (Japanese Pharmacopoeia) | 1,404 combined |
| Entries returned by `rest.kegg.jp/find/drug/JAN` | 2,273 (newly verified 2026-08-06) |
| Entries returned by `rest.kegg.jp/find/drug/JP18` | 1 (newly verified 2026-08-06) |

The `JAN` tag is the reliable Japan-approval marker. The JP pharmacopoeia tags cover classical/excipient compounds. The `find/drug/JAN` endpoint returns 2,273 lines (newly verified 2026-08-06 at that count), each formatted `D{5-digit}\t{name string}`.

**Linked databases in KEGG DRUG (from `info/drug` response):**
- `yk` — Yakult drug database
- `jtc` — Japan therapeutic codes
- `ndc` — US NDC codes
- `atc` — WHO ATC codes
- `pubchem`, `chebi` — cross-references

The `yk` and `jtc` databases are linked but the `rest.kegg.jp/info/yk` and `info/jtc` endpoints returned no output (agent verified: `Bash completed with no output`). These may require subscription access.

### 2b. KEGG BRITE structure

The downloaded `brite.txt` is a hierarchical classification. Lines are prefixed A/B/C/D/E/F for hierarchy depth. Example (first few lines verified):
```
+F  DGroup
!
AAntibacterial
B  DG01710  beta-Lactam antibiotic
C    DG01713  Penicillin skeleton group
D      DG01480  Penicillin
E        DG00517  Ampicillin
F          D00204  Ampicillin
```
Leaf nodes (F-level) carry the D-code (KEGG DRUG ID). This allows traversal from therapeutic class → individual compounds.

### 2c. KEGG licence terms — COMMERCIAL USE REQUIRES A PAID LICENCE

From `https://www.kegg.jp/kegg/legal.html` — **VERIFIED** 2026-08-05, re-confirmed same language 2026-08-06:

> **"Academic users may freely use the KEGG website... Academic users who utilize KEGG for providing services are requested to obtain an academic service provider license, which is included in the KEGG FTP academic subscription."**
>
> **"Non-academic users must understand that KEGG is not a public database, nor is it a publicly funded database. Non-academic use of KEGG requires a commercial license. Please contact Pathway Solutions, which operates KEGG FTP sites and a KEGG mirror website, for license agreements."**

**Implication for this project:** This is a commercial drug repurposing company. Using KEGG DRUG for commercial screening without a licence agreement violates KEGG's terms. The REST API at `rest.kegg.jp` is accessible without auth, but commercial scraping of it would still fall under non-academic use. **Before building any pipeline on KEGG DRUG data, obtain a commercial licence from Pathway Solutions (`https://www.pathway.jp`).** The NHI Yakka (§3) and the PMDA XLSX files (§1b) are government open data and do not carry this restriction.

### 2d. Broad Institute Drug Repurposing Hub (co-located file)

The agent also inspected `broad_drug.txt` and `broad_sample.txt` from the prior session's scratchpad. These are the Broad Institute Drug Repurposing Hub files:
- `broad_drug.txt`: 7,550 lines, 646 KB. Header: `pert_iname | clinical_phase | moa | target | disease_area | indication`. File date: 2025-08-18.
- Licence stated in file: **"provided for non-commercial use only"** and cites Corsello et al., Nature Medicine 2017.
- Same commercial-use restriction as KEGG. This file is a useful cross-reference for MoA but cannot be used in a commercial product without a licence agreement.

---

## 3. NHI Drug Price List (薬価基準収載医薬品リスト, Yakka) — The Completeness Anchor

This is the most important finding for the question of whether a **complete machine-readable list of all currently approved prescription drugs in Japan** exists. The answer is: **yes, via the NHI price list, which is updated monthly and covers virtually every marketed drug.**

### 3a. Source and download

| Field | Value |
|---|---|
| Parent page | `https://www.mhlw.go.jp/topics/2026/04/tp20260401-01.html` |
| Status | **VERIFIED** HTTP 200, Last-Modified: 2026-07-31 (2026-08-05; re-confirmed 2026-08-06) |

The MHLW Yakka page for the April 2026 revision carries multiple Excel files, updated monthly as new drugs are listed mid-revision-period. Confirmed links as of 2026-07-31 page update:

| File | URL | Size | Category | Content |
|---|---|---|---|---|
| Aug 1 effective (_01) | `/topics/2026/04/xls/tp20260801-01_01.xlsx` | **VERIFIED** HTTP 200, 669,088 bytes | 内用薬 (oral) | 7,054 products |
| Aug 1 effective (_02) | `/topics/2026/04/xls/tp20260801-01_02.xlsx` | **VERIFIED** HTTP 200 | 注射薬 (injectable) | 3,473 products |
| Jul 15 combined (_05) | `/topics/2026/04/xls/tp20260715-01_05.xlsx` | **VERIFIED** HTTP 200, 683,699 bytes | All categories combined | 12,414 products |
| Apr 1 effective (_04) | `/topics/2026/04/xls/tp20260401-01_04.xlsx` | **VERIFIED** HTTP 200, 24 KB | (small supplement) | — |

Additional _05 snapshots exist for intermediate revision dates (tp20260401-01_05, tp20260415-01_05, tp20260520-01_05, tp20260612-01_05, tp20260715-01_05) — each supersedes the prior.

### 3b. File structure — detailed (verified by agent, from tp20260715-01_05.xlsx download)

**Workbook:** Single sheet named `Sheet1`, 12,415 rows × 8 columns (1 header row + 12,414 data rows).

**Column headers (verified from raw XLSX):**
```
薬価基準収載医薬品コード | 成分名 | 品名 | 各先発医薬品の後発医薬品の有無に関する情報 | 
収載年月日(YYYYMMDD) | 経過措置による使用期限 | 備考 | 
診療報酬における加算等の算定対象から除外する品目
```

English translation:
- Col 0: NHI drug code (12-character alphanumeric)
- Col 1: Active ingredient (成分名)
- Col 2: Brand/trade name (品名)
- Col 3: Originator/generic flag (1 = has generic, blank = originator without generic, `★` = generic product)
- Col 4: Listing date (YYYYMMDD)
- Col 5: Grace period expiry date
- Col 6: Notes (備考)
- Col 7: Excluded from certain reimbursement calculations flag

**Record counts (verified by agent):**
- Total products listed: **12,414**
- Unique active ingredients (成分名): **2,694**
- Unique NHI drug codes: 12,414 (one per product/formulation)
- Rows with listing date populated: 142 (these are recently added drugs only; the column is empty for most of the historical population)

**From the oral-only file (tp20260801-01_01.xlsx), also verified:**
- 7,054 rows (7,055 including header), 15 columns
- Sheet: `ＨＰ用` (HP = home page, i.e., the web-facing version)
- 1,543 unique active ingredients in this file
- Unique 7-digit substance prefixes in the drug code: 1,635

**The tp20260801-01_02.xlsx (injectable-only), also verified:**
- 3,473 data rows
- 936 unique ingredients
- Category: 注射薬 only

**Drug code structure:** 12-character code `XXXXXXXXXXXXX` where the first 7 digits identify the active substance (equivalent to a Japanese ATC-level code). The 8th character is a formulation code, and subsequent characters identify the product. The substance-level prefix is a useful alternative join key if ingredient name matching fails.

### 3c. Answering the core question: does a complete machine-readable list of ALL approved drugs exist?

**Answer: The NHI Yakka (_05 combined file) is the closest practical equivalent, but it is not exactly the same as a registry of all approved drugs.**

Distinctions:
1. **Listed ≠ approved.** A drug can be approved by PMDA but not (yet) listed on the NHI price list. However, non-listed drugs cannot be reimbursed and have essentially zero market, so for practical screening purposes listed ≈ marketed ≈ approved and commercially relevant.
2. **Delisted drugs.** Products whose NHI listing has been withdrawn (grace-period expired, withdrawn from market) are removed from the current Yakka. The PMDA approval itself persists; only the current listing does not. For historical retrospective work, archived Yakka files are needed.
3. **Non-prescription drugs.** The 内用薬/注射薬/外用薬 files in the Yakka cover prescription drugs. OTC drugs are handled separately.
4. **Dental and special categories.** The _03 and _04 files contain dental and other categories (verified as existing from the page; not downloaded separately).

For **enumeration of Japan-approved active substances in machine-readable form**, the recommended recipe is:
1. Download the current `tp20YYMMDD-01_05.xlsx` combined file from `https://www.mhlw.go.jp/topics/20YY/04/tp20YYMMDD-01_05.html`
2. Deduplicate on `成分名` (Col 1) → 2,694 unique ingredients (current as of July 2026)
3. Cross-reference against FDA Drugs@FDA (ANDA/NDA approvals) and EMA centralised approval list
4. Anti-join → Japan-marketed substances with no FDA or EMA approval

**Update frequency:** The _05 combined file is updated on each revision date (typically monthly during the April revision cycle, with dates in April, May, June, July, August). The MHLW page at `tp20260401-01.html` lists all current-year files.

---

## 4. JAPIC (Japan Pharmaceutical Information Center)

| Field | Value |
|---|---|
| Homepage | `https://www.japic.or.jp/` |
| Status | **VERIFIED** HTTP 200, 15,243 bytes (2026-08-05) |
| English content | **None confirmed.** Both `/en/index.html` and `/service/package_insert.html` returned HTTP 404. |
| DI search | `https://www.japic.or.jp/di/index02.html` — **VERIFIED** HTTP 200 |
| iyakuSearch | `https://www.japic.or.jp/di/navi.php?cid=1` — **VERIFIED** HTTP 200 (newly confirmed 2026-08-06) |

JAPIC is the Japan Pharmaceutical Information Center, a non-profit that aggregates Japanese package inserts and drug information. Its main public service is `iyakuSearch` (医薬品サーチ) — a PI search interface.

**Access model:** JAPIC provides a web search interface at `navi.php?cid=1` (prescription drugs) and `navi.php?cid=2` (OTC). The interface is Japanese-language, POST-based, and session-managed. The agent confirmed the page renders (15 KB HTML) but there is **no JSON API and no bulk export visible from the public interface**.

**What JAPIC offers that PMDA does not:**
- Package insert full text (添付文書) in structured form
- Publication `shonin.html` (承認情報) — verified link from the JAPIC homepage
- Cross-links to international product information

**Practical assessment:** JAPIC is useful for fetching individual package insert PDFs once you have a target compound, but it is **not a substitute for the PMDA XLSX or NHI Yakka as a bulk enumeration source**. Its databases are subscription-based for institutional/commercial use.

---

## 5. Japanese Orphan Drug (希少疾病用医薬品 / Kishoyakubyo) Designation System

### 5a. Designation list sources

Three overlapping lists exist. **Use the NIBN Japanese file as the master list.**

#### NIBN English list (stale — critical warning)
- URL: `https://www.nibn.go.jp/activities/promote/documents/orphan_drug_E.pdf`
- **VERIFIED** HTTP 200, content-length not in agent's measurement but redirect chain confirmed: `nibiohn.go.jp` → HTTP 301 → `nibn.go.jp` → HTTP 200, 1,415,820 bytes
- Agency has migrated from `nibiohn.go.jp` → `nibn.go.jp` (National Institute of Biomedical Innovation, Health and Nutrition). Old URLs redirect.
- **⚠️ CRITICAL: This English list is approximately 6 years stale.** Prior agent measured: English tops out at designation #415, latest dates ~2019. Japanese list runs to #733 (August 2025). **That is a 318-designation gap** covering the entire modern biologic/gene-therapy wave. Do not use the English file as the source of truth.

#### NIBN Japanese list (current)
- URL: `https://www.nibn.go.jp/activities/promote/documents/hp_orphanlist_drug.pdf`
- **VERIFIED** HTTP 200 (2026-08-05; re-confirmed 2026-08-06)
- As of prior agent measurement: runs to #733 (令和7年10月1日現在 = current as of 2025-10-01)
- This is the authoritative current list. Machine-translate the Japanese.

**Columns in the Japanese list (translated from prior agent inspection):**
- Fiscal year of designation | Date of designation | Designation number | Drug name | Anticipated indication | Applicant receiving designation | Address | Notes

#### MHLW designation list (partial, post-2020 only)
- URL: `https://www.mhlw.go.jp/content/11120000/001701020.pdf`
- **VERIFIED** HTTP 200, 419,481 bytes, 7 pages (2026-08-05; re-confirmed 2026-08-06)
- Coverage: post-2020-09-01 only. Columns: 指定年度 | 指定日 | 指定番号 | 医薬品の名称 | 予定される効能又は効果 | 指定を受けた者 | 住所 | 備考

#### The NIBN English list (full column schema from prior agent)
Useful for understanding the schema even though stale:
- Fiscal year (Heisei) | Calendar year | Date of designation | Designation number | Grant period | Name of drug | Anticipated indications | Applicant | **Indications approved for marketing** | Applicant obtaining approval | **Date of approval** | Product approved | Trade name | **General name of active ingredient** | Notes | Date of revocation | Status

The approval-date and approval-indication columns create a direct designation → approval join, which is the core analytical table for identifying whether a Japan-orphan drug subsequently obtained marketing approval.

### 5b. Orphan designation and PRV funnel relevance

Japan's orphan designation (希少疾病用医薬品) requires anticipated patient population ≤ 50,000 in Japan and a clinically meaningful unmet need. It confers accelerated review and R&D incentives under the Pharmaceuticals and Medical Devices Act (薬機法, formerly Pharmaceutical Affairs Law).

**For Funnel A (PRV-eligible):** Japan-orphan-designated drugs that are also approved in Japan but have never entered US regulatory review are the highest-priority candidates. The join recipe:
1. From NIBN Japanese orphan list (#733 current) → extract approved drugs (rows where approval date is populated)
2. Cross-reference against FDA Drugs@FDA via active ingredient → identify those with zero FDA NDA/ANDA
3. Residual = Japan-orphan-approved, FDA-unreviewed → Funnel A candidates

The inline designation of orphan status in the PMDA FY XLSX (`【希少疾病用医薬品】`) provides a simpler path for recent approvals: the 29 orphan+new-approval rows in FY2025 above are pre-filtered candidates.

---

## 6. Sakigake Designation (先駆的医薬品等指定制度)

Sakigake is Japan's breakthrough therapy analog, established 2015 (trial phase), formalised under 薬機法. It designates highly innovative drugs for accelerated review (6-month target) and intensive pharmaceutical affairs consultation.

### 6a. Designation list

| Field | Value |
|---|---|
| List page | `https://www.pmda.go.jp/review-services/drug-reviews/0003.html` |
| Status | **VERIFIED** HTTP 200, 125,883 bytes (2026-08-05) |
| Drug list PDF | `https://www.pmda.go.jp/files/000267981.pdf` |
| PDF status | **VERIFIED** HTTP 200, 167,603 bytes (re-confirmed 2026-08-06) |
| As of date | 2026年6月23日現在 (2026-06-23) |

**Drug Sakigake designations (from PDF, agent-verified count):**
- Pattern `第\d+号` appears 9 times in the text extraction, but designation numbers run to 第15号 (15 designations total). The discrepancy is a PDF text-extraction artifact from the multi-column layout.
- **Total drug Sakigake designations current as of 2026-06-23: 15** (numbering confirmed from tail of PDF: 第13号=2024-11-27, 第14号=2025-09-29, 第15号=current)

**Designation detail sample (from agent's PDF extraction):**
- `(R3 先駆薬) 第1号` — 2021-08-24 — ペボネジスタット塩酸塩 — 武田薬品工業 — MDS (骨髄異形成症候群) — **Note: 指定取消 (designation revoked 2021-12-09)**
- `(R3 先駆薬) 第2号` — 2021-11-26 — バリシチニブ — Eli Lilly — Interferonopathies (CANDLE, STING vasculopathy, Aicardi-Goutières) — **Note: 指定取消 (revoked 2024-09-20)**
- `(R7 先駆薬) 第14号` — 2025-09-29 — Oveporexton — 武田薬品工業 — Narcolepsy type 1 — **Approval date: 2026-06-23**
- `(R8 先駆薬) 第15号` — etentamig — アッヴィ合同会社 — Relapsed/refractory systemic AL amyloidosis

**Other Sakigake PDFs on 0003.html (not the drug list):**
- `/files/000248718.pdf` — Medical devices Sakigake list (先駆的医療機器) — confirmed by agent
- `/files/000278346.pdf` — Regenerative medicine Sakigake list (先駆的再生医療等製品) — confirmed by agent (as of 2026-06-08, 4 designations including bemdaneprocel from Bayer and MCO-010 from Nanoscope Therapeutics)

**No English Sakigake drug list exists.** The three PDFs on `0003.html` are all Japanese. The `[SAKIGAKE designation]` tags in the English Approved Drugs PDF (§1a, 5 occurrences) are the only English-language Sakigake coverage.

### 6b. Sakigake and PRV relevance

Sakigake-designated drugs are typically novel active ingredients — making them natural Funnel A candidates if they lack prior US approval. However, many Sakigake drugs are oncology or precision-medicine products that are simultaneously in US/EU development. Cross-check each Sakigake drug against the FDA breakthrough therapy designation list and EU PRIME designation list before treating as Japan-only.

---

## 7. The PMDA iyakuSearch (医薬品 添付文書等情報検索)

| Field | Value |
|---|---|
| URL | `https://www.pmda.go.jp/PmdaSearch/iyakuSearch/` |
| Status | **VERIFIED** HTTP 200 (2026-08-05; re-confirmed 2026-08-06) |
| Technology | Apache Struts, POST-based, JavaScript-rendered |

This is PMDA's prescription drug PI/package insert search. The agent made two attempts to programmatically extract a product count:
1. POST to `/PmdaSearch/iyakuSearch/` with blank search parameters — returned the search form HTML with JavaScript validation alerts, no results
2. Browse-by-character POST — returned the same form HTML

**Conclusion: PMDA iyakuSearch is not bulk-queryable without JavaScript execution.** It requires a browser or Playwright/Puppeteer to submit the form and paginate results. This makes it unsuitable as a primary enumeration source.

**Detail page URL patterns (from prior agent via `06-reference-regulators.md`):**
- `https://www.pmda.go.jp/PmdaSearch/iyakuDetail/GeneralList/{YJ-base}` — product detail page
- English package inserts: effectively nonexistent. The English section lists only 6 products (enteral nutrition, contrast agents). **Do not plan around English SmPCs from PMDA.**

---

## 8. Japan Open Data Portals — Negative Findings

The agent checked two potential routes for a structured machine-readable drug registry beyond the Yakka:

### data.go.jp
- `https://www.data.go.jp` redirects (HTTP 301) to `https://data.e-gov.go.jp`
- **VERIFIED** 2026-08-05

### data.e-gov.go.jp (CKAN API)
- `https://data.e-gov.go.jp/data/api/3/action/package_search?q=医薬品+承認&rows=10` — **VERIFIED** HTTP 200, `count: 993`
- The 993 results are general health ministry statistical reports, white papers, and licensing counts — **not a structured drug approval database**
- Second search `q=薬価+薬社` — **VERIFIED** HTTP 200, `count: 0`
- Third search `q=薬価` (newly verified 2026-08-06) — HTTP 200, `count: 259`, results are pharmaceutical expenditure trend surveys (調剤医療費の動向調査) — statistical reports, not a product registry

**Conclusion: No structured machine-readable drug approval registry is published on Japan's open data portal.** The NHI Yakka XLSX files (§3) on `mhlw.go.jp` are the government's de-facto machine-readable drug list, but they live on a thematic topic page rather than on the open data portal.

---

## 9. The "Approved in Japan, Never Commercialized Elsewhere" Phenomenon

### Why it happens

Japan has distinct approval pathways that generate Japan-only molecules:

1. **JAN compounds with no INN.** Many traditional Japanese-origin drugs received a JAN (Japanese Accepted Name) under the pre-INN era and were never submitted for WHO INN listing. These have no global nomenclature footprint and do not show up in FDA or EMA databases.

2. **Japanese academic/MHLW-driven development.** Japan's MHLW can sponsor or co-develop drugs for rare diseases with no commercial partner intending to market globally. The result is a marketed product with a Japanese approval but no NDA/MAA.

3. **Domestic market sufficient for commercial viability.** Japan's 125M population and high insurance reimbursement rate make Japan-only viable for certain conditions where the US/EU rare-disease economics are unfavorable.

4. **Cultural / regulatory friction for foreign filing.** Some Japanese manufacturers do not pursue overseas approvals due to translation burdens, ICH submission costs, or lack of international regulatory experience.

5. **Time-to-approval gaps becoming permanence.** A drug approved in Japan in the 1990s–2000s before the US rare-disease field matured may never have been submitted to FDA, even if it could qualify now.

### How to identify candidates

The presence of `JAN` (rather than INN/USAN/BAN) in the KEGG drug name string is the strongest machine-readable signal of Japan-only provenance. Of 12,891 KEGG DRUG entries, 2,267 carry the JAN tag. However:
- Many JAN compounds are also approved in the US (warfarin sodium is a JAN/USP compound)
- The anti-join against FDA Drugs@FDA by active ingredient is the definitive check

**Worked example confirmed by prior agent:** Aceneuramic acid (acenobel, `JAN`: aceneuramic acid; INN does not exist separately), approved in Japan March 2024 for GNE myopathy, with English review report at `https://www.pmda.go.jp/files/000273006.pdf`. This is a Japan-only approval. GNE myopathy (UDP-GlcNAc epimerase/kinase deficiency) qualifies as a rare pediatric disease under RPDD criteria.

### The diff is runnable, but requires handling JAN/INN heterogeneity

The major technical barrier is name-matching. Japan uses JAN, not always INN. Systematic transformations needed before joining against FDA/EMA:
- Strip salt/hydrate qualifiers: `iptacopan hydrochloride hydrate` → `iptacopan`
- Strip `（遺伝子組換え）` = `(genetical recombination)` suffix on Japanese biologics
- Normalise Latin `-um` vs Japanese `-ム` phonetic endings
- For compounds with only a JAN, look up ChEBI, ChemSpider, or KEGG's cross-reference (`DBLINKS CAS:` in the KEGG entry) to find a canonical structure for matching

---

## 10. Runnable Recipe: Enumerate Japan-Approved Active Substances in Machine-Readable Form

### Step 1: Download the NHI Yakka combined file

```python
import urllib.request, datetime

# Get the page to find current filename (updates monthly)
parent_url = "https://www.mhlw.go.jp/topics/2026/04/tp20260401-01.html"
# Or replace year: https://www.mhlw.go.jp/topics/YYYY/04/tp{YYYYMMDD}-01.html

# Direct download of the current combined file (as of 2026-08-06):
direct_url = "https://www.mhlw.go.jp/topics/2026/04/xls/tp20260715-01_05.xlsx"
urllib.request.urlretrieve(direct_url, "yakka_combined.xlsx")
```

### Step 2: Extract unique active ingredients

```python
import openpyxl

wb = openpyxl.load_workbook("yakka_combined.xlsx", read_only=True)
ws = wb.active
rows = list(ws.rows)

# Header row: 薬価基準収載医薬品コード | 成分名 | 品名 | ...
# Col index 1 = 成分名 (active ingredient)
ingredients = set()
for row in rows[1:]:  # skip header
    val = str(row[1].value or '').strip()
    if val:
        ingredients.add(val)

print(f"Unique active ingredients: {len(ingredients)}")  # ~2,694
```

### Step 3: Cross-reference against FDA

```python
import requests, time

fda_not_found = []
for ing in ingredients:
    r = requests.get(
        "https://api.fda.gov/drug/drugsfda.json",
        params={"search": f'openfda.generic_name:"{ing}"', "limit": 1},
        timeout=10
    )
    if r.status_code == 404 or r.json().get("meta", {}).get("results", {}).get("total", 0) == 0:
        fda_not_found.append(ing)
    time.sleep(0.1)  # polite rate limiting

# fda_not_found = Japan-listed substances with no FDA match by generic name
```

### Step 4: Enrich with PMDA XLSX for orphan/rare-disease flag

Download each per-FY XLSX from `https://www.pmda.go.jp/review-services/drug-reviews/review-information/p-drugs/0010.html`. For rows where Col 6 (indication) contains `【希少疾病用医薬品】`, flag the ingredient as Japan-orphan-designated.

### Step 5: Enrich with NIBN orphan list

Download `https://www.nibn.go.jp/activities/promote/documents/hp_orphanlist_drug.pdf`, extract Japanese text, machine-translate, and join on drug name to add NIBN orphan designation number and date.

### Expected output record counts

| Source | Records |
|---|---|
| NHI Yakka (combined, Jul 2026) | 12,414 products / **2,694 unique ingredients** |
| NIBN Orphan list (Japanese, current) | **~733 designations** (through Aug 2025) |
| PMDA FY XLSX (FY2025 orphan+new approval) | **29 qualifying rows** |
| KEGG DRUG total | 12,891 entries |
| KEGG DRUG with JAN tag | **2,267** |
| English review reports | **448** |

---

## Unfinished — Worth Re-Running

The original agent was cut off before completing:

1. **PMDA iyakuSearch total product count via browser automation.** The agent confirmed the endpoint is JS-gated. A Playwright/Puppeteer pass that (a) submits a blank search or browses by first character A–Z, (b) extracts total result count per letter, would yield a precise count of all currently approved prescription drugs in PMDA's own database. This would be the authoritative number to compare against the Yakka's 12,414.

2. **e-gov open data portal for any structured MHLW drug dataset.** The agent found 993 results for `医薬品+承認` but only sampled 10. A deeper pass filtering to MHLW as publisher might surface a structured approval dataset not visible in the top-10 sample.

3. **Cross-referencing the 29 FY2025 orphan new approvals against FDA Drugs@FDA.** The agent compiled the full list but did not execute the anti-join. At least triheptanoin (Dojolvi), sepiapterin (Sepreviance), odevixibat (Bylvay), and sebelipase alfa are US-approved — these would be filtered out. The remainder should be checked individually.

4. **JAPIC iyakuSearch product count.** The agent confirmed `navi.php?cid=1` renders but did not successfully extract a product count. JAPIC may index more products than the Yakka if it includes discontinued/withdrawn products with still-accessible package inserts.

5. **Verifying the NIBN Japanese orphan list page count.** The prior agent reported #733 as of 2025-10-01. The current date is 2026-08-06; the list has likely grown. A direct download and line count would give the current figure.

---

## URL Ledger

### VERIFIED

| URL | Method | Result | Date |
|---|---|---|---|
| `https://www.pmda.go.jp/english/review-services/reviews/approved-information/drugs/0002.html` | curl -sI | HTTP 200, 52,895 bytes | 2026-08-05 + 2026-08-06 |
| `https://www.pmda.go.jp/files/000281190.pdf` | curl -sI | HTTP 200, 3,206,009 bytes, `application/pdf` | 2026-08-05 |
| `https://www.pmda.go.jp/review-services/drug-reviews/review-information/p-drugs/0010.html` | curl -sI | HTTP 200, 126,752 bytes | 2026-08-05 |
| `https://www.pmda.go.jp/files/000277966.xlsx` | curl download | HTTP 200, 32,825 bytes, correct XLSX MIME | 2026-08-05 |
| `https://www.pmda.go.jp/english/review-services/reviews/approved-information/drugs/0001.html` | curl | HTTP 200, 267,105 bytes | 2026-08-05 |
| `https://www.pmda.go.jp/files/000273006.pdf` | verified in prior agent | HTTP 200 | 2026-08-05 |
| `https://www.pmda.go.jp/PmdaSearch/iyakuSearch/` | curl -sI | HTTP 200 | 2026-08-05 + 2026-08-06 |
| `https://www.pmda.go.jp/review-services/drug-reviews/0002.html` | curl -sI | HTTP 200, 129,411 bytes | 2026-08-05 |
| `https://www.pmda.go.jp/review-services/drug-reviews/0003.html` | curl -sI | HTTP 200, 125,883 bytes | 2026-08-05 |
| `https://www.pmda.go.jp/files/000267981.pdf` | curl | HTTP 200, 167,603 bytes (Sakigake drug list, 2026-06-23) | 2026-08-05 + 2026-08-06 |
| `https://www.pmda.go.jp/files/000278346.pdf` | curl | HTTP 200, 118,190 bytes (Sakigake regen med list) | 2026-08-05 |
| `https://www.pmda.go.jp/files/000248718.pdf` | curl | fetched (medical device Sakigake list) | 2026-08-05 |
| `https://rest.kegg.jp/info/drug` | curl | HTTP 200; `dr 12,891 entries, Last update 2026/08/05` | 2026-08-05 + 2026-08-06 |
| `https://rest.kegg.jp/list/drug` | curl -sI | HTTP 200, `text/plain` | 2026-08-05 |
| `https://rest.kegg.jp/find/drug/JP18` | curl | HTTP 200, 1 result | 2026-08-06 |
| `https://rest.kegg.jp/find/drug/JAN` | curl | HTTP 200, 2,273 lines | 2026-08-06 |
| `https://www.kegg.jp/kegg/legal.html` | curl | HTTP 200; academic-free / commercial-requires-licence text confirmed | 2026-08-05 + 2026-08-06 |
| `https://www.japic.or.jp/` | curl -sI | HTTP 200, 15,243 bytes | 2026-08-05 |
| `https://www.japic.or.jp/di/index02.html` | curl -sI | HTTP 200 | 2026-08-05 |
| `https://www.japic.or.jp/di/navi.php?cid=1` | curl -sI | HTTP 200 | 2026-08-05 + 2026-08-06 |
| `https://www.mhlw.go.jp/topics/2026/04/tp20260401-01.html` | curl -sI | HTTP 200, Last-Modified 2026-07-31 | 2026-08-05 + 2026-08-06 |
| `https://www.mhlw.go.jp/topics/2026/04/xls/tp20260801-01_01.xlsx` | curl | HTTP 200, 669,088 bytes; 7,054 oral drug products, 1,543 unique ingredients | 2026-08-05 + 2026-08-06 |
| `https://www.mhlw.go.jp/topics/2026/04/xls/tp20260801-01_02.xlsx` | curl download | HTTP 200; 3,473 injectable products, 936 unique ingredients | 2026-08-05 |
| `https://www.mhlw.go.jp/topics/2026/04/xls/tp20260715-01_05.xlsx` | curl | HTTP 200, 683,699 bytes; 12,414 products, 2,694 unique ingredients | 2026-08-05 |
| `https://www.mhlw.go.jp/content/11120000/001701020.pdf` | curl -sI | HTTP 200, 419,481 bytes | 2026-08-05 + 2026-08-06 |
| `https://www.nibn.go.jp/activities/promote/documents/orphan_drug_E.pdf` | curl (via redirect from nibiohn.go.jp) | HTTP 200, 1,415,820 bytes | 2026-08-05 + 2026-08-06 |
| `https://www.nibn.go.jp/activities/promote/documents/hp_orphanlist_drug.pdf` | curl -sI | HTTP 200 | 2026-08-05 + 2026-08-06 |
| `https://www.nibiohn.go.jp/activities/promote/documents/orphan_drug_E.pdf` | curl -sIL | HTTP 301 → `nibn.go.jp` → HTTP 200 | 2026-08-05 |
| `https://data.e-gov.go.jp/data/api/3/action/package_search?q=医薬品+承認&rows=10` | curl | HTTP 200, count: 993 | 2026-08-05 |
| `https://data.e-gov.go.jp/data/api/3/action/package_search?q=薬価` | curl | HTTP 200, count: 259 | 2026-08-06 |
| `https://api.fda.gov/drug/drugsfda.json` | prior agent (from 06-reference-regulators.md) | HTTP 200, JSON | 2026-08-05 |
| `https://download.open.fda.gov/drug/drugsfda/drug-drugsfda-0001-of-0001.json.zip` | prior agent | HTTP 200, 9,376,614 bytes | 2026-08-05 |

### UNVERIFIED

| URL | Reason |
|---|---|
| `https://www.japic.or.jp/service/package_insert.html` | HTTP 404 — page does not exist; JAPIC reorganised site |
| `https://www.japic.or.jp/en/index.html` | HTTP 404 — no English pages confirmed |
| `https://www.japic.or.jp/service/database/iyakusearch.html` | HTTP 404 |
| `https://rest.kegg.jp/info/yk` | Returned no output — may require subscription |
| `https://rest.kegg.jp/info/jtc` | Returned no output — may require subscription |
| `https://www.mhlw.go.jp/content/11120000/001679247.pdf` | Orphan devices list — URL extracted from verified MHLW page, not downloaded |
| `https://www.mhlw.go.jp/content/11120000/001698413.pdf` | Orphan regenerative products list — URL extracted from verified MHLW page, not downloaded |
| `https://www.pathway.jp/en/academic.html` | KEGG commercial licence contact page — not fetched |
| Individual PMDA FY XLSX files for FY2004–FY2024 | Only FY2025 was downloaded; others exist per the index page but were not individually verified |
| Pre-2004 PMDA approval records | Not in any machine-readable public source identified |
| JAPIC iyakuSearch total product count | Interface is JS-gated; count not extractable without browser automation |
