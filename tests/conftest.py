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
    Shared fixture to run commands inside the 'dev' service.
    Supports 'ttl' (timeout in seconds) for automatic retries.
    """
    
    def _run(command, ttl=0):
        base_cmd = [
            "docker", "compose", "exec", "--user", "vscode", "-T", "dev",
            f"/app/.venv/bin/python"
        ]
        full_cmd = base_cmd + [command]
        
        start_time = time.time()
        while True:
            result = subprocess.run(full_cmd, cwd=src_dir, capture_output=True, text=True)
            
            if result.returncode == 0 or ttl == 0 or (time.time() - start_time) >= ttl:
                return result
            
    return _run
