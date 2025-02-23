import os
from pathlib import Path
from typing import Any

import autoregistry

from liblaf import grapes

READERS = autoregistry.Registry()
"""A registry mapping file extensions to their respective deserialization functions.

Supported extensions and their corresponding deserialization functions:

- ".json": grapes.load_json
- ".toml": grapes.load_toml (if the "tomlkit" module is available)
- ".yaml": grapes.load_yaml (if the "ruamel.yaml" module is available)
- ".yml": grapes.load_yaml (if the "ruamel.yaml" module is available)
"""

WRITERS = autoregistry.Registry()
"""A registry mapping file extensions to their respective serialization functions.

Supported extensions and their corresponding serialization functions:

- ".json": grapes.save_json
- ".toml": grapes.save_toml (if the "tomlkit" module is available)
- ".yaml": grapes.save_yaml (if the "ruamel.yaml" module is available)
- ".yml": grapes.save_yaml (if the "ruamel.yaml" module is available)
"""


READERS[".json"] = grapes.load_json
WRITERS[".json"] = grapes.save_json
if grapes.has_module("tomlkit"):
    READERS[".toml"] = grapes.load_toml
    WRITERS[".toml"] = grapes.save_toml
if grapes.has_module("ruamel.yaml"):
    READERS[".yaml"] = grapes.load_yaml
    READERS[".yml"] = grapes.load_yaml
    WRITERS[".yaml"] = grapes.save_yaml
    WRITERS[".yml"] = grapes.save_yaml


def serialize(
    fpath: str | os.PathLike[str], data: Any, *, ext: str | None = None
) -> None:
    """Serialize data to a file.

    Args:
        fpath: The file path where the data will be serialized.
        data: The data to be serialized.
        ext: The file extension to determine the writer to use. If `None`, the extension is derived from the file path.

    Raises:
        ValueError: If the file extension is not supported.
    """
    fpath: Path = Path(fpath)
    if ext is None:
        ext = fpath.suffix
    if ext not in WRITERS:
        msg: str = f"Unsupported file extension: {ext}"
        raise ValueError(msg)
    writer = WRITERS[ext]
    fpath.parent.mkdir(parents=True, exist_ok=True)
    writer(fpath, data)


def deserialize(fpath: str | os.PathLike[str], *, ext: str | None = None) -> Any:
    """Deserialize the contents of a file.

    Args:
        fpath: The path to the file to be deserialized.
        ext: The file extension. If not provided, it will be inferred from the file path.

    Returns:
        The deserialized content of the file.

    Raises:
        ValueError: If the file extension is not supported.
    """
    fpath: Path = Path(fpath)
    if ext is None:
        ext = fpath.suffix
    if ext not in READERS:
        msg: str = f"Unsupported file extension: {ext}"
        raise ValueError(msg)
    return READERS[ext](fpath)
