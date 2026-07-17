# Fudi People Content Pipeline — Agent Architecture

Six-agent system, orchestrated via n8n, built with zero-cost-to-start
tooling where possible.

| # | Agent | Role | Status |
|---|-------|------|--------|
| 1 | Trends / Outlier Scout | Spots content angles, trending formats | Designed — deliberately deprioritised, no dependency on the other agents |
| 2 | Knowledge & Brand Voice | Holds spice science knowledge base + brand voice profile; feeds facts and tone to the Script Writer | **Being built in n8n** — n8n installed, Google Drive connected, knowledge base ~50/52 book spices covered. System prompt at `agents/agent-2-knowledge-voice.md`; build steps in `workflows/n8n/agent-2-3-build-walkthrough.md` Part A |
| 3 | Script Writer | Drafts episode scripts using the six-beat episode framework and brand voice | **Next up** — chains onto Agent 2 once it's tested (Part B of the walkthrough). System prompt at `agents/agent-3-script-writer.md`. No Episode 1 topic picked yet |
| 4 | Thumbnail Designer | Uses the farm/market photo reference library to generate thumbnail concepts | Designed — real reference photos now in `thumbnails/reference-photos/`, still needs a market photo and a farm-work-clothes shot |
| 5 | Editing | Assembles and normalises video (ffmpeg pipeline) | Designed — two real compiled videos now in `video/`, voiceover recorded in `audio/`, not yet mixed together |
| 6 | Publishing | Handles upload and metadata | Designed |

## Episode structure all agents should target

Six beats (per `docs/system-blueprint.md` section 1.5, "Geographic origin"
etc. is the more precise phrasing — same structure, sharper labels):

1. Personal hook / **geographic origin** — where the spice is from, and
   where it's grown/traded today
2. Geography and origin → **trade & migration history** — colonial routes,
   diaspora links, trade corridors, named on camera (e.g. "the Indian
   Ocean spice route")
3. History → **the science** — flavour chemistry, one clear mechanism
   ("the science behind that heat is...") not a lecture
4. **The blend** — typical ratios, shown on screen as text/graphic
5. **The dish** — a classic dish, simplified for a home cook; this is
   Kofi's own recipe, no citation needed
6. Throughline close → **the Africa link** — the signature beat, ties
   every region back to Kofi's own story
7. **Closing CTA** — one line, spoken and on-screen, after the close:
   full written recipe and the exact blend are up at **fudipeople.com**
   (functional, still under construction). The recipe itself always stays
   fully in the video (segments 4–5) — the CTA drives to the website for
   the ready-made blend/printable card, never to gate the recipe. See
   `agents/agent-3-script-writer.md`.

**Citation rule:** every historical/scientific claim pulled from *The
Science of Spice* gets a short spoken attribution on camera (e.g.
"according to Dr Farrimond..."); the underlying page/chapter reference
stays in private notes, never read aloud.

### Named Influences — benchmark set for Agent 1 (Outlier Scout)

| Creator / Video | What Fudi People borrows |
|---|---|
| Atlas Pro — *The Geography of Spices and Herbs* | The "geography first" opening beat (segment 1) |
| Ethan Chlebowski — *Beginner's Guide to Cooking with Spices* | Question-then-explain rhythm for the science segment (3) |
| Brian Lagerstrom — *The Only 10 Spices You Need* | Tight, confident delivery for the blend/ratio segment (4) |

These three are Agent 1's first comparison point whenever it scores a new
outlier in the niche.

## Open questions — resolved

- n8n instance: **self-hosted via Docker** (n8n Cloud dropped its free
  tier), free — see `workflows/n8n/local-install-steps.md`
- Preferred AI model: **Claude (Anthropic API)**, confirmed
- Google Drive: **connected**, `knowledge-base/` uploaded — Agent 2 build
  is in progress (`workflows/n8n/agent-2-3-build-walkthrough.md`)

## Inputs Agent 2 (Knowledge & Brand Voice) should draw on

- `knowledge-base/` — regional files, spice profiles (core + flavour-
  compound batch), recipes, compound-pairing spreadsheet — see
  `knowledge-base/README.md`
- `docs/brand-voice.md` — tone and stylistic signatures

## Inputs Agent 3 (Script Writer) should draw on

- Output of Agent 2
- `docs/agent-architecture.md` (this file) for the six-beat structure
