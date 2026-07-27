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
      - **2026-07-25, fourth round:** with folders excluded, the Default
        Data Loader still failed — "Unsupported mime type:
        application/vnd.openxmlformats-officedocument.spreadsheetml.sheet".
        The loader only supports PDF/CSV/EPub/Docx/Text/JSON, not
        spreadsheets, and `compound-reference/spice-compound-pairing-reference.xlsx`
        is the one non-.md file in the knowledge base. Its data is already
        duplicated in prose/table form in `core-profiles-master.md`, so
        added a small Code node ("Keep markdown files only") between
        Search and Download that keeps only items ending in `.md` —
        simpler and more robust than trying to special-case one file's
        mime type.
      - **2026-07-25, confirmed working end to end:** index build (59
        real markdown files, verified via n8n's execution DB — actual
        file text, not filenames) and the chat test both succeeded. Agent
        2 is genuinely retrieving and voicing real knowledge-base content.
      - **2026-07-25, full Agent 3 chain confirmed working:** tested with
        "Grains of Paradise, Ghana episode" — produced a complete 7-section
        shooting script (two hook versions, on-voice throughout, proper
        B-ROLL/ON-SCREEN TEXT cues, correctly self-flagged 2
        `[NEEDS VERIFICATION]` items instead of inventing facts), and it
        logged correctly to the Google Sheet (Date/Topic/Text/Status all
        populated). The whole pipeline — Agent 2 retrieval → Agent 3
        script writing → Sheet logging — is genuinely working end to end.
      - **Minor scope note, not fixed:** Agent 2 itself returned an
        already-script-shaped response ("Here's the full Ghana episode
        script...") instead of sticking to research facts per its own
        system prompt — Agent 3 still built a proper final script on top,
        so it didn't hurt the result, but it means Agent 2 is doing (and
        costing) more than designed. Worth tightening Agent 2's prompt to
        stick to facts-only if token cost becomes a concern.
      - **Standing reminder:** the vector store is in-memory — wiped on
        every n8n restart. After any Docker restart, re-open Agent 2 and
        run the Manual Trigger's "Execute workflow" once before using
        either agent again.
- [x] Mix `audio/Mokola_voice_over_2.m4a` into
      `video/Fudi_People_Mokola_Market.mp4` (2026-07-25) —
      `video/Fudi_People_Mokola_Market_with_voiceover.mp4`: voiceover
      plays over the first 53s, original audio continues after (full
      2:15 length kept, not truncated to the voiceover's length). See
      `video/README.md`.
- [x] **2026-07-26:** swapped to different narration per Kofi's request
      after listening — a generic, spice-agnostic trim of Episode 1's
      "stall" Hook, so this intro can open any episode. Recorded by Kofi
      (`audio/Mokola_voice_over_generic.m4a`) and re-mixed into
      `video/Fudi_People_Mokola_Market_with_voiceover.mp4`. See
      `video/README.md` for the as-recorded transcript.
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
- [x] Transcribe the 6 raw voice memos in `audio/raw-voice-memos/`
      (2026-07-26, via locally-installed `faster-whisper` — `openai-whisper`
      failed to install due to a Windows path-length limit on one of
      PyTorch's license files, so switched to the lighter dependency-free
      alternative). Raw transcripts in `docs/voice-recording-transcripts.md`
      (Transcripts C–H). These turned out to be a different kind of
      recording from the first two (live present-tense farm vlogs, not
      reflective narration) — documented as a separate "Farm vlog
      register" in `docs/brand-voice.md` rather than merged into the
      core signatures, since merging them would have blurred two
      genuinely different registers together.
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
      `video/README.md`. **2026-07-26: Kofi listened to the presenter
      clip's narration and confirmed it's usable** — clear to use as a
      real intro.
- [x] Compile the 7 seed-to-harvest B-roll clips into a finished sequence
      (2026-07-27) — `video/Seed_To_Harvest_Sequence.mp4` (3:40), sowing
      through potting/watering through planting through harvest, same
      concat + fade pipeline. Still a full reference reel, not a locked
      edit — see `video/README.md`.
- [x] Retrofit Health Benefits into all 9 episode scripts (2026-07-27) —
      the 2026-07-21 Health Benefits work only ever landed in
      `knowledge-base/spice-profiles/`, never in the actual scripts in
      `scripts/`. Added a short researched line + on-screen text into each
      episode's existing Science section (not a new beat — kept the
      6-beat template intact), sourced from each episode's own featured
      spice's profile. Two gaps surfaced and are flagged in the relevant
      scripts rather than guessed at: calabash nutmeg (Episodes 4 & 7) and
      allspice (Episode 9) have no written profile/Health Benefits section
      in the knowledge base at all — worth writing those if either spice
      gets featured again.
- [x] Draft Episode 9 — Caribbean, opening Arc 3 (2026-07-27) —
      `scripts/episode-09-caribbean-jerk.md`, allspice/jerk, picks up
      Episode 7's calabash-nutmeg/slave-trade thread directly. Open items:
      personal hook and one marinade trial (the rub's own ratios are
      already locked from the source, unusually). Flagged a small
      continuity mismatch with Episode 8's closing text — see that
      script's Status section.

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
