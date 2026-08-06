<!-- RECOVERED from subagent transcript agent-aec251056e00b50ae.jsonl, session fd64561f-7c90-41a2-95cf-b4a133a8fe0f, research date 2026-08-05.
     Single-country agent, GEORGIA (Caucasus). Parent interrupted before synthesis.
     Verbatim agent deliverable — not re-edited. -->

# GEORGIA (Caucasus / Tbilisi) — Pharmaceutical Registration Pathways
### Research date: 2026-08-05. Every claim below is tagged to a source I actually retrieved.

**CRITICAL ACCESS NOTE:** `rama.moh.gov.ge` and `moh.gov.ge` sit behind a **Cloudflare managed challenge** — `curl`, WebFetch and Exa all get **403 / "you have been blocked"**. They load normally in a real browser. Everything I mark VERIFIED-browser was read through a real browser session. No CAPTCHA was solved; the challenge passed passively.

---

## 1. THE MINISTRY

| Field | Value |
|---|---|
| English | **Ministry of Internally Displaced Persons from the Occupied Territories, Labour, Health and Social Affairs of Georgia** |
| Georgian | **საქართველოს ოკუპირებული ტერიტორიებიდან დევნილთა, შრომის, ჯანმრთელობისა და სოციალური დაცვის სამინისტრო** |
| Site | `https://moh.gov.ge/` — **VERIFIED (browser)**. Rebuilt site, **Georgian only**. `www.moh.gov.ge` 301s to `moh.gov.ge`. |
| Minister (as displayed on homepage news, Aug 2026) | Mikheil Sarjveladze / მიხეილ სარჯველაძე |

**English MoH site appears to be GONE.** `https://www.moh.gov.ge/en/` → **404 UNVERIFIED**. Legacy English URLs (e.g. `.../en/news/3943/GMP-standard-is-introduced...`) → **404 UNVERIFIED**. Do not plan on English-language ministry content.

---

## 2. THE REGULATOR (RAMA)

**Name discrepancy on the agency's own site — report both:**
- Page `<title>` on every page: **სსიპ სამედიცინო და ფარმაცევტული საქმიანობის სახელმწიფო რეგულირების სააგენტო** (LEPL **State** Regulation Agency for Medical and Pharmaceutical Activities)
- Site footer + header logo: **სსიპ "სამედიცინო და ფარმაცევტული საქმიანობის რეგულირების სააგენტო"** (no "სახელმწიფო") — this matches the name in your brief.
- Common English rendering in industry literature: **LEPL Regulation Agency for Medical and Pharmaceutical Activities**.
- Predecessor names visible in a staff CV on the site: სსიპ წამლის სააგენტო ("Drug Agency", 2019) and სსიპ სამედიცინო საქმიანობის სახელმწიფო რეგულირების სააგენტო.

**Contact — VERIFIED (browser)** at `https://rama.moh.gov.ge/geo/contact/4/kontaqti`:
- Address: **0119 Tbilisi, Ak. Tsereteli Ave. 144** (0119 თბილისი, აკ. წერეთლის გამზ. 144)
- Phone: **(+995 032) 251 00 11**, internal ext. **12-11**
- Email: **regagency@moh.gov.ge**

**Named department for drug registration — VERIFIED (browser)** at `https://rama.moh.gov.ge/geo/static/503`:
- Department: **ფარმაცევტული საქმიანობის რეგულირების დეპარტამენტი** (Department for Regulation of Pharmaceutical Activities)
- Division: **წამლის რეგისტრაციის, კლინიკური კვლევებისა და ნებართვების სამმართველო** (Division of Drug Registration, Clinical Trials and Permits)
- Head: **Gocha Aladashvili / გოჩა ალადაშვილი**, in post since 29 Dec 2022.

⚠️ **RAMA homepage banner currently reads "მიმდინარეობს რეკონსტრუქცია" ("reconstruction under way").** Deep content pages still serve fine.

---

## 3. THE TWO REGIMES — statutory basis

**Primary law:** **Law of Georgia on Medicines and Pharmaceutical Activity** — *"წამლისა და ფარმაცევტული საქმიანობის შესახებ"*, Law No. 659 of 17 April 1996.
- English consolidated: `https://matsne.gov.ge/en/document/view/29836` — **VERIFIED**
- Georgian: `https://matsne.gov.ge/ka/document/view/29836` — appears in matsne search results; I read the English consolidated text, not this URL individually.

**Article numbering warning:** matsne renders superscripts as run-on digits. "Article 117" = **Article 11⁷**; "Article 1111" = **Article 11¹¹**; "Article 118" = **Article 11⁸**; "1113" = **Article 11¹³**; "116" = **Article 11⁶**.

| | **RECOGNITION (აღიარებითი რეჟიმი)** | **NATIONAL (ეროვნული რეჟიმი)** |
|---|---|---|
| Article | **11⁷** | **11¹¹** |
| Statutory timeline | **7 working days** to place product in the Departmental Registry (Art. 11⁷(7)). Deficiency cure: **up to 15 days extra** (RAMA) | **3 months** primary registration; **2 months** re-registration. Deficiency cure: **up to 2 months extra**. Admin check of documents within **14 days** of receipt |
| Assessment scope | **Administrative expertise only.** Art. 11⁴(3): Georgia unilaterally recognises the foreign regulator's safety/efficacy/quality requirements and **"shall not carry out a repeated expertise"** | Full administrative + scientific-technical expertise |
| Who may apply | **Any person.** Art. 11⁷(3): *"Any person may be an interested person"*; Art. 11⁷(4): applies **"irrespective of the purpose of import"** | **Restricted:** Art. 11¹¹(a) — only **a manufacturer of the pharmaceutical product or a trade licence holder** |
| Validity | Same period as the foreign authorisation, **max 5 years** (Art. 11⁷(8)) | **5 years**; circulation permitted after expiry until the product's own shelf-life expires |
| Statutory fee | **500 GEL** | **2,500 GEL** original/innovative · **500 GEL** generic/re-manufactured |

**"Interested person" definition (Art. 2, para 49):** *"a manufacturer, a trade licence holder, an importer or any other natural or legal person interested in the marketing authorisation…"*
**"Trade licence holder" (Art. 2, para 32):** *"an owner of a pharmaceutical product that manufactures a pharmaceutical product or has it manufactured to order."*

---

## 4. THE COUNTRY LIST — VERIFIED PRIMARY SOURCE

**Government of Georgia Resolution (დადგენილება) No. 188 of 22 October 2009** — *"სხვა ქვეყნების ან სახელმწიფოთაშორისი ფარმაცევტული პროდუქტების მარეგულირებელი სახელმწიფო ორგანოების სიის განსაზღვრის შესახებ"*
`https://matsne.gov.ge/ka/document/view/4606?publication=0` — **VERIFIED** (fetched twice with different prompts; consistent). Cross-confirmed by RAMA's own registration page, which names "საქართველოს მთავრობის 2009 წლის 22 ოქტომბრის N188 დადგენილება".

Amendments: **No. 195 (30 Jul 2013)**, **No. 415 (17 Aug 2021)**, **No. 13 (17 Jan 2022)**. Version read is consolidated through 17 Jan 2022.

**The list names ONE international body + 36 COUNTRIES (not individual agencies):**

> **EMEA — European Medicines Agency** (listed as ევროპის წამლების სააგენტო)
>
> USA · Australia · Austria · New Zealand · Belgium · Bulgaria · Germany · Denmark · United Kingdom of Great Britain and Northern Ireland · Estonia · Spain · Ireland · Italy · Japan · Iceland · Canada · Cyprus · **Republic of Korea** · Luxembourg · Latvia · Lithuania · Malta · Norway · Netherlands · Portugal · Poland · Romania · France · Greece · Slovenia · Slovakia · Hungary · Finland · Sweden · **Switzerland** · Czech Republic

**Practical notes:**
- The instrument names **countries**, not agencies (except EMEA). So any national competent authority of a listed country qualifies — you do not need to match a specific agency name.
- **UK is explicitly in the list** and survived Brexit (list amended in 2021 and 2022 without removing it).
- **⚠️ CROATIA and LIECHTENSTEIN appear ABSENT** from the list as extracted, despite Croatia's 2013 EU accession. **Flagging as a possible extraction gap — verify directly with RAMA before relying on a Croatian MA.** Do not treat "EU member = recognised" as automatic.
- Not present: Israel, Singapore, Turkey, Taiwan, EAEU.

---

## 5. STATUTORY FEES — VERIFIED PRIMARY SOURCE

**Law of Georgia on Registration Fees** — *"სარეგისტრაციო მოსაკრებლების შესახებ"*
`https://matsne.gov.ge/ka/document/view/16054` — **VERIFIED**

**Provision: Article 7, paragraph 6 (მუხლი 7, მე-6 პუნქტი).** Heading: *"სარეგისტრაციო მოსაკრებლების სახეები და განაკვეთები; რეგისტრაციის უფლებამოსილების მქონე სახელმწიფო დაწესებულებები."*
*(An earlier extraction pass returned "Article 6 §6"; a targeted re-fetch returned Article 7 §6, and **RAMA's own registration page independently cites "მუხლი 7, მე-6 პუნქტი" three times**. Article 7 §6 is the answer.)*

| Item | Fee |
|---|---|
| **Recognition regime — state registration (first import)** | **500 GEL** |
| National — innovative (new original) product | **2,500 GEL** |
| National — innovative re-registration | **2,000 GEL** |
| National — **generic / re-manufactured product**, blood preparations | **500 GEL** |
| National — generic re-registration | **200 GEL** |
| National — immunobiological | 500 GEL / re-reg 200 GEL |
| National — radiopharmaceutical | 500 GEL / re-reg 200 GEL |
| **Type II ("II რიგის") variation** | **50 GEL** |
| Complementary therapeutic means | 400 / re-reg 200 GEL |
| Biologically active supplements | 600 / re-reg 400 GEL |

For an off-patent generic repurposing play: **recognition = 500 GEL; national generic = 500 GEL.** Fees are trivial; the timeline and dossier burden are the real differentiators.

⚠️ My extraction of the parallel-import (Art. 11⁸ notification) fee line was ambiguous — one pass attached "500 GEL" to both recognition and parallel import. **Treat the Art. 11⁸ notification fee as UNVERIFIED.**

---

## 6. LOCAL REPRESENTATIVE / MAH — the key structural finding

**Recognition regime: NO Georgian legal entity and NO local agent is required by statute.**
- Art. 11⁷(3): *"Any person may be an interested person during the state registration."*
- Art. 11⁷(4): applies *"irrespective of the purpose of import."*
- Nothing in Art. 11⁷ imposes residency, establishment, or local-agent conditions.

**National regime: applicant is RESTRICTED, but not to a Georgian entity.**
- Art. 11¹¹(a): the interested person *"may be a manufacturer of a pharmaceutical product or a trade licence holder."* A foreign manufacturer or foreign product owner qualifies. A pure local distributor with no ownership of the product does **not**.
- Art. 11¹¹(19)(c) requires *"an original document confirming granting by an interested person representative authority to a natural or legal person"* — i.e. a **power of attorney** to whoever files. **The law does not say the representative must be Georgian.** Registration consultancies (mspcorporate, Cratia) describe a **legalised/apostilled Power of Attorney to a representative** as standard practice.

**Practical read:** you can hold the Georgian authorisation in your foreign entity. You will still need a Georgian counterparty for the *commercial* leg — import, wholesale distribution and reference-price compliance are separate licensed activities (Art. 2(21) wholesale distribution). **Confirm import/wholesale licensing separately — I did not verify the wholesale/import licence conditions to primary-source level.**

---

## 7. GMP — VERIFIED, and this is the real gate

**Georgia is NOT a PIC/S member.** `https://picscheme.org/en/members` — **VERIFIED**: 60 Participating Authorities listed (Argentina→USA); **Georgia does not appear anywhere**, not as member, applicant or pre-accession.

**Accepted GMP standards — Government Decree No. 349 of 16 Nov 2010** (*recognition of the list of international, regional and national GMP standards*), annex (დანართი):
`https://matsne.gov.ge/ka/document/view/1100741` — **VERIFIED**
> 1. **WHO GMP** · 2. **EC GMP** (European Commission) · 3. **US FDA current GMP** · 4. **PIC/S GMP** · 5. **ICH Q7 GMP**

Amended 7×: No. 654 (25.12.2015), No. 580 (28.12.2017), No. 581 (12.12.2018), No. 100 (19.02.2019), No. 348 (29.07.2019), No. 635 (31.12.2021), No. 422 (27.10.2023).
Related URLs **VERIFIED**: `https://matsne.gov.ge/ka/document/view/3129781` (Decree 654 amendment), `https://matsne.gov.ge/ka/document/view/5345381` (Decree 635 amendment).

**Government Decree No. 114 of 4 March 2022** — *stages and conditions for submitting the GMP document for products admitted (or intended for admission) under the national OR recognition regime*. Registration code 470200000.10.003.023315.
`https://matsne.gov.ge/ka/document/view/5402664` — **VERIFIED** · PDF `https://matsne.gov.ge/ka/document/download/5402664/0/ge/pdf` — **VERIFIED (Exa)**
- Acceptable GMP issuers: **WHO · EC · US FDA · PIC/S · Georgian national GMP** (issued by RAMA).
- **A GMP document IS required under the RECOGNITION regime**, effective **2 March 2022**. This closes the obvious loophole — recognition is fast, but not GMP-free.
- Enabling law amendment: Law No. 1394-VIIIმს-Xმპ of **17 February 2022** inserted Art. 11⁷(5)("ვ1") and Art. 11¹¹(19)("დ1"). `https://matsne.gov.ge/ka/document/download/5384486/0/ge/pdf` — **VERIFIED (Exa)**

**Amendment history / the live deadline problem:**
- Resolution **No. 99 of 27 March 2024** postponed mandatory GMP submission for national-regime procedures to **1 October 2024** *(source: Cratia newsletter — secondary)*.
- Amending decree at `https://legali.ge/law/6283961/` — **VERIFIED (Exa)** — adds para 1¹: **if the manufacturer's GMP certificate EXPIRES, the product's registration is SUSPENDED** and resumes only on submission of a valid one.
- **1 October 2025:** paragraph 3 of Decree 114 entered force — MAH/manufacturers must hold valid new-standard GMP for **both the finished dosage form AND the active substances**. Without it: no new MA, no renewal, no variation; existing national-regime registrations **suspended**; import of suspended products **prohibited**; wholesale of stock on market allowed to **1 April 2026**, retail thereafter to expiry. *(source: inpharmatis, `https://inpharmatis.com/new-gmp-regulations-in-georgia-key-deadlines-and-compliance-requirements/` — **VERIFIED (Exa)**, WebFetch got 403)*

**Site inspection:** No requirement for a RAMA inspection of the foreign manufacturing site was found in any primary text — the regime is **paper recognition of a foreign GMP certificate**. Georgia does inspect domestic manufacturers (national GMP). **I could not find a primary-source statement either way on foreign-site inspection — treat as UNVERIFIED.**

⚠️ One secondary source (inpharmatis) says Georgia "recognizes the standards of countries with stringent regulations, such as Japan, Iceland, Turkey, Australia, South Korea, and Israel." **This is not a sixth category** — every one of those countries is a **PIC/S participating authority**, so they are covered by the PIC/S limb of Decree 114. Don't cite it as a separate legal basis.

---

## 8. PUBLIC REGISTERS — mixed news

**Statutory duty exists.** Art. 11⁶ (Departmental Registry / უწყებრივი რეესტრი): it shall record *registration number, interested person, manufacturing country, brand name, INN, form, dosage, concentration, registration date, validity period, and an electronic version of packaging and labelling sample*; and Art. 11⁶(3): **"The Departmental Registry shall be a public document… kept in an electronic form and shall be made accessible through the internet."**

| URL | Status |
|---|---|
| `http://pharmacy.moh.gov.ge/Pages/Products.aspx` — the Departmental Registry, linked from RAMA nav as "ფარმაცევტული პროდუქტის უწყებრივი რეესტრი" | **UNVERIFIED.** DNS resolves (45.8.38.180) but **TCP connection times out**; browser navigation denied. Wayback holds only assets, no HTML capture of Products.aspx. Likely geo-restricted or offline during RAMA's "reconstruction". |
| `http://drugorders.moh.gov.ge/index.php?lang_id=GEO&sec_id=108` — registration orders archive, "from 4 April 2013" | **UNVERIFIED.** DNS resolves (45.8.38.160), TCP timeout. |
| `http://apps.ssa.gov.ge/recepti/Camlebi` — "წამლის საძიებელი" (drug finder) | **UNVERIFIED.** DNS resolves (45.8.38.254), TCP timeout. |

### ✅ THE ONE REGISTER THAT ACTUALLY WORKS — use this
**`https://referenceprice.moh.gov.ge/ui/#/main` — VERIFIED, LIVE, and far more useful than expected.**
- Angular app, **Georgian UI**, "განახლების თარიღი: **03.07.2026**", CSV/Excel download button (ჩამოტვირთვა).
- Working JSON API: `https://referenceprice.moh.gov.ge/api/api/refrenceprice/getDrugsMainPage?pageNumber=1` and `.../GetDrugCategories` — **VERIFIED, HTTP 200**.
- **`totalCount: 7794` records.** Per-record fields: `geoNDC` (**Georgian registration number**, e.g. `019803-2`), `inn`, `geoName` (Georgian trade name), `dose`, `formDetailGeo`, `packaging_DetailGeo`, `referalWholesalerPrice`, `unitReferalWholesalerPrice`, `referalRetailPrice`, `unitReferalRetailPrice`, `license_Company` + `license_Country` (**trade licence holder**), `tradeOwnerName` + `tradeCountryName`, `drugStatus`, `publishDate`.
- Sample record: `{geoNDC:"019803-2", inn:"doxycycline", geoName:"უნიდოქს სოლუტაბი", dose:"100mg", referalWholesalerPrice:4.63, referalRetailPrice:6.48, license_Company:"Astellas Pharma Sp. z.o.o.", license_Country:"პოლონეთი", drugStatus:"შესულია ძალაში", publishDate:"2025-11-29"}`

**This is your competitive-intelligence and freedom-to-operate tool**: it tells you, per INN, which products are already on the Georgian market, who holds the trade licence, from which country, and at what capped price. It is not the full Departmental Registry (only price-regulated products), but it is machine-readable and current.

---

## 9. FILING MECHANICS — paper-heavy, no eCTD

From Art. 11¹¹(c) (**VERIFIED**, English law text):
- **Administrative part: TANGIBLE (paper) form, in GEORGIAN.** Plus an electronic Georgian translation of the leaflet **in Word format on a CD**, plus packaging/marking samples.
- **Scientific-technical part: Georgian, Russian OR English**, **three identical copies**, electronic on CD, each CD labelled with trade name, manufacturer, trade licence holder, form/dosage, pack quantity, **registration regime**, and submission dates.

**eCTD: NO.** Cratia (regulatory consultancy, `https://cratia.com/en/countries/gruziya/registracziya-lekarstvennyh-sredstv/` — **VERIFIED via Exa**) states plainly: *"The dossier is submitted in the national format, the CTD format is not accepted."* — **secondary source, but consistent with the statutory CD-and-paper description.** The "Word on a CD" requirement in primary law is strong corroboration.

**Where to submit:** RAMA, Ak. Tsereteli Ave. 144, Tbilisi 0119 — Division of Drug Registration, Clinical Trials and Permits.

**Application forms — Minister's orders (links live on the VERIFIED RAMA page; PDFs not individually fetched):**
| Order | Subject | RAMA PDF |
|---|---|---|
| **N344/ნ of 23 Oct 2009** | **Recognition regime** application form + homology identification procedure | `https://rama.moh.gov.ge/res/docs/_N344ნ.pdf` |
| **N339/ნ of 20 Oct 2009** | **National regime** application form (mandatory since 1 Jan 2019) | `https://rama.moh.gov.ge/res/docs/_N339ნ.pdf` |
| **N325/ნ of 13 Oct 2009** | **Instructions for use / PIL** content requirements | `https://rama.moh.gov.ge/res/docs/_N325ნ.pdf` |
| **N417/ნ of 21 Dec 2009** | amends N344/ნ; confirms notarisation of copies NOT required; e-mockups accepted initially | `https://matsne.gov.ge/ka/document/view/88096` — **VERIFIED** |

⚠️ RAMA's own page is internally inconsistent on N344/ნ's date — it says both "23 ოქტომბერი" and "22 ოქტომბერი" 2009. matsne doc 88096 says **23 October 2009**. Confirm before citing.

---

## 10. RECOGNITION-REGIME DOSSIER (Art. 11⁷(5)) — "homology identification documents"

**VERIFIED from the English law text:**
- (a–d) Product identity: form, dosage, **labelling sample (original OR electronic)**, **authorised Georgian translation of the patient information leaflet + the original PIL**, **reference standard sufficient for 2 tests** (an active substance of the product may be substituted), **product sample — 2 standard packages**
- Period of the foreign marketing authorisation, and the **unique authorisation number**
- (e) **Certificate of a Pharmaceutical Product (CPP)** issued by a recognised foreign/international regulator — *may be issued for any market under that regulator's control*
- (f) **A CPP-equivalent document is acceptable in place of a CPP.** **Duly attested copies of either are acceptable.**
- (f¹) **GMP document** — original, copy, electronic document, **or "another publicly available form, with reference to the source"** (i.e. a link to a public EudraGMDP/FDA record can suffice)
- Test methods may be **printed from a public pharmacopoeia** with a source reference

**Language latitude:** homology identification documents may be in **Georgian, English or Russian** (per mkdlaw, `https://mkdlaw.ge/en/posts/98/importing-pharmaceutical-products-into-the-georgian-market-an-overview` — **VERIFIED**). Cratia adds that when the dossier and mockups are in **English, only the instructions for human use must be translated into Georgian**; if in another language, all administrative documents including packaging design must be translated and **notarised** — **secondary, unverified against primary text.**

---

## 11. GOTCHAS

**a) Labelling — recognition is genuinely lighter than national.**
RAMA's registration page attaches the marking technical regulation (**Government Decree No. 350 of 15 July 2015**) *only* to the **national regime** ("დაინტერესებულმა პირმა **ეროვნული რეჟიმით** რეგისტრაციისას უნდა გაითვალისწინოს, რომ ფარმაცევტული პროდუქტის მარკირება უნდა აკმაყოფილებდეს … N350 დადგენილებით…"). A matsne document title found in search confirms the framing: *"technical regulation — marking rules for pharmaceutical products **admitted by the national regime**"* (`https://www.matsne.gov.ge/ka/document/view/2912395` — **NOT FETCHED, title from search index only**).
➜ **Under recognition you can generally keep the foreign pack.** What you must produce in Georgian is the **authorised translation of the PIL** (Art. 11⁷(5)). Cratia notes the mockup must **match the pack approved in the reference country**.
⚠️ Cratia separately cites *"Order No. 337/N — Requirements for Labeling of Pharmaceutical Products Admitted under the National State Registration Regime"*, which conflicts with Decree N350. **Both UNVERIFIED against each other — resolve with RAMA.**

**b) Batch release / QP:** **No Georgian batch-release or QP requirement was found in any source I retrieved.** Absence of evidence, not evidence of absence — **UNVERIFIED, ask RAMA directly.**

**c) PRICE REGULATION — this is the biggest commercial gotcha.**
- **Government Ordinance No. 593 of 27 December 2020** sets the methodology for state price regulation (`https://gratanet.com/publications/reference-pricing-for-pharmaceuticals-in-georgia` — **VERIFIED via Exa**; the ordinance number is from this secondary source, **I did not open the decree itself — treat No. 593 as UNVERIFIED**).
- Law defines **reference retail price** and **reference wholesale price** as *maximum* GEL prices (Art. 2, paras 22¹/22²), and a **public reference price catalogue** on the Ministry website (Art. 2, para 27¹). Art. 3(11): the Government approves the pricing methodology. **VERIFIED in law text.**
- **External reference countries: Latvia, Montenegro, Bulgaria, North Macedonia.** Wholesale reference = arithmetic average of average wholesale prices (ex-VAT) of comparable products in those four.
- Two price tiers: **original** vs **generic/biosimilar**. Exception only where **no therapeutic alternative exists on the Georgian market**.
- Revised **annually, published in November**, effective **1 month after publication** — consistent with the live portal (`publishDate: 2025-11-29`, update 03.07.2026).
- **Penalty for breaching reference prices: GEL 5,000–30,000.**
- For patent-protected expensive originals, **Managed Entry Agreements (MEA)** apply — Art. 3(12) empowers the Government to approve MEA categories. **VERIFIED in law text.**
➜ For an off-patent generic, you will be priced against **Latvia/Montenegro/Bulgaria/North Macedonia generic averages**. Model this *before* filing.

**d) "Para 3" / import bypassing registration — I found the actual provision, and it is narrower than the rumour.**
**Article 11¹³ — "Exceptional cases of importing pharmaceutical products circumventing the regimes for granting a marketing authorisation in Georgia."** **VERIFIED (English law text).** Import without any Georgian MA is permitted **for NON-COMMERCIAL purposes only**, in these cases:
> (a) pre-clinical and clinical trials · (b) **registration — as a sample** · (c) **individual needs of a natural person** · (d) exhibition/symposium/conference/forum/congress — as a sample, **no right to sell** · (e) re-export · (f) customs warehouse/terminal storage or transit · (g) **bulk pharmaceutical product intended for local manufacturing** · (h) **"under particular circumstances (a natural disaster, mass injury of the population, epidemic, RARE DISEASE) for humanitarian purposes, as well as in the case of a special state interest, with the consent of the Ministry"**

🎯 **Art. 11¹³(h) names "rare disease" explicitly.** This is a named-patient / humanitarian channel requiring **Ministry consent**, and it is **non-commercial**. It is a bridge for early access — **not** a commercial market-entry route. Anyone telling you Georgia lets you sell foreign-registered drugs without registering is conflating this with the recognition regime.

**e) Parallel import / different packaging — Article 11⁸.** Notification-only, **no re-registration**, for first-time import of a product already authorised in Georgia but **differently packaged/labelled**, where that pack is authorised by a Decree-188-listed regulator. **RAMA adds it to the Departmental Registry within 5 working days**; deficiency cure up to 15 days; RAMA may refuse only on **factual grounds**, in writing. The differently-packaged entry rides on the parent authorisation's expiry. **VERIFIED (law text + RAMA page).**
➜ Relevant if a competitor already registered your molecule — you may be able to enter on a **notification** rather than a registration.

**f) Variation timelines — PRIMARY vs REGULATOR CONFLICT. Do not rely on either without checking.**

| Variation | Law text (Art. 11¹¹(9), matsne EN) | RAMA website |
|---|---|---|
| Type II | 3 months | 3 months ✅ |
| **Type I A** | **20 calendar days** | **10 days** ❌ |
| **Type I B** | **40 calendar days** | **1 month** ❌ |
| Re-registration | 2 months | 2 months ✅ |

The RAMA page appears to predate a law amendment. **The Law prevails; confirm with RAMA.**

**g) Re-registration must be filed no later than 2 months before expiry** (RAMA — **VERIFIED**), with 5 years of adverse-event data, publications and bibliography.

**h) Sample replacement rules exist** for products admitted under either regime: `https://matsne.gov.ge/ka/document/view/4979931/0` — **NOT FETCHED**, title only.

---

## 12. STRATEGIC READ FOR AN OFF-PATENT RARE-DISEASE REPURPOSING PLAY

1. **Recognition is the pathway — if and only if you already hold an MA in a Decree-188 country.** 7 working days, 500 GEL, no scientific re-review, **no Georgian legal entity required**, foreign pack retained, only the PIL translated. This is one of the cheapest and fastest legitimate market entries anywhere.
2. **If you don't hold a listed-country MA, recognition is closed to you** and national regime applies — 3 months, 500 GEL for a generic, but **paper dossier in Georgian, three CD copies, no eCTD**, and the applicant must be **the manufacturer or the trade licence holder** (not a local distributor).
3. **GMP is the actual gate, not the timeline.** Since 1 Oct 2025 you need valid **WHO / EC / US FDA / PIC/S / Georgian** GMP covering **finished product AND API**, with a live expiry date. An expired certificate **suspends the registration automatically**. For repurposed off-patent generics sourced from India/China CMOs, this is where deals die — those countries are outside both Decree 188 and (mostly) PIC/S coverage.
4. **Price is set for you** against Latvia/Montenegro/Bulgaria/North Macedonia generic averages. Model revenue from the live reference-price API before committing.
5. **Art. 11¹³(h) rare-disease humanitarian import** is a real, statutorily named bridge for pre-registration patient access with Ministry consent — non-commercial.
6. **Because RAMA's registry is unreachable and the site is "under reconstruction," write to `regagency@moh.gov.ge`** (attn. Division of Drug Registration, Clinical Trials and Permits) to (i) obtain the current consolidated Decree 188 list and settle the Croatia question, (ii) confirm Art. 7 §6 fees are current, (iii) get the N344/ნ recognition application form, (iv) confirm whether foreign-site inspection or batch release is ever required, and (v) ask for Departmental Registry access.

---

## 13. COMPLETE URL LEDGER

### VERIFIED — fetched and returned relevant content
| URL | Method | Language | What it gave |
|---|---|---|---|
| `https://matsne.gov.ge/en/document/view/29836` | WebFetch ×3 | EN | Law on Medicines — Arts. 11⁴, 11⁶, 11⁷, 11⁸, 11¹¹, 11¹³ |
| `https://matsne.gov.ge/ka/document/view/4606?publication=0` | WebFetch ×2 | KA | **Decree No. 188 (22.10.2009) — country list** |
| `https://matsne.gov.ge/ka/document/view/16054` | WebFetch ×2 | KA | **Law on Registration Fees — Art. 7 §6, all GEL amounts** |
| `https://matsne.gov.ge/ka/document/view/5402664` | WebFetch | KA | **Decree No. 114 (04.03.2022) — GMP stages** |
| `https://matsne.gov.ge/ka/document/download/5402664/0/ge/pdf` | Exa | KA | Decree 114 PDF text |
| `https://matsne.gov.ge/ka/document/view/1100741` | WebFetch | KA | **Decree No. 349 (16.11.2010) — GMP standards list** |
| `https://matsne.gov.ge/ka/document/view/3129781` | WebFetch | KA | Decree 654 (25.12.2015) amending 349 |
| `https://matsne.gov.ge/ka/document/view/5345381` | WebFetch | KA | Decree 635 (31.12.2021) amending 349 |
| `https://matsne.gov.ge/ka/document/view/88096` | WebFetch | KA | **Order N417/ნ (21.12.2009) amending N344/ნ** |
| `https://matsne.gov.ge/ka/document/download/5384486/0/ge/pdf` | Exa | KA | Law No. 1394 (17.02.2022) — GMP into Arts. 11⁷/11¹¹ |
| `https://rama.moh.gov.ge/` | Browser | KA | Agency name; "under reconstruction" |
| `https://rama.moh.gov.ge/geo/static/464/farmatsevtuli-produqtis-registratsia` | Browser | KA | **Best single official source: both regimes, timelines, all order/decree numbers, parallel import** |
| `https://rama.moh.gov.ge/geo/contact/4/kontaqti` | Browser | KA | **Address, phone, regagency@moh.gov.ge** |
| `https://rama.moh.gov.ge/geo/static/503` | Browser | KA | **Named division + head** |
| `https://rama.moh.gov.ge/geo/static/471/...instruqtsiebi` | Browser | KA | Registration orders index (data only to 2013) |
| `https://moh.gov.ge/` | Browser | KA | Ministry site; link to reference price portal |
| `https://referenceprice.moh.gov.ge/ui/#/main` | Browser | KA | **LIVE database, 7,794 records** |
| `https://referenceprice.moh.gov.ge/api/api/refrenceprice/getDrugsMainPage?pageNumber=1` | Browser fetch | KA/EN | **Working JSON API, HTTP 200** |
| `https://picscheme.org/en/members` | WebFetch | EN | **60 PIC/S authorities — Georgia ABSENT** |
| `https://mkdlaw.ge/en/posts/98/importing-pharmaceutical-products-...` | WebFetch | EN | Law firm overview; fees, 7 business days |
| `https://inpharmatis.com/new-gmp-regulations-in-georgia-key-deadlines-...` | Exa (WebFetch 403) | EN | Oct 2025 GMP cliff, Apr 2026 sell-through |
| `https://inpharmatis.com/in-georgia-pharmaceutical-companies-that-have-not-provided-a-gmp-certificate...` | Exa | EN | GMP suspension letters, MAH duties |
| `https://gratanet.com/publications/reference-pricing-for-pharmaceuticals-in-georgia` | Exa | EN | **Reference pricing: 4 comparator countries, penalties** |
| `https://legali.ge/law/6283961/` | Exa | KA | Amendment to Decree 114 — expiry ⇒ suspension |
| `https://cratia.com/en/countries/gruziya/registracziya-lekarstvennyh-sredstv/` | Exa | EN | **"CTD format is not accepted"**; language rules |
| `https://mspcorporate.com/registration-medicinal-products-georgia.html` | Exa | EN | Document lists, legalised PoA practice |
| `https://cratia.ua/en/regulatory-newsletter-for-cis-and-eaeu/` | Exa | EN | Resolution No. 99 (27.03.2024) GMP postponement |
| `https://www.biomapas.com/running-a-clinical-trial-in-georgia/` | Exa | EN | Agency English name, CT requirements |
| `https://legal.ge/en/service/healthcare-and-pharmaceutical-law-en/clinical-trial-approval-en` | Exa | EN | CT approval, Georgian-language rules |

### UNVERIFIED — could not retrieve
| URL | Failure |
|---|---|
| `http://pharmacy.moh.gov.ge/Pages/Products.aspx` | **The Departmental Registry.** DNS 45.8.38.180; TCP timeout ×2; browser denied; no HTML in Wayback |
| `http://drugorders.moh.gov.ge/index.php?lang_id=GEO&sec_id=108` | DNS 45.8.38.160; TCP timeout; browser denied |
| `http://apps.ssa.gov.ge/recepti/Camlebi` | DNS 45.8.38.254; TCP timeout |
| `https://www.moh.gov.ge/en/` | **404** — English MoH site gone |
| `https://www.moh.gov.ge/en/news/3943/GMP-standard-is-introduced-...` | **404** |
| `https://rama.moh.gov.ge/geo/static/105/dadgenilebebi` | 403 (WebFetch), Exa CRAWL_UNKNOWN_ERROR — not retried in browser |
| `https://rama.moh.gov.ge/` via curl / WebFetch / Exa | **403 Cloudflare managed challenge** (works in browser) |
| `https://web.archive.org/web/2022/http://pharmacy.moh.gov.ge/Pages/Products.aspx` | WebFetch blocked from web.archive.org; MCP hit HTTP 429 |

### NOT FETCHED — exist in matsne/RAMA indexes, worth pulling next
`https://matsne.gov.ge/ka/document/view/29836` (KA law) · `https://matsne.gov.ge/ka/document/view/2912395` (marking tech. reg., national regime) · `https://matsne.gov.ge/ka/document/view/4979931/0` (sample replacement) · `https://matsne.gov.ge/ka/document/view/4682879` (recognition + different packaging) · `https://matsne.gov.ge/ka/document/view/4617056` (CT/manufacturing/pharmacy/controlled-substance permits) · `https://matsne.gov.ge/ka/document/view/53704` (quality assurance regulation) · `https://www.wipo.int/wipolex/en/text/548941` · RAMA PDFs: `_N344ნ.pdf`, `_N339ნ.pdf`, `_N325ნ.pdf`

---

## 14. EXPLICITLY UNVERIFIED — DO NOT REPRESENT AS FACT
- **Croatia / Liechtenstein absence** from Decree 188 — apparent, but could be an extraction gap.
- **Ordinance No. 593 of 27.12.2020** (pricing methodology) — number from a law-firm article; decree not opened.
- **Resolution No. 99 of 27.03.2024** (GMP postponement) — from Cratia newsletter only.
- **Art. 11⁸ parallel-import notification fee** — my extraction was ambiguous.
- **Whether RAMA ever inspects a foreign manufacturing site** — no primary text found either way.
- **Batch release / QP requirement** — nothing found; not the same as confirmed absence.
- **Order N337/N vs Decree N350** for national-regime labelling — sources conflict.
- **N344/ნ date** — RAMA's own page says both 22 and 23 October 2009.
- **Type I A/B variation timelines** — law and regulator disagree.
- **Current total number of medicines registered in Georgia** — registry unreachable; the 7,794 reference-price records are price-regulated products, **not** the full register.
- I did **not** verify importer/wholesale licence conditions, customs procedures, or pharmacovigilance obligations to primary-source level.

**Single highest-value next action:** email **regagency@moh.gov.ge** (Division of Drug Registration, Clinical Trials and Permits, RAMA, Ak. Tsereteli Ave. 144, Tbilisi 0119; +995 32 251 00 11 ext. 12-11) in **Georgian**, requesting the current consolidated Decree 188 list, the N344/ნ form, and Departmental Registry access.