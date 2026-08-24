-- MIGRATION 2 — layout + subtitle controls for the admin tool
-- Run once in Supabase: Dashboard → SQL Editor → New query → paste → Run

alter table projects add column if not exists section_label text not null default 'Overview';
alter table projects add column if not exists gallery_columns int not null default 2;
alter table projects add column if not exists accent_color text not null default '#A16207';

-- Seed the outline colors currently hardcoded on each page
update projects set accent_color = '#55B83F' where slug = 'esu-farm';
update projects set accent_color = '#F04E23' where slug = 'summit-ct';
update projects set accent_color = '#A16207' where slug = 'williams-lea-gs';
update projects set accent_color = '#7B4FA8' where slug = 'shaashop';
