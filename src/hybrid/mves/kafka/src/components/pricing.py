import os
import random

BASE_FARE = 2.5
PRICE_PER_KM = 1.2


class Pricing:
    """Simulated pricing service, with the failures the lab needs."""

    _failure_rate: float = None
    _bug: bool = None

    def __init__(self) -> None:
        self._failure_rate = float(os.getenv("PRICING_FAILURE_RATE"))
        self._bug = os.getenv("PRICING_BUG") == "true"

    def fare(self, trip: dict) -> float:
        """Raises ValueError for an invalid trip (retrying will not help)
        and ConnectionError for a transient failure (a retry may work)."""
        if trip["distance_km"] <= 0:
            raise ValueError(f"Invalid distance: {trip['distance_km']}")
        if random.random() < self._failure_rate:
            raise ConnectionError("Pricing service unavailable")

        fare = round(BASE_FARE + PRICE_PER_KM * trip["distance_km"], 2)
        return fare * 100 if self._bug else fare
