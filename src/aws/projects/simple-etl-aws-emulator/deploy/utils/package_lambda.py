import os
import zipfile

from dotenv import load_dotenv


def package():
    """Zip src/handler.py as handler.py at the archive root."""
    zip_path = os.environ["LAMBDA_ZIP"]
    os.makedirs(os.path.dirname(zip_path), exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.write("src/handler.py", "handler.py")
    print(f"✓ Packaged {zip_path}")


if __name__ == "__main__":
    load_dotenv()
    package()
