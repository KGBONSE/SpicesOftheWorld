"""YouTube banner (2560x1440) for Fudi People.

Text and a sharp photo panel sit inside YouTube's mobile safe area
(1546x423, centred); a blurred, darkened copy of the photo fills the rest.
Source photo: the smoker racks photo (IMG_4946.JPG, 1080x1350).
"""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps

SRC = sys.argv[1] if len(sys.argv) > 1 else "IMG_4946.JPG"
OUT = sys.argv[2] if len(sys.argv) > 2 else "fudi-youtube-banner.jpg"
FONTS = "/usr/share/fonts/truetype/google-fonts/"  # Lora + Poppins

W, H = 2560, 1440
SX0, SY0, SX1, SY1 = 507, 508, 2053, 931  # mobile safe area

sm = Image.open(SRC).convert("RGB")
racks = sm.crop((0, 230, 1080, 880))
bg = ImageOps.fit(racks, (W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(18))
bg = ImageEnhance.Brightness(bg).enhance(0.35)
bg = ImageEnhance.Color(bg).enhance(1.2)
bg = Image.blend(bg, Image.new("RGB", (W, H), (58, 20, 8)), 0.35)
d = ImageDraw.Draw(bg)

pw, ph = 700, 393
px, py = SX1 - pw - 15, SY0 + 15
src = sm.crop((0, 260, 1080, 260 + int(1080 * ph / pw)))
panel = ImageEnhance.Color(src.resize((pw, ph), Image.LANCZOS)).enhance(1.15)
mask = Image.new("L", (pw, ph), 0)
ImageDraw.Draw(mask).rounded_rectangle((0, 0, pw - 1, ph - 1), 24, fill=255)
d.rounded_rectangle((px - 7, py - 7, px + pw + 6, py + ph + 6), 30, fill=(240, 120, 30))
bg.paste(panel, (px, py), mask)

title = ImageFont.truetype(FONTS + "Lora-Variable.ttf", 124)
title.set_variation_by_name("Bold")
x = SX0 + 30
d.text((x, SY0 + 30), "Fudi People", font=title, fill=(255, 243, 226))
d.rectangle((x, SY0 + 200, x + 100, SY0 + 208), fill=(240, 120, 30))
d.text((x, SY0 + 238), "Grown & smoked in Sidcup, London",
       font=ImageFont.truetype(FONTS + "Poppins-Medium.ttf", 40), fill=(255, 214, 170))
d.text((x, SY0 + 305), "Chilli oil  ·  Spices from six regions",
       font=ImageFont.truetype(FONTS + "Poppins-Regular.ttf", 34), fill=(230, 200, 170))
bg.save(OUT, quality=94)
