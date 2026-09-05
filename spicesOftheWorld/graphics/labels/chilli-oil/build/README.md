# chilli-oil label build scripts

Regenerate the three chilli-oil labels and their bottle mockups from the
committed brand assets. The `.html`/`.png` outputs in the parent folder are
what these produce — edit the scripts here, not the generated HTML.

## Files

| Script | Produces (in `../`) |
|---|---|
| `build_africa.py` | `africa-label.html` — heart/rooster emblem, kente side-borders |
| `build_southasia.py` | `southasia-label.html` — seated Buddha, ghost-face bg, `मिर्च का तेल` |
| `build_eastasia.py` | `eastasia-label.html` — coiled dragon, cloud pattern, `辣油` |
| `build_bottle.py <label.png> <out.html>` | a clear-glass 150 ml bottle mockup wrapping the given flat label PNG |
| `render_all.sh` | runs all of the above + renders every PNG (web 1400px, print 2600px, bottle 1200px) |
| `_assets.py` | shared helper — base64-encodes the committed logo / emblem SVGs for inlining |

## Inputs (all committed, not regenerated here)

- `../fudi-heart-emblem.svg`, `../fudi-buddha-emblem.svg`, `../fudi-dragon-emblem.svg`
  — the emblems, vectorised (with `vtracer`) from Kofi's concept art. The
  dragon is deliberately one flat tone; see `../README.md`.
- `../../../brand-assets/logo/fudi-people-logo-black-bold.png` (Africa) and
  `fudi-people-logo-maroon.png` (East / South Asia).

## Running

```
cd graphics/labels/chilli-oil/build
python3 build_africa.py        # just the HTML
bash render_all.sh             # HTML + all PNGs
```

`render_all.sh` needs a headless Chromium/Edge (it looks for common paths;
override `EDGE=` if needed) and network access — the labels pull fonts from
Google Fonts (Kaushan Script, Sacramento, Tiro Devanagari Hindi, Ma Shan Zheng).

## Not included

The one-off WooCommerce/WordPress API scripts used to push these live
(`upload_jar_labels.py`, `rollout.py`) are **not committed** — they carry
API keys / an app password inline. Their logic and the episode→product-id
mapping are written up in `docs/open-tasks.md`.
