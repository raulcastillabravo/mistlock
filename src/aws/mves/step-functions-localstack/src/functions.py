FUNCTIONS = {
    "LogUserLambdaArn": {
        "env_var": "LOG_USER_FUNCTION",
        "zip_path": "dist/log_user.zip",
        "handler": "log_user.handler",
    },
    "ValidateEmailLambdaArn": {
        "env_var": "VALIDATE_EMAIL_FUNCTION",
        "zip_path": "dist/validate_email.zip",
        "handler": "validate_email.handler",
    },
}
