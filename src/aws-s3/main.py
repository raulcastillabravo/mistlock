import os
import pandas as pd
import pyarrow as pa
import boto3
from dotenv import load_dotenv
from deltalake import write_deltalake, DeltaTable

# Load environment variables
load_dotenv()
load_dotenv(".env.garage")

# Configuration
ENDPOINT_URL = os.environ["S3_ENDPOINT"]
ACCESS_KEY = os.environ["S3_ACCESS_KEY"]
SECRET_KEY = os.environ["S3_SECRET_KEY"]
REGION_NAME = os.environ["AWS_DEFAULT_REGION"]

BRONZE_BUCKET = os.environ["S3_BUCKET_BRONZE"]
SILVER_BUCKET = os.environ["S3_BUCKET_SILVER"]

STORAGE_OPTIONS = {
    "AWS_ACCESS_KEY_ID": ACCESS_KEY,
    "AWS_SECRET_ACCESS_KEY": SECRET_KEY,
    "AWS_ENDPOINT_URL": ENDPOINT_URL,
    "AWS_REGION": REGION_NAME,
    "AWS_ALLOW_HTTP": "true",
    "AWS_S3_ALLOW_UNSAFE_RENAME": "true",
}

def main():
    s3_client = boto3.client(
        "s3",
        endpoint_url=ENDPOINT_URL,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name=REGION_NAME,
    )

    # 1. Upload CSV to Bronze
    print(f"--- 1. Uploading CSV to {BRONZE_BUCKET} ---")
    data = {
        "product_id": [1, 2, 3],
        "name": ["Laptop", "Mouse", "Keyboard"],
        "price": [1200.0, 25.5, 75.0]
    }
    df = pd.DataFrame(data)
    csv_content = df.to_csv(index=False)
    
    s3_client.put_object(
        Bucket=BRONZE_BUCKET,
        Key="products.csv",
        Body=csv_content
    )
    print("✓ CSV uploaded.")

    # 2. Read CSV from Bronze using pyarrow
    print(f"--- 2. Reading CSV from {BRONZE_BUCKET} ---")
    obj = s3_client.get_object(Bucket=BRONZE_BUCKET, Key="products.csv")
    table = pa.csv.read_csv(obj["Body"])
    print("✓ Data read from S3:")
    print(table.to_pandas())

    # 3. Write to Silver as Delta Lake
    print(f"--- 3. Writing to {SILVER_BUCKET} as Delta Lake ---")
    silver_path = f"s3://{SILVER_BUCKET}/products_delta"
    
    write_deltalake(
        silver_path,
        table,
        mode="overwrite",
        storage_options=STORAGE_OPTIONS
    )
    print("✓ Delta table written.")

    # 4. Read from Silver and display
    print(f"--- 4. Reading from {SILVER_BUCKET} ---")
    dt = DeltaTable(silver_path, storage_options=STORAGE_OPTIONS)
    result_df = dt.to_pandas()
    print("✓ Final data:")
    print(result_df)

if __name__ == "__main__":
    main()
