#!/usr/bin/env python3
"""
Assemble the deployable static site into pipeline/report/_site/.

Layout served at the domain root:
  /              -> the "State of Bio" almanac (report index.html + assets)
  /list/         -> the self-contained card-list dashboard (pipeline/ui)
  /funnel.html   -> the pipeline funnel report (rendered from markdown)
  /audit.html    -> the accuracy audit (rendered from markdown)
  /data/summary.json -> the raw pipeline output
  /candidates.html -> static, no-JavaScript table of every candidate (for
                      crawlers, AI fetchers, reader modes)
  /llms.txt, /llms-full.txt -> plain-text site guide + the full candidate list
  /robots.txt, /sitemap.xml -> crawlers are welcome (search + AI). The site is
                      meant to be read by AI assistants; do not reintroduce a
                      Disallow here.
  /404.html        -> real 404 so Cloudflare Pages stops serving index.html with
                      200 for unknown paths (soft-404s confuse crawlers)

The almanac's shortlist is also pre-rendered into index.html (#slList) so the
candidates are present in the raw HTML; app.js re-renders it on load.

The almanac's "Explore" cards are rewritten to these in-site paths (their repo
relative links do not resolve once deployed).

Run:  python3 pipeline/report/build_site.py
Deps: stdlib only.
"""
import os, re, shutil, html, json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
PIPE = os.path.join(ROOT, "pipeline")
SITE = os.path.join(HERE, "_site")
BASE_URL = "https://rarediseasehedge.carterpry.com"


# --------------------------------------------------------------- markdown -> html
def md_to_html(md: str) -> str:
    """Compact markdown renderer: headings, hr, tables, ul, blockquote, inline
    (bold, code, links), paragraphs. Enough for this repo's docs."""
    def inline(s):
        s = html.escape(s, quote=False)
        s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
        s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
        s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
        return s

    out, i, lines = [], 0, md.split("\n")
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1; continue
        if re.match(r"^\s*---+\s*$", ln):
            out.append("<hr>"); i += 1; continue
        m = re.match(r"^(#{1,6})\s+(.*)$", ln)
        if m:
            lvl = len(m.group(1)); out.append(f"<h{lvl}>{inline(m.group(2))}</h{lvl}>"); i += 1; continue
        # table: a header row followed by a |---| separator
        if ln.lstrip().startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            def cells(row): return [c.strip() for c in row.strip().strip("|").split("|")]
            head = cells(ln); i += 2; body = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                body.append(cells(lines[i])); i += 1
            t = ["<table><thead><tr>"] + [f"<th>{inline(c)}</th>" for c in head] + ["</tr></thead><tbody>"]
            for r in body:
                t.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            t.append("</tbody></table>"); out.append("".join(t)); continue
        if re.match(r"^\s*[-*]\s+", ln):
            items = []
            while i < len(lines) and re.match(r"^\s*[-*]\s+", lines[i]):
                items.append(f"<li>{inline(re.sub(r'^\s*[-*]\s+', '', lines[i]))}</li>"); i += 1
            out.append("<ul>" + "".join(items) + "</ul>"); continue
        if ln.lstrip().startswith(">"):
            q = []
            while i < len(lines) and lines[i].lstrip().startswith(">"):
                q.append(inline(re.sub(r"^\s*>\s?", "", lines[i]))); i += 1
            out.append("<blockquote>" + "<br>".join(q) + "</blockquote>"); continue
        # paragraph (gather until blank)
        para = [ln]; i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^\s*(#|\||>|[-*]\s|---)", lines[i]):
            para.append(lines[i]); i += 1
        out.append("<p>" + inline(" ".join(para)) + "</p>")
    return "\n".join(out)


DOC_SHELL = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — State of Bio</title>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=IBM+Plex+Mono:wght@400;600&family=Archivo:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{{--cream:#f1eee4;--paper:#faf9f4;--ink:#101820;--navy:#16213e;--sky:#93dce6;--hairline:#d8d4c6;--slate:#6b7280}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--cream);color:var(--ink);font:16px/1.65 Archivo,sans-serif}}
.bar{{background:var(--ink);color:#eaf2f3;padding:16px 0}}
.bar .wrap{{display:flex;gap:16px;align-items:baseline}}
.wrap{{max-width:900px;margin:0 auto;padding:0 28px}}
a{{color:#0b6e75}} .bar a{{color:var(--sky);font-family:IBM Plex Mono,monospace;font-size:13px;text-decoration:none}}
.brand{{font-family:IBM Plex Mono,monospace;font-weight:600;font-size:18px}}
main{{padding:40px 0 80px}}
h1{{font-family:Anton,sans-serif;font-weight:400;font-size:clamp(34px,6vw,60px);line-height:1.02;text-transform:uppercase;color:var(--navy);margin:0 0 8px}}
h2{{font-family:Anton,sans-serif;font-weight:400;font-size:28px;text-transform:uppercase;color:var(--navy);margin:36px 0 10px;letter-spacing:.01em}}
h3{{font-size:19px;margin:26px 0 6px;color:var(--ink)}} h4{{font-size:16px;margin:20px 0 4px}}
code{{font-family:IBM Plex Mono,monospace;font-size:.86em;background:#e9e5d8;padding:1px 5px;border-radius:4px}}
hr{{border:0;border-top:1px solid var(--hairline);margin:34px 0}}
table{{border-collapse:collapse;width:100%;margin:16px 0;font-size:13.5px}}
th,td{{border:1px solid var(--hairline);padding:7px 10px;text-align:left;vertical-align:top}}
th{{background:var(--paper);font-family:IBM Plex Mono,monospace;font-size:12px}}
blockquote{{border-left:3px solid var(--sky);margin:14px 0;padding:6px 16px;color:var(--slate);background:var(--paper)}}
ul{{padding-left:22px}} li{{margin:4px 0}} p{{margin:12px 0}}
</style></head><body>
<div class="bar"><div class="wrap"><span class="brand">rarediseasehedge</span>
<a href="./">← Almanac</a><a href="candidates.html">Candidates</a><a href="list/">Card list</a><a href="funnel.html">Funnel</a><a href="audit.html">Audit</a></div></div>
<main class="wrap">{body}</main></body></html>"""


def render_doc(md_path, title):
    with open(md_path, encoding="utf-8") as fh:
        return DOC_SHELL.format(title=html.escape(title), body=md_to_html(fh.read()))


# --------------------------------------------------------- crawler-facing output
def load_bio():
    """Parse the generated data.js (`window.BIO = {...};`) back into a dict."""
    with open(os.path.join(HERE, "data.js"), encoding="utf-8") as fh:
        js = fh.read()
    return json.loads(js[js.index("{"): js.rindex("}") + 1])


def sorted_cands(bio):
    """Same default order as app.js slRender(): widest EEA reach, then name."""
    return sorted(bio.get("candidates", []), key=lambda c: (-(c.get("nc") or 0), c.get("name", "")))


def cand_disease(c):
    o = c.get("orpha") or {}
    return (o.get("disease") or c.get("area") or c.get("disease")
            or (c.get("ind") or "").rstrip(".") or "—")


def cand_badges(c):
    b = []
    if c.get("orphan"): b.append("orphan")
    o = c.get("orpha") or {}
    if o.get("rarity") == "rare": b.append("rare disease")
    if o.get("onset") == "pediatric": b.append("pediatric onset")
    if c.get("eu_orphan"): b.append("EU orphan designation")
    if c.get("crl"): b.append("US filed & refused")
    if len(c.get("sources") or []) > 1: b.append("multi-regulator")
    if c.get("fs") == "previously_authorised": b.append("licence pulled")
    return b


def cand_sources(c):
    return [x.replace("EU national (Art57)", "EEA national").replace(" (Art57)", "")
            for x in (c.get("sources") or [])]


def static_shortlist_html(bio):
    """Server-side twin of app.js slCard() for the raw HTML of index.html."""
    e = lambda v: html.escape(str(v), quote=True)
    out = []
    for c in sorted_cands(bio):
        dz = cand_disease(c)
        badges = "".join(f'<span class="badge">{e(b)}</span>' for b in cand_badges(c))
        src = "".join(f'<span class="badge badge-src">{e(x)}</span>' for x in cand_sources(c))
        pm = c.get("pubmed"); tr = c.get("trials")
        atc = f'<span>ATC <b>{e(c["atc"])}</b></span>' if c.get("atc") else ""
        out.append(
            f'<div class="sl-card" data-name="{e(c["name"])}" tabindex="0" role="button">'
            f'<div class="sl-card-top"><span class="sl-name">{e(c["name"])}</span>'
            f'<span class="sl-reach"><b>{c.get("nc") or 0}</b> EEA</span></div>'
            f'<div class="sl-dz">{e(dz if len(dz) <= 96 else dz[:96] + "…")}</div>'
            f'<div class="sl-badges">{badges}</div><div class="sl-badges">{src}</div>'
            f'<div class="sl-foot"><span>papers <b>{pm if pm is not None else "—"}</b></span>'
            f'<span>trials <b>{tr if tr is not None else "—"}</b></span>{atc}</div></div>')
    return "\n".join(out)


def candidates_page(bio):
    """A plain HTML table of every candidate — readable with JavaScript off."""
    e = lambda v: html.escape(str(v), quote=False)
    rows = []
    for c in sorted_cands(bio):
        el = (c.get("elig") or {}).get("verdict", "")
        rows.append("<tr>"
            f'<td><strong>{e(c["name"])}</strong><br><code>{e(c.get("moiety") or "")}</code></td>'
            f'<td>{e(cand_disease(c))}</td>'
            f'<td>{e(c.get("ind") or "")}</td>'
            f'<td>{e(", ".join(cand_sources(c)))}</td>'
            f'<td>{c.get("nc") or 0}</td>'
            f'<td>{e(c.get("fs") or "")}</td>'
            f'<td>{e(", ".join(cand_badges(c)) or "—")}</td>'
            f'<td>{e(c.get("atc") or "—")}</td>'
            f'<td>{c.get("pubmed") if c.get("pubmed") is not None else "—"}</td>'
            f'<td>{c.get("trials") if c.get("trials") is not None else "—"}</td>'
            f'<td>{e(el.replace("_", " ").lower())}</td>'
            "</tr>")
    n = len(rows)
    body = (f"<h1>{n} candidates</h1>"
            f"<p>Every drug in the RareDiseaseHedge \u201cFunnel A\u201d screen: a real marketing "
            f"authorisation from a foreign regulator (EMA, EEA national, Health Canada, Swissmedic, PMDA) "
            f"whose active moiety has <strong>never been approved in the United States</strong> \u2014 the "
            f"population FD&amp;C Act \u00a7529 makes eligible for a rare-pediatric Priority Review Voucher. "
            f"Sorted by how many EEA countries authorise the drug (widest reach first).</p>"
            f"<p>Data snapshot: {e(bio.get('snapshot',''))}. Generated {e(bio.get('generated',''))}. "
            f"Also available as <a href=\"llms-full.txt\">plain text</a> and "
            f"<a href=\"data/summary.json\">raw JSON</a>; the interactive version with the per-candidate "
            f"\u00a7529 checklist is on the <a href=\"./#shortlist\">almanac</a> and the <a href=\"list/\">card list</a>.</p>"
            "<table><thead><tr><th>Drug / moiety</th><th>Disease</th><th>Indication</th><th>Approved by</th>"
            "<th>EEA countries</th><th>Status</th><th>Flags</th><th>ATC</th><th>Papers</th><th>Trials</th>"
            "<th>\u00a7529 verdict</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table>")
    return DOC_SHELL.format(title=f"{n} candidates", body=body)


def llms_txt(bio):
    h = bio.get("headline", {})
    return f"""# RareDiseaseHedge \u2014 State of Bio 2026

> A screen of drugs approved by a foreign regulator (EMA, EEA national registers via
> the EMA Article 57 database, Health Canada, Swissmedic, PMDA) whose active moiety has
> never been approved in the United States. That is the population the FD&C Act
> \u00a7529 makes eligible for a rare-pediatric Priority Review Voucher (PRV). Each
> candidate carries a machine-drafted \u00a7529 eligibility checklist plus PubMed,
> ClinicalTrials.gov, ChEMBL, Orphadata, EU orphan-designation and FDA complete-response
> signals. Automated agents and AI assistants are welcome to read every page here.

Data snapshot: {bio.get("snapshot", "")}
Generated: {bio.get("generated", "")}

## Headline numbers
- Candidates (approved abroad, never in the US): {h.get("candidates")}
- Multi-regulator candidates: {h.get("multi_regulator")}
- Dossier-only (unnamed) rows: {h.get("dossier_only")}; rows queued for human review: {h.get("review")}
- Foreign approval rows screened: {h.get("foreign_rows")}; of which already in the US record: {h.get("in_us")}
- Disclosed PRV sales tracked (SEC 8-K): {h.get("deals")}; 2026 range US$ {h.get("prv_low")}M\u2013{h.get("prv_high")}M; record US$ {h.get("peak")}M (2015)
- Months until the rare-pediatric PRV programme sunset: {h.get("months_to_sunset")}

## Pages
- [Almanac (home)]({BASE_URL}/): searchable shortlist, PRV market charts, pipeline breadth, approval map
- [Candidate table, static HTML]({BASE_URL}/candidates.html): all candidates in one plain table, no JavaScript needed
- [Full candidate list, plain text]({BASE_URL}/llms-full.txt): one section per candidate incl. the \u00a7529 checklist
- [Card-list dashboard]({BASE_URL}/list/): interactive cards with notes export/import
- [Funnel report]({BASE_URL}/funnel.html): how 18k foreign approval rows narrow to the shortlist
- [Accuracy audit]({BASE_URL}/audit.html): harness results and known limitations
- [Raw pipeline output, JSON]({BASE_URL}/data/summary.json): everything above, machine-readable

## Notes
- Charts labelled "RDH pipeline" and "SEC 8-K filings" are real data; charts labelled "Illustrative" (disease areas, modalities) are design placeholders.
- Nothing on this site is investment, legal, business or tax advice.
"""


def llms_full_txt(bio):
    parts = [llms_txt(bio), "\n## Candidates (widest EEA reach first)\n"]
    for c in sorted_cands(bio):
        parts.append(f"\n### {c['name']}\n")
        parts.append(f"- Active moiety: {c.get('moiety') or '—'}" + (f" (UNII {c['unii']})" if c.get("unii") else ""))
        parts.append(f"- Disease: {cand_disease(c)}")
        if c.get("ind"): parts.append(f"- Indication: {c['ind']}")
        parts.append(f"- Approved by: {', '.join(cand_sources(c)) or '—'}; authorised in {c.get('nc') or 0} EEA countries; status: {c.get('fs') or '—'}")
        b = cand_badges(c)
        if b: parts.append(f"- Flags: {', '.join(b)}")
        if c.get("atc"): parts.append(f"- ATC: {c['atc']}")
        parts.append(f"- Research activity: {c.get('pubmed') if c.get('pubmed') is not None else '—'} PubMed papers, {c.get('trials') if c.get('trials') is not None else '—'} registered trials")
        if c.get("chembl"): parts.append(f"- ChEMBL indications: {', '.join(c['chembl'])}")
        eo = c.get("eu_orphan")
        if eo: parts.append(f"- EU orphan designation: {eo.get('use') or ''} ({eo.get('status') or ''})")
        o = c.get("orpha")
        if o: parts.append(f"- Orphadata: {o.get('disease') or ''}; rarity {o.get('rarity') or '?'}; onset {o.get('onset') or '?'}")
        if c.get("crl"): parts.append(f"- US complete response letter on file: {c['crl'] if isinstance(c['crl'], str) else 'yes'}")
        el = c.get("elig")
        if el:
            parts.append(f"- \u00a7529 verdict: {el.get('verdict', '').replace('_', ' ')}")
            for cr in el.get("criteria", []):
                parts.append(f"  - [{cr.get('status')}] {cr.get('key', '').replace('_', ' ')}: {cr.get('note', '')} ({cr.get('citation', '')})")
        for f in c.get("flags") or []:
            parts.append(f"- Note: {f}")
    return "\n".join(parts) + "\n"


ROBOTS_TXT = """# RareDiseaseHedge — crawlers, search engines and AI assistants are welcome.
# This site exists to be read; please index it and cite it.
User-agent: *
Allow: /

# Explicit allows for AI fetchers/crawlers (some check for a named record).
User-agent: ClaudeBot
User-agent: Claude-User
User-agent: Claude-SearchBot
User-agent: anthropic-ai
User-agent: GPTBot
User-agent: ChatGPT-User
User-agent: OAI-SearchBot
User-agent: PerplexityBot
User-agent: Perplexity-User
User-agent: Google-Extended
User-agent: Googlebot
User-agent: Bingbot
User-agent: Applebot
User-agent: Applebot-Extended
User-agent: Amazonbot
User-agent: CCBot
User-agent: DuckAssistBot
User-agent: meta-externalagent
User-agent: Bytespider
User-agent: cohere-ai
User-agent: MistralAI-User
User-agent: YouBot
Allow: /

# Content Signals (contentsignals.org): search, AI answers and AI training all OK.
Content-Signal: search=yes, ai-input=yes, ai-train=yes

Sitemap: {base}/sitemap.xml
"""


def sitemap_xml(bio):
    pages = ["/", "/candidates.html", "/list/", "/funnel.html", "/audit.html",
             "/llms.txt", "/llms-full.txt", "/data/summary.json"]
    mod = bio.get("generated") or ""
    lm = f"<lastmod>{mod}</lastmod>" if mod else ""
    urls = "".join(f"<url><loc>{BASE_URL}{p}</loc>{lm}</url>" for p in pages)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n'


def write(path, text):
    with open(os.path.join(SITE, path), "w", encoding="utf-8") as fh:
        fh.write(text)



def main():
    if os.path.exists(SITE):
        shutil.rmtree(SITE)
    os.makedirs(os.path.join(SITE, "list"))
    os.makedirs(os.path.join(SITE, "data"))

    # 1) almanac report + assets, with Explore links rewritten for the deploy
    with open(os.path.join(HERE, "index.html"), encoding="utf-8") as fh:
        idx = fh.read()
    idx = (idx.replace('href="../ui/index.html"', 'href="list/"')
              .replace('href="../data/out/funnel_report.md"', 'href="funnel.html"')
              .replace('href="../../AUDIT-2026-08-29.md"', 'href="audit.html"'))
    # pre-render the shortlist so the candidates exist in the raw HTML (AI
    # fetchers, search crawlers and reader modes rarely execute app.js)
    bio = load_bio()
    n = len(bio.get("candidates", []))
    idx = idx.replace('<span id="slCount">—</span>', f'<span id="slCount">{n}</span>', 1)
    idx = idx.replace('<div class="sl-list" id="slList"></div>',
                      '<div class="sl-list" id="slList">\n' + static_shortlist_html(bio) + '\n</div>', 1)
    assert 'id="slList">\n<div class="sl-card"' in idx, "shortlist pre-render anchor not found"
    with open(os.path.join(SITE, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(idx)
    for f in ("style.css", "app.js", "data.js"):
        shutil.copy(os.path.join(HERE, f), os.path.join(SITE, f))

    # 2) self-contained card-list dashboard
    shutil.copy(os.path.join(PIPE, "ui", "index.html"), os.path.join(SITE, "list", "index.html"))

    # 3) rendered docs
    with open(os.path.join(SITE, "funnel.html"), "w", encoding="utf-8") as fh:
        fh.write(render_doc(os.path.join(PIPE, "data", "out", "funnel_report.md"), "Funnel report"))
    with open(os.path.join(SITE, "audit.html"), "w", encoding="utf-8") as fh:
        fh.write(render_doc(os.path.join(ROOT, "AUDIT-2026-08-29.md"), "Accuracy audit"))

    # 4) raw data
    shutil.copy(os.path.join(PIPE, "data", "out", "summary.json"),
                os.path.join(SITE, "data", "summary.json"))
    # 5) crawler / AI-assistant facing files. The site WANTS to be read by
    #    bots (the old "noindex" robots.txt made ChatGPT/Claude refuse to fetch).
    write("robots.txt", ROBOTS_TXT.format(base=BASE_URL))
    write("sitemap.xml", sitemap_xml(bio))
    write("llms.txt", llms_txt(bio))
    write("llms-full.txt", llms_full_txt(bio))
    write("candidates.html", candidates_page(bio))
    # a real 404.html switches Cloudflare Pages out of SPA mode (unknown paths
    # were returning index.html with HTTP 200)
    write("404.html", DOC_SHELL.format(title="Not found",
          body="<h1>Not found</h1><p>That page does not exist. Try the "
               "<a href=\"/\">almanac</a>, the <a href=\"/candidates.html\">candidate table</a> "
               "or <a href=\"/llms.txt\">llms.txt</a> for a map of the site.</p>"))

    files = sum(len(fs) for _, _, fs in os.walk(SITE))
    print(f"built {SITE} ({files} files) — deploy with:")
    print("  npx wrangler pages deploy pipeline/report/_site --project-name=rarediseasehedge")


if __name__ == "__main__":
    main()
