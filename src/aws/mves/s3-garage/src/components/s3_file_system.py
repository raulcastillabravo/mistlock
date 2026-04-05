import os
import pyarrow as pa
import pyarrow.parquet as pq
from pyarrow.fs import S3FileSystem as PaS3FileSystem


class S3FileSystem:
    _s3_file_system: PaS3FileSystem = None

    def __init__(self):
        endpoint_url = os.environ["S3_ENDPOINT"]
        access_key = os.environ["S3_ACCESS_KEY"]
        secret_key = os.environ["S3_SECRET_KEY"]
        region = os.environ["AWS_DEFAULT_REGION"]

        self._s3_file_system = PaS3FileSystem(
            endpoint_override=endpoint_url,
            access_key=access_key,
            secret_key=secret_key,
            region=region,
            scheme="http",
        )

    def read_table(self, path: str) -> pa.Table:
        return pq.read_table(path, filesystem=self._s3_file_system)

    def write_table(self, path: str, table: pa.Table):
        pq.write_table(table, path, filesystem=self._s3_file_system)
