<!-- RECOVERED from subagent transcript agent-a66a6700f30327d69.jsonl, session fd64561f-7c90-41a2-95cf-b4a133a8fe0f, research date 2026-08-05.
     Reference-regulator agent, Swissmedic.
     Verbatim agent deliverable — not re-edited. -->

All URLs verified. Here are the findings.

---

# Swissmedic Machine-Accessible Drug Approval Data — Verified Findings (2026-08-05)

## 0. Is there a public API? — **No.**

- Swissmedic publishes **no REST/GraphQL API** for authorisation data. Probed `https://www.swissmedic.ch/api`, `/api/v1`, `/swissmedic/en/home/services/api.html` → all **HTTP 404** (VERIFIED).
- Everything is **static file drops**: monthly XLSX on the AEM `dam` tree, a monthly XML ZIP on an Azure-hosted OGD bucket, and per-product PDFs.
- The only queryable API touching Swissmedic is **opendata.swiss's CKAN API** (federal portal, not Swissmedic): `https://opendata.swiss/api/3/action/package_search?q=swissmedic` → HTTP 200, `count: 7` (6 Swissmedic-owned) (VERIFIED). It returns *metadata pointing at the same static files* — no record-level query.
- Practical consequence: you diff monthly snapshots yourself. There is no "what changed" endpoint and no webhook.

---

## 1. BEST SOURCE — OGD bulk XML export (relational, 10 tables)

This is buried and not linked from the "Listen und Verzeichnisse" page. It is materially better than the Excel files.

- **URL:** `https://ogd.swissmedic.cloud/ogd-arzneimittel/Daten/OGD.zip` — **VERIFIED** (HTTP 200, 2,873,492 bytes, `application/zip`, PK magic, `last-modified: Fri, 31 Jul 2026 22:56:11 GMT`)
- **Auth:** none. No cookie, no T&C click-through, no key.
- **Contents:** 10 XML files, 75.7 MB uncompressed. `OGD-Export-Datum.XML` declares `<EXPORT_DATUM>2026-07-31</EXPORT_DATUM>`.

| File | Record tag | Count (VERIFIED) |
|---|---|---|
| `OGD-Praeparate.XML` | `<PRAEPARAT>` | **7,965** (HAM 7,207 / TAM 758) |
| `OGD-Sequenzen.XML` | `<SEQUENZ>` | 12,631 |
| `OGD-Packungen.XML` | `<PACKUNG>` | 20,048 |
| `OGD-Deklarationen.XML` | `<DEKLARATION>` | (54 MB — full composition, per component/line) |
| `OGD-ATC-Codes.XML` | `<ATC>` | 2,219 |
| `OGD-Stoff-Synonyme.XML` | `<SYNONYME>` | substance synonyms w/ `QUELLE` (e.g. `DCI`) |
| `OGD-Adressen.XML` | `<ADRESSEN>` | MA-holder addresses (`PARTNER_NR` FK) |
| `OGD-User-Defined-Codes.XML` | `<UDC>` | 7,121 code rows, 4 languages |
| `OGD-Applikationsarten pro Sequenz.XML` | `<APPLIKATIONSART>` | route of admin |

- **`<PRAEPARAT>` fields (VERIFIED by parsing):** `VERWENDUNG` (HAM/TAM), `ZULASSUNGSNUMMER`, `PRAEPARATENAME`, `ARZNEIFORM`, `ATC_CODE`, `HEILMITTEL_CODE`, `ZULASSUNGSSTATUS`, `ZULASSUNGSKATEGORIE`, `ZULASSUNGSINHABERIN`, `ERSTZULASSUNGSDATUM`, `BASIS_ZULASSUNGSNUMMER`, `ABGABEKATEGORIE`, `IT_NUMMER`, `ANWENDUNGSGEBIET`, `ABLAUFDATUM`, `CHARGENFREIGABE_PFLICHT`, `EINZELEINFUHR_BEWILLIG_PFLICHT`.
- **Value distributions (VERIFIED):** `ZULASSUNGSSTATUS` = Z 7,933 / B 20 / D 11 / S 1. `ZULASSUNGSKATEGORIE` = blank 7,463 / C 350 / S 86 / P 66. ATC populated on 6,307 / 7,207 HAM.
- **Code decoding:** `MA_TYPE` → `H`=main authorisation, `E`=export, `2`=provisional registration, `3`/`4`=in-house speciality IIb/IIa. `TP_CODE` → 20 values incl. `TGT` transplant: gene therapy product, `TGW` tissue product, `BT` biological, `S` synthetic. UDC carries `SPRACH_CODE` D/E/F/I — **English descriptions ARE present** (1,929 EN rows).
- **XSDs:** `https://ogd.swissmedic.cloud/ogd-arzneimittel/Beschreibungen/OGD-Praeparate.xsd` (+ `OGD-Sequenzen.xsd`, `OGD-ATC-Codes.xsd`, `OGD-Deklarationen.xsd`) — all **VERIFIED HTTP 200**.
- **Docs (EN):** `https://ogd.swissmedic.cloud/ogd-arzneimittel/Beschreibungen/Beschreibungen_OGD_EN.pdf` — **VERIFIED** (12-page PDF, read; contains the ER diagram and field definitions). DE/FR/IT variants at same path with `_DE`/`_FR`/`_IT`.
- **Update cadence (from that PDF, VERIFIED):** regenerated **the 1st calendar day of each month**; snapshot reflects the **last calendar day of the previous month**. Includes status `authorised`, `temporary`, `suspended`, plus items whose status changed since last publication (`no longer authorised`, `temporary authorisation expired`).

### Historical archive — the single most valuable asset for your use case
- **Directory:** `https://ogd.swissmedic.cloud/ogd-arzneimittel/Archiv/` — **VERIFIED** (HTTP 200, browsable Apache-style index).
- **53 monthly snapshots, `202202` → `202607`, contiguous except `202505` is MISSING** (VERIFIED by parsing the index).
- **GOTCHA:** the EN documentation says the naming is `OGD_JJJJMM.ZIP` (uppercase). Actual files are **lowercase `.zip`** — `OGD_202607.ZIP` → **404**, `OGD_202202.zip` → **200 / 2,400,908 bytes / PK magic** (both VERIFIED). Uppercase probes silently fail.
- This gives you a 4.5-year monthly time series to reconstruct indication changes and first-authorisation events without scraping.

### Critical limitation
- **There is NO orphan-drug field anywhere in the OGD export.** I grepped all 10 XML files for `orphan*`: every hit is a false positive — `Dextromethorphan` product names (Bisolvon, Coop Vitality, Amavita) and substance names `orphanum`/`Orphanol` (VERIFIED by inspecting match context). Orphan status is **only** in the separate Excel file (§3).

---

## 2. The authorised medicines lists (XLSX) — exact URLs

Landing page: `https://www.swissmedic.ch/swissmedic/en/home/services/listen_neu.html` — **VERIFIED** (HTTP 200, 144,538 bytes; 47 dam links extracted from raw HTML).

> **MAJOR GOTCHA — host.** The pattern is `https://www.swissmedic.ch/dam/...`. There is **no `dam.swissmedic.ch` host** — `curl: (6) Could not resolve host: dam.swissmedic.ch` (VERIFIED). Any tool that "helpfully" rewrites the relative `/dam/...` href into a `dam.swissmedic.ch` origin produces a dead URL. Likewise the `schemaLocation` inside the OGD XML points at `https://ogd.swissmedic.ch/...` which **also does not resolve** — the live host is `ogd.swissmedic.cloud`.

### 2a. Extended list of authorised medicinal products — **use this one**
- **URL:** `https://www.swissmedic.ch/dam/swissmedic/en/dokumente/internetlisten/erweiterte_ham_ind.xlsx.download.xlsx/erweiterte_ham_ind.xlsx`
- **VERIFIED:** HTTP 200, 2,581,811 bytes, `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`, PK magic, `Microsoft Excel 2007+`.
- Sheet: **`Erweiterte Liste HAM`** (single sheet). Header row **7**. **11,066 data rows**, **25 columns**. Preamble rows 1–6 carry the title and `Stand / État au: 31.07.2026`.
- **Grain:** one row per **dosage strength**, not per product — 11,066 rows map to only **6,762 distinct `Zulassungsnummer`** (VERIFIED). De-duplicate before counting products.
- **Columns (exact, VERIFIED — each cell is bilingual DE/FR separated by newlines):**

| # | Col | Field |
|---|---|---|
| 1 | A | Zulassungsnummer / N° d'autorisation |
| 2 | B | Dosisstärke-nummer / N° de dosage |
| 3 | C | Bezeichnung des Arzneimittels |
| 4 | D | Zulassungsinhaberin (MA holder) |
| 5 | E | **Zulassungsart** (Hauptzulassung 10,275 / Exportzulassung 791) |
| 6 | F | Heilmittelcode (21 distinct: Synthetika 8,420; Biotechnologika 981; …; Transplantat: Gentherapieprodukt 22) |
| 7 | G | **Verfahren nach Art. 14 Abs. 1 Bst. abis-quater HMG** ← reliance flag |
| 8 | H | IT-Nummer |
| 9 | I | **ATC-Code** — populated on **10,586 / 11,066 (95.7%)** |
| 10 | J | **Erstzulassungsdatum Arzneimittel** — parses as datetime on 100% of rows; range **1933-09-13 → 2026-07-30** |
| 11 | K | Zulassungsdatum Dosisstärke |
| 12 | L | Gültigkeitsdauer der Zulassung |
| 13/14 | M/N | Abgabekategorie (dose strength / product) |
| 15 | O | **Wirkstoff(e)** — active substance, Latin INN (`capecitabinum`) |
| 16 | P | Zusammensetzung (full composition) |
| 17 | Q | Volldeklaration rev. AMZV umgesetzt |
| 18 | R | **Anwendungsgebiet Arzneimittel** ← indication free text |
| 19 | S | Anwendungsgebiet Dosisstärke |
| 20 | T | Gentechnisch hergestellte Wirkstoffe |
| 21 | U | Kategorie bei Insulinen |
| 22 | V | Verz. bei betäubungsmittelhaltigen Arzneimitteln |
| 23 | W | Besondere Angaben |
| 24 | X | **Zulassungsstatus** (zugelassen 11,042 / befristet 24) |
| 25 | Y | **Befristet zugelassene Indikation(en) / Ablauf Datum** |

- **No orphan column here.** Join to the orphan file on `Zulassungsnummer`.

### 2b. Basic authorised medicines list
- **URL:** `https://www.swissmedic.ch/dam/swissmedic/en/dokumente/internetlisten/zugelassene_arzneimittel_ham_ind.xlsx.download.xlsx/Zugelassene_Arzneimittel_HAM.xlsx`
- **VERIFIED:** HTTP 200, 1,004,159 bytes, PK magic. Sheet `Zugelassene Arzneimittel HAM mI`, header row 7, **11,066 data rows, 10 columns**.
- Strict subset of 2a (no ATC, no indication, no substance). **Ignore it — 2a supersedes it entirely at 2.5× the size.**

### 2c. Other lists on the same page (all `.download.xlsx`, all `www.swissmedic.ch/dam/...`)
Paths verified present in raw HTML; sizes/dates from the page's own link labels:
- Authorised packaging: `.../zugelassene_packungen_human.xlsx.download.xlsx/zugelassene_packungen_ham.xlsx`
- Active substances (Stoffliste): `.../zugelassen_wirkstoffe.xlsx.download.xlsx/Stoffliste.xlsx`
- Temporarily authorised: `.../befristete_ham.xlsx.download.xlsx/Befristet_zugelassene_Arzneimittel%20HAM.xlsx`
- Co-marketing: `.../co-marketing_ham.xlsx.download.xlsx/Co-Marketing_nachBasis%20HAM.xlsx`
- **Document protection (data exclusivity): `.../unterlagenschutz.xlsx.download.xlsx/Unterlagenschutz.xlsx`** ← directly relevant to repurposing exclusivity
- Vaccines/blood/immunologicals: `.../zugelassene-impfstoffe-blutprodukte-andere-immunologische-arzneimittel.xlsx.download.xlsx/IBP.xlsx`
- Gene-tech substances: `.../gentechnologisch_ws_ham.xlsx.download.xlsx/Gentechliste%20HAM.xlsx`
- Reallocations to category B: `.../liste-umteilungen-abgabekategorie_b.xlsx.download.xlsx/Liste-Umteilungen-Abgabekategorie_B.xlsx`
- Authorised **procedures**: `.../zugelassene_Verfahren.xlsx.download.xlsx/Verfahren.xlsx` — **VERIFIED downloaded** (255,448 bytes, PK). Tiny and **stale: `Stand 01.09.2020`**, 4 data rows (pathogen-inactivation systems).
- Applications received: `.../gesuchseingaenge-ham.xlsx.download.xlsx/Gesuchseing%C3%A4nge%20HAM_31012021.xlsx` — **filename dates to 2021; treat as abandoned.**

---

## 3. Orphan drug status list — the key file for you

- **URL:** `https://www.swissmedic.ch/dam/swissmedic/en/dokumente/internetlisten/status_orphandrug_ham.xlsx.download.xlsx/Liste_OrphanDrug_Internet.xlsx`
- **VERIFIED:** HTTP 200, **345,547 bytes**, `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`, PK magic, `Microsoft Excel 2007+`.
- Sheet: **`Orphan`** (single). Header row **4**. **726 data rows**, **11 columns**. `Stand / État au: 31.07.2026`.
- **Columns (exact, VERIFIED):**
  1. `Wirkstoff(e)` / Principe(s) actif(s) — Latin INN
  2. `Gesuchstellerin / Zulassungsinhaberin` — applicant / MA holder
  3. **`Orphan Drug Status gem. Art.14 Abs.1 Bst.f HMG, Art.4, 5, 24-26 VAZV — verliehen für folgende Indikation(en)`** ← the designated indication (free text)
  4. **`Status verliehen am`** — designation granted date
  5. **`Status entzogen / verzichtet am`** — withdrawn/renounced date
  6. `Zulassungsstatus des Arzneimittels`
  7. **`Zulassungsnummer`** ← join key to §2a / OGD
  8. `Bezeichnung des Arzneimittels`
  9. `Zulassungsdatum`
  10. `Befristete Zulassung bis`
  11. `Zugelassenes Anwendungsgebiet` — the *authorised* indication (vs. col 3 = *designated* indication)
- **Statistics (VERIFIED):** 459 distinct active substances; 320 distinct authorisation numbers. Designation dates span **2005-04-19 → 2026-07-17**. **53 rows carry a withdrawal/renunciation date.**
- `Zulassungsstatus` split: **Zugelassen 442 / blank 265 / Befristet 19**. The **265 blanks are designations with no Swiss authorisation yet** — i.e. designated-but-unapproved, the highest-signal subset for repurposing whitespace analysis.
- **Grain gotcha:** one row per (substance × designated indication × authorisation number). A substance with 2 designated indications and 2 authorisation numbers yields 4 rows — e.g. `acalabrutinibum` appears for both Waldenström and CLL/SLL against the same Zul.-Nr. 68817. Never count rows as "number of orphan drugs".
- **Col 3 vs col 11 diverge** — designated indication is often broader/different from the authorised one (visible on the acalabrutinib rows). For repurposing, col 3 is the designation scope and col 11 is what actually made it onto the label.

---

## 4. SwissPAR (Swiss Public Assessment Reports)

- **Index page:** `https://www.swissmedic.ch/swissmedic/en/home/humanarzneimittel/authorisations/swisspar.html` — **VERIFIED** (HTTP 200, 231,924 bytes).
- **Yes, there is a single index page** listing everything alphabetically (A–C, D–F, G–K, L–N, O–R, S–U, V–Z sections). **388 SwissPAR PDF links** on that one page (VERIFIED by parsing raw HTML) — no pagination, no JS required, one fetch gets the whole corpus.
- **Format:** PDF. **Language: English only** — per the page text, published in English only using specific technical terminology. This is the *only* substantial Swissmedic assessment content that is natively English.
- **Coverage:** human medicines with **new active substances**, transplant products, **both approved and rejected** applications, plus supplementary reports for **additional indications** (that last category is directly useful for repurposing precedent).
- **Filename convention is fully machine-parseable (VERIFIED, 355 of 388 parsed cleanly):**
  `/dam/swissmedic/en/dokumente/zulassung/swisspar/{Zulassungsnummer}-{product}-{NN}-swisspar-{YYYYMMDD}.pdf.download.pdf/{free-form}.pdf`
  → gives you authorisation number, sequence (`01`=initial, `02`=indication extension), and publication date **without opening the PDF**.
- **270 distinct authorisation numbers**; by publication year: 2019:2, 2020:24, 2021:35, 2022:54, 2023:38, 2024:65, 2025:79, 2026:55 (VERIFIED).
- **Parsing gotchas:** the trailing filename segment is free-form and inconsistently cased/encoded (`SwissPAR%20Tecvayli_G102764195.pdf`, `2026-07-20_final_SwissPAR_Leqvio_IE%20ab%2012J%20plus%20FI%20engl.pdf`). Product slug case varies (`Cablivi` vs `cablivi`). Two entries carry malformed dates (`2027xxxx`, `2408xxxx`) — validate before parsing.
- **Sample verified download:** `https://www.swissmedic.ch/dam/swissmedic/en/dokumente/zulassung/swisspar/69592-reblozyl-01-swisspar-20260716.pdf.download.pdf/SwissPAR_Reblozyl.pdf` — **VERIFIED** HTTP 200, 726,551 bytes, valid PDF 1.7.
- **Update cadence:** rolling, per authorisation decision (most recent on the page: 2026-07-24 Tecvayli).

### Public Summary SwissPAR (lay summaries) — separate, HTML not PDF
- **Index:** `https://www.swissmedic.ch/swissmedic/en/home/humanarzneimittel/authorisations/public-summary-swisspar.html` — **VERIFIED** HTTP 200, 214,445 bytes.
- **362 sub-page links**, and **zero PDF links** (VERIFIED) — these are **HTML pages**, not PDFs, under `/swissmedic/en/home/about-us/publications/public-summary-swiss-par/public-summary-swiss-par-{product}.html`.
- Sample verified: `.../public-summary-swiss-par-ezmekly.html` — **VERIFIED** HTTP 200, 47,748 bytes.

---

## 5. MAGHP — Marketing Authorisation for Global Health Products

- **Exact URL:** `https://www.swissmedic.ch/swissmedic/en/home/about-us/development-cooperation/marketing-authorisation-for-global-health-products.html` — **VERIFIED** (HTTP 200, 51,190 bytes). Note it lives under **about-us/development-cooperation**, *not* under human-medicines/authorisations — easy to miss.
- **What it is:** a Swissmedic authorisation track to accelerate access to therapeutic products in **low- and middle-income countries (World Bank definition)**, emphasis on **sub-Saharan Africa**. It builds on the normal Swiss MA procedure.
- **Eligibility:** new active substances, known active substances, and biosimilars addressing diseases disproportionately affecting the target regions. Example cited: a paediatric antimalarial.
- **Mechanics:** **National Regulatory Authorities (NRAs) of recipient countries participate actively in the assessment** (capacity building + confidence building). Optional pre-submission **scientific advice** meetings run jointly with other authorities and **the WHO**.
- **Guidance documents:**
  - `https://www.swissmedic.ch/dam/swissmedic/en/dokumente/stab/networking/maghp_procedure.pdf.download.pdf/maghp_procedure.pdf` — **VERIFIED** HTTP 200, 623,725 bytes, **PDF 1.7, 18 pages** (`ZL000_00_047e_WL`)
  - `https://www.swissmedic.ch/dam/swissmedic/en/dokumente/stab/networking/scientific_advicemeetingsmaghpprocedure.pdf.download.pdf/scientific_advicemeetingsmaghpprocedure.pdf` — UNVERIFIED (href confirmed in raw HTML; not downloaded)
  - `https://www.swissmedic.ch/dam/swissmedic/en/dokumente/stab/networking/Swissmedic_MAGHP_Procedure.pdf.download.pdf/Swissmedic_MAGHP_Procedure.pdf` — leaflet, 344 kB, 21.01.2021 — UNVERIFIED (href confirmed in raw HTML)
- **Relevance caveat:** MAGHP is a **global-health / LMIC access** instrument. It is **not** a rare-disease route and **not** a reliance shortcut into the Swiss market. **There is no published list of MAGHP-approved products** — approvals surface only as individual news items.

---

## 6. Reliance / foreign-decision procedures (found — directly relevant)

The extended list (§2a col G) **exposes reliance route as structured data**. Distribution across 11,066 rows (VERIFIED):

| Value | Rows |
|---|---|
| *(blank — ordinary full procedure)* | 10,947 |
| `Zul. nach Art. 14 Abs. 1 Bst. abis HMG: Zul. in EU / EFTA` | **113** |
| `Zul. nach Art. 14 Abs. 1 Bst. aquater HMG: Kant. Zulassung` | 4 |
| `Zul. nach Art. 14 Abs. 1 Bst. ater HMG: Langj. med. Verw. im Ausland` | **2** |

- `Bst. ater` = **"long-standing medical use abroad"** — this is the closest thing Switzerland has to a codified repurposing/well-established-use route, and only **2 products** currently carry it. That scarcity is itself a finding.
- `Bst. f` (Art. 14 Abs. 1 Bst. f HMG) is the **orphan drug** basis — cited in the orphan file header alongside Art. 4, 5, 24–26 VAZV.
- **Art. 13 TPA** (consideration of a foreign assessment) guidance page: `https://www.swissmedic.ch/swissmedic/en/home/humanarzneimittel/authorisations/information/anpassung-wl-ham-art-13.html` — **VERIFIED** HTTP 200, 44,130 bytes (guidance updated 01.03.2026).
- **International procedures hub:** `https://www.swissmedic.ch/swissmedic/en/home/humanarzneimittel/authorisations/internationale-zlverfahren-link.html` — **VERIFIED** HTTP 200, 48,555 bytes. Links (hrefs confirmed in fetched content, individual pages UNVERIFIED): Access Consortium, **Project Orbis** (`/swissmedic/en/home/about-us/international-collaboration/multilateral-co-operation-with-international-organisations---ini/project-orbis.html`), EMA OPEN, MAGHP.

---

## 7. Other machine-readable sources

### AIPS bulk XML — full label texts (SmPC + patient info)
- **URL:** `https://download.swissmedicinfo.ch/` — **VERIFIED** HTTP 200 (redirects http→https), 6,111 bytes.
- Operated by **Refdata**, not Swissmedic. Ships **the entire corpus of Fachinformation (SmPC) + Patienteninformation in XML**, explicitly "designed for data refiners."
- **Format change (VERIFIED from page text): from 28 August 2025 a new XML format** carries **URLs to the published HTML and PDF texts** rather than embedding everything. Technical contact: `partner@refdata.ch`.
- **Auth/gotcha:** no login for the third-party download, but there is a **click-through "Continue Download?" + Terms of use gate** — you must POST past the consent interstitial; a naive GET returns the landing page, not the data. Copyright asserted by Refdata (licensing diligence required before redistribution).
- The password-protected *upload* side (`simisinfo.ch`) is for MA holders only — not useful to you.
- Human-facing front-ends: `https://www.swissmedicinfo.ch` (patients), `https://www.swissmedicinfo-pro.ch/?Lang=EN` (professionals).

### New authorisations by year
- `https://www.swissmedic.ch/swissmedic/en/home/humanarzneimittel/authorisations/new-medicines.html` — **VERIFIED** HTTP 200, 122,245 bytes.
- Archive of Swissmedic Journal notices for **NAS (new active substance)** authorisations, chronological, includes products whose authorisation has since lapsed. **~75 per-product HTML sub-pages** at `/new-medicines/{slug}.html` (VERIFIED in raw HTML) — recent entries include Ezmekly, Agamree, Qalsody, Voxzogo, Filsuvez, Imcivree, Bylvay, Yorvipath (heavily rare-disease).
- Annual report page: `/swissmedic/en/home/humanarzneimittel/authorisations/new-medicines/zl-ham-nas-ie-2024.html` — UNVERIFIED (href confirmed in raw HTML).
- **HTML only — no XLSX/CSV/JSON export.** Scrape or use §1 instead.

### ATC list — **misleadingly named, probably not what you want**
- `https://www.swissmedic.ch/dam/swissmedic/en/dokumente/internetlisten/atc-liste.xlsx.download.xlsx/ATC-Liste.xlsx` — **VERIFIED** HTTP 200, 274,801 bytes, PK magic.
- Sheet `Zuteilung zu RA`, header row 6, **242 data rows, 8 columns**, `Stand 06.03.2026`.
- **GOTCHA:** this is **"Allocation of ATC code to Regulatory Assessment"** — it maps ATC groups to the **named Swissmedic reviewer** (`Regulatory Manager`, `Kurzzeichen RM`, `Regulatory Associate`, `RA Einheit`). It is an internal-workload directory, **not** a product↔ATC mapping and **not** an ATC dictionary.
- For an actual ATC dictionary use `OGD-ATC-Codes.XML` (2,219 codes, **English** descriptions, e.g. `A01A → STOMATOLOGICAL PREPARATIONS`). For product↔ATC use §2a col I or `PRAEPARAT/ATC_CODE`.

### Swissmedic Journal
- `https://www.swissmedic.ch/swissmedic/en/home/about-us/publications/swissmedic-journal.html`
- Monthly PDF, published mid-month, free. Contains authorisation announcements. **German and French only.** Archives grouped 2026 / 2021–2025 / 2011–2020 / 2002–2010.
- Sample verified: `https://www.swissmedic.ch/dam/swissmedic/en/dokumente/stab/journal/swissmedic-journal-2026-05.pdf.download.pdf/Swissmedic%20Journal%2005-2026_web.pdf` — **VERIFIED** HTTP 200, 735,898 bytes, valid PDF.

### opendata.swiss (metadata only)
- `https://opendata.swiss/api/3/action/package_show?id=daten-von-human-und-tierarzneimitteln` — **VERIFIED** HTTP 200.
- `accrualPeriodicity: MONTHLY`; `issued 2021-07-01`, `modified 2025-06-13`. **`license_title: None`** — no licence declared, which is a genuine legal gotcha for commercial redistribution. Resources = the OGD ZIP + the 4 description PDFs.
- The HTML dataset page returns **403 to WebFetch** — UNVERIFIED via browser fetch (fetch blocked — bot filtering on opendata.swiss HTML); the CKAN JSON API works fine with a browser UA.

---

## 8. Language matrix (explicit)

| Source | Language | Note |
|---|---|---|
| **SwissPAR PDFs** | **English only** | The only substantial native-English assessment content |
| Public Summary SwissPAR | English (EN pages exist) | DE/FR/IT parallel pages |
| OGD `User-Defined-Codes` | **DE/EN/FR/IT** | 1,929 EN rows — code labels translatable |
| OGD `ATC-Codes` | **English only** | Per the ER diagram: "ATC Codes nur in Englisch" |
| OGD `ANWENDUNGSGEBIET` (indication) | **German (mostly), some French** | Free text, source-language as filed |
| **All XLSX column headers** | **German + French only** | Bilingual in one cell, newline-separated |
| **XLSX cell values** (indications, substances) | **German/French/Latin** | **No English** |
| Swissmedic Journal | **German and French only** | No EN |
| New authorisations sub-pages | EN page chrome, **German product/form names** | Page states several docs are DE/FR only |
| MAGHP guidance | English | |

> **BIGGEST LANGUAGE TRAP (VERIFIED):** the `/en/`, `/de/`, `/fr/`, `/it/` segment in the `dam` URL is **purely cosmetic for the XLSX files**. I downloaded the orphan list from all four language paths — all returned **345,547 bytes with identical MD5 `da57a62ad3cc70d26c390fc95495cac1`**. Fetching the `/en/` URL does **not** get you an English file. Every list is DE/FR regardless of path.

---

## 9. Consolidated gotchas

1. **`dam.swissmedic.ch` does not exist** (DNS failure). Use `www.swissmedic.ch/dam/...`. Same trap with `ogd.swissmedic.ch` (in the XML `schemaLocation`) vs. the live `ogd.swissmedic.cloud`.
2. **Archive ZIPs are lowercase `.zip`**, contradicting Swissmedic's own documentation which says `.ZIP`. Uppercase → 404.
3. **`202505` snapshot is missing** from the archive — 53 files, not 54.
4. **XLSX row grain = dosage strength, not product.** 11,066 rows ↔ 6,762 authorisation numbers. Orphan file grain is (substance × indication × auth-no).
5. **Header rows are not row 1.** Extended/basic HAM = row 7; orphan = row 4; ATC = row 6. Rows above hold title + `Stand` date. Naive `pandas.read_excel` mangles all of them — pass `skiprows`.
6. **Headers are bilingual inside a single cell**, newline-separated (`"Zulassungs-\nnummer\n\nN° d'autorisation"`), with soft hyphens breaking words. Normalise whitespace before column matching.
7. **Orphan status exists in exactly one place** — the XLSX. Not in OGD XML, not in the extended list. Join on `Zulassungsnummer`, and expect 265 orphan rows with no authorisation number at all.
8. **`ATC-Liste.xlsx` is a reviewer-assignment roster, not ATC product data.**
9. **`Verfahren.xlsx` (Stand 2020-09-01) and `Gesuchseingaenge` (filename 2021) are stale/abandoned.**
10. **No licence declared** on the opendata.swiss record (`license_title: None`) — clear this before commercial redistribution. AIPS/Refdata separately asserts copyright.
11. **AIPS bulk download sits behind a click-through T&C interstitial** and changed XML format on 2025-08-28.
12. **Update timing:** OGD ZIP regenerates on the **1st of the month** reflecting the **last day of the prior month**; XLSX lists showed `Stand 31.07.2026` on 2026-08-05. Poll on ~the 2nd–3rd; use `last-modified`/`etag` (both served on the OGD ZIP) for cheap change detection.

---

## 10. Recommended ingestion design

- **Backbone:** `OGD.zip` monthly + backfill all 53 archive snapshots → relational store keyed on `(ZULASSUNGSNUMMER, SEQUENZNUMMER)`. Gives products, dose strengths, packs, full composition, ATC, MA holders, routes, substance synonyms, with EN code labels. Diff consecutive snapshots to derive authorisation/withdrawal/indication-change events — this is your only route to a change feed.
- **Overlay 1 — orphan:** monthly `Liste_OrphanDrug_Internet.xlsx`, join on `Zulassungsnummer`. Keep the 265 unauthorised designations as a separate entity (designation ≠ product). Track col 5 for withdrawals and col 3-vs-11 divergence for designated-vs-authorised indication drift.
- **Overlay 2 — reliance:** `erweiterte_ham_ind.xlsx` col G for Art. 14 route, col Y for time-limited indications, and `unterlagenschutz.xlsx` for data-exclusivity expiry.
- **Overlay 3 — narrative:** SwissPAR index → 388 PDFs, English, filename-parseable for auth-no/sequence/date. Sequence `02+` = indication extension, the highest-value repurposing precedent signal.
- **Optional:** AIPS XML for full SmPC text (clear licensing first).
- **Do not** build against `zugelassene_arzneimittel_ham_ind.xlsx` (strict subset), `ATC-Liste.xlsx` (wrong content), or expect an API.