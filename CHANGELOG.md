# Changelog

## 2026-10-20 — Local files fix and jailbreak packages

- Fixed a crash while resolving cover artwork for local tracks when Spotify receives malformed or unrelated metadata URLs. Valid local paths, file URLs and local-image URIs remain supported.
- Added rootless and rootful jailbreak packages, runtime patch guards, initialization and package build sources.
- Pixie currently uses an English interface.
- Regular IPA: tested through LiveContainer and SideStore. Jailbreak DEBs: local package, signature and patch-engine checks passed; execution on a jailbroken device is **not tested**.
- The local-cover resolver fixture covers malformed URLs, valid artwork paths, fallback metadata and edited artwork precedence.
- The jailbreak DEB does not include the IPA-only Live Activity / App Intents extension.

## 2026-10-20 — Playlist and mix controls fix

- Fixed the common redesigned playlist header, including mixes and header variants: when Spotify supplies both Add and Download, both now appear as separate glass buttons on the left, with Play on the right.
- Kept the independent action row stable across transient header model updates.
- Download uses Spotify’s existing action. No download button is fabricated when Spotify does not supply one.
- Preserved the existing row for own playlists and Liked Songs when the independent action pair is absent.
- Added playlist simulator fixture checks for narrow layouts and native action forwarding.

Local fixture results: mix, late-save and no-download variants passed. These are component checks; this source publication does not introduce a new IPA release.
