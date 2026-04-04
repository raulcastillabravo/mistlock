import os
from src.databricks_shim.connect import get_spark_session
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType
from pyspark.sql.functions import col, current_timestamp

def run_etl():
    spark = get_spark_session("ETL_Sample_Job")
    bucket = os.getenv("BUCKET_NAME")
    prefix = os.getenv("STORAGE_PREFIX", "s3a")

    print("🚀 Starting ETL Job...")
    schema = StructType([
        StructField("id", IntegerType(), True),
        StructField("name", StringType(), True),
        StructField("price", DoubleType(), True)
    ])
    data = [(1, "Product A", 100.0), (2, "Product B", 200.0)]
    df_raw = spark.createDataFrame(data, schema)
    
    print("💾 Writing Bronze Layer...")
    path = f"{prefix}://{bucket}/bronze/products"
    df_raw.write.format("delta").mode("overwrite").save(path)
    
    print("💾 Writing Silver Layer...")
    df_silver = spark.read.format("delta").load(path) \
        .withColumn("ingestion_time", current_timestamp())
    
    spark.sql("CREATE DATABASE IF NOT EXISTS sales")
    df_silver.write.format("delta").mode("append") \
        .option("path", f"{prefix}://{bucket}/silver/products") \
        .saveAsTable("sales.products_silver")
    
    print("✅ ETL Job Completed Successfully!")
    print("📊 Verification Query:")
    spark.read.table("sales.products_silver").show()
    spark.stop()

if __name__ == "__main__":
    run_etl()
