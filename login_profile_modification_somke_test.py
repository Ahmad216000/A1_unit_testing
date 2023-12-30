import login
import profile_modification
from unittest.mock import patch
from checkout_and_payment import checkoutAndPayment, ShoppingCart, Product
from logout import logout
import json
import pytest
from unittest import mock


# Logout stub
@pytest.fixture
def stub_logout(mocker):
    return mocker.patch('logout.logout', return_value=True)


@pytest.fixture
def mocker():
    return mock.Mock()


# Fake input
def fake_input(input_list):
    i = 0

    def _fake_input(foo_bar):
        nonlocal i
        mimicked_input = input_list[i]
        i += 1
        return mimicked_input

    return _fake_input


def test_password_and_valid_login():
    # Test valid and invalid passwords
    valid_password = "Testpass2!"
    invalid_password = "pass1234"

    assert login.is_valid_password(valid_password) == True
    assert login.is_valid_password(invalid_password) == False

    # Test valid login credentials
    with patch('builtins.input', side_effect=["Ramanathan", "Notaproblem23*"]):
        user_data = login.login()
    assert user_data is not None  # Assuming login returns user data upon success


def test_user_registration_with_additional_details():
    # Load existing data from users.json if available
    try:
        with open('users.json', 'r') as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        existing_data = []

    new_user_data = {
        "username": "somke",
        "password": "Testpass@!",
        "wallet": 0,
        "address": "Uppsalasvagen 1",
        "phone_number": "073222999",
        "email": "uppsala_email@uu.se",
        "credit_cards": [
            {
                "card_number": "1234567890123456",
                "expiry_date": "12/24",
                "name_on_card": "Uppsala Student",
                "cvv": "999"
            }
        ]
    }

    # Append the new user data to existing_data
    existing_data.append(new_user_data)

    # Write the updated data back to users.json
    with open('users.json', "w") as file:
        json.dump(existing_data, file, indent=4)

    # Simulate logging in with valid credentials
    with patch('builtins.input', side_effect=["somke", "Testpass@!"]):
        user_data = login.login()

    # Assert that the login function returned the expected user data
    assert user_data["username"] == "somke"
    assert user_data["wallet"] == 0
    assert user_data["address"] == "Uppsalasvagen 1"
    assert user_data['phone_number'] == "073222999"
    assert user_data['email'] == "uppsala_email@uu.se"
    assert user_data['credit_cards'][0]['card_number'] == "1234567890123456"
    assert user_data['credit_cards'][0]['expiry_date'] == "12/24"
    assert user_data['credit_cards'][0]['name_on_card'] == "Uppsala Student"
    assert user_data['credit_cards'][0]['cvv'] == "999"


def test_add_user_details():
    # Create test input data
    test_username = "Maximus"
    test_address = "cantralsvagen 2"
    test_phone_number = "0711122222"
    test_email = "new_email@uu.se"
    test_card_number = "6666555544443333"
    test_expiry_date = "01/25"
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
    test_username = "Maximus"
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


def test_add_item(stub_logout, capsys, monkeypatch):
    card1 = {"card_number": "1234567890123456", "expiry_date": "12/24", "holder_name": "Stockholm Student",
             "cvv": "555"}
    login_details = {"username": "Maximus", "wallet": 75, "cards": [card1]}
    cart = ShoppingCart()
    products = [Product("Laptop Mouse", 15, 1)]
    monkeypatch.setattr("checkout_and_payment.products", products)
    monkeypatch.setattr("checkout_and_payment.cart", cart)
    monkeypatch.setattr("builtins.input", fake_input(["1", "l", "y"]))
    checkoutAndPayment(login_details)
    out, err = capsys.readouterr()
    output = "Laptop Mouse added to your cart."
    assert output in out[30:]


def test_buy_with_wallet(capsys, monkeypatch):
    card1 = {"card_number": "1234567890123456", "expiry_date": "12/24", "holder_name": "Stockholm Student",
             "cvv": "555"}
    # card2 = {"card_number": "9876 5432 1098 7654", "expiry_date": "06/23", "holder_name": "Simba", "cvv": "456"}
    login_details = {"username": "Maximus", "wallet": 100, "cards": [card1]}
    products = [Product("Laptop Mouse", 15, 1), Product("Banana", 15, 5), Product("Pens", 0.5, 10)]
    monkeypatch.setattr("checkout_and_payment.products", products)
    monkeypatch.setattr("builtins.input", fake_input(["1", "c", "y", "wallet", "l"]))
    checkoutAndPayment(login_details)
    captured = capsys.readouterr()

    # Assert that the prompt message is printed
    assert "Thank you for your purchase, Maximus! Your remaining balance is 85.0" in captured.out


def test_several_products(stub_logout, capsys, monkeypatch):
    card1 = {"card_number": "1234567890123456", "expiry_date": "12/24", "holder_name": "Stockholm Student",
             "cvv": "555"}
    login_details = {"username": "Maximus", "wallet": 75, "cards": [card1]}
    products = [Product("Backpack", 15, 1), Product("Laptop Mouse", 15, 5), Product("Pens", 0.5, 10)]
    monkeypatch.setattr("checkout_and_payment.products", products)
    monkeypatch.setattr("builtins.input", fake_input(["l"]))
    checkoutAndPayment(login_details)
    out, err = capsys.readouterr()
    expected_o = "1. Backpack - $15.0 - Units: 1\n2. Laptop Mouse - $15.0 - Units: 5\n3. Pens - $0.5 - Units: 10"
    assert expected_o in out[:96]


def test_product_out_of_stock(stub_logout, capsys, monkeypatch):
    card1 = {"card_number": "1234567890123456", "expiry_date": "12/24", "holder_name": "Stockholm Student",
             "cvv": "555"}
    login_details = {"username": "Maximus", "wallet": 75, "cards": [card1]}
    products = [Product("Laptop Mouse", 15, 0)]
    monkeypatch.setattr("checkout_and_payment.products", products)
    monkeypatch.setattr("builtins.input", fake_input(["1", "c", "w", "l"]))
    checkoutAndPayment(login_details)
    out, err = capsys.readouterr()
    expected_o = "Sorry, Laptop Mouse is out of stock."
    assert expected_o in out[:96]


def test_cart_not_empty(capsys, monkeypatch):
    card1 = {"card_number": "1234567890123456", "expiry_date": "12/24", "holder_name": "Stockholm Student",
             "cvv": "555"}
    login_details = {"username": "Maximus", "wallet": 0, "cards": [card1]}
    products = [Product("Laptop Mouse", 15, 1), Product("Banana", 15, 5), Product("Pens", 0.5, 10)]
    monkeypatch.setattr("checkout_and_payment.products", products)
    monkeypatch.setattr("builtins.input", fake_input(["1", "c", "y", "wallet", "l", "y"]))
    checkoutAndPayment(login_details)
    captured = capsys.readouterr()
    # Assert that the prompt message is printed
    assert "Your cart is not empty." in captured.out


def test_logout_with_non_empty_cart_logout_cancelled():
    cart = ShoppingCart()
    cart.add_item(Product("Product A", 8.0, 1))
    cart.add_item(Product("Product B", 12.0, 4))

    with patch('builtins.input', side_effect=["N"]):
        result = logout(cart)

    assert result is False
    assert len(cart.retrieve_item()) == 2


def test_logout_with_multiple_items_invalid_input():
    cart = ShoppingCart()
    cart.add_item(Product('Item X', 8.0, 2))
    cart.add_item(Product('Item Y', 10.0, 3))

    with patch('builtins.input', side_effect=["W"]):
        result = logout(cart)

    assert result is False
    assert len(cart.retrieve_item()) == 2
