from dataclasses import dataclass
from pathlib import Path


@dataclass()
class Buffer:
    string: str
    fn: Path


def join(buffs: list[Buffer], new_fn: str = "@bundle"):
    string = ""
    for buff in buffs:
        string += buff.string + "\n"

    return Buffer(string, Path(new_fn))
