"""Lay Kofi's full-bowl photos over the Yaji section + raw skewers over 'season lightly'.
Usage: python patch_yaji_photos.py <in_video_only.mp4> <out.mp4>   (duration unchanged)"""
import json, os, sys, subprocess, tempfile
from PIL import Image, ImageFilter, ImageDraw
A = sys.argv[1:]; sys.argv = sys.argv[:1]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import finish_v3 as f
W, H = 1920, 1080
FIT = 0.80                                   # photos sit above the 'What goes into Yaji' bar
PH = os.path.join(f.ROOT, "graphics/episode-01/yaji-photos")
plan = json.load(open(os.path.join(f.HERE, "finish_v3_plan.json")))
tmp = tempfile.mkdtemp(prefix="yajiphotos_")

def still(name, out, fit=FIT):
    im = Image.open(os.path.join(PH, name)).convert("RGB")
    k = max(W / im.width, H / im.height)
    bg = im.resize((int(im.width * k) + 1, int(im.height * k) + 1), Image.LANCZOS)
    bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2, (bg.width - W) // 2 + W, (bg.height - H) // 2 + H))
    bg = bg.filter(ImageFilter.GaussianBlur(40)).point(lambda v: int(v * 0.78))
    fh = int(H * fit); fw = int(im.width * fh / im.height)
    if fw > int(W * 0.94): fw = int(W * 0.94); fh = int(im.height * fw / im.width)
    fg = f.rounded(im.resize((fw, fh), Image.LANCZOS).convert("RGBA"), 26)
    x, y = (W - fw) // 2, int(H * 0.025)
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((x, y + 10, x + fw, y + fh + 10), 26, fill=(0, 0, 0, 140))
    bg = bg.convert("RGBA"); bg.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14))); bg.alpha_composite(fg, (x, y))
    bg.convert("RGB").save(out); return out

# (start, end, kind, file / (clip, in))
SHOTS = [(247.8, 249.6, "p", "grains-of-paradise.jpg"), (249.6, 252.0, "p", "grains-of-selim.jpg"),
         (252.0, 256.2, "p", "dried-chillies.jpg"), (256.2, 260.6, "p", "kuli-kuli.jpg"),
         (260.6, 262.5, "p", "ginger.jpg"), (262.5, 268.3, "v", ("video/raw/ep01-ending/IMG_0603.MOV", 39.0)),
         (268.3, 271.0, "p", "yaji-mix.jpg"), (343.8, 347.0, "p", "raw-skewers.jpg")]
cmd = ["ffmpeg", "-y", "-v", "error", "-i", A[0]]; fc = []; idx = 1; last = "0:v"
bug = os.path.join(tmp, "bug.png"); f.draw_bug(W, H, bug)
for j, (a, b, kind, src) in enumerate(SHOTS):
    d = b - a
    if kind == "p":
        p = still(src, os.path.join(tmp, f"s{j}.png"), 0.76 if a > 300 else FIT)
        cmd += ["-loop", "1", "-t", f"{d:.3f}", "-i", p]
    else:
        clip = os.path.join(f.ROOT, src[0])
        vf = ("zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=mobius,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,"
              f"setparams=colorspace=bt709:color_trc=bt709:color_primaries=bt709:range=tv,fps=30,split[a][b];"
              f"[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=48:2,eq=brightness=-0.12[bg];"
              f"[b]scale=-2:{int(H * FIT)}:flags=lanczos[fg];[bg][fg]overlay=(W-w)/2:{int(H * 0.025)},setsar=1,format=yuv420p")
        out = os.path.join(tmp, f"v{j}.mp4")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{src[1]}", "-t", f"{d:.3f}", "-i", clip, "-vf", vf, "-an", "-c:v", "libx264",
                        "-preset", "veryfast", "-crf", "16", "-colorspace", "bt709", "-color_trc", "bt709", "-color_primaries", "bt709", "-color_range", "tv", out], check=True)
        cmd += ["-i", out]
    fc.append(f"[{idx}:v]setpts=PTS-STARTPTS+{a:.3f}/TB,format=yuv420p[b{j}]")
    fc.append(f"[{last}][b{j}]overlay=0:0:eof_action=pass:enable='between(t,{a:.3f},{b:.3f})'[vb{j}]"); last = f"vb{j}"; idx += 1

layers = []                                    # (png, start, end, fade)
for a, b, *_ in SHOTS: layers.append((bug, a, b, False))
# re-draw the cards that sit over these shots
cards = {round(c["start"], 2): c for c in plan["cards"]}
lab = cards[247.8] if cards.get(247.8, {}).get("type") == "label" else [c for c in plan["cards"] if c["type"] == "label" and c["start"] == 247.8][0]
p = os.path.join(tmp, "lab1.png"); f.draw_label(W, H, lab["text"], p, lab.get("y", 418), lab.get("minw", 200)); layers.append((p, lab["start"], lab["end"], lab.get("fade", True)))
bd = [c for c in plan["cards"] if c["type"] == "build" and c["start"] == 247.8][0]
steps = bd["items"]; n = len(steps)
for k in range(n):
    p = os.path.join(tmp, f"bd{k}.png"); f.draw_build(W, H, bd["title"], [x[1] for x in steps], k, p)
    a = bd["start"] if k == 0 else steps[k][0]; bb = steps[k + 1][0] if k + 1 < n else bd["end"]
    fd = ("in" if k == 0 else False)
    if k == n - 1: fd = True if fd == "in" else "out"
    # only the part of the bar that overlaps our shots needs re-drawing (<= 271.0); the rest is already in the base video
    if a < 271.0: layers.append((p, a, min(bb, 271.0), False if k else "in"))
sk = [c for c in plan["cards"] if c["type"] == "label" and c["start"] == 343.8][0]
p = os.path.join(tmp, "lab2.png"); f.draw_label(W, H, sk["text"], p, sk.get("y", 418), sk.get("minw", 200)); layers.append((p, sk["start"], sk["end"], sk.get("fade", True)))
for k, (png, a, b, fade) in enumerate(layers):
    cmd += ["-loop", "1", "-t", f"{b - a + 1:.3f}", "-i", png]
    ch = f"[{idx}:v]format=rgba,setpts=PTS-STARTPTS+{a:.3f}/TB"
    if fade in (True, "in"): ch += f",fade=t=in:st={a:.3f}:d=0.25:alpha=1"
    if fade in (True, "out"): ch += f",fade=t=out:st={b - 0.25:.3f}:d=0.25:alpha=1"
    fc.append(ch + f"[o{k}]"); fc.append(f"[{last}][o{k}]overlay=0:0:eof_action=pass:enable='between(t,{a:.3f},{b:.3f})'[v{k}]"); last = f"v{k}"; idx += 1
fc.append(f"[{last}]format=yuv420p[vout]")
cmd += ["-filter_complex", ";".join(fc), "-map", "[vout]", "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-r", "30", "-threads", "6", "-movflags", "+faststart", A[1]]
subprocess.run(cmd, check=True); print("wrote", A[1])
