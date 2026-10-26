---
name: super-paper-reader
description: >-
  Super Paper Reader: turn one research paper into a long-form Chinese lecture
  script (论文讲解稿 / 讲稿), in the spoken teaching voice of a video course:
  section-faithful to the paper's own headings, every figure, table and equation
  explained, background taught instead of cited, one analogy per mechanism, and
  provenance anchors such as 「论文第X页的图Y」. Every formula is written inside
  `$…$` or `$$…$$`. Use when the user asks for 论文讲解稿、讲解文稿、逐节讲解、精讲、
  视频讲稿、把这篇论文讲一遍、帮我讲清楚这篇论文, or wants a paper turned into
  read-aloud narration for learning. Do not use for short reading notes
  (`paper-reading`), full-paper bilingual translation (`nature-reader`), the fixed
  Paper Card (`nature-paper-card`), referee reports (`nature-reviewer`), or slide
  decks.
---

# Super Paper Reader (论文讲解稿)

**Super Paper Reader** is the long spoken lecture script skill. One paper in, one
read-aloud 讲解稿 out, as Markdown. It installs into DeepSeek Harness only.

Turn one paper into a **spoken-word lecture script** that a listener can follow
without the PDF open. This is not a summary and not a review. It is the narration
track of a good course video: long, patient, section by section, explaining every
mechanism, every figure, every equation, and every experiment design decision.

**The deliverable is long.** A 15–25 page paper becomes **10,000–16,000 Chinese
characters**. If your draft is 3,000 characters, it is a summary — start over.

## Formula principle (公式硬性原则)

**Every formula lives inside math delimiters: `$…$` inline, and a `$$…$$` block on its
own lines for a display equation.** Nothing mathematical is left outside them. This is
the one rule checked character by character before delivery, because text outside the
delimiters reaches the listener verbatim — `a_{t:t+k}` survives exactly as typed, and
glyphs many fonts lack are shown as empty boxes. That is the 「公式乱码」 defect, and it
spoils a page that is otherwise good.

- **Banned outside `$…$` / `$$…$$`:** bare LaTeX script (`a_{t:t+k}`, `\sum`,
  `\pi_\theta`), Unicode super/subscripts (`Σᵢ`, `x²`, `a⁰`), Unicode math letters
  standing in for symbols (`π₀` as body text), and combining accents (`ℓ̂`, `q̇`).
- **The delimiters are the fix, not a font choice.** Write `$\pi_{0.5}$`, `$a_{t:t+H}$`,
  `$\sum_i w_i A_t[i]$`, `$\hat{\ell}$`, `$\lVert x \rVert^2$`.
- **A display equation gets its own lines.** Never run `$$…$$` into a paragraph, never
  leave one unclosed, and never use it for emphasis.
- **Symbol tables are Markdown tables, and every symbol in them is math.** The left
  column holds `$w_i$`, not `w_i`; a value column holds `$0.1$`, not `0.1`; a symbol
  mentioned in the table's prose column is `$…$` too. If a symbol needs a defining
  equation with conditions, that equation goes in its own `$$` block above or below the
  table, not inside the cell. 符号统一放在数学定界符里 — a table of bare `w_i` is the same
  defect as bare `w_i` in a sentence.
- **Rebuild each displaced equation from the rendered page**, not from the extracted
  text: `extract_paper.py` flattens two-dimensional math (a Σ has arrived as the letter
  `P`, KL bars as `k`, a two-line loss as token soup), so a term you added from memory is
  a fabricated symbol — rule 7 in formula form. See
  [references/narrating-visuals.md](references/narrating-visuals.md#equations) for the
  written form of an equation, a symbol table, and a worked substitution.

## What "good" means here

The reference scripts this skill is distilled from work because they answer a
fixed ladder of listener questions for *every* element of the paper, in order:

| # | Question | Failure if skipped |
|---|---|---|
| 1 | 这是什么？ | listener meets an unexplained term |
| 2 | 为什么需要它？ | listener cannot see the motivation |
| 3 | 它具体怎么工作？ | listener cannot re-derive it |
| 4 | 为什么这样设计，而不是别的做法？ | listener memorizes without understanding |
| 5 | 它解决了前面哪个问题？ | the argument chain breaks |
| 6 | 它在论文哪一页 / 哪张图 / 哪个附录？ | claims feel ungrounded |

At the paper level, the spine is always:

`领域愿景 → 然而根本矛盾 → 旧方法为什么不行 → 本文的路子 → 怎么做出来的 → 证据够不够 → 边界在哪 → 上升为什么`

The target is those scripts' teaching quality **with their defects removed**. They
routinely narrate a figure without ever naming it, skip tables entirely (measured:
0/1, 0/15, and 3/6 tables cited), state a wrong count confidently, and mangle the
proper nouns that speech-to-text could not hear. See
[references/worked-analysis.md](references/worked-analysis.md) for the measurements
and the full defect list — it is the reason several rules below are non-negotiable.

## Non-negotiable rules

1. **Keep the paper's own section headings, verbatim** (including original
   capitalisation): `INTRODUCTION`, `RELATED WORK`, `VISION-LANGUAGE-ACTION MODELS`,
   `THE π0 MODEL`, `SynGrasp-1B Dataset Generation`, `EXPERIMENTAL EVALUATION`.
   Do not rename them, do not reorder them, do not merge them. If the paper has no
   Limitations section, do not invent a heading — fold that content into the
   discussion/conclusion section the paper actually has.
2. **Speak, don't write.** Use 讲解腔: 我们 / 大家 / 你; the paper as the subject
   (「论文指出」「论文提到」「论文带我们回顾了」); transitions; self-asked questions.
   Never use 综上所述 / 本文认为 / 首先其次最后 as a default rhythm.
3. **Every figure in the paper gets explained** — at minimum the main framework
   figure plus every figure used as evidence, each with its number and page.
   Appendix figures are folded in whenever they carry the argument (failure cases,
   scaling curves, latency breakdowns), which is often.
4. **Every displayed equation gets explained**, whether the paper numbers it or
   not. Most ML papers print unnumbered display equations, so never treat "no
   equation numbers" as "no equations". Give what it computes, what each symbol
   physically means, and a concrete numeric example.
5. **Every experiment is introduced before its result**: what question, who is
   being tested, who the baselines are and why those baselines, what the metric
   means (with a worked numeric example), where the result figure is, then the
   reading of the result, then the reason.
6. **Every table that carries a result is cited by number and page, and its
   headline cells are read out.** Tables are the most commonly skipped element in
   lecture transcripts and the easiest place to lose a listener who wants numbers.
   *Naming a table is not covering it.* A sentence that says 「结果列在表七里」 without
   reading a cell from table 7 is a gap, not a citation. If a table is too large to
   read in full, read the row or column that carries the paper's claim and say which
   one you are reading.
7. **Never fabricate.** No number, page, figure number, baseline, dataset size, or
   parameter count that you did not read in the paper. If something is not
   stated, say it is not stated. Numbers you invent to illustrate an algorithm are
   allowed only if you label them as your own illustration at the moment you use
   them (「这几个数字是我为了演示算的例子，论文没有给出具体取值」).
8. **Trace every headline number to a cell.** For each number in the abstract that
   the script repeats as a result (a percentage-point gain, a success rate, a
   parameter count), show where it comes from — the figure panel or table row the
   listener can open. If the paper's own numbers disagree with each other (a figure
   panel averaging differently from the table beneath it), report both and say the
   conventions differ rather than picking one silently.
9. **Section ordinals must match the paper's numbering.** Citing a section by name
   and page is always safe; if you give an ordinal (「第 11 节」), verify it against
   the paper's own numbering — an ordinal that contradicts the heading three lines
   above it reads as carelessness.
10. **Do not assert a venue the paper does not state.** If the PDF is an arXiv
    preprint with no venue line, write `arXiv 预印本 <id>，<date>`. If the venue
    exists only in the PDF's metadata, you may mention that fact but must not
    present it as the paper's own claim. Attributing a paper to a conference you
    did not verify is a factual error.
11. **Analogies are mandatory, must preserve structure, and must cover the
    mechanisms.** One analogy per load-bearing mechanism, 1–2 sentences, then
    immediately return to the real term. Before drafting, list the mechanisms the
    paper turns on (the discretisation, the loss, the data weighting, the training
    schedule, the deployment trick, the ablation) and check that each has one; the
    failure mode is not a bad analogy but a mechanism that never got one. See
    [references/style-guide.md](references/style-guide.md#analogy-engineering).
12. **Follow the paper's own conventions, not the field's.** The same symbol can
    mean opposite things in two papers that cite each other. Never carry a
    convention across papers. See
    [references/grounding-workflow.md](references/grounding-workflow.md#convention-traps).

## Word budget

Calibrate against the PDF: **400–800 Chinese characters per PDF page**, about 600
on average. Distribute roughly as follows (percentages are of the whole script):

| Section | Share | Chinese chars |
|---|---|---|
| 开篇定位 / Abstract | 2–3% | 150–400 |
| Introduction | 5–18% | 700–1,900 |
| Related Work | 10–17% | 1,400–1,800 |
| Method + Data + Training recipe | 25–55% | 4,200–7,500 |
| Experiments | 25–32% | 3,000–4,900 |
| Limitations + Conclusion | 6–16% | 600–1,700 |

These are independent guidance bands, not a partition of 100%.

Two calibrations matter more than the individual numbers:

- **Experiment sections are stable at 27–31%** across every reference script. Treat
  that as a floor for a paper with real evaluation.
- **Method weight tracks how novel the method is.** A new architecture or training
  recipe takes 45–55% (π0, GraspVLA). A paper whose idea is simple but whose framing
  and evaluation are the contribution can go as low as ~20% (RT-2, where "actions as
  text tokens" takes a few pages and the rest of the paper is generalisation
  experiments). Do not pad a simple method to hit a target; spend those words on
  Introduction and Related Work instead, because the listener still needs the frame.

A paper that is *the first of its kind* shifts weight *into* Introduction and
Related Work. A paper whose contribution is a dataset shifts weight into the data
section.

Read [references/structure-template.md](references/structure-template.md) for the
section-by-section playbook before drafting, and copy
[assets/script-template.md](assets/script-template.md) as a starting scaffold if
you want the paragraph prompts in place.

## Workflow

### Phase 1 — Extract and map (never skip)
```bash
python3 scripts/extract_paper.py PAPER.pdf -o work/
```
This writes:
- `<slug>.paged.txt` — text in reconstructed reading order with `<!-- page N -->`
  markers. Read this one.
- `<slug>.layout.txt` — the `pdftotext -layout` rendering, for reading equations
  and tables where spatial layout matters more than reading order.
- `<slug>.structure.md` — first-pass inventory: section candidates (pattern matches
  plus font-size candidates), figure/table captions with pages, equation-bearing
  lines, and a proper-noun frequency table.

The inventory is a first pass, not ground truth. Two-column layouts, styled
headings, and broken font maps all degrade it; the script says so and reports what
it dropped. **Confirm the section list against the paper's printed headings by
reading the paged text.** For pages that extract as garbage, render and read them
as images.

Then build an **evidence inventory**:
- the section tree with start pages, headings verbatim;
- every Figure/Table/Equation with its page and one-line meaning;
- key quantities (data size, params, tasks, objects, hardware, metrics, headline
  results) each with a page;
- the paper's canonical spelling of every model, dataset, metric, and tool name;
- the paper's own symbol conventions;
- which appendix carries content you will use.

### Phase 2 — Get the figure structure
```bash
python3 scripts/render_pages.py PAPER.pdf 1 3 5 7 -o work/pages/ --dpi 150
python3 scripts/figure_map.py PAPER.pdf 1 3 5 7 -o work/figmaps/
```

**If your model accepts images**, open each rendered page with the image reader.
Descriptions like 「图的左侧是…中间是…右侧是…」「从上到下依次是」can only be written
by looking, and looking is always better.

**If your model cannot accept images** (check before promising anything), use
`figure_map.py`, which recovers structure from the PDF's own objects:
- image blocks merged into figure regions, with bounding boxes and a coarse
  left/centre/right and top/middle/bottom position;
- on-figure **vector text with coordinates** — for diagrams drawn as vectors this
  is the real label set, and for result plots it is often the printed values, so a
  bar chart's numbers and their left-to-right grouping *are* recoverable;
- the caption, and a per-region verdict on whether anything was recoverable.

Then respect the limit: if a region reports no recoverable labels, it is flat
raster, and its panel layout, colours, and axis ticks are not in the text. Narrate
it from the caption and the body prose, use the tick values only if they appear as
vector text, and do not assert internals you cannot verify. State no visual detail
you did not obtain either way.

Whichever path you took, read
[references/narrating-visuals.md](references/narrating-visuals.md) before writing
the figure, table, and equation passages — different visual types need different
narration.

### Phase 3 — Draft section by section
Write in the paper's order, at the paper's own headings, following
[references/structure-template.md](references/structure-template.md). Draft the
method and experiment sections first if the paper is method-heavy — they are the
bulk, and writing them first keeps the background sections calibrated to what the
listener actually needs.

### Phase 4 — Coverage and fidelity audit
```bash
python3 scripts/check_coverage.py work/<slug>.structure.md DRAFT.md
python3 scripts/check_coverage.py work/<slug>.structure.md DRAFT.md --main-figures-only 1-11
```
It reports the figures, tables, and equations the paper contains that the draft
never mentions. Use `--main-figures-only` with the main-text figure range when the
paper has many appendix figures, and `--strict` when you want tables and equations
to gate delivery too. Remember that being *referenced* is not the same as being
*explained* — re-read each covered figure's narration.

Then run every item in
[references/qa-checklist.md](references/qa-checklist.md). Fix gaps rather than
declaring them out of scope — an unnamed main figure and an uncited result table
are the two most common quality failures, and both are defects the reference
lecture scripts consistently exhibit.

### Phase 5 — Deliver
Write the script to a `.md` file in the directory the user asks for (default: a
`讲解稿/` or `outputs/` folder next to the paper), named
`<论文短名>_讲解稿.md`. Report the character count and the coverage summary
(figures covered / total, equations covered / total) in the reply.

## Format of the artifact

```markdown
# <中文标题>（<English original title>）

> 讲解稿 · <机构/团队> · <会议，或 arXiv 预印本 id + 日期> · 全文 <N> 页
> 一句话核心：<the paper's contribution in one sentence>

## Abstract
<narration>
```

The header block is for the **listener**, not for your process. It may say what
version of the paper this follows and, in learner terms, how complete the reading is
— for example `材料范围：正文与附录全文，图表读数已逐张核对`. It must not narrate your
tooling, your model's capabilities, or your own pipeline: sentences like
「本会话没有可用的图像识读模型」「我们做了 300 到 900dpi 的光学字符识别核对」
belong in your reply to the operator, not in the artifact. The listener wants to
know how far to trust the numbers, not how they were obtained.

Keep the header to at most three lines. Delete or rephrase anything that would read
as a grader's note inside a spoken lecture.

## Introduction
<narration>

## Related Work
<narration>

## <论文原始小节标题，逐字照抄>
...

## Experiments / EXPERIMENTAL EVALUATION
...

## Limitations
...

## Conclusion
...
```

No bullet-point dumps in the narration body: this is prose meant to be read
aloud. Short bullet or numbered lists are acceptable only where the paper itself
enumerates parallel items (five generalisation axes, three data sources, four
baselines) and even there, prefer numbered prose sentences
(「第一是…第二是…」) over markdown bullets.

### Math notation

| Write this | Not this |
|---|---|
| `$a_{t:t+H}$`, `$\sum_i w_i A_t[i]$`, `$\pi_\theta$` | `a_{t:t+H}`, `Σᵢ wi·At[i]` |
| `$\pi_{0.5}$`, `$\hat{\ell}$`, `$\lVert x \rVert^2$`, `$x^{2}$` | `π₀.₅`, `ℓ̂`, a combining accent, `x²` |
| a `$$` block on its own lines, for a display equation | a display equation run into the paragraph |
| a symbol table whose every symbol cell is math: `$w_i$`, `$p_\theta$`, `$0.1$` | a symbol table of bare `w_i`, `p_θ`, `0.1` |

Outside `$…$` a renderer prints `_{t:t+H}` verbatim, and characters many fonts lack
show as boxes; inside it the same characters typeset as real math. The HTML delivery
path (`paper-lecture-html`) uses the same delimiters, so the script stays portable
between `.md` and the page.

## Adapting to the paper

Read [references/paper-types.md](references/paper-types.md) when the paper is not
a standard method paper (dataset/resource, system, theory, benchmark/survey).
Read [references/domain-embodied-ai.md](references/domain-embodied-ai.md) when the
paper is about robot learning, VLA models, or embodied AI — it lists the facts
that such a script must always state (action space, control frequency, coordinate
frames, observation definition, success criterion) and the recurring concepts that
always need teaching.

## Handling imperfect inputs

- **PDF only**: normal case, run Phase 1–2.
- **PDF + an existing transcript or notes**: mine them for the author's chosen
  explanations, but re-verify every number and proper noun against the PDF — such
  transcripts are usually speech-to-text output and contain mangled terms.
- **Text only, no PDF**: state `材料范围：仅正文文本，未核对图表像素` in the
  header block, and do not narrate figure internals.
- **Partial (abstract only / excerpts)**: say so plainly; produce a short script
  and mark what cannot be determined as `论文未提供`.
- **Multiple papers**: write one full script per paper. Do not merge their
  evidence into a single narrative. Add a short cross-paper section only if asked.

## Language

Default to Chinese, matching the reference corpus. Keep canonical English terms on
first mention (`流匹配 flow matching`, `动作分块 action chunking`) and thereafter
use whichever reads more naturally aloud — usually the Chinese term. For an
English request, keep the same structure and voice, and write in English.

## Skill map

| File | Read it when |
|---|---|
| [references/structure-template.md](references/structure-template.md) | before drafting — the section-by-section paragraph playbook |
| [references/style-guide.md](references/style-guide.md) | before drafting — voice rules, sentence bank, analogy engineering |
| [references/narrating-visuals.md](references/narrating-visuals.md) | before writing figure / table / equation passages |
| [references/grounding-workflow.md](references/grounding-workflow.md) | during extraction — evidence inventory and convention traps |
| [references/asr-error-atlas.md](references/asr-error-atlas.md) | when the input includes a transcript or notes |
| [references/paper-types.md](references/paper-types.md) | when the paper is not a standard method paper |
| [references/domain-embodied-ai.md](references/domain-embodied-ai.md) | when the paper is robot learning / VLA / embodied AI |
| [references/qa-checklist.md](references/qa-checklist.md) | before delivery |
| [references/worked-analysis.md](references/worked-analysis.md) | when judging or revising this skill |
| [references/evaluation-rubric.md](references/evaluation-rubric.md) | when comparing two candidate scripts |
| [assets/script-template.md](assets/script-template.md) | as a fill-in scaffold |
| `scripts/extract_paper.py` | Phase 1 |
| `scripts/render_pages.py` | Phase 2 (with vision) |
| `scripts/figure_map.py` | Phase 2 (without vision) |
| `scripts/check_coverage.py` | Phase 4 |

## Relationship to adjacent skills

- `paper-reading` owns short 通俗精读笔记 and critical deep reviews.
- `nature-reader` owns full-text bilingual translation and source maps.
- `nature-paper-card` owns the fixed 16-section Paper Card.
- `nature-reviewer` owns formal referee reports.
- `paper-lecture-html` owns the **HTML delivery** of this same script: keep the
  content rules here, hand the draft to that skill when the user wants a page.
- This skill owns the **long spoken lecture script**. If the user asks for
  something short, they want `paper-reading`, not a truncated version of this.