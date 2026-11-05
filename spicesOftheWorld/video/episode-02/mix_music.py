"""Lay a music bed under a rendered episode (edit.py has no music stage). Voice ducks the music; video is copied untouched.

  python mix_music.py VIDEO.mp4 MUSIC.mp3 OUT.mp4 [--vol 0.55]
Preview with Epidemic's low-quality mp3; re-run with the licensed file for the final.
"""
import argparse, subprocess

ap = argparse.ArgumentParser()
ap.add_argument("video"); ap.add_argument("music"); ap.add_argument("out")
ap.add_argument("--vol", type=float, default=0.12)
o = ap.parse_args()

dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", o.video],
                           capture_output=True, text=True, check=True).stdout)
fg = (f"[1:a]atrim=0:{dur},asetpts=PTS-STARTPTS,volume={o.vol},afade=t=in:d=3,afade=t=out:st={dur - 4:.2f}:d=4[m];"
      "[0:a]asplit=2[v][vsc];[m][vsc]sidechaincompress=threshold=0.02:ratio=8:attack=20:release=400[md];"
      "[v][md]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", o.video, "-stream_loop", "-1", "-i", o.music, "-filter_complex", fg,
                "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", o.out], check=True)
print("wrote", o.out)
