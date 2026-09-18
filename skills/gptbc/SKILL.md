---
name: gptbc
description: GBC-first GB Studio workflow skill. Use for GB Studio project inspection, asset QA, Color Only optimization, plugin/resource discovery, compatibility analysis, safe curated asset import, project linting, build-readiness checks, and release preparation. Prefer Game Boy Color capabilities unless the user explicitly requests DMG/monochrome compatibility.
---

# GptBC

Use this skill for GB Studio work where project quality, hardware constraints, plugins, assets, reusable resources, or release readiness matter.

## Default stance

- Prefer **Game Boy Color / Color Only** unless the user explicitly requests DMG compatibility.
- Target GB Studio **4.3.x** first, but inspect the project's actual version before applying version-sensitive advice.
- Never modify the user's `.gbsproj`, engine files, plugin folders, or source assets destructively without an explicit request.
- Back up files before overwrite/import replacement.
- Treat engine plugins as higher risk than event plugins or ordinary asset packs.
- Prefer official GB Studio resources when an equivalent exists.
- Do not redistribute third-party assets inside GptBC. Fetch from upstream and preserve license/provenance.

## Curated resource behavior

GptBC includes a deduplicated curated catalog of public GitHub repositories useful for GB Studio game creation. The catalog was built from the project's curated spreadsheet and includes canonical asset packs, fonts, palettes, templates, plugins, audio/art tools, examples, and workflow resources.

When a user asks for assets/resources:

1. Search the curated catalog first.
2. Prefer canonical repositories over mirrors/forks.
3. Prefer official/creator-maintained sources where practical.
4. Sync only repositories relevant to the request; do not clone all sources blindly.
5. Inspect the upstream GitHub license before copying any file into a GB Studio project.
6. If GitHub reports no license or `NOASSERTION`, do not import automatically. Tell the user the license must be reviewed; only proceed with explicit approval and `--allow-unverified-license` when reuse is actually permitted.
7. Do not execute downloaded third-party binaries or scripts as part of asset import.
8. For plugins/engine extensions, use plugin-specific installation and compatibility checks rather than treating them as ordinary assets.
9. Record repository URL, source path, commit SHA, detected license, destination, checksum, and validation result for every imported asset.
10. Default imports to GBC Color Only constraints and validate graphics before placement.

## Resource commands

The marketplace package exposes resource management through the PowerShell wrapper:

`./scripts/gptbc.ps1 resources list`

Search/list curated resources:

`./scripts/gptbc.ps1 resources list --query "sprites"`

Recommend resources for a particular need:

`./scripts/gptbc.ps1 resources recommend "GBC backgrounds and UI" --live`

Clone/update one approved repository into the project-local cache:

`./scripts/gptbc.ps1 resources sync "DeerTears/GB-Studio-Community-Assets" <project-folder> --include-archived`

Inspect candidate files before import:

`./scripts/gptbc.ps1 resources inspect "DeerTears/GB-Studio-Community-Assets" <project-folder> --kind backgrounds --include-archived`

Import one reviewed file:

`./scripts/gptbc.ps1 resources import "OWNER/REPO" "path/in/repo/file.png" <project-folder> --dest-type backgrounds`

Use `--overwrite` only when replacement is intended; GptBC backs up the existing project asset first.

Use `--force` only after reviewing a graphics-validation error.

## Supported asset destinations

GptBC can place reviewed assets into these common GB Studio project paths:

- `assets/backgrounds`
- `assets/sprites`
- `assets/fonts`
- `assets/music`
- `assets/sounds`
- `assets/avatars`
- `assets/emotes`
- `assets/ui`

Ambiguous PNGs require an explicit `--dest-type` rather than guessing.

## GBC validation before import

- Backgrounds should align to 8x8 tiles.
- Native screen target is 160x144.
- GBC Color Only background target is 384 unique 8x8 tiles, considering flip equivalence.
- Large backgrounds are checked against GB Studio dimension/area limits.
- Sprite source art is checked against canonical GB Studio source colors and specifically flags `#306850`.
- Pixel art is copied byte-for-byte; GptBC does not resample or blur source images during import.

## Provenance and backups

Imported files are logged to:

`<project>/.gptbc/provenance/imports.jsonl`

Cached repositories live under:

`<project>/.gptbc/resource-cache/`

Overwritten assets are backed up under:

`<project>/.gptbc/backups/assets/`

## Primary project workflow

1. Locate the `.gbsproj`.
2. Run `python scripts/gptbc.py audit <project-folder>`.
3. Resolve blockers before warnings.
4. Discover curated resources with `gptbc.ps1 resources recommend ...`.
5. Inspect a resource before import.
6. Import only selected files with acceptable reuse terms.
7. For GB Studio plugins, use the live official plugin catalog and compatibility checks.
8. Re-run the project audit after imports or plugin changes.
9. Generate `GptBC_BUILD_REPORT.md` for release preparation.

## Plugin/resource policy

The live official GB Studio plugin catalog is:
`https://plugins.gbstudio.dev/repository.json`

The curated resource catalog supplements that live plugin catalog. Do not claim a community plugin is compatible unless metadata/source supports that conclusion. Archived repositories are excluded by default and require an explicit opt-in.

## Output style

For audits and resource imports, present blockers, warnings, provenance/license status, optimization opportunities, and recommended next actions. Never imply an unclear license is automatically safe to reuse.
