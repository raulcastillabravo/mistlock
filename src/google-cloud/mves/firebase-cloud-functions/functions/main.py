import os
import json
from firebase_functions import https_fn, logger
from firebase_functions.params import IntParam, StringParam

MIN_INSTANCES = IntParam("MIN_INSTANCES")
ADMIN_USER = StringParam("ADMIN_USER")

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
        return https_fn.Response(json.dumps({"secret": secret_value}))
    else:
        logger.error(f"Error: Access denied for user '{username}'")
        return https_fn.Response(json.dumps({"error": "Access Denied"}), status=403)
