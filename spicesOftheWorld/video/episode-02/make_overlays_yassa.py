"""Yassa mix build-up labels (landscape 1920x1080 transparent PNGs -> overlays-landscape/).
Edit LABELS to change the wording; amounts are per 100 g of finished blend (from Kofi's recipe sheet)."""
import os
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "..", "episode-01", "fonts")
OUT = os.path.join(HERE, "overlays-landscape")
W, H = 1920, 1080
ORANGE = (224, 118, 16, 255); CREAM = (253, 243, 228, 255); DARK = (107, 27, 31); GOLD = (231, 154, 46, 255)
def inter(s, w="Bold"): return ImageFont.truetype(os.path.join(FONTS, f"Inter-{w}.otf"), s)

LABELS = {  # file: (name, grams or None)
    "y_onion": ("Dried onion", "35 g"), "y_garlic": ("Garlic", "20 g"), "y_mustard": ("Yellow mustard", "18 g"),
    "y_lemon": ("Lemon peel", "9 g"), "y_salt": ("Salt", "9 g"), "y_pepper": ("Black pepper", "3.5 g"),
    "y_thyme": ("Dried thyme", "1.5 g"), "y_chilli": ("Farm chilli flakes", "3 g"), "y_bay": ("Bay leaf", "1 g"),
}

def label(file, name, grams):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    nf, gf = inter(58, "ExtraBold"), inter(58, "ExtraBold")
    nw = d.textlength(name, font=nf); gw = d.textlength(grams, font=gf)
    x0, y0, pad = 70, 70, 36
    w = pad + nw + 40 + gw + pad
    d.rounded_rectangle((x0, y0, x0 + w, y0 + 110), 28, fill=DARK + (225,))
    d.rectangle((x0 + pad + nw + 18, y0 + 28, x0 + pad + nw + 24, y0 + 82), fill=ORANGE)
    d.text((x0 + pad, y0 + 20), name, font=nf, fill=CREAM)
    d.text((x0 + pad + nw + 40, y0 + 20), grams, font=gf, fill=GOLD)
    img.save(os.path.join(OUT, file + ".png"))

def title(file, line1, line2):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    f1, f2 = inter(120, "ExtraBold"), inter(46, "Medium")
    w1, w2 = d.textlength(line1, font=f1), d.textlength(line2, font=f2)
    pw = max(w1, w2) + 120; x0 = (W - pw) / 2; y0 = 380
    d.rounded_rectangle((x0, y0, x0 + pw, y0 + 270), 34, fill=DARK + (215,))
    d.text(((W - w1) / 2, y0 + 30), line1, font=f1, fill=CREAM)
    d.rectangle(((W - 120) / 2, y0 + 175, (W + 120) / 2, y0 + 183), fill=ORANGE)
    d.text(((W - w2) / 2, y0 + 195), line2, font=f2, fill=GOLD)
    img.save(os.path.join(OUT, file + ".png"))

def banner(file, text, sub=None):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    f1, f2 = inter(62, "ExtraBold"), inter(40, "Medium")
    w1 = d.textlength(text, font=f1); w2 = d.textlength(sub, font=f2) if sub else 0
    pw = max(w1, w2) + 90; h = 110 if not sub else 165; x0, y0 = 70, 70
    d.rounded_rectangle((x0, y0, x0 + pw, y0 + h), 28, fill=DARK + (225,))
    d.text((x0 + 45, y0 + 20), text, font=f1, fill=CREAM)
    if sub: d.text((x0 + 45, y0 + 100), sub, font=f2, fill=GOLD)
    img.save(os.path.join(OUT, file + ".png"))

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for k, (n, g) in LABELS.items(): label(k, n, g)
    title("y_title", "YASSA MIX", "Part 1: build the blend (per 100 g)")
    banner("y_toast", "TOAST the spices", "Dry pan, 2 to 3 minutes")
    banner("y_blend", "Then blend to a fine powder", "Your finished Yassa mix")
    banner("y_marinate", "Marinate the lamb", "Rub in the Yassa mix")
    banner("y_grill", "Grill it", "Yassa lamb, ready")
    print("ok")
