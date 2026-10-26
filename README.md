# Super Paper Reader · 超级论文阅读

把一个研究论文变成一篇**可以连续听下来的中文长文讲解稿**（Markdown）。它逐节、逐图、
逐表、逐公式地讲清楚一篇论文，而不是写一篇摘要。

**只支持 DeepSeek Harness（DSH）安装。**

## 最终会得到什么

```text
<论文所在目录>/
└── 讲解稿/
    └── <论文短名>_讲解稿.md
```

- **长度**：每页 PDF 约 400–800 个中文字；15–25 页的论文大约 10,000–16,000 字。三千字
  的稿子说明写成了摘要，需要重写。
- **结构**：沿用论文自己的章节标题（逐字照抄，包括原始大小写，不改名、不调序、不合并），
  论文没有的章节不凭空补标题。
- **覆盖**：每张图（含编号与页码）、每个独立公式（论文不给公式编号也算）、每张承载结论的
  表格。表格要读出关键单元格，只说「结果列在表七里」不算讲到。
- **溯源**：正文里带「论文第X页的图Y」「附录 L」这类定位锚点，头条数字要能追到某个单元格。
- **不编造**：论文没给的数字就说没给；为了演示而举的数字会当场声明是讲解者自己举的例子。
- **公式**：所有公式都写在 `$…$`（行内）或 `$$…$$`（独立成行）里；符号表用 Markdown 表格，
  且每个符号单元格都是 `$…$`。
- **风格**：讲解腔的连续长文，一段一段讲，不是要点清单；每个关键机制配一个不改变结构的类比。

## 它不是什么

| 你想要 | 请用 |
| --- | --- |
| 简短的通俗精读笔记、批判性深读 | `paper-reading` |
| 全文双语翻译与来源对照 | `nature-reader` |
| 固定 16 节的 Paper Card | `nature-paper-card` |
| 正式审稿意见 | `nature-reviewer` |
| 同一份讲稿的网页版 | `paper-lecture-html` |
| **论文讲解稿（本仓库）** | `super-paper-reader` |

## 环境要求

- 已安装并配置 **DeepSeek Harness**（这是唯一支持的宿主）。
- **Python 3**，用于 PDF 提取、图表测绘与覆盖核对脚本。
- **PyMuPDF**（`pip install pymupdf`）：把 PDF 页面渲染成图片给模型看，以及在没有图像识读
  能力时做图表结构测绘。装了它提取质量也更好。
- `pdftotext` / `pdftoppm`（poppler-utils）：没有 PyMuPDF 时的后备提取方式。
- agent 需要能读文件、执行命令，并且**能看图片**——图里的面板布局、曲线、坐标刻度只能看图
  得到，不能从文本猜。
- 安装脚本需要 **Node.js 20 或以上**；不想装 Node 就按下面方式二手动复制。

## 安装

### 方式一：安装脚本

```bash
git clone https://github.com/chaotan2003/super-paper-reader.git
cd super-paper-reader

# 用户级安装：$DSH_HOME/skills，未设置 DSH_HOME 时用 ~/.dsh/skills
node scripts/install.mjs

# 只装给某个项目
node scripts/install.mjs --project "/path/to/your/project"

# 先看看会装到哪里，不写任何文件
node scripts/install.mjs --dry-run

# 覆盖已有同名 skill（旧版本会先移到备份目录）
node scripts/install.mjs --replace
```

| 选项 | 作用 |
| --- | --- |
| （不加） | 用户级：`$DSH_HOME/skills/super-paper-reader`，未设置 `DSH_HOME` 时 `~/.dsh/skills/super-paper-reader` |
| `--project <root>` | 项目级：`<项目根>/.dsh/skills/super-paper-reader` |
| `--dir <skills 父目录>` | 自行指定技能父目录，与 `--project` 互斥 |
| `--replace` | 覆盖前把旧版本移到 `.super-paper-reader-backups/` |
| `--dry-run` | 只打印目标路径 |
| `--help` | 打印用法 |

脚本只复制 `skills/super-paper-reader/`，不复制仓库历史、README 和开发目录，不修改全局
配置，不启动后台服务，不联网下载。

### 方式二：手动复制

```bash
cp -r skills/super-paper-reader ~/.dsh/skills/
```

设置了 `DSH_HOME` 时复制到 `$DSH_HOME/skills/`。安装完开一个新对话；技能还没出现就重启
宿主。不要在两个位置同时保留同名 skill。

## 使用

在 DSH 里从技能入口选 `super-paper-reader`，或者直接说：

```text
请使用 super-paper-reader，精读这篇论文：/path/to/paper.pdf
```

也可以给链接或已提取的笔记。默认输出到论文旁边的 `讲解稿/` 目录，文件名
`<论文短名>_讲解稿.md`；也可以指定目录，路径含空格时加引号。

技能内部按五个阶段走：

1. **提取与测绘**——`extract_paper.py` 得到分页文本与章节/图表/公式清单，再核对成证据清单。
2. **拿到图的真实结构**——`render_pages.py` 渲染页图给模型看；不能看图时用 `figure_map.py`
   从 PDF 对象里恢复图内文字与位置。
3. **逐节起草**——按论文原始标题顺序写，方法重就先把方法与实验写完，再校准背景章节。
4. **覆盖与保真核对**——`check_coverage.py` 找出漏讲的图表公式，再过一遍 QA 清单。
5. **交付**——写出 `.md`，并在回复里报告字数与覆盖统计（图 x/y、公式 x/y）。

## 仓库结构

```text
skills/super-paper-reader/
├── SKILL.md                  # 技能主体：公式硬性原则、不可协商规则、字数预算、五阶段流程
├── references/               # 10 份细则：风格、逐节结构、图表与公式讲法、领域适配、QA 清单
├── assets/script-template.md # 填空式讲稿脚手架
└── scripts/                  # 4 个 Python 脚本（提取 / 渲染 / 图表测绘 / 覆盖核对）
scripts/install.mjs           # 安装器，只支持 DSH
scripts/test-install.mjs      # 安装器测试
```

细则里最常用的几份：[风格指南](skills/super-paper-reader/references/style-guide.md)、
[逐节结构模板](skills/super-paper-reader/references/structure-template.md)、
[图表与公式讲法](skills/super-paper-reader/references/narrating-visuals.md)、
[交付前 QA 清单](skills/super-paper-reader/references/qa-checklist.md)。

## 自检

```bash
npm test                                   # 安装器测试 + 文档内链检查
python3 -m py_compile skills/super-paper-reader/scripts/*.py
```

## 版本说明

仓库早期版本是一个 Codex + DSH 双宿主、输出 HTML 的讲解 skill（自带离线数学渲染器）。
现在这个仓库改为**只支持 DSH、输出 Markdown 讲稿**的 Super Paper Reader；旧版本的代码与
许可证文件仍在 git 历史里，需要时可以取回。想要网页版输出，请配合 `paper-lecture-html`
skill 使用同一份讲稿底稿。

## 许可

MIT，见 [LICENSE](LICENSE)。