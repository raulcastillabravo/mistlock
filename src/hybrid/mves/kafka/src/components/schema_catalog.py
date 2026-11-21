import json
import os
from pathlib import Path

from fastavro import parse_schema


class SchemaCatalog:
    """Trip schemas kept in the repository, one file per version.

    It is a minimal schema registry: the producer tags each event with its
    schema version and the consumer looks that version up here.
    """

    _directory: Path = None

    def __init__(self) -> None:
        self._directory = Path(os.getenv("SCHEMA_DIR"))

    def load(self, version: int) -> dict:
        path = self._directory / f"trip_v{version}.avsc"
        return parse_schema(json.loads(path.read_text()))

    def versions(self) -> list[int]:
        files = self._directory.glob("trip_v*.avsc")
        return sorted(int(file.stem.split("_v")[1]) for file in files)
