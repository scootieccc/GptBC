from pathlib import Path
import importlib.util

HERE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("gptbc", HERE / "scripts" / "gptbc.py")
gptbc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gptbc)

def test_semver():
    assert gptbc.compatible("4.3.2", ">=4.2.0")
    assert not gptbc.compatible("4.1.3", ">=4.2.0")
