#!/usr/bin/env python3
from __future__ import annotations

import argparse, base64, datetime as dt, hashlib, json, re, shutil, subprocess, sys, urllib.request, zlib
from pathlib import Path

VERSION = "0.3.0"
_CATALOG_Z = "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"
CURATED = json.loads(zlib.decompress(base64.b64decode(_CATALOG_Z)).decode("utf-8"))
CURATED_MAP = {x["repository"].lower(): x for x in CURATED}
OFFICIAL_OWNERS = {"chrismaltby", "gb-studio-dev"}
BLOCKED_EXT = {".exe",".msi",".dll",".com",".scr",".bat",".cmd",".ps1",".vbs",".jar",".app",".dmg"}
IMPORTABLE_EXT = {".png",".uge",".mod",".wav",".vgm",".mid",".midi",".sav"}
DEST = {"backgrounds":"assets/backgrounds","sprites":"assets/sprites","fonts":"assets/fonts","music":"assets/music","sounds":"assets/sounds","avatars":"assets/avatars","emotes":"assets/emotes","ui":"assets/ui"}

def die(msg): raise SystemExit(msg)
def slug(s): return re.sub(r"[^A-Za-z0-9._-]+","-",s).strip("-").lower()

def entry(repo):
    x=CURATED_MAP.get(repo.lower())
    if not x: die(f"Repository is not in GptBC's curated catalog: {repo}")
    return x

def gh_meta(repo):
    req=urllib.request.Request(f"https://api.github.com/repos/{repo}",headers={"User-Agent":f"GptBC/{VERSION}","Accept":"application/vnd.github+json"})
    try:
        with urllib.request.urlopen(req,timeout=30) as r: d=json.load(r)
        return {"repository":d.get("full_name",repo),"url":d.get("html_url",f"https://github.com/{repo}"),"default_branch":d.get("default_branch"),"archived":bool(d.get("archived")),"disabled":bool(d.get("disabled")),"fork":bool(d.get("fork")),"stars":int(d.get("stargazers_count") or 0),"forks":int(d.get("forks_count") or 0),"updated_at":d.get("updated_at"),"license":(d.get("license") or {}).get("spdx_id") or "NOASSERTION","description":d.get("description") or ""}
    except Exception as ex: return {"repository":repo,"url":f"https://github.com/{repo}","license":"UNKNOWN","metadata_error":str(ex)}

def trust(repo): return "official" if repo.split("/",1)[0].lower() in OFFICIAL_OWNERS else "curated-community"

def find_project(p):
    p=Path(p).expanduser().resolve()
    if p.is_file() and p.suffix.lower()==".gbsproj": return p
    hits=sorted(p.glob("*.gbsproj"))
    if len(hits)==1: return hits[0]
    if not hits: die(f"No .gbsproj found in {p}")
    die("Multiple .gbsproj files found; pass the desired project file.")

def root(p): return find_project(p).parent
def cache(repo,p): return root(p)/".gptbc"/"resource-cache"/slug(repo)

def git(args,cwd=None,capture=False):
    exe=shutil.which("git")
    if not exe: die("Git is required for resource syncing and was not found in PATH.")
    r=subprocess.run([exe]+list(args),cwd=str(cwd) if cwd else None,check=True,text=True,capture_output=capture)
    return r.stdout.strip() if capture else ""

def sync(repo,project,include_archived=False):
    e=entry(repo); m=gh_meta(repo)
    if m.get("disabled"): die(f"Repository is disabled: {repo}")
    if m.get("archived") and not include_archived: die(f"{repo} is archived. Use --include-archived only after reviewing age and compatibility.")
    d=cache(repo,project); d.parent.mkdir(parents=True,exist_ok=True); url=e.get("url") or f"https://github.com/{repo}"
    if (d/".git").exists():
        git(["fetch","--depth","1","origin"],d); branch=m.get("default_branch")
        try: git(["checkout","-B",branch,f"origin/{branch}"],d) if branch else git(["reset","--hard","origin/HEAD"],d)
        except Exception: git(["reset","--hard","origin/HEAD"],d)
        status="updated"
    elif d.exists(): die(f"Cache path exists but is not a Git repo: {d}")
    else: git(["clone","--depth","1",url,str(d)]); status="cloned"
    return {"repository":repo,"status":status,"path":str(d),"commit":git(["rev-parse","HEAD"],d,True),"metadata":m}

def classify(p):
    p=Path(p); ext=p.suffix.lower()
    if ext in BLOCKED_EXT or ext not in IMPORTABLE_EXT: return None
    tokens=set(re.split(r"[/_.\-]+",p.as_posix().lower()))
    if ext in {".uge",".mod",".mid",".midi"} or tokens & {"music","song","songs"}: return "music"
    if ext in {".wav",".vgm",".sav"} or tokens & {"sfx","sound","sounds","audio"}: return "sounds"
    if ext==".png":
        rules=[("backgrounds",{"background","backgrounds","tileset","tilesets","tilemap","maps"}),("sprites",{"sprite","sprites","actor","actors","character","characters"}),("fonts",{"font","fonts","typeface"}),("avatars",{"avatar","avatars","portrait","portraits"}),("emotes",{"emote","emotes"}),("ui",{"ui","interface","window","windows","frame","frames"})]
        for kind,words in rules:
            if tokens & words: return kind
        return "unknown-png"

def files(repo_dir):
    out=[]
    for p in sorted(Path(repo_dir).rglob("*")):
        if not p.is_file(): continue
        rel=p.relative_to(repo_dir)
        if ".git" in rel.parts: continue
        kind=classify(rel)
        if kind: out.append({"path":rel.as_posix(),"kind":kind,"size":p.stat().st_size})
    return out

def pillow():
    try:
        from PIL import Image
        return Image
    except Exception: return None

def tile_count(img):
    I=pillow(); a=img.convert("RGBA"); seen=set()
    for y in range(0,a.height-a.height%8,8):
        for x in range(0,a.width-a.width%8,8):
            t=a.crop((x,y,x+8,y+8)); variants=[t]
            if I: variants += [t.transpose(I.Transpose.FLIP_LEFT_RIGHT),t.transpose(I.Transpose.FLIP_TOP_BOTTOM),t.transpose(I.Transpose.FLIP_LEFT_RIGHT).transpose(I.Transpose.FLIP_TOP_BOTTOM)]
            seen.add(min(v.tobytes() for v in variants))
    return len(seen)

def validate(path,kind):
    if Path(path).suffix.lower()!=".png": return {"status":"ok","issues":[]}
    I=pillow()
    if not I: return {"status":"warning","issues":["Pillow not installed; PNG validation skipped."]}
    try: img=I.open(path).convert("RGBA")
    except Exception as ex: return {"status":"error","errors":[f"Cannot open PNG: {ex}"],"issues":[]}
    w,h=img.size; errors=[]; issues=[]
    if w%8 or h%8: (errors if kind=="backgrounds" else issues).append(f"{w}x{h} is not aligned to 8x8 tiles.")
    if kind=="backgrounds":
        if w<160 or h<144: issues.append(f"Background {w}x{h} is smaller than native 160x144.")
        if w>2040 or h>2040 or w*h>1048320: errors.append("Background exceeds GB Studio size limits.")
        n=tile_count(img)
        if n>384: errors.append(f"{n} flip-equivalent 8x8 tiles exceed the GBC Color Only target of 384.")
    elif kind=="sprites":
        colors={"#{:02x}{:02x}{:02x}".format(*px[:3]) for px in img.getdata() if px[3]}
        if "#306850" in colors: errors.append("Sprite contains unsupported GB Studio source color #306850.")
        canonical={"#071821","#86c06c","#e0f8cf","#65ff00"}; bad=sorted(colors-canonical)
        if bad: issues.append("Non-canonical sprite source colors may require conversion: "+", ".join(bad[:8]))
    return {"status":"error" if errors else ("warning" if issues else "ok"),"size":[w,h],"errors":errors,"issues":issues}

def inspect_repo(repo,project,include_archived=False):
    s=sync(repo,project,include_archived); ff=files(Path(s["path"]))
    return {"catalog":entry(repo),"sync":s,"fileCount":len(ff),"files":ff}

def sha256(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for c in iter(lambda:f.read(1048576),b""): h.update(c)
    return h.hexdigest()

def import_one(repo,source_path,project,dest_type="auto",include_archived=False,allow_unverified_license=False,force=False,overwrite=False):
    rr=root(project); info=inspect_repo(repo,project,include_archived); m=info["sync"]["metadata"]
    if str(m.get("license","")).upper() in {"","UNKNOWN","NOASSERTION","OTHER"} and not allow_unverified_license: die("Upstream license is unknown/NOASSERTION. Review the repository license and use --allow-unverified-license only if reuse is permitted.")
    rd=Path(info["sync"]["path"]).resolve(); src=(rd/source_path).resolve()
    if rd not in src.parents or not src.is_file(): die("Invalid or missing source path.")
    inferred=classify(Path(source_path))
    if not inferred: die("File is not an importable GB Studio asset type.")
    kind=inferred if dest_type=="auto" else dest_type
    if kind=="unknown-png": die("PNG destination is ambiguous; supply --dest-type backgrounds|sprites|fonts|avatars|emotes|ui.")
    if kind not in DEST: die(f"Unsupported destination type: {kind}")
    check=validate(src,kind)
    if check["status"]=="error" and not force: die("Asset failed GB Studio validation. Fix it or use --force only after reviewing the reported errors.")
    ddir=rr/DEST[kind]; ddir.mkdir(parents=True,exist_ok=True); dst=ddir/src.name; backup=None
    if dst.exists() and not overwrite: die(f"Destination exists: {dst}. Use --overwrite to back up and replace it.")
    if dst.exists():
        stamp=dt.datetime.now().strftime("%Y%m%d-%H%M%S"); backup=rr/".gptbc"/"backups"/"assets"/stamp/dst.relative_to(rr); backup.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(dst,backup)
    shutil.copy2(src,dst)
    rec={"importedAt":dt.datetime.now(dt.timezone.utc).isoformat(),"gptbcVersion":VERSION,"repository":repo,"repositoryUrl":m.get("url") or entry(repo).get("url"),"commit":info["sync"]["commit"],"license":m.get("license"),"sourcePath":source_path,"destinationType":kind,"destinationPath":dst.relative_to(rr).as_posix(),"sha256":sha256(dst),"validation":check,"backup":backup.relative_to(rr).as_posix() if backup else None}
    log=rr/".gptbc"/"provenance"/"imports.jsonl"; log.parent.mkdir(parents=True,exist_ok=True)
    with log.open("a",encoding="utf-8") as f: f.write(json.dumps(rec,ensure_ascii=False)+"\n")
    return {"imported":str(dst),"provenance":str(log),"record":rec}

def selected(query=None,typ=None):
    items=list(CURATED)
    if query:
        q=query.lower(); items=[x for x in items if q in " ".join(x.values()).lower()]
    if typ:
        q=typ.lower(); items=[x for x in items if q in x["resource_type"].lower()]
    return items

def score(x,q):
    text=" ".join(x.values()).lower(); toks=[t for t in re.split(r"\W+",q.lower()) if t]
    return sum(5 for t in toks if t in text)+(3 if trust(x["repository"])=="official" else 0)+(1 if "asset" in x["resource_type"].lower() else 0)

def cmd_list(a):
    for x in selected(a.query,a.type): print(f'{x["repository"]}\t{x["resource_type"]}\t{x["primary_use"]}')
def cmd_recommend(a):
    ranked=sorted(((score(x,a.query),x) for x in selected(typ=a.type)),key=lambda z:(-z[0],z[1]["repository"].lower()))
    for _,x in [z for z in ranked if z[0]>0][:a.limit]: print(json.dumps({**x,"trust":trust(x["repository"]),"live":gh_meta(x["repository"]) if a.live else None},ensure_ascii=False))
def cmd_sync(a): print(json.dumps(sync(a.repository,a.project,a.include_archived),indent=2))
def cmd_inspect(a):
    r=inspect_repo(a.repository,a.project,a.include_archived)
    if a.kind: r["files"]=[x for x in r["files"] if x["kind"]==a.kind]; r["fileCount"]=len(r["files"])
    print(json.dumps(r,indent=2))
def cmd_import(a): print(json.dumps(import_one(a.repository,a.source_path,a.project,a.dest_type,a.include_archived,a.allow_unverified_license,a.force,a.overwrite),indent=2))

def main():
    ap=argparse.ArgumentParser(prog="gptbc resources",description="Curated GB Studio resource discovery and safe asset importer")
    ap.add_argument("--version",action="version",version=f"GptBC resources {VERSION}"); sub=ap.add_subparsers(dest="cmd",required=True)
    p=sub.add_parser("list"); p.add_argument("--query"); p.add_argument("--type"); p.set_defaults(fn=cmd_list)
    p=sub.add_parser("recommend"); p.add_argument("query"); p.add_argument("--type"); p.add_argument("--limit",type=int,default=10); p.add_argument("--live",action="store_true"); p.set_defaults(fn=cmd_recommend)
    p=sub.add_parser("sync"); p.add_argument("repository"); p.add_argument("project"); p.add_argument("--include-archived",action="store_true"); p.set_defaults(fn=cmd_sync)
    p=sub.add_parser("inspect"); p.add_argument("repository"); p.add_argument("project"); p.add_argument("--kind",choices=list(DEST)+["unknown-png"]); p.add_argument("--include-archived",action="store_true"); p.set_defaults(fn=cmd_inspect)
    p=sub.add_parser("import"); p.add_argument("repository"); p.add_argument("source_path"); p.add_argument("project"); p.add_argument("--dest-type",default="auto",choices=["auto"]+list(DEST)); p.add_argument("--include-archived",action="store_true"); p.add_argument("--allow-unverified-license",action="store_true"); p.add_argument("--force",action="store_true"); p.add_argument("--overwrite",action="store_true"); p.set_defaults(fn=cmd_import)
    a=ap.parse_args(); result=a.fn(a); raise SystemExit(0 if result is None else result)

if __name__=="__main__": main()
