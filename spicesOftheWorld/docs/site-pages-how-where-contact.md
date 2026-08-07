# "How We Do It" / "Where to Buy" / "Contact Us" — Page Copy

Draft copy for the three pages Kofi flagged as untouched on fudipeople.com
(2026-08-07). Same situation as the WooCommerce import: **no CMS/Elementor
access**, so this is copy to paste in yourself — nothing here publishes
automatically. Written to match `docs/brand-voice.md` (warm, memory-driven,
first-person) where the content is personal/story-led, and kept plainer
where the page is purely functional (Contact details, buy links).

Facts confirmed directly by Kofi (2026-08-07) — nothing below is invented:
- Phone: `+44 7952 983201`
- Social handles: `fudipeople` on Instagram, TikTok, X, Facebook
- Sourcing: home-grown chillies/okra/produce from the Sidcup farm; other
  whole spices bought from a specific online supplier, kept unnamed on the
  page per Kofi's call
- Sales channel: website only for now — no physical stockists, no wholesale
  route yet (revisit this page if that changes)

---

## Page 1 — How We Do It

**Suggested URL slug:** `/how-we-do-it`

### Headline

From the farm in Sidcup to the jar in your kitchen

### Body copy

Every Fudi People blend starts the same way it always has — with my hands
in the soil.

We grow our chillies, our okra, and a good part of what goes into every
jar on a small farm in Sidcup, London. It's not a big operation — it's a
family one. Watering, potting, harvesting, the twist-not-cut way my mum
taught me for pulling okra off the plant without bruising it — the same
care that went into everything she grew goes into everything we grow now.

What we can't grow ourselves — the whole spices that don't take to a
London climate — we source as whole spices from a trusted online spice
supplier, then grind and blend them ourselves, by hand, in small batches.
Nothing pre-ground, nothing sitting in a warehouse for months losing its
flavour before it reaches you. That's the whole philosophy: grow what we
can, source carefully what we can't, and never let a blend sit around
before it's fresh in your hands.

Everything is made from our home kitchen, registered with our local
Environmental Health Officer — every batch handled the way I'd want it
handled if it were going to my own family's table. Because it is.

That's the throughline for every jar we make: real ingredients, real
hands, real care — the same seeds my mum planted for me, planted for you
too.

### On-screen / CTA block (optional, matches episode closing style)

**"See the full story behind every blend — and the recipes that go with
them — at fudipeople.com."**

### Feature blocks (2026-08-07 update)

Replacements for the theme's four demo icon-box sections currently on this
page. Kofi confirmed (2026-08-07) Fudi People **is certified organic** —
if you have the certifying body's name and certificate/licence number
(Soil Association, OF&G, etc.), add it under block 4 below; UK Trading
Standards expect an organic claim to be backed by a visible certification
reference, not just the word "organic" on its own.

**Block 1**

> ### Products That Keep Your Family Happy
>
> Every blend starts the same way it would if it were going on my own
> daughters' plates — real ingredients, nothing you can't pronounce, and
> the same care my mum put into every meal she made for us.

**Block 2**

> ### We Keep It Simple — Certified Organic
>
> No fillers, no shortcuts. Just certified organic whole spices, ground
> and blended by hand in small batches, the way it's always been done.

**Block 3**

> ### It's Our Priority That You Feel Welcome
>
> We're a small, family-run kitchen, not a faceless brand. Every order,
> every question, every message gets a real reply from real people who
> care that you're happy with what lands on your table.

**Block 4**

> ### Our Products Are Purely Organic
>
> From the chillies and okra grown on our own farm in Sidcup to the whole
> spices we source in, every ingredient that goes into a Fudi People jar
> is certified organic — grown and handled the way food should be. [Add
> certifying body + certificate/licence number here if available.]

---

## Page 2 — Where to Buy

**Suggested URL slug:** `/where-to-buy`

### Headline

Right here — fudipeople.com

### Body copy

Right now, the only place to get Fudi People spice blends and chilli oil
is directly through this website. Every jar ships straight from our
kitchen in Sidcup to your door — no middleman, no warehouse sitting
between us and you.

Browse the full range under **Spices of Africa**, **Spices of South
Asia**, and **Spices of East Asia** [or the current live category
structure — confirm against the site before publishing], add what you
need, and check out securely online.

We're not in any shops or markets yet — when that changes, this page
will be the first place to find out. Follow along on Instagram, TikTok,
X, and Facebook (**@fudipeople**) for updates.

### CTA block

**[Shop Now → button linking to the shop/category page]**

---

## Page 3 — Contact Us

**Suggested URL slug:** `/contact-us` (or `/contact`, matching whatever
WordPress already generated — check before publishing)

### Headline

Get in touch

### Body copy

Got a question about an order, a blend, an allergen, or just want to say
hello? We'd love to hear from you.

**Email:** fudipeople@gmail.com
**Phone:** +44 7952 983201
**Instagram / TikTok / X / Facebook:** @fudipeople

We're a small, family-run kitchen, so replies may take a day or two — but
every message gets a real reply from us, not a bot.

### Contact form fields (if using Elementor's form widget instead of/alongside the block above)

- Name
- Email
- Order number (optional)
- Message

Route submissions to `fudipeople@gmail.com`.

---

## Before publishing — flag these for Kofi

1. **"Where to Buy" category names** — copy above uses the three product
   lines from `CLAUDE.md` (Spices of Africa / South Asia / East Asia).
   The WooCommerce import CSV (`spices-of-the-world-woocommerce-import.csv`)
   actually structures the shop as **7 regions** (Africa, Middle East,
   East Asia, South Asia, Southeast Asia, Americas, Europe) — confirm
   which structure is actually live before publishing this page, so it
   doesn't point at categories that don't exist (or don't yet have
   published products, per `docs/spices-of-the-world-site-setup-guide.md`).
2. **Contact form vs. static block** — copy above gives you both a plain
   contact-details block and a form-field list; use whichever matches your
   theme's existing contact page pattern, or both.
3. **Allergen/food-safety note** — not added here since it's already
   handled per-product per `docs/product-catalog-notes.md`; flag if you
   want a general allergen disclaimer added to Contact Us or How We Do It
   too.
