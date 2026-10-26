#!/usr/bin/env python3
"""Map a page's figure regions structurally, without needing to see pixels.

Usage:
    python3 figure_map.py PAPER.pdf 4 7 8 -o work/figmaps/
    python3 figure_map.py PAPER.pdf 4 --caption-lines 6

Why this exists: narrating a framework diagram well requires knowing where the
panels are and what labels sit in them. If the model reading this file CAN accept
images, the better move is to render the page (render_pages.py) and look at it.
If it cannot, this script recovers as much structure as the PDF's own objects allow:

  * image blocks, with bounding boxes and a coarse left/centre/right and
    top/middle/bottom classification, plus size in points;
  * vector text that lies inside or near a figure region — for diagrams drawn as
    PDF vectors, this is the actual set of on-figure labels, and their coordinates
    reveal the layout (which label is left of which, what is stacked above what);
  * the caption text and its page;
  * a note on whether the figure is vector-text-bearing or a flat raster, which
    tells you how much you can legitimately claim about its internals.

Limits: labels inside raster images (most result plots and many architecture
diagrams) are NOT recoverable. For those, ground the narration in the caption and
the surrounding body text, and do not assert panel positions, colours, or axis
ticks that you cannot verify.
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
        try:
            import fitz  # type: ignore
            return fitz
        except ImportError:
            return None


CAPTION_START = re.compile(
    r"(?:^|(?<=\s{3}))(?:Appendix\s+)?(?:Figure|Fig\.|Tables?)\s*([IVXLC]+|\d+)\s*[:.|]",
    re.IGNORECASE,
)


def hpos(x: float, width: float, page_w: float) -> str:
    if width > 0.55 * page_w:
        return "full-width"
    c = (x + width / 2) / page_w
    return "left" if c < 0.38 else ("centre" if c < 0.62 else "right")


def vpos(y0: float, y1: float, page_h: float) -> str:
    c = (y0 + y1) / 2 / page_h
    return "top" if c < 0.34 else ("middle" if c < 0.67 else "bottom")


def merge_regions(images: list[dict], gap: float = 40.0) -> list[dict]:
    """Merge overlapping / adjacent image blocks into figure regions.

    An architecture diagram is usually many small image blocks plus vector text.
    Treating each block as a figure produces noise; merging them by vertical
    overlap and horizontal proximity recovers the region a human would call
    "the figure".
    """
    boxes = sorted((dict(b) for b in images), key=lambda b: (b["y0"], b["x0"]))
    changed = True
    while changed:
        changed = False
        out: list[dict] = []
        for b in boxes:
            for r in out:
                v_overlap = not (b["y1"] < r["y0"] - gap or b["y0"] > r["y1"] + gap)
                h_close = not (b["x1"] < r["x0"] - gap or b["x0"] > r["x1"] + gap)
                if v_overlap and h_close:
                    r["x0"] = min(r["x0"], b["x0"])
                    r["y0"] = min(r["y0"], b["y0"])
                    r["x1"] = max(r["x1"], b["x1"])
                    r["y1"] = max(r["y1"], b["y1"])
                    r["w"] = r["x1"] - r["x0"]
                    r["h"] = r["y1"] - r["y0"]
                    r["n"] = r.get("n", 1) + 1
                    changed = True
                    break
            else:
                b["n"] = 1
                out.append(b)
        boxes = out
    return sorted(boxes, key=lambda b: (b["y0"], b["x0"]))


def map_page(page, pno: int, caption_lines: int, near_pad: float = 14.0) -> str:
    pw, ph = page.rect.width, page.rect.height
    d = page.get_text("dict")

    images: list[dict] = []
    texts: list[dict] = []
    for blk in d["blocks"]:
        x0, y0, x1, y1 = blk["bbox"]
        if blk.get("type") == 1:  # image
            images.append({"x0": x0, "y0": y0, "x1": x1, "y1": y1,
                           "w": x1 - x0, "h": y1 - y0})
            continue
        lines = []
        for ln in blk.get("lines", []):
            t = "".join(s.get("text", "") for s in ln.get("spans", [])).strip()
            if t:
                lines.append((ln["bbox"], t))
        if lines:
            texts.append({"x0": x0, "y0": y0, "x1": x1, "y1": y1, "lines": lines})

    regions = merge_regions(images)
    out: list[str] = [f"## Page {pno} — {pw:.0f} x {ph:.0f} pt\n"]

    # caption
    caps: list[str] = []
    page_lines = [ln for ln in page.get_text("text").splitlines() if ln.strip()]
    for i, ln in enumerate(page_lines):
        if CAPTION_START.search(ln):
            chunk = " ".join(page_lines[i:i + caption_lines])
            caps.append(re.sub(r"\s+", " ", chunk)[:400])
    if caps:
        out.append("**Caption(s) on this page**")
        for c in caps:
            out.append(f"- {c}")
        out.append("")

    # region -> on-figure labels
    labelled: list[tuple[dict, list[tuple[float, float, str]]]] = []
    for im in regions:
        inside: list[tuple[float, float, str]] = []
        for tb in texts:
            cx = (tb["x0"] + tb["x1"]) / 2
            cy = (tb["y0"] + tb["y1"]) / 2
            if (im["x0"] - near_pad <= cx <= im["x1"] + near_pad
                    and im["y0"] - near_pad <= cy <= im["y1"] + near_pad):
                for bb, t in tb["lines"]:
                    if not CAPTION_START.search(t):
                        inside.append((bb[0], bb[1], t))
        inside.sort(key=lambda r: (round(r[1] / 6), r[0]))
        labelled.append((im, inside))

    n_lab = sum(len(l) for _, l in labelled)
    out.append(f"**Digest:** {len(images)} image block(s) merged into "
               f"{len(regions)} figure region(s); {n_lab} on-figure vector label(s) "
               f"recovered.\n")

    if not regions:
        out.append("_No image blocks on this page._\n")
        return "\n".join(out)

    out.append("| region | position | bbox (x0,y0,x1,y1) | size pt | labels |")
    out.append("|---|---|---|---|---|")
    for i, (im, inside) in enumerate(labelled, 1):
        pos = f"{hpos(im['x0'], im['w'], pw)} / {vpos(im['y0'], im['y1'], ph)}"
        out.append(f"| {i} | {pos} | {im['x0']:.0f},{im['y0']:.0f},"
                   f"{im['x1']:.0f},{im['y1']:.0f} | {im['w']:.0f} x {im['h']:.0f} | "
                   f"{len(inside)} |")
    out.append("")

    for i, (im, inside) in enumerate(labelled, 1):
        out.append(f"**Region {i}** "
                   f"({hpos(im['x0'], im['w'], pw)} / {vpos(im['y0'], im['y1'], ph)}, "
                   f"{im['w']:.0f}x{im['h']:.0f} pt)")
        if inside:
            for x, y, t in inside[:60]:
                col = "left" if x < pw * 0.38 else (
                    "centre" if x < pw * 0.62 else "right")
                out.append(f"- x={x:.0f} y={y:.0f} [{col}] {t[:90]}")
            if len(inside) > 60:
                out.append(f"- ... {len(inside) - 60} more")
            out.append("- _Order by (y, x): same y band = one visual row; same x band "
                       "= one column. Treat these as on-figure labels only if they "
                       "read like labels rather than body prose._")
        else:
            out.append("- _No recoverable labels: the region is flat raster. Its panel "
                       "layout, colours, and axis values are NOT in the PDF text. "
                       "Narrate from the caption and body text; do not assert internals "
                       "you cannot verify._")
        out.append("")

    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf")
    ap.add_argument("pages", nargs="+")
    ap.add_argument("-o", "--outdir", default=None,
                    help="write one .md per page into this directory instead of stdout")
    ap.add_argument("--caption-lines", type=int, default=5)
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
        wanted: list[int] = []
        for spec in args.pages:
            m = re.fullmatch(r"(\d+)\s*-\s*(\d+)", spec)
            if m:
                a, b = int(m.group(1)), int(m.group(2))
                wanted.extend(range(min(a, b), max(a, b) + 1))
            elif spec.isdigit():
                wanted.append(int(spec))
            else:
                print(f"error: bad page spec {spec!r}", file=sys.stderr)
                return 2
        wanted = [p for p in dict.fromkeys(wanted) if 1 <= p <= npages]
        if not wanted:
            print(f"error: no valid pages (document has {npages})", file=sys.stderr)
            return 2

        if args.outdir:
            os.makedirs(args.outdir, exist_ok=True)
        for p in wanted:
            block = map_page(doc.load_page(p - 1), p, args.caption_lines)
            if args.outdir:
                path = os.path.join(args.outdir, f"figmap_{p:03d}.md")
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(block)
                print(f"wrote {path}")
            else:
                print(block)
    finally:
        doc.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())