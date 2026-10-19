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
catalog = json.loads((ROOT / "projects/catalog.json").read_text())
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
    "CANDIDATE_SUMMARY": esc(p["candidate_summary"]),
    "TRIAL_PLAN": "".join(f'<li>{esc(r)}</li>' for r in p["trial_plan"]),
    "IDEAS": "".join(f'<article class="idea"><h3>{esc(r["title"])}</h3><p>{esc(r["hook"])}</p><p class="muted">{esc(r["evidence"])}</p></article>' for r in p["ideas"]),
    "SAMPLES": "".join(f'<div class="sample"><span class="views">{esc(r["views"])}</span>{link(r)}<p>{esc(r["note"])}</p></div>' for r in s["samples"]),
    "SOURCES": "".join(f'<div class="source">{link(r)}<p>{esc(r["note"])}</p></div>' for r in s["tools"]),
}
def idea_card(idea):
    title = esc(idea["title"])
    content = f'<div class="idea-preview"><span class="idea-state">{esc(idea["status"])}</span><h4>{title}</h4><p>{esc(idea["hook"])}</p>'
    if "url" in idea:
        assert idea["url"] == "ai-music/", "Unexpected idea route"
        content += f'<a href="ai-music/">查看研究与实验 →</a>'
    else:
        content += f'<details><summary>展开这个 idea</summary><p>{esc(idea["next"])}</p></details>'
    return content + '</div>'

cards = []
for column in catalog["columns"]:
    entry = ""
    if "url" in column:
        assert column["url"] == "ai-music/", "Unexpected column route"
        entry = f'<a class="column-entry" href="ai-music/">{esc(column["entry"])}</a>'
    cards.append(f'<article class="column-card" id="{esc(column["id"])}"><span class="label">{esc(column["label"])}</span><h3>{esc(column["title"])}</h3><p class="column-description">{esc(column["description"])}</p>{entry}{"".join(idea_card(idea) for idea in column["ideas"])}</article>')
index_fields = {"COLUMNS":"".join(cards), "COLUMN_COUNT":str(len(cards)), "IDEA_COUNT":str(sum(len(c["ideas"]) for c in catalog["columns"])), "UPDATED":esc(catalog["updated"]), "COMMIT":esc(commit)}

def render(template, replacements):
    text = (ROOT / "site" / template).read_text()
    for key, value in replacements.items():
        text = text.replace("{{"+key+"}}", value)
    assert "{{" not in text, "Unresolved template"
    for bad in ("/Users/", "/home/", "library/", "file://", "localhost", "127.0.0.1"):
        assert bad not in text, f"Private reference: {bad}"
    return text

out = ROOT / "dist"
(out / "ai-music").mkdir(parents=True,exist_ok=True)
(out / "index.html").write_text(render("index.html", index_fields))
(out / "ai-music/index.html").write_text(render("ai-music.html", fields))
for name in ("style.css", "favicon.svg"):
    shutil.copyfile(ROOT / "site" / name, out / name)
public_files = ("index.html", "ai-music/index.html", "style.css", "favicon.svg")
manifest = {"source_repository":"https://github.com/farmcan/video-creation", "source_commit":commit,"content_date":max(p["updated"],catalog["updated"]),"files":{name:hashlib.sha256((out/name).read_bytes()).hexdigest() for name in public_files}}
(out / "build-manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
print(f"Built {len(cards)} columns, {index_fields['IDEA_COUNT']} ideas and separate AI music detail")
