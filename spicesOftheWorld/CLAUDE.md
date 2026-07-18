# spicesOftheWorld — Project Brief for Claude Code

This file is read at the start of every Claude Code session in this project.
It captures everything built so far in chat with Claude, so work can continue
here without losing context.

## Who this is for

Kofi — founder of **Fudi People**, a spice and chilli oil brand based in London
with deep roots in Ghana. Three product lines: Spices of Africa, Spices of
South Asia, Spices of East Asia. Farm-grown chillies, okra, and dried spices
from a farm in Sidcup, London; production out of a home kitchen registered
with the local Environmental Health Officer. Sold direct-to-consumer and
wholesale. Website: **fudipeople.com** (functional, still under
construction) — every episode script closes on a spoken CTA pointing here
for the full recipe + the ready-made blend.

Personal anchor of the brand: **Mokola Market** in Accra, Ghana (note correct
spelling — not "Makola"), which Kofi visited as a child with his late mother.
The brand carries that memory forward, telling global spice history through
an African lens.

## What we're building

A YouTube content pipeline for Fudi People, powered by a six-agent AI system
orchestrated in **n8n** (self-hosted via Docker, free — Claude/Anthropic API
confirmed as the model):

1. **Trends / Outlier Scout** — spots content angles and trending formats *(designed, deliberately deprioritised)*
2. **Knowledge & Brand Voice** — holds spice science + brand voice, feeds facts and tone to the writer *(ready to wire — `agents/agent-2-knowledge-voice.md`)*
3. **Script Writer** — drafts episode scripts in Kofi's voice *(ready to wire — `agents/agent-3-script-writer.md`)*
4. **Thumbnail Designer** — uses farm/market photo library for thumbnail concepts *(designed — real reference photos in `thumbnails/reference-photos/`)*
5. **Editing** — assembles/normalises video *(designed — real videos in `video/`, voiceover in `audio/`, not yet mixed)*
6. **Publishing** — handles upload/metadata *(designed)*

**Cost philosophy: $0 to start.** Every tool in the pipeline has a free tier
(YouTube Data API, Google Sheets/Gmail, Google AI Studio for thumbnails,
Whisper/FFmpeg locally, n8n self-hosted). The only real cost is Claude API
usage, pay-as-you-go — kept low by running on-demand rather than 24/7 while
still finding the format. Full breakdown: `docs/system-blueprint.md` section 5.

**2026-07-15 — big import:** Kofi located and pulled in a large batch of files
he'd built across several earlier claude.ai chat sessions (zips in his
Downloads folder) — the knowledge base, a refined voice profile, ready-to-paste
n8n system prompts for Agents 2 & 3, two compiled videos, the Mokola Market
voiceover recording, and real thumbnail reference photos. Most of the
blueprint's "Phase 1 — Foundation" gap is now closed.

**2026-07-16 — n8n up and running:** Docker/n8n installed locally, Anthropic
API credential added, Google Drive connected with `knowledge-base/` uploaded.
Kofi is now building Agent 2 in n8n — step-by-step at
`workflows/n8n/agent-2-3-build-walkthrough.md` (also published as an
interactive checklist artifact). See `docs/open-tasks.md` for what's left.

**2026-07-16/17 — Agent 2 build in progress:** Google Sheets/YouTube/other
Google credentials also connected in n8n (beyond just Drive). Embeddings
choice decided: **OpenAI embeddings** (`text-embedding-3-small`), not
Ollama — OpenAI API key obtained and added as an n8n credential.
`knowledge-base/` content uploaded as plain files (not converted to Google
Docs) to a Drive folder named "fudi people knowledge base". Next: start
Part A of the walkthrough (create the "Agent 2 — Knowledge & Brand Voice"
workflow itself — no nodes built yet).

The canonical blueprint text (citation rules, the Named Influences benchmark
set, and the $0-to-start cost breakdown) lives at `docs/system-blueprint.md`.

## Episode content framework (established)

Every episode follows six beats:
1. Personal hook
2. Geography and origin
3. History
4. The blend
5. The dish
6. Throughline close — links back to the brand

Five episodes drafted so far, all in `scripts/`, following the confirmed
"all of Africa first, in the book's own regional order" plan (full roadmap:
`docs/spice-channel-framework.md`):
1. West Africa — Ghana & Nigeria, via Yaji/chinchinga/suya (`episode-01-west-africa-yaji.md`)
2. Senegal — jollof's real origin + grains of selim's smoky secret (`episode-02-senegal-yassa.md`)
3. Horn of Africa (Ethiopia) — fenugreek + niter kibbeh (`episode-03-ethiopia-niter-kibbeh.md`)
4. West Africa — Sierra Leone/Liberia — pepper soup, uda, dumboy; sourced from web research, not the book (`episode-04-sierra-leone-liberia.md`)
5. The Maghreb — cumin, cinnamon, harissa (`episode-05-maghreb-harissa.md`)
6. East Africa — Zanzibar, ginger, pilau masala (`episode-06-east-africa-pilau.md`)
7. Central Africa — mbongo, njangsa, calabash nutmeg's slave-trade thread to the Caribbean (`episode-07-central-africa-mbongo.md`) — heavier history, worth real thought before filming, not a quick read-through
8. Southern Africa — Durban curry masala, closes the Africa arc and points to South Asia (`episode-08-southern-africa-durban.md`)

**The full Africa arc (8 episodes) is now drafted.** Next per
`docs/spice-channel-framework.md`: Arc 3, starting with the Caribbean, then
South Asia, East Asia, Middle East. Each episode has an open
`[NEEDS KOFI]` personal-hook placeholder and a closing CTA to fudipeople.com
— everything else is fully drafted and grounded in `knowledge-base/` (or
clearly flagged when it isn't), no invented facts.

**Citation rule:** every historical/scientific claim pulled from *The
Science of Spice* gets a short spoken attribution on camera (e.g.
"according to Dr Farrimond..."); the page/chapter reference stays in
private notes, never read aloud. Book content is background research
only — always paraphrased in Kofi's voice, never quoted directly.

**Named Influences** (Agent 1's benchmark set — see `docs/system-blueprint.md`
section 1.5): Atlas Pro (geography-first opener), Ethan Chlebowski
(question-then-explain science segment), Brian Lagerstrom (tight,
confident blend/ratio segment).

Season 1 roadmap (11 episodes, West Africa → wider Africa → diaspora/trade
routes) and a reusable per-episode research prompt: `docs/spice-channel-framework.md`.

## Brand voice signatures (from voice profile work)

Built from analysis of three source samples: two narration recordings
(Mokola1, Mokola2) plus one independently-written memory passage —
signatures confirmed across all three are treated as core:
- Memory-first openers — episodes/segments open on a personal memory, not a fact
- Stacks of 2–3 adjectives for texture and emotion (count varies naturally)
- Recurring metaphor: "planted the seeds for…" — strong enough to be a
  deliberate series motif, not just an occasional callback
- Trailing list-closes on emotionally weighted passages
- References to his late mother ("God bless her soul") — only when they
  arise naturally, never inserted for effect
- Full profile: `docs/brand-voice.md`. Raw source transcripts (for
  traceability): `docs/voice-recording-transcripts.md`. Only 2 of the
  recommended 5–10 transcripts have been processed so far — more would
  strengthen the profile further, but isn't blocking.

## Video & audio production pipeline (ffmpeg — established pattern)

1. Normalise all clips to **720x1280**, `veryfast` preset, **CRF 21**
2. Assemble with the concat demuxer using `-c copy`
3. Apply a single fade re-encode pass
4. Mix in the voiceover audio track

Real assets now in the repo:
- `video/Fudi_People_Mokola_Market.mp4` — compiled Mokola Market intro
- `video/Family_Okra_Harvest_Clip.mp4` — normalised family harvest clip,
  Sidcup farm — stays its own standalone piece, not merged with the market video
- `audio/Mokola_voice_over_2.m4a` — recorded voiceover, not yet mixed in (step 4 above)
- `thumbnails/reference-photos/` — 4 real polytunnel photos of Kofi and his
  daughters; still missing a market shot and a farm-work-clothes solo shot

Both video files are 70–80MB — under GitHub's 100MB hard limit, but worth
knowing before pushing (repo gets noticeably heavier; consider Git LFS if
more raw footage gets added).

## Knowledge base (from *The Science of Spice*)

`knowledge-base/` is now populated — see `knowledge-base/README.md` for the
full breakdown. Headline: **regional files complete (7/7)**, and between
the core profiles file and the flavour-compound batch, **~50 of ~52 book
spices now have a written profile** (previously an ~40-spice gap). Also
includes 18 worked recipes and a 9-spice compound-pairing spreadsheet.
Remaining gap is small: Clove's blending-science half plus 1–2 other
spices — re-upload the relevant book photos to close it. The book itself
was never actually acquired as usable text (a `.lcpl` file in Kofi's
Downloads is just a DRM loan license, not extractable content) — all of
this knowledge base content came from photos of physical pages uploaded in
earlier chats.

## Working conventions

- Always spell it **Mokola Market**, never "Makola"
- Keep the brand voice doc (`docs/brand-voice.md`) as the single source of
  truth for tone — check new scripts against it
- Treat this CLAUDE.md as living documentation — update it as agents get
  built and gaps get closed
- See `docs/open-tasks.md` for the current, maintained task list and
  `docs/project-context-brief.md` for a fuller narrative handoff doc
