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
"""
**BaseUi**

the base ui library for a centerlised theme cli ui among SysCoreutil & SysEnv

"""

from typing import Any, Callable, Generator, Literal, NamedTuple, overload
from ansi.colour import *  # type: ignore
import sys


def ascii_border(text):
    lines = text.split("\n")
    max_len = max(len(line) for line in lines)
    border_char = "-"
    border = border_char * (max_len + 4)
    result = []
    for line in lines:
        bordered_line = f"| {line.ljust(max_len)} |"
        result.append(bordered_line)
    result.insert(0, border)
    result.append(border)
    return "\n".join(result)


class ProgressBar:
    def __init__(self, default: int = 0, max: int = 100, size: int = 10) -> None:
        self.value = default
        self.max = max
        self.size = size

    def update(self, ammount: int = 1):
        self.value += ammount

    def reset(self):
        self.value = 0

    def __str__(self):
        result = ""
        ammount_filled: int = self.value * self.size // self.max
        for i in range(ammount_filled):
            result += fg.cyan("o") if i == (ammount_filled - 1) else fg.cyan("-")
        result += fg.gray("-") * (self.size - ammount_filled)

        return f"<{result}>"


class Spinner:

    class SpinnerAnimation(NamedTuple):
        frames: list[str]

    default_animation = SpinnerAnimation(
        ["(|)", "(/)", "(─)", "(\\)", "(|)", "(/)", "(─)", "(\\)"]
    )

    def __init__(self, animation: None | SpinnerAnimation = None) -> None:
        self.animation: "Spinner.SpinnerAnimation" = animation if animation != None else self.default_animation  # type: ignore
        self.frame: int = 0

    def __iter__(self):
        return self

    def __next__(self):
        self.frame += 1
        return

    def __str__(self):
        result = self.animation.frames[self.frame % len(self.animation.frames)]

        return f"{result}"


class DataTable:

    class Column:
        def __init__(self, text: str) -> None:
            self.text = text

        def __str__(self):
            return self.text

    class Row:
        def __init__(self, *cols) -> None:
            self.cols = cols

    def __init__(self) -> None:
        self.data: list["DataTable.Row"] = []

    def add_row(self, row: "DataTable.Row"):
        self.data.append(row)

    def __str__(self):
        result = ""

        for row in self.data:
            items = []
            for item in row.cols:
                items.append(str(item))

            result += f"[{"| ".join(items)}]\n"

        return result


class Padding:
    @classmethod
    def left(cls, text: str, amount: int = 5):
        return (" " * amount) + text

    @classmethod
    def right(cls, text: str, amount: int = 5):
        return text + (" " * amount)

    @classmethod
    def center(cls, text: str, Amount: int = 5):
        return Padding.left(Padding.right(text, amount=Amount), amount=Amount)

    @classmethod
    def up(cls, text: str, amount: int = 1):
        return ((" " * len(text) + "\n") * amount) + text

    @classmethod
    def down(cls, text: str, amount: int = 1):
        return text + ((" " * len(text) + "\n") * amount)

    @classmethod
    def middle(cls, text: str, amount: int = 1):
        return Padding.down(Padding.up(text, amount=amount), amount=amount)

    @classmethod
    def complete(cls, text: str, amount: tuple[int, int] = (5, 1)):
        return Padding.middle(Padding.center(text, Amount=amount[0]), amount=amount[1])


class SwitchText:
    def __init__(self, text_a: str, text_b: str):
        self.text_a = text_a
        self.text_b = text_b
        self.switch: Literal[0, 1] = 0

    def __str__(self):
        return self.text_a if self.switch == 0 else self.text_b

    def alternate(self):
        if self.switch == 0:
            self.switch = 1
        else:
            self.switch = 0

    def update(self, text: str):
        if self.switch == 0:
            self.text_a = text
        else:
            self.text_b = text


class Input:
    def __init__(self, prompt: str = ""):
        self.prompt = prompt

    def __str__(self):
        return input(self.prompt)


class Title:
    def __init__(self, text: str):
        self.text = f"-[{text}]-"

    def __str__(self):
        return self.text


class Bar:
    def __init__(self, *cols) -> None:
        self.cols = cols

    def __str__(self):
        return " > ".join(self.cols)


class Icon:
    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self):
        return f"</{self.name.capitalize()}>"


class Chain:
    def __init__(self, *cols):
        self.cols = cols

    def __str__(self):
        result = ""

        for item in self.cols:
            result += f"({item})-"

        return result[:-1]


class PrettyLogging:
    def error(self, name, detail):
        print(fg.red("ERROR") + " -> " + fg.cyan(name) + ": " + fg.gray(detail))

    def warn(self, name, detail):
        print(fg.yellow("WARN") + " -> " + fg.cyan(name) + ": " + fg.gray(detail))

    def info(self, name, detail):
        print(fg.blue("INFO") + " -> " + fg.cyan(name) + ": " + fg.gray(detail))


def get_logger() -> PrettyLogging:
    if "global_logger" not in globals():
        globals()["global_logger"] = PrettyLogging()
        return globals()["global_logger"]
    else:
        return globals()["global_logger"]


class Pointer:
    left: str = " "
    right: str = " "
    up: str = " "
    down: str = " "


def join_string(*objs: str):
    return " ".join(objs)


class AnsiCol:
    def __init__(self, controls: str) -> None:
        self.controls = controls


class Segment:

    def __init__(self, text: str, control: AnsiCol | None = None):
        self.text = text
        self.control = control

    def __len__(self):
        return len(self.text)

    def __str__(self):
        return "".join(list(self._render()))

    def _render(self):
        if self.control:
            yield self.control.controls  # type: ignore
        yield self.text
        yield "\x1b[0m"


class Text:

    def __init__(self, text: str | list[Segment]) -> None:
        if isinstance(text, str):
            result = []
            for line in text.split("\n"):
                result.append(Segment(line))
            self.segments: list[Segment] = result
        else:
            self.segments: list[Segment] = text

    def __str__(self) -> str:
        result = ""
        for seg in self.segments:
            result += seg.__str__() + "\n"
        return result

    def apply(self, func: Callable[[str], str]):
        for line in self.segments:
            line.text = func(line.text)


class Select:
    def __init__(self, choices: list[str]) -> None:
        self.dt = DataTable()
        self.choices = choices
        i = 0
        for choice in choices:
            self.dt.add_row(
                DataTable.Row(DataTable.Column(str(i)), DataTable.Column(choice))
            )
            i += 1

    def __str__(self):
        print(self.dt)
        while 1:
            inp = input("> ")
            try:
                result = self.choices[int(inp)]
                break
            except KeyboardInterrupt:
                get_logger().info("Select", "Canceled By The User.")
                sys.exit(-1)
            except:
                get_logger().error(
                    "SelectionError",
                    "input value is not an number or out of range. try again",
                )

        return result  # type: ignore


class MenuBar:

    def __init__(self, *options):
        self.options = options

    def __str__(self) -> str:
        result = Bar(*self.options)
        return str(result).replace(">", "|")


class Widget:
    def __str__(self) -> str: ...


class Styler:
    def __init__(self) -> None:
        self.styles = {}

    def set_styles(self, styles: dict):
        self.styles = styles

    def separate_by_line(self, text: str):
        return text.split("\n")

    def __call__(self, text: str, **kwds):
        _text: list[str] = self.separate_by_line(text)
        result: list[str] = []

        for segment in _text:
            new = segment

            if "padding" in self.styles:
                new = Padding.complete(new, self.styles["padding"])
            if "color" in self.styles:
                new = rgb.rgb256(*self.styles["color"]) + new
            if "background" in self.styles:
                new = rgb.rgb256(*self.styles["background"], bg=True) + new

            result.append(new)

        return "\n".join(result)


class Br:
    def __str__(self) -> str:
        return "\n"


class UiBase:

    STYLE: dict[str, Any] = {}
    mounted: bool = False

    @overload
    def compose(self) -> Generator["Widget", None, None]: ...

    def on_render(self, string: str) -> str:
        return string

    def _pack(self):
        items = list(self.compose())
        return map(str, items)

    def init(self): ...

    def render(self):
        if self.mounted == False:
            self.mounted = True
            self.init()
        styler = Styler()
        styler.set_styles(self.STYLE)
        for string in self._pack():
            print(styler(self.on_render(string)), end="")

    def clean(self):
        print("\x1b[H\x1b[2J", end="")

from pathlib import Path
import sys

help_description: str = rf"""

                              _
 _ __  _   _ _ __   __ _  ___| | __
| '_ \| | | | '_ \ / _` |/ __| |/ /
| |_) | |_| | |_) | (_| | (__|   <
| .__/ \__, | .__/ \__,_|\___|_|\_\
|_|    |___/|_|


{Padding.center(str(Title("pypack is a bundler for python")))}
"""

def main(argv: list[str], argc: int):

    if argc >= 2:
        if "--help" in argv:
            print(help_description)
            print()
            return


    log = get_logger()

    cwd = Path(".")

    config_path = cwd / "pypack.cfg.tcl"

    if not (config_path.is_file()) or not (config_path.exists()):
        log.error("Config",f"{config_path} not found or is a directory.")
        return

    cl = ConfigLoader(config_path.read_text())
    cfg = cl.config

    buffs: list[Buffer] = []

    for file in cfg.get("files", []):
        new = Buffer(Path(file.path).read_text(), file.fn)

        buffs.append(new)

    result: str = ""
    for buff in buffs:
        for line in buff.string.splitlines():
            no_space = line.replace(" ", "")
            if "pack:ignore" in no_space and not ("pack:escape" in no_space):
                log.info("Bundler",f"removing `{line=}` from the final bundle.")
                continue
            if "pack:escape" in no_space:
                if cfg.get("fix-escape", False):
                    line = line.replace("\\", "\\\\")
                log.warn("Bundler", f"escaping `{line=}`.")
            result += line + "\n"

    try:
        Path(cfg.get("output")).write_text(result) # pyright: ignore
    except Exception as err:
        log.error("Save()", repr(err))
    log.info("Writer", f"done writing the bundle to {cfg.get("output")=}.")

    

    return


if __name__ == "__main__":
    main(sys.argv, len(sys.argv))
# end main
