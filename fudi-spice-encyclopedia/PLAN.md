# Plan and decisions

## Folder structure
```
src/components   Layout, ArticleCard, Markdown, Paywall, BuyBar, Seo, RequireAdmin
src/pages        Home, Encyclopedia, ArticlePage, About, Login, Membership, Account, admin/*
src/lib          supabase client, api calls, types, placeholder demo data
src/context      AuthContext (session + profile: member/admin)
supabase/migrations  0001 schema, 0002 RLS + paywall function, 0003 storage
supabase/functions   create-checkout, customer-portal, stripe-webhook
scripts          import-scripts.ts (+ tests)
```

## Schema
- `regions` (slug, name): editable. Seeded with 7 (you said six; the shop has 5 categories and the knowledge base has 7).
- `profiles` (id, email, role user|admin, membership_status free|member, stripe ids, current_period_end). Auto-created by trigger on sign-up.
- `products` (name, region, description, price_display, image_url, buy_url).
- `articles` (slug, title, region, summary, cover, preview_percent, product_id, featured, published). Metadata only.
- `article_bodies` (article_id, body_md). Separate table so full text can't leak via a normal query.

## Paywall (server-side)
`article_bodies` has no public RLS policy. The browser calls `get_article(slug)` (security definer). It returns the full body to members/admins, and for everyone else the first `preview_percent`% cut at a paragraph boundary, with `is_preview = true`. Users have no UPDATE policy on `profiles`, so only the Stripe webhook (service role) can grant membership.

## Admin
Role-based via `profiles.role = 'admin'`, enforced by RLS on every table and the storage bucket. The `/admin` route guard is only a convenience.

## Import
`npm run import:scripts`: drafts only, filename -> title/slug, content untouched, skips existing slugs, skips filming/read-aloud files by default.

## Build order (all steps done as a first pass)
Setup, schema/RLS, layout/home/about, index/article, auth, paywall, admin, import, Stripe, SEO/deploy config.

## Decisions for you
1. Regions: keep 7 or trim to 6.
2. Home/About copy is draft text from your brief. Rewrite in your voice.
3. Membership prices are `£X.XX` placeholders.
4. Imported titles are filename-derived ("Episode 09 Caribbean Jerk"). Retitle in admin (e.g. "Allspice").
