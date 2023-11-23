from pytest_mock import mocker

from products import display_csv_as_table
import pytest

def test_display_empty_csv(mocker,capsys):
    mocker.patch("builtins.open", mocker.mock_open(read_data=""))
    display_csv_as_table("empty.csv")
    captured = capsys.readouterr()
    assert captured.out.strip() == "Csv empty"
def test_display_csv_missing_header(mocker,capsys):
    mocker.patch("builtins.open", mocker.mock_open(read_data="Laptop,200,25"))
    display_csv_as_table("missing_header.csv")
    captured = capsys.readouterr()
    assert captured.out.strip() == "Header is missing"

def test_display_csv_header_only(mocker,capsys):
    mocker.patch("builtins.open", mocker.mock_open(read_data="Product,Price,Units"))
    display_csv_as_table("header_only.csv")
    captured = capsys.readouterr()
    assert captured.out.strip() == "No product"
def test_display_single_row_csv(mocker,capsys):
    mocker.patch("builtins.open", mocker.mock_open(read_data="Product,Price,Units\nLaptop,200,25"))
    display_csv_as_table("single_row.csv")
    captured = capsys.readouterr()
    assert captured.out.strip() == "['Product', 'Price', 'Units']\n['Laptop', '200', '25']"
def test_display_special_characters_csv(mocker,capsys):
    mocker.patch("builtins.open", mocker.mock_open(read_data="Product,Price,Units\nLaptop#221,200,25"))
    display_csv_as_table("special_characters.csv")
    captured = capsys.readouterr()
    assert captured.out.strip() == "['Product', 'Price', 'Units']\n['Laptop#221', '200', '25']"
def test_display_empty_fields_csv(mocker,capsys):
    mocker.patch("builtins.open", mocker.mock_open(read_data="Product,Price,Units\nLaptop,,25"))
    display_csv_as_table("empty_fields.csv")
    captured = capsys.readouterr()
    assert captured.out.strip() == "['Product', 'Price', 'Units']\n['Laptop', '', '25']"

def test_display_quoted_strings_csv(mocker,capsys):
    mocker.patch("builtins.open", mocker.mock_open(read_data="Product,Price,Units\nLaptop,\"200\",25"))
    display_csv_as_table("quoted_strings.csv")
    captured = capsys.readouterr()
    assert captured.out.strip() == "['Product', 'Price', 'Units']\n['Laptop', '\"200\"', '25']"

def test_display_multiple_line_endings_csv(mocker,capsys):
    mocker.patch("builtins.open", mocker.mock_open(read_data="Product,Price,Units\nLaptop,200,25\nXbox,150,16"))
    display_csv_as_table("multiple_line_endings.csv")
    captured = capsys.readouterr()
    assert captured.out.strip() == "['Product', 'Price', 'Units']\n['Laptop', '200', '25']\n['Xbox', '150', '16']"
def test_display_irregular_columns_csv(mocker,capsys):
    mocker.patch("builtins.open", mocker.mock_open(read_data="Product,Price,Units\nLaptop,200,25\nXbox,16"))
    display_csv_as_table("irregular_columns.csv")
    captured = capsys.readouterr()
    assert captured.out.strip() == "['Product', 'Price', 'Units']\n['Laptop', '200', '25']\n['Xbox','16']"
def test_display_csv_missing_values(mocker):
    mocker.patch("builtins.open", mocker.mock_open(read_data="Product,Price,Units\nLaptop,25\nXbox, 16"))
    display_csv_as_table("missing_values.csv")
