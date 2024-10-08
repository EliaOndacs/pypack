from pathlib import Path
from src.config import ConfigLoader  # pack: ignore
from src.buff import Buffer  # pack: ignore
from Lib.BaseUi import get_logger # pack: ignore

def main():

    log = get_logger()

    cwd = Path(".")

    config_path = cwd / "pypack.cfg.tcl"

    if not (config_path.is_file()) or not (config_path.exists()):
        log.error("Config",f"{config_path} not found or is a directory.")
        return

    cl = ConfigLoader(config_path.read_text())
    cfg = cl.config

    buffs: list[Buffer] = []

    for file in cfg.get("files"):
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
                log.warn("Bundler", f"escaping `{line=}`.")
            result += line + "\n"

    Path(cfg.get("output")).write_text(result) # pyright: ignore
    log.info("Writer", f"done writing the bundle to {cfg.get("output")=}.")


    return


if __name__ == "__main__":
    main()
# end main
