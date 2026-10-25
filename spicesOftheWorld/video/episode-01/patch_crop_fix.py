"""Replace the two tightly-cropped bowl shots (grains of paradise 38.8-45.73, grains of selim 107.03-115.10)
with Kofi's full-bowl photos. Only the first 404.3 s are rendered (the part before the full-cook insert).
Usage: python patch_crop_fix.py <in_video_only.mp4> <out.mp4>"""
import json, os, sys, subprocess, tempfile
A = sys.argv[1:]; sys.argv = sys.argv[:1]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "patch_yaji_photos.py")).read().split("# (start, end, kind")[0]
src = src.replace("A = sys.argv[1:]; sys.argv = sys.argv[:1]", "")
exec(src)                                   # reuses still(), W, H, plan, f, tmp
FITL = 0.88                                  # no bar here, only a small label: show the bowl bigger
SHOTS = [(38.8, 45.73, "grains-of-paradise-sheen.jpg", "Grains of paradise", 38.5, 45.85),
         (107.03, 115.10, "grains-of-selim.jpg", "Grains of selim", 106.7, 115.25)]
cmd = ["ffmpeg", "-y", "-v", "error", "-t", "404.3", "-i", A[0]]; fc = []; idx = 1; last = "0:v"
bug = os.path.join(tmp, "bug.png"); f.draw_bug(W, H, bug)
layers = []
for j, (a, b, name, text, la, lb) in enumerate(SHOTS):
    p = still(name, os.path.join(tmp, f"s{j}.png"), FITL)
    cmd += ["-loop", "1", "-t", f"{b - a:.3f}", "-i", p]
    fc.append(f"[{idx}:v]setpts=PTS-STARTPTS+{a:.3f}/TB,format=yuv420p[b{j}]")
    fc.append(f"[{last}][b{j}]overlay=0:0:eof_action=pass:enable='between(t,{a:.3f},{b:.3f})'[vb{j}]"); last = f"vb{j}"; idx += 1
    layers.append((bug, a, b, False))
    lp = os.path.join(tmp, f"l{j}.png"); f.draw_label(W, H, text, lp, 418, 200); layers.append((lp, max(la, a), lb, False))
for k, (png, a, b, fade) in enumerate(layers):
    cmd += ["-loop", "1", "-t", f"{b - a + 1:.3f}", "-i", png]
    fc.append(f"[{idx}:v]format=rgba,setpts=PTS-STARTPTS+{a:.3f}/TB[o{k}]")
    fc.append(f"[{last}][o{k}]overlay=0:0:eof_action=pass:enable='between(t,{a:.3f},{b:.3f})'[v{k}]"); last = f"v{k}"; idx += 1
fc.append(f"[{last}]format=yuv420p[vout]")
cmd += ["-filter_complex", ";".join(fc), "-map", "[vout]", "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "15", "-r", "30", "-threads", "6", A[1]]
subprocess.run(cmd, check=True); print("wrote", A[1])
