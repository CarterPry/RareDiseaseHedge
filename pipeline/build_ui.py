#!/usr/bin/env python3
"""
Build the candidate dashboard from the pipeline's summary.json.

Plain-language-first, single-file HTML: data + scoring embedded inline, vanilla
JS, no build step, opens by double-click, works offline. The simple searchable
card list is the whole default surface; all analyst machinery (promise score,
funnel, competitor monitor, EV proxy) lives behind one collapsed "Advanced"
section.

Reads  pipeline/data/out/summary.json
Writes pipeline/ui/index.html
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SUMMARY = os.path.join(HERE, "data", "out", "summary.json")
OUT_DIR = os.path.join(HERE, "ui")
OUT = os.path.join(OUT_DIR, "index.html")

# --- scoring inputs ported verbatim from SCORING_MODEL.md --------------------
PED_STRONG = [
 "pediatric","paediatric","children","child","infant","neonatal","congenital",
 "inherited","inborn","lysosomal","mucopolysaccharid","gaucher","fabry","pompe",
 "niemann-pick","krabbe","batten","neuronal ceroid","spinal muscular atrophy","sma",
 "duchenne","friedreich","hunter syndrome","hurler","sanfilippo","glycogen storage",
 "fatty acid oxidation","organic acidemia","maple syrup urine","phenylketonuria","pku",
 "urea cycle","galactosemia","biotinidase","homocystinuria","tyrosinemia",
 "propionic acidemia","methylmalonic","isovaleric","adrenoleukodystrophy",
 "adrenomyeloneuropathy","ald","metachromatic leukodystrophy","mld","globoid",
 "lesch-nyhan","wilson disease","menkes","epidermolysis bullosa","progeria",
 "hutchinson","angelman","rett syndrome","cdkl5","dravet","tuberous sclerosis",
 "neurofibromatosis","cystinosis","nephropathic cystinosis","transthyretin",
 "ttr amyloidosis","methylation disorder","cobalamin","cblc","bile acid synthesis",
 "peroxisomal",
]
PED_MODERATE = [
 "orphan","rare disease","rare disorder","autoinflammatory","familial","hereditary",
 "genetic","muscular dystrophy","myopathy","mitochondrial","metabolic disorder",
 "enzyme deficiency","enzyme replacement","ataxia","neuropathy","leukodystrophy",
 "retinal dystrophy","leber","stargardt","haemophilia","hemophilia",
 "thrombotic thrombocytopenic","paroxysmal nocturnal hemoglobinuria","pnh",
 "primary biliary","alagille","cholestasis","systemic mastocytosis","myelofibrosis",
 "amyloidosis","epidermolysis","ichthyosis","pulmonary hypertension","pah",
 "cystic fibrosis","sickle cell",
]
HIGH_ATC = ["A16","N07","L04","B06","A11","A12","V03","S01"]
MED_ATC  = ["N06","A14","M09","D11","L01","G04","H04"]
# human-readable ATC level-2 labels for the codes that actually appear
ATC_LABELS = {
 "A16":"Other alimentary/metabolism","N07":"Other nervous-system","L04":"Immunosuppressant",
 "B06":"Other hematological","A11":"Vitamins","A12":"Mineral supplements","V03":"Other therapeutic",
 "S01":"Ophthalmological","N06":"Psychoanaleptic","A14":"Anabolic agent","M09":"Other musculoskeletal",
 "D11":"Other dermatological","L01":"Antineoplastic","G04":"Urological","H04":"Pancreatic hormone",
 "J02":"Antimycotic (systemic)","L02":"Endocrine therapy","N02":"Analgesic","C02":"Antihypertensive",
 "A10":"Diabetes","J05":"Antiviral","L03":"Immunostimulant",
}


def main():
    with open(SUMMARY, encoding="utf-8") as fh:
        data = json.load(fh)
    os.makedirs(OUT_DIR, exist_ok=True)
    payload = {
        "meta": data,
        "ped_strong": PED_STRONG, "ped_moderate": PED_MODERATE,
        "high_atc": HIGH_ATC, "med_atc": MED_ATC, "atc_labels": ATC_LABELS,
    }
    html = TEMPLATE.replace("__PAYLOAD__", json.dumps(payload))
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(html)
    print(f"wrote {OUT}  ({len(html)//1024} KB, {len(data['candidates'])} candidates)")


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Rare-disease voucher candidates</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap');
:root{
  --parchment:#F5F2EC; --parchment-raised:#FDFCF9; --ink:#0F1A20; --ink-secondary:#3B4D58;
  --ink-tertiary:#6E7E8A; --ink-ghost:#9DAAB4; --rule:rgba(15,26,32,.10); --rule-strong:rgba(15,26,32,.18);
  --signal:#0B6E75; --signal-dim:#D5EEF0; --signal-ink:#075056;
  --keep:#2B7A3D; --keep-bg:#EAF3EC; --investigate:#B06000; --investigate-bg:#FDF3E0;
  --reject:#A52828; --reject-bg:#FAECEC;
  --gold:#9a7a10; --gold-bg:#FBF1CE; --green:#2B7A3D; --green-bg:#EAF3EC; --blue:#255E8E; --blue-bg:#E6EFF7;
  --purple:#5b4a86; --purple-bg:#EEEAF6;
  --shadow-card:0 1px 2px rgba(15,26,32,.04),0 3px 8px rgba(15,26,32,.06);
  --sans:'IBM Plex Sans',-apple-system,system-ui,sans-serif; --mono:'IBM Plex Mono',ui-monospace,monospace;
}
*{box-sizing:border-box}
html,body{margin:0}
body{background:var(--parchment);color:var(--ink);font:15px/1.5 var(--sans);-webkit-font-smoothing:antialiased}
.mono{font-family:var(--mono)}
a{color:var(--signal-ink)}
.wrap{max-width:900px;margin:0 auto;padding:0 22px}
/* tooltips */
#tip{position:fixed;z-index:100;max-width:300px;background:var(--ink);color:#eaf4f5;
  font:12.5px/1.5 var(--sans);font-weight:400;padding:9px 12px;border-radius:8px;
  box-shadow:0 6px 22px rgba(15,26,32,.28);pointer-events:none;display:none;letter-spacing:.1px}
#tip b{color:#fff}
[data-tip]{cursor:help;border-bottom:1px dotted var(--ink-ghost)}
.scard [data-tip],button[data-tip],.pill[data-tip],.b[data-tip]{border-bottom:none}
/* header */
header.top{background:var(--ink);color:#EAF2F3;padding:16px 0;position:sticky;top:0;z-index:40}
header.top .wrap{display:flex;align-items:center;gap:14px}
header.top .brand{font-weight:600;font-size:19px;letter-spacing:.3px}
header.top .brand small{display:block;font-weight:400;font-size:12px;color:#8FB6BA;letter-spacing:.2px;margin-top:2px}
header.top .right{margin-left:auto;display:flex;align-items:center;gap:12px;font-family:var(--mono);font-size:11px;color:#8FB6BA}
header.top button.exp{background:transparent;border:1px solid #3a4f57;color:#cfe3e5;font-family:var(--mono);font-size:11px;padding:5px 11px;border-radius:5px;cursor:pointer}
header.top button.exp:hover{border-color:var(--signal);color:#fff}
/* intro */
.intro{background:var(--parchment-raised);border:1px solid var(--rule);border-radius:12px;padding:22px 24px;margin:24px 0 18px}
.intro h1{font-size:22px;font-weight:600;margin:0 0 12px;letter-spacing:-.2px}
.intro p{font-size:15px;line-height:1.65;color:var(--ink-secondary);margin:0 0 12px;max-width:720px}
.intro p:last-child{margin-bottom:0}
.intro b{color:var(--ink)}
.intro .money{color:var(--signal-ink);font-weight:600}
.intro .deadline{background:var(--investigate-bg);border:1px solid #e8c88c;border-radius:8px;padding:11px 14px;color:#6d4400;font-size:14px}
.steps{display:flex;flex-wrap:wrap;gap:10px;margin:14px 0 0}
.step{flex:1;min-width:180px;background:var(--parchment);border:1px solid var(--rule);border-radius:8px;padding:12px 14px}
.step .k{font-family:var(--mono);font-size:11px;color:var(--signal-ink);font-weight:600}
.step .t{font-size:13px;color:var(--ink-secondary);margin-top:4px;line-height:1.45}
/* controls */
.controls{display:flex;flex-wrap:wrap;gap:9px;align-items:center;margin:22px 0 8px}
.search{flex:1;min-width:220px;padding:11px 14px;border:1px solid var(--rule-strong);border-radius:8px;font-family:var(--sans);font-size:14px;background:var(--parchment-raised)}
.search:focus{outline:2px solid var(--signal);border-color:var(--signal)}
select.sort{padding:11px 12px;border:1px solid var(--rule-strong);border-radius:8px;font-size:13px;background:var(--parchment-raised);color:var(--ink)}
.chips{display:flex;flex-wrap:wrap;gap:7px;margin:2px 0 4px}
.chip{border:1px solid var(--rule-strong);background:var(--parchment-raised);border-radius:16px;padding:6px 13px;font-size:12.5px;cursor:pointer;color:var(--ink-secondary);user-select:none}
.chip.on{background:var(--signal-ink);color:#fff;border-color:var(--signal-ink)}
.count{font-family:var(--mono);font-size:12px;color:var(--ink-tertiary);margin:6px 0 0}
/* legend */
.legend{display:flex;flex-wrap:wrap;gap:16px;margin:12px 0 4px;font-size:12.5px;color:var(--ink-tertiary)}
.legend span{display:inline-flex;align-items:center;gap:6px}
.pill{font-family:var(--mono);font-size:11px;font-weight:600;padding:2px 9px;border-radius:20px;white-space:nowrap}
.pill.open{background:var(--keep-bg);color:var(--keep)} .pill.soon{background:var(--investigate-bg);color:var(--investigate)}
.pill.prot{background:var(--reject-bg);color:var(--reject)} .pill.unk{background:#eef1f0;color:var(--ink-tertiary)}
.dot{width:9px;height:9px;border-radius:50%;display:inline-block}
.dot.open{background:var(--keep)} .dot.soon{background:var(--investigate)} .dot.prot{background:var(--reject)} .dot.unk{background:var(--ink-ghost)}
/* group heading */
.grouphd{margin:26px 0 10px}
.grouphd h2{font-size:16px;font-weight:600;margin:0;display:flex;align-items:baseline;gap:9px}
.grouphd h2 .n{font-family:var(--mono);font-size:13px;color:var(--ink-tertiary);font-weight:400}
.grouphd p{font-size:13px;color:var(--ink-tertiary);margin:3px 0 0}
/* cards */
.scard{background:var(--parchment-raised);border:1px solid var(--rule);border-left:4px solid var(--ink-ghost);border-radius:10px;padding:15px 18px;margin-bottom:10px;cursor:pointer;transition:background .12s}
.scard:hover{background:#fff;box-shadow:var(--shadow-card)}
.scard.open{border-left-color:var(--keep)} .scard.soon{border-left-color:var(--investigate)}
.scard.prot{border-left-color:var(--reject)} .scard.unk{border-left-color:var(--ink-ghost)}
.scard.tri-keep{border-left-color:var(--keep);border-left-width:5px} .scard.tri-reject{opacity:.5}
.sc-top{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.sc-name{font-size:17px;font-weight:600;letter-spacing:.2px}
.b{font-family:var(--mono);font-size:10px;font-weight:600;padding:2px 7px;border-radius:4px;letter-spacing:.3px}
.b.orphan{background:var(--gold-bg);color:var(--gold)} .b.caveat{background:var(--investigate-bg);color:var(--investigate)}
.sc-desc{font-size:14px;line-height:1.55;color:var(--ink-secondary);margin:8px 0 11px}
.sc-checks{display:flex;flex-wrap:wrap;gap:7px 16px;font-size:13px}
.chk-y{color:var(--keep)} .chk-w{color:var(--investigate)} .chk-i{color:var(--ink-tertiary)}
.empty{padding:40px;text-align:center;color:var(--ink-tertiary)}
/* advanced */
details.adv{margin:34px 0 10px;background:var(--parchment-raised);border:1px solid var(--rule);border-radius:12px;padding:2px 22px}
details.adv>summary{cursor:pointer;font-weight:600;font-size:15px;padding:16px 0;list-style:none}
details.adv>summary::-webkit-details-marker{display:none}
details.adv>summary::before{content:'▸ ';color:var(--ink-tertiary)}
details.adv[open]>summary::before{content:'▾ '}
details.adv .advnote{font-size:13px;color:var(--ink-tertiary);margin:-4px 0 14px}
.cards{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:6px 0 18px}
.card{background:var(--parchment);border:1px solid var(--rule);border-radius:8px;padding:14px 15px}
.card .n{font-family:var(--mono);font-size:24px;font-weight:600;line-height:1;color:var(--ink)}
.card .l{font-size:12px;color:var(--ink-secondary);margin-top:7px;font-weight:500}
.card .s{font-size:11px;color:var(--ink-tertiary);margin-top:3px}
.advsub{font-family:var(--mono);font-size:11px;text-transform:uppercase;letter-spacing:.7px;color:var(--ink-tertiary);margin:20px 0 8px;border-top:1px solid var(--rule);padding-top:16px}
.frow{display:flex;align-items:center;gap:12px;margin:6px 0}
.frow .bar{height:22px;border-radius:3px;background:var(--signal);display:flex;align-items:center;padding:0 9px;color:#fff;font-family:var(--mono);font-size:11px;min-width:38px}
.frow.dim .bar{background:var(--rule-strong)}
.frow .lab{font-size:12.5px;color:var(--ink-secondary)}
.mon-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px;padding:4px 0 8px}
.mon-grid h4{font-family:var(--mono);font-size:11px;text-transform:uppercase;letter-spacing:.5px;color:var(--ink-tertiary);margin:0 0 8px}
.mon-num{font-family:var(--mono);font-size:24px;font-weight:600;color:var(--signal-ink)}
.mon-list{font-size:12px;line-height:1.6;margin-top:6px}
.mon-list .mi{display:flex;gap:8px;border-bottom:1px solid var(--rule);padding:3px 0}
.mon-list .mi .d{font-family:var(--mono);color:var(--ink-tertiary);white-space:nowrap}
@media(max-width:720px){.mon-grid,.cards{grid-template-columns:1fr 1fr}}
/* drawer */
.overlay{position:fixed;inset:0;background:rgba(15,26,32,.32);opacity:0;pointer-events:none;transition:opacity .18s;z-index:50}
.overlay.open{opacity:1;pointer-events:auto}
.drawer{position:fixed;top:0;right:0;bottom:0;width:min(560px,94vw);background:var(--parchment-raised);
  box-shadow:-6px 0 30px rgba(15,26,32,.18);transform:translateX(100%);transition:transform .2s;z-index:51;overflow-y:auto}
.drawer.open{transform:translateX(0)}
.dhead{position:sticky;top:0;background:var(--parchment-raised);border-bottom:1px solid var(--rule-strong);padding:16px 22px;display:flex;align-items:center;gap:12px}
.dhead h2{margin:0;font-size:19px;font-weight:600;flex:1}
.dhead .x{background:none;border:none;font-size:20px;cursor:pointer;color:var(--ink-tertiary)}
.seg-ctl{display:flex;border:1px solid var(--rule-strong);border-radius:6px;overflow:hidden}
.seg-ctl button{background:var(--parchment-raised);border:none;border-right:1px solid var(--rule);padding:6px 10px;font-family:var(--mono);font-size:10.5px;cursor:pointer;color:var(--ink-secondary)}
.seg-ctl button:last-child{border-right:none}
.seg-ctl button.on-keep{background:var(--keep);color:#fff} .seg-ctl button.on-investigate{background:var(--investigate);color:#fff} .seg-ctl button.on-reject{background:var(--reject);color:#fff}
.dbody{padding:18px 22px 60px}
.dsec{margin:18px 0}
.dsec .lbl{font-family:var(--mono);font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.7px;color:var(--ink-tertiary);margin-bottom:6px}
.dsec .val{font-size:14px;color:var(--ink);line-height:1.5}
.dsec .prose{font-size:13.5px;line-height:1.6;color:var(--ink-secondary);font-style:italic;border-left:2px solid var(--rule-strong);padding-left:12px;margin-top:6px}
.checkline{display:flex;gap:9px;align-items:flex-start;font-size:13.5px;margin:8px 0;line-height:1.45}
.checkline .ic{flex-shrink:0}
.caveat{background:var(--investigate-bg);border:1px solid #e8c88c;border-radius:6px;padding:10px 12px;font-size:12.5px;color:#7a4d00;margin-top:8px}
.chk{display:flex;align-items:center;gap:8px;font-size:13px;margin:6px 0;color:var(--ink-secondary)}
textarea.note{width:100%;min-height:70px;border:1px solid var(--rule-strong);border-radius:6px;padding:9px;font-family:var(--sans);font-size:13px;resize:vertical;background:var(--parchment)}
.links a{font-family:var(--mono);font-size:12px;margin-right:14px;display:inline-block;margin-top:4px}
details.adv2{margin-top:8px}
details.adv2 summary{cursor:pointer;font-family:var(--mono);font-size:11px;color:var(--ink-tertiary)}
.scorebox{background:var(--parchment);border:1px solid var(--rule-strong);border-radius:8px;padding:14px;margin-top:8px}
.scorebox .big{font-family:var(--mono);font-size:30px;font-weight:600;line-height:1}
.scorebox .note{font-size:12px;color:var(--ink-tertiary);margin-top:8px;line-height:1.5}
.brk table{width:100%;border-collapse:collapse;font-family:var(--mono);font-size:11.5px;margin-top:8px}
.brk td{padding:3px 6px;border-bottom:1px solid var(--rule)}
.brk td:last-child{text-align:right}
footer{color:var(--ink-tertiary);font-size:12px;text-align:center;margin:40px 0 30px;font-family:var(--mono)}
@media print{.controls,.chips,.drawer,.overlay,header.top .right{display:none!important}.scard{break-inside:avoid}body{background:#fff}}
</style>
</head>
<body>
<header class="top"><div class="wrap">
  <span class="brand">Rare-disease voucher candidates<small>Drugs approved abroad · never approved in the US</small></span>
  <span class="right"><button class="exp" id="export">Export notes</button><label class="exp" style="cursor:pointer">Import<input id="import" type="file" accept="application/json" hidden></label><span id="gen"></span></span>
</div></header>

<div class="wrap">
  <!-- PLAIN-ENGLISH INTRO -->
  <div class="intro">
    <h1>What am I looking at?</h1>
    <p>These are medicines with a <b>real marketing authorisation from Europe, Canada or Switzerland</b> that have <b>never been approved in the United States</b>. That gap is the opportunity: if you get one of them approved in the US to treat a <b>rare childhood disease</b>, the FDA awards a <b class="money">Priority Review Voucher</b> — a freely transferable prize. The three SEC-verified 2026 sales went for <b class="money">$180M, $195M and $205M</b> (record $350M in 2015).</p>
    <p>Think of this as a <b>starting shortlist</b>, not a list of ready businesses. Every drug here clears the first gate (novel to the US), but each still needs a few human checks before it's real — shown on every card and explained when you click one.</p>
    <div class="steps">
      <div class="step"><div class="k">THE GAP</div><div class="t">Approved abroad, never in the US → clears the first eligibility gate.</div></div>
      <div class="step"><div class="k">THE FIT</div><div class="t">Must be developable for a <b>rare pediatric disease</b> to qualify for the voucher.</div></div>
      <div class="step"><div class="k">THE FILING</div><div class="t">Must be filed as a <b>full 505(b)(1) NDA</b> — since 2021 a 505(b)(2) forfeits the voucher.</div></div>
      <div class="step"><div class="k">THE CHECKS</div><div class="t">Confirm US patents / rights are clear and the active ingredient is sourceable.</div></div>
      <div class="step"><div class="k">THE PRIZE</div><div class="t">Get it approved → a voucher you can sell to any drugmaker.</div></div>
    </div>
    <p style="font-size:13px;color:var(--ink-secondary);margin-top:12px;border-left:2px solid var(--rule-strong);padding-left:12px">
      <b>What this list deliberately excludes.</b> Drugs whose only overseas record is a
      <i>refused</i> or <i>withdrawn application</i> are <b>not</b> counted here — they were never
      approved abroad, so the headline claim would be false. They are kept separately as
      "dossier-only" leads in <code>funnelA_dossier_only.csv</code>, because a dossier and human
      data still exist. Before 2026-08-29 they were mixed into this list and inflated it by
      roughly half.
    </p>
    <p class="deadline" style="margin-top:14px">⏳ <b>The program ends 30 September 2029.</b> The voucher is awarded on <i>approval</i>, so a drug must be approved by that date — a realistic program needs to start soon. (The program briefly lapsed in Dec 2024 and was reauthorized in Feb 2026; new designations are open again.) <span id="sunset-remain"></span></p>
  </div>

  <!-- SEARCH + FILTER -->
  <div class="controls">
    <input class="search" id="search" placeholder="Search a drug, disease, or therapy area…">
    <select class="sort" id="sort">
      <option value="best">Sort: Most promising first</option>
      <option value="name">Name (A–Z)</option>
      <option value="oldest">Oldest approval first (likely off-patent)</option>
      <option value="research">Most research activity</option>
    </select>
  </div>
  <div class="chips" id="chips"></div>
  <div class="legend" id="legend"></div>
  <div class="count" id="count"></div>

  <div id="list"></div>

  <!-- ADVANCED (analyst machinery, collapsed) -->
  <details class="adv" id="adv">
    <summary>Advanced — the numbers, the funnel, and who else is filing</summary>
    <div class="advnote">Everything below is the analyst layer behind the shortlist above. You don't need it to use the list.</div>

    <div class="cards" id="cards"></div>

    <div class="advsub">How the raw pile narrows to the shortlist</div>
    <div id="funnel"></div>

    <div class="advsub">Who else is in the game — live competitor monitor</div>
    <div id="monitor"></div>

    <div class="advsub">How to read the "most promising" ranking, honestly</div>
    <p style="font-size:13px;color:var(--ink-secondary);max-width:720px;margin:0 0 8px">
      The ranking scores how likely a drug is to <b>survive a week of diligence</b> — <b>not</b> its
      chance of FDA approval. It rewards rare/pediatric relevance, a foreign rare-disease flag,
      approval by multiple regulators, and match confidence. It can't see freedom-to-operate,
      existing US orphan exclusivity, ingredient sourcing, or trial feasibility — so a high rank
      means "worth a closer look," never "a sure thing."
    </p>
    <p style="font-size:13px;color:var(--ink-secondary);max-width:720px;margin:0 0 8px">
      Two known gaps in the ranking, stated plainly. <b>Orphan flags are EMA-only</b>, so a
      Canadian or Swiss drug can never earn that badge and is scored down for a reason that has
      nothing to do with the drug. <b>"Approved by more than one regulator" is currently always
      zero</b> — not because no drug qualifies, but because EMA here is centralised-only while
      Canada and Switzerland list mostly nationally-approved drugs, so the sets barely overlap.
      Both dimensions therefore deflate every candidate roughly equally.
    </p>
  </details>

  <footer id="footer"></footer>
</div>

<div class="overlay" id="overlay"></div>
<aside class="drawer" id="drawer" role="dialog" aria-modal="true" aria-label="Candidate detail"></aside>

<script>
const P = __PAYLOAD__;
const DATA = P.meta, CANDS = DATA.candidates;
const LS = 'rdh_triage_v2';
let triage = JSON.parse(localStorage.getItem(LS) || '{}');
function saveTriage(){ localStorage.setItem(LS, JSON.stringify(triage)); }
function tstate(u){ return (triage[u]||{}).state || null; }

const el=(t,c,x)=>{const e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e;};
const titleCase=s=>s.toLowerCase().replace(/\b([a-z])/g,(m,c)=>c.toUpperCase());

/* ---------- hover tooltips (plain-English) ---------- */
const TIPS={
 orphan:"Carries an EU orphan-medicine flag AND holds a real EU marketing authorisation. Only EMA supplies this flag — Canada, Switzerland and Japan are not screened for orphan status, so absence of the badge means 'not checked', not 'not rare'. A strong rare-disease signal, but it does NOT by itself prove US voucher eligibility.",
 caveat:"Heads up — this drug was matched through a salt or prodrug form. Open the card to see the exact flag to double-check.",
 fstatus_authorised:"Currently holds a marketing authorisation from this regulator.",
 fstatus_previously:"Was authorised by this regulator and the licence has since been withdrawn, lapsed, expired or been revoked. Still a genuine prior approval — but find out WHY it was pulled before going further.",
 off_open:"Approved abroad 20+ years ago, so the original patents have almost certainly expired. A signal, not a legal clearance — still verify.",
 off_soon:"Approved abroad 12–20 years ago — core patents may have expired. Verify the exact dates.",
 off_prot:"Approved abroad recently — very likely still under patent protection.",
 off_unk:"No overseas approval date on record, so patent age can't be estimated here.",
 research:"Left: research papers mentioning this drug in a rare/pediatric context. Right: registered clinical trials. A rough read on how much is already known and whether others are working on it.",
 novel:"No US human-drug (NDA/BLA) approval on record for this active moiety, so it clears the program's first gate — 'novel' to the US. Veterinary approvals and OTC-monograph marketing do NOT disqualify: the statute bars only a prior approval in a 505(b)(1)/(b)(2)/(j) application. Measured residual gap: of 30 hand-checked drugs approved by FDA and later withdrawn, 13 are missing from the bulk files — every one withdrawn before ~2000. None currently appears in any foreign register loaded here, but verify pre-2000-era candidates by hand.",
 fedreg:"Live count of Priority Review Voucher documents in the Federal Register — the program's official public ledger.",
 edgar:"Live count of recent SEC filings mentioning 'rare pediatric disease designation'. The FDA publishes no list of who holds these, so SEC filings are the main way to spot competitors.",
};
function tp(node,key){ if(node) node.setAttribute('data-tip', TIPS[key]||key); return node; }
const TIP=el('div'); TIP.id='tip'; document.body.appendChild(TIP);
let tipCur=null;
function placeTip(t){
  const txt=t.getAttribute('data-tip'); if(!txt) return;
  TIP.innerHTML=txt.replace(/\b(NOT|does not|only|verify|must|never)\b/g,'<b>$&</b>'); TIP.style.display='block';
  const r=t.getBoundingClientRect(), tr=TIP.getBoundingClientRect();
  let top=r.top-tr.height-9; if(top<8) top=r.bottom+9;
  let left=r.left+r.width/2-tr.width/2;
  left=Math.max(8,Math.min(left, window.innerWidth-tr.width-8));
  TIP.style.top=top+'px'; TIP.style.left=left+'px';
}
document.addEventListener('mouseover',e=>{const t=e.target.closest('[data-tip]'); if(t){tipCur=t;placeTip(t);}});
document.addEventListener('mouseout',e=>{if(tipCur&&(!e.relatedTarget||!tipCur.contains(e.relatedTarget))){TIP.style.display='none';tipCur=null;}});
document.addEventListener('click',()=>{TIP.style.display='none';},true);

/* ---------- scoring (drives "most promising" sort; surfaced only in detail) ---------- */
function pedScore(c){
  const text=((c.indication||'')+' '+(c.area||'')).toLowerCase();
  if(!text.trim()) return {v:0.2, floored:true};
  if(P.ped_strong.some(k=>text.includes(k))) return {v:1.0, floored:false};
  if(P.ped_moderate.some(k=>text.includes(k))) return {v:0.5, floored:false};
  return {v:0.0, floored:false};
}
function atcSub(c){ if(!c.atc) return 0.3; const k=c.atc.slice(0,3).toUpperCase();
  if(P.high_atc.includes(k)) return 1.0; if(P.med_atc.includes(k)) return 0.5; return 0.1; }
function recencySub(c){ if(!c.approved) return 0.3; const m=(c.approved.match(/(\d{4})/)||[])[1]; const y=m?+m:0;
  if(y>=2015) return 1.0; if(y>=2005) return 0.7; if(y>=1995) return 0.4; return 0.1; }
const TIERMAP={'exact-moiety':1.0,'exact':1.0,'moiety-base':0.7,'salt-stripped':0.7,'moiety':0.7,'direct':0.5,'name-match':0.4,'fuzzy':0.1};
function regSub(c){const n=c.sources.length; return n>=3?1.0:n===2?0.6:n===1?0.2:0.0;}
function score(c){
  const ped=pedScore(c), orph=c.orphan?1:0, reg=regSub(c),
        match=(TIERMAP[c.tier]??0.3), atc=atcSub(c), rec=recencySub(c);
  const total=Math.round(35*ped.v+25*orph+15*reg+15*match+5*atc+5*rec);
  return {total, floored:ped.floored, parts:[
    ['Rare / pediatric relevance',35,ped.v, ped.floored?'no indication text on record':''],
    ['Rare-disease flag abroad',25,orph,''],
    ['Approved by multiple regulators',15,reg, c.sources.length+' regulator(s)'],
    ['Match confidence',15,match, c.tier],
    ['Drug-class fit',5,atc, c.atc||'—'],
    ['Approval recency',5,rec, c.approved||'—'],
  ]};
}
CANDS.forEach(c=>{ const s=score(c); c._s=s.total; c._floored=s.floored; c._parts=s.parts; });

/* ---------- off-patent-by-age proxy ---------- */
const NOW_Y=2026;
function approvedYear(c){ const m=(c.approved||'').match(/(\d{4})/); return m?+m[1]:null; }
function availability(c){
  const y=approvedYear(c);
  if(y===null) return {k:'unk', pill:'Patent status unknown', tipk:'off_unk',
    say:'No overseas approval date on record — patent status can\'t be estimated here.'};
  const age=NOW_Y-y;
  if(age>=20) return {k:'open', pill:'Likely off-patent', tipk:'off_open',
    say:`Approved abroad in ${y} (~${age} ${age===1?'year':'years'} ago) — original patents have almost certainly expired.`};
  if(age>=12) return {k:'soon', pill:'Maybe off-patent', tipk:'off_soon',
    say:`Approved abroad in ${y} (~${age} ${age===1?'year':'years'} ago) — core patents may have expired; verify the exact dates.`};
  return {k:'prot', pill:'Likely still patented', tipk:'off_prot',
    say:`Approved abroad in ${y} (only ~${age} ${age===1?'year':'years'} ago) — likely still under patent protection.`};
}
CANDS.forEach(c=>{ c._avail=availability(c); });
function evText(c){ const pm=(c.pubmed==null?'—':c.pubmed), ct=(c.trials==null?'—':c.trials);
  return `${pm} papers · ${ct} trials`; }
function whereApproved(c){
  return c.sources.includes('EMA')?'Europe':c.sources.includes('Health Canada')?'Canada'
    :c.sources.includes('Swissmedic')?'Switzerland':c.sources.includes('PMDA-JP')?'Japan':'overseas';
}
function plainDesc(c){
  const area=(c.area||'').split(';')[0];
  let s='Approved in '+whereApproved(c)+(approvedYear(c)?(' in '+approvedYear(c)):'');
  if(area) s+=' to treat '+area.toLowerCase().replace(/;/g,', ');
  else if(c.indication) s+=' — '+c.indication.replace(/\.$/,'');
  s+='. Never approved in the US.';
  return s;
}
function caveats(c){
  const out=[]; (c.flags||[]).forEach(f=>out.push(f));
  if(['moiety-base','salt-stripped','moiety'].includes(c.tier)) out.push('Matched on the base/salt form only — double-check the active ingredient against the FDA Orange Book.');
  if(!(c.flags&&c.flags.length) && /onium|sulfate ester|prodrug/i.test(c.name)) out.push('Might be a prodrug — the active form could already be US-approved under a different parent name.');
  return out;
}

/* ---------- header bits ---------- */
document.getElementById('gen').textContent='data as of '+DATA.generated;
(function(){ // months to sunset
  const g=(DATA.generated||'').match(/(\d{4})-(\d{2})/);
  if(g){ const months=(2029-+g[1])*12+(9-+g[2]); if(months>0)
    document.getElementById('sunset-remain').textContent='About '+months+' months left.'; }
})();
document.getElementById('footer').textContent='Generated by pipeline/build_ui.py · your keep/investigate notes stay in this browser · data embedded, works offline';

/* ---------- filters ---------- */
const FILTERS=[
  ['rare','Rare-disease flagged', c=>c.orphan],
  ['offpatent','Likely off-patent', c=>c._avail.k==='open'||c._avail.k==='soon'],
  ['research','Has clinical trials', c=>(c.trials||0)>0],
  ['eu','Europe', c=>c.sources.includes('EMA')],
  ['ca','Canada', c=>c.sources.includes('Health Canada')],
  ['ch','Switzerland', c=>c.sources.includes('Swissmedic')],
];
let active=new Set(), query='', sortBy='best';
(function(){ const w=document.getElementById('chips');
  FILTERS.forEach(([k,label])=>{ const c=el('span','chip',label);
    c.onclick=()=>{active.has(k)?active.delete(k):active.add(k);c.classList.toggle('on');render();}; w.appendChild(c);});
})();
(function(){ const lg=document.getElementById('legend');
  [['open','Likely off-patent'],['soon','Maybe off-patent'],['prot','Likely still patented'],['unk','Date unknown']]
   .forEach(([k,t])=>{const s=el('span'); s.appendChild(el('span','dot '+k)); s.appendChild(el('span',null,t)); lg.appendChild(s);});
  const o=el('span'); o.appendChild(tp(el('span','b orphan','ORPHAN'),'orphan')); o.appendChild(el('span',null,'rare-disease flagged abroad')); lg.appendChild(o);
})();
document.getElementById('sort').onchange=e=>{sortBy=e.target.value;render();};
let searchTO; document.getElementById('search').oninput=e=>{clearTimeout(searchTO);
  searchTO=setTimeout(()=>{query=e.target.value.trim().toLowerCase();render();},180);};

function passes(c){
  for(const [k,,fn] of FILTERS){ if(active.has(k)&&!fn(c)) return false; }
  if(query){ const h=(c.name+' '+(c.indication||'')+' '+(c.area||'')).toLowerCase(); if(!h.includes(query)) return false; }
  return true;
}
const SORTS={
  best:(a,b)=>b._s-a._s || a.name.localeCompare(b.name),
  name:(a,b)=>a.name.localeCompare(b.name),
  oldest:(a,b)=>((a.approved||'9999').slice(0,4)).localeCompare((b.approved||'9999').slice(0,4))||b._s-a._s,
  research:(a,b)=>(b.trials||0)-(a.trials||0)||(b.pubmed||0)-(a.pubmed||0),
};

/* ---------- cards ---------- */
function cardNode(c){
  const a=c._avail, st=tstate(c.unii);
  const card=el('div','scard '+a.k+(st?' tri-'+st:''));
  const top=el('div','sc-top');
  top.appendChild(el('span','sc-name',titleCase(c.name)));
  top.appendChild(tp(el('span','pill '+a.k,a.pill),a.tipk));
  if(c.orphan) top.appendChild(tp(el('span','b orphan','ORPHAN'),'orphan'));
  if(c.foreign_status==='previously_authorised')
    top.appendChild(tp(el('span','b caveat','LICENCE PULLED'),'fstatus_previously'));
  if(caveats(c).length) top.appendChild(tp(el('span','b caveat','⚑ check'),'caveat'));
  card.appendChild(top);
  card.appendChild(el('div','sc-desc',plainDesc(c)+' '+a.say));
  const ch=el('div','sc-checks');
  ch.appendChild(tp(el('span','chk-y','✓ Never US-approved — clears the first gate'),'novel'));
  ch.appendChild(tp(el('span','chk-i','📄 '+evText(c)),'research'));
  ch.appendChild(el('span','chk-w','⚠ Still to verify: rare-pediatric fit · US patents · ingredient supply'));
  card.appendChild(ch);
  card.onclick=()=>openDrawer(c);
  return card;
}
function groupHead(title,n,sub){
  const w=el('div','grouphd'); const h=el('h2'); h.appendChild(document.createTextNode(title));
  h.appendChild(el('span','n','('+n+')')); w.appendChild(h);
  if(sub) w.appendChild(el('p',null,sub)); return w;
}
function render(){
  const listEl=document.getElementById('list'); listEl.innerHTML='';
  let rows=CANDS.filter(passes);
  rows.sort(SORTS[sortBy]||SORTS.best);
  const grouped = !query && active.size===0 && sortBy==='best';
  if(!rows.length){ listEl.appendChild(el('div','empty','No drugs match — try clearing a filter or the search box.')); }
  else if(grouped){
    const orphan=rows.filter(c=>c.orphan), other=rows.filter(c=>!c.orphan);
    if(orphan.length){
      listEl.appendChild(groupHead('Flagged for a rare disease abroad', orphan.length,
        'The sharpest starting point — already recognised as rare-disease drugs by a foreign regulator.'));
      orphan.forEach(c=>listEl.appendChild(cardNode(c)));
    }
    if(other.length){
      listEl.appendChild(groupHead('Other never-in-US drugs', other.length,
        'A broader pool — worth scanning for a rare-disease use even without a formal flag.'));
      other.forEach(c=>listEl.appendChild(cardNode(c)));
    }
  } else {
    rows.forEach(c=>listEl.appendChild(cardNode(c)));
  }
  document.getElementById('count').textContent =
    (query||active.size) ? ('Showing '+rows.length+' of '+CANDS.length+' drugs' + (active.size?' (filtered)':''))
                         : (CANDS.length+' drugs approved abroad, never in the US');
}

/* ---------- detail drawer ---------- */
const overlay=document.getElementById('overlay'), drawer=document.getElementById('drawer');
let lastFocus=null;
function checkline(ic,cls,text){ const w=el('div','checkline'); w.appendChild(el('span','ic '+cls,ic)); w.appendChild(el('span',null,text)); return w; }
function openDrawer(c){
  lastFocus=document.activeElement;
  const cav=caveats(c), a=c._avail, rec=(triage[c.unii]||{});
  const atcLab=c.atc?(P.atc_labels[c.atc.slice(0,3).toUpperCase()]||''):'';
  const links=[['EMA','https://www.ema.europa.eu/en/search?search_api_fulltext='+encodeURIComponent(c.name)],
    ['PubMed','https://pubmed.ncbi.nlm.nih.gov/?term='+encodeURIComponent(c.name)],
    ['DrugBank','https://go.drugbank.com/unearth/q?query='+encodeURIComponent(c.name)+'&searcher=drugs'],
    ['FDA record','https://gsrs.ncats.nih.gov/ginas/app/beta/substances/'+c.unii]];
  drawer.innerHTML='';
  const head=el('div','dhead');
  head.appendChild(el('h2',null,titleCase(c.name)));
  const seg=el('div','seg-ctl');
  [['keep','KEEP'],['investigate','MAYBE'],['reject','SKIP']].forEach(([k,l])=>{
    const b=el('button',(tstate(c.unii)===k?'on-'+k:''),l);
    b.onclick=()=>{setTriage(c.unii, tstate(c.unii)===k?null:k); openDrawer(c); render();};
    seg.appendChild(b);
  });
  head.appendChild(seg);
  const x=el('button','x','✕'); x.onclick=closeDrawer; head.appendChild(x);
  drawer.appendChild(head);

  const body=el('div','dbody');

  // the one-line story
  const st=el('div','dsec'); st.appendChild(el('div','lbl','In plain terms'));
  st.appendChild(el('div','val',plainDesc(c)));
  if(c.indication) st.appendChild(Object.assign(el('div','prose'),{textContent:c.indication}));
  body.appendChild(st);

  // where it stands
  const gate=el('div','dsec'); gate.appendChild(el('div','lbl','Where it stands'));
  gate.appendChild(checkline('✅','chk-y','Never approved in the US — clears the program’s first gate.'));
  if(c.orphan) gate.appendChild(checkline('✅','chk-y','Already flagged as a rare-disease (orphan) drug abroad.'));
  gate.appendChild(checkline(a.k==='open'?'🟢':a.k==='soon'?'🟡':a.k==='prot'?'🔴':'⚪',
     a.k==='open'||a.k==='soon'?'chk-y':'chk-i', a.pill+'. '+a.say));
  body.appendChild(gate);

  // still to check
  const todo=el('div','dsec'); todo.appendChild(el('div','lbl','Still to check before it’s real'));
  todo.appendChild(checkline('⚠️','chk-w','Is it developable for a rare pediatric disease? (the voucher requires this)'));
  todo.appendChild(checkline('⚠️','chk-w','Are US patents / rights clear? (freedom-to-operate)'));
  todo.appendChild(checkline('⚠️','chk-w','Can the active ingredient be sourced at quality?'));
  todo.appendChild(checkline('⚠️','chk-w','Any existing US orphan designation/exclusivity? (searchable in FDA’s public orphan database)'));
  body.appendChild(todo);

  // evidence
  const ev=el('div','dsec'); ev.appendChild(el('div','lbl','How much is already known'));
  ev.appendChild(el('div','val','Research papers (rare/pediatric context): '+(c.pubmed==null?'—':c.pubmed)
    +'  ·  Registered clinical trials: '+(c.trials==null?'—':c.trials)));
  body.appendChild(ev);

  // facts
  const facts=el('div','dsec'); facts.appendChild(el('div','lbl','The basics'));
  const sbs=c.status_by_source||{};
  const statusTxt=Object.keys(sbs).length
    ? Object.keys(sbs).sort().map(k=>k+': '+String(sbs[k]).replace(/_/g,' ')).join('  ·  ')
    : String(c.foreign_status||'—').replace(/_/g,' ');
  const rows2=[['Approved by', c.sources.join(', ')||'—'],
    ['Regulatory standing', statusTxt],
    ['Authorisation date', c.approved||'—'],
    ['Therapy area', (c.area||'').replace(/;/g,' · ')||'—'],
    ['Drug class (ATC)', c.atc?(c.atc+(atcLab?'  ·  '+atcLab:'')):'—']];
  rows2.forEach(([k,v])=>{ const d=el('div','val'); d.style.margin='3px 0';
    d.innerHTML='<span style="color:var(--ink-tertiary)">'+k+':</span> '+v; facts.appendChild(d); });
  body.appendChild(facts);

  // caveats
  if(cav.length){ const w=el('div','dsec'); w.appendChild(el('div','lbl','Data caveats to double-check'));
    cav.forEach(t2=>w.appendChild(Object.assign(el('div','caveat'),{textContent:t2}))); body.appendChild(w); }

  // look it up
  const lk=el('div','dsec'); lk.appendChild(el('div','lbl','Look it up'));
  const la=el('div','links'); links.forEach(([t2,u])=>{const A=el('a',null,t2);A.href=u;A.target='_blank';A.rel='noopener';la.appendChild(A);});
  lk.appendChild(la); body.appendChild(lk);

  // your note
  const nt=el('div','dsec'); nt.appendChild(el('div','lbl','Your note'));
  const ta=el('textarea','note'); ta.value=rec.note||''; ta.placeholder='Working notes for this drug…';
  let nto; ta.oninput=()=>{clearTimeout(nto);nto=setTimeout(()=>{if(!triage[c.unii])triage[c.unii]={};triage[c.unii].note=ta.value;saveTriage();},400);};
  nt.appendChild(ta); body.appendChild(nt);

  // analyst detail (collapsed inside the drawer)
  const adv=el('details','adv2'); adv.appendChild(el('summary',null,'Analyst detail (promise score & match)'));
  const box=el('div','scorebox');
  box.appendChild(el('div','big', c._s));
  box.appendChild(el('div','note','Promise score (0–100): how likely this survives a week of diligence — not a probability of FDA approval.'
    +(c._floored?' Partial: no indication text for this row, so the rare/pediatric component is floored.':'')));
  const brk=el('div','brk'); const tbl=el('table');
  c._parts.forEach(([n,w,v,note])=>{const tr=el('tr');
    tr.appendChild(el('td',null,n)); tr.appendChild(el('td',null,note||''));
    tr.appendChild(el('td',null,Math.round(w*v)+' / '+w)); tbl.appendChild(tr);});
  brk.appendChild(tbl); box.appendChild(brk);
  const prov=el('div','note'); prov.style.marginTop='8px';
  prov.textContent='Match: '+c.tier+' · FDA ingredient ID (UNII) '+c.unii;
  box.appendChild(prov);
  adv.appendChild(box); body.appendChild(adv);

  drawer.appendChild(body);
  overlay.classList.add('open'); drawer.classList.add('open');
  drawer.querySelector('.x').focus();
}
function setTriage(u,state){
  if(!triage[u])triage[u]={};
  if(state===null){ delete triage[u].state; if(!triage[u].note) delete triage[u]; }
  else { triage[u].state=state; triage[u].ts=Date.now(); }
  saveTriage();
}
function closeDrawer(){overlay.classList.remove('open');drawer.classList.remove('open');if(lastFocus)lastFocus.focus();}
overlay.onclick=closeDrawer;
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&drawer.classList.contains('open'))closeDrawer();});

/* export / import */
document.getElementById('export').onclick=()=>{
  const blob=new Blob([JSON.stringify(triage,null,1)],{type:'application/json'});
  const a=el('a');a.href=URL.createObjectURL(blob);a.download='rdh_notes_'+DATA.generated+'.json';a.click();
};
document.getElementById('import').onchange=e=>{const f=e.target.files[0];if(!f)return;const r=new FileReader();
  r.onload=()=>{try{triage=JSON.parse(r.result);saveTriage();render();}catch(err){alert('Invalid notes file');}};r.readAsText(f);};

/* ---------- advanced: stat cards, funnel, monitor ---------- */
(function(){
  const C=DATA.counts, F=DATA.funnel;
  const cards=[
   [C.named,'Approved abroad, never in US','the screening shortlist'],
   [C.orphan,'EU orphan-flagged','and holding a real EU authorisation'],
   [C.dossier_only||0,'Dossier-only','refused/withdrawn abroad — NOT approvals'],
   [C.review||0,'Need a human call','data on hand cannot settle them'],
   ['~'+(((2029-+(DATA.generated||'2026').slice(0,4))*12)||37),'Months to deadline','program ends 2029-09-30'],
  ];
  const cw=document.getElementById('cards');
  cards.forEach(([n,l,s])=>{const d=el('div','card');d.appendChild(el('div','n',n));d.appendChild(el('div','l',l));d.appendChild(el('div','s',s));cw.appendChild(d);});
  const stages=[['dim',F.foreign_rows,'Foreign approval records looked at'],['dim',F.resolved,'Identified as a known ingredient'],
   ['',F.resolved-F.in_us,'Not found in the US approval record'],['',F.candidate_small_mol,'Small molecules (biologics removed)'],
   ['',(F.named_drug||0)+(F.no_authorisation_in_loaded_registers||0),'Have a real generic name'],
   ['',F.named_drug,'…and a genuine foreign authorisation (the shortlist)'],
   ['',C.orphan,'…and an EU orphan flag']];
  const fw=document.getElementById('funnel'), fmax=F.foreign_rows||1;
  stages.forEach(([cls,n,l])=>{const r=el('div','frow '+cls);const b=el('div','bar',(n||0).toLocaleString());
   b.style.width=Math.max(4,Math.round((n||0)/fmax*66))+'%';r.appendChild(b);r.appendChild(el('div','lab',l));fw.appendChild(r);});
})();
(function(){
  const m=DATA.monitor; const w=document.getElementById('monitor');
  if(!m){ w.textContent='No competitor data in this build.'; return; }
  const grid=el('div','mon-grid');
  const a=el('div');
  a.appendChild(el('h4','Priority Review Vouchers — Federal Register ledger'));
  a.appendChild(tp(el('div','mon-num',(m.fedreg&&m.fedreg.count!=null)?m.fedreg.count:'—'),'fedreg'));
  a.appendChild(el('div',null,'PRV documents on file'));
  const al=el('div','mon-list');
  (m.fedreg&&m.fedreg.recent||[]).forEach(r=>{const mi=el('div','mi');mi.appendChild(el('span','d',r.date||''));mi.appendChild(el('span',null,r.title||''));al.appendChild(mi);});
  a.appendChild(al); grid.appendChild(a);
  const b=el('div');
  b.appendChild(el('h4','Who is filing — SEC EDGAR ("rare pediatric disease designation")'));
  b.appendChild(tp(el('div','mon-num',(m.edgar&&m.edgar.total!=null)?m.edgar.total:'—'),'edgar'));
  b.appendChild(el('div',null,'filings mention it (2025–26)'));
  const bl=el('div','mon-list');
  (m.edgar&&m.edgar.filers||[]).forEach(f=>{const mi=el('div','mi');mi.appendChild(el('span','d',f.date||''));mi.appendChild(el('span',null,(f.name||'')+(f.form?(' · '+f.form):'')));bl.appendChild(mi);});
  b.appendChild(bl); grid.appendChild(b);
  w.appendChild(grid);
  const note=el('div'); note.style.cssText='font-size:11.5px;color:var(--ink-tertiary);padding-bottom:12px';
  note.textContent='As of '+(m.as_of||'—')+'. The FDA publishes no public rare-pediatric-designation list, so SEC filings + the Federal Register are the only competitor-detection channels. Refresh with: python3 pipeline/enrich.py';
  w.appendChild(note);
})();

render();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    main()
