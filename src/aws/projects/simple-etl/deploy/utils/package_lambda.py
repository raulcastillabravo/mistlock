import zipfile
import os

def create_lambda_package():
    """Create a ZIP package for the Lambda function."""
    source_file = "src/lambda.py"
    zip_filename = "./tmp/lambda.zip"
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(zip_filename), exist_ok=True)
    
    # Remove existing zip if it exists
    if os.path.exists(zip_filename):
        os.remove(zip_filename)
        print(f"Removed existing {zip_filename}")
    
    # Create new zip file
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(source_file, "lambda.py")
    
    print(f"Created {zip_filename} successfully")
    print(f"Size: {os.path.getsize(zip_filename)} bytes")

if __name__ == "__main__":
    create_lambda_package()
