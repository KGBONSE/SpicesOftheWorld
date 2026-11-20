"""Two 4:5 (1080x1350) Facebook clips from the clean 1080p Episode 1, each ending on a 'watch the full episode' card.
usage: python make_facebook_clips.py SOURCE.mp4   (SOURCE = clean 1080p Ep1, 510.56 s; parts 1+2 joined)"""
import os, sys, subprocess
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "facebook"); FONTS = os.path.join(HERE, "fonts")
W, H = 1080, 1350; MAROON = (110, 31, 42); ORANGE = (224, 130, 30); CREAM = (250, 243, 232); GOLD = (253, 214, 66)
F = lambda s, w="ExtraBold": ImageFont.truetype(os.path.join(FONTS, f"Inter-{w}.otf"), s)
CLIPS = [
    dict(name="fb_ep01_clip1_suya", t0=343.5, t1=404.6, fit="cover",
         title="Suya, the Yaji way", sub="Grilled over fire, rolled in spice"),
    dict(name="fb_ep01_clip2_farm", t0=404.8, t1=451.8, fit="blurpad",
         title="From our farm in Sidcup", sub="The chillies behind our spice"),
]
END_SECS = 3.5

def title_png(c, path):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    f1, f2 = F(68), F(40, "SemiBold")
    w = max(d.textlength(c["title"], font=f1), d.textlength(c["sub"], font=f2)) + 90
    x0 = (W - w) / 2; y0 = 60
    d.rounded_rectangle((x0, y0, x0 + w, y0 + 170), 34, fill=MAROON + (232,))
    d.text((W / 2, y0 + 58), c["title"], font=f1, fill=CREAM, anchor="mm")
    d.text((W / 2, y0 + 128), c["sub"], font=f2, fill=GOLD, anchor="mm")
    # small persistent reminder at the bottom
    t = "Full episode on YouTube · @fudi.people"; f3 = F(36, "SemiBold"); w3 = d.textlength(t, font=f3) + 60
    d.rounded_rectangle(((W - w3) / 2, H - 130, (W + w3) / 2, H - 66), 32, fill=(0, 0, 0, 150))
    d.text((W / 2, H - 98), t, font=f3, fill=CREAM, anchor="mm")
    im.save(path)

def end_png(path):
    im = Image.new("RGB", (W, H), MAROON); d = ImageDraw.Draw(im)
    d.text((W / 2, 430), "WATCH THE", font=F(84), fill=CREAM, anchor="mm")
    d.text((W / 2, 530), "FULL EPISODE", font=F(96), fill=CREAM, anchor="mm")
    d.rounded_rectangle((250, 620, 830, 720), 50, fill=GOLD); d.text((W / 2, 670), "ON YOUTUBE", font=F(60), fill=MAROON, anchor="mm")
    d.text((W / 2, 820), "Spices of the World · Episode 1", font=F(44, "SemiBold"), fill=CREAM, anchor="mm")
    d.text((W / 2, 880), "Yaji, Suya & Chinchinga", font=F(44, "SemiBold"), fill=ORANGE, anchor="mm")
    d.text((W / 2, 1010), "@fudi.people", font=F(58), fill=CREAM, anchor="mm")
    im.save(path)

def render(src, c):
    tp = os.path.join(OUT, c["name"] + "_title.png"); title_png(c, tp)
    ep = os.path.join(OUT, "end_card.png"); end_png(ep)
    d = c["t1"] - c["t0"]
    if c["fit"] == "cover":
        v = f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},setsar=1,fps=30[v0]"
    else:
        v = (f"[0:v]split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=40:4,eq=brightness=-0.1[bg];"
             f"[b]scale={W}:-2:flags=lanczos[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1,fps=30[v0]")
    fc = (v + f";[v0][1:v]overlay=0:0:enable='lt(t,{d - 0.05})'[v1];"
          f"[2:v]scale={W}:{H},setsar=1,fps=30,format=yuv420p[e];[v1]format=yuv420p[v2];"
          f"[0:a]afade=t=in:d=0.3,afade=t=out:st={d - 0.6}:d=0.6,aresample=48000[a0];[3:a]aresample=48000[a1];"
          f"[v2][a0][e][a1]concat=n=2:v=1:a=1[v][a]")
    out = os.path.join(OUT, c["name"] + ".mp4")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(c["t0"]), "-t", f"{d:.3f}", "-i", src, "-loop", "1", "-t", f"{d:.3f}", "-i", tp,
                    "-loop", "1", "-t", str(END_SECS), "-i", ep, "-f", "lavfi", "-t", str(END_SECS), "-i", "anullsrc=r=48000:cl=stereo",
                    "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out], check=True)
    print("wrote", out)

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for c in CLIPS: render(sys.argv[1], c)
