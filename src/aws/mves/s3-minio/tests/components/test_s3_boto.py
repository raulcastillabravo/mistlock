import pandas as pd
from src.components.s3_boto import S3Boto

def test_s3_boto_put_get():
    s3 = S3Boto()
    df = pd.DataFrame({"product_id": [1], "name": ["Test"]})
    path = "bronze/test_boto.csv"
    content = df.to_csv(index=False).encode()
    
    s3.put_object(path, content)
    retrieved = s3.get_object(path)
    
    assert retrieved == content
