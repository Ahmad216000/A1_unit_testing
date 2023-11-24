
from unittest.mock import patch
import logout

def test_logout_with_empty_cart():
    # Create an empty cart
    cart = {}

    # Simulate logging out with an empty cart
    result = logout.logout(cart)

    # Assert that the logout function returned True
    assert result is True
def test_logout_with_non_empty_cart():
    # Create a cart with items
    cart = {"item1": 1, "item2": 2}

    # Simulate user confirming logout by providing "Y" as input
    with patch('builtins.input', side_effect=["Y"]):
        result = logout.logout(cart)
    assert result is True