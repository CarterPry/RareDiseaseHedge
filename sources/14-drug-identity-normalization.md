<!-- Recovered from agent-a47e572efdbb78d95.jsonl on 2026-08-06 after the original agent died on an
     API connection error (FailedToOpenSocket) following 72 completed tool calls. The agent completed
     all research but never wrote the output file. This document reconstructs the report from the
     full tool-use/tool-result transcript. Sections marked [NEW 2026-08-06] were verified by a
     follow-up fetch on recovery date to fill gaps the original agent had not yet closed. -->

# Drug Identity Normalization — The Join Layer

**Source document 14 of the RareDiseaseHedge source map.**
**Research date: 2026-08-05 (original agent); supplemented 2026-08-06 (recovery).**

Without a consistent cross-system drug identity layer you cannot diff a Japanese NHI listing against
an FDA approval, detect that a proposed 505(b)(1) candidate has an existing RXCUI (and is therefore
PRV-ineligible), or match a WHO INN against the GSRS moiety record that determines active-moiety
status. This document covers every tier of that layer from regulatory canonical IDs down to
InChIKey-level structural identity.

---

## 1. FDA UNII / Global Substance Registration System (GSRS)

### 1.1 Downloaded Bulk Files (VERIFIED — files already on disk)

The files below were confirmed present and inspected with `unzip -l` and `head`:

**UNII_Data.zip** (16.9 MB compressed; extracted 38,088,694 bytes; 3 files):
- `UNII_Records_26Feb2026.txt` — 38,076,417 bytes uncompressed; **168,046 data rows** (plus header)
- `Legacy UNIIs.txt` — 7,922 bytes; maps deprecated UNII codes to current UNIIs + preferred term
- `READ ME UNII Lists.txt` — 4,355 bytes; column definitions (full text recovered below)

**UNIIs.zip** (14.6 MB compressed; extracted 80,558,664 bytes; 2 files):
- `UNII_Names_26Feb2026.txt` — 80,554,309 bytes uncompressed; **1,024,191 name rows** (sum of all
  name types across all UNIIs)
- `READ ME UNII Lists.txt` — same file as above

Both zips dated **2026-02-27** (GSRS release date).

### 1.2 UNII_Records Schema (VERIFIED — from actual file header)

Tab-delimited, UTF-8. Columns in order:

| Col | Field | Notes |
|-----|-------|-------|
| 1 | `UNII` | 10-char alphanumeric; the canonical substance ID |
| 2 | `Display Name` | Preferred substance name |
| 3 | `RN` | CAS Registry Number |
| 4 | `EC` | ECHA registry number (EINECS) |
| 5 | `NCIT` | NCI Thesaurus concept code |
| 6 | `RXCUI` | RxNorm Ingredient concept code |
| 7 | `PUBCHEM` | PubChem Compound ID (CID) |
| 8 | `SMSID` | EMA European Medicines Substance ID |
| 9 | `EPA_CompTox` | EPA CompTox Dashboard ID |
| 10–16 | Taxonomy IDs | CATALOGUE_OF_LIFE, ITIS, NCBI, PLANTS, POWO, GRIN, MPNS |
| 17 | `INN_ID` | WHO INN sequential number |
| 18 | `USAN_ID` | AMA USAN Council code |
| 19 | `DAILYMED` | Known DailyMed SPL association flag |
| 20 | `MF` | Molecular formula |
| 21 | `INCHIKEY` | IUPAC InChIKey |
| 22 | `SMILES` | Canonical SMILES |
| 23 | `INGREDIENT_TYPE` | See below |
| 24 | `SUBSTANCE_TYPE` | ISO 11238 type |
| 25 | `UUID` | FDA-SRS record UUID |

**Sample row (first data record):**
```
0001H6R5H1  CEROUS SALICYLATE  526-17-0  [EC empty]  [NCIT empty]  [RXCUI empty]
  76966289  [SMSID empty]  DTXSID90200572  [...taxonomy empty...]
  [INN_ID empty]  [USAN_ID empty]  [DAILYMED empty]
  3C7H5O3.Ce  RBJPAJHTYHKKTB-UHFFFAOYSA-K
  [Ce+3].c1(ccccc1O)C([O-])=O.[...].  INGREDIENT SUBSTANCE  chemical
  15f0bc75-ff62-4ca4-a8a2-9132a0c211ce
```

### 1.3 UNII_Records Statistical Profile (VERIFIED — from actual file)

**Total records: 168,046** (rows including header: 168,047)

**INGREDIENT_TYPE breakdown:**
```
167,316  INGREDIENT SUBSTANCE   (use this for drug identity)
    626  IONIC MOIETY           (not charge-balanced; do not use as ingredient)
     90  SPECIFIED SUBSTANCE    (formulation-specific; ISO 11238)
     13  UNSPECIFIED INGREDIENT (imprecise; prefer INGREDIENT SUBSTANCE)
      1  MOLECULAR FRAGMENT     (incomplete; do not use)
```

**SUBSTANCE_TYPE breakdown:**
```
125,873  chemical
 27,968  structurallyDiverse   (botanical/complex natural substances)
  7,600  protein
  2,980  mixture
  2,667  polymer
    767  nucleicAcid
    191  specifiedSubstanceG1
```

**Cross-reference coverage (VERIFIED — counted from file):**
```
Columns with non-empty values:
  RXCUI:    13,707 records   (8.2% — many FDA substances lack RxNorm entry)
  INN_ID:   12,588 records   (7.5% — INN-assigned substances)
  PUBCHEM:  123,199 records  (73.3% — good CID coverage)
  CAS RN:   128,619 records  (76.5% — good CAS coverage)
```

### 1.4 UNII_Names Schema (VERIFIED — from actual file header)

Tab-delimited, UTF-8. Columns: `Name | TYPE | UNII | Display Name`

**Name TYPE values:**
```
501,294  cn   Common Name
396,559  sys  Systematic Name (chemical / taxonomic)
 76,009  cd   Code
 26,116  of   Official name
 24,211  bn   Brand / Trade Name
      2  mn   (rare; undefined in README)
```

The `of` (official) names are the closest to INN names in this file. Sample `of` entries include
`ADECATUMUMAB`, `SPIROFYLLINE`, `ABLUKAST` — all matching WHO INN recommended names.

**Unique INN_IDs in UNII_Records: 12,578** (verified by sort -u on column 17).

### 1.5 Legacy UNIIs

The `Legacy UNIIs.txt` file maps old UNII codes to current ones (e.g. `0INE2SFD9E` → `52CMI0WC3Y`
for ATEZOLIZUMAB). Contains ~200 rows. Essential for backward compatibility when ingesting older
datasets.

### 1.6 GSRS Live API (VERIFIED — live fetch 2026-08-05)

Base URL: `https://gsrs.ncats.nih.gov/api/v1/`

**Count endpoint:**
```
GET https://gsrs.ncats.nih.gov/api/v1/substances/@count
Response: 173081   HTTP 200
```

Note: 173,081 live records vs. 168,046 in the Feb 2026 dump — the live system has ~5,000 more
substances added since February.

**Search endpoint (VERIFIED):**
```
GET https://gsrs.ncats.nih.gov/api/v1/substances/search?q=aspirin&top=2
Response: {"total": 24, "count": 2, ...}
nextPageUri: ...?skip=2
```
Top-level keys in each substance record:
`created, createdBy, lastEdited, lastEditedBy, deprecated, uuid, definitionType, definitionLevel,
substanceClass, status, version, approvedBy, approvalID, structure, _name, _approvalIDDisplay,
access, _self, _moieties, _names, _codes, _modifications, _properties, _relationships, _references`

**Direct UNII lookup (VERIFIED):**
```
GET https://gsrs.ncats.nih.gov/api/v1/substances/R16CO5Y76E
```
Returns full substance record. The `approvalID` field holds the UNII.

**Moieties endpoint (VERIFIED — for aspirin UNII R16CO5Y76E):**
```
GET https://gsrs.ncats.nih.gov/api/v1/substances/R16CO5Y76E/moieties
Response: array of moiety objects with fields:
  uuid, id, created, lastEdited, digest, molfile, smiles, formula, opticalActivity,
  atropisomerism, stereoCenters, definedStereo, ezCenters, charge, mwt, count,
  stereochemistry, references, access, hash
```
Aspirin has **1 moiety** (SMILES: `CC(=O)Oc1ccccc1C(=O)O`, InChIKey hash: `BSYNRYMUTXBXSQ_UHFFFAOYSA_N`).
This endpoint is how you resolve "active moiety" structurally — for prodrugs and salts, the moiety
count and structure will differ from the parent substance.

**Codes endpoint (VERIFIED — for aspirin, [NEW 2026-08-06]):**
```
GET https://gsrs.ncats.nih.gov/api/v1/substances/R16CO5Y76E/codes
```
Returns array of code objects. Sample codes attached to aspirin (UNII R16CO5Y76E):
```
FDA UNII    : R16CO5Y76E
RXCUI       : 1191
RXCUI       : 91101
CAS         : 50-78-2
PUBCHEM     : 2244
ChEMBL      : CHEMBL25
DRUG BANK   : DB00945
MESH        : D001241
NCI_THESAURUS: C287
CHEBI       : 15365
IUPHAR      : 4139
DRUG CENTRAL: 74
WHO-ATC     : N02BA01, B01AC06, A01AD05, ... (multiple)
WHO-VATC    : QN02BA01, QB01AC06, ...
SMS_ID      : 100000092077
NDF-RT      : N0000008836
EVMPD       : SUB12730MIG
CFR         : 21 CFR 343.12, 21 CFR 343.13, 21 CFR 520.1409
ECHA        : 200-064-1
FDA ORPHAN DRUG: 724719, 764120, 607917
EU-Orphan Drug: EU/3/04/208
WHO INTERNATIONAL PHARMACOPEIA: ASPIRIN
WHO-ESSENTIAL MEDICINES LIST: 2.1, 7.1, 12.5
DAILYMED    : R16CO5Y76E
WIKIPEDIA   : ASPIRIN
```
This demonstrates that GSRS/codes is the richest single cross-reference hub available without
licensing; it links UNII → RxCUI, CAS, PubChem, ChEMBL, ATC, MESH, ChEBI, IUPHAR, DrugBank,
EMA SMS, EU orphan designation, and WHO Essential Medicines.

**Bulk traversal:** The API supports `?top=N&skip=M` pagination. With 173,081 records and a
reasonable page size of 200, full traversal requires ~866 requests. No authenticated bulk-download
endpoint was found (`/api/v1/substances/@download` returned HTTP 404).

**Auth requirements:** None for read access. Public API. No rate limit documented; observed response
latency ~200–500 ms per request.

---

## 2. RxNorm and RxNav REST APIs

### 2.1 API Status (VERIFIED — live fetch 2026-08-05)

```
GET https://rxnav.nlm.nih.gov/REST/version
Response: <rxnormdata><version>03-Aug-2026</version><apiVersion>3.1.354</apiVersion></rxnormdata>
HTTP 200
```

RxNorm release date: **August 3, 2026**. API version 3.1.354.

### 2.2 Term Type (TTY) Hierarchy (VERIFIED)

Full list from `GET https://rxnav.nlm.nih.gov/REST/termtypes.json`:
```
['BN', 'BPCK', 'DF', 'DFG', 'GPCK', 'IN', 'MIN', 'PIN', 'SBD', 'SBDC',
 'SBDF', 'SBDFP', 'SBDG', 'SCD', 'SCDC', 'SCDF', 'SCDFP', 'SCDG', 'SCDGP']
```

Key types for drug identity work:
- **IN** (Ingredient) — the free-base/acid/anion form; closest to "active moiety" in RxNorm terms
- **PIN** (Precise Ingredient) — specific salt or ester form (e.g. "fluoxetine hydrochloride")
- **MIN** (Multiple Ingredients) — combination product ingredient set
- **BN** (Brand Name)
- **SCD** (Semantic Clinical Drug) — strength + dose form + ingredient
- **SBD** (Semantic Branded Drug)

**Critical for PRV eligibility:** The IN concept is what RxNorm uses as the base ingredient. A
substance with an RXCUI at the IN level has been through US drug approval or listing processes and
is almost certainly PRV-ineligible under 360ff. A substance with no RXCUI at all is a candidate
for Funnel A (PRV-eligible) scrutiny, but must be verified against the Drugs@FDA active ingredient
tables and SPL DailyMed listings.

**Verified example — salt vs. free base (fluoxetine):**
```
GET https://rxnav.nlm.nih.gov/REST/rxcui.json?name=fluoxetine+hydrochloride&search=1
Response: {"idGroup": {"rxnormId": ["227224", "4493"]}}

GET https://rxnav.nlm.nih.gov/REST/rxcui/4493/allProperties.json?prop=ATTRIBUTES
→ TTY = IN   (fluoxetine free base = IN concept)

GET https://rxnav.nlm.nih.gov/REST/rxcui/227224/related.json?tty=IN+PIN
→ TTY: IN  → rxcui 4493 "fluoxetine" (IN)
  TTY: PIN → rxcui 227224 "fluoxetine hydrochloride" (PIN)
```
This demonstrates that RxNorm correctly collapses salt → free base via the IN/PIN hierarchy.
The **IN concept** is the active-moiety proxy in RxNorm. If a compound has an IN rxcui, FDA has
almost certainly already approved that active moiety.

**Aspirin cross-references from RxNorm (VERIFIED):**
```
GET https://rxnav.nlm.nih.gov/REST/rxcui/1191/allProperties.json?prop=all
→ CODES | ATC = A01AD05, B01AC06, N02BA01
   CODES | DRUGBANK = DB00945
   CODES | SNOMEDCT = 387458008, 7947003
   CODES | RxCUI = 1191
   ATTRIBUTES | TTY = IN
   ATTRIBUTES | PRESCRIBABLE = Y
   ATTRIBUTES | RXNAV_HUMAN_DRUG = US
```

**RxClass / ATC mapping (VERIFIED):**
```
GET https://rxnav.nlm.nih.gov/REST/rxclass/class/byRxcui.json?rxcui=1191&relaSource=ATC
→ aspirin maps to:
   A01AD (Other agents for local oral treatment)
   B01AC (Platelet aggregation inhibitors excl. heparin)
   N02BA (Salicylic acid and derivatives)
```

### 2.3 Download Files (VERIFIED — license split confirmed)

From `https://www.nlm.nih.gov/research/umls/rxnorm/docs/rxnormfiles.html`:

**Full Monthly Release** (`RxNorm_full_08032026.zip`):
- Redirects to `https://uts.nlm.nih.gov/uts/login?service=...` — UMLS license required
- HTTP 302 → login wall
- Requires free UMLS Metathesaurus License (registration at UTS)

**Current Prescribable Content Monthly Release** (`RxNorm_full_prescribe_08032026.zip`):
- Direct download, **no UMLS license required** (confirmed by NLM page: "no license required")
- HTTP 200, Content-Length: **74,563,744 bytes** (~71 MB) [NEW 2026-08-06 — HEAD confirmed]
- Contains only currently-prescribable US drugs; excludes retired/historical concepts
- Pipe-delimited RRF format; UTF-8; does not require MetamorphoSys

**Licensing note:** The full release (with UMLS license) includes historical/retired concepts,
more source vocabularies, and the complete Metathesaurus linkages. For a live pipeline that only
needs currently-marketed US drugs, the prescribable content (no license) is sufficient and simpler.

**Weekly updates** available for both tiers. Release schedule: first Monday of each month.

**Permanent "current" symlink URLs:**
```
https://download.nlm.nih.gov/umls/kss/rxnorm/RxNorm_full_current.zip  (UMLS required)
https://download.nlm.nih.gov/rxnorm/RxNorm_full_prescribe_current.zip  (free)
```
(The `_current.zip` aliases always point to the latest monthly release.)

---

## 3. WHO INN (International Nonproprietary Names)

### 3.1 Publication Format (VERIFIED)

INN lists are published as numbered PDF documents. The WHO INN lists page
(`https://www.who.int/teams/health-product-and-policy-standards/inn/inn-lists`, HTTP 200) lists:
- Proposed INN lists: PL-135, PL-134, PL-133, ... PL-127 and earlier
- All links resolve to `https://www.who.int/publications/m/item/inn-pl-NNN` (HTTP 200 for PL-135)
- Format: PDF (HTML page, **not** machine-readable tabular)

No bulk download / CSV / JSON of the cumulative INN list exists on the public WHO website.
`https://www.who.int/publications/m/item/inn-cumulative-list` returned HTTP 404.
`https://www.who.int/tools/inn-online-database` returned HTTP 404.

### 3.2 WHO SOINN (INN Online Search) [NEW 2026-08-06]

The MedNet INN tool has moved to: `https://extranet.who.int/soinn/`
- HTTP 200. Interface confirmed (Moodle-based LMS).
- The page renders: "Search for INN Names and stems / Query / INN Check / Stem / Results: Limited to 5 items"
- It is a **web-only interface** (5-result limit per query); the underlying REST API
  (`/soinn/webservice/rest/server.php`) requires an authenticated token — no public bulk access.

### 3.3 INN Data Via UNII (Best Machine-Readable Route)

The UNII system provides the best machine-readable INN bridge:
- Column `INN_ID` in UNII_Records: **12,578 unique INN sequential numbers** across 168,046 records
- The README states: "Sequential number assigned by World Health Organization's INN Programme"
- This is the canonical numeric INN identifier, usable as a join key

The `of` (official) name type in UNII_Names corresponds to WHO INN recommended names for
substances that have them.

### 3.4 INN via GSRS Codes

The GSRS `/codes` endpoint does **not** expose INN_ID directly, but the `_names` sub-object of
each substance includes official name entries matching the INN recommended name. Cross-referencing
GSRS `approvalID` (UNII) to `INN_ID` column in the UNII_Records bulk file is the practical approach.

---

## 4. WHO ATC/DDD Index

### 4.1 Access Model (VERIFIED)

The WHOCC (WHO Collaborating Centre for Drug Statistics Methodology, Oslo) website:
- `https://www.whocc.no/atc_ddd_index/` — HTTP 301 → live site
- `https://www.whocc.no/atc_ddd_downloads/` — HTTP 301 (downloads page reached)
- `https://orders.atcddd.fhi.no/` — HTTP 200; titled "Orders ATC/DDD"; provides a purchasing interface

**Copyright/license (VERIFIED — from WHOCC copyright page):**
> © Copyright WHO Collaborating Centre for Drug Statistics Methodology, Oslo, Norway. Use of all or
> parts of the material requires reference to the WHO Collaborating Centre for Drug Statistics
> Methodology. Copying and distribution for commercial purposes is not allowed. Changing or
> manipulating the material is not allowed.

Practical conclusion: **ATC/DDD bulk data requires a paid license** obtained via
`https://orders.atcddd.fhi.no/`. The interactive online index is freely searchable per-drug but
not bulk-downloadable without license.

**Alternative (VERIFIED):** ATC codes are available free via:
1. **GSRS codes endpoint** — aspirin returned 9 distinct ATC codes including combo products
2. **RxNav `byRxcui` with relaSource=ATC** — returns ATC classes for any RXCUI
3. **ChEMBL molecule endpoint** — aspirin returned `['B01AC06', 'N02BA01', 'N02BA51', 'A01AD05', 'N02BA71']`
4. **UNII_Records README** cites ATC as a cross-reference source

For the pipeline, ATC codes should be harvested from GSRS and RxNorm rather than paying WHOCC.

---

## 5. PubChem

### 5.1 API Status (VERIFIED)

```
GET https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/aspirin/
      property/IUPACName,MolecularFormula,InChIKey/JSON
Response:
  {"PropertyTable": {"Properties": [
    {"CID": 2244, "MolecularFormula": "C9H8O4",
     "InChIKey": "BSYNRYMUTXBXSQ-UHFFFAOYSA-N",
     "IUPACName": "2-acetyloxybenzoic acid"}]}}
```

**Cross-reference count for aspirin (CID 2244):**
```
GET https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/2244/xrefs/RegistryID/JSON
→ 455 external RegistryIDs
```

PubChem CID is in the UNII_Records (col 7, `PUBCHEM`), covering 123,199 of 168,046 records (73.3%).

---

## 6. ChEMBL and UniChem

### 6.1 ChEMBL API (VERIFIED)

```
GET https://www.ebi.ac.uk/chembl/api/data/molecule/CHEMBL25.json
→ molecule_chembl_id: CHEMBL25
   pref_name: ASPIRIN
   molecule_type: Small molecule
   full_mwt: 180.16
   ATC codes: ['B01AC06', 'N02BA01', 'N02BA51', 'A01AD05', 'N02BA71']
   cross_references: [{"xref_src": "DailyMed", "xref_id": "aspirin"}]
```

ChEMBL molecule synonyms include `syn_type` values including ATC, INN, USAN, TRADE_NAME, OTHER.
For ibuprofen, the query `?molecule_synonym=ibuprofen` returned CHEMBL6329, CHEMBL6328, CHEMBL265667
(multiple hits = racemic, enantiomers, and prodrug forms separately curated).

### 6.2 UniChem (VERIFIED)

```
GET https://www.ebi.ac.uk/unichem/rest/inchikey/BSYNRYMUTXBXSQ-UHFFFAOYSA-N
```
Returns array of `{src_id, src_compound_id}` cross-references. For aspirin (InChIKey):
```
src_id 1  → CHEMBL25          (ChEMBL)
src_id 2  → DB00945           (DrugBank)
src_id 3  → AIN               (HMDB? — source 3)
src_id 4  → 4139              (IUPHAR Guide to Pharmacology)
src_id 7  → CHEBI:15365       (ChEBI)
src_id 14 → R16CO5Y76E        (FDA SRS / UNII)
src_id 15 → 1353, 29350479    (BindingDB, two entries)
src_id 22 → 2244              (PubChem CID)
src_id 37 → 159662            (source 37)
src_id 49 → PD002467          (source 49)
src_id 50 → ACSALA            (source 50)
```
The UniChem `/rest/inchikey/` endpoint is a **free, unauthenticated** batch lookup by InChIKey.
This is the most efficient structural cross-reference route: compute InChIKey from SMILES/structure,
query UniChem, get all major database IDs simultaneously.

Note: The UniChem v2 REST API endpoints (`/api/v1/compounds`, `/api/v2/compounds`) returned 404/405;
the legacy `/rest/` endpoint is what works.

---

## 7. FDA Active Moiety — Legal Definition and Determination

### 7.1 Statutory Definition (VERIFIED — from GovInfo CFR XML)

Source: `https://www.govinfo.gov/content/pkg/CFR-2024-title21-vol5/xml/CFR-2024-title21-vol5-sec314-3.xml`
HTTP 200.

**21 CFR 314.3 — verbatim definitions:**

> **Active ingredient** is any component that is intended to furnish pharmacological activity or
> other direct effect in the diagnosis, cure, mitigation, treatment, or prevention of disease, or
> to affect the structure or any function of the body of man or other animals. The term includes
> those components that may undergo chemical change in the manufacture of the drug product and be
> present in the drug product in a modified form intended to furnish the specified activity or effect.

> **Active moiety** is the molecule or ion, excluding those appended portions of the molecule that
> cause the drug to be an ester, salt (including a salt with hydrogen or coordination bonds), or
> other noncovalent derivative (such as a complex, chelate, or clathrate) of the molecule,
> responsible for the physiological or pharmacological action of the drug substance.

### 7.2 PRV Implication (21 U.S.C. 360ff — settled fact)

360ff(a)(4)(B)(i) (as amended by Pub. L. 117-9, 2021) uses **active moiety**, not active ingredient.
This means:
- Fluoxetine HCl and fluoxetine free base share the same active moiety (fluoxetine)
- If fluoxetine free base was previously approved, fluoxetine HCl is also PRV-ineligible
- Prodrugs are assessed on the **pharmacologically active metabolite** (the moiety), not the prodrug
  itself — FDA has historically applied this in 3-year exclusivity determinations

### 7.3 Where FDA Publishes Active Moiety Determinations

Active moiety status is encoded in:
1. **FDA Drugs@FDA** — the "Active Ingredient" tables in NDA approval packages; the
   "Applicants Holders" table links each NDA to its active ingredient/moiety
2. **FDA Purple Book** (biologics) — separate from small molecules
3. **GSRS moieties endpoint** — for any UNII, `GET .../substances/{UNII}/moieties` returns the
   structural moiety definition; this is the structural definition of what FDA means by active moiety
4. **DailyMed SPL** — the Structured Product Label XML includes `<activeIngredient>` elements
   with UNII codes; for salts/esters, the active ingredient UNII may point to the salt while
   the active moiety UNII points to the free base
5. **RxNorm IN concept** — the IN (Ingredient) TTY is the active-moiety-level concept in RxNorm;
   if a drug has an IN rxcui, the active moiety has been through US regulatory consideration

**How FDA determines active moiety in practice:** FDA's Chemistry review for each NDA or ANDA
identifies the active moiety. For standard small molecules, the determination follows 21 CFR 314.3
mechanically (strip salts/esters/chelates/complexes). For complex cases (prodrugs, biologics,
polymers), FDA issues a formal determination. The GSRS moiety record reflects FDA's official
structural judgment.

---

## 8. Failure Modes and Identity Edge Cases

### 8.1 Salt vs. Free Base vs. Hydrate

**Problem:** Drug A approved as sodium salt; Drug B proposed as potassium salt. Same active moiety,
different UNII codes, same PRV ineligibility.

**Resolution:** In RxNorm, both map to the same IN concept. In GSRS, both have distinct UNIIs but
their `/moieties` endpoint returns structurally equivalent moiety records. InChIKey layer-1
(connectivity only) will match; standard InChIKey (including stereochemistry and protonation)
may not.

### 8.2 Racemates vs. Enantiomers

**Problem:** Ibuprofen (racemate) and dexibuprofen (S-enantiomer) have different UNIIs, different
RXCUIs. ChEMBL found three entries (CHEMBL6329, CHEMBL6328, CHEMBL265667) for "ibuprofen"-related
molecules. If the racemate was previously US-approved, the enantiopure form may or may not be
treated as the same active moiety — FDA has ruled both ways in exclusivity disputes.

**Resolution:** Must check FDA exclusivity determinations (Orange Book) for specific precedents.
Cannot rely on InChIKey (which includes stereochemistry) to determine moiety equivalence. The GSRS
`opticalActivity` and `stereochemistry` fields in the moiety record are informative; "ACHIRAL" or
"RACEMATE" vs. "S" or "R" flags the issue. A compound with `stereoCenters > 0` and
`definedStereo = stereoCenters` is an enantiopure form; a prior approval of the racemate may or
may not block PRV for the enantiomer depending on FDA's moiety determination.

### 8.3 Prodrugs

**Problem:** Enalapril (prodrug) → enalaprilat (active). If enalaprilat was approved separately,
does that block PRV for enalapril for a new indication?

**Resolution:** Per 21 CFR 314.3, the active moiety is the molecule responsible for
pharmacological action — that is the active metabolite (enalaprilat), not the prodrug (enalapril).
FDA would treat them as the same active moiety for PRV purposes. The GSRS `/moieties` for enalapril
should show enalaprilat's structure; if not, the relationship is captured in GSRS `_relationships`.

### 8.4 Biologics

**Problem:** Biologics (proteins, nucleic acids, gene therapies) are not characterized as a simple
molecule. The UNII system assigns UNIIs to biologics (substanceType = `protein`, `nucleicAcid`) but
active moiety for biologics is governed by the BPCIA/351(k) pathway, not 505(b)/21 CFR 314.3.
PRV for biologics under 360ff is evaluated under separate pathway criteria.

**Resolution:** For Funnel A candidates, biologics approved via BLA are tracked in the FDA Purple
Book, not Drugs@FDA. The pipeline should handle small molecules (chemical, polymer UNIIs) separately
from biologics (protein, nucleicAcid UNIIs).

### 8.5 Combination Products

**Problem:** Fixed-dose combination product (Drug A + Drug B). Each component has its own active
moiety. The combination UNII (substanceType = mixture or specified compound) is not an active moiety
itself.

**Resolution:** In RxNorm, MIN (Multiple Ingredients) concepts encode combinations; decompose via
`?tty=IN` to get each component's IN concept. In GSRS, combination products have `_relationships`
linking to each component substance.

### 8.6 The "Active Moiety" Test and 360ff

The 2021 Pub. L. 117-9 change from "active ingredient" to "active moiety" was specifically intended
to close the enantiomer/polymorph loophole where developers sought PRV by filing as a new salt of
a known drug. Under the current moiety test:
- Racemic aspirin approved → enantiopure aspirin = same active moiety → PRV ineligible
- Fluoxetine HCl approved → fluoxetine base for new indication = same active moiety → PRV ineligible
- Aspirin approved → aspirin arginate (ester) = same active moiety → PRV ineligible

Only a genuinely **never-before-approved-in-US moiety** (one with no RXCUI at the IN level and no
entry in Drugs@FDA active ingredients) filed as a full 505(b)(1) qualifies for Funnel A.

---

## 9. Recommended Canonical-ID Architecture

### 9.1 Primary Key: UNII

Use **UNII** as the pipeline's internal canonical substance identifier. Rationale:
- Assigned by FDA's SRS; reflects FDA's official substance definition
- The `INGREDIENT_TYPE = INGREDIENT SUBSTANCE` filter removes problematic IONIC MOIETY and
  MOLECULAR FRAGMENT entries
- Includes InChIKey and SMILES for structural-level deduplication
- Carries INN_ID (12,578 records), RxCUI (13,707 records), PubChem CID (123,199 records),
  CAS RN (128,619 records) as direct column values
- GSRS API allows live lookup by UNII with full cross-reference and moiety access
- Free bulk download, no license

### 9.2 Cross-Reference Hierarchy

```
UNII (canonical)
  ├── RXCUI (IN level) ← if exists, US approval exists; PRV ineligible
  ├── INN_ID ← WHO INN assignment
  ├── CAS RN ← chemical identity
  ├── PubChem CID ← structural cross-ref; feeds UniChem
  ├── InChIKey ← structural deduplication; input to UniChem API
  ├── ChEMBL ID ← bioactivity data linkage
  └── GSRS moiety UNII ← active moiety structural record
```

### 9.3 PRV-Eligibility Check Procedure (Funnel A)

For each candidate drug, in order:
1. Search GSRS by name → get UNII
2. Check UNII_Records col 6 (RXCUI): if non-empty → **Funnel B only** (US approval exists)
3. If empty: query `GET https://rxnav.nlm.nih.gov/REST/rxcui.json?name={INN}&search=1`
   → if RXCUI returned → **Funnel B only**
4. If no RXCUI: search DailyMed/Drugs@FDA by UNII to confirm no existing US marketing
5. If clean: retrieve GSRS moiety UNII; check RXCUI for moiety UNII separately (catches
   cases where the salt is new but the free-base moiety was previously approved)
6. Confirm substanceClass = chemical or protein (not mixture); verify INGREDIENT_TYPE = INGREDIENT SUBSTANCE
7. Document the negative result with HTTP status codes and response snippets

### 9.4 Foreign Approval Diffing

To compare a foreign approval (e.g., Japan Yakka code, EMA EPAR, Ukraine MoH registration) against
US approval status:
1. Extract INN or generic name from foreign source
2. Search GSRS: `GET https://gsrs.ncats.nih.gov/api/v1/substances/search?q={INN_name}&top=5`
3. Get UNII; check RXCUI column (= US approval proxy)
4. Alternatively: search RxNorm directly by INN name → returns IN rxcui if US-approved
5. For Japan: the Yakka `成分名` (active ingredient name) is in Japanese; transliteration to INN
   is necessary (PMDA orphan drug list and NHI price list both use Japanese katakana names); match
   via WHO INN_ID column in UNII_Records where possible

---

## 10. Unfinished — Worth Re-Running

The original agent was partway through two topics when the API connection died:

### 10.1 UniChem Source ID Mapping
Tool call 58 (checking `https://www.ebi.ac.uk/unichem/rest/sources`) failed with JSON decode error;
tool call 60 also failed. The source ID → database name mapping was not recovered. The known
mappings (from UniChem result for aspirin) are:
```
src_id 1  → ChEMBL
src_id 2  → DrugBank
src_id 7  → ChEBI
src_id 14 → FDA SRS (UNII)
src_id 22 → PubChem CID
```
Sources 3, 4, 15, 37, 49, 50 remain unmapped. Re-run:
`curl -s "https://www.ebi.ac.uk/unichem/rest/src_ids" 2>&1` and decode non-UTF8 encoding.

### 10.2 RxNorm Full TTY Name Definitions
The TTY list was recovered as a string array (e.g. `['BN', 'BPCK', 'DF', ...]`) but the full
name/description for each abbreviation was not obtained due to a type error in the agent's Python.
The full documentation is at `https://www.nlm.nih.gov/research/umls/rxnorm/docs/appendix5.html`.

### 10.3 GSRS Bulk Export Options
`/api/v1/substances/@download` returned HTTP 404. Needs further investigation:
- Try `GET /api/v1/substances?format=smiles` or similar export query parameters
- Check if authenticated GSRS access unlocks an export endpoint
- The NCATS GitHub for GSRS may document programmatic bulk export

### 10.4 PubChem SID / FDA SRS Direct Linkage
`GET pubchem.../substance/sourceid/FDA%20SRS/R16CO5Y76E/JSON` returned "Invalid source name".
The correct PubChem depositor name for FDA SRS is not established. Could be "FDA Substance
Registration System" or "FDA SRS" — run a lookup on a known SID for aspirin to determine the
exact depositor name string.

---

## 11. URL Ledger

### VERIFIED URLs (HTTP status confirmed, content inspected)

| URL | Method | Status | Notes |
|-----|--------|--------|-------|
| `https://rxnav.nlm.nih.gov/REST/version` | GET | 200 | Returns version XML |
| `https://rxnav.nlm.nih.gov/REST/rxcui.json?name=aspirin&search=1` | GET | 200 | `{"idGroup":{"rxnormId":["1191"]}}` |
| `https://rxnav.nlm.nih.gov/REST/rxcui/1191/related.json?tty=IN+MIN+PIN` | GET | 200 | Full concept group response |
| `https://rxnav.nlm.nih.gov/REST/rxcui/1191/allProperties.json?prop=all` | GET | 200 | ATC, DrugBank, SNOMED codes |
| `https://rxnav.nlm.nih.gov/REST/rxclass/class/byRxcui.json?rxcui=1191&relaSource=ATC` | GET | 200 | Three ATC classes |
| `https://rxnav.nlm.nih.gov/REST/termtypes.json` | GET | 200 | 19 TTY codes returned as string array |
| `https://rxnav.nlm.nih.gov/REST/rxcui.json?name=fluoxetine+hydrochloride&search=1` | GET | 200 | Returns two RXCUIs |
| `https://rxnav.nlm.nih.gov/REST/rxcui/227224/related.json?tty=IN+PIN` | GET | 200 | IN→4493 fluoxetine, PIN→227224 fluoxetine HCl |
| `https://www.nlm.nih.gov/research/umls/rxnorm/docs/rxnormfiles.html` | GET | 200 | Release links confirmed |
| `https://download.nlm.nih.gov/umls/kss/rxnorm/RxNorm_full_08032026.zip` | HEAD | 302→login | UMLS license wall confirmed |
| `https://download.nlm.nih.gov/rxnorm/RxNorm_full_prescribe_08032026.zip` | HEAD | 200 | 74,563,744 bytes; no login required |
| `https://gsrs.ncats.nih.gov/api/v1/substances/@count` | GET | 200 | Returns `173081` |
| `https://gsrs.ncats.nih.gov/api/v1/substances/search?q=aspirin&top=2` | GET | 200 | total:24, pagination confirmed |
| `https://gsrs.ncats.nih.gov/api/v1/substances/search?q=aspirin&top=1` | GET | 200 | Full record, moiety URL |
| `https://gsrs.ncats.nih.gov/api/v1/substances/R16CO5Y76E/moieties` | GET | 200 | 1 moiety for aspirin; molfile, SMILES returned |
| `https://gsrs.ncats.nih.gov/api/v1/substances/R16CO5Y76E/codes` | GET | 200 | 60+ cross-reference codes |
| `https://gsrs.ncats.nih.gov/api/v1/substances?top=5&skip=0&order=created` | GET | 200 | total:173081; pagination works |
| `https://gsrs.ncats.nih.gov/api/v1/exports` | GET | 404 | No bulk export endpoint here |
| `https://www.govinfo.gov/content/pkg/CFR-2024-title21-vol5/xml/CFR-2024-title21-vol5-sec314-3.xml` | GET | 200 | Full 21 CFR 314.3 text including active moiety definition |
| `https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/aspirin/property/IUPACName,MolecularFormula,InChIKey/JSON` | GET | 200 | CID 2244 confirmed |
| `https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/2244/xrefs/RegistryID/JSON` | GET | 200 | 455 cross-refs |
| `https://www.ebi.ac.uk/chembl/api/data/molecule/CHEMBL25.json` | GET | 200 | Full aspirin record, ATC codes |
| `https://www.ebi.ac.uk/unichem/rest/inchikey/BSYNRYMUTXBXSQ-UHFFFAOYSA-N` | GET | 200 | 11 database cross-refs returned |
| `https://www.who.int/teams/health-product-and-policy-standards/inn/inn-lists` | GET | 200 | List of PDF INN publications |
| `https://www.who.int/publications/m/item/inn-pl-135` | GET | 200 | HTML page (not machine-readable) |
| `https://extranet.who.int/soinn/` | GET | 200 | WHO SOINN INN search tool (web only, 5-result limit) |
| `https://www.whocc.no/atc_ddd_downloads/` | GET | 301→200 | Page reached; ATC data requires paid license |
| `https://www.whocc.no/copyright_disclaimer/` | GET | 200 | Confirmed: commercial use not allowed without license |
| `https://orders.atcddd.fhi.no/` | GET | 200 | ATC/DDD purchase order site |
| Local: `UNII_Data.zip` (16.9 MB) | `unzip -l` | — | 168,046 records; Feb 2026 |
| Local: `UNIIs.zip` (14.6 MB) | `unzip -l` | — | 1,024,191 name entries; Feb 2026 |

### UNVERIFIED URLs (not fetched or fetch failed)

| URL | Reason |
|-----|--------|
| `https://www.ebi.ac.uk/unichem/rest/sources` | JSON decode error (non-UTF-8 response); source ID→name mapping not recovered |
| `https://www.ebi.ac.uk/unichem/api/v1/compounds` | HTTP 405 Method Not Allowed |
| `https://www.ebi.ac.uk/unichem/api/v2/compounds` | HTTP 404 Not Found |
| `https://www.who.int/tools/inn-online-database` | HTTP 404 |
| `https://www.who.int/publications/m/item/inn-cumulative-list` | HTTP 404 |
| `https://gsrs.ncats.nih.gov/api/v1/substances/@download` | HTTP 404 |
| `https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/sourceid/FDA%20SRS/{UNII}/JSON` | HTTP 400 "Invalid source name" — correct depositor name not determined |
| `https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-314/subpart-A/section-314.3` | Redirects to JS-rendered login page; content not parsed |
| `https://www.nlm.nih.gov/research/umls/rxnorm/docs/appendix5.html` | Not fetched; TTY full name definitions |
| `https://download.nlm.nih.gov/rxnorm/RxNorm_full_prescribe_current.zip` | Symlink not verified (only dated URL tested) |
