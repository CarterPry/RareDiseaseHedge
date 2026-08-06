# IP & Exclusivity Clearance — PARTIAL

> ⚠️ **This file is incomplete.** The parent research agent covering drug identity resolution, repurposing databases, and the full IP/exclusivity stack was interrupted before finishing. Only the **SPC / patent-term-extension** sub-agent completed. See `HANDOFF.md` §"Not done" for exactly what is missing and the prompt to re-run.
>
> **Completed here:** European SPC (Supplementary Protection Certificate) data sources, INPADOC legal-event codes, national patent registers, paediatric extension, SPC manufacturing waiver.
> **Missing:** RxNorm/UNII/GSRS/ATC identity normalization · DrugBank/ChEMBL/PubChem/DrugCentral/repoDB/Open Targets · DailyMed SPL · **Orange Book patent + exclusivity data files** · Orphan/RPD designation conflict checking · PatentsView/Google Patents BigQuery/EPO OPS/PATENTSCOPE · US patent term extension · **the "approved abroad but not in the US" diff method** · 505(b)(2) precedent mining · competitor RPD-filing detection.

*Verified 2026-08-05 by curl/WebFetch only. Egress IP was blocked by `register.epo.org`, `data.inpi.fr`, and Cloudflare on the new UKIPO service — flagged inline.*

---

## Three findings that will break an FTO pipeline if not handled

1. **The EPO Federated Register does NOT carry SPC data.** Every national-office spec page has an explicit row "9 SPC" and it reads **"No"** on every page reachable. FRS deep-links to separate national SPC registers instead. **Treating FRS as an SPC source yields silent false negatives.**
2. **UKIPO Ipsum was retired on 22 January 2025** and replaced by "One IPO Search". All `ipo.gov.uk/p-ipsum/*` URLs 301 to a new domain. **There is no live Ipsum REST API** — APIs are announced as future work.
3. **The EU SPC package (unitary SPC + centralised examination) is NOT law.** As of today all four 2023 proposals sit at **"Awaiting Council's 1st reading position"**. There is no unitary SPC and no EUIPO examining office. **Do not build against one.**

---

## 1. EPO Federated Register

| Claim | Status |
|---|---|
| Federated Register exists, documented | **VERIFIED** — `https://www.epo.org/en/searching-for-patents/legal/register/documentation/federated-register` 200 |
| Quote | *"The Federated Register provides a single point of access to reliable post-grant bibliographic and legal status information on European patents. It is available free of charge."* It is a **tab inside the European Patent Register**, not a standalone endpoint. Post-grant only: *"It does not show the pre-grant status of EP applications."* |
| Countries federated | **VERIFIED** — 35 listed: AT BA BE BG CH CZ DE EE ES FI FR GB GR HR HU IE IT LI LT LU LV MC MD ME(no data yet) MK MT NL NO PL PT RO RS SE SI SK SM TR |
| Integration-status PDF | **VERIFIED** — `https://link.epo.org/web/documentation/federated-register/en-federated-register-status.pdf` 200, 386 KB, footer *"Federated Register – integration status 06/2025"*. Covers 39 member states, 1 extension state (BA), 6 validation states (KH, GE, LA, MD, MA, TN). |
| Post-grant status code list | **VERIFIED** — `https://link.epo.org/web/FRS_post-grant_status_list_en.pdf` 200, 62 KB. Codes `NO_STATUS_1`…`NO_STATUS_32` in EN/FR/DE (`NO_STATUS_15` validation request received, `NO_STATUS_21` lapsed, `NO_STATUS_22` expired). |
| Deep-link coverage table | **VERIFIED** — `.../documentation/data-coverage`. Start dates: FR 1.1.1989, GB 31.12.1988, MC 4.9.1996, SI 1.3.1994, RO 1.3.2003, RS 4.6.2006, MD 1.11.2015, SM 1.6.2015. Most offices `(*)` = no coverage limit. |
| **SPC in FRS** | **VERIFIED NEGATIVE** — per-country field 9 "SPC": **GB** "No — SPC Register available separately (`https://www.ipo.gov.uk/p-find-spc.htm`)"; **FR** "No — SPC available in the INPI database"; **ES** "No — Deep linking will be provided"; **IT** "No"; **PT** "No — available through Deep linking"; **MT** "No — Deep-linking to the NPO's SPC database will be provided"; **SK** "No — Separate SPC Register at `https://wbr.indprop.gov.sk/WebRegistre/DodatkoveOchranneOsvedcenie`"; **LV/MK** "No — not currently provided"; **BG** "No". Only **NL** states *"European patents, with deep linking for national patents, European patents and SPCs."* |
| Live register UI | **UNVERIFIED** — `https://register.epo.org/` returns 200 on `errorpages/error403.htm?reason=RestrictedRequest`; datacentre IP blocked. |

### OPS `register` API
- **VERIFIED** — docs PDF `https://link.epo.org/web/searching-for-patents/data/en-ops-v3.2-documentation-version-1.3.20.pdf` (200, 4.9 MB).
- Endpoints: `http://ops.epo.org/rest-services/register/{publication|application|priority}/{epodoc|docdb|original}/{number}/{biblio|procedural-steps|events|upp}`, plus CQL search `…/register/search/?q=pa%3DIBM` (`Accept: application/register+xml`). Separate INPADOC service: `…/rest-services/legal/publication/docdb/EP.1000000.A1` (`Accept: application/ops+xml`, schema `ops_legal.xsd` — VERIFIED fetchable at `http://ops.epo.org/schema/ops_legal.xsd`).
- Auth: **VERIFIED** — unauthenticated call → 403, body `<error><code>403</code><message>This request has been rejected due to the violation of Fair Use policy</message>`. Register at `https://developers.epo.org/` (200).
- **Searched the whole OPS 3.2 spec: "SPC" and "Supplementary" appear 0 times.** OPS `register` is EP-procedure data; **SPC signal must come from the `legal` (INPADOC) service or national registers.**

---

## 2. INPADOC legal-status SPC event codes — VERIFIED

**Authoritative doc:** `https://link.epo.org/web/inpadoc_classification_scheme_v1.0_en.pdf` (200, 212 KB, v1.0, EPO, 6 June 2018), linked from `https://www.epo.org/en/searching-for-patents/helpful-resources/first-time-here/legal-event-data/inpadoc-classification-scheme`.

Scheme is 2-level; the **category level is modeled on WIPO ST.27**. Per the PDF: *"the EPO has classified 2 800 INPADOC legal event codes used since 1997 on the category level."*

**SPC maps to these categories — filter on these, not on raw office codes:**

| Cat | Title | SPC relevance (verbatim) |
|---|---|---|
| **G** | Protection beyond IP right term | *"patent term adjustment (PTA) · term extension of a patent or utility model · **supplementary protection certificate (SPC)** · extension of a supplementary protection certificate (**paediatric extension (PE)**)"*. Events: requested / not requested; found admissible; **refused**; withdrawn or deemed withdrawn; **not granted**; **granted or registered**. |
| **H** | IP right cessation | *"the discontinuation of a granted supplementary protection certificate is covered in category H"* → SPC lapse/expiry/surrender/invalidation. |
| **P** | Re-publication after modification | *"modified certificates, e.g. **modified SPCs**"* |
| **Q** | Document publication | *"certificates, e.g. **SPCs**"* |
| **F** | IP right grant | Cross-ref: *"Events related to the grant of protection beyond IP right term are covered in category G."* |

**So: filing/grant/rejection = G; lapse = H; SPC certificate publication = Q; corrected SPC = P; paediatric extension = G.**

- Category **N** (permanent termination) *"is not used by the EPO in the INPADOC classification scheme."*
- Bulk source: `https://www.epo.org/en/searching-for-patents/data/bulk-data-sets/inpadoc` (200). Feature matrix `https://link.epo.org/web/searching-for-patents/data/en-main-features-bulk-data-sets-and-webservices.xlsx`.
- **UNVERIFIED:** the raw ~2 800 office-specific code→category mapping table (e.g. GB `SPCF/SPCG/SPCX`, DE `R065/R067`). No free downloadable file found; it ships as an attribute inside INPADOC bulk/OPS `legal` payloads. **Do not hard-code office codes from memory — read the category attribute.**

---

## 3. National registers

### Germany — DPMA
- **DPMAregister** `https://register.dpma.de/DPMAregister/Uebersicht` — 200.
- **Dedicated SPC expert search: VERIFIED** — `https://register.dpma.de/DPMAregister/pat/experte/schutzzertifikate` (add `?lang=en`) 200. Field group **"Master data supplementary protection certificates"** with exactly the fields an FTO pipeline needs:
  `Utilisation of certificate (VZ)` · `(95) Product designation (TIEZ)` · `(54) Title of basic patent (TIGZ)` · `(94) Start of term of protection (LB)` · `(94) Expiry of term of protection (LE)` · `Date of publication of application for certificate (OT)` · `(68) DE file number of basic patent (GAKZ)` · `(68) EP file number of basic patent (GEAKZ)` · `(92) Domestic authorisation authority/number/date (GIS/GIN/GIT)` · `(93) Authorisation EU authority/country/number/date (GES/GEC/GEN/GET)` · `(21) File number of SPC (ZAKZ)`.
- Access: **HTML search only**, JavaScript required. **No public API.**
- **Bulk: "DPMAdatenabgabe" is now DPMAconnectPlus** — `https://www.dpma.de/recherche/datenabgabe/index.html` (200, page dated 10.12.2025). The old English path `/english/services/electronic_services/dpmadatenabgabe/` is **404**.
  `https://www.dpma.de/recherche/datenabgabe/dpmaconnect/index.html` — VERIFIED: *"SSL verschlüsselte, REST basierte Schnittstelle"*, weekly XML incl. **Rechtsstandsdaten** (legal-status data). **Not open data** — requires a signed standard contract and cost-recovery fee. Contact `datenabgabe@dpma.de`. SPCs ride inside the patent register data, not as a separate product.

### United Kingdom — **Ipsum is dead**
- **VERIFIED** — `https://www.gov.uk/government/news/new-patent-search-tool-to-boost-uk-innovation`: **One IPO Search** launched **22 January 2025**, *"replaces the previous Ipsum service, which has served UK innovators well for 13 years."*
- `https://www.ipo.gov.uk/p-ipsum/` → 301 → `https://www.gov.uk/search-for-patent` (200). `…/p-ipsum/Case/PublicationNumber/GB2532851` → 301 → `https://www.search-for-intellectual-property.service.gov.uk/GB2532851`.
- **New service URL: `https://www.search-for-intellectual-property.service.gov.uk/`**
- **SPC coverage: VERIFIED** — gov.uk landing page: *"You can also use this service to search for supplementary protection certificates (SPCs)."* Confirmed again by `https://www.gov.uk/guidance/supplementary-protection-certificates`.
- **REST API: UNVERIFIED / believed absent.** The same news release lists *"new APIs for bulk data access"* as **future** work. Probed `/api`, `/openapi.json`, `/robots.txt`, `/GB2532851` on the new host — **all 403 with `cf-mitigated: challenge`** (Cloudflare bot block on the whole origin). Could not confirm or exclude an undocumented endpoint. Free / no registration for the human UI.
- **Bulk data: VERIFIED but stale** — `https://www.gov.uk/government/publications/ipo-patent-data`. A dedicated **SPC** file downloads OK: `https://assets.publishing.service.gov.uk/media/5b7675d2ed915d14cfdf358f/SPCopendataJuly2018.xlsx` (200, 294 KB) — **but it is a July 2018 snapshot. Unusable for current FTO.**
- Ongoing feed: weekly XML **Patents Journal**, `https://www.gov.uk/check-the-patents-journal` (200).
- Legacy SPC register link cited by EPO, `https://www.ipo.gov.uk/p-find-spc.htm`, now redirects to `https://www.gov.uk/search-for-patent`.

### France — INPI
- **UNVERIFIED (blocked).** `https://data.inpi.fr/` and `/search` → **403** to both curl and WebFetch (bot protection). `https://www.inpi.fr/open-data`, `/services-et-prestations/open-data`, `/donnees-libres-de-droit` → 404.
- **VERIFIED indirectly** — EPO's FR spec page gives the live French register as `https://bases-brevets.inpi.fr/en/home.html` and states *"SPC available in the INPI database. Deep linking will be provided."* **FR updates weekly — slowest of the majors.**
- Open-data pointer: `https://www.data.gouv.fr/datasets/les-brevets-francais-a-linpi-et-loeb` (200).

### Netherlands — OCNL
- **VERIFIED** — `https://www.octrooiregister.nl/` → 301 → `https://www.octrooicentrum.nl/` (200). Actual register: `https://mijnoctrooi.rvo.nl/fo-eregister-view/` (200).
- **Best SPC coverage of any FRS participant** — *"Coverage: European patents, with deep linking for national patents, European patents **and SPCs**."* **Daily updates.** Rich status vocabulary documented with worked examples (EP1237494, EP2310453, EP2017066, EP2242984, EP2257502).
- **API/open data: UNVERIFIED** — found none.

### Italy — UIBM
- **VERIFIED** — `https://www.uibm.gov.it/` → 302 → `https://uibm.mise.gov.it/index.php/it/` (200). Database `https://www.uibm.gov.it/bancadati/` (200).
- FRS spec: updates *"at most every 2 days"*, **file inspection: No**, **SPC: "No"** (blank comment — no SPC route at all). **Weakest of the majors.**

### Others
| Office | Result |
|---|---|
| **Spain OEPM** | Register `http://consultas2.oepm.es/ceo/` — 403 to my IP (UNVERIFIED reachability). FRS spec VERIFIED: daily, file inspection yes, **SPC "No — Deep linking will be provided"**. |
| **Slovakia** | **Dedicated SPC register VERIFIED** — `https://wbr.indprop.gov.sk/WebRegistre/DodatkoveOchranneOsvedcenie` 200. **Best-in-class: a real standalone SPC register.** |
| **Ireland** | `https://www.ipoi.gov.ie/en/ip-search-tools/patents-search/` 200 |
| **Sweden PRV** | `https://www.prv.se/en/patent/search-patent/` 200 |
| **Denmark** | `https://www.dkpto.org/` and `https://onlineweb.dkpto.dk/pvsonline/Patent` both 200. Deep-linking since 2.8.2012 but per the 06/2025 PDF FRS integration is *"in progress"*. |
| **Portugal / Malta** | Both: SPC data reachable **only via deep linking**, not via FRS. |

---

## 4. EU unitary SPC / centralised examination — status as of 2026-08-05

**VERIFIED: NOT ADOPTED. Stalled in Council since the 2024 EP first reading.**

Four procedures, all from COM proposals of **27/04/2023**. Fetched from `https://oeil.secure.europarl.europa.eu/oeil/en/procedure-file?reference=…` (all 200):

| Procedure | Title | COM doc | EP 1st reading | **Status today** |
|---|---|---|---|---|
| **2023/0127(COD)** | Unitary SPC for **medicinal** products | COM(2023)0222 | T9-0097/2024, 28/02/2024 | **"Awaiting Council's 1st reading position"** |
| **2023/0126(COD)** | Unitary SPC for **plant protection** | COM(2023)0221 | T9-0096/2024, 28/02/2024 | **"Awaiting Council's 1st reading position"** |
| **2023/0130(COD)** | SPC for medicinal products — **recast** (centralised examination) | COM(2023)0231 | T9-0099/2024, 28/02/2024 | **"Awaiting Council's 1st reading position"** |
| **2023/0128(COD)** | SPC plant protection — **recast** | COM(2023)0223 | T9-0098/2024, 28/02/2024 | **"Awaiting Council's 1st reading position"** |

- Last key event on all four: **13/11/2024 "Resumption of business from the previous parliamentary term."** Rapporteur Tiemo Wölken (S&D), JURI, re-appointed 18/11/2024.
- **Page freshness confirmed:** the 2023/0127 transparency table lists a rapporteur meeting dated **16/01/2026**, so this is current data, not a stale cache.
- **Corroborated on EUR-Lex** (`https://eur-lex.europa.eu/procedure/EN/2023_127`, `…/2023_130`, both 200): both **"Ongoing"**. Council preparatory-body discussions logged to **30/01/2025** (ST 15980 2024 INIT, ST 5190 2025 INIT) for 2023/0127. **No Council first-reading position, no trilogue agreement, no adopted act, no OJ publication, no application date.**
- Proposals: `https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A52023PC0222` and `…52023PC0231` — both 200. Legal basis TFEU 118(1).
- **EUIPO as examining office: UNVERIFIED.** `https://www.euipo.europa.eu/en` returns 200 but is a JS-rendered SPA; its search page returned **0 SPC mentions in server-side HTML**. `…/news/unitary-supplementary-protection-certificate` → **403**. The EUIPO designation is however visible in the proposal itself (2023/0127 amends EUIPO regulation 2017/1001), which is VERIFIED.

**Pipeline implication: through at least 2026, SPCs remain purely national grants — 27+ separate registers, no central EU source.**

---

## 5. Paediatric extension (6 months)

- **Legal basis VERIFIED** — Reg. 469/2009 **Article 13(3)**: *"The periods laid down in paragraphs 1 and 2 shall be extended by six months in the case where Article 36 of Regulation (EC) No 1901/2006 applies."* Art. 13(1)–(2) set the base term (filing → first EU MA, minus 5 years; **capped at 5 years**). Art. 1(e) defines *"application for an extension of the duration"*.
- Reg. 1901/2006 (paediatric): `https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32006R1901` — 200.
- **Visibility in data sources:**
  - **INPADOC — VERIFIED, best machine-readable route.** Category **G** names *"extension of a supplementary protection certificate (paediatric extension (PE))"* directly, with granted / refused / withdrawn / not-granted event types. Reg. 469/2009 Art. 11 requires notification of both grant and rejection, so the events do get published.
  - **DPMAregister — implicit only.** Exposes `Expiry of term of protection (LE)` but no explicit PE flag. Infer PE from the +6 months on `LE`.
  - **UKIPO — VERIFIED via forms, not as a queryable field.** Dedicated forms: `https://www.gov.uk/government/publications/application-to-extend-a-supplementary-protection-certificate`.
  - **EPO Federated Register — NO.** Carries no SPC data at all, therefore no PE.

---

## 6. SPC manufacturing waiver — Regulation (EU) 2019/933 — VERIFIED

- `https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32019R0933` — 200. ELI `https://eur-lex.europa.eu/eli/reg/2019/933/oj` — 200.
- **Exact citation:** *Regulation (EU) 2019/933 of 20 May 2019 amending Regulation (EC) No 469/2009 concerning the supplementary protection certificate for medicinal products.* **OJ L 153, 11.6.2019, pp. 1–10.** In force **1 July 2019**.
- **What it does** — inserts Art. 5(2) into Reg. 469/2009, creating two exceptions:
  1. **Export waiver** — an EU-established maker may manufacture *"for the purpose of export to third countries"* where protection never existed or has expired, plus *"any related act that is strictly necessary"*.
  2. **Stockpiling waiver** — manufacture *"no earlier than six months before the expiry of the certificate"* for storing in the Member State of making, to place on the market **after** expiry (day-one EU generic entry).
  - **Limit:** *"shall not… cover placing… on the market of a Member State where a certificate is in force"*; no re-importation during the term. Notification and diligence duties attach.
- **FTO relevance:** the waiver does **not** shorten the SPC. It carves out specific acts. **A pipeline must model SPC expiry, minus 6 months for the stockpiling window, and treat export-to-non-protected-territory manufacturing as permitted-with-notification.** UK equivalent retained post-Brexit: notify holder + IPO **3 months** in advance (`https://www.gov.uk/government/publications/notification-for-spc-manufacturing-waiver`).

---

## 7. Base SPC regulations on EUR-Lex — VERIFIED

| Regulation | URL | Detail |
|---|---|---|
| **(EC) No 469/2009** — medicinal products | `https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32009R0469`<br>ELI: `https://eur-lex.europa.eu/eli/reg/2009/469/oj` | **OJ L 152, 16.6.2009, pp. 1–10.** In force; **current consolidated version 01/07/2019**. Codifies Council Reg. (EEC) No 1768/92. |
| **(EC) No 1610/96** — plant protection | `https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A31996R1610`<br>ELI: `https://eur-lex.europa.eu/eli/reg/1996/1610/oj` | Both forms resolve. |

**Use the consolidated view for 469/2009** — the base CELEX text predates the 2019 waiver amendment.

---

## 8. Recommended source stack for the FTO pipeline

1. **Primary SPC signal → INPADOC legal events**, filtered on category **G** (filing/grant/refusal/PE) and **H** (lapse). Via EPO OPS `rest-services/legal/` (OAuth, `developers.epo.org`, fair-use quota) or INPADOC bulk.
2. **Confirm per-jurisdiction against national registers** — they are the legal source of truth. DE (DPMAregister SPC search, richest fields), NL (mijnoctrooi, daily, SPC-inclusive), SK (standalone SPC register), UK (One IPO Search).
3. **Do NOT rely on the EPO Federated Register for SPCs.** Use it for EP post-grant national validation status only, then follow its deep links out.
4. **Do NOT use the UK July-2018 SPC xlsx** as a current source; use One IPO Search + the weekly Patents Journal XML.
5. **Do NOT model a unitary SPC or EUIPO central examination.**
6. **Always add the Art. 13(3) +6 months** where a paediatric extension event appears, and cap base SPC term at 5 years per Art. 13(2).
