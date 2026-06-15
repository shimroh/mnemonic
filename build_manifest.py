#!/usr/bin/env python3
"""
Scan the images/ folder and write manifest.json that the gallery reads.

Rules
-----
- An image's SYSTEM is the first subfolder under images/.
    images/endo/thyroid_storm.png   -> system "Endo"
    images/cardio/afib.jpg          -> system "Cardio"
    images/loose_image.png          -> system "Uncategorized"
- An image's TITLE is derived from the filename (underscores/dashes -> spaces,
  title-cased), unless overridden in titles.json (see below).
- Anchors + explanation: put them in a text file next to the image with the SAME
  name, ending in .md (or .txt). It shows up under the image in the detail view.
    images/endo/palopegteriparatide.png
    images/endo/palopegteriparatide.md   <- anchors + explanation (Markdown)
  Markdown supported: **bold**, *italic*, `code`, [links](url), - bullets, # headings.
- Optional titles.json in the project root lets you set nicer titles/tags:
    {
      "images/endo/thyroid_storm.png": {"title": "Thyroid Storm — Burning House",
                                        "tags": ["thyroid", "hyperthyroid"]}
    }

Run it before pushing (or let the GitHub Action run it for you):
    python build_manifest.py
"""
import json
import os
from datetime import datetime, timezone

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".avif"}
ROOT = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(ROOT, "images")

# Acronyms to keep upper-cased when prettifying filenames
ACRONYMS = {"dka", "hhs", "tsh", "acth", "ms", "afib", "copd", "ckd", "uti",
            "gi", "ekg", "ecg", "cva", "pe", "dvt", "htn", "t1dm", "t2dm",
            "glp", "sglt2", "pcos", "siadh", "raas"}


def prettify(filename: str) -> str:
    base = os.path.splitext(filename)[0]
    words = base.replace("_", " ").replace("-", " ").split()
    out = []
    for w in words:
        out.append(w.upper() if w.lower() in ACRONYMS else w.capitalize())
    return " ".join(out).strip() or filename


def load_overrides() -> dict:
    path = os.path.join(ROOT, "titles.json")
    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"  ! titles.json is not valid JSON ({e}); ignoring it")
    return {}


def read_sidecar(abspath: str) -> str:
    """Return text from <image-basename>.md or .txt sitting next to the image."""
    base = os.path.splitext(abspath)[0]
    for ext in (".md", ".txt"):
        p = base + ext
        if os.path.exists(p):
            with open(p, encoding="utf-8") as f:
                return f.read().strip()
    return ""


def resolve_notes(abspath: str, ov: dict) -> str:
    """Notes priority: sidecar file > titles.json 'notes' > built from anchors/explanation."""
    sidecar = read_sidecar(abspath)
    if sidecar:
        return sidecar
    if ov.get("notes"):
        return ov["notes"]
    bits = []
    if ov.get("anchors"):
        bits.append("\n".join("- " + str(a) for a in ov["anchors"]))
    if ov.get("explanation"):
        bits.append(str(ov["explanation"]))
    return "\n\n".join(bits)


def main():
    if not os.path.isdir(IMAGES_DIR):
        print("No images/ folder found. Create one and add images, then re-run.")
        os.makedirs(IMAGES_DIR, exist_ok=True)

    overrides = load_overrides()
    images = []

    for dirpath, _dirs, files in os.walk(IMAGES_DIR):
        for fn in sorted(files):
            if os.path.splitext(fn)[1].lower() not in IMAGE_EXTS:
                continue
            abspath = os.path.join(dirpath, fn)
            rel = os.path.relpath(abspath, ROOT).replace(os.sep, "/")

            # system = first folder under images/
            parts = os.path.relpath(abspath, IMAGES_DIR).replace(os.sep, "/").split("/")
            system = parts[0].replace("_", " ").title() if len(parts) > 1 else "Uncategorized"

            ov = overrides.get(rel, {})
            images.append({
                "src": rel,
                "system": ov.get("system", system),
                "title": ov.get("title", prettify(fn)),
                "tags": ov.get("tags", []),
                "notes": resolve_notes(abspath, ov),
            })

    images.sort(key=lambda i: (i["system"].lower(), i["title"].lower()))
    systems = sorted({i["system"] for i in images})
    with_notes = sum(1 for i in images if i["notes"])

    manifest = {
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "count": len(images),
        "systems": systems,
        "images": images,
    }

    with open(os.path.join(ROOT, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"Wrote manifest.json — {len(images)} images across {len(systems)} system(s); "
          f"{with_notes} with anchors/notes.")
    for s in systems:
        n = sum(1 for i in images if i["system"] == s)
        print(f"  {s}: {n}")


if __name__ == "__main__":
    main()
