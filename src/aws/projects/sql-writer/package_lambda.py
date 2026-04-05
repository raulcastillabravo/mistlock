import subprocess
import os
import shutil

# Configuration
PYTHON_VERSION = "3.11"
ZIP_FILE_NAME = "lambda.zip"
IMAGE_TAG = "sql_builder"
CONTAINER_NAME = "temp_container"

def run(command):
    """Executes a shell command."""
    print(f"Executing: {' '.join(command)}")
    subprocess.run(command, check=True)

def build_lambda_package():
    # Initial cleanup
    print("Pre-build cleanup...")
    if os.path.exists(ZIP_FILE_NAME): os.remove(ZIP_FILE_NAME)
    if os.path.exists("dist"): shutil.rmtree("dist")

    # 1. Build the Docker image
    print("Building Docker image...")
    run(["docker", "build", "-t", IMAGE_TAG, "-f", "add_user_lambda/Dockerfile", "."])

    # 2. Extract files from container
    print("Extracting dependencies from container...")
    run(["docker", "create", "--name", CONTAINER_NAME, IMAGE_TAG])
    run(["docker", "cp", f"{CONTAINER_NAME}:/asset", "./dist"])
    run(["docker", "rm", "-f", CONTAINER_NAME])

    # 3. Add source code to the dist folder
    print("Adding source code...")
    for f in ["lambda_handler.py", "models.py"]:
        shutil.copy(f"add_user_lambda/{f}", "dist/")

    # 4. Create ZIP (from dist root)
    print(f"Creating {ZIP_FILE_NAME}...")
    shutil.make_archive("lambda", "zip", "dist")

    # 5. Final cleanup
    shutil.rmtree("dist")
    
    print(f"\n✅ Created '{ZIP_FILE_NAME}' successfully using Docker.")

if __name__ == "__main__":
    build_lambda_package()
