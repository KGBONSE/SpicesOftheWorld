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
Docs) to a Drive folder named "fudi people knowledge base".

**2026-07-25 — Agent 2 & 3 built and wired.** Both workflows existed in
n8n already (built 2026-07-17 to 07-23, just never reflected here) —
system prompts pasted in, Anthropic/OpenAI/Google Drive/Google Sheets
credentials all connected. Found and fixed via n8n's CLI (no UI/API-key
access needed — export → patch JSON → re-import): Agent 2's knowledge-base
retrieval tool wasn't actually connected to its AI Agent node (would've
answered from general knowledge, not the spice files), and its Google
Drive step only listed filenames, never downloaded content. Agent 3 had a
stray text fragment in its system prompt and a malformed date expression,
both fixed. **Still needs a manual step in the n8n UI**: the knowledge
base index is an in-memory vector store, lost on every n8n restart — run
Agent 2's Manual Trigger once (each time after a restart) to (re)build it,
then test per `workflows/n8n/agent-2-3-build-walkthrough.md` A9. See
`docs/open-tasks.md`.

The canonical blueprint text (citation rules, the Named Influences benchmark
set, and the $0-to-start cost breakdown) lives at `docs/system-blueprint.md`.

## Episode content framework (established)

Every episode follows six beats:
1. Personal hook
2. Geography and origin
3. History
4. The blend
5. The dish — quick one-line mentions of 2–3 other real regional dishes
   using the same blend, then dive deep into cooking one of them in full
   (added 2026-07-25; not yet retrofitted into the 8 drafted Africa scripts)
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

**Season 1 is now fully drafted — all 34 episodes**, across Africa (8),
the Middle East sub-arc (10–17), the South Asia sub-arc (18–23), the East
Asia sub-arc (24–29), and the Americas sub-arc (Episode 9 plus 30–34).
East Asia's Episode 24 opens — and Episode 29 closes — the third and
final Fudi People jar (Spices of East Asia). Episode 34 closes the whole
season and lands, unplanned, on a Japanese-Peruvian (Nikkei) thread that
loops straight back to East Asia. Every episode still has an open
`[NEEDS KOFI]`/`[DRAFT]` personal-hook placeholder and a closing CTA to
fudipeople.com as its one remaining item before shooting — everything
else is fully drafted and grounded in `knowledge-base/` (or clearly
flagged when it isn't), no invented facts. See `docs/spice-channel-framework.md`.

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
  traceability): `docs/voice-recording-transcripts.md`. 8 transcripts
  processed as of 2026-07-26 (2 reflective narration + 6 farm vlogs,
  the latter transcribed locally via `faster-whisper` and analysed as a
  distinct "farm vlog register" — see `docs/brand-voice.md`).

**2026-08-28 — Demo Voice register added:** a second voice-profile track,
`docs/kofi-voice-profile.md`, was imported — built from finished YouTube
video transcripts rather than raw memos. It confirms the six-part Story
Voice framework against a real produced episode and adds a new **Demo
Voice** register for straight cooking-process videos (jollof, fufu,
salad/garden, roasted plantain), distinct from the reflective-narration
and farm-vlog registers already in `docs/brand-voice.md`. Not yet wired
into Agent 2/3's system prompts — see `docs/open-tasks.md`.

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

**2026-07-21 — Health Benefits added to all 50 spice profiles:** since the
book doesn't cover health benefits, Kofi asked for these to be researched
externally so viewers get real nutritional/wellness value alongside the
history and flavour science. Every spice-profile file (both
`core-profiles-master.md` and `by-flavour-compound/`) now has a Health
Benefits section — research-backed bullets, an evidence-strength note,
and a generic spoken attribution line ("research shows...") rather than
naming specific studies on camera, matching the existing citation
convention. Sources logged privately per entry.

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
