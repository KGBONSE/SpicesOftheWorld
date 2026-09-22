---
name: product-to-ad
description: Turns a Fudi People product photo or URL into a finished UGC-style talking-head video ad via Higgsfield. Use when asked for a product-to-ad, a UGC video ad, or with "/product-to-ad".
---

## What this skill does

Produces one finished, hosted 9:16 UGC-style video ad: an AI-generated adult
creator holds/talks about a real Fudi People product on camera. This is not a
local render like `explainer-infographic` / `product-infographic` — it
orchestrates Higgsfield's own bundled `ugc-review-video` workflow (image
boards -> de-slop pass -> video clips -> ffmpeg assembly), which runs on
Higgsfield's paid generation credits and takes several minutes end to end.

## Trigger phrases

"/product-to-ad", "product to ad", "UGC video ad", "turn this product into a
video ad", "make me a UGC ad for this product".

## Step 1 — Get the input

Ask, if not already given: a **product photo or URL**, and a **duration**
(offer 10s / 15s / 30s / 45s — Higgsfield's own intake step asks this too if
skipped here).

- **Fudi People product** — check `docs/product-catalog-notes.md` and the
  current published-product list first. Only promote the 20 live dry blends
  and chilli oils (shared rule in `agents/marketing-team.md`). If the
  product named is a wet/not-yet-sellable item, say so and stop rather than
  generating an ad for something that can't be bought yet.
- **Sanko Plum Wine** — do not run this skill for it without Kofi's explicit
  go-ahead first. It's alcohol: UK ASA/CAP rules require 18+ framing, no
  appeal to minors, no linking to social/health outcomes, and Higgsfield's
  own safety gate is stricter about age-restricted goods than plain food
  products. Flag this clearly if asked and wait for confirmation.
- **Claims** — pull only real claims from `docs/product-catalog-notes.md`,
  the relevant `scripts/episode-NN-*.md`, or the product's own listing copy.
  These become the workflow's `approved_claims` allowlist — never let the
  creator's monologue say anything not in that list. No health claims beyond
  "research suggests" framing. Any allergen mention needs
  `[VERIFY ALLERGENS AGAINST SUPPLIER]`.

## Step 2 — Cost check before generating anything

This is real spend, unlike the free Playwright-based skills. Before
submitting any job:

1. Call `mcp__higgsfield__balance` to confirm available credits.
2. Get a cost estimate for the models this run will use (`generate_video`
   with `get_cost:true` for the clip model at the locked duration/resolution
   is enough — the workflow below names the exact models).
3. Tell the user the credit estimate and get an explicit go-ahead before
   submitting the first paid job. Only pass `use_unlim: true` if the user
   explicitly asks to spend free-trial unlimited generations — never add it
   to save them credits on your own initiative, and never drop it once
   they've asked for it.

## Step 3 — Run Higgsfield's ugc-review-video workflow

Call `mcp__higgsfield__get_workflow_instructions` with
`{"workflow": "ugc-review-video"}` and follow it exactly, phase by phase —
do not improvise around it. In particular:

- **Safety and truth gate first.** Generated adult creator (21+) only, never
  a real/uploaded photo of a specific person without clear consent, and
  never a Fudi People family photo — those show Kofi's children and are off
  limits for any synthetic-ad use regardless of what's technically uploadable.
  No fabricated testimonials or invented purchase/use history. Frame the
  output as a brand demo/creator concept, not an organic review, and include
  an ad/sponsorship disclosure line in the delivered post package.
- **Product intake** locks the real product photo and a `product_description`
  from what's actually visible/stated — never invented.
- **Monologue** (Phase 3) uses only the `approved_claims` gathered in Step 1
  above — preserve them verbatim, never strengthen or combine them.
- Boards, de-slop pass, clips, QA, and ffmpeg assembly all run through
  Higgsfield's own tools (`generate_image_batch`, `generate_video_batch`,
  `sandbox_exec`, `jobs_wait`) exactly as that workflow's SKILL.md specifies.
- Job IDs and intermediate mechanics stay internal — only the final hosted
  video URL and duration are user-facing, per that workflow's own delivery
  rule.

## Step 4 — Save and deliver

Higgsfield returns a hosted video URL, not a local file — there's no
Playwright-style PNG to save here. Save a short brief instead, to
`marketing/product-ads/YYYY-MM-DD-<slug>.md`:

- the product and source (photo/URL)
- duration and the hosted video URL
- the exact `approved_claims` used
- the ad/sponsorship disclosure line delivered with it
- date generated and credit cost spent

Deliver the video URL to the user directly in chat (and the post package —
caption, hashtags, pinned comment, disclosure — if they asked for one).

## Step 5 — Summarize

Short summary: product, duration, credit cost, the hosted video URL, and a
"Needs Kofi" list that always includes: review the video before any use (an
AI creator is not Kofi and should never be presented as him or as a real
customer), confirm the ad/sponsorship disclosure gets used wherever this is
posted, and re-verify any allergen/claim line against real supplier facts
before publishing.

## Rules

- Never invent a product claim, price, or fact the source didn't state.
- Never use a real photo of Kofi or his family as the on-screen "creator" —
  generated creator identities only.
- Only promote published, sellable products (shared rule). Sanko Plum Wine
  needs explicit go-ahead first (see Step 1).
- No health claims beyond "research suggests" framing (shared rule).
- Always disclose the output as brand-created/sponsored content, never as an
  organic customer review.
- Confirm estimated credit cost with the user before submitting paid jobs.
