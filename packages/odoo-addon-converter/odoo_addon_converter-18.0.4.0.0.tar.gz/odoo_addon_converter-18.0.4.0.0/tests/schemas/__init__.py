import json
import pkgutil
from typing import Any
from collections.abc import Generator


def get_schemas() -> Generator[Any]:
    for file_prefix in ("product",):
        data: bytes | None = pkgutil.get_data(__name__, f"{file_prefix}.schema.json")
        if data:
            yield json.loads(data)
