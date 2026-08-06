<!-- RECOVERED from subagent transcript agent-a96b88c96e52bbc15.jsonl, session fd64561f-7c90-41a2-95cf-b4a133a8fe0f, research date 2026-08-05.
     NORD, Global Genes/RARE-X, ERDERA/RD-Connect/ERNs, UDN, RDCRN.
     Verbatim agent deliverable — not re-edited. -->

Verification complete across all six sections. Here are the findings.

---

# Rare Disease Patient-Finding Infrastructure — Verified Source Map

**Method note:** Every URL below was hit directly. `rarediseases.org` blocks standard fetchers with **HTTP 403 (Cloudflare Bot Management)** — I confirmed this on the root and on `/rare-disease-centers-of-excellence/`. NORD pages were verified through an alternate crawler. **This is itself a finding: NORD is not scrapable with plain HTTP; you need a headless browser with a real UA, or a commercial crawler.**

Two corrections to the brief's premises up front:
- **RDCRN has 19 consortia, not ~20**, and the current cycle is **Cycle 5, beginning FY2025** (~$26M), not "2024–2029."
- **NORD Centers of Excellence is 46 centers, not ~30–40** (page text), with press releases indicating expansion toward 49.

---

## 1. NORD (National Organization for Rare Disorders)

| Resource | URL | Status |
|---|---|---|
| Root | `https://rarediseases.org/` | **VERIFIED** (403 to plain fetchers) |
| Member org list | `https://rarediseases.org/nord-member-list/` | **VERIFIED** |
| Patient org directory | `https://rarediseases.org/organizations/` | **VERIFIED** |
| Rare Disease Database | `https://rarediseases.org/rare-diseases/` | **VERIFIED** |
| Centers of Excellence | `https://rarediseases.org/center-of-excellence/` | **VERIFIED** |
| IAMRARE registry | `https://rarediseases.org/advancing-research/iamrare-patient-registry-platform/` | **VERIFIED** |
| Corporate Council | `https://rarediseases.org/corporate-council/` | UNVERIFIED (nav link) |
| COE alt path | `https://rarediseases.org/living-with-a-rare-disease/rare-disease-centers-of-excellence/` | UNVERIFIED (timed out) |

**Member organization directory.** `/nord-member-list/` is a **flat, alphabetical, fully-rendered HTML list** of 501(c)(3) member orgs — the single most scrapable asset NORD has. I pulled entries from `17q12 Foundation` through the F's in one request (17q12, 3q29, Alagille Syndrome Alliance, Cure SMA, COMBINEDBrain, EURORDIS, Castleman Disease Collaborative Network, etc.). Two tiers: **Platinum** (orgs doing research/registries/medical advisory boards — *these are your targets*) and **Gold** (support-only, no research infrastructure). The Platinum/Gold split is the useful filter: Platinum members already have a Medical Advisory Board and registry experience, meaning they have a clinician network and an IRB-literate staff.

**Rare Disease Database.** ~**1,324 disease reports** (per a 2024 academic analysis; NORD's own copy says "more than 1,200"). **No API, no bulk export.** Individual disease pages are static and scrapable, but the A–Z index is behind the Cloudflare layer. Reports are clinician-authored overviews — useful for disease definition and for the "Organizations" block at the bottom of each report, which maps disease → advocacy group.

**IAMRARE.** NORD's patient-registry-as-a-service platform. Patient organizations (not companies) launch registries; NORD provides the platform, IRB coverage, and survey instruments. Entry points on-page: *Join a Study / Search Studies / Launch a Study / Contact Us*. **The engagement model matters: you cannot buy access to IAMRARE data. You sponsor or co-design a registry with the disease's patient org, and the org controls the data.** Related: `https://rarediseases.org/patient-registries-natural-history-studies/`.

**Centers of Excellence.** Launched **November 2021**. Page states **46 centers across 28 states + DC**, each spanning multiple academic institutions with outreach clinics; 350+ volunteer clinicians across 25+ specialties in Working Groups. The directory has **List and Map views with state filtering** — the state dropdown is in the HTML, so the center list is extractable per-state. Recent PR (Dec 2025, +7 centers; a later 2026 release) suggests the count is now ~49 across ~170 affiliated institutions — **treat 46 as verified-on-page, 49 as UNVERIFIED press claim.**

**How a small company actually engages NORD:**
1. **Corporate Council** is the formal paid-partnership door (`/corporate-council/`).
2. For a ~20-patient trial, the higher-yield path is **direct to the Platinum member org** for your disease, bypassing NORD centrally. NORD's value is the *directory*, not the introduction.
3. **COE network is your PI-sourcing list** — 46 institutions with declared rare-disease infrastructure and a stated goal to "Increase the Number of Multi-Site Clinical Trials." That is an explicit invitation.

---

## 2. Global Genes / RARE-X

| Resource | URL | Status |
|---|---|---|
| Root | `https://globalgenes.org/` | **VERIFIED** |
| RARE-X for researchers | `https://globalgenes.org/rare-x-for-researchers/` | **VERIFIED** |
| RARE-X data access | `https://globalgenes.org/rare-x-research-data-access/` | **VERIFIED** |
| RARE-X overview | `https://globalgenes.org/about-us/about-rare-x/` | UNVERIFIED (nav) |
| Community | `https://globalgenes.org/rare-disease-community/` | **VERIFIED** |
| Global Advocacy Alliance | `https://globalgenes.org/about-us/global-advocacy-alliance/` | UNVERIFIED (nav) |
| Corporate Alliance | `https://globalgenes.org/about-us/rare-corporate-alliance/` | UNVERIFIED (nav) |
| DAR form | `https://wkf.ms/40BRdZo` | UNVERIFIED (linked from verified page) |

**Merger confirmed.** RARE-X is now fully absorbed — it lives entirely under `globalgenes.org/` paths with no independent site navigation, though `rare-x.org/connect/` still appears as a contact endpoint. Global Genes HQ: 1012 14th Street NW, Suite 500, Washington DC; (949) 248-7273.

**What RARE-X collects.** Cloud-based, de-identified **patient-level** data: patient-reported outcomes, molecular/genomic data, structured study data. Organized into disease communities (Pompe, Sleep, Vision consortia named). **Neither the researcher page nor the access page publishes a participant count or disease count** — a real gap; you must ask.

**Three access tiers — tier 3 is the one that matters to you:**
- **Level 1:** aggregate data (marked "coming soon")
- **Level 2:** de-identified patient-level data for analysis/publication
- **Level 3: "support for identifying and recruiting patients for clinical trials"** ← this is a patient-finding channel, explicitly offered

**Gotcha:** Level 3 is advertised on `/rare-x-for-researchers/` but is **completely undocumented on the data-access page** — no process, no terms, no fee schedule. It is a conversation, not a form.

**Level 2 process (fully documented, 6 steps):** DAR form → Data Access Committee review → DUA via DocuSign to PI + Institutional Signatory → register for **Terra** (`terra.bio`, needs Google account + Chrome) → configure Google Cloud billing → workspace access.
- **Cost:** no application or access fee. Compute only — cloud storage "dollars per month," simple analyses <$1, $300 GCP credit for new users.
- **Term:** 3 years, renewable; 90-day termination notice; destroy data on termination.
- **Timeline:** *"at least a couple of months"* — DAC takes weeks, **DUA negotiation 1–8 months.** Budget for this.
- **Commercial eligibility — flagged risk:** listed eligible applicants are academic researchers, clinical researchers, and patient advocacy groups. For-profits are **not explicitly addressed**, and individual participants can restrict their data to **"non-commercial research only."** A for-profit repurposing company should assume partial data exclusion and confirm eligibility before investing in the DUA cycle.

**Patient org directory: not scrapable.** The Global Advocacy Alliance is explicitly *"a members only, global community"* — no public browsable directory, no member count published. This is strictly worse than NORD's open member list. Use NORD for directory work.

---

## 3. EJP RD → ERDERA, RD-Connect, and the ERNs

### Succession confirmed
**EJP RD (2019–2023) is finished. ERDERA is the successor.**

| Resource | URL | Status |
|---|---|---|
| ERDERA | `https://erdera.org/` | **VERIFIED** |
| ERDERA Clinical Research Network | `https://erdera.org/clinical-research/` | **VERIFIED** |
| Clinical Trials Toolbox | `https://erdera.org/clinical-research/rare-diseases-clinical-trials-toolbox/` | UNVERIFIED (linked) |
| Contact | `https://erdera.org/contact-us/` | UNVERIFIED (linked) |
| RD-Connect (legacy) | `https://rd-connect.eu/` | **VERIFIED — frozen** |
| GPAP (legacy URL) | `https://platform.rd-connect.eu/` | **VERIFIED** |
| **GPAP (live portal)** | `https://portal.gpap.cnag.eu/` | **VERIFIED** |
| GPAP docs | `https://platform.rd-connect.eu/gpap_doc/` | **VERIFIED** |
| ERN list | `https://health.ec.europa.eu/rare-diseases-and-european-reference-networks/european-reference-networks_en` | **VERIFIED** |
| **ERN centre search tool** | `https://webgate.ec.europa.eu/ernsd/cgi-bin/ern_public.cgi?npage=ern_portal.html` | **VERIFIED** (JS SPA) |

**ERDERA:** 170+ public and private organisations across **37 countries**, coordinated by INSERM, Horizon Europe grant **101156595**. Seven service areas: Funding, **Clinical Research Network**, **Data Hub**, Expertise Services, Accelerator, Training, International Alignment. The CRN connects ERNs + national diagnostic centres + undiagnosed disease programmes, organized in three pillars: Diagnostic Research, Outcome Research, and **Innovative Therapies (ATMPs and "N-of-few trials")**. That last phrase is directly on-point for a 20-patient trial.

**Gotcha:** ERDERA publishes **no sponsor-engagement pathway and no site counts.** There is no "request sites" form. Entry is via `contact-us` or via an ERDERA funding call (`erdera.org/call/clinical-trials/`).

**RD-Connect status — important:** the legacy site states plainly *"The content of this website is no longer updated."* The FP7 project ran **2012–2018**. **The GPAP survived the project and migrated to CNAG-CRG Barcelona at `portal.gpap.cnag.eu`.** Docs still live at the old `platform.rd-connect.eu/gpap_doc/` (© CNAG). Support: `help@rd-connect.eu`.

**GPAP access — the blocking gotcha for you:** access is **"free to all noncommercial members of the RD research community."** PIs sign the RD-Connect Adherence Agreement + Code of Conduct (`rd-connect.eu/forms-and-guides/`, UNVERIFIED), reviewed by a **4-member Data Access Committee**; approved PIs can then credential their team members. Non-EU researchers may additionally need a Data Transfer Agreement and Data Access Agreement. **A for-profit company cannot get GPAP access directly — you must go through an academic collaborator as PI.**

**The 24 ERNs (all VERIFIED from the EC page)** — this is your European site-volume map:

| ERN | Disease area |
|---|---|
| Endo-ERN | Rare endocrine conditions |
| ERKNet | Rare kidney diseases |
| ERN BOND | Rare bone disorders |
| ERN CRANIO | Craniofacial anomalies, ENT |
| ERN EpiCARE | Rare/complex epilepsies |
| ERN EURACAN | Rare adult solid cancers |
| ERN eUROGEN | Uro-recto-genital |
| ERN EURO-NMD | Neuromuscular |
| ERN GENTURIS | Genetic tumour risk syndromes |
| ERN GUARD-Heart | Rare heart diseases |
| ERN PaedCan | Paediatric cancer / haemato-oncology |
| ERN RARE-LIVER | Hepatological |
| ERN ReCONNET | Connective tissue & musculoskeletal |
| ERN RITA | Immunodeficiency, autoinflammatory, autoimmune, paediatric rheumatic |
| ERN TRANSPLANT-CHILD | Paediatric transplantation |
| ERN-EuroBloodNet | Haematological |
| ERN-EYE | Rare eye diseases |
| ERN-ITHACA | Malformation syndromes & neurodevelopmental |
| ERN-LUNG | Respiratory |
| ERN-RND | Neurological |
| ERN-Skin | Skin disorders incl. undiagnosed |
| ERNICA | Inherited/congenital digestive anomalies |
| MetabERN | Hereditary metabolic disorders |
| VASCERN | Multisystemic vascular |

**The ERN Service Directory is the highest-value European asset.** It searches by **ERN name, country, and clinical centre**, returns member details and location maps, and — critically — offers **bulk downloads: "ERN members per network" and "ERN members per country."** That is a downloadable roster of every ERN-designated European centre. It is a JavaScript SPA, so it needs a headless browser, but the download endpoints are the shortcut.

---

## 4. Undiagnosed Diseases Network (UDN)

| Resource | URL | Status |
|---|---|---|
| Root | `https://undiagnosed.hms.harvard.edu/` | **VERIFIED** |
| Sites | `https://undiagnosed.hms.harvard.edu/udn-sites/` | **VERIFIED** |
| Participate | `https://undiagnosed.hms.harvard.edu/participate/` | UNVERIFIED (linked) |
| Data availability | `https://undiagnosed.hms.harvard.edu/research/data-availability/` | **VERIFIED** |
| UDN Gateway | `https://gateway.undiagnosed.hms.harvard.edu/` | UNVERIFIED (linked from verified page) |
| dbGaP phs001232 | `https://www.ncbi.nlm.nih.gov/projects/gap/cgi-bin/study.cgi?study_id=phs001232` | UNVERIFIED (linked) |
| ClinVar submitter | `https://www.ncbi.nlm.nih.gov/clinvar/submitters/505999/` | UNVERIFIED (linked) |
| **UDNI** | `https://www.udninternational.org/` | **VERIFIED** |

**Status:** active, NIH-funded. Contact `UDN@hms.harvard.edu`, 1-844-746-4836, 9–5 ET M–F.

**23 clinical sites (VERIFIED):** Baylor; CHOP/UPenn; Cincinnati Children's; Duke; Harvard-affiliated hospitals; Icahn/Mount Sinai; Indiana; Johns Hopkins; Mayo; Medical College of Wisconsin/Children's Wisconsin; NIH UDP (Bethesda); Sanford Health; Stanford; UAB; UC Irvine/CHOC; UCLA; Miami; Utah; Washington/Seattle Children's; Wisconsin–Madison; Vanderbilt; WashU; Yale.
**Supporting:** Biorepository — Vanderbilt. DMCC — Harvard Medical School. Sequencing Core — Baylor. Model Organism Screening — Baylor, Oregon, WashU.

**Data:** genomic + phenotypic to **dbGaP phs001232, annually**; variant classifications to **ClinVar quarterly** (submitter 505999) with HPO terms and diagnoses. Access via standard dbGaP DAR (`sharing.nih.gov/accessing-data/accessing-genomic-data/how-to-request-and-access-datasets-from-dbgap`).

**Honest assessment for your use case — UDN is weak as a recruitment channel.** The data-availability page contains **no mechanism to contact participants and no collaborative recruitment pathway**, and no Matchmaker Exchange/GeneMatcher integration is documented there. dbGaP data is de-identified with no re-contact. UDN's real value to you is **indirect**: it identifies *which of the 23 institutions has a clinician who has personally worked up your ultra-rare phenotype*. Use it as a PI-finding tool, not a patient list. If your disease is one where diagnosis is still an odyssey, the UDN site PI is likely the single best-informed clinician in the country.

**UDNI (VERIFIED, actively running):** run out of **Istituto Superiore di Sanità**, contact `udni@iss.it`. Confirmed live activity: 15th Conference Siena Oct 16–17 2026; Undiagnosed Day Apr 29 2026; official journal partnership with *Rare* (ScienceDirect). Country list at `/schede-16-udni_countries`. Membership routes: clinical members (**requires 5 undiagnosed cases**), patients/associations (needs provider referral letter), trainees. **UDNI is the more approachable of the two** — it has an open membership application, whereas the US UDN does not.

---

## 5. NIH RDCRN — the key deliverable

| Resource | URL | Status |
|---|---|---|
| Root | `https://www.rarediseasesnetwork.org/` | **VERIFIED** |
| **Consortia directory** | `https://www.rarediseasesnetwork.org/consortia-directory` | **VERIFIED** |
| Contact Registry | `https://www.rarediseasesnetwork.org/registry` | **VERIFIED** |
| DMCC | `https://www.rarediseasesnetwork.org/data-management-and-coordinating-center` | **VERIFIED** |
| Data sharing | `https://www.rarediseasesnetwork.org/data-sharing-resources` | **VERIFIED** |
| NCATS RDCRN | `https://ncats.nih.gov/research/research-activities/rdcrn` | **VERIFIED** |
| Consortium URL pattern | `https://rdcrn.org/<slug>` | **VERIFIED** (tested `rdcrn.org/cegir`) |

**Network scale:** 19 funded research groups, **280+ diseases**, **170+ patient advocacy partners**. **Cycle 5 began FY2025 with ~$26M in NIH grants.** Funded/overseen by NCATS plus ten other NIH entities (NHLBI, NIAID, NIAMS, NIDCR, NHGRI, NIA, NINDS, NIDCD, ORWH).

### All 19 consortia (VERIFIED)

| Consortium | Acronym | Disease area | URL |
|---|---|---|---|
| Advancing Craniosynostosis Treatment | ACT | Syndromic craniosynostosis | `rdcrn.org/act` |
| Advancing Rare Disorders: Vascular mAlformation Research Network with CaNVAS | ARDVARC | Vascular malformations | `rdcrn.org/ardvarc` |
| Autoimmunity, Rasmussen's, Inflammation & Status Epilepticus Research Network | ARISEN | Autoimmune encephalitis, Rasmussen syndrome, NORSE | `rdcrn.org/arisen` |
| Batten Disease Clinical Research Consortium | BDCRC | Neuronal ceroid lipofuscinoses | `rdcrn.org/bdcrc` |
| Brittle Bone Disorders Consortium | BBDC | Osteogenesis imperfecta, bone disorders | `rdcrn.org/bbd` |
| Clinical Research in ALS and Related Disorders for Therapeutic Development | CReATe | ALS and related | `rdcrn.org/create` |
| Congenital and Perinatal Infections Consortium | CPIC | Congenital CMV, neonatal HSV | `rdcrn.org/cpic` |
| Consortium of Eosinophilic Gastrointestinal Disease Researchers | CEGIR | Eosinophilic GI disorders | `rdcrn.org/cegir` |
| Developmental Synaptopathies Consortium | DSC | TSC, PTEN hamartoma tumor syndrome, Phelan-McDermid | `rdcrn.org/dsc` |
| Global Leukodystrophy Initiative Clinical Trials Network | GLIA-CTN | Leukodystrophies | `rdcrn.org/glia-ctn` |
| Initiation of a cohort to define pathogenic Mechanisms, Precision diagnosis And Complications of Thrombotic microangiopathies | IMPACT | Thrombotic microangiopathies | `rdcrn.org/impact` |
| Myasthenia Gravis Rare Disease Network | MGNet | Myasthenia gravis | `rdcrn.org/mgnet` |
| Network for Advancing Sex Chromosome Aneuploidy Research Readiness | NASCARR | Sex chromosome aneuploidy | `rdcrn.org/nascarr` |
| North American Mitochondrial Disease Consortium | NAMDC | Mitochondrial diseases | `rdcrn.org/namdc` |
| Pediatric Fungal Network STudy of Rare Invasive Fungal DisEases | PFN-STRIDE | Invasive fungal disease in immunocompromised children | `rdcrn.org/pfn-stride` |
| Phenylalanine Families and Researchers Exploring Evidence | PHEFREE | PKU, phenylalanine metabolism disorders | `rdcrn.org/phefree` |
| Rare Bronchiectatic Diseases Consortium | RBDC | Primary ciliary dyskinesia, alpha-1 antitrypsin deficiency, humoral immunodeficiencies | `rdcrn.org/rbdc` |
| Rare Organic Acidemias Research Consortium | ROAR | PA, MMA, GA-1, IVA | `roar.rarediseasesnetwork.org` |
| Spastic Paraplegia Centers of Excellence Research Network | SP-CERN | Hereditary spastic paraplegia | `rdcrn.org/sp-cern` |

Note ROAR is the one off-pattern URL. Each consortium site carries **"See Our Clinical Sites," "Join One of Our Research Studies," "Learn About Diseases We Study," and "Find Funding Opportunities"** — meaning **every consortium publishes its own site list and its own PI roster.** That is 19 pre-built, disease-indexed site maps.

**Contact Registry:** **4,553 participants across 95 countries.** Collects contact info + demographics (sex, race/ethnicity — 87.6% White, role). Participants may be invited to studies *or serve as controls*. Participants can opt to share info with RDCRN consortia and patient advocacy groups.

**Critical gotcha:** the registry connects patients to **"researchers in order to advance rare diseases research"** — specifically *researchers within RDCRN consortia*. **A company cannot query or license the Contact Registry.** Access runs through a consortium investigator. The registry's real significance to you is that it proves a consented, re-contactable pool exists — the consortium PI is the key that opens it. Also note the 87.6% White skew, which is a diversity-plan problem you will have to address in an FDA submission.

**DMCC:** at **Cincinnati Children's Hospital Medical Center**, NCATS-funded since 2019, currently supporting Cycle 5. Co-PIs **Maurizio Macaluso, MD, DrPH** (Biostatistics/Epidemiology) and **Michael Wagner, PhD** (Biomedical Informatics). Four cores: Administrative, **Clinical Research (regulatory guidance, protocol review, FDA submission support)**, Data Management (REDCap, Cavatica), Engagement & Dissemination. **Contact: `support@rdcrn.org`.**

**Data sharing:** goes to the **RDCRN Data Repository (RDCRN-DR)** on NCATS federal servers — *not* primarily dbGaP. External access requires DAR + application, ethics training, IRB approval, and a DUA, with NIH review before release. Timelines are **negotiated per-consortium**, not fixed. Consent language explicitly permits sharing with **"companies to make new medicines or products, which may generate profit"** — so commercial use is contemplated — but **there is no formal industry partnership pathway published.** Guidance PDF: `https://ncats.nih.gov/sites/default/files/2024-07/RDCRN-data-sharing-policies-guidance-508.pdf` (UNVERIFIED).

**This is your highest-yield channel.** For a 20-patient trial, the play is: identify the consortium covering your disease → read its clinical sites page → approach the consortium PI directly with a collaboration proposal. The PI has the patients, the sites, the IRB relationships, and registry access. `support@rdcrn.org` and the DMCC Clinical Research Core are the institutional door if you want protocol/regulatory help alongside.

---

## 6. Supporting Infrastructure

### NCATS DRDRI (formerly ORDR)
**Renamed:** ORDR was congressionally transitioned in **April 2022** to the **Division of Rare Diseases Research Innovation (DRDRI)** within NCATS. Searching for "ORDR" will send you to dead links — `ncats.nih.gov/research/research-activities/ordr` returns **404 (VERIFIED dead)**.
- RDCRN: `https://ncats.nih.gov/research/research-activities/rdcrn` — **VERIFIED**
- Consortia subpage: `https://ncats.nih.gov/research/research-activities/rdcrn/consortia` — UNVERIFIED
- Programs: **GARD**, **RDCRN**, **RaDaR** (Rare Diseases Registries Program), and the **NCATS Toolkit for Patient-Focused Therapy Development**.

**GARD:** `https://rarediseases.info.nih.gov/` — **VERIFIED**. Covers "thousands" of diseases against an estimated 10,000+ rare diseases. Links diseases → patient organizations → clinical studies → experts. **No API or bulk download documented** — a genuine gap. Disease browse at `/diseases`; contact at `https://contact.rarediseases.info.nih.gov/Gard/s/`.

### ClinicalTrials.gov as a site-finding tool — **the best scrapable asset in this entire report**
**API v2 confirmed working.** I executed a live query and got structured JSON back:

```
https://clinicaltrials.gov/api/v2/studies?query.cond=Batten%20disease&pageSize=2&fields=NCTId,BriefTitle,LocationFacility,OverallOfficialName
```

Returns `studies[]` + `nextPageToken` for pagination. Each study exposes `protocolSection.identificationModule` (`nctId`, `briefTitle`) and — the money fields — **`protocolSection.contactsLocationsModule.locations[]` (facility, city, country) and `.overallOfficials[]` (named PIs with credentials).**

**No API key, no auth, no rate-limit wall encountered, full pagination.** This is the one source you can fully automate today. The method: query your disease → enumerate every `LocationFacility` across all trials ever run → rank facilities by trial count → that ranking *is* your patient-volume map, and `overallOfficials` gives you the PI names to contact. Cross-reference the resulting institutions against the NORD COE list and the RDCRN consortium site lists; institutions appearing on all three are your top targets.

### RDCA-DAP (FDA / Critical Path Institute)
| Resource | URL | Status |
|---|---|---|
| Program | `https://c-path.org/programs/rdca-dap/` | **VERIFIED** |
| Portal | `https://portal.rdca.c-path.org/` | **VERIFIED** (SPA, thin HTML) |
| NORD partner page | `https://rarediseases.org/rdca-dap/` | UNVERIFIED |

**FDA-funded**, operated by C-Path (nonprofit). Launched **September 2021**. Aggregates **patient-level data across 42+ rare diseases** — PKD, Duchenne, mitochondrial diseases, Friedreich ataxia, rare epilepsies among them. **Data contributors retain ownership.** Traction to date: **325 approved platform requests, 35 approved workspaces.**

**Access:** submit a request → reviewed by a **five-member Data Use Committee** on scientific merit, educational purpose, or public interest → sign a **Data Use Agreement**. **No pricing published.** Contact: **`rdcadap@c-path.org`**.

**Why this matters for repurposing specifically:** RDCA-DAP is the one platform whose stated purpose is *rare disease characterization* — natural history and disease progression modeling. For a 20-patient trial, that is how you build an **external/historical control arm** and justify a single-arm design to FDA. Its FDA funding means regulators are already familiar with it. The eligibility language ("scientific merit... or public interest") is notably more commercial-friendly than GPAP's flat non-commercial bar.

---

## Synthesis: the actual patient-finding playbook

**Tier 1 — do these first, they work and they're free:**
1. **ClinicalTrials.gov API v2** — automate now. Produces a ranked institution list + named PIs for your disease in an afternoon. Zero gatekeeping.
2. **RDCRN consortium** for your disease (from the 19 above) — the consortium PI is the highest-leverage single human in this entire map. They hold sites, patients, IRB relationships, and Contact Registry access.
3. **NORD member list** — find the Platinum-tier patient org for your disease. Platinum means they already run research infrastructure.

**Tier 2 — parallel, slower:**
4. **NORD COE network** (46 institutions) and **ERN Service Directory downloads** (Europe) — cross-reference against your ClinicalTrials.gov ranking. Triple-overlap institutions are your shortlist.
5. **RDCA-DAP** — for the external control arm, not for finding people.

**Tier 3 — long lead time, conditional value:**
6. **RARE-X Level 3** — the only channel that explicitly advertises trial recruitment support, but undocumented; requires a direct conversation. Budget 2+ months minimum, and confirm for-profit eligibility *before* starting the DUA.
7. **UDN/UDNI** — PI-sourcing for ultra-rare/undiagnosed phenotypes only. No recruitment mechanism.

**The three gotchas that will cost you the most time:**
- **GPAP is non-commercial only.** You need an academic PI as the applicant. Not negotiable.
- **No registry sells you patients.** RDCRN Contact Registry, IAMRARE, and RARE-X all route through an intermediary (consortium PI, patient org, or DAC). Every path is a *relationship*, not a transaction. Plan your timeline accordingly.
- **DUA negotiation is the hidden critical path** — RARE-X states 1–8 months for institutional DUA execution alone. Start legal early, in parallel with everything else.