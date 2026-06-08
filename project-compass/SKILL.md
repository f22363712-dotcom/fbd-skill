---
name: project-compass
description: Routes any project to the right next workflow: clarification, documented alignment, TDD implementation, PRD synthesis, debugging, prototyping, code review, deep reading, or Socratic discussion. Never limits routing to student/coursework contexts.
---

# Project Compass

## Purpose

Act as a thin router. Do not replace the downstream skills — hand off as soon as the route is clear.

Identify the user's current stage, then route them to the best next skill. Works for any project: personal, course, work, open-source, professional, production, research, or exploratory.

Do not use the user's identity, role, seniority, or learning status as an applicability filter. If memory says the user is a student, use that only to tune explanation style, not to classify the project as coursework or reject work/professional contexts.

Keep responses brief and practical. Prefer Chinese when the user is speaking Chinese.

## Workflow

### 1. Identify the stage

Ask at most three short questions if the route is not obvious:

- What do you need right now: clarify, implement/fix, debug, review, produce a document, or read/discuss/learn?
- Is there already a repo or codebase? (skip if the request is reading/learning-related)
- Is this a one-shot task or an ongoing project?

If the route is already obvious from the user's message, skip questions. Do not ask whether the project is a student project unless the user specifically mentions coursework, class deliverables, teachers, grades, or campus constraints.

### 2. Route

Use this decision table:

**Clarify & plan:**
- Vague idea, unclear scope, unsure what to build → `grill-me`
- Ongoing repo, repeated confusion about terms, modules, or decisions → `grill-with-docs`

**Build & fix:**
- Clear feature or bug, wants reliable implementation or test-first flow → `tdd`
- Working idea but wants a quick throwaway implementation to validate → `prototype`
- Has a diff/PR and wants quality review → `code-review` or `review`

**Diagnose & verify:**
- Bug is hard to reproduce, performance regression, or unexpected behavior → `diagnose`
- Wants to confirm a change works by running or observing the app → `verify`

**Document & organize:**
- Needs a requirements doc, project brief, report seed, or structured summary → `to-prd`
- Has a PRD or design and wants structured dev tasks → `to-issues`
- Fixed a complex bug and wants a structured postmortem / 复盘笔记 → `postmortem-note`

**Quality & meta:**
- Wants to audit, review, or improve a Claude Code skill → `skill-review`
- Wants to prioritize / classify issues, bugs, tasks, or risks → `triage`

**Infra & automation:**
- Wants long-running autonomous task execution → `autonomous-agent`
- New or existing repo needs a CLAUDE.md scaffold → `init`
- Needs a repeatable SOP for a multi-step workflow → `sop-creator`

**Refactor & improve:**
- Has working code but architecture or design quality needs improvement → `improve-codebase-architecture`

**Security:**
- Wants a security-focused review of code or design → `security-review`

**Read & internalize:**
- Has material (book/article/video/course) and wants structured deep reading → `actor-reader`
- Has consumed content and wants to discuss, challenge, teach, or connect it → `socratic-discuss`

### 3. Semi-automatic behavior

If the route is clear and low-risk, explain the reason in one sentence and invoke the target skill.

If the route may create persistent files, tracker items, repo changes, or external issue/PR content, pause briefly and explain what will happen before invoking.

If two routes are both plausible, present the top two choices with a one-line tradeoff and let the user choose.

### 4. Target skill not found

If the target skill is not installed, say so briefly and offer alternatives:
> "`[skill-name]` 未安装。要我换一种方式处理，还是先安装它？"

Do not fall through to general conversation silently.

### 5. No-match exit

If the user's intent does not fit any route above, say so briefly and continue the conversation normally. Do not force-fit.

Examples of non-matching requests: tiny one-line edits, asking about tooling unrelated to a project, casual conversation not requiring structured workflow.

## Examples

- "I want to build a lost-and-found app but the features are messy." → `grill-me`
- "Our project already has code, but user/order/item terms keep drifting." → `grill-with-docs`
- "Help me implement login, test first." → `tdd`
- "I have an idea for a CLI tool, can you quickly hack it together?" → `prototype`
- "The API keeps returning 500 after that deploy, I can't figure out why." → `diagnose`
- "Can you check my local changes before I commit?" → `code-review`
- "Can you review PR #123 before I merge?" → `review`
- "The teacher wants a project requirement summary tomorrow." → `to-prd`
- "This production bug keeps coming back after deploys." → `diagnose`
- "Review this auth module for vulnerabilities." → `security-review`
- "I want to deeply read and internalize《政治学通识》." → `actor-reader`
- "我刚看完 ACTOR 框架的视频，帮我讨论和理解它。" → `socratic-discuss`
- "帮我用 ACTOR 框架读这篇论文。" → `actor-reader`
- "我对这个观点不太确定，帮我挑战一下。" → `socratic-discuss`
- "帮我把这次修复沉淀为复盘笔记。" → `postmortem-note`
- "审查一下这个 skill 的质量。" → `skill-review`
- "帮我分类这些 bug 的优先级。" → `triage`
- "帮我写个多步骤的自动化 SOP。" → `sop-creator`
- "这段代码能跑但架构太烂了，帮我重构。" → `improve-codebase-architecture`

## Guardrails

- Do not answer with a long methodology lecture when a clear route exists.
- Do not force setup or scaffolding on tiny or one-shot tasks.
- Do not rewrite the downstream skills; hand off as soon as the route is clear.
- Do not assume the project is student/coursework — treat all projects equally.
- Never reject a route because the project is not a student project.
- Never infer project type from the user's saved profile; infer it only from the current request and visible project context.
