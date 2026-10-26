#!/usr/bin/env python3
"""Render specific PDF pages to PNG so figures can actually be looked at.

Usage:
    python3 render_pages.py PAPER.pdf 1 3 5 7 -o work/pages/ --dpi 150
    python3 render_pages.py PAPER.pdf 8-12 --dpi 200

Requires PyMuPDF (`pip install pymupdf`). Output files are named
`page_001.png`, `page_002.png`, ... and are intended to be opened with an image
reader, not just referenced.

Why this matters: figure layout (which panel is left, where arrows point, which
curve is on top) cannot be recovered from extracted text. Narrate a figure only
after viewing its page.
"""

from __future__ import annotations

import argparse
import os
import re
import sys


def load_pymupdf():
    try:
        import pymupdf  # type: ignore
        return pymupdf
    except ImportError:
        pass
    try:
        import fitz  # type: ignore
        return fitz
    except ImportError:
        return None


def parse_pages(specs: list[str], npages: int) -> list[int]:
    out: list[int] = []
    for spec in specs:
        spec = spec.strip()
        m = re.fullmatch(r"(\d+)\s*-\s*(\d+)", spec)
        if m:
            a, b = int(m.group(1)), int(m.group(2))
            if a > b:
                a, b = b, a
            out.extend(range(a, b + 1))
        elif spec.isdigit():
            out.append(int(spec))
        else:
            raise ValueError(f"bad page spec: {spec!r} (use 5 or 8-12)")
    seen: set[int] = set()
    result: list[int] = []
    for p in out:
        if 1 <= p <= npages and p not in seen:
            seen.add(p)
            result.append(p)
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf")
    ap.add_argument("pages", nargs="+", help="page numbers or ranges, e.g. 1 3 8-12")
    ap.add_argument("-o", "--outdir", default="pages")
    ap.add_argument("--dpi", type=int, default=150,
                    help="render resolution; 150 is readable, 200+ for dense tables")
    ap.add_argument("--prefix", default="page")
    args = ap.parse_args()

    if not os.path.isfile(args.pdf):
        print(f"error: no such file: {args.pdf}", file=sys.stderr)
        return 2

    pymupdf = load_pymupdf()
    if pymupdf is None:
        print("error: PyMuPDF is required (`pip install pymupdf`)", file=sys.stderr)
        return 3

    doc = pymupdf.open(args.pdf)
    try:
        npages = doc.page_count
        try:
            pages = parse_pages(args.pages, npages)
        except ValueError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        if not pages:
            print(f"error: no valid pages (document has {npages})", file=sys.stderr)
            return 2

        os.makedirs(args.outdir, exist_ok=True)
        written: list[str] = []
        for p in pages:
            page = doc.load_page(p - 1)
            pix = page.get_pixmap(dpi=args.dpi)
            name = f"{args.prefix}_{p:03d}.png"
            path = os.path.join(args.outdir, name)
            pix.save(path)
            written.append(path)
            print(f"wrote {path}  ({pix.width}x{pix.height})")

        print(f"\n{len(written)} page(s) rendered from {npages}-page document.")
        print("Open these with an image reader before narrating their figures.")
    finally:
        doc.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())