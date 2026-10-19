# Changelog

## 2026-10-20 — Playlist and mix controls fix

- Fixed the common redesigned playlist header, including mixes and header variants: when Spotify supplies both Add and Download, both now appear as separate glass buttons on the left, with Play on the right.
- Kept the independent action row stable across transient header model updates.
- Download uses Spotify’s existing action. No download button is fabricated when Spotify does not supply one.
- Preserved the existing row for own playlists and Liked Songs when the independent action pair is absent.
- Added playlist simulator fixture checks for narrow layouts and native action forwarding.

Local fixture results: mix, late-save and no-download variants passed. These are component checks; this source publication does not introduce a new IPA release.
