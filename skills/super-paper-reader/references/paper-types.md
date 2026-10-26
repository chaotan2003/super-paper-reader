# Adapting to the paper type

The skeleton in [structure-template.md](structure-template.md) is calibrated for a
**method/model paper**. Almost every paper is one of five shapes; pick the shape
first, then adjust the weight distribution. In all shapes, keep the paper's own
headings and order.

## Shape A — method / model paper (default)

Contribution is a new architecture, objective, or training recipe.
Examples in the reference corpus: RT-2, π0, GraspVLA.

Weight: Method + Data/training 45–55%, Experiments 25–32%.

Emphasis adjustments:
- The main framework figure is the spine — narrate it fully.
- Every numbered equation gets the five-step treatment (see Beat 5).
- Data and training recipe are part of the method, not an appendix to it: the
  listener cannot judge the claims without knowing what was trained on.
- Expect 2–4 named baselines, each with a reason for existing.

## Shape B — dataset / resource paper

Contribution is a dataset, benchmark, or simulator.

Weight: Data/resource section 35–45%, Experiments 25–30%, Method 10–15%.

Emphasis adjustments:
- The data section becomes the core. Narrate: what is in it, how it was
  collected or generated, annotation schema, statistics, licensing, filtering,
  quality control, and what was deliberately excluded and why.
- Give the generation or collection pipeline as an ordered process with the
  engineering decisions called out (caching, parallel writes, fault handling) —
  these usually live in appendices and are where the real craft is.
- Experiments become "what can be trained on this resource, and how does it
  compare to models trained on other resources". Say explicitly whether the
  comparison is apples-to-apples.
- Add a short honesty note if the paper reports missing/corrupt data rates or
  known biases.

## Shape C — system / engineering paper

Contribution is a working system: latency, throughput, cost, hardware.

Weight: Method 30–40%, Systems/implementation detail 20–30%, Experiments 20–25%.

Emphasis adjustments:
- The interesting content is trade-offs. For each design decision, state what was
  given up: 「这也是性能与速度之间的经典权衡问题」.
- Narrate the control/pipeline path end to end, in time order, with numbers
  (frequency, latency budget, memory).
- Include the failure handling and safety mechanisms; these are usually in
  appendices and are the most useful part for a practitioner.
- Experiments should be read as cost-versus-quality, not just accuracy.

## Shape D — theory / analysis paper

Contribution is a theorem, bound, or analysis.

Weight: Theory 40–50%, Experiments or validation 15–25%, Related Work 15–20%.

Emphasis adjustments:
- For each theorem or proposition give: 前提假设, 结论 (in plain language), 直觉
  (why it should be true), 证明思路 (the trick, not the algebra), 它有什么用.
- State the assumptions explicitly and say what breaks if they fail — that is the
  most common listener question.
- Experiments are validation, not demonstration; frame them as "do the predictions
  hold up".
- Analogies matter more here than anywhere else, because the formalism is the
  barrier.

## Shape E — benchmark / survey paper

Contribution is a taxonomy, evaluation protocol, or field map.

Weight: taxonomy/organising structure 40–50%, findings 25–30%, gaps 10–15%.

Emphasis adjustments:
- The taxonomy becomes the skeleton of the whole script: one 脉络 per branch, each
  explained with its representative works and its criterion for membership.
- Say what axis the taxonomy uses and why that axis is the useful one.
- Where the paper compares numbers across works, flag non-comparable settings
  rather than repeating the table.
- Close on the gaps the paper identifies, not on a leaderboard.

---

## Cross-cutting: what changes with paper maturity

| Situation | Adjustment |
|---|---|
| First-of-its-kind paper | Add frame-building to Introduction and Related Work; the listener has no vocabulary yet. Define the problem space before the solution. |
| Incremental improvement | Spend more words on *what was wrong* with the previous version, less on re-teaching the field. |
| Contested or heavily cited work | Report the authors' claims, note the field's reception only if the paper itself addresses it, and avoid adjudicating. |
| Very long paper with heavy appendix | Appendix content is often the most valuable for a learner (implementation detail, failure cases, extra ablations). Bring it into the main narration with explicit appendix locators. |
| Short paper (4–8 pages) | Scale the script to ~4,000–6,000 characters, but keep all sections and all figures. Do not compensate for the short paper with padding. |

## When the user's purpose is narrow

If the user asks to explain one specific part (「只讲方法」,「实验部分仔细讲」), produce
that section at full length and keep the others to a two-to-three-sentence bridge
so the script still stands alone. Do not silently drop the rest.