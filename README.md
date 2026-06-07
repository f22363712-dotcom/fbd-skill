# FBD Skill 集合

Claude Code 技能（Skill）集合仓库，包含一系列增强 Claude Code 能力的专用工具包。

## 技能清单

| 技能 | 说明 |
|------|------|
| [sop-creator](skill.md) | 确定性状态机 SOP 生成器 — 将概率性 AI 转化为可靠的自动化流水线 |
| [actor-reader](actor-reader/SKILL.md) | ACTOR 五步阅读框架 — 将 AI 作为阅读教练，深度内化书籍与长文 |
| [socratic-discuss](socratic-discuss/SKILL.md) | 苏格拉底式讨论伴侣 — 通过结构化对话帮助深度内化知识 |

## 安装

将本仓库克隆到 Claude Code 的 skills 目录：

```bash
# 进入 Claude Code skills 目录
cd ~/.claude/skills

# 克隆仓库
git clone https://github.com/f22363712-dotcom/fbd-skill.git

# 或使用符号链接（推荐，方便更新）
ln -s /path/to/fbd-skill/* .
```

## 使用

在 Claude Code 中通过斜杠命令调用各技能：

- `/sop-creator` — 生成 SOP 工作流
- `/actor-reader` — 启动 ACTOR 阅读框架
- `/socratic-discuss` — 启动苏格拉底式讨论

## 项目结构

```
fbd-skill/
├── skill.md                   # sop-creator 核心定义
├── scripts/                   # sop-creator 验证脚本
├── assets/                    # sop-creator 模板资源
├── actor-reader/              # ACTOR 阅读框架
│   ├── SKILL.md
│   └── references/
├── socratic-discuss/          # 苏格拉底讨论伴侣
│   ├── SKILL.md
│   └── references/
├── README.md
├── ARCHITECTURE.md
└── CLAUDE.md
```

## 许可

MIT
