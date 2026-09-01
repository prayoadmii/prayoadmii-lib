import tomllib

from pathlib import Path
from typing import Any

class Config:
    def __init__(self, path: Path, data: dict[str, Any]):
        self.path = path
        self.data = data

    def get_config(self, path: str, default: Any = None) -> Any:
        value: Any = self.data

        for key in path.split("."):
            if not isinstance(value, dict):
                return default

            value = value.get(key)

            if value is None:
                return default

        return value


def load(filename: str | Path) -> Config:
    path = Path(filename)

    if not path.is_absolute():
        path = Path.cwd() / path

    path = path.resolve()

    with path.open("rb") as file:
        data = tomllib.load(file)

    return Config(path, data)