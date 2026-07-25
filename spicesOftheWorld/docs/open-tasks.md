# Open Tasks

Most of the blueprint's Phase 1 gaps closed on 2026-07-15 when Kofi's
claude.ai chat exports (transcripts, voice profile, knowledge base, agent
system prompts, video, audio, photos) were located and imported into this
repo. What's left is genuinely short.

## Real remaining blockers

- [x] Install n8n locally (Docker) and add Anthropic + Google Drive
      credentials — see `workflows/n8n/local-install-steps.md`
- [x] Connect Google Drive with the `knowledge-base/` folder — uploaded as
      plain files to a Drive folder named "fudi people knowledge base"
      (2026-07-17)
- [ ] Build Agent 2 in n8n, paste in `agents/agent-2-knowledge-voice.md`,
      test with a few spice questions — step-by-step:
      `workflows/n8n/agent-2-3-build-walkthrough.md` Part A
- [ ] Chain Agent 3 (`agents/agent-3-script-writer.md`) on top once
      Agent 2's voice output checks out — same walkthrough, Part B
- [ ] Mix `audio/Mokola_voice_over_2.m4a` into
      `video/Fudi_People_Mokola_Market.mp4` (ffmpeg step 4 in
      `video/README.md` — not yet done)
- [x] Pick an Episode 1 topic and draft a script — West Africa (Ghana +
      Nigeria), Yaji/suya: `scripts/episode-01-west-africa-yaji.md`. Only
      open item on it: test-cook the Yaji blend to lock in real ratios
- [ ] Re-upload book photos for the last ~2 spice profiles (Clove's
      blending-science half + whatever else `knowledge-base/spice-profiles/
      by-flavour-compound/00_INDEX.md` shows as missing) — see
      `knowledge-base/README.md`
- [x] Farm-work-clothes solo shot of Kofi — added 2026-07-24,
      `thumbnails/reference-photos/kofi-solo-potting-seedlings-home-garden.jpg`
      (pulled from raw video `MVI_0135.MP4`, home garden not the Sidcup farm)
- [x] Market thumbnail photo — decided 2026-07-24 not to pursue; too long
      since the Mokola Market visit for a real photo. Market stays a
      spoken/narrated element via `audio/Mokola_voice_over_2.m4a` instead of
      a thumbnail source.
- [ ] Transcribe the 6 raw voice memos in `audio/raw-voice-memos/` (via
      Whisper or manually) and fold any new patterns into
      `docs/brand-voice.md` — strengthens the voice profile beyond the 2
      transcripts already processed, not blocking
- [ ] Locate/re-source raw Mokola Market video clips if the compiled video
      in `video/` ever needs rebuilding (source contact: Ghana-based)
- [x] Process the 7 raw seed-to-harvest video clips from `myprojectphotos/`
      (2026-07-25) — pulled 5 more thumbnail stills and cut/normalised 7
      B-roll segments into `video/`, see `thumbnails/index.md` and
      `video/README.md`. Segments are unedited raw cuts, not compiled into
      a finished sequence — that's still open if wanted.
- [x] Process `PHOTO-2026-07-24-23-18-31.zip` (WhatsApp export, Downloads,
      2026-07-25) — 5 current-day stills copied in and a talking-to-camera
      video normalised into two clips, see `thumbnails/index.md` and
      `video/README.md`. The presenter clip's narration hasn't been
      listened to/transcribed yet — worth doing before using it as a real
      intro.

## Not started (later phases, per blueprint build order)

- [ ] Agent 1 (Trends & Outlier Scout) — deliberately deprioritised, no
      dependency on Agents 2/3
- [ ] Agent 4 build-out — needs a real outlier thumbnail to reference
      (Agent 1); the reference-photo gap is now closed
- [ ] Agent 5 (Editing) and Agent 6 (Publishing) — Phase 2+

## Reference

- `docs/system-blueprint.md` — the full system blueprint (canonical copy),
  including the citation rule, the Named Influences benchmark set, and the
  $0-to-start cost breakdown
- `docs/project-context-brief.md` — consolidated handoff doc from the
  agent-building chat session, useful for the full "what's built / what's
  missing" picture in one place
- `docs/spice-channel-framework.md` — Season 1 roadmap (11 episodes) and
  the reusable per-episode research prompt
