import pytest
from unittest.mock import Mock, patch

from _pytest import monkeypatch

from products import *
from login import login

# Assuming your_module contains the functions login, display_csv_as_table,
# display_filtered_table, and checkoutAndPayment

@pytest.fixture
def mock_login(mocker):
    return mocker.patch('products.login', return_value='filler')

@pytest.fixture
def mock_display_csv_as_table(mocker):
    return mocker.patch('products.display_csv_as_table', return_value='filler')

@pytest.fixture
def mock_display_filtered_table(mocker):
    return mocker.patch('products.display_filtered_table', return_value='filler')

@pytest.fixture
def mock_checkout_and_payment(mocker):
    return mocker.patch('products.checkoutAndPayment', return_value="Temp")
def make_input(inputs):
    i = 0
    def v(anything):
        nonlocal i
        input = inputs[i]
        i += 1
        return input
    return v
def test_searchAndBuyProduct_all_inventory(mock_login,mock_display_csv_as_table, mock_display_filtered_table,monkeypatch,mock_checkout_and_payment, mocker):
    monkeypatch.setattr('builtins.input', make_input(["all", "Y"]))
    searchAndBuyProduct()
    mock_login.assert_called_once_with()
    mock_display_csv_as_table.assert_called_once_with("products.csv")
    mock_checkout_and_payment.assert_called_once_with("filler")

def test_searchAndBuyProduct_filtered_product(mock_login, mock_display_csv_as_table, mock_display_filtered_table, mock_checkout_and_payment, mocker):

    mocker.patch('builtins.input', side_effect=["filtered", "Y"])
    searchAndBuyProduct()
    mock_login.assert_called_once()
    mock_display_filtered_table.assert_called_once_with("products.csv", "filtered")
    mock_checkout_and_payment.assert_called_once_with("filler")

def test_searchAndBuyProduct_search(mock_login, mock_display_csv_as_table,mock_display_filtered_table,monkeypatch, mock_checkout_and_payment, mocker):

    monkeypatch.setattr('builtins.input', make_input(["filtered", "all", "Y"]))
    searchAndBuyProduct()
    assert mock_login.call_count == 1
    assert mock_display_csv_as_table.call_count == 1
    mock_display_filtered_table.assert_called_once_with("products.csv", "filtered")
def test_searchAndBuyProduct_multiple_searches(mock_login, mock_display_csv_as_table,monkeypatch, mock_checkout_and_payment, mocker):

    monkeypatch.setattr('builtins.input', make_input(["filtered", "all", "Y"]))
    searchAndBuyProduct()
    assert mock_login.call_count == 1
    assert mock_display_csv_as_table.call_count == 1
    mock_checkout_and_payment.assert_called_once_with("filler")

def test_searchAndBuyProduct_no_search(mock_login, monkeypatch,mocker):

    monkeypatch.setattr('builtins.input', make_input(["", "all", "Y"]))
    searchAndBuyProduct()
    mock_login.assert_called_once_with()


def test_searchAndBuyProduct_no_products(mock_login, mock_display_csv_as_table,monkeypatch, mocker):
    monkeypatch.setattr('builtins.input', make_input(["all", "Y"]))
    mocker.patch('products.display_csv_as_table', return_value=None)
    searchAndBuyProduct()
    assert mock_login.call_count == 1
    assert mock_display_csv_as_table.call_count == 1

def test_searchAndBuyProduct_display_error(mock_login, mock_display_csv_as_table,monkeypatch, mocker):

    monkeypatch.setattr('builtins.input', make_input(["all", "Y"]))
    mock_display_csv_as_table.side_effect = Exception("Display error")
    with pytest.raises(Exception, match="Display error"):
        searchAndBuyProduct()
    assert mock_login.call_count == 1
    assert mock_display_csv_as_table.call_count == 1

def test_searchAndBuyProduct_invalid_checkout(mock_login, mock_display_csv_as_table,monkeypatch, mocker):
    monkeypatch.setattr('builtins.input', make_input(["all", "Y"]))
    mocker.patch('products.checkoutAndPayment', side_effect=RuntimeError("Invalid checkout"))
    with pytest.raises(RuntimeError, match="Invalid checkout"):
        searchAndBuyProduct()
    assert mock_login.call_count == 1
    mock_display_csv_as_table.assert_called_once_with("products.csv")
def test_searchAndBuyProduct_successful_checkout(mock_login, mock_display_csv_as_table, mock_checkout_and_payment,monkeypatch, mocker):
    monkeypatch.setattr('builtins.input', make_input(["all", "Y"]))
    searchAndBuyProduct()
    assert mock_login.call_count == 1
    mock_display_csv_as_table.assert_called_once_with("products.csv")
    mock_checkout_and_payment.assert_called_once()

def test_searchAndBuyProduct_successful_shopping_cycle(mock_login,monkeypatch, mock_display_csv_as_table, mock_checkout_and_payment, mocker):

    monkeypatch.setattr('builtins.input', make_input(["all", "Y", "N", "all", "Y"]))
    searchAndBuyProduct()
    assert mock_login.call_count == 1
    assert mock_display_csv_as_table.call_count == 2
    assert mock_checkout_and_payment.call_count == 1
