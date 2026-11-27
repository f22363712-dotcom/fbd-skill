---
name: memory-dreaming
description: "Manage project-level file-system progressive memory (.agents/memory/ or .claude/memory/) and run out-of-band Dreaming memory consolidation (prune stale notes, deduplicate/merge, extract blind spots, and promote recurring pitfalls into deterministic code gates or Skills). Use when the user asks to initialize project memory, run Dreaming or memory cleanup/consolidation, or audit project memory against the current codebase."
---

# 文件系统渐进式记忆与带外整理规范 (`memory-dreaming`)

本技能用于在任意项目中维护轻量化、零膨胀的 **文件系统项目活记忆库**（Antigravity 默认 `.agents/memory/`，Claude Code 可用 `.claude/memory/`），并通过周期性 **Dreaming（带外记忆整理）** 实现记忆的新陈代谢（去腐烂、合并、以及把高频踩坑**晋升**为代码门禁或 Skill 后删除旧文本）。

---

## 一、目录结构与职责边界（防多头记账）

```text
.agents/memory/       # （Claude Code 环境可用 .claude/memory/）
├── INDEX.md          # 总索引（严控 <= 50 行，每条仅文件名 + 一句话摘要）
├── architecture/     # 尚未固化为文档/代码的项目架构权衡、模块隐性依赖
├── pitfalls/         # 跨会话易复发的环境/工具/平台隐蔽陷阱（一次性报错禁入）
└── preferences/      # 用户明确纠正的个人代码风格、命名规范与交互偏好
```

**与其他层的严格分工（零重复抄写）**：
- **L1 硬门禁**（Linter / 测试 / 校验脚本 / Hook）：能用代码自动拦截的规则，**只写代码，不留在 `memory/`**；
- **L2 薄宪法**（`AGENTS.md` / `CLAUDE.md`）：全局不可妥协底线 + 路由表 + 一行 `INDEX.md` 入口路标；
- **L3 稳定工序**（`skills/` + `references/`）：稳定可复用的 SOP 与命令手册；
- **L4 活记忆库**（`memory/`）：仅存**尚未固化为代码或 Skill 的项目私有活事实、隐蔽坑与长期偏好**。

---

## 二、日常读写自律协议（按需读 + 严控噪音写）

### 1. 按需读取（进入新任务、跨模块改动或遇到异常报错时）
- 先读取 `INDEX.md`；
- 仅当当前任务与索引中某条直接相关时，按需读取对应 `.md` 文件，**严禁一次性全量加载所有记忆**。

### 2. 自主写入准入门槛（严防流水账）
- **仅允许写入两类内容**：① 跨会话一定会再踩的隐蔽 Bug / 环境或平台怪癖；② 用户明确纠正的长期风格/交互偏好。**一次性拼写错、偶发网络抖动、常规已知语法绝不写入。**
- 每篇记忆笔记必须精炼（建议 `<= 40` 行），顶部强制带元信息方便日后核销：
  ```markdown
  ---
  category: architecture | pitfalls | preferences
  related_files: [path/to/file1, path/to/file2]
  last_verified: YYYY-MM-DD
  ---
  ```
- 写入后同步更新 `INDEX.md`（一行摘要），并在当轮回复末尾**用一行明确告知用户记入了哪条记忆**，绝不暗中静默塞垃圾。

---

## 三、新项目冷启动初始化（当项目尚无记忆目录时）

按需创建以下骨架，并在项目根规则文件（`AGENTS.md` 或 `CLAUDE.md`）顶部补一行入口路标：
1. 创建 `INDEX.md` 与 `architecture/`、`pitfalls/`、`preferences/` 三个子目录；
2. 在根规则文件顶部加一行路标：
   > **项目活记忆入口**：新任务/跨模块改动/遇异常时先按需查 `.agents/memory/INDEX.md`（或 `.claude/memory/INDEX.md`，禁全量加载）；跨会话隐蔽坑与长期偏好按 `memory-dreaming` 规范精炼入库并明示。

---

## 四、Dreaming（带外记忆整理）四步执行流程

当用户要求进入 **Dreaming / 整理记忆库** 时，**暂停新功能开发**，严格按以下四步执行：

1. **全量盘点与去重**：扫描记忆目录下所有 `.md` 文件（含 `INDEX.md`）与项目最新代码/技能结构。
2. **对照代码去腐烂（验证实效性）**：检查每条笔记的 `related_files` 与关键符号在当前代码中是否仍存在、是否已被新代码/Linter 替代或与最新逻辑冲突，逐条标记「仍有效 / 已过期 / 已冲突」。
3. **提炼高频盲区与“晋升”评估**：
   - 回顾近期对话中用户反复强调的纠正或反复踩中的坑，提炼结构化条目；
   - 对高频命中且**可量化/可机检**的 `pitfalls/` 条目，提出 **【晋升】** 建议（改写成 Linter/测试或收编进对应 Skill，然后**删除原记忆笔记**，防止记忆库无限膨胀）。
4. **先呈批《记忆库整理提案》，人工确认后再落盘**：
   - **严禁直接静默覆盖或删除文件！**
   - 向用户输出结构化《记忆库整理提案》，清晰分列四类操作与理由：**【晋升】、【新增】、【合并】、【删除（去腐烂）】**；
   - 待用户明确回复 **“确认”** 后，再正式执行文件增删改、升级对应脚本/Skill，并重构精简 `INDEX.md`（目标保持 `<= 50` 行）。
