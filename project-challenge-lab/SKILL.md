---
name: project-challenge-lab
description: Challenge a project direction with repository evidence, compare methods or concepts through a controlled baseline, decompose the winning result into a safe first slice, and personalize it to the user. Use when the user asks to question a project, test whether a skill or approach actually helps, compare concepts before implementation, or establish an experiment-first project workflow. Do not use for ordinary implementation, simple reviews, or open-ended ideation without a decision to test.
---

# Project Challenge Lab

Turn a disputed project choice into an auditable decision and a small, personalized action. Preserve the user's scope and existing work.

## Establish the decision

Write down the decision under test, the baseline, the candidate intervention, and the observable result that would authorize action. Separate these questions:

- Does the project still solve a distinct problem?
- Does the proposed method improve the work?
- Which first slice is worth implementing now?

Do not let a broad project critique silently become permission to redesign or edit the project.

## Build an evidence packet

Inspect the minimum artifacts that can answer the decision. Prefer product truth, source files, current screenshots, tests, and documented constraints. Exclude dependency caches, build output, generated files, and unrelated history unless a claim depends on them. Record the allowed evidence set before dispatching parallel work.

Capture the current observable baseline before edits. Run existing checks when they are safe and relevant.

## Run a controlled comparison

Use a no-method baseline whenever the question is whether a skill, prompt, or workflow adds value. Keep the task, evidence packet, model, and output contract fixed across variants. Change one factor at a time.

Randomize anonymous labels. Participants must not see the label mapping, other reports, or the intended winner. The independent judge must not read the mapping or method sources.

Read [references/evaluation-rubric.md](references/evaluation-rubric.md) when scoring product, design, or implementation proposals. Adapt dimensions only before the reports are generated, never after seeing results.

When multiple agents are unavailable or not authorized, run the variants sequentially in isolated contexts and disclose the weaker independence.

## Challenge before personalizing

For each candidate, look for duplicated existing capability, contradictions with the product definition, hidden state or data errors, user effort, privacy changes, and unsupported dependencies. Reject proposals that win through presentation while weakening correctness.

Personalization must come from observed user behavior, explicit preferences, project constraints, or prior accepted decisions. Label generic best practice as generic. Do not invent a persona to make a direction feel distinctive.

## Decide and act

Predeclare the significance rule. For a 35-point rubric, default to a lead of at least 6 points across at least three dimensions. A single run is directional evidence, not population-level proof.

- If the intervention clears the rule and the user authorized implementation, apply only the first reversible vertical slice and verify it.
- If scores are close, do not install, rewrite, or implement merely because a candidate ranked first. Extract any isolated finding that is independently supported.
- If the baseline wins, keep the baseline and identify the narrow instruction the tested method lacked.

The first slice should repair one user-visible path with explicit acceptance checks. Defer adjacent polish, persistence, and new dependencies unless the tested decision requires them.

## Preserve the experiment

Keep a compact record containing the protocol, anonymous outputs, private mapping, judge report, result, failures, and any before-and-after evidence. Record startup stalls, scope corrections, or contaminated runs instead of hiding them.

At handoff, state what changed, what did not change, how strong the evidence is, and the next experiment that could overturn the decision.
