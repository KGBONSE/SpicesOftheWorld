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

**Added 2026-07-25 — current-day talking-to-camera clip**, from a
WhatsApp video Kofi sent 2026-07-24 (`VIDEO-2026-07-24-23-18-32.mp4`,
2:53 total, portrait, WhatsApp-compressed ~800kbps — noticeably lower
quality than the other source footage, but the first clip in the whole
library where Kofi actually talks to camera rather than just working):

- `Presenter_Intro_Talking_Clip.mp4` — Kofi talking directly to camera in
  the polytunnel, hand gestures, narrating (content of the narration not
  transcribed — worth a listen before using as a real intro)
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

Additional transcripts beyond the two already-analysed Mokola Market
clips are still wanted to strengthen the voice profile further (2 of the
recommended 5–10 processed so far).

## Done — 2026-07-25: voiceover mixed in

`Fudi_People_Mokola_Market_with_voiceover.mp4` — voiceover plays for the
first 53 seconds (`Mokola_voice_over_2.m4a`'s full length), then the
original video's own audio picks back up for the remaining ~82 seconds.
Chosen over the literal step-4 command (which would have replaced all
audio and truncated the video to match the 53-second voiceover, dropping
over a minute of footage) or leaving the tail silent. Video stream
untouched (`-c:v copy`); audio re-encoded as AAC. **Not yet checked by
ear** — worth a playback listen to confirm the handoff at 0:53 sounds
smooth before treating this as final. The 7 raw source clips backing the
new B-roll above remain in `myprojectphotos/` (not in the repo) in case
different segments are needed later.
