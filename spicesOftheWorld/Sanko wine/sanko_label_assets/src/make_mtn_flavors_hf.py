import os
ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets')
from PIL import Image
import numpy as np

ALPHA_SRC = os.path.join(ASSETS, "mtn_hf_alpha_full.png")

FLAVOR_COLORS = {
    "pineapple":        (214, 178, 72),
    "pineapple_orange": (214, 178, 72),
    "mixed_fruit":       (214, 178, 72),
    "plum":              (198, 164, 86),
    "ginger":            (150, 100, 40),
    "plum_pink":         (120, 36, 44),
}

a = Image.open(ALPHA_SRC).convert("L")
alpha_arr = np.array(a)
w, h = a.size

for key, color in FLAVOR_COLORS.items():
    rgba = np.zeros((h, w, 4), dtype=np.uint8)
    rgba[..., 0] = color[0]
    rgba[..., 1] = color[1]
    rgba[..., 2] = color[2]
    rgba[..., 3] = alpha_arr
    out = Image.fromarray(rgba, "RGBA")
    out.save(os.path.join(ASSETS, f"mtnicon_{key}.png"))
    print("wrote", key, out.size)

print("aspect h/w =", h / w)
