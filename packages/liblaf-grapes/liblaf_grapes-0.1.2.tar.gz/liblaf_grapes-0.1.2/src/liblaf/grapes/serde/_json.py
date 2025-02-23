import json
import os
from pathlib import Path
from typing import Any


def load_json(fpath: str | os.PathLike[str]) -> Any:
    """Load and parse a JSON file from the given file path.

    Args:
        fpath: The path to the JSON file.

    Returns:
        Any: The parsed JSON data.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file contains invalid JSON.
    """
    fpath: Path = Path(fpath)
    with fpath.open() as fp:
        return json.load(fp)


def save_json(fpath: str | os.PathLike[str], data: Any) -> None:
    """Save data to a JSON file.

    Args:
        fpath: The file path where the JSON data will be saved.
        data: The data to be serialized to JSON and saved to the file.
    """
    fpath: Path = Path(fpath)
    with fpath.open("w") as fp:
        json.dump(data, fp)
