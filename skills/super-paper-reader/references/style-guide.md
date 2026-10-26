# Style guide — the 讲解腔

The target voice is a good course lecturer talking to one learner: warm, patient,
concrete, and never showing off. It is spoken prose that happens to be written
down, not written prose that happens to be long.

## The 14 voice rules

**V1 — 讲解人称.** Use 我们 / 大家 / 你们 for the audience, and make the paper the
subject of report: 论文指出、论文提到、论文带我们回顾了、研究团队、团队、作者.
Avoid the impersonal academic passive.

**V2 — 自问自答 for every design decision.** Before explaining *why* something was
built a certain way, ask it out loud, then answer. This is the single most
characteristic move of the target voice.

> 那现在问题来了，我们如何让 VLM 能输出这些动作编码？
> 是不是就会产生相互干扰？那怎么办？

**V3 — 类比先行.** Every abstract mechanism gets one analogy *before* the formal
explanation, so the listener has somewhere to hang the detail. See
[Analogy engineering](#analogy-engineering).

**V4 — 术语三件套.** On first mention of any term: 中文译名, then the English
original in parentheses or inline, then a one-clause gloss. Thereafter use the
form that reads most naturally aloud — usually the Chinese one. Never leave a
bare acronym standing alone the first time.

**V5 — 数字具象化.** Any headline number gets converted into something a person
can picture. Verify the arithmetic yourself.

> 10 亿帧是个什么概念？以每秒 30 帧的速度播放，可以连续播放约 387 天。

**V6 — 出处定位.** Every figure, table, appendix, and section reference carries its
page: 「论文第 5 页的图三」「论文的附录 C 中还补充到」「论文第 10 页的图六 a」.
This is the script's credibility anchor and the listener's ability to go check.

**V7 — 承上启下.** End each section with a sentence that hands the listener over,
and open the next by accepting the handoff. Never let a section start cold after a
heading.

> 好，那了解完这些 VLA 的相关技术之后，我们开始进入论文的核心部分。

**V8 — 先判断，后展开.** Every paragraph opens with its conclusion, then earns it.
「RT-2 的第二个局限是计算成本的挑战。」then the explanation. Not the reverse.

**V9 — 附着式回扣.** Periodically remind the listener where a fact came from
earlier: 「这个问题我们在第四节提到过」「之前咱们说过，云服务推理的方案…」. Cheap,
and it makes a 15,000-character script feel like one argument.

**V10 — 具体到动作.** Never describe a mechanism only at the level of "the model
generates an action". Say what the robot does: 「先打开微波炉，然后把保鲜盒放进去，
最后再关上」. Concrete verbs, concrete objects, in order.

**V11 — 长句可以，但要能读.** Speech allows run-on sentences, but each sentence
should carry exactly one idea. Do not nest three clauses deep. Use 逗号 to chunk
rather than 顿号 lists of abstract nouns.

**V12 — 不做审稿人.** The script reports what the paper claims and what the
authors concede. Evaluation language is limited to 「研究团队也给出相应的解释」,
「论文坦言」, 「这也是性能与速度之间的经典权衡」. No 我认为论文的不足在于…, no
打分, no recommendations. Critique belongs to `paper-reading`.

**V13 — 补充背景要标好来源.** You will teach more than the paper does. Keep the
provenance legible: paper assertions use 论文指出/认为, and your own background
additions read as plain facts. Never attribute your supplement to the paper.

**V14 — 篇幅服从讲解，不服从简洁.** Do not compress for elegance. If a concept
needs 300 characters to land, write 300. The only reason to cut is duplication.

## Sentence bank

Functional templates. Vary them; do not use the same opener three paragraphs in a
row.

| Function | Patterns |
|---|---|
| 开篇定位 | 本期/这次我要详细讲解的是…；这篇论文是…；题目是… |
| 引入新内容 | 我们先来看…；我们再来看…；回到…；接着往下看…；然后我们再来了解… |
| 追问 | 那现在问题来了…；为什么…？；这又是为什么？；那怎么办？；是不是就会…？ |
| 澄清与简化 | 这里需要注意的是…；简单来说…；通俗理解就是…；这两个要区分开；换句话说… |
| 类比 | 就好比…；我们可以把它理解为…；它一个特别真实的虚拟世界；就有点像… |
| 强调 | 绝妙之处就在于…；关键就在…；我们也能发现…；我们可以看到… |
| 出处 | 论文第 X 页的图 Y…；论文附录 D 中提到…；论文的附录中还补充到… |
| 承上启下 | 好，那了解完这些…之后，我们开始进入论文的核心部分；了解了这些背景，我们再来看… |
| 回扣 | 这个问题我们在前面提到过；之前咱们说过…；我们刚才讲过… |
| takeaway | 这说明…；也就是说…；这足以说明…；这就证明了… |
| 收束 | 总的来说…；这篇论文告诉我们…；这篇论文可以说是为…提供了一个新的范式 |

## Analogy engineering

An analogy is not decoration. It is a temporary scaffold that lets the listener
run the mechanism in their head. Two rules govern its quality.

**Rule 1 — the analogy must preserve the mechanism's structure.** Map, explicitly
or implicitly: what goes in, what comes out, what the constraint is, what the cost
is. An analogy that only "feels similar" teaches a wrong intuition.

Good, from the reference corpus:
- 扩散模型 vs 流匹配 —「扩散模型像是在摸索中前行，每走一步都要停下来重新感知方向并随机
  调整，路径可能磕磕绊绊；流匹配则像是预先铺设了一条平滑轨迹。」Preserves: both
  iterate, one is stochastic, one learns a deterministic field.
- 动作专家 —「把 VLM 看作是大脑，动作专家就是小脑。」Preserves: division of labour,
  the perception module does not execute.
- 预训练 + 后训练 —「预训练就好比是让模型上大学学习通用知识，后训练就是岗前培训。」
  Preserves: sequence, generality → specificity.
- 消融实验 —「老中医写了一个补肾的药方，把茯苓这味药去掉，再看药效有没有下降。」
  Preserves: remove one component, measure the delta.
- 阻抗控制 —「给机械臂装上了弹簧，遇到碰撞不是硬碰硬，而是像弹簧一样柔顺地退让或贴合。」
  Preserves: force compliance.
- 雅可比矩阵 —「是笛卡尔空间指令和关节空间指令之间的翻译。」Preserves: the mapping
  between two coordinate descriptions of the same motion.
- 网格简化 —「3D 模型像马赛克拼图，面越多越精细但处理越慢，ACVD 把密集小面合并成
  更少的大面。」Preserves: fidelity/speed tradeoff.

**Rule 2 — source analogies from the listener's shared experience, in this order
of preference:**
1. 日常身体动作与生活经验 (夹菜, 弹簧, 游泳, 岗前培训);
2. 已在论文里讲过的技术 (compare a new mechanism to one already explained in
   this same script);
3. 组织与角色分工 (大脑/小脑, 规划器/控制器, 考生/对手);
4. 已有领域直觉 (图像生成的平均图像 vs 机器人动作的平均动作).

**Rule 3 — one analogy per mechanism.** Stacking two analogies confuses. Follow
the analogy immediately with the real term so the listener lands back on solid
ground.

**Rule 4 — never let the analogy introduce a false causal claim.** If flow matching
still iterates, say so inside the analogy. If the cerebellum metaphor would imply
the action expert cannot use language, correct it in the next sentence.

**Rule 5 — keep it to one or two sentences.** A long analogy becomes its own
lecture and the listener forgets what it was for.

**Rule 6 — negative analogies are valuable.** Contrasting the *wrong* approach
against the right one with a shared metaphor is often the clearest way to explain
a design choice.

**Recurring slots that need an analogy in almost every VLA/robotics paper:**
the action space and its discretisation; the noisy-action time step; why a
separate action module exists; why data mixing is weighted rather than proportional;
why a simulation does or does not transfer; open-loop versus closed-loop control;
the difference between success rate and path efficiency; what freezing parameters
buys you.

## Terminology hygiene

Speech-to-text transcripts of lectures in this field are full of mangled proper
nouns, and a written script has no excuse for repeating them. Build the canonical
list from the PDF text and copy spellings exactly.

- Extract every model, dataset, metric, tool, and benchmark name, and copy its
  exact rendering including case, hyphens, digits, and subscripts:
  `RT-2`, `RT-1`, `PaLI-X`, `PaLM-E`, `PaliGemma`, `OpenVLA`, `Octo`, `π0`, `π0.5`,
  `GraspVLA`, `DINOv2`, `SigLIP`, `InternLM2-1.8B`, `Gemma`, `LIBERO`, `AnyGrasp`,
  `Grounding DINO`, `MuJoCo`, `Isaac Sim`, `cuRobo`, `ACVD`, `TFDS`, `OXE`,
  `Magic Soup`, `Bridge V2`, `DROID`, `Ego4D`, `Language Table`, `SPL`.
- Do not "normalise" a name the paper deliberately spells unusually; do not
  translate a product or dataset name.
- For units and quantities, keep the paper's unit and add a parenthetical
  conversion only when it genuinely helps: 200 毫秒, 50 Hz, 40×50×20 厘米.
- Mathematical symbols: never just read the letter. Say what the quantity is —
  「套/τ 是流匹配的时间步」「N 是该组合的样本数量」.
- Where the paper's symbol is hard to say aloud, use the Chinese name
  (时间步, 向量场, 动作块) and mention the symbol once.

## Punctuation and rhythm for read-aloud text

- Use commas to chunk one idea per clause; a listener cannot re-read.
- Use 中文全角标点 throughout, including around embedded English terms.
- Avoid parentheses that nest; convert them to a following clause.
- When enumerating, prefer 「第一…第二…第三…」 sentences over Markdown bullets;
  bullets break the spoken flow. Reserve lists for genuinely tabular content
  (data-source tables, baseline inventories) and even then keep them short.
- Bold or italics are fine for a term on first mention, or for one sentence that a
  whole section hinges on. Do not bold whole paragraphs — nothing gets emphasis if
  everything does.

## Length discipline

The failure mode of this skill is not bloat, it is **thinning**: dropping the
equation walkthroughs, the baseline justifications, and the figure narration to
keep the script tidy. Keep those. Cut instead:
- repeated restatements of the same claim in two sections;
- inventory lists of every dataset the paper merely cites;
- re-explaining a term already explained (add a回扣 clause instead);
- hedged meta-commentary about the paper's importance.

## Self-check sentences

Before delivery, read the opening of each paragraph. If three consecutive
paragraphs begin with the same pattern (「此外，」 / 「论文还…」), rewrite two of them.
If any section has an opening sentence that does not tell the listener what the
paragraph is about, rewrite it (V8).