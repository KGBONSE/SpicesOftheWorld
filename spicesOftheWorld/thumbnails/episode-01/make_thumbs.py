import sys
sys.path.insert(0,'/home/claude/spicesoftheworld/spicesOftheWorld/video/episode-01')
from finish_v3 import font, MARIGOLD, CREAM, INK, GOLD
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
W,H=1280,720
def load(t, crop=None):
    im=Image.open(f'frames/f_{t}.png').convert('RGB')
    if crop: im=im.crop(crop)
    return im
def fill(im,w,h):
    k=max(w/im.width,h/im.height); im=im.resize((int(im.width*k+1),int(im.height*k+1)),Image.LANCZOS)
    x=(im.width-w)//2; y=(im.height-h)//2; im=im.crop((x,y,x+w,y+h))
    im=im.filter(ImageFilter.UnsharpMask(2,80,2))
    return ImageEnhance.Color(ImageEnhance.Contrast(im).enhance(1.08)).enhance(1.12)
def shadow_text(img, xy, t, f, fill, anchor='la', blur=10, off=(0,6)):
    sh=Image.new('RGBA',img.size,(0,0,0,0)); ImageDraw.Draw(sh).text((xy[0]+off[0],xy[1]+off[1]),t,font=f,fill=(0,0,0,200),anchor=anchor)
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur))); ImageDraw.Draw(img).text(xy,t,font=f,fill=fill,anchor=anchor)
def grad(img, top=True, strength=200, frac=0.55):
    g=Image.new('RGBA',img.size,(0,0,0,0)); d=ImageDraw.Draw(g); n=int(img.height*frac)
    for i in range(n):
        a=int(strength*(1-i/n)**1.6); y=i if top else img.height-1-i
        d.line([(0,y),(img.width,y)],fill=(30,8,6,a))
    img.alpha_composite(g)
def logo_bug(img):
    lg=Image.open('/home/claude/spicesoftheworld/spicesOftheWorld/brand-assets/logo/fudi-people-logo-cream-bold.png').convert('RGBA')
    lg=lg.resize((int(lg.width*70/lg.height),70),Image.LANCZOS); img.alpha_composite(lg,(W-lg.width-28,H-lg.height-22))

# A: skewer heap + origin claim (no face)
a=fill(load(395,(60,40,854,480)),W,H).convert('RGBA'); grad(a,True,215,0.6)
f1=font('ExtraBold',118)
shadow_text(a,(54,40),'THE SPICE',f1,CREAM); d=ImageDraw.Draw(a)
x=54+d.textlength('THE ',font=f1)
ImageDraw.Draw(a).text((x,40),'SPICE',font=f1,fill=MARIGOLD)
shadow_text(a,(54,160),'EUROPE FORGOT',f1,CREAM)
logo_bug(a); a.convert('RGB').save('A_spice_europe_forgot.jpg',quality=92)

# B: ingredient catalogue grid + "WHAT'S IN YAJI?"
tiles=[(41,'GRAINS OF PARADISE'),(203,'GRAINS OF SELIM'),(253,'DRIED CHILLIES'),(257.5,'KULI-KULI'),(261,'GINGER'),(269.5,'= YAJI')]
b=Image.new('RGBA',(W,H),(58,18,16,255)); top=150; tw,th=W//3,(H-top)//2
for i,(t,lab) in enumerate(tiles):
    tile=fill(load(t,(110,40,854,420)),tw-6,th-6).convert('RGBA')
    b.alpha_composite(tile,((i%3)*tw+3, top+(i//3)*th+3))
    fl=font('ExtraBold',26); bx=(i%3)*tw+16; by=top+(i//3)*th+th-52
    d=ImageDraw.Draw(b); w=d.textlength(lab,font=fl)+28
    d.rounded_rectangle((bx,by,bx+w,by+40),20,fill=MARIGOLD if lab=='= YAJI' else (107,27,31,235))
    d.text((bx+14,by+20),lab,font=fl,fill=INK if lab=='= YAJI' else CREAM,anchor='lm')
fb=font('ExtraBold',96)
d=ImageDraw.Draw(b); t1="WHAT'S IN "; wt=d.textlength(t1+'YAJI?',font=fb); x0=(W-wt)/2
d.text((x0,22),t1,font=fb,fill=CREAM); d.text((x0+d.textlength(t1,font=fb),22),'YAJI?',font=fb,fill=MARIGOLD)
b.convert('RGB').save('B_whats_in_yaji.jpg',quality=92)

# C: one spice, two names — suya heap with SUYA / CHINCHINGA split + Kofi face badge
c=fill(load(398,(60,40,854,480)),W,H).convert('RGBA'); grad(c,False,230,0.55)
fc=font('ExtraBold',104); fs=font('Bold',40)
shadow_text(c,(W/2,500),'SUYA = CHINCHINGA',fc,CREAM,anchor='mm')
shadow_text(c,(W/2,600),'ONE SPICE  ·  TWO COUNTRIES',fs,GOLD,anchor='mm')
face=load(8,(290,40,610,360)).resize((250,250),Image.LANCZOS)
m=Image.new('L',(250,250),0); ImageDraw.Draw(m).ellipse((0,0,249,249),fill=255)
ring=Image.new('RGBA',(266,266),(0,0,0,0)); ImageDraw.Draw(ring).ellipse((0,0,265,265),fill=MARIGOLD)
c.alpha_composite(ring,(W-310,34)); c.paste(face,(W-302,42),m)
c.convert('RGB').save('C_suya_chinchinga_face.jpg',quality=92)
