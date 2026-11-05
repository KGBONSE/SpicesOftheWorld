-- Public bucket for article covers and product images. Anyone can read; only admins write.
insert into storage.buckets (id, name, public) values ('covers', 'covers', true)
on conflict (id) do nothing;

create policy covers_public_read on storage.objects for select using (bucket_id = 'covers');
create policy covers_admin_insert on storage.objects for insert with check (bucket_id = 'covers' and public.is_admin());
create policy covers_admin_update on storage.objects for update using (bucket_id = 'covers' and public.is_admin());
create policy covers_admin_delete on storage.objects for delete using (bucket_id = 'covers' and public.is_admin());
