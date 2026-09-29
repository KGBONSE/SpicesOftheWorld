from PIL import Image, ImageDraw, ImageFont, ImageEnhance
U='/root/.claude/uploads/8c7b8b3d-bc7c-55e0-adeb-bd8e98e9ab34/'
files=[('9dcca5ca-image.png','AFRICA'),('65187586-image.png','SOUTH ASIA'),('74361d79-image.png','EAST ASIA')]
F='/usr/share/fonts/truetype/google-fonts/'
# --- 1080x1350 post: three bottles
W,H=1080,1350
post=Image.new('RGB',(W,H),(24,14,8));d=ImageDraw.Draw(post)
pw=W//3
for i,(f,lab) in enumerate(files):
    im=Image.open(U+f).convert('RGB'); k=im.width/1500
    # crop a tall strip centred on bottle
    cx=int(690*k); top=int(40*k); bot=int(1950*k); h=bot-top; w=int(h*pw/1050)
    c=im.crop((cx-w//2,top,cx+w//2,bot)).resize((pw,1050),Image.LANCZOS)
    post.paste(c,(i*pw,170))
    t=ImageFont.truetype(F+'Poppins-Medium.ttf',30)
    tw=d.textlength(lab,font=t); d.text((i*pw+(pw-tw)/2,1240),lab,font=t,fill=(255,200,150))
for x in (pw,2*pw): d.line([(x,170),(x,1220)],fill=(24,14,8),width=6)
hd=ImageFont.truetype(F+'Poppins-Bold.ttf',60)
s='One chilli. Three journeys.'; d.text(((W-d.textlength(s,font=hd))/2,50),s,font=hd,fill=(255,246,232))
post.save('fudi-three-oils-post.jpg',quality=93)
# --- profile pic alt: Africa bottle close crop
im=Image.open(U+files[0][0]).convert('RGB'); k=im.width/1493
cx,cy,s=int(680*k),int(1150*k),int(1150*k)
pp=im.crop((cx-s//2,cy-s//2,cx+s//2,cy+s//2)).resize((1080,1080),Image.LANCZOS)
pp.save('fudi-profile-africa-bottle.jpg',quality=95)
m=Image.new('L',(1080,1080),0);ImageDraw.Draw(m).ellipse((0,0,1079,1079),fill=255)
pv=Image.new('RGB',(1080,1080),'white');pv.paste(pp,(0,0),m);pv.resize((300,300)).save('pv2.png')
post.resize((540,675)).save('pv_post.png')
