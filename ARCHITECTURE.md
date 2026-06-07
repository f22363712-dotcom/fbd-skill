# 架构文档

## 概述

FBD Skill 集合是运行在 Claude Code 环境中的一组技能（Skill）。每个技能是一个自包含的目录，包含 `SKILL.md`（或 `skill.md`）定义文件、可选脚本和参考文档。

该集合由两层架构组成：

```
┌────────────────────────────────────────────────────────┐
│                  路由层 (Router)                        │
│  project-compass → 识别阶段 → 路由到最佳技能             │
└────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────────┐    ┌──────────────────┐
│  构建型技能   │    │   阅读内化型技能   │    │ 其他下游技能      │
│ sop-creator   │    │ actor-reader      │    │ grill-me        │
│               │    │ socratic-discuss  │    │ tdd             │
│               │    │                   │    │ diagnose        │
│               │    │                   │    │ code-review     │
│               │    │                   │    │ ...             │
└──────────────┘    └──────────────────┘    └──────────────────┘
```

## 技能架构模式

每个技能遵循统一的架构模式：

```
{skill-name}/
├── SKILL.md           # 技能定义 — YAML 前置元数据 + Markdown 行为描述
├── references/        # 参考文档 — 框架详解、策略库等
├── scripts/           # [可选] 可执行脚本
└── assets/            # [可选] 模板资源
```

### SKILL.md 结构

- **YAML 前置元数据**：`name`、`description`、`version`
- **核心理念**：技能的设计哲学
- **工作流**：步骤化的执行流程
- **行为约束**：全局约束、FORBIDDEN/REQUIRED 规则
- **错误处理**：降级策略

## 各技能架构

### 0. project-compass（路由层）

**定位**：全局路由导航 — 识别用户当前阶段，路由到最适合的下一个技能。

**工作流**：

```
用户输入 → 识别阶段 → 查路由表 → 路由到目标技能
```

**路由决策表**：

| 用户需求 | 路由目标 |
|---------|---------|
| 想法模糊、范围不清 | `grill-me` |
| 项目术语混乱 | `grill-with-docs` |
| 实现功能/修复 bug | `tdd` / `prototype` |
| 审查 diff/PR | `code-review` / `review` |
| 硬 bug / 性能回退 | `diagnose` |
| 需要文档/PRD | `to-prd` |
| 需要分解任务 | `to-issues` |
| 安全审查 | `security-review` |
| 深度阅读 | `actor-reader` |
| 讨论内化 | `socratic-discuss` |

**关键设计原则**：
- 薄路由层 — 识别后立即交棒，不替代下游技能
- 无身份过滤 — 不因用户身份限制路由范围
- 不强制依赖 — 未安装的下游技能在 Route 表中跳过即可

**关键文件**：
- `project-compass/SKILL.md` — 路由定义与决策表

---

**定位**：元技能 — 用于生成其他 SOP 技能。

**状态机**：REQUIREMENTS → DESIGN → GENERATION → VALIDATION → COMPLETE

**核心机制**：
- 物理验证网关（exit code 强制）
- 显式状态机（有限、可审计的状态转换）
- 内置错误处理（三级降级阶梯）
- 结构化 I/O（类型化输入/输出）

**关键文件**：
- `skill.md` — 主定义（4 状态流水线）
- `scripts/validate_requirements.py` — 需求验证网关
- `scripts/validate_design.py` — 设计验证网关
- `scripts/validate_generation.py` — 生成验证网关
- `scripts/final_validation.sh` — 最终验证网关
- `assets/gateway-template.py` — 网关脚本模板
- `assets/gateway-template.sh` — Shell 网关模板
- `assets/state-machine-sop.md` — SOP Markdown 模板
- `references/vibecoding-principles.md` — VibeCoding 原则
- `references/engineering-gateways.md` — 网关工程指南

---

### 2. actor-reader

**定位**：阅读内化工具 — 将被动阅读转化为主动学习。

**工作流（ACTOR 框架）**：

```
Activate Purpose → Compress → Test → Own → Runbook
```

**各步骤**：
- **A** — 阅读前明确使命，从"游客式阅读"变为"间谍式阅读"
- **C** — 找到"树干"（核心论点），而非收集"树叶"（金句）
- **T** — 结构化反驳，与作者搏斗
- **O** — 移开视线，用自己的话重新梳理
- **R** — 将想法转化为决定/规则/检查清单/实验

**模式**：全流程模式、单步模式、续接模式

**关键文件**：
- `SKILL.md` — 主定义
- `references/actor-framework.md` — 框架详解与提示词库

---

### 3. socratic-discuss

**定位**：深度讨论工具 — 通过结构化对话内化知识。

**五种讨论模式**：

| 模式 | 典型信号 | 核心行为 |
|---|---|---|
| 🔍 理解验证 | "帮我理解""确认一下" | 让你先解释 → AI 指出遗漏 |
| ⚔️ 对手挑战 | "测试""反驳" | AI 扮演最强反驳者 |
| 🎓 教学模拟 | "教我""费曼" | 你当老师，AI 当学生 |
| 🔗 连接激活 | "和什么有关" | 扫描知识库，引导创建链接 |
| 🏃 行动转化 | "怎么用""行动" | 想法 → 可执行计划 |

**三级自适应深度**：
- 🟢 浅层（2-3 轮）— 快速确认理解
- 🟡 中层（4-6 轮）— 挑战隐含假设（默认）
- 🔴 深层（7-10+ 轮）— 彻底内化，改变思维框架

**关键文件**：
- `SKILL.md` — 主定义
- `references/depth-framework.md` — 自适应深度框架
- `references/questioning-strategies.md` — 苏格拉底提问策略库

## 跨技能集成

四个技能可以组合使用：

```
project-compass      → 路由导航，识别当前阶段
    │
    ├── sop-creator  → 生成自动化工作流
    ├── actor-reader → 深度阅读书籍/长文
    └── socratic-discuss → 讨论验证理解，挑战观点
```

例如：用户用 `/project-compass` 导航，识别到需要深度阅读 → 路由到 `/actor-reader` 执行阅读 → 读完后路由到 `/socratic-discuss` 挑战理解。

## 版本历史

- **1.1.0** — 集成 project-compass 路由层，形成"路由 → 执行"双层架构
- **1.0.0** — 初始版本，集成 sop-creator、actor-reader、socratic-discuss 三个技能
