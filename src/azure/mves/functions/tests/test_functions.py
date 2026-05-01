import os

import azure.functions as func
from dotenv import load_dotenv

from function_app import get_secret

load_dotenv()

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")

def test_get_secret_admin():
    req = func.HttpRequest(
        method='GET',
        body=None,
        url='/api/get_secret',
        params={'username': ADMIN_USERNAME}
    )

    resp = get_secret(req)

    assert resp.status_code == 200
    assert resp.get_body() == b"super-secret-value-from-emulator"

def test_get_secret_forbidden():
    req = func.HttpRequest(
        method='GET',
        body=None,
        url='/api/get_secret',
        params={'username': 'guest'}
    )

    resp = get_secret(req)

    assert resp.status_code == 403
    assert b"Forbidden" in resp.get_body()

def test_get_secret_no_username():
    req = func.HttpRequest(
        method='GET',
        body=None,
        url='/api/get_secret',
        params={}
    )

    resp = get_secret(req)

    assert resp.status_code == 403
