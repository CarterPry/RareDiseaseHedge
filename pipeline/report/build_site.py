#!/usr/bin/env python3
"""
Assemble the deployable static site into pipeline/report/_site/.

Layout served at the domain root:
  /              -> the "State of Bio" almanac (report index.html + assets)
  /list/         -> the self-contained card-list dashboard (pipeline/ui)
  /funnel.html   -> the pipeline funnel report (rendered from markdown)
  /audit.html    -> the accuracy audit (rendered from markdown)
  /data/summary.json -> the raw pipeline output

The almanac's "Explore" cards are rewritten to these in-site paths (their repo
relative links do not resolve once deployed).

Run:  python3 pipeline/report/build_site.py
Deps: stdlib only.
"""
import os, re, shutil, html

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
PIPE = os.path.join(ROOT, "pipeline")
SITE = os.path.join(HERE, "_site")


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
<a href="./">← Almanac</a><a href="list/">Card list</a><a href="funnel.html">Funnel</a><a href="audit.html">Audit</a></div></div>
<main class="wrap">{body}</main></body></html>"""


def render_doc(md_path, title):
    with open(md_path, encoding="utf-8") as fh:
        return DOC_SHELL.format(title=html.escape(title), body=md_to_html(fh.read()))


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
    # noindex helper so search engines don't index the demo
    with open(os.path.join(SITE, "robots.txt"), "w") as fh:
        fh.write("User-agent: *\nDisallow: /\n")

    files = sum(len(fs) for _, _, fs in os.walk(SITE))
    print(f"built {SITE} ({files} files) — deploy with:")
    print("  npx wrangler pages deploy pipeline/report/_site --project-name=rarediseasehedge")


if __name__ == "__main__":
    main()
