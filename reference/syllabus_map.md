# What the exam actually examines

Both past papers follow the same shape: 12 questions, 100 marks, three
hours. They are not the same questions, but they are drawn from the same
small set of archetypes. This table is the union of the two, which is the
best available guess at the syllabus.

| Week | Topic | Jan 2026 | Sep 2025 | Marks seen |
|---:|---|---|---|---:|
| 1 | Lists, dicts, indexing | Q1 list of lists | Q1 nested dict update | 5 |
| 2 | Loops and simulation | Q2 `while` + `random` | Q3 `for` over a dict | 5 |
| 3 | Conditionals, decision trees | Q3 flow diagram | — | 10 |
| 4 | Strings, f-strings, dates | — | Q2 `datetime`, Q3 f-strings | 5–10 |
| 5 | Functions, docstrings, errors | Q5 document a function | Q7 fix a function, Q9 error handling | 5–10 |
| 6 | Regex on free text | Q6 extract weeks | Q10 classify diet text | 10–15 |
| 7 | Classes | Q7 add a method | Q5 drive the branches | 5 |
| 8 | Selecting from a DataFrame | Q4 three ways to a cell | Q6 build a frame from a table | 5 |
| 9 | Reading files, sorting | Q8 CSV, top 3 | Q8 **zipped** CSV | 5–10 |
| 10 | Grouping, binning | Q10 boolean flag + means | Q11 age bands + means | 10 |
| 11 | Merging, cross-tabulating | Q11 merge + crosstab | Q4 merge + proportions | 10–15 |
| 12 | Plotting | Q9 scatter + describe | Q12 three variables on one figure | 10–15 |
| 13 | Features, logistic regression | Q12 GLM binomial | Q12 derive a feature | 15 |

## What the mark scheme rewards

Reading both papers' instructions together, several things are stated
explicitly and are easy marks:

- **Comment every step.** Both papers ask for it in the instructions.
- **Do not hard-code values.** Both papers say so outright, with an example.
  Define `icd = "F20"` and use the variable.
- **Write prose, not just code.** Questions worth 10–15 marks almost always
  end with "describe your findings" or "discuss". A correct figure with no
  interpretation drops a large fraction of the marks available.
- **Tables and figures are the deliverable.** "Produce a detailed report
  using a combination of code, text, figures, and tables."
- **Error handling earns extra marks** where offered (Sep 2025 Q9 says so).
- **No shell commands.** This is why the zipped CSV in Sep 2025 Q8 has to be
  opened from Python — `pd.read_csv(path, compression="zip")`.

## Traps actually present in the papers

- **Jan 2026 Q5 has a typo.** The expected output is printed as
  `{23: 5, 33: 4, 43: 2, 53: 1, 63: 1}`, but only three of the five ages
  (45, 35, 67) are ≥ 33, and the paper's own starter code returns
  `{33: 3}`. If a stated output contradicts the given code, say so in a
  comment and go with the code.
- **Sep 2025 Q10's labels are internally inconsistent.** One participant
  describing themselves as "mostly vegan but sometimes I eat meat" is
  labelled Omnivore, while "I see myself as vegan but I do eat meat
  sometimes" is labelled Vegan. No rule gets both right. Report the
  disagreement rather than fitting to the labels.
- **Sep 2025 Q11's bands are inclusive at both ends** ("35 - 54 years"), so
  `pd.cut` needs its edges offset accordingly. Off-by-one here is silent.
- **GLM, not Logit.** Jan 2026 Q12 names
  `sm.GLM(..., family=sm.families.Binomial())`. Both fit a logistic
  regression; use the one the paper asks for, and remember
  `sm.add_constant`.
- **Units.** Heights are in centimetres in `health_info.csv`. A BMI of 0.002
  means you forgot to divide by 100.

## Timing

Three hours, 100 marks — roughly 1.7 minutes per mark. The last two
questions are worth 30 marks between them, so reaching Q11 with less than
40 minutes left is the main way to lose marks you could have earned. The
`make mock` timer prints the checkpoints.
