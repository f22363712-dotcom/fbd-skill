# FBD Skill Collection

A curated set of [Claude Code](https://claude.ai/code) skills that turn probabilistic AI into reliable, auditable workflows.

> 👉 [中文版说明 →](docs/README_CN.md)

## Overview

This repository follows a **Router → Executor** two-layer architecture:

```
project-compass (Router) — identifies the stage and routes to the right skill
    │
    ├── sop-creator        — state-machine SOP generator
    ├── actor-reader       — structured deep reading (ACTOR framework)
    ├── socratic-discuss   — Socratic discussion partner
    ├── skill-review       — 8-dimension skill quality auditor
    ├── postmortem-note    — structured postmortem notes
    ├── repo-steward       — evidence-led repository reflection and dissent
    └── ...                — routes to external skills (grill-me, tdd, diagnose, etc.)
```

## Skills

| Skill | Description |
|-------|-------------|
| [project-compass](project-compass/SKILL.md) | Project navigator — routes to the right next skill for your current stage |
| [sop-creator](sop-creator/SKILL.md) | Deterministic state-machine SOP generator — turns probabilistic AI into reliable automation pipelines |
| [actor-reader](actor-reader/SKILL.md) | ACTOR 5-step reading framework — your AI reading coach for deep internalization |
| [socratic-discuss](socratic-discuss/SKILL.md) | Socratic discussion companion — structured dialogue for deeper understanding |
| [skill-review](skill-review/SKILL.md) | Meta-skill auditor — evaluates skills across 8 dimensions with scored reports |
| [postmortem-note](postmortem-note/SKILL.md) | Structured postmortem notes — turns non-trivial fixes into searchable knowledge |
| [repo-steward](repo-steward/SKILL.md) | Quiet repository steward — reconstructs decisions, surfaces contradictions, and asks only decision-changing questions |

## Installation

Clone the repository anywhere, then run the installer. It places each bundled skill at Claude Code's expected `~/.claude/skills/<skill-name>/SKILL.md` path.

```bash
git clone https://github.com/f22363712-dotcom/fbd-skill.git
cd fbd-skill
python scripts/install_skills.py
```

Re-run with `--update` after pulling changes:

```bash
git pull
python scripts/install_skills.py --update
```

On Windows (PowerShell):

```powershell
git clone https://github.com/f22363712-dotcom/fbd-skill.git
Set-Location .\fbd-skill
python .\scripts\install_skills.py
```

Install only the two navigation and repository-review skills:

```bash
python scripts/install_skills.py --skills project-compass,repo-steward
```

`project-compass` contains routes to 15 external skills that are not bundled here. When a target is unavailable it reports the missing dependency and offers a fallback; see [skill_catalog.json](skill_catalog.json) for the exact split.

## Usage

Invoke skills via slash commands in Claude Code:

- `/project-compass` — navigate to the right skill
- `/sop-creator` — generate an SOP workflow
- `/actor-reader` — start ACTOR reading framework
- `/socratic-discuss` — start a Socratic discussion
- `/skill-review` — review a skill's quality
- `/postmortem-note` — write a postmortem after a complex fix
- `/repo-steward` — review repository history, evidence, and stop/continue signals

## Project Structure

```
fbd-skill/
├── skill_catalog.json         # bundled skills and external route targets
├── scripts/                   # collection installer and validator
├── tests/                     # catalog and installer checks
├── docs/
│   └── README_CN.md           # Chinese documentation
├── sop-creator/
│   ├── SKILL.md
│   ├── scripts/
│   ├── assets/
│   └── references/
├── project-compass/           # Router skill
│   └── SKILL.md
├── actor-reader/              # ACTOR reading framework
│   ├── SKILL.md
│   └── references/
├── socratic-discuss/          # Socratic discussion
│   ├── SKILL.md
│   └── references/
├── skill-review/              # Meta-skill auditor
│   ├── SKILL.md
│   └── RUBRIC.md
├── postmortem-note/           # Postmortem note generator
│   ├── SKILL.md
│   └── TEMPLATE.md
├── repo-steward/              # Evidence-led repository reflection
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── references/evidence-cards.md
├── README.md                  # This file (English)
└── ARCHITECTURE.md            # Architecture documentation
```

## Borrow the Architecture, Not Just the Skills

The **real value** of this repository is the **router → executor architecture** and the skill design patterns, not an exhaustive collection you must install fully.

`project-compass` routes to many downstream skills. Seven skills live in this repository and 15 route targets are external. You can:

- **Bundled install** — install the seven included skills with the repository installer
- **Selective borrowing** — adopt the architecture but swap in your own skills
- **Custom routing** — edit `project-compass/SKILL.md` to keep only the routes you need

Skills included in this repo: `project-compass`, `sop-creator`, `actor-reader`, `socratic-discuss`, `skill-review`, `postmortem-note`, `repo-steward`.

## License

[MIT](LICENSE)
