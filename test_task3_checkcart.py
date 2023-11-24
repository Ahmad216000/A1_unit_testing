import json
import shutil
from unittest.mock import patch

import pytest
from checkout_and_payment import *


# Fixture to create a sample user
@pytest.fixture
def Test_user():
    with open("users.json") as user_file:
        user_data_list = json.load(user_file)
        # Assuming there's at least one user in the list
        user_data = user_data_list[0]
    return User(user_data["username"], user_data["wallet"])


# Fixture to create a sample product
@pytest.fixture
def Test_product():
    products = load_products_from_csv("products.csv")
    return products[0] if products else None


# Fixture to create a sample cart
@pytest.fixture
def Test_cart():
    return ShoppingCart()

@pytest.fixture
def original_products_csv(tmp_path):
    original_path = "products.csv"
    copy_path = tmp_path / "products_copy.csv"
    shutil.copy(original_path, copy_path)
    return str(copy_path)

# TestCase1: Test to check "print(i.get_product())"working as expected in check_cart
def test_check_cart_print_product_details(capsys, Test_user, Test_cart, Test_product):
    Test_cart.add_item(Test_product)
    Test_cart.retrieve_item()
    print(Test_cart.retrieve_item()[0].get_product())
    captured = capsys.readouterr()
    # Access the captured output
    printed_output = captured.out
    assert Test_product.name in printed_output


# TestCase2: User checks out an empty cart
def test_check_cart_empty_cart(capsys,Test_user, Test_cart):
    with patch('builtins.input', return_value='Y'):
        check_cart(Test_user, Test_cart)
        captured = capsys.readouterr()
        assert "Your basket is empty" in captured.out

# Test Case 3: User checks out with items in the cart
def test_check_cart_with_checkout(Test_user, Test_cart, Test_product):
    Test_cart.add_item(Test_product)
    with patch('builtins.input', return_value='Y'), patch('checkout_and_payment.checkout') as mock_checkout:
        assert check_cart(Test_user, Test_cart)
        mock_checkout.assert_called_once_with(Test_user, Test_cart)

# Test Case 4: User checks out with insufficient funds
def test_check_cart_insufficient_funds(Test_user, Test_cart, Test_product, capsys):
    Test_user.wallet = 1.0
    Test_cart.add_item(Test_product)
    with patch('builtins.input', return_value='Y'):
        check_cart(Test_user, Test_cart)
        captured = capsys.readouterr()
        assert "You don't have enough money" in captured.out

# Test Case 5: User enters an invalid input and decides not to check out
def test_check_cart_invalid_input(Test_user, Test_cart):
    with patch('builtins.input', side_effect=['invalid', 'N']):
        assert check_cart(Test_user, Test_cart) is False

# Test Case 6: User adds a valid product to the cart
def test_check_cart_add_valid_product(Test_user, Test_cart, Test_product):
    with patch('builtins.input', side_effect=['1', 'N']):
        assert check_cart(Test_user, Test_cart) is False


# Test Case 7: User tries to add an out-of-stock product
def test_check_cart_add_out_of_stock_product(Test_user, Test_cart, Test_product,original_products_csv):
    products = load_products_from_csv(original_products_csv)
    # Set the units of the first product in the list to 0
    products[0].units = 0
    with patch('builtins.input', side_effect=['1', 'N']):
        assert check_cart(Test_user, Test_cart) is False
        assert Test_cart.retrieve_item() == []

# Test Case 8: User decides not to check out
def test_check_cart_no_checkout(Test_user, Test_cart):
    with patch('builtins.input', return_value='N'):
        assert check_cart(Test_user, Test_cart) is False



# Test Case 9: Test invalid input ('X') in check_cart function
def test_check_cart_invalid_input_x(Test_user, Test_cart, capsys):
    with patch('builtins.input', side_effect=['X']):
        result = check_cart(Test_user, Test_cart)
    captured = capsys.readouterr()
    # Check that the printed output does not contain the error message
    assert "Invalid input. Please try again." not in captured.out
    # Check that the result is False, indicating the user did not checkout
    assert result is False


# Test Case 10: Test invalid input ('') in check_cart function
def test_check_cart_empty_input(Test_user, Test_cart, capsys):
    with patch('builtins.input', side_effect=['']):
        result = check_cart(Test_user, Test_cart)
    captured = capsys.readouterr()
    # Check that the printed output does not contain the error message
    assert "Invalid input. Please try again." not in captured.out
    # Check that the result is False, indicating the user did not checkout
    assert result is False