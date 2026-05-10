import pytest
from src.components.sam_cli import SamCli

@pytest.fixture(scope="session", autouse=True)
def sam_api():
    """
    Starts the SAM local API in the background using the SamCli component.
    """
    with SamCli() as sam_cli:
        yield sam_cli
