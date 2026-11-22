# Bone Room

A short murder mystery you solve in the terminal. Each run picks one of three cases. You
read the case, reveal clues one at a time, and try to name the killer in three tries or
fewer. No download or extra packages are needed to play, only Python 3.13.

## Play

```powershell
py -3.13 -m bone_room
```

At the `>` prompt:

| Input | What it does |
|-------|--------------|
| `c` | Reveal the next clue (free, doesn't use a try) |
| `s` | Show the suspect list again |
| `q` | Quit and reveal the killer |
| a number or name, e.g. `2` or `mara quill` | Guess the killer |

You have 3 tries. A guess that isn't a suspect, or one you've already ruled out, doesn't
count.

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

Each test name and docstring says which requirement (R1–R3 in [problem.md](problem.md))
it checks. The full behaviour is in [spec.md](spec.md).
