"""Builds the 60 s 'full cook' insert (Kofi's IMG_0616, first 72 s at 1.2x) that goes in at 404.6 s.
Usage: python insert_full_cook.py <out.mp4>"""
import os, sys, subprocess, tempfile
A = sys.argv[1:]; sys.argv = sys.argv[:1]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import finish_v3 as f
W, H, N = 1920, 1080, 60.0
tmp = tempfile.mkdtemp(prefix="ins_")
raw = os.path.join(tmp, "raw.mp4")
f.render_broll({"start": 0, "end": N, "kind": "video", "src": "video/raw/ep01-ending/IMG_0616.MOV", "in": 0.0, "speed": 1.2}, W, H, raw)
bug = os.path.join(tmp, "bug.png"); f.draw_bug(W, H, bug)
ch = os.path.join(tmp, "ch.png"); f.draw_chapter_c(W, H, "THE FULL COOK", "Suya & chinchinga, start to finish", ch)
lab = [(os.path.join(tmp, "l1.png"), "Coat the skewers in the Yaji", 6.0, 30.0), (os.path.join(tmp, "l2.png"), "Onto the grill to cook", 53.0, 59.5)]
for p, t, a, b in lab: f.draw_label(W, H, t, p, 418, 200)
LP = lambda p: ["-loop", "1", "-t", str(N), "-i", p]
cmd = ["ffmpeg", "-y", "-v", "error", "-i", raw] + LP(bug) + LP(ch) + sum([LP(p) for p, *_ in lab], [])
fc = ["[0:v]format=yuv420p[v0]", "[v0][1:v]overlay=0:0[v1]",
      "[2:v]format=rgba,fade=t=in:st=0.3:d=0.25:alpha=1,fade=t=out:st=4.6:d=0.25:alpha=1[c]", "[v1][c]overlay=0:0:eof_action=pass:enable='between(t,0.3,4.85)'[v2]"]
last = "v2"
for i, (p, t, a, b) in enumerate(lab):
    fc.append(f"[{3+i}:v]format=rgba,setpts=PTS-STARTPTS+{a}/TB,fade=t=in:st={a}:d=0.25:alpha=1,fade=t=out:st={b-0.25}:d=0.25:alpha=1[l{i}]")
    fc.append(f"[{last}][l{i}]overlay=0:0:eof_action=pass:enable='between(t,{a},{b})'[o{i}]"); last = f"o{i}"
cmd += ["-filter_complex", ";".join(fc), "-map", f"[{last}]", "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "16", "-r", "30", "-t", str(N), A[0]]
subprocess.run(cmd, check=True); print("wrote", A[0])
