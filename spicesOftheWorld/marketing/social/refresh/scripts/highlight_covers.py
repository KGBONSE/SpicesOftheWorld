"""Instagram highlight covers (Farm, Smoking, Chilli Oil, Recipes, Wholesale).

Each cover is a 1080x1920 PNG: a cream line icon on burnt orange, centred in
the circle Instagram crops highlights to. The icons are hand-written SVG,
rendered with a headless Edge/Chrome screenshot (no Pillow/cairo needed).

Usage: python highlight_covers.py [out_dir]
"""
import os, subprocess, sys, tempfile, pathlib

BG, INK, RING = "#E8741C", "#FFF3E2", "#F4A53A"

# 24x24 line icons (stroke only, round caps).
ICONS = {
    "farm": '<path d="M7 21h10"/><path d="M12 21V11"/>'
            '<path d="M12 13C7.5 13 5 10 5 6c4.5 0 7 2.5 7 7z"/>'
            '<path d="M12 11c0-4 2.5-7 7-7 0 4-2.5 7-7 7z"/>',
    "smoking": '<path d="M12 22c-4.2 0-7-3-7-6.6 0-3.8 2.8-5.8 3.8-9.4 1.6 1.8 2.2 3.4 2.2 5 1.4-1.4 2-3.8 1.4-8 4 2.8 6.6 7 6.6 12.4 0 3.6-2.8 6.6-7 6.6z"/>'
               '<path d="M12 22c-1.8 0-3-1.3-3-2.9 0-1.8 1.4-2.7 2-4.6 1.6 1.4 4 2.6 4 4.8 0 1.6-1.2 2.7-3 2.7z"/>',
    "chilli-oil": '<path d="M15.5 7.5c-1.8-.4-3.4 1-4 3.6-.8 3.6-3 6.6-7 8.4 5.4.9 11.2-1.8 12.8-7.6.6-2.3 0-4-1.8-4.4z"/>'
                  '<path d="M13 8.3c.9-1.6 3.4-1.9 4.6-.4"/><path d="M15.4 7.4c-.1-1.9.6-3.5 2.6-4.4"/>',
    "recipes": '<path d="M3 11h18c0 5-4 9-9 9s-9-4-9-9z"/><path d="M9 20v1.5h6V20"/>'
               '<path d="M8 3c0 1.5 1.5 1.5 1.5 3S8 7.5 8 9"/><path d="M12 3c0 1.5 1.5 1.5 1.5 3S12 7.5 12 9"/>'
               '<path d="M16 3c0 1.5 1.5 1.5 1.5 3S16 7.5 16 9"/>',
    "wholesale": '<path d="M3 7.5 12 3l9 4.5v9L12 21l-9-4.5z"/><path d="M3 7.5 12 12l9-4.5"/><path d="M12 12v9"/>'
                 '<path d="M7.5 5.3 16.5 9.8"/>',
}

PAGE = """<!doctype html><html><head><meta charset="utf-8"><style>
html,body{{margin:0;width:1080px;height:1920px;background:{bg};overflow:hidden}}
.c{{position:absolute;left:50%;top:50%;width:720px;height:720px;margin:-360px 0 0 -360px;
border-radius:50%;border:10px solid {ring};box-sizing:border-box;display:flex;align-items:center;justify-content:center}}
svg{{width:400px;height:400px}}
</style></head><body><div class="c">
<svg viewBox="0 0 24 24" fill="none" stroke="{ink}" stroke-width="1.35" stroke-linecap="round" stroke-linejoin="round">{icon}</svg>
</div></body></html>"""

BROWSERS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "/usr/bin/google-chrome", "/usr/bin/chromium",
]


def main():
    out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).parent.parent / "assets" / "highlights")
    out.mkdir(parents=True, exist_ok=True)
    browser = next(b for b in BROWSERS if os.path.exists(b))
    tmp = pathlib.Path(tempfile.mkdtemp())
    for name, icon in ICONS.items():
        html = tmp / f"{name}.html"
        html.write_text(PAGE.format(bg=BG, ink=INK, ring=RING, icon=icon), encoding="utf-8")
        png = out / f"highlight-{name}.png"
        subprocess.run([browser, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        "--window-size=1080,1920", f"--screenshot={png}", html.as_uri()],
                       check=True, capture_output=True)
        print(png)


if __name__ == "__main__":
    main()
