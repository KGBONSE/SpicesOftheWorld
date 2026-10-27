"""Ep1 Shorts (9:16) cut from v15 with burned-in captions (script text aligned to word timings).
usage: python make_shorts.py 1|2   -> out/ep01_short_0N.mp4"""
import subprocess, os, sys, re, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from align import align
REPO="/home/claude/spicesoftheworld/spicesOftheWorld"
SRC=f"{REPO}/video/episode-01/out/Spices_of_the_World_Ep1_v15.mp4"
FONT=f"{REPO}/video/episode-01/fonts/Inter-ExtraBold.otf"; FONTM=f"{REPO}/video/episode-01/fonts/Inter-SemiBold.otf"
OUT=os.path.dirname(os.path.abspath(__file__)); W,H=1080,1920
MAROON=(110,31,42); ORANGE=(224,130,30); CREAM=(250,243,232)
def F(p,s): return ImageFont.truetype(p,s)
def pill(txt,sub,path):
    im=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    sz=78
    while d.textlength(txt,font=F(FONT,sz))>880: sz-=2
    f=F(FONT,sz); fs=F(FONTM,40); bw=d.textlength(txt,font=f)+90; x0=(W-bw)/2; y0=430
    d.rounded_rectangle([x0,y0,x0+bw,y0+150],34,fill=MAROON+(235,)); d.text((W/2,y0+75),txt,font=f,fill=CREAM,anchor="mm")
    if sub:
        sw=d.textlength(sub,font=fs)+60; d.rounded_rectangle([(W-sw)/2,y0+170,(W+sw)/2,y0+235],30,fill=ORANGE+(240,))
        d.text((W/2,y0+203),sub,font=fs,fill=(255,255,255),anchor="mm")
    im.save(path)
def endcard(ep_line,l1,l2,l3,path):
    im=Image.new("RGB",(W,H),MAROON); d=ImageDraw.Draw(im)
    d.text((W/2,700),"FULL EPISODE",font=F(FONT,96),fill=CREAM,anchor="mm")
    d.text((W/2,820),ep_line,font=F(FONTM,52),fill=ORANGE,anchor="mm")
    for y,t,fo,sz in [(980,l1,FONT,62),(1060,l2,FONTM,50),(1125,l3,FONTM,50)]:
        if t: d.text((W/2,y),t,font=F(fo,sz),fill=CREAM,anchor="mm")
    d.text((W/2,1330),"Watch the full episode on the channel",font=F(FONTM,46),fill=ORANGE,anchor="mm"); im.save(path)
def chunks(words):
    out=[];cur=[]
    for w,s,e in words:
        cur.append((w,s,e))
        txt=" ".join(x[0] for x in cur)
        if re.search(r"[,.;:!?—]$",w) and len(cur)>=3 or len(cur)>=6 or len(txt)>=34:
            out.append(cur);cur=[]
    if cur: out.append(cur)
    return out
def cap_png(text,path):
    im=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(im); f=F(FONT,66)
    words=text.replace("—","").split(); lines=[];ln=""
    for w in words:
        t=(ln+" "+w).strip()
        if d.textlength(t,font=f)>900 and ln: lines.append(ln); ln=w
        else: ln=t
    lines.append(ln); y=1330-(len(lines)-1)*42
    for l in lines:
        d.text((W/2,y),l,font=f,fill=(255,255,255),anchor="mm",stroke_width=9,stroke_fill=(20,10,10)); y+=84
    im.save(path)
def lerp_track(kf):
    ts=[k[0] for k in kf]; xs=[k[1] for k in kf]
    return lambda t: float(np.interp(t,ts,xs))
def render_seg(t0,t1,path,cx,grad,vt0=None):
    d=t1-t0; vt=t0 if vt0 is None else vt0; track=cx if callable(cx) else (lambda t,c=cx:c)
    dec=subprocess.Popen(["ffmpeg","-loglevel","error","-ss",f"{vt}","-t",f"{d}","-i",SRC,"-vf","fps=30","-f","rawvideo","-pix_fmt","bgr24","-"],stdout=subprocess.PIPE)
    enc=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","bgr24","-s",f"{W}x{H}","-r","30","-i","-","-ss",f"{t0}","-t",f"{d}","-i",SRC,
        "-map","0:v","-map","1:a","-c:v","libx264","-crf","18","-preset","fast","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-shortest",path],stdin=subprocess.PIPE)
    n=0; fs=1920*1080*3
    gy=np.clip((np.arange(H)-1470)/170.0,0,1)[:,None,None]**1.3 if grad else None
    mar=np.array(MAROON[::-1],dtype=np.float32)[None,None,:]
    while True:
        buf=dec.stdout.read(fs)
        if len(buf)<fs: break
        f=np.frombuffer(buf,np.uint8).reshape(1080,1920,3)
        x=int(round(min(max(track(vt+n/30.0)-304,0),1920-608))); n+=1
        o=cv2.resize(f[:,x:x+608],(W,H),interpolation=cv2.INTER_LANCZOS4)
        if grad: o=(o.astype(np.float32)*(1-gy)+mar*gy).astype(np.uint8)
        enc.stdin.write(o.tobytes())
    enc.stdin.close(); enc.wait(); dec.wait()
SHORTS={
 1:dict(name="ep01_short_01",t0=19.73,t1=58.97,hook=("The spice Europe forgot","Grains of paradise"),
   text="Growing up in Ghana, there was one stall at Makola Market my mum, God bless her soul, would always stop at — before we even got to the fish, before the plantain, before the Koobi, before anything else. She'd pick up a handful of these small, reddish-brown seeds, crack one between her fingers, and let me smell it. Sharp, peppery, warm — nothing like the black pepper I knew from school dinners back home.",
   segs=[(19.73,38.77,960,False),(38.77,45.70,960,False),
         (45.70,58.97,lerp_track([(45.7,806),(50.7,806),(53.2,864),(55.7,1100),(57.2,1050),(59,1000)]),True)]),
 2:dict(name="ep01_short_02",t0=119.27,t1=175.5,hook=("Europe called it paradise","Then the Portuguese ruined it"),
   text="Here's the thing that gets me — hundreds of years ago, Arab and Berber and Jewish traders carried these grains across the Sahara, all the way to Europe, and Europeans gave it this beautiful name, grains of paradise, just to sell it as a cheaper stand-in for black pepper. It was everywhere, in wine, in beer, in Europe's kitchens. And then the Portuguese found a direct sea route to Asia, and just like that, the world moved on to real black pepper — and grains of paradise, grains of selim, they quietly went back to being a West African secret. Ours never left, it just stopped being anyone else's.",
   segs=[(119.27,127.77,lerp_track([(119.3,.42*1920),(121.5,.39*1920),(123.5,.51*1920),(125.5,.45*1920),(127.7,.33*1920)]),True),
         (127.77,133.70,1056,False),
         (133.70,160.07,lerp_track([(133.7,.56*1920),(136,.38*1920),(138,.36*1920),(140,.43*1920),(142,.52*1920),(144,.43*1920),(146,.35*1920),(148,.39*1920),(150,.41*1920),(152,.42*1920),(154,.46*1920),(156,.48*1920),(158,.38*1920),(160,.36*1920)]),True),
         (160.07,168.13,960,False),
         (168.13,175.5,lerp_track([(168.1,.36*1920),(170.5,.43*1920),(172.5,.42*1920),(175.5,.41*1920)]),True)]),
}
SHORTS[3]=dict(name="ep01_short_03",t0=248.45,t1=334.3,hook=("One rub, two names","Suya in Nigeria · Chinchinga in Ghana"),
   spans=[(248.45,272.52,"Yaji. It's grains of paradise, grains of selim, whole Ashanti pepper or any good dry chillies, crushed kuli-kuli — that's crushed peanut puffs — ginger powder, a crumbled stock cube, salt, and black pepper, all combined into one dry rub."),
          (304.62,334.3,"And what Yaji is really for is grilled meat skewers, coated in this dry rub before they hit the fire — chinchinga, if you grew up in Ghana; suya, if you grew up in Nigeria. Same spice mix, same fire, two names for basically the same street food. That's the whole story of this episode in one bite.")],
   segs=[(248.45,271.8,940,True),
         (271.8,272.52,lerp_track([(271.8,.33*1920),(272.52,.33*1920)]),True),
         (304.62,315.2,960,True),
         (315.2,329.7,lerp_track([(315.2,.42*1920),(317,.42*1920),(319,.46*1920),(321,.45*1920),(323,.42*1920),(325,.39*1920),(327,.46*1920),(329,.45*1920),(329.7,.45*1920)]),True),
         (329.7,330.1,lerp_track([(329.7,.45*1920),(330.1,.44*1920)]),True),
         (330.1,334.3,960,False,411.1)])  # finished skewers (v15 411.1-415.3) over "...the whole story of this episode in one bite"
def main(n):
    S=SHORTS[n]; nm=S["name"]; t0,t1=S["t0"],S["t1"]; body=sum(b-a for a,b,_ in S["spans"]) if S.get("spans") else t1-t0
    os.makedirs(f"{OUT}/{nm}",exist_ok=True); D=f"{OUT}/{nm}"
    parts=[]
    for i,sg in enumerate(S["segs"]):
        a,b,cx,g=sg[:4]; vt0=sg[4] if len(sg)>4 else None
        p=f"{D}/seg{i}.mp4"; render_seg(a,b,p,cx,g,vt0); parts.append(p)
    open(f"{D}/list.txt","w").write("".join(f"file '{p}'\n" for p in parts))
    subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",f"{D}/list.txt","-c","copy",f"{D}/body.mp4"],check=True)
    pill(*S["hook"],f"{D}/hook.png")
    endcard("Spices of the World · Ep 1","Suya & Chinchinga:","the forgotten spice Ghana","and Nigeria share",f"{D}/end.png")
    spans=S.get("spans") or [(t0,t1,S["text"])]; caps=[]; off=0.0
    for (a,b,txt) in spans:
        words,frac=align(txt,a-0.2,b); print("anchor frac",round(frac,2))
        ch=chunks(words)
        for i,c in enumerate(ch):
            s=max(c[0][1]-a,0)+off; e=((ch[i+1][0][1]-a)+off) if i+1<len(ch) else (b-a)+off
            e=min(e,s+4.0); caps.append((s,e," ".join(x[0] for x in c)))
        off+=b-a
    for i,c in enumerate(caps): cap_png(c[2],f"{D}/cap{i}.png")
    cmd=["ffmpeg","-y","-loglevel","error","-i",f"{D}/body.mp4","-loop","1","-t","3.2","-i",f"{D}/hook.png","-loop","1","-t","2.6","-i",f"{D}/end.png"]
    for i in range(len(caps)): cmd+=["-i",f"{D}/cap{i}.png"]
    f=["[1:v]format=rgba,fade=t=in:st=0.2:d=0.3:alpha=1,fade=t=out:st=2.8:d=0.4:alpha=1[h]","[0:v][h]overlay=0:0:enable='lt(t,3.2)'[c0]"]
    for i,(s,e,_) in enumerate(caps):
        f.append(f"[c{i}][{3+i}:v]overlay=0:0:enable='between(t,{s:.2f},{e:.2f})'[c{i+1}]")
    f.append(f"[2:v]format=yuv420p,fade=t=in:st=0:d=0.3,setsar=1[e]"); f.append(f"[c{len(caps)}]format=yuv420p[cv];[cv][e]concat=n=2:v=1:a=0[v]")
    f.append(f"[0:a]afade=t=out:st={body-0.35:.2f}:d=0.35,apad=pad_dur=2.6[a]")
    cmd+=["-filter_complex",";".join(f),"-map","[v]","-map","[a]","-c:v","libx264","-crf","18","-preset","fast","-c:a","aac","-b:a","192k","-shortest","-movflags","+faststart",f"{OUT}/{nm}.mp4"]
    subprocess.run(cmd,check=True)
    open(f"{D}/captions.txt","w").write("\n".join(f"{s:6.2f}-{e:6.2f} {t}" for s,e,t in caps))
    print("done",nm,round(body+2.6,1))
if __name__=="__main__": main(int(sys.argv[1]))
