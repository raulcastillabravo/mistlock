import azure.functions as func
from shared.db_utils import get_session
from shared.user import User

bp = func.Blueprint()

@bp.route(route="users", methods=["POST"])
def register_user(req: func.HttpRequest) -> func.HttpResponse:
    """HTTP Trigger that receives user data and saves it to SQL.
    
    Expected body: {"name": "John Doe", "email": "john@example.com"}
    """

    req_body = req.get_json()
    name = req_body['name']
    email = req_body['email']
    new_user = User(Name=name, Email=email)

    with get_session() as session:
        session.add(new_user)
        session.commit()

    return func.HttpResponse(
        f"User {name} successfully registered!",
        status_code=201
    )
