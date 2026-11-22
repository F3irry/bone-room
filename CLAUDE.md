# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Project
Bone Room is a short terminal murder-mystery game in Python. `problem.md` holds the
original problem and requirement IDs (R1, R2, ...); `spec.md` holds the agreed behaviour
and design decisions. Read both before changing behaviour.

## Environment
- Windows. Use Python 3.13 through the launcher: `py -3.13`. The `python` on PATH is an
  old 3.8 — never use it.
- Dev dependencies (pytest) live in a local virtual environment `.venv`:
  - Create: `py -3.13 -m venv .venv`
  - Install: `.venv\Scripts\python -m pip install -r requirements-dev.txt`
- The game itself uses only the standard library.

## Commands
- Run the game: `py -3.13 -m bone_room`
- Run tests: `.venv\Scripts\python -m pytest`

## Layout
- `bone_room/cases.py` — case data (`Case`) and `choose_case`
- `bone_room/game.py` — game rules (clues, guesses, win/loss); no input/output here
- `bone_room/cli.py` — terminal loop; reads/writes through injectable functions
- `bone_room/__main__.py` — entry point for `python -m bone_room`
- `tests/` — pytest tests

## Conventions
- Every test names the requirement it checks in its name (`test_r1_...`) and docstring.
  New requirements get new IDs in `problem.md`/`spec.md` before code.
- Keep game logic free of `input`/`print` so it stays testable.
- Small commits; each message says what changed and why.
- Never undo, amend, or force-push commits.
- Git author email must be the GitHub no-reply address, never a personal email.
- If a requirement is unclear, ask before building.
