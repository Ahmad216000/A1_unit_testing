import json
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

# Test case: Successful checkout, should print a thank you message
def test_successful_checkout(Test_user, Test_cart, capsys):
    # Add a product to the cart with a price lower than the user's wallet
    Test_cart.add_item(Product("Affordable Product", 50.0, 1))
    checkout(Test_user, Test_cart)
    captured = capsys.readouterr()
    assert "Thank you for your purchase" in captured.out

# Test case: Cart with zero units of a product, should remove the product from the cart
def test_zero_units_product(Test_user, Test_cart, capsys):
    # Add a product to the cart with zero units
    zero_units_product = Product("Zero Units Product", 10.0, 0)
    Test_cart.add_item(zero_units_product)
    checkout(Test_user, Test_cart)
    assert zero_units_product not in Test_cart.retrieve_item()


# Test case: Add product to cart and check remaining wallet balance
def test_add_product_and_check_wallet_balance(Test_user, Test_cart, capsys):
    Test_product = Product("Sample Product", 10.0, 2)
    Test_cart.add_item(Test_product)
    checkout(Test_user, Test_cart)
    assert Test_user.wallet == 90.0


# Test case: Attempt to checkout with an empty cart after adding and removing items
def test_checkout_empty_cart_after_adding_and_removing(Test_user, Test_cart, capsys):
    Test_product = Product("Sample Product", 10.0, 2)

    # Add a product to the cart
    Test_cart.add_item(Test_product)
    # Remove the product from the cart
    Test_cart.remove_item(Test_product)
    # Attempt to checkout with an empty cart
    checkout(Test_user, Test_cart)

    captured = capsys.readouterr()
    assert "Your basket is empty" in captured.out

# Test case: Attempt to checkout with empty product selection
def test_checkout_with_empty_product_selection(Test_user, Test_cart, capsys):
    checkout(Test_user, Test_cart)

    captured = capsys.readouterr()
    assert "Your basket is empty" in captured.out


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


def test_product_units_updated(Test_user, Test_cart,Test_product):
    Test_cart.add_item(Test_product)
    # Call the checkout function
    checkout(Test_user, Test_cart)
    # Check that the product units are updated to 1
    assert Test_product.units == 9
    # Check that the product is not removed from the list
    assert Test_product in products
