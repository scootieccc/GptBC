# GptBC

**GptBC** is a Game Boy Color-first workflow assistant for **GB Studio** projects. It is distributed as a Codex plugin marketplace package and is designed to help creators catch asset problems, inspect project constraints, discover compatible GB Studio plugins/resources, and generate repeatable build-readiness reports.

GptBC favors **Game Boy Color / Color Only** workflows by default. It does not bundle third-party GB Studio plugins or art; it reads upstream sources and keeps third-party licensing and compatibility visible.

## Install from the Codex plugin marketplace UI

In Codex, open **Add plugin marketplace** and use:

```text
Source
https://github.com/scootieccc/GptBC

Git ref
main

Sparse paths
[leave completely blank]
```

Then choose **Add marketplace** and install **GptBC** from the imported marketplace.

The marketplace manifest is stored at:

```text
.agents/plugins/marketplace.json
```

and the installable plugin is stored at:

```text
plugins/gptbc/
```

See [docs/INSTALL.md](docs/INSTALL.md) for the full install, update, troubleshooting, and local-development workflow.

## What GptBC does

- Audits GB Studio projects with a GBC-first rule set.
- Detects `.gbsproj` files and attempts to identify GB Studio version and color mode.
- Checks background PNG dimensions, 8x8 alignment, native-screen sizing, tile counts, flip-equivalent tile counts, and automatic-palette pressure.
- Uses the Color Only 384-background-tile budget as the default GBC target.
- Checks sprite PNG alignment and canonical GB Studio source colors.
- Inventories project-local GB Studio plugins.
- Warns when multiple plugins appear to override the same engine file.
- Compares declared `gbsVersion` compatibility against the detected/selected GB Studio version.
- Searches the live official GB Studio plugin catalog.
- Installs selected official plugins with a backup-first workflow.
- Synchronizes approved GitHub/resource sources into a non-destructive local cache.
- Generates Markdown build-readiness reports.

## Current release

**GptBC 0.2.0**

Primary target:

```text
GB Studio 4.3.x
Game Boy Color
Color Only
Windows-first local workflow
```

GptBC is version-aware and is intended to expand support as GB Studio evolves. It will report uncertainty rather than silently assume a project setting when the project schema cannot be identified reliably.

## Python dependency

PNG-level image inspection uses Pillow:

```powershell
python -m pip install Pillow
```

Without Pillow, project/plugin metadata checks can still run, but image-level checks are skipped.

## Command-line usage

From the installed GptBC plugin directory, audit a project:

```powershell
python .\scripts\gptbc.py audit "C:\Games\MyGBStudioGame"
```

Generate a Markdown report:

```powershell
python .\scripts\gptbc.py report "C:\Games\MyGBStudioGame"
```

List official plugins compatible with GB Studio 4.3.2:

```powershell
python .\scripts\gptbc.py catalog --gbs-version 4.3.2
```

Search the official plugin catalog:

```powershell
python .\scripts\gptbc.py search "smooth fade" --gbs-version 4.3.2
```

Install an official plugin by exact repository ID:

```powershell
python .\scripts\gptbc.py install-plugin "pau-tomas/Smooth Fade" "C:\Games\MyGBStudioGame" --gbs-version 4.3.2
```

Synchronize enabled GitHub/resource sources into the project cache:

```powershell
python .\scripts\gptbc.py sync-resources "C:\Games\MyGBStudioGame"
```

The project-local cache is written under:

```text
<project>\.gptbc\resource-cache
```

GptBC does not automatically dump cached third-party packs into your project assets. The cache is intentionally separate so compatibility, licensing, duplicates, and project needs can be reviewed first.

## Why the plugin catalog is live

GptBC reads the official GB Studio repository index at:

```text
https://plugins.gbstudio.dev/repository.json
```

This keeps discovery aligned with upstream plugin metadata instead of maintaining a permanently frozen list inside GptBC.

Additional trusted resource sources can be configured in:

```text
references/resource-registry.json
```

## Repository layout

```text
GptBC/
├── .agents/plugins/marketplace.json
├── plugins/gptbc/
│   ├── .codex-plugin/plugin.json
│   ├── skills/
│   ├── scripts/
│   ├── references/
│   └── assets/
├── .github/
├── docs/
├── tests/
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
└── LICENSE
```

The top-level source files are retained for development/history, while `plugins/gptbc/` is the marketplace-installable package.

## Safety and project integrity

GptBC is intentionally conservative around GB Studio engine extensions. It does **not** install every available plugin automatically. Engine plugins can replace shared engine files, depend on specific GB Studio versions, or conflict with other extensions. GptBC therefore favors compatibility filtering, visible conflict warnings, project-local backups, and non-destructive resource caching.

## Contributing

Bug reports, compatibility findings, GB Studio resource suggestions, and pull requests are welcome. Start with [CONTRIBUTING.md](CONTRIBUTING.md).

For plugin/resource additions, include the upstream URL, license, supported GB Studio versions if known, and any engine-file or scanline-related compatibility concerns.

## Roadmap

Planned areas include deeper GB Studio 4.3 project-schema parsing, dialogue/font overflow checks, actor/sprite hardware-budget diagnostics, build-log and ROM-bank analysis, SameBoy test integration, GB Studio executable discovery, one-command build validation, stronger plugin conflict signatures, pinned resource revisions, and optional GIMP/Aseprite preprocessing workflows.

## License

GptBC is released under the [MIT License](LICENSE). Third-party GB Studio plugins, resource packs, and assets discovered by GptBC retain their own licenses and are not relicensed by this repository.
