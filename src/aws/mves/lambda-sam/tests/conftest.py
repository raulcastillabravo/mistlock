import pytest
from src.components.sam_cli import SamCli

@pytest.fixture(scope="module")
def sam_api():
    """
    Starts the SAM local API in the background.
    """
    with SamCli(command="api") as sam:
        yield sam

@pytest.fixture(scope="module")
def sam_lambda():
    """
    Starts the SAM local Lambda in the background.
    """
    with SamCli(command="lambda") as sam:
        yield sam
