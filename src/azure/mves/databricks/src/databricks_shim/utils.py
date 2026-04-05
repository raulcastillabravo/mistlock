import os

class SecretsMock:
    def get(self, scope, key):
        """Mock for dbutils.secrets.get backed by env vars."""
        # Ignores scope in local mode, just looks for key
        val = os.getenv(key) or os.getenv(f"{scope}_{key}".upper())
        if val is None:
            raise ValueError(f"Secret '{key}' not found in environment.")
        return val

class WidgetsMock:
    def get(self, name):
        """Mock for dbutils.widgets.get backed by env vars."""
        return os.getenv(name)
        
    def text(self, name, defaultValue, label=None):
        pass # No-op in non-interactive mode

class FSMock:
    def ls(self, path):
        print(f"[Mock] Listing {path} not implemented fully in local.")
        return []

class DBUtilsShim:
    """
    Shim to mock Databricks DBUtils in local environments.
    This is a partial mock and should be extended with additional methods 
    (from fs, secrets, notebooks, etc.) based on specific project needs.
    """
    def __init__(self, spark=None):
        self.secrets = SecretsMock()
        self.widgets = WidgetsMock()
        self.fs = FSMock()

def get_dbutils(spark):
    """
    Returns DBUtils. Tries to import from pyspark.dbutils (Databricks),
    falls back to Shim (Local).
    """
    try:
        from pyspark.dbutils import DBUtils
        return DBUtils(spark)
    except ImportError:
        return DBUtilsShim(spark)
