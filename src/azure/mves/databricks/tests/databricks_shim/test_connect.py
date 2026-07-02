import os

from pyspark.sql.types import StructType, StructField, IntegerType, StringType


def test_delta_roundtrip(spark):
    bucket = os.environ["BUCKET_NAME"]
    prefix = os.environ["STORAGE_PREFIX"]
    schema = StructType([
        StructField("id", IntegerType(), True),
        StructField("name", StringType(), True),
    ])
    df = spark.createDataFrame([(1, "Product A")], schema)
    path = f"{prefix}://{bucket}/test/products"

    df.write.format("delta").mode("overwrite").save(path)
    result = spark.read.format("delta").load(path)

    assert result.count() == 1
