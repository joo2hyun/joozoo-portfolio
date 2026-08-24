# Joohyun Kim — Portfolio

Live: https://joozoo.work

Static site (HTML/CSS/JS) with a Supabase-backed admin.

## Structure
- `index.html` — home
- `work-*.html` — project detail pages
- `admin-login.html` / `admin.html` — content admin (login required)
- `supabase-config.js` — Supabase project URL + public anon key
- `supabase-*.sql` — schema & migrations

## Editing content
Log in at `/admin-login.html`. Text, images, colors and page sections are
stored in Supabase, so content edits appear live without a redeploy.

## Deploying
Pushes to `main` auto-deploy to Netlify. Only code changes need a deploy.
