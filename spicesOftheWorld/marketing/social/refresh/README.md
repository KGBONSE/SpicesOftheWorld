# Fudi People — social media refresh

Brand assets and copy for rebuilding the Fudi People Instagram, TikTok, Facebook and YouTube accounts (Sept 2026). The working checklist with final bios, descriptions, captions and progress is in [CHECKLIST.md](CHECKLIST.md).

## Brand look

- Colours: dark brown `#3A1408` / `#5A1A0C`, burnt orange `#F0781E` / `#E8741C`, cream `#FFF3E2`, gold `#F4A53A`
- Type: Lora Bold (headlines), Poppins (body, labels)
- Story: farmer-founder in Sidcup, London; grows and smokes his own chillies; chilli oil with spices of Africa, South Asia and East Asia; vegan
- Handle everywhere: `@fudi.people`; all links → fudipeople.com

## Assets

| Path | What | Size |
| --- | --- | --- |
| `assets/profile/fudi-profile-picture.jpg` | Profile picture for all platforms (bowl of chillies + Spices of Africa bottle) | 1080×1080 |
| `assets/profile/fudi-profile-africa-bottle.jpg` | Alternative profile picture (close crop of the Africa bottle) | 1080×1080 |
| `assets/youtube/fudi-youtube-banner.jpg` | YouTube banner; text + photo inside the 1546×423 mobile safe area | 2560×1440 |
| `assets/posts/post0…post6*.jpg` | Seven feed posts for Instagram/Facebook (order + captions in CHECKLIST.md) | 1080×1350 |
| `assets/video/fudi-smoker-reel.mp4` | 20 s vertical Reel/TikTok/Short from the smoker clip, captioned, with end card | 1080×1920 |
| `assets/video/endcard.png` | End card used in the reel | 1080×1920 |
| `assets/labels/south-asia-peacock-bottle.png` | South Asia bottle with the peacock replacing the Buddha (Higgsfield AI edit — for social use; not print artwork) | 1744×2336 |
| `assets/label-concepts/` | Hand-drawn SVG emblem concepts (peacock variations, masala dabba, chilli rangoli, elephant) and comparison sheets; the chosen direction was the simple side-profile peacock generated in Higgsfield | — |

## Scripts

Python 3 + Pillow (+ cairosvg for the SVG concepts), ffmpeg for video. Fonts expected at `/usr/share/fonts/truetype/google-fonts/` (Lora, Poppins). Source photos are not in this repo; paths inside the scripts point at the original upload locations and need adjusting.

| Script | Produces |
| --- | --- |
| `scripts/youtube_banner.py <IMG_4946.JPG> [out]` | Current YouTube banner |
| `scripts/profile_and_banner_v1.py` | Profile picture (and the superseded v1 banner) |
| `scripts/three_oils_and_profile_alt.py` | Alternative Africa-bottle profile picture |
| `scripts/posts.py` | All seven feed posts |
| `scripts/smoker_reel.sh <smoker.mp4> <endcard.png> [out]` | The 20 s reel |
| `scripts/peacock_options.py`, `scripts/south_asia_options.py` | SVG label-emblem concepts |

## Open items

See the unticked items in CHECKLIST.md. Label print files need a designer (peacock artwork, and the misspelled "PEOPLE" on the South Asia and East Asia labels).
