"""Finishing pass for Episode 1 v3 (ep01_v3_16x9_480p.mp4).

Reads finish_v3_plan.json, draws the on-screen graphics (brand bug, chapter
title, location tag, captions, lower third, list-close, CTA + Yaji jar,
end screen) and renders with ffmpeg.

  python video/episode-01/finish_v3.py --preview   # ending only, 854x480, fast
  python video/episode-01/finish_v3.py --final     # whole episode, 1920x1080

Run from the spicesOftheWorld/ folder. Output goes to video/episode-01/out/
(not committed: renders stay out of git).

Brand (make_overlays.py): Inter, Marigold #E07610, Cream #FDF3E4,
Maroon #6B1B1F panels, Gold #E79A2E, Ink #3A1210.
"""
import argparse
import json
import os
import shutil
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
REF_W, REF_H = 854, 480            # v3 frame; all layout below is in these units

MAROON = (107, 27, 31)
MARIGOLD = (224, 118, 16, 255)
CREAM = (253, 243, 228, 255)
GOLD = (231, 154, 46, 255)
INK = (58, 18, 16, 255)

FONT_DIRS = [os.path.join(HERE, "fonts"), "/usr/share/fonts/opentype/inter",
             "/usr/share/fonts/truetype/inter", os.path.expanduser("~/Library/Fonts"),
             "C:/Windows/Fonts"]


def font(weight, size):
    for d in FONT_DIRS:
        p = os.path.join(d, f"Inter-{weight}.otf")
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    # fallback: variable font as used by make_overlays.py
    p = os.path.join(HERE, "fonts", "Inter-Variable.ttf")
    return ImageFont.truetype(p, size)


class Canvas:
    def __init__(self, W, H):
        self.W, self.H, self.s = W, H, W / REF_W
        self.img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.img)

    def u(self, v):
        return int(round(v * self.s))

    def f(self, weight, size):
        return font(weight, self.u(size))

    def panel(self, box, alpha=225, radius=10, shadow=True):
        x0, y0, x1, y1 = [self.u(v) for v in box]
        if shadow:
            sh = Image.new("RGBA", self.img.size, (0, 0, 0, 0))
            ImageDraw.Draw(sh).rounded_rectangle((x0, y0 + self.u(2), x1, y1 + self.u(2)),
                                                 self.u(radius), fill=(0, 0, 0, 110))
            self.img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(self.u(5))))
        self.d.rounded_rectangle((x0, y0, x1, y1), self.u(radius), fill=MAROON + (alpha,))

    def text(self, xy, t, fnt, fill, anchor="la"):
        self.d.text((self.u(xy[0]), self.u(xy[1])), t, font=fnt, fill=fill, anchor=anchor)

    def tw(self, t, fnt):
        return self.d.textlength(t, font=fnt) / self.s

    def save(self, path):
        self.img.save(path)


def logo(path_root):
    return Image.open(os.path.join(path_root, "brand-assets/logo/fudi-people-logo-cream-bold.png")).convert("RGBA")


def draw_bug(W, H, out):
    """Channel bug, top-left. Also hides the burned-in '#NN 0m00s' cut labels."""
    c = Canvas(W, H)
    c.panel((4, 3, 124, 31), alpha=240, radius=8, shadow=False)
    lg = logo(ROOT)
    lh = c.u(24)
    lg = lg.resize((int(lg.width * lh / lg.height), lh), Image.LANCZOS)
    c.img.alpha_composite(lg, (c.u(9), c.u(5)))
    c.text((38, 17), "FUDI PEOPLE", c.f("ExtraBold", 12), CREAM, anchor="lm")
    c.save(out)


def draw_caption(W, H, text, emph, out):
    """Subtitle bar, bottom centre. Sized to always cover the burned-in [tag] box."""
    c = Canvas(W, H)
    fnt = c.f("ExtraBold" if emph else "SemiBold", 21 if emph else 19)
    w = max(c.tw(text, fnt) + 36, 130)
    x0, x1 = REF_W / 2 - w / 2, REF_W / 2 + w / 2
    c.panel((x0, 420, x1, 492), alpha=255)
    c.text((REF_W / 2, 450), text, fnt, MARIGOLD if emph else CREAM, anchor="mm")
    c.save(out)


def draw_chapter(W, H, kicker, title, out):
    c = Canvas(W, H)
    fk, ft = c.f("Bold", 11), c.f("ExtraBold", 26)
    w = max(c.tw(title, ft), c.tw(kicker, fk) * 1.25) + 46
    c.panel((26, 356, 26 + w, 424))
    c.d.rectangle((c.u(26), c.u(368), c.u(31), c.u(412)), fill=MARIGOLD)
    c.text((44, 365), "  ".join(kicker), fk, GOLD)
    c.text((44, 381), title, ft, CREAM)
    c.save(out)


def draw_location(W, H, text, out):
    c = Canvas(W, H)
    fnt = c.f("Bold", 14)
    w = c.tw(text, fnt) + 30
    x0, y0, y1 = 26, 368, 398
    c.d.rounded_rectangle((c.u(x0), c.u(y0), c.u(x0 + w), c.u(y1)), c.u(15), fill=MARIGOLD)
    c.text((x0 + 15, (y0 + y1) / 2), text, fnt, INK, anchor="lm")
    c.save(out)


def draw_lower_third(W, H, title, sub, out):
    c = Canvas(W, H)
    ft, fs = c.f("ExtraBold", 26), c.f("Medium", 15)
    w = max(c.tw(title, ft), c.tw(sub, fs)) + 46
    c.panel((26, 392, 26 + w, 464))
    c.d.rectangle((c.u(26), c.u(404), c.u(31), c.u(452)), fill=MARIGOLD)
    c.text((44, 400), title, ft, CREAM)
    c.text((44, 434), sub, fs, GOLD)
    c.save(out)


def draw_list(W, H, items, upto, out):
    """Trailing list-close: phrases build up one at a time, centred; newest in marigold."""
    c = Canvas(W, H)
    fnt = c.f("SemiBold", 18)
    sep = "  ·  "
    shown = items[: upto + 1]
    full_w = c.tw(sep.join(shown), fnt)
    w = max(full_w + 40, 130)
    x0 = REF_W / 2 - w / 2
    c.panel((x0, 420, x0 + w, 492), alpha=255)
    x = REF_W / 2 - full_w / 2
    for i, it in enumerate(shown):
        c.text((x, 450), it, fnt, MARIGOLD if i == upto else CREAM, anchor="lm")
        x += c.tw(it, fnt)
        if i < upto:
            c.text((x, 450), sep, fnt, GOLD, anchor="lm")
            x += c.tw(sep, fnt)
    c.save(out)


def draw_cta(W, H, line1, line2, out):
    c = Canvas(W, H)
    f1, f2 = c.f("Medium", 16), c.f("ExtraBold", 31)
    w = max(c.tw(line1, f1), c.tw(line2, f2)) + 60
    x0 = REF_W / 2 - w / 2
    c.panel((x0, 402, x0 + w, 492), alpha=255)
    c.text((REF_W / 2, 420), line1, f1, CREAM, anchor="mm")
    c.text((REF_W / 2, 452), line2, f2, MARIGOLD, anchor="mm")
    c.save(out)


def rounded(im, r):
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), r, fill=255)
    im = im.convert("RGBA")
    im.putalpha(m)
    return im


def draw_product(W, H, cta, out):
    c = Canvas(W, H)
    im = Image.open(os.path.join(ROOT, cta["product"])).convert("RGBA")
    if "product_crop" not in cta:          # square jar label (old layout)
        size = c.u(196)
        im = im.resize((size, size), Image.LANCZOS)
        sh = Image.new("RGBA", c.img.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).ellipse((c.u(628), c.u(96), c.u(628) + size, c.u(96) + size), fill=(0, 0, 0, 150))
        c.img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(c.u(10))))
        c.img.alpha_composite(im, (c.u(624), c.u(88)))
        c.save(out)
        return
    # portrait bottle photo in a rounded card, right of frame, with a small name tag
    im = im.crop(tuple(cta["product_crop"]))
    bw = 118
    bh = bw * im.height / im.width
    x0, y0 = 708, 46
    card = rounded(im.resize((c.u(bw), c.u(bh)), Image.LANCZOS), c.u(10))
    sh = Image.new("RGBA", c.img.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((c.u(x0 - 3), c.u(y0), c.u(x0 + bw + 3), c.u(y0 + bh + 6)),
                                         c.u(12), fill=(0, 0, 0, 150))
    c.img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(c.u(8))))
    c.d.rounded_rectangle((c.u(x0 - 3), c.u(y0 - 3), c.u(x0 + bw + 3), c.u(y0 + bh + 3)), c.u(12), fill=CREAM)
    c.img.alpha_composite(card, (c.u(x0), c.u(y0)))
    tag = cta.get("product_tag")
    if tag:
        fnt = c.f("Bold", 10)
        tw = c.tw(tag, fnt) + 16
        cx, ty = x0 + bw / 2, y0 + bh + 10
        c.d.rounded_rectangle((c.u(cx - tw / 2), c.u(ty), c.u(cx + tw / 2), c.u(ty + 18)), c.u(9), fill=MARIGOLD)
        c.text((cx, ty + 9), tag, fnt, INK, anchor="mm")
    c.save(out)


def draw_end_screen(W, H, out, banner=None, crop=None):
    """Room for YouTube end-screen elements: a video (left) + subscribe (right)."""
    if banner:
        return draw_end_screen_banner(W, H, out, banner, crop)
    c = Canvas(W, H)
    bg = Image.new("RGBA", (W, H))
    bd = ImageDraw.Draw(bg)
    for y in range(H):  # vertical maroon gradient
        k = y / H
        bd.line([(0, y), (W, y)], fill=(int(120 - 40 * k), int(32 - 12 * k), int(34 - 12 * k), 255))
    c.img = bg
    c.d = ImageDraw.Draw(c.img)
    lg = logo(ROOT)
    lh = c.u(78)
    lg = lg.resize((int(lg.width * lh / lg.height), lh), Image.LANCZOS)
    c.img.alpha_composite(lg, ((W - lg.width) // 2, c.u(26)))
    c.text((REF_W / 2, 132), "Thanks for watching", c.f("ExtraBold", 28), CREAM, anchor="mm")
    # guide frames where the end-screen elements will sit
    c.d.rounded_rectangle((c.u(96), c.u(170), c.u(416), c.u(350)), c.u(12),
                          outline=GOLD, width=max(2, c.u(2)))
    c.text((256, 260), "WATCH NEXT", c.f("Bold", 13), GOLD, anchor="mm")
    cx, cy, r = 600, 260, 70
    c.d.ellipse((c.u(cx - r), c.u(cy - r), c.u(cx + r), c.u(cy + r)), outline=GOLD, width=max(2, c.u(2)))
    c.text((cx, cy), "SUBSCRIBE", c.f("Bold", 13), GOLD, anchor="mm")
    c.text((REF_W / 2, 398), "fudipeople.com", c.f("ExtraBold", 30), MARIGOLD, anchor="mm")
    c.text((REF_W / 2, 432), "Spices of Africa  ·  grown in Sidcup, rooted in Ghana",
           c.f("Medium", 15), CREAM, anchor="mm")
    c.save(out)


def draw_end_screen_banner(W, H, out, banner, crop=None):
    """End screen with the chilli-oil brand banner along the bottom (it carries fudipeople.com)."""
    c = Canvas(W, H)
    bg = Image.new("RGBA", (W, H))
    bd = ImageDraw.Draw(bg)
    for y in range(H):  # deep brown, matches the banner's own background
        k = y / H
        bd.line([(0, y), (W, y)], fill=(int(70 - 18 * k), int(24 - 6 * k), int(18 - 5 * k), 255))
    c.img = bg
    c.d = ImageDraw.Draw(c.img)
    lg = logo(ROOT)
    lh = c.u(50)
    lg = lg.resize((int(lg.width * lh / lg.height), lh), Image.LANCZOS)
    c.img.alpha_composite(lg, ((W - lg.width) // 2, c.u(12)))
    c.text((REF_W / 2, 88), "Thanks for watching", c.f("ExtraBold", 24), CREAM, anchor="mm")
    c.d.rounded_rectangle((c.u(118), c.u(112), c.u(418), c.u(281)), c.u(12),
                          outline=GOLD, width=max(2, c.u(2)))
    c.text((268, 196), "WATCH NEXT", c.f("Bold", 13), GOLD, anchor="mm")
    cx, cy, r = 598, 196, 64
    c.d.ellipse((c.u(cx - r), c.u(cy - r), c.u(cx + r), c.u(cy + r)), outline=GOLD, width=max(2, c.u(2)))
    c.text((cx, cy), "SUBSCRIBE", c.f("Bold", 13), GOLD, anchor="mm")
    b = Image.open(os.path.join(ROOT, banner)).convert("RGBA")
    if crop:
        b = b.crop(tuple(crop))
    bw = 560
    bh = bw * b.height / b.width
    bx, by = (REF_W - bw) / 2, 296
    b = rounded(b.resize((c.u(bw), c.u(bh)), Image.LANCZOS), c.u(12))
    c.img.alpha_composite(b, (c.u(bx), c.u(by)))
    c.save(out)


def render_broll(br, W, H, out):
    """Pre-render one cutaway as a silent W x H, 30fps clip of exactly (end - start) seconds.
    Portrait sources sit sharp in the middle over a blurred, darkened fill of themselves.
    iPhone HLG footage is tonemapped to SDR the same way as build_ep01.py."""
    d = br["end"] - br["start"]
    src = os.path.join(ROOT, br["src"])
    fill = (f"split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
            f"boxblur=luma_radius={max(8, W // 40)}:luma_power=2,eq=brightness=-0.10:saturation=0.85[bg];"
            f"[b]scale=-2:{H}:flags=lanczos[fg];[bg][fg]overlay=(W-w)/2:0")
    if br["kind"] == "video":
        trc = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                       "stream=color_transfer", "-of", "csv=p=0", src]).decode().strip()
        tm = ("zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=mobius,"
              "zscale=t=bt709:m=bt709:r=tv,format=yuv420p," if trc in ("arib-std-b67", "smpte2084") else "")
        vf = f"{tm}fps=30,{fill},setsar=1,format=yuv420p"
        cmd = ["ffmpeg", "-y", "-v", "error", "-ss", f"{br['in']}", "-t", f"{d:.3f}", "-i", src, "-vf", vf]
    else:
        # still: compose the fill frame at 1.15x, then push in slowly towards `focus`
        im = Image.open(src)
        im = ImageOps.exif_transpose(im).convert("RGB")
        S = 1.15
        CW, CH = int(W * S) // 2 * 2, int(H * S) // 2 * 2
        bg = im.copy()
        k = max(CW / bg.width, CH / bg.height)
        bg = bg.resize((int(bg.width * k) + 1, int(bg.height * k) + 1), Image.LANCZOS)
        bg = bg.crop(((bg.width - CW) // 2, (bg.height - CH) // 2, (bg.width - CW) // 2 + CW, (bg.height - CH) // 2 + CH))
        bg = bg.filter(ImageFilter.GaussianBlur(CW // 60))
        bg = Image.eval(bg, lambda v: int(v * 0.85))
        fg = im.resize((int(im.width * CH / im.height), CH), Image.LANCZOS)
        bg.paste(fg, ((CW - fg.width) // 2, 0))
        still = out + ".png"
        bg.save(still)
        p = br.get("push", 1.06)
        fx, fy = br.get("focus", [0.5, 0.5])
        z = f"(1+{p - 1:.4f}*t/{d:.3f})"                    # 1 -> push over the shot
        vf = (f"fps=30,scale=w='trunc({W}*{z}/2)*2':h='trunc({H}*{z}/2)*2':eval=frame:flags=lanczos,"
              f"crop={W}:{H}:'(in_w-out_w)*{fx}':'(in_h-out_h)*{fy}',setsar=1,format=yuv420p")
        cmd = ["ffmpeg", "-y", "-v", "error", "-loop", "1", "-t", f"{d:.3f}", "-i", still, "-vf", vf]
    cmd += ["-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-r", "30", out]
    subprocess.run(cmd, check=True)


def zoom_expr(zooms, t0):
    """Zoom factor z(t): ease in 0.5s to peak, hold, ease out 0.5s (t = output time)."""
    parts = []
    for z in zooms:
        a, b, p = z["start"] - t0, z["end"] - t0, z["peak"] - 1
        ramp = f"min(min((t-{a:.3f})/0.5,1),min(({b:.3f}-t)/0.5,1))"
        parts.append(f"if(between(t,{a:.3f},{b:.3f}),{p:.4f}*{ramp},0)")
    return "1+" + "+".join(parts) if parts else "1"


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--preview", action="store_true")
    g.add_argument("--final", action="store_true")
    ap.add_argument("--plan", default=os.path.join(HERE, "finish_v3_plan.json"))
    args = ap.parse_args()

    plan = json.load(open(args.plan))
    src = os.path.join(ROOT, plan["source"])
    if args.preview:
        W, H, t0, crf, preset, name = 854, 480, plan["preview_start"], 23, "veryfast", "ep01_v4_ending_preview.mp4"
    else:
        W, H, t0, crf, preset, name = 1920, 1080, 0.0, 18, "medium", "ep01_v4_16x9_1080p.mp4"
    es = plan["end_screen"]
    cut = es["start"]                              # main picture ends here
    total = (cut - t0) + es["duration"]
    src_dur = float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src]).decode())

    tmp = tempfile.mkdtemp(prefix="ep01v4_")
    layers = []  # (png, start, end, fade)

    def add(png, a, b, fade=False):
        layers.append((png, a, b, fade))

    p = os.path.join(tmp, "bug.png"); draw_bug(W, H, p); add(p, max(plan["label_cover_from"], t0), cut)
    for i, ch in enumerate(plan["chapter"]):
        p = os.path.join(tmp, f"ch{i}.png"); draw_chapter(W, H, ch["kicker"], ch["title"], p); add(p, ch["start"], ch["end"], True)
    for i, lo in enumerate(plan["location"]):
        p = os.path.join(tmp, f"loc{i}.png"); draw_location(W, H, lo["text"], p); add(p, lo["start"], lo["end"], True)
    for i, cap in enumerate(plan["captions"]):
        p = os.path.join(tmp, f"cap{i}.png"); draw_caption(W, H, cap[2], len(cap) > 3, p); add(p, cap[0], cap[1])
    for i, lt in enumerate(plan["lower_third"]):
        p = os.path.join(tmp, f"lt{i}.png"); draw_lower_third(W, H, lt["title"], lt["sub"], p); add(p, lt["start"], lt["end"], True)
    lc = plan["list_close"]
    items = [x[1] for x in lc["items"]]
    starts = [x[0] for x in lc["items"]]
    for i in range(len(items)):
        p = os.path.join(tmp, f"list{i}.png"); draw_list(W, H, items, i, p)
        a = lc["start"] if i == 0 else starts[i]
        b = starts[i + 1] if i + 1 < len(items) else lc["end"]
        add(p, a, b)
    cta = plan["cta"]
    p = os.path.join(tmp, "cta.png"); draw_cta(W, H, cta["line1"], cta["line2"], p); add(p, cta["start"], cta["end"])
    p = os.path.join(tmp, "prod.png"); draw_product(W, H, cta, p); add(p, cta["start"] + 0.4, cta["end"], True)
    endpng = os.path.join(tmp, "end.png"); draw_end_screen(W, H, endpng, es.get("banner"), es.get("banner_crop"))

    # cutaways (new farm footage / photos): pre-rendered, laid over the picture under all graphics
    brolls = []
    for i, br in enumerate(plan.get("broll", [])):
        if br["end"] <= t0:
            continue
        bp = os.path.join(tmp, f"broll{i}.mp4")
        print("cutaway", i, br["src"])
        render_broll(br, W, H, bp)
        brolls.append((bp, br["start"] - t0, br["end"] - t0))

    # keep only layers that touch the render window, shift to output time
    layers = [(png, max(a, t0) - t0, b - t0, f) for png, a, b, f in layers if b > t0]

    # -reinit_filter 0: v3 switches pixel format mid-stream (yuvj420p shots near the end);
    # letting ffmpeg rebuild the graph there resets trim/overlay timing and drops ~30s.
    cmd = ["ffmpeg", "-y", "-v", "error", "-stats", "-reinit_filter", "0",
           "-ss", f"{t0}", "-t", f"{cut - t0:.3f}", "-i", src]
    for bp, *_ in brolls:
        cmd += ["-i", bp]
    for png, *_ in layers:
        cmd += ["-loop", "1", "-t", f"{cut - t0:.3f}", "-i", png]   # no longer than the main picture
    cmd += ["-loop", "1", "-t", f"{es['duration']}", "-i", endpng]
    cmd += ["-ss", f"{t0}", "-i", src]           # audio: runs on under the end card

    zexpr = zoom_expr([z for z in plan["zooms"] if z["end"] > t0], t0)
    fc = [f"[0:v]setpts=PTS-STARTPTS,fps=30,scale=in_range=auto:out_range=tv,format=yuv420p,"
          f"scale=w='trunc({W}*({zexpr})/2)*2':h='trunc({H}*({zexpr})/2)*2':eval=frame:flags=lanczos,"
          f"crop={W}:{H}:'(in_w-out_w)/2':'(in_h-out_h)/2',"
          f"setsar=1,format=yuv420p[v0]"]
    last = "v0"
    for j, (bp, a, b) in enumerate(brolls, start=1):
        fc.append(f"[{j}:v]setpts=PTS-STARTPTS+{a:.3f}/TB,format=yuv420p[b{j}]")
        fc.append(f"[{last}][b{j}]overlay=0:0:eof_action=pass:enable='between(t,{a:.3f},{b:.3f})'[vb{j}]")
        last = f"vb{j}"
    nb = len(brolls)
    for i, (png, a, b, fade) in enumerate(layers, start=1):
        chain = f"[{i + nb}:v]format=rgba"
        if fade:
            chain += f",fade=t=in:st={a:.3f}:d=0.3:alpha=1,fade=t=out:st={b - 0.3:.3f}:d=0.3:alpha=1"
        fc.append(chain + f"[o{i}]")
        fc.append(f"[{last}][o{i}]overlay=0:0:shortest=1:enable='between(t,{a:.3f},{b:.3f})'[v{i}]")
        last = f"v{i}"
    ei = len(layers) + nb + 1
    fc.append(f"[{ei}:v]format=yuv420p,fps=30,fade=t=in:st=0:d=0.5,"
              f"fade=t=out:st={es['duration'] - 0.8}:d=0.8,setsar=1[ve]")
    fc.append(f"[{last}][ve]concat=n=2:v=1:a=0[vout]")
    a_end = src_dur - t0
    fc.append(f"[{ei + 1}:a]atrim=duration={a_end:.3f},asetpts=PTS-STARTPTS,"
              f"afade=t=out:st={a_end - 1.0:.3f}:d=1.0,apad=whole_dur={total:.3f}[aout]")

    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    out = os.path.join(HERE, "out", name)
    cmd += ["-filter_complex", ";".join(fc), "-map", "[vout]", "-map", "[aout]",
            "-c:v", "libx264", "-preset", preset, "-crf", str(crf), "-r", "30",
            "-c:a", "aac", "-b:a", "192k", "-t", f"{total:.3f}", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)
    shutil.rmtree(tmp, ignore_errors=True)
    print("wrote", out, f"({total:.1f}s)")


if __name__ == "__main__":
    main()
