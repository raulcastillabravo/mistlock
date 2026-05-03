import os
import pyarrow as pa
from src.components.s3_file_system import S3FileSystem

def test_s3_fs_write_read():
    s3_fs = S3FileSystem()
    table = pa.table({"product_id": [1], "name": ["Test"]})
    bucket = os.environ["S3_BUCKET_BRONZE"]
    path = f"{bucket}/test_fs.parquet"
    
    s3_fs.write_table(path, table)
    retrieved = s3_fs.read_table(path)
    
    assert retrieved.equals(table)
