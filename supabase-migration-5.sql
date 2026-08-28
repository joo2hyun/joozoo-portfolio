-- MIGRATION 5 — bring the project rows in line with the finished pages
-- Run once in Supabase: Dashboard → SQL Editor → New query → paste → Run
--
-- The rows still held the placeholder copy from the original seed, and the
-- detail pages let a DB value win over the static HTML — so a finished case
-- study was rendering with its old year, role and statement. This makes the
-- rows say what the pages say.

-- SUMMIT C&T — built from the design handoff, two brands in one engagement
update projects set
  client      = 'Summit C&T LLC',
  year        = '2025 — 2026',
  category    = 'Brand Design, Packaging',
  role        = 'Brand & Packaging Designer',
  tags        = array['Brand Design','Packaging','Retail Content'],
  statement   = 'One brand built from nothing, one brand helped onto Amazon.',
  description = 'In-house design at a Korean food importer in New Jersey — building HOXY, the company''s own brand, from packaging to trade-show booth, and running Amazon marketing for Gung Jeon Bang, a partner rice-cake maker.',
  overview    = 'Summit C&T imports and distributes Korean pantry goods across the US. HOXY is its own brand, and I designed it end to end — a yellow speech-bubble mark and noodle character carried through seasoning pouches, ramen cartons, display shippers, Amazon listings and booths at KeHE and Fancy Food. Gung Jeon Bang is a separate rice-cake maker, in business since 1983, whose US launch we supported: there the work was Amazon marketing — A+ content and listing art direction inside their existing brand, not a rebrand of it.',
  hero_image_url = 'assets/summit-ct/hero-table-spread.webp',
  updated_at  = now()
where slug = 'summit-ct';

-- WILLIAMS LEA / GS — the row lagged the page on client, category and role
update projects set
  client      = 'Williams Lea / Goldman Sachs',
  year        = '2023 — 2024',
  category    = 'Presentation Design, Brand Systems',
  role        = 'Presentation Designer',
  tags        = array['Presentation Design','Brand Systems'],
  description = 'Presentation design on the Goldman Sachs account — pitchbook templates, cover and section systems, and an infographic library built to survive the deal desk.',
  updated_at  = now()
where slug = 'williams-lea-gs';

-- SHAASHOP — role and copy are already current; only the intro was missing
update projects set
  description = 'Design for a global e-commerce platform built around cross-border buying — landing pages, banners, posters, and the deck template behind its IR pitches.',
  updated_at  = now()
where slug = 'shaashop';

-- Check the result
select slug, client, year, category, role, tags, hero_image_url from projects order by sort_order;
