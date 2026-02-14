import os
import subprocess
import time
import pytest

@pytest.fixture(scope="module", autouse=True)
def infrastructure(request):
    """
    Generalized fixture to handle Docker infrastructure for any MVE.
    It detects the MVE name from the directory of the test file.
    """
    # request.path is the Path to the current test file
    mve_name = request.path.parent.name
    
    # rootdir is the location of the project root
    src_dir = os.path.abspath(os.path.join(request.config.rootdir, "src", mve_name))
    
    if not os.path.exists(src_dir):
        pytest.skip(f"Source directory not found for MVE: {mve_name}")

    request.module.MVE_DIR = src_dir

    subprocess.run(["docker", "compose", "up", "-d"], cwd=src_dir, check=True)
    
    yield src_dir
    
    subprocess.run(["docker", "compose", "down", "-v"], cwd=src_dir, check=True)

@pytest.fixture(scope="module")
def dev_container(request):
    """
    Shared fixture to run commands inside the 'dev' service.
    Supports 'ttl' (timeout in seconds) for automatic retries.
    """
    mve_dir = getattr(request.module, "MVE_DIR", None)
    mve_name = request.path.parent.name
    
    def _run(command, ttl=0):
        base_cmd = [
            "docker", "compose", "exec", "-T", "dev", 
            f"/workspaces/{mve_name}/.venv/bin/python"
        ]
        full_cmd = base_cmd + [command]
        
        start_time = time.time()
        while True:
            result = subprocess.run(full_cmd, cwd=mve_dir, capture_output=True, text=True)
            
            if result.returncode == 0 or ttl == 0 or (time.time() - start_time) >= ttl:
                return result
            
    return _run
