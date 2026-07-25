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
- [x] Build Agent 2 in n8n and chain Agent 3 on top — turns out this was
      already ~90% built (2026-07-17 to 07-23, not reflected in this doc
      until now). Found and fixed 2026-07-25 via n8n's CLI
      (export/patch/re-import — no UI access needed):
      - Agent 2's knowledge-base retrieval tool was never actually
        connected to the AI Agent node — it would have answered from
        Claude's general knowledge, not your spice files
      - The Google Drive step only listed files, never downloaded their
        content — added a Download step so the Data Loader gets real text
      - Agent 3 had a stray leftover "ou are a helpful assistant" fragment
        tacked onto its system prompt, and a malformed date expression in
        its Google Sheets step — both fixed
      - **2026-07-25, found while testing:** Agent 2's AI Agent node had
        its prompt hardcoded to `{{ $json.topic }}`, but the Chat Trigger
        (used for manual testing) outputs `chatInput`, not `topic` — so
        typing into the chat panel hit "No prompt specified". Only worked
        by luck when called from Agent 3, which explicitly maps
        `chatInput` → `topic`. Fixed to `{{ $json.topic || $json.chatInput }}`
        so both paths work.
      - **2026-07-25, second round of testing:** after the prompt fix, the
        agent answered but said it could only see filenames, not real
        file content. Root cause found via n8n's execution DB
        (`database.sqlite`, `execution_data` table): the full indexing
        chain (Search files → Download → Vector Store insert) had never
        actually been run since the fixes went in — only the Manual
        Trigger node in isolation had been tested. What the agent was
        retrieving was **stale data from 2026-07-23**, left in memory
        from before any of these fixes, when the pipeline had the same
        "filename only, no real content" bug. In-memory store survives
        workflow edits, only wiped on a full n8n restart. Set
        `clearStore: true` on the Insert-mode Simple Vector Store node so
        the next full run replaces the stale index instead of adding to
        it.
      - **2026-07-25, third round:** the Google credential itself needed
        reconnecting (OAuth refresh token had expired — the Cloud project
        was still in "Testing" publishing status, which caps tokens at 7
        days; switched to "In production" to stop this recurring weekly).
        After reconnecting, the Download step failed with "Export only
        supports Docs Editors files" — decoded the real error from n8n's
        execution DB and found the cause: "Search files and folders"
        returns 60 items from the Drive folder, but 6 of them are actual
        **subfolders** (`spice-profiles`, `regional`, `recipes`,
        `compound-reference`, `superseded`, `by-flavour-compound-batch`),
        not files — the Download node chokes trying to export the first
        folder it hits as if it were a Google Doc. Good news found in the
        same check: all ~54 real files ARE direct children of the target
        folder already (no recursive subfolder traversal needed — good
        news given Drive's search API isn't recursive). Fixed by setting
        `filter.whatToSearch: "files"` on the search node, which excludes
        folders server-side via Drive's own query syntax.
      - **Next step: run the full "Execute workflow" (from the Manual
        Trigger node specifically, not a single-node test) on Agent 2,
        then re-test chat.**
      - **One step only doable in the n8n UI (not automatable headlessly):**
        open `http://localhost:5678` → Agent 2 workflow → run the Manual
        Trigger ("Agent 2 — Knowledge & Brand Voice") once to build the
        index. It's an in-memory vector store — **lost on every n8n
        restart**, so this needs re-running after any Docker restart, not
        just once ever. Then test with the two questions in
        `workflows/n8n/agent-2-3-build-walkthrough.md` A9.
- [ ] Mix `audio/Mokola_voice_over_2.m4a` into
      `video/Fudi_People_Mokola_Market.mp4` (ffmpeg step 4 in
      `video/README.md` — not yet done)
- [x] Pick an Episode 1 topic and draft a script — West Africa (Ghana +
      Nigeria), Yaji/suya: `scripts/episode-01-west-africa-yaji.md`. Only
      open item on it: test-cook the Yaji blend to lock in real ratios
- [x] Re-upload book photos for Clove's blending-science half (2026-07-25,
      book pp.84–85) — `core-profiles-master.md`'s Clove entry is now
      complete (blending science, food partners, blends to try, releasing
      the flavour). At most 1 of ~52 spices may still be incomplete — see
      `knowledge-base/README.md`.
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
