"""Crossed hammer + tool emblem with a tight grape cluster, matching the
reference: a pick-hammer (curved pointed head, upper-left) on one diagonal
with its handle running to a lower-right tip, crossing a second plain
straight tool-shaft running from upper-centre down to a lower-left tip,
forming a clean X, inside a thin circle outline. Grapes are solid
tightly-packed circles (no individual outlines), flat single-color fill."""
import os
ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets')
from PIL import Image, ImageDraw
import math

def _unit(p0, p1):
    dx, dy = p1[0]-p0[0], p1[1]-p0[1]
    L = math.hypot(dx, dy)
    return dx/L, dy/L

def _thick_line(d, p0, p1, w, color, round_end0=False, round_end1=False):
    dx, dy = _unit(p0, p1)
    px, py = -dy, dx
    poly = [
        (p0[0]+px*w, p0[1]+py*w), (p1[0]+px*w, p1[1]+py*w),
        (p1[0]-px*w, p1[1]-py*w), (p0[0]-px*w, p0[1]-py*w),
    ]
    d.polygon(poly, fill=color)
    if round_end0:
        d.ellipse([p0[0]-w, p0[1]-w, p0[0]+w, p0[1]+w], fill=color)
    if round_end1:
        d.ellipse([p1[0]-w, p1[1]-w, p1[0]+w, p1[1]+w], fill=color)

def hammer_grape_icon(size=600, color=(196, 155, 74), stroke=5):
    SS = 4
    S = size * SS
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy = S / 2, S / 2
    r = S * 0.46
    st = max(2, int(stroke * SS))

    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=st)

    # --- diagonal 1: hammer. head at upper-left, handle tip lower-right ---
    head_pt  = (cx - r*0.30, cy - r*0.42)   # where head sits on the handle
    tip1     = (cx + r*0.66, cy + r*0.60)   # lower-right handle tip
    w1 = r * 0.050
    _thick_line(d, head_pt, tip1, w1, color, round_end1=True)

    # --- diagonal 2: plain second tool, top tucked near the hammer head,
    # running down to a lower-left tip ---
    top2 = (cx - r*0.06, cy - r*0.20)
    tip2 = (cx - r*0.70, cy + r*0.62)
    w2 = r * 0.032
    _thick_line(d, top2, tip2, w2, color, round_end0=True, round_end1=True)

    # --- pick-hammer head: curved pointed wedge pointing up-left, blockier
    # body toward the handle, the crossbar roughly perpendicular to diag1 ---
    hdx, hdy = _unit(head_pt, tip1)     # along handle, pointing down-right
    hpx, hpy = -hdy, hdx                # perpendicular
    head_len = r * 0.60
    head_h = r * 0.155
    # body: short block straddling the handle at head_pt, extended toward +perp
    body = [
        (head_pt[0] - hpx*head_len*0.16 - hdx*head_h, head_pt[1] - hpy*head_len*0.16 - hdy*head_h),
        (head_pt[0] + hpx*head_len*0.62 - hdx*head_h*0.8, head_pt[1] + hpy*head_len*0.62 - hdy*head_h*0.8),
        (head_pt[0] + hpx*head_len*0.62 + hdx*head_h*0.8, head_pt[1] + hpy*head_len*0.62 + hdy*head_h*0.8),
        (head_pt[0] - hpx*head_len*0.16 + hdx*head_h, head_pt[1] - hpy*head_len*0.16 + hdy*head_h),
    ]
    d.polygon(body, fill=color)
    # curved pointed pick tip extending toward -perp (up/left side)
    base_c = (head_pt[0] - hpx*head_len*0.16, head_pt[1] - hpy*head_len*0.16)
    tip_pt = (head_pt[0] - hpx*head_len*0.68 - hdx*head_h*0.1,
              head_pt[1] - hpy*head_len*0.68 - hdy*head_h*0.1)
    pick = [
        (base_c[0] - hdx*head_h*0.95, base_c[1] - hdy*head_h*0.95),
        tip_pt,
        (base_c[0] + hdx*head_h*0.65, base_c[1] + hdy*head_h*0.65),
    ]
    d.polygon(pick, fill=color)
    d.ellipse([head_pt[0]-head_h*0.5, head_pt[1]-head_h*0.5,
               head_pt[0]+head_h*0.5, head_pt[1]+head_h*0.5], fill=color)

    # --- grape cluster: solid, tightly packed circles, no outlines ---
    gcx, gcy = cx + r * 0.40, cy - r * 0.32
    grape_r = r * 0.105
    offsets = [
        (0.0, -1.35), (0.95, -1.0), (-0.55, -0.85),
        (0.25, -0.35), (1.2, -0.25), (-0.95, 0.05),
        (0.55, 0.45), (-0.25, 0.75), (1.0, 0.75),
        (0.15, 1.3),
    ]
    for ox, oy in offsets:
        gx = gcx + ox * grape_r * 1.15
        gy = gcy + oy * grape_r * 1.15
        d.ellipse([gx-grape_r, gy-grape_r, gx+grape_r, gy+grape_r], fill=color)

    img = img.resize((size, size), Image.LANCZOS)
    return img

if __name__ == "__main__":
    colors = {
        "pineapple": (214, 178, 72),
        "pineapple_orange": (214, 178, 72),
        "mixed_fruit": (214, 178, 72),
        "plum": (198, 164, 86),
        "ginger": (120, 76, 30),
        "plum_pink": (120, 36, 44),
    }
    for key, color in colors.items():
        ic = hammer_grape_icon(color=color)
        ic.save(os.path.join(ASSETS, f"icon_{key}.png"))
    print("icons done")
