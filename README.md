# Bone Room

A run of short mysteries you solve in the terminal. You read a case, reveal clues one at
a time, and try to name the culprit in three tries or fewer. Solve it and the next case
starts straight away. No download or extra packages are needed to play, only Python 3.13.

## Play

```powershell
py -3.13 -m bone_room
```

At the `>` prompt:

| Input | What it does |
|-------|--------------|
| `c` | Reveal the next clue (free, doesn't use a try) |
| `s` | Show the suspect list again |
| `q` | Quit the run and reveal the culprit |
| a number or name, e.g. `2` or `clara osei` | Guess the culprit |

You have 3 tries per case. A guess that isn't a suspect, or one you've already ruled out,
doesn't count.

## The run

There are 7 cases, always in the same order, from a missing heirloom to a murder on a
night train. Each case opens with a counter and its severity:

```
Case 2 of 7 · Poisoning · Severity: Serious
=== Tea at the Lighthouse ===
```

Later cases are harder: more suspects, more clues, and some clues that point at the wrong
person (red herrings). Every case can still be solved from its clues.

Each case gives you 3 fresh tries. Three wrong guesses on any case end the run, and the
game tells you how many cases you solved. Solve all 7 to complete the run.

## Test

One-time setup:

```powershell
py -3.13 -m venv .venv
.venv\Scripts\python -m pip install -r requirements-dev.txt
```

Run the tests:

```powershell
.venv\Scripts\python -m pytest
```

Each test name and docstring says which requirement (R1–R8 in [problem.md](problem.md))
it checks. The full behaviour is in [spec.md](spec.md).
