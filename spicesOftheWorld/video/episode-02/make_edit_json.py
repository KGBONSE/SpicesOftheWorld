"""Builds episode-02/edit.json from the original take (IMG_0632) and its silence map.

Cuts: head trim, the jollof personal hook removed (re-filming it), long pauses tightened.
Re-run after changing HOOK_CUT / BROLL below; then `python ../edit-engine/edit.py edit.json --format landscape --preview`.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SILENCE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "silence_0632.txt")  # "start end" per line, ffmpeg silencedetect

START, END = 9.8, 375.2          # trim dead air before "Today we are going..." and after "Check it out."
HOOK_CUT = (22.2, 88.55)         # hook removed: after "...its smoky secret", resume at "Jollof rice, one of the most..."
LONG_PAUSE, KEEP = 0.9, 0.25     # pauses >= LONG_PAUSE are tightened to KEEP seconds each side
BROLL = [                        # [t0, t1, src, src_start] in original-take time
    [98.0, 108.0, "MAP1", 0.0],  # "...it started in Senegal" - map holds its last frame through "Senegal sits on the Francophone side"
    [119.5, 125.5, "MAP2", 0.0], # "Jollof traveled east... Nigeria and Ghana"
    [147.0, 153.0, "MAP3", 0.0], # "It went north to Europe in the Middle Ages..." (Ep 1 West Africa -> Europe route)
]

TEXTS = [                        # [png, t0, t1] in original-take time (overlays-landscape/, see make_overlays.py)
    ["health_yassa", 248.5, 262.0],  # mustard / garlic benefits, not said on camera
]

sil = [tuple(map(float, l.split())) for l in open(SILENCE) if l.strip()]
cuts = [(HOOK_CUT[0], HOOK_CUT[1])]
for s, e in sil:
    if e - s >= LONG_PAUSE and START < s and e < END and not (HOOK_CUT[0] <= s <= HOOK_CUT[1]):
        cuts.append((s + KEEP, e - KEEP))
cuts.sort()

blocks, t = [], START
for c0, c1 in cuts:
    blocks.append((t, c0))
    t = c1
blocks.append((t, END))

timeline = []
for a0, a1 in blocks:
    br = [b for b in BROLL if b[0] >= a0 and b[1] <= a1]
    e = {"type": "main", "a0": round(a0, 3), "a1": round(a1, 3)}
    if br:
        e["broll"] = br
    tx = [t for t in TEXTS if t[1] < a1 and t[2] > a0]  # unclipped: the engine clips per segment and fades only at true ends
    if tx:
        e["texts"] = tx
    timeline.append(e)

cfg = {
    "name": "ep02-senegal",
    "fps": 30,
    "target_lufs": -14,
    "work_dir": "work",
    "output_dir": "output",
    "sources": {
        "M": {"path": "C:/Users/mark/OneDrive/Documents/Spices of the world/copy/IMG_0632.MOV", "kind": "hdr", "gain": 0.0},
        "MAP1": {"path": "../../graphics/episode-02/broll/ep02-broll-senegal-coastline-map.mp4", "kind": "pillar"},
        "MAP2": {"path": "../../graphics/episode-02/broll/ep02-broll-senegal-nigeria-ghana-trade-route.mp4", "kind": "pillar"},
        "MAP3": {"path": "../../graphics/episode-01/broll/ep01-broll-trade-route-animation.mp4", "kind": "pillar"},
    },
    "timeline": timeline,
}
json.dump(cfg, open(os.path.join(HERE, "edit.json"), "w"), indent=2)
print(f"{len(timeline)} blocks, {sum(b[1]-b[0] for b in blocks):.1f}s before frame snapping")
