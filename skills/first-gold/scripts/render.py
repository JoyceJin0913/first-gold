#!/usr/bin/env python3
"""Render a First Gold progress.json into progress.html.

Usage:
    python3 render.py first-gold/<slug>/progress.json [output.html]

The page is built from ../assets/progress-template.html: only the JSON inside
<script id="fg-data" type="application/json"> is replaced, so the look stays the
same every time. Output defaults to progress.html next to progress.json.
"""
import json
import sys
from pathlib import Path

START_TAG = '<script id="fg-data" type="application/json">'
END_TAG = "</script>"


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: python3 render.py path/to/progress.json [output.html]")
        return 1

    src = Path(sys.argv[1])
    try:
        data = json.loads(src.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"error: {src} not found")
        return 1
    except json.JSONDecodeError as e:
        print(f"error: {src} is not valid JSON (line {e.lineno}, column {e.colno}): {e.msg}")
        return 1

    missing = [k for k in ("project", "steps") if k not in data]
    if missing:
        print(f"error: progress.json is missing required fields: {', '.join(missing)}")
        return 1

    template = Path(__file__).resolve().parent.parent / "assets" / "progress-template.html"
    html = template.read_text(encoding="utf-8")
    try:
        start = html.index(START_TAG) + len(START_TAG)
        end = html.index(END_TAG, start)
    except ValueError:
        print(f"error: data block not found in {template}")
        return 1

    payload = json.dumps(data, ensure_ascii=False, indent=2).replace("</", "<\\/")
    out = html[:start] + "\n" + payload + "\n" + html[end:]

    dst = Path(sys.argv[2]) if len(sys.argv) > 2 else src.with_name("progress.html")
    dst.write_text(out, encoding="utf-8")
    print(f"wrote {dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
