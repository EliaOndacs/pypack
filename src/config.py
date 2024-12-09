from dataclasses import dataclass
from pathlib import Path
from typing import Any
from tkinter import Tcl


@dataclass()
class ResourceScheme:
    path: str

    @property
    def fn(self) -> str:
        return Path(self.path).name


class ConfigLoader:
    def __init__(self, code: str) -> None:
        self.tcl = Tcl()
        self.__output__: dict[str, Any] = {
            "files": [],
            "output": "bundle.py",
            "fix-escape": False,
            "add-comment-helper": False,
            "use-breakpoint": False,
            "channels": [],
        }
        self._setup()
        self._code = code

    def _setup(self):
        self.tcl.createcommand("packadd", self.packadd)
        self.tcl.createcommand("set-output", self.set_output)
        self.tcl.createcommand("fix-escape", self.fix_escape)
        self.tcl.createcommand("add-comment-helper", self.add_comment_helper)
        self.tcl.createcommand("use-breakpoint", self.use_breakpoint)
        self.tcl.createcommand("create-channel", self.create_channel)

    def set_output(self, new_path: str):
        self.__output__["output"] = new_path

    def create_channel(self, name: str):
        self.__output__["channels"].append(name)

    def fix_escape(self):
        self.__output__["fix-escape"] = True

    def add_comment_helper(self):
        self.__output__["add-comment-helper"] = True

    def use_breakpoint(self):
        self.__output__["use-breakpoint"] = True

    def packadd(self, file, PriortyIndex: int | None = None):
        if PriortyIndex and isinstance(PriortyIndex, int):
            self.__output__["files"].insert(PriortyIndex, file)
            return
        self.__output__["files"].append(ResourceScheme(file))

    @property
    def config(self):
        self.tcl.eval(self._code)
        return self.__output__
