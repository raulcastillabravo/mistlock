import azure.functions as func
from shared.database import save_user

bp = func.Blueprint()

@bp.route(route="users", methods=["POST"])
def register_user(req: func.HttpRequest) -> func.HttpResponse:
    """HTTP Trigger that receives user data and saves it to SQL.
    
    Expected body: {"name": "John Doe", "email": "john@example.com"}
    """

    req_body = req.get_json()
    name = req_body['name']
    email = req_body['email']

    save_user(name, email)

    return func.HttpResponse(
        f"User {name} successfully registered!",
        status_code=201
    )

