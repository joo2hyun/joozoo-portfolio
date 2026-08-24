-- MIGRATION 4 — project description (paragraph under the title)
-- Run once in Supabase: Dashboard → SQL Editor → New query → paste → Run

alter table projects add column if not exists description text not null default '';
