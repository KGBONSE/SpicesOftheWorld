---
name: content-repurposing
description: Turns one piece of source content (a YouTube link, a transcript, or a reference to an episode/video already in this project) into a full content pack by running the blog-post, newsletter, and linkedin-post skills on it in one go, all in Fudi People's brand voice. Trigger phrases — "repurpose this", "turn this video into content", "content repurpose". Use for repurposing a single piece of content across channels; not for a campaign plan (use the marketing-campaign-planner agent) or short-form social scripts (use the marketing-social-shorts agent).
---

## What this skill does

Runs the existing `blog-post`, `newsletter`, and `linkedin-post` skills, one after another, on a single source. It holds no writing logic of its own — it is a thin orchestrator. If those skills change, this one doesn't need to.

## Step 1 — Get the source

Ask which of the three the user has:

1. A YouTube link
2. A transcript (pasted text or a file)
3. A video file / an episode already in this project

Handle each:

- **YouTube link** — try to fetch it with WebFetch. Most YouTube pages don't expose a usable transcript to a plain fetch; if nothing usable comes back, say so plainly and ask the user to paste the transcript instead. Don't guess at what the video says.
- **Transcript** — read it directly (pasted text, or Read the given file path).
- **Video file / episode reference** — this project has no audio/video transcription tool. Look for a matching script under `scripts/` (e.g. `episode-0X-*.md`, `episode-0X-filming-script.md`, `episode-0X-read-aloud.md`) or in `docs/voice-recording-transcripts.md`, matched by episode number or keyword. If nothing matches, ask the user to point to the transcript or script file rather than guessing.

## Step 2 — Pull out the main ideas

Read `agents/marketing-team.md` and `docs/brand-voice.md` once. From the source, extract: the core story or hook, 2-3 concrete facts or moments, the product/blend/episode it ties to, and anything the source explicitly says that must not be embellished. Do not invent details the source doesn't contain.

## Step 3 — Run each content skill

Invoke each of the following in turn via the Skill tool, passing along the extracted ideas and source so each one has what it needs without re-deriving it:

1. `blog-post` → saves to `marketing/seo/`
2. `newsletter` → saves to `marketing/email/`
3. `linkedin-post` → saves to `marketing/social/`

Run them one after another, not in parallel — each is a real piece of writing for the user to review, and sequential output stays legible. If a skill can't verify something (e.g. an unpublished blend, an unconfirmed allergen), let it flag that in its own "Needs Kofi" list rather than skipping the piece.

## Step 4 — Summarize

Once all three are done, show one summary: the source used, and for each piece — its title/subject/hook line, one line on what it covers, and the exact file path it was saved to. Roll up every "Needs Kofi" flag from all three outputs into one combined list at the end.

## Adding more content skills later

This skill only orchestrates. If more content skills get added later (an Instagram-caption skill, a press-release skill, etc.), remind the user they can plug them into Step 3 the same way: invoke the skill, save to its own folder under `marketing/`, and fold its "Needs Kofi" list into the final summary.
