<!-- RECOVERED from subagent transcript agent-acb35431faca4fc7d.jsonl, session fd64561f-7c90-41a2-95cf-b4a133a8fe0f, research date 2026-08-05.
     Single-country agent, UKRAINE. Parent (agent 2) was interrupted before synthesis; this is the child's verbatim deliverable.
     Verbatim agent deliverable — not re-edited. -->

I have comprehensive primary-source verification. Here are my findings.

---

# UKRAINE — PHARMACEUTICAL REGISTRATION PATHWAYS FOR RELIANCE/RECOGNITION
**Research date: 5–6 August 2026.** All legal text below was read from the *actual fetched document text*, not from summaries, unless flagged otherwise.

**Method note:** WebSearch budget was exhausted mid-research; the majority of findings come from direct `curl` fetches of primary legal texts (zakon.rada.gov.ua print views) and regulator sites, which I parsed and quoted. `moz.gov.ua` is behind Cloudflare bot protection and returned **403 to every automated request** — everything I would have taken from MoZ I sourced from zakon.rada.gov.ua (official) or dec.gov.ua instead.

---

## 1. INSTITUTIONS

### 1.1 State Expert Center (SEC / ДЕЦ) — the expert body
| Field | Value |
|---|---|
| Full legal name (UA) | Державне підприємство «Державний експертний центр Міністерства охорони здоров'я України» |
| English (self-styled, from site metadata) | State Expert Center of the Ministry of Health of Ukraine |
| Legal address | 03057, м. Київ, Шевченківський район, вул. Антона Цедіка, буд. 14 |
| Actual/operating address | 03057, м. Київ, Солом'янський район, вул. Сім'ї Бродських, буд. 10 (вул. Смоленська, 10) |
| Switchboard | +38 (044) 202-17-00 |
| Service centre (Сервісний центр) | +38 (044) 202-17-05 |
| Accounting (Бухгалтерія) | +38 (044) 202-17-06 |
| **"Single window" (Єдине вікно)** | **+38 (044) 202-17-09** ← submission desk |
| General email | dec@dec.gov.ua |
| eCTD technical support | ectd@dec.gov.ua |
| Site support | support@dec.gov.ua |

- `https://www.dec.gov.ua/` — **VERIFIED** (HTTP 200). ⚠️ **TLS gotcha:** the certificate chain is incomplete — standard clients throw `unable to verify the first certificate`. I had to use `curl -k`. Browsers generally cope; automated tooling will not.
- `https://www.dec.gov.ua/contact-page/` — **VERIFIED** (200), full departmental phone directory + downloadable .xlsx.
- Legacy URLs (`/kontakty/`, `/pro-nas/`) **404** — site was re-platformed; old deep links are dead.

**Structurally relevant:** DEC's own news pages confirm an EU **Twinning project to create "Укрфармагентство"** (an independent Ukrainian Pharmaceutical Agency) — this is the new "орган державного контролю" (state control body) that Law 2469-IX requires the Cabinet to establish before the law becomes operative. Today's split (MoH decides / DEC evaluates) collapses into a single agency.

### 1.2 Ministry of Health (MOZ)
- `https://moz.gov.ua/` — **UNVERIFIED — blocked.** Returns **HTTP 403** ("Just a moment…" Cloudflare challenge) to every automated fetch, including with full browser headers. Individual `moz.gov.ua/uk/decrees/...` order pages also 403.
- Role under current law: MoH issues the registration decision (order) and the registration certificate. DEC performs the expertise/review and issues the *висновок* (conclusion).

### 1.3 State Service on Medicines and Drugs Control (Держлікслужба / SMDC)
| Field | Value |
|---|---|
| Name (UA) | Державна служба України з лікарських засобів та контролю за наркотиками |
| English | State Service of Ukraine on Medicines and Drugs Control (SMDC) |
| Address | 120-A Beresteiska Avenue, Kyiv 03115 |
| Phone | +380 (44) 422-55-77 (General Administration); +380 (44) 422-55-73 (Head's office) |
| Email | dls@dls.gov.ua |
| Hours | Mon–Thu 08:00–17:00; Fri 08:00–15:45; lunch 12:00–12:45 |

- `https://www.dls.gov.ua/` and `https://www.dls.gov.ua/en/contacts/` — **VERIFIED** (200). Full English site.
- Role: **GMP compliance confirmation** (Certificate or Conclusion), manufacturing licences, **import licences**, wholesale/retail licensing, quality control, market surveillance.

---

## 2. LAW No. 2469-IX — THE ACTUAL TRANSITION TIMELINE ⚠️ CRITICAL

**Source:** full text fetched from `https://zakon.rada.gov.ua/laws/show/2469-20/print` — **VERIFIED** (200, 793 KB, 1,765 lines parsed). Status line on page: *"станом на 06.08.2026 — чинний"*, редакція від 05.06.2025.

**Identification:** Закон України «Про лікарські засоби» від 28.07.2022 № 2469-IX. Signed by President Zelensky, Kyiv, 28 July 2022.
**Publications:** Голос України 18.08.2022 № 169 · Урядовий кур'єр 31.08.2022 № 188 · Офіційний вісник України 02.09.2022, № 68, ст. 4068.

### 2.1 Entry into force — the two-step Ukrainian construct

Ukrainian law distinguishes **набрання чинності** ("entry into force") from **введення в дію** ("putting into operation"). Both matter and they are 4.5 years apart here.

> **Розділ XI. ПРИКІНЦЕВІ ПОЛОЖЕННЯ, п. 1:**
> «Цей Закон **набирає чинності з дня його опублікування та вводиться в дію з 1 січня 2027 року**, крім:»
> *{Абзац перший пункту 1 розділу XI **в редакції Закону № 4239-IX від 12.02.2025**}*

- **набрання чинності = 18 August 2022** (day of publication in Голос України).
- **введення в дію = 1 January 2027.**

**⭐ The amending law you asked for: Law of Ukraine No. 4239-IX of 12 February 2025** is what set the current 1 January 2027 date. This is stated explicitly in the redaction note under п.1. (`https://zakon.rada.gov.ua/laws/show/4239-20` — **VERIFIED**, title *"Про внесення змін до деяких… від 12.02.2025 № 4239-IX"*.)

Independent corroboration: **CMU Resolution No. 687 of 27 May 2026** (National List of Essential Medicines) is itself stated to enter into force on 1 January 2027 "simultaneously with the putting into operation of Law 2469-IX" — confirming the government is planning to 1 Jan 2027.

### 2.2 The staggered exceptions (verbatim from п.1)

| Provision | Operative from |
|---|---|
| **The Law generally** | **1 January 2027** *(per Law 4239-IX, 12.02.2025)* |
| Art. 10(16) para 2; Art. 42(2); **Arts. 46, 50, 57**; Art. 74(5) | **1 January 2028** *(per Law 4239-IX, 12.02.2025)* |
| **Art. 13(6) — mandatory eCTD** | **three years from publication → 18 August 2025** *(already operative)* |
| Art. 15(1) para 2 | 30 months from publication (≈18 Feb 2025); lapses when Art. 13(6) kicks in |
| Art. 2(1) pts 16, 19; Art. 72(1) pt 2; Art. 73 (except pt 1(1),(2)); **Art. 78 (parallel import)** | **1 January 2025** *(added by Law № 3860-IX of 16.07.2024)* |
| Art. 78(1) para 6 | From entry into force of Ukraine's EU accession treaty, not earlier than Art. 57 |

**Full amending-law chain on the law's card (VERIFIED):** № 3345-IX (23.08.2023), **№ 3860-IX (16.07.2024)**, № 3911-IX (21.08.2024), **№ 4239-IX (12.02.2025)**, № 4454-IX (15.05.2025). A further amendment by № 3860-IX is flagged as pending at a later date.

### 2.3 What happens on 1 January 2027
- **Old Law 123/96-ВР «Про лікарські засоби» is REPEALED** (п.2 Прикінцевих положень), together with the VR Resolution on its implementation. Everything built on it — including CMU Resolution 376 and MoH Orders 426/1245 in their current form — must be replaced.
- A **new CMU state registration procedure "adapted to EU legislation"** must be adopted (Art. 13(3)); MoH must set dossier content/forms/expertise procedure adapted to EU law (Art. 13(4)).
- The Cabinet must **create and fund the new state control body** and appoint its head by open competition (п.6 Прикінцевих положень) → Укрфармагентство.

### 2.4 GRANDFATHERING — verbatim, Розділ XII ПЕРЕХІДНІ ПОЛОЖЕННЯ

> **п.1:** «реєстраційне посвідчення… яке видано **до набрання чинності цим Законом** та має обмежений строк дії, є чинним протягом строку, зазначеного у цьому посвідченні.
> Реєстраційне посвідчення… яке видано до набрання чинності цим Законом та має **необмежений строк дії, є чинним… безстроково**. Таке реєстраційне посвідчення замінюється на **витяг із Державного реєстру** за заявою власника реєстрації (представника в Україні) **безоплатно протягом п'яти років** з дня набрання чинності цим Законом. Витяг видається **без внесення змін до реєстраційних матеріалів та/або без вимог щодо надання додаткових матеріалів**.»

> **п.2:** «лікарські засоби, зареєстровані в Україні до набрання чинності цим Законом, **можуть вводитися в обіг протягом п'яти років** з дня набрання чинності цим Законом та знаходитися в обігу **до завершення строку їх придатності** відповідно до законодавства, що діяло до набрання чинності цим Законом, **без застосування щодо них заборон чи обмежень** з таких причин.»

> **п.5(1):** «власники реєстрації **протягом п'яти років з дня введення в дію цього Закону** мають привести реєстраційні матеріали… **маркування, пакування** у відповідність із цим Законом»

**Reading these against the dates:**

| Obligation | Anchor used in the text | Deadline on a literal reading |
|---|---|---|
| Replace unlimited-term MA certificate with a Register extract (free) | набрання чинності (18.08.2022) | **18 August 2027** |
| Placing pre-existing registered products on the market | набрання чинності (18.08.2022) | **18 August 2027**, then sell-through to expiry |
| Bring dossier + labelling + packaging into conformity with the new Law | **введення в дію (01.01.2027)** | **1 January 2032** |

**⚠️ FLAGGED AMBIGUITY — DO NOT PLAN AROUND THIS WITHOUT UKRAINIAN COUNSEL.** Points 1 and 2 anchor to *набрання чинності* (18.08.2022), which produces an 18 August 2027 deadline that falls **7.5 months after the law even becomes operative**. That is almost certainly a legacy of the original drafting (when entry into force and operation were not split), and it has not been corrected by any of the five amending laws I checked. Some secondary commentary I encountered reads п.2 as "until 18 August 2027"; others treat the five years as running from 1 January 2027 (→ 2032). **The statute as written says 18.08.2022 + 5 years. I could not find an authoritative MoH/DEC clarification resolving this.** Treat 18 August 2027 as the conservative planning date for the Register-extract swap.

**Net answer: YES, grandfathered.** No re-registration is triggered by the new Law. Unlimited-term MAs survive indefinitely; they are simply re-papered as a Register extract, free, with no dossier changes and no additional materials. The real cliff is the **dossier/labelling/packaging conformity obligation**, not the MA itself.

### 2.5 Registration term under the new law (Art. 35 — VERIFIED)
- First registration: **5 years**.
- Re-registration application due **not later than 9 months** before expiry.
- Re-registration decision within **210 calendar days**; outcome is either **indefinite (безстроковий) extension** if benefit/risk is favourable, or a further 5 years for justified pharmacovigilance reasons, or refusal.
- Products released to market during a valid registration stay in circulation to shelf-life expiry (Art. 35(10)).

### 2.6 Other new-law provisions that matter to a repurposing company
- **Art. 23 — Well-established use (bibliographic) registration.** No preclinical/clinical results required if the API has ≥10 years' well-established use **in Ukraine or an EU/EEA-EFTA state**, with recognised efficacy and acceptable safety; literature substitutes. This is Ukraine's transposition of Art. 10a of Directive 2001/83/EC — **the single most relevant route for off-patent repurposing**.
- **Art. 24 — Registration under obligations / in exceptional circumstances**, expressly covering (1) serious debilitating or life-threatening diseases, (2) public-health emergencies, **(3) orphan medicinal products**.
- **Art. 41 — Data exclusivity: 5 years** (+1 year if a significantly-beneficial new indication is registered in the first 3 years), with the "8+2+1" EU model **not** adopted. Applies where the reference MA application was filed in Ukraine within 2 years of first registration anywhere. Favourable to generics vs. the EU.
- **Art. 116 — Equivalence assessment of national regulatory systems.** The state control body may assess (documentary review) another country's regulatory system; if equivalent, MoH adds it to the **SRA list**. Conducted in cooperation with EMA and EU member state authorities. This is the new law's formal reliance mechanism.

---

## 3. THE VERIFICATION / FAST-TRACK PROCEDURES

There are **three distinct** procedures, frequently conflated in secondary sources. Both live ones are still running in 2026.

### 3.1 ⭐ The "recognition" route (спрощена процедура) — MoH Order No. 1245

**Legal instrument (VERIFIED, full text read from `https://zakon.rada.gov.ua/laws/show/z1619-16/print`):**

> **Наказ МОЗ України від 17.11.2016 № 1245** — «Про затвердження **Порядку розгляду реєстраційних матеріалів** на лікарські засоби, що подаються на державну реєстрацію (перереєстрацію), та матеріалів про внесення змін до реєстраційних матеріалів протягом дії реєстраційного посвідчення на лікарські засоби, які зареєстровані компетентними органами **Сполучених Штатів Америки, Великої Британії, Швейцарської Конфедерації, Японії, Австралії, Канади**, лікарських засобів, що **за централізованою процедурою зареєстровані компетентним органом Європейського Союзу**»

Registered at MoJ 22.12.2016 under № 1619/29749. Issued under Art. 9 of Law 123/96-ВР and CMU Resolution 376.

**Amending orders (VERIFIED from the document header):** № 1202 of 02.10.2017 · № 1391 of 15.06.2020 · **№ 1613 of 24.10.2025** (as itself amended by № 1736 of 17.11.2025). Current consolidated version on zakon.rada dated **09.12.2025** (basis z1649-25).

**⭐ Reference regulator list — EXACT, current:**
1. **USA (FDA)**
2. **United Kingdom (Велика Британія)** ← **added by the 2020/2025 amendments; post-Brexit addition. Many consultancy pages and even DEC's own contract-template page still omit the UK.**
3. **Switzerland (Swissmedic)**
4. **Japan (PMDA)**
5. **Australia (TGA)**
6. **Canada (Health Canada)**
7. **EU — centralised procedure (EMA)**

Note: **Health Canada, PMDA and TGA are in; a national EU member-state MA is NOT** (only the EU centralised procedure) for this route. Products must be *registered by and applied on the territory of* those countries.

**Statutory timeline (verbatim):**
| Step | Statutory period |
|---|---|
| DEC concludes contract with applicant | ≤ **14 calendar days** from applicant's approach |
| DEC issues invoice | **7 working days** |
| Applicant submits materials after MoH referral letter | within **90 calendar days**, else product withdrawn from consideration |
| **DEC review of registration materials** | **«Строк розгляду реєстраційних матеріалів не може перевищувати 10 робочих днів»** |
| DEC notifies applicant of completion + issues draft MA/QC/labelling/PIL for editorial agreement | **2 working days** |
| Applicant's editorial agreement time | **excluded from the clock** |
| **MoH decision (order) on registration or refusal** | **7 working days** from receipt of DEC conclusion |
| DEC prepares MA and transmits to MoH for signature | **2 working days** |
| Applicant's response to DEC queries | up to **30 working days**; **clock stops** |

Realistic elapsed time is therefore materially longer than "10 days" — contracting, invoicing, payment, editorial agreement and any deficiency round all sit outside the statutory clock.

**Substantive scope (from CMU Res. 376, п.19, as amended by CMU Res. № 1351 of 22.10.2025):**
> «Під час розгляду реєстраційних матеріалів… **експертиза матеріалів реєстраційного досьє, поданого регуляторному органу країни, де такий лікарський засіб зареєстрований, не проводиться.**»

No expert assessment of the foreign dossier. In place of the standard п.13(1)–(6) document set you file only:
1. Derzhliksluzhba GMP document **OR** a written manufacturer undertaking (see §6.2)
2. QC methods
3. Package artwork + primary/secondary labelling text in the required language
4. The foreign registration dossier, with country/authority/date of registration, certified by applicant or authorised representative
5. PIL in the required language
6. Proof of payment of the state registration fee

**MA validity:** 5 years; after re-registration, **unlimited**, except where MoH orders an additional re-registration after 5 years for justified pharmacovigilance reasons (Order 1245 п.11; mirrored in CMU 376 п.52).

**⭐ STATUS IN 2026 — STILL LIVE, EVIDENCE:**
- DEC publishes **2026 contract templates** for this procedure, including a dedicated bilingual **Ukrainian-English contract for foreign applicants** — page updated **24.07.2026**. `https://www.dec.gov.ua/materials/dogovori-shhodo-rozglyadu-re-straczijnih-materialiv-na-likarski-zasobi-sproshhena-proczedura/` — **VERIFIED** (200).
- Order 1245 was substantively amended as recently as **24.10.2025 / 17.11.2025** — a regulator does not amend a dead procedure.
- CMU Res. 376's п.19 was rewritten by **CMU Res. № 1351 of 22.10.2025**.

**What replaces it:** From 1 January 2027, Law 2469-IX supersedes the whole architecture. The successor is the **SRA construct**: Art. 25 (separate registration procedure), **Art. 27 (30-day decision)**, and Art. 116 (equivalence assessment → SRA list). See §3.4.

### 3.2 The authenticity-verification route (перевірка на автентичність) — procurement only

**Legal instrument:** **Наказ МОЗ України від 15.06.2020 № 1391** — English title confirmed verbatim from DEC's own eCTD FAQ: *"On approval of Procedure for checking authenticity of registration materials pertinent to medicinal product that is submitted for state registration for the purpose of its procurement by a person authorized for health care procurement or a specialized procurement organization."*
**Amended by MoH Order № 192 of 03.02.2025.**
⚠️ I could **not** fetch Order 1391's or Order 192's own full text (moz.gov.ua 403). Order numbers/dates are corroborated by DEC's FAQ, CMU Res. 376's cross-references and search-result metadata — but the *text* is **UNVERIFIED**.

**This route is only available for medicines being procured by the state procurement agency or an international specialised procurement organisation.** It is not a general commercial pathway. Its substantive rules are in **CMU Res. 376 п.7, 7-1, 21, 21-1, 21-2, 22, 23-1** — which I read in full.

**Timelines (verbatim from CMU Res. 376):**
| Case | Period |
|---|---|
| Authenticity check of materials under п.21 / 21-1 | **≤ 7 working days** from submission *(п.21-2, added by CMU № 1351 of 22.10.2025)* |
| MoH decision on procured medicines after authenticity check | **≤ 5 working days** *(п.26)* |
| Post-tender-award registration: authenticity check **+** decision, combined | **≤ 30 calendar days** |
| Full expertise for procured medicines (any manufacturer country) | **≤ 30 working days** |

Again: *«Під час перевірки реєстраційних матеріалів на їх автентичність експертиза матеріалів реєстраційного досьє… не проводиться.»*

**Eligible bases for this route (verbatim, CMU 376 п.7/п.1 of fees section):** registered by the competent authority of **USA, United Kingdom, Switzerland, Japan, Australia, Canada, an EU member state**, or **EU centralised**; **OR** in the **PEPFAR** procurable-medicines database on the FDA website; **OR** holding an **FDA Tentative Approval**; **OR** on the **WHO prequalification** lists and manufactured at the site listed there on the application date.

**Live in 2026 — EVIDENCE:** DEC publishes rolling *"Переліки ЛЗ, на які завершено експертизу щодо автентичності реєстраційних матеріалів"*. Most recent entries: **13.07.2026** (published 20.07.2026) and **09.07.2026** (published 10.07.2026), plus 27.03.2026, 10.03.2026, 20.01.2026. `https://www.dec.gov.ua/applicant/perelikiv-lz-na-yaki-zaversheno-ekspertizu-shhodo-avtentichnosti-re-straczijnih-materialiv/` — **VERIFIED** (200).

### 3.3 WHO Prequalification / international-organisation procurement

**Covered by CMU Res. 376 п.21-1**, inserted by **CMU Resolution № 1351 of 22.10.2025** — a genuinely new, dedicated WHO-PQ track. For a WHO-prequalified product being procured by the authorised procurement person, you file instead of the standard set:
1. The dossier materials **submitted for WHO prequalification**, with all variations
2. QC methods for the finished product
3. **The WHO assessment report**
4. PIL/product information **in the original (non-Ukrainian) language**
5. Package artwork + labelling text in the original language
6. **Ukrainian translations** of labelling and PIL, certified by signature of the applicant or authorised representative

Authenticity check: **≤ 7 working days** (п.21-2). **State registration fee: NIL** (see §6.5).

Procurement is executed under agreements between MoH and specialised procurement organisations — Law 2469-IX Art. 25(2) requires the separate procedure to respect the Public Procurement Law. The named organisations (UNDP / Crown Agents / UNICEF) are designated by separate CMU acts which I did **not** verify.

### 3.4 ⭐ What the new law replaces this with — and why it is *better* for rare disease

**Art. 2(1) pt 37 — definition of SRA (verbatim):**
> «країни із строгими регуляторними органами (Stringent Regulatory Authorities (SRAs) — країни, які відповідають одному із таких критеріїв:
> — країни, регуляторні органи яких **до 23 жовтня 2015 року були членами або спостерігачами ICH**;
> — країни, які уклали з Україною або з Європейським Союзом **угоду про взаємне визнання (MRA)** у сфері лікарських засобів;
> — країни, які уклали з Україною або з ЄС **угоду про оцінку відповідності та прийнятність промислових товарів (ACAA)** у сфері лікарських засобів.
> **Перелік країн із SRAs… затверджується та… оновлюється** центральним органом виконавчої влади [МОЗ]»

The pre-23-Oct-2015 ICH members/observers criterion is the WHO's own SRA definition — it captures the EU/EEA, USA, Japan, Switzerland, Canada, Australia, Norway, Iceland, Liechtenstein.

**⚠️ UNVERIFIED — could not confirm:** whether MoH has yet issued the order **approving the SRA list**. I found no such order. This is a live gap: the SRA list is the load-bearing element of the entire post-2027 reliance architecture, and I have no evidence it exists yet.

**⭐ Art. 27 — Special registration timelines (verbatim, VERIFIED):**
> «Рішення за заявою про державну реєстрацію (перереєстрацію) **орфанних лікарських засобів**, інноваційних лікарських засобів, лікарських засобів передової терапії, лікарських засобів для профілактики та/або лікування ВІЛ, лікування гемофілії, **онкологічних захворювань**, вакцин, **зареєстрованих у країнах із строгими регуляторними органами (SRAs) або Європейським агентством з лікарських засобів (ЕМА)**… приймається органом державного контролю **не пізніше ніж за 30 днів** після отримання ним відповідної заяви»

**This is the headline for a rare-disease company: a 30-day statutory decision for orphan medicines already registered in an SRA country or by EMA** — versus the 210-calendar-day standard (Art. 26).

**Art. 25** empowers the Cabinet to establish a separate registration procedure for procurement medicines **and for the Art. 27 medicines registered in SRA countries** — i.e. the reliance route survives the transition, re-based on SRAs instead of a hard-coded country list.

---

## 4. WARTIME EMERGENCY PROVISIONS

### 4.1 Emergency state registration during martial law
**Наказ МОЗ України від 26.02.2022 № 384** — «Деякі питання екстреної державної реєстрації лікарських засобів під час воєнного стану». Approves the *«ПОРЯДОК екстреної державної реєстрації лікарських засобів, медичних імунобіологічних препаратів, препаратів крові, що постачаються в Україну протягом введення воєнного стану, під зобов'язання»* + 3 annexes.
DEC hosting page (order PDF, 374 KB, + annexes, published 01.03.2022): `https://www.dec.gov.ua/news/nakaz-moz-ukrayiny-vid-26-02-2022-№-384-.../` — **VERIFIED** (200). Also listed on DEC's English-translations page.

Features (from search-result summary of the Порядок — the PDF itself I did **not** parse, so treat as **PARTIALLY VERIFIED**): MoH decides on the basis of DEC's conclusion; **free of charge**; products so registered may be used by healthcare professionals in healthcare facilities **without the right of retail sale**; registration may be terminated by MoH before certificate expiry upon termination/cancellation of martial law.

**⚠️ UNVERIFIED — could not confirm current 2026 status.** I found no repeal, but I also could not reach moz.gov.ua to check. **Do not treat "still in force" as established.**

**Circumstantial evidence it is still operative:** the State Register's own search form (drlz.com.ua) carries two dedicated live search radio options — *«для екстренного застосування»* and *«екстрена державна реєстрація під час воєнного стану»* — as of my fetch on 5 August 2026.

### 4.2 Martial-law regime inside CMU Resolution 376 (all VERIFIED from the print text)

**Automatic extension of expiring MAs — YES, but narrowly scoped:**
> **п.1-1:** «Установити, що **до 1 січня 2028 р. продовжується строк дії реєстраційних посвідчень** на лікарські засоби, **які закуповуються особою, уповноваженою на здійснення закупівель у сфері охорони здоров'я**, та який закінчився протягом періоду дії воєнного стану, із внесенням інформації про продовження… до Державного реєстру.»
> *{Пункт 1-1 **в редакції Постанови КМ № 377 від 25.03.2026**}*

**⚠️ Read this carefully: the automatic extension applies ONLY to state-procured medicines, not to the general commercial market.** Deadline **1 January 2028**, most recently reset by **CMU Resolution № 377 of 25 March 2026** (`https://zakon.rada.gov.ua/laws/show/377-2026-п` — **VERIFIED** (200), *"Деякі питання обігу лікарських з… від 25.03.2026 № 377"*).

**Sunset clauses on the wartime relaxations (п.1-2):**
- CMU Res. 529 of 26.04.2024 wording of п.7-8, 21-23, 26¶4, 27¶3, 29¶5, 41-43 and the fee provisions: in force during martial law **+ 30 months** after its termination/cancellation *(as amended by CMU № 1351 of 22.10.2025)*.
- CMU Res. 529 wording of п.11, 35, 37, 44, 50¶2 and the Annex: martial law **+ 3 months**.

Martial law is anchored to Presidential Decree of 24 February 2022 № 64, approved by Law № 2102-IX of 24.02.2022.

**Electronic/remote filing during martial law (п.11, VERIFIED):** during martial law **and/or 6 months after** its termination, applications may be filed with MoH on paper **or** electronically via DEC's information system with a qualified electronic signature, **or** as scanned copies to a DEC-designated email address **with or without** a QES. Materials to DEC may be filed on paper, or electronically as scanned copies without QES, or as electronic documents with QES, **or with an authorised e-signature or equivalent — the Resolution names DocuSign and Adobe Sign explicitly** — subject to a guarantee letter with QES. *(Two sub-paragraphs of п.11 were deleted by CMU № 377 of 25.03.2026.)*

**Other wartime provisions:** п.35 — MoH may approve transfer of manufacture to another licensed Ukrainian manufacturer's facilities, and sale to shelf-life expiry with changes not yet entered in the dossier, where the manufacturer's facilities were destroyed or rendered unusable by the armed aggression of the Russian Federation. п.45 — registration is **refused** where any manufacturing stage (including development and/or clinical trials started after martial law was introduced) is carried out at facilities located in the territory of the aggressor state (Russian Federation).

---

## 5. PUBLIC REGISTER — drlz.com.ua

**Державний реєстр лікарських засобів України** (State Register of Medicinal Products of Ukraine). Operated by DEC under MoH's Pharmaceutical Directorate ("Фармацевтичне управління"). Platform: **Lotus Domino 5.0.5**, **cp1251-encoded, Ukrainian only**, no English interface.

**⚠️ HTTP-ONLY. HTTPS connections are REFUSED (`ECONNREFUSED :443`).** Any tool that force-upgrades HTTP→HTTPS will fail on this site.

| URL | Status |
|---|---|
| `http://www.drlz.com.ua/` | **VERIFIED** — HTTP 200. Title: *«Державний реєстр лікарських засобів України»* |
| `http://www.drlz.com.ua/ibp/ddsite.nsf/all/shlist?opendocument` | **VERIFIED** — HTTP 200. **This is the search page.** |
| `http://www.drlz.com.ua/ibp/ddsite.nsf/slz1?CreateDocument` (POST) | **VERIFIED** — HTTP 200, returns a live results table. Params: `ltype=1&rtype=N&<field>=<value>` |
| `http://www.drlz.com.ua/ibp/ddsite.nsf/all/stat?opendocument` | statistics (linked from homepage, not individually fetched) |
| `http://www.drlz.com.ua/ibp/ddsite.nsf/all/zak?opendocument` | legislation section |
| `http://www.drlz.com.ua/ibp/tpsite.nsf/all/index?opendocument` | secondary index |
| `https://www.drlz.com.ua/...` (any HTTPS) | **UNVERIFIED — connection refused** |
| `https://aisf.dec.gov.ua/` (AISF pharmacovigilance system, linked from drlz) | **UNVERIFIED — connection timed out** on repeated attempts |
| `http://clinicaltrials.dec.gov.ua/` (clinical trials register) | **VERIFIED** — HTTP 200 |

**Search fields (read off the live form, `rtype` values confirmed):**
| `rtype` | Search by | Minimum |
|---|---|---|
| 2 | Trade name (за назвою) | 5 chars |
| 1 | MA number (за номером РП) | 4 chars |
| 4 | MA validity start month + year | dropdowns, 2014–2026 |
| 5 | **INN (за МНН)** | 5 chars |
| 6 | **ATC code** | 3 chars |
| 7 | Active-substance composition | 4 chars |
| 8 | **For emergency use** (для екстренного застосування) | — |
| 9 | **Emergency state registration during martial law** | — |

Results table columns: MA number · validity from/to · name/dosage form/strength/pack · active-substance composition · manufacturer · applicant.
**A CSV export of the whole register is offered** from the homepage (*«Відомості із державного реєстру лікарських засобів в форматі csv»*) — useful for bulk screening of off-patent molecules.

**MoH's own register page:** **UNVERIFIED** — moz.gov.ua is 403-blocked. Both drlz.com.ua and dls.gov.ua link to the State Register at drlz.com.ua as the authoritative source, and dls.gov.ua lists "State register of medicines of Ukraine" among its state registers.

---

## 6. PRACTICALS

### 6.1 MAH / applicant / local representative

**Under the CURRENT regime (to 31.12.2026):** CMU Res. 376 п.9 defines the applicant simply as *«юридична або фізична особа, що несе відповідальність за якість, безпечність та ефективність лікарського засобу»* — **no nationality or establishment requirement**. Documents may be certified "by the applicant **or its authorised representative**" throughout. DEC publishes a bilingual UA-EN contract template **specifically for foreign applicants** (2026 edition). **A foreign entity can be the applicant/MAH today.**

**⭐ Under Law 2469-IX (from 01.01.2027) — this TIGHTENS. Verbatim, Art. 2(1) pt 10:**
> «**власник реєстрації на лікарський засіб** — зареєстрована в установленому законодавством України порядку юридична особа чи фізична особа - підприємець **або** зареєстрована в установленому законодавством відповідної **держави - члена Європейського Союзу або Європейської асоціації вільної торгівлі, що є стороною Угоди про Європейську економічну зону**, порядку особа…»

So the **default rule from 2027 is: MAH must be established in Ukraine or in the EU/EEA-EFTA.** A US-only entity would **not** qualify under the general rule.

**⭐ BUT — the orphan carve-out (Art. 2(1) pt 10, para 2, verbatim):**
> «Власником реєстрації на лікарський засіб, **призначений для лікування рідкісних (орфанних) захворювань у країнах із строгими регуляторними органами (SRAs)**, орфанний, інноваційний лікарський засіб, лікарський засіб передової терапії, лікарський засіб для профілактики та/або лікування ВІЛ, лікування гемофілії, **онкологічних захворювань**, вакцину **може бути** зареєстрована в установленому законодавством України порядку юридична особа чи ФОП **або особа, зареєстрована в установленому законодавством країни із строгими регуляторними органами (SRAs)**.»

**For orphan products, an entity established in any SRA country (including the USA) can be the MAH.** This is a material advantage specific to the rare-disease space. A third carve-out (para 3) allows an MAH **registered in any country** for medicines subject to state/specialised-organisation procurement.

**Representative in Ukraine — Art. 2(1) pt 73 (verbatim):**
> «**представник власника реєстрації на лікарський засіб в Україні** (далі — представник в Україні) — зареєстрована в установленому законодавством України порядку юридична особа або ФОП, яку **уповноважив згідно з відповідним договором та/або довіреністю** власник реєстрації, що зареєстрований у державі - члені ЄС або ЄАВТ/ЄЕЗ, для представництва його інтересів в Україні та здійснення встановлених законодавством України вимог протягом дії державної реєстрації»

**Art. 13(11) — the mandate (verbatim):**
> «Власник реєстрації, зареєстрований у державі - члені Європейського Союзу або ЄАВТ/ЄЕЗ, **та не зареєстрований в Україні** в установленому порядку, **зобов'язаний призначити свого представника в Україні** шляхом укладення письмового договору та/або довіреності, в яких має бути визначений обсяг прав та обов'язків такого представника.»

**Art. 36(1):** *«Призначення представника в Україні не звільняє власника реєстрації від юридичної відповідальності відповідно до законів України.»* — appointing a representative does **not** transfer liability.

**⚠️ FLAGGED DRAFTING GAP:** Art. 13(11) and the pt-73 definition both address only an **EU/EEA-EFTA-established** MAH. **Neither expressly states whether an SRA-country (e.g. US) orphan MAH under the pt-10 para-2 carve-out must appoint a representative in Ukraine.** Art. 28(1)(3) and Art. 13(6)/15 repeatedly use the formula *«заявника (представника в Україні)»* as though a representative is always contemplated. **In practice you should assume a Ukrainian representative is required, but this needs Ukrainian counsel to confirm — I could not resolve it from the statute alone.**

### 6.2 ⭐ GMP — THE GOTCHA, RESOLVED

**PIC/S membership: CONFIRMED, TWO INDEPENDENT SOURCES.**
- `https://picscheme.org/en/members` — **VERIFIED**: Ukraine listed; **State Service of Ukraine on Medicines and Drugs Control (SMDC)**, 120 A Beresteiska av., UA-03115 Kyiv; **"Accession to PIC Scheme: January 2011."**
- `https://www.dls.gov.ua/en/joining-the-pic-s-timeline/` — **VERIFIED**: *"01.01.2011 — The State Service of Ukraine on Medicines and Drugs Control has become a full member of PIC/S."* Standard reassessment conducted **22–26 October 2018** by a PIC/S audit team (Portugal INFARMED, Taiwan FDA, Danish Medicines Agency) — passed. DLS also participates in the **PIC/S Working Group on Inspection Reliance**.

**Does Ukraine require its OWN GMP document even for EU/FDA-approved sites? — YES, but it is a desk exercise, not a re-inspection.**

**Instrument (VERIFIED, full text read from `https://zakon.rada.gov.ua/laws/show/z0133-13/print`):**
> **Наказ МОЗ України від 27.12.2012 № 1130** — «Про затвердження **Порядку проведення підтвердження відповідності умов виробництва лікарських засобів вимогам належної виробничої практики**». Registered at MoJ 21.01.2013 under № 133/22665. Amended *inter alia* by MoH Orders **№ 152 of 25.01.2022** and **№ 1891 of 12.11.2024**. Current version dated **11.06.2025**.

**Two different Derzhliksluzhba outputs — know which one you need:**

| | **Сертифікат (Certificate)** | **Висновок (Conclusion)** |
|---|---|---|
| Basis | Derzhliksluzhba's **own inspection** of the site | **Documentary ("specialised") expertise** recognising a foreign GMP document |
| Definition | *"документ, виданий Держлікслужбою за результатами інспектування, який засвідчує відповідність умов виробництва чинним в Україні вимогам GMP"* | *"…за результатами проведеної спеціалізованої експертизи поданих документів офіційний документ [GMP], виданий уповноваженим органом країни - члена ЄС, Великої Британії або країни, що має угоду про взаємне визнання з ЄС або з Україною, **вважається таким, що підтверджує відповідність**…"* |
| Validity | **3 years** from inspection date (2 years if based on remote assessment) | **Co-terminous with the underlying foreign GMP document** |

**What counts as an acceptable "official document" (verbatim):**
> «сертифікат відповідності умов виробництва… GMP, виданий уповноваженим органом **країни - члена ЄС, Великої Британії або країни, яка має угоду про взаємне визнання з ЄС або з Україною** (**відомості з офіційного електронного реєстру — для FDA США**), або **ліцензія на виробництво** лікарських засобів (якщо… не передбачена видача сертифіката…)»

Note the **FDA is handled via data from its official electronic register** rather than a paper certificate.

**⭐ SPECIALISED EXPERTISE TIMELINES (Section III, п.1) — ORPHAN DRUGS GET THE FAST LANE:**

| Case | Statutory period |
|---|---|
| **Standard** — EU/UK/MRA-country GMP document provided | **≤ 15 working days** from application registration |
| **TB, HIV/AIDS, viral hepatitis, oncology, RARE (ORPHAN) DISEASES**; medicines registered in Ukraine under the **simplified procedure**; medicines in Ukrainian treatment protocols during a WHO-declared pandemic/PHEIC | **≤ 5 working days** |
| **EMA centralised**-registered; **WHO-prequalified** | **≤ 5 working days** |
| Unregistered-in-Ukraine but US/UK/CH/JP/AU/CA/EU-registered, for state procurement *(added by Order № 1891 of 12.11.2024)* | **≤ 5 working days**, on production of the tender-award document |
| **All other cases** | **≤ 20 working days** |

> «…для лікарських засобів, призначених для… **онкологічних та рідкісних (орфанних) захворювань**… спеціалізована експертиза здійснюється **позачергово**.» — orphan applications are handled **out of turn**.

**⚠️ You must flag the eligibility on the application form** — the 5-working-day track applies *«у разі зазначення цієї інформації у поданій Заяві»*.

**Clock stops:** time to answer Derzhliksluzhba deficiency notices is excluded (applicant response window: 15 calendar days for additional documents; application left without consideration if not cured within **30 working days**). Time awaiting a reply to a Derzhliksluzhba query to a foreign competent authority is also excluded.

**⭐ THE ESCAPE HATCH — you may not need a Derzhliksluzhba GMP document at all.**
CMU Resolution 376 **п.19(1)** (recognition route) — verbatim:
> «засвідчена в установленому порядку копія документа… що виданий Держлікслужбою… **або письмове зобов'язання виробника виробляти відповідний лікарський засіб для постачання в Україну на тих самих виробничих потужностях, що застосовуються у виробництві лікарських засобів, призначених для використання у Сполучених Штатах Америки, Швейцарській Конфедерації, Японії, Австралії, Канаді або державах - членах Європейського Союзу**»

**A written manufacturer undertaking to produce for Ukraine on the same sites used for the US/CH/JP/AU/CA/EU markets substitutes for the Ukrainian GMP document on the recognition route.** The same alternative appears in п.21(8) and п.23-1(5) for procurement routes.
⚠️ **Note the asymmetry:** the eligibility list in п.19 *includes* the **United Kingdom**, but the written-undertaking clause in п.19(1) enumerates **USA, Switzerland, Japan, Australia, Canada, EU member states — and omits the UK.** For a UK-only site, do not rely on the undertaking; get the Висновок.

For the **standard** (non-recognition) route, CMU Res. 376 **п.13(5)** *does* mandate the Derzhliksluzhba document (or, for domestic manufacturers, a valid Ukrainian manufacturing licence), and **п.15** disapplies the GMP check where that document already exists.

### 6.3 Submission format — eCTD is ALREADY MANDATORY

**Statutory basis — Law 2469-IX Art. 13(6), verbatim:**
> «Подання документів для державної реєстрації (перереєстрації, безстрокового подовження державної реєстрації) лікарських засобів, внесення змін до матеріалів реєстраційного досьє на лікарський засіб здійснюються **в електронній формі відповідно до стандарту електронного загального технічного документа (Electronic Common Technical Document, (eCTD) ICH**.»

Art. 13(6) is one of the **early-operative exceptions**: *«вводиться в дію через три роки з дня опублікування цього Закону»*. Publication = **18.08.2022** → **18 August 2025**.

**DEC states this itself, in English (VERIFIED, `https://www.dec.gov.ua/materials/answers-to-the-most-frequently-asked-questions-ectd-faq/`, HTTP 200):**
> *"the mandatory submission of eCTD registration dossier materials in Ukraine is set three years after the date of publication of the Law – **18.08.2025**."*
> Test period: state registration from **01.05.2024**; re-registration and variations from **01.07.2024**; open (non-test) eCTD submission from **01.01.2025**.

⚠️ That FAQ page carries "Оновлено: 08.05.2024" — it states the *scheduled* date. The statutory basis is unambiguous, but I could **not** independently verify a MoH/DEC confirmation that 18.08.2025 took effect without slippage. Transitional provision **п.4** of Розділ XII permits paper and/or electronic filing only *«до введення в дію частини шостої статті 13»* — i.e. that permission expired 18.08.2025.

**eCTD implementing framework (VERIFIED, `https://www.dec.gov.ua/speczyfikkacziya-ua-m1-ectd/`, HTTP 200):**
- MoH Orders **№ 588 (08.04.2024)**, **№ 691 (23.04.2024)**, **№ 733 (29.04.2024)**, **№ 909 (29.05.2024)**. Order **№ 691 of 23.04.2024** approves the *Requirements to Module 1 eCTD specification*.
- **UA Module 1 specification v1.2** (current); v1.0 archived. Downloads: specification, annexes, validation criteria (.xlsx), DTD, MD5 checksums for `ua-regional.dtd` / `ua-envelope.mod` / `ua-leaf.mod` / `ua-regional.xsl`.
- **Electronic Applicant Cabinet ("Кабінет заявника") exists** — user guide (UA + EN) and access-request letter templates published; cabinet instructions PDF refreshed April 2026. ⚠️ I did **not** locate a public login URL for the cabinet.
- **File formats: PDF only** for Modules 1–5. `.docx` permitted only in the "Working documents" folder.
- **Baseline submission is not mandatory** but recommended; **mandatory** for variations requiring new registration in the scope of Modules 2–5 (to comply with MoH Order 426).
- **No going back:** once eCTD is used for a product, reverting to another format is prohibited (Requirements, Section III п.1) — the lifecycle must not be broken.

**⭐ IMPORTANT EXEMPTION (verbatim from DEC's FAQ):**
> *"submission of eCTD materials is **not envisaged** for the above mentioned registration procedures for medicinal products registered or submitted for state registration in accordance with the **MOH Ukraine Order dated 15.06.2020 No. 1391** and **MOH Ukraine Order dated 17.11.2016 No. 1245**."*

**The recognition route (Order 1245) and the procurement authenticity route (Order 1391) are exempt from eCTD.** ⚠️ Statement dated 08.05.2024 — confirm it still holds before relying on it.

**Martial-law filing channel** remains available in parallel (CMU 376 п.11): paper, DEC information system with QES, or scanned copies to a DEC email address, with DocuSign/Adobe Sign expressly permitted subject to a QES-signed guarantee letter.

### 6.4 Ukrainian-language labelling and PIL

**Current (CMU Res. 376):** for the recognition route (п.19), you file *«текст маркування… викладений мовою маркування лікарських засобів відповідно до вимог законодавства»* and *«інструкція про застосування… викладена відповідно до вимог щодо мови, визначених законодавством»*. For procurement routes (п.21(7), 21-1(6), 23-1(3)-(4)), the original-language texts **plus certified Ukrainian translations** of labelling, PIL and SmPC, certified by the signature of the applicant or authorised representative.

**From 2027 — Law 2469-IX Art. 53 (verbatim):**
> «1. Мова маркування, листка-вкладки, короткої характеристики лікарських засобів, зареєстрованих в Україні, визначається відповідно до **Закону України "Про забезпечення функціонування української мови як державної"**… Положення… не виключає можливості викладення таких даних **кількома мовами, за умови що в тексті всіма мовами зазначена ідентична інформація**.
> 2. Маркування, листок-вкладка, коротка характеристика лікарського засобу, **що закуповується за рахунок бюджетних коштів**, державну реєстрацію якого здійснено відповідно до статті 25… **можуть викладатися мовою оригіналу**, за умови: 1) забезпечення імпортером супроводу кожної упаковки… **копією засвідченого підписом уповноваженої особи імпортера перекладу** тексту маркування та (за наявності) листка-вкладки і короткої характеристики державною мовою; 2) підтвердження цільового призначення такого ввезення…»

**Default: Ukrainian.** Multilingual packs allowed if the content is identical across languages. Original-language packs are permitted **only** for budget-funded procurement products registered under Art. 25, with a certified Ukrainian translation accompanying every pack.

Related: Arts. 54–62 set EU-style labelling content, blister/small-pack rules (Art. 55), accessibility for people with disabilities (Art. 59), and **Art. 57 — National verification system (2D DataMatrix serialisation), operative 1 January 2028**, voluntary until then (Розділ XII п.5(3)).

### 6.5 ⭐ FEES

#### State registration fee — VERIFIED, EXACT
**CMU Resolution No. 376 of 26.05.2005**, «Розміри збору за державну реєстрацію (перереєстрацію) лікарських засобів». Fetched from `https://zakon.rada.gov.ua/laws/show/376-2005-п/print` — **VERIFIED** (HTTP 200; the non-print card URL returns metadata only, not the text).

Verbatim, п.4:
> «1) за державну реєстрацію (перереєстрацію) лікарських засобів, у тому числі МІБП, крім радіоактивних… — у сумі, **еквівалентній 100 євро за кожну лікарську форму, 10 євро за кожну наступну дозу, 10 євро за кожну наступну упаковку** лікарського засобу;
> 2) за державну реєстрацію (перереєстрацію) радіоактивних лікарських засобів, діагностичних засобів, простих або складних (галенових) препаратів з рослинної лікарської сировини, діючих препаратів обмеженого застосування… препаратів з донорської крові або плазми — у сумі, **еквівалентній 25 євро за одне найменування, 5 євро за кожну наступну дозу, 5 євро за кожну наступну упаковку**.»

- **⚠️ The fee is denominated in EUR, not UAH.** п.3: payable in national or foreign currency; **conversion to UAH at the NBU official rate on the date the payment invoice is issued.** There is therefore *no fixed UAH figure* — anyone quoting one is quoting a snapshot.
- Paid by the applicant **into the State Budget**.
- **⭐ п.2: «До реєстраційного збору НЕ включається вартість експертизи лікарського засобу, а також додаткової експертизи.»** The state fee and DEC's expert fee are entirely separate.
- Fee is **not refunded** if registration is subsequently cancelled (п.37).

**Fee waiver (п.1, in the wording of CMU № 1351 of 22.10.2025):** **no fee is payable** for a medicine procured by the authorised healthcare procurement person that is registered by the competent authority of the **USA, United Kingdom, Switzerland, Japan, Australia, Canada, an EU member state** (and applied there), or **EU-centralised**; **or** included in the **PEPFAR** procurable database on the FDA website; **or** holding an **FDA Tentative Approval**; **or** on the **WHO prequalification** lists and manufactured at the listed site on the application date.

#### DEC expert evaluation fee — ⚠️ **UNVERIFIED — COULD NOT CONFIRM AMOUNTS**

**Where the tariff is published:** `https://www.dec.gov.ua/materials/vitrati-na-re-stracziyu/` ("Вартість послуг") — **VERIFIED** (HTTP 200, page last updated 13.07.2026). DEC sets its own service prices by **internal DEC orders**, superseded frequently.

**Currently in force (from that page):**
- **Наказ ДЕЦ № 60 від 24.02.2026** «Про затвердження вартості послуг» — 26.2 MB, uploaded 03.03.2026 ← **the master tariff**
- Наказ ДЕЦ № 61 від 24.02.2026 — COVID-19 medicines expertise
- Наказ ДЕЦ № 158 від 31.07.2025 — amendments to the cost of expertise/**verification**/review/expert evaluation of registration, re-registration and variation materials
- Наказ ДЕЦ № 120 від 29.05.2025 — further amendments to the same
- Наказ ДЕЦ № 86 від 16.04.2025 — parallel import
- Наказ ДЕЦ № 262 від 11.12.2025, № 255 від 04.12.2025, № 239 від 19.11.2025 — HTA and information/consultancy services

**I downloaded Order No. 60 of 24.02.2026 in full (27,465,781 bytes, PDF 1.7). It has NO text layer — `pdfinfo` reports Creator "HP Scan", Producer "HP Scan Extended Application", created 02.03.2026. `pdftotext` extracted 6 bytes.** It is a scan of a paper document. **I therefore cannot and will not state any UAH figure for DEC expertise. Anyone who quotes you one without OCR'ing this PDF is guessing.**

**How to actually get the number:** DEC issues a formal invoice under contract — Order 1245 п.2: contract within **≤14 calendar days**, invoice within **7 working days**. Contract templates (incl. bilingual UA-EN for foreign applicants, 2026 edition) are at `https://www.dec.gov.ua/materials/dogovori-shhodo-rozglyadu-re-straczijnih-materialiv-na-likarski-zasobi-sproshhena-proczedura/` — **VERIFIED**. Separate template sets exist for authenticity expertise, full expertise, lab testing, HTA, parallel import.
**Materials are only accepted after the invoice is paid** (Order 1245 п.2). Budget the DEC fee as an unknown at kickoff and request the invoice early — it is on the critical path.

#### Derzhliksluzhba GMP fee
**UNVERIFIED.** dls.gov.ua carries "Bank details" pages under both Manufacture and Import sections; I did not open them. Amount not confirmed.

### 6.6 Import licence
**Держлікслужба** licenses **import of medicines** (separate from manufacturing) — dls.gov.ua carries dedicated sections: *Licensing of import*, *Templates and sample documents*, *Bank details*, *Decision on licensing*, *Re-issuance of license*, *Change in the list of medicines*, plus *Information for Importers of medicines* and a *Licensing register of import of medicines*. Under Law 2469-IX this is Arts. 42–44 (Art. 42(2) operative **1 January 2028**). Detailed procedure and fees: **UNVERIFIED**.

---

## 7. RECOMMENDED PLAY FOR AN OFF-PATENT RARE-DISEASE REPURPOSING COMPANY

1. **Move NOW, before 1 January 2027.** The Order 1245 recognition route is live, exempt from eCTD, has a 10-working-day DEC review + 7-working-day MoH decision, and — critically — MAs granted under it are **grandfathered** by Розділ XII п.1–2 with **no re-registration** required and unlimited-term MAs converting to a free Register extract. Post-2027 the reliance architecture depends on an SRA list I found **no evidence has been adopted**.
2. **Entity structure.** Today: no establishment requirement. From 2027: MAH must be Ukraine or EU/EEA-EFTA established **unless** the product is orphan/oncology/ATMP/innovative — in which case **any SRA-country entity (incl. US) qualifies**. If your product is orphan, the carve-out is your route; otherwise consider an EU entity now. Assume you need a Ukrainian representative regardless (confirm with counsel — the statute is silent for SRA-MAHs).
3. **GMP.** Get the Derzhliksluzhba **Висновок** (desk review of your EU/UK GMP certificate or FDA register data) — **5 working days, out of turn**, if you flag the orphan/oncology indication on the application. Or use the п.19(1) manufacturer's written undertaking — but not for a UK-only site.
4. **Art. 23 well-established use (10-year bibliographic)** is the natural registration basis for repurposed off-patent molecules from 2027, and Art. 41 gives only **5 years** data exclusivity (not EU 8+2+1) — favourable.
5. **Art. 27's 30-day decision for orphan products registered by an SRA/EMA** is the prize post-2027. Its availability depends entirely on the MoH SRA list existing. **Track that.**
6. **Watch the 18 August 2027 date** for the Register-extract swap under Розділ XII п.1–2, and the ambiguity flagged in §2.4.

---

## 8. COMPLETE URL LEDGER

### VERIFIED (fetched, HTTP 200, relevant content confirmed)
| URL | Note |
|---|---|
| `https://zakon.rada.gov.ua/laws/show/2469-20` | Law 2469-IX card; metadata + amending-law chain |
| `https://zakon.rada.gov.ua/laws/show/2469-20/print` | **Full text of Law 2469-IX** — use `/print`, the card URL alone yields no body text |
| `https://zakon.rada.gov.ua/laws/show/376-2005-п/print` | **Full text of CMU Res. 376** (registration procedure + fees) |
| `https://zakon.rada.gov.ua/laws/show/z1619-16/print` | **Full text of MoH Order 1245** (recognition route) |
| `https://zakon.rada.gov.ua/laws/show/z0133-13/print` | **Full text of MoH Order 1130** (GMP confirmation) |
| `https://zakon.rada.gov.ua/laws/show/z1069-05` | MoH Order 426 card (main expertise procedure) |
| `https://zakon.rada.gov.ua/laws/show/4239-20` | **Law 4239-IX of 12.02.2025** — set the 1 Jan 2027 date |
| `https://zakon.rada.gov.ua/go/3860-20` / `.../laws/show/3860-IX` | Law 3860-IX of 16.07.2024 (parallel import) |
| `https://zakon.rada.gov.ua/go/4454-20` | Law 4454-IX of 15.05.2025 (basis of current redaction) |
| `https://zakon.rada.gov.ua/laws/show/1351-2025-п` | **CMU Res. 1351 of 22.10.2025** — major rewrite of Res. 376 |
| `https://zakon.rada.gov.ua/laws/show/377-2026-п` | **CMU Res. 377 of 25.03.2026** — MA extension to 1 Jan 2028 |
| `http://www.drlz.com.ua/` | State Register homepage — **HTTP only** |
| `http://www.drlz.com.ua/ibp/ddsite.nsf/all/shlist?opendocument` | **Register search page** |
| `http://www.drlz.com.ua/ibp/ddsite.nsf/slz1?CreateDocument` | Register search POST endpoint — returns live results |
| `https://www.dec.gov.ua/` | DEC homepage — **needs `-k`, broken cert chain** |
| `https://www.dec.gov.ua/contact-page/` | Official DEC addresses + phone directory |
| `https://www.dec.gov.ua/materials/pereklady-normatyvno-pravovyh-aktiv-anglijskoyu-movoyu/` | **English translations** of Law 2469-IX, Law 123/96, CMU 376, Order 384, Order 426, Order 690, Order 898 (unofficial) |
| `https://www.dec.gov.ua/materials/vitrati-na-re-stracziyu/` | **Fee/tariff page** — DEC Order № 60 of 24.02.2026 etc. |
| `https://www.dec.gov.ua/speczyfikkacziya-ua-m1-ectd/` | **eCTD** — UA M1 spec v1.2, MoH Orders 588/691/733/909, applicant cabinet guides |
| `https://www.dec.gov.ua/materials/answers-to-the-most-frequently-asked-questions-ectd-faq/` | **eCTD FAQ (English)** — confirms 18.08.2025 mandatory date + Order 1245/1391 exemption |
| `https://www.dec.gov.ua/applicant/perelikiv-lz-na-yaki-zaversheno-ekspertizu-shhodo-avtentichnosti-re-straczijnih-materialiv/` | Authenticity-verification lists, **latest 13.07.2026** |
| `https://www.dec.gov.ua/applicant/perelik-zayav-pro-derzhavnu-re-stracziyu-likarskih-zasobiv/` | List of registration applications filed |
| `https://www.dec.gov.ua/materials/dogovori-shhodo-rozglyadu-re-straczijnih-materialiv-na-likarski-zasobi-sproshhena-proczedura/` | **Simplified-procedure contracts, 2026, incl. bilingual for foreign applicants** (upd. 24.07.2026) |
| `https://www.dec.gov.ua/materials/dogovori-na-provedennya-ekspertizi-shhodo-avtentichnosti-re-straczijnih-materialiv-na-lz/` | Authenticity-expertise contract templates |
| `https://www.dec.gov.ua/news/nakaz-moz-ukrayiny-vid-26-02-2022-№-384-…/` | **MoH Order 384** martial-law emergency registration + annexes |
| `https://www.dec.gov.ua/applicant/main/` | DEC applicant portal index |
| `http://clinicaltrials.dec.gov.ua/` | Ukrainian clinical trials register |
| `https://www.dls.gov.ua/` | Derzhliksluzhba homepage |
| `https://www.dls.gov.ua/en/contacts/` | **SMDC address, phones, email** (English) |
| `https://www.dls.gov.ua/en/joining-the-pic-s-timeline/` | **PIC/S accession timeline** — 01.01.2011 |
| `https://picscheme.org/en/members` | **PIC/S member list** — Ukraine, accession January 2011 |

### UNVERIFIED
| URL | Reason |
|---|---|
| `https://moz.gov.ua/` and all `moz.gov.ua/uk/decrees/...` order pages | **HTTP 403 — Cloudflare bot challenge on every attempt**, incl. full browser headers. MoH order texts unobtainable directly. |
| `https://aisf.dec.gov.ua/` | **Connection timed out** repeatedly (AISF pharmacovigilance system) |
| `https://www.drlz.com.ua/` (HTTPS) | **ECONNREFUSED :443** — site is HTTP-only |
| `https://www.dec.gov.ua/kontakty/`, `/pro-nas/`, `?post_type=materials&p=14557`, `&p=31797` | **HTTP 404** — dead legacy links after DEC site rebuild |
| `https://cratia.ua/en/state-registration-…/abridged-registration-procedures` | **HTTP 404** |
| `https://www.golos.com.ua/documents/z-2469-ix.pdf` | Downloads (7.2 MB) but is CCITT-fax scanned images — no extractable text |
| DEC Order № 60 of 24.02.2026 fee schedule PDF | **Downloaded successfully (27.5 MB) but scanned, no text layer** — UAH amounts not extractable |
| MoH Order **№ 1391 of 15.06.2020** full text | Not fetchable (moz.gov.ua 403); number/date/English title corroborated via DEC FAQ + CMU 376 cross-references |
| MoH Order **№ 192 of 03.02.2025** full text | moz.gov.ua **403** |
| MoH order approving the **SRA country list** under Law 2469-IX | **Not found — no evidence it has been adopted.** Material gap in the post-2027 architecture. |
| Current status of **MoH Order 384** (martial-law emergency registration) in 2026 | No repeal found, but not positively confirmed |
| Derzhliksluzhba GMP confirmation **fees** | Not retrieved |
| Import licence procedure detail and fees | Not retrieved |
| CMU acts designating UNDP / Crown Agents / UNICEF as specialised procurement organisations | Not retrieved |

### Secondary sources consulted (NOT primary — cross-check before relying)
`apteka.ua` (articles 746824, 715290, 718907, 631351), `protocol.ua`, `cratia.ua`, `deltaswiss.eu`, `mspcorporate.com`, `pharmdoc.com.ua`. Where these conflicted with the statute, **I used the statute** — notably on the entry-into-force date, where one search summary asserted "the law came into force on August 18, 2022" and another "January 1, 2027". Both are half-right: 18.08.2022 = *набрання чинності*, 01.01.2027 = *введення в дію*.

---

## 9. THINGS I EXPLICITLY COULD NOT VERIFY — DO NOT ASSUME
1. **Exact UAH amounts for DEC expert evaluation.** The tariff is a scanned PDF. No figure quoted here or elsewhere is reliable without OCR of DEC Order № 60 of 24.02.2026 or a direct invoice.
2. **Whether MoH has adopted the SRA country list.** The entire post-2027 reliance route (Arts. 25, 27, 116) hangs on it.
3. **Whether MoH Order 384 (martial-law emergency registration) is still in force.**
4. **Whether the 5-year grandfather window in Розділ XII п.2 runs from 18.08.2022 or 01.01.2027.** The text says the former; the result (18.08.2027, before the law is even operative) is anomalous.
5. **Whether an SRA-country (e.g. US) orphan MAH must appoint a representative in Ukraine.** Art. 13(11) addresses only EU/EEA-EFTA MAHs; the drafting is silent for the orphan carve-out.
6. **Whether the eCTD mandate actually took effect on 18.08.2025** without administrative slippage, and whether the Order 1245/1391 eCTD exemption (stated 08.05.2024) still holds.
7. **Full text of MoH Orders 1391, 192, and 426** — moz.gov.ua is inaccessible to automated tooling; Order 426 has a verified zakon.rada card (z1069-05) but I did not parse its body.