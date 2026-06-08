---
name: skill-review
description: Evaluate a Claude Code skill's quality across 7 dimensions: trigger precision, progressive disclosure, negative space, output contract, environment independence, failure modes, and composability. Produces a scored report with actionable improvements. Use when the user wants to review, audit, or improve a skill — "/skill-review my-skill", "审查这个skill", "这个skill有什么问题", "帮我改进这个skill".
---

# Skill Review — 元技能审查器

审查任何 Claude Code skill 的质量，输出评分报告 + 具体改进建议。

## 工作流

### 1. 定位目标 skill

用户必须指定一个 skill 名称或路径：
- 如果是名称（如 `postmortem-note`），去 `~/.claude/skills/<name>/` 和 `.claude/skills/<name>/` 找
- 如果是路径，直接使用

### 2. 收集材料

读取以下文件（如果存在）：
- `SKILL.md`（必须）
- 所有被 SKILL.md 引用的配套文件（TEMPLATE.md, REFERENCE.md, EXAMPLES.md 等）
- `scripts/` 下的脚本

### 3. 七维评分

每个维度 1-5 分。使用 [RUBRIC.md](RUBRIC.md) 中定义的锚定描述符评分。

**维度一览**：

| # | 维度 | 核心问题 | 权重 |
|---|------|---------|------|
| D1 | 触发精度 | description 够不够准确？会不会被误触发或漏触发？ | 1.5x |
| D2 | 渐进披露 | 主文件是否 <100 行？引用是否合理外置？ | 1.0x |
| D3 | 负空间 | 有没有定义"不做什么"？有没有边界？ | 1.0x |
| D4 | 输出契约 | 每步有没有可验证的产物？用户能不能判断"完成了"？ | 1.0x |
| D5 | 环境独立 | 有没有硬编码路径？能否在别人的机器上工作？ | 0.5x |
| D6 | 失败模式 | 出错了会怎样？有没有覆盖同名文件、空输入等边界？ | 1.0x |
| D7 | 组合性 | 能不能被其他 skill 调用？有没有清晰的 I/O 边界？ | 0.5x |

### 4. 综合评分

```
总分 = (D1×1.5 + D2×1.0 + D3×1.0 + D4×1.0 + D5×0.5 + D6×1.0 + D7×0.5) / 6.5 × 20
```

> 满分 100。权重反映该维度对 skill 可复用性的相对重要性。

评级：
- 85-100：🟢 生产级，可公开发布
- 70-84：🟡 可用，有改进空间
- 50-69：🟠 需重视，关键维度有缺口
- <50：🔴 不建议使用，需重构

### 5. 输出报告

严格使用以下结构。**规则**：
- 评分必须有理由（引用文件中的具体内容）
- 改进建议必须可执行（不是"建议优化"，而是"把第 X 行的 X 改为 X"）
- 报告末尾给出 TOP 3 优先修复项

```markdown
# Skill Review: [skill-name]

**审查时间**: [date]
**SKILL.md 行数**: [N]
**总分**: [XX/100] [评级]

---

## 各维度评分

| 维度 | 得分 | 权重 | 加权 |
|------|------|------|------|
| D1 触发精度 | N/5 | 1.5x | N |
| D2 渐进披露 | N/5 | 1.0x | N |
| D3 负空间 | N/5 | 1.0x | N |
| D4 输出契约 | N/5 | 1.0x | N |
| D5 环境独立 | N/5 | 0.5x | N |
| D6 失败模式 | N/5 | 1.0x | N |
| D7 组合性 | N/5 | 0.5x | N |

## 诊断

### D1 触发精度 — [得分]/5

**证据**: [引用 description 原文或具体行为]
**分析**: [为什么给这个分]
**改进**:
- [ ] [具体可执行的修改建议]

> 每个 D2-D7 重复同一结构

## TOP 3 优先修复

1. **[维度名称]** — [一句话说清问题和修复]（预估影响：+N 分）
2. ...
3. ...

## 一句话总结

[用一句话评价这个 skill 的最大优点和最大弱点]
```

### 6. 询问是否执行改进

报告输出后，问用户：**"是否要我现在执行 TOP 3 修复？"**

只有用户明确同意后才 Edit 目标 skill 的文件。
