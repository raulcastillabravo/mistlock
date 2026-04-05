import zipfile
import io
import os

def create_lambda_zip(file_path):
    """Create a ZIP file containing the lambda function."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.write(file_path, arcname=os.path.basename(file_path))
    return buf.getvalue()

def get_boto_config():
    """Returns standard boto3 configuration for LocalStack."""
    return {
        "endpoint_url": os.getenv("LOCALSTACK_ENDPOINT", "http://localhost:4566"),
        "region_name": os.getenv("AWS_REGION", "us-east-1"),
        "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID", "test"),
        "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY", "test")
    }

def deploy_lambda(client, name, handler, zip_data, role, env_vars=None):
    """Create or update a Lambda function with environment variables."""
    params = {
        "FunctionName": name,
        "Runtime": "python3.14",
        "Role": role,
        "Handler": handler,
        "Code": {"ZipFile": zip_data},
        "Timeout": 30
    }
    if env_vars:
        params["Environment"] = {"Variables": env_vars}

    try:
        res = client.create_function(**params)
        print(f"Lambda '{name}' created.")
        return res["FunctionArn"]
    except client.exceptions.ResourceConflictException:
        client.update_function_code(FunctionName=name, ZipFile=zip_data)
        client.get_waiter("function_updated").wait(FunctionName=name)
        
        config_params = {"FunctionName": name, "Timeout": 30}
        if env_vars:
            config_params["Environment"] = {"Variables": env_vars}
        
        client.update_function_configuration(**config_params)
        print(f"Lambda '{name}' updated.")
        
        region = client.meta.region_name
        return f"arn:aws:lambda:{region}:000000000000:function:{name}"
