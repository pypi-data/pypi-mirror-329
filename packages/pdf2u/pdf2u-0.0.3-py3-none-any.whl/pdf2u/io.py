import json
from pathlib import Path
from typing import Any


def load_json(file_path: Path) -> dict[str, Any]:
    with open(file_path) as f:
        return json.load(f)
