-- MIGRATION 3 — content blocks (page builder)
-- Run once in Supabase: Dashboard → SQL Editor → New query → paste → Run

alter table projects add column if not exists content_blocks jsonb not null default '[]'::jsonb;
