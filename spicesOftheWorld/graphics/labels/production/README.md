# Label production files — all 34 blends

Individual front-of-jar label files, cut from the approved design in
`../all-34-labels-proof-sheet.html` (which is a review proof sheet, not
production art). Same fixed template as `../yaji-label-west-africa.html`:
real Fudi People logo (cream bold silhouette), gold rule, headline, thin
gold trade-route line, region tag, micro copy — only the field colour and
the two copy lines (blend name + dish tie-in) change per blend.

## What's here, per blend

| File | What it is |
|---|---|
| `epNN-<slug>.html` | The source. Canvas-agnostic — all interior sizing is in `vmin`, so one file renders correctly at any square size. |
| `epNN-<slug>-digital-1200.png` | 1200 × 1200px product image, transparent corners (round die-cut look). Use for the website / WooCommerce. |
| `epNN-<slug>-print-95mm-300dpi.png` | 1122 × 1122px = 95mm round @ 300dpi, transparent background. Print-ready resolution (Yaji's older `.png` pair was 359px / 96dpi — re-render from HTML if a true-300dpi Yaji is needed). |

`_index.html` — contact sheet of all 34 digital renders, grouped by region.

## Re-rendering

Headless Edge, one line per size (fonts come from Adobe Typekit, so the
machine needs to be online):

```
"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe" \
  --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
  --default-background-color=00000000 --virtual-time-budget=5000 \
  --window-size=1200,1200 \
  --screenshot="epNN-<slug>-digital-1200.png" \
  "file:///.../production/epNN-<slug>.html"
```

Change `--window-size` to `1122,1122` for the print file. Any other square
size works too — the layout scales.

## Not done here (deliberately)

- **Back-of-jar labels** — ingredients, allergens (Natasha's Law), net
  weight in full, barcode, best-before. Deferred; front-of-jar only.
- **Net weight** — every label reads `NET WT 50g`, matching the Yaji
  label. Placeholder until the packaging-size decision in
  `../../../docs/product-catalog-notes.md` is made.
- **Bleed / crop marks** — the PNGs are the finished circle only. Add
  bleed at the printer's spec when a print run is booked.
- **Region palette / copy sign-off** — pulled straight from the proof
  sheet, which pulled them from each episode script's own `## 5. The
  Blend` / `## 6. The Dish` text. No per-continent approval pass has
  happened since.
