"""
SANKO — final print-ready label composer.
Builds front + back pages for all 5 flavors:
  pineapple (black), mixed_fruit (maroon), plum (deep purple),
  ginger (cream), plum_pink (renamed from "Plum & Rhubarb" -> "Plum", pink bg kept as-is)

Backs are rebuilt on the new template (adopted from the red "PLUM WINE" QR
reference): big centered title, story text, tasting note, hammer&grape icon,
ALC/VOL line, DRINK RESPONSIBLY — QR code removed. Essential print-compliance
fields (allergens / producer / storage / lot no.) are kept, in the same quiet
footnote style, since the label still has to clear bottling requirements.
"""
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, mm
from reportlab.lib.colors import Color
from pypdf import PdfReader, PdfWriter
import os

TRIM_W, TRIM_H = 3.15 * inch, 3.94 * inch
BLEED = 3 * mm
PAGE_W, PAGE_H = TRIM_W + 2 * BLEED, TRIM_H + 2 * BLEED

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets")
OUT = os.path.join(HERE, "..", "out")
os.makedirs(OUT, exist_ok=True)

def C(hexstr):
    hexstr = hexstr.lstrip("#")
    r, g, b = (int(hexstr[i:i+2], 16) for i in (0, 2, 4))
    return Color(r/255, g/255, b/255)

STORY_LINES = [
    "Crafted in honor of the Balee people of",
    "Santrokofi — mountain dwellers, artisans, and",
    "keepers of the Selee language — whose homeland,",
    "Sanko, sits among the rolling Ghana–Togo hills.",
]

FLAVORS = [
    dict(
        key="pineapple", bg="bg_pineapple.png", mtn="mtn_pineapple.png", icon="icon_pineapple.png",
        name_lines=["PINEAPPLE", "WINE"], product="Pineapple Wine",
        name_col=C("#F3EADB"), sanko_col=C("#D6B248"), border_col=C("#D6B248"),
        tagline_col=C("#D6B248"), frame_bg=C("#F3EADB"), frame_ink=C("#1C1712"),
        tasting=["Bright and tropical, this pineapple wine offers a",
                 "crisp, refreshing sweetness with a tangy citrus",
                 "edge from sun-ripened fruit."],
    ),
    dict(
        key="pineapple_orange", bg="bg_pineapple_orange.png", mtn="mtn_pineapple_orange.png", icon="icon_pineapple_orange.png",
        name_lines=["PINEAPPLE", "WINE"], product="Pineapple Wine (Orange)",
        name_col=C("#FBF4E6"), sanko_col=C("#E9C65A"), border_col=C("#E9C65A"),
        tagline_col=C("#E9C65A"), frame_bg=C("#F3EADB"), frame_ink=C("#8A3A14"),
        tasting=["Bright and tropical, this pineapple wine offers a",
                 "crisp, refreshing sweetness with a tangy citrus",
                 "edge from sun-ripened fruit."],
    ),
    dict(
        key="mixed_fruit", bg="bg_mixed_fruit.png", mtn="mtn_mixed_fruit.png", icon="icon_mixed_fruit.png",
        name_lines=["MIXED FRUIT", "WINE"], product="Mixed Fruit Wine",
        name_col=C("#F3EADB"), sanko_col=C("#D6B248"), border_col=C("#D6B248"),
        tagline_col=C("#D6B248"), frame_bg=C("#F3EADB"), frame_ink=C("#5D141B"),
        tasting=["Delightfully balanced, this mixed fruit wine",
                 "offers a harmonious medley of tropical and",
                 "orchard fruits, with vibrant sweetness and a",
                 "refreshing finish."],
    ),
    dict(
        key="plum", bg="bg_plum.png", mtn="mtn_plum.png", icon="icon_plum.png",
        name_lines=["PLUM", "WINE"], product="Plum Wine",
        name_col=C("#F3EADB"), sanko_col=C("#D6B248"), border_col=C("#D6B248"),
        tagline_col=C("#D6B248"), frame_bg=C("#F3EADB"), frame_ink=C("#2A122E"),
        tasting=["Rich and fruity, this plum wine offers a smooth",
                 "and luscious flavor with subtle sweetness and a",
                 "touch of tartness from sun-ripened fruit."],
    ),
    dict(
        key="ginger", bg="bg_ginger.png", mtn="mtn_ginger.png", icon="icon_ginger.png",
        name_lines=["GINGER", "WINE"], product="Ginger Wine",
        name_col=C("#2B1B0E"), sanko_col=C("#7A1F2B"), border_col=C("#B0862F"),
        tagline_col=C("#B0862F"), frame_bg=C("#F3EADB"), frame_ink=C("#7A5A1E"),
        tasting=["Spicy and invigorating, this ginger wine offers a",
                 "warming blend of zesty ginger spice and natural",
                 "sweetness, for a unique, revitalising taste."],
    ),
    dict(
        key="plum_pink", bg="bg_plum_pink.png", mtn="mtn_plum_pink.png", icon="icon_plum_pink.png",
        name_lines=["PLUM"], product="Plum Wine (Rosé)",
        name_col=C("#5D141B"), sanko_col=C("#5D141B"), border_col=C("#5D141B"),
        tagline_col=C("#5D141B"), frame_bg=C("#F3EADB"), frame_ink=C("#5D141B"),
        tasting=["Lush and tangy, this plum wine offers a sweet",
                 "and tart flavor with mellow fruitiness and a",
                 "crisp, refreshing finish."],
    ),
]

def centered(cv, text, cy, font, size, col):
    cv.setFont(font, size)
    cv.setFillColor(col)
    cv.drawCentredString(PAGE_W / 2, cy, text)

def bg_image(cv, path):
    cv.drawImage(path, 0, 0, width=PAGE_W, height=PAGE_H)

def rule(cv, cx, y, w, col, width=1.1):
    cv.setStrokeColor(col)
    cv.setLineWidth(width)
    cv.line(cx - w/2, y, cx + w/2, y)

def frame(cv, col, inset):
    cv.setStrokeColor(col)
    cv.setLineWidth(1.4)
    cv.rect(inset, inset, PAGE_W - 2*inset, PAGE_H - 2*inset, stroke=1, fill=0)
    cv.setLineWidth(0.7)
    inset2 = inset + 5
    cv.rect(inset2, inset2, PAGE_W - 2*inset2, PAGE_H - 2*inset2, stroke=1, fill=0)


def front_page(cv, f):
    bg_image(cv, f"{ASSETS}/{f['bg']}")
    frame(cv, f["border_col"], BLEED + 10)

    top = PAGE_H - BLEED - 0.62*inch
    centered(cv, "SANKO", top, "Times-Bold", 40, f["sanko_col"])
    rule(cv, PAGE_W/2, top - 0.16*inch, 1.55*inch, f["border_col"])

    y = top - 0.52*inch
    for line in f["name_lines"]:
        centered(cv, line, y, "Times-Roman", 23, f["name_col"])
        y -= 0.34*inch

    centered(cv, "2 0 2 4", y - 0.06*inch, "Times-Roman", 13, f["tagline_col"])

    # Higgsfield-generated engraved mountain range (exact reference match)
    # with pine treeline — sits in the clear band between the date and tagline
    icon_w = 2.55*inch
    icon_h = icon_w * (392/1173)
    icon_cy = y - 0.46*inch
    cv.drawImage(f"{ASSETS}/mtnicon_{f['key']}.png",
                 PAGE_W/2 - icon_w/2, icon_cy - icon_h/2,
                 width=icon_w, height=icon_h, mask="auto")

    bot = BLEED + 0.60*inch
    centered(cv, "C U L T U R A L L Y   R O O T E D", bot + 0.34*inch, "Times-Roman", 11.5, f["tagline_col"])
    centered(cv, "13.5% ABV  •  750ML", bot, "Times-Roman", 11.5, f["name_col"])


def wrap_to_lines(text, max_chars):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if len(trial) > max_chars and cur:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def back_page(cv, f):
    # cream parchment card, framed — same quiet paper the current backs use
    bg_image(cv, f"{ASSETS}/bg_ginger.png")
    frame(cv, f["frame_ink"], BLEED + 12)

    cx = PAGE_W / 2
    y = PAGE_H - BLEED - 0.46*inch

    title = (f["name_lines"][0] + " WINE") if len(f["name_lines"]) == 1 else " ".join(f["name_lines"])
    centered(cv, title, y, "Times-Bold", 16.5, f["frame_ink"])
    y -= 0.225*inch
    centered(cv, "2 0 2 4", y, "Times-Roman", 9, f["frame_ink"])
    y -= 0.085*inch
    rule(cv, cx, y, 1.7*inch, f["frame_ink"])
    y -= 0.195*inch

    tasting_lines = []
    for t in f["tasting"]:
        tasting_lines.extend(wrap_to_lines(t, 58))
    tasting_lines = wrap_to_lines(" ".join(f["tasting"]), 54)

    cv.setFont("Times-Italic", 7.5)
    cv.setFillColor(f["frame_ink"])
    for line in STORY_LINES:
        cv.drawCentredString(cx, y, line)
        y -= 0.122*inch
    y -= 0.075*inch

    cv.setFont("Times-Roman", 7.7)
    for line in tasting_lines:
        cv.drawCentredString(cx, y, line)
        y -= 0.122*inch
    y -= 0.11*inch

    # hammer & grape icon
    icon_sz = 0.40*inch
    cv.drawImage(f"{ASSETS}/{f['icon']}", cx - icon_sz/2, y - icon_sz, width=icon_sz, height=icon_sz, mask="auto")
    y -= icon_sz + 0.12*inch

    centered(cv, "13.5% ALC / VOL", y, "Times-Bold", 10, f["frame_ink"])
    y -= 0.185*inch
    centered(cv, "DRINK RESPONSIBLY", y, "Times-Bold", 8, f["frame_ink"])
    y -= 0.125*inch
    centered(cv, "Not suitable for persons under 18.  Contains sulphites.", y, "Times-Roman", 6.6, f["frame_ink"])
    y -= 0.125*inch
    centered(cv, "750ML  ·  Producer: FUDI PEOPLE  ·  Store cool & dry, serve chilled.", y, "Times-Roman", 6.6, f["frame_ink"])


def build_combo_pdf(path, flavors):
    cv = canvas.Canvas(path, pagesize=(PAGE_W, PAGE_H))
    for f in flavors:
        front_page(cv, f)
        cv.showPage()
        back_page(cv, f)
        cv.showPage()
    cv.save()


# ---- print-ready variant: crop marks + margin for the trim guides ----
CROP_MARGIN = 0.2 * inch
MARK_LEN = 0.17 * inch
MARK_GAP = 0.0625 * inch
PRINT_W = PAGE_W + 2 * CROP_MARGIN
PRINT_H = PAGE_H + 2 * CROP_MARGIN

def draw_crop_marks(cv):
    tx0, ty0 = CROP_MARGIN + BLEED, CROP_MARGIN + BLEED
    tx1, ty1 = tx0 + TRIM_W, ty0 + TRIM_H
    cv.setStrokeColor(C("#000000"))
    cv.setLineWidth(0.5)
    for (cx, cy, sx, sy) in [
        (tx0, ty0, -1, -1), (tx1, ty0, 1, -1),
        (tx0, ty1, -1, 1), (tx1, ty1, 1, 1),
    ]:
        # horizontal mark
        cv.line(cx + sx*MARK_GAP, cy, cx + sx*(MARK_GAP+MARK_LEN), cy)
        # vertical mark
        cv.line(cx, cy + sy*MARK_GAP, cx, cy + sy*(MARK_GAP+MARK_LEN))

def build_combo_pdf_cropmarks(path, flavors):
    cv = canvas.Canvas(path, pagesize=(PRINT_W, PRINT_H))
    for f in flavors:
        cv.saveState()
        cv.translate(CROP_MARGIN, CROP_MARGIN)
        front_page(cv, f)
        cv.restoreState()
        draw_crop_marks(cv)
        cv.showPage()
        cv.saveState()
        cv.translate(CROP_MARGIN, CROP_MARGIN)
        back_page(cv, f)
        cv.restoreState()
        draw_crop_marks(cv)
        cv.showPage()
    cv.save()


if __name__ == "__main__":
    build_combo_pdf(f"{OUT}/sanko_wine_labels_full_range.pdf", FLAVORS)
    print("combined pdf built")

    # split per flavor
    reader = PdfReader(f"{OUT}/sanko_wine_labels_full_range.pdf")
    for i, f in enumerate(FLAVORS):
        w = PdfWriter()
        w.add_page(reader.pages[2*i])
        w.add_page(reader.pages[2*i + 1])
        out_path = f"{OUT}/sanko_{f['key']}_label_FINAL.pdf"
        with open(out_path, "wb") as fh:
            w.write(fh)
        print("wrote", out_path)

    # print-ready: crop marks (RGB first, CMYK-converted afterward via ghostscript)
    build_combo_pdf_cropmarks(f"{OUT}/sanko_wine_labels_PRINT_RGB.pdf", FLAVORS)
    print("print-ready (with crop marks) combo built")
