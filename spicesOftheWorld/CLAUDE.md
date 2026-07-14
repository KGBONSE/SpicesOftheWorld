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
wholesale.

Personal anchor of the brand: **Mokola Market** in Accra, Ghana (note correct
spelling — not "Makola"), which Kofi visited as a child with his late mother.
The brand carries that memory forward, telling global spice history through
an African lens.

## What we're building

A YouTube content pipeline for Fudi People, powered by a six-agent AI system
orchestrated in **n8n**:

1. **Trends / Outlier Scout** — spots content angles and trending formats
2. **Knowledge & Brand Voice** — holds spice science + brand voice, feeds facts and tone to the writer *(in progress)*
3. **Script Writer** — drafts episode scripts in Kofi's voice *(in progress)*
4. **Thumbnail Designer** — uses farm/market photo library for thumbnail concepts
5. **Editing** — assembles/normalises video
6. **Publishing** — handles upload/metadata

Currently at the stage of building out Agent 2 and Agent 3. Still open:
confirming the n8n instance details, preferred AI model for each agent, and
the Google Drive connection for pulling source docs/photos.

## Episode content framework (established)

Every episode follows six beats:
1. Personal hook
2. Geography and origin
3. History
4. The blend
5. The dish
6. Throughline close — links back to the brand

Episode 1 (drafted): Ghana, shito, and the Portuguese introduction of
chillies to West Africa.

## Brand voice signatures (from voice profile work)

Built from analysis of Kofi's own narration recordings and written passages:
- Memory-first openers — episodes/segments open on a personal memory, not a fact
- Stacks of 2–3 adjectives for texture and emotion
- Recurring metaphor: "planted the seeds for…"
- Trailing list-closes on emotionally weighted passages
- Full profile lives in `docs/brand-voice.md` — keep it updated as new
  recordings are analysed, but there's no need to track which specific
  recording each trait came from — just the pattern itself.

## Video production pipeline (ffmpeg — established pattern)

1. Normalise all clips to **720x1280**, `veryfast` preset, **CRF 21**
2. Assemble with the concat demuxer using `-c copy`
3. Apply a single fade re-encode pass at the end

Assets so far: compiled vertical Mokola Market footage (sourced via a Ghana
contact), a normalised family harvest clip from the Sidcup farm, and a
polytunnel photo set used as a thumbnail reference library
(`thumbnails/index.md`).

## Knowledge base (from *The Science of Spice*)

Regional markdown files completed for: Africa, Middle East, South Asia,
Southeast Asia, East Asia, Americas, Europe — plus a master spice science
profiles document, a recipes markdown file, and a three-tab Excel
spreadsheet. Location: `knowledge-base/`.

**Gap:** batches 2–8 of spice profiles (~40 spices) were never saved as
standalone files and need re-uploading from source to be fully recovered.

## Food safety (HACCP)

A HACCP-based hazard analysis was completed for the production process
(pressure canner/autoclave operating at 116–121°C). Dried garlic in two
flavours was flagged as higher-risk. Priority recommended action: validate
the heat-process step. Summary in `docs/food-safety-haccp.md` — treat as
reference only, not a substitute for a qualified food-safety review before
any process change.

## Open items to pick up here

- [ ] Confirm n8n instance details (self-hosted vs cloud, version)
- [ ] Decide preferred AI model per agent
- [ ] Connect Google Drive (for source docs + photos)
- [ ] Source additional video transcripts beyond the two Mokola Market clips already analysed
- [ ] Re-upload/recover spice profile batches 2–8 (~40 spices)
- [ ] Confirm voiceover for the Mokola Market video segment is recorded and uploaded

## Working conventions

- Always spell it **Mokola Market**, never "Makola"
- Keep the brand voice doc (`docs/brand-voice.md`) as the single source of
  truth for tone — check new scripts against it
- Treat this CLAUDE.md as living documentation — update it as agents get
  built and gaps get closed
