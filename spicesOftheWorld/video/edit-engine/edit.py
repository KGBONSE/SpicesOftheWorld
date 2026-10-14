"""Reusable episode renderer. The edit lives in a JSON config; this script has no episode-specific code.

Usage:
  python edit.py CONFIG.json --edl-only                 # write the EDL + total length, render nothing
  python edit.py CONFIG.json [--format vertical|landscape] [--size 3840x2160]
                 [--only 3,4] [--resume] [--jobs 1] [--preview] [--out FILE]

Pipeline: each timeline entry renders to segs/NNN.mp4 (video) + NNN.wav (audio),
then concat -> two-pass loudnorm -> mux. --resume skips segments already rendered.
See ../../.claude/skills/video-edit/SKILL.md for the config format.
"""
import os, sys, json, subprocess, argparse
from concurrent.futures import ThreadPoolExecutor

FORMATS = {"vertical": (1080, 1920), "landscape": (1920, 1080)}
TONEMAP = ("zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=100,"
           "format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=mobius:desat=0,"
           "zscale=t=bt709:m=bt709:r=tv,format=yuv420p")


class Edit:
    def __init__(self, cfg_path, fmt, size, preview):
        self.cfg_dir = os.path.dirname(os.path.abspath(cfg_path))
        self.cfg = json.load(open(cfg_path, encoding="utf-8"))
        self.fps = self.cfg.get("fps", 30)
        self.W, self.H = size or FORMATS[fmt]
        self.preview = preview
        name = self.cfg["name"]
        work = self.p(self.cfg.get("work_dir", "work"))
        self.segs = os.path.join(work, f"segs-{fmt}" + ("-preview" if preview else ""))
        self.ovl = self.p(self.cfg.get("overlays_dir", f"overlays-{fmt}"))
        self.lufs = self.cfg.get("target_lufs", -14)
        self.out_default = os.path.join(self.p(self.cfg.get("output_dir", "output")),
                                        f"{name}_{fmt}{'_preview' if preview else ''}.mp4")
        self.src = self.cfg["sources"]
        self.tl = []
        for e in self.cfg["timeline"]:
            self.add(e)
        self.x264 = ["-c:v", "libx264", "-preset", "ultrafast" if preview else "veryfast",
                     "-crf", "28" if preview else "18", "-pix_fmt", "yuv420p", "-r", str(self.fps),
                     "-g", str(self.fps * 2), "-video_track_timescale", "15360"]

    def p(self, path):
        path = os.path.expandvars(os.path.expanduser(path))
        return path if os.path.isabs(path) else os.path.join(self.cfg_dir, path)

    def fr(self, t):
        return round(t * self.fps) / self.fps

    # ------------------------------------------------------------ timeline
    def seg(self, v, vs, dur, a=None, as_=None, texts=(), note="", cont=False):
        self.tl.append(dict(v=v, vs=vs, dur=self.fr(dur), a=a, as_=as_, texts=list(texts), note=note, cont=cont))

    def add(self, e):
        t = e["type"]
        if t == "sync":  # picture + sound from the same clip
            a0, a1 = e["a0"], e["a1"]
            self.seg(e["src"], a0, a1 - a0, a=e["src"], as_=a0,
                     texts=[(n, t0 - a0, t1 - a0, True, True) for n, t0, t1 in e.get("texts", [])], note=e.get("note", ""))
        elif t == "card":  # still image or clip with room tone / chosen audio
            self.seg(e["src"], e.get("vs", 0), e["dur"], a=e.get("audio", "TONE"), as_=e.get("as", 0),
                     texts=[(n, t0, t1, True, True) for n, t0, t1 in e.get("texts", [])], note=e.get("note", ""))
        elif t == "main":  # continuous audio a0..a1; picture = main face except broll [[t0,t1,src,vs]]
            self.main_block(e["a0"], e["a1"], e.get("broll", []), e.get("texts", []), e.get("note", ""),
                            e.get("asrc", "M"), e.get("face", "M"))
        else:
            raise ValueError(f"unknown timeline type {t!r}")

    def main_block(self, a0, a1, broll, texts, note, asrc, face):
        fr = self.fr
        cuts = sorted({a0, a1} | {b[0] for b in broll} | {b[1] for b in broll})
        snapped = [a0 + fr(c - a0) for c in cuts if a0 <= c <= a1]
        first = True
        for s, e in zip(snapped[:-1], snapped[1:]):
            if e - s < 1 / self.fps:
                continue
            b = next((b for b in broll if b[0] <= s + 0.05 and b[1] >= e - 0.05), None)
            v, vs = (b[2], b[3] + (s - b[0])) if b else (face, s)
            tx = [(n, max(t0, s) - s, min(t1, e) - s, t0 >= s - 0.01, t1 <= e + 0.01)
                  for n, t0, t1 in texts if t1 > s and t0 < e]
            self.seg(v, vs, e - s, a=asrc, as_=s, texts=tx, note=note if first else "", cont=not first)
            first = False

    # ------------------------------------------------------------ render
    def vfilter(self, kind):
        body = {"hdrflip": TONEMAP + ",hflip,", "hdr": TONEMAP + ",", "flip": "hflip,"}.get(kind, "")
        return (f"setpts=PTS-STARTPTS,{body}scale={self.W}:{self.H}:force_original_aspect_ratio=increase:flags=lanczos,"
                f"crop={self.W}:{self.H},setsar=1,fps={self.fps},format=yuv420p")

    @staticmethod
    def text_chain(texts, first_input):
        parts, cur = [], "base"
        for k, t in enumerate(texts):
            _, t0, t1, fin, fout = t
            f = f"[{first_input + k}:v]format=rgba"
            if fin:
                f += f",fade=t=in:st={t0:.3f}:d=0.25:alpha=1"
            if fout:
                f += f",fade=t=out:st={max(t0, t1 - 0.25):.3f}:d=0.25:alpha=1"
            parts.append(f + f"[t{k}]")
            parts.append(f"[{cur}][t{k}]overlay=0:0:enable='between(t,{t0:.3f},{t1:.3f})'[o{k}]")
            cur = f"o{k}"
        return parts, cur

    @staticmethod
    def run(cmd):
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError(" ".join(cmd) + "\n" + r.stderr[-3000:])

    def render(self, i):
        s = self.tl[i]
        d = s["dur"]
        vout, aout = os.path.join(self.segs, f"{i:03d}.mp4"), os.path.join(self.segs, f"{i:03d}.wav")
        pngs = []
        for t in s["texts"]:
            pngs += ["-loop", "1", "-t", f"{d:.3f}", "-i", os.path.join(self.ovl, t[0] + ".png")]
        path, kind, _ = self.srcinfo(s["v"])
        if kind == "png":
            cmd = ["ffmpeg", "-v", "error", "-y", "-loop", "1", "-t", f"{d:.3f}", "-i", path] + pngs
            base = (f"[0:v]scale={self.W}:{self.H},setsar=1,fps={self.fps},format=yuv420p,"
                    f"fade=t=in:d=0.4,fade=t=out:st={max(0, d - 1.0):.3f}:d=1.0[base]")
        else:
            cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{s['vs']:.3f}", "-t", f"{d + 0.5:.3f}", "-i", path] + pngs
            base = f"[0:v]{self.vfilter(kind)}[base]"
        tp, last = self.text_chain(s["texts"], 1)
        self.run(cmd + ["-filter_complex", ";".join([base] + tp), "-map", f"[{last}]", "-t", f"{d:.3f}", "-an"]
                 + self.x264 + [vout])

        if s["a"] == "TONE":
            k, t0, td = self.cfg["roomtone"]
            self.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0}", "-t", f"{td}", "-i", self.srcinfo(k)[0], "-af",
                      f"aresample=48000,aloop=loop=-1:size={int(td * 48000)},atrim=0:{d:.3f},"
                      f"afade=t=in:d=0.3,afade=t=out:st={max(0, d - 0.5):.3f}:d=0.5",
                      "-ac", "2", "-t", f"{d:.4f}", "-c:a", "pcm_s16le", aout])
        else:
            apath, _, gain = self.srcinfo(s["a"])
            fades = "" if s["cont"] else ",afade=t=in:d=0.015"
            if not (i + 1 < len(self.tl) and self.tl[i + 1]["cont"]):
                fades += f",afade=t=out:st={max(0, d - 0.02):.3f}:d=0.02"
            self.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{s['as_']:.4f}", "-t", f"{d + 0.2:.3f}", "-i", apath,
                      "-af", f"aresample=48000,volume={gain}dB,apad,atrim=0:{d:.4f}{fades}",
                      "-ac", "2", "-t", f"{d:.4f}", "-c:a", "pcm_s16le", aout])
        return i

    def srcinfo(self, key):
        s = self.src[key]
        return self.p(s["path"]), s.get("kind", "sdr"), s.get("gain", 0.0)

    @staticmethod
    def probe_dur(path):
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                           capture_output=True, text=True)
        try:
            return float(r.stdout.strip())
        except ValueError:
            return -1

    def done(self, i):
        d = self.tl[i]["dur"]
        return all(os.path.exists(p) and abs(self.probe_dur(p) - d) < 0.05
                   for p in (os.path.join(self.segs, f"{i:03d}.mp4"), os.path.join(self.segs, f"{i:03d}.wav")))

    def assemble(self, out):
        n = len(self.tl)
        v, a = os.path.join(self.segs, "_video.mp4"), os.path.join(self.segs, "_audio.wav")
        for ext, tgt in (("mp4", v), ("wav", a)):
            lst = os.path.join(self.segs, ext + ".txt")
            open(lst, "w").writelines(f"file '{i:03d}.{ext}'\n" for i in range(n))
            self.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", tgt])
        L = self.lufs
        r = subprocess.run(["ffmpeg", "-hide_banner", "-i", a, "-af", f"loudnorm=I={L}:TP=-1.5:LRA=11:print_format=json",
                            "-f", "null", "-"], capture_output=True, text=True)
        js = json.loads(r.stderr[r.stderr.rfind("{"):r.stderr.rfind("}") + 1])
        ln = (f"loudnorm=I={L}:TP=-1.5:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}:"
              f"measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}:"
              f"offset={js['target_offset']}:linear=true,aresample=48000")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        self.run(["ffmpeg", "-v", "error", "-y", "-i", v, "-i", a, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                  "-af", ln, "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out])

    def edl(self):
        t = 0.0
        lines = ["| # | Out time | Dur | Picture | Sound | Text | Note |", "|---|---|---|---|---|---|---|"]
        for i, s in enumerate(self.tl):
            snd = "room tone" if s["a"] == "TONE" else f"{s['a']} @{s['as_']:.2f}"
            tx = ", ".join(x[0] for x in s["texts"])
            lines.append(f"| {i} | {int(t // 60)}:{t % 60:05.2f} | {s['dur']:.2f} | {s['v']} @{s['vs']:.1f} | {snd} | {tx} | {s['note']} |")
            t += s["dur"]
        lines.append(f"\nTotal: {int(t // 60)}:{t % 60:05.2f}")
        path = os.path.join(self.p(self.cfg.get("work_dir", "work")), f"{self.cfg['name']}_EDL.md")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w", encoding="utf-8").write("\n".join(lines))
        return t, path


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("--format", default="vertical", choices=list(FORMATS))
    ap.add_argument("--size", help="override WxH, e.g. 3840x2160")
    ap.add_argument("--only", default="")
    ap.add_argument("--jobs", type=int, default=1, help="keep at 1 for HDR footage (memory)")
    ap.add_argument("--edl-only", action="store_true")
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--preview", action="store_true", help="fast low-quality render for checking cuts")
    ap.add_argument("--out")
    o = ap.parse_args()
    size = tuple(int(x) for x in o.size.lower().split("x")) if o.size else None
    E = Edit(o.config, o.format, size, o.preview)
    total, edl_path = E.edl()
    print(f"{len(E.tl)} segments, {total:.1f}s ({o.format} {E.W}x{E.H}); EDL: {edl_path}")
    if o.edl_only:
        sys.exit()
    os.makedirs(E.segs, exist_ok=True)
    todo = [int(x) for x in o.only.split(",")] if o.only else list(range(len(E.tl)))
    if o.resume:
        todo = [i for i in todo if not E.done(i)]
        print("to render:", todo)
    with ThreadPoolExecutor(o.jobs) as ex:
        for i in ex.map(E.render, todo):
            print("seg", i, "ok", flush=True)
    if not o.only or o.resume:
        out = o.out or E.out_default
        E.assemble(out)
        print("wrote", out)
