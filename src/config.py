from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal
from tkinter import Tcl
from Lib.ecl import *  # pack: ignore
from Lib.BaseUi import get_logger # pack: ignore

logger = get_logger()

@dataclass()
class ResourceScheme:
    path: str

    @property
    def fn(self) -> str:
        return Path(self.path).name


class ConfigLoader:
    def __init__(self, code: str, mode: Literal["tcl", "ecl"]) -> None:
        self.__output__: dict[str, Any] = {
            "files": [],
            "output": "bundle.py",
            "fix-escape": False,
            "add-comment-helper": False,
            "use-breakpoint": False,
            "channels": [],
        }
        self.mode = mode
        if self.mode == "tcl":
            self._setup_tcl()
        if self.mode == "ecl":
            self._setup_ecl()
        self._code = code

    def _setup_ecl(self):
        self.pylibs = {
            "Packadd": self.packadd_ecl,
            "SetOutput": self.set_output_ecl,
            "FixEscape": self.fix_escape_ecl,
            "AddCommentHelper": self.add_comment_helper_ecl,
            "UseBreakpoint": self.use_breakpoint_ecl,
            "CreateChannel": self.create_channel_ecl,
        }

    def _setup_tcl(self):
        self.tcl = Tcl()
        self.tcl.createcommand("packadd", self.packadd)
        self.tcl.createcommand("set-output", self.set_output)
        self.tcl.createcommand("fix-escape", self.fix_escape)
        self.tcl.createcommand("add-comment-helper", self.add_comment_helper)
        self.tcl.createcommand("use-breakpoint", self.use_breakpoint)
        self.tcl.createcommand("create-channel", self.create_channel)

    def set_output(self, new_path: str):
        self.__output__["output"] = new_path

    def set_output_ecl(self, scope, new_path: String):
        self.__output__["output"] = new_path.value
        return scope

    def create_channel(self, name: str):
        self.__output__["channels"].append(name)

    def create_channel_ecl(self, scope, name: String):
        self.__output__["channels"].append(name.value)
        return scope

    def fix_escape(self):
        self.__output__["fix-escape"] = True

    def fix_escape_ecl(self, scope):
        self.__output__["fix-escape"] = True
        return scope

    def add_comment_helper(self):
        self.__output__["add-comment-helper"] = True

    def add_comment_helper_ecl(self, scope):
        self.__output__["add-comment-helper"] = True
        return scope

    def use_breakpoint(self):
        self.__output__["use-breakpoint"] = True

    def use_breakpoint_ecl(self, scope):
        self.__output__["use-breakpoint"] = True
        return scope

    def packadd(self, file, PriortyIndex: int | None = None):
        if PriortyIndex and isinstance(PriortyIndex, int):
            self.__output__["files"].insert(PriortyIndex, ResourceScheme(file))
            return
        self.__output__["files"].append(ResourceScheme(file))

    def packadd_ecl(self, scope, file: String, PriortyIndex: Integer | None = None):
        if PriortyIndex and isinstance(PriortyIndex, Integer):
            self.__output__["files"].insert(
                PriortyIndex.value, ResourceScheme(file.value)
            )
            return
        self.__output__["files"].append(ResourceScheme(file.value))
        return scope

    @property
    def config(self):
        if self.mode == "tcl":
            self.tcl.eval(self._code)
        if self.mode == "ecl":
            program(self._code, default_scope=self.pylibs)
        return self.__output__
