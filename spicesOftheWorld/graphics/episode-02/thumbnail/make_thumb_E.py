"""Episode 2 thumbnail E ('BOTH WRONG.') for A/B testing against thumb_D_which_one.png.
Different on purpose: one hero image (the jollof pot), two words, crossed-out Nigeria and Ghana flags.
Run: python3 make_thumb_E.py   (needs graphics/fonts/Anton-Regular.ttf, OFL licence)"""
import os, math
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1280, 720
F = lambda s: ImageFont.truetype(os.path.join(HERE, "..", "..", "fonts", "Anton-Regular.ttf"), s)

pot = Image.open(os.path.join(HERE, "source", "pot_frame_IMG_0658.jpg")).convert("RGB")
src = pot
bgp = ImageEnhance.Brightness(src.resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(28))).enhance(0.55)
fg = src.crop((300, 0, 1620, 1080)).resize((880, 720), Image.LANCZOS)          # whole pot, sits on the right
pot = bgp.copy(); pot.paste(fg, (W - 880, 0))
pot = ImageEnhance.Color(pot).enhance(1.6); pot = ImageEnhance.Contrast(pot).enhance(1.32)
r, g, b = pot.split(); pot = Image.merge("RGB", (r.point(lambda v: min(255, int(v * 1.08))), g, b.point(lambda v: int(v * 0.86))))
pot = ImageEnhance.Sharpness(pot).enhance(1.7)

# dark fade on the left so the words read at phone size
fade = Image.new("L", (W, H), 0); fd = ImageDraw.Draw(fade)
for x in range(W):
    a = 245 if x < 405 else max(0, int(245 * (1 - (x - 405) / 230)))
    fd.line([(x, 0), (x, H)], fill=a)
c = Image.composite(Image.new("RGB", (W, H), (14, 8, 6)), pot, fade)
d = ImageDraw.Draw(c)

def star(cx, cy, r):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5; rr = r if i % 2 == 0 else r * 0.38
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    return pts

def flag(x, y, w, h, kind):
    f = Image.new("RGB", (w, h)); fd = ImageDraw.Draw(f)
    if kind == "nigeria":
        fd.rectangle((0, 0, w, h), fill=(255, 255, 255)); fd.rectangle((0, 0, w // 3, h), fill=(0, 135, 81)); fd.rectangle((w - w // 3, 0, w, h), fill=(0, 135, 81))
    else:
        fd.rectangle((0, 0, w, h // 3), fill=(206, 17, 38)); fd.rectangle((0, h // 3, w, 2 * h // 3), fill=(252, 209, 22)); fd.rectangle((0, 2 * h // 3, w, h), fill=(0, 107, 63))
        fd.polygon(star(w / 2, h / 2, h * 0.17), fill=(0, 0, 0))
    c.paste(f, (x, y)); d.rectangle((x - 4, y - 4, x + w + 4, y + h + 4), outline=(255, 255, 255), width=5)
    for (a, b_) in (((x - 14, y - 14), (x + w + 14, y + h + 14)), ((x - 14, y + h + 14), (x + w + 14, y - 14))):   # red cross
        d.line([a, b_], fill=(0, 0, 0), width=30); d.line([a, b_], fill=(226, 24, 30), width=20)

flag(52, 50, 200, 132, "nigeria"); flag(300, 50, 200, 132, "ghana")
d.text((42, 212), "BOTH", font=F(196), fill=(255, 255, 255), stroke_width=10, stroke_fill=(0, 0, 0))
d.text((42, 440), "WRONG.", font=F(196), fill=(255, 214, 0), stroke_width=10, stroke_fill=(0, 0, 0))
c.save(os.path.join(HERE, "thumb_E_both_wrong.png")); print("ok")
