from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps
U='/mnt/user-data/uploads/'
# ---- profile picture
im=ImageOps.exif_transpose(Image.open(U+'IMG_3339.jpeg')).convert('RGB')
cx,cy,s=966,1010,1932
pp=im.crop((cx-s//2,cy-s//2,cx+s//2,cy+s//2)).resize((1080,1080),Image.LANCZOS)
pp=ImageEnhance.Color(pp).enhance(1.08)
pp.save('fudi-profile-picture.jpg',quality=95)
m=Image.new('L',(1080,1080),0);ImageDraw.Draw(m).ellipse((0,0,1079,1079),fill=255)
prev=Image.new('RGB',(1080,1080),'white');prev.paste(pp,(0,0),m);prev.resize((400,400)).save('preview-circle.png')
# ---- banner 2560x1440
W,H=2560,1440
sm=Image.open(U+'IMG_4946.JPG').convert('RGB')
racks=sm.crop((0,230,1080,880))  # chilli racks, above existing text overlay
bg=ImageOps.fit(racks,(W,H),Image.LANCZOS,centering=(0.5,0.45))
bg=bg.filter(ImageFilter.GaussianBlur(3))
bg=ImageEnhance.Color(bg).enhance(1.15)
# dark overlay, stronger in centre band for legibility
ov=Image.new('L',(W,H),0);d=ImageDraw.Draw(ov)
for y in range(H):
    dist=abs(y-H/2)/(H/2)
    d.line([(0,y),(W,y)],fill=int(max(120,235-230*dist)))
bg=Image.composite(Image.new('RGB',(W,H),(18,10,6)),bg,ov)
d=ImageDraw.Draw(bg)
F='/usr/share/fonts/truetype/google-fonts/'
title=ImageFont.truetype(F+'Poppins-Bold.ttf',190)
sub=ImageFont.truetype(F+'Poppins-Medium.ttf' ,58) if __import__('os').path.exists(F+'Poppins-Medium.ttf') else ImageFont.truetype(F+'Poppins-Regular.ttf',58)
def ctext(t,f,y,fill,spacing=0):
    w=d.textlength(t,font=f)+spacing*(len(t)-1)
    x=(W-w)/2
    if spacing:
        for ch in t:
            d.text((x,y),ch,font=f,fill=fill);x+=d.textlength(ch,font=f)+spacing
    else: d.text((x,y),t,font=f,fill=fill)
ctext('FUDI PEOPLE',title,H/2-175,(255,246,232),spacing=18)
d.rectangle((W/2-60,H/2+62,W/2+60,H/2+70),fill=(240,110,40))
ctext('Grown & smoked in Sidcup, London',sub,H/2+95,(255,214,170))
bg.save('fudi-youtube-banner.jpg',quality=93)
# safe-area preview
p=bg.copy();pd=ImageDraw.Draw(p)
pd.rectangle(((W-1546)/2,(H-423)/2,(W+1546)/2,(H+423)/2),outline=(0,255,120),width=6)
p.resize((1280,720)).save('preview-banner.png')
