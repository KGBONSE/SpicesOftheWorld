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
