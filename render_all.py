#!/usr/bin/env python3
"""Render one/all Manim scenes into MP4 files with the exact published filenames.

If you already rendered your 13 MP4s, run import_local_assets.py instead:
    python import_local_assets.py "C:\\path\\to\\your\\folder"
"""
from pathlib import Path
import argparse
import json
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
MEDIA = ROOT / "media"
OUT = ROOT / "docs" / "videos"
FIGURES = {item["figure"]: item for item in json.loads((ROOT / "figures.json").read_text(encoding="utf-8"))}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--quality", choices=["low", "medium", "high", "production", "4k"], default="high")
    ap.add_argument("--figure", type=int, choices=sorted(FIGURES), help="Render only one figure")
    opts = ap.parse_args()
    qual = {"low": "-ql", "medium": "-qm", "high": "-qh", "production": "-qp", "4k": "-qk"}[opts.quality]
    OUT.mkdir(parents=True, exist_ok=True)
    selection = [FIGURES[opts.figure]] if opts.figure else FIGURES.values()

    for item in selection:
        filename = item["python"]
        scene = item["scene"]
        video = item["video"]
        cmd = [sys.executable, "-m", "manim", qual, "--format=mp4", "--media_dir", str(MEDIA),
               "-o", video, str(ROOT / "scripts" / filename), scene]
        print(f"Rendering Figure {item['figure']:02d}: {filename} ({scene})", flush=True)
        subprocess.run(cmd, check=True, cwd=ROOT)
        candidates = [p for p in MEDIA.rglob(video) if p.is_file()]
        if not candidates:
            raise FileNotFoundError(f"Manim did not generate {video} in {MEDIA}")
        source = max(candidates, key=lambda p: p.stat().st_mtime)
        target = OUT / video
        shutil.copy2(source, target)
        print(f"Published: {target}", flush=True)


if __name__ == "__main__":
    main()
