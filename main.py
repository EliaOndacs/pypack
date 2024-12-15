from pathlib import Path
from src.config import ConfigLoader  # pack: ignore
from src.buff import Buffer, handle_channel  # pack: ignore
from Lib.BaseUi import *  # pack: ignore
from Lib.BaseUiThemes import minimal_space  # pack: ignore
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
