from src.components.trip_store import TripStore


def test_trip_store_overwrites_on_replay(store_path):
    store = TripStore()
    store.save("trip-1", "madrid", 1000.0)
    store.save("trip-1", "madrid", 10.0)

    assert store.summary() == (1, 10.0)
