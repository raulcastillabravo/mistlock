import os
import pyarrow as pa
import pyarrow.parquet as pq
from pyarrow.fs import S3FileSystem


class S3FileSystemComponent:
    def __init__(self):
        self.endpoint_url: str = os.environ["S3_ENDPOINT"]
        self.access_key: str = os.environ["S3_ACCESS_KEY"]
        self.secret_key: str = os.environ["S3_SECRET_KEY"]
        self.region: str = os.environ["AWS_DEFAULT_REGION"]

        self.s3_fs = S3FileSystem(
            endpoint_override=self.endpoint_url,
            access_key=self.access_key,
            secret_key=self.secret_key,
            region=self.region,
            scheme="http",
        )

    def read_table(self, path: str) -> pa.Table:
        return pq.read_table(path, filesystem=self.s3_fs)

    def write_table(self, path: str, table: pa.Table):
        pq.write_table(table, path, filesystem=self.s3_fs)
