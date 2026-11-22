"""End-to-end tests of the terminal loop with scripted input. Each test names the requirement it checks."""

import pytest

from bone_room.cases import Case
from bone_room.cli import run
from bone_room.game import Status

CASE = Case(
    title="The Test Case",
    summary="Someone did something.",
    suspects=("Ann Ash", "Ben Birch", "Cy Cedar"),
    clues=("Clue one.", "Clue two."),
    killer="Cy Cedar",
)


def play(*inputs):
    """Run a game with scripted input; returns (status, all output as one string)."""
    lines = iter(inputs)
    output = []

    def read(_prompt):
        try:
            return next(lines)
        except StopIteration:
            raise EOFError

    status = run(CASE, read=read, out=output.append)
    return status, "\n".join(output)


def test_r1_opening_shows_case_details_and_only_first_clue():
    """R1: the opening shows title, summary and only the first clue."""
    _, text = play("q")
    assert "The Test Case" in text
    assert "Someone did something." in text
    assert "Clue 1: Clue one." in text
    assert "Clue two." not in text


def test_r1_c_reveals_next_clue_then_reports_none_left():
    """R1: 'c' reveals one clue at a time, then says there are no more."""
    _, text = play("c", "c", "q")
    assert "Clue 2: Clue two." in text
    assert "No more clues" in text


def test_r1_clue_command_works_with_byte_order_mark():
    """R1: 'c' still reveals a clue when input starts with a BOM (PowerShell pipes)."""
    _, text = play("﻿c", "q")
    assert "Clue 2: Clue two." in text


def test_r2_suspects_are_listed_with_numbers():
    """R2: the player sees a numbered suspect list to guess from."""
    _, text = play("q")
    assert "1. Ann Ash" in text
    assert "3. Cy Cedar" in text


def test_r2_unknown_guess_gets_a_message():
    """R2: a guess that isn't a suspect is explained, not counted."""
    status, text = play("Zed", "q")
    assert "not one of the suspects" in text
    assert "2 tries left" not in text
    assert status is Status.PLAYING


@pytest.mark.parametrize("guess", ["3", "cy cedar"])
def test_r3_correct_guess_wins(guess):
    """R3: naming the killer (by number or name) wins."""
    status, text = play(guess)
    assert status is Status.WON
    assert "You solved the case" in text


def test_r3_three_wrong_guesses_lose_and_reveal_killer():
    """R3: three wrong tries lose and the killer is revealed."""
    case = Case(
        title="Four", summary="s", suspects=("A", "B", "C", "D"), clues=("x", "y"), killer="D"
    )
    lines = iter(["1", "2", "3"])
    output = []
    status = run(case, read=lambda _p: next(lines), out=output.append)
    text = "\n".join(output)
    assert status is Status.LOST
    assert "2 tries left" in text
    assert "1 try left" in text
    assert "The killer was D" in text


def test_r3_win_on_third_try():
    """R3: a correct guess on the third try still wins."""
    case = Case(
        title="Four", summary="s", suspects=("A", "B", "C", "D"), clues=("x", "y"), killer="C"
    )
    lines = iter(["1", "1", "2", "c", "3"])
    status = run(case, read=lambda _p: next(lines), out=lambda _s: None)
    assert status is Status.WON


def test_r3_end_of_input_exits_cleanly():
    """R3: if input ends mid-game, the game stops without crashing."""
    status, text = play()
    assert status is Status.PLAYING
    assert "Goodbye" in text
