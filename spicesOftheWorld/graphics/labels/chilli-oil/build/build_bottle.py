"""Wraps a rendered flat label PNG onto a clear-glass 150 ml bottle mockup.

Usage:  python build_bottle.py <label-png> <out-html>
The label PNG path and out-html path are resolved relative to the parent
graphics/labels/chilli-oil/ directory when not absolute.
"""
import base64
import os
import sys
import xml.dom.minidom as _m

HERE = os.path.dirname(os.path.abspath(__file__))
LABELS = os.path.dirname(HERE)


def _resolve(p):
    return p if os.path.isabs(p) else os.path.join(LABELS, p)


label_png = _resolve(sys.argv[1] if len(sys.argv) > 1 else "africa-label.png")
out_html = _resolve(sys.argv[2] if len(sys.argv) > 2 else "africa-bottle.html")

LBL = base64.b64encode(open(label_png, "rb").read()).decode()

LW = 284
LH = round(LW / 0.813)
LX = 600 - LW // 2
LY = 452

BODY = ("M572 300 C 572 322, 476 348, 458 424 L 458 966 "
        "Q 458 1000 492 1000 L 708 1000 Q 742 1000 742 966 "
        "L 742 424 C 724 348, 628 322, 628 300 Z")

import random
random.seed(7)
flakes = ""
for _ in range(26):
    x = random.uniform(475, 725); y = random.uniform(360, 980)
    r = random.uniform(2.2, 5.5)
    flakes += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="rgba(120,22,8,{random.uniform(.28,.6):.2f})"/>'

HTML = f'''<!DOCTYPE html><html><head><meta charset="UTF-8"/>
<title>Fudi People &mdash; Chilli Oil 150ml bottle</title>
<style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  html,body{{width:100%;height:100%}}
  body{{display:flex;align-items:center;justify-content:center;
    background:radial-gradient(circle at 50% 38%, #f7f3ec 0%, #ece3d4 62%, #e0d6c4 100%)}}
  .stage{{position:relative;width:1200px;height:1200px}}
  .stage>*{{position:absolute;left:0;top:0}}
  .label{{width:{LW}px;left:{LX}px;top:{LY}px;z-index:6;border-radius:3px;overflow:hidden;
    box-shadow:0 2px 10px rgba(60,20,0,.28);
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
    <linearGradient id="oil" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#8f1f0b"/><stop offset="0.10" stop-color="#b8330f"/>
      <stop offset="0.30" stop-color="#e05f22"/><stop offset="0.50" stop-color="#f6903f"/>
      <stop offset="0.70" stop-color="#dd571f"/><stop offset="0.90" stop-color="#a5280c"/>
      <stop offset="1" stop-color="#7c1907"/>
    </linearGradient>
    <linearGradient id="oilV" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#ffb063" stop-opacity=".55"/>
      <stop offset="0.18" stop-color="#ffb063" stop-opacity="0"/>
      <stop offset="0.75" stop-color="#5c1404" stop-opacity="0"/>
      <stop offset="1" stop-color="#5c1404" stop-opacity=".5"/>
    </linearGradient>
    <linearGradient id="glassEdge" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#ffffff" stop-opacity=".0"/>
      <stop offset="0.02" stop-color="#ffffff" stop-opacity=".85"/>
      <stop offset="0.07" stop-color="#ffffff" stop-opacity=".0"/>
      <stop offset="0.90" stop-color="#000000" stop-opacity=".0"/>
      <stop offset="0.97" stop-color="#3a1206" stop-opacity=".38"/>
      <stop offset="1" stop-color="#3a1206" stop-opacity=".0"/>
    </linearGradient>
    <linearGradient id="cork2" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#7c5530"/><stop offset=".24" stop-color="#bd9058"/>
      <stop offset=".5" stop-color="#d9b57e"/><stop offset=".76" stop-color="#b0824b"/>
      <stop offset="1" stop-color="#6f4a28"/>
    </linearGradient>
    <clipPath id="bodyclip"><path d="{BODY}"/></clipPath>
  </defs>

  <ellipse cx="600" cy="1030" rx="196" ry="24" fill="rgba(70,40,15,.22)"/>

  <rect x="556" y="150" width="88" height="30" rx="4" fill="#5a3c20"/>
  <rect x="560" y="176" width="80" height="70" rx="6" fill="url(#cork2)"/>
  <rect x="560" y="176" width="80" height="70" rx="6" fill="none" stroke="rgba(90,60,30,.5)" stroke-width="1.5"/>
  <line x1="576" y1="182" x2="576" y2="240" stroke="rgba(120,85,45,.4)" stroke-width="2"/>
  <line x1="612" y1="182" x2="612" y2="240" stroke="rgba(120,85,45,.35)" stroke-width="2"/>

  <rect x="572" y="242" width="56" height="60" fill="url(#oil)"/>
  <rect x="572" y="242" width="56" height="60" fill="url(#glassEdge)"/>

  <g clip-path="url(#bodyclip)">
    <rect x="440" y="330" width="320" height="700" fill="url(#oil)"/>
    <rect x="440" y="330" width="320" height="700" fill="url(#oilV)"/>
    {flakes}
    <ellipse cx="600" cy="340" rx="150" ry="16" fill="#ffcf9c" opacity=".35"/>
    <rect x="440" y="300" width="320" height="40" fill="#f7f3ec"/>
    <ellipse cx="600" cy="340" rx="150" ry="15" fill="none" stroke="#ffd9ad" stroke-width="3" opacity=".6"/>
  </g>

  <path d="{BODY}" fill="url(#glassEdge)"/>
  <path d="{BODY}" fill="none" stroke="rgba(255,255,255,.35)" stroke-width="1.5"/>
  <g clip-path="url(#bodyclip)">
    <path d="M486 356 C 478 520, 478 800, 492 986" stroke="rgba(255,255,255,.9)" stroke-width="10" fill="none" stroke-linecap="round"/>
    <path d="M500 356 C 494 520, 494 800, 504 986" stroke="rgba(255,255,255,.35)" stroke-width="5" fill="none" stroke-linecap="round"/>
    <path d="M712 372 C 720 560, 720 820, 706 980" stroke="rgba(255,255,255,.28)" stroke-width="6" fill="none" stroke-linecap="round"/>
    <ellipse cx="600" cy="992" rx="150" ry="26" fill="rgba(255,220,180,.20)"/>
  </g>

  <text x="600" y="958" text-anchor="middle" font-family="Arial, Helvetica, sans-serif"
        font-size="23" fill="rgba(255,255,255,.75)" letter-spacing="3">150 ml</text>
</svg>
<div class="label"><img src="data:image/png;base64,{LBL}" alt="Chilli Oil label"/></div>
<div class="curve"></div>
</div>
</body></html>'''

_m.parseString(HTML[HTML.index("<svg"):HTML.index("</svg>") + 6])
with open(out_html, "w", encoding="utf-8") as f:
    f.write(HTML)
print("bottle written:", os.path.basename(out_html), "from", os.path.basename(label_png))
