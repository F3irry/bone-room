"""Tests for the case ladder used by a continuous run. Each test names the requirement it checks."""

import pytest

from bone_room.cases import CASES, LADDER, SEVERITIES, Case


def _ladder_metric(metric):
    return [metric(case) for case in LADDER]


# --- R6: variety and size of the ladder -----------------------------------------------


def test_r6_ladder_has_at_least_seven_cases():
    """R6: the run has 7 or more cases."""
    assert len(LADDER) >= 7


def test_r6_ladder_has_at_least_four_new_cases():
    """R6: at least 4 ladder cases are new (not among the round-1 classic cases)."""
    classic_titles = {case.title for case in CASES}
    assert len([c for c in LADDER if c.title not in classic_titles]) >= 4


def test_r6_ladder_titles_are_unique():
    """R6: every case in the ladder is a different case."""
    assert len({case.title for case in LADDER}) == len(LADDER)


def test_r6_ladder_varies_in_genre():
    """R6: the ladder covers at least 4 different genres."""
    assert len({case.genre for case in LADDER}) >= 4


def test_r6_ladder_varies_in_severity():
    """R6: the ladder covers at least 4 different severity levels."""
    assert len({case.severity for case in LADDER}) >= 4


@pytest.mark.parametrize("case", LADDER, ids=lambda c: c.title)
def test_r6_each_ladder_case_is_well_formed(case):
    """R6: every ladder case has details, 4-6 distinct suspects, the culprit among them, 3+ clues."""
    assert case.title.strip() and case.summary.strip() and case.genre.strip()
    assert case.role.strip()
    assert 4 <= len(case.suspects) <= 6
    assert len({s.lower() for s in case.suspects}) == len(case.suspects)
    assert case.killer in case.suspects
    assert len(case.clues) >= 3


# --- R5: difficulty rises along the ladder --------------------------------------------


@pytest.mark.parametrize(
    "metric",
    [
        lambda c: len(c.suspects),
        lambda c: len(c.clues),
        lambda c: len(c.red_herrings),
        lambda c: c.level,
    ],
    ids=["suspects", "clues", "red_herrings", "severity_level"],
)
def test_r5_difficulty_never_drops_and_ends_higher(metric):
    """R5: suspects, clues, red herrings and severity never go down, and the last case is harder."""
    values = _ladder_metric(metric)
    assert values == sorted(values)
    assert values[-1] > values[0]


def test_r5_red_herrings_only_in_later_cases():
    """R5: the opening cases have no red herrings; the final case has some."""
    assert all(not case.red_herrings for case in LADDER[:3])
    assert len(LADDER[-1].red_herrings) >= 1


@pytest.mark.parametrize("case", LADDER, ids=lambda c: c.title)
def test_r5_red_herrings_point_at_real_clues_but_never_the_first(case):
    """R5: red herrings are 1-based clue numbers within the case, and clue 1 is always genuine."""
    for number in case.red_herrings:
        assert 2 <= number <= len(case.clues)


@pytest.mark.parametrize(
    "bad",
    [{"red_herrings": (1,)}, {"red_herrings": (3,)}, {"level": 0}, {"level": len(SEVERITIES) + 1}],
)
def test_r5_case_rejects_invalid_red_herrings_or_level(bad):
    """R5: a case cannot mark clue 1 or a missing clue as a red herring, or use an unknown level."""
    with pytest.raises(ValueError):
        Case(title="t", summary="s", suspects=("A", "B", "C"), clues=("x", "y"), killer="A", **bad)


# --- R4: fixed case order -------------------------------------------------------------


def test_r4_ladder_order_starts_light_and_ends_heavy():
    """R4: the run always plays the same order, from the missing heirloom to the night train."""
    assert LADDER[0].title == "The Missing Locket"
    assert LADDER[-1].title == "The Night Train to Vell"


# --- R7: severity names ---------------------------------------------------------------


def test_r7_severity_names_follow_level():
    """R7: each case's severity name matches its level (1 Petty ... 5 Notorious)."""
    assert SEVERITIES == ("Petty", "Serious", "Grave", "Dire", "Notorious")
    for case in LADDER:
        assert case.severity == SEVERITIES[case.level - 1]


def test_r7_defaults_keep_round_one_cases_working():
    """R7: a case built without the new fields is a level-1 murder with no red herrings."""
    case = Case(title="t", summary="s", suspects=("A", "B", "C"), clues=("x", "y"), killer="A")
    assert case.role == "killer"
    assert case.level == 1
    assert case.severity == "Petty"
    assert case.red_herrings == ()
