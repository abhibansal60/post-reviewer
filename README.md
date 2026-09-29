# post-reviewer

Paste in a tweet, README or prompt about some tool, and get a signal-vs-noise verdict for *your* setup:
`adopt`, `trial` or `skip`, with each claim marked supported / unsupported / contradicted / unverifiable
against the files you gave it, and reasons tied to a profile of your own setup.

It is one system prompt (`prompts/v2.md`), run through headless Claude Code (`claude -p`) with no web access
and none of your settings, hooks or memory (`--setting-sources ""`), plus the eval that tuned it.

## Use

    cp profile.example.md profile.md      # fill in your own setup
    mkdir case && cp post.md README.md screenshot.png case/
    ./review.sh case

Needs Claude Code. Runs on Sonnet 5.5 at medium effort, about $0.03 at list price per review.

## As a Claude Code skill

`skill/post-reviewer/SKILL.md` wraps this as a skill that gathers the post and READMEs into a case folder and runs
the review in a subagent, so the long files stay out of your conversation:

    ln -s "$PWD/skill/post-reviewer" ~/.claude/skills/post-reviewer

Then ask "is this worth it?" with a post, link or screenshot. The eval below tested `claude -p` in isolation; the
subagent also sees your normal context, so results can differ slightly (`./review.sh` is the exact tested path).

## How the prompt was tuned

13 real cases: 6 posts that should be skipped and 7 tools their owner had adopted. Sonnet 5.5 reviews each
case; Opus 5.5 grades the review against the points a good review must make, flags invented facts, and checks
the verdict. Three metrics: flag recall, verdict OK, clean (no invented facts). Whole set scored every round,
so read the numbers as directional, not a benchmark.

| Round | Change | Flag recall | Verdict OK | Clean |
|---|---|---|---|---|
| baseline | first prompt | 0.88 | 0.62 | 0.65 |
| 1 | decide by adoption cost and whether the core idea holds, not by proven benefit | 0.94 | 0.96 | 0.54 |
| 2 | state only what a file or the profile says; write "the files don't say" for gaps | 0.87 | 0.96 | 0.88 |
| 3 | add "Think the problem through before you answer." ([Sonnet 5.5 prompting guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5)) | flat | flat | flat |
| 4-5 | effort medium / high | flat | flat / +0.08 | flat |

Kept: `prompts/v2.md` at medium effort. See `results/narrative.md`. Rounds 1-2 ran 2 reps per case, rounds 3-5 one.
With 13 cases, differences under about 0.1 are noise.

## Files

- `skill/post-reviewer/SKILL.md`: the Claude Code skill.
- `prompts/v0-v3.md`: each version of the system prompt.
- `judge.md`: the grader's instructions.
- `eval-fill.mjs`: the app-specific part of the eval runner. Paste it over the "fill these in" block of the runner
  scaffold that ships with Anthropic's `claude-api` skill (`/claude-api build-eval`); the scaffold is not redistributed here.
- `score.py`: per-case table, means with 95% intervals, and rep noise from a results folder.
- `cases/README.md`: how to build your own cases. The real cases are not published (they contain other people's
  screenshots and READMEs, and one person's setup).
