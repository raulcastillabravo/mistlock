import os
import logging
import azure.functions as func
from azurite_client import AzuriteClient

app = func.FunctionApp()

@app.function_name(name="UploadFile")
@app.route(route="upload", methods=["POST"])
def upload_file(req: func.HttpRequest) -> func.HttpResponse:
    """HTTP trigger function that uploads a file to Azurite."""
    logging.info("Processing file upload request.")

    filename = req.params.get("filename")
    if not filename:
        return func.HttpResponse(
            "Please provide a filename parameter.", status_code=400
        )
    
    file_data = req.get_body()
    container_name = os.getenv("BLOB_CONTAINER_NAME", "uploads")
    client = AzuriteClient()
    client.create_container(container_name)
    client.upload_blob(container_name, filename, file_data)
    logging.info(f"File '{filename}' uploaded successfully.")
    
    return func.HttpResponse(
        f"File '{filename}' uploaded to '{container_name}'.",
        status_code=200
    )


