import os
import pyarrow as pa
from src.components.s3_delta import S3Delta

def test_s3_delta_write_read():
    s3_delta = S3Delta()
    table = pa.table({"product_id": [1], "name": ["Test"]})
    bucket = os.environ["S3_BUCKET_SILVER"]
    path = f"s3://{bucket}/test_delta"
    
    s3_delta.write_table(path, table)
    retrieved = s3_delta.read_table(path)
    
    assert retrieved.equals(table)
