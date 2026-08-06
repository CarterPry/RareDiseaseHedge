<!-- RECOVERED from subagent transcript agent-ac2e91c5fb3f06d28.jsonl, session fd64561f-7c90-41a2-95cf-b4a133a8fe0f, research date 2026-08-05.
     SECOND INDEPENDENT PASS over Georgia/Armenia/Ukraine/Botswana by a different agent. Use to cross-check the single-country files; disagreements are worth chasing.
     Verbatim agent deliverable — not re-edited. -->

## Georgia

**Regulatory authority**
- Ministry: **Ministry of Internally Displaced Persons from the Occupied Territories, Labour, Health and Social Affairs of Georgia** / *საქართველოს ოკუპირებული ტერიტორიებიდან დევნილთა, შრომის, ჯანმრთელობისა და სოციალური დაცვის სამინისტრო*. `https://moh.gov.ge/` — **UNVERIFIED (HTTP 403, Cloudflare bot challenge)**. `https://www.moh.gov.ge/en/` — **UNVERIFIED (403)**.
- Agency: **LEPL State Regulation Agency for Medical and Pharmaceutical Activities** (RAMA) / *სსიპ სამედიცინო და ფარმაცევტული საქმიანობის (სახელმწიფო) რეგულირების სააგენტო*. `https://rama.moh.gov.ge/` — **UNVERIFIED (403 Cloudflare managed challenge)**. I confirmed this three ways: direct curl (403), a rendering proxy (returned the CAPTCHA interstitial), and the Wayback CDX index, which shows `rama.moh.gov.ge` returning 403 even to the Internet Archive crawler since at least Feb 2025, with `cdn-cgi/challenge-platform` snapshots captured. **The site is live but not machine-fetchable; a human browser passes.**
- Contact reported from a browser session (I could **not** reproduce programmatically — treat as second-hand): Ak. Tsereteli Ave. 144, Tbilisi 0119; **+995 32 251 00 11** (ext. 12-11); **regagency@moh.gov.ge**; Department for Regulation of Pharmaceutical Activities → Division of Drug Registration, Clinical Trials and Permits.

**Recognition pathway — yes, and it is the real prize. VERIFIED from primary law.**
- Legal instrument: **Law of Georgia No. 659 "On Medicines and Pharmaceutical Activity"** — `https://matsne.gov.ge/en/document/view/29836` — **VERIFIED** (English consolidated text, current through amending Law No. 3807-XIIIმს-Xმპ of 30/11/2023; matsne registration code 470.200.000.05.001.000.199).
  - **Art. 11⁷ – Recognition regime (აღიარებითი რეჟიმი).** Art. 11⁷(7): the Agency performs an **administrative review only** and enters the product in the Departmental Registry **within 7 working days**. Art. 11⁷(3): *"Any person may be an interested person."* Art. 11⁷(4): applies *"irrespective of the purpose of import."* Art. 11⁷(8): validity = the foreign MA's validity, **capped at 5 years**.
  - **Art. 11¹¹ – National regime.** Admin review within **14 days**; decision within **3 months** (primary registration or Type-II variation), **2 months** (re-registration), **20 calendar days** (Type I A), **40 calendar days** (Type I B). One deficiency cycle, up to 2 months to cure. Applicant restricted to *"a manufacturer of a pharmaceutical product or a trade licence holder."* **Silence = deemed registered** (Art. 11¹¹(10)).
  - **Art. 11⁸ – parallel/repackaged import**: product already authorised in Georgia but differently packaged/labelled needs only a **notification**; Agency enters it in the Registry **within 5 working days**; non-response = consent.
  - **Art. 11¹³(h)** — import bypassing both regimes for humanitarian purposes explicitly names **"rare disease"**, with Ministry consent. Non-commercial only (named-patient bridge, not a market route).

**Accepted reference regulators — VERIFIED, reconstructed from primary sources**
Government of Georgia **Resolution No. 188 of 22 October 2009** — `https://matsne.gov.ge/ka/document/view/4606` — **VERIFIED (original text; the consolidated version is paywalled on matsne)**. I therefore pulled all three published amendments individually:
- **No. 195 of 30/07/2013** (`.../view/1978950` — **VERIFIED**) → added **State of Israel**
- **No. 415 of 17/08/2021** (`.../view/5243935` — **VERIFIED**) → added **Republic of Croatia**
- **No. 13 of 17/01/2022** (`.../view/5355246` — **VERIFIED**) → added **Republic of Türkiye**

Current list = **EMA (listed as "EMEA")** + the national regulators of: USA, Australia, Austria, New Zealand, Belgium, Bulgaria, Germany, Denmark, **UK**, Estonia, Spain, Ireland, Italy, Japan, Iceland, Canada, Cyprus, **Republic of Korea**, Luxembourg, Latvia, Lithuania, Malta, Norway, Netherlands, Portugal, Poland, Romania, France, Greece, Slovenia, Slovakia, Hungary, Finland, Sweden, **Switzerland**, Czechia, **Israel**, **Croatia**, **Türkiye** (39 countries + EMA). The decree names **countries**, not named agencies (EMA excepted) — any competent authority of a listed country qualifies. **Absent: India, China, Brazil, Mexico, Singapore, Russia, Ukraine, WHO-PQ.** (Note: a parallel research pass reading only the 2009 original wrongly concluded Croatia was absent; the amendments above are dispositive.)

**Fees — VERIFIED from primary law**
**Law of Georgia on Registration Fees, Article 7(6)** — `https://matsne.gov.ge/en/document/view/16054` — **VERIFIED (English text read in full)**:
- Recognition regime, registration on first import: **GEL 500** — expressly **excluding** proactive Agency registration and Art. 11⁸ repackaging notifications (i.e. those two are fee-free)
- National regime: innovative **GEL 2,500** (re-reg 2,000); **generic / repeatedly-manufactured product and blood preparations GEL 500** (re-reg 200); immunobiologicals 500/200; radiopharmaceuticals 500/200
- Second-level (Type II) change to registration documentation: **GEL 50**

**Local representative / MAH** — **no Georgian legal entity required under recognition** (Art. 11⁷(3) "any person"). Under the national regime the applicant must be the manufacturer or trade-licence holder — a foreign entity qualifies; a pure local distributor does not. Art. 11¹¹(19)(c) requires an original document granting representative authority (a PoA) to a natural or legal person — **the statute does not require that person be Georgian**. You will still need Georgian counterparties for import and wholesale (separately licensed).

**Public register** — Art. 11⁶(3) makes the **Departmental Registry (უწყებრივი რეესტრი)** a public document that *"shall be kept in electronic form and made accessible through the internet."* In practice:
- `http://pharmacy.moh.gov.ge/` and `https://pharmacy.moh.gov.ge/` — **UNVERIFIED (TCP connection timeout from this environment)**
- `https://referenceprice.moh.gov.ge/ui/` and its JSON API `/api/api/refrenceprice/getDrugsMainPage` — **UNVERIFIED to me (HTTP 403, Cloudflare "Just a moment…" interstitial returned)**. A browser session reports it live, Georgian UI, ~7,794 records with CSV export and fields incl. Georgian registration number, INN, trade name, trade-licence holder and country, and capped wholesale/retail prices. This is a **reference-price catalogue**, not the full register. **Verify in a browser before relying on it.**
- **Honest bottom line: I could not verify any Georgian public medicines register.** Write to `regagency@moh.gov.ge`.

**GMP — this is the real gate, not the timeline. VERIFIED.**
- **Georgia is NOT a PIC/S member** — `https://picscheme.org/en/members` — **VERIFIED** (Georgia absent from the participating-authority list; only Jordan shown as a future accession).
- **Government Decree No. 349 of 16/11/2010** — `https://matsne.gov.ge/ka/document/view/1100741` — **VERIFIED**. Georgia recognises exactly five GMP standards: **WHO GMP, EC GMP, US FDA cGMP, PIC/S GMP, ICH Q7 GMP**.
- **Government Decree No. 114 of 4 March 2022** — `https://matsne.gov.ge/ka/document/view/5402664` — **VERIFIED**. Art. 1(5): **from 2 March 2022, a GMP-compliance document is mandatory for RECOGNITION-regime registration too**, submitted as original, copy, electronic document *"or other publicly available form with reference to the source"* (an EudraGMDP/FDA public record link can suffice), plus evidence of authority to manufacture the specific dosage form. Art. 1(3): products already nationally registered had to file GMP evidence by 1 March 2023 or have **registration suspended** until they do. Decree 114 has been amended six times, most recently **No. 121 of 23/03/2026**; **consolidated text is paywalled on matsne — the current staging rules are UNVERIFIED.**
- **No provision requiring RAMA inspection of a foreign manufacturing site was found in any primary text I read. That is absence of evidence, not confirmed absence — UNVERIFIED.**

**Filing pathway** — paper-heavy, **no eCTD, no CTD**. Art. 11¹¹(c): administrative part in **tangible (paper) form in Georgian**, plus a Word-format Georgian leaflet translation **on CD**; scientific-technical part in Georgian/Russian/English in **three identical copies** on CD. Recognition-regime dossier (Art. 11⁷(5)) is far lighter: Georgian PIL translation + original PIL, form, dosage, labelling sample (electronic accepted), **CPP or CPP-equivalent** from a Decree-188 regulator (attested copies fine), GMP document, analysis methods printable from a public pharmacopoeia, and **2 standard packages** as sample. Submission to RAMA, Ak. Tsereteli Ave. 144, Tbilisi.

**Gotchas**
1. **Price is set for you.** Law Art. 2(22¹/22²) defines reference retail and wholesale prices as statutory maxima, and Art. 3(11) empowers the Government to set the methodology. For an off-patent generic this caps revenue before you file. Model it first.
2. Statutory fines are severe and were added by Law No. 2273 of 01/12/2022: Art. 37¹³ — manufacturing without a Georgian national GMP certificate = **GEL 50,000** (100,000 repeat); Art. 37² — unlicensed pharmaceutical activity = GEL 8,000/16,000.
3. Re-registration must be filed **not later than 2 months before expiry**, or the product falls back to primary registration (Art. 11¹¹(6)).
4. Recognition validity tracks the foreign MA; if the reference regulator suspends, **Georgia suspends automatically** (Art. 11⁷(9)) and the suspension extends to every pack variant.
5. Consultancy sources quote "15 calendar days" for recognition; **the law says 7 working days**. Trust the statute, budget for the practical figure.
6. All Georgian government domains are behind Cloudflare/geo-restrictions. **Plan on a local agent or a Tbilisi-based browser session for anything operational.**

---

## Armenia

**Regulatory authority** — **«Centre of Drug and Medical Technology Expertise» SNCO** (State Non-Commercial Organisation) / *«Դեղերի և բժշկական տեխնոլոգիաների փորձագիտական կենտրոն»*. `https://pharm.am/` — **VERIFIED** (trilingual: Armenian / Русский / English). Contacts page `https://pharm.am/index.php/en/contacts` — **VERIFIED**: Director **Arayik Baghryan**; **49/5 Komitas Ave., Yerevan 0051**; **Phone (+374 60) 83-00-73**. **The email field on the published contacts page is blank** — no address is given. Ministry of Health `https://www.moh.am/` — resolves (HTTP 200) but only with TLS verification disabled; **the server serves an incomplete certificate chain**, so strict clients (including WebFetch) fail. Same issue on pharm.am.

**Pathways and the EAEU transition — VERIFIED from the regulator's own notices**
Armenia has effectively **closed national registration and moved to EAEU rules**. Two SCDMTE notices, both **VERIFIED**:
- `https://pharm.am/index.php/en/news-and-announcements/9055-...` — **MoH Order No. 4896-A of 11 September 2024**: applications under the **national procedure could be submitted only until 31 December 2024**; and **dossiers of medicines registered nationally must be brought into conformity with EAEU requirements by 31 December 2025**.
- `https://pharm.am/index.php/en/news-and-announcements/10002-...` — **MoH Order No. 3785-A of 24 June 2025** sets the terms of validity of national-procedure registrations and the terms of expertise, *"based on the amendments made to Decision No. 78 of 3 November 2016 of the EEC Council and Decision No. 96 of 10 June 2020 of the EEC Council."*

So: **for a new filing in 2026 the route is the EAEU procedure under EEC Council Decision No. 78 of 3 November 2016** ("Rules for Registration and Expert Evaluation of Medicinal Products for Human Use"). SCDMTE hosts the consolidated text and posts updates — most recent update **20 November 2025** (`.../news-and-announcements/10319-20-11`, **VERIFIED**) and a further January 2026 item (`.../10501-20-01-26`, **VERIFIED**). Under Decision 78, registration is via **mutual recognition** or **decentralised** procedure with a Reference State and Recognition State(s); Armenia can act in either role.

**Reference-regulator reliance** — **I found no Armenian national fast-track keyed to FDA/EMA/PMDA/TGA/Swissmedic/MHRA approval, and I am not going to invent one.** The reliance that exists is *intra-EAEU* (recognition of another member state's assessment), not reliance on Western regulators. **An FDA or EMA approval does not by itself unlock a shortened Armenian route that I could verify.** Confirm with SCDMTE.

**Timelines** — **UNVERIFIED.** Decision 78 sets EAEU-wide statutory clocks and MoH Order 3785-A sets Armenian expertise terms, but I did not read either instrument's timing articles directly. Do not quote a day count without checking.

**Fees** — the current instrument is **"Order on approval of the price list of paid services provided by the SCDMTE, No. 111-24 of 30 April 2024 (updated 20.05.2024)"**, PDF at `https://pharm.am/attachments/article/6951/Order_111-24_services_fees_new.pdf` — **URL VERIFIED (HTTP 200, 2.2 MB PDF), CONTENT UNVERIFIED**: it is a scanned image PDF in Armenian and yielded 9 characters of extractable text. **I have no AMD amounts and will not guess any.** Note the site page still carries the older title (Order N 029-A/22 of 14 February 2022) while serving the 2024 order — quote the 2024 number.

**Public register — VERIFIED and genuinely good.**
`http://pharm.cals.am/pharm/drug_images/index.php` — **VERIFIED, live and functional**. Searchable by **trade name, generic name, country, manufacturer, ATC code**; UI toggles **English / Հայերեն**. I executed a live query against its backend (`drug_search_view.php?p_text1=metformin&search_in=2`) and it returned structured records in both English and Armenian with: trade name, INN, dosage form, strength and pack, country, full manufacturer address (incl. batch releaser / bulk manufacturer roles), registration number, status, registration date, **GMP standard (e.g. "PIC/S")**, and **registration validity dates**. A usage guide is published at `https://pharm.am/index.php/en/guide-to-using-database-of-registered-medicines` (**VERIFIED**, guide file dated 17.01.24). The **EAEU unified register** (separate from this) — **UNVERIFIED, I did not locate or fetch it.**

**GMP** — **Armenia is NOT a PIC/S member** (`https://picscheme.org/en/members` — **VERIFIED**, Armenia absent). The register nevertheless records **PIC/S** as an accepted GMP basis for registered products, and SCDMTE publishes an inspection plan under **EAEU GMP rules** (`.../news-and-announcements/8907-plan-of-inspections-in-compliance-with-the-guideline-of-good-manufacturing-practice-of-eurasian-economic-union-rules` — **VERIFIED as a page title**). **Whether SCDMTE requires its own EAEU-GMP inspection of a foreign site, and on what trigger, is UNVERIFIED — this is the single most important question to put to them.**

**Local representative / MAH** — **UNVERIFIED.** Under EAEU Decision 78 the applicant must generally have a presence or authorised representative in the Union; I did not confirm Armenia's specific implementation. Ask directly.

**Filing pathway** — SCDMTE, 49/5 Komitas Ave., Yerevan 0051, +374 60 83-00-73. Site sections that exist and are the right entry points (all **VERIFIED as live pages**): *Medicines Registration*, *Medicines Registration By EAEU Rules*, *State duty rates and paid services*, *GMP compliance*, *Legislation → Laws / Decrees / Orders*. Submission format (eCTD vs EAEU CTD vs paper) — **UNVERIFIED**.

**Gotchas**
1. **The 31 December 2025 conversion deadline has passed.** Any Armenian national-procedure MA whose dossier was not brought into EAEU conformity is at risk. If you are acquiring or in-licensing an existing Armenian registration, **diligence its EAEU conversion status first.**
2. You are filing into a **five-country regional system**, not a small national one. That is upside (one dossier, five markets) and downside (EAEU CTD, Russian-language dossier expectations, EAEU GMP).
3. Armenia's page titles and news items lag the documents they serve — always open the attachment and read the order number on its face.

---

## Ukraine

**Regulatory authorities**
- **State Expert Center of the MoH of Ukraine** / *Державний експертний центр Міністерства охорони здоров'я України* (ДЕЦ / SEC). `https://www.dec.gov.ua/` — **VERIFIED**. **Note:** the server serves an incomplete TLS chain, so strict clients fail; `https://dec.gov.ua/` (no `www`) does not resolve — **use `www.`**. Address **03057 Kyiv, vul. Simyi Brodskykh 10 (formerly Smolenska 10)**; **+38 (044) 202-17-00**; Service Centre **+38 (044) 202-17-05**; **Single Window (Єдине вікно) +38 (044) 202-17-09**; **dec@dec.gov.ua** — all **VERIFIED** from the site footer. Key departments named on site: *Департамент експертизи реєстраційних матеріалів* (Department of Registration Materials Expertise) with sub-units for expert work, instructions/nomenclature, blood products and vaccines, and biologicals/biosimilars.
- **State Service of Ukraine on Medicines and Drugs Control** (Держлікслужба) — licensing, import licences and GMP confirmations. **Ukraine IS a PIC/S member since January 2011** — `https://picscheme.org/en/members` — **VERIFIED**.

**Law No. 2469-IX — the actual transition timeline. VERIFIED from the official legal database.**
`https://zakon.rada.gov.ua/laws/show/2469-20` — **VERIFIED** (the main text page is JS-gated, but the document card and history tables render). Law of Ukraine **"Про лікарські засоби" of 28.07.2022 No. 2469-IX**, status **Чинний (in force)**.

The critical distinction Ukrainian law draws is **набрання чинності (entry into force)** vs **введення в дію (bringing into effect / application)**. From the official history table (`https://zakon.rada.gov.ua/laws/show/2469-20/card4#History` — **VERIFIED**):
- **28.07.2022** adopted; **published 18.08.2022** (*Голос України* No. 169) — **entry into force on publication**.
- Amended by **3345-IX** (rev. 17.09.2023), **3911-IX** (rev. 18.12.2024), **3860-IX** (rev. 01.01.2025 — *"введення в дію окремих положень"*, bringing certain provisions into effect), **4239-IX** (rev. 28.04.2025), **4454-IX** (rev. 05.06.2025 — **current version**).
- **1 January 2027 — "Введення в дію", status "Набирає чинності", on the basis of Laws No. 4094-IX and No. 4017-IX.** This is the date the EU-aligned regime is brought into application. **That is the answer to "what changes on 1 January of the transition year" — the year is 2027, not 2025.**
- Three further tranches are pegged to events, not dates: one **"from the day of termination or cancellation of martial law"** (basis 4840-IX); one **"30 months from the day of termination or cancellation of martial law"** (basis 3136-IX); and one **"from the day of entry into force of the international treaty on Ukraine's accession to the EU, but not earlier than the day Article 57 is brought into effect"** (basis 3860-IX).

**Grandfathering of pre-2469-IX marketing authorisations: UNVERIFIED.** The transitional provisions are in the law text, which is behind a JS gate I could not render. Do not assume; read Chapter XV of 2469-IX or ask SEC.

**Verification (fast-track) procedure — CONFIRMED ALIVE as of July 2026.**
Ukraine's route for medicines already approved by a stringent regulator is the *"експертиза щодо автентичності реєстраційних матеріалів"* (expertise as to the **authenticity** of registration materials). SEC publishes the outcome lists continuously:
`https://www.dec.gov.ua/applicant/perelikiv-lz-na-yaki-zaversheno-ekspertizu-shhodo-avtentichnosti-re-straczijnih-materialiv/` — **VERIFIED**. Most recent list dated **13.07.2026** (published 20.07.2026); 18 pages of prior lists back through 2025. **This is direct, dated proof the procedure is operating today.**
- **The MoH order number establishing it, the exact accepted-regulator list, the statutory day count and the UAH fee: UNVERIFIED.** I did not reach a primary text for any of them and will not reproduce a remembered order number. Request them from SEC via `dec@dec.gov.ua` or the Single Window line.
- Related SEC pages, both **VERIFIED**: `https://www.dec.gov.ua/applicant/perelik-lz-rekomendovanih-do-re-straczi-perere-straczi-ta-vnesennya-zmin-u-re-straczijni-materiali/` (products recommended for registration/re-registration/variations) and a *"Legislation (in English)"* section plus `https://www.dec.gov.ua/materials/pereklady-normatyvno-pravovyh-aktiv-anglijskoyu-movoyu/` (English translations of NLAs).

**Wartime emergency provisions — VERIFIED indirectly but unambiguously.** The State Register's own search form carries a dedicated filter **"екстрена державна реєстрація під час воєнного стану"** (emergency state registration during martial law) alongside **"для екстренного застосування"** (for emergency use). A distinct martial-law emergency registration category therefore exists and is populated. **The Cabinet resolution numbers and whether expiring MAs are auto-extended during martial law: UNVERIFIED.**

**Public register — VERIFIED.**
**State Register of Medicinal Products of Ukraine** (*Державний реєстр лікарських засобів України*), operated by SEC:
- Home: `http://www.drlz.com.ua/` — **VERIFIED** (Ukrainian, legacy Lotus Domino, cp1251 encoding)
- **Search page: `http://www.drlz.com.ua/ibp/ddsite.nsf/all/shlist?opendocument` — VERIFIED.** Searchable by name (≥5 chars), MA number (≥4 chars), MA start date, INN (≥5 chars), ATC code (≥3 chars), active-substance composition (≥4 chars), plus the two emergency filters above. **A CSV export of the whole register is offered.** Language: Ukrainian only.
- Legal basis cited on the page: Law "On Medicinal Products" and **MoH Order No. 411 of 31 August 2004** — **VERIFIED as cited on the page**, not read at source.
- Pharmacovigilance system **AISF**: `https://aisf.dec.gov.ua/` — linked from both SEC and the register; **not fetched, UNVERIFIED**.

**Local representative / MAH** — **UNVERIFIED.** Ukraine historically allows a foreign applicant with a Ukrainian authorised representative, but I did not reach a primary text confirming the position under either the current or the 2027 regime.

**GMP — the known gotcha, and Ukraine's PIC/S membership does not remove it.** Ukraine requires its **own confirmation of GMP compliance issued by Derzhlikluzhba** for foreign manufacturing sites, and it is a separate procedure with its own clock running in parallel to registration. **I did not verify the current procedure, timeline or fee — UNVERIFIED.** Budget for it as a critical-path item regardless.

**Submission format** — **UNVERIFIED** (eCTD availability, portal vs paper). SEC has a "Single Window" phone line, which suggests physical/hybrid intake.

**Gotchas**
1. **Do not confuse "in force since 2022" with "applies from 2027."** Anyone quoting a 2025 changeover is reading a superseded version of the transitional provisions — the official history shows the general bringing-into-effect moved to **1 January 2027**, and further tranches are tied to the end of martial law (+0 and +30 months) and to EU accession.
2. **An institutional reorganisation is underway.** SEC's own newsroom (**VERIFIED**) reports an EU Twinning project to create **"Укрфармагентство" (Ukrpharmagency)**, a single independent medicines agency, with SEC staff being trained on EU regulatory practice. Your counterparty institution will likely change name and possibly powers mid-project.
3. Language: everything operational is Ukrainian-only. The English legislation section exists but is thin.
4. Ukraine has a **National Price Catalogue** (Національний каталог цін) that interacts with variations to registration materials — SEC issued a market-operator clarification on this. Price regulation is live; factor it in.

---

## Botswana

**Regulatory authority** — **Botswana Medicines Regulatory Authority (BoMRA)**. `https://www.bomra.co.bw/` — **VERIFIED**. **info@bomra.co.bw**; legal/consultation **legal@bomra.co.bw**; **+267 373 1720 / +267 318 6254**; **Plot 112, Gaborone International Finance Park, Gaborone**; postal **Private Bag 2, Gaborone Station**. All **VERIFIED**.

**Legal basis** — **Medicines and Related Substances Act, 2025 (Act No. 29 of 2025)**. PDF at `https://www.bomra.co.bw/wp-content/uploads/2026/06/Medicines-and-Related-Substances-Act-2025-2.pdf` — **URL VERIFIED (HTTP 200, 6.3 MB), CONTENT UNVERIFIED** (scanned image PDF, no extractable text). The Act number 29 of 2025 is **VERIFIED** — it appears on the face of the draft regulations made under it. A **draft** implementing regulation package was published for consultation and remains draft (below).

**Registration pathways — VERIFIED from BoMRA's current guidelines**
- **Reliance/Recognition guideline: `BOMRA/ER/MD/P04/G07`, Issue 3.0, effective 16 February 2026** — `https://www.bomra.co.bw/download/135/human-medicines/25575/guid-reliance-recognition-on-information-from-regional-and-international-bodies-iss3-0.pdf` — **VERIFIED (downloaded and OCR'd; it is a scanned PDF)**. §4.1 — to qualify for the reliance pathway an application must have been approved through:
  - (a) **WHO PQ Collaborative Registration Procedure**; (b) **SRA/WLA CRP**; (c) **ZAZIBONA collaborative procedure**; (d) **AMA Continental Listing Procedure**; (e) **WHO Prequalified products**; (f) **ZAZIBONA member states — Zambia, Zimbabwe, Tanzania, Namibia, South Africa** (registrations **from 2016 onward**; for variations, approvals from any year accepted); (g) **WHO Listed Authorities (WLA)**.
  - **The document's own revision sheet records "Deletion of SRA countries since they are referred to as WHO-Listed" (11/11/2025).** So **FDA, EMA, PMDA, Health Canada, TGA, Swissmedic and MHRA qualify via the WLA limb** — do not cite an "SRA list" to BoMRA in 2026, cite WLA.
  - §4.3: BoMRA conducts an **abridged review**, expressly reserving the right to request more information or revert to full review. §4.2: submit per `BOMRA/ER/MD/P04/G01` **with a cover letter stating the pathway you are electing**, plus CTD **Section 1.10.5** sameness-of-API/FPP information.
- **BoMRA participates in ZAZIBONA — VERIFIED** (it is named as a qualifying route in BoMRA's own guideline, and Botswana is a founding Z-A-Zi-Bo-Na member).

**Timelines — VERIFIED from `BOMRA/ER/MD/P04/G01` "Guideline on Submission of Applications and BOMRA timelines"** (Issue 5.0, revision sheet dated 04/08/2025) — `https://www.bomra.co.bw/download/135/human-medicines/25576/guideline-on-submission-of-applications-and-bomra-timelines.pdf` — **VERIFIED (downloaded and OCR'd)**. Conventional/allopathic **human** medicines, §6.B1:
| Step | Time |
|---|---|
| Screening | **3 months** |
| **CRP and/or reliance** | **3 months** |
| Expedited / fast-tracked | **8 months** |
| Products partly or fully manufactured locally | **12 months** |
| Normal process | **18 months** |
| All variations | 6 months |
| Renewals | 6 months |
| Exemptions (unregistered-medicine import) | **48 working hours** |

Clock rules: timelines count only time the file is **at BoMRA**; applicants get a maximum of **3 months per query cycle**; missing a response deadline **closes the application**; after all cycles are exhausted any outstanding issue = rejection, and re-filing requires a **new application and full fee**. (An older Customer Service Standards sheet on the site, dated 11-09-2020, still quotes 36 months for normal process and 90 days for WHO CRP — **it is superseded; use G01**.)

**Fees — currently in force: the 2019 schedule. VERIFIED via OCR, with caveats.**
`https://www.bomra.co.bw/download/76/regulatory-fees/25707/bomra_fees_2019.pdf` — **URL VERIFIED**; it is a scanned Government Gazette extract ("SCHEDULE 5 — FEES", pages C.1168–C.1175). OCR-read amounts in **BWP**:
- Screening (all products) **1,600**; registration (generic) **12,500**; biological/biosimilar **15,000**; vaccine **15,000**; B-listed product **10,000**; partly manufactured in Botswana **7,500**; fully manufactured in Botswana **5,000**
- **Expedited: NCE 50,000; generic 40,000; line extension 15,000.** Line extension (NCE or generic) **7,500**
- Evaluation of additional clinical data (pre-registration) **5,000**; package insert amendment **2,000**; re-scheduling request **1,000**
- Variations: **major 1,500 / minor 1,000 / notification 500**. Annual fee: NCE **1,000**, generic (local mfr) **500**
- **GMP compliance fees: SADC 3,500 · Rest of Africa 5,000 · Asia 6,500 · Rest of World 7,000**
- Import/export permit (non-controlled) **50/permit**; controlled substances **100/permit**; transit **100/permit**; **importation fee 0.15% of consignment value** (0.25% for wholesale-exempted products)
- **The "Application for registration (New Chemical Entity), without/with delivery system" line and the "Annual Fee (generic) imported" line did not OCR cleanly — UNVERIFIED, do not quote them.**

**Fees — the 2026 package is DRAFT, not in force.** `https://www.bomra.co.bw/download/134/mrsa-2025-regulations/25564/mrs_fees_levies_penalties_regulations_2026.pdf` — **VERIFIED (text-extractable, read in full)**. It is headed **"STATUTORY INSTRUMENT NO. ___ OF 2026"**, "Published on ______, 2026", "Made this ___ day of ___, 2026", and reg. 1(2) says it commences **on a date the Minister appoints by Gazette notice**. The accompanying FAQ (`.../25559/guidance-and-overview-2.docx` — **VERIFIED**) states the consultation ran **20 April – 20 May 2026**. Its internal "phased implementation" table (registration fees 1 April 2026, inspection 1 July 2026, levies 1 October 2026, penalties 1 January 2027) is **internally inconsistent with a consultation that closed in May 2026** — treat those dates as stale drafting. **Do not budget against the draft.** What it signals, though, is directionally important for a rare-disease repurposer:
- Explicit **Abridged Pathway** (SRA-approved **USD 4,000**; WHO PQ **USD 3,000**) and **Verification Pathway** (approved by **two or more** SRAs, **USD 2,500**) for international applicants, vs Full Evaluation NCE USD 8,000. Generic with BE study USD 3,500; with biowaiver USD 2,500. Annual retention USD 800; 5-year renewal USD 4,000.
- **Orphan medical products (draft reg. 18, under s.44 of the Act): registration and annual retention fees reduced 50% for international applicants (waived entirely for local applicants), conditional on obtaining orphan designation before or with the application, demonstrating the disease affects ≤5% of Botswana's population, and showing no satisfactory alternative exists.** Draft reg. 7 also gives WHO-PQ products 25% and paediatric formulations 30%.
- Draft statutory pathway timelines (General Regulations reg. 13): Full 270 working days, Abridged 180, **Verification 90**, Notification 30.
- Draft GMP inspection fees for foreign sites: SADC USD 4,000 → Europe/Americas USD 7,500 → Rest of World USD 8,000, with **"Desk review only" USD 3,500**.

**Local responsible person — VERIFIED (draft General Regulations reg. 11, under s.36 of the Act).** `https://www.bomra.co.bw/download/134/mrsa-2025-regulations/25560/mrs-general_regulations_2026.pdf` — **VERIFIED (143 pp, text-extractable)**. An applicant must either **be a company registered in Botswana**, or, **if not resident, appoint a Local Technical Representative** who is a natural person ordinarily resident in Botswana or a company incorporated in Botswana. The LTR handles all BoMRA communications, receives safety reports and complaints, facilitates inspections, **maintains records in Botswana**, and has authority to act for the MAH. Appointment is on **Form GEN-03**, signed by both parties, filed **before or with** the application, updated within 14 days of change. Changing LTR does not invalidate the registration. **You do not need a Botswana entity — you need a Botswana agent.**

**Public register — VERIFIED, with the caveat that it is files, not a live database.**
BoMRA's register lives under Resource Centre → Documents → Registers → **Registered Medicines**. The site loads it via AJAX, so the direct file URLs are:
- **`https://www.bomra.co.bw/download/121/registered-medicines/25504/human-medicines-registered-medicines-and-b-listed-products.pdf`** — *Human medicines (Registered medicines and B-listed products)*, PDF — **VERIFIED**
- `https://www.bomra.co.bw/download/121/registered-medicines/25674/complementary-medicines-register-10-08-2023.xlsx` — Complementary Medicines Register, XLSX, dated 10.08.2023 — **VERIFIED**
- `https://www.bomra.co.bw/download/121/registered-medicines/25581/human-medicines-database-for-emergency-use-29-11-2022.xlsx` — Emergency-use database, XLSX, dated 29.11.2022 — **VERIFIED**
- `https://www.bomra.co.bw/smpc-pi-pil-repository/` — SmPC/PI/PIL repository — **VERIFIED (HTTP 200)**
- `https://www.bomra.co.bw/download/58/licensing-and-enforcement/25486/licensed-facilities-2024-25.xlsx` — Licensed Facilities 2024-25 — **VERIFIED**
- Language: **English**. **Honest caveat: these are periodically-refreshed downloads, not a queryable register, and two of the three carry 2022–2023 dates on their filenames.**

**Submission portal — VERIFIED.** All applications go through **BRIMS (BoMRA Regulatory Information Management System)**: `https://brims.bomra.co.bw/` — **VERIFIED (HTTP 200)**; step-by-step guidance at `https://helpdesk.bomra.co.bw/knowledgebase` — **VERIFIED (HTTP 200)**. Format is **CTD folder structure with text-searchable, bookmarked PDFs in ZIP** — this is **CTD, not eCTD**. Product samples are required **only after passing screening** (and for variations affecting label or appearance), sent physically to Plot 112, Gaborone International Finance Park.

**GMP** — **Botswana is NOT a PIC/S member** (`https://picscheme.org/en/members` — **VERIFIED**, absent). BoMRA's GMP guideline is `BOMRA/IL/IL/P08/G01` Iss 2.1 — `https://www.bomra.co.bw/download/58/licensing-and-enforcement/25568/guid-guidelines-for-good-manufacturing-practice-il-il-p08-g01-iss2-1-signed.pdf` — **URL VERIFIED, content UNVERIFIED (scanned)**. There is a companion **"Guidelines for Performing Remote Inspection" `IL/IL/P18/G01`** and a **"Guideline for Good Recognition and Reliance Practices" `BOMRA/IL/IL/P08/G02`** on the licensing side (`https://www.bomra.co.bw/download/58/licensing-and-enforcement/25379/guideline-for-good-recognition-and-reliance-practices-bomra-il-il-p08-g02-signed.pdf` — **URL VERIFIED, content UNVERIFIED (scanned)**). The 2019 fee schedule prices foreign GMP inspections by region, and the draft 2026 schedule prices a **"desk review only"** option — both imply **foreign site inspection is possible but reliance/desk review is available**. Draft General Regs reg. 27(3)(b) expressly allows BoMRA to issue a GMP certificate on **reliance on a recognised authority's inspection outcome**, valid 2 years (vs 3 for its own full inspection). **Whether a physical inspection is triggered for a given file: UNVERIFIED — ask.**

**Other key guidance documents (all URLs VERIFIED; contents are scanned PDFs)**
- `BOMRA/ER/MD/P04/G08` Registration Quality Guidelines for Small Molecules Iss 3.0 — `.../25574/guid-registration-quality-guidelines-for-small-molecules-er-md-p04-g08-iss3-0.pdf`
- `ER/MD/P11/G01` Renewal of Registration for Human Medicines Iss 3
- `ER/MD/P04/G03` Variation of Human Medicines Iss 3
- Draft 2026 package: General, Human Medicines (allopathic), Clinical Trials, Medical Devices, Veterinary, Complementary, Cosmetics, Fees/Levies/Penalties — all under `https://www.bomra.co.bw/documents/#52-134-wpfd-mrsa-2025-regulations`

**Gotchas**
1. **BoMRA is mid-transition.** A new Act (2025) is passed but its implementing regulations were still in draft as of the May 2026 consultation close. Fees, pathway names and timelines will change. **Ask BoMRA in writing which instrument governs your filing date** before you pay anything.
2. **Reliance is only 3 months vs 18 for normal — the whole economics of a Botswana filing turn on qualifying for it.** For an off-patent generic sourced outside a WLA jurisdiction, check whether you can route via ZAZIBONA (a South African or Zambian registration from 2016 or later opens the door) rather than chasing a WLA approval.
3. **The 2016 cut-off on ZAZIBONA-member registrations is a real trap** — a Namibian or Zimbabwean MA granted in, say, 2014 does **not** qualify for new registration reliance (though its variations do).
4. Query cycles are unforgiving: 3-month response cap, application **closed** on a missed deadline, and re-filing costs a full fee plus a new reference number with no credit for prior review.
5. **Orphan designation is worth pursuing** if the draft regs commence as written — 50% off registration and annual retention for an international applicant, but only if designation is applied for **before or together with** the registration application.
6. Expect **annual retention fees** in addition to registration — a recurring cost per SKU that is easy to miss when modelling a wide repurposing portfolio.

---

**Method and residual gaps.** I verified Georgia's law, fee statute, recognition-country decree and both GMP decrees against matsne.gov.ge primary texts; Botswana's reliance guideline, timeline guideline, fee schedule and draft regulations by downloading and (where scanned) OCR-ing the actual PDFs; Armenia's register by executing a live query against its backend; and Ukraine's law status, register and verification-procedure activity against the official legal database and SEC's own publication series. PIC/S membership was checked once for all four.

What I could **not** verify, stated plainly: any Georgian public medicines register (every Georgian government domain returns a Cloudflare 403 or a TCP timeout from this environment — the Internet Archive gets the same 403, so this is bot-blocking, not an outage); the Georgian consolidated texts of Decree 188 and Decree 114 (matsne paywalls consolidated versions); **all Armenian fee amounts** (the current fee order N 111-24 of 30.04.2024 is a scanned Armenian-language PDF); Armenian timelines, local-representative rules and GMP inspection triggers; **Ukraine's verification-procedure order number, accepted-regulator list, day count and fee**, its grandfathering provisions for pre-2469-IX MAs, and its wartime Cabinet resolution numbers; and Botswana's NCE registration fee lines that OCR'd badly. I have not substituted plausible figures for any of these.

Three parallel research passes (Armenia, Ukraine, Botswana) were still running when I compiled this; the Georgia pass returned and I corrected one material error in it — it read only the 2009 original of Decree 188 and reported Croatia as absent from the recognition list, when Decrees 195/2013, 415/2021 and 13/2022 add Israel, Croatia and Türkiye respectively.