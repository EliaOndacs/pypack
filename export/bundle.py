
#     [ file: 'BaseUiThemes.py' ]     #
from typing import Any
from ansi.colour import fg

#simulate [copy and paste] BaseUi `Style` object 
class Style:
    def __init__(self, options: dict[str, Any]):
        self.__data__: dict[str, Any] = options
        self.get = self.__data__.get

    def __repr__(self):
        return f"[object of 'Style' id: {hex(id(self))!r} size: {self.__sizeof__()!r}]"

    def __setitem__(self, key, value):
        self.__data__[key] = value

    def __getitem__(self, key):
        return self.__data__[key]

smooth_cute = Style({
    'ascii_border': '─',
    'border_vertical_char': '│',
    'ProgressBar.left': '[',
    'ProgressBar.right': ']',
    'ProgressBar.tip': '>',
    'ProgressBar.lineOff': ' ',
    'ProgressBar.lineOn': '=',
    'ProgressBar.color:on': fg.yellow,
    'DataTable.seperator': '│',
    'DataTable.right': '│',
    'DataTable.left': '│',
    'Bar.seperator': ':',
    'Chain.left': '{',
    'Chain.right': '}',
    'Chain.seperator': '~',
    'Ruler.begin': '/',
    'Ruler.end': '>',
    'Ruler.line': '-',
    'List.override_index': True,
    'Compersition.not_equal': '!=',
    'Notification.left': '(',
    'Notification.right': ')',
})


# note: this requires nerdfont
so_nerdy = Style({
    'ProgressBar.left': '\uf104',
    'ProgressBar.right': ' \uf105',
    'ProgressBar.tip': ' \ueabc',
    'ProgressBar.lineOff': '\uf45b',
    'ProgressBar.lineOn': '\uf45b',
    'ProgressBar.color:on': fg.magenta,
    'DataTable.seperator': '\udb84\udef1',
    'DataTable.right': '\udb84\udef1',
    'DataTable.left': '\udb84\udef1',
    'Bar.seperator': '\uf142',
    'Chain.left': '\ue0b7',
    'Chain.right': '\ue0b5',
    'Chain.seperator': '-',
    'Ruler.begin': '\ue0b6',
    'Ruler.end': '>',
    'Ruler.line': '-',
    'List.override_index': True,
    'Compersition.not_equal': '!=',
    'Notification.left': '\uf12a\ue0b7',
    'Notification.right': '\ue0b5',
})

minimal_space = Style({
    "ascii_border": '.',
    "border_vertical_char": ':',
    "ProgressBar.left": ' ',
    "ProgressBar.right": ' ',
    "ProgressBar.tip": '>',
    "ProgressBar.lineOn": '-',
    "ProgressBar.lineOff": ' ',
    "ProgressBar.color:on": fg.grey,
    "DataTable.seperator": ' : ',
    "DataTable.left": ' ',
    "DataTable.right": ' ',
    "Bar.seperator": '%',
    "Chain.left": " ",
    "Chain.right": " ",
    "Chain.seperator": "-",
    "Select.promptText": ':',
    "Ruler.begin": " ",
    "Ruler.end": ">",
    "Ruler.line": "-",
    "Mark.off": " ",
    "Mark.on": "*",
    "Compersition.not_equal": "!=",
    "Notification.left": "|",
    "Notification.right": "|",
    "ImportanceText.fg": fg.red,
    "Paginator.left": " ",
    "Paginator.right": " ",
    "Input.promptText": ": "
})


#     [ file: 'BaseUi.py' ]     #
"""
**BaseUi**

the base ui library for a centralized theme cli ui among SysCoreutil & SysEnv

"""

from dataclasses import dataclass
from typing import (
    Any,
    Generator,
    Iterable,
    Literal,
    NamedTuple,
    Protocol,
    Callable,
    runtime_checkable,
)
from ansi.colour import *  # type: ignore
from enum import StrEnum
import sys


@runtime_checkable
class Renderable(Protocol):
    def __str__(self) -> str: ...


class Component(Renderable):
    
    def __init__(self, states: dict[str, Any]) -> None:
        self.states = states

    def compose(self) -> Generator["Renderable|Component"]:
        yield from ()

    @property
    def package(
        self,
    ) -> Generator["Renderable|Component", None, None]:
        yield from self.compose()

    def render(self):
        result = ""
        for item in self.package:
            if isinstance(item, Renderable):
                result += str(item)
            elif isinstance(item, Component):
                result += str(item)

        return result

    def __str__(self):
        return self.render()


class codes(StrEnum):
    CLEAR = "\x1b[h\x1b[2J"


class Style:
    "style object for all styles of all components"

    def __init__(self, options: dict[str, Any]):
        self.__data__: dict[str, Any] = options
        self.get = self.__data__.get

    def __repr__(self):
        return f"[object of 'Style' id: {hex(id(self))!r} size: {self.__sizeof__()!r}]"

    def __setitem__(self, key, value):
        self.__data__[key] = value

    def __getitem__(self, key):
        return self.__data__[key]


AT_STYLE = "Style"
AT_DISPLAY = "Display"


def make_auto(_type, instance):
    "turn an object to an auto object"
    if _type == "Style":
        globals()["@auto[style]"] = instance
        return
    elif _type == "Display":
        globals()["@auto[display]"] = instance
        return

    raise TypeError(f"type {_type!r} it not supported as an auto object!")


def get_style(style: Style | None):
    "get the the auto style if exists or None or the past style pram"
    if style:
        return style
    if "@auto[style]" in globals():
        return globals()["@auto[style]"]


def get_display(display: "Display|None"):
    "get the auto display if exists or None or the past display pram"
    if display:
        return display
    if "@auto[display]" in globals():
        return globals()["@auto[display]"]


class Animation:
    "Base Object For All Animations"

    class Frame:
        def __init__(self, text: str) -> None:
            self.text: str = text

    @classmethod
    def FramesFromList(cls, frames: list[Any]) -> list["Animation.Frame"]:
        result = []
        for frame in frames:
            result.append(Animation.Frame(str(frame)))

        return result

    def __init__(self, frames: list["Animation.Frame"]) -> None:
        self.frames = frames
        self.frameI = 0

    def __iter__(self):
        return self

    def __next__(self):
        self.frameI += 1

    def __str__(self) -> str:
        return self.frames[self.frameI % len(self.frames)].text


class Measurements(NamedTuple):
    """Measurements of an text"""

    columns: int
    lines: int
    text: str

    @classmethod
    def measure(cls, text: str):
        "measure a text"
        l = text.split("\n")
        max_columns = len(max(l, key=len))
        return Measurements(max_columns, len(l), text)


class Block:
    """A Block Of Text (a multiline text)"""

    def __init__(self, raw: str) -> None:
        self._raw = raw  # very unsafe, but might be required later
        self.measurements = Measurements.measure(self._raw)
        self.text: list[str] = self._raw.split("\n")

    def render(self) -> Generator[str, None, None]:
        for line in self.text:
            yield line

    def __str__(self) -> str:
        return "\n".join(self.text)


#                    (ln   col)
type Position = tuple[int, int]


class Selection:
    def __init__(self, text: str, start: Position, end: Position):
        self.text = text
        self.start = start
        self.end = end

    def __str__(self) -> str:
        lines = self.text.splitlines()
        start_line, start_col = self.start
        end_line, end_col = self.end

        # Ensure the positions are within bounds
        if (
            start_line < 0
            or end_line < 0
            or start_line >= len(lines)
            or end_line >= len(lines)
        ):
            return ""

        if start_line == end_line:
            # Selection is within the same line
            return lines[start_line][start_col:end_col]

        # Selection spans multiple lines
        selected_text = []

        # Add the text from the start line
        selected_text.append(lines[start_line][start_col:])

        # Add the text from the lines in between
        for line in range(start_line + 1, end_line):
            selected_text.append(lines[line])

        # Add the text from the end line
        selected_text.append(lines[end_line][:end_col])

        return "\n".join(selected_text)


class Display:
    def __init__(self, inital: str = "", *, auto: bool = False):
        self.text = inital
        self._alive: bool = True
        if auto == True:
            make_auto(AT_DISPLAY, self)

    def __enter__(self):
        return self

    def __exit__(self, *args): ...

    def loop(self, hook: Callable[[], str]):
        while self._alive:
            self.update(hook())
            print(codes.CLEAR, end="")
            print(str(self), end="")

    def update(self, new: str):
        self.text = new

    def __str__(self) -> str:
        return self.text


def ParseCode(code: str):
    _code = code.encode()
    i = 0
    i += 1
    if _code[i] != 91:
        get_logger().error("ParseCode()", "invalid escape code!")
        return
    i += 1
    _prams = _code[i:].decode().split(";")
    mode = _prams[0]
    prams = _prams[1:]
    return mode, prams


def GenerateCode(mode: int, prams: list[Renderable]) -> str:
    _mode = f"\x1b[{mode}"
    _prams = ";".join(str(seg) for seg in prams)
    return f"{_mode}{_prams}"


def deleteText(text: str):
    return "\b" * len(text)


def ascii_border(text, style: Style | None = None):
    "make an ascii border around the `text`"
    style = get_style(style)
    lines = text.split("\n")
    max_len = max(len(line) for line in lines)
    if style:
        border_char = style.get("ascii_border", "-")
        border_vertical_char = style.get("border_vertical_char", "|")
    else:
        border_char = "-"
        border_vertical_char = "|"
    border = border_char * (max_len + 2)
    result = []
    for line in lines:
        bordered_line = (
            f"{border_vertical_char}{line.ljust(max_len)}{border_vertical_char}"
        )
        result.append(bordered_line)
    result.insert(0, border)
    result.append(border)
    return "\n".join(result)


def VerticalLabel(text: str):
    return "\n".join(list(text))


class ProgressBar:
    "ProgressBar Component"

    def __init__(
        self,
        default: int = 0,
        max: int = 100,
        size: int = 10,
        style: Style | None = None,
    ) -> None:
        self.value = default
        self.max = max
        self.style = get_style(style)
        self.size = size

    def update(self, amount: int = 1):
        self.value += amount

    def reset(self):
        self.value = 0

    def __str__(self):
        result = ""
        if self.style:
            left = self.style.get("ProgressBar.left", "<")
            right = self.style.get("ProgressBar.right", ">")
            tip = self.style.get("ProgressBar.tip", "o")
            line_off = self.style.get("ProgressBar.lineOff", "-")
            line_on = self.style.get("ProgressBar.lineOn", "-")
            on_color = self.style.get("ProgressBar.color:on", fg.cyan)
            off_color = self.style.get("ProgressBar.color:off", fg.grey)
        else:
            left = "<"
            right = ">"
            tip = "o"
            line_on = "-"
            line_off = "-"
            on_color = fg.cyan
            off_color = fg.grey
        amount_filled: int = self.value * self.size // self.max
        for i in range(amount_filled):
            result += (
                (on_color + tip) if i == (amount_filled - 1) else (on_color + line_on)
            )
        result += (off_color + line_off) * (self.size - amount_filled)

        return f"{left}{result}{right}\x1b[0m"


class Spinner:
    "Spiner Component (Composition `Animation` object with an default animation)"

    def _get_default_animation(self) -> Animation:
        return Animation(
            Animation.FramesFromList(["|", "/", "─", "\\", "|", "/", "─", "\\"])
        )

    def __init__(self, animation: None | Animation = None) -> None:
        self.animation: "Animation" = animation if animation != None else self._get_default_animation  # type: ignore

    def __iter__(self):
        return self

    def __next__(self):
        next(self.animation)

    def __str__(self):
        return str(self.animation)


class DataTable:
    "DataTable component"

    class Column:
        "A Column Object For DataTable.Row"

        def __init__(self, text: str) -> None:
            self.text = text

        def __str__(self):
            return self.text

    class Row:
        "A Row Object for DataTable"

        def __init__(self, *cols) -> None:
            self.cols = cols

    def __init__(self, style: Style | None = None) -> None:
        self.data: list["DataTable.Row"] = []
        self.style = get_style(style)

    def add_row(self, row: "DataTable.Row"):
        self.data.append(row)

    def __str__(self):
        result = ""

        if self.style:
            seperator = self.style.get("DataTable.seperator", "|")
            left = self.style.get("DataTable.left", "[")
            right = self.style.get("DataTable.right", "]")
        else:
            seperator = "|"
            left = "["
            right = "]"

        for row in self.data:
            items = []
            for item in row.cols:
                items.append(str(item))

            result += f"{left}{f'{seperator}'.join(items)}{right}\n"

        return result


class Padding:
    "Adds Padding For strings"

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
    "SwitchText Atomic, allow you to switch between text on render"

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
    "Input Component (Only Fires When Try To Convert To A String And Will Return The UserInput)"

    def __init__(self, prompt: str = "", style: Style | None = None):
        self.prompt = prompt
        self.style = get_style(style)

    def __str__(self):
        if self.style:
            prompt = self.style.get("Input.promptText", "")
        else:
            prompt = ""
        return input(prompt)


class Title:
    "Title Desighn"

    def __init__(self, text: str):
        self.text = f"-[{text}]-"

    def __str__(self):
        return self.text


class Bar:
    "Bar Seperates Multiple Items In One Line"

    def __init__(
        self, *cols, style: Style | None = None, active: int | None = None
    ) -> None:
        self.cols = cols
        self.active = active
        self.style = get_style(style)

    def __str__(self):
        if self.style:
            sep = self.style.get("Bar.seperator", ">")
        else:
            sep = ">"
        if self.active and len(self.cols) <= self.active:
            self.cols = list(self.cols)
            self.cols[self.active] = fx.underline(self.cols[self.active])
        return f" {sep} ".join(self.cols)


class Icon:
    "Icon Desighn, An Icon For Diffrent Names"

    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self):
        return f"</{self.name.capitalize()}>"


class Chain:
    "Chain Desighn, A Chain For A Chain Of Values"

    def __init__(self, *cols, style: Style | None = None):
        self.cols = cols
        self.style = get_style(style)

    def __str__(self):
        result = ""

        if self.style:
            left = self.style.get("Chain.left", "(")
            right = self.style.get("Chain.right", ")")
            sep = self.style.get("Chain.seperator", "-")
        else:
            left = "("
            right = ")"
            sep = "-"

        for item in self.cols:
            result += f"{left}{item}{right}{sep}"

        return result[:-1]


class PrettyLogging:
    "Pretty Logging"

    def error(self, name, detail, use_stdout: bool = False):
        text = fg.red("ERROR") + " -> " + fg.cyan(name) + ": " + fg.gray(detail)
        if use_stdout == True:
            print(text)
            return
        sys.stderr.write(text + "\n")
        sys.stderr.flush()

    def warn(self, name, detail, use_stdout: bool = False):
        text = fg.yellow("WARN") + " -> " + fg.cyan(name) + ": " + fg.gray(detail)
        if use_stdout == True:
            print(text)
            return
        sys.stderr.write(text + "\n")
        sys.stderr.flush()

    def info(self, name, detail, use_stdout: bool = False):
        text = fg.blue("INFO") + " -> " + fg.cyan(name) + ": " + fg.gray(detail)
        if use_stdout == True:
            print(text)
            return
        sys.stderr.write(text + "\n")
        sys.stderr.flush()

    def debug(self, name, detail, use_stdout: bool = False):
        text = fg.green("DEBUG") + " -> " + fg.cyan(name) + ": " + fg.gray(detail)
        if use_stdout == True:
            print(text)
            return
        sys.stderr.write(text + "\n")
        sys.stderr.flush()


def get_logger() -> PrettyLogging:
    "if `global_logger` exsist it will just return ir, if not it will create and then remove it"
    if "global_logger" not in globals():
        globals()["global_logger"] = PrettyLogging()
        return globals()["global_logger"]
    else:
        return globals()["global_logger"]


class Pointer:
    "Four Directional Pointer Desighn"
    left: str = " "
    right: str = " "
    up: str = " "
    down: str = " "


def join_string(*objs: str):
    "joins multiple string by space"
    return " ".join(objs)


class Select:
    "MultiChoice Menu (Composition DataTable)"

    def __init__(self, choices: list[str], style: Style | None = None) -> None:
        self.dt = DataTable(style)
        self.choices = choices
        self.style = get_style(style)
        i = 0
        for choice in choices:
            self.dt.add_row(
                DataTable.Row(DataTable.Column(str(i)), DataTable.Column(choice))
            )
            i += 1

    def __str__(self):
        print(self.dt)
        while 1:
            if self.style:
                inp = input(self.style.get("Select.promptText", "> "))
            else:
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


class Br:
    "New Line Object"

    def __str__(self) -> str:
        return "\n"


class Ruler:
    "A Ruller Object that can display a length of numbers"

    def __init__(self, lenght: int, style: Style | None = None) -> None:
        self.lenght = lenght
        self.style = get_style(style)

    def __str__(self) -> str:
        result = ""

        if self.style:
            begin = self.style.get("Ruler.begin", "|")
            end = self.style.get("Ruler.end", ">")
            line = self.style.get("Ruler.line", "-")
            number_on_top: bool = self.style.get("Ruler.NumberOnTop?", False)
        else:
            begin = "|"
            end = ">"
            line = "-"
            number_on_top = False

        # the ruler it self

        if number_on_top == False:
            result += begin + (line * (self.lenght * 3)) + end + "\n"

        # the numbers

        for i in range(self.lenght + 1):
            result += str(i) + "  "
        result += "\n"

        if number_on_top == True:
            result += begin + (line * (self.lenght * 3)) + end + "\n"

        return result


# (4) point


class Mark:
    "A Mark For Behind A Text or An Option"
    _mode: bool
    _override_mode: None | tuple[str, str] = None

    def __init__(
        self, string: str, mode: bool = False, style: Style | None = None
    ) -> None:
        self.string = string
        self.style = get_style(style)
        self.mode = mode

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, new: bool):
        self._mode = new

    def __str__(self) -> str:
        if self.style:
            mark_on = self.style.get("Mark.on", "($)")
            mark_off = self.style.get("Mark.off", "( )")
        else:
            mark_on = "($)"
            mark_off = "( )"

        if self._override_mode:
            mark_on = self._override_mode[0]
            mark_off = self._override_mode[1]

        if self.mode:
            mark = mark_on
        else:
            mark = mark_off

        return f"{mark} {self.string}"


class List:
    "A List Displayt Of multiple items"

    def __init__(
        self, items: Iterable | list | tuple, style: Style | None = None
    ) -> None:
        self.style = get_style(style)
        self.items = items

    def __str__(self) -> str:
        result = ""
        if self.style:
            mode = self.style.get("List.Marker.mode", True)
        else:
            mode = True

        i = 0
        for item in self.items:
            m = Mark(item, mode, style=self.style)
            if self.style:
                if self.style.get("List.override_index", True):
                    m._override_mode = (f"{i}.", "undefined")
            result += f"{str(m)}\n"
            i += 1

        return result


class Compersition:
    "Show Relations between two object"

    def __init__(self, a, b, style: Style | None = None) -> None:
        self.a = a
        self.b = b
        self.style = get_style(style)

    def __str__(self):
        if self.style:
            not_equal = self.style.get("Compersition.not_equal", "<>")
        else:
            not_equal = "<>"
        result = ""
        if self.a == self.b:
            result += f"({self.a} == {self.b})" + " "
        if self.a != self.b:
            result += f"({self.a} {not_equal} {self.b})" + " "
        if self.a < self.b:
            result += f"({self.a} < {self.b})" + " "
        if self.a > self.b:
            result += f"({self.a} > {self.b})" + " "
        return result[:-1]


class Crop:
    "Adds Cropping to strings"

    @classmethod
    def line(cls, string: str, amount: int = 5, offset: int = 0):
        return string[offset:amount]

    @classmethod
    def text(
        cls,
        string: str,
        measurements: Measurements | None = None,
        amount: tuple[int, int] = (3, 5),
        offset: tuple[int, int] = (0, 0),
    ):
        if (
            measurements
        ):  # a lot of typing errors, but trust me, this works perfectly fine
            amount: list[int] = list(amount)
            amount[0] = measurements.lines
            amount[1] = measurements.columns
            amount: tuple[int, int] = tuple(amount)

        result = ""
        lines = string.splitlines()
        for li in range(len(string)):
            if li >= amount[0]:
                break
            if li + offset[0] >= len(lines):
                break
            result += Crop.line(lines[li + offset[0]], amount[1], offset[1]) + "\n"
            li += 1

        return result[:-1]


class Notification:
    "Notification Component"

    def __init__(
        self,
        message: str,
        severity: Literal["Error", "Info", "Warning"] | None = None,
        style: Style | None = None,
    ) -> None:
        self.message = message
        self.severity = severity
        self.style = get_style(style)

    def __str__(self):
        if self.style:
            err_bg = self.style.get("Notification.error_bg", bg.red)
            err_fg = self.style.get("Notification.error_fg", fg.black)
            info_bg = self.style.get("Notification.info_bg", bg.blue)
            info_fg = self.style.get("Notification.info_fg", fg.black)
            warn_bg = self.style.get("Notification.warn_bg", bg.yellow)
            warn_fg = self.style.get("Notification.warn_fg", fg.black)
            left = self.style.get("Notification.left", "[")
            right = self.style.get("Notification.right", "]")
            do_reset = self.style.get("Notification.reset", True)
        else:
            err_bg = bg.red
            err_fg = fg.black
            info_bg = bg.blue
            info_fg = fg.black
            warn_bg = bg.yellow
            warn_fg = fg.black
            left = "["
            right = "]"
            do_reset = True

        _bg = ""
        _fg = ""
        if self.severity != None:
            match self.severity:
                case "Error":
                    _bg = err_bg
                    _fg = err_fg
                case "Info":
                    _bg = info_bg
                    _fg = info_fg
                case "Warning":
                    _bg = warn_bg
                    _fg = warn_fg
        return f"{_bg}{_fg}{left}{self.message}{right}{'\x1b[0m' if do_reset else ''}"


def fill(text: str, desired_length: int, filler: str = " "):
    "fills the infront of the `text` with the `filler` to make the text the `desired_length`"
    if len(text) >= desired_length:
        return text
    amount = desired_length - len(text)
    return text + (filler * amount)


class Tree:
    "Tree Component"

    def __init__(self, items: list[str | list]) -> None:
        self.items = items

    def _visit_node(self, items: list[str | list], depth: int = 0):
        result = ""
        for item in items:
            if isinstance(item, str):
                result += "\n" + Padding.left(item, amount=(depth * 4))
            elif isinstance(item, list):
                result += Padding.left(self._visit_node(item, depth + 1))
        return result

    def __str__(self) -> str:
        return self._visit_node(self.items)


class Canvas:
    "Canavs Component"

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self._buffer: list[list[str]] = [
            [" " for __ in range(self.width)] for _ in range(self.height)
        ]

    def addstr(self, x: int, y: int, string: str):
        lines = string.split("\n")
        iy = 0
        for line in lines:
            self.addline(x, y + iy, line)
            iy += 1

    def addline(self, x: int, y: int, string: str):
        if len(string.split("\n")) > 1:
            raise ValueError(
                f"expected the string: {string!r}, would be only one line, found multiple instead!"
            )
        ix = 0
        for char in string:
            self.addpixel(x + ix, y, char)
            ix += 1

    def addpixel(self, x: int, y: int, char: str):
        if x >= self.width:
            x = x % self.width
        if x < 0:
            x = 0
        if y >= self.height:
            y = y % self.height
        self._buffer[y][x] = char

    def getpixel(self, x: int, y: int):
        if x >= self.width:
            x = x % self.width
        if x < 0:
            x = 0
        if y >= self.height:
            y = y % self.height
        return self._buffer[y][x]

    def __str__(self) -> str:
        result = ""
        for row in self._buffer:
            for col in row:
                result += Canvas.RuleOneChar(col)
            result += "\n"
        return result

    @classmethod
    def RuleOneChar(cls, string: str):
        "strip a string to only one char"
        return string[0]


class ImportanceText:
    def __init__(self, messages: str, style: Style | None = None) -> None:
        self.messages = messages
        self.style = get_style(style)

    def __str__(self) -> str:
        if self.style:
            wall_fg = self.style.get("ImportanceText.fg", fg.grey)
            wall_bg = self.style.get("ImportanceText.bg", "")
        else:
            wall_fg = fg.grey
            wall_bg = ""
        return (
            wall_fg
            + wall_bg
            + "{"
            + "\x1b[0m"
            + f" {self.messages} "
            + wall_fg
            + wall_bg
            + "}"
            + "\x1b[0m"
        )


class AnsiText:

    class Segment:
        def __init__(self, text: str, is_control: bool) -> None:
            self.text = text
            self.is_control = is_control

        def __len__(self):
            return len(self.text)

    def __init__(self, segments: list["AnsiText.Segment"]) -> None:
        self.segs = segments

    def __len__(self):
        result = 0
        for seg in self.segs:
            if seg.is_control:
                continue
            result += len(seg)
        return result

    def __str__(self):
        result = ""
        for seg in self.segs:
            result += seg.text
        return result


class FilesystemDeco:
    NormalFile = lambda filename: fg.yellow(filename)
    Directory = lambda filename: fg.blue(filename)
    Executable = lambda filename: fg.red(filename) + fg.grey("*")


class Paginator:
    def __init__(
        self,
        default_page: int = 1,
        amount_of_pages: int = 5,
        style: Style | None = None,
    ) -> None:
        self.pages: int = amount_of_pages
        self.pageN = default_page + 1
        self.style = get_style(style)

    def __str__(self):
        if self.style:
            left = self.style.get("Paginator.left", "[")
            right = self.style.get("Paginator.right", "]")
            active_page = self.style.get("Paginatio.active", "o")
            unactive_page = self.style.get("Paginator.unactive", ".")
        else:
            left = "["
            right = "]"
            active_page = "o"
            unactive_page = "."
        result = left
        for i in range(self.pages):
            if i == (self.pageN % self.pages):
                result += active_page
            else:
                result += unactive_page
        return result + right


def Compose(items: list[Renderable]) -> str:
    return "\n".join(*[str(obj) for obj in items])


class Page(Renderable):
    def __init__(self, content: str, db: dict[str, Any] | None = {}) -> None:
        if not (db):
            db = {}
        self.db: dict[str, Any] = db
        self.content = content

    def __str__(self) -> str:
        result = self.content
        for key in self.db:
            value = self.db[key]
            result = result.replace(f";{key};", value)
        return result


class Scene(Renderable):
    def __init__(self, pages: list[Page]) -> None:
        self.pages = pages
        self.current_page = 1
        self.paginator = Paginator(self.current_page, len(self.pages))

    def __str__(self) -> str:
        self.paginator.pageN = self.current_page
        print(
            (Measurements.measure(str(self.pages[self.current_page])).columns + 2) * "_"
        )
        print(str(self.pages[self.current_page]))
        print(
            (Measurements.measure(str(self.pages[self.current_page])).columns + 2) * "_"
        )
        print(Padding.center(str(self.paginator)))
        _pagen: str = input("/")
        if _pagen == "q":
            return ""
        pagen = int(_pagen)
        self.current_page = pagen
        str(self)
        return ""


#     [ file: 'ecl.py' ]     #
from shlex import shlex
from dataclasses import dataclass
from typing import Any

@dataclass
class Flag:
    name: str

    def __repr__(self) -> str:
        return f"Flag('-{self.name}')"

@dataclass
class Data[T]:
    value: T

    def __repr__(self) -> str:
        return str(self.value)

class String(Data[str]):
    ...
class Integer(Data[int]):
    ...
class Boolean(Data[bool]):
    ...
class Word(Data[str]):
    ...

@dataclass
class Command:
    name: str

type action = tuple[Command, list[String | Integer | Boolean | Flag | Word ]]

def parse_line(line: str) -> action|None:
    parser = shlex(line, punctuation_chars=True)
    tokens: list = []
    name = parser.get_token()
    if not (name):
        return None
    tokens.append(Command(name))
    arguments: list[String | Integer | Boolean | Flag | Word ] = []
    for arg in parser:
        if arg[0] == "-":
            arguments.append(Flag(arg[1:]))
            continue
        if arg.isdigit():
            arguments.append(Integer(int(arg)))
            continue
        if arg == "true":
            arguments.append(Boolean(True))
            continue
        if arg == "false":
            arguments.append(Boolean(False))
            continue
        if arg[0] == '"':
            string = arg[1:-1]
            arguments.append(String(string))
            continue
        arguments.append(Word(arg))
    tokens.append(arguments)
    return tokens[0], tokens[1]


def parse(text: str) -> list[action]:
    result: list[action] = []
    for line in text.splitlines():
        cmd = parse_line(line)
        if cmd:
            result.append(cmd)
    return result


def execute_line(action, scope: dict[str, Any]):

    command = action[0]
    prams = action[1]

    match command.name:
        case "set":
            if not(isinstance(prams[0], Word)):
                print(f"|    error: expected an variable name!\n|    got {type(prams[0]).__name__!r} instead!")
                exit()
            scope[prams[0].value] = prams[1]

        case "print":
            if isinstance(prams[0], Word):
                print(scope.get(prams[0].value, "undefined"))
            else:
                print(prams[0].value)

        case _:
            if command.name in scope:
                scope = scope[command.name](scope, *prams)
    return scope

def execute(ast: list[action], scope: dict[str, Any]|None):
    scope = scope or {}
    for line in ast:
        scope = execute_line(line, scope) # type: ignore
    return scope

def program(text: str, *, default_scope: dict[str, Any]|None = None):
    ast = parse(text)
    result = execute(ast, default_scope)
    return result

#     [ file: 'buff.py' ]     #
from dataclasses import dataclass
from pathlib import Path
from pprint import pprint
import sys
from tkinter import Tcl
from typing import Any



log = get_logger()


@dataclass()
class Buffer:
    string: str
    fn: Path

    def ignore(self, ignores: list[tuple[str, int]]):
        for batch in ignores:
            p = Path(batch[0]).name
            log.debug("Buffer()->ignore", f"{p==self.fn}, {self.fn=}, {p=}")
            if p == self.fn:
                line = batch[1]
                print(f"{line=} {type(line)=}")
                # log.debug("Buffer()->ignore", f"{self.string.splitlines()[line]=}")
                log.info("Bundler", f"removing `{line=}` from the file {batch[0]!r}")
                # n = self.string.splitlines()
                # del n[batch[1]]
                # self.string = "\n".join(n)


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


def handle_channel(channels: list[str], dir: Path) -> int | list[BuildSchedule]:
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

#     [ file: 'config.py' ]     #
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal
from tkinter import Tcl

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
            "ignores": [],
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
            "Ignore": self.ignore_ecl
        }

    def _setup_tcl(self):
        self.tcl = Tcl()
        self.tcl.createcommand("packadd", self.packadd)
        self.tcl.createcommand("set-output", self.set_output)
        self.tcl.createcommand("fix-escape", self.fix_escape)
        self.tcl.createcommand("add-comment-helper", self.add_comment_helper)
        self.tcl.createcommand("use-breakpoint", self.use_breakpoint)
        self.tcl.createcommand("create-channel", self.create_channel)
        self.tcl.createcommand("ignore", self.ignore)

    def ignore(self, file: str, line: int):
        if ResourceScheme(file) not in self.__output__["files"]:
            logger.warn("Config()->ignore", f"file {file!r} not found in the packed files. (skiping)")
            return
        print(f"ignore [ {file=} {line=} ]")
        self.__output__["ignores"].append((file, line))

    def ignore_ecl(self, scope, file: String, line: Integer):
        if ResourceScheme(file.value) not in self.__output__["files"]:
            logger.warn("Config()->ignore", f"file {file.value!r} not found in the packed files. (skiping)")
            return
        self.__output__["ignores"].append((file.value, line.value))
        return scope

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

#     [ file: 'main.py' ]     #
from pathlib import Path
import sys
import shutil

help_description: str = rf"""

{fg.yellow}
                              _
_ __  _   _ _ __   __ _ __   | | __
| '_ \| | | | '_ \ / _` |/ __| |/ /
| |_) | |_| | |_) | (_| | (__|   <
| .__/ \__, | .__/ \__,_|\___|_|\_\
|_|    |___/|_|

{'\x1b[0m'}
{Padding.center(str(Title(fg.red(" pypack is a bundler for python "))))}
"""

make_auto(AT_STYLE, minimal_space)


def main(argv: list[str], argc: int):

    log = get_logger()

    cwd = Path(".")

    if argc >= 2:
        if "--help" in argv:
            print(help_description)
            print()
            return
        cwd = Path(argv[-1])
        if not (cwd.exists()):
            log.warn("MetadataLoader", f"file {argv[-1]!r} does not exists!")
            cwd = Path(".")

    if (cwd / "pypack.cfg.ecl").exists():
        config_path = cwd / "pypack.cfg.ecl"
        if not (config_path.is_file()):
            log.error("Config", f"file {config_path} is an directory.")
            return
    elif (cwd / "pypack.cfg.tcl").exists():
        config_path = cwd / "pypack.cfg.tcl"
        if not (config_path.is_file()):
            log.error("Config", f"file {config_path} is an directory.")
            return
    else:
        log.error("Config", "'./pypack.cfg.{ .tcl, .ecl }' not found.")
        return

    channel_folder = cwd / "pack"
    if not (channel_folder.is_dir()) and channel_folder.exists():
        log.error("Config", "invalid channel directory 'pack/'")
        return

    cm = "tcl" if config_path.suffix[1:] == "tcl" else "ecl"
    cl = ConfigLoader(config_path.read_text(), cm)
    cfg = cl.config

    if channel_folder.exists():
        build_schedule = handle_channel(cfg["channels"], channel_folder)

        if build_schedule == -1:
            log.error("BuildSchedule", "Failed Due To A Channel Non-Existing!")
            return

    buffs: list[Buffer] = []

    for file in cfg.get("files", []):
        p = Path(file.path)
        if not (p.exists()):
            log.warn("FileLoader", f"file {file.path!r} not found! skipping.")
            continue
        new = Buffer(Path(file.path).read_text(), file.fn)
        buffs.append(new)

    result: str = ""
    for buff in buffs:
        if cfg.get("add-comment-helper", False):
            result += f"\n#{Padding.center(f"[ file: {buff.fn!r} ]")}#\n"
        for line in buff.string.splitlines():
            no_space = line.replace(" ", "")
            if "pack:ignore" in no_space and not (  # pack: escape
                "pack:escape" in no_space
            ):  # pack: escape
                log.info("Bundler", f"removing `{line=}` from the final bundle.")
                continue
            buff.ignore(cfg.get("ignores", []))
            if "pack:escape" in no_space:
                if cfg.get("fix-escape", False):  # pack: escape
                    line = line.replace("\\", "\\\\")
                log.warn("Bundler", f"escaping `{line=}`.")
            if (
                "pack:breakpoint" in no_space  # pack: escape
                and cfg.get("use-breakpoint")
                and not ("pack:escape" in no_space)
            ):
                print(Notification("Breakpoint Hit!", severity="Info"))
                print(f"Current Line: {line!r}")
                try:
                    match input(fg.cyan("[Enter/edit/remove] Continue? ")).lower():
                        case "edit" | "e":
                            try:
                                line = input("Please Enter New Content\n-> ")
                            except KeyboardInterrupt:
                                print(
                                    Notification(
                                        "KeyboardInterrupt!", severity="Warning"
                                    )
                                )
                                pass
                        case "enter" | "c":
                            pass
                        case "remove" | "r" | "dd":
                            line = "# [This Line Was Deleted]"
                except KeyboardInterrupt:
                    pass
                print()
            result += line + "\n"

    try:
        (cwd / Path(cfg.get("output"))).write_text(result)  # pyright: ignore
    except Exception as err:
        log.error("Save()", repr(err))
    log.info("Writer", f"done writing the bundle to {cfg.get("output")=}.")
    if channel_folder.exists():
        log.info("PostBuilder", "Starting Build.")
        if isinstance(build_schedule, int):  # pyright: ignore
            return

        def copy_file(_in: Path, out: Path):
            _in.write_text(out.read_text())

        if not ((cwd / "build").exists()):
            (cwd / "build").mkdir()

        for sched in build_schedule:  # pyright: ignore
            log.info("PostBuilder", f"building channel {sched.dir.name!r}")
            dest = (cwd / "build") / sched.dir.name
            dest.mkdir(exist_ok=True)
            for file in sched.files:
                log.info("PostBuilder", f"Copying File: {file!r}")
                _f = Path(sched.dir / file)
                copy_file(dest / file, _f)

        log.info("PostBuilder", "Build Complete.")

    return


if __name__ == "__main__":
    main(sys.argv, len(sys.argv))
# end main
