# Fudi People Content Pipeline — Agent Architecture

Six-agent system, orchestrated via n8n, built with zero-cost-to-start
tooling where possible.

| # | Agent | Role | Status |
|---|-------|------|--------|
| 1 | Trends / Outlier Scout | Spots content angles, trending formats | Designed |
| 2 | Knowledge & Brand Voice | Holds spice science knowledge base + brand voice profile; feeds facts and tone to the Script Writer | **In progress** |
| 3 | Script Writer | Drafts episode scripts using the six-beat episode framework and brand voice | **In progress** |
| 4 | Thumbnail Designer | Uses the farm/market photo reference library to generate thumbnail concepts | Designed |
| 5 | Editing | Assembles and normalises video (ffmpeg pipeline) | Designed |
| 6 | Publishing | Handles upload and metadata | Designed |

## Episode structure all agents should target

1. Personal hook
2. Geography and origin
3. History
4. The blend
5. The dish
6. Throughline close — ties back to the Fudi People brand

## Open questions to resolve before finishing Agent 2 & 3

- n8n instance: self-hosted or cloud? Version?
- Preferred AI model per agent (can differ by agent — e.g. cheaper model
  for Trends Scout, stronger model for Script Writer)
- Google Drive connection for pulling the knowledge base docs, transcripts,
  and photo library into the workflow

## Inputs Agent 2 (Knowledge & Brand Voice) should draw on

- `knowledge-base/` — regional spice science markdown files, master spice
  profiles doc, recipes file, three-tab spreadsheet
- `docs/brand-voice.md` — tone and stylistic signatures

## Inputs Agent 3 (Script Writer) should draw on

- Output of Agent 2
- `docs/agent-architecture.md` (this file) for the six-beat structure
- Existing Episode 1 draft (Ghana / shito / Portuguese introduction of
  chillies to West Africa) as a style reference
