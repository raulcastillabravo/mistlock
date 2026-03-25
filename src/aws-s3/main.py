import os
import io
import pandas as pd
import pyarrow as pa
from dotenv import load_dotenv

from src.components.s3_boto import S3Boto
from src.components.s3_file_system import S3FileSystemComponent
from src.components.s3_delta import S3Delta

load_dotenv()

def main():
    # Configuration
    BRONZE_BUCKET = os.environ["S3_BUCKET_BRONZE"]
    SILVER_BUCKET = os.environ["S3_BUCKET_SILVER"]

    # Component instantiation
    s3_boto = S3Boto()
    s3_fs = S3FileSystemComponent()
    s3_delta = S3Delta()

    # 1. Sample data
    data = {
        "product_id": [1, 2, 3],
        "name": ["Laptop", "Mouse", "Keyboard"],
        "price": [1200.0, 25.5, 75.0]
    }
    df = pd.DataFrame(data)

    # 2. S3Boto CSV flow
    print(f"--- 1. S3Boto: CSV in {BRONZE_BUCKET}/csv/ ---")
    csv_path = f"{BRONZE_BUCKET}/csv/products.csv"
    s3_boto.put_object(csv_path, df.to_csv(index=False).encode())
    
    csv_bytes = s3_boto.get_object(csv_path)
    csv_df = pd.read_csv(io.BytesIO(csv_bytes))
    print("✓ CSV read with S3Boto:")
    print(csv_df)

    # 3. S3FileSystem Parquet flow
    print(f"--- 2. S3FileSystem: Parquet in {BRONZE_BUCKET}/parquet/ ---")
    pq_path = f"{BRONZE_BUCKET}/parquet/products.parquet"
    table = pa.Table.from_pandas(df)
    s3_fs.write_table(pq_path, table)
    
    pq_table = s3_fs.read_table(pq_path)
    print("✓ Parquet read with S3FileSystem:")
    print(pq_table.to_pandas())

    # 4. S3Delta flow
    print(f"--- 3. S3Delta: Delta Table in {SILVER_BUCKET}/delta/ ---")
    delta_path = f"s3://{SILVER_BUCKET}/delta/products"
    s3_delta.write_table(delta_path, table)
    
    delta_table = s3_delta.read_table(delta_path)
    print("✓ Delta Table read with S3Delta:")
    print(delta_table.to_pandas())

if __name__ == "__main__":
    main()
