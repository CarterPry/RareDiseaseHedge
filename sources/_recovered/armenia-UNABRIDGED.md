<!-- RECOVERED from subagent transcript agent-abe941cdd0b1aee38.jsonl, session fd64561f-7c90-41a2-95cf-b4a133a8fe0f, research date 2026-08-05.
     Raw agent output, 50,601 chars vs 38,327 on disk — the on-disk armenia.md was abridged by the parent. Diff before trusting the short one.
     Verbatim agent deliverable — not re-edited. -->

Research complete. Here are my findings.

---

# ARMENIA — Pharmaceutical Registration Pathways (research as of 2026-08-05)

## ⚠️ HEADLINE FINDING (read first)

**The single most important fact for your project: Armenia's purely national registration route legally closed on 1 July 2021, and the window to convert existing national marketing authorisations to EAEU dossiers closed on 31 December 2025 — it has already passed.** Both dates are verified from the consolidated text of EEC Council Decision No. 78 (version as amended through Decision No. 93 of 26 Nov 2025). Details and the important nuance that makes this less fatal than it sounds are in §7.

---

## 1. THE REGULATOR — SCDMTE

| Item | Value | Status |
|---|---|---|
| Name on own contacts page | **«CENTRE OF DRUG AND MEDICAL TECHNOLOGY EXPERTISE» SNCO** | VERIFIED |
| Armenian legal name (from its own 2024 Director's Order) | **«Դեղերի և բժշկական տեխնոլոգիաների փորձագիտական կենտրոն» ՊՈԱԿ** | VERIFIED |
| Legal form | **ՊՈԱԿ = SNCO (State Non-Commercial Organisation)** | VERIFIED |
| "after Academician Emil Gabrielyan" | Appears in pharm.am page titles (Good Practice Inspection dept.) | VERIFIED |
| Director | **Arayik Baghryan** (signs the PoA requirements + price orders) | VERIFIED |
| Address | **49/5 Komitas Ave., Yerevan 0051, Republic of Armenia** | VERIFIED |
| Phone | **+374 60 83-00-73** | VERIFIED |
| Email | **info@ampra.am** (JS-obfuscated on the page; decoded from source) | VERIFIED (decoded) |
| Founded | 1992, accountable to the Ministry of Health | VERIFIED |

**Correction to your brief:** it is a **ՊՈԱԿ / SNCO**, *not* a CJSC/ՓԲԸ. Third-party consultancies (Cratia et al.) describe it as "JSC/CJSC" — that conflicts with the Centre's own 2024 order and its contacts page. Treat the consultancy description as wrong or outdated.

**Oddity worth knowing:** the contact email domain is **ampra.am**, not pharm.am. `ampra.am` resolves (83.139.3.43) on **government nameservers ns.gov.am** with MX `mail.ampra.am`, but **ports 80/443 are closed — there is no website**. This looks like a renamed/reorganised agency whose web presence has not launched. I could not verify what AMPRA stands for. **UNVERIFIED — could not confirm.** Use the email, but expect the pharm.am brand in correspondence.

**Named departments** (from site structure, VERIFIED): Medical Devices Registration Department; **Good Practice (GMP/GDP) Inspection Department**; Pharmacological Council sits at the **Ministry of Health**, not the Centre.

### Ministry of Health
- **moh.am** — VERIFIED (HTTP 200). `www.moh.am/en` → **404, UNVERIFIED** (no English path at that address).
- MoH is the **"Authorized Body"** under the Law. Per Article 6 it performs state registration, issues registration/GMP/GDP certificates, maintains the register, and licenses. **The Minister's individual order is the legal act that registers a medicine.** SCDMTE is the expert/assessment organisation; the **Pharmacological Council of the MoH** issues recommend / do-not-recommend opinions. VERIFIED.
- Registration orders are being issued continuously — most recent seen: **N 4378-A of 29.07.2026** (47 pages of orders). VERIFIED. Armenia is actively registering medicines right now.

---

## 2. THE LAW

**RA Law "On Medicinal Products" / «Դեղերի մասին», adopted 17 May 2016.** VERIFIED (full English text).

**Law number: UNVERIFIED — could not confirm the ՀՕ-/HO- number.** The English translation carries no number, and I could not open the arlis.am Armenian record for it. Do **not** cite "HO-172" — that number belongs to something else. (For contrast, I *did* verify the State Duty law's number: **ՀՕ-186 of 27 December 1997**.)

Key articles (all VERIFIED from the English text):
- **Art. 16(3)** — two routes: **general** and **simplified**. Simplified applies to medicines registered in a member state of "the international professional organization defined by a decree of the RA Government", **or WHO-prequalified**.
- **Art. 16(9)** — applicant = manufacturer **or another sole entrepreneur or legal entity responsible for the product**; becomes the certificate holder. Documents may be filed by an authorised person.
- **Art. 16(13)** — timelines (see §4).
- **Art. 16(15)** — **generic data waivers (critical for you, see §5).**
- **Art. 16(17)** — pre-registration inspection possible; applicant pays; recognition of foreign inspection reports per Government procedure.
- **Art. 16(18)** — **5-year registration term**; SmPC + PIL **in Armenian** attached to the certificate; register must be public and on the Authorized Body's website.
- **Art. 16(21)** — **state duty per the RA Law on State Duty** (this is the key that unlocked the fee schedule).
- **Art. 16(26)** — enables **recognition of registrations** from those countries by agreement.
- **Art. 16(27)(8)** — refusal if the product is **not registered in the applicant's own country**, *except* for medicines registered in an ICH member state.
- **Art. 20(3)** — retail medicines must have an **Armenian-language insert**.

### The "international professional organization" = **ICH**
VERIFIED twice over:
1. **Government Decision N 162-N, point 11**: *"Simplified procedure for registration of medicine shall be applied to the medicines registered (undergone expert-examination) in a member state of the **ICH** or pre-qualified by the World Health Organisation."*
2. The State Duty law refers to *«Դեղերի տեխնիկական պահանջների ներդաշնակեցման միջազգային խորհրդի (Այ-Սի-Էյչ) անդամ երկրի իրավասու մարմնի»* — "the competent authority of an **ICH** member country."

The governing instrument is **Government Decree N 172-A of 23 February 2017** "On determination of the international organization as defined by the Law 'On Medicines'". The pharm.am page for it exists but **its body is empty and it carries no attachment — I could not read the decree text itself. UNVERIFIED.**

**⚠️ Important honest caveat on scope:** the legal text says "member state of the **ICH**" — it does **not** enumerate FDA/EMA/PMDA. Consultancy sites uniformly gloss this as "EU, USA, Japan" (the ICH founding regulatory members). ICH today has many more regulatory members (Health Canada, Swissmedic, MHRA, TGA, MFDS, NMPA, ANVISA, Türkiye, Singapore, Saudi FDA, etc.). **Whether SCDMTE applies the narrow founders list or the full current ICH membership is NOT publicly documented and I could not verify it.** Point 11 was also **amended by Decision N 1873-N of 28 November 2024**, and I could not retrieve what that amendment added. **This is your single highest-value question to put to SCDMTE in writing**, because it determines whether e.g. an MHRA or Health Canada approval buys you the 31-day route. Note: PMDA/Japan, FDA/US and EC/EU are safe on any reading; **TGA, Swissmedic, MHRA, Health Canada are the uncertain band**; **WHO-PQ is independently and explicitly named in the statute, so it is safe.**

---

## 3. GOVERNING SECONDARY LEGISLATION

- **Government Decision N 162-N of 28 February 2019** — the operative registration rules; repealed Decision N 347 of 25 April 2001. **English text VERIFIED** (36 pp). Annexes: 1 registration procedure, 2 expert-examination procedure, 3 required document list, 4 no-new-registration variations, 5 recognition of foreign inspection reports. Amended by **N 1873-N of 28 November 2024** (many points).
- **MoH Order N 31-N of 10 June 2019** — registration certificate form, **register structure and operating rules**, Rx/OTC classification. VERIFIED (listed).
- **Government Decision N 202-N of 28 February 2019** — import/export of medicines, substances, herbal substances, IMPs. VERIFIED (listed).
- **Government Decision N 164-N of 28 February 2019** — rapid alert, recall, unregistered/falsified products. VERIFIED (listed).
- **Government Decision N 734-N of 28 May 2011** — GMP implementation schedule. VERIFIED (listed).

---

## 4. PATHWAYS AND TIMELINES

### National routes (Law Art. 16(13) + Decision 162-N §§19–21, 35) — all VERIFIED
| Route | Total | Of which expert examination |
|---|---|---|
| **General procedure** | **150 calendar days** | 140 calendar days |
| **Simplified** (ICH member state registration or WHO-PQ) | **31 calendar days** | **21 calendar days** |
| **Re-registration** (5-yr renewal) | 31 calendar days | 21 calendar days |
| **Certificate term extension** | **10 calendar days** | — |

- **+10 calendar days** if the applicant supplements documents mid-review (Art. 16(13); Decision 162-N §21).
- **Clock stops:** time the applicant spends answering deficiency requests is **excluded** from the total (Decision 162-N §22). So 31 days is the *regulator's* clock, not elapsed time.
- **Simplified mechanics (§§19, 36–37):** the assessment is a **comparative review** of the Reference Competent Authority's assessment report against your dossier — composition, specs/quality ND, manufacturing sites, research data, product information. **No laboratory testing of samples.** If composition, manufacturing site, stability, specs or product information are **inconsistent** with the reference approval, you are notified and — with your consent and further payment — **the file is converted to the general procedure**. Plan for this: perfect alignment with the reference dossier is the whole game.
- **Registration validity: 5 years**, renewable; after re-registration the term can be extended every 5 years based on post-registration safety monitoring.
- Armenian SmPC/PIL are **drafted by the Centre during the assessment** (Decision 162-N §38), and may be completed after the fact if workload is heavy.

### EAEU routes (Decision 78) — all VERIFIED
| Procedure | Timeline |
|---|---|
| **Reference State** registration + expertise (§46) | **≤ 140 working days** from application to MA issue |
| **Mutual Recognition** in each Recognition State (§69) | **≤ 40 working days** from access to the assessment report |
| **Decentralised (DCP)** (§84) | **≤ 140 working days** reference state + **≤ 50 working days** recognition states |
| Applicant response window | up to 90 working days (§72), **excluded** from the clock |

**Armenia can be either Reference State or Recognition State** — Decision 78 §23: *"The applicant independently chooses the reference state and, if necessary, the recognition state."* VERIFIED. No restriction on Armenia.

**🔑 The key structural insight (Decision 78 §21(a), VERIFIED):** Mutual Recognition is performed *"by the reference state under these Rules for the purpose of circulation of the medicinal product on the market of **only that state** — **(national registration procedure)**."* In other words, **an EAEU MRP filing naming Armenia as sole Reference State with no Recognition States IS the modern national registration.** This is exactly the category the Armenian fee law calls *"registration under EAEU rules for use only in the Republic of Armenia."* You have not lost a national route — it has been re-plumbed through EAEU rules, and you can later bolt on Russia/Belarus/Kazakhstan/Kyrgyzstan via MRP without re-doing the science.

---

## 5. GENERIC / REPURPOSING DATA WAIVERS — the commercially decisive provisions

**Law Art. 16(15), VERIFIED verbatim.** Two distinct waivers:

1. **No preclinical / clinical data required** if you show the product is reproduced from an originator registered in **Armenia or an ICH member state for at least 8 years**.
2. **No bioequivalence data required** if your documents confirm the product has been **used in Armenia or an ICH member state for more than 10 years** — *"In such case, the applicant shall submit only appropriate data from the scientific literature."*

That second limb is a genuine **bibliographic / well-established-use pathway** and is close to ideal for off-patent repurposing. It is mirrored in the dossier structure: **CTD Module 1.5.1 "Information for Bibliographical Applications"** (VERIFIED).

Art. 16(15) also contains a **10-year market protection** for the originator: a reproduced product may circulate 10 years after the originator's registration, **extendable by up to 10 further years if the certificate holder registers new indications** during that period. Diligence this before filing against a recently-repurposed originator.

**Also relevant:** the EAEU fee law has a dedicated category — *«Լավ ուսումնասիրված բժշկական կիրառություն ունեցող վերարտադրված դեղ»* = **"reproduced medicine with well-established medical use"** — priced materially below ordinary generics (§6). Notably, **that category exists only in the EAEU fee lines, not the national general/simplified lines.** VERIFIED.

**New indication:** registering a **new indication** costs a flat **400,000 AMD** (State Duty Art. 20.3(1)(12)) — the single most relevant line item for a repurposing business. VERIFIED.

---

## 6. FEES — FULL STATUTORY SCHEDULE (this is normally the hardest thing to get; I found it)

**Legal basis:** RA Law "On State Duty" (**ՀՕ-186 of 27 Dec 1997**), **new Article 20.3**, inserted by the amending law **adopted 11 April 2024**. VERIFIED from the consolidated official text on arlis.am.

**Base duty (բազային տուրք) = 1,000 AMD.** VERIFIED verbatim: *"Բազային տուրքի չափ է սահմանվում 1000 դրամը"*. All figures below = multiplier × 1,000 AMD.

### 20.3(1)(1) — Generic, or hybrid not differing from the original in API(s)/strength/dosage form
*(charged for the first dosage form, strength and route, AND for each subsequent one)*
| Action | AMD |
|---|---|
| General procedure, **or** EAEU registration for Armenia-only use | **1,100,000** |
| **Simplified procedure** | **500,000** |
| Re-registration / certificate extension (Armenia-only) | 500,000 |
| EAEU registration — **Reference State** | 2,100,000 |
| EAEU DCP or MRP — **Recognition State** | 1,500,000 |
| Bring Armenian dossier into EAEU conformity (reference) or mutual recognition | 1,200,000 |
| Bring dossier into EAEU conformity, Armenia-only use | 900,000 |
| EAEU re-registration | 1,000,000 |
| **Maintaining EAEU registration in force — ANNUAL** | **100,000/yr** |
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

### 20.3(1)(4) — Biosimilar, blood-derived, radiopharmaceutical, new combination of known drugs, hybrid
2,100,000 / 900,000 / 900,000 / 3,100,000 / 2,200,000 / 2,000,000 / 1,400,000 / 1,500,000 / 200,000 / 1,000,000 (same column order)

### 20.3(1)(6) & (7) — Herbal medicine / packaged-labelled herbal raw material
Herbal: 800,000 general · 500,000 simplified · 1,500,000 EAEU ref · 1,000,000 EAEU recog · 100,000/yr
Herbal raw material: 250,000 general · 250,000 simplified · 500,000 EAEU ref · 50,000/yr

### 20.3(1)(8) & (9) — Homeopathic / homeopathic without indications
800,000 / 500,000 … and 400,000 / 250,000 respectively

### Line extensions and variations
| Item | AMD |
|---|---|
| Each subsequent pack/release form, **same** primary pack | 50,000 |
| Each subsequent pack/release form, **different** primary pack | 200,000 |
| **Each subsequent manufacturing site OR NEW INDICATION** (registration or post-reg variation) | **400,000** |
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

### Import / export, licences, clinical trials
Import documentary expertise: 10,000 (1–5 names) / 20,000 (6–20) / 1,000 per name (21+) · Sampling: 12,000/20,000/1,000 · Registration-status or identity check: 12,000/20,000/1,000 · **Lab expertise of a medicine/IMP 300,000** · Lab expertise of substance/herbal material 100,000 · Export permit documentary expertise 1,000 per name · **Manufacturing licence expertise 280,000** · **Wholesale licence expertise 140,000** · **Clinical trial authorisation 500,000** · **BE study, or post-registration CT of an Armenia-registered drug, or a CT of a drug already authorised for CT or compassionate use by an ICH-member competent authority: 250,000** · CT document changes 100,000/change · IMP safety monitoring 100,000/yr · Advertising permit 10,000 per material · GLP certificate 30,000

### SCDMTE's own paid services (separate from state duty)
**Order N 111-A-24 of 30 April 2024**, Annex 1, AMD **incl. VAT**. Later amendments: N 74-25-A (26.02.2025), N 105-25-L (13.03.2025), N 231-25-A (22.05.2025), **N 60-26-L (10.02.2026 — most recent)**. All PDFs are **scanned Armenian images**; I read them by rendering to image. VERIFIED:
- Registration/expertise status information per INN — **3,000**
- **Risk Management Plan agreement — 160,000**
- **Safety report assessment — 120,000**
- Preliminary expertise of registration-sample conformity for import — **24,000**
- **Certificate of Pharmaceutical Product (CPP) issuance — 20,000**
- **Reference drug approval — 50,000**
- Annual list of RA-registered drugs/devices, electronic — 1,000
- Archival information, electronic, per INN — 30,000
- Other services — **by contract**

**⚠️ The 10.02.2026 order (N 60-26-L) is a scanned image with no text layer and I could not extract its figures — the amounts above are from the 2024 base list and may have been superseded. UNVERIFIED for 2026. Request the current price list from info@ampra.am.**

**Not obtained:** **MoH Order N 189-A of 6 February 2014 "On adopting the GMP compliance inspection fee"** exists on the site but **I did not open it — I have no GMP inspection fee amount. UNVERIFIED.** Also, GMP inspection and pre-registration inspection costs are explicitly **by contract with the applicant** (Law Art. 16(17); Decision 162-N Annex 5 §4), so no fixed published figure should be expected.

**Bank details** for payment: `pharm.am/attachments/article/8786/Bank details 3125.docx` — VERIFIED (link resolves).

---

## 7. EAEU — CURRENT STATE AS OF 2026 (the critical section)

**Primary source used:** the **consolidated text of EEC Council Decision No. 78 of 3 November 2016 "On the Rules for Registration and Expert Evaluation of Medicinal Products for Human Use"**, as amended through **Decision No. 93 of 26 November 2025**, published by pharm.am as `Degree_78_26.12.2025.pdf` (1,091 pages, Russian). **VERIFIED.** Full amendment chain on its face: N55 (14.06.2018), N9 (30.01.2020), N128 (23.12.2020), N14 (05.03.2021), N34 (23.04.2021), N36 (17.03.2022), N141 (23.09.2022), N60 (22.05.2023), N114 (20.10.2023), N43 (29.05.2024), N117 (29.11.2024), N12 (22.01.2025), **N34 (22.05.2025)**, **N77 (12.09.2025)**, **N93 (26.11.2025)**.

### The actual deadlines — Decision 78, point 2 (VERIFIED verbatim)
- **2(b):** *Until **1 July 2021*** (Russia: until 31 Dec 2020) an applicant could choose EAEU Rules **or** member-state law. Nationally registered products circulate **only in the territory of the state that issued the MA**. → **Armenia's national registration route closed 1 July 2021.**
- **2(c):** MAs applied for nationally before 1 July 2021 could be extended under national law **but only until 31 December 2025**; national-law variations to such dossiers likewise only until 31 Dec 2025.
- **2(d):** Nationally registered medicines **had to be brought into conformity with EAEU law by 31 December 2025** via the **Section XIII** procedure.
- **§170 (Section XIII), as amended:** *"The application for bringing the registration dossier … into conformity with Union requirements must be submitted to the authorised body (expert organisation) of the **reference state before 31 December 2025**."*

### What Decision No. 34 of 22 May 2025 actually did — and did NOT do
It is widely misreported as an extension. **It did not extend the 31 Dec 2025 filing deadline.** It created a **grace mechanism** for those who filed in time (VERIFIED):
- If a conformity application was filed with the reference state **by 31 Dec 2025** and the procedure was not finished, the national MA is **extended for the duration of the procedure — up to 3 years in each declared member state** from the reference-state filing date, **plus up to 2 further years** from the recognition-state filing date. The recognition-state application must be filed within the 3-year window.
- If the conformity procedure **completed** in the reference state before 31 Dec 2025, MAs in recognition states are extended for the procedure duration, **max 2 years from 31 December 2025**.
- **§164 as amended:** third-country-manufactured product imported during MA validity for which **no** conformity application was filed **may still be sold after 31 Dec 2025 under that member state's own legislation** — i.e. sell-through of existing stock only.

### ⚠️ Do not confuse with medical devices
The widely-cited EEC news item *"Possibility to register medical products according to national rules extended"* (14 Feb 2023, Protocol signed 13 Feb 2023, extending to 31 Dec 2025 / full transition 1 Jan 2026) is about **MEDICAL DEVICES, not medicines**. VERIFIED by fetching it. Several regulatory-consultancy blogs blend the two. Ignore it for pharmaceuticals.

### Does Armenia still accept national-only applications in 2026?
**Legally: no** — EAEU law closed that on 1 July 2021, and the conversion window closed 31 Dec 2025.

**But the Armenian domestic instruments still contain the national procedures**, and they are not dead letters: the Law's Art. 16 general/simplified procedures stand; **Decision 162-N was amended as recently as 28 November 2024** and still describes them; and the **April 2024** State Duty law created *new* fee lines for "general procedure" and "simplified procedure" registration — legislating fees in 2024 for a route supposedly closed in 2021.

The reconciliation is almost certainly Decision 78 **§21(a)**: single-reference-state MRP *is* the national procedure, and the Armenian fee law prices *"general procedure **or** EAEU-rules registration for Armenia-only use"* **at the same rate on the same line** — strongly implying they are being run as one thing.

**I could not verify definitively whether SCDMTE today accepts a filing labelled "simplified national procedure" (31 days, 500,000 AMD for a generic) or whether every new file must be styled as an EAEU submission. UNVERIFIED — this must be confirmed with SCDMTE.** It is your second highest-value question, and it is worth a lot: the simplified national route at **500,000 AMD / 31 days** versus EAEU reference-state at **2,100,000 AMD / 140 working days** is a ~4× cost and ~4× time difference.

### EAEU registers
| Register | URL | Status |
|---|---|---|
| EEC databases index page | `https://eec.eaeunion.org/comission/department/deptexreg/BD.php` | **VERIFIED** |
| **Unified Register of Registered Medicinal Products of the EAEU** | `https://portal.eaeunion.org/sites/odata/_layouts/15/registry/pmm01/tableview.aspx?filter=…` | **UNVERIFIED — 404.** The EEC's own link is **truncated mid-query-string in its HTML**; every case/path variant I tried returned 404 |
| Unified register of **medical devices** (PMM06) | `https://portal.eaeunion.org/sites/odata/_layouts/15/Registry/PMM06/TableView.aspx` | **VERIFIED** (HTTP 200, JS-rendered) |
| PMM02/03/04/05/09 (QPs, substandard/falsified, ADRs, suspended, pharma inspectors) | same pattern | **UNVERIFIED — all 404** |
| EAEU legal portal | `https://docs.eaeunion.org/` | **VERIFIED** |
| **EAEU Agreement on medicines, 23 Dec 2014** (Art. 20 transitional provisions) | `https://docs.eaeunion.org/docs/ru-ru/0147061/itia_24122014` (page) → PDF `…/upload/iblock/378/hq2zq9oemikhx26fzr95d5qt0ihuy09s/itia_24122014_doc.pdf` | **VERIFIED** (English, 13 pp) |
| `portal.eaeunion.org/` root | redirects → `opendata.eaeunion.org/opendata/` | VERIFIED |

Agreement **Article 20** verbatim: *"Medicinal products registered in the Member States before the entry into force of this Agreement shall be brought into compliance with the requirements and regulations of the Union **before 31 December 2025**."* VERIFIED.

---

## 8. PUBLIC REGISTER OF MEDICINES — you asked specifically; there are TWO

### (a) 🔍 SEARCHABLE register — **pharm.cals.am** (this is the one you were looking for)
**`http://pharm.cals.am/pharm/drug_images/index.php` — VERIFIED, HTTP 200.**
Found via the EEC's own page listing member-state registers, where it is the **official Armenian entry**: `https://eec.eaeunion.org/comission/department/deptexreg/formirovanie-obshchikh-rynkov/drug-registry-eaeu.php` — **VERIFIED**.

- **Searchable by:** Trade name · Generic name · Country · Manufacturer · **ATC code**
- **Languages:** English and Հայերեն (toggle) — records are stored **bilingually in both**
- Has a login for extended access; public search works without it
- **I tested it live.** `GET /pharm/drug_images/drug_search_view.php?p_text1=metformin&search_in=2` returned **111 KB / 78 records**, `****`-delimited, `#$`-delimited fields
- **Fields returned:** trade name, INN, dosage form, strength & pack, country, manufacturer (full address, with role tags like *batch releaser / bulk manufacturer, packager, quality control*), Armenian equivalents of all of the above, **registration number**, status (`Registered`), registration date, expiry, **ATC code**, **registration category** (e.g. *"generic, first dosage form and strength"*), **GMP standard (e.g. `PIC/S`)**, and validity/extension dates
- Minimum 3 characters per query
- **This is effectively a scrapeable API** — highly usable for competitive/whitespace analysis

### (b) 📄 DOWNLOADABLE full register — pharm.am
- Landing page: `https://www.pharm.am/index.php/en/register-of-medicines` — **VERIFIED**
- File: `https://www.pharm.am/attachments/article/2966/Registereng_total_up_to_30.06.26.pdf` — **VERIFIED**, **5.2 MB, 539 pages, English**, titled *"LIST OF REGISTERED MEDICINAL PRODUCTS IN REPUBLIC OF ARMENIA (Up to 30.06.2026)"*
- Columns: trade name · INN · drug form · dose & packaging · manufacturer · country · ATC code · **registration number** · **term of registration** · legal status for supply (PoM/OTC) · **licence (MA) holder with address**
- Text-extractable (not a scan). The filename encodes the cut-off date, so it changes each update — link from the landing page, don't hardcode.
- Site's own caveat: the list alone is not sufficient for a final conclusion on registration; approved packaging/label/PIL in the register must be checked.

**Sub-lists, all VERIFIED as existing URLs:** non-prescription `/index.php/en/non-prescription-medicines-registered-in-republic-of-armenia` · prescription `/list-of-registred-prescription-drugs-in-republic-of-armenia` · controlled `/list-of-registred-under-controled-drugs-in-republic-of-armenia` · Armenian-made `/list-of-registred-armenian-drugs-up-to-30-04-2017` · **rejections** `/rejection-for-registration` · withdrawals · Pharmacological Council recommended / not-recommended lists · MoH registration orders `/order-on-medicines-state-registration-by-minister-of-health-moh-of-the-republic-of-armenia-ra`.

**`/index.php/en/registered-medicenes` (sic) and `/index.php/en/registration-statistics` and `/index.php/en/state-duty-of-medicines-registration` all return 404 — UNVERIFIED** (dead links in the site's own menu).

**Open-data mirror (not fetched, listed only):** `https://data.opendata.am/dataset/scientific-centre-of-drug-and-medical-technology-expertise-medicines-data` — **UNVERIFIED.**

---

## 9. GMP

- **Armenia is NOT a PIC/S member, applicant, or pre-applicant.** **VERIFIED** by fetching `https://picscheme.org/en/members` — 58 participating authorities, Armenia absent.
- **Does SCDMTE do its own inspections? YES.** It has a **Good Practice (GMP/GDP) Inspection Department** (MoH Order N 1325-A of 8 July 2011 on its QMS). MoH issues GMP certificates, and the site publishes an *"Inspection PLAN in compliance with the EAEU GMP guideline 2024 and 2025"*, GMP inspection contract templates, and a list of GMP-certified manufacturers. **VERIFIED.** Real-world proof of active foreign-site inspection: **MoH Orders N 2411-A and N 2412-A of 29 April 2026 refusing GMP certificates to "Laboratorios Atrall S.A." (Portugal) and "SENEXI" (France).** VERIFIED. **Armenia does inspect and does refuse.**
- **Recognition of foreign GMP inspections — Decision 162-N, Annex 5 §11, VERIFIED verbatim:** positive GMP inspection results by competent authorities of **PIC/S member states and EAEU member states within the previous 3 years are RECOGNISED and no Armenian inspection is conducted** — unless the assessment reveals inconsistencies requiring inspection.
- **Annex 5 §12:** for **preclinical, clinical and bioequivalence sites**, positive observations from **WHO prequalification**, and from **ICH and EAEU** member state authorities, are likewise **recognised, no inspection**.
- **Annex 5 §7:** in non-high-risk cases, inspection may be deferred to **within 3 years after registration**.
- **§10:** site monitoring within 30 calendar days of notifying the applicant; **max 5 working days on site**.
- **§4:** **applicant pays**, by contract.
- Practical read: **a PIC/S-member GMP certificate (EU GMP, FDA, MHRA, Health Canada, TGA, Swissmedic, etc.) less than 3 years old should avoid an Armenian inspection.** Note the recognition list here is **PIC/S + EAEU** — which is *broader* than the ICH list used for the simplified registration route. **FDA is a PIC/S participating authority**, so US sites qualify for GMP recognition.
- Refusal ground, Law Art. 16(27)(3): production not complying with **GMP rules approved by the Authorized Body**.
- The searchable register displays a **GMP standard field per product** (observed value: `PIC/S`).
- **EAEU-specific caveat: under EAEU Rules, third-country manufacturing sites generally need an EAEU GMP certificate issued by an EAEU inspectorate. I searched Decision 78 for that requirement and my search returned no hits, so I did NOT confirm it from primary text. UNVERIFIED — treat as an open risk and confirm.** This is a well-known cost/time driver in EAEU filings and should not be assumed away.

---

## 10. FILING FORMAT AND MECHANICS

- **Format: EU-style CTD, Modules 1–5.** The Centre's guidance explicitly cites **`https://www.ich.org/products/ctd.html`** and the EU **Notice to Applicants**. **VERIFIED**: `https://www.pharm.am/attachments/article/4781/Registration dossier presentation and format_CTD_eng.pdf`
- **NOT eCTD.** The instruction is: *"Provide Modules 2–5 with an electronic carrier (storage device), each module in a separate folder … Submit electronic versions of documents in **PDF format (with content search feature)**."* SmPC/labelling/PIL in **Microsoft Word**; mock-ups in PDF. **This is CTD-on-physical-media, not eCTD.** VERIFIED.
- Module 1 notables: **1.3.1.1** Armenian translation of SmPC and PIL (*"if available"*) · **1.3.5** product information already approved in other countries (*"applicable only to the national standard registration procedure"*) · **1.5.1 Bibliographical applications** · **1.5.2 Generic/Hybrid/Biosimilar** · **1.5.3 Data/Market Exclusivity** · **1.5.4 Exceptional Circumstances** · **1.5.5 Conditional Marketing Authorisation** · **1.7 Orphan Market Exclusivity (Similarity; Market Exclusivity)** · 1.8 Pharmacovigilance system + RMP.
- **Submission channels — Decision 162-N §14, VERIFIED:** *"in person and (or) by **e-mail** and (or) through an **electronic system** and (or) by **postal delivery**."* Filed to **"the Organisation"** (= SCDMTE). Document lists are published on **www.moh.am**.
- **Where:** SCDMTE, 49/5 Komitas Ave., Yerevan 0051. Registration of applications during working days/hours; out-of-hours submissions count as next working day (§16).
- **Forms** (`/index.php/en/registration-application/4759-registration-application` — VERIFIED): `Application_Final_eng_HUM_VET_1.docx` plus Appendices 1–3 in **English and bilingual DOCX**. Variation application at `/registration-application/4760-post-registration-change-application`. Variation dossier `/variation-dossier`. Re-registration dossier format `/re-registration-dossie-presentation-and-format`. FAQ page exists.
- **EAEU-format** application forms and CTD guidance are separately published under `/index.php/en/the-eaeu-rules-of-medicines-registration-and-assessments` (registration application form updated 07.10.2022; EAEU CTD). **VERIFIED.**

---

## 11. LOCAL REPRESENTATIVE / MAH

**There is NO statutory requirement for the applicant or MAH to be an Armenian legal entity.** Evidence, all VERIFIED:
- **Law Art. 16(9):** applicant may be the manufacturer **or another sole entrepreneur or legal entity responsible for the product**, who becomes the certificate holder. No nationality or residency qualifier. Documents may be filed by an authorised person.
- **Empirical proof from the register:** the "License holder" column shows foreign MAHs, e.g. *"Eli Lilly Regional Operations GmbH, Koelblgasse 8-10, 1030, Vienna, Austria."* A foreign MAH is plainly accepted in practice.
- **EAEU Decision 78 definitions:** *"marketing authorisation holder"* and *"applicant"* are both simply **"legal entity"** (юридическое лицо) — no establishment requirement. Decision 78 does define a separate concept, **"representative of the marketing authorisation holder" — a legal entity** (§671).

**In practice you will need an authorised representative to file**, and the **Power of Attorney requirements are strict** — `https://www.pharm.am/attachments/article/4810/PoA-requirements_eng_1.pdf` **VERIFIED**:
- Written, **notarially certified**; copies and translations **also notarially certified**
- From Hague Convention (5 Oct 1961) states: **apostille required**
- **Maximum validity 3 years** (longer stated term is cut to 3; no term stated → valid 1 year)
- Must name authorizer and authorised person with passport data/legal address, date of issue (undated = void), the right to complete the registration application, **explicitly which state bodies and which region** the agent may act before, **whether it covers all products or one specific product**, and **explicitly the right to pay the state duty / assessment fees**
- Must state whether sub-delegation is permitted; sub-PoA cannot outlast the main PoA
- Signed and sealed; issued by the director or a person empowered by the charter

**The PoA rules do not state that the representative must be Armenian-registered. UNVERIFIED whether SCDMTE accepts a non-Armenian agent in practice** — but note the requirement to specify "in which region and state bodies" the agent acts, plus the practical need for someone to physically pay duties and receive correspondence, means an Armenian agent is the realistic route. Confirm with SCDMTE.

**Separate and mandatory:** importation and wholesale require **Armenian licences** (manufacturing licence expertise 280,000 AMD; **wholesale licence expertise 140,000 AMD**) — so you will need a licensed Armenian importer/wholesaler regardless of where the MAH sits.

---

## 12. GOTCHAS

- **Armenian language.** SmPC + PIL **in Armenian** are attached to the registration certificate and are the legal reference throughout circulation (Art. 16(18)). Retail products must carry an Armenian insert (Art. 20(3)); pharmacies must supply an Armenian PIL on buyer demand. **Mitigation:** the Centre **drafts the Armenian SmPC/PIL during assessment** (Decision 162-N §38), and **absence of an Armenian insert at the moment of import is expressly NOT a ground to refuse import** (Art. 21(9)) — it can be remedied post-import. Import *is* refused if packaging language is not among the accepted languages (Art. 21(8)(15)).
- **Marketing prohibition:** it is **forbidden to put the Armenian supplier's name or trademark** on the marking, SmPC or PIL (Art. 20(4)).
- **Registration granularity — this drives cost.** Art. 16(5): separate registration for **every name, ingredient, strength, dosage form, presentation, new indication, manufacturer (including every performer of the production process), and certificate holder.** Fees are charged **per first *and* per each subsequent** dosage form/strength/route. A multi-strength, multi-pack portfolio multiplies fast. Same primary pack = 50,000/pack; different primary pack = 200,000/pack.
- **Pricing / reimbursement.** Law Art. 10 (full or partial price reimbursement) and **Art. 11 (State Regulation of Prices of Reimbursed Medicinal Products)** — note Art. 11's entry into force was **deferred** under the final provisions. There is a "Reimbursed medicinal product price list" approved by the Authorized Body (Art. 3(55)). **I did not research the reimbursement/pricing mechanics — UNVERIFIED.**
- **Orphan drugs: there is NO orphan designation regime in the Law.** I searched the full English text for "orphan" and "rare disease" — **zero hits. VERIFIED absence.** The nearest analogues:
  - **Art. 16(11):** expert examination for medicines with **low demand but of major therapeutic and public-health interest, intended for serious or life-threatening diseases**, may be performed **under a government order** (i.e. state-funded assessment). The Authorized Body approves the list of low-demand/vitally-necessary medicines. There is a live page `/list-of-medicines-liable-to-registration-within-the-framework-of-the-government-orders`. **For a rare-disease company this is the provision to lean on — it can take the assessment cost off you entirely.**
  - **Art. 16(26):** agreements with ICH member states may allow **direct recognition** of registrations there; and *"the Authorized Body may address applicants at its initiative and with its own resources"* to get needed medicines registered.
  - **CTD Module 1.7 Orphan Market Exclusivity** exists in the dossier template, but that is inherited from the EU Notice to Applicants and does **not** evidence an Armenian orphan regime.
- **Unregistered / named-patient import.** **Art. 16(23)(4):** registration is **not required** for medicines *"used with a **special permission of the Authorized Body**"*, nor for products used in research/clinical trials, registration samples, or exhibition samples. So a **named-patient / special-permission import route exists via MoH permission**. **The detailed procedure is in Government Decision N 202-N of 28 Feb 2019, which I did not open — the mechanics, evidence requirements and timelines are UNVERIFIED.**
- **Parallel imports are permitted** under a Government-defined permission procedure (Art. 21(10)–(11)), refused if manufacturer or country of production differs from what is registered in Armenia.
- **Rx/OTC status is fixed at registration** (Art. 16(24)) against ten statutory criteria.
- **Confidentiality:** the Authorized Body must protect legally-protected data; assessors sign conflict-of-interest and confidentiality declarations (Art. 16(14)).
- **Six-month abandonment rule:** if requested supplementary materials are not filed within **6 months** of due notice, the examination terminates and the application is rejected (Art. 16(16)).
- **Underpaid duty:** if the assessment reveals the state duty paid was insufficient, the shortfall is payable within **5 days** of notice (Decision 162-N, Annex 2 §20).
- **Technical gotcha for your own tooling:** **pharm.am serves an incomplete TLS chain** (missing intermediate; GoGetSSL RSA DV SSL CA 2). Standard fetchers fail with *"unable to verify the first certificate."* The site is fine — you need a client that tolerates the incomplete chain or supplies the intermediate. This is why several agents report pharm.am as "down."

---

## 13. STRATEGIC READ FOR AN OFF-PATENT REPURPOSING PLAY

1. **Your best-case route is the simplified procedure at 31 calendar days / 500,000 AMD for a generic** — *if* it is still accepted (see §7) and *if* your reference approval is from a qualifying ICH member state or WHO-PQ. Confirm both in writing before modelling anything.
2. **Art. 16(15) limb two is the crown jewel**: >10 years of use in Armenia or an ICH member state ⇒ **no bioequivalence study**, literature only. Combined with the EAEU **"well-established medical use"** fee category (800,000 AMD Armenia-only), this is one of the cheapest legitimate routes to a marketing authorisation anywhere.
3. **New indications cost a flat 400,000 AMD.** That is the core repurposing transaction and it is cheap.
4. **Watch the 10(+10)-year originator protection in Art. 16(15)** — it is triggered and *extended* by the originator registering new indications. Diligence the originator's Armenian indication history before committing.
5. **Armenia as EAEU Reference State is a strategic asset.** Register once in Armenia (cheapest EAEU reference-state fees of any member: 2,100,000 AMD for a generic, 1,500,000 for well-established use), then extend by MRP into Russia/Belarus/Kazakhstan/Kyrgyzstan at ≤40 working days each. Budget the **100,000 AMD/year** maintenance duty per registration.
6. **Bring a PIC/S-member GMP certificate less than 3 years old** — it should eliminate an Armenian site inspection outright.
7. **Explore Art. 16(11) government-order status early.** For a serious/life-threatening rare disease with low demand, the state may fund the assessment. That is a direct, legislated subsidy for exactly your business model, and there is a published list to get onto.

---

## 14. COMPLETE URL LEDGER

### VERIFIED (fetched, returned relevant content)
```
https://pharm.am/                                                        200
https://www.pharm.am/index.php/en/                                       200
https://www.pharm.am/index.php/en/aboutus                                200
https://www.pharm.am/index.php/en/contacts                               200  (email decoded: info@ampra.am)
https://www.pharm.am/index.php/en/sm                                     200  (full sitemap)
https://www.pharm.am/index.php/en/register-of-medicines                  200  ← register landing
https://www.pharm.am/attachments/article/2966/Registereng_total_up_to_30.06.26.pdf   200  5.2MB/539pp EN
http://pharm.cals.am/pharm/drug_images/index.php                         200  ← SEARCHABLE register
http://pharm.cals.am/pharm/drug_images/drug_search_view.php?p_text1=metformin&search_in=2   200 (78 records)
https://www.pharm.am/attachments/article/4871/Law on Medicines_ENG_ 27.06.2017.pdf    200  50pp EN
https://www.pharm.am/attachments/article/4813/Degree_162_eng_1.pdf       200  36pp EN (Decision 162-N)
https://www.pharm.am/attachments/article/5113/Degree_78_26.12.2025.pdf   200  1091pp RU (consolidated Decision 78)
https://www.pharm.am/attachments/article/9850/Degree_34_22_05_2025.pdf   200  (EAEU Decision N34/2025)
https://www.pharm.am/attachments/article/10249/Decree_N7712-09-2025.pdf  200  (scanned, no text layer)
https://www.pharm.am/attachments/article/4810/PoA-requirements_eng_1.pdf 200  EN
https://www.pharm.am/attachments/article/4781/Registration dossier presentation and format_CTD_eng.pdf  200 EN
https://www.pharm.am/attachments/article/4759/Application_Final_eng_HUM_VET_1.docx    200
https://www.pharm.am/attachments/article/8846/Order_111-A-25 _ price_list.pdf         200  10pp scanned AM
https://www.pharm.am/attachments/article/8846/Order_60-26-L-10-02-2026.pdf            200  scanned, unreadable
https://www.pharm.am/attachments/article/8846/Order_231-25-A.pdf                      200
https://www.pharm.am/attachments/article/8786/Bank details 3125.docx                  200
https://www.pharm.am/index.php/en/medicines-state-tax/4944-medicines-state-tax        200
https://www.pharm.am/index.php/en/expertise-fees-of-state-regulation-of-the-medicinal-products-and-medical-devices-circulation   200
https://www.pharm.am/index.php/en/expertise-fees-of-state-regulation-of-the-medicinal-products-and-medical-devices-circulation/8786-republic-of-armenia-law-on-state-duty  200
https://www.pharm.am/index.php/en/services-and-fees-of-expertise-center               200
https://www.pharm.am/index.php/en/the-eaeu-rules-of-medicines-registration-and-assessments   200
https://www.pharm.am/index.php/en/medicines-pharmaceutical-production-and-proper-distribution  200 (GMP)
https://www.pharm.am/index.php/en/requirements-for-the-power-of-attorney/4810-...      200
https://www.pharm.am/index.php/en/registration-application/4759-registration-application   200
https://www.pharm.am/index.php/en/presentation-and-format-of-the-registration-dossier-common-technical-document-ctd/4781-...  200
https://www.pharm.am/index.php/en/order-on-medicines-state-registration-by-...-ra     200 (orders to 29.07.2026)
https://www.pharm.am/index.php/en/laws/84-on-state-duty                               200
https://www.arlis.am/DocumentView.aspx?DocID=192788    200  ← consolidated Law On State Duty (Art. 20.3 fees, base duty 1000 AMD)
https://www.arlis.am/DocumentView.aspx?docid=192548    200  ← 11 Apr 2024 amending law inserting Art. 20.3
https://moh.am/                                                          200
https://picscheme.org/en/members                                         200  (Armenia ABSENT)
https://eec.eaeunion.org/                                                200
https://eec.eaeunion.org/comission/department/deptexreg/                 200
https://eec.eaeunion.org/comission/department/deptexreg/BD.php           200  ← EAEU registers index
https://eec.eaeunion.org/comission/department/deptexreg/formirovanie-obshchikh-rynkov/            200
https://eec.eaeunion.org/comission/department/deptexreg/formirovanie-obshchikh-rynkov/drug-registry-eaeu.php  200 ← lists pharm.cals.am as Armenia's register
https://eec.eaeunion.org/en/news/prodlena-vozmozhnost-registratsii-meditsinskikh-izdeliy-po-natsionalnym-pravilam/  200 (MEDICAL DEVICES only)
https://docs.eaeunion.org/                                               200
https://docs.eaeunion.org/docs/ru-ru/0147061/itia_24122014               200
https://docs.eaeunion.org/upload/iblock/378/hq2zq9oemikhx26fzr95d5qt0ihuy09s/itia_24122014_doc.pdf  200 EN Agreement
https://portal.eaeunion.org/sites/odata/_layouts/15/Registry/PMM06/TableView.aspx    200 (devices register)
https://portal.eaeunion.org/  → redirects to https://opendata.eaeunion.org/opendata/ 200
https://www.pharm.am/index.php/en/decrees/4813-...162-n...               200
https://www.pharm.am/index.php/en/the-eaeu-rules-.../5113-decision-of-eaeu-n78-...    200
```

### UNVERIFIED (404, blocked, empty, or not retrieved)
```
https://ampra.am/ , http://ampra.am/            ports 80/443 CLOSED (DNS+MX exist on ns.gov.am)
https://www.moh.am/en                                                    404
https://www.pharm.am/index.php/en/registered-medicenes                   404 (dead link in own menu)
https://www.pharm.am/index.php/en/registration-statistics                404 (dead link in own menu)
https://www.pharm.am/index.php/en/state-duty-of-medicines-registration   404 (dead link in own menu)
https://www.pharm.am/index.php/en/gmp-compliance                         404 (correct path differs)
https://www.pharm.am/index.php/am/contacts                               404
http://www.pharm.am/index.php/en/legal-documents-on-registration/4977-decree-...-n-172-a-...   200 but BODY EMPTY, no attachment — decree text NOT obtained
https://portal.eaeunion.org/sites/odata/_layouts/15/registry/pmm01/tableview.aspx   404 ← EAEU MEDICINES register; EEC's own link truncated in HTML
https://portal.eaeunion.org/sites/odata/_layouts/15/Registry/PMM01..05,09/TableView.aspx   all 404
https://portal.eaeunion.org/sites/commonprocesses/ru-ru/Pages/Home.aspx  404
https://medreg.eaeunion.org/ , https://lekreg.eaeunion.org/              no connection
https://data.opendata.am/dataset/scientific-centre-of-drug-...-medicines-data   NOT FETCHED
MoH Order N 189-A of 06.02.2014 (GMP inspection fee)                     listed on site, NOT OPENED — no amount
Government Decision N 202-N of 28.02.2019 (import/export, named patient) listed, NOT OPENED
Government Decision N 1873-N of 28.11.2024 (amends 162-N incl. point 11) NOT OBTAINED
RA Law "On Medicines" ՀՕ-/HO- number                                     NOT CONFIRMED
```

---

## 15. WHAT TO ASK SCDMTE (info@ampra.am / +374 60 83-00-73)

1. **Which specific ICH member authorities** qualify for the simplified procedure — full current ICH regulatory membership, or only EU/US/Japan? And what did **Decision N 1873-N of 28.11.2024** change in point 11 of Decision 162-N?
2. **Is a national general/simplified registration application still accepted in 2026**, or must every new application be filed under EAEU rules (single-reference-state MRP for Armenia-only use)?
3. **Current SCDMTE paid-services price list** — the machine-readable text of **Order N 60-26-L of 10.02.2026**.
4. **GMP inspection fee** (Order N 189-A of 06.02.2014) and current pre-registration inspection contract rates.
5. Confirmation that a **non-Armenian entity may act as authorised representative**, or whether an Armenian agent is required in practice.
6. Whether a **PIC/S-member GMP certificate** alone is sufficient, and whether an **EAEU GMP certificate** is separately required for third-country sites under EAEU-route filings.
7. Route into the **Art. 16(11) government-order** list for low-demand, life-threatening-disease medicines.
8. The **named-patient / special-permission import** procedure under Decision N 202-N.
9. A copy of **Government Decree N 172-A of 23.02.2017** (its webpage is empty).

**Note:** I did not create any files. The scratchpad working copies of the PDFs and extracts remain at `/private/tmp/claude-501/-Users-carte-Downloads-RareDiseaseHedge/fd64561f-7c90-41a2-95cf-b4a133a8fe0f/scratchpad/` if you want the source documents.