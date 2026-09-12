# projects.danielpokras.com

A cream-and-purple gallery for the photo albums. Every photo from every album,
grouped by album, with a lightbox — served from one static `index.html`. No
build step, no framework, no database.

Two pages, hash-routed: **Dinners** (`#/dinners`) and **Design** (`#/design`).

## How photos get here

They don't. Photos live on `photos.danielpokras.com` (the photo blog app) and
that stays the only place you upload. This site holds no image files at all:

- `photos.json` records which photos exist in which album
- the page points at the blog's image optimizer, which resizes and caches them
  (`/_next/image?url=...&w=1080`), so a 3MB original arrives as ~125KB

`photos.json` is rebuilt by `.github/workflows/manifest.yml` every day and on
demand (Actions tab → Rebuild photo manifest → Run workflow). Upload through
the admin as usual and the new photos appear here within a day, or immediately
if you run the workflow.

To rebuild by hand: `python3 tools/build-manifest.py`

## Adding an album

Add it to `tools/albums.json` with its slug, a `section` (`dinners` or
`design`) and the date to display, then rebuild. The album title and its
photos are read from the site — only the slug, section and date are set here,
because a dinner is remembered by the night it happened, not by when its
photos were uploaded.

## Deploying

Static hosting. On Vercel: import this repo, framework preset *Other*, no
build command, output directory `.`. This is a separate project from the
photo blog; the two share nothing but links.

## Editing the design

Everything is in `index.html`: palette tokens at the top of the `<style>`
block (`--ground`, `--paper`, `--ink`, `--violet`), then layout, then the
render script and lightbox. Light and dark are both defined.
