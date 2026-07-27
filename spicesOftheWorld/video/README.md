# Video Assets & Pipeline

## Established ffmpeg pattern

```bash
# 1. Normalise each clip
ffmpeg -i input.mp4 -vf "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280" \
  -preset veryfast -crf 21 -c:a copy normalised_clip.mp4

# 2. Assemble with concat demuxer (list normalised clips in files.txt)
ffmpeg -f concat -safe 0 -i files.txt -c copy assembled.mp4

# 3. Single fade re-encode pass
ffmpeg -i assembled.mp4 -vf "fade=in:0:30,fade=out:st=<duration-1>:d=1" \
  -preset veryfast -crf 21 final.mp4

# 4. Mix in the voiceover track
ffmpeg -i final.mp4 -i voiceover.m4a -c:v copy -map 0:v:0 -map 1:a:0 \
  -shortest final_with_voiceover.mp4
```

## Assets so far

- `Fudi_People_Mokola_Market.mp4` — compiled vertical Mokola Market intro
  (title card + 5 clips, corrected "Mokola" spelling, crossfade/title
  treatment)
- `Family_Okra_Harvest_Clip.mp4` — 109-second continuous take of family
  harvesting okra on the Sidcup farm, normalised to match the market
  video's format (720x1280 vertical)
- Voiceover recorded and ready to mix in: `../audio/Mokola_voice_over_2.m4a`
  (53 sec, reads the mum/Mokola Market memory — replaces an earlier take
  that wasn't good enough to use)
- Polytunnel photo set → see `../thumbnails/index.md`

**Added 2026-07-25 — seed-to-harvest B-roll**, cut and normalised (same
720x1280/veryfast/CRF21 pipeline, ~30s segments, raw audio kept via
`-c:a copy`) from 7 raw clips Kofi supplied in `myprojectphotos/`
(all shot May 2020, home garden + allotment — 5 more stills pulled from
the same batch, see `../thumbnails/index.md`):

- `Seed_Sowing_Solo_Clip.mp4` — solo, sowing seeds into trays, greenhouse (from `MVI_0089.MP4`)
- `Lettuce_Harvest_Family_Clip.mp4` — both daughters + Kofi, harvesting a lettuce bed (from `MVI_0116.MP4`)
- `Tomato_Potting_Solo_Clip.mp4` — solo, potting up tomato seedlings (from `MVI_0135.MP4`, same clip the solo thumbnail still came from)
- `Watering_Pots_Solo_Clip.mp4` — solo, watering the potted seedlings, continuation of the clip above (from `MVI_0136.MP4`)
- `Family_Planting_Patio_Clip.mp4` — all three together on the patio, teaching the girls to plant — strongest family warmth in the batch (from `MVI_0138.MP4`)
- `Chard_Harvest_Allotment_Clip.mp4` — solo, harvesting chard at an allotment plot, a third distinct growing location (from `MVI_0148.MP4`)
- `Seed_Sowing_Bonding_Clip.mp4` — youngest daughter on his lap, sowing seeds together, tender close moment (from `MVI_0166.MP4`)

These are unedited normalised segments, not compiled sequences — pick
and trim further at actual edit time depending on which episode/segment
they're cut into.

**Added 2026-07-27 — compiled into a sequence:** `Seed_To_Harvest_Sequence.mp4`
(3:40, 720x1280) concatenates all 7 clips above (already-matching codecs —
h264/yuvj420p + AAC 48kHz stereo, so `-c copy` concat worked cleanly) into
one continuous seed-to-harvest arc, in this order: Seed_Sowing_Solo →
Seed_Sowing_Bonding → Tomato_Potting_Solo → Watering_Pots_Solo →
Family_Planting_Patio → Lettuce_Harvest_Family → Chard_Harvest_Allotment —
sowing through potting/watering through planting through harvest, solo
clips leading into the family ones. Same fade re-encode pass as step 3 of
the established pipeline (1s fade in/out); original ambient audio kept
throughout, no voiceover mixed in (none written for this sequence yet).
This is a full-length reference reel, not a finished edit — still meant to
be cut down/re-ordered per episode at actual edit time; the 7 individual
source clips above remain available separately for that.

**Added 2026-07-25 — current-day talking-to-camera clip**, from a
WhatsApp video Kofi sent 2026-07-24 (`VIDEO-2026-07-24-23-18-32.mp4`,
2:53 total, portrait, WhatsApp-compressed ~800kbps — noticeably lower
quality than the other source footage, but the first clip in the whole
library where Kofi actually talks to camera rather than just working):

- `Presenter_Intro_Talking_Clip.mp4` — Kofi talking directly to camera in
  the polytunnel, hand gestures, narrating. **Confirmed usable by Kofi
  2026-07-26** (listened himself) — clear to use as a real intro.
- `Harvest_Cutting_Closeup_Clip.mp4` — hands-on close-up, cutting/harvesting
  with a knife, same session

Same photo batch also included 5 new current-day stills — see
`../thumbnails/index.md`.

All video files together are now ~245MB — still under GitHub's 100MB
per-file hard limit, but the repo is getting noticeably heavier. Worth
moving to Git LFS if more raw footage gets added.

## Decided

`Family_Okra_Harvest_Clip.mp4` stays its own standalone piece — not merged
into the Mokola Market video.

## Gap

Voice profile now has 8 processed transcripts (2 reflective narration +
6 farm vlogs transcribed 2026-07-26) — see `docs/brand-voice.md`.

## Done — 2026-07-25: voiceover mixed in

`Fudi_People_Mokola_Market_with_voiceover.mp4` — voiceover plays for the
first 53 seconds (`Mokola_voice_over_2.m4a`'s full length), then the
original video's own audio picks back up for the remaining ~82 seconds.
Chosen over the literal step-4 command (which would have replaced all
audio and truncated the video to match the 53-second voiceover, dropping
over a minute of footage) or leaving the tail silent. Video stream
untouched (`-c:v copy`); audio re-encoded as AAC. The 7 raw source clips
backing the new B-roll above remain in `myprojectphotos/` (not in the
repo) in case different segments are needed later.

## Done — 2026-07-26: voiceover swapped to the generic "stall" version

After listening to the first mix, Kofi decided he preferred different
narration for this video: the "stall" memory used as Episode 1's Personal
Hook (`scripts/episode-01-west-africa-yaji.md`), trimmed to a **generic,
spice-agnostic version** so this compiled intro can open any episode, not
just Episode 1. Episode 1's own script is unchanged — it keeps the full
version, including the grains-of-paradise line.

Recorded by Kofi as `New Recording 5.m4a` (51.78s), kept in the repo as
`audio/Mokola_voice_over_generic.m4a`. Re-mixed the same way as before —
voiceover over the intro, original audio continuing after — replacing
`Fudi_People_Mokola_Market_with_voiceover.mp4`.

**As actually recorded** (transcribed for the record — light natural
variation from the drafted version above is expected and fine, this is
what's actually in the video):

> "Growing up in Ghana, there was one store at Mokola Market. My mom, God
> blessed, so, would always stop at before we even got to the fish,
> before the plantain, before the Kobi, before anything else. She'll pick
> up a handful of these small ready brown seeds, crack one between the
> fingers, and let me smell it. With sharp, pepperish, warm, nothing like
> the black pepper I knew from school dinners back home. That smell
> planted the seeds for everything that came after. My love for spices,
> for farming, for cooking, and all that good stuff that I've been doing
> all these years."

## Added 2026-07-27 — Episode 1 rough-cut animatic

`episode-01-rough-cut-DRAFT.mp4` (60s, 720x1280) — a rough cut of the full
Episode 1 script (`scripts/episode-01-west-africa-yaji.md`), built to use
as much real Fudi People material as actually exists in the repo, not just
flat placeholder cards. First pass leaned too heavily on text cards; this
version replaces four of those with real photos/footage/audio once a
closer look turned up material that had been overlooked.

**Real assets used, with text overlaid (not flat cards):**
- **Personal Hook** — the first 16s of `Fudi_People_Mokola_Market_with_voiceover.mp4`,
  which turns out to already contain real Mokola Market photography and
  Kofi's real recorded voice. Not word-for-word identical to this script's
  locked Hook (missing the "grains of paradise" name-drop and the closing
  "take you back to that exact stall" line) — flagged on-screen as an
  approximate match, not silently passed off as exact.
- **The Science** — real photo `thumbnails/reference-photos/kofi-kneeling-tending-chillies-crate-2026.jpg`
  (Kofi, hands-on, real chilli plants), Ken Burns slow zoom, silent —
  still genuinely needs a voiceover recording, flagged as such.
- **The Blend** — real photo `thumbnails/reference-photos/harvest-spread-tomatoes-chillies-eggplants-peas.jpg`
  (real harvested chillies/tomatoes/veg), Ken Burns zoom, with a real
  ~10s audio excerpt from `audio/raw-voice-memos/IMG_3382.mp3` — Kofi's
  own voice talking about smoking and crushing chillies into a blend.
  Flagged clearly: this is a different recording (not the literal Yaji
  ingredient line) and the exact in/out points are an approximate cut
  based on transcript position, not verified by ear — worth a listen and
  re-trim before treating as final.
- **The Dish** — real footage, `Harvest_Cutting_Closeup_Clip.mp4` (Kofi,
  hands-on, greenhouse), muted, as a visual stand-in. Flagged "not the
  actual dish yet" — this one's honest limit: no cooking/grilling footage
  exists anywhere in the library, so this is placeholder-grade regardless.

**Already real/final (unchanged from the first pass):**
- Two on-brand map graphics (`graphics/episode-01/ep01-map-ghana.png`,
  `ep01-map-trade-route.png`) for Geography and Trade History — built with
  Pillow, matching the real Fudi People brand palette pulled from
  `brand-assets/product-labels/chili-oil-south-asia-label.pdf`
- 8 real seconds of `Family_Okra_Harvest_Clip.mp4` for the Africa Link close
- CTA card — clean brand-styled text card (no product photo exists yet)

**Still a genuine, unavoidable gap:** no audio or video anywhere in the
library actually shows Kofi mixing Yaji or grilling chinchinga/suya, and
no recording exists of him reading this episode's *exact* locked script
lines. Those two things still need him — everything else in this cut is
now real material with honest flags on the approximations, not a blank
placeholder standing in for "footage I didn't look for."

Source overlay/graphic PNGs kept in `graphics/episode-01/` (map cards) and
`graphics/episode-01/overlays/` (transparent text overlays composited onto
the real photos/footage above) in case wording or timing needs adjusting.

Built with a from-scratch Pillow script (no map/design tool available
locally), each card rendered to a silent-audio timed clip, concatenated
with the existing project pipeline, single fade pass. Source PNGs kept in
`graphics/episode-01/` in case durations/text need adjusting later.
