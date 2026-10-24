# 第三方与参考来源

- 本项目新增代码和文档采用 MIT 许可，见 `project-MIT.txt`。以下第三方组件继续遵循各自许可。
- `scripts/vendor/am.mjs`：保留 Answer me with HTML 0.5.7 独立构建，来源 https://github.com/QingYunA/answer-me-with-html 。上游 MIT 许可见 `answer-me-with-html-MIT.txt`；内嵌法律声明保留。入口 `scripts/render.mjs` 为本技能新增。
- 渲染入口还会在成品中去掉自动字母章标与目录字母前缀；原始 bundle、底稿及用于跳转的锚点保持完整。
- 该构建内含 Dagre/Graphlib、Marked、Temml 和 Bangers 字体等；对应随包许可保存在本目录，Temml 涉及 Apache-2.0 的部分也保留许可文本。运行不依赖在线下载这些包。
- 公开包不含私人风格范本、论文全文或论文原图。`references/pi0-calibration.md` 是独立整理的讲解原则，不包含范本原文。
- `paper-reading-skill-main`：吸收其来源范围、图表核验、实验条件与证据边界思想，重新编写本技能规则；未整包复制，也不依赖它运行。

整合不包含上游技能的自动清理、更新、视频或主动全局调用策略。生成的论文内容及用户自行提供的资料不因本仓库许可证而自动获得新的授权。
