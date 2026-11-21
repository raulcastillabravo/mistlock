import pytest

from src.components.trip_repository import TripRepository

TRIP = {"trip_id": "trip-1", "city": "madrid", "distance_km": 3.5}


def count_events(repository: TripRepository) -> int:
    query = "SELECT COUNT(*) FROM outbox"
    return repository._connection.execute(query).fetchone()[0]


def test_trip_and_event_commit_together(database):
    repository = TripRepository()
    with repository.transaction():
        repository.insert_trip(TRIP)
        repository.insert_event(TRIP)

    assert repository.trip_ids() == {"trip-1"}
    assert count_events(repository) == 1


def test_trip_and_event_roll_back_together(database):
    repository = TripRepository()
    with pytest.raises(RuntimeError):
        with repository.transaction():
            repository.insert_trip(TRIP)
            repository.insert_event(TRIP)
            raise RuntimeError("Crash before the commit")

    assert repository.trip_ids() == set()
    assert count_events(repository) == 0
