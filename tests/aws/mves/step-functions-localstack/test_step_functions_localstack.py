import pytest


@pytest.mark.parametrize(
    "deploy", ["boto3", "cli", "cloudformation", "terraform"], indirect=True
)
def test_deployment_methods(deploy, dev_python):
    """Runs the workflow once per deployment method."""
    result = dev_python("main.py", ttl=30)

    assert result.returncode == 0
    assert "SUCCEEDED" in result.stdout


def test_step_functions_localstack(run_tests):
    """Runs the Lab's own tests against their isolated stack."""
    pass
