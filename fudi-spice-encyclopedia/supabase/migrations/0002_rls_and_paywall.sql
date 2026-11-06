-- Row Level Security + server-side paywall

-- Helper: is the current user an admin? (security definer avoids RLS recursion on profiles)
create function public.is_admin() returns boolean
language sql stable security definer set search_path = public as $$
  select coalesce((select role = 'admin' from public.profiles where id = auth.uid()), false)
$$;

create function public.is_member() returns boolean
language sql stable security definer set search_path = public as $$
  select coalesce((select membership_status = 'member' or role = 'admin'
                   from public.profiles where id = auth.uid()), false)
$$;

alter table public.regions enable row level security;
alter table public.profiles enable row level security;
alter table public.products enable row level security;
alter table public.articles enable row level security;
alter table public.article_bodies enable row level security;

-- regions: public read, admin write
create policy regions_read on public.regions for select using (true);
create policy regions_admin on public.regions for all using (public.is_admin()) with check (public.is_admin());

-- profiles: users read ONLY their own row; nobody but the service role (Stripe webhook) changes
-- membership_status. There is deliberately no user UPDATE policy, so users can't promote themselves.
create policy profiles_read_own on public.profiles for select using (id = auth.uid() or public.is_admin());

-- products: public read, admin write
create policy products_read on public.products for select using (true);
create policy products_admin on public.products for all using (public.is_admin()) with check (public.is_admin());

-- articles (metadata only): public sees published; admin sees and edits everything
create policy articles_read_published on public.articles for select using (published or public.is_admin());
create policy articles_admin on public.articles for all using (public.is_admin()) with check (public.is_admin());

-- article_bodies: NO public policy at all. Only admins can read the table directly.
-- Everyone else gets text through get_article(), which truncates for non-members.
create policy bodies_admin on public.article_bodies for all using (public.is_admin()) with check (public.is_admin());

-- ---------- paywall RPC ----------
-- Members/admins get the full body. Everyone else gets roughly the first preview_percent% of the
-- text, cut at a paragraph boundary (never mid-sentence).
create function public.get_article(p_slug text)
returns table (
  id uuid, slug text, title text, region_slug text, summary text, cover_image_url text,
  product_id uuid, published_at timestamptz, updated_at timestamptz,
  body_md text, is_preview boolean
)
language plpgsql stable security definer set search_path = public as $$
declare
  a public.articles%rowtype;
  full_body text;
  paras text[];
  target int;
  acc text := '';
  p text;
begin
  select * into a from public.articles where articles.slug = p_slug and (articles.published or public.is_admin());
  if not found then return; end if;

  select b.body_md into full_body from public.article_bodies b where b.article_id = a.id;
  full_body := coalesce(full_body, '');

  if public.is_member() then
    return query select a.id, a.slug, a.title, a.region_slug, a.summary, a.cover_image_url,
      a.product_id, a.published_at, a.updated_at, full_body, false;
    return;
  end if;

  target := (length(full_body) * a.preview_percent / 100.0)::int;
  if a.preview_percent > 0 then
    paras := regexp_split_to_array(full_body, E'\n{2,}');
    foreach p in array paras loop
      exit when acc <> '' and length(acc) >= target;
      acc := acc || case when acc = '' then '' else E'\n\n' end || p;
    end loop;
  end if;

  return query select a.id, a.slug, a.title, a.region_slug, a.summary, a.cover_image_url,
    a.product_id, a.published_at, a.updated_at, acc, length(acc) < length(full_body);
end $$;

revoke all on function public.get_article(text) from public;
grant execute on function public.get_article(text) to anon, authenticated;
