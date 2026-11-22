# Bone Room — Specification (round 1)

Bone Room is a short murder-mystery game played in the terminal. The player reads a
case, reveals clues one at a time, and tries to name the killer in three guesses or fewer.
No download beyond Python 3.13; no external runtime dependencies.

## Requirements (from problem.md)

| ID | Requirement |
|----|-------------|
| R1 | The game shows the details and facts of a case, one clue at a time. |
| R2 | The player can guess who the killer is from a list of suspects. |
| R3 | The player wins by naming the killer in three tries or fewer, and loses otherwise. |

## Decisions that clarify the requirements

These were confirmed with the product owner before building:

- **Clue reveal (R1):** the game opens with the case title, the case summary, and the
  first clue. Each further clue appears only when the player asks for it. Wrong guesses
  do not reveal clues automatically.
- **What counts as a try (R3):** only a guess at the killer uses a try. Asking for clues is
  free and unlimited until every clue has been shown.
- **Cases:** the game ships with 3 cases. One is chosen at random at the start of each run.
- **Invalid and repeated guesses (R2, R3):** a guess that does not match a suspect, or that
  repeats a suspect already guessed wrongly, is rejected with a message and does not use
  a try.

## Detailed behaviour

### Case data
- Each case has a title, a short summary, a list of 3–5 suspects, an ordered list of at
  least 2 clues, and exactly one killer, who must be one of the suspects.
- Taken together, a case's clues must be enough to identify the killer.

### Clues (R1)
- At the start of a game exactly one clue is visible.
- Revealing a clue makes exactly one more clue visible, in the case's order.
- When all clues are visible, asking for another shows a "no more clues" message and
  changes nothing.

### Guessing (R2)
- The suspects are shown as a numbered list.
- The player can guess by number (`2`) or by full name, ignoring case and surrounding
  spaces (`  mara quill `).
- Unknown input and repeated wrong suspects are rejected without using a try (see above).

### Winning and losing (R3)
- The player has 3 tries.
- A correct guess on try 1, 2 or 3 wins the game.
- A wrong guess uses a try and tells the player how many remain.
- The third wrong guess loses the game, and the killer is revealed.
- Once the game is won or lost, no further guesses are accepted.

### Terminal interface
- Commands at the prompt:
  - `c` — reveal the next clue
  - `s` — show the suspect list again
  - `q` — quit
  - anything else — treated as a guess (number or name)
- The game also ends cleanly if input ends (Ctrl+Z / Ctrl+D) or the player presses Ctrl+C.

## Out of scope for round 1
- Saving progress, scores, or statistics.
- Difficulty levels, hints, timers.
- Colour or graphical interfaces.
