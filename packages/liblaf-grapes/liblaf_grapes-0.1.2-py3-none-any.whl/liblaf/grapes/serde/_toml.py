import os
from pathlib import Path
from typing import Any

from liblaf import grapes

with grapes.optional_imports(extra="toml"):
    import tomlkit


def load_toml(fpath: str | os.PathLike[str]) -> tomlkit.TOMLDocument:
    """Load a TOML file and return its contents as a TOMLDocument.

    Args:
        fpath: The file path to the TOML file.

    Returns:
        The contents of the TOML file as a TOMLDocument.
    """
    fpath: Path = Path(fpath)
    with fpath.open() as fp:
        return tomlkit.load(fp)


def save_toml(
    fpath: str | os.PathLike[str], data: Any, *, sort_keys: bool = False
) -> None:
    """Save data to a TOML file.

    Args:
        fpath: The file path where the TOML data will be saved.
        data: The data to be serialized and saved in TOML format.
        sort_keys: Whether to sort the keys in the output.
    """
    fpath: Path = Path(fpath)
    with fpath.open("w") as fp:
        tomlkit.dump(data, fp, sort_keys=sort_keys)
