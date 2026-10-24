# Episode 1 — handoff for Claude Code (2026-10-24)

Everything from the cloud session on branch `ep01-v4-finish-ending`. Read this first, then
`README.md` (v4 sections) and `finish_v3_plan.json` (every graphic has a `reason`).

## Where things stand

- **Edit is finished at preview stage.** `finish_v3.py` + `finish_v3_plan.json` turn Kofi's v3 cut
  into the finished episode: every `[tag]` placeholder covered by its graphic, chapter titles, map side
  text, captions, zooms, farm cutaways, chilli-harvest cards, CTA with Yaji label + Spices of Africa
  chilli oil, 15s end screen with the chilli-oil banner, -14 LUFS loudness.
- **Final 1080p render not done yet.** Kofi has not given the final go-ahead, and the source in the
  plan is only 480p (`video/raw/ep01_v3_16x9_480p.mp4`).
- **A 1080p export exists on Kofi's PC:**
  `video\episode-01\v3_work\out\ep01_v3_16x9_1080p_clean.mp4` (not in git; too big).
- **Thumbnail A won** the Instagram poll: `thumbnails/episode-01/A_spice_europe_forgot.jpg`.

## Next steps (in order)

1. **Check the 1080p file lines up with the 480p one** before rendering anything:
   ```
   ffprobe -v error -show_entries format=duration -of csv=p=0 <1080p file>   # must be 510.4
   ```
   Spot-check a few cut points against the 480p file (e.g. 80.4, 175.5, 248.1, 404.3, 480.3, 506.3 s):
   same shot on both sides of each cut. If "clean" means the `#NN` labels and `[tag]` boxes are gone,
   that's fine; the covers just sit over clean picture.
2. **Preview from the 1080p source** (fast, 854x480 output):
   ```
   python video/episode-01/finish_v3.py --preview --start 0 --source <path to ep01_v3_16x9_1080p_clean.mp4>
   ```
3. **Final, only after Kofi says go:**
   ```
   python video/episode-01/finish_v3.py --final --source <path to ep01_v3_16x9_1080p_clean.mp4>
   ```
   Output: `video/episode-01/out/ep01_v4_16x9_1080p.mp4` (git-ignored).

Run from the `spicesOftheWorld/` folder. Needs Python 3 + Pillow, and an ffmpeg build with `zscale`
(gyan.dev "full" builds on Windows have it). Fonts are bundled in `video/episode-01/fonts/` (Inter, OFL).

### Footage that is NOT in git (put it back before rendering)

The farm cutaways near the end use files kept out of git (`.gitignore`: `video/raw/ep01-ending/`).
Copy these from Kofi's desktop into `spicesOftheWorld/video/raw/ep01-ending/`:
- `IMG_0637.MOV` (daughter picking chillies), `IMG_0638.MOV` (orange habaneros in hand)
- `IMG_0636.MOV` (selfie clip — not used, keep for later)
- `daughters_polytunnel.jpg` (the two girls in the polytunnel, school uniforms)
- `daughter_chilli_oil_garden.jpg` (daughter holding chilli oil bottles in the garden)
Without them the render fails at the "cutaway" step.

## Decisions still open with Kofi

1. Final render go-ahead.
2. Okra caption at 6:53: currently *"One of the best vegetables in the whole world"* (best guess from
   noisy audio) — confirm or replace with his exact words.
3. Chilli cards at 7:00 / 7:07: "Habaneros, ghost peppers & Carolina Reapers, grown in Sidcup" and
   "Naga Morich · Trinidad Moruga — picked by hand, then into the smoker". He does **not** grow
   Scotch bonnets — never use that name.
4. Music: none yet. Option: quiet royalty-free bed (Epidemic Sound is connected in claude.ai).
5. Title: recommended **"The Spice Europe Forgot: Grains of Paradise, Yaji & Suya"** (pairs with A).

## Launch checklist

- Description (to write): fix "Mokola" -> **Makola**; Yaji list must include grains of paradise;
  chapters below; fudipeople.com; 3-5 hashtags. The old `docs/*Title-Description.docx` files have both errors.
- Chapters: 0:00 Intro · 0:20 Makola Market · 1:20 Where it comes from · 2:02 The trade ·
  2:55 The science · 4:01 The blend: Yaji · 5:04 The dish · 6:44 From our farm
- Upload with thumbnail A (YouTube Studio, or Blotato from claude.ai — YouTube account is connected).
- After upload (Kofi, in Studio): end-screen elements in the last 15s (subscribe + watch next),
  set Ep 1 as channel trailer + featured video, add to "Spices of the World" playlist, pin comment.
- Then run YouTube **Test & compare** with thumbnails A, B, C (advanced features must be on).

## YouTube channel tidy-up (@fudi.people, 49 subs, 11 old videos + 2 Shorts)

- Keep public + retitle: fufu, meat pie, gizzard kebab, oven jollof, roasted plantain & peanuts,
  organic farming, grow your own food, garden salad. Unlist: egg muffins, homemade dressings,
  Asian salad dressing. Create playlists: Spices of the World / From the Farm / Ghanaian Kitchen.
- **Makola Market Short** has "MOKOLA MARKET" burned into its opening. Fixed version renders from
  `video/Fudi_People_Mokola_Market_with_voiceover_upscaled_1080p.mp4` (LFS) with the overlay in
  `thumbnails/shorts/makola_title_fix/title_fix.png`:
  ```
  ffmpeg -i video/Fudi_People_Mokola_Market_with_voiceover_upscaled_1080p.mp4 -loop 1 -t 4.3 -i thumbnails/shorts/makola_title_fix/title_fix.png -filter_complex "[1:v]format=rgba,fade=t=in:st=0:d=0.3:alpha=1,fade=t=out:st=4.05:d=0.25:alpha=1[t];[0:v][t]overlay=0:0:eof_action=pass:enable='lte(t,4.3)',format=yuv420p[v]" -map "[v]" -map 0:a -c:v libx264 -crf 20 -preset slow -c:a copy -movflags +faststart Makola_Market_Story_Behind_Fudi_People.mp4
  ```
  Re-upload as a new Short, title "Makola Market: The Story Behind Fudi People 🌶️"; set the old one Unlisted.
  Covers: `thumbnails/shorts/`.

## Already done (don't redo)

- Instagram (@fudi.people) thumbnail poll: feed post + story, posted 2026-10-21 via Blotato.
- Competitor research lives in the **SpicesProject** repo: `competitors/channel-list.md`.
