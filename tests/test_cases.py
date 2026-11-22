"""Tests for the shipped case data in bone_room.cases. Each test names the requirement it checks."""

import random

import pytest

from bone_room.cases import CASES, choose_case


def test_r1_ships_three_cases():
    """R1: the game has 3 cases to present (spec decision)."""
    assert len(CASES) == 3


@pytest.mark.parametrize("case", CASES, ids=lambda c: c.title)
def test_r1_each_case_has_details_and_several_clues(case):
    """R1: every case has a title, a summary and at least 2 clues to reveal one at a time."""
    assert case.title.strip()
    assert case.summary.strip()
    assert len(case.clues) >= 2
    assert all(clue.strip() for clue in case.clues)


@pytest.mark.parametrize("case", CASES, ids=lambda c: c.title)
def test_r2_each_case_has_a_valid_suspect_list(case):
    """R2: every case offers 3-5 distinct suspects, and the killer is one of them."""
    assert 3 <= len(case.suspects) <= 5
    assert len({s.lower() for s in case.suspects}) == len(case.suspects)
    assert case.killer in case.suspects


def test_r2_case_rejects_killer_not_in_suspects():
    """R2: a case whose killer is not a suspect cannot be built."""
    from bone_room.cases import Case

    with pytest.raises(ValueError):
        Case(title="t", summary="s", suspects=("A", "B", "C"), clues=("x", "y"), killer="Z")


def test_r1_choose_case_picks_from_the_shipped_cases():
    """R1: a case is chosen at random from the shipped cases."""
    rng = random.Random(0)
    picks = {choose_case(rng).title for _ in range(200)}
    assert picks == {c.title for c in CASES}
