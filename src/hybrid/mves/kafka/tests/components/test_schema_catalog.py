import os
from io import BytesIO

import pytest
from fastavro import schemaless_reader, schemaless_writer

from src.components.schema_catalog import SchemaCatalog

# Sample value per Avro type, to build a trip for any schema version
SAMPLES = {"string": "x", "double": 1.0}

CATALOG = SchemaCatalog()
CURRENT = int(os.environ["TRIP_SCHEMA_VERSION"])
EARLIER = [v for v in CATALOG.versions() if v < CURRENT]


def sample_trip(schema: dict) -> dict:
    trip = {}
    for field in schema["fields"]:
        kind = field["type"]
        trip[field["name"]] = None if isinstance(kind, list) else SAMPLES[kind]
    return trip


def roundtrip(writer: dict, reader: dict) -> dict:
    buffer = BytesIO()
    schemaless_writer(buffer, writer, sample_trip(writer))
    return schemaless_reader(BytesIO(buffer.getvalue()), writer, reader)


@pytest.mark.parametrize("version", EARLIER)
def test_current_reads_earlier(version):
    """Backward: a new consumer reads trips already in the topic."""
    roundtrip(CATALOG.load(version), CATALOG.load(CURRENT))


@pytest.mark.parametrize("version", EARLIER)
def test_earlier_reads_current(version):
    """Forward: an old consumer still running reads the new trips."""
    roundtrip(CATALOG.load(CURRENT), CATALOG.load(version))
