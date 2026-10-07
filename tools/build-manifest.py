#!/usr/bin/env python3
"""Rebuild photos.json by reading the public album pages on the photo blog.

The photo blog is the only place photos live; this just records which ones
exist so the static site can lay them out. Image bytes are never copied—the
page points at the blog's image optimizer, which resizes and caches them.

Usage: python3 tools/build-manifest.py
"""
import json
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone

CONFIG = 'tools/albums.json'
OUTPUT = 'photos.json'
TIMEOUT = 30


def fetch(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'album-manifest'})
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        return response.read().decode('utf-8', 'replace')


def unique(values):
    seen = []
    for value in values:
        if value not in seen:
            seen.append(value)
    return seen


def blob_url_for_photo(site, slug, photo_id):
    """Fall back to the photo's own page when an album page comes up short."""
    html = fetch(f'{site}/album/{slug}/{photo_id}')
    urls = re.findall(r'https://[a-z0-9]+\.public\.blob\.vercel-storage\.com/[^"&\\]+', html)
    return urls[0] if urls else None


def build_album(site, album):
    slug = album['slug']
    html = fetch(f'{site}/album/{slug}')

    title_match = re.search(r'<title>([^<]*)</title>', html)
    title = re.sub(r'\s*\(\d+ Photos?\)\s*$', '', title_match.group(1)) if title_match else slug

    photo_ids = unique(re.findall(rf'href="/album/{re.escape(slug)}/([A-Za-z0-9_-]{{6,}})"', html))

    # Album pages carry each photo's image URL in document order, so one
    # request usually covers the whole album.
    encoded = unique(re.findall(r'url=(https%3A%2F%2F[^&"]+)', html))
    blob_urls = [urllib.parse.unquote(url) for url in encoded]

    if len(blob_urls) != len(photo_ids):
        print(f'  {slug}: pairing by page ({len(blob_urls)} urls vs '
              f'{len(photo_ids)} ids)', file=sys.stderr)
        blob_urls = [blob_url_for_photo(site, slug, photo_id) for photo_id in photo_ids]

    photos = [
        {'id': photo_id, 'src': blob_url}
        for photo_id, blob_url in zip(photo_ids, blob_urls)
        if blob_url
    ]

    print(f'  {slug}: {len(photos)} photos', file=sys.stderr)
    return {
        'slug': slug,
        'title': title,
        'section': album['section'],
        'date': album['date'],
        'blurb': album.get('blurb', ''),
        'photos': photos,
    }


def main():
    with open(CONFIG) as config_file:
        config = json.load(config_file)

    site = config['site'].rstrip('/')
    albums = [build_album(site, album) for album in config['albums']]

    missing = [album['slug'] for album in albums if not album['photos']]
    if missing:
        # Better to keep the last good manifest than publish empty albums.
        print(f'error: no photos found for {", ".join(missing)}', file=sys.stderr)
        return 1

    manifest = {
        'site': site,
        'generated': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'albums': albums,
    }
    with open(OUTPUT, 'w') as output_file:
        json.dump(manifest, output_file, indent=2)
        output_file.write('\n')

    total = sum(len(album['photos']) for album in albums)
    print(f'{OUTPUT}: {len(albums)} albums, {total} photos', file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main())
