"""Ep1 Short #1 (9:16): 'The spice Europe forgot' — Makola memory -> grains of paradise. Cut from v15."""
import subprocess, os
from PIL import Image, ImageDraw, ImageFont
SRC="/home/claude/spicesoftheworld/spicesOftheWorld/video/episode-01/out/Spices_of_the_World_Ep1_v15.mp4"
FONT="/home/claude/spicesoftheworld/spicesOftheWorld/video/episode-01/fonts/Inter-ExtraBold.otf"
FONTM="/home/claude/spicesoftheworld/spicesOftheWorld/video/episode-01/fonts/Inter-SemiBold.otf"
OUT=os.path.dirname(os.path.abspath(__file__)); W,H=1080,1920
MAROON=(110,31,42); ORANGE=(224,130,30); CREAM=(250,243,232)
def pill(txt,sub,path):
    im=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    f=ImageFont.truetype(FONT,78); fs=ImageFont.truetype(FONTM,40)
    tw=d.textlength(txt,font=f); bw=tw+90; x0=(W-bw)/2; y0=430
    d.rounded_rectangle([x0,y0,x0+bw,y0+150],34,fill=MAROON+(235,))
    d.text((W/2,y0+75),txt,font=f,fill=CREAM,anchor="mm")
    if sub:
        sw=d.textlength(sub,font=fs)+60; d.rounded_rectangle([(W-sw)/2,y0+170,(W+sw)/2,y0+235],30,fill=ORANGE+(240,))
        d.text((W/2,y0+203),sub,font=fs,fill=(255,255,255),anchor="mm")
    im.save(path)
pill("The spice Europe forgot","Grains of paradise",f"{OUT}/hook.png")
# end card
im=Image.new("RGB",(W,H),MAROON); d=ImageDraw.Draw(im)
d.text((W/2,700),"FULL EPISODE",font=ImageFont.truetype(FONT,96),fill=CREAM,anchor="mm")
d.text((W/2,820),"Spices of the World · Ep 1",font=ImageFont.truetype(FONTM,52),fill=ORANGE,anchor="mm")
d.text((W/2,980),"Suya & Chinchinga:",font=ImageFont.truetype(FONT,62),fill=CREAM,anchor="mm")
d.text((W/2,1060),"the forgotten spice Ghana",font=ImageFont.truetype(FONTM,50),fill=CREAM,anchor="mm")
d.text((W/2,1125),"and Nigeria share",font=ImageFont.truetype(FONTM,50),fill=CREAM,anchor="mm")
d.text((W/2,1330),"Watch the full episode on the channel",font=ImageFont.truetype(FONTM,46),fill=ORANGE,anchor="mm")
im.save(f"{OUT}/end.png")
A0,A1=19.73,38.77; B1=45.70; C1=58.97
segs=[("A",A0,A1,"fill"),("B",A1,B1,"fill"),("C",B1,C1,"face")]
def vf(kind):
    if kind=="fill":
        return "scale=-2:1920:flags=lanczos,crop=1080:1920,setsar=1"
    return "crop=608:1080:x='if(lt(t,5),502+(502-502)*(t-0)/(5-0),if(lt(t,7.5),502+(560-502)*(t-5)/(7.5-5),if(lt(t,10),560+(776-560)*(t-7.5)/(10-7.5),if(lt(t,11.5),776+(740-776)*(t-10)/(11.5-10),if(lt(t,13.3),740+(690-740)*(t-11.5)/(13.3-11.5),690)))))':y=0,scale=1080:1920:flags=lanczos,setsar=1"
parts=[]
for n,s,e,k in segs:
    subprocess.run(["ffmpeg","-y","-loglevel","error","-ss",str(s),"-t",str(e-s),"-i",SRC,"-vf",vf(k)+",fps=30,format=yuv420p",
      "-af","aresample=48000","-c:v","libx264","-crf","18","-preset","fast","-c:a","aac","-b:a","192k",f"{OUT}/seg_{n}.mp4"],check=True); parts.append(f"{OUT}/seg_{n}.mp4")
open(f"{OUT}/list.txt","w").write("".join(f"file '{p}'\n" for p in parts))
subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",f"{OUT}/list.txt","-c","copy",f"{OUT}/body.mp4"],check=True)
body=(C1-A0)
# hook overlay 0-3s, end card 2.4s with audio fade
subprocess.run(["ffmpeg","-y","-loglevel","error","-i",f"{OUT}/body.mp4","-loop","1","-t","3.2","-i",f"{OUT}/hook.png","-loop","1","-t","2.6","-i",f"{OUT}/end.png",
 "-filter_complex",
 f"[1:v]format=rgba,fade=t=in:st=0.2:d=0.3:alpha=1,fade=t=out:st=2.8:d=0.4:alpha=1[h];[0:v][h]overlay=0:0:enable='lt(t,3.2)'[v0];"
 f"[2:v]format=yuv420p,fade=t=in:st=0:d=0.3,setsar=1[e];[v0][e]concat=n=2:v=1:a=0[v];"
 f"[0:a]afade=t=out:st={body-0.35:.2f}:d=0.35,apad=pad_dur=2.6[a]",
 "-map","[v]","-map","[a]","-c:v","libx264","-crf","18","-preset","fast","-c:a","aac","-b:a","192k","-shortest","-movflags","+faststart",f"{OUT}/ep01_short_01.mp4"],check=True)
print("ok",body+2.6)
