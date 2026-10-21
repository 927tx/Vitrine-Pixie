# Source provenance

Current source snapshot: **Pixie Manager v1.2**. The existing jailbreak release/tag retains its earlier source snapshot and DEB files.

- Base: [Vitrine](https://github.com/My-Name-Is-Jeff/vitrine), pinned to commit `914343731f66ccb2e639b8164a36be849a043276`.
- `patches/vitrine-pixie.patch`: the local changes against that exact revision. Vitrine's existing code remains under its original GPL-3.0 licence and authorship.
- `NativeDownloads/`: Pixie companion implementation, build patchers, jailbreak runtime/bootstrap and development fixtures, evolved from Glongq's EeveeSpotifyReincarnated extension and ported to Spotify 9.1.90 / Vitrine.
- Integration, development and builds: OpenAI Codex under Glongq's direction. Device testing: Glongq.
- `source-manifest.json`: SHA-256 hashes of the published source snapshot and documentation, generated before this provenance file and the manifest itself.

This snapshot excludes generated binaries, IPAs, personal/device logs, private signing files, dependency installations and the complete upstream Git checkout.
