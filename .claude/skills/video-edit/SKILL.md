---
name: video-edit
description: Assembles a Fudi People episode edit by writing/changing a JSON config and running the reusable renderer in spicesOftheWorld/video/edit-engine/ (cuts, B-roll, text overlays, loudnorm, vertical and landscape exports). Use when asked to edit, re-cut, or render an episode video. Not for motion graphics or AI video generation.
---

The edit is data, not prompting. Never hand-run ffmpeg or rebuild the pipeline; change the config and run the script. This keeps the work cheap and repeatable.

## Steps

1. Find the episode's config (`spicesOftheWorld/video/<episode>/edit.json`). If none exists, copy `spicesOftheWorld/video/edit-engine/example-config.json` and fill it from the episode's EDL/script. Reference `spicesOftheWorld/video/episode-01/build_ep01.py` for a worked real example (Episode 1 predates the engine and keeps its own script; don't port it unless asked).
2. Edit only the config: `sources` (paths, `kind`: `sdr` | `hdr` | `hdrflip` | `flip` | `png` | `audio`, `gain` dB), `timeline` entries, `roomtone`.
3. `python spicesOftheWorld/video/edit-engine/edit.py CONFIG --edl-only` to check segment count and total length. No rendering, cheap.
4. `--preview` for a fast low-quality render to check cuts. Use `--only N,N` to re-render single segments, `--resume` to render only what's missing.
5. Final: `--format vertical` (1080x1920) and/or `--format landscape` (1920x1080, or `--size 3840x2160`). Ep 1 is vertical only; Ep 2+ are shot landscape 4K and exported both ways.

## Timeline entry types

- `main`: continuous audio `a0..a1` from source `asrc` (default `M`); picture is the face source (`face`, default `M`) except `broll: [[t0, t1, src, src_start]]` in audio-source time. `texts: [[png_name, t0, t1]]` in audio-source time.
- `sync`: picture and sound from the same clip, `a0..a1`.
- `card`: still `png` or clip for `dur` seconds with `audio` (`TONE` = looped room tone from `roomtone: [src, start, dur]`).

## Rules

- `--jobs 1` for HDR footage (3 parallel jobs ran out of memory on Ep 1).
- Overlay PNGs are named files in `overlays_dir` (default `overlays-<format>`); they are size-specific, so landscape needs its own set (adapt `spicesOftheWorld/video/episode-01/make_overlays.py`: Poppins + Lora, brand orange/cream/brown).
- Raw footage and rendered outputs stay out of git (LFS quota). Only configs, EDLs and scripts are committed.
- Audio is normalised to -14 LUFS (two-pass loudnorm). Don't change without reason.
- Never publish or upload; report the output path and EDL, and list anything for Kofi to review.
