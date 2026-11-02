# Working on this with the study group

## Ground rules

This is a **revision** repo. Everything in it is for practice before the
exam, not during it. The papers both state that collusion is not permitted
and that generative AI is not allowed in the exam itself (AI category 1) —
none of which restricts what you do while revising, which is what this is.

One thing worth keeping to anyway: **do not commit your mock attempts.**
`mocks/attempts/` is gitignored for that reason. Sitting a paper is only
useful if you have not seen someone else's answers to it first.

## Getting set up

```bash
git clone <the repo url>
cd pphr-capstone
make setup
make drill WEEK=1
```

`make setup` builds a virtualenv in `.venv/` and installs the package in
editable mode, so `import capstone` works from a notebook in any directory.

## The weekly rhythm

After each lecture, whoever is on rota does two things:

1. **Add drills for the new topic.** Function stubs in
   `drills/weekNN_topic.py`, reference answers in `solutions/`, tests in
   `tests/test_weekNN.py`. Keep the three in step.
2. **Extend the capstone.** Add a section to `capstone/report.ipynb` applying
   the new topic to the sepsis data.

Everyone else pulls and attempts the new drills before the next session.

## Writing a good drill

The stub is the spec, so put the detail in the docstring — inputs, output
shape, edge cases, and a worked example. Then the test checks exactly what
the docstring promised. If someone has to guess what you meant, the drill is
not finished.

Three things make a drill worth having:

- **Test the edge case, not just the happy path.** Empty input, a zero
  denominator, a missing value, a boundary exactly on a threshold. That is
  where the exam marks hide, and where your own code will break.
- **Make it deterministic.** Anything involving randomness takes an `rng`
  parameter (a `random.Random` instance), so the test can pin the seed.
- **Check it against the reference.** `make verify` runs the whole suite
  against `solutions/`. It must be green. If it is not, the test is wrong,
  which is worth knowing before five people lose an evening to it.

```bash
make verify            # tests vs solutions/ - should always pass
make drills            # tests vs drills/ - your actual progress
make progress          # the summary table
```

## Notebooks in git

Executed notebooks produce large, conflict-prone diffs. Two conventions:

- `capstone/report.ipynb` keeps its outputs — it is a report, and the
  findings are the point. Coordinate before editing it, or expect to resolve
  conflicts by hand.
- Blank papers in `mocks/` stay blank. Never commit one with answers in it.

## Marking each other

`pytest` cannot grade the half of the paper that carries the written marks —
the comments, the findings paragraphs, the discussion of limitations. So
after a mock, swap papers and mark those by hand against
`reference/syllabus_map.md`. In both past papers, questions worth 10 or 15
marks end by asking you to describe or discuss something, and that is
reliably where people lose marks they could have had.
