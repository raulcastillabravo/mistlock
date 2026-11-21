import json
import os
from contextlib import AbstractContextManager

import psycopg


class TripRepository:
    _connection: psycopg.Connection = None

    def __init__(self) -> None:
        self._connection = psycopg.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            dbname=os.getenv("POSTGRES_DB"),
            autocommit=True,
        )

    def transaction(self) -> AbstractContextManager:
        """Everything inside commits together or not at all."""
        return self._connection.transaction()

    def insert_trip(self, trip: dict) -> None:
        self._connection.execute(
            "INSERT INTO trips (trip_id, city, distance_km) "
            "VALUES (%(trip_id)s, %(city)s, %(distance_km)s)",
            trip,
        )

    def insert_event(self, trip: dict) -> None:
        """Writes the trip.created event to the outbox table. Debezium reads
        it from the WAL and publishes it to the `trips` topic."""
        self._connection.execute(
            "INSERT INTO outbox (aggregatetype, aggregateid, type, payload) "
            "VALUES ('trip', %s, 'trip.created', %s)",
            (trip["trip_id"], json.dumps(trip)),
        )

    def trip_ids(self) -> set[str]:
        rows = self._connection.execute("SELECT trip_id FROM trips")
        return {trip_id for (trip_id,) in rows}

    def close(self) -> None:
        self._connection.close()
