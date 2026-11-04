# 架构文档

## 概述

FBD Skill 集合是运行在 Claude Code 环境中的一组技能（Skill）。每个技能是一个自包含的目录，包含 `SKILL.md` 定义文件、可选脚本和参考文档。

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

- **YAML 前置元数据**：`name`、`description`
- **核心理念**：技能的设计哲学
- **工作流**：步骤化的执行流程
- **行为约束**：全局约束、FORBIDDEN/REQUIRED 规则
- **错误处理**：降级策略

## 各技能架构

> **技能索引**：0. project-compass | 1. sop-creator | 2. actor-reader | 3. socratic-discuss | 4. skill-review | 5. postmortem-note | 6. repo-steward | 7. human-elite-english | 8. project-challenge-lab | 9. hackathon-practice | 10. recall-loop

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
| 候选技能、方法或项目方向需要与基线做受控比较 | `project-challenge-lab` |
| 实现功能/修复 bug | `tdd` / `prototype` |
| 审查 diff/PR | `code-review` / `review` |
| 硬 bug / 性能回退 | `diagnose` |
| 需要文档/PRD | `to-prd` |
| 需要分解任务 | `to-issues` |
| 复盘沉淀 | `postmortem-note` |
| 审查技能质量 | `skill-review` |
| 重建仓库决策、检查继续或停止信号 | `repo-steward` |
| 安全审查 | `security-review` |
| 深度阅读 | `actor-reader` |
| 讨论内化 | `socratic-discuss` |
| 英文社媒或专业文案真人感、专业度与发布前检查 | `human-elite-english` |
| 线上黑客松准备、执行或复盘 | `hackathon-practice` |
| 复习、备考、抽背、模拟考 | `recall-loop` |

**关键设计原则**：
- 薄路由层 — 识别后立即交棒，不替代下游技能
- 无身份过滤 — 不因用户身份限制路由范围
- 不强制依赖 — 未安装的下游技能在 Route 表中跳过即可

**关键文件**：
- `project-compass/SKILL.md` — 路由定义与决策表

---

### 4. skill-review

**定位**：元技能审查器 — 用八维评分体系评估 Claude Code skill 的质量。

**八维评分体系**：

| 维度 | 权重 | 核心问题 |
|------|------|---------|
| D1 触发精度 | 1.5x | description 够不够准确？会不会被误触发？ |
| D2 渐进披露 | 1.0x | 主文件是否 <100 行？细节是否合理外置？ |
| D3 负空间 | 1.0x | 有没有定义"不做什么"？ |
| D4 输出契约 | 1.0x | 每步有没有可验证的产物？ |
| D5 环境独立 | 0.5x | 有没有硬编码路径？能否跨机器工作？ |
| D6 失败模式 | 1.0x | 出错了会怎样？覆盖了边界情况吗？ |
| D7 组合性 | 0.5x | 能不能被其他 skill 调用？ |
| D8 指令可执行性 | 1.0x | 关键行为能否通过停止点、自检或脚本得到约束？ |

**评级**：🟢 生产级(85-100) / 🟡 可用(70-84) / 🟠 需重视(50-69) / 🔴 不建议(<50)

**关键文件**：
- `SKILL.md` — 主定义与工作流
- `RUBRIC.md` — 锚定评分描述符

---

### 5. postmortem-note

**定位**：故障修复复盘笔记 — 将非平凡修复转化为可检索、可复用的知识资产。

**工作流**：

```
收集素材 → 确认目录 → 按模板生成 → 用户确认后写入
```

**关键文件**：
- `SKILL.md` — 主定义与工作流
- `TEMPLATE.md` — 复盘笔记模板

---

### 6. repo-steward

**定位**：仓库决策复盘技能 — 从项目指令、领域文档、ADR、当前差异和 Git 历史中重建决策链，发现继续与转向/停止信号。

**工作流**：

```
识别当前决定 → 读取仓库约束 → 最小证据扫描 → 重建决策链 → 正反证据搜索 → 证据卡与下一步
```

**关键原则**：
- 安静是默认状态；没有新颖且可行动的证据时不制造输出
- 只提出会改变下一步的问题
- 观察不等于行动授权，持久记忆必须写入用户可见的项目文档
- 不保留宠物人格、情绪施压、独立 UI 或隐藏记忆系统

**关键文件**：
- `repo-steward/SKILL.md` — 主工作流与安全边界
- `repo-steward/references/evidence-cards.md` — 发现、异议、问题和复盘卡片格式

---

### 7. human-elite-english

**定位**：英文社媒与专业文案写作、改稿和发布前风格验收。

**工作流**：

```
确认形式与说话位置 → 检查材料 → 起草 → 九项风格 TDD → 确定性脚本检查 → 交付
```

**关键原则**：
- 真人感来自具体对象、材料和自然推进，不靠俚语或伪造经历
- 精英感来自克制判断、术语准确和边界意识，不靠密集黑话
- 九项语义门禁全部通过后才能标记 `style_tdd=PASS`
- 检查脚本只报告确定性问题，不自动改稿，也不代替事实核验

**关键文件**：
- `human-elite-english/SKILL.md` — 主工作流与形式约束
- `human-elite-english/references/tdd-rubric.md` — 九项 TDD 门禁
- `human-elite-english/scripts/check_english.py` — 确定性风格检查器

---

### 8. project-challenge-lab

**定位**：项目质疑与受控实验技能。先限定证据、基线和采用门槛，再比较候选方法或方向，把有证据的结果拆成可逆的个性化首段制作。

**工作流**：

```
定义待验证决定 → 建立最小证据包 → 基线与候选对照 → 匿名评审 → 达标后拆首段制作
```

**关键原则**：
- 仓库历史与继续/停止判断仍交给 `repo-steward`
- 候选方法是否增加价值必须与无方法基线比较
- 结果接近时保留独立发现，不把排名包装成显著优势
- 只有达到预先声明的门槛且用户已授权，才进入可逆的首段制作

**关键文件**：
- `project-challenge-lab/SKILL.md` — 决策、实验与行动边界
- `project-challenge-lab/references/evaluation-rubric.md` — 七项评分锚点和淘汰规则
- `project-challenge-lab/agents/openai.yaml` — 调用界面元数据

---

### 9. hackathon-practice

**定位**：线上黑客松证据交付工作流。它把赛事信息、选题、最高风险验证、时间冻结、断线续作、提交和复盘放进同一套可观察流程。

**关键边界**：它管理比赛过程；`gate` 管单次交付的判断；它不代替用户决定不可逆选题、诚信披露、停止或提交。

**关键文件**：
- `hackathon-practice/SKILL.md` — 触发条件、硬规则、模式和输出契约
- `hackathon-practice/references/operating-model.md` — 时间比例、选题门和交付优先级
- `hackathon-practice/references/continuity-playbook.md` — 断线、用量和官方渠道故障处理
- `hackathon-practice/references/retro-template.md` — 事实时间线与可迁移规则模板

---

### 10. recall-loop

**定位**：检索式学习闭环。把「看过」变成「调得出」：检索练习（testing effect）+ 间隔重复排期 + 苏格拉底追问 + 限时模拟考。

**关键边界**：它只出题、判定、追问、排期，**绝不生成总结/大纲/笔记**——那是卸载认知。懂不等于会，说出来才算会。理解材料用 `socratic-discuss` / `actor-reader`；长期保持与考前彩排用本技能。

**关键文件**：
- `recall-loop/SKILL.md` — 六条铁律、四类会话、收尾格式
- `recall-loop/references/question-design.md` — 六种高杠杆题型与再认反例
- `recall-loop/references/scheduling.md` — 1→3→7→16→35→75 天阶梯与台账格式
- `recall-loop/references/exam-simulation.md` — 组卷、开考、批改口径、复盘三问
- `recall-loop/scripts/due.py` — 从台账计算今日到期卡片

---

### 1. sop-creator

**定位**：元技能 — 用于生成其他 SOP 技能。

**状态机**：REQUIREMENTS → DESIGN → GENERATION → VALIDATION → COMPLETE

**核心机制**：
- 物理验证网关（exit code 强制）
- 显式状态机（有限、可审计的状态转换）
- 内置错误处理（三级降级阶梯）
- 结构化 I/O（类型化输入/输出）

**关键文件**：
- `sop-creator/SKILL.md` — 主定义（4 状态流水线）
- `sop-creator/scripts/validate_requirements.py` — 需求验证网关
- `sop-creator/scripts/validate_design.py` — 设计验证网关
- `sop-creator/scripts/validate_generation.py` — 生成验证网关
- `sop-creator/scripts/final_validation.sh` — 最终验证网关
- `sop-creator/assets/gateway-template.py` — 网关脚本模板
- `sop-creator/assets/gateway-template.sh` — Shell 网关模板
- `sop-creator/assets/state-machine-sop.md` — SOP Markdown 模板
- `sop-creator/references/vibecoding-principles.md` — VibeCoding 原则
- `sop-creator/references/engineering-gateways.md` — 网关工程指南

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

十一个技能可以组合使用：

```
project-compass      → 路由导航，识别当前阶段
    │
    ├── sop-creator        → 生成自动化工作流
    ├── actor-reader       → 深度阅读书籍/长文
    ├── socratic-discuss   → 讨论验证理解，挑战观点
    ├── skill-review       → 审查本仓库其他技能的质量
    ├── postmortem-note    → 修复后沉淀复盘笔记
    ├── repo-steward       → 仓库复盘、决策异议与停止信号
    └── project-challenge-lab → 候选方法对照实验与个性化首段制作
```

典型用户旅程：
1. `/project-compass` → 识别到需要深度阅读 → 路由到 `/actor-reader`
2. 读完后 → 调用 `/socratic-discuss` 挑战理解
3. 或：遇到复杂 bug → `/diagnose` → 修复后 → `/postmortem-note` 沉淀
4. 或：写了一个新 skill → `/skill-review` 审查质量
5. 或：项目方向摇摆 → `/repo-steward` 重建决策链并寻找继续/停止信号
6. 或：候选技能或方案是否有效尚无证据 → `/project-challenge-lab` 与基线做受控比较

## 多语言文档

- `README.md` — 英文说明（GitHub 首页默认渲染）
- `docs/README_CN.md` — 中文版说明

## 版本历史

- **1.4.0** — 新增 project-challenge-lab，并接通受控项目实验路由
- **1.3.0** — 接通 repo-steward 路由；统一技能目录；增加安装器、目录检查和八维文档
- **1.2.0** — 集成 skill-review、postmortem-note；增加多语言文档
- **1.1.0** — 集成 project-compass 路由层，形成"路由 → 执行"双层架构
- **1.0.0** — 初始版本，集成 sop-creator、actor-reader、socratic-discuss 三个技能
