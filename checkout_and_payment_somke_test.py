from unittest.mock import patch

from checkout_and_payment_task2_inplementation import checkoutAndPayment, ShoppingCart, Product
from logout import logout
from login import login
import pytest
import shutil
import os
import json
from unittest import mock

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
    return {"username": "Simba", "password": "LionKing@^456", "wallet": 100}


# Open file stub
@pytest.fixture
def open_file_stub(monkeypatch, user_registered):
    read_data = json.dumps([user_registered])
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


# Fake input
def fake_input(input_list):
    i = 0

    def _fake_input(foo_bar):
        nonlocal i
        mimicked_input = input_list[i]
        i += 1
        return mimicked_input

    return _fake_input


def test_login(stub_logout, capsys, monkeypatch):
    with patch('builtins.input', side_effect=["Simba", "LionKing@^456"]):
        user_data = login()
    #Assert that the login function returned the expected user data
    assert user_data["username"] == "Simba"
    assert user_data["wallet"] == 100

def test_add_item(stub_logout, capsys, monkeypatch):
    card1 = {"card_number": "1234 5678 9012 3456", "expiry_date": "12/24", "holder_name": "Simba", "cvv": "123"}
    login_details = {"username": "Simba", "wallet": 100, "cards": [card1]}
    cart = ShoppingCart()
    products = [Product("Backpack", 15, 1)]
    monkeypatch.setattr("checkout_and_payment.products", products)
    monkeypatch.setattr("checkout_and_payment.cart", cart)
    monkeypatch.setattr("builtins.input", fake_input(["1", "l", "y"]))
    checkoutAndPayment(login_details)
    out, err = capsys.readouterr()
    output = "Backpack added to your cart."
    assert output in out[30:]


# Test several products
def test_several_products(stub_logout, capsys, monkeypatch):
    login_details = {"username": "Simba", "wallet": 100}
    card1 = {"card_number": "1234 5678 9012 3456", "expiry_date": "12/24", "holder_name": "Simba", "cvv": "123"}
    login_details = {"username": "Simba", "wallet": 100, "cards": [card1]}
    products = [Product("Backpack", 15, 1), Product("Banana", 15, 5), Product("Pens", 0.5, 10)]
    monkeypatch.setattr("checkout_and_payment.products", products)
    monkeypatch.setattr("builtins.input", fake_input(["l"]))
    checkoutAndPayment(login_details)
    out, err = capsys.readouterr()
    expected_o = "1. Backpack - $15.0 - Units: 1\n2. Banana - $15.0 - Units: 5\n3. Pens - $0.5 - Units: 10"
    assert expected_o in out[:96]

def test_product_out_of_stock(stub_logout, capsys, monkeypatch):
    login_details = {"username": "Simba", "wallet": 100}
    card1 = {"card_number": "1234 5678 9012 3456", "expiry_date": "12/24", "holder_name": "Simba", "cvv": "123"}
    login_details = {"username": "Simba", "wallet": 100, "cards": [card1]}
    products = [Product("Banana", 15, 0)]
    monkeypatch.setattr("checkout_and_payment.products", products)
    monkeypatch.setattr("builtins.input", fake_input(["1","c","w","l"]))
    checkoutAndPayment(login_details)
    out, err = capsys.readouterr()
    expected_o = "Sorry, Banana is out of stock."
    assert expected_o in out[:96]
def test_buyWithWallet(capsys, monkeypatch):
    card1 = {"card_number": "1234 5678 9012 3456", "expiry_date": "12/24", "holder_name": "Simba", "cvv": "123"}
    # card2 = {"card_number": "9876 5432 1098 7654", "expiry_date": "06/23", "holder_name": "Simba", "cvv": "456"}
    login_details = {"username": "Simba", "wallet": 100, "cards": [card1]}
    products = [Product("Backpack", 15, 1), Product("Banana", 15, 5), Product("Pens", 0.5, 10)]
    monkeypatch.setattr("checkout_and_payment.products", products)
    monkeypatch.setattr("builtins.input", fake_input(["1", "c", "y", "wallet", "l"]))
    checkoutAndPayment(login_details)
    captured = capsys.readouterr()

    # Assert that the prompt message is printed
    assert "Thank you for your purchase, Simba! Your remaining balance is 85.0" in captured.out

def test_buy_wallet_valance_zero(capsys, monkeypatch):
    card1 = {"card_number": "1234 5678 9012 3456", "expiry_date": "12/24", "holder_name": "Simba", "cvv": "123"}
    # card2 = {"card_number": "9876 5432 1098 7654", "expiry_date": "06/23", "holder_name": "Simba", "cvv": "456"}
    login_details = {"username": "Simba", "wallet": 0, "cards": [card1]}
    products = [Product("Backpack", 15, 1), Product("Banana", 15, 5), Product("Pens", 0.5, 10)]
    monkeypatch.setattr("checkout_and_payment.products", products)
    monkeypatch.setattr("builtins.input", fake_input(["1", "c", "y", "wallet", "l","y"]))
    checkoutAndPayment(login_details)
    captured = capsys.readouterr()
    # Assert that the prompt message is printed
    assert "You don't have enough money to complete the purchase." in captured.out


def test_showSingleCard(capsys, monkeypatch):
    card1 = {"card_number": "1234 5678 9012 3456", "expiry_date": "12/24", "holder_name": "Simba", "cvv": "123"}
    login_details = {"username": "Simba", "wallet": 100,"cards":[card1]}
    products = [Product("Backpack", 15, 1), Product("Banana", 15, 5), Product("Pens", 0.5, 10)]
    monkeypatch.setattr("checkout_and_payment.products", products)
    monkeypatch.setattr("builtins.input", fake_input(["1","c","y","card","1","l"]))
    checkoutAndPayment(login_details)
    captured = capsys.readouterr()
    # Assert that the prompt message is printed
    assert "1. {'card_number': '1234 5678 9012 3456', 'expiry_date': '12/24" in captured.out


def test_showMultipleCard(capsys, monkeypatch):
    card1 = {"card_number": "1234 5678 9012 3456", "expiry_date": "12/24", "holder_name": "Simba", "cvv": "123"}
    card2 = {"card_number": "9876 5432 1098 7654", "expiry_date": "06/23", "holder_name": "Simba", "cvv": "456"}
    login_details = {"username": "Simba", "wallet": 100,"cards":[card1,card2]}
    products = [Product("Backpack", 15, 1), Product("Banana", 15, 5), Product("Pens", 0.5, 10)]
    monkeypatch.setattr("checkout_and_payment.products", products)
    monkeypatch.setattr("builtins.input", fake_input(["1","c","y","card","1","l"]))
    checkoutAndPayment(login_details)
    captured = capsys.readouterr()
    # Assert that the prompt message is printed
    assert "1. {'card_number': '1234 5678 9012 3456', 'expiry_date': '12/24', 'holder_name': 'Simba', 'cvv': '123'}\n2. {'card_number': '9876 5432 1098 7654', 'expiry_date': '06/23', 'holder_name': 'Simba', 'cvv': '456'}" in captured.out

def test_buyWithCard(capsys, monkeypatch):
    card1 = {"card_number": "1234 5678 9012 3456", "expiry_date": "12/24", "holder_name": "Simba", "cvv": "123"}
    login_details = {"username": "Simba", "wallet": 100,"cards":[card1]}
    products = [Product("Backpack", 15, 1), Product("Banana", 15, 5), Product("Pens", 0.5, 10)]
    monkeypatch.setattr("checkout_and_payment.products", products)
    monkeypatch.setattr("builtins.input", fake_input(["1","c","y","card","1","l"]))
    checkoutAndPayment(login_details)
    captured = capsys.readouterr()
    # Assert that the prompt message is printed
    assert "Payment using card 1 successful." in captured.out

def test_cart_not_empty(capsys, monkeypatch):
    card1 = {"card_number": "1234 5678 9012 3456", "expiry_date": "12/24", "holder_name": "Simba", "cvv": "123"}
    # card2 = {"card_number": "9876 5432 1098 7654", "expiry_date": "06/23", "holder_name": "Simba", "cvv": "456"}
    login_details = {"username": "Simba", "wallet": 0, "cards": [card1]}
    products = [Product("Backpack", 15, 1), Product("Banana", 15, 5), Product("Pens", 0.5, 10)]
    monkeypatch.setattr("checkout_and_payment.products", products)
    monkeypatch.setattr("builtins.input", fake_input(["1", "c", "y", "wallet", "l","y"]))
    checkoutAndPayment(login_details)
    captured = capsys.readouterr()
    # Assert that the prompt message is printed
    assert "Your cart is not empty." in captured.out

def test_log_out(capsys, monkeypatch):
    card1 = {"card_number": "1234 5678 9012 3456", "expiry_date": "12/24", "holder_name": "Simba", "cvv": "123"}
    login_details = {"username": "Simba", "wallet": 100, "cards": [card1]}
    products = [Product("Backpack", 15, 1), Product("Banana", 15, 5), Product("Pens", 0.5, 10)]
    monkeypatch.setattr("checkout_and_payment.products", products)
    monkeypatch.setattr("builtins.input", fake_input(["1", "c", "y", "wallet", "l"]))
    checkoutAndPayment(login_details)
    captured = capsys.readouterr()

    # Assert that the prompt message is printed
    assert "You have been logged out" in captured.out
