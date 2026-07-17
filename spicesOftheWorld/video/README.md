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

Both video files are 70–80MB — under GitHub's 100MB hard limit, but worth
knowing before pushing: a few of these will make the repo noticeably
heavier. Consider Git LFS if more raw footage gets added later.

## Decided

`Family_Okra_Harvest_Clip.mp4` stays its own standalone piece — not merged
into the Mokola Market video.

## Gap

Mix `Mokola_voice_over_2.m4a` into the Mokola Market video per the ffmpeg
pipeline above (step 4: mix in the voiceover track) — not yet done.
Additional transcripts beyond the two already-analysed Mokola Market
clips are still wanted to strengthen the voice profile further (2 of the
recommended 5–10 processed so far).
