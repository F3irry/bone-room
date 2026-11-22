"""Terminal interface for Bone Room."""

from __future__ import annotations

from typing import Callable, Sequence

from bone_room.cases import Case
from bone_room.game import Game, GuessOutcome, Run, RunStatus, Status

HELP = "Commands: [c] next clue   [s] suspects   [q] quit   or type a suspect's number/name to guess."

Read = Callable[[str], str]
Out = Callable[[str], None]


def _show_suspects(game: Game, out: Out) -> None:
    out("Suspects:")
    for number, suspect in enumerate(game.suspects, start=1):
        mark = "  (ruled out)" if suspect in game.wrong_guesses else ""
        out(f"  {number}. {suspect}{mark}")


def _open_case(game: Game, out: Out) -> None:
    case = game.case
    out(f"=== {case.title} ===")
    out(case.summary)
    out("")
    out(f"Clue 1: {game.visible_clues[0]}")
    out("")
    _show_suspects(game, out)
    out(f"You have {game.guesses_left} tries to name the {case.role}.")
    out(HELP)


def _play_case(game: Game, read: Read, out: Out) -> bool:
    """Play one case until it is won or lost. Returns False if the player left instead."""
    case = game.case
    while game.status is Status.PLAYING:
        try:
            # Strip a byte-order mark, which PowerShell adds to piped input.
            command = read("> ").replace("﻿", "").strip()
        except (EOFError, KeyboardInterrupt):
            out("")
            out("Case closed unsolved. Goodbye.")
            return False

        key = command.lower()
        if key == "q":
            out(f"You walk away from the case. The {case.role} was {case.killer}.")
            return False
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
            out(f"Wrong. You're out of tries. The {case.role} was {case.killer}.")
        else:
            tries = "try" if game.guesses_left == 1 else "tries"
            out(f"Wrong. {game.guesses_left} {tries} left.")
    return True


def run(case: Case, read: Read = input, out: Out = print) -> Status:
    """Play one case on its own. Returns the final status (PLAYING if the player quit)."""
    game = Game(case)
    _open_case(game, out)
    _play_case(game, read, out)
    return game.status


def _solved_text(count: int) -> str:
    return f"You solved {count} {'case' if count == 1 else 'cases'}."


def play_run(cases: Sequence[Case] | None = None, read: Read = input, out: Out = print) -> Run:
    """Play a continuous run: each solved case leads straight into the next (R4).

    The run ends when a case is lost (R8), the last case is solved, or the player leaves.
    Returns the finished Run.
    """
    the_run = Run(cases)
    while True:
        case = the_run.game.case
        out(f"Case {the_run.case_number} of {the_run.total} · {case.genre} · Severity: {case.severity}")
        _open_case(the_run.game, out)
        finished = _play_case(the_run.game, read, out)

        if finished and the_run.status is RunStatus.PLAYING:
            the_run.next_case()
            out("")
            continue
        if the_run.status is RunStatus.COMPLETE:
            out(f"Run complete. {_solved_text(the_run.solved)}")
        else:
            out(f"Run over. {_solved_text(the_run.solved)}")
        return the_run


def main() -> None:
    play_run()
