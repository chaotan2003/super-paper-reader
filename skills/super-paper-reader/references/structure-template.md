# Structure playbook

The script walks the paper's own sections in the paper's own order. Each beat
below gives: the job of the section, its internal paragraph sequence, its opening
move, and its closing move. The paragraph sequences are derived from how the
reference lecture scripts actually flow — follow them; they are what makes the
narration feel organised rather than rambling.

---

## Beat 0 — 篇首定位块

A three-line header before any narration.

```markdown
# 中文标题（English Original Title）

> 讲解稿 · 团队/机构 · 会议或时间 · 全文 N 页
> 一句话核心：<the contribution, one sentence, concrete>

## <the paper's first section heading, verbatim>
```

The one-line core must name the mechanism and the payoff, not the topic. Write
「用大规模合成动作数据替代昂贵真机数据训练抓取基础模型，首次在真机上实现零样本泛化抓取」,
not 「研究机器人抓取」.

---

## Beat 1 — Abstract / 开篇（150–400 字，1–3 段）

Job: in one breath, tell the listener what this paper is, who made it, why it
matters, and what it claims.

Paragraph sequence:
1. **定位句** — 讲解口吻开头, then the paper's identity: 团队, 时间/会议, 题目.
2. **地位句** — where it sits in the field. Use the paper's own framing plus the
   field's consensus, and only claim priority ("首个", "开山之作") as the authors'
   claim if the paper does not establish it: 「论文称这是首个…」.
3. **贡献句** — 提出了 <方法>，首次实现 <能力>，从而 <后果>.
4. *(optional)* **痛点预告** — 「然而通往这一目标的路上始终存在 N 个障碍」. Only if
   the paper's intro really is organised around enumerated obstacles.

Closing move: hand off to the introduction, e.g.「那这篇论文为什么要这么做？我们从引言说起。」

---

## Beat 2 — Introduction（700–1,900 字，4–10 段）

Job: make the listener *feel* the problem before showing the solution.

This section has the most stable internal logic of any section. Five moves:

1. **愿景 → 然而 → 根本矛盾.** First sentence states the field's dream. The very
   next clause turns: 「虽然很美好，却始终面临着…」. Then name the contradiction's
   source in one phrase — usually data (「源自数据层面的根本矛盾」).
2. **矛盾的展开.** Decompose into two or three layers. Typical for this field:
   - 数据层：the data that made LLMs/VLMs strong (internet-scale) does not exist
     for robots; robot data is expensive and cannot reach that scale.
   - 表征层：those models consume semantics and text prompts, robots need
     low-level actions in Cartesian space; 语义理解与物理控制之间的矛盾.
   - *(optional)* 规模层：the compute/parameter gap.
3. **旧方法为什么不行.** Name the actual prior approaches from the paper, and
   say why each fails. The reference scripts use a memorable framing here —
   「传统的方法是把大脑和身体分开了。大脑虽然聪明，但身体却学不到大脑的智慧」.
   Find the paper's version of that framing and keep it.
4. **本文的路子.** One sentence: 既简单又有效的解决方案. Then **decompose the name**
   of the new concept word by word — the reference scripts always do this:
   「vision 指的是图像，language 指的是语言指令，action 指的是机器人动作」. Then say
   what makes it elegant (「不需要从头设计新的模型框架，也不需要添加新的参数」).
5. **走一遍具体例子 + 预告.** Take one concrete example from the paper's Figure 1
   or 2 — robot scene, instruction, expected output — and narrate input → output.
   Then preview the rest of the script: 数据的两类来源, 训练策略, 后文安排.

Opening move: a vision sentence. The π0 script opens with a literary quote. That
is allowed **only** if you tie it explicitly to the paper's own argument in the
next sentence; do not decorate. A plainer and always-safe opening is:
「<领域>一直都有一个愿景：<愿景>。然而…」

Closing move: 「了解了这些，我们再来看论文的相关工作 / 核心方法。」

---

## Beat 3 — Related Work（1,400–1,800 字，6–10 段）

Job: **teach the background the listener needs**, not list citations. This is the
single biggest difference between a lecture script and a paper summary, and it is
where the reference scripts add the most value. They routinely explain CLIP, the
five axes of generalisation, ablations, SPL, MQA, pseudo-randomisation — content
that goes well beyond what the paper's own Related Work section contains.

Internal sequence, repeated for each 脉络 (2–4 of them):

1. **引子句** — 「在详细讲解 X 之前，我们先来回顾几个与 X 相关的技术。」
2. **脉络的定义与分叉** — e.g. 「论文将 VLM 分成了两类，一类是表征学习模型…另一类
   是生成式模型」. If the paper does not subdivide, subdivide it yourself along a
   meaningful axis and say so.
3. **代表工作怎么工作** — one or two named works, with the mechanism explained in
   the define→motivate→mechanism→payoff ladder. Include a concrete example
   (「一张猫片和『这是一只猫』的文本表征就非常近」).
4. **代表工作的局限** — always. 「但这类模型也有局限性，它主要是用于计算相似度匹配
   关系，但是不能直接生成输出。」
5. **本文站在哪里** — 「那 RT-2 选择的正是这类生成式的 VLM 模型，通过扩展这类模型的
   功能，让它来生成机器人动作。」

Then close the whole section with a收束句 that folds all 脉络 into the paper's
gap: 「好，那了解完这些之后，我们开始进入论文的核心部分。」

Governance: supplementary background is **encouraged**, but the provenance must
stay legible. Paper claims take 「论文指出 / 论文认为 / 论文提到」. Your own
background additions read as plain statements of fact. Never attribute your
addition to the paper.

---

## Beat 4 — Method 总览与逐图（约方法块的一半）

Job: let the listener build a mental picture of the whole system before any
detail. Always anchored to the paper's main framework figure.

Paragraph sequence:
1. **过渡句** — 「好，那了解完这些背景之后，我们开始进入论文的核心部分。」
2. **总览句** — 「论文第 X 节的 <节名> 主要围绕论文第 Y 页的图 Z 展开，是 <模型> 训练
   框架的总览。」
3. **读图** — walk the figure in a spatial order you state explicitly: 上半部分 /
   下半部分, or 左侧 / 中间 / 右侧, or 从输入到输出. For each region: what it is and
   what it does. The reference scripts narrate like this: 「这张图的左侧展示的是…中间
   部分展示的是…最后图片的右侧展示的是…」.
4. **宏观架构** — 由几大核心模块组成, each in one sentence: what it receives, what it
   produces, what it is responsible for. Use the brain/cerebellum framing when the
   paper has a perception module plus an action module: 「把 VLM 看作是大脑，动作专家
   就是小脑」.
5. **两大阶段** — if the paper has pretraining / post-training, say what each stage
   is for, using the listener's own experience: 「预训练就好比是让模型上大学学习通用
   知识，后训练就是岗前培训」.

Closing move: 「以上整个 X 的结构，现在来看它是如何被训练出来的。」

---

## Beat 5 — Method 细节与公式（约方法块的其余部分）

Job: for each load-bearing design decision, the listener must be able to say
*why* it exists. This beat is where the script earns its length.

For each mechanism, hit these in order:
1. **它要解决什么** — the problem this mechanism answers.
2. **自问自答** — pose the design question out loud. The reference scripts do this
   constantly: 「那现在问题来了，我们如何让 VLM 能输出这些动作编码？」「是不是就会
   产生相互干扰？」「为什么不能均匀分布？」
3. **类比** — one analogy, structured, short (see style guide).
4. **机制本体** — how it actually works, with the paper's own terminology.
5. **为什么不是别的做法** — the alternative that was rejected and why. This is the
   step that most distinguishes a lecture script from a summary.

For each numbered equation:
1. **一句话说它算什么** — 「这是一个…损失函数，用于训练模型统一学习…」.
2. **逐符号解释物理含义** — not names but meanings: 「其中 $N$ 是总的测试次数」,
   「$s_i$ 是一个标记，成功就记为一，失败就记为零」.
3. **代入具体数字算一遍** — mandatory. The reference scripts do this every time:
   「假设一个 2D 边框用四个数值 $x_1$ $y_1$ $x_2$ $y_2$ 来表示…那么 $N_{box}$ 就等于四」 /
   「假设测试了两次，第一次抓取成功了 $s_1=1$，最优路径 $l_1$ 是 10cm，实际路径 $p_1$ 是 12cm，
   本次的得分就是 1×10÷12」.
4. **训练时怎么用 / 推理时怎么用** — trace the equation into the pipeline.
5. **显式声明本篇约定** — whenever a symbol's direction or sign can be reversed by
   convention, state the paper's choice in words. See
   [grounding-workflow.md](grounding-workflow.md#convention-traps).

Also explain every basis concept the paper assumes but does not define — 六自由度,
力闭合, 雅可比矩阵, 键值缓存, 因果注意力掩码, 消融实验, 混合专家. These are where the
analogies live. Keep them to 2–4 sentences each so they do not swallow the section.

---

## Beat 6 — Data collection and training recipe（1,400–2,100 字）

Job: the listener should be able to state exactly what the model was trained on.
Skip or shrink only if the paper has no data contribution at all.

Paragraph sequence:
1. **为什么数据是核心** — 「想要训练出一个具有强大泛化能力的基础模型，其中一个关键在
   于数据集。数据集不仅规模要大，还要保证多样性。」
2. **数据来源逐个讲** — for each source: 名字 (canonical spelling), 规模, 覆盖
   (机器人平台/场景/任务/技能数), 采集方式, 为什么选它.
3. **规模具象化** — mandatory for at least one headline number. Turn the number
   into something a human can picture: 「10 亿帧是个什么概念？以每秒 30 帧的速度播放，
   可以连续播放约 387 天，足足有一年多」. Verify the arithmetic.
4. **配比与平衡策略** — what was mixed, at what ratio, and why. Include the failure
   mode the strategy prevents (「直接按照比例来训练，模型就会被数据量大的机器人所
   主导」).
5. **格式统一** — how heterogeneous data was made one shape: dimension padding,
   missing-modality handling, image duplication, unit normalisation.
6. **训练范式的两个阶段** — what each stage optimises, and what data each stage
   uses. 预训练追求通用性，后训练追求特定任务的流畅稳定.

---

## Beat 7 — Experiments（3,000–4,900 字）

Job: the listener must be able to judge the evidence. Never open with results.

Paragraph sequence:
1. **设计总览** — 「论文第 X 节…围绕 N 个核心问题展开，一是…二是…三是…四是…」.
   Enumerate the questions *before* any experiment.
2. **考生** — the model variants under test, with parameter counts and base models.
3. **对手 / 基线** — one sentence on each baseline: what it is, and why it was
   chosen. The reference scripts make the *reason* explicit: 「如果 RT-2 能超越它，
   就证明 VLM 预训练是有价值的」. Also state baseline fairness measures.
4. **指标** — define each metric and work a numeric example (§ Beat 5, step 3).
   State the success criterion exactly (「将指定物体抬高至少 15cm 才算」).
5. **逐个问题展开**, each with this fixed order:
   - 任务设置（what the robot must do, on which platform）
   - 条件与变化维度（lighting / background / distractors / height / unseen objects）
   - 结果图位置（论文第 X 页的图 Y）
   - 读数（who wins, by how much, with numbers）
   - 原因解释（the paper's explanation, plus your reading of the mechanism）
   - takeaway（一句话结论）
6. **消融 / 控制变量** — explain what an ablation is the first time it appears, then
   per variant: what was removed or changed, and what the score did.
7. **公平性与干扰因素** — report the paper's own caveats. If the paper says a
   comparison is confounded (e.g. model size bundled with pretraining), say so
   plainly and say why it cannot be untangled.

Closing move: fold the four questions back into the one thing they all test.

---

## Beat 8 — Limitations（600–1,700 字, or the paper's discussion section）

Job: the boundary, honestly, without becoming a review.

Paragraph sequence:
1. **承接句** —回扣 an earlier design choice, then pivot: 「尽管 RT-2 展现出了出色的
   泛化和涌现能力，但任何技术都有其局限性。」
2. **逐条局限** — 「第 N 个局限是…」. For each: what the limit is → a concrete
   failure example or analogy that makes it vivid → the authors' stated remedy.
   The reference scripts use this pattern well: 「一个人学习游泳，虽然通过看书已经掌握
   了四种泳姿的理论知识，但实际在水里他只练过蛙泳这一种…」
3. **失败案例分析** — if an appendix lists failure modes, narrate them with concrete
   scenes (「任务是让机器人把红色马克笔推到游戏手柄这里，结果机器人就推跑偏了」),
   then explain the underlying cause, then note whether it is specific to this paper
   or a field-wide open problem.
4. **区分作者承认的与未说的** — this section reports only what the authors state.
   Your own criticism does not belong in the script; if the user wants critique,
   that is `paper-reading`.

---

## Beat 9 — Conclusion（180–350 字，1–3 段）

Job: close the loop and lift.

Paragraph sequence:
1. **回到核心问题** — 「总的来说，这篇论文主要就是在探索一个核心问题：<问题>？答案是
   <肯定/否定>。」
2. **手段回顾** — 通过构建 <A> 和设计 <B>，让模型既能 <能力1>，又能 <能力2>。
3. **实验证据一句话** — 最终实验证明 <headline result>。
4. **升华** — 上升为范式或理念: 「这篇论文告诉我们，机器人也可以像大语言模型一样，
   先在海量的数据上学习通识，然后再用少量事例进修专业技能」/「它不仅是一个技术突破，
   更是一个理念范式」。
5. *(optional)* **一句边界** — 「但距离真正的广泛应用还任重而道远。」

---

## Multi-paper requests

Write one complete script per paper, each with its own header and its own section
tree. Do not interleave evidence. Only after both are complete, add a short
comparison section if the user asked for one — and when comparing, compare like
with like (same metric, same hardware, same task) and say when they are not
comparable.