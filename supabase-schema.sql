-- Run this once in Supabase: Dashboard → SQL Editor → New query → paste → Run

create table projects (
  id uuid primary key default gen_random_uuid(),
  slug text unique not null,
  name text not null,
  client text not null default '',
  year text not null default '',
  category text not null default '',
  role text not null default 'Design',
  tags text[] not null default '{}',
  statement text not null default '',
  overview text not null default '',
  cover_class text not null default 'c1',
  cover_pattern text not null default 'cover-lines',
  hero_image_url text,
  gallery_image_urls text[] not null default '{}',
  sort_order int not null default 0,
  updated_at timestamptz not null default now()
);

-- Public (anonymous) visitors can only READ. Only a logged-in admin can write.
alter table projects enable row level security;

create policy "Anyone can read projects"
  on projects for select
  using (true);

create policy "Only logged-in users can insert"
  on projects for insert
  to authenticated
  with check (true);

create policy "Only logged-in users can update"
  on projects for update
  to authenticated
  using (true);

create policy "Only logged-in users can delete"
  on projects for delete
  to authenticated
  using (true);

-- Storage bucket for project images
insert into storage.buckets (id, name, public) values ('project-images', 'project-images', true);

create policy "Anyone can view project images"
  on storage.objects for select
  using (bucket_id = 'project-images');

create policy "Only logged-in users can upload project images"
  on storage.objects for insert
  to authenticated
  with check (bucket_id = 'project-images');

create policy "Only logged-in users can update project images"
  on storage.objects for update
  to authenticated
  using (bucket_id = 'project-images');

create policy "Only logged-in users can delete project images"
  on storage.objects for delete
  to authenticated
  using (bucket_id = 'project-images');

-- Seed the 4 existing projects with their current content
insert into projects (slug, name, client, year, category, role, tags, statement, overview, cover_class, cover_pattern, sort_order) values
('esu-farm', 'ESU Farm', 'ESU Farm', '2026', 'Branding, Marketing', 'Design', array['Branding','Marketing'], 'I led brand identity and marketing for ESU Farm.', '', 'c4', 'cover-lines', 1),
('summit-ct', 'Summit C&T', 'Summit C&T', '2026', 'CPG, Packaging', 'Design', array['CPG','Packaging'], 'I designed CPG packaging systems for Summit C&T.', '', 'c8', 'cover-grid', 2),
('williams-lea-gs', 'Williams Lea / GS', 'Williams Lea / GS', '2025', 'Presentation Design', 'Design', array['Presentation Design'], 'I created presentation design systems for Williams Lea and Goldman Sachs.', '', 'c1', 'cover-split', 3),
('shaashop', 'Shaashop', 'Shaashop', '2021', 'UI/UX, Marketing', 'Design', array['UI/UX','Marketing'], 'I designed the UI/UX and marketing assets for Shaashop.', '', 'c5', 'cover-lines', 4);
