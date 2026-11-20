#!/usr/bin/env python3
r"""Copy your 13 finished MP4 and 13 .py files into this repository.

Example (run on the computer containing your files):
    python import_local_assets.py "C:\Users\YourName\Videos\LightAnimations"

Files are copied, not moved. Existing matching destination files are overwritten.
The import never creates or re-renders the videos.
"""
from pathlib import Path
import argparse
import json
import shutil

ROOT = Path(__file__).resolve().parent
FIGURES = json.loads((ROOT / "figures.json").read_text(encoding="utf-8"))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("folder", type=Path, help="Folder with Fig01_*.mp4 ... Fig13_*.mp4 and fig01_manim.py ... fig13_manim.py")
    ap.add_argument("--videos-only", action="store_true", help="Keep scripts already included in this repository")
    ap.add_argument("--scripts-only", action="store_true", help="Import only Python scripts")
    opts = ap.parse_args()
    if opts.videos_only and opts.scripts_only:
        ap.error("Use only one of --videos-only and --scripts-only")
    folder = opts.folder.expanduser().resolve()
    if not folder.is_dir():
        ap.error(f"Folder not found: {folder}")

    pairs = []
    for item in FIGURES:
        if not opts.videos_only:
            pairs.append((folder / item['python'], ROOT / 'scripts' / item['python']))
        if not opts.scripts_only:
            pairs.append((folder / item['video'], ROOT / 'docs' / 'videos' / item['video']))

    missing = [str(source) for source, dest in pairs if not source.is_file()]
    if missing:
        print("ERROR: Missing these files in your local folder:")
        for path in missing: print('  -', path)
        raise SystemExit(1)
    for source, dest in pairs:
        dest.parent.mkdir(parents=True, exist_ok=True)
        if source != dest.resolve():
            shutil.copy2(source, dest)
        print(f"OK: {source.name} -> {dest.relative_to(ROOT)}")
    print(f"Imported {len(pairs)} files. Publish the repository to make the videos accessible.")

if __name__ == "__main__":
    main()
