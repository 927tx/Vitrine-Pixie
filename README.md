# Vitrine + Pixie Download Manager

Liquid Glass Spotify with **Pixie Download Manager**. Based on [Vitrine](https://github.com/My-Name-Is-Jeff/vitrine), with native offline downloads and a download manager.

**Pixie Manager: v1.2** · **Spotify version: 9.1.90** · **Maintainer: [Glongq](https://github.com/Glongq)**

## Downloads and updates

**[Download Spotify 9.1.90 + Pixie Manager — Telegram post](https://t.me/glongqforks/5)**

Download the IPA from the linked post. Updates and release announcements: [@glongqforks](https://t.me/glongqforks). This repository contains source code and patches; no IPA files are hosted here. GitHub's “Source code” archives are not installable apps.

**Jailbreak packages:** [rootless / rootful DEBs](https://github.com/Glongq/Vitrine-Pixie/releases/tag/pixie-9.1.90-jailbreak-1). The jailbreak build has **not been tested on a jailbroken device**; the regular IPA has been tested through LiveContainer and SideStore.

## Pixie

- Native offline downloads for tracks, albums and playlists.
- Download the album of the currently playing track from the manager.
- **Vitrine settings → Pixie Download Manager**: current-track actions, download status, optional diagnostics and journal/report export.
- English interface.
- Redesigned album controls, plus playlist and mix headers where Spotify supplies both Add and Download: Play on the right, separate glass controls on the left, horizontal scrolling when needed.
- Diagnostics can be switched off. WAV capture is disabled in release builds.

Music stays in **Spotify's offline storage**, for playback inside Spotify. Exporting ordinary MP3/M4A/OGG audio files is not implemented.

See [CHANGELOG.md](CHANGELOG.md) for source updates.

## Compatibility

The Pixie extension targets Spotify **9.1.90**, ARM64 UUID `fbce22c17e1b3e0d9be866ff9291943e`, with Vitrine **1.0.0-beta.13** as the base. The builder checks the executable UUID and instruction bytes. Other Spotify binaries require a separate port.

Native downloads and album controls were checked on an iPhone 15 Pro Max, iOS 27.0.1, using LiveContainer. Vitrine's Liquid Glass redesign requires iOS 26 or later. Long-term offline licence renewal has not been verified.

## Latest update — Pixie Manager v1.2

- Detailed diagnostic tracing runs only while diagnostics are enabled.
- Export diagnostics as one JSON file.
- Manage offline devices and remove selected devices to free download slots.

Local component tests and the settings simulator passed during development. The latest diagnostics changes have not yet been verified on an iPhone. The regular download baseline was tested through LiveContainer and SideStore.

The jailbreak DEBs linked above remain the **previous release**. They have not been rebuilt from v1.2 sources. See [CHANGELOG.md](CHANGELOG.md).

## Source and build

This is a compact source overlay: Pixie sources plus the changes to Vitrine, rather than a copy of its entire repository or Git history.

See [BUILD.md](BUILD.md) for the pinned upstream revision, patch application and build commands. [SOURCE.md](SOURCE.md) records authorship, scope and source hashes.

## Credits

A fork of **[My-Name-Is-Jeff/vitrine](https://github.com/My-Name-Is-Jeff/vitrine)**, itself based on [spoti.pw](https://github.com/skopevoj/spoti.pw). Vitrine and its contributors retain credit for the base tweak and redesign.

Pixie development, integration and builds: OpenAI Codex under Glongq's direction. Device testing and feedback: Glongq. The earlier download-manager work is available in [Glongq/EeveeSpotifyReincarnated](https://github.com/Glongq/EeveeSpotifyReincarnated).

[GPL-3.0](LICENSE). Existing source notices are retained.
