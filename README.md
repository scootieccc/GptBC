![GptBC banner](https://github.com/scootieccc/GptBC/raw/main/assets/gptbc-banner.jpg)

<p align="center">
  <img src="https://raw.githubusercontent.com/scootieccc/GptBC/main/assets/gptbc-icon.svg" alt="GptBC icon" width="128">
</p>

<h1 align="center">GptBC</h1>

<p align="center"><strong>GBC-first tooling, resource discovery, asset QA, and release checks for GB Studio.</strong></p>

**GptBC** is a Game Boy Color-first workflow assistant for **GB Studio** projects, distributed as a public Codex plugin marketplace package. It helps creators audit projects, validate GBC assets, discover compatible plugins, find reusable public resources, safely import selected upstream assets, and generate build-readiness reports.

> **Independent project:** GptBC is not affiliated with, sponsored by, or endorsed by Nintendo, GB Studio, or OpenAI. Product names and trademarks belong to their respective owners.

## Install from Codex

In **Add plugin marketplace**, use:

```text
Source
https://github.com/scootieccc/GptBC

Git ref
main

Sparse paths
[leave completely blank]
```

Then choose **Add marketplace** and install **GptBC** from the imported marketplace.

The public marketplace manifest is:

```text
.agents/plugins/marketplace.json
```

The installable plugin package is:

```text
plugins/gptbc/
```

For detailed setup and troubleshooting, see [docs/INSTALL.md](docs/INSTALL.md).

## Current release

**GptBC 0.3.0**

Primary target:

```text
GB Studio 4.3.x
Game Boy Color
Color Only
Windows-first local workflow
```

## What GptBC does

- Audits GB Studio projects with a GBC-first rule set.
- Checks native 160x144 targeting and 8x8 tile alignment.
- Measures Color Only background tile usage and flip-equivalent tile savings.
- Checks background size limits, sprite source colors, and palette pressure.
- Inventories project-local GB Studio plugins and flags likely engine-file collisions.
- Searches the live official GB Studio plugin repository with version filtering.
- Installs selected official plugins with backup-first behavior.
- Discovers curated public GitHub resources for GB Studio creation.
- Safely caches, inspects, and imports selected third-party assets with provenance records.
- Generates repeatable build-readiness reports.

## Curated GB Studio resource importer

GptBC includes a deduplicated catalog of **73 canonical public GitHub repositories** selected from the project's curated GB Studio resource research. It covers asset packs, backgrounds/sprites, fonts, palettes, music/SFX tooling, templates, examples, plugins, engine extensions, and workflow tools.

GptBC does **not** bundle or relicense third-party assets. It pulls selected resources from upstream GitHub repositories and keeps their original licensing visible.

### Resource commands

From the installed plugin directory:

```powershell
.\scripts\gptbc.ps1 resources list
```

Search the catalog:

```powershell
.\scripts\gptbc.ps1 resources list --query "fonts"
```

Get recommendations:

```powershell
.\scripts\gptbc.ps1 resources recommend "GBC backgrounds UI sprites" --live
```

Sync one curated repository into the project-local cache:

```powershell
.\scripts\gptbc.ps1 resources sync "OWNER/REPO" "C:\Games\MyGBStudioGame"
```

Inspect importable assets:

```powershell
.\scripts\gptbc.ps1 resources inspect "OWNER/REPO" "C:\Games\MyGBStudioGame"
```

Filter candidates:

```powershell
.\scripts\gptbc.ps1 resources inspect "OWNER/REPO" "C:\Games\MyGBStudioGame" --kind backgrounds
```

Import a selected asset:

```powershell
.\scripts\gptbc.ps1 resources import "OWNER/REPO" "path/in/repo/file.png" "C:\Games\MyGBStudioGame" --dest-type backgrounds
```

### Import safeguards

Before copying a third-party asset into a project, GptBC:

- requires the repository to be in the curated canonical catalog;
- checks current public GitHub repository metadata;
- excludes archived repositories by default;
- blocks executable/script payloads from the ordinary asset importer;
- checks the upstream GitHub license and blocks automatic import for `UNKNOWN` / `NOASSERTION` unless reuse rights have been separately verified;
- validates PNGs against GBC/GB Studio constraints where applicable;
- requires an explicit destination for ambiguous PNGs;
- refuses accidental overwrite by default;
- backs up replaced project assets when `--overwrite` is used;
- records repository URL, commit SHA, license, source path, checksum, and destination in a provenance log.

Imported-resource provenance is stored at:

```text
<project>\.gptbc\provenance\imports.jsonl
```

Repository caches are stored at:

```text
<project>\.gptbc\resource-cache\
```

Backups are stored at:

```text
<project>\.gptbc\backups\assets\
```

### Supported asset destinations

```text
assets/backgrounds
assets/sprites
assets/fonts
assets/music
assets/sounds
assets/avatars
assets/emotes
assets/ui
```

Plugin repositories remain subject to plugin-specific compatibility checks and are **not** blindly copied into project asset folders.

## GBC-first validation

GptBC favors **Game Boy Color / Color Only** workflows by default and checks, where applicable:

- 160x144 native screen target
- 8x8 tile alignment
- Color Only 384-background-tile budget
- flip-equivalent tile usage
- background size limits
- sprite source colors
- palette pressure
- duplicate plugin engine overrides
- declared GB Studio plugin compatibility

PNG inspection uses Pillow:

```powershell
python -m pip install Pillow
```

## Project commands

Audit a project:

```powershell
python .\scripts\gptbc.py audit "C:\Games\MyGBStudioGame"
```

Generate a build-readiness report:

```powershell
python .\scripts\gptbc.py report "C:\Games\MyGBStudioGame"
```

Search the official GB Studio plugin repository:

```powershell
python .\scripts\gptbc.py search "smooth fade" --gbs-version 4.3.2
```

Install an official plugin with backup-first behavior:

```powershell
python .\scripts\gptbc.py install-plugin "<plugin id>" "C:\Games\MyGBStudioGame" --gbs-version 4.3.2
```

## Repository layout

```text
GptBC/
├── .agents/plugins/marketplace.json
├── plugins/gptbc/
│   ├── .codex-plugin/plugin.json
│   ├── skills/gptbc/SKILL.md
│   ├── scripts/gptbc.py
│   ├── scripts/resources.py
│   ├── scripts/gptbc.ps1
│   ├── references/
│   └── assets/
├── docs/
├── tests/
├── CHANGELOG.md
├── CONTRIBUTING.md
├── PRIVACY.md
├── SECURITY.md
├── TERMS.md
└── LICENSE
```

## Safety, trust, and licensing

"Curated" means a repository is a selected public upstream source relevant to GB Studio and deduplicated against known mirrors. It does **not** mean GptBC grants rights to every file or guarantees third-party code is defect-free.

GptBC never treats a missing license as permission. Users remain responsible for complying with upstream licenses, attribution requirements, and asset-specific terms.

For project policies, see [Privacy](PRIVACY.md), [Terms](TERMS.md), and [Security](SECURITY.md).

## Contributing

Bug reports, compatibility findings, resource suggestions, and pull requests are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

GptBC itself is MIT-licensed. Third-party resources discovered or imported through GptBC retain their own licenses and are never relicensed by GptBC.
