# Installing GptBC

GptBC is distributed as a Codex plugin marketplace hosted on GitHub.

## Marketplace install

Open **Add plugin marketplace** in Codex and enter:

```text
Source
https://github.com/scootieccc/GptBC

Git ref
main

Sparse paths
[leave blank]
```

Choose **Add marketplace**, then install **GptBC** from the imported marketplace.

Do not enter `plugins/gptbc`, `plugins/codex`, or any other value in **Sparse paths** for the standard installation. The marketplace manifest is located at the repository root under `.agents/plugins/marketplace.json`, so Codex needs the root layout available.

## Expected repository structure

```text
GptBC/
├── .agents/plugins/marketplace.json
└── plugins/gptbc/
    ├── .codex-plugin/plugin.json
    ├── skills/
    ├── scripts/
    ├── references/
    └── assets/
```

## Updating

Because the marketplace source points to the `main` branch, future marketplace refreshes can pick up repository updates after they are pushed to GitHub.

For stable production use, a future release workflow may recommend a tagged Git ref rather than `main`.

## Local development install

For development/testing outside the marketplace UI, clone the repository and work from the source checkout:

```powershell
git clone https://github.com/scootieccc/GptBC.git
cd GptBC
```

PNG-level asset auditing requires Pillow:

```powershell
python -m pip install Pillow
```

Run an audit directly:

```powershell
python .\scripts\gptbc.py audit "C:\Games\MyGBStudioGame"
```

or use the marketplace package copy:

```powershell
python .\plugins\gptbc\scripts\gptbc.py audit "C:\Games\MyGBStudioGame"
```

## Troubleshooting

### `marketplace root does not contain a supported manifest`

Confirm all of the following:

- Source is `https://github.com/scootieccc/GptBC`
- Git ref is `main`
- Sparse paths is blank
- `.agents/plugins/marketplace.json` exists on the selected ref

### GptBC installs but PNG checks are skipped

Install Pillow:

```powershell
python -m pip install Pillow
```

### A GB Studio plugin is reported incompatible

Check the plugin's declared `gbsVersion` and the version of GB Studio used by your project. Do not force-install an engine plugin unless you understand the compatibility impact.

### Resource sync does not clone GitHub repositories

The `sync-resources` command uses the local `git` executable for GitHub repository sources. Confirm:

```powershell
git --version
```

## Reporting bugs

Include:

- GptBC version
- GB Studio version
- operating system
- exact command used
- relevant console output
- whether the issue involves a specific third-party plugin/resource

Do not attach proprietary or private game assets unless they are required to reproduce the issue and you are comfortable sharing them.
