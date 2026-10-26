# Grounding workflow

A lecture script that gets a number, a name, or a symbol convention wrong is worse
than no script, because the listener learns the error confidently. This reference
covers how to build the evidence base and the traps to watch for.

## 1. Extract with page markers

```bash
python3 scripts/extract_paper.py PAPER.pdf -o work/
```

Outputs:
- `work/<slug>.paged.txt` — full text with `<!-- page N -->` markers, so every
  claim can be traced to a page.
- `work/<slug>.structure.md` — a first-pass inventory: detected section headings,
  figure and table captions, lines containing numbered equations, and a
  proper-noun frequency table.

The preprint/extracted text is a starting point, not the truth. Captions are often
split across lines, headings are sometimes styled as graphics, and two-column
layouts can interleave. Confirm anything load-bearing by reading the paged text
around it, and by looking at the rendered page.

## 2. Get at the pages you will narrate

```bash
python3 scripts/render_pages.py PAPER.pdf 1 3 5 7 -o work/pages/ --dpi 150
python3 scripts/figure_map.py PAPER.pdf 1 3 5 7 -o work/figmaps/
```

**With vision**: open the PNGs with the image reader. Narrate a figure only after
seeing it. The claims that require eyes:
- which panel is left / middle / right, top / bottom;
- arrows and their direction (data flow vs supervision vs gradient);
- what is a box, what is a stack, what is a colour-coded group;
- axis labels, units, and axis ranges on result plots;
- which curve is which, and whether the gap is large or marginal;
- table cells, including footnotes and bolded winners.

At minimum, view: every framework/overview figure, every result figure you cite,
and any figure whose caption is unclear.

**Without vision**: `figure_map.py` merges image blocks into figure regions and
recovers on-figure **vector text with coordinates**. For vector-drawn diagrams that
is the real label set; for result plots it is frequently the printed values, so a
bar chart's numbers and their left-to-right grouping can be read exactly. Where a
region reports no recoverable labels, it is flat raster — narrate from the caption
and the body prose only, and do not assert layout, colours, or tick values. Record
which figure facts were recovered and which were not, so the script never claims
more than the PDF supports.

## 3. Build the evidence inventory

Before drafting, write out (as scratch notes, not necessarily in the deliverable):

- **Section tree**: heading verbatim → start page.
- **Figure/Table/Equation table**: number → page → one-line meaning → will you
  narrate it? (Default: yes for every figure and equation.)
- **Quantity sheet**: every number you intend to state → value → page → unit.
- **Term sheet**: canonical spelling → what it is → first mention gloss.
- **Convention sheet**: see below.
- **Argument sheet**: the paper's core question, its answer, and the three or four
  pieces of evidence that carry it.

## 4. Convention traps

These are the errors that survive a careless reading because they look right.

### Time-step direction flips between papers
Diffusion and flow-matching papers disagree about which end is noise. In the
reference corpus:
- **π0**: τ = 0 is pure noise, τ = 1 is the clean action.
- **GraspVLA**: t = 0 is the clean, noise-free action; t = 1 is fully noised.

Both are internally consistent and both are correct *for their own paper*. State
the paper's choice explicitly in words the moment you introduce the symbol, and
never carry a convention over from a related paper you explained earlier.

### Noisy versus clean symbols
Papers often use the same base letter with a superscript for the noised version
($a_t$ clean versus $a_t^{\tau}$ noised). Say which is which when first used, and
repeat the distinction at least once later — this is exactly the kind of detail a
listener loses.

### Abbreviations that collide
$N$ may be sample count, token sequence length, or camera count depending on the
equation. $L$ may be a loss or a length. $s_i$ may be a success flag. Always
resolve the symbol from the surrounding text; never assume from the field's habit.

### Version and scale suffixes
`5B` / `55B` / `1B` / `1.8B` are parameter counts, but model *names* also contain
digits (`RT-2`, `π0.5`, `InternLM2-1.8B`, `Bridge V2`, `VC-1`). Keep the two apart,
and check whether `b` means billion or a version letter.

### Dataset slices
A paper may use a subset of a public dataset. Write the subset name, not the
umbrella name: `OXE` vs `OXE Magic Soup`; `ObjectVerse` vs its `ELVIS` subset.

### Metric definitions
Success rate depends on the paper's own criterion (lift height, attempts allowed,
whether the scene resets). SPL has a specific formula involving a shortest-path
reference. Read the definition, quote the criterion, and work an example. Never
assume a metric means what it meant in another paper.

### Units and normalisation
Scores are often normalised to 0–1 with a task-specific maximum. Say what the
maximum was, otherwise the numbers are uninterpretable.

## 5. Coverage discipline

The script must mention every one of:
- each top-level section of the paper;
- each numbered figure;
- each numbered table;
- each numbered equation;
- each named baseline;
- each metric;
- each appendix that carries content used in the main text.

Run `scripts/check_coverage.py` for the mechanical part (figures, tables,
equations). The rest is manual. When something is genuinely not worth narrating,
say so in one clause rather than silently dropping it — but reserve that for
genuinely peripheral items, not for the main framework figure.

## 6. When the source is not a clean PDF

- **Speech-to-text transcript supplied alongside the PDF**: useful for the
  author's chosen explanations and analogies; treat every proper noun, number, and
  page anchor as suspect and re-derive it from the PDF. The full catalog of what
  actually goes wrong — eight risk categories, a correction table, and a
  do-not-"fix"-these list — is in
  [asr-error-atlas.md](asr-error-atlas.md). Read it before mining a transcript.
  Highlights: backbone family names get swapped for the wrong family entirely
  (PaliGemma described as Llama-based when it is Gemma-based); model names are
  rendered phonetically (π0 → 泰林 / 看领); homophones change technical meaning
  (流匹配 → 流体力学, 向量场 → 测量场, 域随机化 → 预随机化); counts shift
  (10,680 → "16800"); and page anchors drift by a page or two.
- **Scanned PDF**: `pdftotext` will return little; render pages and read them as
  images. State the reduced evidence scope in the header block.
- **Broken font mapping**: some PDFs embed Type3/CID fonts whose ToUnicode map is
  wrong, so a page extracts as garbage (`°2G)©¯SO/,SG )¡G`) even though it renders
  fine. `extract_paper.py` drops the worst lines and reports how many; for those
  pages, render and read the image instead.
- **Two-column layouts**: prose, headings, and captions can interleave under
  `pdftotext -layout`. `extract_paper.py` reconstructs column reading order with
  PyMuPDF and writes a separate `.layout.txt` for equations and tables, where
  spatial fidelity matters more than reading order.
- **arXiv HTML or publisher page only**: fetch it, but verify figure numbering
  against the PDF version if one exists — HTML renderings renumber.
- **No figures available**: narrate the text and say `该图未获得，仅依据正文描述`
  rather than imagining the layout.

## 7. Provenance marking in the deliverable

Keep two tiers visibly separate in your own drafting, even if the prose reads
smoothly:
- **论文主张** — always introduced with 论文指出/认为/提到/坦言 or 研究团队.
- **讲解补充** — background you add (what CLIP is, what an ablation is, how MQA
  works). Plain declarative sentences, never attributed to the paper.

If you are unsure whether something is in the paper, search the paged text for it.
If it is not there and you still want to teach it, teach it as background and do
not cite a page.