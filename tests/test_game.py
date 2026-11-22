"""Tests for the game rules in bone_room.game. Each test names the requirement it checks."""

import pytest

from bone_room.cases import Case
from bone_room.game import Game, GameOverError, GuessOutcome, Status


@pytest.fixture
def case():
    return Case(
        title="The Test Case",
        summary="Someone did something.",
        suspects=("Ann Ash", "Ben Birch", "Cy Cedar", "Di Dogwood"),
        clues=("Clue one.", "Clue two.", "Clue three."),
        killer="Cy Cedar",
    )


@pytest.fixture
def game(case):
    return Game(case)


# --- R1: case details and facts, one clue at a time ---------------------------------


def test_r1_game_exposes_case_details(game, case):
    """R1: the game shows the details of the case (title and summary)."""
    assert game.case.title == case.title
    assert game.case.summary == case.summary


def test_r1_game_starts_with_exactly_one_clue(game):
    """R1: only the first clue is visible at the start."""
    assert game.visible_clues == ("Clue one.",)


def test_r1_reveal_shows_exactly_one_more_clue_in_order(game):
    """R1: each reveal adds the next clue, one at a time."""
    assert game.reveal_next_clue() == "Clue two."
    assert game.visible_clues == ("Clue one.", "Clue two.")
    assert game.reveal_next_clue() == "Clue three."
    assert game.visible_clues == ("Clue one.", "Clue two.", "Clue three.")


def test_r1_reveal_when_no_clues_left_changes_nothing(game):
    """R1: after the last clue, asking again returns None and shows nothing new."""
    game.reveal_next_clue()
    game.reveal_next_clue()
    assert not game.has_more_clues
    assert game.reveal_next_clue() is None
    assert len(game.visible_clues) == 3


def test_r1_wrong_guess_does_not_reveal_a_clue(game):
    """R1: clues are revealed only when the player asks, not by wrong guesses."""
    game.guess("Ann Ash")
    assert game.visible_clues == ("Clue one.",)


# --- R2: guess the killer from a list of suspects ------------------------------------


def test_r2_suspects_come_from_the_case(game, case):
    """R2: the player chooses from the case's suspect list."""
    assert game.suspects == case.suspects


@pytest.mark.parametrize("text", ["Cy Cedar", "cy cedar", "  CY CEDAR  ", "3", " 3 "])
def test_r2_guess_by_name_or_number(game, text):
    """R2: a suspect can be named by full name (any case) or by list number."""
    assert game.resolve_suspect(text) == "Cy Cedar"


@pytest.mark.parametrize("text", ["", "   ", "Nobody", "0", "5", "-1", "Cy"])
def test_r2_unknown_guess_is_rejected_without_using_a_try(game, text):
    """R2: input that matches no suspect is rejected and costs nothing."""
    assert game.guess(text) is GuessOutcome.UNKNOWN
    assert game.guesses_left == 3
    assert game.status is Status.PLAYING


def test_r2_repeated_wrong_guess_is_rejected_without_using_a_try(game):
    """R2: guessing a suspect already ruled out is rejected and costs nothing."""
    assert game.guess("Ann Ash") is GuessOutcome.WRONG
    assert game.guess("1") is GuessOutcome.REPEAT
    assert game.guesses_left == 2


# --- R3: win in three tries or fewer, lose otherwise ---------------------------------


def test_r3_starts_with_three_tries(game):
    """R3: the player has three tries."""
    assert game.guesses_left == 3
    assert game.status is Status.PLAYING


def test_r3_correct_first_guess_wins(game):
    """R3: naming the killer on the first try wins."""
    assert game.guess("Cy Cedar") is GuessOutcome.CORRECT
    assert game.status is Status.WON


def test_r3_correct_third_guess_wins(game):
    """R3: naming the killer on the third try still wins."""
    assert game.guess("Ann Ash") is GuessOutcome.WRONG
    assert game.guess("Ben Birch") is GuessOutcome.WRONG
    assert game.guesses_left == 1
    assert game.guess("Cy Cedar") is GuessOutcome.CORRECT
    assert game.status is Status.WON


def test_r3_three_wrong_guesses_lose(game):
    """R3: three wrong tries lose the game."""
    game.guess("Ann Ash")
    game.guess("Ben Birch")
    assert game.status is Status.PLAYING
    assert game.guess("Di Dogwood") is GuessOutcome.WRONG
    assert game.guesses_left == 0
    assert game.status is Status.LOST


def test_r3_each_wrong_guess_uses_one_try(game):
    """R3: a wrong guess uses exactly one try."""
    game.guess("Ann Ash")
    assert game.guesses_left == 2


def test_r3_asking_for_clues_does_not_use_tries(game):
    """R3: only guesses count as tries; clues are free."""
    game.reveal_next_clue()
    game.reveal_next_clue()
    game.reveal_next_clue()
    assert game.guesses_left == 3


@pytest.mark.parametrize("moves", [["Cy Cedar"], ["Ann Ash", "Ben Birch", "Di Dogwood"]])
def test_r3_no_guesses_after_game_over(game, moves):
    """R3: once the game is won or lost, further guesses are refused."""
    for move in moves:
        game.guess(move)
    with pytest.raises(GameOverError):
        game.guess("Cy Cedar")


def test_r3_invalid_guesses_cannot_cause_a_loss(game):
    """R3: unknown and repeated guesses never push the player to a loss."""
    game.guess("Ann Ash")
    for _ in range(10):
        game.guess("Ann Ash")
        game.guess("nobody")
    assert game.guesses_left == 2
    assert game.status is Status.PLAYING
