"""Builds episode-02/edit.json from the original take (IMG_0707) and its silence map.

Cuts: head trim, the jollof personal hook removed (re-filming it), long pauses tightened.
Re-run after changing HOOK_CUT / BROLL below; then `python ../edit-engine/edit.py edit.json --format landscape --preview`.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SILENCE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "silence_0707.txt")  # "start end" per line, ffmpeg silencedetect

START, END = 1.7, 490.4          # trim dead air before "Today we are going..." and after "Check it out."
HOOK_CUT = (0.0, 0.0)           # IMG_0707 keeps the spoken jollof hook; set e.g. (15.5, 94.5) to drop it
LONG_PAUSE, KEEP = 0.9, 0.25     # pauses >= LONG_PAUSE are tightened to KEEP seconds each side
BROLL = [
    [107.8, 117.8, "MAP1", 0.0],  # "...it started in Senegal"
    [133.0, 144.5, "MAP2", 0.0],  # "Jollof travel east... Nigeria and Ghana"
    [167.0, 173.0, "MAP3", 0.0],  # "...Europe in the Middle Ages"
]

import subprocess
MAPLEN = {}  # filled below from the b-roll files
TEXTS = []                      # health points are now said on camera in 0707, so no health_yassa card

for _k, _p in {"MAP1": "ep02-broll-senegal-coastline-map.mp4", "MAP2": "ep02-broll-senegal-nigeria-ghana-trade-route.mp4"}.items():
    MAPLEN[_k] = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", os.path.join(HERE, "../../graphics/episode-02/broll", _p)]))
MAPLEN["MAP3"] = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", os.path.join(HERE, "../../graphics/episode-01/broll/ep01-broll-trade-route-animation.mp4")]))

sil = [tuple(map(float, l.split())) for l in open(SILENCE) if l.strip()]
cuts = [HOOK_CUT] if HOOK_CUT[1] > HOOK_CUT[0] else []
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
    br = []  # windows may straddle tightened pauses: split per block, advancing the map's own start so it keeps playing
    for b0, b1, src, ss in BROLL:
        lo, hi = max(a0, b0), min(a1, b1)
        if hi - lo > 0.3:
            br.append([round(lo, 3), round(hi, 3), src, round(min(ss + (lo - b0), MAPLEN[src] - 0.1), 3)])  # past the clip's end -> hold its last frame
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
        "M": {"path": "C:/Users/mark/OneDrive/Documents/Spices of the world/senegal/IMG_0707.MOV", "kind": "hdr", "gain": 0.0},
        "MAP1": {"path": "../../graphics/episode-02/broll/ep02-broll-senegal-coastline-map.mp4", "kind": "pillar"},
        "MAP2": {"path": "../../graphics/episode-02/broll/ep02-broll-senegal-nigeria-ghana-trade-route.mp4", "kind": "pillar"},
        "MAP3": {"path": "../../graphics/episode-01/broll/ep01-broll-trade-route-animation.mp4", "kind": "pillar"},
    },
    "timeline": timeline,
}
json.dump(cfg, open(os.path.join(HERE, "edit.json"), "w"), indent=2)
print(f"{len(timeline)} blocks, {sum(b[1]-b[0] for b in blocks):.1f}s before frame snapping")
