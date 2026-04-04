import os
import zipfile

def package_lambda(source_file, output_zip):
    """Create a ZIP package for the Lambda function."""
    print(f"Packaging {source_file} into {output_zip}...")
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_zip), exist_ok=True)
    
    # Remove existing zip if it exists
    if os.path.exists(output_zip):
        os.remove(output_zip)
    
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Standardize internal name to lambda.py
        zipf.write(source_file, "lambda.py")
    
    print(f"Created {output_zip} successfully")
    print(f"Size: {os.path.getsize(output_zip)} bytes")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    src_path = os.path.join(base_dir, "src/lambda.py")
    dist_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dist")
    output_path = os.path.join(dist_dir, "function.zip")
    
    package_lambda(src_path, output_path)
