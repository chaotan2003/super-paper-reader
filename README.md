# Super Paper Reader · 超级论文阅读

一个支持 **Codex** 和 **DeepSeek Harness（DSH）** 的论文讲解 skill。输入论文链接或本地 PDF，让 agent 阅读原文、核对图表，生成适合连续阅读的中文精读网页。

重点是讲清“为什么需要这一步、具体怎样算、结果又交给谁”，并保留论文自己的术语与数学符号。

## 最终会得到什么

```text
outputs/<paper-slug>/
├── <paper-slug>.html   # 阅读成品：目录、原图、教学图和离线数学
├── <paper-slug>.md     # 可继续修改的底稿
└── assets/            # 从当前论文整理的图片
```

HTML 内嵌图片及数学资源，可以离线打开并单独发送；论文来源等外部链接仍需联网。Markdown 和图片保留在本地，方便之后修订。

全文沿实际论文主章节展开：相关工作交代问题如何演进及本文位置；Method 内部只设“1. 方法概述”和“2. 具体实现”，结合主图与问题建模后，以连续段落走通实现；实验以问题展开，说明对照、设计、实施、图表结果及有依据的原因。材料不足时会说明范围，不补造论文没有的事实。

## 环境要求

- 已安装并配置好 Codex 或 DeepSeek Harness。
- **Node.js 20 或以上**，用于安装脚本和 HTML 渲染。运行 `node --version` 检查。
- agent 能读取文件、执行命令，以及阅读 PDF 和查看图表。链接输入还需要宿主允许联网获取论文。
- 使用 Git 克隆，或下载 GitHub 的 ZIP 后解压。

渲染器和所需库已随包提供，**不需要运行 `npm install`**。这个仓库提供 skill，不替代 agent，也不提供模型服务或 API key；实际阅读使用宿主已配置的模型及工具。

## 安装

### 1. 获取仓库

克隆仓库，或下载 ZIP，解压后在仓库根目录打开终端。

```bash
git clone https://github.com/chaotan2003/super-paper-reader.git
cd super-paper-reader
```

### 2. 选择安装对象

Windows PowerShell、macOS 和 Linux 使用相同命令：

```bash
# 安装到 Codex
node scripts/install.mjs --target codex

# 或安装到 DeepSeek Harness
node scripts/install.mjs --target dsh

# 或同时安装到两者
node scripts/install.mjs --target both
```

安装脚本只复制 `skills/super-paper-reader/`，不复制仓库历史、README 或开发目录，不修改全局配置、不启动服务。

| 安装对象 | 默认用户级目录 | 指定项目后的目录 |
| --- | --- | --- |
| Codex | `~/.agents/skills/super-paper-reader/` | `<项目根>/.agents/skills/super-paper-reader/` |
| DSH | `~/.dsh/skills/super-paper-reader/` | `<项目根>/.dsh/skills/super-paper-reader/` |

`~` 表示用户主目录。DSH 设置了 `DSH_HOME` 时，用户级安装改用该目录下的 `skills/`。项目安装应指向项目的 Git 仓库根目录：

```bash
node scripts/install.mjs --target both --project "/path/to/your/project"
```

只想预览安装位置，可加 `--dry-run`：

```bash
node scripts/install.mjs --target both --dry-run
```

需要自行管理技能目录，或正在使用旧版 Codex 的 `~/.codex/skills` 时，用 `--dir` 指定实际的 **skills 父目录**；此选项只支持一个安装对象。不要在新旧目录同时保留同名 skill。

```bash
node scripts/install.mjs --target codex --dir "/actual/path/to/skills"
```

安装后开启新对话；如果技能尚未出现，重启宿主。DSH 自定义组合需要启用其 filesystem skill provider 和 skill tool，默认目录由宿主扫描。

安装路径依据 [Codex 官方说明](https://developers.openai.com/codex/skills/) 和 [DSH 上游 Skills 文档](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/skills.md)。DSH 也支持共享的 `.agents/skills`；已经能在两边发现同一份 skill 时，无需再装重复副本。

### Codex 的另一种安装方式

也可以在 Codex 对话中让内置安装器完成安装，选择此方式就不用再运行上面的安装脚本：

```text
$skill-installer 从 https://github.com/chaotan2003/super-paper-reader
安装 skills/super-paper-reader。
```

## 使用方法

### Codex

在对话中输入 `$super-paper-reader`，或从技能选择器中选中它，然后提供链接或 PDF：

```text
$super-paper-reader
请精读这篇论文：https://arxiv.org/abs/论文编号
结合原方法主图解释输入输出与计算过程，生成中文离线网页。
```

### DeepSeek Harness

从宿主技能入口选择 `super-paper-reader`，或直接告诉 agent 使用它：

```text
请使用 super-paper-reader skill，精读我附上的论文PDF。
先阅读正文与必要附录，查看原图表，再生成中文精读网页。
```

本地文件也可以直接给路径，含空格时保留引号：

```text
使用 super-paper-reader，精读 "/path/to/My Paper.pdf"。
输出保存到 outputs/my-paper/。
```

### 修改已有精读

```text
用 super-paper-reader 更新 outputs/my-paper/my-paper.md。
只优化Method：保留方法概述和具体实现两个标题，按原计算流程连续讲解，
术语和数学符号与原文一致。重新生成同名HTML。
```

可指定只处理某个章节；明确的范围要求优先。源材料只有摘要时，不能生成声称已核验全文的解读。

## 本地渲染与检查

skill 的阅读、分析和写作由 agent 完成；渲染脚本负责把已经写好的 Markdown 转为网页。

在仓库根目录运行：

```bash
# 不访问模型或论文，检查渲染环境
npm run demo

# 渲染实际底稿，图片使用相对于底稿的本地路径
node skills/super-paper-reader/scripts/render.mjs outputs/my-paper/my-paper.md

# 自定义成品路径
node skills/super-paper-reader/scripts/render.mjs outputs/my-paper/my-paper.md --out outputs/my-paper/reading.html

# 检查安装、更新保护、离线资源和渲染可迁移性
npm test
```

示例会生成 `examples/render-demo.html`，它只演示排版，不是论文分析。渲染状态存于输出旁的 `.paper-reading-renderer/`，不会修改用户的全局渲染设置。已安装副本也能从其他工作目录运行，使用该副本中 `scripts/render.mjs` 的实际路径即可。

结构和渲染测试不能替代人工核对论文事实、原图表及讲解逻辑。仓库附有 Windows、macOS、Linux 的 CI 配置，实际通过情况以 GitHub Actions 为准。

## 更新与卸载

更新仓库后重新安装：

```bash
git pull --ff-only
node scripts/install.mjs --target both --replace
```

只使用一个宿主时，把 `both` 换成原来的安装对象；使用 `--project` 或 `--dir` 安装的，更新时仍带上原参数。默认拒绝覆盖；`--replace` 会先备份旧版本，终端显示备份路径。备份保存在所选 skills 父目录上一级的 `.super-paper-reader-backups/`，不参与正常技能扫描，也会保留旧副本内的本地修改。

卸载时，在文件管理器中删除安装脚本显示的 `super-paper-reader` 目录即可。已有阅读成品和底稿保存在工作区，不受卸载影响；不再需要的备份可单独处理。

## 仓库结构

```text
super-paper-reader/
├── README.md
├── LICENSE
├── scripts/                       # 跨平台安装及安装测试
├── examples/render-demo.md         # 最小渲染示例
├── .github/workflows/ci.yml
└── skills/super-paper-reader/
    ├── SKILL.md                   # 技能入口
    ├── agents/openai.yaml         # Codex界面元数据；DSH无需依赖
    ├── references/                # 写法、证据、HTML与验收规范
    ├── scripts/                   # 渲染入口、测试和离线bundle
    └── licenses/                  # 项目与第三方许可
```

## 许可证与来源

本项目新增代码和文档采用 [MIT](LICENSE)。离线渲染器基于 [Answer me with HTML](https://github.com/QingYunA/answer-me-with-html)，其上游许可与内嵌依赖许可完整保留，见 [第三方说明](skills/super-paper-reader/licenses/NOTICE.md)。

公开包不包含私人风格范本、论文全文或原图，也不包含作者电脑路径、凭据和实际阅读输出。生成时使用的论文和图片保留原作者权利。

作者：[Chao Tan · chaotan2003](https://github.com/chaotan2003)。

## 发布到 GitHub（维护者）

在 `chaotan2003` 账号下创建名为 `super-paper-reader` 的空仓库，然后在本仓库根目录执行：

```bash
git init -b main
git add .
git commit -m "Initial release of super-paper-reader"
git remote add origin https://github.com/chaotan2003/super-paper-reader.git
git push -u origin main
```

本地已经初始化或配置过 `origin` 时，跳过对应命令。上传的是整个仓库；需要单独复制安装时，只复制 `skills/super-paper-reader/`。实际阅读输出和渲染状态已在 `.gitignore` 中排除。跨平台 CI 会在上传后运行，检查结果可在仓库 Actions 页面查看。
