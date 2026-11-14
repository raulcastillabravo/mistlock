import pytest


def test_simple_etl_aws_emulator(mise_run):
    """Lab tests and main.py pass on the Boto3 stack from postCreateCommand."""
    assert mise_run("test").returncode == 0
    assert mise_run("main").returncode == 0


@pytest.fixture(scope="module")
def default_stack_removed(mise_run):
    """Free the resource names taken by the default Boto3 deployment."""
    assert mise_run("destroy:boto3").returncode == 0


@pytest.mark.parametrize(
    "mise_deploy", ["terraform", "cloudformation", "aws-cli"], indirect=True
)
def test_deployment_method(default_stack_removed, mise_deploy, mise_run):
    """main.py works on the stack deployed by each alternative method."""
    result = mise_run("main")

    assert result.returncode == 0
    assert "data.json | 16 bytes | application/json" in result.stdout
