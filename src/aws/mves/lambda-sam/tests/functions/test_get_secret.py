import os
import requests
from dotenv import load_dotenv

load_dotenv()

_api_url: str = os.getenv("SAM_API_URL")
_endpoint: str = f"{_api_url}/get_secret"

def test_get_secret_admin():
    """
    Test that admin user can access the secret.
    """
    response = requests.get(_endpoint, params={"username": "admin"})
    
    assert response.status_code == 200
    assert response.text == "super-secret-value-from-emulator"

def test_get_secret_guest():
    """
    Test that guest user is forbidden from accessing the secret.
    """
    response = requests.get(_endpoint, params={"username": "guest"})
    
    assert response.status_code == 403
    assert "Forbidden" in response.text
