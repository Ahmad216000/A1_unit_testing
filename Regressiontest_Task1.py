import json
import shutil
import io
from unittest.mock import patch

import pytest
from checkout_and_payment_new import *


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

# Fixture for the original CSV file (or its copy) with negative prices and special charatcers
@pytest.fixture
def original_products_csv_with_negative_price(original_products_csv):
    copy_path = original_products_csv

    # Modify the copy to include negative prices
    with open(copy_path, 'a') as file:
        file.write("\nBanana,-2,5")
    with open(copy_path, 'a') as file:
        file.write("\nOrange $ Juice,1.5,8")
    with open(copy_path, 'a') as file:
        file.write("\ntest,1.5,-8")
    return copy_path


@pytest.fixture
def original_products_csv_with_string_price(original_products_csv):
    copy_path = original_products_csv
    with open(copy_path, 'a') as file:
        file.write("\ntest,testing,-8")
# Stub for the Product class
class ProductStub:
    def __init__(self, name, price, units):
        self.name = name
        self.price = float(price)
        self.units = int(units)

@pytest.fixture
def empty_csv_file(tmp_path):
    # Create a temporary file path for product.csv
    product_csv_path = tmp_path / "product.csv"
    # Write an empty content to product.csv
    with open(product_csv_path, 'w', newline='') as csvfile:
        fieldnames = ['Product', 'Price', 'Units']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

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
    with patch('builtins.input', return_value='Y'), patch('checkout_and_payment_new.checkout') as mock_checkout:
        assert check_cart(Test_user, Test_cart)
        mock_checkout.assert_called_once_with(Test_user, Test_cart)

# Test Case 4: User checks out with insufficient funds

# Test Case 5: User enters an invalid input and decides not to check out
def test_check_cart_invalid_input(Test_user, Test_cart):
    with patch('builtins.input', side_effect=['invalid', 'N']):
        assert check_cart(Test_user, Test_cart) is False
# Test Case 6: User adds a valid product to the cart

# Test Case 7: User tries to add an out-of-stock product
def test_check_cart_add_out_of_stock_product(Test_user, Test_cart, Test_product,original_products_csv):
    products = load_products_from_csv(original_products_csv)
    # Set the units of the first product in the list to 0
    products[0].units = 0
    with patch('builtins.input', side_effect=['1', 'N']):
        assert check_cart(Test_user, Test_cart) is False
        assert Test_cart.retrieve_item() == []

# Test Case 8: User decides not to check out

# Test Case 9: Test invalid input ('X') in check_cart function

# Test Case 10: Test invalid input ('') in check_cart function

#******************Checkout*****************************
# Test case: Empty cart, should print a message about an empty basket
def test_empty_cart(Test_user, Test_cart, capsys):
    checkout(Test_user, Test_cart)
    captured = capsys.readouterr()
    assert "Your basket is empty" in captured.out

# Test case: Insufficient wallet balance, should print a message about not enough money
def test_insufficient_balance(Test_user, Test_cart, capsys):
    # Add a product to the cart with a price higher than the user's wallet
    Test_cart.add_item(Product("Expensive Product", 150.0, 1))
    checkout(Test_user, Test_cart)
    captured = capsys.readouterr()
    assert "You don't have enough money" in captured.out

# Test case: Cart with zero units of a product, should remove the product from the cart
def test_zero_units_product(Test_user, Test_cart, capsys):
    # Add a product to the cart with zero units
    zero_units_product = Product("Zero Units Product", 10.0, 0)
    Test_cart.add_item(zero_units_product)
    checkout(Test_user, Test_cart)
    assert zero_units_product not in Test_cart.retrieve_item()

# Test case: Checkout and check if the cart is cleared
def test_checkout_clears_cart(Test_user, Test_cart):
    Test_product = Product("Sample Product", 10.0, 2)
    Test_cart.add_item(Test_product)
    checkout(Test_user, Test_cart)
    assert not Test_cart.retrieve_item()

# Test case: Add multiple products to the cart and check if the wallet balance is correct
def test_add_multiple_products_and_check_total_price(Test_user, Test_cart):
    initial_walletbalance=Test_user.wallet
    product1 = Product("Product 1", 20.0, 3)
    product2 = Product("Product 2", 30.0, 2)
    Test_cart.add_item(product1)
    Test_cart.add_item(product2)
    total_price = product1.price + product2.price
    checkout(Test_user, Test_cart)
    assert Test_user.wallet == initial_walletbalance - total_price

#********************************loadproductsfromcsv********************************
# Test case 1: Check if the correct number of products is loaded
def test_load_products_from_csv_correct_number_of_products(original_products_csv):
    products = load_products_from_csv(original_products_csv)
    assert len(products) == 71

# Test case 2: Check if the loaded products have the correct attributes
def test_load_products_from_csv_correct_product_attributes(original_products_csv_with_string_price):
    with pytest.raises(TypeError):
        load_products_from_csv(original_products_csv_with_string_price)

# Test case 3: Check if the loaded products have the correct values
def test_load_products_from_csv_correct_product_values(original_products_csv):
    products = load_products_from_csv(original_products_csv)
    print(products[0].name,products[1].price)

    assert products[0].name == "Apple"
    assert products[1].price == 1.0

# Test case 4: Check if the function handles a non-existing file gracefully
def test_load_products_from_csv_non_existing_file():
    with pytest.raises(FileNotFoundError):
        load_products_from_csv("non_existing_file.csv")

# Test case 8: Check if the function handles a CSV file with negative units
def test_load_products_from_csv_negative_units(original_products_csv_with_negative_price):
    products = load_products_from_csv(original_products_csv_with_negative_price)
    assert products[73].units == -8


#******************************Additional implemenation testcases********************************
def test_query_cart(Test_user, Test_cart, capsys,Test_product):
    # Create a mock inventory
    mock_products_dict = {Test_product.name: Test_product}

    # Add the product to the cart
    Test_cart.add_item(Test_product, mock_products_dict)

    with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
        with patch("builtins.input", return_value="Q"):
            result = check_cart(Test_user, Test_cart)
            output = mock_stdout.getvalue().strip()

    assert result == False
    assert "1. Apple - $2.0 - Units: 10" in output
    assert "Do you want to query (Q) or remove (R) items from the cart (Y to checkout, L to logout)? " not in output

def test_remove_from_cart(Test_user, Test_cart, Test_product,capsys):
    """product1 = ProductStub("Product1", 10, 5)
    Test_cart.add_item(product1)"""
    # Create a mock inventory
    mock_products_dict = {Test_product.name: Test_product}

    # Add the product to the cart
    Test_cart.add_item(Test_product, mock_products_dict)
    with patch("builtins.input", side_effect=["R", "1"]):
        removed_product = Test_cart.items[0]
        result = check_cart(Test_user, Test_cart)

    assert result == False
    assert len(Test_cart.items) == 0
    assert f"{removed_product.name} removed from the cart." in capsys.readouterr().out

# Test Case for Putting Product Back into Inventory upon Removal
"""def test_put_product_back_into_inventory(Test_user, Test_cart, capsys):
    original_units = 5
    product1 = ProductStub("Product1", 10, original_units)
    Test_cart.add_item(product1)

    # Ensure the product is in the cart
    assert len(Test_cart.items) == 1

    with patch("builtins.input", side_effect=["R", "1"]):
        removed_product = Test_cart.items[0]
        result = check_cart(Test_user, Test_cart)

    # Ensure the product is removed from the cart
    assert result == False
    assert len(Test_cart.items) == 0

    # Ensure the product is put back into the inventory
    assert removed_product.units == original_units + 1  # Assuming one unit is added back

    # Ensure the product is updated in the inventory (this is an additional assertion)
    for product in products:
        if product.name == removed_product.name:
            assert product.units == original_units + 1  # Assuming one unit is added back"""
def test_put_product_back_into_inventory(Test_user, Test_product, Test_cart):
    # Create a mock inventory
    mock_products_dict = {Test_product.name: Test_product}

    # Add the product to the cart
    Test_cart.add_item(Test_product, mock_products_dict)

    # Ensure the product is in the cart
    assert len(Test_cart.items) == 1

    with patch("builtins.input", side_effect=["R", "1"]):
        removed_product = Test_cart.items[0]
        result = check_cart(Test_user, Test_cart)

    # Ensure the product is removed from the cart
    assert result == False
    assert len(Test_cart.items) == 0

    # Ensure the product is put back into the inventory
    assert Test_product.units == mock_products_dict[Test_product.name].units