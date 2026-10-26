# Domain notes — robot learning, VLA, embodied AI

Use this when the paper is about robot learning, vision-language-action models,
manipulation, or embodied AI. It lists the facts such a script must always state,
the concepts that always need teaching, and the traps that are specific to this
literature.

## 1. Facts that must always be stated

A robotics listener cannot judge any result without these. If the paper states
them, include them. If it does not, say so rather than guessing.

| Fact | What to give |
|---|---|
| 动作空间 | dimensionality, what each component is (translation, rotation, gripper, base, terminate), and the coordinate frame |
| 观测定义 | camera count and mounting (wrist / shoulder / base / front / side), RGB vs depth, and whether proprioceptive state is an input |
| 控制频率 | Hz, and whether it is the policy rate or the execution rate |
| 机器人平台 | model, degrees of freedom, gripper type |
| 数据规模 | trajectories, hours, or time steps — say which unit the paper uses |
| 任务覆盖 | number of tasks, skills, scenes, object categories, robot platforms |
| 训练 / 推理硬件 | GPU type and count, cloud vs on-robot, latency |
| 成功判定 | the exact criterion and attempts allowed |
| 指标 | definition, range, and normalisation |
| 参数规模 | total parameters and how they split across modules |

## 2. Concepts that always need teaching

Each of these appears in VLA papers with the assumption that the reader knows it.
Teach it the first time it appears in the script, using the define → motivate →
mechanism → payoff ladder and one analogy.

**Core vocabulary**
- VLA 视觉语言动作模型 — decompose the acronym, as the reference scripts do.
- 自回归离散化 action tokenisation — why actions are cast as text tokens, what is
  lost (precision, frequency) and what is gained (reuse of a pretrained VLM).
- 动作分块 action chunking — predicting H future steps at once instead of one step;
  why it buys smoothness and frequency.
- 扩散 diffusion vs 流匹配 flow matching — both start from noise and iterate; the
  difference is stochastic denoising versus a learned deterministic vector field.
  Analogy: groping forward versus following a pre-laid track.
- 动作专家 action expert — a small separate module for action output; why sharing
  one weight set between image/text and continuous actions causes interference.
- 独立权重 + 共享注意力 — two weight sets interacting only through attention.
- 键值缓存 KV cache — compute the conditioning tokens once, reuse across denoising
  steps; the reason a 10-step sampler can still run at high frequency.
- 跨具身 cross-embodiment — one model across robot platforms; requires unifying
  action/state dimensions by padding and masking.
- 零样本 / 少样本 / 后训练 — zero-shot, few-shot, post-training; what each does and
  does not require.
- 联合微调 vs 微调 vs 从零训练 — co-fine-tuning keeps internet data in the mix to
  avoid catastrophic forgetting of semantics.

**Generalisation vocabulary**
- The five common axes: 新物体、新组合、新指令、新语义类别、新环境.
- 类内泛化 vs 类间泛化 — more instances per class versus more classes.
- 开环 vs 闭环抓取 — pre-planned versus feedback-corrected.
- 模仿学习 vs 强化学习 — imitating demonstrations versus trial-and-error.
- 域随机化 domain randomisation and sim-to-real — what transfers, what does not.
  Note that semantic knowledge and visual concepts transfer far more readily than
  motor skills; the reference corpus is explicit that no paper expects a robot to
  learn a new motor skill from internet knowledge alone.
- 涌现能力 emergent ability — capability that appeared from scale/pretraining
  rather than from robot data; distinguish 语义理解 transfer from 新运动技能.

**Grasping-specific**
- 6D 抓取位姿 — position plus orientation; the token count that follows from the
  representation (three positions plus a quaternion is seven numbers).
- 力闭合 force closure — a friction-based stability condition; note that it is
  formally a rigid-body criterion, which is why deformable objects are hard.
- 抓取合成与运动规划 — grasp synthesis then collision-free trajectory planning,
  then physics validation.

**Metrics**
- 成功率 — always state the criterion (lift height, attempt limit, scene reset).
- SPL 路径长度加权成功率 — succeeds *and* is efficient; explain the ratio and work
  a two-trial example.
- 规划得分 / normalised score — fractional credit per completed sub-step.

## 3. Domain traps

**Degrees of freedom is not action dimensionality.** A configuration space of 14
dimensions can pair with a 16- or 17-dimensional action space once a mobile base
contributes translation and rotation. State both.

**Count the action vector out loud.** For a fixed-base arm: 3 translation + 3
rotation + 1 gripper + 1 terminate = 8. For a grasp pose: 3 position + 4 quaternion
= 7. Discretisation (e.g. into 256 bins per continuous dimension) applies only to
the continuous components, never to the discrete terminate command.

**Time-step direction is per-paper.** See
[grounding-workflow.md](grounding-workflow.md#convention-traps). Two of the
reference papers use opposite conventions.

**Symbol reuse.** $a_t$, $q_t$, $o_t$, $s_t$, $\tau$/$t$ are reused across papers with
different meanings. Resolve each from the paper.

**Dataset umbrellas.** Name the actual slice used (OXE Magic Soup, ELVIS subset),
and give the paper's own counts for it, not the umbrella's marketing numbers.

**Frequency claims.** Distinguish the model's inference frequency from the
controller's execution frequency from the sensor rate. A 50 Hz control rate does
not mean the 3-billion-parameter network runs at 50 Hz — action chunking and KV
caching are what bridge the gap. This is a frequent and important clarification.

**Latency versus throughput.** A 200 ms inference latency is fine for static scenes
and insufficient for fast-moving objects. Say which regime a claim belongs to.

**Comparability.** Cross-paper numbers are rarely comparable: different hardware,
attempt limits, success thresholds, and task suites. When the script sets two
papers side by side, state the conditions.

## 4. Framing that works for this domain

The reference scripts converge on a small set of framings that land well:

- **大脑与身体** — perception/planning versus execution; use it to explain why
  modular systems lose the benefit of large-model knowledge.
- **课本知识 vs 手上的功夫** — semantics and visual concepts transfer; motor skills
  do not. Use it for knowledge-transfer limits.
- **上大学 vs 岗前培训** — pretraining versus post-training.
- **考生与对手** — framing evaluation as a comparison with named contestants and
  baselines, each introduced before the result.
- **摸索前行 vs 铺好的轨道** — diffusion versus flow matching.
- **弹簧** — compliant control.
- **翻译** — coordinate-frame transformations and the Jacobian.

## 5. What a learner in this field most often gets wrong

Address these explicitly if the paper touches them; they are the highest-value
clarifications a script can make:

1. Thinking "VLA" means the model outputs text about actions — it outputs action
   tokens that are de-tokenised into continuous values.
2. Confusing one action token (one time step) with a sequence of actions.
3. Believing internet-scale pretraining can teach new motor skills.
4. Treating a high control frequency as if the whole network runs that fast.
5. Assuming simulation results predict real performance at equal data scale; the
   gap narrows with more data but does not vanish, and simulation usually looks
   better.
6. Assuming a generalist model must lose to a specialist. It may win on instruction
   following and language-conditioned tasks while losing on raw grasp robustness —
   say which axis is being measured.
7. Reading a normalised score without asking what the maximum was.