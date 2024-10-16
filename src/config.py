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
        self.__output__: dict[str, Any] = {"files": [], "output": "bundle.py", "fix-escape": False}
        self._setup()
        self._code = code

    def _setup(self):
        self.tcl.createcommand("packadd", self.packadd)
        self.tcl.createcommand("set-output", self.set_output)
        self.tcl.createcommand("fix-escape", self.fix_escape)

    def set_output(self, new_path: str):
        self.__output__["output"] = new_path

    def fix_escape(self):
        self.__output__["fix-escape"] = True

    def packadd(self, file):
        self.__output__["files"].append(ResourceScheme(file))

    @property
    def config(self):
        self.tcl.eval(self._code)
        return self.__output__
