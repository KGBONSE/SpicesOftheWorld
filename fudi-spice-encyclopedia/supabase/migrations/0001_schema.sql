-- Fudi People Spice Encyclopedia: schema
create extension if not exists "pgcrypto";

-- ---------- regions ----------
create table public.regions (
  slug text primary key,
  name text not null,
  sort_order int not null default 0
);

insert into public.regions (slug, name, sort_order) values
  ('africa', 'Africa', 1),
  ('middle-east', 'Middle East', 2),
  ('south-asia', 'South Asia', 3),
  ('east-asia', 'East Asia', 4),
  ('southeast-asia', 'Southeast Asia', 5),
  ('americas', 'Americas', 6),
  ('europe', 'Europe', 7);

-- ---------- profiles ----------
create table public.profiles (
  id uuid primary key references auth.users (id) on delete cascade,
  email text,
  role text not null default 'user' check (role in ('user', 'admin')),
  membership_status text not null default 'free' check (membership_status in ('free', 'member')),
  stripe_customer_id text unique,
  stripe_subscription_id text,
  current_period_end timestamptz,
  created_at timestamptz not null default now()
);

-- Create a profile row for every new auth user.
create function public.handle_new_user() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  insert into public.profiles (id, email) values (new.id, new.email);
  return new;
end $$;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();

-- ---------- products ----------
create table public.products (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  region_slug text references public.regions (slug) on update cascade on delete set null,
  description text not null default '',
  price_display text not null default '',   -- e.g. "£6.50" (display only; no checkout of our own)
  image_url text,
  buy_url text not null,                    -- link to the live Fudi People shop
  created_at timestamptz not null default now()
);

-- ---------- articles ----------
-- Public metadata lives here. The Markdown body lives in article_bodies so the
-- full text can never leak through a plain SELECT on this table.
create table public.articles (
  id uuid primary key default gen_random_uuid(),
  slug text not null unique check (slug ~ '^[a-z0-9]+(-[a-z0-9]+)*$'),
  title text not null,
  region_slug text references public.regions (slug) on update cascade on delete set null,
  summary text not null default '',
  cover_image_url text,
  preview_percent int not null default 25 check (preview_percent between 0 and 100),
  product_id uuid references public.products (id) on delete set null,
  featured boolean not null default false,
  published boolean not null default false,
  published_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table public.article_bodies (
  article_id uuid primary key references public.articles (id) on delete cascade,
  body_md text not null default ''
);

create index articles_region_idx on public.articles (region_slug) where published;
create index articles_published_idx on public.articles (published_at desc) where published;

create function public.touch_article() returns trigger language plpgsql as $$
begin
  new.updated_at = now();
  if new.published and new.published_at is null then new.published_at = now(); end if;
  return new;
end $$;

create trigger articles_touch before insert or update on public.articles
  for each row execute function public.touch_article();
