"""Vertical (1080x1920) captions for the Yassa Short. Output: overlays-vertical-short/.
Captions sit at y~300-560: below the top 220 px and well above the bottom ~450 px that TikTok/Reels/Shorts cover."""
import os
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "..", "episode-01", "fonts")
OUT = os.path.join(HERE, "overlays-vertical-short")
W, H = 1080, 1920
DARK = (107, 27, 31); ORANGE = (224, 118, 16); CREAM = (253, 243, 228); GOLD = (253, 214, 66)
F = lambda s, w="ExtraBold": ImageFont.truetype(os.path.join(FONTS, f"Inter-{w}.otf"), s)

def cap(name, main, sub=None, size=86, y=300):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    lines = main.split("\n"); fm = F(size); fs = F(52, "SemiBold")
    lh = int(size * 1.18); h = 50 + lh * len(lines) + (78 if sub else 0) + 30
    wmax = max([d.textlength(l, font=fm) for l in lines] + ([d.textlength(sub, font=fs)] if sub else []))
    x0 = (W - wmax) / 2 - 50; d.rounded_rectangle((x0, y, W - x0, y + h), 36, fill=DARK + (228,))
    yy = y + 40
    for l in lines:
        d.text(((W - d.textlength(l, font=fm)) / 2, yy), l, font=fm, fill=CREAM); yy += lh
    if sub: d.text(((W - d.textlength(sub, font=fs)) / 2, yy + 8), sub, font=fs, fill=GOLD)
    im.save(os.path.join(OUT, name + ".png"))

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    cap("s_hook", "9 SPICES.\n1 BOWL.", "Senegal's Yassa", size=120)
    for n, a, b in [("s_onion", "Dried onion", "35 g"), ("s_garlic", "Garlic", "20 g"), ("s_mustard", "Mustard seed", "18 g"),
                    ("s_chilli", "Chilli flakes", "3 g"), ("s_bay", "Bay leaf", "1 g")]:
        cap(n, a, b)
    cap("s_toast", "Toast it", "2 to 3 minutes in a dry pan")
    cap("s_bowls", "Chicken · Lamb & goat\n· Pork ·", "Marinated in the Yassa mix", size=72)
    cap("s_grill", "Onto the grill")
    cap("s_baste", "Baste with\nthe marinade")
    cap("s_turn", "Low and slow")
    cap("s_onions", "Then the\nonion sauce")
    cap("s_end", "Full episode\non YouTube", "@fudi.people", size=100)
    print("ok")
