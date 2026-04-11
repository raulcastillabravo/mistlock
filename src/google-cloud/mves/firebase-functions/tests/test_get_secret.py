import requests
import pytest

BASE_URL = "http://localhost:5001/demo-mve-firebase-functions/us-central1/get_secret"

def test_get_secret_admin_success() -> None:
    """
    Test that the function returns the secret for the admin user.
    """
    params = {"username": "admin"}
    response = requests.get(BASE_URL, params=params)
    
    assert response.status_code == 200
    data = response.json()
    assert data["secret"] == "super-secret-value-from-emulator"

def test_get_secret_denied_user() -> None:
    """
    Test that the function returns 403 for a non-admin user.
    """
    params = {"username": "guest"}
    response = requests.get(BASE_URL, params=params)
    
    assert response.status_code == 403
    data = response.json()
    assert data["error"] == "Access Denied"
