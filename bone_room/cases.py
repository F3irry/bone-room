"""Case data for Bone Room and the random case picker."""

from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass(frozen=True)
class Case:
    title: str
    summary: str
    suspects: tuple[str, ...]
    clues: tuple[str, ...]
    killer: str

    def __post_init__(self) -> None:
        if self.killer not in self.suspects:
            raise ValueError(f"killer {self.killer!r} is not one of the suspects")
        if not self.clues:
            raise ValueError("a case needs at least one clue")


CASES: tuple[Case, ...] = (
    Case(
        title="The Bone Room",
        summary=(
            "Professor Alder Finch is found dead in his bone room, the locked study where he "
            "kept his collection of animal skeletons. Four people were at Finch House that night."
        ),
        suspects=("Mara Quill", "Otto Lenz", "Ivy Finch", "Bram Hollis"),
        clues=(
            "Finch was struck with a heavy femur from his own collection between 9 and 10 pm.",
            "Bram Hollis, the groundskeeper, was at the village pub from 8 pm until it closed at 11.",
            "The blow landed on the right side of Finch's head: the killer swung left-handed. "
            "Mara Quill and Otto Lenz are both left-handed.",
            "Otto Lenz's train ticket is stamped 10:40 pm. He arrived after Finch was already dead.",
            "Fine white bone dust was found on the cuff of a left-hand glove in the study bin.",
        ),
        killer="Mara Quill",
    ),
    Case(
        title="Tea at the Lighthouse",
        summary=(
            "Keeper Silas Dunmore collapses after his afternoon tea at Gull Point lighthouse. "
            "The doctor finds foxglove in the cup."
        ),
        suspects=("Nell Harrow", "Captain Reyes", "Theo Dunmore", "Agnes Pike"),
        clues=(
            "Silas drank his tea at 4 pm. Foxglove takes effect within the hour.",
            "Captain Reyes's boat was logged arriving at the jetty at 5 pm.",
            "Foxglove grows only in the cliff garden, behind a bramble gate. Nell Harrow and "
            "Theo Dunmore both have fresh scratches on their hands; Agnes Pike has none.",
            "Nell Harrow spent the whole afternoon at the mainland market and took the 6 pm ferry "
            "back. The ferryman confirms it.",
        ),
        killer="Theo Dunmore",
    ),
    Case(
        title="The Clockmaker's Last Hour",
        summary=(
            "Clockmaker Edda Voss is found stabbed with an engraving tool in her workshop. "
            "A clock knocked from the bench stopped when it hit the floor."
        ),
        suspects=("Jonah Pell", "Lucia Marr", "Felix Voss", "Rosa Tan"),
        clues=(
            "The fallen clock stopped at 11:15 am.",
            "Rosa Tan, the neighbour, was on a video call from 11:00 to 12:00. The recording shows "
            "her the whole time.",
            "The shop bell logs every opening of the front door. Nobody came in after 10:30, so the "
            "killer used the back door, which only opens with a key. Jonah Pell and Felix Voss "
            "carry keys; Lucia Marr does not.",
            "Jonah Pell was depositing the week's takings at the bank at 11:10. The teller remembers him.",
        ),
        killer="Felix Voss",
    ),
)


def choose_case(rng: random.Random | None = None) -> Case:
    """Pick one shipped case at random."""
    return (rng or random).choice(CASES)
