from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance
G='/usr/share/fonts/truetype/google-fonts/'
U='/mnt/user-data/uploads/'; U2='/root/.claude/uploads/8c7b8b3d-bc7c-55e0-adeb-bd8e98e9ab34/'
DARK=(58,20,8); CREAM=(255,243,226); ORANGE=(240,120,30)
def lora(sz):
    f=ImageFont.truetype(G+'Lora-Variable.ttf',sz); f.set_variation_by_name('Bold'); return f
def pop(sz,w='Medium'): return ImageFont.truetype(G+f'Poppins-{w}.ttf',sz)
W,H=1080,1350
def spaced(d,xy,t,f,fill,sp=6):
    x,y=xy
    for ch in t: d.text((x,y),ch,font=f,fill=fill); x+=d.textlength(ch,font=f)+sp
def wrap(d,text,f,maxw):
    words=text.split(); lines=[]; cur=''
    for w in words:
        t=(cur+' '+w).strip()
        if d.textlength(t,font=f)<=maxw: cur=t
        else: lines.append(cur); cur=w
    lines.append(cur); return lines
def full(photo,centering,eyebrow,head,sub,out,zoom=1.0):
    im=ImageOps.exif_transpose(Image.open(photo)).convert('RGB')
    if zoom!=1.0:
        w,h=im.size; cw,ch=int(w/zoom),int(h/zoom)
        cx=int((w-cw)*centering[0]); cy=int((h-ch)*centering[1]); im=im.crop((cx,cy,cx+cw,cy+ch))
    im=ImageOps.fit(im,(W,H),Image.LANCZOS,centering=centering)
    ov=Image.new('L',(W,H),0); od=ImageDraw.Draw(ov)
    for y in range(H):
        t=max(0,(y-H*0.28)/(H*0.5)); od.line([(0,y),(W,y)],fill=int(242*min(1,t**0.9)))
    for y in range(160): od.line([(0,y),(W,y)],fill=int(120*(1-y/160)))
    im=Image.composite(Image.new('RGB',(W,H),DARK),im,ov); d=ImageDraw.Draw(im)
    spaced(d,(64,56),'FUDI PEOPLE',pop(30,'Bold'),CREAM,7)
    y=H-120
    d.text((64,y+40),'fudipeople.com',font=pop(28,'Regular'),fill=(230,200,170))
    sl=wrap(d,sub,pop(34,'Regular'),W-128)
    y-= 50*len(sl)
    for i,l in enumerate(sl): d.text((64,y+i*50),l,font=pop(34,'Regular'),fill=CREAM)
    hf=lora(96); y-= 30+108*len(head)
    for i,l in enumerate(head): d.text((64,y+i*108),l,font=hf,fill=CREAM)
    y-=62; d.rectangle((64,y+40,124,y+46),fill=ORANGE)
    spaced(d,(64,y-4),eyebrow,pop(28,'Bold'),ORANGE,4)
    im.save(out,quality=93)
def split(photo,cx_frac,eyebrow,head,sub,out):
    im=Image.open(photo).convert('RGB'); s=H/im.height
    im=im.resize((int(im.width*s),H),Image.LANCZOS)
    PW=600; cx=int(im.width*cx_frac)
    ph=im.crop((cx-PW//2,0,cx+PW//2,H))
    c=Image.new('RGB',(W,H),DARK); c.paste(ph,(W-PW,0)); d=ImageDraw.Draw(c)
    TW=W-PW-100
    spaced(d,(56,56),'FUDI PEOPLE',pop(28,'Bold'),CREAM,6)
    ef=pop(24,'Bold'); el=wrap(d,eyebrow,ef,TW)
    y=380
    for i,l in enumerate(el): spaced(d,(56,y+i*36),l,ef,ORANGE,3)
    y+=36*len(el)+14; d.rectangle((56,y,110,y+6),fill=ORANGE); y+=40
    hf=lora(70)
    for l in head: d.text((56,y),l,font=hf,fill=CREAM); y+=84
    y+=24; sf=pop(30,'Regular')
    for l in wrap(d,sub,sf,TW): d.text((56,y),l,font=sf,fill=(240,220,200)); y+=46
    d.text((56,H-90),'fudipeople.com',font=pop(24,'Regular'),fill=(230,200,170))
    c.save(out,quality=93)
full(U+'IMG_3339.jpeg',(0.5,0.45),'FROM OUR FARM IN SIDCUP',['Grown here.','Smoked here.','Bottled here.'],
     'Chilli oil made with chillies from our own London farm.','post1-intro.jpg')
full('smoker.png',(0.5,0.3),'HOW WE DO IT',['Low heat.','Hours of smoke.'],
     'Every chilli is smoked by hand before it goes anywhere near a bottle.','post2-smoker.jpg',zoom=1.15)
split(U2+'9dcca5ca-image.png',0.46,'CHILLI OIL WITH SPICES OF AFRICA',['Sankofa.'],
      'The Adinkra symbol on this label means "go back and fetch it": learn from where you come from. That is how we cook.','post3-africa.jpg')
split(U2+'74361d79-image.png',0.46,'CHILLI OIL WITH SPICES OF EAST ASIA',['Made for','noodles.'],
      'Farm-grown chillies with the spices of East Asia. Spoon it over noodles, dumplings and fried rice.','post4-east-asia.jpg')
# 5 how-to card
c=Image.new('RGB',(W,H),ORANGE); d=ImageDraw.Draw(c)
spaced(d,(64,56),'FUDI PEOPLE',pop(30,'Bold'),DARK,7)
d.text((64,170),'5 ways to use',font=lora(96),fill=DARK); d.text((64,280),'your chilli oil',font=lora(96),fill=DARK)
items=['Drizzled over fried eggs','Stirred into jollof & rice dishes','Tossed through noodles','Spooned onto pizza & flatbreads','Brushed on roast veg']
y=470
for i,t in enumerate(items):
    d.ellipse((64,y,144,y+80),fill=DARK); n=str(i+1); f=lora(48)
    d.text((104-d.textlength(n,font=f)/2,y+8),n,font=f,fill=CREAM)
    d.text((176,y+14),t,font=pop(42,'Medium'),fill=DARK); y+=132
d.text((64,H-100),'Save this for dinner tonight',font=pop(32,'Bold'),fill=CREAM)
c.save('post5-how-to-use.jpg',quality=93)
# preview sheet
from PIL import Image as I
names=['post1-intro','post2-smoker','post3-africa','post4-east-asia','post5-how-to-use']
sh=I.new('RGB',(3*360+40,2*450+30),(245,240,235))
for i,n in enumerate(names):
    t=I.open(n+'.jpg').resize((360,450)); sh.paste(t,(10+(i%3)*370,10+(i//3)*460))
sh.save('preview.png')
SA=U2+'9209e4d4-image.png'
split(SA,0.46,'CHILLI OIL WITH SPICES OF SOUTH ASIA',['Warm,','fragrant','heat.'],
      'Farm-grown chillies with the spices of South Asia. Made for dals, curries, parathas and eggs.','post6-south-asia.jpg')
# three oils
files=[(U2+'9dcca5ca-image.png','AFRICA'),(SA,'SOUTH ASIA'),(U2+'74361d79-image.png','EAST ASIA')]
c=Image.new('RGB',(W,H),DARK); d=ImageDraw.Draw(c); pw=W//3
for i,(f,lab) in enumerate(files):
    im=Image.open(f).convert('RGB'); k=im.width/1500
    cx=int(690*k); top=int(40*k); bot=int(1950*k); h=bot-top; w=int(h*pw/1000)
    c.paste(im.crop((cx-w//2,top,cx+w//2,bot)).resize((pw,1000),Image.LANCZOS),(i*pw,200))
    t=pop(30,'Bold'); tw=d.textlength(lab,font=t); d.text((i*pw+(pw-tw)/2,1235),lab,font=t,fill=ORANGE)
for x in (pw,2*pw): d.line([(x,200),(x,1200)],fill=DARK,width=6)
hf=lora(64); s='One chilli. Three journeys.'; d.text(((W-d.textlength(s,font=hf))/2,70),s,font=hf,fill=CREAM)
c.save('post0-three-oils.jpg',quality=93)
sh=Image.new('RGB',(2*360+30,450+20),(245,240,235))
for i,n in enumerate(['post6-south-asia','post0-three-oils']):
    sh.paste(Image.open(n+'.jpg').resize((360,450)),(10+i*370,10))
sh.save('preview2.png')
