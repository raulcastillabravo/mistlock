import pytest

from src.components.pricing import Pricing


def test_pricing():
    assert Pricing().fare({"distance_km": 10}) == 14.5


def test_pricing_rejects_invalid_trip():
    with pytest.raises(ValueError):
        Pricing().fare({"distance_km": 0})


def test_pricing_bug(monkeypatch):
    monkeypatch.setenv("PRICING_BUG", "true")
    assert Pricing().fare({"distance_km": 10}) == 1450.0
