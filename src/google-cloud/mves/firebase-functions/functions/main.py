import os
import logging
from firebase_functions import https_fn
from firebase_functions.params import IntParam, StringParam

# Parameters
# These are loaded from .env.local in development
MIN_INSTANCES = IntParam("MIN_INSTANCES")
ADMIN_USER = StringParam("ADMIN_USER")

# Initialize standard logging
# Firebase Functions captures logs from the standard logging library
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@https_fn.on_request(
    min_instances=MIN_INSTANCES,
    secrets=["MY_SECRET"]
)
def get_secret(req: https_fn.Request) -> https_fn.Response:
    """
    Returns a secret if the username parameter matches the ADMIN_USER.
    """
    username: str = req.args.get("username", "")

    if username == ADMIN_USER.value:
        logger.info(f"Success: Authorized access for user {username}")
        secret_value = os.environ.get("MY_SECRET", "No secret found")
        return https_fn.Response(f"Secret: {secret_value}")
    else:
        logger.error(f"Error: Access denied for user {username}")
        return https_fn.Response("Access Denied", status=403)
