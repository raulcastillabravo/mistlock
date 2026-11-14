import pytest
from dotenv import load_dotenv

from deploy.boto3.stack import Stack
from deploy.utils.package_lambda import package


load_dotenv()
load_dotenv(".env.test", override=True)


@pytest.fixture(scope="session", autouse=True)
def test_stack():
    package()
    stack = Stack()
    stack.deploy()
    yield
    stack.destroy()
