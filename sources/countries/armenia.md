# Armenia — Pharmaceutical Registration Pathways

*Researched 2026-08-05. VERIFIED = URL fetched and content read. UNVERIFIED = referenced but not confirmed.*

## Headline finding

**Armenia's purely national registration route legally closed on 1 July 2021, and the window to convert existing national marketing authorisations to EAEU dossiers closed on 31 December 2025 — that date has passed.** Both dates verified from the consolidated text of EEC Council Decision No. 78 (as amended through Decision No. 93 of 26 Nov 2025). See §7 for the nuance that makes this less fatal than it sounds.

---

## 1. The regulator — SCDMTE

| Item | Value | Status |
|---|---|---|
| Name on own contacts page | **"CENTRE OF DRUG AND MEDICAL TECHNOLOGY EXPERTISE" SNCO** | VERIFIED |
| Legal form | **ՊՈԱԿ = SNCO (State Non-Commercial Organisation)** | VERIFIED |
| Director | **Arayik Baghryan** | VERIFIED |
| Address | **49/5 Komitas Ave., Yerevan 0051, Republic of Armenia** | VERIFIED |
| Phone | **+374 60 83-00-73** | VERIFIED |
| Email | **info@ampra.am** (JS-obfuscated on page; decoded from source) | VERIFIED (decoded) |
| Founded | 1992, accountable to the Ministry of Health | VERIFIED |

**Correction to common secondary sources:** it is an SNCO, *not* a CJSC/ՓԲԸ. Consultancies (Cratia et al.) describe it as "JSC/CJSC" — that conflicts with the Centre's own 2024 order and its contacts page.

**Oddity:** the contact email domain is **ampra.am**, not pharm.am. `ampra.am` resolves (83.139.3.43) on government nameservers ns.gov.am with MX `mail.ampra.am`, but **ports 80/443 are closed — there is no website**. Looks like a renamed agency whose web presence has not launched. What AMPRA stands for is UNVERIFIED.

**Ministry of Health** is the "Authorized Body" under the Law. Per Article 6 it performs state registration, issues certificates, maintains the register, and licenses. **The Minister's individual order is the legal act that registers a medicine.** SCDMTE is the expert/assessment organisation; the Pharmacological Council of the MoH issues recommend/do-not-recommend opinions. Registration orders are issued continuously — most recent seen: **N 4378-A of 29.07.2026**. Armenia is actively registering medicines right now.

- `moh.am` — VERIFIED (200). `www.moh.am/en` → **404** (no English path there).

---

## 2. The law

**RA Law "On Medicinal Products" / «Դեղերի մասին», adopted 17 May 2016.** VERIFIED (full English text). Law number UNVERIFIED — do **not** cite "HO-172", that number belongs to something else.

Key articles (all VERIFIED from the English text):

- **Art. 16(3)** — two routes: **general** and **simplified**. Simplified applies to medicines registered in a member state of "the international professional organization defined by a decree of the RA Government", **or WHO-prequalified**.
- **Art. 16(9)** — applicant = manufacturer or another entrepreneur/legal entity responsible for the product; becomes the certificate holder.
- **Art. 16(13)** — timelines (see §4).
- **Art. 16(15)** — **generic data waivers (critical — see §5).**
- **Art. 16(17)** — pre-registration inspection possible; applicant pays; recognition of foreign inspection reports per Government procedure.
- **Art. 16(18)** — **5-year registration term**; SmPC + PIL **in Armenian** attached to the certificate; register must be public.
- **Art. 16(21)** — state duty per the RA Law on State Duty.
- **Art. 16(26)** — enables **recognition of registrations** from those countries by agreement.
- **Art. 16(27)(8)** — refusal if the product is **not registered in the applicant's own country**, *except* for medicines registered in an ICH member state.
- **Art. 20(3)** — retail medicines must have an **Armenian-language insert**.

### The "international professional organization" = **ICH**

VERIFIED twice over:
1. **Government Decision N 162-N, point 11**: *"Simplified procedure for registration of medicine shall be applied to the medicines registered (undergone expert-examination) in a member state of the **ICH** or pre-qualified by the World Health Organisation."*
2. The State Duty law refers to "the competent authority of an **ICH** member country."

Governing instrument: **Government Decree N 172-A of 23 February 2017**. The pharm.am page for it exists but **its body is empty and it carries no attachment — decree text NOT obtained. UNVERIFIED.**

⚠️ **Honest caveat on scope:** the legal text says "member state of the **ICH**" — it does **not** enumerate FDA/EMA/PMDA. Consultancy sites gloss this as "EU, USA, Japan" (the ICH founding regulatory members). ICH today has many more regulatory members (Health Canada, Swissmedic, MHRA, TGA, MFDS, NMPA, ANVISA, Türkiye, Singapore, Saudi FDA). **Whether SCDMTE applies the narrow founders list or full current ICH membership is not publicly documented.** Point 11 was also amended by Decision N 1873-N of 28 Nov 2024, content not retrieved. **This is the single highest-value question to put to SCDMTE in writing.** PMDA/FDA/EC are safe on any reading; TGA, Swissmedic, MHRA, Health Canada are the uncertain band; **WHO-PQ is independently and explicitly named in the statute, so it is safe.**

---

## 3. Governing secondary legislation

- **Government Decision N 162-N of 28 Feb 2019** — the operative registration rules. **English text VERIFIED** (36 pp). Annexes: 1 registration procedure, 2 expert-examination procedure, 3 required document list, 4 no-new-registration variations, 5 recognition of foreign inspection reports. Amended by N 1873-N of 28 Nov 2024.
- **MoH Order N 31-N of 10 June 2019** — certificate form, register structure/rules, Rx/OTC classification.
- **Government Decision N 202-N of 28 Feb 2019** — import/export of medicines, substances, IMPs.
- **Government Decision N 164-N of 28 Feb 2019** — rapid alert, recall, unregistered/falsified products.
- **Government Decision N 734-N of 28 May 2011** — GMP implementation schedule.

---

## 4. Pathways and timelines

### National routes (Law Art. 16(13) + Decision 162-N §§19–21, 35) — all VERIFIED

| Route | Total | Of which expert examination |
|---|---|---|
| **General procedure** | **150 calendar days** | 140 calendar days |
| **Simplified** (ICH member state registration or WHO-PQ) | **31 calendar days** | **21 calendar days** |
| **Re-registration** (5-yr renewal) | 31 calendar days | 21 calendar days |
| **Certificate term extension** | **10 calendar days** | — |

- **+10 calendar days** if the applicant supplements documents mid-review.
- **Clock stops:** time spent answering deficiency requests is **excluded** (Decision 162-N §22). 31 days is the *regulator's* clock, not elapsed time.
- **Simplified mechanics (§§19, 36–37):** a **comparative review** of the Reference Competent Authority's assessment report against your dossier — composition, specs/quality ND, manufacturing sites, research data, product information. **No laboratory testing of samples.** If composition, site, stability, specs or product information are **inconsistent** with the reference approval, you are notified and — with consent and further payment — **converted to the general procedure**. Perfect alignment with the reference dossier is the whole game.
- Registration validity **5 years**, renewable.
- Armenian SmPC/PIL are **drafted by the Centre during assessment** (Decision 162-N §38).

### EAEU routes (Decision 78) — all VERIFIED

| Procedure | Timeline |
|---|---|
| **Reference State** registration + expertise (§46) | **≤ 140 working days** |
| **Mutual Recognition** in each Recognition State (§69) | **≤ 40 working days** from access to assessment report |
| **Decentralised (DCP)** (§84) | ≤ 140 working days reference + ≤ 50 working days recognition |
| Applicant response window | up to 90 working days (§72), **excluded** from the clock |

**Armenia can be either Reference State or Recognition State** — Decision 78 §23: *"The applicant independently chooses the reference state and, if necessary, the recognition state."*

🔑 **Key structural insight (Decision 78 §21(a), VERIFIED):** Mutual Recognition is performed *"by the reference state under these Rules for the purpose of circulation of the medicinal product on the market of **only that state** — **(national registration procedure)**."* **An EAEU MRP filing naming Armenia as sole Reference State with no Recognition States IS the modern national registration.** You have not lost a national route — it has been re-plumbed through EAEU rules, and you can later bolt on Russia/Belarus/Kazakhstan/Kyrgyzstan via MRP without redoing the science.

---

## 5. Generic / repurposing data waivers — the commercially decisive provisions

**Law Art. 16(15), VERIFIED verbatim.** Two distinct waivers:

1. **No preclinical / clinical data required** if you show the product is reproduced from an originator registered in **Armenia or an ICH member state for at least 8 years**.
2. **No bioequivalence data required** if documents confirm the product has been **used in Armenia or an ICH member state for more than 10 years** — *"In such case, the applicant shall submit only appropriate data from the scientific literature."*

That second limb is a genuine **bibliographic / well-established-use pathway** and is close to ideal for off-patent repurposing. Mirrored in the dossier structure: **CTD Module 1.5.1 "Information for Bibliographical Applications"** (VERIFIED).

Art. 16(15) also contains **10-year market protection** for the originator, **extendable by up to 10 further years if the certificate holder registers new indications** during that period. Diligence this before filing against a recently-repurposed originator.

The EAEU fee law has a dedicated category — **"reproduced medicine with well-established medical use"** — priced materially below ordinary generics. That category exists only in the EAEU fee lines, not the national general/simplified lines.

**New indication:** registering a new indication costs a flat **400,000 AMD** — the single most relevant line item for a repurposing business.

---

## 6. Fees — full statutory schedule

**Legal basis:** RA Law "On State Duty" (**ՀՕ-186 of 27 Dec 1997**), **new Article 20.3**, inserted by the amending law adopted 11 April 2024. VERIFIED from consolidated official text on arlis.am.

**Base duty = 1,000 AMD.** All figures below = multiplier × 1,000 AMD.

### 20.3(1)(1) — Generic, or hybrid not differing in API/strength/dosage form
*(charged for first dosage form/strength/route AND each subsequent one)*

| Action | AMD |
|---|---|
| General procedure, **or** EAEU registration for Armenia-only use | **1,100,000** |
| **Simplified procedure** | **500,000** |
| Re-registration / certificate extension (Armenia-only) | 500,000 |
| EAEU registration — **Reference State** | 2,100,000 |
| EAEU DCP or MRP — **Recognition State** | 1,500,000 |
| Bring Armenian dossier into EAEU conformity (reference) or MR | 1,200,000 |
| Bring dossier into EAEU conformity, Armenia-only use | 900,000 |
| EAEU re-registration | 1,000,000 |
| **Maintaining EAEU registration — ANNUAL** | **100,000/yr** |
| Re-expertise for other states' mutual recognition | 1,000,000 |

### 20.3(1)(2) — Generic with **well-established medical use** (EAEU lines only)

| Action | AMD |
|---|---|
| EAEU registration, Armenia-only use | **800,000** |
| EAEU — Reference State | 1,500,000 |
| EAEU DCP/MRP — Recognition State | 1,000,000 |
| EAEU re-registration | 500,000 |
| Annual maintenance | 100,000/yr |
| Re-expertise for mutual recognition | 700,000 |

### 20.3(1)(3) — Original, immunological, or new combination
General / EAEU-Armenia-only **2,400,000** · Simplified **1,000,000** · Re-reg 1,000,000 · EAEU Reference 3,500,000 · EAEU Recognition 2,500,000 · Conformity (ref)/MR 2,100,000 · Conformity Armenia-only 1,400,000 · EAEU re-reg 1,500,000 · Annual 200,000 · Re-expertise 1,100,000

### 20.3(1)(4) — Biosimilar, blood-derived, radiopharmaceutical, hybrid
2,100,000 / 900,000 / 900,000 / 3,100,000 / 2,200,000 / 2,000,000 / 1,400,000 / 1,500,000 / 200,000 / 1,000,000 (same column order)

### 20.3(1)(6)–(9) — Herbal / homeopathic
Herbal: 800,000 general · 500,000 simplified · 1,500,000 EAEU ref · 1,000,000 EAEU recog · 100,000/yr. Herbal raw material: 250,000 / 250,000 / 500,000 / 50,000/yr. Homeopathic: 800,000 / 500,000. Homeopathic without indications: 400,000 / 250,000.

### Line extensions and variations

| Item | AMD |
|---|---|
| Each subsequent pack/release form, **same** primary pack | 50,000 |
| Each subsequent pack/release form, **different** primary pack | 200,000 |
| **Each subsequent manufacturing site OR NEW INDICATION** | **400,000** |
| Variation **Type IA / IB**, national or EAEU-Armenia-only | 60,000 each |
| Variation IA/IB, simplified-registered product | 60,000 |
| Variation IA/IB, EAEU Reference State | 100,000 |
| Variation IA/IB, EAEU Recognition State | 50,000 |
| **Notification of a change not requiring expertise** | **5,000** |
| **Type II** variation, national/EAEU-Armenia-only | 300,000 |
| Type II, simplified-registered | 150,000 |
| Type II, EAEU Reference | 700,000 |
| Type II, EAEU Recognition | 350,000 |
| Lab expertise, ≤3 specification parameters changed | 300,000 |
| Lab expertise, >3 parameters | 500,000 |

### Import/export, licences, clinical trials
Import documentary expertise 10,000 (1–5 names) / 20,000 (6–20) / 1,000 per name (21+) · Sampling 12,000/20,000/1,000 · Registration-status check 12,000/20,000/1,000 · **Lab expertise of a medicine/IMP 300,000** · Lab expertise of substance 100,000 · Export permit 1,000/name · **Manufacturing licence expertise 280,000** · **Wholesale licence expertise 140,000** · **Clinical trial authorisation 500,000** · **BE study, or post-registration CT of an Armenia-registered drug, or a CT of a drug already authorised for CT/compassionate use by an ICH-member authority: 250,000** · CT document changes 100,000/change · IMP safety monitoring 100,000/yr · Advertising permit 10,000/material · GLP certificate 30,000

### SCDMTE's own paid services (separate from state duty)
**Order N 111-A-24 of 30 April 2024**, Annex 1, AMD incl. VAT. Later amendments: N 74-25-A (26.02.2025), N 105-25-L (13.03.2025), N 231-25-A (22.05.2025), **N 60-26-L (10.02.2026 — most recent)**. All PDFs are scanned Armenian images.

- Registration/expertise status info per INN — 3,000
- **Risk Management Plan agreement — 160,000**
- **Safety report assessment — 120,000**
- Preliminary expertise of registration-sample conformity for import — 24,000
- **Certificate of Pharmaceutical Product (CPP) issuance — 20,000**
- **Reference drug approval — 50,000**
- Annual list of RA-registered drugs/devices, electronic — 1,000
- Archival information, electronic, per INN — 30,000
- Other services — by contract

⚠️ **The 10.02.2026 order (N 60-26-L) is a scanned image with no text layer; figures above are the 2024 base list and may be superseded. UNVERIFIED for 2026.** Request current price list from info@ampra.am.

**Not obtained:** MoH Order N 189-A of 06.02.2014 (GMP inspection fee) — no amount. GMP and pre-registration inspection costs are explicitly **by contract**, so no fixed published figure should be expected.

Bank details: `pharm.am/attachments/article/8786/Bank details 3125.docx` — VERIFIED.

---

## 7. EAEU — current state as of 2026

**Primary source:** consolidated text of **EEC Council Decision No. 78 of 3 Nov 2016**, as amended through **Decision No. 93 of 26 Nov 2025**, published by pharm.am as `Degree_78_26.12.2025.pdf` (1,091 pages, Russian). **VERIFIED.** Amendment chain: N55 (2018), N9, N128 (2020), N14, N34 (2021), N36, N141 (2022), N60, N114 (2023), N43, N117 (2024), N12, **N34 (22.05.2025)**, **N77 (12.09.2025)**, **N93 (26.11.2025)**.

### The actual deadlines — Decision 78, point 2 (VERIFIED verbatim)
- **2(b):** Until **1 July 2021** (Russia: 31 Dec 2020) an applicant could choose EAEU Rules or member-state law. → **Armenia's national registration route closed 1 July 2021.**
- **2(c):** MAs applied for nationally before 1 July 2021 could be extended under national law **only until 31 December 2025**.
- **2(d):** Nationally registered medicines **had to be brought into conformity with EAEU law by 31 December 2025** via the Section XIII procedure.
- **§170:** *"The application for bringing the registration dossier … into conformity with Union requirements must be submitted to the authorised body of the **reference state before 31 December 2025**."*

### What Decision No. 34 of 22 May 2025 actually did
Widely misreported as an extension. **It did not extend the 31 Dec 2025 filing deadline.** It created a grace mechanism for those who filed in time:
- Conformity application filed by 31 Dec 2025 but procedure unfinished → national MA **extended for the duration of the procedure, up to 3 years in each declared member state**, plus up to 2 further years from recognition-state filing.
- Conformity procedure completed before 31 Dec 2025 → MAs in recognition states extended for procedure duration, **max 2 years from 31 December 2025**.
- **§164 as amended:** third-country-manufactured product imported during MA validity with **no** conformity application **may still be sold after 31 Dec 2025 under that member state's own legislation** — sell-through of existing stock only.

⚠️ **Do not confuse with medical devices.** The widely-cited EEC news item *"Possibility to register medical products according to national rules extended"* (14 Feb 2023, extending to 31 Dec 2025) is about **MEDICAL DEVICES, not medicines**. VERIFIED by fetching it. Several consultancy blogs blend the two.

### Does Armenia still accept national-only applications in 2026?

**Legally: no.** But the Armenian domestic instruments still contain the national procedures and are not dead letters: Art. 16 general/simplified stands; Decision 162-N was amended as recently as 28 Nov 2024 and still describes them; and the **April 2024** State Duty law created *new* fee lines for "general procedure" and "simplified procedure" — legislating fees in 2024 for a route supposedly closed in 2021.

The reconciliation is almost certainly Decision 78 **§21(a)**: single-reference-state MRP *is* the national procedure, and the Armenian fee law prices *"general procedure **or** EAEU-rules registration for Armenia-only use"* **at the same rate on the same line**.

⚠️ **UNVERIFIED whether SCDMTE today accepts a filing labelled "simplified national procedure" (31 days, 500,000 AMD) or whether every new file must be styled as an EAEU submission. This must be confirmed with SCDMTE.** Second highest-value question — simplified national at 500,000 AMD / 31 days versus EAEU reference-state at 2,100,000 AMD / 140 working days is a ~4× cost and ~4× time difference.

### EAEU registers

| Register | URL | Status |
|---|---|---|
| EEC databases index | `https://eec.eaeunion.org/comission/department/deptexreg/BD.php` | **VERIFIED** |
| **Unified Register of Registered Medicinal Products** | `https://portal.eaeunion.org/sites/odata/_layouts/15/registry/pmm01/tableview.aspx?filter=…` | **UNVERIFIED — 404.** EEC's own link is truncated mid-query-string in its HTML; all variants 404 |
| Unified register of **medical devices** (PMM06) | `https://portal.eaeunion.org/sites/odata/_layouts/15/Registry/PMM06/TableView.aspx` | **VERIFIED** (200) |
| PMM02/03/04/05/09 | same pattern | **UNVERIFIED — all 404** |
| EAEU legal portal | `https://docs.eaeunion.org/` | **VERIFIED** |
| EAEU Agreement on medicines (23 Dec 2014) | `https://docs.eaeunion.org/docs/ru-ru/0147061/itia_24122014` | **VERIFIED** (English, 13 pp) |

Agreement **Article 20** verbatim: *"Medicinal products registered in the Member States before the entry into force of this Agreement shall be brought into compliance with the requirements and regulations of the Union **before 31 December 2025**."*

---

## 8. Public register of medicines — there are TWO

### (a) Searchable register — **pharm.cals.am**

**`http://pharm.cals.am/pharm/drug_images/index.php` — VERIFIED, HTTP 200.**
Found via the EEC's own page listing member-state registers, where it is the **official Armenian entry**: `https://eec.eaeunion.org/comission/department/deptexreg/formirovanie-obshchikh-rynkov/drug-registry-eaeu.php` — VERIFIED.

- **Searchable by:** Trade name · Generic name · Country · Manufacturer · **ATC code**
- **Languages:** English and Հայերեն; records stored bilingually
- **Tested live:** `GET /pharm/drug_images/drug_search_view.php?p_text1=metformin&search_in=2` returned **111 KB / 78 records**, `****`-delimited, `#$`-delimited fields
- **Fields:** trade name, INN, dosage form, strength & pack, country, manufacturer (full address, with role tags like *batch releaser / bulk manufacturer, packager, quality control*), Armenian equivalents, **registration number**, status, registration date, expiry, **ATC code**, **registration category** (e.g. *"generic, first dosage form and strength"*), **GMP standard (e.g. `PIC/S`)**, validity/extension dates
- Minimum 3 characters per query
- **Effectively a scrapeable API** — highly usable for competitive/whitespace analysis

### (b) Downloadable full register — pharm.am

- Landing: `https://www.pharm.am/index.php/en/register-of-medicines` — VERIFIED
- File: `https://www.pharm.am/attachments/article/2966/Registereng_total_up_to_30.06.26.pdf` — VERIFIED, **5.2 MB, 539 pages, English**
- Columns: trade name · INN · drug form · dose & packaging · manufacturer · country · ATC code · registration number · term of registration · legal status for supply (PoM/OTC) · **MA holder with address**
- Text-extractable. **Filename encodes the cut-off date — link from the landing page, don't hardcode.**

**Sub-lists (all VERIFIED as existing URLs):** non-prescription · prescription · controlled · Armenian-made · **rejections** (`/rejection-for-registration`) · withdrawals · Pharmacological Council recommended/not-recommended · MoH registration orders.

**Dead links in the site's own menu (404):** `/en/registered-medicenes` (sic), `/en/registration-statistics`, `/en/state-duty-of-medicines-registration`.

Open-data mirror (not fetched): `https://data.opendata.am/dataset/scientific-centre-of-drug-and-medical-technology-expertise-medicines-data` — UNVERIFIED.

---

## 9. GMP

- **Armenia is NOT a PIC/S member, applicant, or pre-applicant.** VERIFIED by fetching `https://picscheme.org/en/members` — 58 participating authorities, Armenia absent.
- **SCDMTE does its own inspections.** Good Practice (GMP/GDP) Inspection Department; MoH issues GMP certificates; site publishes an inspection plan per EAEU GMP guideline 2024/2025, contract templates, and a list of GMP-certified manufacturers. Real-world proof of active foreign-site inspection: **MoH Orders N 2411-A and N 2412-A of 29 April 2026 refusing GMP certificates to "Laboratorios Atrall S.A." (Portugal) and "SENEXI" (France).** **Armenia does inspect and does refuse.**
- **Recognition of foreign GMP inspections — Decision 162-N, Annex 5 §11, VERIFIED verbatim:** positive GMP inspection results by competent authorities of **PIC/S member states and EAEU member states within the previous 3 years are RECOGNISED and no Armenian inspection is conducted** — unless the assessment reveals inconsistencies.
- **Annex 5 §12:** for preclinical, clinical and bioequivalence sites, positive observations from **WHO prequalification, ICH and EAEU** member state authorities are likewise recognised.
- **Annex 5 §7:** in non-high-risk cases, inspection may be deferred to within 3 years after registration.
- **§10:** site monitoring within 30 calendar days of notifying the applicant; max 5 working days on site.
- **§4:** applicant pays, by contract.

**Practical read: a PIC/S-member GMP certificate (EU GMP, FDA, MHRA, Health Canada, TGA, Swissmedic) less than 3 years old should avoid an Armenian inspection.** The recognition list here is **PIC/S + EAEU** — *broader* than the ICH list used for simplified registration. **FDA is a PIC/S participating authority**, so US sites qualify.

⚠️ **EAEU-specific caveat: under EAEU Rules, third-country manufacturing sites generally need an EAEU GMP certificate issued by an EAEU inspectorate. Search of Decision 78 returned no hits, so NOT confirmed from primary text. UNVERIFIED — treat as an open risk.** Well-known cost/time driver in EAEU filings; do not assume it away.

---

## 10. Filing format and mechanics

- **Format: EU-style CTD, Modules 1–5.** Guidance cites `https://www.ich.org/products/ctd.html` and the EU Notice to Applicants. VERIFIED: `https://www.pharm.am/attachments/article/4781/Registration dossier presentation and format_CTD_eng.pdf`
- **NOT eCTD.** Instruction: *"Provide Modules 2–5 with an electronic carrier (storage device), each module in a separate folder … Submit electronic versions in **PDF format (with content search feature)**."* SmPC/labelling/PIL in **Microsoft Word**; mock-ups in PDF. **CTD-on-physical-media, not eCTD.**
- Module 1 notables: **1.3.1.1** Armenian translation of SmPC and PIL (*"if available"*) · **1.3.5** product information approved in other countries (*"applicable only to the national standard registration procedure"*) · **1.5.1 Bibliographical applications** · 1.5.2 Generic/Hybrid/Biosimilar · 1.5.3 Data/Market Exclusivity · 1.5.4 Exceptional Circumstances · 1.5.5 Conditional MA · **1.7 Orphan Market Exclusivity** · 1.8 Pharmacovigilance system + RMP.
- **Submission channels — Decision 162-N §14, VERIFIED:** *"in person and (or) by **e-mail** and (or) through an **electronic system** and (or) by **postal delivery**."*
- **Where:** SCDMTE, 49/5 Komitas Ave., Yerevan 0051. Out-of-hours submissions count as next working day (§16).
- **Forms:** `Application_Final_eng_HUM_VET_1.docx` plus Appendices 1–3 in English and bilingual DOCX. Variation, re-registration dossier formats separately published. EAEU-format forms under `/index.php/en/the-eaeu-rules-of-medicines-registration-and-assessments`.

---

## 11. Local representative / MAH

**There is NO statutory requirement for the applicant or MAH to be an Armenian legal entity.**

- **Law Art. 16(9):** applicant may be the manufacturer or another entrepreneur/legal entity responsible for the product. No nationality or residency qualifier.
- **Empirical proof from the register:** "License holder" column shows foreign MAHs, e.g. *"Eli Lilly Regional Operations GmbH, Koelblgasse 8-10, 1030, Vienna, Austria."*
- **EAEU Decision 78 definitions:** "marketing authorisation holder" and "applicant" are both simply **"legal entity"** — no establishment requirement.

**In practice you will need an authorised representative to file, and PoA requirements are strict** — `https://www.pharm.am/attachments/article/4810/PoA-requirements_eng_1.pdf` VERIFIED:
- Written, **notarially certified**; copies and translations also notarially certified
- From Hague Convention states: **apostille required**
- **Maximum validity 3 years** (longer stated term cut to 3; no term stated → 1 year)
- Must name authorizer and authorised person with passport data/legal address, date of issue (undated = void), the right to complete the registration application, **explicitly which state bodies and which region**, **whether it covers all products or one specific product**, and **explicitly the right to pay the state duty**
- Must state whether sub-delegation is permitted

⚠️ The PoA rules do not state the representative must be Armenian-registered. **UNVERIFIED whether SCDMTE accepts a non-Armenian agent in practice** — but the requirement to specify region/state bodies plus the practical need for someone to pay duties and receive correspondence means an Armenian agent is the realistic route.

**Separate and mandatory:** importation and wholesale require **Armenian licences** (manufacturing licence expertise 280,000 AMD; **wholesale licence expertise 140,000 AMD**) — you need a licensed Armenian importer/wholesaler regardless of where the MAH sits.

---

## 12. Gotchas

- **Armenian language.** SmPC + PIL in Armenian are attached to the certificate and are the legal reference (Art. 16(18)). Retail products must carry an Armenian insert (Art. 20(3)). **Mitigation:** the Centre drafts the Armenian SmPC/PIL during assessment (§38), and **absence of an Armenian insert at the moment of import is expressly NOT a ground to refuse import** (Art. 21(9)). Import *is* refused if packaging language is not among accepted languages (Art. 21(8)(15)).
- **Marketing prohibition:** forbidden to put the Armenian supplier's name or trademark on marking, SmPC or PIL (Art. 20(4)).
- **Registration granularity drives cost.** Art. 16(5): separate registration for **every name, ingredient, strength, dosage form, presentation, new indication, manufacturer (including every performer of the production process), and certificate holder.** Fees charged per first *and* per each subsequent dosage form/strength/route. Same primary pack = 50,000/pack; different primary pack = 200,000/pack.
- **Pricing / reimbursement.** Art. 10 and Art. 11 (State Regulation of Prices of Reimbursed Medicinal Products) — Art. 11's entry into force was **deferred**. **Reimbursement/pricing mechanics NOT researched — UNVERIFIED.**
- **Orphan drugs: there is NO orphan designation regime in the Law.** Searched the full English text for "orphan" and "rare disease" — **zero hits. VERIFIED absence.** Nearest analogues:
  - **Art. 16(11):** expert examination for medicines with **low demand but of major therapeutic and public-health interest, intended for serious or life-threatening diseases**, may be performed **under a government order** (state-funded assessment). There is a live page `/list-of-medicines-liable-to-registration-within-the-framework-of-the-government-orders`. **For a rare-disease company this is the provision to lean on — it can take the assessment cost off you entirely.**
  - **Art. 16(26):** agreements with ICH member states may allow **direct recognition**; *"the Authorized Body may address applicants at its initiative and with its own resources"* to get needed medicines registered.
  - CTD Module 1.7 Orphan Market Exclusivity exists but is inherited from the EU Notice to Applicants and does **not** evidence an Armenian orphan regime.
- **Unregistered / named-patient import.** **Art. 16(23)(4):** registration is **not required** for medicines *"used with a **special permission of the Authorized Body**"*, nor for research/clinical trials, registration samples, or exhibition samples. Detailed procedure is in Government Decision N 202-N of 28 Feb 2019 — **NOT opened; mechanics, evidence requirements and timelines UNVERIFIED.**
- **Parallel imports permitted** under a Government-defined permission procedure (Art. 21(10)–(11)); refused if manufacturer or country of production differs from what is registered.
- **Rx/OTC status fixed at registration** (Art. 16(24)) against ten statutory criteria.
- **Six-month abandonment rule:** requested supplementary materials not filed within **6 months** → examination terminates, application rejected (Art. 16(16)).
- **Underpaid duty:** shortfall payable within **5 days** of notice.
- **Technical gotcha for tooling:** **pharm.am serves an incomplete TLS chain** (missing intermediate; GoGetSSL RSA DV SSL CA 2). Standard fetchers fail with *"unable to verify the first certificate."* The site is fine — you need a client that tolerates the incomplete chain or supplies the intermediate. This is why several tools report pharm.am as "down."

---

## 13. Strategic read for an off-patent repurposing play

1. **Best-case route is simplified procedure at 31 calendar days / 500,000 AMD for a generic** — *if* still accepted (§7) and *if* your reference approval is from a qualifying ICH member state or WHO-PQ. Confirm both in writing before modelling anything.
2. **Art. 16(15) limb two is the crown jewel**: >10 years of use in Armenia or an ICH member state ⇒ **no bioequivalence study**, literature only. Combined with the EAEU "well-established medical use" fee category (800,000 AMD Armenia-only), one of the cheapest legitimate routes to a marketing authorisation anywhere.
3. **New indications cost a flat 400,000 AMD.** That is the core repurposing transaction and it is cheap.
4. **Watch the 10(+10)-year originator protection in Art. 16(15)** — triggered and *extended* by the originator registering new indications.
5. **Armenia as EAEU Reference State is a strategic asset.** Register once (cheapest EAEU reference-state fees of any member: 2,100,000 AMD generic, 1,500,000 well-established use), then extend by MRP into Russia/Belarus/Kazakhstan/Kyrgyzstan at ≤40 working days each. Budget **100,000 AMD/year** maintenance per registration.
6. **Bring a PIC/S-member GMP certificate less than 3 years old** — should eliminate an Armenian site inspection outright.
7. **Explore Art. 16(11) government-order status early.** For a serious/life-threatening rare disease with low demand, the state may fund the assessment. A legislated subsidy for exactly this business model, with a published list to get onto.

---

## 14. Questions to put to SCDMTE (info@ampra.am / +374 60 83-00-73)

1. **Which specific ICH member authorities** qualify for the simplified procedure — full current ICH regulatory membership, or only EU/US/Japan? And what did **Decision N 1873-N of 28.11.2024** change in point 11 of Decision 162-N?
2. **Is a national general/simplified registration application still accepted in 2026**, or must every new application be filed under EAEU rules?
3. **Current SCDMTE paid-services price list** — machine-readable text of **Order N 60-26-L of 10.02.2026**.
4. **GMP inspection fee** (Order N 189-A of 06.02.2014) and current pre-registration inspection contract rates.
5. Confirmation that a **non-Armenian entity may act as authorised representative**.
6. Whether a **PIC/S-member GMP certificate** alone suffices, and whether an **EAEU GMP certificate** is separately required for third-country sites.
7. Route into the **Art. 16(11) government-order** list for low-demand, life-threatening-disease medicines.
8. The **named-patient / special-permission import** procedure under Decision N 202-N.
9. A copy of **Government Decree N 172-A of 23.02.2017** (its webpage is empty).

---

## 15. URL ledger

### VERIFIED
```
https://pharm.am/                                                        200
https://www.pharm.am/index.php/en/                                       200
https://www.pharm.am/index.php/en/contacts                               200  (email decoded: info@ampra.am)
https://www.pharm.am/index.php/en/sm                                     200  (full sitemap)
https://www.pharm.am/index.php/en/register-of-medicines                  200  <- register landing
https://www.pharm.am/attachments/article/2966/Registereng_total_up_to_30.06.26.pdf   200  5.2MB/539pp EN
http://pharm.cals.am/pharm/drug_images/index.php                         200  <- SEARCHABLE register
http://pharm.cals.am/pharm/drug_images/drug_search_view.php?p_text1=metformin&search_in=2   200 (78 records)
https://www.pharm.am/attachments/article/4871/Law on Medicines_ENG_ 27.06.2017.pdf    200  50pp EN
https://www.pharm.am/attachments/article/4813/Degree_162_eng_1.pdf       200  36pp EN (Decision 162-N)
https://www.pharm.am/attachments/article/5113/Degree_78_26.12.2025.pdf   200  1091pp RU (consolidated Decision 78)
https://www.pharm.am/attachments/article/9850/Degree_34_22_05_2025.pdf   200  (EAEU Decision N34/2025)
https://www.pharm.am/attachments/article/4810/PoA-requirements_eng_1.pdf 200  EN
https://www.pharm.am/attachments/article/4781/Registration dossier presentation and format_CTD_eng.pdf  200 EN
https://www.pharm.am/attachments/article/4759/Application_Final_eng_HUM_VET_1.docx    200
https://www.pharm.am/attachments/article/8846/Order_111-A-25 _ price_list.pdf         200  10pp scanned AM
https://www.pharm.am/attachments/article/8786/Bank details 3125.docx                  200
https://www.arlis.am/DocumentView.aspx?DocID=192788    200  <- consolidated Law On State Duty (Art. 20.3 fees)
https://www.arlis.am/DocumentView.aspx?docid=192548    200  <- 11 Apr 2024 amending law inserting Art. 20.3
https://moh.am/                                                          200
https://picscheme.org/en/members                                         200  (Armenia ABSENT)
https://eec.eaeunion.org/comission/department/deptexreg/BD.php           200  <- EAEU registers index
https://eec.eaeunion.org/comission/department/deptexreg/formirovanie-obshchikh-rynkov/drug-registry-eaeu.php  200
https://docs.eaeunion.org/docs/ru-ru/0147061/itia_24122014               200
https://portal.eaeunion.org/sites/odata/_layouts/15/Registry/PMM06/TableView.aspx    200 (devices register)
```

### UNVERIFIED (404, blocked, empty, or not retrieved)
```
https://ampra.am/                                ports 80/443 CLOSED (DNS+MX exist on ns.gov.am)
https://www.moh.am/en                                                    404
https://www.pharm.am/index.php/en/registered-medicenes                   404 (dead link in own menu)
https://www.pharm.am/index.php/en/registration-statistics                404 (dead link in own menu)
https://www.pharm.am/index.php/en/state-duty-of-medicines-registration   404 (dead link in own menu)
.../4977-decree-...-n-172-a-...                   200 but BODY EMPTY, no attachment — decree text NOT obtained
https://portal.eaeunion.org/sites/odata/_layouts/15/registry/pmm01/tableview.aspx   404 <- EAEU MEDICINES register
MoH Order N 189-A of 06.02.2014 (GMP inspection fee)     listed on site, NOT OPENED — no amount
Government Decision N 202-N of 28.02.2019 (import/export, named patient)  listed, NOT OPENED
Government Decision N 1873-N of 28.11.2024 (amends 162-N incl. point 11)  NOT OBTAINED
RA Law "On Medicines" HO- number                                         NOT CONFIRMED
```
