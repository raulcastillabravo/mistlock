import azure.functions as func
from functions.register_user import bp as register_user_bp

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Register blueprints
app.register_blueprint(register_user_bp)
