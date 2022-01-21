from pathlib import Path


def appendID(filename: str, id: str) -> str:
    # https://stackoverflow.com/a/37487898
    p = Path(filename)
    return "{0}_{2}{1}".format(Path.joinpath(p.parent, p.stem), p.suffix, id)
