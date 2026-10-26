# Pre-delivery QA checklist

Run all of it. Fix, then re-run the mechanical parts. Report the character count
and the coverage summary in the reply to the user.

## A. Mechanical coverage
- [ ] `python3 scripts/check_coverage.py work/<slug>.structure.md DRAFT.md` reports
      no uncovered **main-text** figures.
- [ ] Every covered figure is narrated, not merely name-dropped: the draft says
      what it shows and how to read it.
- [ ] Every displayed equation in the paper (numbered or not) is explained.
- [ ] **Every formula in the draft sits inside `$…$` or a `$$…$$` block.** No bare
      `_{` / `^{`, no LaTeX command loose in the prose, no Unicode super/subscript
      (`Σᵢ`, `x²`), no combining accent (`ℓ̂`). Wrap each offender; a renderer prints
      whatever is outside the delimiters verbatim, and missing glyphs show as boxes.
- [ ] **Every symbol table is a Markdown table whose every symbol cell is math.** The
      left column reads `$w_i$`, not `w_i`; a value column reads `$0.1$`, not `0.1`. A
      bare symbol inside a table is the same defect as a bare symbol in a sentence. A
      symbol defined by an equation with conditions needs that `$$` block above or below
      the table rather than inside a cell.
- [ ] **Each displaced equation was rebuilt from the rendered page**, not from the
      extracted text: `extract_paper.py` flattens two-dimensional math (a Σ has
      arrived as `P`, KL bars as `k`). A term you did not look at is an invented
      symbol, which is the rule-7 defect in formula form.
- [ ] Each numbered table that carries a result is referenced with its number and
      page, and its headline cells are read out.
- [ ] Every top-level section of the paper has a corresponding heading in the draft,
      spelled exactly as the paper spells it.
- [ ] Every named baseline appears, each with a one-sentence identification and a
      reason it was chosen.
- [ ] Every metric is defined, with a worked numeric example.
- [ ] Appendix content used in the narration carries an explicit appendix locator
      (附录 A / 附录 L).

## B. Structure and length
- [ ] Chinese character count is within 400–800 per PDF page of the paper.
- [ ] The method+data block is the largest block; experiments second; background
      third. (Compare against the table in `SKILL.md`.)
- [ ] Each section opens with an orientation sentence and closes with a handoff.
- [ ] No section starts cold immediately after its heading.
- [ ] The Experiments section enumerates its questions *before* presenting any
      result.
- [ ] The Conclusion returns to the paper's core question and states the answer.
- [ ] **Every section ordinal matches the paper's own numbering.** If the draft says
      「第 11 节」, check the paper's heading list that says 6. Name-plus-page is
      always safe; an ordinal that contradicts your own heading is a visible slip.
- [ ] **The header block contains no process narration.** If it mentions your
      tooling, your model, OCR, dpi, or your pipeline, delete that sentence: the
      listener needs to know how far to trust the numbers, not how they were
      obtained.

## C. Voice
- [ ] The whole draft reads aloud naturally: one idea per clause, no nested
      parenthesis mazes.
- [ ] 讲解人称 is consistent (我们 / 大家 / the paper as subject).
- [ ] At least one self-asked question appears in each of the method, data, and
      experiment sections.
- [ ] Every configurational decision that the paper explains is accompanied by the
      rejected alternative ("为什么不是别的做法").
- [ ] No grader/reviewer language: no 我认为该方法的不足在于, no scores, no
      recommendations. Only 论文指出/认为/坦言 and neutral mechanism talk.
- [ ] No three consecutive paragraphs start with the same connective.
- [ ] No paragraph opens with a sentence that fails to announce what it is about.

## D. Analogies
- [ ] **You wrote down the list of load-bearing mechanisms before drafting, and
      each one has an analogy.** This is the failure mode that actually happens: not
      a bad analogy, but a mechanism — the data-mixture weighting, the training
      schedule, the blocking-control experiment — that never got one.
- [ ] Every abstract mechanism the listener is expected to internalise has an
      analogy.
- [ ] Each analogy preserves the mechanism's structure (input / output /
      constraint / cost) — not merely a surface resemblance.
- [ ] No analogy silently asserts a false property that the following sentence has
      to undo.
- [ ] Each analogy is 1–2 sentences and is followed by the real term.
- [ ] Analogies were generated for *this* paper. Do not reuse the reference
      corpus's analogies (茯苓 / 游泳 / 大学与岗前培训) unless the mechanism genuinely
      matches; at most adapt one.

## E. Fidelity
- [ ] Every number in the draft was read in the paper. Spot-check each against the
      paged text.
- [ ] Units and magnitudes are right (billion vs million; steps vs frames vs hours;
      Hz vs ms).
- [ ] Parameter counts are attributed to the correct model variant —
      name the variant in the same sentence as the number.
- [ ] Symbol conventions are stated explicitly and match this paper (especially
      time-step direction; see `grounding-workflow.md`).
- [ ] Every proper noun uses the paper's exact spelling, including case, hyphens,
      and digits.
- [ ] Venue claims are sourced. If the PDF does not state a venue, write
      `arXiv 预印本 <id>，<date>` and do not assert a conference.
- [ ] Invented arithmetic (e.g. "10 亿帧相当于播放 387 天") has been recomputed and
      is correct.
- [ ] Anything not stated in the paper is marked `论文未提供` or omitted, not
      guessed.
- [ ] **Every table you cite has had a cell read aloud from it.** Search the draft
      for 表 followed by each number, and confirm the surrounding sentences contain
      actual values from that table — not just its location.
- [ ] **Every headline number in the abstract is traced to a cell.** For each
      percentage-point gain or success rate the draft repeats, the listener is told
      which figure panel or table row it comes from.
- [ ] Where the paper's own numbers disagree (a figure panel averaging differently
      from the table beneath it), both are reported and the convention difference is
      named — not silently reconciled by picking one.

## F. Provenance legibility
- [ ] Paper claims are all introduced with 论文指出 / 论文认为 / 论文提到 / 研究团队 /
      论文坦言.
- [ ] Background you added (CLIP, ablations, MQA, force closure, SPL) reads as plain
      fact and is never attributed to the paper.
- [ ] Page, figure, and table references are exact and were verified against the
      PDF, not against the reference corpus. (Reference transcripts and any
      supplied speech-to-text notes contain wrong numbers and mangled names.)

## G. Deliverable
- [ ] File written to the requested location with the agreed name.
- [ ] Header block complete: 中文标题, 英文原题, 团队, 会议或预印本, 页数, 一句话核心.
- [ ] No leftover scratch notes, TODO markers, or placeholder text.
- [ ] The reply states the character count and coverage summary.