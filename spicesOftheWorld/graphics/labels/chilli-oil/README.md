# Fudi People Chilli Oil — front-of-bottle labels

Three chilli-oil labels, rebuilt from the AI-generated concept artwork Kofi
supplied (2026-09-03/04). Each keeps the concept's look — orange field,
maroon frame, region emblem, script "Chilli Oil", native-script line — but
is re-authored as clean HTML/CSS with the real Fudi People logo and
razor-sharp vector emblems.

| Region | Emblem | Native-script line | Product (WooCommerce) |
|---|---|---|---|
| Africa | heart / rooster (Adinkra-style) | — (kente borders instead) | `SOTW-AFR-CHILLIOIL` (id 2226) |
| East Asia | coiled dragon | 辣油 (là yóu — "chilli oil") | `SOTW-EAS-CHILLIOIL` (id 2241) |
| South Asia | seated Buddha | मिर्च का तेल (mirch ka tel — "chilli oil") | `SOTW-SAS-CHILLIOIL` (id 2250) |

The concept's South Asia line read "(là jiāo yóu)" — that is romanised
**Mandarin**, not an Indian language. Replaced with Hindi Devanagari per
Kofi's call. The marketing tagline ("Authentic East Asian Flavor" / "True
Flavor of South Asia") was dropped.

## Files per region

| File | What |
|---|---|
| `<region>-label.html` | Source. Fixed 1000×1230 canvas, fonts from Google Fonts (needs network to render), logo + emblem embedded as base64. |
| `<region>-label.png` | 1400×1722 — web / product-listing use. |
| `<region>-label-print-2600.png` | 2600×3198 — print-res proof (~1000 dpi at a 65 mm label). |
| `<region>-bottle-mockup.png` | 1200×1200 — label on a clear-glass 150 ml bottle, cork cap. Used as the WooCommerce product image. |

Shared emblem assets (vectorised with vtracer from the concept art):
`fudi-heart-emblem.svg`, `fudi-dragon-emblem.svg`, `fudi-buddha-emblem.svg`.
Maroon logo: `../../../brand-assets/logo/fudi-people-logo-maroon.png`.

## Re-rendering

Headless Edge, one line per output (see `../production/README.md` for the
pattern). The build scripts that generate the HTML live in the chat
scratchpad for this session — the committed `.html` files are the rendered
output and can be edited directly.

```
"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe" \
  --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1.4 \
  --default-background-color=00000000 --virtual-time-budget=9000 \
  --window-size=1000,1230 --screenshot="africa-label.png" \
  "file:///.../africa-label.html"
```

## Known limitations / not done

- **East Asia dragon** is flattened to a single cream tone. The concept
  art's dragon is fine white-and-gold filigree at ~95 px in the file
  supplied — too low-res to vectorise the two-tone detail. The heart and
  Buddha are bolder shapes and kept full fidelity. Replace with a
  higher-res dragon file if the gold detail is wanted.
- **Bottle mockups are illustrative** (CSS/SVG), not photography. Bottle
  sourcing is still open (`docs/business-plan.md` §3.3).
- **Price / size**: labels read `150 ml`; the products are priced £8.99.
  No back-of-bottle label (ingredients, allergens, best-before, barcode)
  — front only, same as the spice-jar label system.
- Chilli oil is `150 ml`; the spice jars are a separate `NET WT 50g`
  packaging decision (`docs/product-catalog-notes.md`).
