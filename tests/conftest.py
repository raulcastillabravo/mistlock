import os
import subprocess
import time
import pytest

@pytest.fixture(scope="module")
def src_dir(request):
    """
    It detects the path to the MVE source directory.
    """
    # request.path is the Path to the current test file
    mve_name = request.path.parent.name
    
    # rootdir is the location of the project root
    path = os.path.abspath(os.path.join(request.config.rootdir, "src", mve_name))
    
    if not os.path.exists(path):
        raise NotImplementedError(f"Source directory not found for MVE: {mve_name}")

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
        # command should be a list of strings
        full_cmd = [
            "docker", "compose", "exec", "--user", "vscode", "-T", "dev"
        ] + command
        
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
        return dev_container(["/app/.venv/bin/python", script_path], ttl=ttl)
            
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
    result = dev_container(["bash", deploy_script])
    assert result.returncode == 0
    
    yield
    
    print(f"\n[Teardown] Running {destroy_script}...")
    dev_container(["bash", destroy_script])
