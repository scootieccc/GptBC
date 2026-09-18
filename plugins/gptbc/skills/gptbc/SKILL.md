---
name: gptbc
description: GBC-first GB Studio workflow skill. Use for GB Studio project inspection, asset QA, Color Only optimization, plugin/resource discovery, compatibility analysis, project linting, build-readiness checks, and release preparation. Prefer Game Boy Color capabilities unless the user explicitly requests DMG/monochrome compatibility.
---

# GptBC

Use this skill for GB Studio work where project quality, hardware constraints, plugin compatibility, assets, or release readiness matter.

## Default stance

- Prefer **Game Boy Color / Color Only** unless the user explicitly requests DMG compatibility.
- Target GB Studio **4.3.x** first, but inspect the project's actual version before applying version-sensitive advice.
- Never modify the user's `.gbsproj`, engine files, plugin folders, or source assets destructively without an explicit request.
- Before installing or updating plugins, make a project-local backup of the affected `plugins/` directory.
- Treat engine plugins as higher risk than event plugins or asset packs.
- Detect conflicts involving shared engine files, scanline interrupts, palette/UI assumptions, and scene-type replacements.
- Prefer official GB Studio plugins when equivalent functionality exists.
- Do not redistribute third-party assets or plugins inside GptBC. Fetch from upstream sources and preserve license metadata.

## Primary workflow

1. Locate the `.gbsproj`.
2. Run:
   `python scripts/gptbc.py audit <project-folder>`
3. Read the generated report and resolve errors before warnings.
4. Sync approved GitHub/resource sources when fresh packs are needed:
   `python scripts/gptbc.py sync-resources <project-folder>`
5. For plugin discovery:
   `python scripts/gptbc.py catalog --gbs-version 4.3.2`
6. Search by need:
   `python scripts/gptbc.py search "smooth fade" --gbs-version 4.3.2`
7. Install only after checking compatibility and conflict notes:
   `python scripts/gptbc.py install-plugin "<plugin id>" <project-folder> --gbs-version 4.3.2`
8. Re-run the audit after plugin or asset changes.
9. For release handoff, run:
   `python scripts/gptbc.py report <project-folder> --out GptBC_BUILD_REPORT.md`

## GBC quality priorities

- Color Only mode where appropriate.
- Background tile budget: 384 unique 8x8 tiles per scene for Color Only.
- Up to 8 background palettes and 8 sprite palettes; preserve UI/dialogue palette behavior.
- Favor automatic tile flipping when it materially reduces Color Only tile usage.
- Validate automatic-palette images per 8x8 tile and scene-level palette-set counts.
- Warn when artwork is technically valid but inefficient for VRAM/tile reuse.
- Treat 160x144 as the native screen and preview target.
- Prefer nearest-neighbor transformations; never introduce resampling blur into pixel art.
- Flag non-grid background dimensions and suspicious sprite dimensions.
- Surface likely scanline/engine conflicts before recommending plugins.

## Plugin/resource policy

The live official plugin catalog is:
`https://plugins.gbstudio.dev/repository.json`

GptBC may also index user-added GitHub resource repositories through:
`references/resource-registry.json`

Do not claim a community plugin is compatible unless its metadata or project files support that conclusion. If a repository is archived, label it legacy/read-only.

## When generating or editing assets

- Backgrounds: align to 8x8 tiles.
- Pixel art: nearest-neighbor only.
- For GB Studio manual background palettes, honor the canonical GB Studio source colors.
- For sprites, honor GB Studio sprite source-color rules and transparent key behavior.
- When the user supplies a full-color source intended for automatic palettes, check per-tile 4-color limits and total palette-set pressure.

## Output style

For audits, present:
- blockers
- warnings
- optimization opportunities
- installed plugin inventory
- recommended next actions

Do not hide uncertainty. If the `.gbsproj` schema does not expose a setting reliably, say it was not detected rather than guessing.
