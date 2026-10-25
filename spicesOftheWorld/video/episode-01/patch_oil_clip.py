"""Fast path: lay the IMG_0616 cutaways + their labels over an already-rendered v5 picture.
Usage: python patch_oil_clip.py <in_video_only.mp4> <out.mp4>   (duration unchanged, audio untouched)"""
import json, os, sys, subprocess, tempfile
sys.argv, A = sys.argv[:1], sys.argv[1:]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import finish_v3 as f
W, H = 1920, 1080
plan = json.load(open(os.path.join(f.HERE, "finish_v3_plan.json")))
tmp = tempfile.mkdtemp(prefix="oilpatch_")
new_b = [b for b in plan["broll"] if "IMG_0616" in b["src"]]
cards = [c for c in plan["cards"] if c["start"] == 343.8 or "IMG_0616" in c.get("reason", "")]
cmd = ["ffmpeg", "-y", "-v", "error", "-i", A[0]]; fc = []; idx = 1; last = "0:v"
win = (min(b["start"] for b in new_b), max(b["end"] for b in new_b))
for j, b in enumerate(new_b):
    out = os.path.join(tmp, f"b{j}.mp4"); f.render_broll(b, W, H, out)
    cmd += ["-i", out]
    fc.append(f"[{idx}:v]setpts=PTS-STARTPTS+{b['start']:.3f}/TB,format=yuv420p[b{j}]")
    fc.append(f"[{last}][b{j}]overlay=0:0:eof_action=pass:enable='between(t,{b['start']:.3f},{b['end']:.3f})'[vb{j}]"); last = f"vb{j}"; idx += 1
layers = []
bug = os.path.join(tmp, "bug.png"); f.draw_bug(W, H, bug)
for b in new_b: layers.append((bug, b["start"], b["end"], False))
for i, c in enumerate(cards):
    p = os.path.join(tmp, f"c{i}.png")
    if c["type"] == "label": f.draw_label(W, H, c["text"], p, c.get("y", 418), c.get("minw", 200))
    else: f.draw_caption_c(W, H, c["title"], c.get("sub"), p)
    layers.append((p, c["start"], c["end"], c.get("fade", True)))
for k, (png, a, b, fade) in enumerate(layers):
    cmd += ["-i", png]
    ch = f"[{idx}:v]format=rgba,setpts=PTS-STARTPTS+{a:.3f}/TB"
    if fade in (True, "in"): ch += f",fade=t=in:st={a:.3f}:d=0.25:alpha=1"
    if fade in (True, "out"): ch += f",fade=t=out:st={b-0.25:.3f}:d=0.25:alpha=1"
    fc.append(ch + f"[o{k}]")
    fc.append(f"[{last}][o{k}]overlay=0:0:eof_action=pass:enable='between(t,{a:.3f},{b:.3f})'[v{k}]"); last = f"v{k}"; idx += 1
fc.append(f"[{last}]format=yuv420p[vout]")
cmd += ["-filter_complex", ";".join(fc), "-map", "[vout]", "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-r", "30", "-threads", "6", "-movflags", "+faststart", A[1]]
print("cards:", [(c['start'], c.get('text') or c.get('title')) for c in cards])
subprocess.run(cmd, check=True); print("wrote", A[1])
