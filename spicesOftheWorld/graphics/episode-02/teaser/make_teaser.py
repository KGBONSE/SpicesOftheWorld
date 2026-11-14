"""Episode 2 'coming tomorrow' teaser graphics built from the real thumbnail.
Outputs: landscape 1920x1080 (LinkedIn/YouTube community), square 1080 (Instagram/Facebook), vertical 1080x1920 (TikTok/Stories).
Edit DAY / LINES below to change the wording. Run: python3 make_teaser.py"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
THUMB = os.path.join(HERE, "..", "thumbnail", "thumb_D_which_one.png")
FONTS = os.path.join(HERE, "..", "..", "..", "video", "episode-01", "fonts")
DARK = (74, 16, 20); DARK2 = (107, 27, 31); ORANGE = (224, 118, 16); CREAM = (253, 243, 228); GOLD = (253, 214, 66); RED = (200, 28, 34)
DAY = "TOMORROW"
SUB = "Sunday 15 November  ·  1pm  ·  on YouTube"
def F(s, w="ExtraBold"): return ImageFont.truetype(os.path.join(FONTS, f"Inter-{w}.otf"), s)

def bg(w, h):
    im = Image.new("RGB", (w, h), DARK); d = ImageDraw.Draw(im)
    for y in range(h):  # soft vertical gradient
        t = y / h; d.line([(0, y), (w, y)], fill=tuple(int(DARK2[i] * (1 - t) + DARK[i] * t * 0.7) for i in range(3)))
    return im

def place_thumb(im, x, y, w):
    th = Image.open(THUMB).convert("RGB"); h = round(w * th.height / th.width)
    th = th.resize((w, h), Image.LANCZOS)
    sh = Image.new("RGBA", (w + 80, h + 80), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((40, 48, w + 40, h + 48), 26, fill=(0, 0, 0, 170))
    im.paste(sh.filter(ImageFilter.GaussianBlur(18)), (x - 40, y - 40), sh.filter(ImageFilter.GaussianBlur(18)))
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w, h), 22, fill=255)
    im.paste(th, (x, y), m)
    ImageDraw.Draw(im).rounded_rectangle((x - 3, y - 3, x + w + 3, y + h + 3), 25, outline=CREAM, width=6)
    return h

def centre(d, cx, y, text, font, fill, stroke=0):
    w = d.textlength(text, font=font); d.text((cx - w / 2, y), text, font=font, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0)); return w

def pill(d, cx, y, text, font, fill, fg, padx=44, pady=18):
    w = d.textlength(text, font=font); b = d.textbbox((0, 0), text, font=font); h = b[3]
    d.rounded_rectangle((cx - w / 2 - padx, y, cx + w / 2 + padx, y + h + pady * 2), (h + pady * 2) // 2, fill=fill)
    d.text((cx - w / 2, y + pady - b[1] / 2), text, font=font, fill=fg); return h + pady * 2

def landscape():
    W, H = 1920, 1080; im = bg(W, H); d = ImageDraw.Draw(im)
    tw = 1120; th = round(tw * 720 / 1280); tx = 70; ty = (H - th) // 2 + 30
    centre(d, W / 2, 70, "SPICES OF THE WORLD  ·  EPISODE 2  ·  SENEGAL", F(44, "Bold"), CREAM)
    place_thumb(im, tx, ty, tw); d = ImageDraw.Draw(im)
    cx = tx + tw + (W - tx - tw) / 2
    centre(d, cx, 300, "NEW EPISODE", F(58), CREAM)
    centre(d, cx, 385, "DROPS", F(110), CREAM)
    pill(d, cx, 550, DAY, F(78), GOLD, DARK, padx=36, pady=26)
    centre(d, cx, 740, "Sunday 15 November", F(42, "SemiBold"), CREAM)
    centre(d, cx, 800, "1pm on YouTube", F(42, "SemiBold"), CREAM)
    centre(d, cx, 900, "@fudi.people", F(46), ORANGE)
    im.save(os.path.join(HERE, "ep02_tomorrow_landscape_1920x1080.png"))

def square():
    W = H = 1080; im = bg(W, H); d = ImageDraw.Draw(im)
    centre(d, W / 2, 50, "SPICES OF THE WORLD  ·  EPISODE 2", F(38, "Bold"), CREAM)
    centre(d, W / 2, 112, "NEW EPISODE DROPS", F(74), CREAM)
    pill(d, W / 2, 212, DAY, F(92), GOLD, DARK, padx=46, pady=22)
    tw = 900; th = place_thumb(im, (W - tw) // 2, 372, tw); d = ImageDraw.Draw(im)
    centre(d, W / 2, 372 + th + 34, SUB, F(40, "SemiBold"), CREAM)
    centre(d, W / 2, 372 + th + 92, "@fudi.people", F(44), ORANGE)
    im.save(os.path.join(HERE, "ep02_tomorrow_square_1080.png"))

def vertical():
    W, H = 1080, 1920; im = bg(W, H); d = ImageDraw.Draw(im)
    # keep text clear of the top ~220px and bottom ~420px that TikTok/Reels cover with their own buttons
    centre(d, W / 2, 250, "SPICES OF THE WORLD", F(50, "Bold"), CREAM)
    centre(d, W / 2, 322, "EPISODE 2  ·  SENEGAL", F(50, "Bold"), ORANGE)
    centre(d, W / 2, 440, "NEW EPISODE", F(104), CREAM)
    centre(d, W / 2, 560, "DROPS", F(104), CREAM)
    pill(d, W / 2, 710, DAY, F(116), GOLD, DARK, padx=50, pady=28)
    tw = 1000; th = place_thumb(im, (W - tw) // 2, 940, tw); d = ImageDraw.Draw(im)
    centre(d, W / 2, 940 + th + 44, "Sunday 15 November  ·  1pm", F(48, "SemiBold"), CREAM)
    centre(d, W / 2, 940 + th + 108, "on YouTube  ·  @fudi.people", F(48), ORANGE)
    im.save(os.path.join(HERE, "ep02_tomorrow_vertical_1080x1920.png"))

if __name__ == "__main__":
    landscape(); square(); vertical(); print("ok")
