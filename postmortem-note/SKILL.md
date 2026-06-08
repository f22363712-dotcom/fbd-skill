---
name: postmortem-note
description: After a non-trivial bug fix, debugging session, or config issue, generates a structured postmortem note in the user's knowledge base for future reference ("以史为鉴"). Use when the user says "沉淀文档", "记录这次修复", "写个复盘", "/postmortem", or after a multi-step debugging session wraps up.
---

# Postmortem Note — 故障修复复盘笔记

> 将每一次非平凡的修复转化为可检索、可复用的知识资产。

## 触发条件

以下情况**应该**写复盘笔记：
- 修复涉及 ≥2 个配置层 / 文件的联动
- 根因不直观，排查路径值得记录
- 涉及工具/框架的隐藏行为（如配置加载顺序、版本差异）
- 修复过程走了弯路，有"以史为鉴"的方法论价值

以下情况**不必**写：
- 单行拼写错误
- 一眼可见的语法修复
- 无通用性的环境特殊问题

## 与其他 Skill 的连接

- **`diagnose` → 本 skill**：当 `diagnose` 完成一次复杂修复后，主动问用户"要不要写个复盘笔记？"然后调用本 skill
- **本 skill → 知识库**：生成的笔记自动挂载 `related` 字段，指向相关的技术文档/项目笔记

## 工作流

### 1. 收集素材

从当前会话中提取：
- **错误演进史**：原始报错 → 每次修改后的新报错（按时间线）
- **排查路径**：用了哪些检查命令、读了哪些文件、排除了哪些假设
- **根因**：最终确认的问题源头
- **修复步骤**：实际生效的修改（不是"尝试过但无效的"）

如果会话较长，请用户确认收集范围（"只记录最近 N 轮的修复"）。

### 2. 确认目录

询问用户保存到哪个目录。如用户未指定：
- 在当前 vault 中，建议 `10_Projects/AI工程笔记/CC使用笔记/`
- 在其他项目中，建议 `docs/postmortems/` 或当前工作目录
- **不要假设路径**——用户的 vault/项目结构不同

### 3. 按模板生成

严格使用 [TEMPLATE.md](TEMPLATE.md) 的结构。
确保：
- YAML frontmatter 有 `tags` 和 `related` 双向链接
- 根因章节不超 3 句话
- 每个修改都有"为什么"列
- "核心教训"用具体规则而非泛泛而谈

### 4. 用户确认后写入

⛔ **写入前必须让用户审阅**：
1. 在对话中展示完整笔记内容
2. 等用户确认或修改
3. 用户说"可以写"或"保存"后再 Write
4. 写入后告知文件路径（wiki-link 格式）

**边界处理**：
- 如果目标文件已存在 → 询问"同名文件已存在，覆盖 / 追加 / 取消？"
- 如果用户中断确认（Ctrl+C）→ 不写入，直接退出
- 如果内容提取不完整（会话太短、无排查路径）→ 告知用户"缺少素材，建议手动提供关键信息"
