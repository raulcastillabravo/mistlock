import random
import string
from models import User, get_session

def lambda_handler(event, context):
    session = get_session()
    
    # Note: Creating the table here for simplicity in this MVE.
    # In a production environment, this should be handled separately.
    User.__table__.create(session.get_bind(), checkfirst=True)
    
    # Generate random ID for user format: user[1234]@example.com
    random_id = "".join(random.choices(string.digits, k=4))
    user_name = f"user{random_id}"
    user_email = f"{user_name}@example.com"
    
    user = User(name=user_name, email=user_email)
    
    session.add(user)
    session.commit()
    
    print(f"User {user_name} created successfully!")
    return {"status": "success", "user": user_name}
