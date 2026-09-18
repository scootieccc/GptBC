# GptBC

**GptBC** is a GBC-first Codex plugin for improving GB Studio workflow and output quality.

It does **not** bundle other developers' plugins or art. Instead, it reads the live official GB Studio plugin repository and can install compatible upstream plugins into a project after making a backup.

## Goals

- Prefer Game Boy Color / **Color Only** workflows.
- Catch broken or inefficient assets before they become build problems.
- Search the current GB Studio plugin ecosystem instead of relying on a stale hard-coded list.
- Surface plugin/engine conflicts.
- Keep installs non-destructive and license-aware.
- Produce a repeatable release-readiness report.

## Current features (0.2.0)

- Codex plugin manifest and `gptbc` skill.
- `.gbsproj` discovery and version/color-mode heuristics.
- Background PNG checks:
  - 8x8 alignment
  - 160x144 native-screen minimum warning
  - maximum dimensions/area
  - exact and flip-equivalent tile counts
  - Color Only 384-tile budget
  - automatic-palette per-tile 4-color checks
  - scene palette-set pressure warning
- Sprite PNG checks:
  - 8px alignment warning
  - canonical GB Studio source-color validation
  - explicit `#306850` error
- Project-local GB Studio plugin inventory.
- Duplicate engine override detection.
- Declared `gbsVersion` compatibility checks.
- Live official catalog/search.
- Safe upstream ZIP extraction.
- Backup-before-install behavior.
- Markdown build-readiness report.
- Extensible upstream resource registry.
- GitHub/resource-pack sync into a non-destructive local cache.

## Install as a personal Codex plugin on Windows

Extract this folder, open PowerShell inside it, then run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install-personal.ps1
```

Restart Codex after installation.

The personal plugin lives at:

```text
%USERPROFILE%\plugins\gptbc
```

and is added to:

```text
%USERPROFILE%\.agents\plugins\marketplace.json
```

## Python dependency

For image inspection:

```powershell
python -m pip install Pillow
```

Without Pillow, project/plugin metadata checks still work, but PNG-level checks are skipped.

## Commands

Audit a project:

```powershell
python .\scripts\gptbc.py audit "C:\Games\WaffleHole"
```

Create a Markdown report:

```powershell
python .\scripts\gptbc.py report "C:\Games\WaffleHole"
```

Show plugins compatible with GB Studio 4.3.2:

```powershell
python .\scripts\gptbc.py catalog --gbs-version 4.3.2
```

Search:

```powershell
python .\scripts\gptbc.py search "smooth fade" --gbs-version 4.3.2
```

Install by exact official repository ID:

```powershell
python .\scripts\gptbc.py install-plugin "pau-tomas/Smooth Fade" "C:\Games\WaffleHole" --gbs-version 4.3.2
```

Sync enabled GitHub resource packs and the live official catalog into the project cache:

```powershell
python .\scripts\gptbc.py sync-resources "C:\Games\WaffleHole"
```

The cache is written under:

```text
<project>\.gptbc\resource-cache
```

GptBC never copies those cached packs into `assets/` automatically; Codex can inspect the pack, license, and project needs first.

## Why the plugin catalog is live

GB Studio 4.2+ uses the official plugin repository at:

```text
https://plugins.gbstudio.dev/repository.json
```

That repository contains plugin type, author, version, `gbsVersion`, license, ID, and ZIP path. GptBC queries it at runtime so "available plugins" tracks upstream changes.

## Resource packs

Edit:

```text
references/resource-registry.json
```

to add GitHub repositories or other indexes you trust. GptBC currently treats the official GB Studio catalog as authoritative for installable plugins and other GitHub sources as resource references.

## Roadmap

- Parse more of the GB Studio 4.3 project schema directly.
- Dialogue/font overflow heuristics.
- Scene-level actor/sprite budget checks.
- ROM/bank usage parsing from build logs.
- SameBoy test-run integration.
- GB Studio executable discovery and one-command build.
- Per-plugin conflict signatures (scanline IRQ, scene-type replacement, core engine override).
- GitHub resource-pack cache with pinned commits and license manifest.
- Optional GIMP/Aseprite asset preprocessing profiles.
- GBC palette harmonization and palette reuse suggestions.
- CI workflow for GB Studio project audits.

## Important

GptBC intentionally avoids automatically installing every plugin. Engine plugins can replace the same files or compete for scanline interrupts, and indiscriminate installation would reduce build quality rather than improve it. The tool indexes broadly, filters for compatibility, and installs selectively.
