#!/usr/bin/env python3
"""
Generate a self-contained dashboard from the pipeline's summary.json.

Reads  pipeline/data/out/summary.json
Writes pipeline/ui/index.html   (open it in any browser — no server needed)

The HTML embeds the data inline, so the file is portable and works offline.
Re-run after rdh_diff.py to refresh.
"""
import json, os, html

HERE = os.path.dirname(os.path.abspath(__file__))
SUMMARY = os.path.join(HERE, "data", "out", "summary.json")
OUT_DIR = os.path.join(HERE, "ui")
OUT = os.path.join(OUT_DIR, "index.html")

TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>RareDiseaseHedge — Funnel A candidates</title>
<style>
  :root{
    --bg:#eef1f5; --panel:#ffffff; --ink:#132029; --muted:#5c6b76; --line:#e2e7ee;
    --accent:#0b6e75; --accent-ink:#075056; --gold:#b7791f; --gold-bg:#fdf3d7;
    --green:#2f855a; --green-bg:#e6f4ec; --blue:#2b6cb0; --blue-bg:#e7f0fa;
    --danger:#b83232;
    --shadow:0 1px 2px rgba(19,32,41,.04),0 6px 20px rgba(19,32,41,.06);
  }
  *{box-sizing:border-box}
  html,body{margin:0}
  body{background:var(--bg);color:var(--ink);
    font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,Helvetica,Arial,sans-serif;
    -webkit-font-smoothing:antialiased;padding:0 0 80px}
  .wrap{max-width:1080px;margin:0 auto;padding:0 22px}
  header.top{background:linear-gradient(135deg,#0b6e75,#0a565c);color:#eafcff;padding:34px 0 30px;box-shadow:var(--shadow)}
  header.top .wrap{display:flex;flex-direction:column;gap:6px}
  header.top h1{margin:0;font-size:25px;letter-spacing:-.3px;font-weight:650}
  header.top p{margin:0;color:#bfeef2;font-size:14px;max-width:760px}
  header.top .meta{color:#8fd4da;font-size:12.5px;margin-top:8px}

  .verdict{background:#fff;border-left:4px solid var(--gold);border-radius:10px;
    box-shadow:var(--shadow);padding:16px 20px;margin:22px 0;font-size:14px;color:#3b4a54}
  .verdict b{color:var(--ink)}

  .cards{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:20px 0}
  .card{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:16px 18px;box-shadow:var(--shadow)}
  .card .n{font-size:30px;font-weight:680;letter-spacing:-.5px;line-height:1}
  .card .l{color:var(--muted);font-size:12.5px;margin-top:7px}
  .card.gold .n{color:var(--gold)} .card.accent .n{color:var(--accent)}

  section{margin:30px 0}
  h2{font-size:15px;text-transform:uppercase;letter-spacing:.6px;color:var(--muted);
     font-weight:650;margin:0 0 14px;padding-bottom:8px;border-bottom:1px solid var(--line)}

  /* funnel */
  .funnel{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:20px 22px;box-shadow:var(--shadow)}
  .frow{display:flex;align-items:center;gap:14px;margin:9px 0}
  .frow .bar{height:30px;border-radius:6px;background:linear-gradient(90deg,#0b6e75,#3aa6ad);
     display:flex;align-items:center;padding:0 11px;color:#fff;font-size:12.5px;font-weight:600;min-width:44px;white-space:nowrap}
  .frow.dim .bar{background:linear-gradient(90deg,#9aa7b1,#b9c3cc)}
  .frow.win .bar{background:linear-gradient(90deg,#b7791f,#d8a13a)}
  .frow .lab{font-size:13.5px;color:#3b4a54;flex:1}
  .frow .lab b{color:var(--ink)}

  /* controls */
  .controls{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-bottom:16px}
  .search{flex:1;min-width:220px;padding:10px 13px;border:1px solid var(--line);border-radius:9px;font-size:14px;background:#fff}
  .search:focus{outline:2px solid var(--accent);border-color:var(--accent)}
  .chip{border:1px solid var(--line);background:#fff;border-radius:20px;padding:7px 14px;font-size:13px;cursor:pointer;color:#3b4a54;user-select:none}
  .chip.on{background:var(--accent-ink);color:#fff;border-color:var(--accent-ink)}
  .count{color:var(--muted);font-size:13px;margin-left:auto}

  /* candidate list */
  .list{display:grid;gap:10px}
  .item{background:var(--panel);border:1px solid var(--line);border-radius:11px;padding:14px 16px;box-shadow:var(--shadow);
    display:grid;grid-template-columns:1fr auto;gap:6px 14px;align-items:start}
  .item.orphan{border-left:3px solid var(--gold)}
  .name{font-size:16px;font-weight:620;letter-spacing:-.2px}
  .sub{color:var(--muted);font-size:12.5px;margin-top:2px;font-family:ui-monospace,SFMono-Regular,Menlo,monospace}
  .badges{display:flex;flex-wrap:wrap;gap:6px;margin-top:9px}
  .b{font-size:11.5px;font-weight:600;padding:3px 9px;border-radius:20px;border:1px solid transparent}
  .b.orphan{background:var(--gold-bg);color:var(--gold);border-color:#e6d59a}
  .b.inn{background:var(--green-bg);color:var(--green)}
  .b.usan{background:var(--blue-bg);color:var(--blue)}
  .b.src{background:#eef1f5;color:#4a5a65}
  .b.tier{background:#f3f0fb;color:#6b4fb0}
  .links{display:flex;gap:12px;justify-self:end;align-self:center}
  .links a{font-size:12.5px;color:var(--accent);text-decoration:none;white-space:nowrap}
  .links a:hover{text-decoration:underline}
  .empty{color:var(--muted);text-align:center;padding:40px;font-size:14px}

  details.caveats{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:4px 18px;box-shadow:var(--shadow)}
  details.caveats summary{cursor:pointer;font-weight:600;padding:14px 0;font-size:14px}
  details.caveats ul{margin:0 0 16px;padding-left:20px;color:#3b4a54;font-size:13.5px}
  details.caveats li{margin:7px 0}
  footer{color:var(--muted);font-size:12.5px;text-align:center;margin-top:36px}
  @media(max-width:720px){.cards{grid-template-columns:repeat(2,1fr)}.item{grid-template-columns:1fr}.links{justify-self:start}}
</style>
</head>
<body>
<header class="top"><div class="wrap">
  <h1>Funnel A — PRV-eligible candidate universe</h1>
  <p>Active substances approved by a foreign regulator whose active moiety has <b>never been approved in the US</b> — the only route to a transferable Priority Review Voucher for a repurposed drug (21 U.S.C. § 360ff).</p>
  <div class="meta" id="meta"></div>
</div></header>

<div class="wrap">
  <div class="verdict" id="verdict"></div>

  <div class="cards" id="cards"></div>

  <section>
    <h2>How the funnel narrows</h2>
    <div class="funnel" id="funnel"></div>
  </section>

  <section>
    <h2>Candidates — start manual review with the orphan-flagged rows</h2>
    <div class="controls">
      <input class="search" id="search" placeholder="Search by name…">
      <span class="chip" data-f="orphan">★ Orphan only</span>
      <span class="chip" data-f="inn">INN only</span>
      <span class="chip" data-f="EMA">EMA</span>
      <span class="chip" data-f="Health Canada">Canada</span>
      <span class="chip" data-f="Swissmedic">Swissmedic</span>
      <span class="count" id="count"></span>
    </div>
    <div class="list" id="list"></div>
  </section>

  <section>
    <h2>Excipients, antiseptics &amp; reagents (not repurposing candidates)</h2>
    <div class="verdict" style="border-left-color:#9aa7b1">These <span id="unnamed-n"></span> substances are approved abroad and absent from the US drug record too, but they have no INN or USAN — overwhelmingly excipients, antiseptics, sunscreen filters, reagents and veterinary-only actives. Listed for completeness; not drug-repurposing candidates.</div>
    <details class="caveats"><summary>Show the excipient/reagent list</summary><div class="list" id="unnamed-list" style="margin:10px 0 16px"></div></details>
  </section>

  <section>
    <h2>Known limitations — read before acting</h2>
    <details class="caveats" open>
      <summary>Four residual error classes</summary>
      <ul>
        <li><b>US exclusion set is NDA-based.</b> Drugs@FDA + Orange Book exclude OTC-monograph, pre-1938 and DESI-withdrawn drugs, so a monograph-only moiety (e.g. aspirin) can appear as a false candidate. This also intersects the <i>Sun Pharma</i> pre-1962 carve-out population — treat these as “investigate,” not “discard.”</li>
        <li><b>Prodrugs can leak.</b> Salt/base forms collapse correctly, but a prodrug whose active moiety is US-approved under a different parent (isavuconazole vs US-approved isavuconazonium) is not caught without the GSRS active-moiety graph.</li>
        <li><b>EMA is centralised-only.</b> Nationally-authorised EU drugs are absent, so a “never-US” call may in fact be approved via an individual EU member state.</li>
        <li><b>Japan is under-covered.</b> Only PMDA FY2025 loads and katakana names mostly fail to resolve without a transliteration layer — the highest-yield source is the least complete here.</li>
      </ul>
    </details>
  </section>

  <footer>This is a screening list, not a clearance. The § 360ff(a)(3) rare-pediatric gate, freedom-to-operate, and orphan-exclusivity conflict checks are downstream of this diff. Generated by <code>pipeline/build_ui.py</code>.</footer>
</div>

<script>
const DATA = __DATA__;

const titleCase = s => s.toLowerCase().replace(/\b([a-z])/g,(m,c)=>c.toUpperCase());
const el = (t,c,txt)=>{const e=document.createElement(t);if(c)e.className=c;if(txt!=null)e.textContent=txt;return e;};

// meta + verdict
document.getElementById('meta').textContent =
  `Generated ${DATA.generated} · data snapshot: ${DATA.snapshot}`;
document.getElementById('verdict').innerHTML =
  `<b>${DATA.counts.named} named-drug candidates</b> survive the "never approved in the US" test, `+
  `<b>${DATA.counts.orphan} already flagged orphan</b> by a foreign regulator. Read this as a shortlist to review — `+
  `not ${DATA.counts.named} businesses. The feasibility analysis projects roughly <b>~7 truly actionable programs</b> `+
  `once the rare-pediatric, freedom-to-operate and orphan-exclusivity filters (downstream of this diff) are applied.`;

// stat cards
const F=DATA.funnel, C=DATA.counts;
[['accent',C.named,'named-drug candidates'],
 ['gold',C.orphan,'orphan-flagged (priority)'],
 ['','',''],['','','']].slice(0,0); // noop
const cards=[
  ['accent',C.named,'never-US named candidates'],
  ['gold',C.orphan,'orphan-flagged'],
  ['',C.inn,'INN-designated'],
  ['',F.foreign_rows.toLocaleString(),'foreign rows screened'],
];
const cwrap=document.getElementById('cards');
cards.forEach(([cls,n,l])=>{const c=el('div','card '+cls);c.appendChild(el('div','n',n));c.appendChild(el('div','l',l));cwrap.appendChild(c);});

// funnel
const stages=[
  ['dim', F.foreign_rows, 'Foreign approval rows ingested (EMA, Canada, Swissmedic, Japan)'],
  ['dim', F.resolved, 'Resolved to an FDA UNII'],
  ['', F.resolved - F.in_us, 'Moiety not found in the US approval record'],
  ['', F.candidate_small_mol, 'Small-molecule (biologics/vaccines removed)'],
  ['', F.named_drug, 'Named drug — has an INN or USAN'],
  ['win', C.orphan, 'Already flagged orphan by a foreign regulator'],
];
const max=F.foreign_rows, fw=document.getElementById('funnel');
stages.forEach(([cls,n,lab])=>{
  const row=el('div','frow '+cls);
  const bar=el('div','bar', n.toLocaleString());
  bar.style.width=Math.max(4, Math.round(n/max*70))+'%';
  const l=el('div','lab'); l.innerHTML=lab;
  row.appendChild(bar); row.appendChild(l); fw.appendChild(row);
});

// candidate rendering
function lookupLinks(c){
  const q=encodeURIComponent(c.name);
  return [
    ['EMA', `https://www.ema.europa.eu/en/search?search_api_fulltext=${q}`],
    ['PubMed', `https://pubmed.ncbi.nlm.nih.gov/?term=${q}`],
    ['FDA GSRS', `https://gsrs.ncats.nih.gov/ginas/app/beta/substances/${c.unii}`],
  ];
}
function itemNode(c){
  const it=el('div','item'+(c.orphan?' orphan':''));
  const left=el('div');
  left.appendChild(el('div','name', titleCase(c.name)));
  left.appendChild(el('div','sub', `UNII ${c.unii}`));
  const b=el('div','badges');
  if(c.orphan) b.appendChild(el('span','b orphan','★ Orphan'));
  if(c.inn) b.appendChild(el('span','b inn','INN'));
  if(c.usan) b.appendChild(el('span','b usan','USAN'));
  c.sources.forEach(s=>b.appendChild(el('span','b src',s)));
  b.appendChild(el('span','b tier',c.tier));
  left.appendChild(b);
  it.appendChild(left);
  const links=el('div','links');
  lookupLinks(c).forEach(([t,u])=>{const a=el('a',null,t);a.href=u;a.target='_blank';a.rel='noopener';links.appendChild(a);});
  it.appendChild(links);
  return it;
}

// filters
let filters={orphan:false,inn:false,EMA:false,'Health Canada':false,Swissmedic:false};
let query='';
const list=document.getElementById('list'), count=document.getElementById('count');
function render(){
  const srcFilters=['EMA','Health Canada','Swissmedic'].filter(s=>filters[s]);
  const rows=DATA.candidates.filter(c=>{
    if(filters.orphan && !c.orphan) return false;
    if(filters.inn && !c.inn) return false;
    if(srcFilters.length && !srcFilters.some(s=>c.sources.includes(s))) return false;
    if(query && !c.name.toLowerCase().includes(query)) return false;
    return true;
  });
  list.innerHTML='';
  if(!rows.length){list.appendChild(el('div','empty','No candidates match those filters.'));}
  else rows.forEach(c=>list.appendChild(itemNode(c)));
  count.textContent=`${rows.length} of ${DATA.candidates.length} shown`;
}
document.querySelectorAll('.chip').forEach(chip=>{
  chip.addEventListener('click',()=>{const f=chip.dataset.f;filters[f]=!filters[f];chip.classList.toggle('on');render();});
});
document.getElementById('search').addEventListener('input',e=>{query=e.target.value.trim().toLowerCase();render();});
render();

// unnamed appendix
document.getElementById('unnamed-n').textContent=DATA.unnamed.length;
const ul=document.getElementById('unnamed-list');
DATA.unnamed.forEach(c=>ul.appendChild(itemNode(c)));
</script>
</body>
</html>
"""


def main():
    with open(SUMMARY, encoding="utf-8") as fh:
        data = json.load(fh)
    os.makedirs(OUT_DIR, exist_ok=True)
    html_out = TEMPLATE.replace("__DATA__", json.dumps(data))
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(html_out)
    print(f"wrote {OUT}  ({len(html_out)//1024} KB, {len(data['candidates'])} candidates)")


if __name__ == "__main__":
    main()
