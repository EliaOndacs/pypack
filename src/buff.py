from dataclasses import dataclass
from pathlib import Path
from pprint import pprint
import sys
from tkinter import Tcl
from typing import Any


from Lib.BaseUi import get_logger  # pack: ignore

log = get_logger()


@dataclass()
class Buffer:
    string: str
    fn: Path


def join(buffs: list[Buffer], new_fn: str = "@bundle"):
    string = ""
    for buff in buffs:
        string += buff.string + "\n"

    return Buffer(string, Path(new_fn))


@dataclass()
class BuildSchedule:
    dir: Path
    files: list[str]


class BSConfigLoader:
    def __init__(self, code: str) -> None:
        self.tcl = Tcl()
        self.__output__: dict[str, Any] = {"files": []}
        self._setup()
        self._code = code

    def _setup(self):
        self.tcl.createcommand("include-file", self.include_file)

    def include_file(self, path: str):
        self.__output__["files"].append(path)

    @property
    def config(self):
        self.tcl.eval(self._code)
        return self.__output__


def _make_schedule(channel: Path):
    config = channel / "channel.cfg.tcl"
    if not (config.exists):
        log.error("ChannelConfigLoader", f"config {config} not found!")
        sys.exit()

    text = config.read_text()
    cl = BSConfigLoader(text)
    return BuildSchedule(channel, cl.config["files"])


def handle_channel(channels: list[str], dir: Path) -> int|list[BuildSchedule]:
    paths = []
    for channel in channels:
        _p = dir / channel
        if not (_p.exists()):
            return -1
        paths.append(_p)

    r = []
    for channel in paths:
        r.append(_make_schedule(channel))
    pprint(r)
    return r
