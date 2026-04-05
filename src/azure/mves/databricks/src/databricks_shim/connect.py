import os
from pyspark.sql import SparkSession

def get_spark_session(app_name="DatabricksLocal"):
    """
    Returns a SparkSession configured for the current environment.
    If running in Databricks, it returns a default session. Otherwise, it configures a local Spark session with MinIO, Delta Lake, and Hive Metastore.
    """
    # Detect environment (prefer APP_ENV, fallback to Databricks runtime detection)
    env = os.getenv("APP_ENV", "local")
    
    if env != "local":
        return SparkSession.builder.appName(app_name).getOrCreate()

    print(f"⚡ Initializing Local Spark Session (Databricks Emulator)...")
    
    # Local configuration for MinIO and Postgres Metastore
    builder = SparkSession.builder \
        .appName(app_name) \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .config("spark.sql.catalogImplementation", "hive") \
        .config("spark.hadoop.fs.s3a.endpoint", os.getenv("AWS_ENDPOINT_URL")) \
        .config("spark.hadoop.fs.s3a.access.key", os.getenv("AWS_ACCESS_KEY_ID")) \
        .config("spark.hadoop.fs.s3a.secret.key", os.getenv("AWS_SECRET_ACCESS_KEY")) \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider") \
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false") \
        .config("spark.hadoop.fs.s3a.signing-algorithm", "AWSS3V4SignerType") \
        .config("spark.delta.logStore.class", "org.apache.spark.sql.delta.storage.S3SingleDriverLogStore") \
        .config("spark.hadoop.fs.s3a.endpoint.region", os.getenv("AWS_REGION", "us-east-1")) \
        .config("spark.jars", "/opt/spark/jars/delta-spark_2.12-3.2.0.jar,"
                              "/opt/spark/jars/delta-storage-3.2.0.jar,"
                              "/opt/spark/jars/hadoop-aws-3.3.4.jar,"
                              "/opt/spark/jars/aws-java-sdk-bundle-1.12.262.jar,"
                              "/opt/spark/jars/postgresql-42.6.0.jar") \
        .config("spark.sql.warehouse.dir", f"{os.getenv('STORAGE_PREFIX')}://{os.getenv('BUCKET_NAME')}/warehouse") \
        .config("spark.hadoop.javax.jdo.option.ConnectionURL", 
                f"jdbc:postgresql://{os.getenv('POSTGRES_HOST')}:5432/{os.getenv('POSTGRES_DB')}") \
        .config("spark.hadoop.javax.jdo.option.ConnectionDriverName", "org.postgresql.Driver") \
        .config("spark.hadoop.javax.jdo.option.ConnectionUserName", os.getenv("POSTGRES_USER")) \
        .config("spark.hadoop.javax.jdo.option.ConnectionPassword", os.getenv("POSTGRES_PASSWORD")) \
        .config("spark.hadoop.datanucleus.schema.autoCreateTables", "true") \
        .config("spark.hadoop.hive.metastore.schema.verification", "false")

    return builder.getOrCreate()
