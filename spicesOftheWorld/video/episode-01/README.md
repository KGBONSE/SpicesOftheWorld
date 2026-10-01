# Episode 1 — West Africa: Yaji (edit v1)

v1 assembled 2026-10-01: 9:02, 1080x1920, -14.5 LUFS. The rendered file
(`ep01_v1.mp4`, ~775MB) is **not in the repo**. It's too big for the LFS quota.
It lives with the raw footage in OneDrive:
`Documents\Spices of the world\africa-ghana nigeria\_ep01_work\ep01_v1.mp4`.

## Files

| File | What it is |
|---|---|
| `build_ep01.py` | The edit: every shot, cut point, B-roll and text card as code, plus the renderer (segments, then concat, then 2-pass loudnorm to -14 LUFS) |
| `ep01_v1_EDL.md` | The same edit as a readable table (out time, picture source, sound source, text) |
| `make_overlays.py` | Generates the on-screen text PNGs in `overlays/` (Poppins + Lora, brand orange/cream/brown) |
| `transcribe.py` | faster-whisper (medium.en) transcription with word timings, used to find cut points and to verify the final soundtrack |

The scripts run from the `_ep01_work` folder (they expect `fonts/`, `overlays/`, `segs/`
next to them and the raw footage paths listed in `SRC`). This copy is the
version-controlled record of the edit.

## Sources (raw, not in repo)

- `IMG_4702.mov`: main take, full script to camera (front camera, so mirrored; flipped in the edit)
- `copy/IMG_0603-0619.MOV` + photos: Yaji ingredients, prep, grill, rub, finished plate (9 Aug)
- `Downloads/IMG_4573 (1).MOV`: overhead grill shot (cold open + Dish section)
- Repo clips: Mokola Market footage, map B-roll, farm footage, end card

The iPhone footage is HDR (HLG). It's tonemapped to SDR bt709 with zscale + `tonemap=mobius`.

## Render notes

- Use `--jobs 1`: three parallel jobs ran the PC out of memory.
- `--only N` re-renders one shot; `--resume` renders anything missing, then reassembles.

## Open (Kofi to review)

- 32s health voiceover (optional), to drop in at the health card (~4:08)
- Brightness of the outdoor HDR cook shots
- Pacing of the long talking-head stretches (Trade ~50s, Science ~38s)
- Background music (royalty-free)
