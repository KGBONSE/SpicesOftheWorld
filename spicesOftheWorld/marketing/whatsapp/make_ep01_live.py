"""WhatsApp Status image (1080x1920) saying Episode 1 is live."""
import os, sys
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "video", "episode-01"))
from finish_v3 import logo, rounded, CREAM, GOLD, MARIGOLD
F = lambda w, s: ImageFont.truetype(os.path.join(ROOT, "video/episode-01/fonts", f"Inter-{w}.otf"), s)
W, H = 1080, 1920
im = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(im)
for y in range(H):
    k = y / H; d.line([(0, y), (W, y)], fill=(int(78 - 30 * k), int(26 - 10 * k), int(20 - 8 * k), 255))
lg = logo(ROOT); lh = 150; lg = lg.resize((int(lg.width * lh / lg.height), lh), Image.LANCZOS)
im.alpha_composite(lg, ((W - lg.width) // 2, 110))
def ctext(y, t, f, fill, track=0):
    if track:
        widths = [d.textlength(ch, font=f) + track for ch in t]; x = (W - sum(widths) + track) / 2
        for ch, w in zip(t, widths): d.text((x, y), ch, font=f, fill=fill, anchor="lm"); x += w
    else: d.text((W / 2, y), t, font=f, fill=fill, anchor="mm")
ctext(330, "SPICES OF THE WORLD", F("Bold", 40), GOLD, track=8)
ctext(395, "EPISODE 1", F("ExtraBold", 84), CREAM)
th = Image.open(os.path.join(ROOT, "thumbnails/episode-01/A_spice_europe_forgot.jpg")).convert("RGBA")
tw = 960; th = rounded(th.resize((tw, int(tw * th.height / th.width)), Image.LANCZOS), 28)
ty = 480; d.rounded_rectangle((W/2 - tw/2 - 8, ty - 8, W/2 + tw/2 + 8, ty + th.height + 8), 34, fill=GOLD)
im.alpha_composite(th, ((W - tw) // 2, ty))
y = ty + th.height + 110
for line in ("Suya & Chinchinga:", "The Forgotten Spice", "Ghana and Nigeria Share"):
    ctext(y, line, F("ExtraBold", 64), CREAM); y += 82
y += 60
pill = "WE ARE LIVE  ·  WATCH NOW"; f = F("ExtraBold", 46)
pw = d.textlength(pill, font=f) + 100
d.rounded_rectangle((W/2 - pw/2, y - 52, W/2 + pw/2, y + 52), 52, fill=MARIGOLD); ctext(y, pill, f, (40, 14, 10, 255))
ctext(y + 130, "From Makola Market in Accra to our farm in Sidcup", F("Medium", 36), CREAM)
ctext(H - 150, "youtu.be/K3wfXvK3ss0", F("Bold", 50), GOLD)
im.convert("RGB").save(os.path.join(HERE, "ep01_whatsapp_live.jpg"), quality=92); print("ok")
