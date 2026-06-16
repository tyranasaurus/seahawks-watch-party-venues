# Seahawks Watch Party — Eastside Venue Guide

A living, filterable guide to private/semi-private spots to watch a Seahawks game
with ~30 people on the Seattle Eastside (plus a few cross-lake options).

**Live page:** https://tyranasaurus.github.io/seahawks-watch-party-venues/

## Editing

`index.html` is the whole thing — venue data, styles, and logic in one file.
Edit it, commit, and push; GitHub Pages redeploys automatically in ~1 minute.

- Venue records live in the `const venues = [...]` array.
- Room photos are wired up in `const ROOM_PHOTOS = {...}` (keyed by venue name)
  and live in `images/`.
- Starred picks are listed in `const STARRED = [...]`.
