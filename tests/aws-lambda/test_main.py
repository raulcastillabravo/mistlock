import pytest

@pytest.mark.parametrize("deploy", ["terraform", "cloudformation", "boto3"], indirect=True)
def test_main(dev_python, dev_container, deploy):
    """
    Validates the full workflow for a given deployment method.
    The deployment and cleanup are handled by the 'deploy' fixture in conftest.py.
    """
    # 1. Execute Main Logic
    main_result = dev_python("main.py", ttl=10)
    
    assert main_result.returncode == 0
    assert "✓ Lambda response" in main_result.stdout
    assert "✓ Content: Hello from Lambda!" in main_result.stdout

    # 2. Verify S3 content using AWS CLI as shown in README
    s3_result = dev_container(["aws", "s3", "ls", "s3://test-bucket/", "--profile", "localstack"])
    assert s3_result.returncode == 0
    assert "hello.txt" in s3_result.stdout
