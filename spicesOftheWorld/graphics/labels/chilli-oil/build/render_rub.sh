#!/bin/bash
# Regenerate the three Chilli Oil Rub labels (web + print PNG) and their jar mockups.
# Same requirements as render_all.sh (python3, headless Edge/Chrome, network for fonts).
set -e
cd "$(dirname "$0")"
OUT="$(cd .. && (cygpath -m "$(pwd)" 2>/dev/null || pwd))"
EDGE="/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
[ -x "$EDGE" ] || { echo "Edge not found — set EDGE manually."; exit 1; }

shot() { # html-basename  png-basename  scale  w  h
  "$EDGE" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor="$3" \
    --default-background-color=00000000 --virtual-time-budget=9000 --window-size="$4","$5" \
    --screenshot="$OUT/$2" "file:///$OUT/$1" 2>&1 | grep -iE 'fail' | grep -vi task_manager || true
  echo "  $2"
}

python build_rub.py labels
for r in africa southasia eastasia; do
  shot "${r}-rub-label.html" "${r}-rub-label.png"            1.4 1000 1230
  shot "${r}-rub-label.html" "${r}-rub-label-print-2600.png" 2.6 1000 1230
done
python build_rub.py jars
for r in africa southasia eastasia; do
  shot "${r}-rub-jar.html" "${r}-rub-jar-mockup.png" 1 1200 1200
done
echo "done -> $OUT"
