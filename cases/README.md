# Cases

Not published: the real cases include screenshots and copied READMEs of other people's work, and
`expected.jsonl` refers to one person's setup. Build your own, one folder per case:

    cases/<id>/            post text, screenshots, README/SKILL.md snapshots, notes
    cases/expected.jsonl   one JSON object per line:
      {"id": "x1", "tags": ["skill"], "verdict_ok": ["skip"],
       "must_flag": ["a point a good review must make"], "must_not": ["something it must not do"]}

`verdict_ok` is the list of verdicts you'd accept (adopt / trial / skip). Write `must_flag` items as
checkable statements about your own setup and the case files.
