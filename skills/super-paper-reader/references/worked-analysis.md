# Worked analysis of the reference corpus

This skill was derived from three lecture scripts supplied by the user
(RT-2, π0, GraspVLA), each paired with the paper it explains. This file records
what was measured, so the templates can be defended and revised rather than
guessed at. Do not copy passages from the reference scripts; use this as evidence
for *how* they are built.

## 1. Shape

All three scripts share the same architecture: they walk the paper's own sections
in the paper's own order, keeping the paper's headings verbatim, and they treat
"explain" as an obligation that scales with the page count rather than a budget to
be minimised.

| Property | RT-2 | π0 | GraspVLA |
|---|---|---|---|
| PDF pages | 26 | 17 | 26 |
| Chinese characters | 10,494 | 13,991 | 15,796 |
| Characters per PDF page | 404 | 823 | 607 |
| Section headers | verbatim from paper | verbatim | verbatim |
| Figures cited | 9 / 10 | 11 / 14 | 7 / 14 |
| Tables cited | 3 / 6 | 0 / 1 | 0 / 15 |

The 400–800 characters-per-page band and the "10,000–16,000 characters for a
15–25 page paper" rule in `SKILL.md` come from this table.

## 2. Section weight distribution

Measured Chinese-character counts per section:

| Section | RT-2 | π0 | GraspVLA | Share of total |
|---|---|---|---|---|
| Abstract / 开篇 | 182 | 351 | 122 | 1–3% |
| Introduction | 1,913 | 746 | 1,844 | 5–18% |
| Related Work | 1,766 | 1,455 | 1,584 | 10–17% |
| Method (+ data / training) | 1,998 | 7,281 | 7,132 | 19–52% |
| Experiments | 3,121 | 3,804 | 4,891 | 27–31% |
| Limitations | 1,338 | 354 | (inside §7) | 2–13% |
| Conclusion | 176 | — | 223 | 1–2% |

Two stable regularities:

1. **Experiments is always 27–31%.** Predictable and worth respecting.
2. **Method+data scales with how novel the method is.** GraspVLA and π0 spend
   ~45–52% there because the mechanism is the contribution. RT-2 spends 19%
   because the *idea* ("actions as text tokens") is simple and the paper's weight
   is in framing and evaluation.

RT-2's Introduction and Related Work together take 35% — a first-of-its-kind paper
must build the reader's frame before it can describe anything. Use this as the
signal for the "first-of-its-kind" adjustment in `paper-types.md`.

## 3. Recurring paragraph moves

Sampled from the opening clause of every paragraph in the three scripts. These
became the paragraph sequences in `structure-template.md`.

- **Introduction** is the most formulaic section: vision → 然而 → the contradiction
  and its source → why prior work fails → the proposed route → decompose the new
  concept's name → walk one concrete figure example → preview the rest.
- **Related Work is taught, not cited.** All three spend 1,400–1,800 characters on
  background that the paper's own Related Work section does not contain: what CLIP
  is, the five axes of generalisation, what an ablation is, what MQA is, the
  history of synthetic data, the three research directions in grasping. Each thread
  ends by placing the paper against that background.
- **Method narrated as a reading of the framework figure**, then each module as
  "one-sentence responsibility → components → each component". Design decisions
  are introduced by a self-asked question.
- **Experiments are framed as an examination.** "考生" (the model variants) and
  "对手" (the baselines) are introduced with reasons before any number appears.
  Metrics get a worked numeric example every time.
- **Limitations** are enumerated as "第 N 个局限是…" with a concrete failure image
  (a swimmer who only ever practised breaststroke; a red marker pushed off course)
  and then the authors' own remedy.
- **Conclusion** returns to the core question and answers it, then lifts to a
  paradigm claim.

## 4. Analogy inventory

The analogies are the load-bearing part of the teaching, and each one maps the
mechanism's structure rather than merely resembling it:

| Target | Analogy | Structure preserved |
|---|---|---|
| 消融实验 | 去掉补肾药方里的茯苓，看药效降不降 | remove one component, measure the delta |
| 知识迁移的限度 | 看书学了四种泳姿，水里只练过蛙泳 | theory does not confer motor skill |
| 模块化 vs 端到端 | 大脑聪明，身体学不到大脑的智慧 | planning and execution disconnected |
| 表征学习 vs 生成式 VLM | 猫片与"这是一只猫"距离近，与"狗在吃饭"距离远 | shared embedding space |
| 动作离散化 | 阿拉伯数字一 / one / 汉字一，代表同一个概念 | symbol substitution without meaning change |
| 扩散 vs 流匹配 | 摸索前行 vs 预先铺好的轨道 | both iterate; one stochastic, one deterministic |
| 动作专家 | 大脑与小脑 | division of labour |
| 预训练 + 后训练 | 上大学 + 岗前培训 | generality then specialisation |
| 阻抗控制 | 给机械臂装上弹簧 | force compliance |
| 雅可比矩阵 | 笛卡尔指令与关节指令之间的翻译 | coordinate mapping |
| 网格简化 (ACVD) | 马赛克拼图，小面合并成大面 | fidelity / speed tradeoff |
| 长训练任务 | 清理桌面要先分类垃圾与餐具 | semantic decision inside physical action |

Generate new ones per paper. Reusing "茯苓" or "游泳" for an unrelated mechanism
makes the script worse, not better, because the structure will not match.

## 5. What the reference scripts get wrong

This is the quality bar the skill must beat. Measured with
`scripts/check_coverage.py` against the same papers.

| Defect | Evidence |
|---|---|
| Tables almost never cited by number | π0 0/1, GraspVLA 0/15, RT-2 3/6 |
| Appendix figures dropped | π0 Figure 14 (timestep sampling) discussed in prose but never cited; RT-2 Figure 10 missing |
| Some main-text figures dropped | GraspVLA 7/14, π0 11/14 |
| Figure numbers corrupted by speech-to-text | 「图集」for 图七; 「图示。二」for 图十二 |
| Wrong count stated confidently | GraspVLA object instances given as 16,800; the paper says 10,680 |
| Mangled proper nouns | parli-x, pomme, 帕里扎马, 五洲口, 阿罗卡, 泰林 |
| Section boundary lost | GraspVLA script says "§6 is a conclusion… we'll look at §7, then come back to §6" |
| Run-on transcription artefacts | 「也」used for 「也就是」throughout; missing clause boundaries |

The skill's countermeasures: mandatory figure/table/equation coverage with a
mechanical audit, canonical proper nouns taken from the PDF, page anchors on every
citation, and the provenanced-background rule. The target is the reference scripts'
teaching quality with these defects removed.

## 6. What NOT to take from the reference scripts

- Their length is right; their **compactness of citation is not**. Cite figures and
  tables by number even when the surrounding prose already describes them.
- They sometimes narrate a figure they never identify, leaving the reader unable to
  find it. Always name and locate.
- They occasionally lapse into a summary register for a whole section (GraspVLA's
  Related Work briefly does). Keep the define→motivate→mechanism→payoff ladder.
- They are video narration, so they tolerate a looser sentence structure than a
  written script should. Keep the voice, tighten the syntax.
## 7. Measured standing (blind A/B on a held-out paper)

The skill was tested on a paper outside the reference corpus (OpenVLA, arXiv
2406.09246, 37 pages) against a deliberately fair baseline: the same model, the
same PDF, the same permission to run tools, given only the three reference
transcripts and told to produce the same kind of script. Two independent runs had
to be discarded first, because the agents found and loaded this skill on their own
from its description — evidence that the trigger is well-targeted.

| Measure | Reference transcripts | Skill output | Examples-only baseline |
|---|---|---|---|
| Figures cited | 27/38 (71%) | 11/11 (100%) | 11/11 (100%) |
| Tables cited | 3/22 (14%) | 12/12 (100%) | 12/12 (100%) |
| Mangled proper nouns | many (§5) | 0 | 0 |
| Wrong numbers | yes (§5) | 1 | 1 |
| Length per PDF page | 404 / 823 / 607 | 548 | 584 |

Blind rubric scoring (eight 0–5 dimensions, max 40, evaluator shown neither
provenance nor method): the skill script 38, the baseline 39 — inside noise. The
skill script was decisively better on the three things the rubric weights for
verifiability: reading the numbers printed *inside* figures (exact on every
checkable value), tracing the abstract's headline gain to the figure panel that
produces it, and supplying worked numeric examples for the discretisation and the
loss. The baseline was better on analogy breadth and on keeping process talk out of
the deliverable.

Three defects in the skill's own output, now fixed in the rules and in
`qa-checklist.md`:

1. Its header block narrated the *process* ("做了 300 到 900dpi 的 OCR 核对；本会话
   没有可用的图像识读模型") inside a document meant to be read aloud. The header is
   for the listener.
2. Three load-bearing mechanisms (the data-mixture weighting, the 27-epoch signal,
   the blocking-control experiment) got no analogy, because the rule said "one
   analogy per mechanism" without requiring a mechanism list first.
3. It cited a table by number and page but read no cell from it, and it wrote
   「第 11 节」 for what its own heading called section 6.

Both scripts failed to reconcile the abstract's other headline number (+16.5
points), which is the rollout-weighted average of the two benchmark gaps. That is
the remaining bar: a script should trace *every* abstract number, not just the one
that happens to decompose cleanly.

Lesson for future revisions: a strong model can infer most of an implicit standard
from good examples, so the skill's value is not raw quality on a good day. Its value
is that the standard holds when the model is weaker, the paper is harder, or the
operator does not know what to check — which is why the mechanical audit
(`check_coverage.py`) and the countable rules matter more than the prose guidance.
