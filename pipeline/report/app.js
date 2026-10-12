/* ============================================================
   STATE OF BIO 2026 — app.js
   Design adapted from a data-almanac template. Charts labelled
   "RDH pipeline" / "SEC 8-K" are driven by real data in data.js
   (window.BIO); "Illustrative" charts use seeded synthetic data
   for the design only.
   ============================================================ */

"use strict";

const BIO = window.BIO || {};

/* ---------------- seeded PRNG ---------------- */
function mulberry32(seed) {
  let a = seed >>> 0;
  return function () {
    a |= 0; a = (a + 0x6D2B79F5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/* ---------------- shared helpers ---------------- */
const tooltip = document.getElementById("tooltip");
function showTip(html, x, y) {
  tooltip.innerHTML = html;
  tooltip.classList.add("show");
  const pad = 16;
  const w = tooltip.offsetWidth, h = tooltip.offsetHeight;
  let left = x + pad, top = y - h - pad;
  if (left + w > innerWidth - 8) left = x - w - pad;
  if (top < 8) top = y + pad;
  tooltip.style.left = left + "px";
  tooltip.style.top = top + "px";
}
function hideTip() { tooltip.classList.remove("show"); }

const toast = document.getElementById("toast");
let toastTimer = null;
function showToast(msg) {
  toast.textContent = msg;
  toast.classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove("show"), 2400);
}

document.querySelectorAll(".share-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    const label = btn.dataset.share || "chart";
    const url = location.origin + location.pathname + "#" + (btn.closest("section")?.id || "");
    if (navigator.clipboard) navigator.clipboard.writeText(url).catch(() => {});
    showToast(`Link to "${label}" copied`);
  });
});

document.getElementById("tickerInfo").addEventListener("click", () =>
  showToast("Pipeline figures are live RareDiseaseHedge output; voucher prices are SEC-disclosed.")
);

const fmtM = v => v >= 1000 ? "$" + (v / 1000).toFixed(2) + "B" : "$" + Math.round(v) + "M";
const fmtCount = v =>
  v >= 1e6 ? (v / 1e6).toFixed(1) + "M" :
  v >= 1e3 ? (v / 1e3).toFixed(1) + "K" : String(Math.round(v));

/* ============================================================
   TICKER — real headline metrics from the pipeline + SEC data
   ============================================================ */
{
  const h = BIO.headline || {};
  const items = [
    ["Candidates (never-US)", h.candidates, ""],
    ["Multi-regulator", h.multi_regulator, ""],
    ["EU orphan-flagged", h.orphan, ""],
    ["Dossier-only leads", h.dossier_only, ""],
    [h.prv_high_status === "agreement" ? "Top recent voucher (signed, not closed)" : "Top recent voucher",
     h.prv_high != null ? "$" + h.prv_high + "M" : "", ""],
    ["Record sale", h.peak != null ? "$" + h.peak + "M" : "", ""],
    ["Vouchers sold", h.deals, ""],
    ["Months to sunset", h.months_to_sunset, ""],
    ["Foreign approvals scanned", h.foreign_rows != null ? fmtCount(h.foreign_rows) : "", ""],
  ].filter(it => it[1] !== undefined && it[1] !== "");
  const track = document.getElementById("tickerTrack");
  // No sparklines / trend arrows: these are point-in-time metrics and a
  // seeded random polyline next to a real number implies a trend no data supports.
  const html = items.map(([label, val]) =>
    `<span class="tick">${label}
      <span class="delta">${val}</span></span>`).join("");
  track.innerHTML = html + html;
}

/* ============================================================
   HERO — scroll-driven pixel dissolve (unchanged machinery)
   ============================================================ */
const heroMosaic = document.getElementById("heroMosaic");
const heroScrollEl = document.querySelector(".hero-scroll");
const heroTitleEl = document.querySelector(".hero-title");
const heroSubEl = document.querySelector(".hero-sub");
const heroHintEl = document.getElementById("heroHint");
const MOSAIC_COLORS = ["#9a7cf5", "#7fd6e3", "#8f6ff0", "#6fc9d6", "#a98cf7"];
let heroBlocks = [];

function buildMosaic() {
  const stage = heroMosaic.parentElement;
  const W = stage.clientWidth, H = stage.clientHeight;
  const size = W < 640 ? 30 : 46;
  const cols = Math.ceil(W / size), rows = Math.ceil(H / size);
  const rnd = mulberry32(20260831);
  const frag = document.createDocumentFragment();
  heroBlocks = [];
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const el = document.createElement("div");
      el.className = "px";
      el.style.cssText =
        `left:${c * size}px;top:${r * size}px;width:${size + 1}px;height:${size + 1}px;` +
        `background:${MOSAIC_COLORS[(rnd() * MOSAIC_COLORS.length) | 0]}`;
      heroBlocks.push({ el, t: rnd() * 0.82, on: false });
      frag.appendChild(el);
    }
  }
  heroMosaic.innerHTML = "";
  heroMosaic.appendChild(frag);
}

let heroTicking = false;
function heroScrollUpdate() {
  heroTicking = false;
  const dist = heroScrollEl.offsetHeight - innerHeight;
  const p = dist > 0 ? Math.min(1, Math.max(0, scrollY / dist)) : 0;
  for (const b of heroBlocks) {
    const should = p > b.t;
    if (should !== b.on) { b.on = should; b.el.classList.toggle("on", should); }
  }
  if (heroTitleEl) heroTitleEl.style.transform = `translateY(${-p * 46}px)`;
  if (heroSubEl) heroSubEl.style.opacity = String(Math.max(0, 1 - p * 1.9));
  if (heroHintEl) heroHintEl.style.opacity = String(Math.max(0, 0.5 - p * 1.6));
}
addEventListener("scroll", () => {
  if (!heroTicking) { heroTicking = true; requestAnimationFrame(heroScrollUpdate); }
}, { passive: true });
buildMosaic();
heroScrollUpdate();

/* ============================================================
   SHORTLIST — searchable candidate list (RDH pipeline)
   ============================================================ */
const SL = {
  q: "", sort: "reach",
  filters: { orphan: false, multi: false, rare: false, ped: false, pulled: false },
};
const SL_CHIPS = [
  ["euorphan", "EU orphan designation", c => c.eu_orphan],
  ["multi", "Multi-regulator", c => (c.sources || []).length > 1],
  ["rare", "Rare (Orphanet)", c => c.orpha && c.orpha.rarity === "rare"],
  ["ped", "Pediatric onset", c => c.orpha && c.orpha.onset === "pediatric"],
  ["nocrl", "No US CRL record", c => !c.crl],
  ["pulled", "Licence pulled", c => c.fs === "previously_authorised"],
];
function slPredicate(key) { return SL_CHIPS.find(x => x[0] === key)[2]; }

function slFiltered() {
  const cands = BIO.candidates || [];
  const q = SL.q.trim().toLowerCase();
  let out = cands.filter(c => {
    for (const k in SL.filters) if (SL.filters[k] && !slPredicate(k)(c)) return false;
    if (!q) return true;
    return [c.name, c.moiety, c.area, c.ind, c.atc, c.disease, c.orpha && c.orpha.disease,
            (c.chembl || []).join(" "), (c.sources || []).join(" ")].some(s => (s || "").toLowerCase().includes(q));
  });
  const research = c => (c.pubmed || 0) + (c.trials || 0);
  out.sort(SL.sort === "name" ? (a, b) => a.name.localeCompare(b.name)
    : SL.sort === "research" ? (a, b) => research(b) - research(a)
    : (a, b) => (b.nc - a.nc) || a.name.localeCompare(b.name));
  return out;
}

function slCard(c) {
  const badges = [];
  if (c.orphan) badges.push('<span class="badge badge-orphan">orphan</span>');
  if (c.orpha && c.orpha.rarity === "rare") badges.push('<span class="badge badge-rare">rare disease</span>');
  if (c.orpha && c.orpha.onset === "pediatric") badges.push('<span class="badge badge-ped">pediatric onset</span>');
  if (c.eu_orphan) badges.push('<span class="badge badge-orphan">EU orphan designation</span>');
  if (c.crl) badges.push('<span class="badge badge-crl">US filed &amp; refused</span>');
  if ((c.sources || []).length > 1) badges.push('<span class="badge badge-multi">multi-regulator</span>');
  if (c.fs === "previously_authorised") badges.push('<span class="badge badge-pulled">licence pulled</span>');
  const dz = (c.orpha && c.orpha.disease) || c.area || c.disease || (c.ind || "").replace(/\.$/, "") || "—";
  const src = (c.sources || []).map(s => s.replace("EU national (Art57)", "EEA national").replace(" (Art57)", ""))
    .map(s => `<span class="badge badge-src">${s}</span>`).join("");
  return `<div class="sl-card" data-name="${c.name.replace(/"/g, "&quot;")}" tabindex="0" role="button">
    <div class="sl-card-top"><span class="sl-name">${c.name}</span>
      <span class="sl-reach"><b>${c.nc || 0}</b> EEA</span></div>
    <div class="sl-dz">${dz.length > 96 ? dz.slice(0, 96) + "…" : dz}</div>
    <div class="sl-badges">${badges.join("")}</div>
    <div class="sl-badges">${src}</div>
    <div class="sl-foot"><span>papers <b>${c.pubmed != null ? c.pubmed : "—"}</b></span>
      <span>trials <b>${c.trials != null ? c.trials : "—"}</b></span>
      ${c.atc ? `<span>ATC <b>${c.atc}</b></span>` : ""}</div>
  </div>`;
}

function slRender() {
  const rows = slFiltered();
  const listEl = document.getElementById("slList");
  const total = (BIO.candidates || []).length;
  document.getElementById("slCount").textContent = total;
  document.getElementById("slStatus").textContent =
    `Showing ${rows.length} of ${total} candidates` + (SL.q ? ` matching “${SL.q}”` : "");
  listEl.innerHTML = rows.length
    ? rows.map(slCard).join("")
    : `<p class="sl-empty">No candidates match. Try a drug name, a disease, or clear the filters.</p>`;
}

/* ---------- candidate detail panel (was the #1 UX gap: cards did nothing) ---------- */
const ST = { PASS: ["✓", "st-pass"], FAIL: ["✕", "st-fail"], HUMAN: ["?", "st-human"], UNKNOWN: ["–", "st-unknown"] };
function slPanel(c) {
  const wrap = document.getElementById("slPanel");
  const badge = (t, cls) => `<span class="badge ${cls}">${t}</span>`;
  const badges = [];
  if (c.orphan) badges.push(badge("orphan", "badge-orphan"));
  if (c.eu_orphan) badges.push(badge("EU orphan designation", "badge-orphan"));
  if (c.orpha && c.orpha.rarity === "rare") badges.push(badge("rare disease", "badge-rare"));
  if (c.orpha && c.orpha.onset === "pediatric") badges.push(badge("pediatric onset", "badge-ped"));
  if (c.crl) badges.push(badge("US filed &amp; refused", "badge-crl"));
  if (c.fs === "previously_authorised") badges.push(badge("licence pulled", "badge-pulled"));
  const elig = c.elig ? c.elig.criteria.map(cr => {
    const [g, cls] = ST[cr.status] || ST.UNKNOWN;
    return `<div class="pc-crit"><span class="pc-st ${cls}">${g}</span>
      <div><div class="pc-k">${cr.key.replace(/_/g, " ")}</div>
      <div class="pc-note">${cr.note} <span class="pc-cite">${cr.citation}</span></div></div></div>`;
  }).join("") : "<p>No assessment.</p>";
  const rows = [
    ["Disease", (c.orpha && c.orpha.disease) || c.area || c.disease || "—"],
    ["Approved in", (c.sources || []).join(", ").replace("EU national (Art57)", "EEA (Article 57)")],
    ["EEA countries", (c.nc || 0) + (c.countries && c.countries.length ? " — " + c.countries.slice(0, 12).join(", ") : "")],
    ["Regulatory standing", (c.fs || "—").replace(/_/g, " ")],
    ["Orphanet prevalence", c.orpha ? (c.orpha.rarity + (c.orpha.prev ? " · ~" + c.orpha.prev.toLocaleString() + " in US" : "")) : "no Orphanet match"],
    ["EU orphan designation", c.eu_orphan ? (c.eu_orphan.status + " — " + c.eu_orphan.use) : "—"],
    ["US CRL / prior filing", c.crl ? ((c.crl.kind && c.crl.kind !== "COMPLETE RESPONSE" ? c.crl.kind + ": " : "") + (c.crl.application || "") + " · " + (c.crl.date || "")) : "no CRL record found (openFDA set covers 2024+ letters; older refusals are hand-curated)"],
    ["ChEMBL indications", (c.chembl || []).join("; ") || "—"],
    ["ATC", c.atc || "—"],
    ["Research", "PubMed " + (c.pubmed != null ? c.pubmed : "—") + " · trials " + (c.trials != null ? c.trials : "—")],
  ];
  const q = encodeURIComponent(c.name);
  wrap.innerHTML = `
    <div class="pc-inner" role="dialog" aria-label="${c.name} detail">
      <button class="pc-close" id="pcClose" aria-label="Close">✕</button>
      <div class="pc-name">${c.name}</div>
      <div class="pc-verdict">${c.elig ? c.elig.verdict.replace(/_/g, " ").toLowerCase() : ""}</div>
      <div class="pc-badges">${badges.join("")}</div>
      <div class="pc-sec">s.529 eligibility — what's settled and what a human must decide</div>
      <div class="pc-crits">${elig}</div>
      <div class="pc-sec">Facts &amp; signals</div>
      ${rows.map(([k, v]) => `<div class="pc-row"><span>${k}</span><div>${v}</div></div>`).join("")}
      <div class="pc-sec">Look it up</div>
      <div class="pc-links">
        <a target="_blank" rel="noopener" href="https://www.ebi.ac.uk/chembl/g/#search_results/all/query=${q}">ChEMBL</a>
        <a target="_blank" rel="noopener" href="https://www.orpha.net/en/disease/search?query=${q}">Orphanet</a>
        <a target="_blank" rel="noopener" href="https://pubmed.ncbi.nlm.nih.gov/?term=${q}">PubMed</a>
        <a target="_blank" rel="noopener" href="https://clinicaltrials.gov/search?intr=${q}">ClinicalTrials</a>
      </div>
      <p class="pc-disc">A screening record, not a clearance. "Likely eligible pending review" means no criterion has ruled it out — the HUMAN/UNKNOWN rows above still require diligence and, ultimately, FDA.</p>
    </div>`;
  wrap.classList.add("open");
  document.getElementById("pcClose").onclick = slClosePanel;
}
function slClosePanel() { document.getElementById("slPanel").classList.remove("open"); }

function slInit() {
  const chipHost = document.getElementById("slChips");
  chipHost.innerHTML = SL_CHIPS.map(([key, label, pred]) => {
    const n = (BIO.candidates || []).filter(pred).length;
    return `<button class="sl-chip" data-k="${key}">${label}<span class="n">${n}</span></button>`;
  }).join("");
  chipHost.querySelectorAll(".sl-chip").forEach(btn => btn.addEventListener("click", () => {
    const k = btn.dataset.k;
    SL.filters[k] = !SL.filters[k];
    btn.classList.toggle("on", SL.filters[k]);
    slRender();
  }));
  const inp = document.getElementById("slSearch");
  let t = null;
  inp.addEventListener("input", () => { clearTimeout(t); t = setTimeout(() => { SL.q = inp.value; slRender(); }, 120); });
  document.getElementById("slSort").addEventListener("change", e => { SL.sort = e.target.value; slRender(); });
  // data-freshness line (the site never surfaced the snapshot before)
  const fresh = document.getElementById("slFresh");
  if (fresh) fresh.textContent = "Pipeline data generated " + (BIO.generated || "—") +
    (BIO.snapshot ? " · snapshot: " + BIO.snapshot : "");
  const built = document.querySelector(".footer-built");
  if (built && BIO.generated) built.textContent = "Data as of " + BIO.generated + " · built with D3";
  // open the detail panel on card click / Enter (event delegation)
  const byName = {}; (BIO.candidates || []).forEach(c => (byName[c.name] = c));
  const listEl = document.getElementById("slList");
  const openCard = el => { const card = el.closest(".sl-card"); if (card && byName[card.dataset.name]) slPanel(byName[card.dataset.name]); };
  listEl.addEventListener("click", e => openCard(e.target));
  listEl.addEventListener("keydown", e => { if (e.key === "Enter") openCard(e.target); });
  const panel = document.getElementById("slPanel");
  panel.addEventListener("click", e => { if (e.target === panel) slClosePanel(); });
  addEventListener("keydown", e => { if (e.key === "Escape") slClosePanel(); });
  slRender();
}
slInit();

/* ============================================================
   VOUCHER MARKET — real PRV sales (SEC 8-K)
   Primary: annual $ disclosed, stacked by voucher type.
   Secondary: cumulative disclosed value.
   Tabs filter which voucher types are included.
   ============================================================ */
const VTYPE = {
  RPD: { label: "Rare pediatric", color: "#16213e" },
  TD:  { label: "Tropical",       color: "#23c0d8" },
  MCM: { label: "Countermeasure", color: "#e8961e" },
};
const ECO_VIEWS = [
  { key: "all", tab: "All vouchers", types: ["RPD", "TD", "MCM"] },
  { key: "rpd", tab: "Rare pediatric", types: ["RPD"] },
  { key: "trop", tab: "Tropical", types: ["TD"] },
  { key: "mcm", tab: "Countermeasure", types: ["MCM"] },
];
const eco = { current: "all", legendEl: document.getElementById("ecoLegend"),
              host: document.getElementById("ecoChart") };

function ecoTypes() { return (ECO_VIEWS.find(v => v.key === eco.current) || ECO_VIEWS[0]).types; }

function syncEcoText() {
  const v = ECO_VIEWS.find(x => x.key === eco.current) || ECO_VIEWS[0];
  document.getElementById("ecoTitle").textContent =
    v.key === "all" ? "PRV SALES BY YEAR" : v.tab.toUpperCase() + " VOUCHER SALES";
  document.getElementById("ecoBarMethod").innerHTML =
    "<strong>Methodology:</strong> Each bar is the total disclosed sale value of Priority Review Vouchers sold that year, from SEC 8-K filings or the seller's own disclosure (2014–2026), stacked by voucher type. 2026 includes signed agreements not yet confirmed closed (SEZABY, GENGLYCOS). Undisclosed deals are excluded, so totals are a floor.";
  document.getElementById("ecoMethod").innerHTML =
    "<strong>Methodology:</strong> Cumulative disclosed PRV sale value across all tracked deals; the same series as the bars above, summed forward.";
}

function buildTabs() {
  const holder = document.getElementById("metricTabs");
  ECO_VIEWS.forEach((v, i) => {
    const b = document.createElement("button");
    b.className = "mtab" + (v.key === eco.current ? " active" : "");
    b.setAttribute("role", "tab");
    b.textContent = v.tab;
    b.addEventListener("click", () => {
      eco.current = v.key;
      holder.querySelectorAll(".mtab").forEach(x => x.classList.remove("active"));
      b.classList.add("active");
      syncEcoText(); drawEcoBars(true); drawEco(true);
    });
    holder.appendChild(b);
    if (i < ECO_VIEWS.length - 1) {
      const s = document.createElement("span");
      s.className = "tab-sep"; s.textContent = "/";
      holder.appendChild(s);
    }
  });
  syncEcoText();
}

function drawEcoBars(animate) {
  const rows = BIO.prvByYear || [];
  const types = ecoTypes();
  const host = document.getElementById("ecoBarChart");
  const W = host.clientWidth, H = Math.max(470, host.clientHeight);
  const M = { top: 18, right: 16, bottom: 46, left: 62 };
  host.innerHTML = "";
  const svg = d3.select(host).append("svg").attr("width", W).attr("height", H);

  const stacked = d3.stack().keys(types)(rows);
  const x = d3.scaleBand().domain(rows.map(r => r.year)).range([M.left, W - M.right]).padding(0.28);
  const yMax = d3.max(rows, r => d3.sum(types, t => r[t] || 0)) || 1;
  const y = d3.scaleLinear().domain([0, yMax * 1.08]).range([H - M.bottom, M.top]);

  svg.append("g").selectAll("line").data(y.ticks(6)).join("line")
    .attr("class", "gridline").attr("x1", M.left).attr("x2", W - M.right)
    .attr("y1", d => y(d)).attr("y2", d => y(d));
  svg.append("g").attr("class", "axis").attr("transform", `translate(${M.left},0)`)
    .call(d3.axisLeft(y).ticks(6).tickFormat(fmtM).tickSize(0).tickPadding(10))
    .call(g => g.select(".domain").remove());
  svg.append("g").attr("class", "axis").attr("transform", `translate(0,${H - M.bottom})`)
    .call(d3.axisBottom(x).tickFormat(d3.format("d")).tickSizeOuter(0));

  const clip = svg.append("clipPath").attr("id", "ecoBarClip").append("rect")
    .attr("x", M.left).attr("width", W - M.left - M.right)
    .attr("y", animate ? H - M.bottom : M.top)
    .attr("height", animate ? 0 : H - M.top - M.bottom);
  const root = svg.append("g").attr("clip-path", "url(#ecoBarClip)");
  root.selectAll("g.layer").data(stacked).join("g")
    .attr("fill", d => VTYPE[d.key].color)
    .selectAll("rect").data(d => d.map(v => ({ v, key: d.key }))).join("rect")
    .attr("x", d => x(d.v.data.year)).attr("width", x.bandwidth())
    .attr("y", d => y(d.v[1])).attr("height", d => Math.max(0, y(d.v[0]) - y(d.v[1])))
    .attr("rx", 2)
    .on("mousemove", (ev, d) => {
      const r = d.v.data;
      const total = types.reduce((s, t) => s + (r[t] || 0), 0);
      const lines = types.filter(t => r[t]).map(t =>
        `<div><span style="color:${VTYPE[t].color}">■</span> ${VTYPE[t].label}&nbsp; $${r[t]}M</div>`).join("");
      showTip(`<div class="tt-title">${r.year} · $${Math.round(total)}M disclosed</div>${lines}`, ev.clientX, ev.clientY);
    })
    .on("mouseleave", hideTip);
  if (animate) clip.transition().duration(720).ease(d3.easeCubicOut)
    .attr("y", M.top).attr("height", H - M.top - M.bottom);

  const legendEl = document.getElementById("ecoBarLegend");
  legendEl.innerHTML = types.map(t => {
    const sum = rows.reduce((s, r) => s + (r[t] || 0), 0);
    return `<div class="legend-item"><span class="swatch" style="background:${VTYPE[t].color}"></span>${VTYPE[t].label}<span class="pct">$${Math.round(sum)}M</span></div>`;
  }).join("");
}

function drawEco(animate) {
  const rows = BIO.prvByYear || [];
  const types = ecoTypes();
  let cum = 0;
  const data = rows.map(r => { cum += types.reduce((s, t) => s + (r[t] || 0), 0); return { year: r.year, v: cum }; });

  const W = eco.host.clientWidth, H = Math.max(360, eco.host.clientHeight);
  const M = { top: 16, right: 18, bottom: 42, left: 62 };
  eco.host.innerHTML = "";
  const svg = d3.select(eco.host).append("svg").attr("width", W).attr("height", H);
  const x = d3.scalePoint().domain(data.map(d => d.year)).range([M.left, W - M.right]);
  const y = d3.scaleLinear().domain([0, (d3.max(data, d => d.v) || 1) * 1.06]).range([H - M.bottom, M.top]);

  svg.append("g").selectAll("line").data(y.ticks(6)).join("line")
    .attr("class", "gridline").attr("x1", M.left).attr("x2", W - M.right)
    .attr("y1", d => y(d)).attr("y2", d => y(d));
  svg.append("g").attr("class", "axis").attr("transform", `translate(0,${H - M.bottom})`)
    .call(d3.axisBottom(x).tickFormat(d3.format("d")).tickSizeOuter(0));
  svg.append("g").attr("class", "axis").attr("transform", `translate(${M.left},0)`)
    .call(d3.axisLeft(y).ticks(6).tickFormat(fmtM).tickSize(0).tickPadding(10))
    .call(g => g.select(".domain").remove());

  const area = d3.area().x(d => x(d.year)).y0(H - M.bottom).y1(d => y(d.v)).curve(d3.curveMonotoneX);
  const areaFlat = d3.area().x(d => x(d.year)).y0(H - M.bottom).y1(H - M.bottom).curve(d3.curveMonotoneX);
  const line = d3.line().x(d => x(d.year)).y(d => y(d.v)).curve(d3.curveMonotoneX);
  const p = svg.append("path").datum(data).attr("fill", "#93dce6").attr("opacity", 0.55)
    .attr("d", animate ? areaFlat : area);
  if (animate) p.transition().duration(750).ease(d3.easeCubicOut).attr("d", area);
  svg.append("path").datum(data).attr("fill", "none").attr("stroke", "#16213e")
    .attr("stroke-width", 2).attr("d", line).attr("opacity", animate ? 0 : 1)
    .transition().delay(animate ? 400 : 0).duration(400).attr("opacity", 1);

  const last = data[data.length - 1];
  eco.legendEl.innerHTML = `<div class="legend-item"><span class="swatch" style="background:#93dce6"></span>Cumulative<span class="pct">${fmtM(last ? last.v : 0)}</span></div>`;
}

/* ============================================================
   PIPELINE BREADTH — real histogram (RDH pipeline)
   ============================================================ */
function drawWallets() {
  const host = document.getElementById("walletChart");
  const rows = BIO.breadthHist || [];
  const W = host.clientWidth, H = Math.max(420, host.clientHeight);
  const M = { top: 16, right: 14, bottom: 52, left: 56 };
  host.innerHTML = "";
  const svg = d3.select(host).append("svg").attr("width", W).attr("height", H);
  const x = d3.scaleBand().domain(rows.map(r => r.label)).range([M.left, W - M.right]).padding(0.24);
  const y = d3.scaleLinear().domain([0, (d3.max(rows, r => r.n) || 1) * 1.1]).range([H - M.bottom, M.top]);

  svg.append("g").selectAll("line").data(y.ticks(5)).join("line")
    .attr("class", "gridline").attr("x1", M.left).attr("x2", W - M.right)
    .attr("y1", d => y(d)).attr("y2", d => y(d));
  svg.append("g").attr("class", "axis").attr("transform", `translate(${M.left},0)`)
    .call(d3.axisLeft(y).ticks(5).tickSize(0).tickPadding(10))
    .call(g => g.select(".domain").remove());
  svg.append("g").attr("class", "axis").attr("transform", `translate(0,${H - M.bottom})`)
    .call(d3.axisBottom(x).tickSizeOuter(0));
  svg.append("text").attr("x", M.left).attr("y", H - 8)
    .style("font-family", "var(--font-mono)").style("font-size", "11px").style("fill", "#7d786c")
    .text("EEA countries where the candidate is authorised");

  svg.append("g").selectAll("rect").data(rows).join("rect")
    .attr("x", d => x(d.label)).attr("width", x.bandwidth())
    .attr("y", H - M.bottom).attr("height", 0)
    .attr("fill", "#16213e").attr("rx", 3)
    .on("mousemove", (ev, d) => {
      showTip(`<div class="tt-title">${d.label} countries</div>${d.n} candidate drugs`, ev.clientX, ev.clientY);
      d3.select(ev.currentTarget).attr("fill", "#5b6ee1");
    })
    .on("mouseleave", ev => { hideTip(); d3.select(ev.currentTarget).attr("fill", "#16213e"); })
    .transition().duration(600).delay((d, i) => i * 70).ease(d3.easeCubicOut)
    .attr("y", d => y(d.n)).attr("height", d => H - M.bottom - y(d.n));
}

/* ============================================================
   CANDIDATES — real bubbles (RDH pipeline)
   ============================================================ */
const BUBBLE_PALETTE = [
  "#2f6df6", "#8a4fe0", "#1f9d57", "#f2765a", "#e0189a", "#e8961e",
  "#23c0d8", "#b3232b", "#9acd32", "#3d6b99", "#c94f7c", "#5f8575",
  "#7c5cd6", "#2d9d9a", "#d4772b",
];
function drawBubbles() {
  const host = document.getElementById("bubbleChart");
  const W = host.clientWidth, H = Math.max(560, host.clientHeight);
  host.innerHTML = "";
  const svg = d3.select(host).append("svg").attr("width", W).attr("height", H);

  const nodes = (BIO.bubbles || []).map((b, i) => ({
    name: b.name, v: Math.max(1, b.v), orphan: b.orphan, area: b.area,
    color: BUBBLE_PALETTE[i % BUBBLE_PALETTE.length], i,
  }));
  if (!nodes.length) return;
  const maxV = d3.max(nodes, d => d.v);
  const kR = Math.min(104, H / 5) / Math.sqrt(maxV);
  nodes.forEach(d => (d.r = Math.max(10, kR * Math.sqrt(d.v))));

  const frac = x => x - Math.floor(x);
  nodes.forEach(d => (d.sortKey = frac(Math.sin(d.i * 12.9898) * 43758.5453)));
  const ordered = [...nodes].sort((a, b) => a.sortKey - b.sortKey);
  const m = 96;
  ordered.forEach((d, idx) => (d.tx = m + (idx / Math.max(1, ordered.length - 1)) * (W - 2 * m)));

  const sim = d3.forceSimulation(nodes)
    .force("x", d3.forceX(d => d.tx).strength(0.26))
    .force("y", d3.forceY(H / 2).strength(0.09))
    .force("collide", d3.forceCollide(d => d.r + 2.5).strength(1))
    .force("charge", d3.forceManyBody().strength(2.5))
    .stop();
  for (let t = 0; t < 340; t++) sim.tick();
  nodes.forEach(d => {
    d.x = Math.max(d.r + 4, Math.min(W - d.r - 4, d.x));
    d.y = Math.max(d.r + 4, Math.min(H - d.r - 4, d.y));
  });

  const g = svg.selectAll("g").data(nodes).join("g").attr("transform", d => `translate(${d.x},${d.y})`);
  g.append("circle").attr("fill", d => d.color).attr("opacity", 0.95).attr("r", 0)
    .attr("stroke", d => d.orphan ? "#f6c700" : "none").attr("stroke-width", d => d.orphan ? 3 : 0)
    .style("cursor", "pointer")
    .on("mousemove", (ev, d) => showTip(
      `<div class="tt-title">${d.name}</div>${d.v} EEA countr${d.v === 1 ? "y" : "ies"}` +
      (d.orphan ? " · EU orphan" : "") + (d.area ? `<div style="opacity:.6;margin-top:4px">${d.area}</div>` : ""),
      ev.clientX, ev.clientY))
    .on("mouseleave", hideTip)
    .transition().duration(680).delay((d, i) => i * 16).ease(d3.easeBackOut.overshoot(1.1))
    .attr("r", d => d.r);

  const label = g.filter(d => d.r > 26);
  label.append("text").attr("text-anchor", "middle").attr("dy", "-0.15em")
    .style("font-family", "var(--font-kicker)").style("font-weight", "600")
    .style("text-transform", "uppercase").style("letter-spacing", ".02em")
    .style("fill", "#fff").style("pointer-events", "none")
    .style("font-size", d => Math.max(9, Math.min(d.r / 4.2, 16)) + "px")
    .text(d => d.name.length * (d.r / 4.2) * 0.6 > d.r * 1.9 ? d.name.split(" ")[0] : d.name);
  label.append("text").attr("text-anchor", "middle").attr("dy", "1.25em")
    .style("font-family", "var(--font-mono)").style("fill", "rgba(255,255,255,.9)")
    .style("pointer-events", "none").style("font-size", d => Math.max(9, Math.min(d.r / 5.5, 13)) + "px")
    .text(d => d.v);
}

/* ============================================================
   DISEASE AREAS — illustrative sunburst
   ============================================================ */
const CAT_TREE = {
  name: "root",
  children: [
    { name: "Metabolic", color: "#3f4e5a", children: [
      { name: "Lysosomal storage", v: 8 }, { name: "Urea cycle", v: 4 }, { name: "Amino-acid", v: 3 }, { name: "Mitochondrial", v: 3 }, { name: "Glycogen storage", v: 2 }] },
    { name: "Neurology", color: "#a24df0", children: [
      { name: "Epilepsy", v: 6 }, { name: "Leukodystrophy", v: 4 }, { name: "Neuromuscular", v: 4 }, { name: "Movement", v: 2 }] },
    { name: "Oncology", color: "#0a7d3a", children: [
      { name: "Solid tumours", v: 6 }, { name: "Neuroblastoma", v: 3 }, { name: "Glioma", v: 3 }, { name: "Sarcoma", v: 2 }] },
    { name: "Haematology", color: "#4d8df6", children: [
      { name: "Haemoglobinopathy", v: 4 }, { name: "Coagulation", v: 3 }, { name: "Marrow failure", v: 2 }] },
    { name: "Ophthalmology", color: "#21c8dd", children: [
      { name: "Retinal dystrophy", v: 3 }, { name: "Optic atrophy", v: 2 }] },
    { name: "Dermatology", color: "#f0932a", children: [
      { name: "Epidermolysis bullosa", v: 3 }, { name: "Ichthyosis", v: 1 }] },
    { name: "Endocrine", color: "#9aa2ad", children: [
      { name: "Growth", v: 2 }, { name: "Adrenal", v: 2 }, { name: "Thyroid", v: 1 }] },
    { name: "Renal", color: "#ee3d8f", children: [
      { name: "Cystinosis", v: 2 }, { name: "Nephropathy", v: 1 }] },
    { name: "Immunology", color: "#d92d2d", children: [
      { name: "Primary immunodef.", v: 2 }, { name: "Autoinflammatory", v: 1 }] },
    { name: "Cardiology", color: "#f4632e", children: [
      { name: "Cardiomyopathy", v: 2 }, { name: "Amyloidosis", v: 1 }] },
    { name: "Pulmonology", color: "#23c063", children: [
      { name: "Cystic fibrosis", v: 1 }, { name: "PAH", v: 1 }] },
    { name: "Other rare", color: "#17223f", children: [
      { name: "Progeria", v: 1 }, { name: "Menkes", v: 1 }] },
  ],
};

function drawSunburst(year) {
  year = year || +document.getElementById("catYear").value;
  const host = document.getElementById("donutChart");
  const W = host.clientWidth, H = Math.max(560, host.clientHeight);
  const R = Math.min(W, H) / 2 - 12;
  host.innerHTML = "";
  const svg = d3.select(host).append("svg").attr("width", W).attr("height", H)
    .append("g").attr("transform", `translate(${W / 2},${H / 2})`);

  const jit = mulberry32(7100 + year);
  const tree = { name: "root", children: CAT_TREE.children.map(c => ({
    ...c, children: c.children.map(s => ({ ...s, v: s.v * (0.75 + jit() * 0.5) })) })) };
  const root = d3.hierarchy(tree).sum(d => d.v);
  d3.partition().size([2 * Math.PI, 1])(root);
  const grand = root.value;

  const r0 = R * 0.19, r1 = R * 0.63, r2 = R;
  const arc = d3.arc().startAngle(d => d.x0).endAngle(d => d.x1).padAngle(0.004).padRadius(R)
    .innerRadius(d => (d.depth === 1 ? r0 : r1)).outerRadius(d => (d.depth === 1 ? r1 : r2));
  const arcPop = d3.arc().startAngle(d => d.x0).endAngle(d => d.x1).padAngle(0.004).padRadius(R)
    .innerRadius(d => (d.depth === 1 ? r0 : r1)).outerRadius(d => (d.depth === 1 ? r1 + 5 : r2 + 7));
  const fill = d => {
    if (d.depth === 1) return d.data.color;
    const idx = d.parent.children.indexOf(d);
    return d3.color(d.parent.data.color).brighter(0.3 + idx * 0.28).formatHex();
  };
  const nodes = root.descendants().filter(d => d.depth > 0);
  svg.selectAll("path").data(nodes).join("path")
    .attr("fill", fill).attr("stroke", "#fff").attr("stroke-width", d => (d.depth === 1 ? 1.6 : 1))
    .attr("d", arc).attr("opacity", 0).style("cursor", "pointer")
    .on("mousemove", function (ev, d) {
      d3.select(this).attr("d", arcPop(d));
      const overall = (d.value / grand) * 100;
      if (d.depth === 1) showTip(`<div class="tt-title">${d.data.name}</div>${overall.toFixed(1)}% of the illustrative set`, ev.clientX, ev.clientY);
      else showTip(`<div class="tt-title">${d.data.name}</div>${overall.toFixed(1)}% overall · ${((d.value / d.parent.value) * 100).toFixed(0)}% of ${d.parent.data.name}`, ev.clientX, ev.clientY);
    })
    .on("mouseleave", function (ev, d) { d3.select(this).attr("d", arc(d)); hideTip(); })
    .transition().duration(520).delay((d, i) => (d.depth === 1 ? d.parent.children.indexOf(d) * 40 : 260 + i * 6))
    .attr("opacity", d => (d.depth === 1 ? 0.97 : 0.92));

  const DARK_TEXT = new Set(["#21c8dd", "#f0932a", "#9aa2ad", "#23c063"]);
  svg.selectAll("text.arc-label").data(nodes.filter(d => d.depth === 1 && d.x1 - d.x0 > 0.14)).join("text")
    .attr("class", "arc-label")
    .attr("transform", d => {
      const mid = (d.x0 + d.x1) / 2, a = mid * 180 / Math.PI - 90, rr = (r0 + r1) / 2;
      const flip = (a > 90 || a < -90) ? 180 : 0;
      return `rotate(${a}) translate(${rr},0) rotate(${flip})`;
    })
    .attr("text-anchor", "middle").attr("dy", "0.34em")
    .style("font-family", "var(--font-body)").style("font-weight", "600")
    .style("font-size", d => (d.x1 - d.x0 > 0.55 ? 13.5 : 11) + "px")
    .style("fill", d => (DARK_TEXT.has(d.data.color) ? "#16213e" : "#fff")).style("pointer-events", "none")
    .each(function (d) {
      const t = d3.select(this), words = d.data.name.split(" ");
      if (words.length > 1) {
        const half = Math.ceil(words.length / 2);
        t.text(null);
        t.append("tspan").attr("x", 0).attr("dy", "-0.22em").text(words.slice(0, half).join(" "));
        t.append("tspan").attr("x", 0).attr("dy", "1.08em").text(words.slice(half).join(" "));
      } else t.text(d.data.name);
    });

  document.getElementById("donutLegend").innerHTML = root.children.map(d => `
    <div class="legend-item"><span class="swatch" style="background:${d.data.color}"></span>${d.data.name}</div>`).join("");
}
document.getElementById("catYear").addEventListener("change", ev => drawSunburst(+ev.target.value));

/* ============================================================
   MODALITIES — illustrative marimekko
   ============================================================ */
const MOSAIC_CATS = {
  "Metabolic": "#3f4e5a", "Neurology": "#a24df0", "Oncology": "#0a7d3a",
  "Haematology": "#4d8df6", "Ophthalmology": "#21c8dd", "Dermatology": "#f0932a",
  "Immunology": "#d92d2d", "Other rare": "#17223f",
};
const TECH_MIX = [
  ["Small molecule", 46, { "Metabolic": 22, "Neurology": 24, "Oncology": 20, "Ophthalmology": 8, "Dermatology": 8, "Immunology": 10, "Other rare": 8 }],
  ["Enzyme replacement", 16, { "Metabolic": 70, "Haematology": 10, "Other rare": 20 }],
  ["Gene therapy", 14, { "Ophthalmology": 26, "Haematology": 24, "Neurology": 26, "Metabolic": 14, "Other rare": 10 }],
  ["Antisense / RNA", 9, { "Neurology": 40, "Metabolic": 30, "Haematology": 30 }],
  ["Monoclonal antibody", 8, { "Oncology": 55, "Immunology": 30, "Haematology": 15 }],
  ["Cell therapy", 4, { "Haematology": 50, "Dermatology": 30, "Oncology": 20 }],
  ["Peptide", 3, { "Metabolic": 40, "Neurology": 30, "Other rare": 30 }],
];
const MOSAIC_ORDER = Object.keys(MOSAIC_CATS);

function drawMosaic(year) {
  year = year || +document.getElementById("techYear").value;
  const host = document.getElementById("mosaicChart");
  const W = host.clientWidth, H = Math.max(620, host.clientHeight);
  host.innerHTML = "";
  const svg = d3.select(host).append("svg").attr("width", W).attr("height", H);
  const jit = mulberry32(6200 + year);
  let cols = TECH_MIX.map(([name, share, mix]) => ({
    name, share: share * (0.85 + jit() * 0.3),
    mix: MOSAIC_ORDER.filter(c => mix[c]).map(c => ({ cat: c, v: mix[c] * (0.85 + jit() * 0.3) })),
  })).sort((a, b) => b.share - a.share);
  const shareSum = d3.sum(cols, c => c.share);
  cols.forEach(c => {
    c.share = (c.share / shareSum) * 100;
    const s = d3.sum(c.mix, m => m.v);
    c.mix.forEach(m => (m.v = (m.v / s) * 100));
  });

  const GAP = 18, HEAD = 78, SEG_GAP = 5;
  const usableW = W - GAP * (cols.length - 1), usableH = H - HEAD;
  let cx = 0;
  const colG = svg.selectAll("g.col").data(cols).join("g").attr("class", "col")
    .attr("transform", d => { const t = `translate(${cx},0)`; d.w = (d.share / 100) * usableW; cx += d.w + GAP; return t; });
  colG.append("text").attr("x", 0).attr("y", 26)
    .style("font-family", "var(--font-kicker)").style("font-weight", "600").style("font-size", "21px").style("fill", "#16213e")
    .text(d => d.name);
  colG.append("text").attr("x", 0).attr("y", 50)
    .style("font-family", "var(--font-body)").style("font-size", "15px").style("fill", "#4b5563")
    .text(d => Math.round(d.share) + "%");
  colG.each(function (col) {
    const g = d3.select(this);
    const segH = usableH - SEG_GAP * (col.mix.length - 1);
    let sy = HEAD;
    col.mix.forEach((m, i) => {
      const h = (m.v / 100) * segH;
      const seg = g.append("g").attr("transform", `translate(0,${sy})`);
      seg.append("rect").attr("width", col.w).attr("height", Math.max(2, h)).attr("rx", 2)
        .attr("fill", MOSAIC_CATS[m.cat]).attr("opacity", 0).style("cursor", "pointer")
        .on("mousemove", ev => showTip(`<div class="tt-title">${col.name} · ${m.cat}</div>${Math.round(m.v)}% of ${col.name}`, ev.clientX, ev.clientY))
        .on("mouseleave", hideTip)
        .transition().duration(450).delay(i * 55).attr("opacity", 1);
      if (h > 40 && col.w > 92) {
        seg.append("text").attr("x", 10).attr("y", 21)
          .style("font-family", "var(--font-body)").style("font-weight", "600").style("font-size", "13.5px").style("fill", "#fff").style("pointer-events", "none")
          .text(m.cat.length * 7.6 > col.w - 20 ? m.cat.slice(0, Math.floor((col.w - 30) / 7.6)) + "…" : m.cat);
        seg.append("text").attr("x", 10).attr("y", 39)
          .style("font-family", "var(--font-body)").style("font-size", "12px").style("fill", "rgba(255,255,255,.85)").style("pointer-events", "none")
          .text(Math.round(m.v) + "%");
      }
      sy += h + SEG_GAP;
    });
  });
}
document.getElementById("techYear").addEventListener("change", ev => drawMosaic(+ev.target.value));

/* ============================================================
   APPROVAL MAP — real country counts (RDH pipeline)
   ============================================================ */
let mapWorld = null;
async function drawMap() {
  const host = document.getElementById("mapChart");
  const W = host.clientWidth, H = Math.max(560, host.clientHeight);
  host.innerHTML = "";
  const spots = (BIO.countries || []).filter(c => c.lon != null);
  try {
    if (!mapWorld) mapWorld = await d3.json("https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json");
    const countries = topojson.feature(mapWorld, mapWorld.objects.countries).features.filter(f => f.id !== "010");
    const svg = d3.select(host).append("svg").attr("width", W).attr("height", H);

    /* focus the projection on Europe (where almost all bubbles sit) */
    const proj = d3.geoNaturalEarth1().center([12, 52]).scale(W * 1.05).translate([W / 2, H / 2 + 40]);
    const path = d3.geoPath(proj);
    svg.append("path").attr("d", path(d3.geoGraticule10())).attr("fill", "none").attr("stroke", "#e6e1d3").attr("stroke-width", 0.7);
    svg.append("g").selectAll("path").data(countries).join("path")
      .attr("d", path).attr("fill", "#c9ab87").attr("stroke", "#faf9f4").attr("stroke-width", 0.5);

    const maxN = d3.max(spots, s => s.n) || 1;
    const kR = (Math.min(W, 1200) / 1200) * 30;
    spots.forEach(s => { const p = proj([s.lon, s.lat]); s.x = p ? p[0] : -99; s.y = p ? p[1] : -99; s.r = Math.max(5, kR * Math.sqrt(s.n / maxN)); });

    const spot = svg.append("g").selectAll("g.spot").data(spots.filter(s => s.x > -50)).join("g")
      .attr("class", "spot").attr("transform", d => `translate(${d.x},${d.y})`);
    spot.append("circle").attr("fill", "#16213e").attr("fill-opacity", 0.82)
      .attr("stroke", "#93dce6").attr("stroke-width", 1.2).attr("r", 0).style("cursor", "pointer")
      .on("mousemove", (ev, d) => showTip(`<div class="tt-title">${d.name}</div>${d.n} candidate drugs authorised`, ev.clientX, ev.clientY))
      .on("mouseleave", hideTip)
      .transition().duration(620).delay((d, i) => i * 30).ease(d3.easeBackOut.overshoot(1.15))
      .attr("r", d => d.r);

    const lbl = spot.filter(d => d.r > 15).append("g").attr("pointer-events", "none").attr("opacity", 0);
    lbl.append("text").attr("text-anchor", "middle").attr("dy", "0.34em")
      .style("font-family", "var(--font-mono)").style("font-weight", "600").style("font-size", "11px").style("fill", "#fff")
      .text(d => d.n);
    lbl.transition().duration(400).delay((d, i) => 300 + i * 30).attr("opacity", 1);
  } catch (e) {
    const top = spots.slice(0, 6).map(s => `${s.name} ${s.n}`).join(", ");
    host.innerHTML = `<p style="font-family:var(--font-mono);font-size:13px;color:#6b7280;padding:40px 0">Map unavailable offline — top: ${top}.</p>`;
  }
}

/* ============================================================
   SCROLL REVEAL + LAZY DRAW
   ============================================================ */
const drawn = new Set();
function drawFor(id) {
  if (drawn.has(id)) return;
  drawn.add(id);
  if (id === "ecosystem") { drawEcoBars(true); drawEco(true); }
  if (id === "wallets") drawWallets();
  if (id === "blockchains") drawBubbles();
  if (id === "categories") drawSunburst();
  if (id === "technologies") drawMosaic();
  if (id === "locations") drawMap();
}
const io = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add("in"); drawFor(e.target.id); io.unobserve(e.target); } });
}, { threshold: 0.12 });
document.querySelectorAll(".reveal").forEach(el => io.observe(el));

let sT = null;
addEventListener("scroll", () => {
  if (sT) return;
  sT = setTimeout(() => {
    sT = null;
    document.querySelectorAll(".reveal:not(.in)").forEach(el => {
      const r = el.getBoundingClientRect();
      if (r.top < innerHeight * 0.9 && r.bottom > 0) { el.classList.add("in"); drawFor(el.id); io.unobserve(el); }
    });
  }, 150);
}, { passive: true });

buildTabs();

let rT = null;
addEventListener("resize", () => {
  clearTimeout(rT);
  rT = setTimeout(() => {
    buildMosaic(); heroScrollUpdate();
    if (drawn.has("ecosystem")) { drawEcoBars(false); drawEco(false); }
    if (drawn.has("wallets")) drawWallets();
    if (drawn.has("blockchains")) drawBubbles();
    if (drawn.has("categories")) drawSunburst();
    if (drawn.has("technologies")) drawMosaic();
    if (drawn.has("locations")) drawMap();
  }, 250);
});
