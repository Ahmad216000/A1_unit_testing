import json
import shutil

import pytest
from unittest.mock import patch, MagicMock
from checkout_and_payment import *


# Fixture for a sample CSV file
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
def Test_user():
    with open("users.json") as user_file:
        user_data_list = json.load(user_file)
        # Assuming there's at least one user in the list
        user_data = user_data_list[0]
    return User(user_data["username"], user_data["wallet"])

# Fixture to create a sample cart
@pytest.fixture
def Test_cart():
    return ShoppingCart()


@pytest.fixture
def empty_csv_file(tmp_path):
    # Create a temporary file path for product.csv
    product_csv_path = tmp_path / "product.csv"
    # Write an empty content to product.csv
    with open(product_csv_path, 'w', newline='') as csvfile:
        fieldnames = ['Product', 'Price', 'Units']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

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

# Test case 5: Check if the function handles an empty CSV file
def test_load_products_from_csv_empty_file(empty_csv_file):
    # Call the function with the path to the empty CSV file
    products = load_products_from_csv(empty_csv_file)
    # Assert that the function returns an empty list
    assert products == []

# Test case 6: Check if the function handles a CSV file with missing columns
def test_load_products_from_csv_missing_columns(tmp_path):
    invalid_csv = tmp_path / "invalid.csv"
    invalid_csv.write_text("Product,Price\nItem1,10.0")
    with pytest.raises(ValueError):
        load_products_from_csv(str(invalid_csv))

# Test case 7: Check if the function handles a CSV file with invalid numeric values
def test_load_products_from_csv_invalid_numeric_values(tmp_path):
    invalid_csv = tmp_path / "invalid.csv"
    invalid_csv.write_text("Product,Price,Units\nItem1,invalid,5")
    with pytest.raises(ValueError):
        load_products_from_csv(str(invalid_csv))

# Test case 8: Check if the function handles a CSV file with negative units
def test_load_products_from_csv_negative_units(original_products_csv_with_negative_price):
    products = load_products_from_csv(original_products_csv_with_negative_price)
    assert products[73].units == -8

# Test case 9: Check if negative prices result in an empty product list
def test_negative_price_input_type(original_products_csv_with_negative_price):
    products = load_products_from_csv(original_products_csv_with_negative_price)
    assert products[71].price == -2

# Test case 10: Check if special characters are getting added in the product list
def test_specialcharacters_input_type(original_products_csv_with_negative_price):
    products = load_products_from_csv(original_products_csv_with_negative_price)
    print(len(products))
    assert products[72].name == "Orange $ Juice"

