"""Episode 1 (Yaji) v1 assembly.

Spine = main take IMG_4702 (full script to camera). Every segment below is
one shot on the timeline; segments render to segs/NNN.mp4 (video only) and
segs/NNN.wav (audio), then concat -> loudnorm -> mux.

Times are SOURCE seconds. Main-take blocks are split into shots with
`main_block`, so the audio stays continuous while the picture cuts between
Kofi's face and B-roll.

Usage: python build_ep01.py [--only N,N,...] [--jobs 3] [--preview]
"""
import os, sys, json, subprocess, argparse
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                                   # africa-ghana nigeria
SOTW = os.path.dirname(ROOT)                                   # Spices of the world
REPO = r"C:\Users\mark\OneDrive\Documents\GitHub\SpicesOftheWorld\spicesOftheWorld"
FPS = 30

SRC = {  # key: (path, kind, gain_dB)  kind: hdr|hdrflip|sdr|png
    "M":    (os.path.join(ROOT, "IMG_4702.mov"), "hdrflip", 0.0),
    "I3":   (os.path.join(SOTW, "copy", "IMG_0603.MOV"), "hdr", 0.0),
    "I8":   (os.path.join(SOTW, "copy", "IMG_0608.MOV"), "hdr", 1.4),
    "I11":  (os.path.join(SOTW, "copy", "IMG_0611.MOV"), "hdr", 7.9),
    "I13":  (os.path.join(SOTW, "copy", "IMG_0613.MOV"), "hdr", 1.6),
    "I16":  (os.path.join(SOTW, "copy", "IMG_0616.MOV"), "hdr", 4.6),
    "I19":  (os.path.join(SOTW, "copy", "IMG_0619.MOV"), "hdr", 3.7),
    "OV":   (r"C:\Users\mark\Downloads\IMG_4573 (1).MOV", "sdr", 4.3),
    "MOK":  (os.path.join(REPO, "video", "Fudi_People_Mokola_Market.mp4"), "sdr", 0.0),
    "POLY": (os.path.join(REPO, "video", "Family_Polytunnel_Walkthrough_Clip.mp4"), "sdr", 0.0),
    "CRATE": (os.path.join(REPO, "video", "Chilli_Harvest_Crate_Overflow_Clip.mp4"), "sdr", 0.0),
    "DAUGHTER": (os.path.join(REPO, "video", "Daughter_Okra_Plate_Patio_Clip.mp4"), "sdr", 0.0),
    "MAPG": (os.path.join(REPO, "graphics", "episode-01", "broll", "ep01-broll-ghana-coastline-map.mp4"), "sdr", 0.0),
    "MAPT": (os.path.join(REPO, "graphics", "episode-01", "broll", "ep01-broll-trade-route-animation.mp4"), "sdr", 0.0),
    "END":  (os.path.join(REPO, "marketing", "social", "refresh", "assets", "video", "endcard.png"), "png", 0.0),
}
OVL = os.path.join(HERE, "overlays")
SEGS = os.path.join(HERE, "segs")
TONEMAP = ("zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=100,"
           "format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=mobius:desat=0,"
           "zscale=t=bt709:m=bt709:r=tv,format=yuv420p")
ROOMTONE = ("M", 251.45, 1.7)   # quiet gap in the main take, looped under cards


def fr(t):
    return round(t * FPS) / FPS


# ---------------------------------------------------------------- timeline
TL = []  # list of dict segments


def seg(v, vs, dur, a=None, as_=None, texts=(), speed=1.0, note="", cont=False, custom=None):
    TL.append(dict(v=v, vs=vs, dur=fr(dur), a=a, as_=as_, texts=list(texts),
                   speed=speed, note=note, cont=cont, custom=custom))


def sync(src, a0, a1, texts=(), note=""):
    """On-location bite: picture and sound from the same clip."""
    seg(src, a0, a1 - a0, a=src, as_=a0, texts=[(png, t0 - a0, t1 - a0) for png, t0, t1 in texts], note=note)


def main_block(a0, a1, broll=(), texts=(), note=""):
    """Main-take audio a0..a1; picture = Kofi's face except broll [(t0,t1,src,vs)].
    texts [(png,t0,t1)] are in main-take source time."""
    cuts = sorted({a0, a1} | {b[0] for b in broll} | {b[1] for b in broll})
    cuts = [c for c in cuts if a0 <= c <= a1]
    # snap boundaries to frames relative to the block start, keep audio contiguous
    snapped = [a0 + fr(c - a0) for c in cuts]
    first = True
    for s, e in zip(snapped[:-1], snapped[1:]):
        if e - s < 1 / FPS:
            continue
        b = next((b for b in broll if abs(b[0] - s) < 0.05 or (b[0] <= s + 0.01 and b[1] >= e - 0.01)), None)
        if b and b[0] <= s + 0.05 and b[1] >= e - 0.05:
            v, vs = b[2], b[3] + (s - b[0])
        else:
            v, vs = "M", s
        tx = []
        for png, t0, t1 in texts:
            if t1 > s and t0 < e:
                tx.append((png, max(t0, s) - s, min(t1, e) - s, t0 >= s - 0.01, t1 <= e + 0.01))
        seg(v, vs, e - s, a="M", as_=s, texts=tx, note=note if first else "", cont=not first)
        first = False


# 0. Cold open: overhead grill at 3x, sizzle, Kofi's intro voice comes in at 3.0s,
#    cut to his face at 5.0s (J-cut), title card over the grill.
seg(None, 0, 18.4, custom="coldopen", note="Cold open + intro", texts=[("title", 0.3, 4.9, True, True)])

# 1. Personal hook
main_block(17.6, 71.9, broll=[
    (17.6, 25.0, "MOK", 3.6),      # one stall at Mokola Market
    (25.0, 33.9, "MOK", 101.0),    # before the fish, before the plantain...
    (33.9, 36.9, "MOK", 34.0),     # the spice stall (bag of seeds)
    (36.9, 43.7, "I3", 74.0),      # small reddish-brown seeds = grains of paradise
], texts=[("l_gop", 37.4, 43.5), ("hook", 61.6, 71.7)], note="Personal hook")

# 2. Geography & origin (cut "from Europe. It's" 108.85-111.05)
main_block(71.9, 108.85, broll=[
    (89.2, 95.2, "MAPG", 0.0),     # Grain Coast / Pepper Coast map
    (101.6, 108.85, "I3", 1.0),    # its cousin, grains of selim
], texts=[("geo", 82.2, 88.6), ("l_selim", 102.0, 108.85)], note="Geography & origin")
main_block(111.05, 118.5, broll=[(111.05, 118.5, "MOK", 68.0)])

# 3. Trade & migration history
main_block(118.5, 178.0, broll=[
    (122.0, 128.0, "MAPT", 0.0),   # across the Sahara to Europe
], texts=[("trade", 166.9, 177.8)], note="Trade & migration")

# 4. The science
main_block(179.9, 251.6, broll=[
    (179.9, 188.2, "I3", 65.7),    # grains of paradise close-up
    (204.6, 213.8, "I3", 52.0),    # grains of selim
], texts=[("paradol", 186.8, 194.2), ("l_selim", 205.0, 213.6), ("dose", 220.1, 229.9)], note="The science")
# 4b. Health card (text only for now; Kofi may record the 32s VO to drop in here)
seg("I3", 46.0, 7.0, a="TONE", texts=[("health", 0.2, 6.9, True, True)], note="Health card")

# 5. The blend (cut ad-lib 270.9-277.8)
main_block(253.0, 270.9, broll=[
    (259.3, 263.3, "I3", 1.5),     # grains of selim
    (263.3, 267.8, "I3", 13.0),    # dried chillies
    (267.8, 270.9, "I3", 20.0),    # peanuts
], texts=[("l_selim", 259.4, 263.3), ("l_chilli", 263.4, 267.8), ("l_peanut", 267.9, 270.9)], note="The blend")
main_block(277.8, 293.1, broll=[
    (277.8, 279.3, "I3", 32.0),    # ginger powder
    (279.3, 282.1, "I3", 41.0),    # stock cubes
    (282.1, 284.0, "I3", 44.0),    # salt + black pepper
    (284.0, 287.1, "I11", 3.0),    # the finished Yaji
], texts=[("l_ginger", 277.8, 279.3), ("l_cube", 279.3, 282.1), ("l_pepper", 282.1, 284.0),
          ("l_yaji", 284.0, 287.1), ("samemix", 287.3, 291.8)])
sync("I11", 57.0, 64.6, texts=[("l_toast", 57.2, 64.4)], note="Tip: toast spices")

# 6. The dish
main_block(293.4, 326.2, broll=[(308.0, 314.0, "I13", 0.5)],
           texts=[("alsoseasons", 298.0, 317.8)], note="The dish")
main_block(326.5, 354.3, broll=[(326.5, 354.3, "OV", 0.0)], texts=[("samefire", 336.3, 349.6)])
main_block(354.9, 366.1, broll=[(354.9, 366.1, "I8", 14.5)], texts=[("l_soak", 355.3, 365.9)])
main_block(366.1, 370.0, broll=[(366.1, 370.0, "I8", 0.5)])
sync("I8", 136.3, 156.6, texts=[("l_veg", 136.6, 156.4)], note="Tip: veg between the meat")
main_block(370.0, 381.7, broll=[(370.0, 381.7, "OV", 12.0)], texts=[("l_spray", 375.4, 381.5)])
sync("OV", 51.0, 62.5, texts=[("l_late", 51.3, 62.4)], note="Why the Yaji goes on late")
sync("OV", 75.4, 85.4)
main_block(381.4, 390.8, broll=[(381.4, 390.8, "I16", 25.0)])
main_block(390.8, 395.5, broll=[(390.8, 395.5, "I16", 65.0)])
sync("I16", 79.7, 98.6, note="Payoff: nothing burnt")
sync("I16", 110.8, 122.4, texts=[("l_oil", 111.0, 122.2)], note="Olive oil finish")
sync("I19", 1.7, 15.7, note="Finished plate")

# 7. Africa link close + CTA
main_block(395.9, 442.2, broll=[
    (421.8, 429.0, "POLY", 0.5),
    (429.0, 434.5, "CRATE", 2.0),
    (434.5, 442.2, "DAUGHTER", 5.0),
], texts=[("close", 424.0, 434.3)], note="Africa link close")
main_block(442.5, 450.6, texts=[("cta", 443.0, 450.5)], note="Closing CTA")
seg("END", 0, 4.0, a="TONE", note="End card")


# ---------------------------------------------------------------- render
def vfilter(kind, speed=1.0):
    pre = f"setpts=(PTS-STARTPTS)/{speed}," if speed != 1 else "setpts=PTS-STARTPTS,"
    if kind == "hdrflip":
        body = TONEMAP + ",hflip,"
    elif kind == "hdr":
        body = TONEMAP + ","
    else:
        body = ""
    return (pre + body + "scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,"
            "crop=1080:1920,setsar=1,fps=30,format=yuv420p")


def text_chain(texts, base_label, first_input):
    """overlay PNG inputs [first_input..] onto base_label with fades."""
    parts, cur = [], base_label
    for k, t in enumerate(texts):
        png, t0, t1 = t[:3]
        fin, fout = (t[3], t[4]) if len(t) > 3 else (True, True)
        idx = first_input + k
        f = f"[{idx}:v]format=rgba"
        if fin:
            f += f",fade=t=in:st={t0:.3f}:d=0.25:alpha=1"
        if fout:
            f += f",fade=t=out:st={max(t0, t1 - 0.25):.3f}:d=0.25:alpha=1"
        parts.append(f + f"[t{k}]")
        nxt = f"o{k}"
        parts.append(f"[{cur}][t{k}]overlay=0:0:enable='between(t,{t0:.3f},{t1:.3f})'[{nxt}]")
        cur = nxt
    return parts, cur


X264 = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-r", "30", "-g", "60", "-video_track_timescale", "15360"]


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(" ".join(cmd) + "\n" + r.stderr[-3000:])


def render(i, s):
    vout, aout = os.path.join(SEGS, f"{i:03d}.mp4"), os.path.join(SEGS, f"{i:03d}.wav")
    d = s["dur"]
    pngs = []
    for t in s["texts"]:
        pngs += ["-loop", "1", "-t", f"{d:.3f}", "-i", os.path.join(OVL, t[0] + ".png")]

    if s["custom"] == "coldopen":
        ov, m = SRC["OV"][0], SRC["M"][0]
        g = SRC["OV"][2]
        cmd = ["ffmpeg", "-v", "error", "-y", "-ss", "10", "-t", "15.5", "-i", ov,
               "-ss", "4.2", "-t", "14", "-i", m] + pngs + ["-filter_complex"]
        fc = [f"[0:v]trim=0:15,{vfilter('sdr', 3)}[hook]",
              f"[1:v]trim=0:{d - 5:.3f},{vfilter('hdrflip')}[face]",
              "[hook][face]concat=n=2:v=1:a=0[base]"]
        tp, last = text_chain(s["texts"], "base", 2)
        fc += tp
        cmd += [";".join(fc), "-map", f"[{last}]", "-t", f"{d:.3f}"] + X264 + [vout]
        run(cmd)
        # audio: sizzle (speech-free stretch of the overhead clip) + intro voice from 3.0s
        run(["ffmpeg", "-v", "error", "-y", "-ss", "31.8", "-t", "3.4", "-i", ov,
             "-ss", "2.2", "-t", f"{d - 3.0:.3f}", "-i", m, "-filter_complex",
             f"[0:a]aresample=48000,volume={g}dB,afade=t=in:d=0.2,afade=t=out:st=2.6:d=0.8[sz];"
             f"[1:a]aresample=48000,adelay=3000|3000[vo];"
             f"[sz][vo]amix=inputs=2:normalize=0:duration=longest,apad,atrim=0:{d:.3f}[a]",
             "-map", "[a]", "-ac", "2", "-t", f"{d:.4f}", "-c:a", "pcm_s16le", aout])
        return i

    path, kind, _ = SRC[s["v"]]
    if kind == "png":
        cmd = ["ffmpeg", "-v", "error", "-y", "-loop", "1", "-t", f"{d:.3f}", "-i", path] + pngs
        base = (f"[0:v]scale=1080:1920,setsar=1,fps=30,format=yuv420p,"
                f"fade=t=in:d=0.4,fade=t=out:st={d - 1.0:.3f}:d=1.0[base]")
    else:
        cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{s['vs']:.3f}", "-t", f"{d + 0.5:.3f}", "-i", path] + pngs
        base = f"[0:v]{vfilter(kind)}[base]"
    tp, last = text_chain(s["texts"], "base", 1)
    cmd += ["-filter_complex", ";".join([base] + tp), "-map", f"[{last}]", "-t", f"{d:.3f}", "-an"] + X264 + [vout]
    run(cmd)

    # audio
    if s["a"] == "TONE":
        k, t0, td = ROOMTONE
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0}", "-t", f"{td}", "-i", SRC[k][0], "-af",
             f"aresample=48000,aloop=loop=-1:size={int(td * 48000)},atrim=0:{d:.3f},"
             f"afade=t=in:d=0.3,afade=t=out:st={max(0, d - 0.5):.3f}:d=0.5",
             "-ac", "2", "-t", f"{d:.4f}", "-c:a", "pcm_s16le", aout])
    else:
        apath, _, gain = SRC[s["a"]]
        fades = "" if s["cont"] else ",afade=t=in:d=0.015"
        nxt_cont = i + 1 < len(TL) and TL[i + 1]["cont"]
        if not nxt_cont:
            fades += f",afade=t=out:st={max(0, d - 0.02):.3f}:d=0.02"
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{s['as_']:.4f}", "-t", f"{d + 0.2:.3f}", "-i", apath, "-af",
             f"aresample=48000,volume={gain}dB,apad,atrim=0:{d:.4f}{fades}",
             "-ac", "2", "-t", f"{d:.4f}", "-c:a", "pcm_s16le", aout])
    return i


def probe_dur(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                       capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return -1


def done(i, d):
    v, a = os.path.join(SEGS, f"{i:03d}.mp4"), os.path.join(SEGS, f"{i:03d}.wav")
    return all(os.path.exists(p) and abs(probe_dur(p) - d) < 0.05 for p in (v, a))


def assemble(out):
    vl, al = os.path.join(SEGS, "v.txt"), os.path.join(SEGS, "a.txt")
    with open(vl, "w") as f:
        f.writelines(f"file '{i:03d}.mp4'\n" for i in range(len(TL)))
    with open(al, "w") as f:
        f.writelines(f"file '{i:03d}.wav'\n" for i in range(len(TL)))
    v, a = os.path.join(SEGS, "_video.mp4"), os.path.join(SEGS, "_audio.wav")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", vl, "-c", "copy", v])
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", al, "-c", "copy", a])
    # two-pass loudnorm to YouTube's -14 LUFS
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", a, "-af",
                        "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    js = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}:"
          f"measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}:"
          f"offset={js['target_offset']}:linear=true,aresample=48000")
    run(["ffmpeg", "-v", "error", "-y", "-i", v, "-i", a, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
         "-af", ln, "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out])


def edl(path):
    t, lines = 0.0, ["| # | Out time | Dur | Picture | Sound | Text | Note |", "|---|---|---|---|---|---|---|"]
    for i, s in enumerate(TL):
        pic = "cold open" if s["custom"] else (f"{s['v']} @{s['vs']:.1f}" if s["v"] != "END" else "end card")
        snd = "mixed" if s["custom"] else ("room tone" if s["a"] == "TONE" else f"{s['a']} @{s['as_']:.2f}")
        tx = ", ".join(x[0] for x in s["texts"])
        lines.append(f"| {i} | {int(t // 60)}:{t % 60:05.2f} | {s['dur']:.2f} | {pic} | {snd} | {tx} | {s['note']} |")
        t += s["dur"]
    lines.append(f"\nTotal: {int(t // 60)}:{t % 60:05.2f}")
    open(path, "w", encoding="utf-8").write("\n".join(lines))
    return t


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--edl-only", action="store_true")
    ap.add_argument("--resume", action="store_true", help="skip segments already rendered at the right length")
    ap.add_argument("--out", default=os.path.join(HERE, "ep01_v1.mp4"))
    o = ap.parse_args()
    os.makedirs(SEGS, exist_ok=True)
    total = edl(os.path.join(HERE, "ep01_v1_EDL.md"))
    print(f"{len(TL)} segments, {total:.1f}s")
    if o.edl_only:
        sys.exit()
    todo = [int(x) for x in o.only.split(",")] if o.only else list(range(len(TL)))
    if o.resume:
        todo = [i for i in todo if not done(i, TL[i]["dur"])]
        print("to render:", todo)
    with ThreadPoolExecutor(o.jobs) as ex:
        for i in ex.map(lambda i: render(i, TL[i]), todo):
            print("seg", i, "ok", flush=True)
    if not o.only or o.resume:
        assemble(o.out)
        print("wrote", o.out)
