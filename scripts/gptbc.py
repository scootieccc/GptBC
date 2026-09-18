#!/usr/bin/env python3
"""
GptBC 0.1.0
GBC-first GB Studio project auditor and plugin catalog helper.

No third-party plugin code is bundled. Official plugins are fetched from the
GB Studio upstream repository when the user explicitly runs install-plugin.
"""
from __future__ import annotations

import argparse
import copy
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request
import zipfile

VERSION = "0.2.0"
OFFICIAL_REPO = "https://plugins.gbstudio.dev/repository.json"
OFFICIAL_BASE = "https://plugins.gbstudio.dev/"
MANUAL_BG = {"#071821", "#306850", "#86c06c", "#e0f8cf"}
SPRITE_COLORS = {"#071821", "#86c06c", "#e0f8cf", "#65ff00"}
MAX_BG_AREA = 1_048_320
MAX_BG_DIM = 2040
MIN_BG = (160, 144)
COLOR_ONLY_TILES = 384
MONO_TILES = 192

def eprint(*a):
    print(*a, file=sys.stderr)

def fetch_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": f"GptBC/{VERSION}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def fetch_bytes(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": f"GptBC/{VERSION}"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()

def find_project(path: Path) -> Path:
    path = path.expanduser().resolve()
    if path.is_file() and path.suffix.lower() == ".gbsproj":
        return path
    hits = sorted(path.glob("*.gbsproj"))
    if len(hits) == 1:
        return hits[0]
    if not hits:
        raise SystemExit(f"No .gbsproj found in {path}")
    raise SystemExit("Multiple .gbsproj files found; pass the desired file explicitly.")

def load_project(path: Path):
    p = find_project(path)
    return p, json.loads(p.read_text(encoding="utf-8"))

def walk_values(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{path}.{k}" if path else k
            yield p, v
            yield from walk_values(v, p)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            p = f"{path}[{i}]"
            yield p, v
            yield from walk_values(v, p)

def detect_color_mode(data):
    candidates = []
    for p, v in walk_values(data):
        if isinstance(v, str) and "color" in p.lower():
            lv = v.lower().replace("_", "").replace("-", "").replace(" ", "")
            if lv in {"coloronly", "gbccoloronly"}:
                candidates.append(("colorOnly", p, v))
            elif lv in {"colorandmono", "color+monochrome", "colorandmonochrome"}:
                candidates.append(("colorAndMonochrome", p, v))
            elif lv in {"monochrome", "mono"}:
                candidates.append(("monochrome", p, v))
        if p.lower().endswith(("colormode", "color_mode")):
            candidates.append(("unknown", p, v))
    for item in candidates:
        if item[0] != "unknown":
            return item
    return candidates[0] if candidates else (None, None, None)

def detect_gbs_version(data):
    for p, v in walk_values(data):
        if not isinstance(v, str):
            continue
        pl = p.lower()
        if "version" in pl and re.fullmatch(r"\d+\.\d+(?:\.\d+)?(?:[-+].*)?", v.strip()):
            if "release" in pl or "gbs" in pl or "project" in pl or pl.endswith("version"):
                return v.strip(), p
    return None, None

def semver_tuple(s):
    m = re.search(r"(\d+)\.(\d+)(?:\.(\d+))?", s or "")
    if not m:
        return None
    return tuple(int(x or 0) for x in m.groups())

def compatible(version, spec):
    """Practical subset for current GB Studio plugin metadata."""
    if not spec or not version:
        return True
    v = semver_tuple(version)
    if not v:
        return True
    parts = [x.strip() for x in re.split(r"\s+", spec.strip()) if x.strip()]
    ok = True
    for part in parts:
        m = re.match(r"(>=|<=|>|<|=|\^|~)?\s*(\d+\.\d+(?:\.\d+)?)", part)
        if not m:
            continue
        op, raw = m.groups()
        t = semver_tuple(raw)
        if op == ">=": ok &= v >= t
        elif op == "<=": ok &= v <= t
        elif op == ">": ok &= v > t
        elif op == "<": ok &= v < t
        elif op in ("=", None): ok &= v == t
        elif op == "^": ok &= (v[0] == t[0] and v >= t)
        elif op == "~": ok &= (v[:2] == t[:2] and v >= t)
    return bool(ok)

def pillow():
    try:
        from PIL import Image
        return Image
    except Exception:
        return None

def rgb_hex(px):
    if len(px) >= 3:
        return "#{:02x}{:02x}{:02x}".format(px[0], px[1], px[2])
    return None

def image_tiles(img, flip_equivalent=False):
    rgb = img.convert("RGBA")
    w, h = rgb.size
    tiles = set()
    for y in range(0, h, 8):
        for x in range(0, w, 8):
            if x + 8 > w or y + 8 > h:
                continue
            tile = rgb.crop((x,y,x+8,y+8))
            variants = [tile]
            if flip_equivalent:
                from PIL import Image as PILImage
                variants += [
                    tile.transpose(PILImage.Transpose.FLIP_LEFT_RIGHT),
                    tile.transpose(PILImage.Transpose.FLIP_TOP_BOTTOM),
                    tile.transpose(PILImage.Transpose.FLIP_LEFT_RIGHT).transpose(PILImage.Transpose.FLIP_TOP_BOTTOM),
                ]
            keys = [v.tobytes() for v in variants]
            tiles.add(min(keys))
    return len(tiles)

def lint_background(path: Path, color_only=True):
    Image = pillow()
    issues = []
    metrics = {}
    if Image is None:
        return issues, {"note": "Pillow not installed; image-level checks skipped."}
    try:
        img = Image.open(path).convert("RGBA")
    except Exception as ex:
        return [("error", f"Cannot open PNG: {ex}")], metrics
    w,h = img.size
    metrics["size"] = [w,h]
    if w % 8 or h % 8:
        issues.append(("error", f"Dimensions {w}x{h} are not multiples of 8."))
    if w < 160 or h < 144:
        issues.append(("warning", f"{w}x{h} is smaller than the native 160x144 screen."))
    if w > MAX_BG_DIM or h > MAX_BG_DIM:
        issues.append(("error", f"{w}x{h} exceeds the 2040 px per-dimension limit."))
    if w*h > MAX_BG_AREA:
        issues.append(("error", f"Area {w*h:,} exceeds {MAX_BG_AREA:,} px."))
    tile_count = image_tiles(img, flip_equivalent=False)
    flip_count = image_tiles(img, flip_equivalent=color_only)
    metrics["uniqueTilesExact"] = tile_count
    metrics["uniqueTilesWithFlipEquivalence"] = flip_count
    limit = COLOR_ONLY_TILES if color_only else MONO_TILES
    if flip_count > limit:
        issues.append(("error", f"{flip_count} flip-equivalent unique 8x8 tiles exceed limit {limit}."))
    elif tile_count > limit and color_only:
        issues.append(("info", f"{tile_count} exact tiles drop to {flip_count} with flip equivalence; automatic tile flip may save VRAM."))
    palette_sets = set()
    tile_over = 0
    for y in range(0, h - h%8, 8):
        for x in range(0, w - w%8, 8):
            colors = set()
            for px in img.crop((x,y,x+8,y+8)).getdata():
                if len(px) == 4 and px[3] == 0:
                    continue
                colors.add(rgb_hex(px))
            if len(colors) > 4:
                tile_over += 1
            palette_sets.add(tuple(sorted(c for c in colors if c)))
    metrics["automaticPaletteSets"] = len(palette_sets)
    metrics["tilesOver4Colors"] = tile_over
    if tile_over:
        issues.append(("warning", f"{tile_over} tile(s) use more than 4 colors; invalid for automatic palettes."))
    if len(palette_sets) > 8:
        issues.append(("error", f"{len(palette_sets)} unique tile palette sets exceed 8."))
    elif len(palette_sets) > 7:
        issues.append(("warning", "8 palette sets may consume the palette used by dialogue/menu UI; 7 or fewer is safer for automatic palettes."))
    return issues, metrics

def lint_sprite(path: Path):
    Image = pillow()
    issues = []
    metrics = {}
    if Image is None:
        return issues, {"note": "Pillow not installed; image-level checks skipped."}
    try:
        img = Image.open(path).convert("RGBA")
    except Exception as ex:
        return [("error", f"Cannot open PNG: {ex}")], metrics
    w,h = img.size
    metrics["size"] = [w,h]
    if w % 8 or h % 8:
        issues.append(("warning", f"Dimensions {w}x{h} are not aligned to 8px tiles."))
    colors = set()
    for px in img.getdata():
        if px[3] == 0:
            continue
        colors.add(rgb_hex(px))
    metrics["opaqueColors"] = sorted(colors)
    invalid = sorted(c for c in colors if c not in SPRITE_COLORS)
    if invalid:
        issues.append(("warning", "Non-canonical GB Studio sprite source colors: " + ", ".join(invalid[:12]) + ("..." if len(invalid)>12 else "")))
    if "#306850" in colors:
        issues.append(("error", "Sprite uses #306850, which GB Studio sprite source art does not support."))
    return issues, metrics

def scan_plugins(project_root: Path):
    pdir = project_root / "plugins"
    found = []
    if not pdir.exists():
        return found
    for manifest in pdir.rglob("plugin.json"):
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
            found.append({
                "path": str(manifest.parent.relative_to(project_root)),
                "name": data.get("name", manifest.parent.name),
                "type": data.get("type"),
                "version": data.get("version"),
                "gbsVersion": data.get("gbsVersion"),
                "license": data.get("license")
            })
        except Exception as ex:
            found.append({"path": str(manifest.parent.relative_to(project_root)), "error": str(ex)})
    return found

def engine_conflicts(project_root: Path):
    pdir = project_root / "plugins"
    file_map = {}
    if not pdir.exists():
        return []
    for f in pdir.rglob("*"):
        if not f.is_file():
            continue
        parts = [x.lower() for x in f.parts]
        try:
            idx = parts.index("engine")
        except ValueError:
            continue
        rel = "/".join(f.parts[idx+1:]).lower()
        file_map.setdefault(rel, []).append(str(f))
    return [(k,v) for k,v in file_map.items() if len(v) > 1]

def audit(project_path: Path):
    proj, data = load_project(project_path)
    root = proj.parent
    mode, mode_path, raw_mode = detect_color_mode(data)
    gbs_ver, gbs_path = detect_gbs_version(data)
    color_only = mode != "monochrome" and mode != "colorAndMonochrome"
    report = {
        "gptbcVersion": VERSION,
        "project": str(proj),
        "detected": {
            "colorMode": mode,
            "colorModePath": mode_path,
            "rawColorMode": raw_mode,
            "gbStudioVersion": gbs_ver,
            "gbStudioVersionPath": gbs_path
        },
        "summary": {"errors":0, "warnings":0, "info":0},
        "issues": [],
        "assets": {"backgrounds": [], "sprites": []},
        "plugins": scan_plugins(root),
        "engineConflicts": []
    }
    def add(level, area, msg, path=None):
        report["summary"][{"error":"errors","warning":"warnings","info":"info"}[level]] += 1
        report["issues"].append({"level":level,"area":area,"message":msg,"path":path})

    if mode is None:
        add("warning","project","Could not reliably detect project color mode from .gbsproj schema.")
    elif mode != "colorOnly":
        add("warning","project",f"GptBC is GBC-first; detected color mode is {mode!r}, not Color Only.")
    else:
        add("info","project","Color Only mode detected.")

    if not gbs_ver:
        add("warning","project","Could not reliably detect GB Studio version in .gbsproj.")
    elif semver_tuple(gbs_ver) and semver_tuple(gbs_ver) < (4,2,0):
        add("warning","project",f"Detected GB Studio {gbs_ver}; official Plugin Manager repository support is documented for 4.2.0+.")

    for path in sorted((root/"assets"/"backgrounds").glob("*.png")) if (root/"assets"/"backgrounds").exists() else []:
        issues, metrics = lint_background(path, color_only=color_only)
        row = {"path": str(path.relative_to(root)), "metrics": metrics, "issues": []}
        for level,msg in issues:
            row["issues"].append({"level":level,"message":msg})
            add(level,"background",msg,row["path"])
        report["assets"]["backgrounds"].append(row)

    for path in sorted((root/"assets"/"sprites").glob("*.png")) if (root/"assets"/"sprites").exists() else []:
        issues, metrics = lint_sprite(path)
        row = {"path": str(path.relative_to(root)), "metrics": metrics, "issues": []}
        for level,msg in issues:
            row["issues"].append({"level":level,"message":msg})
            add(level,"sprite",msg,row["path"])
        report["assets"]["sprites"].append(row)

    for rel, paths in engine_conflicts(root):
        report["engineConflicts"].append({"engineFile":rel,"providers":paths})
        add("warning","plugins",f"Multiple plugins provide engine file '{rel}', which may conflict.")

    for p in report["plugins"]:
        if p.get("gbsVersion") and gbs_ver and not compatible(gbs_ver, p["gbsVersion"]):
            add("error","plugins",f"Installed plugin {p.get('name')} declares {p.get('gbsVersion')} but project appears to use {gbs_ver}.", p.get("path"))

    if pillow() is None:
        add("warning","tooling","Pillow is not installed. Install with: python -m pip install Pillow")

    return report

def markdown_report(rep):
    s = rep["summary"]
    d = rep["detected"]
    lines = [
        "# GptBC Build-Readiness Report",
        "",
        f"- Project: `{rep['project']}`",
        f"- Detected GB Studio version: `{d.get('gbStudioVersion') or 'unknown'}`",
        f"- Detected color mode: `{d.get('colorMode') or 'unknown'}`",
        f"- Errors: **{s['errors']}**",
        f"- Warnings: **{s['warnings']}**",
        f"- Info: **{s['info']}**",
        "",
        "## Issues",
        ""
    ]
    if not rep["issues"]:
        lines += ["No issues detected by the current GptBC rule set.", ""]
    else:
        for x in rep["issues"]:
            loc = f" — `{x['path']}`" if x.get("path") else ""
            lines.append(f"- **{x['level'].upper()} / {x['area']}**: {x['message']}{loc}")
        lines.append("")
    lines += ["## Installed GB Studio plugins", ""]
    if rep["plugins"]:
        for p in rep["plugins"]:
            if p.get("error"):
                lines.append(f"- `{p['path']}` — unreadable manifest: {p['error']}")
            else:
                lines.append(f"- **{p.get('name')}** {p.get('version') or ''} — {p.get('type') or 'unknown type'} — `{p.get('path')}`")
    else:
        lines.append("No project-local plugins detected.")
    lines += ["", "## Engine-file conflicts", ""]
    if rep["engineConflicts"]:
        for c in rep["engineConflicts"]:
            lines.append(f"- `{c['engineFile']}`")
            for p in c["providers"]:
                lines.append(f"  - `{p}`")
    else:
        lines.append("No duplicate engine override paths detected.")
    lines += ["", "## Asset counts", ""]
    lines.append(f"- Background PNGs checked: {len(rep['assets']['backgrounds'])}")
    lines.append(f"- Sprite PNGs checked: {len(rep['assets']['sprites'])}")
    lines.append("")
    return "\n".join(lines)

def catalog(gbs_version=None):
    repo = fetch_json(OFFICIAL_REPO)
    items = repo.get("plugins", [])
    if gbs_version:
        items = [x for x in items if compatible(gbs_version, x.get("gbsVersion"))]
    return repo, items

def print_catalog(items):
    for x in items:
        print(f"{x.get('id')}\t{x.get('type')}\t{x.get('version')}\t{x.get('gbsVersion')}\t{x.get('name')}")

def search_catalog(query, gbs_version=None):
    _, items = catalog(gbs_version)
    q = query.lower()
    out = []
    for x in items:
        blob = " ".join(str(x.get(k,"")) for k in ("id","name","author","description","type","url")).lower()
        if q in blob:
            out.append(x)
    return out

def safe_extract_zip(data: bytes, dest: Path):
    with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tf:
        tf.write(data)
        tmp = Path(tf.name)
    try:
        with zipfile.ZipFile(tmp) as z:
            base = dest.resolve()
            for info in z.infolist():
                target = (dest / info.filename).resolve()
                if base not in target.parents and target != base:
                    raise RuntimeError(f"Unsafe zip path: {info.filename}")
            z.extractall(dest)
    finally:
        tmp.unlink(missing_ok=True)

def backup_plugins(project_root: Path):
    pdir = project_root / "plugins"
    if not pdir.exists():
        return None
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    out = project_root / ".gptbc" / "backups" / f"plugins-{stamp}"
    out.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(pdir, out)
    return out

def install_plugin(plugin_id: str, project_path: Path, gbs_version=None):
    proj, data = load_project(project_path)
    root = proj.parent
    if not gbs_version:
        gbs_version, _ = detect_gbs_version(data)
    repo = fetch_json(OFFICIAL_REPO)
    match = next((x for x in repo.get("plugins", []) if x.get("id","").lower() == plugin_id.lower()), None)
    if not match:
        raise SystemExit(f"Plugin id not found: {plugin_id}")
    if gbs_version and not compatible(gbs_version, match.get("gbsVersion")):
        raise SystemExit(f"Incompatible: plugin declares {match.get('gbsVersion')} but target is {gbs_version}")
    backup = backup_plugins(root)
    filename = match.get("filename")
    if not filename:
        raise SystemExit("Plugin entry has no downloadable filename.")
    url = urllib.parse.urljoin(OFFICIAL_BASE, urllib.parse.quote(filename, safe="/"))
    data_bytes = fetch_bytes(url)
    sha = hashlib.sha256(data_bytes).hexdigest()
    stage = Path(tempfile.mkdtemp(prefix="gptbc-plugin-"))
    try:
        safe_extract_zip(data_bytes, stage)
        manifests = list(stage.rglob("plugin.json"))
        if not manifests:
            raise SystemExit("Downloaded archive has no plugin.json.")
        src = manifests[0].parent
        target = root / "plugins" / match["id"]
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(src, target)
    finally:
        shutil.rmtree(stage, ignore_errors=True)
    return {"installed": str(target), "backup": str(backup) if backup else None, "sha256": sha, "metadata": match}


def slugify(value: str):
    value = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip()).strip("-").lower()
    return value or "source"

def load_resource_registry():
    path = Path(__file__).resolve().parent.parent / "references" / "resource-registry.json"
    return path, json.loads(path.read_text(encoding="utf-8"))

def sync_resources(cache_dir: Path, include_archived=False):
    registry_path, registry = load_resource_registry()
    cache_dir = cache_dir.expanduser().resolve()
    cache_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for src in registry.get("sources", []):
        if not src.get("enabled", True):
            if not (include_archived and src.get("archived")):
                continue
        if src.get("archived") and not include_archived:
            continue
        kind = src.get("kind")
        name = src.get("name") or src.get("url")
        url = src.get("url")
        row = {"name": name, "kind": kind, "url": url, "status": "unknown"}
        try:
            if kind == "gbstudioRepository":
                data = fetch_json(url)
                out = cache_dir / "official-gbstudio-repository.json"
                out.write_text(json.dumps(data, indent=2), encoding="utf-8")
                row.update(status="updated", path=str(out), plugins=len(data.get("plugins", [])))
            elif kind == "github":
                dest = cache_dir / slugify(name)
                git = shutil.which("git")
                if not git:
                    row.update(status="skipped", note="git executable not found")
                elif (dest / ".git").exists():
                    subprocess.run([git, "-C", str(dest), "fetch", "--depth", "1", "origin"], check=True)
                    subprocess.run([git, "-C", str(dest), "reset", "--hard", "origin/HEAD"], check=True)
                    row.update(status="updated", path=str(dest))
                elif dest.exists():
                    row.update(status="skipped", note=f"destination exists but is not a git repo: {dest}")
                else:
                    subprocess.run([git, "clone", "--depth", "1", url, str(dest)], check=True)
                    row.update(status="cloned", path=str(dest))
            else:
                row.update(status="skipped", note=f"unsupported source kind: {kind}")
        except Exception as ex:
            row.update(status="error", error=str(ex))
        results.append(row)
    manifest = cache_dir / "GptBC_RESOURCE_CACHE.json"
    manifest.write_text(json.dumps({
        "gptbcVersion": VERSION,
        "registry": str(registry_path),
        "generatedAt": dt.datetime.now().isoformat(),
        "sources": results
    }, indent=2), encoding="utf-8")
    return results, manifest

def cmd_sync_resources(args):
    if args.cache_dir:
        cache = Path(args.cache_dir)
    elif args.project:
        proj = find_project(Path(args.project))
        cache = proj.parent / ".gptbc" / "resource-cache"
    else:
        cache = Path.home() / ".gptbc" / "resource-cache"
    results, manifest = sync_resources(cache, args.include_archived)
    print(json.dumps({"manifest": str(manifest), "sources": results}, indent=2))
    return 2 if any(x.get("status") == "error" for x in results) else 0

def cmd_audit(args):
    rep = audit(Path(args.project))
    print(json.dumps(rep, indent=2))
    if rep["summary"]["errors"]:
        return 2
    return 1 if rep["summary"]["warnings"] else 0

def cmd_report(args):
    rep = audit(Path(args.project))
    out = Path(args.out)
    if not out.is_absolute():
        out = Path(args.project).resolve()
        if out.is_file():
            out = out.parent
        out = out / args.out
    out.write_text(markdown_report(rep), encoding="utf-8")
    print(out)
    return 0

def cmd_catalog(args):
    _, items = catalog(args.gbs_version)
    print_catalog(items)
    return 0

def cmd_search(args):
    items = search_catalog(args.query, args.gbs_version)
    print_catalog(items)
    return 0

def cmd_install(args):
    result = install_plugin(args.plugin_id, Path(args.project), args.gbs_version)
    print(json.dumps(result, indent=2))
    return 0

def cmd_registry(args):
    path = Path(__file__).resolve().parent.parent / "references" / "resource-registry.json"
    print(path.read_text(encoding="utf-8"))
    return 0

def main():
    ap = argparse.ArgumentParser(prog="gptbc", description="GBC-first GB Studio workflow helper")
    ap.add_argument("--version", action="version", version=f"GptBC {VERSION}")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("audit", help="Audit a GB Studio project and emit JSON")
    p.add_argument("project")
    p.set_defaults(fn=cmd_audit)

    p = sub.add_parser("report", help="Write a Markdown build-readiness report")
    p.add_argument("project")
    p.add_argument("--out", default="GptBC_BUILD_REPORT.md")
    p.set_defaults(fn=cmd_report)

    p = sub.add_parser("catalog", help="List official GB Studio plugins")
    p.add_argument("--gbs-version", default=None)
    p.set_defaults(fn=cmd_catalog)

    p = sub.add_parser("search", help="Search the official plugin catalog")
    p.add_argument("query")
    p.add_argument("--gbs-version", default=None)
    p.set_defaults(fn=cmd_search)

    p = sub.add_parser("install-plugin", help="Install an official plugin into a project with backup")
    p.add_argument("plugin_id")
    p.add_argument("project")
    p.add_argument("--gbs-version", default=None)
    p.set_defaults(fn=cmd_install)

    p = sub.add_parser("registry", help="Show configured upstream resource registries")
    p.set_defaults(fn=cmd_registry)

    p = sub.add_parser("sync-resources", help="Sync enabled GitHub/resource-pack sources to a local cache")
    p.add_argument("project", nargs="?", default=None, help="Optional GB Studio project; defaults cache inside project/.gptbc")
    p.add_argument("--cache-dir", default=None, help="Explicit resource-cache directory")
    p.add_argument("--include-archived", action="store_true", help="Also sync archived/disabled legacy sources marked archived")
    p.set_defaults(fn=cmd_sync_resources)

    args = ap.parse_args()
    raise SystemExit(args.fn(args))

if __name__ == "__main__":
    main()
