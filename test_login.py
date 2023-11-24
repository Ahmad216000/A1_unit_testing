import json
from unittest.mock import patch
import login

# Test for password validation function
def test_valid_password():
    valid_password = "Testpass@"
    assert login.is_valid_password(valid_password) == True

def test_invalid_password():
    invalid_password = "weakpass"
    assert login.is_valid_password(invalid_password) == False

def test_login_with_valid_credentials():
    # Create a user in the users file
    with open('users.json', "w") as file:
        data = [{"username": "testuser", "password": "Testpass@", "wallet": 0}]
        json.dump(data, file, indent=4)

    # Simulate logging in with valid credentials
    with patch('builtins.input', side_effect=["testuser", "Testpass@"]):
        user_data = login.login()

    # Assert that the login function returned the expected user data
    assert user_data["username"] == "testuser"
    assert user_data["wallet"] == 0

