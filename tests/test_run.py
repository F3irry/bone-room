"""Tests for a continuous run of cases (bone_room.game.Run). Each test names the requirement it checks."""

import pytest

from bone_room.cases import LADDER, Case
from bone_room.game import GameOverError, Run, RunStatus, Status


def make_case(title, killer="C"):
    return Case(title=title, summary="s", suspects=("A", "B", "C", "D"), clues=("x", "y"), killer=killer)


@pytest.fixture
def cases():
    return (make_case("First"), make_case("Second", killer="A"), make_case("Third", killer="D"))


@pytest.fixture
def run(cases):
    return Run(cases)


def lose(game):
    for suspect in game.suspects:
        if suspect != game.case.killer and game.status is Status.PLAYING:
            game.guess(suspect)


# --- R4: the run continues after a win, in order --------------------------------------


def test_r4_run_starts_on_the_first_case(run, cases):
    """R4: a run begins with case 1 of the ladder."""
    assert run.case_number == 1
    assert run.total == 3
    assert run.game.case is cases[0]
    assert run.solved == 0
    assert run.status is RunStatus.PLAYING


def test_r4_default_run_uses_the_ladder():
    """R4: without arguments a run plays the shipped ladder from the start."""
    run = Run()
    assert run.total == len(LADDER)
    assert run.game.case is LADDER[0]


def test_r4_run_continues_after_a_win(run, cases):
    """R4: after solving a case the run is still going and the next case is ready."""
    run.game.guess("C")
    assert run.status is RunStatus.PLAYING
    assert run.solved == 1
    game = run.next_case()
    assert game is run.game
    assert run.case_number == 2
    assert game.case is cases[1]


def test_r4_next_case_starts_fresh(run):
    """R4: each new case has 3 tries and only its first clue, whatever happened before."""
    run.game.guess("A")
    run.game.guess("B")
    run.game.reveal_next_clue()
    run.game.guess("C")
    game = run.next_case()
    assert game.guesses_left == 3
    assert game.visible_clues == ("x",)
    assert game.status is Status.PLAYING


def test_r4_cases_are_played_in_ladder_order(run, cases):
    """R4: solving each case in turn walks the ladder in its fixed order."""
    seen = []
    while True:
        seen.append(run.game.case.title)
        run.game.guess(run.game.case.killer)
        if run.next_case() is None:
            break
    assert seen == [case.title for case in cases]


def test_r4_next_case_refused_before_the_current_one_is_solved(run):
    """R4: the run only moves on after a win."""
    with pytest.raises(GameOverError):
        run.next_case()
    assert run.case_number == 1


def test_r4_solving_the_last_case_completes_the_run(run, cases):
    """R4: after the final case there is no next case and the run is complete."""
    for _ in cases:
        run.game.guess(run.game.case.killer)
        run.next_case()
    assert run.status is RunStatus.COMPLETE
    assert run.solved == 3
    assert run.next_case() is None
    assert run.case_number == 3


def test_r4_run_needs_at_least_one_case():
    """R4: an empty run cannot be built."""
    with pytest.raises(ValueError):
        Run(())


# --- R8: a lost case ends the run -----------------------------------------------------


def test_r8_losing_a_case_ends_the_run(run):
    """R8: three wrong guesses on a case end the whole run."""
    run.game.guess("C")
    run.next_case()
    lose(run.game)
    assert run.game.status is Status.LOST
    assert run.status is RunStatus.LOST


def test_r8_solved_count_after_a_loss(run):
    """R8: after a loss the run reports how many cases were solved before it."""
    run.game.guess("C")
    run.next_case()
    lose(run.game)
    assert run.solved == 1


def test_r8_losing_the_first_case_solves_none(run):
    """R8: failing case 1 ends the run with zero cases solved."""
    lose(run.game)
    assert run.status is RunStatus.LOST
    assert run.solved == 0


def test_r8_no_next_case_after_a_loss(run):
    """R8: once the run is lost it cannot continue."""
    lose(run.game)
    with pytest.raises(GameOverError):
        run.next_case()
