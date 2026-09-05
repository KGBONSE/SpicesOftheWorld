"""Generates eastasia-label.html — coiled dragon emblem, cloud pattern, Chinese line (辣油)."""
import base64
from _assets import logo_maroon, emblem, out_path

LOGO = logo_maroon()
DRAGON = emblem("fudi-dragon-emblem")

# subtle chinese cloud-scroll pattern, tone-on-tone
CLOUDS = '''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1230">
<rect width="1000" height="1230" fill="#ff7b00"/>
<g fill="none" stroke="#e86a00" stroke-width="7" opacity="0.55">
'''
for row in range(9):
    for col in range(6):
        x = col * 190 + (95 if row % 2 else 0) - 60
        y = row * 150 + 40
        CLOUDS += (f'<path d="M{x} {y} q22 -26 46 -6 q10 -22 34 -10 q22 -6 24 20 '
                   f'q22 4 12 26 q-30 14 -52 0 q-26 12 -46 -6 q-22 -10 -8 -34 Z"/>')
CLOUDS += '</g></svg>'
CLOUDS_B64 = base64.b64encode(CLOUDS.encode()).decode()

HTML = f'''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"/>
<title>Fudi People &mdash; Chilli Oil with Spices of East Asia (label)</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Kaushan+Script&family=Ma+Shan+Zheng&family=Sacramento&display=swap" rel="stylesheet">
<style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  html,body{{width:100%;height:100%}}
  body{{display:flex;align-items:center;justify-content:center;background:#fff}}
  .label{{position:relative;width:1000px;height:1230px;overflow:hidden;background:#ff7b00;
    font-family:"Kaushan Script",cursive}}
  .bg{{position:absolute;inset:0;z-index:0;opacity:.5}}
  .bg img{{width:100%;height:100%;display:block}}
  .ghost{{position:absolute;z-index:1;opacity:.10}}
  .ghost img{{width:100%;display:block;filter:brightness(0) saturate(100%) invert(9%) sepia(70%) saturate(3000%) hue-rotate(350deg)}}
  .ghost.tl{{width:520px;left:-190px;top:60px}}
  .ghost.br{{width:520px;right:-190px;bottom:120px;transform:scaleX(-1)}}
  .frame{{position:absolute;inset:16px;border:10px solid #7d1e12;z-index:4}}
  .frame::after{{content:"";position:absolute;inset:5px;border:2px solid rgba(125,30,18,.55)}}
  .col{{position:absolute;inset:0;z-index:3;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;
    padding:58px 90px 76px}}
  .logo{{width:30%;margin-bottom:14px}}
  .disc{{position:relative;width:55%;aspect-ratio:1/1;border-radius:50%;background:#e0401f;
    display:flex;align-items:center;justify-content:center;
    box-shadow:0 0 0 6px rgba(125,30,18,.9), inset 0 0 40px rgba(120,20,10,.4);margin-bottom:8px}}
  .disc img{{width:96%}}
  .title{{font-size:124px;line-height:.9;color:#f7edd6;text-shadow:0 3px 0 rgba(125,30,18,.55)}}
  .cjk{{font-family:"Ma Shan Zheng",cursive;font-size:86px;line-height:1;color:#f7edd6;margin-top:2px;
    text-shadow:0 3px 0 rgba(125,30,18,.5)}}
  .sub{{font-family:"Sacramento",cursive;font-size:50px;line-height:1;color:#ffe2b0;margin-top:12px}}
  .spacer{{display:none}}
</style></head><body>
<div class="label">
  <div class="bg"><img src="data:image/svg+xml;base64,{CLOUDS_B64}" alt=""/></div>
  <div class="ghost tl"><img src="data:image/svg+xml;base64,{DRAGON}" alt=""/></div>
  <div class="ghost br"><img src="data:image/svg+xml;base64,{DRAGON}" alt=""/></div>
  <div class="frame"></div>
  <div class="col">
    <img class="logo" src="data:image/png;base64,{LOGO}" alt="Fudi People"/>
    <div class="disc"><img src="data:image/svg+xml;base64,{DRAGON}" alt=""/></div>
    <div class="title">Chilli&nbsp;Oil</div>
    <div class="cjk">&#36771;&#27833;</div>
    <div class="sub">with Spices of East Asia</div>
    <div class="spacer"></div>
  </div>
</div></body></html>'''

with open(out_path("eastasia-label.html"), "w", encoding="utf-8") as f:
    f.write(HTML)
print("eastasia-label.html written", len(HTML))
