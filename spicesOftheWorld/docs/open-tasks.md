# Open Tasks

Most of the blueprint's Phase 1 gaps closed on 2026-07-15 when Kofi's
claude.ai chat exports (transcripts, voice profile, knowledge base, agent
system prompts, video, audio, photos) were located and imported into this
repo. What's left is genuinely short.

## Real remaining blockers

- [x] Install n8n locally (Docker) and add Anthropic + Google Drive
      credentials — see `workflows/n8n/local-install-steps.md`
- [x] Connect Google Drive with the `knowledge-base/` folder — uploaded as
      plain files to a Drive folder named "fudi people knowledge base"
      (2026-07-17)
- [x] Build Agent 2 in n8n and chain Agent 3 on top — turns out this was
      already ~90% built (2026-07-17 to 07-23, not reflected in this doc
      until now). Found and fixed 2026-07-25 via n8n's CLI
      (export/patch/re-import — no UI access needed):
      - Agent 2's knowledge-base retrieval tool was never actually
        connected to the AI Agent node — it would have answered from
        Claude's general knowledge, not your spice files
      - The Google Drive step only listed files, never downloaded their
        content — added a Download step so the Data Loader gets real text
      - Agent 3 had a stray leftover "ou are a helpful assistant" fragment
        tacked onto its system prompt, and a malformed date expression in
        its Google Sheets step — both fixed
      - **2026-07-25, found while testing:** Agent 2's AI Agent node had
        its prompt hardcoded to `{{ $json.topic }}`, but the Chat Trigger
        (used for manual testing) outputs `chatInput`, not `topic` — so
        typing into the chat panel hit "No prompt specified". Only worked
        by luck when called from Agent 3, which explicitly maps
        `chatInput` → `topic`. Fixed to `{{ $json.topic || $json.chatInput }}`
        so both paths work.
      - **2026-07-25, second round of testing:** after the prompt fix, the
        agent answered but said it could only see filenames, not real
        file content. Root cause found via n8n's execution DB
        (`database.sqlite`, `execution_data` table): the full indexing
        chain (Search files → Download → Vector Store insert) had never
        actually been run since the fixes went in — only the Manual
        Trigger node in isolation had been tested. What the agent was
        retrieving was **stale data from 2026-07-23**, left in memory
        from before any of these fixes, when the pipeline had the same
        "filename only, no real content" bug. In-memory store survives
        workflow edits, only wiped on a full n8n restart. Set
        `clearStore: true` on the Insert-mode Simple Vector Store node so
        the next full run replaces the stale index instead of adding to
        it.
      - **2026-07-25, third round:** the Google credential itself needed
        reconnecting (OAuth refresh token had expired — the Cloud project
        was still in "Testing" publishing status, which caps tokens at 7
        days; switched to "In production" to stop this recurring weekly).
        After reconnecting, the Download step failed with "Export only
        supports Docs Editors files" — decoded the real error from n8n's
        execution DB and found the cause: "Search files and folders"
        returns 60 items from the Drive folder, but 6 of them are actual
        **subfolders** (`spice-profiles`, `regional`, `recipes`,
        `compound-reference`, `superseded`, `by-flavour-compound-batch`),
        not files — the Download node chokes trying to export the first
        folder it hits as if it were a Google Doc. Good news found in the
        same check: all ~54 real files ARE direct children of the target
        folder already (no recursive subfolder traversal needed — good
        news given Drive's search API isn't recursive). Fixed by setting
        `filter.whatToSearch: "files"` on the search node, which excludes
        folders server-side via Drive's own query syntax.
      - **2026-07-25, fourth round:** with folders excluded, the Default
        Data Loader still failed — "Unsupported mime type:
        application/vnd.openxmlformats-officedocument.spreadsheetml.sheet".
        The loader only supports PDF/CSV/EPub/Docx/Text/JSON, not
        spreadsheets, and `compound-reference/spice-compound-pairing-reference.xlsx`
        is the one non-.md file in the knowledge base. Its data is already
        duplicated in prose/table form in `core-profiles-master.md`, so
        added a small Code node ("Keep markdown files only") between
        Search and Download that keeps only items ending in `.md` —
        simpler and more robust than trying to special-case one file's
        mime type.
      - **2026-07-25, confirmed working end to end:** index build (59
        real markdown files, verified via n8n's execution DB — actual
        file text, not filenames) and the chat test both succeeded. Agent
        2 is genuinely retrieving and voicing real knowledge-base content.
      - **2026-07-25, full Agent 3 chain confirmed working:** tested with
        "Grains of Paradise, Ghana episode" — produced a complete 7-section
        shooting script (two hook versions, on-voice throughout, proper
        B-ROLL/ON-SCREEN TEXT cues, correctly self-flagged 2
        `[NEEDS VERIFICATION]` items instead of inventing facts), and it
        logged correctly to the Google Sheet (Date/Topic/Text/Status all
        populated). The whole pipeline — Agent 2 retrieval → Agent 3
        script writing → Sheet logging — is genuinely working end to end.
      - **Minor scope note, not fixed:** Agent 2 itself returned an
        already-script-shaped response ("Here's the full Ghana episode
        script...") instead of sticking to research facts per its own
        system prompt — Agent 3 still built a proper final script on top,
        so it didn't hurt the result, but it means Agent 2 is doing (and
        costing) more than designed. Worth tightening Agent 2's prompt to
        stick to facts-only if token cost becomes a concern.
      - **Standing reminder:** the vector store is in-memory — wiped on
        every n8n restart. After any Docker restart, re-open Agent 2 and
        run the Manual Trigger's "Execute workflow" once before using
        either agent again.
- [x] Mix `audio/Mokola_voice_over_2.m4a` into
      `video/Fudi_People_Mokola_Market.mp4` (2026-07-25) —
      `video/Fudi_People_Mokola_Market_with_voiceover.mp4`: voiceover
      plays over the first 53s, original audio continues after (full
      2:15 length kept, not truncated to the voiceover's length). See
      `video/README.md`.
- [x] **2026-07-26:** swapped to different narration per Kofi's request
      after listening — a generic, spice-agnostic trim of Episode 1's
      "stall" Hook, so this intro can open any episode. Recorded by Kofi
      (`audio/Mokola_voice_over_generic.m4a`) and re-mixed into
      `video/Fudi_People_Mokola_Market_with_voiceover.mp4`. See
      `video/README.md` for the as-recorded transcript.
- [x] Pick an Episode 1 topic and draft a script — West Africa (Ghana +
      Nigeria), Yaji/suya: `scripts/episode-01-west-africa-yaji.md`. Only
      open item on it: test-cook the Yaji blend to lock in real ratios
- [x] Re-upload book photos for Clove's blending-science half (2026-07-25,
      book pp.84–85) — `core-profiles-master.md`'s Clove entry is now
      complete (blending science, food partners, blends to try, releasing
      the flavour). At most 1 of ~52 spices may still be incomplete — see
      `knowledge-base/README.md`.
- [x] Farm-work-clothes solo shot of Kofi — added 2026-07-24,
      `thumbnails/reference-photos/kofi-solo-potting-seedlings-home-garden.jpg`
      (pulled from raw video `MVI_0135.MP4`, home garden not the Sidcup farm)
- [x] Market thumbnail photo — decided 2026-07-24 not to pursue; too long
      since the Mokola Market visit for a real photo. Market stays a
      spoken/narrated element via `audio/Mokola_voice_over_2.m4a` instead of
      a thumbnail source.
- [x] Transcribe the 6 raw voice memos in `audio/raw-voice-memos/`
      (2026-07-26, via locally-installed `faster-whisper` — `openai-whisper`
      failed to install due to a Windows path-length limit on one of
      PyTorch's license files, so switched to the lighter dependency-free
      alternative). Raw transcripts in `docs/voice-recording-transcripts.md`
      (Transcripts C–H). These turned out to be a different kind of
      recording from the first two (live present-tense farm vlogs, not
      reflective narration) — documented as a separate "Farm vlog
      register" in `docs/brand-voice.md` rather than merged into the
      core signatures, since merging them would have blurred two
      genuinely different registers together.
- [ ] Locate/re-source raw Mokola Market video clips if the compiled video
      in `video/` ever needs rebuilding (source contact: Ghana-based)
- [x] Process the 7 raw seed-to-harvest video clips from `myprojectphotos/`
      (2026-07-25) — pulled 5 more thumbnail stills and cut/normalised 7
      B-roll segments into `video/`, see `thumbnails/index.md` and
      `video/README.md`. Segments are unedited raw cuts, not compiled into
      a finished sequence — that's still open if wanted.
- [x] Process `PHOTO-2026-07-24-23-18-31.zip` (WhatsApp export, Downloads,
      2026-07-25) — 5 current-day stills copied in and a talking-to-camera
      video normalised into two clips, see `thumbnails/index.md` and
      `video/README.md`. **2026-07-26: Kofi listened to the presenter
      clip's narration and confirmed it's usable** — clear to use as a
      real intro.
- [x] Compile the 7 seed-to-harvest B-roll clips into a finished sequence
      (2026-07-27) — `video/Seed_To_Harvest_Sequence.mp4` (3:40), sowing
      through potting/watering through planting through harvest, same
      concat + fade pipeline. Still a full reference reel, not a locked
      edit — see `video/README.md`.
- [x] Retrofit Health Benefits into all 9 episode scripts (2026-07-27) —
      the 2026-07-21 Health Benefits work only ever landed in
      `knowledge-base/spice-profiles/`, never in the actual scripts in
      `scripts/`. Added a short researched line + on-screen text into each
      episode's existing Science section (not a new beat — kept the
      6-beat template intact), sourced from each episode's own featured
      spice's profile. Two gaps surfaced and are flagged in the relevant
      scripts rather than guessed at: calabash nutmeg (Episodes 4 & 7) and
      allspice (Episode 9) have no written profile/Health Benefits section
      in the knowledge base at all — worth writing those if either spice
      gets featured again.
- [x] Draft Episode 9 — Caribbean, opening Arc 3 (2026-07-27) —
      `scripts/episode-09-caribbean-jerk.md`, allspice/jerk, picks up
      Episode 7's calabash-nutmeg/slave-trade thread directly. Open items:
      personal hook and one marinade trial (the rub's own ratios are
      already locked from the source, unusually). Flagged a small
      continuity mismatch with Episode 8's closing text — see that
      script's Status section.
- [x] Draft Personal Hooks for Episodes 4–8 (2026-07-28) — Sierra
      Leone/Liberia, Maghreb, East Africa, Central Africa, Southern
      Africa all had `[NEEDS KOFI]` placeholders; each now has a `[DRAFT]`
      hook built on that episode's own suggested direction (a tin of uda,
      a harissa jar, two shelf jars, two spice bags, a table of seven
      blends), echoed in each episode's Africa Link close per the locked
      Episode 1 style. Every specific detail is invented as a starting
      point, not a real Kofi memory — open item on all five is swapping
      in the real detail before locking. Done in parallel while Kofi was
      out filming Episode 1.
- [x] Draft Episode 10 — North India, continuing Arc 3 (2026-07-28) —
      `scripts/episode-10-north-india-garam-masala.md`, garam masala plus
      the "curry powder" colonial-flattening history. Directly pays off
      two threads planted earlier: Episode 6's "two jars on the shelf"
      setup, and Episode 1's Malabar-coast pepper (the "real" black
      pepper that displaced grains of paradise). Open items: personal
      hook and a source-check on the curry-powder history claim (general
      knowledge, not from the book).
- [x] Correct South Asia's scope to match the Africa arc's own rule
      (2026-07-28) — Episode 10 was first drafted as a single compressed
      "South Asia" episode, which broke the "one episode per book region"
      pattern all 8 Africa episodes followed. Renamed/rescoped as the
      first of a 6-episode South Asia sub-arc (Episodes 10–15: North
      India, Himalayan Belt, Central India, East India & Bangladesh, West
      India, South India & Sri Lanka), matching
      `south-asia-spice-notes.md`'s own structure. East Asia and Middle
      East now Episodes 16–17. See `docs/spice-channel-framework.md`.
- [x] Draft Episodes 11–15, completing the South Asia sub-arc (2026-07-28)
      — Himalayan Belt (timur, pays off Episode 3's fenugreek "three
      continents" promise), Central India (chaat masala), East India &
      Bangladesh (panch phoran + the real Masor Tenga fish curry recipe),
      West India (vindaloo paste + the real Goan Vindaloo recipe, Goa's
      Portuguese-dish backstory), and South India & Sri Lanka (gunpowder,
      closes the sub-arc and hands off to East Asia via the star-anise
      thread). All 6 South Asia episodes now drafted, one per book
      region, matching the Africa arc's own rule. Every episode's Personal
      Hook is a `[DRAFT]` placeholder — same open item as Episodes 4–8.
      Done in parallel while Kofi was out filming Episode 1.
- [x] Renumber South Asia (10–15 → 18–23) and draft the Middle East
      sub-arc in its proper place (2026-07-28) — found that both the
      Middle East and South Asia knowledge-base files' own
      cross-references confirm Middle East was meant to come first
      (cardamom/turmeric/fenugreek → Iraq → South Asia;
      saffron/cassia/Sichuan pepper → Turkey/Iraq/Iran → East Asia).
      Renamed all 6 South Asia episode files and internal cross-references
      to Episodes 18–23. Drafted the full 8-episode Middle East sub-arc
      as Episodes 10–17 (Syria, Turkey, Israel, Lebanon, Iraq, Iran,
      Egypt, Arabian Peninsula) — za'atar, Turkish baharat, zhug, taklia,
      Arabic baharat, advieh, dukkah, hawaij, each with exact quantities
      from the source. East Asia (6 sub-regions, not yet drafted) is now
      Episodes 24–29. Every Middle East episode's Personal Hook is also a
      `[DRAFT]` placeholder. See `docs/spice-channel-framework.md` for the
      corrected full roadmap.
- [x] Fix the Caribbean's place in the roadmap (2026-07-29) — Episode 9 was
      framed as its own top-level arc ("Arc 3 — Beyond Africa"), peer to
      the continents, but `americas-spice-notes.md` treats it as region 1
      of 6 within one "The Americas" book chapter. Relabelled as the first
      episode of an Americas sub-arc (same one-episode-per-book-region rule
      as Middle East/South Asia) and queued the other 5 regions — Mexico &
      Central America, the Andes, Amazon Basin, North America, Pacific
      South America — as Episodes 30–34, not yet drafted. Episode 9 keeps
      its number; nothing already drafted was renumbered. See
      `docs/spice-channel-framework.md`.
- [x] Draft Episodes 24–29, the full East Asia sub-arc (2026-07-29) —
      South Korea (yangnyeomjang), Japan (shichimi-togarashi), North China
      (Shandong spice bag), East China (Nanjing spice bag), South China
      (five-spice powder), West China (chilli black bean sauce/mapo tofu).
      Episode 24 opens the third and final Fudi People jar (Spices of East
      Asia), paying off Episode 6's "two/three jars" setup; Episode 29
      closes it and pays off the star anise/cassia/Sichuan pepper thread
      running since the Middle East sub-arc, via the Kashgar/Xinjiang Silk
      Road link `east-asia-spice-notes.md` flags directly. All 6 episodes
      have exact blend quantities straight from the source; each episode's
      Personal Hook is a `[DRAFT]` placeholder, same open item as the rest
      of the series. Only the Americas sub-arc's remaining 5 regions
      (Episodes 30–34) are left undrafted. See
      `docs/spice-channel-framework.md`.
- [x] Draft Episodes 30–34, the remaining Americas sub-arc, closing Season
      1 (2026-07-30) — Mexico & Central America (Mole Mix), the Andes
      (Chimichurri), Amazon Basin (Tucupí), North America (BBQ Rub), and
      Pacific South America (Leche de Tigre). Episode 34 closes both the
      6-episode Americas sub-arc (Episode 9 plus these 5) and the entire
      Season 1 roadmap — all 34 planned episodes across all 5 arcs are now
      drafted. It also lands, unplanned, on the Nikkei (Japanese-Peruvian)
      tradition the knowledge base's own Cross-continent links flag — a
      loop straight back to the East Asia sub-arc drafted immediately
      before it. All 5 episodes have exact blend quantities straight from
      the source; each Personal Hook is a `[DRAFT]` placeholder, same open
      item as every other episode. See `docs/spice-channel-framework.md`.

- [x] **2026-08-07:** Kofi flagged three fudipeople.com pages as untouched —
      How We Do It, Where to Buy, Contact Us. Drafted copy for all three in
      `docs/site-pages-how-where-contact.md`, using facts confirmed
      directly by Kofi (phone `+44 7952 983201`, `@fudipeople` on
      Instagram/TikTok/X/Facebook, whole-spice supplier kept unnamed per
      his call, website-only sales for now).

## 2026-08-01 to 2026-08-10 — homepage + site pages actually built in Elementor

Unlike the note above (written when there was no CMS access), Kofi later set
up a dedicated WordPress user (`claude-assistant`, Editor role) and shared
its Application Password, plus separate WooCommerce REST API keys — from
that point on, work happened directly in Elementor/WooCommerce via
screenshots + guided clicks (Elementor) and API scripting (WooCommerce),
not just drafted-copy handoff docs.

- [x] **Homepage rebuilt section by section**, following
      `docs/homepage-elementor-build-guide.md`: Hero (real headline/copy/
      button, photo gallery slider with real farm/family photos, not the
      demo product carousel), "Three Journeys, One Shelf" (3 live
      WooCommerce category tiles — Middle East tile built but hidden until
      that product line is ready), "How We Do It" 4-value block, two photo
      banners (real Chilli Oil product shot + farm photos, not stock),
      Order/Visit info block with real address/hours/phone and a working
      Google Maps link to the actual "fudi people" Business Profile,
      Testimonials placeholder (fake names replaced, real quotes still
      pending), Product Claims banner. Published live. Header/Footer
      remain locked behind Elementor Pro (not edited).
- [x] **How We Do It, Where to Buy, Contact Us pages** — actually edited in
      Elementor (not just handed off as copy) and published, per the
      drafted copy above. Where to Buy's fake 3-store layout replaced with
      the real single "order online or visit by arrangement" info. Contact
      Us: real hours/address/email added; social icons mid-swap — Facebook
      kept, LinkedIn kept (real URL still needed from Kofi), Twitter icon
      being replaced with X, Instagram + TikTok icons being added (custom
      SVG-code widget, not a standard icon picker — see chat history if
      picking this back up, the exact SVG snippets used are only in
      conversation, not saved to a file yet).
- [x] **Organic claim caught and walked back**: theme's demo copy claimed
      "Purely Organic" in three places (homepage + both new pages). Kofi
      confirmed no actual certifying body/certificate — reworded all three
      to "Real Ingredients, Start to Finish" / "Family-Farmed, Freshly
      Blended" instead, since an uncertified organic claim is a UK Trading
      Standards issue, not just a nice-to-avoid.
- [x] **All 34 spice products imported to WooCommerce** via the REST API
      from `docs/woocommerce-product-import.csv`. Yaji + Garam Masala have
      full real content (published). The other 19 dry/shelf-stable
      products (per `docs/product-catalog-notes.md`'s dry/wet split, Mole
      Mix corrected from "wet" to "dry" — it's tagged Dry Blend in the
      source) all have a flat £7.99 price and a generated branded
      placeholder image (region-colored card, not a real product photo) —
      still drafts, not published. The 13 genuinely wet products are
      marked out-of-stock and left as drafts for future reference, not
      deleted.
- [x] **First real Episode 1 shoot recording received** (2026-08-06) —
      `video/Episode01_Shoot_RawClip_2026-08-06.mp4`, WhatsApp-compressed
      (640x368), deliberately left unprocessed until the rest of the
      shoot's clips exist. Kofi was going to try to get the original
      higher-quality file (before WhatsApp compression) from whatever he
      recorded on.
- [x] YouTube title/description pairs drafted for two Episode 1 sub-videos
      (Yaji spice blend; Suya/Chinchinga cooking), grounded in
      `scripts/episode-01-west-africa-yaji.md` — saved as Word docs:
      `docs/Yaji-Spice-Blend-Video-Title-Description.docx` and
      `docs/Suya-Chinchinga-Video-Title-Description.docx`. The Mokola
      Market intro video itself was uploaded to Kofi's real YouTube
      channel (`@fudipeople18`) as a Short.

**Still open from this stretch:**
- [x] **2026-08-11:** Contact page social icons finished — all 5 done
      (Facebook, LinkedIn — real URL from Kofi, X, Instagram, TikTok).
      Icons are a custom SVG-code widget (Qode Icon SVG), not Elementor's
      standard icon picker — `<line>` elements got silently stripped by
      the widget's sanitizer, so the X icon had to be rebuilt using
      `<path>` instead. Contact page banner also got its real subtitle and
      a real photo (Chilli Oil bottle + harvest crate, side by side) in
      place of the stock architecture shot; middle-of-banner logo hidden,
      same as the other two pages.
- [x] **2026-08-16: mobile Hero headline bug fixed** — root cause wasn't
      actually font-size (that already scaled down correctly: 36px desktop
      → 31px tablet → 20px mobile). It was the widget's own outer
      `_margin`, hardcoded to 104px on all four sides with no responsive
      override at all. Stacked on top of the column's own 33px mobile
      padding, that left only ~100px of usable width on a 375px-wide
      phone — forcing one word per line and pushing the block's height
      (104px margin + 31px padding, both top and bottom) into "filling the
      screen" territory. Fixed via the WordPress REST API directly
      (`claude-assistant`'s Application Password, which Kofi shared in
      chat, not saved to any file): added `_margin_tablet` (40px/24px) and
      `_margin_mobile` (16px top, 0 sides) overrides to the Hero heading
      widget's Elementor data. One wrinkle worth remembering if this
      pattern comes up again — editing `_elementor_data` via raw REST PUT
      does **not** trigger Elementor's cached-CSS regeneration; that only
      happens through the actual editor save flow, or an admin-only
      action. The REST route for it (`DELETE /wp-json/elementor/v1/cache`)
      requires `manage_options`, which the Editor-role `claude-assistant`
      account doesn't have — so Kofi finished it manually via Elementor →
      Tools → **Clear Files & Data**. Confirmed live afterward (post-7.css
      version bumped, new margin values present in the served CSS).
      Desktop/tablet still not checked in detail — worth doing, along with
      the other 3 pages (How We Do It, Where to Buy, Contact Us) at tablet
      and mobile widths, before calling the full responsive pass done.
- [x] **2026-08-16: two more responsive spacing bugs found and fixed**,
      same static-analysis method as the Hero fix (scanned each page's
      `_elementor_data` for widgets with a sizable fixed margin/padding
      and no tablet/mobile override, then confirmed against the live
      rendered CSS):
      - **How We Do It page**: a small 148×112px badge/photo in the page
        banner had a 186px margin on all four sides with zero responsive
        override — on a ~375px phone that needs 520px of space, causing
        overflow/clipping. Confirmed this exact widget ID exists on all 3
        secondary pages but only had the 186px override applied on this
        one (Where to Buy and Contact Us use the default, unaffected).
        Fixed with a `_margin_mobile` override (12px all sides).
      - **All 3 secondary pages' shared banner column** (top: 200px,
        bottom: 145px on How We Do It/Contact Us, 83px on Where to Buy) —
        not broken, just excessive on mobile (nearly half a phone screen
        of empty padding before any banner content). Tightened with a
        `padding_mobile` override (90px top / 60px bottom) on all three.
      - **Two more content sections**, same excessive-vertical-padding
        pattern, found in a follow-up sweep: Where to Buy's "Order Online,
        or Visit by Arrangement" section (143px bottom padding → 70px on
        mobile) and Contact Us's "Get in touch..." section (108px/130px
        top/bottom → 60px/70px on mobile).
      All fixes confirmed live after Kofi cleared Elementor's cache
      (Tools → Clear Files & Data) — same requirement as the Hero fix,
      since raw REST meta writes don't auto-regenerate cached CSS.
      **Flagged but not touched**: the How We Do It page's values timeline
      has 100px icon/point-marker circles with the same "no responsive
      override" pattern — left alone since without a browser there's no
      way to tell if that's actually broken on a phone or just a bold
      design choice; worth a real look on an actual device.
- [x] **2026-08-16: homepage "What People Are Saying" title bug** — Kofi
      spotted this one directly (screenshots of Elementor's tablet preview
      showed the heading rendering one letter per line, filling the whole
      section, over the coriander-plant background photo). Cause: this
      title's font-size is 90px on desktop with a mobile override down to
      70px, but **no tablet override at all** — so any tablet-width screen
      (or Elementor's own tablet preview) rendered the full 90px, un-
      shrunk, same root-cause family as every other fix in this session.
      Added a `title_typography_font_size_tablet` (78px) and
      `_line_height_tablet` (82px) override, landing it between the
      existing desktop/mobile values. Confirmed live (post-7.css now
      shows a proper 3-step scale: 90px → 78px → 70px). Also worth
      knowing for next time: the testimonial slider right below this
      title has 3 placeholder reviews (Tunde/Ose/Ishaq) with **no author
      photos set at all** — not a bug, just unfinished content, same as
      the already-flagged Testimonials placeholder-quotes item below.
      **Not covered**: no actual desktop/tablet visual check was done
      (this was all static data/CSS analysis, no browser available) —
      still worth an eyes-on pass across all 4 pages at tablet and
      desktop widths before calling this fully done.
- [x] **2026-08-16: About Us page photo placeholders filled in** — this
      page turned out to already have real drafted copy (a proper
      Mokola-Market-opener narrative, matching brand voice) that was never
      logged anywhere in this file — an undocumented earlier editing pass.
      But it had 3 literal `[PHOTO PLACEHOLDER — ...]` text blocks showing
      to real site visitors instead of images (market/founder portrait,
      the Sidcup farm, a product jar shot). Replaced all three with real
      photos already sitting in the WordPress media library from the
      homepage rebuild (no new uploads needed): the watering-can/fork
      polytunnel portrait (`kofi-hero-photo-cleaned`), Kofi holding okra
      in the polytunnel (`kofi-hero-photo-3-holding-okra` — ties directly
      to the okra line already in that section's own copy), and the real
      Chilli Oil bottle shot (`chilli-oil-product-cleaned`). Confirmed
      live — placeholder text gone, all 3 images rendering with proper
      srcset.
- [x] **2026-08-16: real card payments enabled** — checked the live
      checkout via WooCommerce's public Store API
      (`/wp-json/wc/store/v1/cart`, no auth needed) rather than guessing,
      since the `claude-assistant` account doesn't have `manage_woocommerce`
      and can't read `/wc/v3/payment_gateways`. Found only **Direct Bank
      Transfer and Cash on Delivery** were actually enabled — no card
      payment method at all, despite **WooCommerce Payments** (Stripe-
      powered) already being installed (its `payments/woopay` REST
      namespace was registered, but not connected/onboarded). Talked
      Kofi through WooCommerce Payments' own onboarding (business details
      + bank account for payouts + ID verification — has to be done by
      him, it's tied to his identity). Confirmed live afterward: the
      Store API now lists `woocommerce_payments` alongside bacs/cod, plus
      Apple Pay/Google Pay (`payment_request`) and Amazon Pay showing up
      as express-checkout options too.
- [x] **2026-08-17: discovered the whole store is behind a site-wide
      "Coming Soon" page** — while about to work on publishing the 19
      dry-product drafts, checked a product page directly and found it
      (and the `/shop/` page) rendering WooCommerce's "Great things are
      on the horizon... store is in the works" placeholder instead of
      real content. This is a **separate, store-wide toggle**, independent
      of any individual product's publish/draft status — real visitors
      currently cannot browse or buy anything at all, regardless of what
      we do to individual products or payment gateways. Confirmed with
      Kofi this is **intentional, not an oversight** — he's not ready to
      launch yet. Leaving it as-is; **check with him before assuming this
      is still true in a future session**, since he may flip it live
      without necessarily updating this file.
      **Also found, now confirmed**: querying the live product catalog via
      the public `/wp-json/wp/v2/product` endpoint returned **78 published
      products**, not the ~34 documented above (2 published + 19 dry
      drafts + 13 wet drafts). Built a searchable review artifact
      (documented vs undocumented, filterable, links to each product +
      its wp-admin editor) rather than dumping raw data, since this needed
      Kofi's own judgement call. **Kofi confirmed the extra 44 were also
      done through Claude** in an earlier, undocumented session — not a
      bulk import or manual work, just never logged here. Precise
      breakdown of the 44: all created the same day (2026-07-30), none
      have a product photo, and they split into two real categories:
      - **20 are genuinely incomplete** — all 6 Europe items, all 10
        Southeast Asia items, and one "Fudi People Chilli Oil with Spices
        of ___" per line (Africa/Middle East/South Asia/Southeast
        Asia/Americas/Europe) — every one has literal bracketed template
        text as its live description, e.g. `[RECIPE PLACEHOLDER – add a
        paired recipe/food sample showing a dish made using the Vietnam
        spice mix]`. Same placeholder convention as the About Us page bug
        fixed earlier this session.
      - **24 have real, well-written copy** citing specific episode
        numbers, but nearly all of them appear to **duplicate a dish
        already in the documented 34** under a broader regional name
        instead of the dish name — e.g. "West Africa Spice Mix"
        (undocumented) retells the same Yaji/suya story as the documented
        "Yaji (West African Suya Spice Rub)" product. Not reconciled yet:
        worth deciding with Kofi whether these are a deliberate second
        navigation path (browse by region vs. browse by dish) worth
        keeping, or true duplicates worth merging/removing.
      Since the whole store is still behind Coming Soon (see above), none
      of this is customer-visible yet — no urgency, but worth resolving
      before that toggle ever comes down.
      **2026-08-17, reconciled**: Kofi's call — **keep all 44 published
      as-is**, including the 20 with literal `[PLACEHOLDER]` bracketed
      text as their live description. No site changes made (would have
      needed his own bulk-edit in wp-admin anyway — `claude-assistant`
      doesn't have `edit_products`, confirmed via a direct PUT attempt
      that 403'd). Worth remembering next time this comes up: the
      placeholder text is only hidden right now because Coming Soon is
      up — it becomes a real visible-to-customers issue the moment that
      toggle comes down, so revisit before launch, not after.
- [x] **2026-08-18: 11 of the 13 wet products converted to real dry
      products** — Kofi's call: rewrite them as genuine dry spice blends
      (dropping fresh/wet elements) rather than just relabelling, and use
      Fudi People's own farm-grown smoked chillies in place of generic or
      regional chilli substitutes wherever a recipe used one. Drafted
      copy for all 13 first in `docs/wet-to-dry-adaptations.md`; Tucupí
      and Leche de Tigre were dropped at Kofi's request (both
      fundamentally liquid products — fermented cassava juice, five
      limes' worth of citrus — where a dry version barely resembled the
      dish). The remaining 11 went live via the WooCommerce REST API
      (description, short description, £7.99 price, in-stock status, a
      new placeholder image, and cleaned-up tags — "Wet - Needs
      Adaptation" removed, "Dry Blend" and, where a chilli was swapped,
      "Fudi People Chillies" added). Two were renamed for accuracy since
      they no longer describe a wet product: **Yangnyeomjang → Yangnyeom
      Sesame Rub**, **Zhug → Zhug-Style Spice Blend**. Placeholder images
      generated locally with Python/Pillow (not an image-gen tool) to
      exactly match the existing 19 products' branded-card style — same
      1200×1200 region-coloured circle template, colours sampled directly
      from an existing placeholder to confirm the palette (Africa=Maroon,
      Middle East=Gold, South Asia=Marigold, Americas=Ground Raised, East
      Asia=Ink). **Access note**: this needed `manage_woocommerce`/
      `edit_products`, which `claude-assistant`'s Editor role didn't have
      — Kofi upgraded the account to WooCommerce's built-in **Shop
      Manager** role (scoped: product/order management, no plugin/theme/
      user access) rather than issuing a separate Admin credential; the
      same Application Password just started working once the role
      changed. **Two flagged for a real test-batch**: Vindaloo and the
      Yangnyeom rub swap out chillies chosen for a specific mild
      heat/flavour (Kashmiri, gochugaru) for Fudi People's own smokier
      chilli — likely to taste noticeably different, not just "better."
- [ ] Confirm/replace the Testimonials section's placeholder quotes with
      real customer feedback
- [x] **2026-08-21: full pre-launch catalog audit and cleanup, superseding
      the "19 drafts" framing above** — Kofi's plugin update broke the
      site (Elementor + WooCommerce vanished from the plugin list
      entirely; fixed by reinstalling both fresh from wp-admin, no data
      loss since products/pages live in the DB not plugin files), and
      afterward he asked to publish everything live. Live catalog state
      no longer matched these notes (drift since 2026-08-17/18), so
      queried it directly via the WooCommerce REST API instead of
      trusting the old counts:
      - Actual state found: **89 total products, 78 published, 11
        private, 0 in "draft" status** (not the 19+2 drafts logged
        above). Of the 78 "published": **22 had literal `[PLACEHOLDER]`
        bracket text** as their live description (20 of the 22 already
        publicly live, only 2 sitting private), and **54 had no price
        set at all** — meaning most of the catalog wasn't actually
        purchasable, a bigger problem than anything logged previously.
      - Kofi's calls: set the 54 unpriced ones to £7.99 and publish;
        unpublish all 22 placeholder-text ones (moved to draft).
      - **Caught during execution, not before**: 2 of the 54 "just needs
        a price" products were actually **Tucupí** and **Leche de
        Tigre** — the two wet products already deliberately dropped
        from the wet-to-dry conversion (fermented sauce / fresh citrus
        marinade, no real dry equivalent) — their description still
        literally says "WET, needs adaptation." Pulled both out of the
        pricing batch and drafted them instead of publishing.
      - **Caught after the batch ran**: a lingering "private" product,
        **West China Spice Mix** (Sichuan doubanjiang/chilli-bean sauce,
        Episode 29's actual product), already had a price but was never
        touched by either batch — checked its description and it's
        *also* still "WET - a fermented sauce, not a dry blend."
        Appears to have been missed entirely during the original
        2026-08-18 wet-to-dry conversion session — **follow-up needed**:
        decide whether to adapt it to a real dry blend (like the other
        11) or drop it (like Tucupí/Leche de Tigre). Set to draft for
        now.
      - **Bigger catch, worth remembering for next time**: after the
        price+publish batch ran, a follow-up sweep found **10 more
        newly-published products still carrying the "Wet - Needs
        Adaptation" tag** — these are the regional-duplicate versions
        (e.g. "Amazon Spice Mix," "South America Spice Mix") that
        describe the *same* wet dishes as Tucupí/Leche de Tigre/niter
        kibbeh/zhug/taklia/vindaloo-style paste/mbongo/harissa under a
        broader region name instead of the specific dish name — missed
        because the first pass only checked for blank price and
        `[PLACEHOLDER]` text, not the "Wet" tag itself. Reverted all 10
        back to draft. **Lesson logged**: the "Wet - Needs Adaptation"
        tag is the authoritative signal, not the description text or
        price field alone — check it directly next time, on the whole
        catalog, before publishing anything.
      - **Final verified state**: 54 published (every one has a real
        price, no `[PLACEHOLDER]` text, no "Wet" tag), 35 draft, 0
        private. Confirmed via a full re-sweep of all published
        products' tags and prices, not just the ones touched.
      - **2026-08-21, same session — store taken live.** Kofi provided
        the `claude-assistant` Application Password. Found the "Coming
        Soon" toggle is WooCommerce's own built-in Coming Soon mode
        (`woocommerce_coming_soon` option, via the `wc-admin/options`
        REST endpoint) — and discovered `woocommerce_store_pages_only`
        was already `"yes"`, meaning the restriction was scoped to just
        shop/product pages, not the whole site as the 2026-08-17 note
        assumed. Confirmed live with Kofi this was the intended final
        step, then set `woocommerce_coming_soon` to `"no"`. Verified
        twice: a direct re-read of the option (POST response was an
        ambiguous bare `true`, didn't trust it) and an unauthenticated
        fetch of `/shop/` showing real products with working "Add to
        cart" buttons instead of the "Great things are on the horizon"
        placeholder. **The store is now publicly live.**
      - **Still open**: West China Spice Mix and the 10 wet
        regional-duplicates need the same real-copy treatment as the
        original 11 wet→dry conversions (or dropping, per-item) — these
        are currently in draft, not customer-visible, but should get
        proper attention now that the store is live and could otherwise
        sit forgotten. Real product photography (see next item) is now
        more urgent too, since the placeholder cards are visible to
        real customers for the first time.
- [ ] Real product photography to replace the generated placeholder cards
      (now 30 products need this: the original 19 dry + the 11 wet→dry
      conversions, all using generated branded placeholder cards, not
      real photos)
- [ ] Continue Episode 1 shooting; normalise/assemble once all clips exist
- [ ] **2026-08-18: Higgsfield MCP added for B-roll generation, trial
      running — CANCEL BEFORE RENEWAL.** Added via `claude mcp add
      --transport http --scope user higgsfield https://mcp.higgsfield.ai/mcp`
      to generate the `[B-ROLL]` cues already written into every episode
      script (239 across all 34 episodes) — map/trade-route animations
      specifically, not anything with Kofi's face/voice/real specific
      places (Mokola Market, the Sidcup farm) in it, which stay real
      footage on purpose. Went through Episode 1's 7 cues as the test
      case: only 2 are genuine AI-generation candidates (the "map
      graphic" and "trade route map animation" in cues 2–3), the rest
      are either tied to a real specific place or are simple cooking-demo
      shots better filmed for real. Draft prompts for both are in this
      session's conversation history, not yet saved to a file — write
      them down properly once the first generation actually confirms the
      approach works.
      **Cost reality check, found the hard way**: initial research
      (aggregator blogs, not Higgsfield's own JS-rendered pricing page,
      which isn't fetchable) suggested a $15/month Starter tier existed —
      wrong. What Kofi's account actually shows is a **3-day free trial
      that auto-renews into $49/month**, no cheaper tier available. His
      call: run the trial, generate Episode 1's 2 clips, **cancel before
      it renews** rather than commit to $49/month yet — this is the one
      part of the project that's departed from the "$0 to start"
      philosophy everything else has followed, and it's not confirmed
      worth it yet. Trial started 2026-08-18 — **if this item is still
      open in a future session, check whether it actually got cancelled**,
      since I have no way to confirm that myself or send a reminder
      outside an active conversation. Kofi should also set his own
      calendar reminder, not rely on this file alone.
      **Access note**: MCP tools only load at session start — even after
      Kofi authenticates, using the actual `generate_video`/
      `generate_image` tools needs a fresh Claude Code session, not the
      one that ran `claude mcp add`.
      **2026-08-18 update — first 2 clips generated.** Used model
      `gemini_omni` (Google, via Higgsfield), vertical 9:16, 720p, 6s
      each, no reference image (pure text-to-video), 18 credits each
      (36 total, from a 58.8 balance). Output saved to
      `graphics/episode-01/broll/`:
      - `ep01-broll-ghana-coastline-map.mp4` — for cue 2 (Geography &
        Origin): "A stylized animated documentary map graphic of West
        Africa, warm editorial style, burnt-orange and deep burgundy
        color palette on aged textured paper-map background. Camera
        slowly pushes in on the West African coastline covering Ghana,
        Ivory Coast, Liberia and Sierra Leone, with a soft warm glow
        gently pulsing along Ghana's coastline, historically known as
        the Grain Coast and Pepper Coast. Fine spice-dust particles
        drift gently in the air. No text, no labels, no logos. Clean,
        elegant, slow and deliberate camera motion, vertical format,
        suitable as narrated B-roll footage."
      - `ep01-broll-trade-route-animation.mp4` — for cue 3 (Trade &
        Migration History): "A stylized animated historical trade-route
        map graphic, warm editorial documentary style, burnt-orange and
        deep burgundy color palette on aged textured paper-map
        background. A glowing line animates and traces a caravan trade
        route from West Africa across the Sahara desert northward into
        Europe, with small dotted waypoints lighting up in sequence as
        the line travels. Subtle sand and dust particles drift along the
        Saharan stretch of the route. No text, no labels, no logos.
        Smooth, elegant motion graphics, slow deliberate pacing, vertical
        format, suitable as narrated B-roll footage."
      Note: the first submission for the Ghana clip was rejected by
      Higgsfield's own recommender in favour of an unrelated horror-genre
      preset ("IN THE DARK") — resubmitted with that preset explicitly
      declined and it generated correctly on the retry; worth expecting
      this on future generations and just declining the wrong preset.
      **2026-08-18, later same day: spliced in and promoted.** Installed
      `ffmpeg` (`winget install Gyan.FFmpeg`) and cut both clips into
      `video/episode-01-rough-cut-DRAFT.mp4` in place of the static
      `ep01-map-ghana.png`/`ep01-map-trade-route.png` title cards for
      those two beats. Kofi reviewed and approved; the file now in the
      repo is the B-roll version — pre-B-roll cut recoverable from
      git/LFS history if ever needed. Full method, one known regression
      (crossfade → hard cut at the Ghana→farm-photo boundary), and
      verification notes in `video/README.md`. **Done** — this item can
      be considered closed; only the trial-cancellation half of this
      task (separate scheduled check, 2026-08-21) remains open.
- [ ] **2026-08-19: Episode 2 (Senegal) trade-route B-roll generated,
      not yet spliced in.** Same `gemini_omni` setup as Episode 1 (9:16,
      720p, 6s, no reference image), 18 credits — last clip affordable
      before the trial balance ran low (22.8 → 4.8 remaining after this
      one, not enough for another). Saved to
      `graphics/episode-02/broll/ep02-broll-senegal-nigeria-ghana-trade-route.mp4`.
      Covers cue 3 (Trade & Migration History) only — on-screen text
      "One dish, one spice, three countries — Senegal to Nigeria and
      Ghana": "A stylized animated historical trade-route map graphic,
      warm editorial documentary style, burnt-orange and deep burgundy
      color palette on aged textured paper-map background. A glowing
      line animates and traces the spread of a dish and its spice blend
      starting from Senegal, branching eastward along the West African
      coast to Nigeria and Ghana, with small dotted waypoints lighting
      up in sequence at each country as the line travels. Subtle fine
      dust particles drift gently along the route. No text, no labels,
      no logos. Smooth, elegant motion graphics, slow deliberate pacing,
      vertical format, suitable as narrated B-roll footage." Cue 2's map
      graphic (Senegal coastline) wasn't generated — deliberately
      skipped, credits ran low and that cue can partly use real market
      footage instead, unlike the trade-route cue which has no
      real-footage alternative. Episode 2 has no rough-cut animatic yet
      (unlike Episode 1), so nothing to splice this into yet — stays as
      a standalone asset until Episode 2 gets its own animatic build.
      **2026-08-19, later same session: cue 2 generated too, pair now
      complete.** Credits had dropped to 4.8 (not enough for another
      `gemini_omni` clip at 18 each), so switched models — **Kling 3.0
      Turbo**, 3s/720p/9:16, 4.5 credits, text-only. Saved to
      `graphics/episode-02/broll/ep02-broll-senegal-coastline-map.mp4`:
      "A stylized animated documentary map graphic of Senegal and the
      West African coastline, warm editorial style, burnt-orange and
      deep burgundy color palette on aged textured paper-map background.
      Camera slowly pushes in on Senegal's coastline, with a soft warm
      glow gently pulsing over Senegal. Fine dust particles drift gently
      in the air. No text, no labels, no logos. Clean, elegant, slow and
      deliberate camera motion, vertical format, suitable as narrated
      B-roll footage." Note: shorter (3s vs the 6s `gemini_omni` clips)
      and a different model, so motion style may not exactly match the
      other Episode 1/2 clips — worth a look side-by-side before relying
      on visual consistency across episodes. **Trial balance now 0.3
      credits — effectively exhausted**, nothing more generatable until
      either the trial renews (2026-08-21, see the cancellation-decision
      item above) or credits are topped up.
- [x] **2026-08-24: "Spice Blend" / "Cooking" video tabs added to every
      product page**, alongside the default Description/Reviews tabs —
      matches the episode structure's "The blend" / "The dish" beats.
      `claude-assistant`'s Shop Manager role can't install plugins or edit
      theme files, so this needed Kofi's own action: installed the free
      "Code Snippets" plugin and activated the filter saved at
      `docs/product-video-tabs-snippet.php` (a `woocommerce_product_tabs`
      filter). Took two tries — the first paste had a stray leftover `php`
      word on its own line (from partially deleting the `<?php` tag,
      which Code Snippets adds automatically and doesn't want in the
      snippet body) plus a stray `:` glued onto `add_filter(`, both fatal
      parse errors; fixed by repasting clean. Confirmed live on Yaji
      (`tab-title-spice_blend_video` / `tab-title-cooking_video` both
      present, "Coming soon" placeholder showing correctly). Both tabs
      read from product custom fields — renamed from an initial
      `_spice_blend_video_url`/`_cooking_video_url` (underscore-prefixed
      meta is hidden from wp-admin's Custom Fields UI by design, so Kofi
      couldn't self-edit them) to `spice_blend_video_url`/
      `cooking_video_url` instead, second snippet re-paste required.
      **Cooking tab now has a real video** — Kofi's own raw iPhone
      footage (`IMG_4573.MOV`, grilling suya/chinchinga skewers with
      Yaji) polished via ffmpeg (rotation fix, subtle contrast/saturation
      boost, loudnorm audio, fade in/out) and self-hosted: Kofi's call
      was to skip YouTube for now and host the file directly. My own
      REST API upload attempts got blocked by the host's mod_security
      WAF for *any* video file regardless of size (confirmed with a
      434KB test clip) — worked fine once Kofi uploaded it himself via
      wp-admin's Media Library screen instead (different request path).
      Snippet updated again to detect a direct file URL
      (`.mp4`/`.mov`/etc via regex) and use `wp_video_shortcode()`
      instead of `wp_oembed_get()`, which only works for oEmbed
      providers like YouTube. Spice Blend tab still shows "Coming soon"
      — no blend-making footage exists yet. **Next step, whenever a real
      video exists for either tab**: tell Claude the product + a
      YouTube link or local file path and it'll handle upload/encoding
      and set the custom field via the API directly.
      (An earlier attempt embedded the video placeholders directly inside
      Yaji's Description tab instead of a new tab — tried and reverted
      same session, Kofi wanted a real separate tab.)

## 2026-08-25 — spice jar label design system

- [x] **Front-of-jar label template designed and approved (Yaji), then
      rolled out to all 34 blends.** One fixed circular template — pin
      mark, "FUDI PEOPLE" wordmark, gold rule, headline, thin gold
      trade-route line, region tag, micro copy — with only the field
      color (per continent) and two lines of copy (blend name + dish
      tie-in) changing per product. Authored as HTML/CSS (Adobe Fonts:
      Source Serif 4 for headline/subhead, Source Sans 3 for wordmark/
      tag/micro copy), rendered to PNG via headless Edge for review
      since there's no other HTML-to-image pipeline available in this
      environment. Files: `graphics/labels/yaji-label-west-africa.html`
      (+ `.png`) for the single approved design, and
      `graphics/labels/all-34-labels-proof-sheet.html` (+ `.png`) for
      the full-catalog proof sheet.
      **Correction caught by Kofi**: Yaji's first draft subhead read
      "Grains of Paradise · West Africa," which wrongly implied a
      single-ingredient product — Yaji is actually a blend (grains of
      paradise, grains of selim, ginger powder, roasted peanut/
      kuli-kuli, etc.). Fixed to "Suya & Chinchinga Blend · West
      Africa" (describes the blend by what it's for, not a false
      single-spice claim) on both the label and the review page's own
      heading.
      **Region palette** (field color only, accent gold/cream constant
      across all): Africa = maroon, Middle East = amber, South Asia =
      marigold, East Asia = ink, The Americas = terracotta — extending
      the palette already used on the product placeholder cards and
      the Higgsfield map B-roll.
      **All 34 blend names, subheads (dish tie-ins), and regions were
      pulled directly from each episode script's own `## 5. The Blend`
      heading and `## 6. The Dish` on-screen text** — nothing invented.
      Headline font-size auto-tiers by name length (4 tiers) so long
      names (e.g. "CHILLI BLACK BEAN SAUCE," "SHICHIMI-TOGARASHI")
      still fit the circle cleanly.
      **What this is and isn't**: the proof sheet is a review/QA
      artifact (34 small cards in one file), not individual production
      files. **Still open**: once the region palettes and copy are
      approved per-continent, each blend needs cutting as its own pair
      of files (95mm round physical + 1200×1200px digital), same as
      Yaji's. Back-of-jar labels (ingredients, allergens, net weight in
      full, barcode) — explicitly deferred, front-of-jar only for now.
      Wet-only products (Yassa, Niter Kibbeh, Pepper Soup Spice,
      Harissa, Mbongo Mix, Zhug, Taklia, Vindaloo Paste, Yangnyeomjang,
      Chilli Black Bean Sauce, Chimichurri, Tucupí, Leche de Tigre)
      still got a label design here — packaging/sell-readiness (see
      `product-catalog-notes.md`) is a separate open question from
      branding.
      **2026-08-27: real logo swapped in for the placeholder mark.**
      Kofi asked whether the label could use the actual Fudi People
      logo instead of the generic pin icon. Found it live on the site
      (`fudipeople.com`'s header image — a WhatsApp-sourced PNG with
      background removed) and pulled it into
      `brand-assets/logo/fudi-people-logo.png`. Built a 4-way
      comparison (`graphics/labels/yaji-label-logo-comparison.png`):
      full-color logo direct on the maroon field (the maroon bowl/text
      nearly vanished — same hue as the background), full-color on a
      cream badge (worked but added a shape), and a single-tone cream
      silhouette (alpha channel preserved, all color stripped via an
      ffmpeg `geq` filter) — no extra shapes, full contrast. Kofi
      picked the silhouette, then asked for the "PEOPLE" sub-text
      bolder since it's thin in the original artwork and got lost at
      label scale — fixed by dilating the alpha channel twice (ffmpeg
      `dilation` filter, thickens every line uniformly, not just that
      one word) before recoloring. Final logo variant:
      `brand-assets/logo/fudi-people-logo-cream-bold.png` (black/white
      bold versions also generated for use on light backgrounds).
      Swapped into the approved `yaji-label-west-africa.html` in place
      of the placeholder pin mark, replacing the separate "FUDI PEOPLE"
      text line too since the real logo already spells it out. Verified
      at true print size (93px wide on the 359px label) — legible.
      **2026-08-30: same swap rolled out to all 34.** Kofi confirmed —
      replaced the placeholder pin-icon + "FUDI PEOPLE" text line with
      the real `fudi-people-logo-cream-bold.png` across every card in
      `all-34-labels-proof-sheet.html` (all 34 occurrences were
      byte-identical, so one scripted find/replace covered the whole
      file safely). Resized `.mark` for the smaller card scale (48px
      wide vs Yaji's dedicated-page 93px, same proportion relative to
      the smaller 190px card), removed the now-unused placeholder-icon
      CSS rules, and updated the intro copy off "pin mark" wording.
      Re-rendered via headless Edge and spot-checked at 2x zoom on both
      the lightest (Africa/maroon) and darkest (East Asia/ink) region
      fields — logo reads cleanly on both, matching the approved Yaji
      look. `all-34-labels-proof-sheet.png` regenerated to match.
      **2026-09-01: all 34 cut into individual production files** —
      `graphics/labels/production/`. One HTML source per blend
      (`epNN-<slug>.html`), canvas-agnostic: all interior sizing is in
      `vmin`, so a single file renders correctly at any square size.
      Generated from the proof-sheet data (headline tiers, subheads,
      region palettes, tags all carried over verbatim — nothing
      re-authored). Each blend rendered via headless Edge to two PNGs:
      `-digital-1200.png` (1200×1200 product image, transparent corners)
      and `-print-95mm-300dpi.png` (1122px = 95mm @ 300dpi — a real print
      resolution, unlike Yaji's older 359px/96dpi pair, which can be
      re-rendered from HTML the same way if needed). Plus `_index.html`
      (contact sheet of all 34) and `README.md` (re-render command, and
      what's deliberately not done: back-of-jar labels, real net weight,
      print bleed/crop marks, per-continent palette sign-off). ~38MB of
      PNGs added — fine for the repo but worth knowing.
      **Still open**: back-of-jar labels (ingredients, allergens per
      Natasha's Law, barcode) remain deferred; net weight reads a
      placeholder `NET WT 50g` on every label pending the packaging-size
      decision in `docs/product-catalog-notes.md`.

## 2026-09-02/04 — gentle store rollout + chilli-oil labels

- [x] **2026-09-02: "gentle rollout" — Africa range + 3 chilli oils only,
      live via the WooCommerce REST API** (ck/cs keys Kofi pasted in chat,
      not saved to a file; `Mozilla/5.0` User-Agent header needed or the
      host's mod_security returns 406). Kofi's call: roll out gently with
      just the African spices in stock, plus the Fudi People Chilli Oil
      with Spices of Africa / East Asia / South Asia.
      - **In stock (14):** the 11 published Africa-category products
        (West/East/Southern Africa Spice Mix, Yaji, Yassa, Harissa, Pilau
        Masala, Durban Curry Masala, Mbongo Mix, Niter Kibbeh, Pepper Soup
        Spice — all £7.99) + the 3 named chilli oils (ids 2226/2241/2250),
        which were published, priced **£8.99 (150 ml)**, set in stock.
      - **Out of stock (43):** every other currently-published product
        (all Middle East, South Asia, East Asia, Americas blends + the
        other regional chilli oils) → `stock_status: outofstock`, left
        published/browsable. Reversible per-product flag.
      - **Untouched:** the ~32 existing drafts.
      - The 3 wet Africa-category drafts (Maghreb / Central Africa / Horn
        of Africa "Spice Mix") were **left as drafts** — their dry
        equivalents (Harissa Spice Blend, Mbongo Mix, Niter Kibbeh Spice
        Blend) are already live and in stock, so publishing the
        region-named duplicates would just double up the Africa range.
- [x] **2026-09-03/04: chilli-oil front-of-bottle labels rebuilt** from
      Kofi's AI-generated concept art (Africa heart/rooster, East Asia
      dragon, South Asia Buddha). Re-authored as clean HTML/CSS with the
      real Fudi People logo, "Chilli" spelling fixed, native-script line
      kept (辣油 / मिर्च का तेल — the concept's South Asia line was
      actually romanised Mandarin, swapped to Hindi per Kofi), tagline
      dropped. Emblems vectorised razor-sharp with **vtracer** (pip
      install; also `pymupdf` for the PDF). Dragon flattened to one cream
      tone — the source was ~95 px, too low-res for the white+gold detail.
      Files in `graphics/labels/chilli-oil/` (label HTML + PNG web/print,
      clear-glass 150 ml bottle mockups, 3 emblem SVGs); maroon logo at
      `brand-assets/logo/fudi-people-logo-maroon.png`. See that folder's
      `README.md`.
      **Still open:** the 3 bottle mockups need to become the WooCommerce
      product images for ids 2226/2241/2250, replacing the generated
      placeholder cards. Blocked this session — the WC consumer key can't
      auth `wp/v2/media`, and the host's mod_security WAF 406s the binary
      upload anyway. Needs the `claude-assistant` Application Password, or
      Kofi uploads the 3 PNGs to the Media Library and shares the URLs
      (then settable via `PUT /products/<id>` `images:[{src}]`).

## Not started (later phases, per blueprint build order)

- [ ] Agent 1 (Trends & Outlier Scout) — deliberately deprioritised, no
      dependency on Agents 2/3
- [ ] Agent 4 build-out — needs a real outlier thumbnail to reference
      (Agent 1); the reference-photo gap is now closed
- [ ] Agent 5 (Editing) and Agent 6 (Publishing) — Phase 2+

## Reference

- `docs/system-blueprint.md` — the full system blueprint (canonical copy),
  including the citation rule, the Named Influences benchmark set, and the
  $0-to-start cost breakdown
- `docs/project-context-brief.md` — consolidated handoff doc from the
  agent-building chat session, useful for the full "what's built / what's
  missing" picture in one place
- `docs/spice-channel-framework.md` — Season 1 roadmap (11 episodes) and
  the reusable per-episode research prompt
