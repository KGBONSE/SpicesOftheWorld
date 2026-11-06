"""Episode 2 on-screen text overlays: full-frame 1920x1080 transparent PNGs -> overlays-landscape/.

Brand colours and style follow episode-01/make_overlays.py (Inter, marigold accent, cream text, maroon panels).
Health claims come from knowledge-base/spice-profiles (mustard.md, garlic.md); keep wording as cautious as the notes.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "..", "episode-01", "fonts")
OUT = os.path.join(HERE, "overlays-landscape")
W, H = 1920, 1080
ORANGE = (224, 118, 16, 255)
CREAM = (253, 243, 228, 255)
DARK = (107, 27, 31)
GOLD = (231, 154, 46, 255)


def inter(size, weight="Bold"):
    return ImageFont.truetype(os.path.join(FONTS, f"Inter-{weight}.otf"), size)


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


def health(name, heading, rows):
    """Right-hand research card (also covers the bright window on the right of the frame)."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x0, x1, pad = 1190, W - 60, 44
    hf, af, bf = inter(46, "ExtraBold"), inter(40), inter(34, "Medium")
    body = [(a, wrap(d, b, bf, x1 - x0 - 2 * pad)) for a, b in rows]
    h = 62 + 62 + sum(52 + 44 * len(bl) + 34 for _, bl in body) + 10
    y0 = (H - h) // 2 - 30
    d.rounded_rectangle((x0, y0, x1, y0 + h), 32, fill=DARK + (225,))
    d.text((x0 + pad, y0 + 38), heading, font=hf, fill=CREAM)
    d.rectangle((x0 + pad, y0 + 100, x0 + pad + 100, y0 + 108), fill=ORANGE)
    y = y0 + 140
    for a, bl in body:
        d.text((x0 + pad, y), a, font=af, fill=GOLD)
        y += 52
        for l in bl:
            d.text((x0 + pad, y), l, font=bf, fill=CREAM)
            y += 44
        y += 34
    img.save(os.path.join(OUT, name + ".png"))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    health("health_yassa", "What the research says", [
        ("Mustard marinade", "cuts harmful compounds that form when meat chars on the grill"),
        ("Mustard seed", "anti-inflammatory action (early research)"),
        ("Garlic", "supports heart health"),
    ])
    print("overlays written to", OUT)
