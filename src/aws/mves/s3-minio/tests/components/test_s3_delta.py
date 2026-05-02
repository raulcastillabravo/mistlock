import pyarrow as pa
from src.components.s3_delta import S3Delta

def test_s3_delta_write_read():
    s3_delta = S3Delta()
    table = pa.table({"product_id": [1], "name": ["Test"]})
    path = "s3://silver/test_delta"
    
    s3_delta.write_table(path, table)
    retrieved = s3_delta.read_table(path)
    
    assert retrieved.equals(table)
