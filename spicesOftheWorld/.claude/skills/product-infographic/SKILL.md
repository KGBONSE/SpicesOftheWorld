---
name: product-infographic
description: Turns a product URL or a product photo into a clean listing image with labeled feature callouts, Amazon-style. Use when asked for a product infographic, a listing image, or a feature-callout graphic, or with "/product-infographic".
---

## What this skill does

Builds a single listing-style image: the product photo, its name, and its real
features or benefits called out around it — some with a pointer line to the
exact part of the product, some as plain badges. Rendered as real HTML/CSS
screenshotted to PNG, same approach as `explainer-infographic` and for the
same reason: text needs to be exact, and an AI-generated image would garble
labels and lines.

## Trigger phrases

"/product-infographic", "product infographic", "listing image", "feature
callout image", "Amazon-style graphic for this product".

## Step 1 — Get the input

Ask, if not already given: a **product URL**, an **uploaded product photo**,
or both.

- **URL only** — fetch the page with WebFetch. Pull the product name and
  3–6 real feature/benefit bullets from the page's own copy (bullet points,
  "About this item," spec table, description) — never invent or embellish a
  claim the page doesn't make. Look for the main product image URL in the
  page content, then try to download it with `curl` into a scratch path so
  the real pixels can be composited. **This step is not reliable in every
  workspace** — confirmed by testing: this environment's network proxy
  blocks `curl` from reaching arbitrary hosts (a 403 on the CONNECT tunnel)
  even when WebFetch itself can read the same page's text fine, and many
  e-commerce pages also render their real gallery image via JavaScript that
  a text fetch never sees in the first place. If the image can't be
  downloaded for either reason, don't retry with a different technique or
  try to route around it — say so plainly and ask the user to attach the
  product photo to the chat instead, then continue from there. Product
  name/copy extraction and photo acquisition are two separate steps; one
  failing doesn't block the other.
- **Photo only** — use the photo directly. Ask for 3–6 features/benefits to
  call out (or a product URL/description to pull them from) if not given —
  don't invent selling points for a photo alone.
- **Both** — use the given photo (guaranteed real pixels) and pull copy from
  the URL.
- **Fudi People product** — check `docs/product-catalog-notes.md` and this
  project's own product photos/labels first, and follow the shared rules in
  `agents/marketing-team.md`: only promote published products, no health
  claims beyond "research suggests," `[VERIFY ALLERGENS AGAINST SUPPLIER]`
  on any allergen mention.

## Step 2 — Look at the photo, sort the features

Read/view the product photo. Sort the features/benefits gathered in Step 1
into two groups:

1. **Visually locatable** — a physical part of the product visible in the
   photo (a lid, a spout, a label panel, a handle, a seal). For each, note
   an approximate position as a percentage of the image's own width/height
   (e.g. "cap — 50%/12% from top-left") based on what's actually visible.
   This is a best-effort visual estimate, not a measurement — say so in the
   final summary.
2. **Not visually locatable** — an ingredient, a certification, a stat, a
   claim ("cold-pressed," "small-batch," "gluten-free") with no physical
   spot on the photo to point to.

Cap it at 3–6 total call-outs across both groups — more than that clutters
the image and stops being readable.

## Step 3 — Build and render

1. Read the `dataviz` skill once for the palette/typography method if not
   already loaded this session (reuse the same palette tokens as
   `explainer-infographic`'s template so the marketing team's visuals read
   as one family).
2. Write a self-contained HTML file from `template.html` in this skill's
   folder: product photo centered on a clean surface, product name as a
   headline, **group 1** features as labeled callout boxes connected to
   their estimated point on the photo by a thin SVG leader line, **group 2**
   features as plain badge chips (no line) placed around the image. Default
   canvas **1080x1350** (portrait), unless the user asks for square
   (1080x1080) or landscape.
3. Render it: `python3 .claude/skills/product-infographic/scripts/render.py <input.html> <output.png> [width] [height]`
4. Open the PNG and check it: no callout box overlapping the product photo,
   nothing clipped by the canvas edge, and no leader line overlapping
   another line or a callout box. A straight line grazing past unrelated
   label text on its way to the target is expected (this template draws
   straight lines, not routed/bent connectors) and is fine as long as it
   stays legible — re-slot a callout only if a line actually obscures
   something. Adjust and re-render if anything looks wrong before calling
   it done.

## Step 4 — Save and deliver

Save both files to `marketing/product-images/YYYY-MM-DD-<slug>.png` and
`.html`. Deliver the PNG to the user directly.

## Step 5 — Summarize

Show: the product, the source (URL or uploaded photo), which features got a
pointer line vs. a badge, canvas size, and the file paths. End with a
"Needs Kofi" list — always including a reminder that pointer-line
placement is a best-effort visual estimate worth a quick human check, plus
anything unverified, health/allergen-adjacent, or touching an unpublished
product.

## Rules

- Never invent a feature, spec, or claim the source (page copy or the
  user) didn't state.
- No health claims beyond "research suggests" framing (shared rule).
- Only use a photo the user supplied or the product's own listing photo —
  never substitute unrelated stock imagery for the actual product.
- If a fetch is blocked or an image can't be found, say so and ask for a
  photo — don't retry with a workaround.
