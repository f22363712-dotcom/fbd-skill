---
name: human-elite-english
description: "Writes and audits English social posts, replies, threads, articles, and professional copy so they sound like a knowledgeable human speaking to peers: specific, evidence-led, restrained, and free of academic, corporate, or model-generated posture. Use when drafting, revising, or testing English X, LinkedIn, blog, product, finance, or research copy for human voice, elite judgment, and publish readiness."
---

# Human Elite English

Write like a well-informed person joining a real conversation. "Human" means the copy has a specific subject, a visible reason for speaking, natural progression, and honest limits. "Elite" means selective judgment, precise terms, and calm restraint. It never means status display, inflated certainty, or dense jargon.

## Workflow

1. Identify the mode: `reply`, `post`, `thread`, or `article`.
2. Establish the speaker position internally:
   - What exact claim, question, event, or reader problem prompted this?
   - What does the speaker know, infer, and still not know?
   - What single useful judgment should remain after reading?
3. Check the material gate. Real-world claims need supplied or verifiable evidence. Never invent experience, quotes, figures, sources, or scene details.
4. Draft once for meaning. Respond to the specific subject early, use ordinary verbs, and add one useful fact, distinction, mechanism, or question at a time.
5. Run the nine-gate style TDD in [references/tdd-rubric.md](references/tdd-rubric.md). Treat the first draft as RED. Any failed gate requires revision and a complete rerun.
6. Save the draft as UTF-8 text and run:

   `python scripts/check_english.py <draft-file> --mode <reply|post|thread|article>`

   Add `--history <recent-copy-file>` when recent posts are available. The script reports deterministic problems; it never rewrites copy and does not replace the semantic gates.
7. Deliver only after all nine gates pass and the script has no failures. For an approval workflow, include the TDD report rather than hiding it.

## Mode contracts

- `reply`: normally 80–280 characters; one main point; respond to the author before adding analysis; use no more than two unexplained specialist terms; an answerable question is welcome when it moves the discussion.
- `post`: the first 280 characters must stand alone; open on the claim or observation, not a generic hook; one post should solve one reader problem.
- `thread`: each post must add a distinct fact, reason, example, or consequence; do not split one paragraph mechanically.
- `article`: list at least five concrete materials and their sources before drafting more than 1,200 words; if the material is thin, research or write shorter.

## Voice constraints

- Prefer clear nouns and active verbs. Vary sentence length without performing informality.
- Distinguish fact, calculation, inference, and unknown. Put limits near the claim they qualify.
- Use technical language only when it improves precision. Explain, replace, or remove terms that merely signal expertise.
- Use contractions and first person only when natural. Do not manufacture slang, praise, intimacy, or personal experience.
- Avoid correction-first templates, mini research notes, management language, motivational endings, and repeated stock openers.
- Read aloud. If it sounds like a memo pasted into a conversation, revise.

## Output contract

When the user requests an audit or an approval packet, return:

```text
mode: <mode>
style_tdd: PASS | FAIL
gates: T1 PASS ... T9 PASS
script: PASS | FAIL
failures: <none or concise reasons>
final_copy: <text only when PASS, unless the user asked to inspect a failed draft>
```

See [EXAMPLES.md](EXAMPLES.md) for calibration. This skill may improve wording and test readiness. It never verifies financial facts by itself, gives investment advice, or authorizes publication.
