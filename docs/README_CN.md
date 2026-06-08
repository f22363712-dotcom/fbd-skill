# FBD Skill 集合

Claude Code 技能（Skill）集合仓库，包含一系列增强 Claude Code 能力的专用工具包。

> [English version →](../README.md)

## 架构概览

本仓库采用 **路由层 → 执行层** 双层架构：

```
project-compass (路由层) — 识别阶段 → 路由到最佳技能
    │
    ├── sop-creator        — 确定性状态机 SOP 生成器
    ├── actor-reader       — ACTOR 五步阅读框架
    ├── socratic-discuss   — 苏格拉底式讨论伴侣
    ├── skill-review       — 七维技能质量审查器
    ├── postmortem-note    — 故障修复复盘笔记生成器
    └── ...                — 路由到外部技能（grill-me、tdd、diagnose 等）
```

## 技能清单

| 技能 | 说明 |
|------|------|
| [project-compass](project-compass/SKILL.md) | 项目导航仪 — 路由到最适合当前阶段的下一个技能 |
| [sop-creator](skill.md) | 确定性状态机 SOP 生成器 — 将概率性 AI 转化为可靠的自动化流水线 |
| [actor-reader](actor-reader/SKILL.md) | ACTOR 五步阅读框架 — 将 AI 作为阅读教练，深度内化书籍与长文 |
| [socratic-discuss](socratic-discuss/SKILL.md) | 苏格拉底式讨论伴侣 — 通过结构化对话帮助深度内化知识 |
| [skill-review](skill-review/SKILL.md) | 元技能审查器 — 七维评分审查技能质量，输出可执行改进建议 |
| [postmortem-note](postmortem-note/SKILL.md) | 故障修复复盘笔记 — 将非平凡修复沉淀为可检索的知识资产 |

## 安装

将本仓库克隆到 Claude Code 的 skills 目录：

```bash
# 进入 Claude Code skills 目录
cd ~/.claude/skills

# 克隆仓库
git clone https://github.com/f22363712-dotcom/fbd-skill.git
```

或使用符号链接（推荐，方便更新）：

```bash
ln -s /path/to/fbd-skill/* .
```

## 使用

在 Claude Code 中通过斜杠命令调用各技能：

- `/project-compass` — 项目导航，路由到正确技能
- `/sop-creator` — 生成 SOP 工作流
- `/actor-reader` — 启动 ACTOR 阅读框架
- `/socratic-discuss` — 启动苏格拉底式讨论
- `/skill-review` — 审查 skill 质量
- `/postmortem-note` — 复杂修复后写复盘笔记

## 项目结构

```
fbd-skill/
├── skill.md                   # sop-creator 核心定义
├── scripts/                   # sop-creator 验证脚本
├── assets/                    # sop-creator 模板资源
├── docs/
│   └── README_CN.md           # 中文文档
├── project-compass/           # 项目导航仪（路由层）
│   └── SKILL.md
├── actor-reader/              # ACTOR 阅读框架
│   ├── SKILL.md
│   └── references/
├── socratic-discuss/          # 苏格拉底讨论伴侣
│   ├── SKILL.md
│   └── references/
├── skill-review/              # 元技能审查器
│   ├── SKILL.md
│   └── RUBRIC.md
├── postmortem-note/           # 复盘笔记生成器
│   ├── SKILL.md
│   └── TEMPLATE.md
├── README.md                  # 英文说明（GitHub 默认首页）
└── ARCHITECTURE.md            # 架构文档
```

## 架构借鉴而非全部安装

本仓库的**核心价值在于路由架构和技能设计模式**，而非让您安装所有依赖。

`project-compass` 是一个路由层，它指向的下游技能众多（如 `grill-me`、`tdd`、`diagnose` 等）。您可以：

- **完整安装** — 克隆仓库并配置所有依赖技能
- **选择性借鉴** — 仅采用架构理念，根据自身需求实现或替换其中部分技能
- **二次开发** — 修改 `project-compass/SKILL.md` 的路由表，只保留或替换您需要的路线

本仓库自带以下技能可直接使用：
- `project-compass` — 路由导航
- `sop-creator` — SOP 生成
- `actor-reader` — ACTOR 阅读框架
- `socratic-discuss` — 苏格拉底讨论
- `skill-review` — 技能审查
- `postmortem-note` — 复盘笔记

## 许可

MIT
