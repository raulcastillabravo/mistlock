import pytest
from src.managers.user_status import UserStatus, Status

def test_user_status_set_and_get():
    """Test setting and getting user status using UserStatus manager."""
    username = "test_user"
    user_status = UserStatus(username)
    
    user_status.set_status(Status.BUSY)
    assert user_status.get_status() == Status.BUSY
    
    user_status.set_status(Status.AVAILABLE)
    assert user_status.get_status() == Status.AVAILABLE

def test_user_status_none():
    """Test getting status for a non-existent user."""
    user_status = UserStatus("non_existent_user")
    assert user_status.get_status() is None
