import os
import requests
import pytest
from dotenv import load_dotenv

load_dotenv()

FUNCTION_URL = os.getenv("FUNCTION_URL")
ADMIN_USER = os.getenv("ADMIN_USER")

def test_get_secret_admin_success() -> None:
    """
    Test that the function returns the secret for the admin user.
    """
    params = {"username": ADMIN_USER}
    response = requests.get(FUNCTION_URL, params=params)
    
    assert response.status_code == 200
    data = response.json()
    assert data["secret"] == "super-secret-value-from-emulator"

def test_get_secret_denied_user() -> None:
    """
    Test that the function returns 403 for a non-admin user.
    """
    params = {"username": "guest"}
    response = requests.get(FUNCTION_URL, params=params)
    
    assert response.status_code == 403
    data = response.json()
    assert data["error"] == "Access Denied"
