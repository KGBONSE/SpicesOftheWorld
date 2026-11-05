-- DEV SEED ONLY: placeholder demo content so the UI has something to show.
-- It is NOT your content. Delete these rows (or skip this file) before launch.
insert into public.products (id, name, region_slug, description, price_display, buy_url) values
  ('00000000-0000-0000-0000-0000000000a1', 'Yaji (Suya Spice)', 'africa', 'Placeholder description. Replace in admin.', '£0.00', 'https://fudipeople.com'),
  ('00000000-0000-0000-0000-0000000000a2', 'Garam Masala', 'south-asia', 'Placeholder description. Replace in admin.', '£0.00', 'https://fudipeople.com');

insert into public.articles (id, slug, title, region_slug, summary, product_id, featured, published) values
  ('00000000-0000-0000-0000-0000000000b1', 'demo-yaji', 'Demo: Yaji', 'africa', 'Placeholder article to test the paywall.', '00000000-0000-0000-0000-0000000000a1', true, true),
  ('00000000-0000-0000-0000-0000000000b2', 'demo-garam-masala', 'Demo: Garam Masala', 'south-asia', 'Placeholder article to test the index.', '00000000-0000-0000-0000-0000000000a2', true, true);

insert into public.article_bodies (article_id, body_md) values
  ('00000000-0000-0000-0000-0000000000b1', E'## Placeholder\n\nThis first paragraph is the free preview.\n\nSecond paragraph of placeholder text.\n\nThird paragraph of placeholder text.\n\nFourth paragraph: members only.'),
  ('00000000-0000-0000-0000-0000000000b2', E'## Placeholder\n\nFirst paragraph.\n\nSecond paragraph.\n\nThird paragraph.\n\nFourth paragraph.');
