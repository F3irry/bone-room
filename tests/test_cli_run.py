"""End-to-end tests of a continuous run in the terminal. Each test names the requirement it checks."""

from bone_room.cases import Case
from bone_room.cli import play_run
from bone_room.game import RunStatus

CASES = (
    Case(
        title="The Stolen Spoon",
        summary="A silver spoon is gone.",
        suspects=("Ann Ash", "Ben Birch", "Cy Cedar", "Dot Dale"),
        clues=("Spoon clue one.", "Spoon clue two."),
        killer="Ben Birch",
        genre="Theft",
        level=1,
        role="thief",
    ),
    Case(
        title="The Cold Cellar",
        summary="A body in the cellar.",
        suspects=("Di Dogwood", "Ed Elm", "Flo Fir", "Gus Gum"),
        clues=("Cellar clue one.", "Cellar clue two.", "Cellar clue three."),
        killer="Gus Gum",
        genre="Cold case",
        level=3,
        red_herrings=(2,),
    ),
)


def play(*inputs):
    """Play a run with scripted input; returns (run, output text, unread inputs)."""
    lines = iter(inputs)
    output = []

    def read(_prompt):
        try:
            return next(lines)
        except StopIteration:
            raise EOFError

    run = play_run(CASES, read=read, out=output.append)
    return run, "\n".join(output), list(lines)


# --- R7: case counter and severity ----------------------------------------------------


def test_r7_first_case_shows_counter_genre_and_severity():
    """R7: the case opens with 'Case 1 of 2 · Theft · Severity: Petty' above its title."""
    _, text, _ = play("q")
    assert "Case 1 of 2 · Theft · Severity: Petty\n=== The Stolen Spoon ===" in text


def test_r7_next_case_shows_its_own_counter_and_severity():
    """R7: the second case shows 'Case 2 of 2' and its own severity."""
    _, text, _ = play("2", "q")
    assert "Case 2 of 2 · Cold case · Severity: Grave" in text


def test_r7_messages_use_the_cases_culprit_role():
    """R7: a theft asks for the thief, not the killer."""
    _, text, _ = play("q")
    assert "You have 3 tries to name the thief." in text
    assert "The thief was Ben Birch." in text


# --- R4: the next case starts automatically -------------------------------------------


def test_r4_next_case_starts_automatically_after_a_win():
    """R4: after a correct guess the next case's details, first clue and suspects appear."""
    run, text, _ = play("ben birch", "q")
    assert "You solved the case." in text
    after_win = text.split("You solved the case.", 1)[1]
    assert "=== The Cold Cellar ===" in after_win
    assert "A body in the cellar." in after_win
    assert "Clue 1: Cellar clue one." in after_win
    assert "4. Gus Gum" in after_win
    assert run.case_number == 2


def test_r4_tries_reset_for_the_next_case():
    """R4: wrong guesses on one case do not carry into the next."""
    _, text, _ = play("1", "3", "2", "q")
    after_win = text.split("You solved the case.", 1)[1]
    assert "You have 3 tries to name the killer." in after_win


def test_r4_solving_every_case_completes_the_run():
    """R4: solving the last case ends the run with all cases solved."""
    run, text, _ = play("2", "4")
    assert run.status is RunStatus.COMPLETE
    assert "Run complete. You solved 2 cases." in text
    assert "Goodbye" not in text


# --- R8: failing a case ends the run --------------------------------------------------


def test_r8_three_wrong_guesses_end_the_run_and_show_solved_count():
    """R8: losing case 2 ends the run, reveals the killer and reports 1 case solved."""
    run, text, unread = play("2", "1", "2", "3", "c", "c")
    assert run.status is RunStatus.LOST
    assert "The killer was Gus Gum." in text
    assert "Run over. You solved 1 case." in text
    assert unread == ["c", "c"]


def test_r8_failing_the_first_case_reports_zero_solved():
    """R8: losing case 1 ends the run with 0 cases solved and never shows case 2."""
    run, text, _ = play("1", "3", "4")
    assert run.status is RunStatus.LOST
    assert "Run over. You solved 0 cases." in text
    assert "The Cold Cellar" not in text


def test_r8_quitting_mid_run_reports_solved_count():
    """R8: quitting ends the run and still says how many cases were solved."""
    _, text, _ = play("2", "q")
    assert "The killer was Gus Gum." in text
    assert "Run over. You solved 1 case." in text


def test_r8_end_of_input_mid_run_reports_solved_count():
    """R8: if input ends mid-run, the run stops cleanly and reports the count."""
    _, text, _ = play("2")
    assert "Goodbye" in text
    assert "Run over. You solved 1 case." in text
