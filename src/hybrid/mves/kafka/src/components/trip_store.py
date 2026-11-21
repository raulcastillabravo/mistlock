import os
import sqlite3


class TripStore:
    """Priced trips in SQLite. Saving a trip twice overwrites it, so a
    replay fixes wrong rows instead of duplicating them."""

    _connection: sqlite3.Connection = None

    def __init__(self) -> None:
        self._connection = sqlite3.connect(os.getenv("TRIP_STORE_PATH"))
        self._connection.execute(
            "CREATE TABLE IF NOT EXISTS trips ("
            "trip_id TEXT PRIMARY KEY, city TEXT, fare REAL)"
        )

    def save(self, trip_id: str, city: str, fare: float) -> None:
        with self._connection:
            self._connection.execute(
                "INSERT INTO trips VALUES (?, ?, ?) "
                "ON CONFLICT (trip_id) DO UPDATE SET fare = excluded.fare",
                (trip_id, city, fare),
            )

    def summary(self) -> tuple[int, float]:
        """Returns the number of trips and the sum of their fares."""
        query = "SELECT COUNT(*), COALESCE(SUM(fare), 0) FROM trips"
        return self._connection.execute(query).fetchone()

    def clear(self) -> None:
        with self._connection:
            self._connection.execute("DELETE FROM trips")
