"""Insert Kofi's own on-camera olive-oil explanation (IMG_0616 ~1:50-2:01, live audio) at 394.0 s of v11.
Builds out/ep01_oil_insert.mp4 (video, 11 s) and /home/claude/ep01work/music/oil_audio_insert.wav."""
import os, sys, subprocess, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import finish_v3 as f
W, H = 1920, 1080
IN, DUR = 110.2, 11.0
tmp = tempfile.mkdtemp(prefix="oilvoice_")
b = {"start": 0, "end": DUR, "kind": "video", "src": "video/raw/ep01-ending/IMG_0616.MOV", "in": IN, "speed": 1.0}
vid = os.path.join(tmp, "b.mp4"); f.render_broll(b, W, H, vid)
bug = os.path.join(tmp, "bug.png"); f.draw_bug(W, H, bug)
cap = os.path.join(tmp, "cap.png"); f.draw_caption_c(W, H, "Tip: a drizzle of olive oil after the Yaji", "It drips onto the coals, and the smoke flavours the meat", cap)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "ep01_oil_insert.mp4")
fc = ("[1:v]format=rgba,fade=t=in:st=0.3:d=0.25:alpha=1,fade=t=out:st=%.2f:d=0.25:alpha=1[c];[0:v][2:v]overlay=0:0[a];[a][c]overlay=0:0,format=yuv420p[v]" % (DUR-0.25))
subprocess.run(["ffmpeg","-y","-v","error","-i",vid,"-loop","1","-t",str(DUR),"-i",cap,"-loop","1","-t",str(DUR),"-i",bug,
  "-filter_complex",fc,"-map","[v]","-an","-c:v","libx264","-preset","veryfast","-crf","16","-r","30","-t",str(DUR),out],check=True)
print("wrote", out)
