# Fudi People — Brand (visual identity)

Single source of truth for colours, font and look. Tone of voice is in `docs/brand-voice.md`.
Updated 2026-10-14: one master palette and one font, replacing the per-surface mix.

## Vibe

**Warm, clean, bold.**

- Warm: cream grounds, orange and maroon, never cold greys or blues.
- Clean: lots of space, one accent per layout, short text.
- Bold: heavy Inter headlines, strong contrast, big type.

## Colours

| Role | Name | Hex | Use |
|---|---|---|---|
| Background | Cream | `#FBF3E7` | Page, card and thumbnail grounds |
| Text | Ink | `#3A1210` | Body text and headlines on cream |
| Accent | Marigold | `#E07610` | Buttons, highlights, key words, badges |

Supporting (use sparingly):

| Role | Name | Hex | Use |
|---|---|---|---|
| Dark background | Maroon | `#6B1B1F` | Dark sections and cards, text on it is cream |
| Text on dark | Cream | `#FDF3E4` | Text on maroon or ink |
| Secondary accent | Gold | `#E79A2E` | Sub-lines, hover states |

Rules:
- Light layouts: Cream background, Ink text, Marigold accent.
- Dark layouts: Maroon background, Cream text, Marigold or Gold accent.
- One accent colour per layout. Don't put Marigold and Gold side by side.
- Contrast: Ink on Cream and Cream on Maroon pass. Don't put Marigold text on Cream for body-size text (headlines and buttons only).

## Font

**Inter** everywhere (Google Fonts, free).

| Use | Weight |
|---|---|
| Headlines, logo text, buttons | 800 (ExtraBold) or 700 |
| Subheads, labels | 600 |
| Body, captions | 400 |

No second font. Use weight and size for hierarchy, not different typefaces.

## Logos (`brand-assets/logo/`)

`fudi-people-logo.png` / `.webp` (default), `-maroon`, `-cream-bold`, `-white-bold`, `-black-bold`. Cream version on Maroon or Ink, Maroon version on Cream.

## Other rules

- Always spell it **Makola Market**.
- Product labels: Cream and Gold stay constant; the label field colour still changes by region (Africa = maroon, Middle East = amber, South Asia = marigold, East Asia = ink, Americas = terracotta).

## Not yet updated to match (needs doing)

These still use the older mixed palette and fonts. Update them when you want consistency:

- Website (Elementor): Fredoka/Karla/Caveat should become Inter; palette already matches. Guide: `docs/homepage-elementor-build-guide.md`.
- Video overlays: `video/episode-01/make_overlays.py` now uses these colours and Inter (done 2026-10-14). It needs `Inter-Variable.ttf` in its `fonts/` folder, and the Ep 1 overlays have not been re-rendered yet.
- Product labels: `graphics/labels/` use Source Serif 4/Source Sans 3 and gold `#C99A4A`.
- Thumbnail brief in `docs/system-blueprint.md` says "light orange, white, a little black".
