# Post reviewer hill-climb (2026-09-29)

Reviewer: Claude Sonnet 5.5 via `claude -p`, isolated from user config, Read/Glob only, no web. Judge: Claude Opus 5.5. 13 real cases (6 skips from today's reviews, 7 tools the user adopted), whole set scored every round; results are directional, not a publishable number.

| Round | Change | Flag recall | Verdict OK | Clean | Kept |
|---|---|---|---|---|---|
| baseline | v0 prompt | 0.88 | 0.62 | 0.65 | - |
| 1 | Verdict criteria: decide by adoption cost and whether the premise holds, not proven benefit | 0.94 | 0.96 | 0.54 | yes |
| 2 | Fact-stating rules: restate only what a file or profile line says, keep qualifiers, "the files don't say" | 0.87 | 0.96 | 0.88 | yes (recall -0.06, borderline) |
| 3 | Guide's "Think the problem through before you answer." | +0.02 | 0 | 0 | no (flat) |
| 4 | Effort medium | +0.03 | 0 | 0 | yes, cheapest ($0.034/case vs $0.046) |
| 5 | Effort high | +0.02 | +0.08 | 0 | no (slower, $0.061/case) |

Rounds 1-2 ran 2 reps; 3-5 ran 1 rep (budget) and compare against round 2's rep 0.

Winner: `prompts/v2.md` at effort medium. Stopped on plateau (three flat rounds).
