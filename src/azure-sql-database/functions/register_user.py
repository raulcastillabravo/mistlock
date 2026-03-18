import azure.functions as func
import logging
from shared.database import save_user

bp = func.Blueprint()

@bp.route(route="users", methods=["POST"])
def register_user(req: func.HttpRequest) -> func.HttpResponse:
    """HTTP Trigger that receives user data and saves it to SQL.
    
    Expected body: {"name": "John Doe", "email": "john@example.com"}
    """
    logging.info('Processing a new user registration...')

    try:
        req_body = req.get_json()
        name = req_body.get('name')
        email = req_body.get('email')

        if not name or not email:
            return func.HttpResponse(
                "Please provide name and email in the request body",
                status_code=400
            )

        # Save to database
        save_user(name, email)

        return func.HttpResponse(
            f"User {name} successfully registered!",
            status_code=201
        )
    except Exception as e:
        logging.info(f"Error saving user: {str(e)}")
        return func.HttpResponse(
            f"An error occurred: {str(e)}",
            status_code=500
        )
