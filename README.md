# projects.danielpokras.com

A cream-and-purple front page for the photo albums. One card per album — cover
image, name, date, photo count — linking through to the full album on
`photos.danielpokras.com`, which runs the photo blog app.

Two pages, hash-routed: **Dinners** (`#/dinners`) and **Design** (`#/design`).
One static `index.html`. No build step, no framework, no database.

## Adding or changing an album card

Cards are plain HTML in `index.html` — copy an existing `<a class="album">`
block and edit four things: the `href` (the album URL), the cover image, the
title, and the meta line (date and photo count).

To grab a cover image from the photo blog:

1. Open the photo on `photos.danielpokras.com`, copy its image URL
   (a `blob.vercel-storage.com` address)
2. `curl -o images/covers/<name>.jpg "<that url>"`
3. `tools/resize.sh images/covers/<name>.jpg images/covers` — caps the long
   edge at 1600px and re-encodes, keeping the repo small. Uses `sips`, built
   into macOS.
4. Set the `width` and `height` attributes on the `<img>` to the resized
   dimensions, so the page doesn't jump while images load

Covers are copies, not live links — replacing a photo in the admin does not
update the card here.

## Deploying

Static hosting, free tier is plenty. On Vercel: New Project → import this repo
→ Framework preset *Other*, no build command, output directory `.` → Deploy,
then Settings → Domains → `projects.danielpokras.com`.

This is a separate Vercel project from the photo blob. The two sites share
nothing but links.

## Editing the design

Everything is in `index.html`: palette tokens at the top of the `<style>`
block (`--ground`, `--paper`, `--ink`, `--violet`), then layout, then a few
lines of routing script. Light and dark are both defined.
