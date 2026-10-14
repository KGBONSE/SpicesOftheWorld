"""Episode 1 on-screen text overlays: full-frame 1080x1920 transparent PNGs.

Brand (docs/brand.md): Inter, Marigold #E07610 accent, Cream #FDF3E4 text,
Maroon #6B1B1F panels, Gold #E79A2E sub-lines, Ink #3A1210 text on marigold.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
OUT = os.path.join(HERE, "overlays")
W, H = 1080, 1920
ORANGE = (224, 118, 16, 255)    # Marigold
CREAM = (253, 243, 228, 255)
DARK = (107, 27, 31)            # Maroon panel
GOLD = (231, 154, 46, 255)
INK = (58, 18, 16)


WEIGHTS = {"Regular": 400, "Medium": 500, "Bold": 700, "ExtraBold": 800}


def inter(size, weight="Bold"):
    """Inter variable font (put Inter-Variable.ttf in fonts/, from Google Fonts)."""
    f = ImageFont.truetype(os.path.join(FONTS, "Inter-Variable.ttf"), size)
    axes = [(a["minimum"] + a["maximum"]) / 2 for a in f.get_variation_axes()]
    for i, a in enumerate(f.get_variation_axes()):
        name = a["name"] if isinstance(a["name"], str) else a["name"].decode()
        if name.lower().startswith("weight"):
            axes[i] = WEIGHTS[weight]
        elif name.lower().startswith("optical"):
            axes[i] = min(max(size, a["minimum"]), a["maximum"])
    f.set_variation_by_axes(axes)
    return f


def wrap(d, text, font, maxw):
    lines, cur = [], ""
    for word in text.split():
        t = (cur + " " + word).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    return lines


def shadowed(img, draw_fn, blur=6, offset=(0, 4), alpha=150):
    """Draw text twice: a blurred dark shadow layer, then the real layer."""
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(sh), shadow=(0, 0, 0, alpha))
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    img.alpha_composite(sh, offset)
    draw_fn(ImageDraw.Draw(img), shadow=None)


def caption(name, text, sub=None, y=1380):
    """Lower-third: dark translucent panel, orange accent bar, cream text."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f, fs = inter(58), inter(40, "Medium")
    lines = wrap(d, text, f, 860)
    slines = wrap(d, sub, fs, 860) if sub else []
    h = 60 + len(lines) * 78 + (len(slines) * 56 + 14 if slines else 0)
    d.rounded_rectangle((60, y, W - 60, y + h), 28, fill=DARK + (215,))
    d.rectangle((60, y + 28, 72, y + h - 28), fill=ORANGE)
    ty = y + 30
    for l in lines:
        d.text((104, ty), l, font=f, fill=CREAM)
        ty += 78
    ty += 14
    for l in slines:
        d.text((104, ty), l, font=fs, fill=GOLD)
        ty += 56
    img.save(os.path.join(OUT, name + ".png"))


def label(name, text, y=1480):
    """Ingredient pill: orange, centred, dark text."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f = inter(56)
    tw = d.textlength(text, font=f)
    x0 = (W - tw) / 2 - 44
    d.rounded_rectangle((x0, y, W - x0, y + 104), 52, fill=ORANGE)
    d.text(((W - tw) / 2, y + 18), text, font=f, fill=INK + (255,))
    img.save(os.path.join(OUT, name + ".png"))


def title(name):
    """Cold-open title: SUYA · CHINCHINGA."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f, fs = inter(124, "ExtraBold"), inter(44, "Medium")
    y = 300
    d.rounded_rectangle((90, y, W - 90, y + 470), 36, fill=DARK + (200,))
    for word, yy in (("SUYA", y + 40), ("CHINCHINGA", y + 210)):
        d.text(((W - d.textlength(word, font=f)) / 2, yy), word, font=f, fill=CREAM)
    d.rectangle((W / 2 - 70, y + 192, W / 2 + 70, y + 202), fill=ORANGE)
    s = "One spice mix · two names"
    d.text(((W - d.textlength(s, font=fs)) / 2, y + 380), s, font=fs, fill=GOLD)
    img.save(os.path.join(OUT, name + ".png"))


def health(name):
    """Health card: four rows on a dark panel, centred."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    rows = [("Grains of paradise", "metabolism"),
            ("Grains of selim", "gut & lungs"),
            ("Ginger", "digestion & nausea"),
            ("Black pepper", "helps you absorb the rest")]
    y0, rh = 560, 170
    d.rounded_rectangle((60, y0 - 150, W - 60, y0 + len(rows) * rh + 40), 32, fill=DARK + (225,))
    hf = inter(64, "ExtraBold")
    t = "What the research says"
    d.text(((W - d.textlength(t, font=hf)) / 2, y0 - 120), t, font=hf, fill=CREAM)
    d.rectangle((W / 2 - 50, y0 - 24, W / 2 + 50, y0 - 16), fill=ORANGE)
    for i, (a, b) in enumerate(rows):
        y = y0 + 20 + i * rh
        d.text((110, y), a, font=inter(54), fill=GOLD)
        d.text((110, y + 70), b, font=inter(46, "Regular"), fill=CREAM)
    img.save(os.path.join(OUT, name + ".png"))


def cta(name):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    y = 1360
    d.rounded_rectangle((60, y, W - 60, y + 250), 28, fill=DARK + (225,))
    f1, f2 = inter(48, "Medium"), inter(76)
    t1, t2 = "Full recipe + get the blend", "fudipeople.com"
    d.text(((W - d.textlength(t1, font=f1)) / 2, y + 40), t1, font=f1, fill=CREAM)
    d.text(((W - d.textlength(t2, font=f2)) / 2, y + 118), t2, font=f2, fill=ORANGE)
    img.save(os.path.join(OUT, name + ".png"))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    title("title")
    caption("hook", "The spice Europe forgot.", "West Africa never did.")
    caption("geo", "Ghana", "Still the world's main producer of grains of paradise")
    caption("trade", "Once Europe's pepper substitute.", "Now West Africa's secret.")
    caption("paradol", "Paradol", "The same heat compound as ginger")
    caption("dose", "Cooking tip", "Use 2–3x more grains of paradise than black pepper")
    caption("alsoseasons", "Yaji also seasons", "Kilishi (dried beef) · roasted plantain & corn · boiled eggs")
    caption("samefire", "CHINCHINGA (Ghana) · SUYA (Nigeria)", "Same mix, same fire")
    caption("samemix", "Chinchinga or suya", "Same mix")
    caption("close", "Spices of Africa", "Grown in Sidcup, rooted in Ghana")
    label("l_selim", "Grains of selim")
    label("l_gop", "Grains of paradise")
    label("l_chilli", "Dried chillies")
    label("l_peanut", "Kuli-kuli · crushed peanuts")
    label("l_ginger", "Ginger powder")
    label("l_cube", "Stock cube")
    label("l_pepper", "Salt + black pepper")
    label("l_yaji", "= YAJI")
    label("l_toast", "Tip: lightly toast your spices first")
    label("l_soak", "Soak the skewers first")
    label("l_veg", "Tip: veg in between the meat")
    label("l_spray", "Spray with water (or beer)")
    label("l_late", "Yaji goes on near the end")
    label("l_oil", "Finish: a drizzle of olive oil")
    health("health")
    cta("cta")
    print("overlays written to", OUT)
