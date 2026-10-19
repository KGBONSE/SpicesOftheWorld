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
- Repo clips: Makola Market footage, map B-roll, farm footage, end card

The iPhone footage is HDR (HLG). It's tonemapped to SDR bt709 with zscale + `tonemap=mobius`.

## Render notes

- Use `--jobs 1`: three parallel jobs ran the PC out of memory.
- `--only N` re-renders one shot; `--resume` renders anything missing, then reassembles.

## v4 finishing pass (2026-10-19, from Kofi's v3)

Kofi's own v3 cut (`video/raw/ep01_v3_16x9_480p.mp4`, 8:30, 16:9) still has the
rough-cut markers burned in: a `#NN 0m00s` label top-left and `[close]`/`[cta]`
style placeholder tags where on-screen text should go. `finish_v3.py` +
`finish_v3_plan.json` finish the ending (6:45 onwards) on top of that file:

- Fudi People bug top-left (covers the cut labels)
- "From our farm · Sidcup, London" chapter title, "Makola Market · Accra, Ghana" tag
- Captions for the Africa close, with "Ghana / Nigeria never let them go" emphasised + a slow push-in
- "Spices of Africa — grown in Sidcup, rooted in Ghana" lower third (the scripted [close] text)
- The "for the smell · for the memory · for the market · for her" list-close built up word by word
- CTA panel + the Yaji jar label (the scripted [cta] text)
- A 15s end screen (YouTube end-screen elements need 5–20s; the old card was 4s)

- New farm cutaways (2026-10-19): daughter picking chillies + Scotch bonnets in hand (IMG_0637/0638),
  the daughters-in-the-polytunnel photo under "carry that same handful forward", and the
  chilli-oil photo under "for the memory · for the market". These sources live in
  `video/raw/ep01-ending/` locally (git-ignored: ~500MB of iPhone HLG footage).
- CTA shows the new Spices of Africa chilli-oil label; the end screen carries the chilli-oil banner
  (`graphics/labels/chilli-oil/marketing/`).

### 0:00–6:45 pass (2026-10-19)

Every burned-in placeholder tag in v3 is now covered by its matching graphic, using the
text from `make_overlays.py` redrawn for 16:9 as opaque bottom-centre tabs/pills:
cold-open title, ingredient pills, Ghana/paradol/selim/dose captions, a research card (only the
two claims kept in this cut), a Yaji ingredient list that builds shot by shot, "Yaji also seasons"
and "Same mix, same fire" lists that build as Kofi names each item, and the cooking-method pills.
Also: six chapter titles (Makola Market · Where it comes from · The trade · The science · The
blend · The dish), side text on the two portrait map shots, captions to break up the 26s trade
stretch, four zoom punch-ins, and -14 LUFS two-pass loudnorm (the edit-engine standard) over
the whole soundtrack. Every entry in `finish_v3_plan.json` carries its `reason`.

`--preview --start 0` renders the whole episode at 480p; `--until N` stops early for quick checks.
`--preview` renders only the ending at 480p; `--final` renders the whole episode at 1080p.
Renders go to `out/` (git-ignored).

## Open (Kofi to review)

- 32s health voiceover (optional), to drop in at the health card (~4:08)
- Brightness of the outdoor HDR cook shots
- Pacing of the long talking-head stretches (Trade ~50s, Science ~38s)
- Background music (royalty-free)
