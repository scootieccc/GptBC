# Contributing to GptBC

Thanks for helping improve GptBC.

## Good contributions

Useful contributions include:

- GB Studio 4.x compatibility fixes
- GBC hardware-budget validation rules
- `.gbsproj` schema handling improvements
- plugin/resource compatibility metadata
- safer backup/install behavior
- false-positive reductions in asset linting
- build/reporting improvements
- tests and fixtures
- documentation fixes

## Before opening a pull request

1. Keep GptBC GBC-first unless a change is specifically about DMG compatibility.
2. Avoid destructive project mutations by default.
3. Do not bundle third-party plugins or art unless redistribution is explicitly permitted by their licenses.
4. Preserve upstream license and source information for resource/plugin integrations.
5. Treat engine plugins as higher risk than ordinary event or asset plugins.
6. Add or update tests where practical.

## Local validation

Install dependencies:

```powershell
python -m pip install -r requirements.txt
python -m pip install pytest
```

Run syntax validation and tests:

```powershell
python -m py_compile scripts/gptbc.py
pytest tests -v
```

## Plugin/resource requests

When proposing a GB Studio plugin or resource source, include:

- project/plugin name
- upstream URL
- license
- known GB Studio versions
- whether it overrides engine files
- whether it uses scanline interrupts or replaces a scene type
- why it improves a GBC workflow

## Pull requests

Keep pull requests focused. Describe what changed, what was tested, and any compatibility risks.

Graphical/branding changes should be kept separate from functional changes when possible.
