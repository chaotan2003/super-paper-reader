# ASR error atlas

A speech-to-text lecture transcript is a *source of explanations*, not a source of
facts. This file catalogs what actually goes wrong, verified against the papers, so
a written script can avoid it. Do not copy a transcript's spellings or numbers;
re-derive both from the PDF.

## The eight highest-risk categories

Ordered by how often they bite.

1. **VLM backbone family names.** The worst category by far. PaLI-X, PaLM-E,
   PaliGemma, and Gemma get substituted for each other, and sometimes for the wrong
   family entirely. Verified examples: `pomme X` / `parli-x` → PaLI-X;
   `pomme` / `pomi` / `prompt` → PaLM-E; `帕里扎马` / `帕里沙瓦` / `哈利 java` →
   PaliGemma; `mamba` / `charge jamma` → Gemma. One transcript states PaliGemma is
   built on a **Llama** language model — the paper says **Gemma 2B**. A wrong
   backbone family is a factual error, not a typo. Check every backbone name
   letter by letter against the PDF.
2. **Model names rendered phonetically.** π0 becomes 排云 / 泰林 / 蔡明 / 帕林 /
   看领 / 42版 / 莫干山板; GraspVLA becomes grouse vla / grok vlm / cross vla;
   AnyGrasp becomes anygrounds / anygrowth; Octo becomes opto / oxo / momo; OpenVLA
   becomes open vlm; SynGrasp-1B becomes "simsp 关闭" / "synthrose 关闭" /
   "single 关闭".
3. **Dataset names inside mixed-script lists.** Version suffixes drop and names
   merge: `bridge，Data oxe 和 droid` → BridgeData V2, OXE, DROID;
   `oele，Range，v2，和 joy 的` → OXE, Bridge V2, DROID; `objectverse…elvis` →
   Objaverse, LVIS subset; `G 数据集` → GRIT; `synth to real B` → SynGrasp-1B.
4. **Robot platform and hardware product names.** `croson` / `viber X` →
   Trossen ViperX; `ros` / `ax` / `hrx` / `lrx` → Trossen, ARX, AgileX; `fcon` /
   `fetch` → Fibocom; `阿罗卡` → ALOHA; `frank panda` → Franka Panda;
   `d415` → RealSense D415i.
5. **Tools and simulators.** `五洲口` / `某周口` → MuJoCo; `S 软件` → Isaac Sim;
   `古 logo` → CuRobo; `evlog` → EnvLogger; `vcad` → ACVD; `plate` → CLIP;
   `clip out` / `cliport` → CLIPort; `木` → MOO; `vc one` → VC-1; `R three m` →
   R3M; `C 看` → SayCan; `grinding dino` → Grounding DINO; `gr two G two X` →
   GR-2 / Gen2Act; `token 学习器` → Token Learner.
6. **Quantities attached to those names.** Numbers on names are the most
   error-prone: `width 1.24` → width = 1024; `16800 个物体实例` → 10,680;
   `20多万条轨迹` (RT-2) → the PDF gives no trajectory count (the RT-1 dataset it
   reuses is 130k, per the GraspVLA table); `Bridge v2 约5万条` → 60k;
   unverifiable pie-chart percentages quoted as if read.
7. **Homophone substitutions of technical terms.** These silently change meaning
   while reading perfectly:

   | Transcript | Correct | Meaning |
   |---|---|---|
   | 自回归零散化 | 自回归离散化 | autoregressive discretisation |
   | 流比配 / 有匹配 / 流体力学 | 流匹配 | flow matching |
   | 测量场 / 下一场杯 / 去噪散场 | 向量场 | vector field |
   | 跨域矩阵 / 跨学参 / 跨域身 | 跨具身 | cross-embodiment |
   | 灵巧 → 领导 / 领养 / 灵药 | 灵巧 | dexterous |
   | 零样本 → 灵量 | 零样本 | zero-shot |
   | 预随机化 | 域随机化 | domain randomisation |
   | 负对数自然损失 | 负对数似然损失 | negative log-likelihood |
   | 抗阻控制 | 阻抗控制 | impedance control |
   | 位置差值 | 位置插值 | positional interpolation |
   | 前线欧拉 | 前向欧拉 | forward Euler |
   | 归一化得分 → 规划得分 | 归一化得分 | normalised score |
   | 纵轴 → 数轴 | 纵轴 | vertical axis |
   | 多力度标注 | 多粒度标注 | multi-granularity labels |
   | 闭环 → 拍环 | 闭环 | closed loop |
   | 长时程 → 常识 | 长时程 | long-horizon |
   | 仿真环境 → 模仿环境 | 仿真环境 | simulation |
   | 失败案例 → 翻转案例 | 失败案例 | failure cases |
   | 疲惫的人 → 辟谣的人 | 疲惫的人 | "someone who is tired" |

8. **Page and figure anchors drifted.** Two verified off-by-N references in the
   corpus: π0's Figure 3 cited as p3 when it is on p4; GraspVLA's Figure 3 cited as
   p3 when it is on p5. Most anchors were correct, so distrust is not warranted —
   but every page number must be **spot-checked against the PDF**, not inherited.
   Similarly, figure numbers can mutate into words: `图七` → `图集`;
   `图十二` → `图示。二`.

## Do not "correct" these — they are already right

A naive cleanup pass breaks correct content. Verified-correct items that look
suspicious:

- `TFDS` is the real name of the storage format.
- `大象` really is the object category used for the Diffusion Policy baseline
  (elephant); `狗狗玩具` really is the dog toy spanning 2 cm–35 cm.
- `SPL` is the metric; `disco 灯` really is a disco light; `acvd`/ACVD is right.
- `单步运动规划` (single-step motion planning) and `非阻塞控制` (non-blocking
  control) are the paper's own terms.
- `LS2` / `LS1` are the loss labels the paper's LaTeX uses.
- `符号调优` = symbol tuning; `A/B 测试` = A/B testing framework; `安卓标志` =
  the Android logo.
- The π0 and GraspVLA **time-step directions are opposite on purpose** — both
  transcripts are right about their own paper.
- A lecturer's own illustrative numbers (a hypothetical chunk of 10 steps, a
  32-bit-to-8-bit quantisation example) are commentary, not paper claims. Mark them
  as illustration or drop them; do not report them as the paper's.

## Protocol for using a transcript as an input

1. Read it for the *explanations*: the chosen analogies, the order of teaching, the
   places the author anticipated confusion.
2. For every proper noun, look the canonical spelling up in
   `work/<slug>.structure.md`'s proper-noun frequency table or in the paged text.
3. For every number, find it in the PDF. If it is not there, do not carry it over —
   either drop it or mark it as the lecturer's illustration.
4. For every figure/table/page anchor, verify the page against the PDF.
5. For every mechanism, re-derive the explanation from the PDF rather than trusting
   the transcript's paraphrase; a transcript that says a backbone is Llama when the
   paper says Gemma will otherwise propagate the error into your script.

## Why this matters for the deliverable

The reference corpus is pedagogically strong and factually imperfect. The skill's
value is to keep the teaching and remove the errors: canonical names, verified
numbers, checked page anchors, and explicit symbol conventions. A script that fixes
`16800` to `10,680` and cites Figure 3 on the right page is strictly better than the
transcript it learned from.