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
```

## Assets so far

- Compiled vertical Mokola Market footage (sourced via Ghana contact) —
  spelling corrected throughout to **Mokola**, not "Makola"
- Normalised family harvest clip from the Sidcup farm
- Polytunnel photo set → see `../thumbnails/index.md`

## Gap

Voiceover for the Mokola Market segment has been written but not yet
confirmed as recorded and uploaded. Additional transcripts beyond the two
already-analysed Mokola Market clips are still needed.
