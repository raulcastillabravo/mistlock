import os
import logging

import azure.functions as func
from dotenv import load_dotenv

load_dotenv()

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="get_secret")
def get_secret(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    username = req.params.get('username')

    if username == ADMIN_USERNAME:
        return func.HttpResponse(
            "super-secret-value-from-emulator",
            status_code=200
        )

    return func.HttpResponse(
        "Forbidden: You do not have access to this secret.",
        status_code=403
    )
