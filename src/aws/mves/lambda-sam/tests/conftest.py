import pytest
from src.components.sam_cli import SamCli

@pytest.fixture(scope="session", autouse=True)
def sam_api():
    """
    Starts the SAM local API in the background using the SamCli component.
    """
    sam_cli = SamCli()
    sam_cli.start_api()
    
    yield sam_cli
    
    sam_cli.stop_api()
