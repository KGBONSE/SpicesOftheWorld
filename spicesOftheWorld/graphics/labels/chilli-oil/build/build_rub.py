"""Chilli Oil Rub: derives the three rub labels from the chilli-oil label HTML
(title becomes "Chilli Oil Rub") and wraps each on a wide-mouth glass jar.

Usage:  python build_rub.py labels   -> writes <region>-rub-label.html
        python build_rub.py jars     -> writes <region>-rub-jar.html (needs <region>-rub-label.png)
Run render_rub.sh to do both plus the PNG rendering.
"""
import base64
import os
import random
import sys
import xml.dom.minidom as _m

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)

# region -> (title font-size in the source label, new title size so "Chilli Oil Rub" fits)
REGIONS = {"africa": (150, 104), "eastasia": (124, 88), "southasia": (124, 88)}


def labels():
    for r, (old, new) in REGIONS.items():
        html = open(os.path.join(OUT, f"{r}-label.html"), encoding="utf-8").read()
        assert "Chilli&nbsp;Oil</div>" in html and f".title{{font-size:{old}px" in html, r
        html = html.replace("Chilli&nbsp;Oil</div>", "Chilli&nbsp;Oil&nbsp;Rub</div>")
        html = html.replace(f".title{{font-size:{old}px", f".title{{font-size:{new}px")
        html = html.replace("Chilli Oil with Spices", "Chilli Oil Rub with Spices")
        with open(os.path.join(OUT, f"{r}-rub-label.html"), "w", encoding="utf-8") as f:
            f.write(html)
        print("label written:", f"{r}-rub-label.html")


# Jar geometry (1200x1200 stage)
BODY = ("M452 392 C 452 376, 466 366, 482 366 L 718 366 C 734 366, 748 376, 748 392 "
        "L 758 430 L 758 1000 Q 758 1030 728 1030 L 472 1030 Q 442 1030 442 1000 "
        "L 442 430 Z")
LW = 300
LH = round(LW / 0.813)
LX = 600 - LW // 2
LY = 560


def jar(region):
    lbl = base64.b64encode(open(os.path.join(OUT, f"{region}-rub-label.png"), "rb").read()).decode()
    random.seed(11)
    bits = ""
    for _ in range(170):  # chilli flakes / seeds suspended in the oil
        x = random.uniform(452, 748); y = random.uniform(470, 1020)
        rx = random.uniform(2.5, 7); ry = rx * random.uniform(.5, .9)
        a = random.uniform(-60, 60)
        col = random.choice(["#5c0f05", "#7a1608", "#a32a0e", "#c9441a", "#3d0a03", "#e0701f"])
        bits += (f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rx:.1f}" ry="{ry:.1f}" '
                 f'transform="rotate({a:.0f} {x:.0f} {y:.0f})" fill="{col}" opacity="{random.uniform(.55,.95):.2f}"/>')
    html = f'''<!DOCTYPE html><html><head><meta charset="UTF-8"/>
<title>Fudi People &mdash; Chilli Oil Rub jar ({region})</title>
<style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  html,body{{width:100%;height:100%}}
  body{{display:flex;align-items:center;justify-content:center;
    background:radial-gradient(circle at 50% 38%, #f7f3ec 0%, #ece3d4 62%, #e0d6c4 100%)}}
  .stage{{position:relative;width:1200px;height:1200px}}
  .stage>*{{position:absolute;left:0;top:0}}
  .label{{width:{LW}px;left:{LX}px;top:{LY}px;z-index:6;border-radius:3px;overflow:hidden;
    box-shadow:0 2px 10px rgba(60,20,0,.3);
    -webkit-mask-image:linear-gradient(90deg,transparent 0,#000 8%,#000 92%,transparent 100%);
            mask-image:linear-gradient(90deg,transparent 0,#000 8%,#000 92%,transparent 100%)}}
  .label img{{display:block;width:100%}}
  .curve{{width:{LW}px;height:{LH}px;left:{LX}px;top:{LY}px;z-index:7;pointer-events:none;border-radius:3px;
    background:linear-gradient(90deg,rgba(0,0,0,.30) 0%,rgba(0,0,0,.05) 15%,rgba(255,255,255,.16) 50%,
      rgba(0,0,0,.05) 85%,rgba(0,0,0,.30) 100%)}}
</style></head><body>
<div class="stage">
<svg width="1200" height="1200" viewBox="0 0 1200 1200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="rub" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#7a1708"/><stop offset="0.12" stop-color="#a82a0e"/>
      <stop offset="0.32" stop-color="#cf4a18"/><stop offset="0.5" stop-color="#e9702a"/>
      <stop offset="0.7" stop-color="#c9441a"/><stop offset="0.9" stop-color="#8f200b"/>
      <stop offset="1" stop-color="#650f04"/>
    </linearGradient>
    <linearGradient id="rubV" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#ffb063" stop-opacity=".4"/>
      <stop offset="0.12" stop-color="#ffb063" stop-opacity="0"/>
      <stop offset="0.8" stop-color="#3d0a03" stop-opacity="0"/>
      <stop offset="1" stop-color="#3d0a03" stop-opacity=".5"/>
    </linearGradient>
    <linearGradient id="glassEdge" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#ffffff" stop-opacity=".0"/>
      <stop offset="0.02" stop-color="#ffffff" stop-opacity=".85"/>
      <stop offset="0.07" stop-color="#ffffff" stop-opacity=".0"/>
      <stop offset="0.90" stop-color="#000000" stop-opacity=".0"/>
      <stop offset="0.97" stop-color="#3a1206" stop-opacity=".38"/>
      <stop offset="1" stop-color="#3a1206" stop-opacity=".0"/>
    </linearGradient>
    <linearGradient id="lid" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#241008"/><stop offset=".22" stop-color="#4a2314"/>
      <stop offset=".5" stop-color="#6b3620"/><stop offset=".78" stop-color="#40200f"/>
      <stop offset="1" stop-color="#1c0b05"/>
    </linearGradient>
    <clipPath id="bodyclip"><path d="{BODY}"/></clipPath>
  </defs>

  <ellipse cx="600" cy="1050" rx="215" ry="24" fill="rgba(70,40,15,.22)"/>

  <!-- lid -->
  <rect x="446" y="296" width="308" height="74" rx="9" fill="url(#lid)"/>
  <rect x="446" y="296" width="308" height="14" rx="7" fill="rgba(255,255,255,.14)"/>
  <rect x="446" y="296" width="308" height="74" rx="9" fill="none" stroke="rgba(0,0,0,.45)" stroke-width="1.5"/>
  <g stroke="rgba(0,0,0,.35)" stroke-width="2">{''.join(f'<line x1="{x}" y1="312" x2="{x}" y2="366"/>' for x in range(462, 744, 12))}</g>

  <g clip-path="url(#bodyclip)">
    <rect x="430" y="360" width="340" height="680" fill="url(#rub)"/>
    <rect x="430" y="360" width="340" height="680" fill="url(#rubV)"/>
    {bits}
    <rect x="430" y="360" width="340" height="62" fill="#f1e9dc" opacity=".5"/>
  </g>

  <path d="{BODY}" fill="url(#glassEdge)"/>
  <path d="{BODY}" fill="none" stroke="rgba(255,255,255,.4)" stroke-width="1.5"/>
  <g clip-path="url(#bodyclip)">
    <path d="M474 440 C 464 600, 464 850, 478 1014" stroke="rgba(255,255,255,.9)" stroke-width="11" fill="none" stroke-linecap="round"/>
    <path d="M490 440 C 482 600, 482 850, 492 1014" stroke="rgba(255,255,255,.35)" stroke-width="5" fill="none" stroke-linecap="round"/>
    <path d="M728 456 C 738 640, 738 860, 724 1008" stroke="rgba(255,255,255,.28)" stroke-width="6" fill="none" stroke-linecap="round"/>
    <ellipse cx="600" cy="1022" rx="150" ry="22" fill="rgba(255,220,180,.18)"/>
  </g>
</svg>
<div class="label"><img src="data:image/png;base64,{lbl}" alt="Chilli Oil Rub label"/></div>
<div class="curve"></div>
</div>
</body></html>'''
    _m.parseString(html[html.index("<svg"):html.index("</svg>") + 6])
    with open(os.path.join(OUT, f"{region}-rub-jar.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("jar written:", f"{region}-rub-jar.html")


if __name__ == "__main__":
    if (sys.argv[1:] or [""])[0] == "labels":
        labels()
    elif (sys.argv[1:] or [""])[0] == "jars":
        for r in REGIONS:
            jar(r)
    else:
        sys.exit(__doc__)
