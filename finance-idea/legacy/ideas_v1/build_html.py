"""build_html.py — combine dashboard + all idea plots/reports into one HTML page.

Run after `dashboard.py` and all idea scripts. Produces:

    ideas/outputs/report.html

Open it directly in a browser — no server needed. All plots are referenced
relatively from the same `outputs/` directory.
"""
from __future__ import annotations

import datetime as dt
import html
import json
import pathlib
import re

OUT = pathlib.Path(__file__).resolve().parent / "outputs"


IDEAS = [
    ("idea01", "01 — QDII Nasdaq ETF 溢价反指 QQQ",
     ["idea01_premium_vs_qqq.png", "idea01_buckets.png", "idea01_equity.png"]),
    ("idea02", "02 — QQQ 跌破 200 日均线买入",
     ["idea02_qqq_ma200.png", "idea02_equity.png"]),
    ("idea03", "03 — VIX 极值反转",
     ["idea03_vix.png", "idea03_buckets.png", "idea03_equity.png"]),
    ("idea04", "04 — Gold/Copper 风险偏好",
     ["idea04_ratio.png", "idea04_buckets.png", "idea04_equity.png"]),
    ("idea05", "05 — DXY 6 个月变动 → EM 倾斜",
     ["idea05_dxy_eem.png", "idea05_buckets.png", "idea05_equity.png"]),
    ("idea06", "06 — 美债 10Y-3M 倒挂 / 再陡峭化",
     ["idea06_curve.png", "idea06_equity.png"]),
    ("idea07", "07 — AH 溢价反转（数据源不可用，跳过）",
     []),
    ("idea08", "08 — 北向资金 20 日累计 → 沪深 300",
     ["idea08_flow.png", "idea08_buckets.png", "idea08_equity.png"]),
    ("idea09", "09 — IWM/SPY 小盘相对强度",
     ["idea09_ratio.png", "idea09_buckets.png", "idea09_equity.png"]),
    ("idea10", "10 — BTC/Gold 情绪温度计",
     ["idea10_btc_gold.png", "idea10_buckets.png", "idea10_equity.png"]),
]


def _md_table_to_html(md: str) -> str:
    """Tiny markdown-table → HTML converter for the per-idea report bodies."""
    lines = md.splitlines()
    out, in_table, header = [], False, []
    for ln in lines:
        if ln.startswith("|") and "|" in ln[1:]:
            cells = [c.strip() for c in ln.strip("|").split("|")]
            if all(re.match(r"^:?-+:?$", c) for c in cells):
                continue  # separator
            if not in_table:
                out.append("<table>")
                header = cells
                out.append("<thead><tr>" + "".join(
                    f"<th>{html.escape(c)}</th>" for c in cells) + "</tr></thead><tbody>")
                in_table = True
            else:
                out.append("<tr>" + "".join(
                    f"<td>{html.escape(c)}</td>" for c in cells) + "</tr>")
        else:
            if in_table:
                out.append("</tbody></table>")
                in_table = False
            if ln.startswith("# "):
                out.append(f"<h3>{html.escape(ln[2:])}</h3>")
            elif ln.startswith("## "):
                out.append(f"<h4>{html.escape(ln[3:])}</h4>")
            elif ln.strip() == "":
                out.append("")
            else:
                out.append(f"<p>{html.escape(ln)}</p>")
    if in_table:
        out.append("</tbody></table>")
    return "\n".join(out)


def _dashboard_section() -> str:
    p = OUT / "dashboard.json"
    if not p.exists():
        return "<p><em>dashboard.json not found — run ideas/dashboard.py first.</em></p>"
    data = json.loads(p.read_text())
    rows = []
    for s in data["signals"]:
        v = s.get("value")
        v_str = "—" if v is None else str(v)
        unit = s.get("unit", "")
        interp = s.get("interpretation", "")
        klass = ""
        text = (interp or "").lower()
        if any(k in text for k in ("hot", "panic", "euphoria", "inverted")):
            klass = "hot"
        elif any(k in text for k in ("cold", "fear", "outflow")):
            klass = "cold"
        elif "neutral" in text:
            klass = "neutral"
        rows.append(
            f"<tr class='{klass}'>"
            f"<td>{html.escape(s['name'])}</td>"
            f"<td class='val'>{html.escape(v_str)} <span class='unit'>{html.escape(unit)}</span></td>"
            f"<td>{html.escape(interp)}</td></tr>"
        )

    detail_bits = []
    for s in data["signals"]:
        d = s.get("detail") or s.get("details")
        if isinstance(d, list):
            inner = "<ul>" + "".join(
                f"<li>{html.escape(x['code'])} {html.escape(x['name'])} "
                f"premium <b>{x['premium_pct']:.2f}%</b></li>"
                for x in d
            ) + "</ul>"
            detail_bits.append(f"<details><summary>{html.escape(s['name'])}</summary>{inner}</details>")
        elif d:
            detail_bits.append(
                f"<details><summary>{html.escape(s['name'])}</summary>"
                f"<p>{html.escape(str(d))}</p></details>")

    return (
        f"<p class='asof'>as of {html.escape(data['asof'])}</p>"
        "<table class='dashboard'>"
        "<thead><tr><th>Signal</th><th>Value</th><th>Interpretation</th></tr></thead>"
        f"<tbody>{''.join(rows)}</tbody></table>"
        + ("<div class='details'>" + "".join(detail_bits) + "</div>" if detail_bits else "")
    )


def _idea_section(idea_id: str, title: str, imgs: list[str]) -> str:
    report_path = OUT / f"{idea_id}_report.md"
    body_html = ""
    if report_path.exists():
        body_html = _md_table_to_html(report_path.read_text())
    img_html = "".join(
        f"<figure><img src='{html.escape(img)}' alt='{html.escape(img)}'/>"
        f"<figcaption>{html.escape(img)}</figcaption></figure>"
        for img in imgs
        if (OUT / img).exists()
    )
    if not imgs:
        img_html = "<p><em>No plots (idea was skipped).</em></p>"
    return (
        f"<section id='{idea_id}'>"
        f"<h2>{html.escape(title)}</h2>"
        f"<div class='plots'>{img_html}</div>"
        f"<div class='report'>{body_html}</div>"
        f"</section>"
    )


HTML_TEMPLATE = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
<title>Finance-Idea Dashboard & Backtests</title>
<style>
  :root {{
    --bg: #fafafa; --fg: #1f2328; --muted: #57606a;
    --border: #d0d7de; --hot: #cf222e; --cold: #1f6feb; --neutral: #6e7781;
    --table: #fff;
  }}
  body {{ font-family: -apple-system, "Helvetica Neue", "PingFang SC", "Microsoft YaHei", Arial, sans-serif;
          background: var(--bg); color: var(--fg); margin: 0; padding: 0 24px 64px; }}
  header {{ padding: 24px 0 8px; border-bottom: 1px solid var(--border); margin-bottom: 24px; }}
  h1 {{ margin: 0 0 4px; font-size: 28px; }}
  .subtitle {{ color: var(--muted); }}
  nav {{ position: sticky; top: 0; background: var(--bg); padding: 8px 0; border-bottom: 1px solid var(--border); z-index: 10; }}
  nav a {{ margin-right: 12px; color: var(--cold); text-decoration: none; font-size: 13px; }}
  nav a:hover {{ text-decoration: underline; }}
  section {{ margin: 40px 0; }}
  h2 {{ margin: 12px 0; padding-bottom: 4px; border-bottom: 2px solid var(--border); }}
  h3 {{ margin: 16px 0 4px; }}
  h4 {{ margin: 14px 0 4px; color: var(--muted); }}
  table {{ border-collapse: collapse; background: var(--table); margin: 8px 0 16px;
           box-shadow: 0 1px 0 var(--border); font-size: 13px; }}
  th, td {{ border: 1px solid var(--border); padding: 6px 10px; text-align: left; }}
  th {{ background: #f6f8fa; font-weight: 600; }}
  table.dashboard td.val {{ font-weight: 600; font-size: 15px; }}
  table.dashboard td.val .unit {{ color: var(--muted); font-weight: 400; }}
  tr.hot td.val {{ color: var(--hot); }}
  tr.cold td.val {{ color: var(--cold); }}
  tr.neutral td.val {{ color: var(--neutral); }}
  .plots {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(420px, 1fr)); gap: 12px; }}
  figure {{ margin: 0; background: white; border: 1px solid var(--border); padding: 8px; }}
  figure img {{ width: 100%; height: auto; display: block; }}
  figure figcaption {{ font-size: 11px; color: var(--muted); margin-top: 4px; }}
  details summary {{ cursor: pointer; padding: 4px 0; color: var(--cold); }}
  details ul {{ margin: 4px 0 12px 24px; padding: 0; }}
  .asof {{ color: var(--muted); font-size: 13px; }}
  p {{ margin: 4px 0; }}
</style>
</head>
<body>
<header>
  <h1>Finance-Idea Dashboard &amp; Backtests</h1>
  <div class="subtitle">10 个市场情绪 / 趋势 idea 的回测结果 + 当日实时信号</div>
  <div class="subtitle">生成时间: {generated}</div>
</header>

<nav>
  <a href="#dashboard">Dashboard</a>
  {nav_links}
</nav>

<section id="dashboard">
  <h2>当日信号面板</h2>
  {dashboard_html}
</section>

{idea_sections}

<footer style="margin-top: 48px; color: var(--muted); font-size: 12px; border-top: 1px solid var(--border); padding-top: 12px;">
  数据源: akshare (Sina / EM) + yfinance. 重新生成: <code>python run_all.py</code>
</footer>
</body>
</html>
"""


def main():
    generated = dt.datetime.now().isoformat(timespec="seconds")
    dashboard_html = _dashboard_section()
    sections = [_idea_section(i, t, imgs) for (i, t, imgs) in IDEAS]
    nav_links = " ".join(
        f"<a href='#{i}'>{html.escape(t.split('—')[0].strip())}</a>"
        for (i, t, _) in IDEAS
    )
    page = HTML_TEMPLATE.format(
        generated=html.escape(generated),
        dashboard_html=dashboard_html,
        nav_links=nav_links,
        idea_sections="\n".join(sections),
    )
    out_path = OUT / "report.html"
    out_path.write_text(page, encoding="utf-8")
    print(f"wrote {out_path}")
    print(f"open with:  open '{out_path}'")


if __name__ == "__main__":
    main()
