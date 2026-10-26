# Evaluation rubric — 讲解稿 quality

Used to compare two candidate lecture scripts for the same paper. Score each
dimension independently for each script, then compare.

## Dimensions

### 1. Structure fidelity (0–5)
- 5: every top-level section of the paper has a heading, spelled as the paper
  spells it, in the paper's order; each section opens with an orientation sentence
  and closes with a handoff.
- 3: sections present but some renamed, reordered, or silently merged.
- 0–1: follows a generic template instead of the paper's structure.

### 2. Coverage (0–5) — count, do not impression
- Every main-text figure narrated (by number, with what it shows and how to read it).
- Every result-carrying table cited by number and page, headline cells read.
- Every displayed equation explained, with symbols and one numeric example.
- 5: all three at or near 100%. 3: figures covered, tables/equations partial.
  0–1: figures narrated without ever being identified.

### 3. Teaching ladder (0–5)
For each major mechanism, does the script supply: what it is → why it is needed →
how it works → why this design rather than an alternative → what it resolves?
- 5: all five rungs for every load-bearing mechanism, plus self-asked questions
  that make the listener predict the answer.
- 3: what/how present, why and alternatives thin.
- 0–1: describes components without motivation.

### 4. Analogies (0–5)
- 5: an analogy for every abstract mechanism; each preserves the mechanism's
  input/output/constraint/cost; generated for *this* paper.
- 3: a few good ones, several mechanisms left abstract.
- 0–1: none, or reused from another paper's mechanism where the structure differs.

### 5. Provenance anchors (0–5)
- 5: figures, tables, appendices, and sections cited with page numbers, and the
  page numbers are correct.
- 3: anchors present but vague or partly wrong.
- 0–1: no locators; the reader cannot check anything.

### 6. Terminology accuracy (count)
Count mangled proper nouns (a model/dataset/metric/tool name that differs from the
paper's spelling). Lower is better. Report both the count and the list.

### 7. Numeric accuracy (count)
Take a fixed list of facts from the paper and count how many the script gets right,
wrong, or omits. A wrong number is worse than an omission.

### 8. Length and pace (0–5)
- 5: Chinese character count within 400–800 per PDF page of the covered scope, and
  the method/experiment weight matches the paper's emphasis.
- 3: outside the band but internally consistent.
- 0–1: a summary rather than a lecture script (< 1,000 characters, or roughly
  one paragraph per section).

### 9. Read-aloud quality (0–5)
One idea per clause; no nested parenthesis mazes; 讲解人称 consistent; no
grader/reviewer register; no bullet dumps in the narration body.

### 10. Faithfulness of framing (0–5)
Paper claims attributed to the paper; added background not attributed to the paper;
no venue asserted unless the PDF states one; nothing fabricated.

## Aggregate

Sum the 0–5 dimensions (max 45) and report the two counts separately. Present the
result as a table with one row per dimension and one column per script, plus a short
paragraph naming the decisive differences.

## Rules for the evaluator

- Check claims against the paper's PDF, not against the other script.
- Do not reward length by itself; a longer script that omits tables and equations
  loses dimension 2.
- Do not reward confident-sounding prose. Wrong numbers and mangled names are
  defects, not style.
- Report the strongest concrete evidence for each score (a quote, a number, a
  missing item), not a general impression.