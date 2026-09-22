# Fudi People Marketing Team

Four Claude agents that sit alongside the YouTube pipeline (Agents 1-6) and
reuse its brand voice, knowledge base and episode scripts. They live in
`.claude/agents/` so Claude Code picks them up automatically when run from
this folder.

| Agent | File | Job |
|---|---|---|
| Social & Shorts | `.claude/agents/marketing-social-shorts.md` | Episodes and farm footage -> TikTok / Reels / Shorts scripts, captions, hashtags |
| Email & Wholesale | `.claude/agents/marketing-email-wholesale.md` | D2C email sequences, plus outreach to shops, delis and restaurants |
| SEO & Website | `.claude/agents/marketing-seo-website.md` | Keywords, product page copy, blog posts for fudipeople.com |
| Campaign Planner | `.claude/agents/marketing-campaign-planner.md` | Launch plans and content calendars (chilli oils, regions, Sanko Plum Wine) |

## How they work together

1. **Campaign Planner** decides what is being pushed, when, and through which channels.
2. **Social**, **Email/Wholesale** and **SEO/Website** each produce their channel's assets from that plan.
3. Every agent reads the same ground truth first: `docs/brand-voice.md`,
   `docs/business-plan.md`, `docs/product-catalog-notes.md`,
   `knowledge-base/` and `scripts/`. None of them invents facts.
4. Nothing is published or sent by an agent. Every output is a draft for Kofi.

## Shared rules (every marketing agent follows these)

**Voice.** Reflective, warm, first-person, memory-first (`docs/brand-voice.md`).
Narration and body copy are not punchy ad copy: punchy phrasing is for
on-screen text, thumbnails, subject lines and headlines only. Farm updates use
the vlog register ("Hello, hello, Fudi people" ... "Look after yourself, look
after each other"). Do not merge the two registers.

**Positioning.** Farmer-founder tracing ingredient origins through an African
lens, not a detached food historian. Anchors: Mokola Market, Accra (never
"Makola"); the Sidcup farm; Sanko, Ghana. Mother references only where they
arise naturally, never as a marketing device.

**Facts.** Only from `knowledge-base/`, `scripts/`, `docs/`. Book content
(*The Science of Spice*) is paraphrased with a spoken/written attribution to
Dr Farrimond, never quoted. Missing fact -> `[NEEDS VERIFICATION: ...]`.
Missing personal detail -> `[NEEDS KOFI: ...]`. Missing business number ->
`[OPEN: ...]`.

**Never gate the recipe.** The full recipe stays in the video. Marketing
points to fudipeople.com for the ready-made blend and a printable card.

**Only promote what can be sold.** Wet blends (Yassa, Harissa, Zhug, Niter
Kibbeh etc.) are not shelf-stable products yet. Do not advertise them for
sale. Check `docs/product-catalog-notes.md` and the current published-product
list before promoting any SKU. Mention only the 20 dry blends and chilli oils
that are live.

**UK compliance guardrails (flag, don't decide).**
- No medical or health claims. The Health Benefits sections are for
  "research suggests..." context in editorial content only, never product
  claims like "boosts immunity". Flag anything close to a claim for review.
- Allergens (peanuts, tree nuts, sesame, mustard, soy, dairy) must be
  correct and confirmed against real supplier ingredients before any copy
  states them. This is a legal requirement (Natasha's Law); agents are not a
  substitute for that check.
- Sanko Plum Wine is alcohol: UK ASA/CAP rules on alcohol advertising apply
  (18+, no targeting minors, no linking to social success or health). Flag
  for review before any draft goes out. Licensing status: `[OPEN]`.
- Email must respect UK GDPR / PECR: consent-based lists only, unsubscribe in
  every email. Cold B2B outreach to named individuals at limited companies is
  a grey area; keep it to a small, relevant, easy-to-opt-out pattern and flag
  for Kofi's decision.

**Budget.** Under GBP 1,000 for the first phase. Favour free and owned
channels, organic content, and reuse of existing footage, photos and scripts.
No paid-ads recommendations without a stated budget from Kofi.

**Output hygiene.** Save drafts under `marketing/<channel>/` with a date
prefix. End every output with a short "Needs Kofi" list.

## Content skills (added 2026-09-21/22)

Four single-piece content skills live in `.claude/skills/` and share the
same rules above: `blog-post`, `newsletter`, `linkedin-post` (each writes one
piece and saves to its own `marketing/<channel>/` folder), and
`content-repurposing`, which runs all three on one source in sequence.

`explainer-infographic` (added 2026-09-22) is a separate, standalone skill:
turns a topic or a set of stats into one shareable infographic image. Real
HTML/CSS rendered to PNG via headless Chromium (`scripts/render.py`), not
AI image generation, so every number and word is exact. Saves to
`marketing/infographics/`.

`product-infographic` (added 2026-09-22) turns a product URL or photo into
a listing image with labeled feature callouts — a pointer line to visible
parts of the product, plain badges for claims with no visual spot to point
to. Same real-HTML-to-PNG approach. Saves to `marketing/product-images/`.
Known limits, tested 2026-09-22: this workspace's network proxy blocks
downloading a linked product image via `curl`, so a URL-only source usually
needs the user to attach the photo directly; pointer-line placement is a
best-effort visual estimate, not a measurement.

`product-to-ad` (added 2026-09-22) turns a product photo/URL into a finished
UGC-style talking-head video ad, orchestrating Higgsfield's bundled
`ugc-review-video` workflow (generated adult creator, not Kofi or any real
person) rather than a local render — the only marketing skill that spends
real paid credits (~120-190 for a 10-15s ad) instead of running free.
Requires an explicit go-ahead on cost before generating; never uses a real
photo of Kofi or his family as the on-screen creator; Sanko Plum Wine needs
Kofi's own sign-off first (alcohol ad rules). Saves a brief with the hosted
video URL and disclosure line to `marketing/product-ads/`. Not live-tested
with a real generation yet (built and cost-checked 2026-09-22; Kofi held off
on spending credits on the test run) — the pipeline itself is Higgsfield's
own, already in production use elsewhere, so the risk is in the Fudi-specific
wiring (claims sourcing, product-allowlist checks), not the render.
