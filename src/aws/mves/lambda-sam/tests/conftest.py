import pytest
from dotenv import load_dotenv
from src.components.sam_cli import SamCli

load_dotenv(".env.test", override=True)

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
