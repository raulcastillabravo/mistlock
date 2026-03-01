import pytest
import time

@pytest.fixture(scope="module", autouse=True)
def package_lambda(dev_python):
    """Package the Lambda function once for all tests in the module."""
    pkg_result = dev_python("deploy/utils/package_lambda.py")
    assert pkg_result.returncode == 0
    return pkg_result

@pytest.fixture
def terraform_deploy(dev_container):
    """Fixture for Terraform deployment and cleanup."""
    print("\n[Setup] Deploying with Terraform...")
    dev_container(["terraform", "-chdir=deploy/terraform", "init"])
    result = dev_container(["terraform", "-chdir=deploy/terraform", "apply", "-auto-approve"])
    assert result.returncode == 0
    
    yield
    
    print("\n[Teardown] Cleaning up Terraform...")
    dev_container(["terraform", "-chdir=deploy/terraform", "destroy", "-auto-approve"])

@pytest.fixture
def cloudformation_deploy(dev_container):
    """Fixture for CloudFormation deployment and cleanup."""
    stack_name = "aws-lambda-stack"
    deploy_bucket = "lambda-deploy-bucket"
    
    print("\n[Setup] Deploying with CloudFormation...")
    # 1. Create temporary bucket
    dev_container(["aws", "s3", "mb", f"s3://{deploy_bucket}", "--profile", "localstack"])
    # 2. Upload zip
    dev_container(["aws", "s3", "cp", "deploy/dist/function.zip", f"s3://{deploy_bucket}/lambda.zip", "--profile", "localstack"])
    # 3. Deploy stack
    result = dev_container([
        "aws", "cloudformation", "deploy",
        "--profile", "localstack",
        "--stack-name", stack_name,
        "--template-file", "deploy/cloudformation/template.yaml",
        "--capabilities", "CAPABILITY_NAMED_IAM"
    ])
    assert result.returncode == 0
    
    yield
    
    print("\n[Teardown] Cleaning up CloudFormation...")
    dev_container(["aws", "cloudformation", "delete-stack", "--stack-name", stack_name, "--profile", "localstack"])
    dev_container(["aws", "s3", "rb", f"s3://{deploy_bucket}", "--force", "--profile", "localstack"])

@pytest.fixture
def boto3_deploy(dev_python, dev_container):
    """Fixture for Boto3 deployment and cleanup."""
    print("\n[Setup] Deploying with Boto3...")
    result = dev_python("deploy/boto3/deploy.py")
    assert result.returncode == 0
    
    yield
    
    print("\n[Teardown] Cleaning up Boto3...")
    dev_container(["aws", "lambda", "delete-function", "--function-name", "upload-to-s3", "--profile", "localstack"])
    dev_container(["aws", "iam", "delete-role", "--role-name", "lambda-s3-role", "--profile", "localstack"])
    dev_container(["aws", "s3", "rb", "s3://test-bucket", "--force", "--profile", "localstack"])


def test_terraform_workflow(dev_python, terraform_deploy):
    """Validates the full workflow using Terraform deployment."""
    main_result = dev_python("main.py", ttl=10)
    assert main_result.returncode == 0
    assert "✓ Lambda response" in main_result.stdout
    assert "✓ Content: Hello from Lambda!" in main_result.stdout

def test_cloudformation_workflow(dev_python, cloudformation_deploy):
    """Validates the full workflow using CloudFormation deployment."""
    main_result = dev_python("main.py", ttl=10)
    assert main_result.returncode == 0
    assert "✓ Lambda response" in main_result.stdout
    assert "✓ Content: Hello from Lambda!" in main_result.stdout

def test_boto3_workflow(dev_python, boto3_deploy):
    """Validates the full workflow using Boto3 deployment."""
    main_result = dev_python("main.py", ttl=10)
    assert main_result.returncode == 0
    assert "✓ Lambda response" in main_result.stdout
    assert "✓ Content: Hello from Lambda!" in main_result.stdout
