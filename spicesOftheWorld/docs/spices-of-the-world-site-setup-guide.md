# "Spices of the World" — Site Build Guide

Fudi People's live site (`fudipeople.com`) is WordPress + WooCommerce +
Elementor, currently still running the theme's default demo content
("Pure raw honey," Lorem ipsum descriptions, Food/Honey/Sweets/Drinks/Tea/
Oils/Olive oil categories). Confirmed by fetching the live site directly
(2026-07-30) — no login access was used or needed, this is all public
page content.

**I have no login/CMS access to this site** — no WordPress admin, no
FTP, no Elementor editor. Everything below is a CSV to import plus manual
steps in WP admin; none of it publishes itself.

## Why a CSV import, not custom page-building

The site's category pages (`/product-category/{slug}/`) and product
pages (`/product/{slug}/`) are already rendered by WooCommerce's own
templates — grid of product cards with a category-filter sidebar on
category pages, and a Description/Additional information/Reviews tab
set on product pages. Importing products via WooCommerce's built-in CSV
importer reuses those exact templates automatically, which is the
cleanest way to "match the existing design system" without touching any
Elementor template or theme file. Building custom Elementor pages for
this instead is possible but is a separate, much bigger job — not
attempted here.

## What's in `spices-of-the-world-woocommerce-import.csv`

55 products: 48 sub-region "Spice Mix" products plus 7 "Chilli Oil"
products, one set per top-level region, matching your spec exactly:

| Category | Sub-region Spice Mixes | Chilli Oil |
|---|---|---|
| Africa | Maghreb, West Africa, Central Africa, Horn of Africa, East Africa, Southern Africa | Fudi People Chilli Oil with Spices of Africa |
| Middle East | Turkey, Syria, Lebanon, Israel, Egypt, Iraq, Arabian Peninsula | Fudi People Chilli Oil with Spices of the Middle East |
| East Asia | West China, North China, East China, South China, South Korea, Japan | Fudi People Chilli Oil with Spices of East Asia |
| South Asia | North India, Himalayan Belt, Central India, West India, East India, South India, Bangladesh, Sri Lanka | Fudi People Chilli Oil with Spices of South Asia |
| Southeast Asia | Myanmar, Thailand, Laos, Cambodia, Vietnam, Malaysia, Singapore, Philippines, Indonesia | Fudi People Chilli Oil with Spices of Southeast Asia |
| Americas | North America, Mexico & Central America, Caribbean, South America, Amazon, Andes | Fudi People Chilli Oil with Spices of the Americas |
| Europe | Scandinavia, Great Britain, France, Spain & Portugal, Italy, Southeast Europe | Fudi People Chilli Oil with Spices of Europe |

**Update: 33 of the 48 spice-mix slots now have real content**, mapped
straight from the matching episode script — exact ingredients, flavour
story, and the actual paired dish from that episode's "The Dish" section.
The remaining slots are still genuine placeholders because no matching
content exists yet: all 9 Southeast Asia slots, all 6 Europe slots, and
all 7 Chilli Oil products (no episode ever covered a chilli oil). Every
row — mapped or placeholder — is still `Published = 0`, since the mapped
copy still needs your photos and a price before it's a real listing, and
the allergen notes still need your sign-off against actual supplier
ingredients before anything goes live.

### The mapping, region by region

| Slot | Source episode | Blend | Status |
|---|---|---|---|
| Maghreb | Ep. 5 | Harissa | Wet |
| West Africa | Ep. 1 | Yaji | Dry |
| Central Africa | Ep. 7 | Mbongo Mix | Wet |
| Horn of Africa | Ep. 3 | Niter Kibbeh | Wet |
| East Africa | Ep. 6 | Pilau Masala | Dry |
| Southern Africa | Ep. 8 | Durban Curry Masala | Dry |
| Turkey | Ep. 11 | Turkish Baharat | Dry |
| Syria | Ep. 10 | Za'atar | Dry |
| Lebanon | Ep. 13 | Taklia | Wet |
| Israel | Ep. 12 | Zhug | Wet |
| Egypt | Ep. 16 | Dukkah | Dry |
| Iraq | Ep. 14 | Arabic Baharat | Dry |
| Arabian Peninsula | Ep. 17 | Hawaij | Dry |
| West China | Ep. 29 | Chilli Black Bean Sauce | Wet |
| North China | Ep. 26 | Shandong Spice Bag | Dry |
| East China | Ep. 27 | Nanjing Spice Bag | Dry |
| South China | Ep. 28 | Five-Spice Powder | Dry |
| South Korea | Ep. 24 | Yangnyeomjang | Wet |
| Japan | Ep. 25 | Shichimi-Togarashi | Dry |
| North India | Ep. 18 | Garam Masala | Dry |
| Himalayan Belt | Ep. 19 | Timur ko Chhop | Dry |
| Central India | Ep. 20 | Chaat Masala | Dry |
| West India | Ep. 22 | Vindaloo Paste | Wet |
| East India | Ep. 21 | Panch Phoran | Dry |
| South India | Ep. 23 | Gunpowder/Podi | Dry (semi-moist) |
| Bangladesh | Ep. 21 *(shared with East India)* | Panch Phoran | Dry |
| Sri Lanka | Ep. 23 *(shared with South India)* | Gunpowder/Podi | Dry (semi-moist) |
| North America | Ep. 33 | BBQ Rub | Dry |
| Mexico & Central America | Ep. 30 | Mole Mix | Dry (packaged) |
| Caribbean | Ep. 9 | Jamaican Jerk Rub | Dry |
| South America | Ep. 34 *("Pacific South America")* | Leche de Tigre | Wet |
| Amazon | Ep. 32 | Tucupí | Wet |
| Andes | Ep. 31 | Chimichurri | Wet |

**Bangladesh and Sri Lanka each share their blend** with East India and
South India respectively, because those were drafted as one combined
episode each ("East India & Bangladesh," "South India & Sri Lanka") before
this finer 8-way split existed. Both product descriptions say so
explicitly and point at each other — worth a distinct Sri Lanka blend
later (Ceylon cinnamon is the obvious candidate) if you want it to stop
being a duplicate of the South India listing.

**Three drafted episodes have no home in this structure at all**:
Senegal's Yassa Marinade (Episode 2) and Sierra Leone/Liberia's Pepper
Soup Spice (Episode 4) — both absorbed into the single "West Africa"
slot, noted in that product's description as candidates for their own
future listing — and Iran's Advieh (Episode 15), which has nowhere to go
since Iran isn't in your Middle East list. See the taxonomy flags below.

Where I set real content, I kept the same structure the placeholders
use: Short description = flavour profile and origin, Description = "How
to Make the Dish" plus the real paired dish from that episode, the dry/wet
flag, and any allergens. Untouched placeholder rows still read exactly as
before — bracketed text for you to fill in yourself.

Every row has `Published = 0` — **nothing goes live on import.** Given
the content is genuinely just brackets right now, do not flip anything to
Published until real copy and photos are in.

A `Position` column is set so each category page lists its spice mixes
first (position 1, 2, 3…) and its chilli oil last (position 99) — this
only works if the category page's sort dropdown is left on "Default
sorting"; if a customer changes the sort dropdown, WooCommerce's own
sorting takes over instead, which is expected behaviour.

## Steps to actually do this (in WP admin)

1. **Products → Import** → upload `spices-of-the-world-woocommerce-import.csv`
   → let it auto-map columns (the headers match WooCommerce's own field
   names) → run the import. This creates all 55 products as drafts and
   auto-creates the 7 new categories (Africa, Middle East, East Asia,
   South Asia, Southeast Asia, Americas, Europe) alongside your existing
   Food/Honey/Sweets/etc. categories — it won't touch or remove those.
2. **Appearance → Menus** — add a new top-level menu item, e.g. "Spices
   of the World," then add the 7 categories as its dropdown children,
   each linking to its `/product-category/{slug}/` archive page (WordPress
   will offer these directly under "Product categories" in the menu
   editor's left panel once the import in step 1 has run). I read your
   brief as one new nav section with 7 items underneath, not a full
   replacement of the existing "Shop" dropdown — flag it if you meant
   something else.
3. Go through each of the 55 draft products: add the real short
   description, the "How to Make the Dish" recipe, a product photo, and
   a price. Only then switch it to Published.

## Three taxonomy points worth your call before you fill anything in

1. **Iran isn't in your Middle East list** (Turkey, Syria, Lebanon,
   Israel, Egypt, Iraq, Arabian Peninsula = 7). We already have a fully
   drafted Iran episode/blend (Advieh, Episode 15) from the YouTube
   series with nowhere to go in this structure. Left out as specified —
   say if that was accidental.
2. **Americas has some overlap**: South America, Amazon, and Andes are
   listed as three separate sub-regions, even though Amazon and Andes are
   both part of South America. Built exactly as specified — just flagging
   it in case "South America" was meant to be the general/coastal
   catch-all (which is where our existing Pacific South America content —
   Leche de Tigre, Episode 34 — would naturally map) rather than a fully
   separate region from Amazon/Andes.
3. **Southeast Asia and Europe have no existing content at all** — no
   episodes, no drafted blends, though both regions do have a source file
   already in `knowledge-base/regional/` (`southeast-asia-spice-notes.md`,
   `europe-spice-notes.md`) if you want real copy pulled from the book
   later instead of writing all 15 of those from scratch yourself.

## Reusing what's already drafted

Done — see the mapping table above. 33 of the 48 spice-mix slots now
carry real content pulled from the matching YouTube episode. What's left
genuinely placeholder: all 9 Southeast Asia slots, all 6 Europe slots
(both regions have a source file in `knowledge-base/regional/` if you
want real copy pulled from the book later instead of writing it from
scratch), and all 7 Chilli Oil products (no episode content exists for
these at all — that's a separate brand product, not something the
YouTube series ever covered).
