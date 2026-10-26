#!/usr/bin/env python3
"""Extract a paper PDF into page-marked text files plus a structure inventory.

Usage:
    python3 extract_paper.py PAPER.pdf -o work/ [--slug myslug]
                                       [--engine auto|pymupdf|pdftotext]

Outputs (in the output directory):
    <slug>.paged.txt      reading-order text with '<!-- page N -->' markers.
                          Best available engine: column-aware PyMuPDF, else
                          `pdftotext -layout`.
    <slug>.layout.txt     `pdftotext -layout` rendering (only when pdftotext is
                          available). Keeps equations and tables spatially intact;
                          reserve it for reading math, not for reading prose.
    <slug>.structure.md   sections / figures / tables / equations with page numbers,
                          plus a proper-noun frequency table. Headings are detected
                          from font weight and size when PyMuPDF is available,
                          otherwise from text patterns.

Both text files are heuristics. Confirm anything load-bearing by reading around it
and by looking at the rendered page (see render_pages.py).
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from collections import Counter

# ---------------------------------------------------------------- extraction


def extract_pdftotext(pdf: str) -> list[str]:
    exe = shutil.which("pdftotext")
    if not exe:
        return []
    try:
        out = subprocess.run(
            [exe, "-layout", "-enc", "UTF-8", pdf, "-"],
            capture_output=True, check=True,
        ).stdout.decode("utf-8", "replace")
    except (subprocess.CalledProcessError, OSError):
        return []
    pages = out.split("\f")
    if pages and not pages[-1].strip():
        pages.pop()
    return pages


def _load_pymupdf():
    try:
        import pymupdf  # type: ignore
        return pymupdf
    except ImportError:
        return None


def extract_ordered(pdf: str):
    """Column-aware extraction. Returns (pages, headings).

    Reconstructs reading order for two-column layouts: full-width blocks
    (figures, tables, wide captions) act as separators, and the column blocks
    between two separators are emitted left column first, then right column.
    Headings are detected from span font size/weight.
    """
    pymupdf = _load_pymupdf()
    if pymupdf is None:
        return [], []

    doc = pymupdf.open(pdf)
    pages: list[str] = []
    all_headings: list[tuple[int, str]] = []
    try:
        for pno, page in enumerate(doc, start=1):
            pw = page.rect.width or 1.0
            blocks: list[dict] = []
            heading_sizes: Counter = Counter()
            for blk in page.get_text("dict")["blocks"]:
                if blk.get("type") != 0:
                    continue
                lines_out: list[str] = []
                line_meta: list[tuple[str, float, bool, float]] = []
                for ln in blk.get("lines", []):
                    spans = ln.get("spans", [])
                    if not spans:
                        continue
                    text = "".join(s.get("text", "") for s in spans)
                    if not text.strip():
                        continue
                    size = max((s.get("size", 0.0) for s in spans), default=0.0)
                    # PyMuPDF span flag bit 4 (value 16) marks bold/black weight
                    bold = any(int(s.get("flags", 0)) & 16 for s in spans)
                    bold_chars = sum(
                        len(s.get("text", "")) for s in spans
                        if int(s.get("flags", 0)) & 16
                    )
                    mostly_bold = bold_chars >= 0.6 * max(len(text), 1)
                    line_meta.append((text.rstrip(), size, mostly_bold, ln["bbox"][0]))
                    lines_out.append(text.rstrip())
                if not lines_out:
                    continue
                x0, y0, x1, y1 = blk["bbox"]
                blocks.append({
                    "text": "\n".join(lines_out),
                    "x0": x0, "y0": y0, "x1": x1, "y1": y1,
                    "width": x1 - x0,
                    "center": (x0 + x1) / 2.0,
                    "meta": line_meta,
                    "nlines": len(lines_out),
                })
                for text, size, mostly_bold, _ in line_meta:
                    if mostly_bold and 1 < len(text.strip()) <= 80:
                        heading_sizes[round(size, 1)] += 1

            if not blocks:
                pages.append("")
                continue

            body_size = heading_sizes.most_common(1)[0][0] if heading_sizes else 0.0
            sizes = [b["meta"][0][1] for b in blocks if b["meta"]]
            if sizes:
                body_size = Counter(round(s, 1) for s in sizes).most_common(1)[0][0]

            full_width = pw * 0.55
            sep = [b for b in blocks if b["width"] > full_width]
            col = [b for b in blocks if b["width"] <= full_width]
            left = [b for b in col if b["center"] < pw / 2.0]
            right = [b for b in col if b["center"] >= pw / 2.0]
            left.sort(key=lambda b: b["y0"])
            right.sort(key=lambda b: b["y0"])
            sep.sort(key=lambda b: b["y0"])

            ordered: list[dict] = []
            li = ri = 0
            for s in sep:
                while li < len(left) and left[li]["y1"] <= s["y0"]:
                    ordered.append(left[li]); li += 1
                while ri < len(right) and right[ri]["y1"] <= s["y0"]:
                    ordered.append(right[ri]); ri += 1
                ordered.append(s)
            ordered.extend(left[li:])
            ordered.extend(right[ri:])

            page_text = "\n\n".join(b["text"] for b in ordered)
            pages.append(page_text)

            for b in ordered:
                for text, size, mostly_bold, _ in b["meta"]:
                    stripped = text.strip()
                    if not stripped or len(stripped) > 80:
                        continue
                    if not is_plausible(stripped):
                        continue
                    # Only a genuine font-size increase marks a heading here.
                    # Bold run-in labels inside paragraphs are not headings; the
                    # text-pattern pass below catches numbered/named headings.
                    if size >= body_size + 0.5:
                        all_headings.append((pno, re.sub(r"\s+", " ", stripped)))
    finally:
        doc.close()
    return pages, all_headings


# ---------------------------------------------------------------- heuristics

NUMBERED_HEADING = re.compile(
    r"^\s*(?:\d+(?:\.\d+)*|[IVX]+)[.)]?\s+[A-Z\u03c0][A-Za-z0-9\u03c0\-:,()/' ]{1,70}$"
)
ALLCAPS_HEADING = re.compile(r"^\s*[A-Z][A-Z0-9 \-:,()/&\.]{3,60}$")
KNOWN_HEADING = re.compile(
    r"^\s*(Abstract|Introduction|Related Work|Background|Overview|Method|Methods|"
    r"Model|Models|Approach|Experiments?|Experimental Evaluation|Evaluation|"
    r"Results|Discussion|Limitations?(?: and Future Work)?|Conclusion|Conclusions|"
    r"Acknowledge?ments?|References|Appendix|Keywords)\s*[:.]?\s*\d*\s*$",
    re.IGNORECASE,
)

_CAP_PREFIX = r"(?:^|(?<=\s{3}))(?:Appendix\s+)?"
CAPTION_FIG = re.compile(
    _CAP_PREFIX + r"(?:Figure|Fig\.)\s*(\d+)\s*[:.|]\s*(\S.*)$", re.IGNORECASE)
CAPTION_FIG_LABEL = re.compile(
    _CAP_PREFIX + r"(?:Figure|Fig\.)\s*(\d+)\s*$", re.IGNORECASE)
CAPTION_TAB = re.compile(
    _CAP_PREFIX + r"Tables?\s*([IVXLC]+|\d+)\s*[:.|]\s*(\S.*)$", re.IGNORECASE)
CAPTION_TAB_LABEL = re.compile(
    _CAP_PREFIX + r"Tables?\s*([IVXLC]+|\d+)\s*$", re.IGNORECASE)
CAPTION_ANY = re.compile(
    _CAP_PREFIX + r"(?:Figure|Fig\.|Tables?)\s*([IVXLC]+|\d+)\s*[:.|]?", re.IGNORECASE)
EQ_NUMBERED = re.compile(r"\((\d{1,2})\)\s*$")
MATH_HINT = re.compile(r"[=∑∏∫√≈≤≥]|\b(?:argmax|argmin|softmax|exp|log)\b|\^|_\{")

PROPER_NOUN = re.compile(
    r"\b(?:[A-Z][a-z]*[A-Z][A-Za-z0-9\-]*"
    r"|[A-Z]{2,}[0-9\-]*"
    r"|[A-Z][a-z]+[0-9]+[A-Za-z0-9\-]*)"
)

SENTENCE_TAIL = re.compile(r"[a-z,;]\s*$")

# Some PDFs embed Type3/CID fonts whose ToUnicode map is broken, so extraction
# yields strings like "°2G)©¯SO/,SG )¡G". Such lines poison headings, captions,
# and the proper-noun list. Drop any line whose characters are mostly implausible.
CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f\ufeff]")
PLAUSIBLE_CHAR = re.compile(
    r"[A-Za-z0-9 \t.,;:!?'\"()\[\]{}/\\%+\-–—_*&#@<>|=~^$°±×÷"
    r"\u00c0-\u024f\u0370-\u03ff\u2010-\u203a\u2070-\u209f\u20a0-\u20bf"
    r"\u2100-\u214f\u2190-\u21ff\u2200-\u22ff\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]"
)


def is_plausible(text: str, threshold: float = 0.72) -> bool:
    """True when a line looks like real text rather than a broken font mapping."""
    kept = "".join(PLAUSIBLE_CHAR.findall(text))
    if not text.strip():
        return True
    return len(kept) / max(len(text), 1) >= threshold


WORD = re.compile(r"[A-Za-z][A-Za-z'\-]*")


def looks_like_latin_prose(text: str) -> bool:
    """Reject garbled ASCII that survives the charset check.

    Broken Type3 font maps often yield strings such as "Z)0./GSO/,SGL" that are
    made only of ordinary ASCII characters. Real English text has several
    vowel-bearing alphabetic words.
    """
    words = WORD.findall(text)
    if len(words) < 2:
        return False
    with_vowel = sum(1 for w in words if re.search(r"[aeiouyAEIOUY]", w))
    alpha = sum(len(w) for w in words)
    return with_vowel >= 2 and alpha / max(len(text), 1) >= 0.5


def clean_pages(pages: list[str]) -> tuple[list[str], int]:
    dropped = 0
    out: list[str] = []
    for text in pages:
        lines = []
        for line in CONTROL_CHARS.sub("", text).splitlines():
            if line.strip() and not is_plausible(line):
                dropped += 1
                continue
            lines.append(line)
        out.append("\n".join(lines))
    return out, dropped


def title_like(text: str) -> bool:
    """A believable heading: short, no sentence tail, not a prose fragment."""
    stripped = text.strip()
    if not (3 < len(stripped) <= 70):
        return False
    if stripped.endswith((",", ";", "-", "—")):
        return False
    if stripped.count(".") and stripped.endswith(".") and not stripped.isupper():
        return False
    if len(WORD.findall(stripped)) > 10:
        return False
    return True


def detect_headings(pages: list[str], font_headings: list[tuple[int, str]]):
    """Returns (pattern_headings, font_candidates).

    Pattern headings match numbered / ALL-CAPS / known-name forms and are reliable
    for IEEE-style papers. Font candidates are any line set in a larger type size;
    they reliably include the headings of papers whose headings are unnumbered but
    also sweep in abstract text and bold run-in labels, so they must be verified.
    """
    pattern: list[tuple[int, str]] = []
    seen_pattern: set[str] = set()
    for pno, text in enumerate(pages, start=1):
        for raw in text.splitlines():
            line = raw.strip()
            if not title_like(line) or MATH_HINT.search(line):
                continue
            if not is_plausible(line) or not looks_like_latin_prose(line):
                continue
            hit = None
            if KNOWN_HEADING.match(line):
                hit = line
            elif ALLCAPS_HEADING.match(line) and not line.endswith("."):
                hit = line
            elif NUMBERED_HEADING.match(line):
                hit = line
            if not hit:
                continue
            hit = re.sub(r"\s+", " ", hit)
            key = hit.lower()
            if key in seen_pattern:
                continue
            seen_pattern.add(key)
            pattern.append((pno, hit))

    candidates: list[tuple[int, str]] = []
    seen_cand: set[str] = set(seen_pattern)
    for pno, h in font_headings:
        h = re.sub(r"\s+", " ", h).strip()
        key = h.lower()
        if not h or key in seen_cand or not is_plausible(h) or not title_like(h):
            continue
        if h.count(",") > 1:
            continue
        if not h.isupper() and not looks_like_latin_prose(h):
            continue
        seen_cand.add(key)
        candidates.append((pno, h))

    pattern.sort(key=lambda t: t[0])
    candidates.sort(key=lambda t: t[0])
    return pattern, candidates[:60]


def detect_captions(pages: list[str]):
    """Find figure/table captions. Handles 'Figure 3: text', 'Figure 3 | text',
    'TABLE I: text', and a bare label with the caption on following lines."""
    figs: list[tuple[str, int, str]] = []
    tabs: list[tuple[str, int, str]] = []
    for pno, text in enumerate(pages, start=1):
        lines = text.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i]
            m_f = CAPTION_FIG.search(line)
            m_t = CAPTION_TAB.search(line)
            m_f2 = CAPTION_FIG_LABEL.search(line) if not (m_f or m_t) else None
            m_t2 = CAPTION_TAB_LABEL.search(line) if not (m_f or m_t or m_f2) else None
            if not (m_f or m_t or m_f2 or m_t2):
                i += 1
                continue

            if m_f or m_t:
                m = m_f or m_t
                buf = [m.group(2).strip()]
                j = i + 1
            else:
                m = m_f2 or m_t2
                buf = []
                j = i + 1

            while j < len(lines) and len(buf) < 4:
                nxt = lines[j].strip()
                if not nxt or CAPTION_ANY.search(nxt) or not is_plausible(nxt):
                    break
                if not looks_like_latin_prose(nxt) and not re.search(r"[a-z]", nxt):
                    break
                buf.append(nxt)
                j += 1

            caption = re.sub(r"\s+", " ", " ".join(buf)).strip()
            is_fig = bool(m_f or m_f2)
            if is_fig:
                figs.append((m.group(1), pno, caption))
            else:
                tabs.append((m.group(1), pno, caption))
            i = max(j, i + 1)
    return figs, tabs


def detect_equations(pages: list[str]):
    numbered: list[tuple[str, int, str]] = []
    candidates: list[tuple[int, str]] = []
    for pno, text in enumerate(pages, start=1):
        for raw in text.splitlines():
            line = raw.strip()
            if len(line) < 8:
                continue
            m = EQ_NUMBERED.search(line)
            if m and ("=" in line or MATH_HINT.search(line)):
                numbered.append((m.group(1), pno, line[:220]))
                continue
            if "=" in line and MATH_HINT.search(line) and len(line) > 20:
                candidates.append((pno, line[:220]))
    return numbered, candidates


def proper_nouns(pages: list[str]) -> Counter:
    c: Counter = Counter()
    for text in pages:
        for line in text.splitlines():
            if not is_plausible(line):
                continue
            for tok in PROPER_NOUN.findall(line):
                if len(tok) < 2:
                    continue
                # require a vowel, or an acronym of 2-6 caps/digits
                if not re.search(r"[aeiouyAEIOUY]", tok) and not re.fullmatch(
                        r"[A-Z0-9\-]{2,6}", tok):
                    continue
                c[tok] += 1
    return c


# ---------------------------------------------------------------- reporting


def build_structure(pages, headings, slug, engine) -> str:
    pattern_h, font_h = headings
    figs, tabs = detect_captions(pages)
    eqn, eqc = detect_equations(pages)
    nouns = proper_nouns(pages)

    out: list[str] = [f"# Structure inventory — {slug}\n",
                      f"Pages: {len(pages)}  ·  text engine: {engine}\n",
                      "This file is a FIRST PASS. The authoritative section list is the "
                      "paper's own table of contents and its printed headings — read the "
                      "paged text and confirm before writing.\n"]

    out.append("## Sections — pattern matches (numbered / ALL-CAPS / known names)\n")
    if pattern_h:
        out.append("| page | heading |")
        out.append("|---|---|")
        for pno, h in pattern_h:
            out.append(f"| p{pno} | {h} |")
    else:
        out.append("_none matched. The paper may use unnumbered bold headings; use the "
                   "candidates below and the paged text._")
    out.append("")

    out.append("## Sections — font-size candidates (VERIFY; excludes pattern matches)\n")
    if font_h:
        out.append("| page | candidate |")
        out.append("|---|---|")
        for pno, h in font_h:
            out.append(f"| p{pno} | {h} |")
        out.append("")
        out.append("Large-type text also includes abstract body and bold figure labels. "
                   "Keep only real section headings.")
    else:
        out.append("_none_")
    out.append("")

    out.append("## Figures\n")
    if figs:
        for num, pno, cap in figs:
            out.append(f"- FIG {num} | p{pno} | {cap}")
    else:
        out.append("_none detected_")
    out.append("")
    out.append("Note: captions in two-column layouts can absorb adjacent body text. "
               "Trim each caption to its first sentence when writing the script.")
    out.append("")

    out.append("## Tables\n")
    if tabs:
        for num, pno, cap in tabs:
            out.append(f"- TAB {num} | p{pno} | {cap}")
    else:
        out.append("_none detected_")
    out.append("")

    out.append("## Numbered equations\n")
    if eqn:
        for num, pno, line in eqn:
            out.append(f"- EQ num={num} | p{pno} | {line}")
    else:
        out.append("_no numbered equations detected. Many papers print display "
                   "equations WITHOUT numbers — every such equation still has to be "
                   "explained. Find them in the candidate list and in the layout file._")
    out.append("")

    out.append("## Candidate display equations (numbered or not)\n")
    if eqc:
        for pno, line in eqc[:100]:
            out.append(f"- EQ~ | p{pno} | {line}")
        if len(eqc) > 100:
            out.append(f"- ... {len(eqc) - 100} more")
    else:
        out.append("_none detected_")
    out.append("")

    out.append("## Proper nouns by frequency (canonical spellings to copy)\n")
    for tok, n in nouns.most_common(140):
        if n < 2 and len(tok) < 5:
            continue
        out.append(f"- {tok} ×{n}")
    out.append("")

    out.append("## Cross-reference check\n")
    out.append("Figure labels found in the text (compare with the Figures list above; "
               "a number present here but missing above means the caption was not "
               "detected — read that page directly):\n")
    refs: Counter = Counter()
    for text in pages:
        for m in re.findall(r"\b(?:Figure|Fig\.)\s*\d+", text, re.IGNORECASE):
            refs[re.sub(r"\s+", " ", m)] += 1
    for r, n in refs.most_common(80):
        out.append(f"- {r} ×{n}")
    out.append("")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf")
    ap.add_argument("-o", "--outdir", default="work")
    ap.add_argument("--slug", default=None)
    ap.add_argument("--engine", choices=["auto", "pymupdf", "pdftotext"],
                    default="auto")
    ap.add_argument("--no-structure", action="store_true")
    args = ap.parse_args()

    if not os.path.isfile(args.pdf):
        print(f"error: no such file: {args.pdf}", file=sys.stderr)
        return 2

    slug = args.slug or re.sub(
        r"[^A-Za-z0-9\u03c0]+", "-", os.path.splitext(os.path.basename(args.pdf))[0]
    ).strip("-")[:60] or "paper"

    font_headings: list[tuple[int, str]] = []
    pages: list[str] = []
    engine = ""

    if args.engine in ("auto", "pymupdf"):
        pages, font_headings = extract_ordered(args.pdf)
        if pages:
            engine = "pymupdf (column-aware)"

    layout_pages = extract_pdftotext(args.pdf)

    if not pages:
        if not layout_pages:
            print("error: could not extract text (no PyMuPDF and no pdftotext)",
                  file=sys.stderr)
            return 3
        pages = layout_pages
        engine = "pdftotext -layout"

    pages, dropped = clean_pages(pages)
    if dropped:
        print(f"note: dropped {dropped} line(s) with implausible characters "
              f"(broken font mapping). Read those pages as images instead.")

    os.makedirs(args.outdir, exist_ok=True)

    paged_path = os.path.join(args.outdir, f"{slug}.paged.txt")
    with open(paged_path, "w", encoding="utf-8") as fh:
        for i, text in enumerate(pages, start=1):
            fh.write(f"<!-- page {i} -->\n{text.strip()}\n\n")

    print(f"extracted {len(pages)} pages via {engine}")
    print(f"wrote {paged_path}")

    if layout_pages:
        layout_path = os.path.join(args.outdir, f"{slug}.layout.txt")
        with open(layout_path, "w", encoding="utf-8") as fh:
            for i, text in enumerate(layout_pages, start=1):
                fh.write(f"<!-- page {i} -->\n{text.strip()}\n\n")
        print(f"wrote {layout_path}  (use this one to read equations/tables)")

    if not args.no_structure:
        headings = detect_headings(pages, font_headings)
        struct_path = os.path.join(args.outdir, f"{slug}.structure.md")
        with open(struct_path, "w", encoding="utf-8") as fh:
            fh.write(build_structure(pages, headings, slug, engine))
        figs, tabs = detect_captions(pages)
        eqn, _ = detect_equations(pages)
        print(f"wrote {struct_path}")
        print(f"detected: {len(headings)} headings, {len(figs)} figures, "
              f"{len(tabs)} tables, {len(eqn)} numbered equations")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())