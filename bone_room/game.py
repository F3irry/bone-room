"""Game rules for Bone Room. No input or output happens here."""

from __future__ import annotations

from enum import Enum

from bone_room.cases import Case

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
