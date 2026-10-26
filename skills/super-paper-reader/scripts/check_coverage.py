#!/usr/bin/env python3
"""Check a lecture-script draft for coverage of the paper's figures/tables/equations.

Usage:
    python3 check_coverage.py work/<slug>.structure.md DRAFT.md
    python3 check_coverage.py work/<slug>.structure.md DRAFT.md --main-figures-only 1-8

Reads the `- FIG n | pN | caption`, `- TAB n | pN | ...` and `- EQ num=n | pN | ...`
lines written by extract_paper.py, then looks for each identifier in the draft in
the forms a Chinese lecture script would actually use:

    图 3 / 图3 / 图三 / Figure 3 / Fig. 3 / 图 3a
    表 2 / 表2 / 表二 / Table 2 / TABLE I
    公式 1 / 式(1) / Equation 1 / (1)

Exit code is 0 when every *main-text* figure is covered and 1 otherwise, so it can
gate a delivery step. Tables and equations are reported but do not fail the run by
default (use --strict to include them).

A figure the draft does not mention is not automatically a defect: some figures are
peripheral. But the main framework figure and every evidence figure must be covered.
"""

from __future__ import annotations

import argparse
import re
import sys

CN_DIGITS = "零一二三四五六七八九"


def to_cn(n: int) -> str:
    if n < 10:
        return CN_DIGITS[n]
    if n < 20:
        return "十" + (CN_DIGITS[n % 10] if n % 10 else "")
    if n < 100:
        return CN_DIGITS[n // 10] + "十" + (CN_DIGITS[n % 10] if n % 10 else "")
    return str(n)


ROMAN = {
    "I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7, "VIII": 8,
    "IX": 9, "X": 10, "XI": 11, "XII": 12, "XIII": 13, "XIV": 14, "XV": 15,
    "XVI": 16, "XVII": 17, "XVIII": 18, "XIX": 19, "XX": 20,
}


def parse_inventory(path: str):
    figs, tabs, eqs = [], [], []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            m = re.match(r"^-\s*FIG\s+(\S+)\s*\|\s*p(\d+)\s*\|(.*)$", line.strip())
            if m:
                figs.append((m.group(1), int(m.group(2)), m.group(3).strip()))
                continue
            m = re.match(r"^-\s*TAB\s+(\S+)\s*\|\s*p(\d+)\s*\|(.*)$", line.strip())
            if m:
                tabs.append((m.group(1), int(m.group(2)), m.group(3).strip()))
                continue
            m = re.match(r"^-\s*EQ\s+num=(\S+)\s*\|\s*p(\d+)\s*\|(.*)$", line.strip())
            if m:
                eqs.append((m.group(1), int(m.group(2)), m.group(3).strip()))
    return figs, tabs, eqs


def roman_to_int(s: str):
    s = s.upper()
    return ROMAN.get(s)


CN_GUARD = r"(?![\d一二三四五六七八九十])"


def mentions(text: str, ident: str, kind: str) -> bool:
    """Does the draft reference this figure/table/equation identifier?

    Chinese lecture scripts mix Arabic and Chinese numerals ("图 3", "图三",
    "图表一") and sometimes say "图表" where they mean either a figure or a table,
    so those forms are accepted for both kinds.
    """
    num = int(ident) if ident.isdigit() else roman_to_int(ident)
    ident_re = re.escape(ident)

    forms: list[str] = []
    if kind == "fig":
        if num is not None:
            cn = to_cn(num)
            forms += [
                rf"图\s*{num}(?!\d)",
                rf"图\s*{cn}{CN_GUARD}",
                rf"图表\s*{num}(?!\d)",
                rf"图表\s*{cn}{CN_GUARD}",
                rf"[Ff]ig(?:ure)?\.?\s*{num}(?!\d)",
                rf"[Ff]ig(?:ure)?\.?\s*{ident_re}(?!\w)",
            ]
        else:
            forms += [rf"图\s*{ident_re}(?!\w)",
                      rf"[Ff]ig(?:ure)?\.?\s*{ident_re}(?!\w)"]
    elif kind == "tab":
        if num is not None:
            cn = to_cn(num)
            forms += [
                rf"表\s*{num}(?!\d)",
                rf"表\s*{cn}{CN_GUARD}",
                rf"图表\s*{num}(?!\d)",
                rf"图表\s*{cn}{CN_GUARD}",
                rf"[Tt]able\s*{num}(?!\d)",
                rf"[Tt]able\s*{ident_re}(?!\w)",
            ]
        else:
            forms += [rf"表\s*{ident_re}(?!\w)",
                      rf"[Tt]able\s*{ident_re}(?!\w)"]
    else:  # equation
        if num is not None:
            forms += [rf"公式\s*{num}(?!\d)", rf"式\s*[（(]?\s*{num}\s*[)）]",
                      rf"[Ee]quation\s*{num}(?!\d)", rf"损失函数\s*{num}(?!\d)",
                      rf"\(\s*{num}\s*\)"]
        else:
            forms += [rf"公式\s*{ident_re}(?!\w)",
                      rf"式\s*[（(]?\s*{ident_re}\s*[)）]"]
    return any(re.search(f, text) for f in forms)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inventory", help="<slug>.structure.md from extract_paper.py")
    ap.add_argument("draft", help="the lecture script draft")
    ap.add_argument("--main-figures-only", default=None,
                    help="restrict the failing check to these figure numbers, "
                         "e.g. 1-8 (appendix figures excluded)")
    ap.add_argument("--strict", action="store_true",
                    help="also fail on uncovered tables and equations")
    args = ap.parse_args()

    try:
        figs, tabs, eqs = parse_inventory(args.inventory)
    except OSError as exc:
        print(f"error: cannot read inventory: {exc}", file=sys.stderr)
        return 2
    try:
        with open(args.draft, encoding="utf-8") as fh:
            draft = fh.read()
    except OSError as exc:
        print(f"error: cannot read draft: {exc}", file=sys.stderr)
        return 2

    if not figs and not tabs and not eqs:
        print("warning: inventory contained no FIG/TAB/EQ lines — nothing to check.")
        return 0

    required: set[int] | None = None
    if args.main_figures_only:
        lo, _, hi = args.main_figures_only.partition("-")
        required = set(range(int(lo), int(hi or lo) + 1))

    def report(items, kind, label):
        missing, covered = [], []
        for ident, page, cap in items:
            ok = mentions(draft, ident, kind)
            (covered if ok else missing).append((ident, page, cap))
        print(f"\n### {label}: {len(covered)}/{len(items)} covered")
        if missing:
            for ident, page, cap in missing:
                print(f"  MISSING  {label[:-1]} {ident}  (p{page})  {cap[:110]}")
        return missing

    miss_f = report(figs, "fig", "Figures")
    miss_t = report(tabs, "tab", "Tables")
    miss_e = report(eqs, "eq", "Equations")

    hard_fail = []
    for ident, page, cap in miss_f:
        if required is None:
            continues = True
        else:
            continues = ident.isdigit() and int(ident) in required
        if continues:
            hard_fail.append(ident)
    if args.strict:
        hard_fail += [i for i, _, _ in miss_t] + [i for i, _, _ in miss_e]

    chars = len(re.findall(r"[\u4e00-\u9fff]", draft))
    print(f"\nDraft length: {chars} Chinese characters.")

    # Unnumbered display equations cannot be checked mechanically. Report how many
    # the extractor found so the writer knows how much manual coverage remains.
    try:
        with open(args.inventory, encoding="utf-8") as fh:
            inv_text = fh.read()
        cand = len(re.findall(r"^- EQ~ \| p\d+ \|", inv_text, re.MULTILINE))
    except OSError:
        cand = 0
    if cand:
        print(f"Unnumbered display-equation candidates in the paper: {cand}.")
        print("  These are NOT machine-checked. Confirm manually that every real "
              "display equation is explained (see qa-checklist.md, section A).")

    if hard_fail:
        print(f"\nRESULT: FAIL — uncovered required items: {', '.join(map(str, hard_fail))}")
        print("Narrate them, or narrow the required set with --main-figures-only.")
        return 1

    print("\nRESULT: PASS — every required figure is referenced.")
    print("Note: being referenced is not the same as being explained. Re-read each "
          "covered figure's narration and confirm it says what the figure shows and "
          "how to read it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())