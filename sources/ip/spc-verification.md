<!-- RECOVERED from subagent transcript agent-a7d3125d741fb5f75.jsonl, session fd64561f-7c90-41a2-95cf-b4a133a8fe0f, research date 2026-08-05.
     European SPC data sources. Overlaps 05-ip-exclusivity-PARTIAL.md — this is the unabridged child output.
     Verbatim agent deliverable — not re-edited. -->

# SPC Data Source Verification — 2026-08-05

All checks by `curl`/WebFetch only. My egress IP is blocked by two hosts (`register.epo.org`, `data.inpi.fr`) and by Cloudflare bot-challenge on the new UKIPO service — flagged explicitly below.

---

## ⚠️ Three findings that will break an FTO pipeline if not handled

1. **The EPO Federated Register does NOT carry SPC data.** Every national-office spec page has an explicit row "9 SPC" and it reads **"No"** on every page I could reach. FRS deep-links to separate national SPC registers instead. Treating FRS as an SPC source yields silent false negatives.
2. **UKIPO Ipsum was retired on 22 January 2025** and replaced by "One IPO Search". All `ipo.gov.uk/p-ipsum/*` URLs 301 to a new domain. **There is no live Ipsum REST API** — APIs are announced as future work.
3. **The EU SPC package (unitary SPC + centralised examination) is NOT law.** As of today all four 2023 proposals sit at **"Awaiting Council's 1st reading position"**. There is no unitary SPC and no EUIPO examining office.

---

## 1. EPO Federated Register

| Claim | Status |
|---|---|
| Federated Register exists, documented | **VERIFIED** — `https://www.epo.org/en/searching-for-patents/legal/register/documentation/federated-register` HTTP 200 |
| Quote | *"The Federated Register provides a single point of access to reliable post-grant bibliographic and legal status information on European patents. It is available free of charge."* It is a **tab inside the European Patent Register**, not a standalone endpoint. Post-grant only: *"It does not show the pre-grant status of EP applications."* |
| Countries federated | **VERIFIED** — 35 listed on-page: AT BA BE BG CH CZ DE EE ES FI FR GB GR HR HU IE IT LI LT LU LV MC MD ME(no data yet) MK MT NL NO PL PT RO RS SE SI SK SM TR |
| Integration-status PDF | **VERIFIED** — `https://link.epo.org/web/documentation/federated-register/en-federated-register-status.pdf` HTTP 200, 386 KB, footer reads *"Federated Register – integration status 06/2025"*. Covers 39 member states, 1 extension state (BA), 6 validation states (KH, GE, LA, MD, MA, TN). |
| Post-grant status code list | **VERIFIED** — `https://link.epo.org/web/FRS_post-grant_status_list_en.pdf` HTTP 200, 62 KB. Codes `NO_STATUS_1` … `NO_STATUS_32` in EN/FR/DE (e.g. `NO_STATUS_15` Request for EP validation received, `NO_STATUS_21` Patent lapsed, `NO_STATUS_22` Patent expired). Greyed entries = pre-grant, not used by FRS. |
| Deep-link coverage table | **VERIFIED** — `.../documentation/data-coverage`. Notable start dates: FR 1.1.1989, GB 31.12.1988, MC 4.9.1996, SI 1.3.1994, RO 1.3.2003, RS 4.6.2006, MD 1.11.2015, SM 1.6.2015. Most offices marked `(*)` = no coverage limit. |
| **SPC in FRS** | **VERIFIED NEGATIVE** — per-country field 9 "SPC": **GB** "No — SPC Register is available separately (`https://www.ipo.gov.uk/p-find-spc.htm`) and linked from IPSUM"; **FR** "No — SPC available in the INPI database. Deep linking will be provided"; **ES** "No — Deep linking will be provided"; **IT** "No"; **PT** "No — SPC data is available through Deep linking"; **MT** "No — Deep-linking to the NPO's SPC database will be provided"; **SK** "No — Separate SPC Register available at `https://wbr.indprop.gov.sk/WebRegistre/DodatkoveOchranneOsvedcenie`"; **LV/MK** "No — not currently provided"; **BG** "No". Only **NL** states coverage *"European patents, with deep linking for national patents, European patents and SPCs."* |
| Live register UI | **UNVERIFIED** — `https://register.epo.org/` returns HTTP 200 on `errorpages/error403.htm?reason=RestrictedRequest&ip=…`; datacentre IP blocked. Same for the event-code list `https://register.epo.org/allEvents?lng=en`. |

### OPS `register` API
- **VERIFIED** — docs PDF `https://link.epo.org/web/searching-for-patents/data/en-ops-v3.2-documentation-version-1.3.20.pdf` (HTTP 200, 4.9 MB).
- Endpoints: `http://ops.epo.org/rest-services/register/{publication|application|priority}/{epodoc|docdb|original}/{number}/{biblio|procedural-steps|events|upp}`, plus CQL search `…/register/search/?q=pa%3DIBM` (`Accept: application/register+xml`, schema `rplus.xsd`). Separate INPADOC service: `…/rest-services/legal/publication/docdb/EP.1000000.A1` (`Accept: application/ops+xml`, schema `ops_legal.xsd` — **VERIFIED** fetchable at `http://ops.epo.org/schema/ops_legal.xsd`).
- Auth: **VERIFIED** — unauthenticated call to `https://ops.epo.org/3.2/rest-services/legal/publication/docdb/EP.1000000.A1` → HTTP 403, body `<error><code>403</code><message>This request has been rejected due to the violation of Fair Use policy</message>`. Registration at `https://developers.epo.org/` (HTTP 200).
- **Searched the whole OPS 3.2 spec: "SPC" and "Supplementary" appear 0 times.** OPS `register` is EP-procedure data; SPC signal must come from the `legal` (INPADOC) service or national registers.

---

## 2. INPADOC legal-status SPC event codes — **VERIFIED**

**Authoritative doc:** `https://link.epo.org/web/inpadoc_classification_scheme_v1.0_en.pdf` (HTTP 200, 212 KB, v1.0, EPO, 6 June 2018, authors Sonia Kaufmann / Christian Soltmann), linked from `https://www.epo.org/en/searching-for-patents/helpful-resources/first-time-here/legal-event-data/inpadoc-classification-scheme`.

Scheme is 2-level; the **category level is modeled on WIPO ST.27**. Per the PDF: *"the EPO has classified 2 800 INPADOC legal event codes used since 1997 on the category level… available as of Q2/2018."* The detailed-structure level was still future work at v1.0.

**SPC maps to these categories — filter on these, not on raw office codes:**

| Cat | Title | SPC relevance (verbatim) |
|---|---|---|
| **G** | Protection beyond IP right term | *"patent term adjustment (PTA) · term extension of a patent or utility model · **supplementary protection certificate (SPC)** · extension of a supplementary protection certificate (**paediatric extension (PE)**)"*. Events: *"protection beyond IP right term requested / not requested; request found admissible; **request refused**; request withdrawn or deemed to be withdrawn; protection beyond IP right term **not granted**; protection beyond IP right term **granted or registered**."* |
| **H** | IP right cessation | *"the discontinuation of a granted supplementary protection certificate is covered in category H"* → SPC lapse/expiry/surrender/invalidation. |
| **P** | Re-publication after modification | *"modified certificates, e.g. **modified SPCs**"* |
| **Q** | Document publication | Documents covered include *"certificates, e.g. **SPCs**"* |
| **F** | IP right grant | Cross-ref: *"Events related to the grant of protection beyond IP right term are covered in category G, including the grant of a supplementary protection certificate."* |

So: **filing/grant/rejection = G; lapse = H; SPC certificate publication = Q; corrected SPC = P; paediatric extension = G.**

- Note: category **N** (permanent termination) *"is not used by the EPO in the INPADOC classification scheme."*
- Bulk source: `https://www.epo.org/en/searching-for-patents/data/bulk-data-sets/inpadoc` (HTTP 200). Feature matrix `https://link.epo.org/web/searching-for-patents/data/en-main-features-bulk-data-sets-and-webservices.xlsx`.
- **UNVERIFIED:** the raw ~2 800 office-specific code→category mapping table (e.g. GB `SPCF/SPCG/SPCX`, DE `R065/R067`). I found no free downloadable file for it; it ships as an attribute inside INPADOC bulk/OPS `legal` payloads. Do not hard-code office codes from memory — read the category attribute.

---

## 3. National registers

### Germany — DPMA
- **DPMAregister** `https://register.dpma.de/DPMAregister/Uebersicht` — HTTP 200.
- **Dedicated SPC expert search: VERIFIED** — `https://register.dpma.de/DPMAregister/pat/experte/schutzzertifikate` (add `?lang=en`) HTTP 200. Has a field group **"Master data supplementary protection certificates"** with exactly the fields an FTO pipeline needs:
  `Utilisation of certificate (VZ)` · `(95) Product designation (TIEZ)` · `(54) Title of basic patent (TIGZ)` · `(94) Start of term of protection (LB)` · `(94) Expiry of term of protection (LE)` · `Date of publication of application for certificate (OT)` · `(68) DE file number of basic patent (GAKZ)` · `(68) EP file number of basic patent (GEAKZ)` · `(92) Domestic authorisation authority/number/date (GIS/GIN/GIT)` · `(93) Authorisation EU authority/country/number/date (GES/GEC/GEN/GET)`. Also `(21) File number of supplementary protection certificate (ZAKZ)` and IP-right-type value **"Protection certificate"**.
- Access: **HTML search only**, JavaScript required. No public API.
- **Bulk: "DPMAdatenabgabe" is now DPMAconnectPlus** — `https://www.dpma.de/recherche/datenabgabe/index.html` (HTTP 200, page dated 10.12.2025). The English path you gave (`/english/services/electronic_services/dpmadatenabgabe/`) is **404**.
  `https://www.dpma.de/recherche/datenabgabe/dpmaconnect/index.html` — **VERIFIED**: *"SSL verschlüsselte, REST basierte Schnittstelle"*, weekly XML incl. **Rechtsstandsdaten** (legal-status data) for patents/utility models. **Not open data** — requires a signed standard contract and cost-recovery fee (*"gegen Erstattung der Bereitstellungskosten (Grenzkosten)"*). Contact `datenabgabe@dpma.de`. Backfiles via "Altdaten". Note DPMAconnectPlus lists rights as patents/utility models, trade marks, designs — SPCs ride inside the patent register data, not as a separate product.

### United Kingdom — **Ipsum is dead**
- **VERIFIED** — `https://www.gov.uk/government/news/new-patent-search-tool-to-boost-uk-innovation`: **One IPO Search** launched **22 January 2025**, *"replaces the previous Ipsum service, which has served UK innovators well for 13 years."*
- `https://www.ipo.gov.uk/p-ipsum/` → 301 → `https://www.gov.uk/search-for-patent` (200). `https://www.ipo.gov.uk/p-ipsum/Case/PublicationNumber/GB2532851` → **301** → `https://www.search-for-intellectual-property.service.gov.uk/GB2532851`.
- **New service URL: `https://www.search-for-intellectual-property.service.gov.uk/`**
- **SPC coverage: VERIFIED** — gov.uk landing page: *"You can also use this service to search for supplementary protection certificates (SPCs)."* Confirmed again by `https://www.gov.uk/guidance/supplementary-protection-certificates`, which points SPC searches at `https://www.gov.uk/search-for-patent`.
- **REST API: UNVERIFIED / believed absent.** Same news release lists *"new APIs for bulk data access"* as **future** work. `gov.uk/search-for-patent` mentions no API. I probed `/api`, `/openapi.json`, `/robots.txt`, `/GB2532851` on the new host — **all HTTP 403 with `cf-mitigated: challenge`** (Cloudflare bot block, whole origin, not just the API paths). So I could not confirm or exclude an undocumented endpoint. **Free / no registration** for the human UI.
- **Bulk data: VERIFIED but stale** — `https://www.gov.uk/government/publications/ipo-patent-data`: *"These datasets are snapshots of patent/SPC applications received and subsequently published by the Intellectual Property Office."* A dedicated **SPC** file downloads OK: `https://assets.publishing.service.gov.uk/media/5b7675d2ed915d14cfdf358f/SPCopendataJuly2018.xlsx` (HTTP 200, xlsx, 294 KB) — **but it is a July 2018 snapshot. Unusable for current FTO.**
- Ongoing feed: weekly XML **Patents Journal**, `https://www.gov.uk/check-the-patents-journal` (HTTP 200).
- Legacy SPC register link cited by EPO, `https://www.ipo.gov.uk/p-find-spc.htm`, now redirects to `https://www.gov.uk/search-for-patent`.

### France — INPI
- **UNVERIFIED (blocked).** `https://data.inpi.fr/` and `https://data.inpi.fr/search` → **HTTP 403** to both curl and WebFetch (bot protection, 5.7 KB challenge body). `https://www.inpi.fr/open-data`, `/services-et-prestations/open-data`, `/donnees-libres-de-droit` → 404.
- **VERIFIED indirectly** — EPO's FR spec page gives the live French patent register as `https://bases-brevets.inpi.fr/en/home.html` and states *"SPC available in the INPI database. Deep linking will be provided to the FR Register."* FR updates weekly (slowest of the majors).
- Open-data pointer: `https://www.data.gouv.fr/datasets/les-brevets-francais-a-linpi-et-loeb` (found via data.gouv.fr API, HTTP 200) — the only INPI patent dataset returned.

### Netherlands — OCNL
- **VERIFIED** — `https://www.octrooiregister.nl/` → 301 → `https://www.octrooicentrum.nl/` (200). The actual register is `https://mijnoctrooi.rvo.nl/fo-eregister-view/` (HTTP 200); `https://www.rvo.nl/onderwerpen/octrooien-ofwel-patenten/octrooiregister` also redirects there.
- **Best SPC coverage of any FRS participant** — NL spec page: *"Coverage: European patents, with deep linking for national patents, European patents **and SPCs**."* Daily updates. Rich status vocabulary documented (Request for validation received / Patent validated / not validated / surrendered / revoked / lapsed / expired) with worked examples (EP1237494, EP2310453, EP2017066, EP2242984, EP2257502).
- **API/open data: UNVERIFIED** — found none.

### Italy — UIBM
- **VERIFIED** — `https://www.uibm.gov.it/` → 302 → `https://uibm.mise.gov.it/index.php/it/` (200). Database: `https://www.uibm.gov.it/bancadati/` (HTTP 200).
- FRS spec: updates *"at most every 2 days"*, **file inspection: No**, **SPC: "No"** (blank comment — no SPC route offered at all). Italian status vocabulary: Revocata / Ritirata / Decaduta / Accolta / Rifiutata / Rinunciata. Weakest of the majors.

### Others
| Office | Result |
|---|---|
| **Spain OEPM** | Register `http://consultas2.oepm.es/ceo/` — **403** to my IP (UNVERIFIED reachability). FRS spec VERIFIED: daily, file inspection yes, **SPC "No — Deep linking will be provided"**. Status codes `NO_STATUS_15/19/21/24/25/26/28/32`. |
| **Slovakia** | **Dedicated SPC register VERIFIED** — `https://wbr.indprop.gov.sk/WebRegistre/DodatkoveOchranneOsvedcenie` HTTP 200. Best-in-class: a real standalone SPC register. |
| **Ireland** | `https://www.ipoi.gov.ie/en/ip-search-tools/patents-search/` HTTP 200. FRS page: `https://www.ipoi.gov.ie/en/ip-search-tools/patents-search/ie-federated-register-services/…` |
| **Sweden PRV** | `https://www.prv.se/en/patent/search-patent/` HTTP 200. FRS page `https://www.prv.se/en/the-advanced-patent-guide/patent-databases/se-federated-register-service/` |
| **Denmark** | `https://www.dkpto.org/` and `https://onlineweb.dkpto.dk/pvsonline/Patent` both HTTP 200. DK has deep-linking (since 2.8.2012) but per the 06/2025 PDF FRS integration is *"in progress"*. |
| **Portugal / Malta** | Both explicitly say SPC data reachable **only via deep linking**, not via FRS. |

---

## 4. EU unitary SPC / centralised examination — status as of 2026-08-05

**VERIFIED: NOT ADOPTED. Stalled in Council since the 2024 EP first reading.**

Four separate procedures, all from COM proposals of **27/04/2023**. Fetched from `https://oeil.secure.europarl.europa.eu/oeil/en/procedure-file?reference=…` (all HTTP 200, redirecting to `oeil.europarl.europa.eu`):

| Procedure | Title | COM doc | EP 1st reading | **Status today** |
|---|---|---|---|---|
| **2023/0127(COD)** | Unitary supplementary certificate for **medicinal** products | COM(2023)0222 | T9-0097/2024, 28/02/2024 (report A9-0019/2024) | **"Awaiting Council's 1st reading position"** |
| **2023/0126(COD)** | Unitary SPC for **plant protection** products | COM(2023)0221 | T9-0096/2024, 28/02/2024 (A9-0020/2024) | **"Awaiting Council's 1st reading position"** |
| **2023/0130(COD)** | SPC for medicinal products — **recast** (centralised examination) | COM(2023)0231 | T9-0099/2024, 28/02/2024 (A9-0022/2024) | **"Awaiting Council's 1st reading position"** |
| **2023/0128(COD)** | SPC for plant protection products — **recast** | COM(2023)0223 | T9-0098/2024, 28/02/2024 (A9-0023/2024) | **"Awaiting Council's 1st reading position"** |

- Last key event on all four: **13/11/2024 "Resumption of business from the previous parliamentary term."** Rapporteur Tiemo Wölken (S&D), JURI, re-appointed 18/11/2024.
- **Page freshness confirmed:** the 2023/0127 transparency table lists a rapporteur meeting dated **16/01/2026** (Permanent Representation of Cyprus to the EU), so this is current data, not a stale cache.
- **Corroborated independently on EUR-Lex** (`https://eur-lex.europa.eu/procedure/EN/2023_127` and `…/2023_130`, both HTTP 200): both marked **"Ongoing"**. Council preparatory-body discussions logged up to **30/01/2025** (ST 15980 2024 INIT, ST 5190 2025 INIT) for 2023/0127, and to 11/07/2024 (ST 12132 2024 INIT) for 2023/0130. No Council first-reading position, no trilogue agreement, no adopted act, no OJ publication, no application date.
- Proposals themselves: `https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A52023PC0222` and `…52023PC0231` — both HTTP 200. Legal basis TFEU 118(1). 2023/0127 amends Reg. 2017/1001, Reg. 1901/2006, Reg. 608/2013.
- **EUIPO as examining office: UNVERIFIED.** `https://www.euipo.europa.eu/en` and `/en/law/eu-legislation` return HTTP 200 but are JS-rendered SPAs; their search page returned **0 SPC mentions in server-side HTML**. `https://www.euipo.europa.eu/en/news/unitary-supplementary-protection-certificate` → **403**. I could not confirm any EUIPO-published SPC page by direct fetch. The EUIPO designation is however visible in the proposal itself (2023/0127 amends the EUIPO regulation 2017/1001), which is VERIFIED.

**Pipeline implication:** through at least 2026, SPCs remain **purely national grants**, 27+ separate registers, no central EU source. Do not build against a unitary SPC.

---

## 5. Paediatric extension (6 months)

- **Legal basis VERIFIED** — Reg. 469/2009 **Article 13(3)**: *"The periods laid down in paragraphs 1 and 2 shall be extended by six months in the case where Article 36 of Regulation (EC) No 1901/2006 applies."* Art. 13(1)–(2) set the base term (time from basic-patent filing to first EU marketing authorisation, minus 5 years; **capped at 5 years**). Art. 1(e) defines *"application for an extension of the duration"* as one *"pursuant to Article 13(3) of this Regulation and Article 36 of Regulation (EC) No 1901/2006."*
- Reg. 1901/2006 (paediatric): `https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32006R1901` — HTTP 200.
- **Visibility in data sources:**
  - **INPADOC — VERIFIED, best machine-readable route.** Category **G** names *"extension of a supplementary protection certificate (paediatric extension (PE))"* directly, with granted / refused / withdrawn / not-granted event types. Reg. 469/2009 Art. 11 requires notification of both grant and rejection of an extension, so the events do get published.
  - **DPMAregister — implicit only.** The SPC field set exposes `Expiry of term of protection (LE)` but no explicit paediatric-extension flag. You would infer PE from the +6 months on `LE`.
  - **UKIPO — VERIFIED via forms, not as a queryable field.** gov.uk guidance: *"An SPC for a medicinal active ingredient may also be extended for a further six months if it has undergone the appropriate paediatric testing."* Dedicated forms exist: `https://www.gov.uk/government/publications/application-to-extend-a-supplementary-protection-certificate` and `.../declarelapseinvalidaterevoke-an-extension-of-a-supplementary-protection-certificate`.
  - **EPO Federated Register — NO.** It carries no SPC data at all, therefore no PE.

---

## 6. SPC manufacturing waiver — Regulation (EU) 2019/933 — **VERIFIED**

- `https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32019R0933` — HTTP 200. ELI `https://eur-lex.europa.eu/eli/reg/2019/933/oj` — HTTP 200.
- **Exact citation:** *Regulation (EU) 2019/933 of the European Parliament and of the Council of **20 May 2019** amending Regulation (EC) No 469/2009 concerning the supplementary protection certificate for medicinal products.* **OJ L 153, 11.6.2019, pp. 1–10.** In force **1 July 2019**.
- **What it does** — inserts Art. 5(2) into Reg. 469/2009, creating two exceptions to SPC protection:
  1. **Export waiver** — an EU-established maker may manufacture the product *"for the purpose of export to third countries"* where protection never existed or has expired, plus *"any related act that is strictly necessary"* for the making or the export.
  2. **Stockpiling waiver** — manufacture *"no earlier than six months before the expiry of the certificate"* for *"storing it in the Member State of making, in order to place that product… on the market of Member States after the expiry"* (day-one EU generic entry).
  - **Limit:** *"shall not… cover placing… on the market of a Member State where a certificate is in force"*; no re-importation during the term. Notification and diligence duties attach.
- **FTO relevance:** the waiver does **not** shorten the SPC. It carves out specific acts. A pipeline must model SPC expiry, minus 6 months for the stockpiling window, and treat export-to-non-protected-territory manufacturing as permitted-with-notification. UK equivalent retained post-Brexit: notify holder + IPO **3 months** in advance (`https://www.gov.uk/government/publications/notification-for-spc-manufacturing-waiver`).

---

## Base SPC regulations on EUR-Lex — **VERIFIED**

| Regulation | URL | HTTP | Detail |
|---|---|---|---|
| **(EC) No 469/2009** — medicinal products | `https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32009R0469`<br>ELI: `https://eur-lex.europa.eu/eli/reg/2009/469/oj`<br>data.europa ELI: `http://data.europa.eu/eli/reg/2009/469/oj` | 200 | *"Regulation (EC) No 469/2009 of the European Parliament and of the Council of 6 May 2009 concerning the supplementary protection certificate for medicinal products (Codified version) (Text with EEA relevance)"*. **OJ L 152, 16.6.2009, pp. 1–10.** In force; **current consolidated version 01/07/2019** (also 01/07/2013). Codifies Council Reg. (EEC) No 1768/92. |
| **(EC) No 1610/96** — plant protection products | `https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A31996R1610`<br>ELI: `https://eur-lex.europa.eu/eli/reg/1996/1610/oj` | 200 | Both forms resolve. |

Use the **consolidated** view for 469/2009 — the base CELEX text predates the 2019 waiver amendment.

---

## Recommended source stack for the FTO pipeline

1. **Primary SPC signal → INPADOC legal events**, filtered on category **G** (filing/grant/refusal/PE) and **H** (lapse). Via EPO OPS `rest-services/legal/` (OAuth, `developers.epo.org`, fair-use quota) or INPADOC bulk.
2. **Confirm per-jurisdiction against national registers** — they are the legal source of truth. DE (DPMAregister SPC search, richest fields), NL (mijnoctrooi, daily, SPC-inclusive), SK (standalone SPC register), UK (One IPO Search).
3. **Do NOT rely on the EPO Federated Register for SPCs.** Use it for EP post-grant national validation status only, then follow its deep links out to national SPC databases.
4. **Do NOT use the UK July-2018 SPC xlsx** as a current source; use One IPO Search + the weekly Patents Journal XML.
5. **Do NOT model a unitary SPC or EUIPO central examination** — still only a proposal, stuck awaiting Council first reading.
6. **Always add the Art. 13(3) +6 months** where a paediatric extension event appears, and cap base SPC term at 5 years per Art. 13(2).

**Scratch files** (delete at will): `/private/tmp/claude-501/-Users-carte-Downloads-RareDiseaseHedge/fd64561f-7c90-41a2-95cf-b4a133a8fe0f/scratchpad/{inpadoc.pdf,inpadoc.txt,ops.pdf,ops.txt,frs.pdf}`. No files written to the project.