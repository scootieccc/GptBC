from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "plugins" / "gptbc" / "scripts" / "resources.py"

spec = importlib.util.spec_from_file_location("gptbc_resources", RES)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_curated_catalog_is_populated_and_unique():
    assert len(mod.CURATED) >= 70
    names = [x["repository"].lower() for x in mod.CURATED]
    assert len(names) == len(set(names))


def test_asset_classification():
    assert mod.classify(Path("assets/backgrounds/forest.png")) == "backgrounds"
    assert mod.classify(Path("sprites/hero.png")) == "sprites"
    assert mod.classify(Path("music/theme.uge")) == "music"
    assert mod.classify(Path("tools/setup.exe")) is None


def test_known_catalog_entries():
    assert mod.entry("gb-studio-dev/gb-studio-plugins")
    assert mod.entry("DeerTears/GB-Studio-Community-Assets")
