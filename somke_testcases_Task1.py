from unittest.mock import patch

from A1_unit_testing.checkout_and_payment_new import check_cart, User, load_products_from_csv, checkout
from checkout_and_payment import checkoutAndPayment,ShoppingCart, Product
from logout import logout
from login import login
import pytest
import shutil
import os
import json
from unittest import mock

# Fixture to create a sample cart
@pytest.fixture
def Test_cart():
    return ShoppingCart()

@pytest.fixture
def Test_product():
    products = load_products_from_csv("products.csv")
    return products[0] if products else None

@pytest.fixture
def Test_product1():
    products = load_products_from_csv("products.csv")
    return products[1] if products else None

@pytest.fixture
def original_products_csv(tmp_path):
    original_path = "products.csv"
    copy_path = tmp_path / "products_copy.csv"
    shutil.copy(original_path, copy_path)
    return str(copy_path)

# Dummy user file
@pytest.fixture(scope='module')
def user_dummmy_file():
    shutil.copy('users.json', 'dummy_users.json')
    print("Dummy file created")
    yield

    os.remove('dummy_users.json')
    print("Dummy file removed")


# Check user registration
@pytest.fixture
def check_user_registered():
    return {"username": "Sasha", "password": "FierceCa%&t789", "wallet": 100}


# Open file stub
@pytest.fixture
def open_file_stub(monkeypatch, check_user_registered):
    read_data = json.dumps([check_user_registered])
    monkeypatch.setattr('builtins.open', mock.mock_open(read_data=read_data))


# Magic mock JSON
@pytest.fixture
def json_dump_mocked(monkeypatch):
    mock_test = mock.MagicMock()
    monkeypatch.setattr('json.dump', mock_test)
    return mock_test


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

#Test case1
def test_login(stub_logout, capsys, monkeypatch):
    with patch('builtins.input', side_effect=["Sasha", "FierceCa%&t789"]):
        user_data = login()
    #Assert that the login function returned the expected user data
    assert user_data["username"] == "Sasha"
    assert user_data["wallet"] == 75

#Test case 2
def test_add_item(stub_logout, capsys, monkeypatch):
    card1 = {"card_number": "1234 5678 9012 3456", "expiry_date": "12/24", "holder_name": "Sasha", "cvv": "123"}
    login_details = {"username": "Sasha", "wallet": 75, "cards": [card1]}
    cart = ShoppingCart()
    products = [Product("Backpack", 15, 1)]
    monkeypatch.setattr("checkout_and_payment.products", products)
    monkeypatch.setattr("checkout_and_payment.cart", cart)
    monkeypatch.setattr("builtins.input", fake_input(["1", "l", "y"]))
    checkoutAndPayment(login_details)
    out, err = capsys.readouterr()
    output = "Backpack added to your cart."
    assert output in out[30:]


#Test case 3 Test several products
def test_several_products(stub_logout, capsys, monkeypatch):
    login_details = {"username": "Sasha", "wallet": 75}
    card1 = {"card_number": "1234 5678 9012 3456", "expiry_date": "12/24", "holder_name": "Sasha", "cvv": "123"}
    login_details = {"username": "Sasha", "wallet": 75, "cards": [card1]}
    products = [Product("Backpack", 15, 1), Product("Banana", 15, 5), Product("Pens", 0.5, 10)]
    monkeypatch.setattr("checkout_and_payment.products", products)
    monkeypatch.setattr("builtins.input", fake_input(["l"]))
    checkoutAndPayment(login_details)
    out, err = capsys.readouterr()
    expected_o = "1. Backpack - $15.0 - Units: 1\n2. Banana - $15.0 - Units: 5\n3. Pens - $0.5 - Units: 10"
    assert expected_o in out[:96]

#Test case 4 End-to-End Test Case 1: Add Product to Cart, Query, and Logout
def test_add_product_to_cart_query_and_logout(Test_product, open_file_stub, user_dummmy_file, monkeypatch):
    mocker.side_effect = [{"username": "Alice", "wallet": 100.0}]

    # Simulate user input for username
    username = "Alice"

    # Login as a user
    user_info = {"username": username, "wallet": 100.0}
    user = User(user_info["username"], user_info["wallet"])

    cart = ShoppingCart()
    product_to_add = Test_product

    # Use monkeypatch to simulate user input
    user_inputs = ["Q", "Y", "L"]  # Simulate user entering "Q", "Y", and "L"
    monkeypatch.setattr('builtins.input', lambda _: user_inputs.pop(0))

    # Add product to cart
    cart.add_item(product_to_add)

    # Query the cart
    assert check_cart(user, cart) is False
    assert product_to_add in cart.retrieve_item()
    assert product_to_add.units == 10  # Ensure product count in inventory remains the same

    # Logout
    logout_result = logout(cart)
    assert logout_result is True


#Test case 5 End-to-End Test Case 2: Add Multiple Products to Cart, Checkout, and Logout
def test_add_multiple_products_to_cart_checkout_and_logout(Test_product,Test_product1, open_file_stub, mocker, user_dummmy_file):
    mocker.side_effect = [{"username": "Alice", "wallet": 100.0}]

    # Simulate user input for username
    username = "Alice"

    # Login as a user
    user_info = {"username": username, "wallet": 100.0}
    user = User(user_info["username"], user_info["wallet"])

    cart = ShoppingCart()

    # Add multiple products to cart
    product = Test_product
    cart.add_item(Test_product)
    product1 = Test_product1
    cart.add_item(Test_product1)

    # Proceed to checkout
    assert checkout(user, cart) is not None
    assert cart.retrieve_item() == []
    assert product.units == 9  # Ensure product units are updated
    assert product1.units == 14  # Ensure product units are updated
    assert user.wallet < user_info["wallet"]  # Ensure wallet deduction

    # Logout
    logout_result = logout(cart)
    assert logout_result is True


#Test case 6 End-to-End Test Case 3: Add Product to Cart, Remove, and Logout
def test_add_product_to_cart_remove_and_logout(Test_product, open_file_stub, mocker, user_dummmy_file):
    mocker.side_effect = [{"username": "Alice", "wallet": 100.0}]

    # Simulate user input for username
    username = "Alice"

    # Login as a user
    user_info = {"username": username, "wallet": 100.0}
    user = User(user_info["username"], user_info["wallet"])

    cart = ShoppingCart()
    product_to_add = Test_product

    # Add product to cart
    cart.add_item(product_to_add)

    # Remove the product from the cart
    cart.remove_item(product_to_add)

    assert product_to_add not in cart.retrieve_item()
    assert product_to_add.units == 10  # Ensure product is put back into the inventory

    # Logout
    logout_result = logout(cart)
    assert logout_result is True

#Test case 7
def test_product_out_of_stock(stub_logout, capsys, monkeypatch):
    login_details = {"username": "Sasha", "wallet": 75}
    card1 = {"card_number": "1234 5678 9012 3456", "expiry_date": "12/24", "holder_name": "Sasha", "cvv": "123"}
    login_details = {"username": "Sasha", "wallet": 75, "cards": [card1]}
    products = [Product("Banana", 15, 0)]
    monkeypatch.setattr("checkout_and_payment.products", products)
    monkeypatch.setattr("builtins.input", fake_input(["1","c","w","l"]))
    checkoutAndPayment(login_details)
    out, err = capsys.readouterr()
    expected_o = "Sorry, Banana is out of stock."
    assert expected_o in out[:96]

#Test case 8
def test_buy_wallet_valance_zero(capsys, monkeypatch):
    card1 = {"card_number": "1234 5678 9012 3456", "expiry_date": "12/24", "holder_name": "Sasha", "cvv": "123"}
    # card2 = {"card_number": "9876 5432 1098 7654", "expiry_date": "06/23", "holder_name": "Sasha", "cvv": "456"}
    login_details = {"username": "Sasha", "wallet": 0, "cards": [card1]}
    products = [Product("Backpack", 15, 1), Product("Banana", 15, 5), Product("Pens", 0.5, 10)]
    monkeypatch.setattr("checkout_and_payment.products", products)
    monkeypatch.setattr("builtins.input", fake_input(["1", "c", "y", "wallet", "l","y"]))
    checkoutAndPayment(login_details)
    captured = capsys.readouterr()
    # Assert that the prompt message is printed
    assert "You don't have enough money to complete the purchase." in captured.out

#Test case 9
def test_cart_not_empty(capsys, monkeypatch):
    card1 = {"card_number": "1234 5678 9012 3456", "expiry_date": "12/24", "holder_name": "Sasha", "cvv": "123"}
    # card2 = {"card_number": "9876 5432 1098 7654", "expiry_date": "06/23", "holder_name": "Sasha", "cvv": "456"}
    login_details = {"username": "Sasha", "wallet": 0, "cards": [card1]}
    products = [Product("Backpack", 15, 1), Product("Banana", 15, 5), Product("Pens", 0.5, 10)]
    monkeypatch.setattr("checkout_and_payment.products", products)
    monkeypatch.setattr("builtins.input", fake_input(["1", "c", "y", "wallet", "l","y"]))
    checkoutAndPayment(login_details)
    captured = capsys.readouterr()
    # Assert that the prompt message is printed
    assert "Your cart is not empty." in captured.out

#Test case 10
def test_log_out(capsys, monkeypatch):
    card1 = {"card_number": "1234 5678 9012 3456", "expiry_date": "12/24", "holder_name": "Sasha", "cvv": "123"}
    login_details = {"username": "Sasha", "wallet": 75, "cards": [card1]}
    products = [Product("Backpack", 15, 1), Product("Banana", 15, 5), Product("Pens", 0.5, 10)]
    monkeypatch.setattr("checkout_and_payment.products", products)
    monkeypatch.setattr("builtins.input", fake_input(["1", "c", "y", "wallet", "l"]))
    checkoutAndPayment(login_details)
    captured = capsys.readouterr()

    # Assert that the prompt message is printed
    assert "You have been logged out" in captured.out





