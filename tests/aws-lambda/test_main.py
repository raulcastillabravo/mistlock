import os
import subprocess
import time
import pytest

# Paths
MVE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src/aws-lambda"))

@pytest.fixture(scope="module", autouse=True)
def infrastructure():
    """
    Setup and Teardown for Docker infrastructure.
    """
    print(f"\n[Setup] Building and starting infrastructure in {MVE_DIR}...")
    # Start both localstack and dev services
    subprocess.run(["docker", "compose", "up", "-d"], cwd=MVE_DIR, check=True)
    
    # Wait for LocalStack to be ready
    print("[Setup] Waiting for LocalStack to be ready...")
    time.sleep(15)
    
    yield
    
    print(f"\n[Teardown] Stopping infrastructure in {MVE_DIR}...")
    subprocess.run(["docker", "compose", "down", "-v"], cwd=MVE_DIR, check=True)

def run_in_dev_container(command):
    """Helper to run a command inside the 'dev' container."""
    base_cmd = ["docker", "compose", "exec", "-t", "dev", "/workspaces/aws-lambda/.venv/bin/python"]
    full_cmd = base_cmd + [command]
    return subprocess.run(full_cmd, cwd=MVE_DIR, capture_output=True, text=True)

def test_full_workflow():
    """
    Test the complete MVE workflow inside the dev container.
    """
    # 0. Sync dependencies (ensures container is up to date with host pyproject.toml)
    print("\n[Test] Syncing dependencies (uv sync)...")
    subprocess.run(
        ["docker", "compose", "exec", "-t", "dev", "uv", "sync"], 
        cwd=MVE_DIR, check=True
    )

    # 1. Package the Lambda
    print("\n[Test] Packaging Lambda (inside container)...")
    pkg_result = run_in_dev_container("deploy/utils/package_lambda.py")
    assert pkg_result.returncode == 0
    assert "Created" in pkg_result.stdout

    # 2. Deploy with Boto3
    print("[Test] Deploying with Boto3 (inside container)...")
    deploy_result = run_in_dev_container("deploy/boto3_deploy.py")
    assert deploy_result.returncode == 0
    assert "Deployment completed successfully" in deploy_result.stdout

    time.sleep(15)

    # 3. Execute Main Logic
    print("[Test] Executing main.py (inside container)...")
    main_result = run_in_dev_container("main.py")
    
    # Verification
    assert main_result.returncode == 0
    assert "✓ Lambda response" in main_result.stdout
    assert "✓ Content: Hello from Lambda!" in main_result.stdout
    print("[Test] Workflow completed successfully! ✓")
