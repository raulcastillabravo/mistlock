import pytest

@pytest.fixture(scope="module", autouse=True)
def infrastructure():
    """
    Override the global autouse fixture to disable devcontainer setup, 
    as this MVE is not compatible with Dev Containers.
    """
    pass

def test_lambda_sam(host_command):
    """
    Test the AWS Lambda SAM MVE on the host machine.
    """
    # 1. Setup Environment
    print("\nRunning ./scripts/setup.sh...")
    result = host_command("bash ./scripts/setup.sh")
    assert result.returncode == 0
    
    # 2. Run Tests
    print("\nRunning ./scripts/run_tests.sh...")
    result = host_command("bash ./scripts/run_tests.sh")
    assert result.returncode == 0
    
    # 3. Run Main
    print("\nRunning ./scripts/run_main.sh...")
    result = host_command("bash ./scripts/run_main.sh")
    assert result.returncode == 0
