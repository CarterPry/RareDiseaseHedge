#!/usr/bin/env python3
"""
Build the "Triage" dashboard (v2) from the pipeline's summary.json.

Implements pipeline/design/BUILD_BRIEF.md (which reconciles DESIGN_SPEC.md and
SCORING_MODEL.md, authored by the design / buy-side-analyst / creative-director
specialists). Self-contained single-file HTML: data + scoring embedded inline,
vanilla JS, no build step, opens by double-click, works offline.

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
<title>Triage — Funnel A PRV candidates</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap');
:root{
  --parchment:#F5F2EC; --parchment-raised:#FDFCF9; --ink:#0F1A20; --ink-secondary:#3B4D58;
  --ink-tertiary:#6E7E8A; --ink-ghost:#9DAAB4; --rule:rgba(15,26,32,.10); --rule-strong:rgba(15,26,32,.18);
  --signal:#0B6E75; --signal-dim:#D5EEF0; --signal-ink:#075056;
  --keep:#2B7A3D; --keep-bg:#EAF3EC; --investigate:#B06000; --investigate-bg:#FDF3E0;
  --reject:#A52828; --reject-bg:#FAECEC;
  --score-top:#0B5A62; --score-mid:#7A5C00; --score-low:#6B3838;
  --gold:#9a7a10; --gold-bg:#FBF1CE; --green:#2B7A3D; --green-bg:#EAF3EC; --blue:#255E8E; --blue-bg:#E6EFF7;
  --purple:#5b4a86; --purple-bg:#EEEAF6;
  --shadow-card:0 1px 2px rgba(15,26,32,.04),0 3px 8px rgba(15,26,32,.06);
  --sans:'IBM Plex Sans',-apple-system,system-ui,sans-serif; --mono:'IBM Plex Mono',ui-monospace,monospace;
}
*{box-sizing:border-box}
html,body{margin:0}
body{background:var(--parchment);color:var(--ink);font:14px/1.4 var(--sans);-webkit-font-smoothing:antialiased}
.mono{font-family:var(--mono)}
a{color:var(--signal-ink)}
/* header */
header.top{background:var(--ink);color:#EAF2F3;height:56px;display:flex;align-items:center;position:sticky;top:0;z-index:40}
header.top .wrap{max-width:1180px;margin:0 auto;padding:0 24px;width:100%;display:flex;align-items:center;gap:14px}
header.top .brand{font-weight:600;font-size:18px;letter-spacing:.5px}
header.top .sub{color:#8FB6BA;font-size:12px;font-family:var(--mono)}
header.top .right{margin-left:auto;display:flex;align-items:center;gap:14px;font-family:var(--mono);font-size:11.5px;color:#8FB6BA}
header.top button.exp{background:transparent;border:1px solid #3a4f57;color:#cfe3e5;font-family:var(--mono);font-size:11px;padding:5px 11px;border-radius:5px;cursor:pointer}
header.top button.exp:hover{border-color:var(--signal);color:#fff}
/* honesty bar */
.honesty{background:#12252b;color:#c8dcde;font-family:var(--mono);font-size:11.7px;letter-spacing:.2px;
  padding:8px 0;border-bottom:1px solid #24404733;position:sticky;top:56px;z-index:39}
.honesty .wrap{max-width:1180px;margin:0 auto;padding:0 24px}
.honesty b{color:#fff;font-weight:600}
.wrap{max-width:1180px;margin:0 auto;padding:0 24px}
/* stat cards */
.cards{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:22px 0 8px}
.card{background:var(--parchment-raised);border:1px solid var(--rule);border-radius:8px;padding:15px 16px}
.card .n{font-family:var(--mono);font-size:27px;font-weight:600;line-height:1;color:var(--ink)}
.card .l{font-size:12.5px;color:var(--ink-secondary);margin-top:7px;font-weight:500}
.card .s{font-size:11px;color:var(--ink-tertiary);margin-top:3px}
/* funnel */
details.funnel{margin:14px 0 6px}
details.funnel summary{cursor:pointer;font-family:var(--mono);font-size:11px;text-transform:uppercase;letter-spacing:.8px;color:var(--ink-tertiary);padding:6px 0}
.frow{display:flex;align-items:center;gap:12px;margin:6px 0}
.frow .bar{height:24px;border-radius:3px;background:var(--signal);display:flex;align-items:center;padding:0 9px;color:#fff;font-family:var(--mono);font-size:11px;min-width:38px}
.frow.dim .bar{background:var(--rule-strong)}
.frow .lab{font-size:12.5px;color:var(--ink-secondary)}
/* section label */
.seclabel{font-family:var(--sans);font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.8px;
  color:var(--ink-tertiary);margin:26px 0 10px;padding-bottom:7px;border-bottom:1px solid var(--rule-strong)}
/* progress */
.progress{position:sticky;top:92px;z-index:38;background:var(--parchment);padding:12px 0 8px;border-bottom:1px solid var(--rule)}
.dots{display:flex;flex-wrap:wrap;gap:3px;margin-top:7px}
.dot{width:7px;height:7px;border-radius:2px;background:var(--rule-strong)}
.dot.keep{background:var(--keep)} .dot.investigate{background:var(--investigate)} .dot.reject{background:var(--reject)}
.ptxt{font-family:var(--mono);font-size:11px;color:var(--ink-tertiary)}
/* controls */
.controls{display:flex;flex-wrap:wrap;gap:9px;align-items:center;margin:16px 0 6px}
.search{flex:1;min-width:200px;padding:9px 12px;border:1px solid var(--rule-strong);border-radius:6px;font-family:var(--sans);font-size:13.5px;background:var(--parchment-raised)}
.search:focus{outline:2px solid var(--signal);border-color:var(--signal)}
select.sort{padding:9px 10px;border:1px solid var(--rule-strong);border-radius:6px;font-family:var(--mono);font-size:12px;background:var(--parchment-raised);color:var(--ink)}
.chips{display:flex;flex-wrap:wrap;gap:7px;margin:4px 0}
.chip{border:1px solid var(--rule-strong);background:var(--parchment-raised);border-radius:15px;padding:5px 12px;font-family:var(--mono);font-size:11.5px;cursor:pointer;color:var(--ink-secondary);user-select:none}
.chip.on{background:var(--signal-ink);color:#fff;border-color:var(--signal-ink)}
.count{margin-left:auto;font-family:var(--mono);font-size:11.5px;color:var(--ink-tertiary)}
.banner{background:var(--investigate-bg);border:1px solid #e8c88c;color:#7a4d00;border-radius:6px;padding:9px 13px;font-size:12.5px;margin:8px 0;display:flex;gap:10px;align-items:center}
.banner button{margin-left:auto;background:none;border:none;color:#7a4d00;cursor:pointer;font-size:15px}
/* rows */
.list{margin-top:4px}
.row{display:grid;grid-template-columns:1fr auto 96px;gap:0 14px;align-items:center;min-height:64px;
  background:var(--parchment-raised);border:1px solid var(--rule);border-top:none;padding:10px 16px 10px 0;cursor:pointer;position:relative}
.row:first-child{border-top:1px solid var(--rule);border-radius:8px 8px 0 0}
.row:last-child{border-radius:0 0 8px 8px}
.row:hover{background:#fff}
.row.rejected{opacity:.5}
.rail{position:absolute;left:0;top:0;bottom:0;width:4px;background:transparent;border-radius:8px 0 0 8px}
.row.t-keep .rail{background:var(--keep)} .row.t-investigate .rail{background:var(--investigate)} .row.t-reject .rail{background:var(--reject)}
.rmain{padding-left:16px;min-width:0}
.rname{font-weight:600;font-size:15px;letter-spacing:.2px}
.rl2{font-size:13px;color:var(--ink-secondary);margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.rl3{display:flex;gap:8px;align-items:center;margin-top:5px;font-family:var(--mono);font-size:11px;color:var(--ink-tertiary);flex-wrap:wrap}
.badges{display:inline-flex;gap:5px;margin-left:9px;vertical-align:middle}
.b{font-family:var(--mono);font-size:10px;font-weight:600;padding:2px 6px;border-radius:3px;letter-spacing:.3px}
.b.orphan{background:var(--gold-bg);color:var(--gold)} .b.inn{background:var(--green-bg);color:var(--green)}
.b.usan{background:var(--blue-bg);color:var(--blue)} .b.atc{background:var(--purple-bg);color:var(--purple)}
.b.caveat{background:var(--investigate-bg);color:var(--investigate)}
.srcchip{background:var(--parchment);border:1px solid var(--rule);border-radius:3px;padding:1px 6px}
.cdot{width:7px;height:7px;border-radius:50%;display:inline-block}
.cdot.high{background:var(--keep)} .cdot.medium{background:var(--investigate)} .cdot.low{background:var(--ink-ghost)}
/* score column */
.score{text-align:right;padding-right:16px}
.snum{font-family:var(--mono);font-size:22px;font-weight:600;line-height:1}
.snum.top{color:var(--score-top)} .snum.mid{color:var(--score-mid)} .snum.low{color:var(--score-low)}
.sbar{display:flex;gap:2px;justify-content:flex-end;margin-top:5px}
.seg{width:6px;height:6px;border-radius:1px;background:var(--rule-strong)}
.seg.on.top{background:var(--score-top)} .seg.on.mid{background:var(--score-mid)} .seg.on.low{background:var(--score-low)}
/* hover triage icons */
.tri{display:none;gap:4px;justify-self:end}
.row:hover .tri{display:flex}
.tri button{width:26px;height:26px;border:1px solid var(--rule-strong);background:var(--parchment-raised);border-radius:5px;cursor:pointer;font-size:13px;color:var(--ink-tertiary);line-height:1}
.tri button:hover{border-color:var(--signal);color:var(--signal-ink)}
.tri button.on-keep{background:var(--keep-bg);color:var(--keep);border-color:var(--keep)}
.tri button.on-investigate{background:var(--investigate-bg);color:var(--investigate);border-color:var(--investigate)}
.tri button.on-reject{background:var(--reject-bg);color:var(--reject);border-color:var(--reject)}
.empty{padding:40px;text-align:center;color:var(--ink-tertiary)}
/* drawer */
.overlay{position:fixed;inset:0;background:rgba(15,26,32,.32);opacity:0;pointer-events:none;transition:opacity .18s;z-index:50}
.overlay.open{opacity:1;pointer-events:auto}
.drawer{position:fixed;top:0;right:0;bottom:0;width:min(560px,94vw);background:var(--parchment-raised);
  box-shadow:-6px 0 30px rgba(15,26,32,.18);transform:translateX(100%);transition:transform .2s;z-index:51;overflow-y:auto}
.drawer.open{transform:translateX(0)}
.dhead{position:sticky;top:0;background:var(--parchment-raised);border-bottom:1px solid var(--rule-strong);padding:16px 22px;display:flex;align-items:center;gap:12px}
.dhead h2{margin:0;font-size:19px;font-weight:600;flex:1}
.dhead .x{background:none;border:none;font-size:20px;cursor:pointer;color:var(--ink-tertiary)}
.seg-ctl{display:flex;gap:0;border:1px solid var(--rule-strong);border-radius:6px;overflow:hidden}
.seg-ctl button{background:var(--parchment-raised);border:none;border-right:1px solid var(--rule);padding:6px 10px;font-family:var(--mono);font-size:10.5px;cursor:pointer;color:var(--ink-secondary)}
.seg-ctl button:last-child{border-right:none}
.seg-ctl button.on-keep{background:var(--keep);color:#fff} .seg-ctl button.on-investigate{background:var(--investigate);color:#fff} .seg-ctl button.on-reject{background:var(--reject);color:#fff}
.dbody{padding:18px 22px 60px}
.dsec{margin:20px 0}
.dsec .lbl{font-family:var(--mono);font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.7px;color:var(--ink-tertiary);margin-bottom:6px}
.dsec .val{font-size:14px;color:var(--ink)}
.dsec .prose{font-size:13.5px;line-height:1.6;color:var(--ink-secondary);font-style:italic;border-left:2px solid var(--rule-strong);padding-left:12px}
.scorebox{background:var(--parchment);border:1px solid var(--rule-strong);border-radius:8px;padding:16px}
.scorebox .big{font-family:var(--mono);font-size:34px;font-weight:600;line-height:1}
.scorebox .tier{font-family:var(--mono);font-size:12px;margin-top:4px}
.scorebox .note{font-size:12px;color:var(--ink-tertiary);margin-top:8px;line-height:1.5}
.evbox{background:var(--parchment);border:1px dashed var(--rule-strong);border-radius:8px;padding:14px}
.evbox .lbl{color:var(--ink-tertiary)}
.evbox .p{font-family:var(--mono);font-size:14px;color:var(--ink)}
.evbox .rng{font-family:var(--mono);font-size:13px;color:var(--ink-secondary);margin-top:4px}
.caveat{background:var(--investigate-bg);border:1px solid #e8c88c;border-radius:6px;padding:10px 12px;font-size:12.5px;color:#7a4d00;margin-top:8px}
.brk table{width:100%;border-collapse:collapse;font-family:var(--mono);font-size:11.5px;margin-top:8px}
.brk td{padding:3px 6px;border-bottom:1px solid var(--rule)}
.brk td:last-child{text-align:right}
.chk{display:flex;align-items:center;gap:8px;font-size:13px;margin:6px 0;color:var(--ink-secondary)}
textarea.note{width:100%;min-height:70px;border:1px solid var(--rule-strong);border-radius:6px;padding:9px;font-family:var(--sans);font-size:13px;resize:vertical;background:var(--parchment)}
.links a{font-family:var(--mono);font-size:12px;margin-right:14px}
footer{color:var(--ink-tertiary);font-size:12px;text-align:center;margin:40px 0 30px;font-family:var(--mono)}
@media(prefers-reduced-motion:reduce){.drawer,.overlay{transition:none}}
@media print{.controls,.chips,.progress,.tri,.drawer,.overlay,header.top .right,details.funnel{display:none!important}
  .row{break-inside:avoid}body{background:#fff}}
@media(max-width:760px){.cards{grid-template-columns:repeat(2,1fr)}.row{grid-template-columns:14px 1fr 70px}.tri{display:none!important}}
</style>
</head>
<body>
<header class="top"><div class="wrap">
  <span class="brand">Triage</span>
  <span class="sub">Funnel A · PRV-eligible candidate universe</span>
  <span class="right"><button class="exp" id="export">Export triage</button><label class="exp" style="cursor:pointer">Import<input id="import" type="file" accept="application/json" hidden></label><span id="gen"></span></span>
</div></header>
<div class="honesty"><div class="wrap" id="honesty"></div></div>

<div class="wrap">
  <div class="cards" id="cards"></div>
  <details class="funnel"><summary>How the funnel narrows</summary><div id="funnel"></div></details>

  <div class="progress">
    <div class="ptxt" id="ptxt"></div>
    <div class="dots" id="dots"></div>
  </div>

  <div class="controls">
    <input class="search" id="search" placeholder="Search name, indication, therapeutic area…">
    <select class="sort" id="sort">
      <option value="score">Sort: Promise score ↓</option>
      <option value="score_asc">Promise score ↑</option>
      <option value="name">Name A–Z</option>
      <option value="area">Therapeutic area</option>
      <option value="sources">Regulator count</option>
      <option value="orphan">Orphan first</option>
      <option value="recency">Recency of approval</option>
      <option value="shuffle">Shuffle</option>
    </select>
  </div>
  <div class="chips" id="chips-src"></div>
  <div class="chips" id="chips-tri"></div>
  <div id="banner-slot"></div>
  <div class="controls"><span class="count" id="count"></span></div>

  <div class="list" id="list"></div>

  <div class="seclabel">Reading this honestly</div>
  <p style="font-size:13px;color:var(--ink-secondary);max-width:760px">The promise score ranks likelihood of surviving downstream diligence — <b>not</b> probability of regulatory approval. It cannot see freedom-to-operate, existing US orphan exclusivity, API sourcing, or trial feasibility. A high score means "worth a diligence week," not "a business." The ~7-actionable estimate, not the 105, is the honest size of the opportunity.</p>
  <footer>Generated by pipeline/build_ui.py · triage state stored locally in your browser · data embedded, works offline</footer>
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

/* ---------- scoring (full PED where indication text exists) ---------- */
function pedScore(c){
  const text=((c.indication||'')+' '+(c.area||'')).toLowerCase();
  if(!text.trim()) return {v:0.2, floored:true};
  if(P.ped_strong.some(k=>text.includes(k))) return {v:1.0, floored:false};
  if(P.ped_moderate.some(k=>text.includes(k))) return {v:0.5, floored:false};
  return {v:0.0, floored:false};
}
function atcSub(c){
  if(!c.atc) return 0.3;
  const k=c.atc.slice(0,3).toUpperCase();
  if(P.high_atc.includes(k)) return 1.0;
  if(P.med_atc.includes(k)) return 0.5;
  return 0.1;
}
function recencySub(c){
  if(!c.approved) return 0.3;
  const m=(c.approved.match(/(\d{4})/)||[])[1]; const y=m?+m:0;
  if(y>=2015) return 1.0; if(y>=2005) return 0.7; if(y>=1995) return 0.4; return 0.1;
}
const TIERMAP={'exact-moiety':1.0,'exact':1.0,'moiety-base':0.7,'salt-stripped':0.7,'moiety':0.7,'direct':0.5,'name-match':0.4,'fuzzy':0.1};
function regSub(c){const n=c.sources.length; return n>=3?1.0:n===2?0.6:n===1?0.2:0.0;}
function score(c){
  const ped=pedScore(c), orph=c.orphan?1:0, reg=regSub(c),
        match=(TIERMAP[c.tier]??0.3), atc=atcSub(c), rec=recencySub(c);
  const total=Math.round(35*ped.v+25*orph+15*reg+15*match+5*atc+5*rec);
  return {total, floored:ped.floored, parts:[
    ['Pediatric-rare signal',35,ped.v, ped.floored?'no indication text — floored':''],
    ['Foreign orphan flag',25,orph,''],
    ['Regulator count',15,reg, c.sources.length+' source(s)'],
    ['Match confidence',15,match, c.tier],
    ['ATC proximity',5,atc, c.atc||'—'],
    ['Approval recency',5,rec, c.approved||'—'],
  ]};
}
function tierOf(s){ return s>=60?{k:'A',lab:'A — Worth a diligence week',cls:'top'}
                  : s>=45?{k:'B',lab:'B — Needs a trigger',cls:'mid'}
                  : {k:'C',lab:'C — Screen level',cls:'low'}; }
CANDS.forEach(c=>{ const s=score(c); c._s=s.total; c._floored=s.floored; c._parts=s.parts; c._tier=tierOf(s.total); });

/* caveat flags derived client-side (v2 interim; pipeline may populate later) */
function caveats(c){
  const out=[];
  if(['moiety-base','salt-stripped','moiety'].includes(c.tier)) out.push('Salt/base match only — verify active moiety against Orange Book.');
  if(/onium|sulfate ester|prodrug/i.test(c.name)) out.push('Possible prodrug — active moiety may already be US-approved under a different parent.');
  return out;
}

/* ---------- header / honesty / cards / funnel ---------- */
document.getElementById('gen').textContent='generated '+DATA.generated;
document.getElementById('honesty').innerHTML=
  `<b>${DATA.counts.named} candidates</b> in screening shortlist · <b>~7 estimated actionable</b> after orphan-designation, pediatric-indication fit, FTO, API sourcing and timeline filters · FDA PRV sunset <b>2029-09-30</b> · window remaining <b>~37 months</b>`;
const C=DATA.counts, F=DATA.funnel;
[['','.',''],].slice(0,0);
const cards=[
 [C.named,'Named drug candidates','screening shortlist'],
 [C.orphan,'Foreign orphan-flagged','rare-disease filter passed; pediatric, FTO, API, timeline remain'],
 ['~7','Estimated actionable','after FTO, orphan exclusivity, API sourcing, timeline'],
 ['37 mo','To PRV sunset','2029-09-30'],
];
const cw=document.getElementById('cards');
cards.forEach(([n,l,s])=>{const d=el('div','card');d.appendChild(el('div','n',n));d.appendChild(el('div','l',l));d.appendChild(el('div','s',s));cw.appendChild(d);});
const stages=[['dim',F.foreign_rows,'Foreign approval rows ingested'],['dim',F.resolved,'Resolved to an FDA UNII'],
 ['',F.resolved-F.in_us,'Moiety not in the US approval record'],['',F.candidate_small_mol,'Small-molecule (biologics removed)'],
 ['',F.named_drug,'Named drug (INN or USAN)'],['',C.orphan,'Foreign orphan-flagged']];
const fw=document.getElementById('funnel'), fmax=F.foreign_rows;
stages.forEach(([cls,n,l])=>{const r=el('div','frow '+cls);const b=el('div','bar',n.toLocaleString());
 b.style.width=Math.max(4,Math.round(n/fmax*66))+'%';r.appendChild(b);r.appendChild(el('div','lab',l));fw.appendChild(r);});

/* ---------- filters/state ---------- */
const SRC=['Orphan only','INN','EMA','Health Canada','Swissmedic','PMDA-JP'];
const TRI=['Keep','Investigate','Untriaged','Rejected'];
let fsrc=new Set(), ftri=new Set(), query='', sortBy='score', shuffleSeed=1;
function mkChips(id,arr,set){const w=document.getElementById(id);arr.forEach(t=>{const c=el('span','chip',t);
 c.onclick=()=>{set.has(t)?set.delete(t):set.add(t);c.classList.toggle('on');render();};w.appendChild(c);});}
mkChips('chips-src',SRC,fsrc); mkChips('chips-tri',TRI,ftri);

function passes(c){
  if(fsrc.has('Orphan only')&&!c.orphan) return false;
  if(fsrc.has('INN')&&!c.inn) return false;
  const srcSel=['EMA','Health Canada','Swissmedic','PMDA-JP'].filter(s=>fsrc.has(s));
  if(srcSel.length&&!srcSel.some(s=>c.sources.includes(s))) return false;
  const st=tstate(c.unii);
  if(ftri.size){
    const want=[]; if(ftri.has('Keep'))want.push('keep'); if(ftri.has('Investigate'))want.push('investigate');
    if(ftri.has('Rejected'))want.push('reject');
    const unt=ftri.has('Untriaged');
    const ok=(st&&want.includes(st))||(unt&&!st);
    if(!ok) return false;
  } else { /* default: hide rejected unless explicitly shown handled below */ }
  if(query){const h=(c.name+' '+(c.indication||'')+' '+(c.area||'')).toLowerCase();if(!h.includes(query))return false;}
  return true;
}
const SORTS={
  score:(a,b)=>b._s-a._s, score_asc:(a,b)=>a._s-b._s,
  name:(a,b)=>a.name.localeCompare(b.name),
  area:(a,b)=>(a.area||'~').localeCompare(b.area||'~'),
  sources:(a,b)=>b.sources.length-a.sources.length||b._s-a._s,
  orphan:(a,b)=>(b.orphan-a.orphan)||b._s-a._s,
  recency:(a,b)=>((b.approved||'').slice(0,4)).localeCompare((a.approved||'').slice(0,4))||b._s-a._s,
  shuffle:(a,b)=>((Math.sin((CANDS.indexOf(a)+1)*shuffleSeed*99)+1)-(Math.sin((CANDS.indexOf(b)+1)*shuffleSeed*99)+1)),
};
document.getElementById('sort').onchange=e=>{sortBy=e.target.value; if(sortBy==='shuffle')shuffleSeed=Math.floor(Math.sin(Date.parse(DATA.generated)/8.64e7)*1e4)/1e4+ (shuffleSeed*1.7%3); render();};
let searchTO; document.getElementById('search').oninput=e=>{clearTimeout(searchTO);searchTO=setTimeout(()=>{query=e.target.value.trim().toLowerCase();render();},200);};

/* interim banner if any candidate PED floored */
if(CANDS.some(c=>c._floored) && localStorage.getItem('rdh_banner_'+DATA.generated)!=='1'){
  const slot=document.getElementById('banner-slot');
  const b=el('div','banner');
  b.appendChild(el('span',null,'Scoring is partial — candidates without abroad-indication text (mostly Canada/Swissmedic/Japan rows) have their pediatric component floored, so their rank understates them. EMA rows are fully scored.'));
  const x=el('button',null,'✕'); x.onclick=()=>{localStorage.setItem('rdh_banner_'+DATA.generated,'1');b.remove();}; b.appendChild(x);
  slot.appendChild(b);
}

/* ---------- rows ---------- */
const listEl=document.getElementById('list');
function segBar(s,cls){const w=el('div','sbar');const on=Math.round(s/10);for(let i=0;i<10;i++){const g=el('div','seg'+(i<on?' on '+cls:''));w.appendChild(g);}return w;}
function rowNode(c){
  const st=tstate(c.unii);
  const r=el('div','row'+(st?' t-'+st:'')+(st==='reject'?' rejected':''));
  r.tabIndex=0; r.setAttribute('role','button');
  r.appendChild(el('div','rail'));
  const main=el('div','rmain');
  const nm=el('div','rname'); nm.appendChild(document.createTextNode(titleCase(c.name)));
  const bd=el('span','badges');
  if(c.orphan)bd.appendChild(el('span','b orphan','ORPHAN'));
  if(c.inn)bd.appendChild(el('span','b inn','INN'));
  if(c.usan)bd.appendChild(el('span','b usan','USAN'));
  if(c.atc)bd.appendChild(el('span','b atc',c.atc));
  if(caveats(c).length)bd.appendChild(el('span','b caveat','⚑'));
  nm.appendChild(bd); main.appendChild(nm);
  const area=(c.area||'').split(';')[0];
  const l2txt=[area, c.indication].filter(Boolean).join(' · ');
  if(l2txt){const l2=el('div','rl2',l2txt);main.appendChild(l2);}
  const l3=el('div','rl3');
  c.sources.forEach(s=>l3.appendChild(el('span','srcchip',s)));
  l3.appendChild(el('span',null, c.approved?('Approved '+c.approved):'—'));
  const conf=(c.tier==='exact-moiety'||c.tier==='exact')?'high':(c.tier==='moiety-base'?'medium':'low');
  const cd=el('span','cdot '+conf); l3.appendChild(cd); l3.appendChild(el('span',null,conf+' confidence'));
  main.appendChild(l3);
  r.appendChild(main);
  // triage hover icons
  const tri=el('div','tri');
  [['keep','◆'],['investigate','◎'],['reject','✕']].forEach(([k,g])=>{
    const bt=el('button',(st===k?'on-'+k:''),g); bt.title=k;
    bt.onclick=(e)=>{e.stopPropagation(); setTriage(c.unii,st===k?null:k); render();};
    tri.appendChild(bt);
  });
  r.appendChild(tri);
  // score column
  const sc=el('div','score');
  const sn=el('div','snum '+c._tier.cls, c._s); sc.appendChild(sn);
  sc.appendChild(segBar(c._s,c._tier.cls));
  r.appendChild(sc);
  r.onclick=()=>openDrawer(c);
  r.onkeydown=(e)=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();openDrawer(c);}};
  return r;
}
function setTriage(u,state){
  if(!triage[u])triage[u]={};
  if(state===null){ delete triage[u].state; if(!triage[u].note && !triage[u].registry_identified && !triage[u].advocacy_contact) delete triage[u]; }
  else { triage[u].state=state; triage[u].ts=Date.now(); }
  saveTriage();
}
function render(){
  let rows=CANDS.filter(passes);
  // default: hide rejected unless "Rejected" chip active
  if(!ftri.has('Rejected')) rows=rows.filter(c=>tstate(c.unii)!=='reject');
  rows.sort(SORTS[sortBy]||SORTS.score);
  listEl.innerHTML='';
  if(!rows.length)listEl.appendChild(el('div','empty','No candidates match those filters.'));
  else rows.forEach(c=>listEl.appendChild(rowNode(c)));
  document.getElementById('count').textContent=`Showing ${rows.length} of ${CANDS.length} candidates`;
  renderProgress();
}
function renderProgress(){
  const counts={keep:0,investigate:0,reject:0};
  CANDS.forEach(c=>{const s=tstate(c.unii); if(s)counts[s]++;});
  const done=counts.keep+counts.investigate+counts.reject;
  document.getElementById('ptxt').textContent=
   `Triaged ${done} of ${CANDS.length}  ·  ${counts.keep} keep · ${counts.investigate} investigate · ${counts.reject} reject`;
  const dw=document.getElementById('dots'); dw.innerHTML='';
  CANDS.forEach(c=>{const s=tstate(c.unii); dw.appendChild(el('span','dot'+(s?' '+s:'')));});
}

/* ---------- drawer ---------- */
const overlay=document.getElementById('overlay'), drawer=document.getElementById('drawer');
let lastFocus=null;
function fmtEV(c){
  // probability-first, generic vs optimized; suppressed for Tier C
  const base=190; // $M
  const pGen=0.04, pOpt=0.21, cost=0.5;
  const lo=Math.round(pGen*base-cost), hi=Math.round(pOpt*base-cost);
  return {pGen,pOpt,lo,hi};
}
function openDrawer(c){
  lastFocus=document.activeElement;
  const cav=caveats(c), t=c._tier, ev=fmtEV(c), rec=(triage[c.unii]||{});
  const links=[['EMA','https://www.ema.europa.eu/en/search?search_api_fulltext='+encodeURIComponent(c.name)],
    ['PubMed','https://pubmed.ncbi.nlm.nih.gov/?term='+encodeURIComponent(c.name)],
    ['DrugBank','https://go.drugbank.com/unearth/q?query='+encodeURIComponent(c.name)+'&searcher=drugs'],
    ['FDA UNII','https://gsrs.ncats.nih.gov/ginas/app/beta/substances/'+c.unii]];
  const atcLab=c.atc?(P.atc_labels[c.atc.slice(0,3).toUpperCase()]||''):'';
  drawer.innerHTML='';
  const head=el('div','dhead');
  head.appendChild(Object.assign(el('h2',null,titleCase(c.name)),{}));
  const seg=el('div','seg-ctl');
  [['keep','KEEP'],['investigate','INVESTIGATE'],['reject','REJECT']].forEach(([k,l])=>{
    const b=el('button',(tstate(c.unii)===k?'on-'+k:''),l);
    b.onclick=()=>{setTriage(c.unii, tstate(c.unii)===k?null:k); openDrawer(c); render();};
    seg.appendChild(b);
  });
  head.appendChild(seg);
  const x=el('button','x','✕'); x.onclick=closeDrawer; head.appendChild(x);
  drawer.appendChild(head);

  const body=el('div','dbody');
  const badge=el('div','dsec');
  const bb=el('div','badges');
  if(c.orphan)bb.appendChild(el('span','b orphan','ORPHAN'));
  if(c.inn)bb.appendChild(el('span','b inn','INN'));
  if(c.usan)bb.appendChild(el('span','b usan','USAN'));
  if(c.atc)bb.appendChild(el('span','b atc',c.atc));
  badge.appendChild(bb); body.appendChild(badge);

  // score
  const ss=el('div','dsec');
  ss.appendChild(el('div','lbl','Promise score (triage rank only)'));
  const sb=el('div','scorebox');
  sb.appendChild(el('div','big '+t.cls, c._s));
  sb.appendChild(el('div','tier '+t.cls, t.lab));
  sb.appendChild(el('div','note','Ranks likelihood of surviving downstream diligence — not probability of regulatory approval.'));
  if(c._floored) sb.appendChild(Object.assign(el('div','caveat'),{textContent:'Score partial — pediatric component (weight 35) floored: no abroad-indication text for this row.'}));
  const brk=el('details','brk'); brk.appendChild(el('summary',null,'Score breakdown'));
  const tbl=el('table');
  c._parts.forEach(([n,w,v,note])=>{const tr=el('tr');
    tr.appendChild(el('td',null,n)); tr.appendChild(el('td',null,note||''));
    tr.appendChild(el('td',null,Math.round(w*v)+' / '+w)); tbl.appendChild(tr);});
  brk.appendChild(tbl); sb.appendChild(brk);
  ss.appendChild(sb); body.appendChild(ss);

  // what it treats
  if(c.area||c.indication){const w=el('div','dsec');w.appendChild(el('div','lbl','What it treats'));
    if(c.area)w.appendChild(el('div','val',c.area.replace(/;/g,' · ')));
    if(c.indication)w.appendChild(Object.assign(el('div','prose'),{textContent:c.indication}));
    body.appendChild(w);}
  // ATC
  if(c.atc){const w=el('div','dsec');w.appendChild(el('div','lbl','ATC classification'));
    w.appendChild(el('div','val',c.atc+(atcLab?'  ·  '+atcLab:'')));body.appendChild(w);}
  // dates
  const dt=el('div','dsec');dt.appendChild(el('div','lbl','Regulatory dates'));
  dt.appendChild(el('div','val','Approved abroad: '+(c.approved||'—')));body.appendChild(dt);

  // EV
  const evs=el('div','dsec');evs.appendChild(el('div','lbl','Risk-adjusted EV proxy'));
  if(t.k==='C'){
    evs.appendChild(Object.assign(el('div','caveat'),{textContent:'EV proxy not shown — a Tier C candidate needs a stronger diligence basis before financial framing is appropriate.'}));
  } else {
    const box=el('div','evbox');
    box.appendChild(el('div','p','P(success): ~4% generic  →  up to ~21% optimized'));
    box.appendChild(el('div','rng','Trial cost floor ~$0.5M · PRV value ~$190M → risk-adjusted EV ≈ $'+ev.lo+'M – $'+ev.hi+'M'));
    evs.appendChild(box);
    evs.appendChild(Object.assign(el('div','caveat'),{textContent:'A proxy, not a valuation. Assumes the candidate clears FTO, has no blocking US orphan exclusivity, sane API sourcing, and a feasible ~20-patient trial — none of which this score can see.'}));
  }
  body.appendChild(evs);

  // timeline check
  const tl=el('div','dsec');tl.appendChild(el('div','lbl','Timeline check'));
  tl.appendChild(el('div','val','Latest viable first-patient-in ≈ 2027-02-28 to clear the 2029-09-30 sunset.'));
  [['registry_identified','Patient registry or natural-history dataset identified'],
   ['advocacy_contact','Advocacy-group contact made']].forEach(([key,lab])=>{
    const row=el('label','chk');const cb=el('input');cb.type='checkbox';cb.checked=!!rec[key];
    cb.onchange=()=>{if(!triage[c.unii])triage[c.unii]={};triage[c.unii][key]=cb.checked;saveTriage();};
    row.appendChild(cb);row.appendChild(el('span',null,lab));tl.appendChild(row);});
  body.appendChild(tl);

  // sources & provenance
  const sp=el('div','dsec');sp.appendChild(el('div','lbl','Sources & provenance'));
  sp.appendChild(el('div','val',c.sources.join(' · ')));
  sp.appendChild(Object.assign(el('div','val'),{style:'font-family:var(--mono);font-size:12px;color:var(--ink-tertiary);margin-top:4px',
    textContent:'UNII '+c.unii+' · match '+c.tier}));
  const lk=el('div','links');lk.style.marginTop='8px';
  links.forEach(([t2,u])=>{const a=el('a',null,t2);a.href=u;a.target='_blank';a.rel='noopener';lk.appendChild(a);});
  sp.appendChild(lk);body.appendChild(sp);

  // caveats
  if(cav.length){const w=el('div','dsec');w.appendChild(el('div','lbl','Caveat flags'));
    cav.forEach(t2=>w.appendChild(Object.assign(el('div','caveat'),{textContent:t2})));body.appendChild(w);}

  // note
  const nt=el('div','dsec');nt.appendChild(el('div','lbl','Triage note'));
  const ta=el('textarea','note');ta.value=rec.note||'';ta.placeholder='Working notes for this candidate…';
  let nto;ta.oninput=()=>{clearTimeout(nto);nto=setTimeout(()=>{if(!triage[c.unii])triage[c.unii]={};triage[c.unii].note=ta.value;saveTriage();},400);};
  nt.appendChild(ta);body.appendChild(nt);

  drawer.appendChild(body);
  overlay.classList.add('open');drawer.classList.add('open');
  drawer.querySelector('.x').focus();
}
function closeDrawer(){overlay.classList.remove('open');drawer.classList.remove('open');if(lastFocus)lastFocus.focus();}
overlay.onclick=closeDrawer;
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&drawer.classList.contains('open'))closeDrawer();});

/* export / import */
document.getElementById('export').onclick=()=>{
  const blob=new Blob([JSON.stringify(triage,null,1)],{type:'application/json'});
  const a=el('a');a.href=URL.createObjectURL(blob);a.download='rdh_triage_'+DATA.generated+'.json';a.click();
};
document.getElementById('import').onchange=e=>{const f=e.target.files[0];if(!f)return;const r=new FileReader();
  r.onload=()=>{try{triage=JSON.parse(r.result);saveTriage();render();}catch(err){alert('Invalid triage file');}};r.readAsText(f);};

render();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    main()
