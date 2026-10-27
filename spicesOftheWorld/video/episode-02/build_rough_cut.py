"""Episode 2 (Senegal) rough cut: tighten pauses on the Session-1 talking-head take, add jollof cutaways + text cards.
Writes ep02_rough_config.json for ../edit-engine/edit.py (landscape). Section times are ESTIMATES from pause structure (no transcript yet)."""
import json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "episode-01"))
import finish_v3 as f
W, H = 1920, 1080
UP = "/mnt/user-data/uploads"
WORK = "/home/claude/ep02"
OVL = os.path.join(WORK, "overlays-landscape"); os.makedirs(OVL, exist_ok=True)
DUR = 376.185

# --- speech / silence map (silencedetect -35 dB, d>=0.6) ---
ev = [(m.group(1), float(m.group(2))) for l in open(os.path.join(WORK, "raw/sil.txt")) for m in [re.search(r"silence_(start|end): ([0-9.-]+)", l)] if m]
sil, s = [], None
for k, v in ev:
    if k == "start": s = v
    elif s is not None: sil.append((s, v)); s = None
    else: sil.append((0.0, v))
if s is not None: sil.append((s, DUR))
START, END = 9.7, 374.4          # setup chatter before 10.1; tail after last word
keep, cur = [], START
for a, b in sil:
    if b <= START or a >= END: continue
    gap = b - a
    if gap > 1.0:                 # long pause: keep 0.25 s either side
        keep.append((cur, a + 0.25)); cur = b - 0.25
keep.append((cur, END))
keep = [(round(a, 3), round(b, 3)) for a, b in keep if b - a > 0.3]

# --- cutaways (original-recording time -> clip, clip start) ---
A, B = "A", "B"   # A = IMG_0620_2 (pot), B = IMG_0622_3 (wide fire pan)
BROLL = [(50.0, 61.0, A, 2.0), (86.5, 98.0, A, 18.0), (100.5, 111.0, B, 6.0),
         (150.0, 160.0, A, 40.0), (262.0, 271.0, B, 26.0)]
# --- text cards (original time) ---
cards = {
 "hook_q":   ("caption", "Whose jollof was really the best?", None, 25.0, 31.0),
 "geo":      ("caption", "Jollof rice — born in Senegal", None, 119.0, 126.0),
 "trade":    ("caption", "One dish, one spice, three countries", "Senegal to Nigeria and Ghana", 193.0, 201.0),
 "sci":      ("caption", "Smoked during drying = the wood-smoke note", "Grind just before use", 238.0, 246.0),
}
for name, (kind, t, sub, a, b) in cards.items():
    f.draw_caption_c(W, H, t, sub, os.path.join(OVL, name + ".png"))

timeline = []
for a0, a1 in keep:
    e = {"type": "main", "a0": a0, "a1": a1}
    br = []
    for b0, b1, src, vs in BROLL:
        if b1 > a0 and b0 < a1:
            c0, c1 = max(b0, a0), min(b1, a1)
            br.append([c0, c1, src, vs + (c0 - b0)])
    if br: e["broll"] = br
    tx = [[n, max(a, a0), min(b, a1)] for n, (k, t, sub, a, b) in cards.items() if b > a0 and a < a1]
    if tx: e["texts"] = tx
    timeline.append(e)
cfg = {"name": "ep02-rough", "fps": 30, "target_lufs": -14, "work_dir": os.path.join(WORK, "work"), "output_dir": os.path.join(WORK, "output"),
       "overlays_dir": OVL, "roomtone": ["M", 9.0, 0.7],
       "sources": {"M": {"path": f"{UP}/IMG_0632.MOV", "kind": "hdr"},
                   "A": {"path": f"{UP}/IMG_0620_2.MOV", "kind": "hdr"},
                   "B": {"path": f"{UP}/IMG_0622_3.MOV", "kind": "hdr"}},
       "timeline": timeline}
json.dump(cfg, open(os.path.join(HERE, "ep02_rough_config.json"), "w"), indent=1)
print(len(keep), "kept runs; kept", round(sum(b - a for a, b in keep), 1), "of", round(END - START, 1), "s")
