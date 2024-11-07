from pathlib import Path
from src.config import ConfigLoader  # pack: ignore
from src.buff import Buffer  # pack: ignore
from Lib.BaseUi import Title, get_logger, Padding, Notification, fg  # pack: ignore
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
        log.error("Config", f"{config_path} not found or is a directory.")
        return

    cl = ConfigLoader(config_path.read_text())
    cfg = cl.config

    buffs: list[Buffer] = []

    for file in cfg.get("files", []):
        new = Buffer(Path(file.path).read_text(), file.fn)

        buffs.append(new)

    result: str = ""
    for buff in buffs:
        if cfg.get("add-comment-helper", False):
            result += f"\n#{Padding.center(f"[ file: {buff.fn!r} ]")}#\n"
        for line in buff.string.splitlines():
            no_space = line.replace(" ", "")
            if "pack:ignore" in no_space and not ("pack:escape" in no_space): #pack: escape
                log.info("Bundler", f"removing `{line=}` from the final bundle.")
                continue
            if "pack:escape" in no_space:
                if cfg.get("fix-escape", False):
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
                    match input(fg.cyan("[Enter/edit] Continue? ")).lower():
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
                except KeyboardInterrupt:
                    pass
                print()
            result += line + "\n"

    try:
        Path(cfg.get("output")).write_text(result)  # pyright: ignore
    except Exception as err:
        log.error("Save()", repr(err))
    log.info("Writer", f"done writing the bundle to {cfg.get("output")=}.")

    return


if __name__ == "__main__":
    main(sys.argv, len(sys.argv))
# end main
