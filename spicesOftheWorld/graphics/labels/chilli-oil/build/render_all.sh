#!/bin/bash
# Regenerate all three chilli-oil labels (web + print PNG) and their bottle mockups.
# Outputs land in the parent graphics/labels/chilli-oil/ directory.
#
# Requires: python3, and headless Chromium/Edge for the HTML->PNG step.
# Fonts (Google Fonts) load over the network, so the machine must be online.
set -e
cd "$(dirname "$0")"
OUT="$(cd .. && pwd)"

# --- find a headless browser -----------------------------------------------
EDGE=""
for c in \
  "/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe" \
  "/c/Program Files/Microsoft/Edge/Application/msedge.exe" \
  "$(command -v google-chrome || true)" \
  "$(command -v chromium || true)" \
  "$(command -v chromium-browser || true)"; do
  [ -n "$c" ] && [ -x "$c" ] && EDGE="$c" && break
done
[ -z "$EDGE" ] && { echo "No headless Chrome/Edge found — set EDGE manually."; exit 1; }

shot() { # html-basename  png-basename  scale  w  h
  "$EDGE" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor="$3" \
    --default-background-color=00000000 --virtual-time-budget=9000 --window-size="$4","$5" \
    --screenshot="$OUT/$2" "file:///$OUT/$1" 2>&1 | grep -iE 'fail' | grep -vi task_manager || true
  echo "  $2"
}

python3 build_africa.py
python3 build_southasia.py
python3 build_eastasia.py

for r in africa southasia eastasia; do
  shot "${r}-label.html" "${r}-label.png"              1.4 1000 1230
  shot "${r}-label.html" "${r}-label-print-2600.png"   2.6 1000 1230
done

for r in africa southasia eastasia; do
  python3 build_bottle.py "${r}-label.png" "${r}-bottle.html"
  shot "${r}-bottle.html" "${r}-bottle-mockup.png"     1   1200 1200
done
echo "done -> $OUT"
