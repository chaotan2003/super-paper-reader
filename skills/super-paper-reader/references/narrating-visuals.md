# Narrating visuals and equations

A lecture script lives or dies on whether the listener can *see* the figure through
your words. Different visual types need different narration; using one pattern for
all of them is the most common weakness in machine-generated scripts.

Rule zero: **get the structure before you narrate it.** Panel order, arrow
direction, which curve is on top, and what a table's bold cells are must come from
the page, never from imagination.

Two ways to get it:

1. **Look at the rendered page** (`render_pages.py` then your image reader). This is
   always the better option when your model accepts images.
2. **If your model cannot accept images**, run `figure_map.py` and work from what it
   recovers: figure regions with bounding boxes and coarse positions, on-figure
   vector text with coordinates (which for a result plot is often the printed
   values themselves), and the caption. Where it reports no recoverable labels, the
   region is flat raster.

Be explicit with yourself about which facts you obtained and which you are
inferring. A script that says 「这张图的左侧是 DinoV2 和 SigLIP 两个编码器」 when the
labels were recovered as vector text is grounded. A script that says 「柱子从左到右
依次变高」 when nothing was recoverable is fabrication, even if it is probably true.

See also [grounding-workflow.md](grounding-workflow.md#2-look-at-the-pages-you-will-narrate).

---

## Framework / architecture diagrams

These carry the paper's main claim, so they get the longest treatment.

Narration order:
1. **Purpose** — what the diagram is a picture of, in one sentence.
2. **Starting point** — where the flow begins (usually an input at the left or top).
3. **Explicit reading order** — say it out loud, then follow it:
   「这张图的左侧展示的是…中间部分展示的是…最后图片的右侧展示的是…」
   or 「我们先来看上半部分…然后我们再来看看这张图的下半部分」.
4. **Each block** — one sentence each: what it receives, what it produces, what it
   is responsible for. Do not skip the boring blocks; the listener cannot infer them.
5. **The arrows** — say what each arrow carries: data, a supervision signal, a
   gradient, or a cached quantity. Never describe an arrow as "flows into".
6. **Colour/shape coding** — if the figure distinguishes trainable from frozen,
   real from synthetic, or one dataset from another, state the code once and use it.
7. **Payoff** — the sentence the figure exists to support.

Keep the narration shorter than the paper's own figure caption would be if expanded
into prose. The listener needs the structure, not a label-by-label translation.

## Result plots (bar / line / scatter)

1. **Axes first** — what is on x, what is on y, what the unit is, and what the range
   is. A normalised score means nothing until the maximum is stated.
2. **What is being compared** — which methods, which conditions, how many trials.
3. **Read the winner and the gap** — give the numbers, not "performs better". Note
   whether the gap is large or within error bars.
4. **Read the pattern, not just the endpoint** — if one curve rises steeply and
   another slowly, that shape *is* the finding (for example, a model needs much more
   data to reach parity on unseen objects than on seen ones).
5. **State what the plot does NOT support** — a two-method comparison says nothing
   about a third method; a simulation curve says nothing directly about real
   hardware. This is the step that prevents the listener from over-generalising.
6. **Error bars and caveats** — if error bars overlap, say so, even when the authors
   emphasise the mean.

## Tables

Tables are the most-skipped element in lecture narration, and the easiest place for
a listener who wants numbers to give up.

1. **Cite it** — 「论文第 6 页的表一」. Always number and locate.
2. **Say what the rows and columns are** before any cell.
3. **Read the headline cells aloud**, with the metric attached:
   「GraspVLA 在基础场景的成功率是 93.3%，SPL 是 87.2%」.
4. **Highlight the comparison the paper wants you to notice**, and note when a
   baseline wins on one axis while losing on another.
5. **Note the footnote conditions** — attempt limits, whether the scene resets,
   which subset was used. These change what the number means.

## Equations

Every displayed equation gets five steps, and the third is the one that is usually
skipped:

1. **What it computes**, in one sentence, in plain language.
2. **Each symbol's physical meaning** — not its name, its meaning. 「$N$ 是总的测试
   次数」「$s_i$ 是一个标记，成功就记为一，失败就记为零」.
3. **A concrete numeric example** — substitute real values and walk one evaluation.
   This is the step that converts an equation into understanding.
4. **Where it is used** — training objective, inference step, evaluation metric.
5. **The paper's convention**, stated in words, whenever direction or sign could be
   reversed: 「本篇论文里 $\tau$ 等于零是纯噪声，$\tau$ 等于一是干净的动作」.

If the paper has no numbered equations, it still has display equations. Never treat
"no equation numbers" as "no equations".

### Written form

Every formula in the script — inline or display — is written inside math delimiters:
`$…$` inline, `$$…$$` on its own lines for a display equation. Nothing mathematical is
left outside them: no bare `_{` / `^{`, no Unicode super/subscript (`Σᵢ`, `x²`), no
combining accent (`ℓ̂`). When the symbols are introduced, put them in a Markdown table
whose every symbol cell is math — `$w_i$` and `$0.1$`, never bare `w_i`. That is the
delivery form of the formula principle in `SKILL.md`; the Markdown script and any page
built from it read the same delimiters.

## Failure cases / qualitative galleries

Papers often show grids of rollouts, including failures. Narrate them as scenes:
what the robot was asked to do, what it did, what went wrong. Then give the cause,
then say whether the cause is specific to this paper or a field-wide open problem.
A concrete failure scene is worth more to a learner than any number of success
rates, because it teaches the boundary.

## When a visual is missing or illegible

Say so once and move on: 「该图在提取版本中无法辨认，这里仅依据正文描述」. Do not
invent panel structure, and do not silently omit a main figure — omission and
fabrication are both failures; a labelled gap is not.

## What to avoid

- Narrating a figure without ever naming its number.
- Labelling panels ("左图是数据集") without saying what to conclude from them.
- Reading every number in a table. Read the headline cells and the comparison that
  matters.
- Repeating the caption. The caption describes; the narration explains.
- Using "如图" as a substitute for explaining what the figure shows.