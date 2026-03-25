import os
import pyarrow as pa
from deltalake import write_deltalake, DeltaTable


class S3Delta:
    def __init__(self):
        self.storage_options: dict[str, str] = {
            "AWS_ACCESS_KEY_ID": os.environ["S3_ACCESS_KEY"],
            "AWS_SECRET_ACCESS_KEY": os.environ["S3_SECRET_KEY"],
            "AWS_ENDPOINT_URL": os.environ["S3_ENDPOINT"],
            "AWS_REGION": os.environ["AWS_DEFAULT_REGION"],
            "AWS_ALLOW_HTTP": "true",
            "AWS_S3_ALLOW_UNSAFE_RENAME": "true",
        }

    def read_table(self, path: str) -> pa.Table:
        return DeltaTable(
            path, storage_options=self.storage_options
        ).to_pyarrow_table()

    def write_table(self, path: str, table: pa.Table):
        write_deltalake(
            path,
            table,
            mode="overwrite",
            storage_options=self.storage_options,
        )
