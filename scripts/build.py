#!/usr/bin/env python3
"""Render the public creation notebook from explicit original project records."""
import hashlib
import html
import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
p = json.loads((ROOT / "projects/ai-music.json").read_text())
s = json.loads((ROOT / "projects/sources.json").read_text())
esc = lambda value: html.escape(str(value), quote=True)
try:
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
except subprocess.CalledProcessError:
    commit = "preview"

def link(item):
    if not re.fullmatch(r"https://[^\s\"<>]+", item["url"]):
        raise ValueError("Invalid public source URL")
    return f'<a href="{esc(item["url"])}" target="_blank" rel="noopener noreferrer">{esc(item["title"])} ↗</a>'

fields = {
    "TITLE": esc(p["title"]), "UPDATED": esc(p["updated"]), "STATUS": esc(p["status"]),
    "GOAL": esc(p["goal"]), "SNAPSHOT": esc(s["snapshot_date"]), "COMMIT": esc(commit),
    "RESULTS": "".join(f'<article class="result"><span class="status {esc(r["state"])}" aria-hidden="true"></span><span class="label">{esc(r["label"])}</span><h3>{esc(r["title"])}</h3><p>{esc(r["detail"])}</p></article>' for r in p["results"]),
    "ROUTES": "".join(f'<article class="route"><span class="label">{esc(r["name"])}</span><p class="flow">{esc(r["steps"])}</p><p>{esc(r["advantage"])}</p><p class="muted">{esc(r["limit"])}</p></article>' for r in p["routes"]),
    "ACCEPTANCE": "".join(f'<div class="criterion"><b>{esc(r["name"])}</b><p>{esc(r["test"])}</p></div>' for r in p["acceptance"]),
    "NEXT": "".join(f'<li>{esc(r)}</li>' for r in p["next"]),
    "IDEAS": "".join(f'<article class="idea"><h3>{esc(r["title"])}</h3><p>{esc(r["hook"])}</p><p class="muted">{esc(r["evidence"])}</p></article>' for r in p["ideas"]),
    "SAMPLES": "".join(f'<div class="sample"><span class="views">{esc(r["views"])}</span>{link(r)}<p>{esc(r["note"])}</p></div>' for r in s["samples"]),
    "SOURCES": "".join(f'<div class="source">{link(r)}<p>{esc(r["note"])}</p></div>' for r in s["tools"]),
}
text = (ROOT / "site/index.html").read_text()
for key,value in fields.items():
    text = text.replace("{{"+key+"}}", value)
assert "{{" not in text, "Unresolved template"
for bad in ("/Users/", "/home/", "library/", "file://", "localhost", "127.0.0.1"):
    assert bad not in text, f"Private reference: {bad}"
out = ROOT / "dist"
out.mkdir(exist_ok=True)
(out / "index.html").write_text(text)
for name in ("style.css", "favicon.svg"):
    shutil.copyfile(ROOT / "site" / name, out / name)
manifest = {"source_repository":"https://github.com/farmcan/video-creation", "source_commit":commit,"content_date":p["updated"],"files":{name:hashlib.sha256((out/name).read_bytes()).hexdigest() for name in ("index.html","style.css","favicon.svg")}}
(out / "build-manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
print(f"Built public creation notebook: {len(p['results'])} result records, {len(s['samples'])} historical samples")
