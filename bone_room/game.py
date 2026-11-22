"""Game rules for Bone Room. No input or output happens here."""

from __future__ import annotations

from collections.abc import Sequence
from enum import Enum

from bone_room.cases import LADDER, Case

MAX_GUESSES = 3


class Status(Enum):
    PLAYING = "playing"
    WON = "won"
    LOST = "lost"


class GuessOutcome(Enum):
    CORRECT = "correct"
    WRONG = "wrong"
    UNKNOWN = "unknown"  # matched no suspect; costs no try
    REPEAT = "repeat"  # suspect already guessed wrongly; costs no try


class GameOverError(Exception):
    """Raised when a guess is made after the game has ended."""


class Game:
    def __init__(self, case: Case) -> None:
        self.case = case
        self._clues_shown = 1
        self._wrong: list[str] = []
        self.status = Status.PLAYING

    # --- clues (R1) ---

    @property
    def visible_clues(self) -> tuple[str, ...]:
        return self.case.clues[: self._clues_shown]

    @property
    def has_more_clues(self) -> bool:
        return self._clues_shown < len(self.case.clues)

    def reveal_next_clue(self) -> str | None:
        """Show one more clue. Returns it, or None when all clues are already shown."""
        if not self.has_more_clues:
            return None
        self._clues_shown += 1
        return self.case.clues[self._clues_shown - 1]

    # --- guessing (R2, R3) ---

    @property
    def suspects(self) -> tuple[str, ...]:
        return self.case.suspects

    @property
    def wrong_guesses(self) -> tuple[str, ...]:
        return tuple(self._wrong)

    @property
    def guesses_left(self) -> int:
        return MAX_GUESSES - len(self._wrong)

    def resolve_suspect(self, text: str) -> str | None:
        """Match a list number or full name (any case) to a suspect."""
        text = text.strip()
        if text.isdigit():
            index = int(text) - 1
            if 0 <= index < len(self.suspects):
                return self.suspects[index]
            return None
        for suspect in self.suspects:
            if suspect.lower() == text.lower():
                return suspect
        return None

    def guess(self, text: str) -> GuessOutcome:
        if self.status is not Status.PLAYING:
            raise GameOverError("the game is already over")
        suspect = self.resolve_suspect(text)
        if suspect is None:
            return GuessOutcome.UNKNOWN
        if suspect in self._wrong:
            return GuessOutcome.REPEAT
        if suspect == self.case.killer:
            self.status = Status.WON
            return GuessOutcome.CORRECT
        self._wrong.append(suspect)
        if self.guesses_left == 0:
            self.status = Status.LOST
        return GuessOutcome.WRONG


class RunStatus(Enum):
    PLAYING = "playing"  # a case is in progress, or one was just solved and another follows
    COMPLETE = "complete"  # the last case was solved
    LOST = "lost"  # a case was lost, which ends the run


class Run:
    """A continuous run through an ordered list of cases (R4, R8)."""

    def __init__(self, cases: Sequence[Case] | None = None) -> None:
        self.cases = tuple(LADDER if cases is None else cases)
        if not self.cases:
            raise ValueError("a run needs at least one case")
        self._index = 0
        self.game = Game(self.cases[0])

    @property
    def case_number(self) -> int:
        """1-based number of the current case."""
        return self._index + 1

    @property
    def total(self) -> int:
        return len(self.cases)

    @property
    def solved(self) -> int:
        return self._index + (1 if self.game.status is Status.WON else 0)

    @property
    def status(self) -> RunStatus:
        if self.game.status is Status.LOST:
            return RunStatus.LOST
        if self.game.status is Status.WON and self.case_number == self.total:
            return RunStatus.COMPLETE
        return RunStatus.PLAYING

    def next_case(self) -> Game | None:
        """Move on after a win. Returns the new case's game, or None if the run is complete."""
        if self.game.status is not Status.WON:
            raise GameOverError("the current case must be solved before moving on")
        if self.case_number == self.total:
            return None
        self._index += 1
        self.game = Game(self.cases[self._index])
        return self.game
