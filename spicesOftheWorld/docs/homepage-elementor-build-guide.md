# Homepage Rebuild — Elementor Build Guide

Turns the homepage direction (artifact: `Fudi People — Homepage Direction`,
same URL from the design conversation) into concrete steps inside your
actual Elementor/WooCommerce site. The artifact is a static design
reference — nothing on it is live code, and nothing here requires touching
theme files or PHP. Every step below is a normal Elementor edit.

Do this **after** the demo-product cleanup (trashing Pure raw honey etc.)
and the "Spices of the World" WooCommerce import — a few sections below
link out to those categories, so they should exist first.

---

## 0. Global setup (do this once, before building sections)

**Colors** — Elementor → Site Settings → Global Colors. Add these 6,
named exactly so they're easy to reuse consistently across sections:

| Name | Hex | Used for |
|---|---|---|
| Ground | `#FBF3E7` | Page background |
| Ground Raised | `#F6E9D6` | Section backgrounds (Three Journeys, footer) |
| Ink | `#3A1210` | Body text |
| Marigold | `#E07610` | Primary accent, buttons, badges |
| Maroon | `#6B1B1F` | Headings, dark section backgrounds |
| Gold | `#E79A2E` | Secondary accent, hover states |

**Fonts** — Elementor → Site Settings → Global Fonts (or Theme Style →
Typography). Elementor pulls these straight from Google Fonts, no file
upload needed:
- **Fredoka**, weight 600/700 — all headings, nav, logo, buttons
- **Caveat**, weight 700 — eyebrows/taglines and the pull-quote only.
  Used sparingly — never for body copy or anything long
- **Karla**, weight 400/600/700 — body text, nav links, captions

Set these as your **Primary/Secondary/Text** global font roles so every
new Heading/Text widget picks them up automatically instead of the theme
default.

**Images** — real assets to use are already in this repo:
`thumbnails/reference-photos/` (photos) and `video/` (clips). Upload the
specific files named in each section below to the WordPress Media
Library before building that section.

---

## 1. Top brand bar

A thin (8px) full-width strip above the header, gradient left-to-right:
Maroon → Marigold → Gold → Marigold.

- Add a new **Section** above your existing header, height set to `8px`,
  content width **Full Width**
- Background type: **Gradient**, angle 90°, stops: Maroon 0% →
  Marigold 35% → Gold 65% → Marigold 100%
- No content inside it — it's purely decorative, so mark it
  `aria-hidden` if your theme's Section settings expose an attributes
  field (Advanced → Custom Attributes: `aria-hidden|true`)

---

## 2. Header / navigation

Keep your existing header structure (logo left, nav center/right, cart +
CTA button right) — just restyle it:

- Logo text: "Fudi People" in Fredoka 700, Maroon, with a small
  "SPICES OF THE WORLD" sub-label underneath in Karla 600, uppercase,
  letter-spacing 2px, Ink-soft color
- Nav menu items (Karla 600): **Spices of the World** (new — see §4),
  **Our Story**, **How We Do It**, **Where to Buy**, **Contact**
- If you want the mega-menu structure discussed earlier: make "Spices of
  the World" a parent nav item with the 7 region categories as dropdown
  children, linking to each `/product-category/{slug}/` page created by
  the earlier CSV import
- CTA button ("Shop Now"): Elementor Button widget, background Maroon,
  text color `#FDF3E4`, border-radius `999px` (fully pill-shaped),
  hover background Maroon Deep (`#4A1015`, add as a 7th global color if
  you want the exact hover state)

---

## 3. Hero section

Two-column layout (Container widget, 55/45 split on desktop, stacks on
mobile):

**Left column:**
- Eyebrow text ("Grown in Sidcup. Rooted in Accra.") — Text widget,
  Caveat 700, Marigold-deep color, ~1.7rem
- Headline ("Spices of the World, Grown by One Family.") — Heading
  widget, Fredoka 700, Maroon, clamp-style responsive size (set Desktop
  ~3.4rem, Tablet ~2.6rem, Mobile ~2.2rem in Elementor's responsive size
  controls)
- Body paragraph (the Mokola Market memory copy) — Text Editor widget,
  Karla 400, Ink-soft, max-width ~46 characters per line (set a max-width
  in px, roughly 520px, so it doesn't stretch full-width)
- Two buttons side by side: "Shop the Spice Journey" (solid Maroon,
  links to a Shop page or the first region category) and "Read Our Story"
  (outline/ghost style, Maroon border and text, links to §6 anchor)
- Three small stats (34 Episodes Told / 3 Spice Journeys / 1 Family
  Farm) — Icon List or a 3-column inner Container, numbers in Fredoka
  700 Marigold-deep, labels in Karla 600 uppercase Ink-soft

**Right column:**
- Image widget: **`kofi-direct-camera-watering-can-fork-2026.jpg`**
  (Kofi, fork and watering can, doorway framing) — this is the one
  already wired into the mockup artifact. Border-radius 22px,
  object-fit cover, aspect ratio ~4:5
- Background of this column: a soft radial glow behind the image using
  Marigold at low opacity — Elementor's Background → Gradient on the
  column itself works for this

**Section background:** two soft radial gradients (Marigold top-right,
Gold top-left) over the Ground color — Elementor's section background
only supports one gradient natively, so either layer a second
Background Overlay, or simplify to a single Marigold radial if your
Elementor version doesn't support stacked backgrounds cleanly.

---

## 4. "Three Journeys, One Shelf" section

Replaces the old "Beyond Organic" product showcase entirely.

- Section background: light gradient from a Marigold-tinted top edge
  into Ground Raised, 3px solid Marigold top border
- Section heading: eyebrow "Three Journeys, One Shelf" (Caveat),
  title "Every Jar Traces Back Somewhere Real" (Fredoka, Maroon),
  centered, max-width ~640px
- **3-column layout**, one card per region:

| Column | Badge color | Title | Description | Link target |
|---|---|---|---|---|
| 1 | Maroon circle, Marigold chilli-pod icon | Spices of Africa | "Yaji, harissa, pilau masala, jerk — eight regions from Ghana to Durban, told one at a time." | `/product-category/africa/` |
| 2 | Maroon circle, Marigold leaf/botanical icon | Spices of South Asia | "Garam masala, chaat masala, gunpowder — the second jar on the shelf, six regions deep." | `/product-category/south-asia/` |
| 3 | Maroon circle, Marigold peppercorn icon | Spices of East Asia | "Five-spice, shichimi, doubanjiang — the third and final jar, from Seoul to Sichuan." | `/product-category/east-asia/` |

Each card: white background, 20px border-radius, 1px border in a warm
tan line color, hover state lifts 4px with a soft shadow (Elementor
Motion Effects → Hover Animation → "Grow" gets close, or set a custom
`transform: translateY(-4px)` via the Advanced → Custom CSS panel if
your plan includes it). Badge icons can be simple Font Awesome icons
(chili-pepper icons exist) inside a colored Icon Box widget instead of
custom SVG if that's easier to maintain in Elementor than an SVG upload.

Below each card's description, add a small pill/tag showing episode
count (e.g. "8 regions · 8 episodes") — a Text widget styled as an
inline badge (Ground background, Ink-soft text, 999px border-radius,
small padding).

---

## 5. "Where It Started" story section

Two-column layout (reverse of the hero — photos left, text right on
desktop):

**Left column** — 2 stacked/offset images:
- **`daughter-glasses-chilli-oil-bottles-lineup.jpg`** (top, larger) —
  "the actual stock" caption
- **`daughter-tongue-out-chilli-oil-africa-garden.jpg`** (bottom,
  slightly offset/smaller, aligned to the right edge) — "family energy,
  not stock photos" caption

Both already wired into the mockup artifact at the right crop/focal
point — screenshot the artifact for exact positioning reference if
needed.

**Right column:**
- Eyebrow "Where It Started" (Caveat)
- Heading "Mokola Market Planted the Seed." (Fredoka, Maroon)
- Two paragraphs of the founder story (already drafted in the mockup —
  copy directly, it's real brand-voice copy, not placeholder)
- Pull-quote: "Every spice on this shelf planted the seeds for the next
  one." — style as Caveat 700, ~1.9rem, Marigold-deep, with a 4px
  Marigold left border and Kofi's name/title underneath in small Karla
  700 caps

---

## 6. "How We Do It" values strip

Full-width Maroon background section, cream text (`#FBE9D4`), 4-column
grid (2x2 on mobile):

1. **Grown, Not Just Sourced** — "Chillies and okra come off our own
   polytunnels in Sidcup before anything reaches a jar."
2. **One Region at a Time** — "Every blend is researched region by
   region, never compressed into a single 'world spice' shortcut."
3. **The Real Recipe, Cited** — "History and science behind every blend
   is sourced and spoken on camera, not invented for the label."
4. **Family Business, Full Stop** — "Farmed, blended, and told by the
   same family, from Accra to Sidcup."

Each: a number label in Gold/Fredoka (purely a visual rhythm device here,
not a real sequence — feel free to drop the numbering if it reads as
decoration rather than order), bold title in Fredoka, body in Karla,
centered.

---

## 7. "Follow the Journey" CTA band

Centered content, Ground background with two overlapping radial
Marigold/Gold glows (same technique as the hero background):

- Eyebrow: "Watch, Then Taste"
- Heading: "Follow the Journey, Region by Region"
- Body: "34 episodes and counting — each one traces a single spice
  blend back to where it actually comes from, then shows you how to cook
  with it."
- Two buttons: "Watch on YouTube" (solid Maroon, links to the channel)
  and "Browse All Spices" (ghost, links to the shop/Spices of the World
  landing)

---

## 8. Footer

4-column layout:

1. **Brand column** — "Fudi People" + one-line mission statement (write
   your own — this was left as a placeholder deliberately)
2. **Shop** — links to the 3 (or 7, depending which catalog you've
   published) region categories, plus Chilli Oils
3. **Learn** — Our Story / How We Do It / Where to Buy / The YouTube
   Series
4. **Get in Touch** — `fudipeople@gmail.com`, shop address, phone,
   social handles (all still placeholders — fill in your real details)

Bottom bar: copyright line + your call on whether to keep the "Website
built by The Free Website Guys" credit.

---

## Build order recommendation

Build and review one section at a time rather than all 8 at once —
Elementor previews live, so you'll catch font/color mismatches faster
section by section:

1. Global colors + fonts (§0) — do this first, everything else depends on it
2. Header + brand bar (§1–2) — sets the tone immediately
3. Hero (§3) — the section that has to land hardest
4. Three Journeys (§4) — needs the WooCommerce categories to exist first
5. Story (§5), Values (§6), CTA (§7), Footer (§8) — lower risk, can go
   in any order

## Not covered here

- Actually writing the footer mission statement, address, phone, and
  social handles — genuine placeholders, your call
- Custom SVG badge icons for the Three Journeys cards — Font Awesome
  substitutes suggested above as the lower-effort path; commission real
  icons later if you want something more distinctive
- Mobile-specific tuning beyond what Elementor's responsive controls
  give you by default — check on an actual phone once built, not just
  Elementor's preview toggle
