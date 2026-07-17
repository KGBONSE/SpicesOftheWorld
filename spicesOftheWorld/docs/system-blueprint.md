# FUDI PEOPLE — AI CONTENT TEAM — SYSTEM BLUEPRINT

*Spices of the world, through an African lens — from Mokola Market, Accra
to the chilli & okra farm in London. A multi-agent research, writing,
design & publishing system.*

---

## Before We Begin — 3 Honest Caveats

| # | Caveat | What it means for you |
|---|---|---|
| 1 | I could not watch your videos | YouTube blocks automated scraping of video lists/transcripts. To capture your real voice, you'll manually pull 5–10 transcripts from YouTube Studio and hand them to the Knowledge Agent. |
| 2 | This system can't run itself from inside a chat | Daily automation needs a scheduler running outside our conversation — that's the role of n8n (self-hosted, free) below. |
| 3 | This is a big build | It's broken into 4 phases so you're not standing up all six agents on day one. |

---
Am 
## 1. The System at a Glance

One team, six specialist agents, one orchestrator, and you as the final approver before anything goes public.

| Layer | Role |
|---|---|
| Orchestrator (n8n) | Runs the whole pipeline daily — trigger, schedule, glue between agents |
| Agent 1 — Trends & Outlier Scout | Finds outlier videos on YouTube / IG / X in your niche |
| Agent 2 — Knowledge & Voice | Holds the Science of Spices book + your personal voice profile |
| Agent 3 — Script Writer | Produces the "as-is" version and the "Fudi People" remix |
| Agent 4 — Thumbnail Designer | Recreates winning thumbnail layouts in your brand style |
| Agent 5 — Editing (Phase 2) | Rough-cuts, captions, splices in your Mokola Market clip |
| Agent 6 — Publishing | Uploads privately, waits for your approval, then goes live |

---

## 1.5 Your Episode Content Framework (Every Video Follows This)

This is the backbone every Script Writer output must follow, per spice/region.
It's factual and citation-based — you're scripting a video, not writing an
essay, so citations stay short and spoken (e.g. "according to Dr Farrimond's
Science of Spices...").

| # | Segment | What goes here | On-camera citation style |
|---|---|---|---|
| 1 | Geographic origin | Where the spice originates, and where it's grown/traded today | "Farrimond traces this to..." / name the modern-day producing regions directly |
| 2 | Trade & migration history | How it spread — colonial routes, diaspora links, historic trade corridors | Name the route/era on camera (e.g. "the Indian Ocean spice route") |
| 3 | The science | Flavour chemistry — the compounds behind the aroma/heat/taste | "The science behind that heat is..." — one clear mechanism, not a lecture |
| 4 | Typical blend / ratios | The classic spice blend and ratios used in that region | Show the ratio on screen as text/graphic while you speak |
| 5 | Classic dish + home recipe | One dish that showcases it, simplified for a home cook | Your own recipe card — no citation needed, this is your content |
| 6 | The Africa link | Direct historical link back to Africa, or the shared trade route | This is your signature beat — ties every region back to your own story |

**Citation rule for the Script Writer agent:** every historical or scientific
claim pulled from the Farrimond book gets a short spoken attribution, and the
underlying page/chapter reference is kept in your private notes (not read
aloud) in case anyone asks for a source.

### Your Named Influences — What Each One Teaches the System

| Creator / Video | Signature format | What Fudi People borrows |
|---|---|---|
| Atlas Pro — *The Geography of Spices and Herbs* | Map-led, geography-first storytelling; explains why a spice grows where it grows before touching flavour | The "geography first" opening beat — visually anchors segment 1 of your framework |
| Ethan Chlebowski — *Beginner's Guide to Cooking with Spices* | Calm, analytical "why this works" structure; opens with a clear question, then builds up the reasoning step by step | The science segment (3) — his question-then-explain rhythm is the model for your flavour-chemistry beats |
| Brian Lagerstrom — *The Only 10 Spices You Need* | Practical, ruthless editing down to "what you actually need" — high information density, no filler | The blend/ratio segment (4) — tight, confident delivery of the practical takeaway |

The Outlier Scout agent treats these three as your core "influencer benchmark
set" — their videos are the first comparison point whenever it scores a new
outlier in your niche.

---

## 2. Agent-by-Agent Breakdown

### Agent 1 — Trends & Outlier Scout

Scans YouTube, Instagram and X daily for trending topics, then flags outlier
videos — favouring small/mid creators whose specific video is overperforming
their own average, not giant channels.

| Field | Detail |
|---|---|
| Core formula | outlier score = video views ÷ that channel's average views. A score of 3x–10x+ is a genuine outlier. |
| Secondary signal | VPH (views per hour) — flags what's trending right now, not just historically |
| YouTube tool | YouTube Data API v3 — free, 10,000 quota units/day |
| Automation | Ready-made open-source n8n workflow templates already do this exact channel-average-vs-new-video comparison |
| Instagram / X | No reliable free official "trending" API. Realistic options: Apify free tier (limited monthly runs) or targeted web searches for weekly trend recaps |
| Output | Intro transcript (first ~30 sec), title, thumbnail image, and outlier score per video — row 1 of the daily sheet |

**Reliability note:** the YouTube half of this agent will be strong and free.
The Instagram/X half will be the weakest link and may need your manual
eyeballing at first.

### Agent 2 — Knowledge & Brand Voice

Two jobs in one: hold the factual spice science from Dr Stuart Farrimond's
book, and hold your personal story so every script sounds like you.

| Field | Detail |
|---|---|
| How to upload the book (step-by-step) | 1) Take clear photos or a scan of each page you want to use, or export the ebook to PDF. 2) Upload the PDF/photos to Claude Code or this chat. 3) Ask for OCR + text extraction (free, built-in) if it's image-based. 4) Split the extracted text into one file per region: Africa, Middle East, South Asia, SE Asia, East Asia, Americas, Europe. |
| Storage | Free open-source local vector store (e.g. Chroma or SQLite) so any agent can search "black pepper history" instantly |
| Citation rule | Every historical/scientific claim sourced from the book gets a short spoken on-camera attribution ("according to Dr Farrimond..."); full page/chapter reference is kept in your private notes, not read aloud |
| Copyright guardrail | Book content is background research only — the Script Writer always paraphrases in your voice, never quotes passages directly |
| Voice profile | Built from 5–10 of your existing transcripts (pulled free from YouTube Studio captions) + a short written memo from you about your mum and Mokola Market |

### Agent 3 — Script Writer

Takes an outlier topic + the knowledge base + your voice profile and produces
two versions every time.

| Field | Detail |
|---|---|
| Version A — "As-is" | Matches the outlier video's intro formula/pacing/structure closely (not word-for-word — the format) |
| Version B — "Fudi People" | Same proven structure, rewritten in your voice: Ghana → Mokola Market → the farm → the spice science → the recipe payoff |
| Intro template | ~10 seconds: state what the video covers + the payoff (e.g. "the perfect spice blend and recipe you'll walk away with") |

### Agent 4 — Thumbnail Designer

Its own dedicated department, exactly as requested — reproduces a winning
thumbnail's composition, restyled in your brand colours with your own photo.

| Field | Detail |
|---|---|
| Brand colours | Light orange, white, small amount of black |
| Input needed from you | A small library of your own photos to draw from |
| $0 starting option | Google AI Studio free tier (Nano Banana / Nano Banana Pro access without a paid API key) — prototype your thumbnail style at no cost |
| $0 open-source option | ComfyUI + FLUX.2, self-hosted — runs on your own machine if it has a GPU, otherwise skip this until you're ready to spend |
| Paid option — later, optional only | Nano Banana Pro via the Gemini API — only worth considering once you're posting daily and the channel is earning; not needed to start |

You do not need to spend anything to start the Thumbnail agent. Stay on the
free Google AI Studio tier until the channel is generating revenue.

### Agent 5 — Editing (Phase 2, not day one)

The most technically demanding piece, and the one where free "AI edits my
video creatively" tools are least mature.

| Field | Detail |
|---|---|
| Transcription | Whisper (OpenAI, open source) — free, local, transcribes your raw footage |
| Cutting / splicing | FFmpeg (free, open source) — cuts, crops, burns in captions, auto-inserts your Mokola Market clip into every intro |
| Realistic expectation | Auto-captioning and rough-cut assembly are realistic to automate now. True creative AI editing is not reliably free yet — budget for this being semi-manual for 6–12 months |

### Agent 6 — Publishing

Uploads to YouTube but always stops for your explicit approval before
anything goes public.

| Field | Detail |
|---|---|
| Upload method | YouTube Data API v3 (free) |
| Approval gate | Uploads as Private/Unlisted, sends you the link via email or Telegram, only flips to Public after you reply "approved" |

---

## 3. The Two "Above and Beyond" Extras

| Extra | How it's delivered |
|---|---|
| Excel / Sheet delivery | Every agent writes to a shared Google Sheet in your requested two-column format: "What the creator did" vs. "Fudi People remix" |
| Daily email to fudipeople@gmail.com | n8n's free Gmail node sends a daily summary of outlier finds + a link to the sheet — roughly a 10-minute build |

---

## 4. Orchestration Layer — Why n8n

n8n is the recommended glue between everything, for four reasons:

- Genuinely free and open source when self-hosted (a $5–7/month VPS is enough)
- Ready-made community templates already exist for YouTube outlier detection — you're not starting from a blank canvas
- Acts as the daily scheduler that calls the Claude API as one step inside a workflow
- Native connectors for Gmail, Google Sheets, and YouTube, plus custom scripts for outlier maths and thumbnail generation

**Division of labour:** Claude Code is the workshop where you build and
version the actual agent skills (prompt templates + logic). n8n is the
factory conveyor belt that triggers those skills on schedule.

---

## 5. Cost Breakdown — $0 to Start

Every tool below can run at $0. Nothing on this list requires payment to get
the system working end to end.

### Free, no time limit

| Item | Cost |
|---|---|
| YouTube Data API v3 | Free |
| Google Sheets + Gmail | Free |
| Google AI Studio (thumbnail prototyping) | Free |
| Whisper + FFmpeg (editing, local compute) | Free |
| ComfyUI + FLUX.2 (if you have a GPU) | Free |
| n8n self-hosted on your own machine | Free (only becomes ~$5–7/month if/when you move it to a cloud VPS for 24/7 uptime) |

### The one real cost, and it scales with use

| Item | Cost |
|---|---|
| Claude API usage (scripts, research calls) | Pay-as-you-go — can be kept very low by running the system on-demand rather than continuously while you're starting out |

### Optional upgrades — only once the channel is earning

| Item | Cost |
|---|---|
| n8n hosted on a cloud VPS (24/7 automation) | ~$5–7 / month |
| Nano Banana Pro API (higher thumbnail consistency) | Pay-per-image, ~$10–20 / month at daily use |
| Apify (IG/X scraping beyond the free tier) | ~$5–15 / month |

**Bottom line:** you can build and run the entire system for $0 upfront. The
only line item you'll actually watch is Claude API usage, and even that
stays small if you run things on-demand rather than 24/7 while you're
finding your format.

---

## 6. Suggested Build Order

| Phase | Timeline | What you build |
|---|---|---|
| 1 — Foundation | Week 1–2 | YouTube API key + Google Sheet set up; pull 5–10 of your own transcripts; write your voice memo; get the Science of Spices book into text form |
| 2 — Research + Writing | Week 2–3 | Build the Outlier Scout (manual/on-demand first); build the Script Writer using your voice profile + book knowledge; test on 3–5 topics |
| 3 — Visual + Automation | Week 3–4 | Build the Thumbnail agent on the free tier; wire Agents 1, 3, 4 into an n8n daily workflow → Sheet → email |
| 4 — Editing + Publishing | Month 2+ | Add Whisper/FFmpeg rough-cuts + Mokola Market splice; add the Publishing agent with private-upload-then-approve; only then build a Shorts repurposing agent |

---

## 7. What I Need From You to Start Building

| # | Item | Purpose |
|---|---|---|
| 1 | 5–10 transcripts from your existing videos | Trains the voice profile (pull from YouTube Studio captions, free) |
| 2 | A short written voice memo | Your own words on Mokola Market, your mum, and the farm |
| 3 | Science of Spices content (PDF/photos of pages) | Builds the knowledge base now rather than later |
| 4 | A handful of your own photos | Reference library for the Thumbnail agent |
| 5 | The Mokola Market clip(s) you want used | Confirmed footage for every video's intro |

Send any of these whenever you're ready, and the next step is building the
actual voice-profile document, the knowledge base structure, and a
first-draft script + thumbnail brief — so you can see the system working
before any automation gets wired up.
