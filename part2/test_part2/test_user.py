#!/usr/bin/env python3
from app.models.user import User


def test_user_creation():
    user = User(first_name="John", last_name="Doe",
                email="john.doe@gmail.com")
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@gmail.com"
    assert user.is_admin is False  # Default value
    print("User creation test passed!")


if __name__ == "__main__":
    test_user_creation()
