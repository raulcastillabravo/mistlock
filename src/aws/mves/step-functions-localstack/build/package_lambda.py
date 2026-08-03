import os
import zipfile

SOURCE_DIR = "lambdas"
DIST_DIR = "dist"


def package(source_file: str) -> str:
    """source_file example: 'log_user.py'."""
    os.makedirs(DIST_DIR, exist_ok=True)
    output_path = os.path.join(DIST_DIR, f"{source_file.removesuffix('.py')}.zip")

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.write(os.path.join(SOURCE_DIR, source_file), arcname=source_file)
    return output_path


def main():
    for source_file in sorted(os.listdir(SOURCE_DIR)):
        print(f"Packaged {package(source_file)}")


if __name__ == "__main__":
    main()
