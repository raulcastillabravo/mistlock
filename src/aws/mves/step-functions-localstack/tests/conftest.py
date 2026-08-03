import subprocess

import pytest
from dotenv import load_dotenv

load_dotenv()
load_dotenv(".env.test", override=True)


@pytest.fixture(scope="session")
def stack():
    """Builds and deploys an isolated stack named after .env.test."""
    subprocess.run(["scripts/build.sh"], check=True)
    subprocess.run(["scripts/deploy/boto3/deploy.sh"], check=True)
    yield
    subprocess.run(["scripts/deploy/boto3/destroy.sh"], check=True)
