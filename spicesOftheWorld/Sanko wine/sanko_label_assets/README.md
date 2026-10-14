# SANKO label assets (final)

- final_print_cmyk/  – print-ready: true CMYK, crop marks, 3mm bleed (combined + one PDF per flavor)
- assets/            – backgrounds, engraved Higgsfield mountain (alpha mask + per-flavor tinted), crossed hammer/tool + grape emblem
- src/               – build scripts (paths are relative; run `python3 src/compose_final.py`, outputs to ./out)

Back-label producer: FUDI PEOPLE. Lot No. line removed.
CMYK conversion: Ghostscript device conversion (no ICC profile) – proof with your printer's profile.
RGB previews regenerate with: python3 src/compose_final.py
