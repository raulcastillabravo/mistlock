from src.managers.user_status import UserStatus, Status

def test_user_status_set_and_get():
    username = "test_user"
    user_status = UserStatus(username)
    
    user_status.set_status(Status.BUSY)
    assert user_status.get_status() == Status.BUSY
    
    user_status.set_status(Status.AVAILABLE)
    assert user_status.get_status() == Status.AVAILABLE

def test_user_status_none():
    user_status = UserStatus("non_existent_user")
    assert user_status.get_status() is None
