import os
from pathlib import Path
from typing import Any

from liblaf import grapes

with grapes.optional_imports(extra="serde"):
    from ruamel.yaml import YAML


def load_yaml(fpath: str | os.PathLike[str]) -> Any:
    fpath: Path = Path(fpath)
    yaml = YAML()
    with fpath.open() as fp:
        return yaml.load(fp)


def save_yaml(fpath: str | os.PathLike[str], data: Any) -> None:
    fpath: Path = Path(fpath)
    yaml = YAML()
    with fpath.open("w") as fp:
        yaml.dump(data, fp)
