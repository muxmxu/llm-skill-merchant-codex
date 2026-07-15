# MISSION: <survey title> — <one-line scope / lens>

授权：<who>，<date>。镜头=<technique-transfer / domain-mapping / failure-mode>（写清是哪种视角，避免变成领域铺陈）；规模=<~N 篇>；记录 Codex 并发槽上限与是否需要跨 session 续跑。

## 阶段

1. **搜索**（按 Codex 当前并发槽分批，N 角度）→ 每角度写 `findings-<角度>.md`，目标 8-12 篇/角度。
2. **排重 + 下载**（主循环）→ 跨角度去重、排除已有（见排重清单）、选定 ~N 篇、PDF 下到 `reference/<topic>/`、生成 `review-manifest.md`（编号表：# | Title | Venue+Year | Primary angle | PDF filename | Note filename）。可旁出 `<topic>.bib`。
3. **精读**（≤4 篇/agent，幂等）→ 笔记写 `AI-Dug-Papers/<YYYY-MM>/`，frontmatter `status: reading` / `origin: ai-survey`，tag 加 `AI-dug` + 主题 tag；杂谈节=迁移分析（高/中/低 + 具体机制 + 命中哪个 transfer target + 风险）。笔记格式见 `references/literature-survey.md`。
4. **核验 + 综述 + 汇报** → 分派独立 reviewer 逐篇对 PDF，返回 FIXED/PASS/FLAG → 每族分派一个 digest → 主会话合成 `synthesis-draft.md` → 写 vault research log → 终检链接（0 死链）→ 汇报。

## 规则

1. 调度：只使用 Codex 当前工具实际暴露的参数。不得虚构子任务模型或 effort 控制。
2. 笔记规范：`references/literature-survey.md` 的 "Per-paper note format"。
3. 检索纪律：peer-reviewed 优先、venue 从论文核实、read-before-claim、负面结果一等公民、收敛 ≥2 源、originals over surveys。
4. AI 不设 `status: read`（那是人亲读后才翻）；log 里不记哪个 AI 干的（人是作者）。
5. 综述引用 AI 笔记标「出自 AI 精读，未亲核」。
6. <项目特定红线，例如：不碰服务器代码、不跑训练>。

## N 角度（每角度带迁移钩子）

> 每个角度 = 一个 `findings-<key>.md` + manifest 的 "Primary angle"。钩子写清「从本项目视角，这个角度要找什么」。

- A. `<key>` — <技术族关键词>；钩子=<项目视角下要找什么>。
- B. `<key>` — …；钩子=…。
- …

## 排重清单（搜索 agent 须排除）

- 已有笔记：<列已存在的 AI-Dug / PaperReview 笔记>。
- 已有 PDF：<列 reference/ 下已有的>。
- Zotero 相关分类：<列分类>——跳过通用基础综述。

## STATE

> 每阶段完成后在此打勾 + 留断点信息（task/run id、文件落点）。这是断点续跑的依据。

- [ ] 阶段1 搜索：
- [ ] 阶段2 排重+下载：
- [ ] 阶段3 精读：
- [ ] 阶段3.5 全量验证：
- [ ] 阶段4 综述+汇报：

## RESUME（usage limit 中断后断点续跑）

**checkpoint = 文件系统**。每篇笔记写到 `AI-Dug-Papers/<YYYY-MM>/` 即落盘，不依赖 session 或 agent 内存。每个 agent 写前先查目标笔记是否已完整，是则 SKIP。中断后只重新分派缺失项。

续跑步骤：
1. 查进度：`bash check-progress.sh`（先填好里面的 MANIFEST / NOTEDIR）→ 打印 已写 / 缺失 + 缺失笔记名。
2. 有缺失就按当前可用并发槽重建精读任务。每个任务只领取互不重叠的 note 文件；已完成项立即 SKIP。
3. 精读齐了 → 阶段3.5 verify → 阶段4 digest + synthesis + log + 终检。

> Codex 子任务共享文件系统。同一个 note 文件禁止并发写入。最终整合、终检和人类汇报只由主会话执行。
