from pathlib import Path
from typing import Any

def _parse_value(value: str) -> Any:
    value = value.strip()

    if (
        len(value) >= 2
        and value[0] == value[-1]
        and value[0] in "\"'"
    ):
        return value[1:-1]

    lowered = value.lower()

    if lowered == "true":
        return True

    if lowered == "false":
        return False

    if lowered in {"none", "null"}:
        return None

    try:
        return int(value)
    except ValueError:
        pass

    try:
        return float(value)
    except ValueError:
        pass

    return value

class Env:
    def __init__(self, path: Path, data: dict[str, Any]):
        self.path = path
        self.data = data

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

def load(filename: str | Path) -> Env:
    path = Path(filename)

    if not path.is_absolute():
        path = Path.cwd() / path

    path = path.resolve()

    data: dict[str, Any] = {}

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                continue

            key, value = line.split("=", 1)

            key = key.strip()
            value = value.strip()

            data[key] = _parse_value(value)

    return Env(path, data)