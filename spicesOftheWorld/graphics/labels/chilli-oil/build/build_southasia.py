"""Generates southasia-label.html — seated Buddha emblem, ghost-face bg, Hindi line."""
from _assets import logo_maroon, emblem, out_path

LOGO = logo_maroon()
EMB = emblem("fudi-buddha-emblem")

HTML = f'''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"/>
<title>Fudi People &mdash; Chilli Oil with Spices of South Asia (label)</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Kaushan+Script&family=Tiro+Devanagari+Hindi:ital@0;1&family=Sacramento&display=swap" rel="stylesheet">
<style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  html,body{{width:100%;height:100%}}
  body{{display:flex;align-items:center;justify-content:center;background:#fff}}
  .label{{position:relative;width:1000px;height:1230px;overflow:hidden;background:#ff7b00;
    font-family:"Kaushan Script",cursive}}
  /* faint diagonal ray texture, like the artwork */
  .label::before{{content:"";position:absolute;left:50%;top:34%;width:2600px;height:2600px;transform:translate(-50%,-50%);
    background:repeating-conic-gradient(from 0deg,rgba(255,205,150,.10) 0deg 4deg, rgba(255,205,150,0) 4deg 11deg);}}
  /* ghosted buddha watermarks */
  .ghost{{position:absolute;top:120px;width:560px;opacity:.09;z-index:1}}
  .ghost img{{width:100%;display:block;filter:brightness(0) saturate(100%) invert(12%) sepia(60%) saturate(2500%) hue-rotate(350deg)}}
  .ghost.l{{left:-230px}} .ghost.r{{right:-230px;transform:scaleX(-1)}}
  .frame{{position:absolute;inset:16px;border:10px solid #7d1e12;z-index:4}}
  .frame::after{{content:"";position:absolute;inset:5px;border:2px solid rgba(125,30,18,.5)}}
  .col{{position:absolute;inset:0;z-index:3;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;
    padding:60px 90px 78px}}
  .logo{{width:30%;margin-bottom:14px}}
  .emblem{{width:55%;display:block;margin-bottom:4px}}
  .title{{font-size:124px;line-height:.9;color:#7d1e12}}
  .hindi{{font-family:"Tiro Devanagari Hindi",serif;font-size:54px;line-height:1.1;color:#7d1e12;margin-top:6px}}
  .sub{{font-family:"Sacramento",cursive;font-size:50px;line-height:1;color:#8a2a18;margin-top:14px}}
  .spacer{{display:none}}
</style></head><body>
<div class="label">
  <div class="ghost l"><img src="data:image/svg+xml;base64,{EMB}" alt=""/></div>
  <div class="ghost r"><img src="data:image/svg+xml;base64,{EMB}" alt=""/></div>
  <div class="frame"></div>
  <div class="col">
    <img class="logo" src="data:image/png;base64,{LOGO}" alt="Fudi People"/>
    <img class="emblem" src="data:image/svg+xml;base64,{EMB}" alt=""/>
    <div class="title">Chilli&nbsp;Oil</div>
    <div class="hindi">&#2350;&#2367;&#2352;&#2381;&#2330; &#2325;&#2366; &#2340;&#2375;&#2354;</div>
    <div class="sub">with Spices of South Asia</div>
    <div class="spacer"></div>
  </div>
</div></body></html>'''

with open(out_path("southasia-label.html"), "w", encoding="utf-8") as f:
    f.write(HTML)
print("southasia-label.html written", len(HTML))
