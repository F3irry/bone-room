"""Terminal interface for Bone Room."""

from __future__ import annotations

from typing import Callable

from bone_room.cases import Case, choose_case
from bone_room.game import Game, GuessOutcome, Status

HELP = "Commands: [c] next clue   [s] suspects   [q] quit   or type a suspect's number/name to guess."


def _show_suspects(game: Game, out: Callable[[str], None]) -> None:
    out("Suspects:")
    for number, suspect in enumerate(game.suspects, start=1):
        mark = "  (ruled out)" if suspect in game.wrong_guesses else ""
        out(f"  {number}. {suspect}{mark}")


def run(case: Case, read: Callable[[str], str] = input, out: Callable[[str], None] = print) -> Status:
    """Play one game. Returns the final status (PLAYING if the player quit)."""
    game = Game(case)
    out(f"=== {case.title} ===")
    out(case.summary)
    out("")
    out(f"Clue 1: {game.visible_clues[0]}")
    out("")
    _show_suspects(game, out)
    out(f"You have {game.guesses_left} tries to name the killer.")
    out(HELP)

    while game.status is Status.PLAYING:
        try:
            # Strip a byte-order mark, which PowerShell adds to piped input.
            command = read("> ").replace("﻿", "").strip()
        except (EOFError, KeyboardInterrupt):
            out("")
            out("Case closed unsolved. Goodbye.")
            return game.status

        key = command.lower()
        if key == "q":
            out(f"You walk away from the case. The killer was {case.killer}.")
            return game.status
        if key == "c":
            clue = game.reveal_next_clue()
            if clue is None:
                out("No more clues. Time to make your guess.")
            else:
                out(f"Clue {len(game.visible_clues)}: {clue}")
            continue
        if key == "s":
            _show_suspects(game, out)
            continue

        outcome = game.guess(command)
        if outcome is GuessOutcome.UNKNOWN:
            out("That's not one of the suspects. " + HELP)
        elif outcome is GuessOutcome.REPEAT:
            out("You already ruled them out. That guess doesn't count.")
        elif outcome is GuessOutcome.CORRECT:
            out(f"Correct! {case.killer} did it. You solved the case.")
        elif game.status is Status.LOST:
            out(f"Wrong. You're out of tries. The killer was {case.killer}.")
        else:
            tries = "try" if game.guesses_left == 1 else "tries"
            out(f"Wrong. {game.guesses_left} {tries} left.")

    return game.status


def main() -> None:
    run(choose_case())
