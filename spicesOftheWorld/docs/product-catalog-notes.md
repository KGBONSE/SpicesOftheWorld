# Product Catalog — WooCommerce Import Notes

`woocommerce-product-import.csv` (same folder) contains all 34 spice
blends from the Season 1 scripts, formatted for WordPress's built-in
importer: **Products → All Products → Import**, upload the CSV, let it
auto-map columns (the headers match WooCommerce's own field names), run
the import. Every blend's ingredient list and use is taken directly from
`scripts/episode-01` through `episode-34` — nothing invented beyond what's
already scripted.

## Everything imports as a draft

Every row has `Published = 0` on purpose — nothing goes live automatically.
Before publishing each one, you still need to:
- Set a **Regular price** (left blank in the CSV)
- Add product **images**
- Decide on **packaging size** (the source recipes are cooking-batch
  quantities, e.g. "2 tbsp cumin," not retail jar weights)
- Confirm **allergen labelling** meets UK requirements (Natasha's Law) —
  the Description field flags known allergens per blend (peanuts, tree
  nuts, sesame, mustard, soy, dairy) based on the scripted ingredients,
  but you (or a food-safety advisor) should verify this against your
  actual supplier ingredients before anything ships to a customer. This
  is a legal requirement, not just a nice-to-have — I'm not a substitute
  for that check.

## Dry vs. wet — 20 sellable as dry blends, 14 need work first

**Dry, shelf-stable as scripted (20):** Yaji, Pilau Masala, Durban Curry
Masala, Jamaican Jerk Rub, Za'atar, Turkish Baharat, Arabic Baharat,
Advieh, Dukkah, Hawaij, Garam Masala, Timur ko Chhop, Chaat Masala, Panch
Phoran, Gunpowder/Podi (semi-moist — see note below), Shichimi-Togarashi,
Shandong Spice Bag, Nanjing Spice Bag, Five-Spice Powder, BBQ Rub, Mole
Mix (the packaged mix is dry; it's designed to be simmered into a wet
sauce at home, same as any dry curry-paste base).

**Wet — paste, marinade, sauce, or butter, needs a shelf-stable
substitute before it's really sellable as a pantry product (14):** Yassa
Marinade, Niter Kibbeh, Pepper Soup Spice, Harissa, Mbongo Mix, Zhug,
Taklia, Vindaloo Paste, Yangnyeomjang, Chilli Black Bean Sauce,
Chimichurri, Tucupí, Leche de Tigre.

Every wet item is still in the CSV (per your call to include everything),
tagged `Wet - Needs Adaptation` and flagged in its own Description with
what specifically makes it wet and what a dry substitute would need to
change. A few practical options worth considering, blend by blend:

- **Mbongo Mix / Pepper Soup Spice** — swap fresh garlic/onion (Mbongo)
  or the fresh chilli/garlic/ginger/onion base (Pepper Soup) for their
  dried/powdered equivalents. Closest to a straightforward dry
  conversion of the group.
- **Harissa, Zhug, Vindaloo Paste, Taklia, Chimichurri, Chilli Black Bean
  Sauce, Yangnyeomjang** — pastes, oil-based mixes, or sauces. These
  would need to be sold refrigerated/frozen with a real shelf-life test,
  not converted to a dry mix, without changing what they fundamentally
  are.
- **Niter Kibbeh** — a dairy product; refrigerated/frozen sale only, same
  category as any spiced butter or ghee product.
- **Yassa Marinade, Tucupí, Leche de Tigre** — built around fresh
  citrus/fermented liquid as the whole point of the product; these are
  the hardest to convert to shelf-stable without becoming a
  fundamentally different product (e.g. a "yassa seasoning" dry rub
  instead of the actual marinade).

None of these conversions have been recipe-tested — treat the wet/dry
split as a starting map for deciding what's worth developing first, not
a finished reformulation.

## Categories used

Top-level: **Africa**, **Middle East**, **South Asia**, **East Asia**,
**The Americas** — matching the 5 arcs in
`docs/spice-channel-framework.md`. Country/book-region and a Dry/Wet flag
are set as Tags instead, so you can filter or build collection pages
either way in WordPress.

## SKU scheme

`FP-<2-digit episode number>-<short code>`, e.g. `FP-01-YAJI`,
`FP-18-GARAM`. Matches the episode numbering in
`docs/spice-channel-framework.md` for easy cross-reference back to the
script and its `Africa Link / Throughline Close` for marketing copy later.
