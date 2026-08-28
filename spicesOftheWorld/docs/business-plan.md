# Fudi People — Business Plan & Prioritised Action List

**Prepared:** 2026-08-26
**Company:** Fudi People Ltd (UK, company no. 14119302)
**Founder:** Kofi

## How to read this document

This plan is grounded in two sources: what you told Claude Code directly, and what's
actually verifiable in the `SpicesOftheWorld` repo as of 2026-08-26. Where the two
disagreed, this document follows the decisions you made when asked:

- **Website**: treated as **live**, not "not started" — fudipeople.com has Coming Soon
  switched off, 54 of 89 products published with real pricing, and real card payments
  enabled.
- **HACCP draft, chilli oil bottle labels (Africa/South Asia/East Asia with Twi/Chinese
  naming), and the AI presenter character concept**: these exist as **your own files
  outside this repo** — Claude Code can't currently see or verify them. Treated below as
  real but **not yet consolidated** into a trackable location, which is itself a small
  action item.
- **Taxonomy**: the **7-region website structure** (adding Southeast Asia and Europe) is
  authoritative. The 34 already-written episodes only cover 5 regions — Southeast Asia
  and Europe content gets written later.
- **Budget**: under £1,000 for the first phase, deliberately **not** rolling out all
  seven regions/34+ SKUs at once.

Figures that would need real numbers you haven't given yet (bottle volume, exact batch
sizes beyond "small," a fixed launch date) are flagged inline as **[OPEN]** rather than
invented.

---

## 1. Current State Summary

### Product & Packaging

| Item | Status |
|---|---|
| Recipes (3 original lines: Africa, South Asia, East Asia) | Done — scripted, in `product-catalog-notes.md` |
| HACCP hazard analysis | **In progress, external** — you have a draft covering allergen assessment and a pressure-canner framework; the only trace inside this repo is one note flagging dried garlic as higher-risk and recommending validation at 116–121°C. Not yet consolidated here, not yet finalised. |
| Spice mix front-of-jar labels (34 blends) | Done as a **design**, not production-ready — HTML/CSS system, Yaji approved as the reference design, all 34 rendered as a proof sheet. **Screen resolution only: 359×359px @96dpi**, not print-ready. |
| Spice mix back-of-jar labels (ingredients, allergens, net weight, barcode) | Not started |
| Chilli oil bottle labels (Africa/South Asia/East Asia, local-language naming) | **In progress, external** — your files, not yet in this repo. One PDF (`chili-oil-south-asia-label.pdf`) exists in `brand-assets/product-labels/`; resolution/print-readiness unconfirmed. |
| Bottle sourcing (chilli oil) | Not started |
| Jar sourcing (spice mixes) | Not started |
| Raw spice ingredient sourcing (non-chilli: ginger, grains of paradise, grains of selim, etc.) | **Research done** — Ghana markets/B2B platforms identified, UK import rules and HS codes checked, a supplier vetting checklist drafted. See `docs/ghana-spice-sourcing.md`. Not yet started: actual supplier outreach, HMRC classification ruling for grains of paradise/selim, confirmed duty rates. |
| Co-packer vs. self-fill decision | Not started |
| Unit costing / margins | Not started |

### Website

| Item | Status |
|---|---|
| Site live, Coming Soon off | **Done** (2026-08-21) |
| Products published with real price/copy | **54 of 89**, verified clean (no placeholder text, no mispriced wet products) |
| Payments | **Done** — WooCommerce Payments (Stripe), Apple Pay, Google Pay, Amazon Pay all live |
| Homepage, How We Do It, Where to Buy, Contact Us | **Done** — real copy, real photos, Kofi-confirmed |
| 7-region taxonomy (55 products: 48 sub-region mixes + 7 chilli oils) | **Planned**, documented in `spices-of-the-world-site-setup-guide.md`, not yet imported |
| Southeast Asia / Europe content | Not started — zero episodes exist for either region |
| 35 draft products (mostly wet-only items needing recipe rework) | In progress |
| Real product photography (replacing generated placeholder cards) | Not started — affects 30+ products |

### YouTube / Content Pipeline

| Item | Status |
|---|---|
| Episode scripts, 5-region structure (Africa, Middle East, South Asia, East Asia, Americas) | **Done** — all 34 written |
| Knowledge base (regional profiles, spice profiles) | **Done** — 7/7 regions, ~50/52 spices |
| Brand voice profile | Done |
| Episode 1 (Yaji) | **Furthest along** — rough cut exists with real farm/market footage plus 2 Higgsfield-generated map B-roll clips spliced in. Still missing: Kofi's own voice reading the script, and footage of Yaji actually being mixed/grilled. |
| Episode 2 (Yassa) B-roll | 2 clips generated, not yet spliced into an animatic (no Episode 2 rough cut exists yet) |
| n8n multi-agent pipeline (Agent 2 Knowledge, Agent 3 Script Writer) | **Built but likely stale** — last confirmed working 2026-07-25, over a month ago. The vector store is in-memory and wipes on every restart; no confirmation it's been rebuilt since. **Treat as needing a re-verification pass, not as "running."** |
| Higgsfield (B-roll generation trial) | Credits exhausted as of last use; trial-renewal status needs checking |
| AI presenter character (locked face, region-coded aprons) | **In progress, external** — your concept, not yet in this repo |
| Southeast Asia / Europe episode scripts (~15 sub-regions) | Not started |

### Company Operations

| Item | Status |
|---|---|
| PSC register (Companies House) | Not started — needs updating to reflect current shareholding |
| Food safety sign-off | Blocked on HACCP finalisation above |
| Allergen labelling verification (Natasha's Law) | Flagged as needed in `product-catalog-notes.md`, not yet done — every product description has a *generated* allergen flag based on scripted ingredients, explicitly marked as needing verification against real supplier ingredients |

---

## 2. Gap Analysis

### Product & Packaging → launch-ready
The biggest gap: **everything here is either a design file or a plan — nothing has been
physically produced.** Specific gaps:
- No print-ready (300 DPI) label files for either product line
- No bottle or jar actually sourced — sizes, materials, and cap types haven't been decided
- No finalised, validated HACCP process — this blocks legal sale regardless of who
  produces it
- No back-of-jar label content (legally required: full ingredients, allergens in bold,
  net weight, best-before/use-by, business name/address)
- No unit cost model, so no pricing confidence

### Website → fully populated
- 7-region taxonomy is designed but not imported (55 products)
- Southeast Asia and Europe have no content to populate their product pages with
- 35 existing drafts need resolving (mostly the wet-only products awaiting the same
  dry-conversion treatment 11 others already got)
- Real photography still missing for 30+ products

### YouTube / Content → repeatable pipeline
- n8n needs a live-status check before being relied on again
- Only 1 of 34 scripted episodes has real progress toward a finished video
- Southeast Asia/Europe need scripts written from scratch (or adapted from the book, per
  the setup guide's own suggested fallback)
- The AI presenter character isn't validated against the pipeline yet — real footage of
  Kofi exists and is already confirmed usable, so the pipeline doesn't strictly need the
  presenter character to produce a first episode

### Company Operations → operationally sound
- PSC register: pure admin, no technical dependency, just needs doing
- HACCP: the one genuine hard blocker across the entire plan — see the sequencing note
  in Section 3

---

## 3. Packaging & Production Action Plan

This is the priority section, per your brief. Given the **under-£1,000, phased, one-region-first**
budget, the plan below assumes **self-fill**, not a co-packer, for the first run — the
reasoning is in 3.4.

### 3.1 Chilli oil labels: screen-res → print-ready

1. **Consolidate what exists first.** Before spending anything, pull your external chilli
   oil label files (Africa/South Asia/East Asia, with Twi/Chinese naming) into this repo
   so they're versioned and not at risk of being lost, same as happened with the earlier
   HACCP note. Check what format they're actually in — vector (AI/EPS/SVG) or raster
   (PNG/JPG) — since that determines the next step entirely.
2. **If vector**: scaling to 300 DPI print size is close to free — vector art has no
   fixed resolution, it just needs re-exporting at the target physical size and DPI.
3. **If raster and below 300 DPI at the target print size**: it needs to be recreated,
   not just upscaled — AI upscaling can help but won't produce genuinely print-safe fine
   text/line art. Given the spice-jar label system here was built as clean HTML/CSS
   (fonts, not flattened images), the **same approach can be reused for the chilli oil
   labels** if they haven't been built that way already: author as HTML/CSS at the real
   physical size in millimetres, which sidesteps the DPI problem entirely (the render is
   generated at whatever resolution you export it at).
4. **Decide the physical label shape/size** — this depends on the bottle (3.3), so
   sequence bottle sourcing before finalising label die-cut dimensions.
5. **Get 2–3 label printer quotes.** Questions to ask every printer:
   - Minimum order quantity, and price per label at your quantity tier (expect this to
     be steep below ~250–500 labels — factor that into whether you order more labels
     than your first bottle batch needs, since labels are usually the cheaper unit cost)
   - **Material**: chilli oil bottles get handled and sometimes get oil on the outside —
     ask specifically for oil/water-resistant vinyl or a laminated finish, not standard
     paper stock, which will degrade
   - File format needed: most professional label printers want vector PDF/AI with fonts
     outlined; confirm before sending your Adobe Fonts-based HTML render
   - Turnaround time and whether a physical proof/sample is offered before full print

### 3.2 Spice mix packaging (not yet designed)

The existing front-of-jar label system was built as a **95mm round label**, which
implicitly assumes a **jar**, not a pouch. Given the budget and phasing constraints:

**Recommendation: jar, not pouch, for the first run.** A pouch would mean designing an
entirely new label shape and format from scratch; a jar lets you reuse the approved
label work directly. Revisit pouches later if a specific product needs it (e.g. a
resealable format for a larger retail size).

Steps:
1. Decide fill weight per jar — **[OPEN]**, needs a real number (the existing labels
   show a placeholder "NET WT 50g")
2. Confirm jar diameter matches (or adjust) the 95mm label design
3. Source small-quantity glass jar suppliers — look for craft/specialty food packaging
   suppliers rather than industrial wholesalers; many sell in quantities of 12–100+
   without large MOQs, which fits a sub-£1,000, single-region-first budget far better
   than a wholesale supplier's typical 500–1,000+ unit minimums
4. Confirm lid type (twist lid is standard and cheapest; consider whether a shaker/sifter
   lid suits spice mixes better than a plain jar lid for a small home-cook audience)
5. Print/apply the already-approved label design once jars are in hand

### 3.3 Chilli oil bottle sourcing

1. **Decide bottle volume first** — **[OPEN]**, this drives everything downstream
   (label size, cost per unit, shipping weight)
2. Look for: food-grade glass (not plastic — chilli oil can degrade some plastics over
   time and glass reads as higher-quality for a premium positioning), a cap/closure
   suited to oil (a pour spout or drizzle top is more on-brand for a chilli oil than a
   plain screw cap, but costs more — weigh against budget)
3. Source from small-quantity suppliers first, same reasoning as jars — avoid wholesale
   MOQs until volume is proven
4. Questions to ask bottle suppliers:
   - Minimum order quantity and price breaks at higher quantities
   - Whether bottles are food-grade certified (get this in writing — you'll need it for
     your own food safety documentation)
   - Cap/closure options and whether a tamper-evident seal is included or needs sourcing
     separately
   - Lead time — glass bottle suppliers can have longer lead times than jar suppliers

### 3.4 Co-packer vs. self-fill: decision framework

| | Self-fill | Co-packer |
|---|---|---|
| Cost to start | Low — fits sub-£1,000 budget | High — most co-packers have minimum order runs well beyond £1,000 of product |
| HACCP requirement | You need your own validated process (home kitchen already EHO-registered, per `docs/site-pages-how-where-contact.md`) | Co-packer typically requires *you* to already have (or jointly develop) a validated HACCP plan before they'll take you on — they carry legal liability too |
| Volume ceiling | Limited by your own kitchen capacity and time | Scales to real commercial volume |
| Control | Full control over recipe/process | Less control, more consistency at scale |
| Right choice given current state | **Yes, for now** | Revisit once (a) HACCP is finalised and validated, (b) volume consistently exceeds home-kitchen capacity, (c) budget supports a real MOQ |

**Recommendation**: self-fill for the first phase. It matches the budget, and a
co-packer isn't really available to you yet regardless of preference, since HACCP isn't
finalised.

### 3.5 Sequencing — what has to happen before what

```
1. Finalise & validate HACCP (pressure-canner validation, full allergen check)
        │  ← hard blocker: nothing below can legally proceed without this
        ▼
2. Decide bottle volume + jar fill weight  ──────┐
        │                                         │
        ▼                                         ▼
3. Source bottles                        4. Source jars
        │                                         │
        └──────────────┬──────────────────────────┘
                        ▼
5. Finalise label print dimensions (needs bottle/jar size)
                        │
                        ▼
6. Get print-ready (300 DPI) label files + printer quotes
                        │
                        ▼
7. Produce first small test batch (self-fill)
                        │
                        ▼
8. Sell through website (already live) — validate before reordering
```

HACCP sits at the top because it's the one item that blocks everything else legally, not
just practically — even a self-fill test batch sold to real customers needs it.

---

## 4. Website Rollout Plan

Sequence regions by **content readiness**, not by taxonomy order, since Southeast Asia
and Europe have zero episode content:

1. **Already live, needs finishing**: Africa, South Asia, East Asia (the original 3
   jars) — resolve the 35 draft products, prioritise real photography here first since
   these are the most customer-visible pages already
2. **Next**: Middle East (8 episodes written) and Americas (6 episodes written, plus the
   Caribbean) — publish/polish product pages using existing script content, since the
   copy work is largely already done
3. **Fix known structural issues** before or alongside step 2: Iran currently has no
   home in the 7-region taxonomy (it's Episode 15's region but isn't listed under Middle
   East's sub-regions); Americas has an internal overlap (South America listed alongside
   its own Amazon/Andes sub-regions) — worth resolving before importing the full 55-product
   taxonomy so it doesn't get baked into live URLs/categories
4. **Last**: Southeast Asia and Europe — no episodes exist yet. The site-setup guide
   already suggests a fallback: pull real copy from the knowledge base's regional files
   (which do exist for both regions) rather than waiting for full episodes, if you want
   these pages live sooner. Otherwise, treat this as gated on the content pipeline
   catching up (Section 5).

---

## 5. Content Pipeline Plan

1. **Re-verify n8n before relying on it.** It's been over a month since confirmed
   working. Concretely: confirm the Docker container is still running, then re-run
   Agent 2's Manual Trigger to rebuild the in-memory vector store (this is wiped on every
   restart — a known standing gap from the last time this was tested).
2. **Finish Episode 1 next** — it's closest to done. Two real gaps remain: Kofi's own
   voice reading the actual script (currently a placeholder TTS voice), and real footage
   of Yaji being mixed and grilled. Both need Kofi's own time, not more AI generation.
3. **Don't block on the AI presenter character.** Real footage of Kofi talking to camera
   already exists and was confirmed usable back in July. Ship Episode 1 (and likely
   Episode 2) with real Kofi footage while the presenter-character concept matures
   separately — that decouples the content pipeline from a system that isn't finished
   yet.
4. **Recommended episode order after Episode 1**: Episode 2 (Senegal) has a head start —
   2 B-roll clips already generated, just needs an animatic built. Then continue through
   the rest of Africa (Episodes 3–8), since that's where the personal voice/story
   material is richest. Then Middle East, South Asia, East Asia, Americas in whatever
   order matches upcoming product launches on the website (Section 4) — releasing an
   episode alongside its region going live on the store is free marketing alignment.
5. **Southeast Asia / Europe scripts last**, matching their website priority — write
   these once the 5-region backlog is genuinely moving, using the same research-prompt
   pattern already established for the other regions.
6. **Check Higgsfield trial/credit status** before assuming more B-roll can be generated
   — credits were exhausted as of the last session; confirm whether the trial renewed,
   converted to paid, or lapsed.

---

## 6. Prioritised Action List

Ordered; **[BLOCKING]** marks items that stop other work until resolved.

1. **[BLOCKING]** Finalise and validate the HACCP hazard analysis — pressure-canner
   validation, full allergen assessment across all products going to market. Nothing in
   Section 3 can legally proceed past sourcing without this.
2. Consolidate your external files (HACCP draft, chilli oil labels, presenter character
   concept) into this repo so they're tracked and not at risk of being lost, same as
   happened once already with the original HACCP note.
3. **[BLOCKING for 4–7]** Decide chilli oil bottle volume and spice jar fill weight —
   both currently open decisions that everything downstream (sourcing, label sizing,
   costing) depends on.
4. Source 2–3 small-quantity chilli oil bottle suppliers, request quotes and food-grade
   certification.
5. Source 2–3 small-quantity glass jar suppliers for spice mixes (reusing the existing
   95mm round label design).
6. Once bottle/jar sizes are confirmed, finalise print-ready (300 DPI) label files for
   both product lines and get 2–3 label printer quotes (oil-resistant stock for the
   chilli oil labels specifically).
7. Confirm self-fill as the production model for the first batch (Section 3.4) — no
   further action needed here beyond acknowledging it, since it falls out of the budget
   and HACCP timing, but worth stating explicitly so it's not revisited unnecessarily.
8. Produce and sell a small first test batch (single region, e.g. Africa/Yaji, since its
   label and much of its content is furthest along) through the already-live website.
9. Update the PSC register at Companies House — pure admin, no dependencies, quick win.
10. Re-verify the n8n pipeline is actually running (Docker status, rebuild the vector
    store) before writing it into any near-term plans.
11. Finish Episode 1: Kofi's own voiceover, real Yaji mixing/grilling footage.
12. Resolve the website's known taxonomy issues (Iran's missing home, Americas overlap)
    before importing the full 7-region/55-product structure.
13. Clear the 35 draft products (mostly wet-only items) — decide per-item: dry-convert,
    drop, or hold for a refrigerated-product line later.
14. Build Episode 2's animatic using the B-roll already generated, then continue through
    the rest of Africa's episodes.
15. Plan real product photography to replace the generated placeholder cards — lower
    urgency than the above, but growing (30+ products affected) and worth scheduling
16. Act on `docs/ghana-spice-sourcing.md`'s open items: get an HMRC (or freight
    forwarder) classification ruling for grains of paradise/selim, confirm actual duty
    rates via trade-tariff.service.gov.uk, and decide whether non-chilli spice sourcing
    starts via a physical market visit (Kumasi/Techiman/Makola) or B2B platform outreach
    before any real marketing push.
