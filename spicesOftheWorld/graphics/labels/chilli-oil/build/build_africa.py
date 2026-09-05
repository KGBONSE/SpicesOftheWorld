"""Generates africa-label.html — heart/rooster emblem, kente borders."""
from _assets import logo_black, emblem, out_path

LOGO = logo_black()
ESVG = emblem("fudi-heart-emblem")

BORDER = '''<svg viewBox="0 0 132 1230" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
<rect width="132" height="1230" fill="#141312"/>
<defs><g id="cell">
  <path d="M4 12 L64 40 L4 68 Z" fill="#c0342b"/>
  <path d="M128 20 L72 44 L128 72 Z" fill="#1f7a3d"/>
  <ellipse cx="66" cy="104" rx="50" ry="12" fill="none" stroke="#e2902f" stroke-width="6"/>
  <circle cx="66" cy="104" r="7" fill="#c0342b"/>
  <path d="M14 140 q52 -30 104 0" stroke="#1f7a3d" stroke-width="7" fill="none"/>
  <circle cx="30" cy="168" r="9" fill="#e2902f"/><circle cx="66" cy="176" r="9" fill="#c0342b"/><circle cx="102" cy="168" r="9" fill="#1f7a3d"/>
  <path d="M8 196 h116" stroke="#e2902f" stroke-width="5"/>
</g></defs>
<use href="#cell" y="0"/><use href="#cell" y="205"/><use href="#cell" y="410"/>
<use href="#cell" y="615"/><use href="#cell" y="820"/><use href="#cell" y="1025"/>
</svg>'''

_C = '''<g>
  <path d="M30 6 C 45 26, 47 62, 36 96 C 33 106, 27 122, 25 124 C 24 112, 27 100, 25 92 C 15 62, 13 30, 21 12 C 23 7, 27 2, 30 6 Z" fill="url(#cr)"/>
  <path d="M27 20 C 34 42, 34 74, 29 96" stroke="#ffe0d8" stroke-opacity=".5" stroke-width="3" fill="none" stroke-linecap="round"/>
  <path d="M30 6 C 27 0, 22 -3, 15 0 C 11 2, 12 8, 17 8 C 13 5, 21 3, 23 7" fill="#3aa043"/>
  <path d="M20 2 C 12 -3, 6 1, 3 -5" stroke="#3aa043" stroke-width="4.5" fill="none" stroke-linecap="round"/>
</g>'''
CHILLIES = f'''<svg class="chillies" viewBox="0 0 200 120" xmlns="http://www.w3.org/2000/svg">
  <defs><linearGradient id="cr" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#ef5142"/><stop offset=".45" stop-color="#cc2418"/><stop offset="1" stop-color="#8f130d"/>
  </linearGradient></defs>
  <g transform="rotate(-58 100 60) translate(70 -8)">{_C}</g>
  <g transform="rotate(58 100 60) translate(70 -8)">{_C}</g>
</svg>'''

HTML = f'''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"/>
<title>Fudi People &mdash; Chilli Oil with Spices of Africa (label)</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Kaushan+Script&family=Sacramento&display=swap" rel="stylesheet">
<style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  html,body{{width:100%;height:100%}}
  body{{display:flex;align-items:center;justify-content:center;background:#fff}}
  .label{{position:relative;width:1000px;height:1230px;overflow:hidden;background:#ff7a08;font-family:"Kaushan Script",cursive}}
  .label::before{{content:"";position:absolute;left:50%;top:26%;width:2400px;height:2400px;transform:translate(-50%,-50%);
    background:repeating-conic-gradient(from 0deg,rgba(255,214,160,.13) 0deg 4.5deg, rgba(255,214,160,0) 4.5deg 12deg);}}
  .label::after{{content:"";position:absolute;inset:-10%;
    background:radial-gradient(circle at 50% 28%, #ff9a33 0%, #ff7a08 46%, #e9670a 100%);mix-blend-mode:multiply;opacity:.5;}}
  .border{{position:absolute;top:0;bottom:0;width:132px;background:#141312;z-index:3}}
  .border.l{{left:0}} .border.r{{right:0;transform:scaleX(-1)}}
  .border svg{{width:100%;height:100%;display:block}}
  .col{{position:absolute;left:132px;right:132px;top:0;bottom:0;z-index:2;display:flex;flex-direction:column;align-items:center;text-align:center;padding:66px 30px 40px}}
  .logo{{width:35%;margin-bottom:30px}}
  .emblem-wrap{{position:relative;width:66%;aspect-ratio:1/1;display:flex;align-items:center;justify-content:center}}
  .emblem-wrap::before{{content:"";position:absolute;inset:0;border-radius:50%;border:3px solid #1a0d08}}
  .emblem{{width:90%;display:block}}
  .chillies{{width:35%;margin-top:-58px;margin-bottom:-6px;filter:drop-shadow(0 5px 6px rgba(80,8,0,.30))}}
  .title{{font-size:150px;line-height:.86;color:#180b06}}
  .sub{{font-family:"Sacramento",cursive;font-size:62px;line-height:1;color:#241108;margin-top:12px}}
  .spacer{{flex:1}}
</style></head><body>
<div class="label">
  <div class="border l">{BORDER}</div><div class="border r">{BORDER}</div>
  <div class="col">
    <img class="logo" src="data:image/png;base64,{LOGO}" alt="Fudi People"/>
    <div class="emblem-wrap"><img class="emblem" src="data:image/svg+xml;base64,{ESVG}" alt=""/></div>
    {CHILLIES}
    <div class="title">Chilli&nbsp;Oil</div>
    <div class="sub">with Spices of Africa</div>
    <div class="spacer"></div>
  </div>
</div></body></html>'''

with open(out_path("africa-label.html"), "w", encoding="utf-8") as f:
    f.write(HTML)
print("africa-label.html written", len(HTML))
