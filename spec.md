# Bone Room — Specification (rounds 1 and 2)

Bone Room is a short murder-mystery game played in the terminal. The player reads a
case, reveals clues one at a time, and tries to name the killer in three guesses or fewer.
No download beyond Python 3.13; no external runtime dependencies.

## Requirements (from problem.md)

| ID | Requirement |
|----|-------------|
| R1 | The game shows the details and facts of a case, one clue at a time. |
| R2 | The player can guess who the killer is from a list of suspects. |
| R3 | The player wins by naming the killer in three tries or fewer, and loses otherwise. |
| R4 | After the player solves a case, the next case starts automatically. |
| R5 | Cases get harder as the run goes on: more suspects, more clues, red herrings later. |
| R6 | Cases vary in genre and severity; at least 4 new cases, 7 or more in all. |
| R7 | The game shows a case counter and difficulty level. |
| R8 | Failing a case (3 wrong guesses) ends the run and shows how many cases were solved. |

## Decisions that clarify the requirements

These were confirmed with the product owner before building:

- **Clue reveal (R1):** the game opens with the case title, the case summary, and the
  first clue. Each further clue appears only when the player asks for it. Wrong guesses
  do not reveal clues automatically.
- **What counts as a try (R3):** only a guess at the killer uses a try. Asking for clues is
  free and unlimited until every clue has been shown.
- **Cases (round 1):** the game shipped with 3 cases, one chosen at random. These three
  "classic" cases are still available as `CASES` / `choose_case`, but the game itself now
  plays the case ladder (round 2, below).
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

## Round 2: the continuous run (R4–R8)

### Decisions
- **The ladder (R4, R6):** the game plays a fixed, ordered ladder of 7 cases: 4 new cases
  plus the 3 round-1 cases. Every run starts at case 1 and plays the same order, so
  difficulty always rises.
- **Tries per case (R4, R8):** every case starts with 3 fresh tries and only its first clue
  visible. Tries do not carry over between cases.
- **Winning the run:** solving the last case ends the run with a "run complete" message and
  the number of cases solved (all of them).
- **Quitting:** `q`, end of input or Ctrl+C ends the whole run, reveals the current
  culprit as before, and shows how many cases were solved.
- **Culprit wording (R6):** not every case is a murder. Each case names its culprit's role
  (`killer` by default, e.g. `thief` for a theft), and the game uses that word in its
  messages ("name the thief", "The thief was ...").
- **Red herrings (R5):** a red herring is a true clue that casts suspicion on an innocent
  suspect. A later clue in the same case always rules that suspect out, so every case can
  still be solved from its clues. The game does not tell the player which clues mislead.
  The first clue of a case is never a red herring.

### Case data
- Besides the round-1 fields, each case has a genre (e.g. "Missing heirloom",
  "Poisoning", "Locked-room murder", "Cold case"), a severity level, the clue numbers
  (1-based) that are red herrings, and the culprit's role.
- Ladder cases have 3–6 suspects and at least 3 clues.
- Severity levels, from lightest to heaviest: 1 Petty, 2 Serious, 3 Grave, 4 Dire,
  5 Notorious.

### Difficulty (R5)
Along the ladder, from one case to the next, none of these ever goes down, and the last
case is strictly higher than the first in each:
- number of suspects,
- number of clues,
- number of red herrings,
- severity level.

The first cases have no red herrings; the later ones do. The ladder covers at least 4
genres and at least 4 severity levels (R6).

### Case header (R7)
Each case opens with a counter line above the usual title, for example:

```
Case 2 of 7 · Poisoning · Severity: Serious
=== Tea at the Lighthouse ===
```

### End of a run (R4, R8)
- After a correct guess, the next case's header, summary, first clue and suspects are
  shown straight away (R4).
- A third wrong guess loses the case, reveals the culprit and ends the run with
  "Run over. You solved N cases." No further input is read (R8).

## Out of scope
- Saving progress, scores, or statistics between runs.
- Choosing a difficulty, hints, timers.
- Colour or graphical interfaces.
