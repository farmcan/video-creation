#!/usr/bin/env python3
"""Explicitly export only the generated public notebook to the existing host."""
import argparse
import shutil
import subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--target", required=True, type=Path)
args = parser.parse_args()
subprocess.run(["python3", str(ROOT / "scripts/build.py")], check=True)
target = args.target.resolve()
assert (target / "sites.json").is_file(), "Expected the existing navigation checkout"
out = target / "site/creation"
out.mkdir(parents=True,exist_ok=True)
for name in ("index.html","ai-music/index.html","style.css","favicon.svg","build-manifest.json"):
    (out / name).parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(ROOT / "dist" / name, out / name)
print("Exported the explicit public bundle into site/creation")
