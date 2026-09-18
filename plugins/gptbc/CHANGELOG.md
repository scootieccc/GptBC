# Changelog

## 0.3.0 — 2026-09-18

- Added a built-in curated catalog of 73 canonical public GitHub repositories relevant to GB Studio creation.
- Added resource commands for listing, recommending, syncing, inspecting and importing selected assets.
- Added project-local GitHub resource caching under `.gptbc/resource-cache`.
- Added safe asset destination mapping for backgrounds, sprites, fonts, music, sounds, avatars, emotes and UI.
- Added GBC-first PNG validation before import, including 8x8 alignment, Color Only tile-budget checks and sprite source-color checks.
- Added license-aware imports; unknown/NOASSERTION licenses are blocked by default.
- Added archived-repository opt-in behavior.
- Added overwrite protection and automatic asset backups.
- Added per-import provenance logging with repository URL, commit SHA, license, source path, checksum and destination.
- Added protection against importing executable/script payloads as ordinary assets.
- Updated Codex skill behavior and marketplace metadata for curated resource discovery/import.

## 0.2.0 — 2026-09-18

- Added GitHub/resource-pack cache synchronization.
- Added cached copy support for the live official GB Studio plugin repository.
- Added project-local or user-level cache targeting.
- Preserved archived repositories as opt-in only.

## 0.1.0 — 2026-09-18

- Initial GptBC Codex plugin.
- GBC-first GB Studio project audit.
- Background/sprite image validation.
- Live official GB Studio plugin catalog/search.
- Compatibility-filtered plugin install with backups.
- Duplicate engine override detection.
- Markdown build-readiness reports.
- Extensible GitHub/resource registry.
