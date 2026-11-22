"""Case data for Bone Room: the case ladder for a run, plus the round-1 classic cases."""

from __future__ import annotations

import random
from dataclasses import dataclass

SEVERITIES: tuple[str, ...] = ("Petty", "Serious", "Grave", "Dire", "Notorious")
"""Severity names by level: level 1 is SEVERITIES[0]."""


@dataclass(frozen=True)
class Case:
    title: str
    summary: str
    suspects: tuple[str, ...]
    clues: tuple[str, ...]
    killer: str  # the culprit, whatever the crime; see `role`
    genre: str = "Murder"
    level: int = 1  # severity level, 1..len(SEVERITIES)
    red_herrings: tuple[int, ...] = ()  # 1-based numbers of the misleading clues
    role: str = "killer"  # what the culprit is called in messages, e.g. "thief"

    def __post_init__(self) -> None:
        if self.killer not in self.suspects:
            raise ValueError(f"killer {self.killer!r} is not one of the suspects")
        if not self.clues:
            raise ValueError("a case needs at least one clue")
        if not 1 <= self.level <= len(SEVERITIES):
            raise ValueError(f"level must be 1-{len(SEVERITIES)}, not {self.level}")
        for number in self.red_herrings:
            if not 2 <= number <= len(self.clues):
                raise ValueError(
                    f"red herring {number} must be a clue number from 2 to {len(self.clues)}"
                )

    @property
    def severity(self) -> str:
        return SEVERITIES[self.level - 1]


# --- Round-1 classic cases -------------------------------------------------------------

BONE_ROOM = Case(
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
    genre="Country-house murder",
    level=3,
)

LIGHTHOUSE = Case(
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
    genre="Poisoning",
    level=2,
)

CLOCKMAKER = Case(
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
    genre="Workshop stabbing",
    level=2,
)

CASES: tuple[Case, ...] = (BONE_ROOM, LIGHTHOUSE, CLOCKMAKER)
"""The three round-1 classic cases."""


# --- Round-2 cases ---------------------------------------------------------------------

MISSING_LOCKET = Case(
    title="The Missing Locket",
    summary=(
        "Grandmother Wren's silver locket, a family heirloom, vanishes from her jewellery box "
        "during Sunday lunch at Wren Cottage. Four guests were at the table."
    ),
    suspects=("Pip Wren", "Clara Osei", "Dennis Hale", "Tom Wren"),
    clues=(
        "The locket was in the jewellery box upstairs at noon and gone by 2 pm. During lunch "
        "each guest left the table once.",
        "Dennis Hale took a phone call in the garden. The neighbour watched him pace the lawn "
        "the whole time.",
        "Tom Wren only went as far as the hall stand to fetch Grandmother's shawl, in full view "
        "of the dining room, and was back within a minute.",
        "There is a smear of strawberry jam on the jewellery box lid. Clara Osei brought the "
        "jam and spread it thickly on her scones; Pip Wren is allergic to strawberries and "
        "never touched it.",
    ),
    killer="Clara Osei",
    genre="Missing heirloom",
    level=1,
    role="thief",
)

SEALED_ARCHIVE = Case(
    title="The Sealed Archive",
    summary=(
        "Archivist Hugo Brandt is found dead inside the steel vault of the city archive. The "
        "door was bolted on the inside and the only window is barred."
    ),
    suspects=("Selma Roth", "Ivo Kesh", "Petra Lind", "Gus Mallory", "Noor Halim"),
    clues=(
        "Brandt died from a blow to the head at about 7 pm. The night guard had to force the "
        "bolted vault door at 9 pm.",
        "The bolt's steel knob has a fresh scuff, and a strong horseshoe magnet is missing from "
        "the conservation lab. Someone slid the bolt shut from outside, through the door.",
        "Ivo Kesh, Brandt's academic rival, was overheard that morning: "
        "\"You'll regret burying my paper, Hugo.\"",
        "Only staff can enter the conservation lab: Selma Roth, Ivo Kesh and Gus Mallory. Petra "
        "Lind and Noor Halim are visiting researchers with reading-room passes only.",
        "Ivo Kesh gave a public lecture from 6:30 to 8 pm in front of eighty people.",
        "Selma Roth's badge shows her leaving the building at 5:15 pm. She did not come back "
        "until the next morning.",
    ),
    killer="Gus Mallory",
    genre="Locked-room murder",
    level=4,
    red_herrings=(3,),
)

WINTER_OF_89 = Case(
    title="The Winter of '89",
    summary=(
        "In January 1989 mill owner Harriet Coombe vanished from Coombe Mill. Last month "
        "builders found her remains under the mill floor. Five people who worked there that "
        "winter are still alive."
    ),
    suspects=("Walter Coombe", "June Aldous", "Ray Penhale", "Lottie Marsh", "Sid Farrow"),
    clues=(
        "Harriet's wristwatch, found with her, stopped on the night of 14 January 1989. The "
        "coroner agrees she died that night.",
        "Walter Coombe, her husband, inherited the mill and remarried within the year.",
        "She was buried in the locked floor store before it was concreted at dawn on 15 "
        "January. Keys were held by Walter Coombe, June Aldous, Ray Penhale and Sid Farrow; "
        "Lottie Marsh had none.",
        "Walter Coombe was in hospital with pneumonia from 13 to 16 January. The old admission "
        "book confirms it.",
        "Sid Farrow was snowed in at his sister's farm across the valley from 12 to 17 January. "
        "Three neighbours remember digging him out.",
        "Fibres under Harriet's fingernails come from a blue mill-issue work jacket. Only floor "
        "workers were given those; June Aldous, the office clerk, never had one.",
    ),
    killer="Ray Penhale",
    genre="Cold case",
    level=4,
    red_herrings=(2,),
)

NIGHT_TRAIN = Case(
    title="The Night Train to Vell",
    summary=(
        "Financier Lionel Crane is found stabbed in his sleeper compartment on the overnight "
        "train to Vell. Six passengers had berths in the sleeper carriage."
    ),
    suspects=(
        "Vera Sokol",
        "Anton Pryce",
        "Mina Calder",
        "Reuben Stroud",
        "Hattie Lowe",
        "Father Corin",
    ),
    clues=(
        "Crane was stabbed in compartment 4 between 1:00 and 1:30 am.",
        "The doors between carriages were locked from midnight to 2 am, so the killer was "
        "already in the sleeper carriage. Mina Calder spent those hours in the dining car with "
        "the steward.",
        "Vera Sokol had written to Crane threatening to ruin him, and her compartment is next "
        "door to his.",
        "The wound was struck downward from well above Crane's shoulder: the killer was tall. "
        "Anton Pryce and Hattie Lowe are both barely five feet.",
        "Father Corin was seen in the corridor at 12:50 am carrying something wrapped in cloth.",
        "Vera Sokol took a sleeping draught at 11 pm. The conductor looked in at 1:00 and 1:30 "
        "and found her fast asleep, her door chained from inside.",
        "From 1:00 to 1:45 am Father Corin was playing chess with the conductor in the "
        "conductor's cabin. The unfinished game is still on the board.",
    ),
    killer="Reuben Stroud",
    genre="Murder on a train",
    level=5,
    red_herrings=(3, 5),
)

LADDER: tuple[Case, ...] = (
    MISSING_LOCKET,
    LIGHTHOUSE,
    CLOCKMAKER,
    BONE_ROOM,
    SEALED_ARCHIVE,
    WINTER_OF_89,
    NIGHT_TRAIN,
)
"""The cases of a run, in play order, from lightest to hardest."""


def choose_case(rng: random.Random | None = None) -> Case:
    """Pick one of the round-1 classic cases at random."""
    return (rng or random).choice(CASES)
