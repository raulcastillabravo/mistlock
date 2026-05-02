import os
import io
import pandas as pd
import pyarrow as pa
from dotenv import load_dotenv

from src.components.s3_boto import S3Boto
from src.components.s3_file_system import S3FileSystem
from src.components.s3_delta import S3Delta

load_dotenv()

BRONZE_BUCKET = os.environ["S3_BUCKET_BRONZE"]
SILVER_BUCKET = os.environ["S3_BUCKET_SILVER"]


def run_s3_boto(df: pd.DataFrame):
    s3_boto = S3Boto()

    print(f"--- 1. S3Boto: CSV in {BRONZE_BUCKET}/csv/ ---")
    path = f"{BRONZE_BUCKET}/csv/products.csv"
    s3_boto.put_object(path, df.to_csv(index=False).encode())
    
    csv_bytes = s3_boto.get_object(path)
    csv_df = pd.read_csv(io.BytesIO(csv_bytes))
    print("✓ CSV read with S3Boto:")
    print(csv_df)
    print('\n')


def run_s3_file_system(df: pd.DataFrame):
    s3_fs = S3FileSystem()

    print(f"--- 2. S3FileSystem: Parquet in {BRONZE_BUCKET}/parquet/ ---")
    path = f"{BRONZE_BUCKET}/parquet/products.parquet"
    table = pa.Table.from_pandas(df)
    s3_fs.write_table(path, table)
    
    pq_table = s3_fs.read_table(path)
    print("✓ Parquet read with S3FileSystem:")
    print(pq_table.to_pandas())
    print('\n')


def run_s3_delta(df: pd.DataFrame):
    s3_delta = S3Delta()

    print(f"--- 3. S3Delta: Delta Table in {SILVER_BUCKET}/delta/ ---")
    path = f"s3://{SILVER_BUCKET}/delta/products"
    table = pa.Table.from_pandas(df)
    s3_delta.write_table(path, table)
    
    delta_table = s3_delta.read_table(path)
    print("✓ Delta Table read with S3Delta:")
    print(delta_table.to_pandas())
    print('\n')


def main():
    df = pd.DataFrame({
        "product_id": [1, 2, 3],
        "name": ["Laptop", "Mouse", "Keyboard"],
        "price": [1200.0, 25.5, 75.0]
    })

    run_s3_boto(df)
    run_s3_file_system(df)
    run_s3_delta(df)


if __name__ == "__main__":
    main()
