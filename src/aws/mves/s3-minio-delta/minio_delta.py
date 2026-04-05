import os
from dotenv import load_dotenv
from deltalake import DeltaTable, write_deltalake
import pandas as pd
from typing import Optional, List

load_dotenv()


class MinioDelta:
    def __init__(self):
        self.endpoint = os.getenv("MINIO_ENDPOINT")
        self.access_key = os.getenv("MINIO_ROOT_USER")
        self.secret_key = os.getenv("MINIO_ROOT_PASSWORD")
        self.bucket = os.getenv("BUCKET_NAME")
        
        self.storage_options = {
            "AWS_ENDPOINT_URL": self.endpoint,
            "AWS_ACCESS_KEY_ID": self.access_key,
            "AWS_SECRET_ACCESS_KEY": self.secret_key,
            "AWS_ALLOW_HTTP": "true",
            "aws_conditional_put": "etag",
        }

    def write(
        self, 
        df: pd.DataFrame, 
        path: str,
        mode: str = "overwrite",
        partition_by: Optional[List[str]] = None,
        predicate: Optional[str] = None
    ) -> None:
        write_deltalake(
            table_or_uri=f"s3://{self.bucket}/{path}",
            data=df,
            mode=mode,
            partition_by=partition_by,
            predicate=predicate,
            storage_options=self.storage_options
        )

    def read(
        self, 
        path: str,
        columns: Optional[List[str]] = None,
        filters: Optional[List] = None
    ) -> pd.DataFrame:
        full_path = f"s3://{self.bucket}/{path}"
        dt = DeltaTable(full_path, storage_options=self.storage_options)

        return dt.to_pandas(columns=columns, filters=filters)
