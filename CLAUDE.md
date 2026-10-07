# danielpokras-projects — cream-and-purple gallery

Static site for `projects.danielpokras.com` (and `danielpokras.com` /
`www.danielpokras.com`, which 307-redirect there at the Vercel domain level —
that redirect is set on the *other* project, not in this repo). No build
step, no framework, no database — just `index.html`.

Full cross-project context (the photo blog, how photos flow, env vars, etc.)
lives one level up in `../CLAUDE.md`. This file covers what's needed when
working inside *this* repo specifically.

## Layout

- `index.html` — the whole site. Palette tokens at the top of `<style>`
  (`--ground`, `--paper`, `--ink`, `--violet`), then layout, then the render
  script and lightbox. Light and dark themes both defined. Two pages,
  hash-routed: `#/dinners`, `#/design`.
- `tools/albums.json` — per-album `slug`, `section` (`dinners`/`design`),
  `date`, `blurb`. Blurbs accept `[label](url)` links, built as real anchor
  nodes, never injected as markup. **This is where blurbs/dates are edited.**
- `tools/build-manifest.py` — regenerates `photos.json`. Run with
  `python3 tools/build-manifest.py`.
- `photos.json` — generated from the live photo blog's album pages. Don't
  hand-edit; rebuild instead.
- `.github/workflows/manifest.yml` — rebuilds `photos.json` daily (05:00 UTC)
  and on demand (Actions → Rebuild photo manifest → Run workflow).

## Where photos actually come from

This repo stores **no image files**. Photos live on `photos.danielpokras.com`
(Vercel Blob) and are uploaded there via `/admin`. This site just lists which
photos exist in which album (`photos.json`) and requests them through the
blog's image optimizer (`/_next/image?url=<blob url>&w=1080&q=75`), which
resizes/caches — a 3.8MB original arrives as ~125KB. Blob URLs send
`access-control-allow-origin: *`, which is what makes the cross-domain
hotlinking work.

Album **titles** come from the album records on the photo blog (renaming in
`/admin` updates this site automatically on next manifest rebuild). Dates and
blurbs are set by hand in `tools/albums.json` here, because e.g. a dinner is
remembered by the night it happened, not by when its photos were uploaded.

To add an album: create it in `/admin` on the photo blog → add
slug/section/date/blurb to `tools/albums.json` → `python3
tools/build-manifest.py` → push.

## Deploying

Vercel project, framework preset *Other*, no build command, output directory
`.`. Push to `main` deploys. Separate Vercel project from the photo blog — the
two share nothing but links.

## Known quirks

- **Edge cache.** For up to a minute after a deploy, Vercel may serve the
  previous version from some edge locations and the new one from others.
  Verify with a cache-busting query (`?v=123`) and check more than once.
- No local clone of the photo blog repo (`photography_portfolio`, private).
  Clone it separately if that side needs work.

## Content as of October 2026

45 photos across five albums: Bonsai Lamp (design, 10), Silk Road Dinner (11),
Earth Beneath Us Dinner (10), Colors Dinner (11), Korean Buddhist Food Dinner
(3). Dolomites 2025 (9 photos, tag `favs`) exists on the photo blog but
appears on neither site.

## Open items

- `Airas Sanchez Keller`, credited in the Silk Road blurb — spelling
  unconfirmed with Daniel.
- The Silk Road map (plant domestication along the route, designed by Airas)
  would make a good lead image for that album if the file turns up.
- The **Colors** and **Korean Buddhist Food** blurbs were drafted by Claude
  from the album names, not from Daniel's account of the evenings. Silk Road,
  Earth Beneath Us and Bonsai Lamp are his.
