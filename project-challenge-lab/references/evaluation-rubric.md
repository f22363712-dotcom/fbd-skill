# Evaluation rubric

Use seven dimensions scored from 0 to 5. A 3 means usable but incomplete. A 5 requires direct evidence and an implementable consequence.

| Dimension | 0 | 3 | 5 |
|---|---|---|---|
| Scope fit | Solves a different problem | Mostly in scope with some drift | Preserves the exact decision and boundaries |
| Evidence specificity | Unsupported opinion | Refers to artifacts without tracing consequences | Connects visible or coded evidence to user impact |
| Product correctness | Contradicts product truth | Mostly correct with an unresolved assumption | Preserves definitions, data lineage, and limitations |
| Personalization | Invented persona or generic style | Uses one real preference | Derives a coherent direction from several observed constraints |
| State coverage | Happy path only | Covers main success and one failure | Covers entry, success, failure, recovery, and repeated use |
| Implementation safety | Expands data, dependencies, or permissions silently | Feasible but leaves one lifecycle risk | Reversible, bounded, and explicit about data and dependencies |
| Priority and actionability | Vague wishlist | Ordered recommendations | One narrow first slice with observable acceptance checks |

Reject a proposal regardless of score when it invents domain claims, changes a protected product definition, adds a dependency without inspecting the existing stack, hides a new data lifecycle, or proposes decoration without a task reason.

Before judging, add domain-specific anchors. Examples include medical claim boundaries, local-data retention, Android permission truth, or financial calculation definitions. Do not add anchors after unblinding.
