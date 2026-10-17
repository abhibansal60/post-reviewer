---
name: post-reviewer
description: Review a tool, skill, plugin, repo, prompt or social post the user is thinking of adopting and say whether it is signal or noise for their setup (adopt / trial / skip), with each claim checked against the files. Use when the user pastes or links a post, README or screenshot and asks "should I use/install this", "is this worth it", "signal or noise", "review this", or "what about this".
---

# Post reviewer

A second opinion on whether to adopt something, judged against the user's own setup profile. It runs as a subagent so the long README and screenshots stay out of the main conversation.

The reviewer prompt and the setup profile live in the post-reviewer repo (call it `$PR`): `$PR/prompts/v2.md` and `$PR/profile.md`. `$PR` is the first of these that contains `prompts/v2.md`: `$POST_REVIEWER_DIR`, two levels above this skill's real path (`realpath <skill dir>/../..`, which works when the skill is a symlink into a clone), then `~/code/post-reviewer`. If none does, ask the user where they cloned it. Read them by path; don't copy their text into this skill.

## Steps

1. **Check the profile exists.** If `$PR/profile.md` is missing, tell the user to copy `$PR/profile.example.md` to `profile.md` and fill it in, then stop. If the user says their setup changed (new hardware, plan, keys), offer to update `profile.md` first.

2. **Build a case folder** at `<scratchpad or /tmp>/post-reviewer/<short-slug>/` with everything the user is reacting to:
   - The post or question as `post.md` (verbatim; note who wrote it if known).
   - Screenshots and images: copy the saved files in as they are.
   - For a GitHub repo or skill: its README (`gh api repos/OWNER/REPO/readme -H "Accept: application/vnd.github.raw" > README.md`) and, for a skill, its `SKILL.md`. Add the license and star/push dates only if the repo page gives them (`gh repo view`).
   - For other links: fetch the page and save the text.
   Never fill anything in from memory. If a page or README can't be read, say so, and pass on what you have; the reviewer will mark those claims unverifiable.

3. **Spawn one subagent** (Agent tool, `subagent_type: general-purpose`, `model: sonnet`) with this prompt, filling in the paths:
   > Follow the reviewer instructions in `<PR>/prompts/v2.md` exactly. The user's setup is in `<PR>/profile.md`. The case directory is `<case dir>`. Read the profile and every file in the case directory, including images. Don't use the web or run anything. Return the review in the format the instructions ask for.

4. **Show the result** verdict first, then the claims table, fit, what's worth keeping, and the summary, in plain language. Don't change the reviewer's verdict. Add one line: it's a second opinion, and `skip` doesn't stop the user from trying something small if they still want to.

5. **If the user disagrees**, ask why in one line and offer to save the case (`cases/<id>/` plus an `expected.jsonl` line) so the reviewer can be re-tuned later. Don't save it without asking.

## Notes

- Tuned and tested with `claude -p` in isolation (`$PR/review.sh`), which sees none of the user's settings. Run as a subagent it also sees the user's normal context, so results can differ slightly. `$PR/review.sh <case dir>` is the exact tested path if needed.
- It has no web access on purpose: everything it says should trace to a file in the case folder or a line in the profile.
