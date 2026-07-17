# Fudi People — Project Context Brief
*Consolidated handoff document — everything needed to pick up this project in a new environment (e.g. Claude Code).*

---

## 1. Brand Overview

**Fudi People** is a spice and chilli oil brand founded by **Kofi**, an entrepreneur based in London with roots in Ghana. Three product lines:
- Spices of Africa
- Spices of South Asia
- Spices of East Asia

Made with farm-grown chillies and dried spices, sold direct-to-consumer and wholesale. Kofi grows chillies, okra, and other produce on a farm in **Sidcup, London**, and operates from a home kitchen registered with his local Environmental Health Officer.

## 2. Personal / Emotional Anchor

**Mokola Market** in Accra, Ghana (correct spelling — NOT "Makola") is the emotional and narrative anchor for the brand. Kofi visited it as a child with his late mother, and the brand is in part a tribute to her. Core memory line (his own words, to be used as narration/intro):

> "Growing up in Ghana, my favourite memories were the trips I took with my mum, God bless her soul, to one of the busiest, liveliest, most vibrant markets in the country, bursting with the most amazing spices you could imagine. Those trips planted the seeds for my lifelong love for spices, farming, and cooking."

## 3. The Six-Part Episode Framework

Every YouTube episode follows this structure:
1. **Personal Hook** — first-person, memory-first
2. **Geography & Origin**
3. **History** — trade routes, migration, cultural history
4. **The Blend** — usage, ratios, pairing science
5. **The Dish** — a classic dish demonstration
6. **Africa Link / Throughline Close** — ties back to brand, farm, and (where natural) Mokola Market / his mother

## 4. The Six-Agent n8n Content Pipeline

Orchestrated via n8n, zero-cost-to-start philosophy (self-hosted, not paid Cloud):

| # | Agent | Status |
|---|---|---|
| 1 | Trends / Outlier Scout | Not started — lowest priority |
| 2 | Knowledge & Brand Voice | **System prompt built, ready to wire** (see file 03) |
| 3 | Script Writer | **System prompt built, ready to wire** (see file 04) |
| 4 | Thumbnail Designer | Not started — needs photo reference library organized first |
| 5 | Editing | Later phase |
| 6 | Publishing | Later phase |

**Build order decision:** Agent 2 → Agent 3 first, since both consume the voice profile + knowledge base already built. Agent 1 has no dependency on either and was deliberately deprioritized.

## 5. What's Already Built (assets included in this export)

- **Voice profile** (`02-fudi-people-voice-profile.md`) — built from 2 audio transcripts (Mokola1, Mokola2) + 1 independently-written memo, cross-validated across all 3 samples. Documents sentence rhythm, recurring motifs ("planted the seeds for..."), adjective-stacking (2-3 stack), tone register, and handling of references to his late mother (rare, natural, never forced).
- **Agent 2 system prompt** (`03-agent2-knowledge-brand-voice-system-prompt.md`) — ready to paste into an n8n AI Agent node. Answers spice/food-history questions in Kofi's voice using a knowledge-base retrieval tool.
- **Agent 3 system prompt** (`04-agent3-script-writer-system-prompt.md`) — ready to paste into an n8n AI Agent node. Turns Agent 2's research into full six-part episode scripts, in Kofi's voice, with [ON-SCREEN TEXT] and [B-ROLL] suggestions.
- **n8n setup guide** (`05-n8n-setup-guide.md`) — exact node-by-node build steps for wiring Agents 2 & 3 (Google Drive → Text Splitter → Embeddings → Vector Store → AI Agent → output).
- **n8n local install steps** (`06-n8n-local-install-steps.md`) — how to get n8n running for free (self-hosted via Docker) plus Anthropic API and Google Drive credential setup.
- **Science of Spice knowledge base** — built separately across regional chapters (Africa, Middle East, South Asia, Southeast Asia, East Asia, Americas, Europe), a master spice science profiles doc, a recipes markdown file, and a three-tab Excel spreadsheet. **NOT included in this export** — these files live in an earlier chat session's outputs and were not re-uploaded to this conversation. See "Known Gaps" below.
- **Video assets** (in `/media`):
  - `Fudi_People_Mokola_Market.mp4` — compiled market intro video (title card + 5 clips, corrected "Mokola" spelling, crossfade/title treatment)
  - `Family_Okra_Harvest_Clip.mp4` — extracted 109-second continuous take of family harvesting okra on the Sidcup farm, normalized to match the market video's format (720x1280 vertical)

## 6. Known Gaps / Outstanding To-Dos

1. **Voice profile transcripts** — only 2 of the recommended 5–10 source transcripts were actually processed (Mokola1, Mokola2). More would strengthen the profile further.
2. **Science of Spice batch 2–8 spice photos (~40 spices)** — this content was discussed and wri9tten up in an earlier session but never saved as standalone files, so it only exists in that earlier chat's history. Needs re-upload of the original book photos to fully recover.
3. **Voiceover recording** — Kofi intended to record himself reading the Mokola Market memory as a voiceover for the video intro. Not yet received.
4. **Farm video structure decision** — Kofi has not yet decided whether the fuller farm/family video should be its own standalone piece or merged with the Mokola Market video. Currently deferred pending his review of the extracted family clip.
5. **Thumbnail reference photos** — 5 selfie photos were received and assessed (2 clean "presenter" shots, 1 casual/personality shot, 2 weaker due to lighting/resolution). No dedicated farm-context/work-clothes photo yet, which was flagged as the most on-brand thumbnail option still missing.
6. **n8n instance** — not yet set up as of this export. Kofi confirmed: no n8n instance running yet, will use Claude (Anthropic API) as the model, Google Drive not yet connected.

## 7. Brand/Spelling Facts to Preserve

- Market name: **Mokola Market**, Accra, Ghana (not "Makola" — this was an early correction that must be applied consistently everywhere)
- Brand name: **Fudi People**
- Three product lines: Spices of Africa, Spices of South Asia, Spices of East Asia
- Farm location: Sidcup, London
- HACCP note (separate workstream, not part of this export): dried garlic in two flavours was flagged as higher-risk in a food safety hazard analysis; heat-process validation (pressure canner/autoclave, 116–121°C) was recommended as a priority action. Relevant if food-safety documentation work resumes.

## 8. Recommended Next Steps (in order)

1. Set up n8n locally (free, via Docker) — see file 06
2. Add Anthropic API credential + Google Drive credential in n8n
3. Build Agent 2 per the setup guide (file 05), paste in system prompt (file 03), test with sample spice questions
4. Once Agent 2's voice output is validated, chain Agent 3 (file 04) on top
5. Re-upload the Science of Spice knowledge base files (regional markdowns, profiles doc, recipes, spreadsheet) from the earlier session if not already saved locally — these are required inputs for Agent 2's retrieval tool but are NOT included in this export
6. Circle back to the outstanding gaps in Section 6 as needed
