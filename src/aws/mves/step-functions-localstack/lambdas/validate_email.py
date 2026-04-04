import re

def handler(event, context):
    """Validate email format."""
    email = event.get("email")
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
    
    if re.search(regex, email):
        return {"status": "Valid", "email": email}
    else:
        raise ValueError(f"Invalid email format: {email}")
