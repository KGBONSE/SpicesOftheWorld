"""Episode 2 thumbnail variants (1280x720). Usage (portrait 1080x1920 pot frame): python make_thumbs.py POT.png PLATE.jpeg OUTDIR"""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
pot_p, plate_p, out = sys.argv[1:4]
W,H=1280,720
def grade(im, color=1.55, contrast=1.18, warm=True):
    im=ImageEnhance.Color(im).enhance(color); im=ImageEnhance.Contrast(im).enhance(contrast)
    if warm:
        r,g,b=im.split(); r=r.point(lambda v:min(255,int(v*1.12))); b=b.point(lambda v:int(v*0.86)); im=Image.merge("RGB",(r,g,b))
    return ImageEnhance.Sharpness(im).enhance(1.5)
pot_full=Image.open(pot_p).convert("RGB")          # landscape 1920x1080 frame with the whole pot
bgp=pot_full.resize((1280,720),Image.LANCZOS).filter(ImageFilter.GaussianBlur(30))
fg=pot_full.crop((120,0,1800,1080)).resize((900,578),Image.LANCZOS)
pot=bgp.copy(); pot.paste(fg,(0,71))
pot=grade(pot,1.12,1.1,warm=False)
r,g,b_=pot.split(); pot=Image.merge("RGB",(r.point(lambda v:min(255,int(v*1.04))),g,b_.point(lambda v:int(v*0.95))))
plate=Image.open(plate_p).convert("RGB").crop((420,0,3444,3024)).resize((H,H),Image.LANCZOS)
plate=grade(plate,1.25,1.12,warm=False)
F=lambda s:ImageFont.truetype("C:/Windows/Fonts/impact.ttf",s)
def text(d,xy,t,size,fill,stroke=10):
    d.text(xy,t,font=F(size),fill=fill,stroke_width=stroke,stroke_fill=(0,0,0))
def base():
    c=Image.new("RGB",(W,H),(20,12,8)); c.paste(pot,(0,0))
    m=Image.new("L",(W,H),0); ImageDraw.Draw(m).polygon([(900,0),(W,0),(W,H),(740,H)],fill=255)
    layer=Image.new("RGB",(W,H)); layer.paste(plate,(680,0)); c.paste(layer,(0,0),m)
    d=ImageDraw.Draw(c); d.line([(900,0),(740,H)],fill=(255,255,255),width=8)
    return c
# A: stacked words top-left, white / yellow
a=base(); d=ImageDraw.Draw(a)
text(d,(30,10),"NOT NIGERIA.",118,(255,255,255)); text(d,(30,125),"NOT GHANA.",118,(255,214,0))
a.save(f"{out}/thumb_A_stacked.png")
# B: dark gradient band at bottom, words across
b=base(); g=Image.new("RGBA",(W,H),(0,0,0,0)); gd=ImageDraw.Draw(g)
for y in range(H-300,H): gd.line([(0,y),(W,y)],fill=(0,0,0,int(235*(y-(H-300))/300)))
b=Image.alpha_composite(b.convert("RGBA"),g).convert("RGB"); d=ImageDraw.Draw(b)
text(d,(30,H-275),"NOT NIGERIA.",118,(255,255,255)); text(d,(30,H-150),"NOT GHANA.",118,(255,214,0))
b.save(f"{out}/thumb_B_bottom.png")
# C: Senegal colours bar + words with red cross-out feel
c=base(); d=ImageDraw.Draw(c)
for i,col in enumerate([(0,133,63),(253,239,66),(227,27,35)]): d.rectangle([0,i*14,W,i*14+14],fill=col)
text(d,(30,60),"NOT NIGERIA.",112,(255,255,255)); text(d,(30,170),"NOT GHANA.",112,(255,255,255))
d.text((30,335),"THE REAL JOLLOF?",font=F(64),fill=(253,239,66),stroke_width=7,stroke_fill=(0,0,0))
c.save(f"{out}/thumb_C_flag.png")
# D: two statements + red "SO WHICH ONE?" strip (curiosity gap)
d_=base(); d=ImageDraw.Draw(d_)
text(d,(30,10),"NOT NIGERIA.",118,(255,255,255)); text(d,(30,125),"NOT GHANA.",118,(255,214,0))
d.rounded_rectangle([30,262,620,350],radius=10,fill=(214,30,30),outline=(255,255,255),width=5)
d.text((50,264),"SO WHICH ONE?",font=F(78),fill=(255,255,255),stroke_width=3,stroke_fill=(0,0,0))
d_.save(f"{out}/thumb_D_which_one.png")
