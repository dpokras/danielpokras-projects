# projects.danielpokras.com

Two-page portfolio: **Dinners** (food photography) and **Design** (selected work).
One static `index.html` — no build step, no framework, no database.

## Adding photos in bulk

Filenames become the captions, so dropping a batch of files in is the whole job.

**Dinners** — `images/dinners/YYYY-MM-DD-title.jpg`
`2026-09-06-cacio-e-pepe.jpg` → *Cacio e pepe*, 6 Sep, grouped under September 2026.

**Design** — `images/design/YYYY-title--Kind.jpg`
`2026-ferment--Identity.jpg` → *Ferment*, 2026, Identity. The `--Kind` part is optional.

Three ways to upload:

1. **GitHub web** — open `images/dinners`, *Add file → Upload files*, drag in up to 100 at once, commit.
2. **Finder + git** — drop files into the folder, then `git add images && git commit -m "New dinners" && git push`.
3. **Resize first** (recommended, keeps the repo small):
   `tools/resize.sh ~/Pictures/dinners/*.jpg images/dinners`
   Caps the long edge at 2000px and re-encodes as JPEG. Uses `sips`, built into macOS.

On every push, the GitHub Action in `.github/workflows/manifest.yml` regenerates `photos.json`
and the site picks up the new photos. Until any real photos exist, the page shows sample
entries so the layout is visible.

### Nicer captions without renaming files

Add entries to `captions.json`, keyed by path. They override anything derived from the filename:

```json
{
  "images/dinners/2026-09-06-cacio-e-pepe.jpg": {
    "title": "Cacio e pepe",
    "note": "Too much pepper, on purpose."
  }
}
```

## Deploying

Static hosting, free tier is plenty:

- **Vercel** (already hosts `photos.danielpokras.com`) — New Project → import this repo →
  Framework preset *Other*, no build command, output directory `.` → Deploy.
  Then Project → Settings → Domains → add `projects.danielpokras.com`. DNS is already
  on Vercel nameservers, so the record is created for you.
- **Cloudflare Pages** works identically if you'd rather keep it off Vercel.

Both are $0 at this size. The only cost is the domain you already own.

## Editing the design

Everything lives in `index.html`: palette tokens at the top of the `<style>` block
(`--ground`, `--paper`, `--ink`, `--violet`), then layout, then the render script.
