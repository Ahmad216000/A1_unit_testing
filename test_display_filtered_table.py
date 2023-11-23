import csv
import sys

from pytest_mock import mocker

from products import display_filtered_table
import pytest

# Test Case 1: Basic Product Search
def test_search_existing_product(mocker,capsys):
    mocker.patch("builtins.open", mocker.mock_open(read_data="Product,Price,Units\nXbox,150,22"))
    display_filtered_table("test.csv", "Xbox")
    captured = capsys.readouterr()
    assert captured.out.strip()=="['Product', 'Price', 'Units']\n['Xbox', '150', '22']"

def test_search_non_existing_product(mocker,capsys):
    mocker.patch("builtins.open", mocker.mock_open(read_data="Product,Price,Units\nLaptop,1000,12\nPhone,500,10"))
    result =display_filtered_table("test.csv", "Tablet")
    captured = capsys.readouterr()
    assert captured.out.strip() == "Product not found."

def test_search_product_with_whitespace(mocker,capsys):
    mocker.patch("builtins.open", mocker.mock_open(read_data="Product,Price,Units\nLaptop,1000,12\nPhone,500,10"))
    display_filtered_table("test.csv", "  Laptop  ")
    captured = capsys.readouterr()
    assert captured.out.strip()=="['Product', 'Price', 'Units']\n['Laptop', '1000', '12']"

def test_search_in_empty_csv(mocker,capsys):
    mocker.patch("builtins.open", mocker.mock_open(read_data=""))
    display_filtered_table("empty.csv", "Laptop")
    captured = capsys.readouterr()
    assert captured.out.strip() == "CSV file is empty."

def test_search_case_sensitive_product(mocker,capsys):
    mocker.patch("builtins.open", mocker.mock_open(read_data="Product,Price,Units\nLaptop,1000,12\nPhone,500,10"))
    display_filtered_table("test.csv", "laptop")
    captured = capsys.readouterr()
    assert captured.out.strip()== "['Product', 'Price', 'Units']\n['Laptop', '1000', '12']"

def test_search_duplicate_product_names(mocker,capsys):
    mocker.patch("builtins.open", mocker.mock_open(read_data="Product,Price,Units\nLaptop,1000,12\nLaptop,1100,12"))
    display_filtered_table("test.csv", "Laptop")
    captured = capsys.readouterr()
    assert captured.out.strip() =="['Product', 'Price', 'Units']\n['Laptop', '1000', '12']\n['Laptop', '1100', '12']"

def test_search_in_invalid_csv(mocker,capsys):
    mocker.patch("builtins.open", mocker.mock_open(read_data="Not a CSV file"))
    with pytest.raises(csv.Error):
        display_filtered_table("invalid.csv", "Laptop")
        captured = capsys.readouterr()
        assert captured.out.strip() == "Invalid Csv"

def test_search_product_with_numeric_name(mocker,capsys):
    mocker.patch("builtins.open", mocker.mock_open(read_data="Product,Price,Units\nLaptop,1000,12\n12345,500,10"))
    display_filtered_table("test.csv", "12345")
    captured = capsys.readouterr()
    assert captured.out.strip() == "['Product', 'Price', 'Units']\n['12345', '500', '10']"
def test_search_product_with_special_characters(mocker,capsys ):
    mocker.patch("builtins.open", mocker.mock_open(read_data='Product,Price\n"Smart#TV",1500\nPhone,500'))
    display_filtered_table("test.csv", 'Smart#TV')
    captured = capsys.readouterr()
    assert captured.out.strip() == "['Product', 'Price']\n['Smart#TV', '1500']"


def test_search_with_empty_product_name(mocker, capsys):
    mocker.patch("builtins.open", mocker.mock_open(read_data="Product,Price,Units\nLaptop,1000,12\n,500,10"))
    display_filtered_table("test.csv", "")
    captured = capsys.readouterr()
    assert captured.out.strip()=="Product name cannot be empty"