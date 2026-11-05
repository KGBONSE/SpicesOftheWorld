# Fudi People Spice Encyclopedia

Vite + React + TypeScript + Tailwind, Supabase (Postgres, Auth, RLS, Storage), Stripe Checkout (GBP). See `PLAN.md` for the architecture and decisions.

## Run it (preview mode, no accounts needed)

```
npm install
npm run dev
```

Without Supabase keys the site runs on clearly-marked placeholder content so you can look at the design.

## Connect Supabase

1. Create a project at supabase.com.
2. In the SQL editor, run in order: `supabase/migrations/0001_schema.sql`, `0002_rls_and_paywall.sql`, `0003_storage.sql`. (Optional dev demo content: `supabase/seed.sql`.)
3. Copy `.env.example` to `.env.local` and fill in the URL and anon key (Project Settings > API).
4. Auth > URL Configuration: add your site URL and `http://localhost:5173` as redirect URLs.
5. Sign up on the site, then make yourself admin in the SQL editor:
   ```sql
   update public.profiles set role = 'admin' where email = 'YOUR@EMAIL';
   ```
   There is no other way to become admin, by design.

## Import your scripts

Your scripts are in `../spicesOftheWorld/scripts/` (34 main episode scripts plus 16 filming/read-aloud files).
Add `SUPABASE_SERVICE_ROLE_KEY` to `.env.local` (never `VITE_`-prefixed), then:

```
npm run import:scripts -- --dry-run --dir ../spicesOftheWorld/scripts
npm run import:scripts -- --dir ../spicesOftheWorld/scripts
```

Drafts only; title and slug come from the filename; text is stored untouched; existing slugs are skipped.
Edit and publish them in `/admin`. Note they still contain production notes and `[NEEDS KOFI]` markers.

## Memberships (Stripe)

1. In Stripe, create a Product with two recurring GBP Prices (monthly, annual). Enable the Customer Portal.
2. Install the Supabase CLI, then:
   ```
   supabase link --project-ref YOUR_REF
   supabase secrets set STRIPE_SECRET_KEY=sk_... STRIPE_PRICE_MONTHLY=price_... STRIPE_PRICE_ANNUAL=price_... SITE_URL=https://your-domain
   supabase functions deploy create-checkout
   supabase functions deploy customer-portal
   supabase functions deploy stripe-webhook --no-verify-jwt
   ```
3. In Stripe > Developers > Webhooks add `https://YOUR_REF.supabase.co/functions/v1/stripe-webhook` for events `checkout.session.completed`, `customer.subscription.created`, `customer.subscription.updated`, `customer.subscription.deleted`. Then `supabase secrets set STRIPE_WEBHOOK_SECRET=whsec_...`.
4. Put your real prices in the display text in `src/pages/Membership.tsx` (currently `£X.XX` placeholders).
5. Test in Stripe test mode with card 4242 4242 4242 4242 first.

## Deploy (Vercel or Netlify)

Build command `npm run build`, output `dist`. Set `VITE_SUPABASE_URL`, `VITE_SUPABASE_ANON_KEY`, `VITE_SITE_URL`. SPA rewrites are already in `vercel.json` and `public/_redirects`.

## Known limits

- Open Graph tags are set in the browser. Facebook/X/WhatsApp crawlers don't run JavaScript, so shared links may not show per-article previews until you add prerendering or an edge function.
- Stripe functions and the paywall SQL were written but not run against a live Supabase/Stripe project.
