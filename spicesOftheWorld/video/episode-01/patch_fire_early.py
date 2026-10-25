"""v12 -> v13: show 'back on the fire' grill footage from 370 s (when the voice says it) until the oil insert at 394,
replacing the early drizzle cutaway at 380-394. Audio untouched. Usage: python patch_fire_early.py in.mp4 out.mp4"""
import os, sys, subprocess, tempfile
A = sys.argv[1:]; sys.argv = sys.argv[:1]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import finish_v3 as f
W, H = 1920, 1080
tmp = tempfile.mkdtemp(prefix="fire_")
S, E = 370.0, 394.0
b = {"start": S, "end": E, "kind": "video", "src": "video/raw/ep01-ending/IMG_0616.MOV", "in": 62.2, "speed": 12.4 / (E - S)}
vid = os.path.join(tmp, "b.mp4"); f.render_broll(b, W, H, vid)
bug = os.path.join(tmp, "bug.png"); f.draw_bug(W, H, bug)
lab = os.path.join(tmp, "lab.png"); f.draw_label(W, H, "Back on the fire to finish", lab, 418, 200)
fc = (f"[1:v]setpts=PTS-STARTPTS+{S}/TB,format=yuv420p[b];"
      f"[0:v][b]overlay=0:0:eof_action=pass:enable='between(t,{S},{E})'[a];"
      f"[2:v]format=rgba,setpts=PTS-STARTPTS+{S}/TB[g];[a][g]overlay=0:0:eof_action=pass:enable='between(t,{S},{E})'[c];"
      f"[3:v]format=rgba,setpts=PTS-STARTPTS+{S+0.3}/TB,fade=t=in:st={S+0.3}:d=0.25:alpha=1,fade=t=out:st={S+5.5}:d=0.25:alpha=1[l];"
      f"[c][l]overlay=0:0:eof_action=pass:enable='between(t,{S+0.3},{S+5.8})',format=yuv420p[v]")
subprocess.run(["ffmpeg","-y","-v","error","-i",A[0],"-i",vid,"-loop","1","-t",str(E+1),"-i",bug,"-loop","1","-t",str(E+7),"-i",lab,
  "-filter_complex",fc,"-map","[v]","-an","-c:v","libx264","-preset","fast","-crf","18","-maxrate","5500k","-bufsize","11000k","-r","30","-threads","8",A[1]],check=True)
print("wrote",A[1])
