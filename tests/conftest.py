import os
import subprocess
import time
import shlex
import pytest

@pytest.fixture(scope="module")
def src_dir(request):
    """
    It detects the path to the MVE source directory by mirroring 
    the tests/ directory structure in src/.
    """
    rel_path = os.path.relpath(request.path.parent, os.path.join(request.config.rootdir, "tests"))
    path = os.path.abspath(os.path.join(request.config.rootdir, "src", rel_path))
    
    if not os.path.exists(path):
        raise NotImplementedError(f"Source directory not found for MVE: {path}")

    return path

@pytest.fixture(scope="module", autouse=True)
def infrastructure(src_dir):
    subprocess.run(["devcontainer", "up", "--workspace-folder", src_dir], check=True)
    
    yield src_dir
    
    subprocess.run(["docker", "compose", "down", "-v"], cwd=src_dir, check=True)

@pytest.fixture(scope="module")
def dev_container(src_dir):
    """
    Runs any command inside the 'dev' service.
    Supports 'ttl' (timeout in seconds) for automatic retries.
    """
    
    def _run(command, ttl=0):
        full_cmd = [
            "docker", "compose", "exec", "--user", "vscode", "-T", "dev"
        ] + shlex.split(command)
        
        start_time = time.time()
        while True:
            result = subprocess.run(full_cmd, cwd=src_dir, capture_output=True, text=True)
            
            if result.returncode == 0 or ttl == 0 or (time.time() - start_time) >= ttl:
                return result
            
    return _run

@pytest.fixture(scope="module")
def dev_python(dev_container):
    """
    Runs a Python script inside the 'dev' service using the project's venv.
    """
    def _run(script_path, ttl=0):
        return dev_container(f"/app/.venv/bin/python {script_path}", ttl=ttl)
            
    return _run

@pytest.fixture(scope="module")
def deploy(request, dev_container):
    """
    Generic fixture to handle deployment and cleanup using scripts.
    It takes the deployment method from the test's parametrization.
    """
    method = request.param
    deploy_script = f"scripts/{method}/deploy.sh"
    destroy_script = f"scripts/{method}/destroy.sh"
    
    print(f"\n[Setup] Running {deploy_script}...")
    result = dev_container(f"bash {deploy_script}")
    assert result.returncode == 0
    
    yield
    
    print(f"\n[Teardown] Running {destroy_script}...")
    dev_container(f"bash {destroy_script}")

@pytest.fixture(scope="module")
def run_tests(dev_container):
    """
    Runs the example tests using ./scripts/run_tests.sh.
    """
    print("\nRunning ./scripts/run_tests.sh...")
    result = dev_container("bash ./scripts/run_tests.sh")
    assert result.returncode == 0
    print("\nTests passed for ./scripts/run_tests.sh")

@pytest.fixture(scope="module")
def run_main(dev_container):
    """
    Runs the example main script using ./scripts/run_main.sh.
    """
    print("\nRunning ./scripts/run_main.sh...")
    result = dev_container("bash ./scripts/run_main.sh")
    assert result.returncode == 0
    print("\nMain script passed for ./scripts/run_main.sh")
