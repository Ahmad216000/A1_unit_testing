import json
from unittest.mock import patch
import login
import profile_modification
from logout import logout
from checkout_and_payment import ShoppingCart, Product


# Test for password validation function
def test_valid_password1():
    valid_password = "Testpass@"
    assert login.is_valid_password(valid_password) == True


def test_valid_password2():
    valid_password = "Testpass2!"
    assert login.is_valid_password(valid_password) == True


def test_invalid_password1():
    invalid_password = "pass1234"
    assert login.is_valid_password(invalid_password) == False


def test_invalid_password2():
    invalid_password = "weakpass!"
    assert login.is_valid_password(invalid_password) == False


def test_login_with_valid_credentials1():
    # Create a user in the users file or append to existing data
    try:
        with open('users.json', 'r') as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        existing_data = []

    # Append new user data to existing or create new data
    new_user_data = {"username": "testuser", "password": "Testpass@", "wallet": 0}
    existing_data.append(new_user_data)

    # Write the updated data back to users.json
    with open('users.json', "w") as file:
        json.dump(existing_data, file, indent=4)

    # Simulate logging in with valid credentials
    with patch('builtins.input', side_effect=["testuser", "Testpass@"]):
        user_data = login.login()

    # Assert that the login function returned the expected user data
    assert user_data["username"] == "testuser"
    assert user_data["wallet"] == 0


def test_logout_with_empty_cart():
    cart = ShoppingCart()
    result = logout(cart)
    assert result is True


def test_logout_with_non_empty_cart_logout_confirmed():
    cart = ShoppingCart()
    cart.add_item(Product("Product 1", 10.0, 2))
    cart.add_item(Product("Product 2", 15.0, 1))
    cart.add_item(Product("Product 3", 20.0, 3))

    with patch('builtins.input', side_effect=["Y"]):
        result = logout(cart)

    assert result is True
    assert len(cart.retrieve_item()) == 0


def test_logout_with_non_empty_cart_logout_cancelled():
    cart = ShoppingCart()
    cart.add_item(Product("Product A", 8.0, 1))
    cart.add_item(Product("Product B", 12.0, 4))

    with patch('builtins.input', side_effect=["N"]):
        result = logout(cart)

    assert result is False
    assert len(cart.retrieve_item()) == 2


def test_logout_with_single_item_cart_logout_confirmed():
    cart = ShoppingCart()
    cart.add_item(Product('Single Product', 5.0, 1))

    with patch('builtins.input', side_effect=["Y"]):
        result = logout(cart)

    assert result is True
    assert len(cart.retrieve_item()) == 0


def test_logout_with_multiple_items_invalid_input():
    cart = ShoppingCart()
    cart.add_item(Product('Item X', 8.0, 2))
    cart.add_item(Product('Item Y', 10.0, 3))

    with patch('builtins.input', side_effect=["W"]):
        result = logout(cart)

    assert result is False
    assert len(cart.retrieve_item()) == 2


def test_user_registration_with_additional_details():
    # Load existing data from users.json if available
    try:
        with open('users.json', 'r') as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        existing_data = []

    new_user_data = {
        "username": "testuser2",
        "password": "Testpass@!",
        "wallet": 0,
        "address": "Karlaplan 1",
        "phone_number": "073222222",
        "email": "change_email@uu.se",
        "credit_cards": [
            {
                "card_number": "6666-5555-4444-3333",
                "expiry_date": "12/30",
                "name_on_card": "Uppsala Student",
                "cvv": "963"
            }
        ]
    }

    # Append the new user data to existing_data
    existing_data.append(new_user_data)

    # Write the updated data back to users.json
    with open('users.json', "w") as file:
        json.dump(existing_data, file, indent=4)

    # Simulate logging in with valid credentials
    with patch('builtins.input', side_effect=["testuser2", "Testpass@!"]):
        user_data = login.login()

    # Assert that the login function returned the expected user data
    assert user_data["username"] == "testuser2"
    assert user_data["wallet"] == 0
    assert user_data["address"] == "Karlaplan 1"
    assert user_data['phone_number'] == "073222222"
    assert user_data['email'] == "change_email@uu.se"
    assert user_data['credit_cards'][0]['card_number'] == "6666-5555-4444-3333"
    assert user_data['credit_cards'][0]['expiry_date'] == "12/30"
    assert user_data['credit_cards'][0]['name_on_card'] == "Uppsala Student"


def test_add_user_details():
    # Create test input data
    test_username = "Ramanathan"
    test_address = "Karlaplan 2"
    test_phone_number = "0711122233"
    test_email = "change_email@uu.se"
    test_card_number = "6666555544443355"
    test_expiry_date = "12/30"
    test_name_on_card = "Uppsala Student"
    test_cvv = "963"

    # Simulate user input for the function
    with patch('builtins.input',
               side_effect=[test_address, test_phone_number, test_email, test_card_number, test_expiry_date,
                            test_name_on_card, test_cvv]):
        # Call the function with the test username
        updated_user = profile_modification.add_user_details(test_username)

    # Assert that the updated_user data matches the expected values
    assert updated_user["username"] == test_username
    assert updated_user["address"] == test_address
    assert updated_user['phone_number'] == test_phone_number
    assert updated_user['email'] == test_email
    assert updated_user['credit_cards'][0]['card_number'] == test_card_number
    assert updated_user['credit_cards'][0]['expiry_date'] == test_expiry_date
    assert updated_user['credit_cards'][0]['name_on_card'] == test_name_on_card
    assert updated_user['credit_cards'][0]['cvv'] == test_cvv


def test_update_details_for_same_user():
    # Create test another input data
    test_username = "Ramanathan"
    test_address = "Karlaplan 5"
    test_phone_number = "0711155555"
    test_email = "update_email@uu.se"
    test_card_number = "1234567890123456"
    test_expiry_date = "12/24"
    test_name_on_card = "Stockholm Student"
    test_cvv = "555"

    # Simulate user input for the function
    with patch('builtins.input',
               side_effect=[test_address, test_phone_number, test_email, test_card_number, test_expiry_date,
                            test_name_on_card, test_cvv]):
        # Call the function with the test username
        updated_user = profile_modification.update_user_details(test_username)

    # Assert that the updated_user data matches the expected values
    assert updated_user["username"] == test_username
    assert updated_user["address"] == test_address
    assert updated_user['phone_number'] == test_phone_number
    assert updated_user['email'] == test_email
    assert updated_user['credit_cards'][0]['card_number'] == test_card_number
    assert updated_user['credit_cards'][0]['expiry_date'] == test_expiry_date
    assert updated_user['credit_cards'][0]['name_on_card'] == test_name_on_card
    assert updated_user['credit_cards'][0]['cvv'] == test_cvv
