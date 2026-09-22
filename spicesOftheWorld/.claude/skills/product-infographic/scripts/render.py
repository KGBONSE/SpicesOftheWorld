#!/usr/bin/env python3
"""
Render a self-contained HTML infographic to a crisp PNG.

Usage:
    python3 render.py <input.html> <output.png> [width] [height]

Defaults to 1080x1350 (a 4:5 portrait canvas that fits Instagram/Pinterest/
most "save and share" infographic feeds) at 2x device scale for crisp text.
The HTML file must size its root element to exactly <width>x<height> px
itself (see the SKILL.md template) — this script does not resize content,
it only captures a viewport at that exact size.
"""
import sys
import os

from playwright.sync_api import sync_playwright

def main():
    if len(sys.argv) < 3:
        print("Usage: render.py <input.html> <output.png> [width] [height]")
        sys.exit(1)

    input_path = os.path.abspath(sys.argv[1])
    output_path = os.path.abspath(sys.argv[2])
    width = int(sys.argv[3]) if len(sys.argv) > 3 else 1080
    height = int(sys.argv[4]) if len(sys.argv) > 4 else 1350

    if not os.path.isfile(input_path):
        print(f"Input HTML not found: {input_path}")
        sys.exit(1)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with sync_playwright() as p:
        # Relies on PLAYWRIGHT_BROWSERS_PATH (pre-set in this workspace) to find
        # the pre-installed Chromium — do not pass an explicit executable_path.
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=2)
        page.goto(f"file://{input_path}")
        page.wait_for_timeout(150)  # let web fonts settle
        page.screenshot(path=output_path, clip={"x": 0, "y": 0, "width": width, "height": height})
        browser.close()

    print(f"Saved: {output_path} ({width}x{height} @2x)")

if __name__ == "__main__":
    main()
