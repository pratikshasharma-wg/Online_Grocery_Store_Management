import pytest
from unittest import TestCase
from unittest.mock import patch, Mock, MagicMock

from users.admin import Admin


class TestAdmin(TestCase):

    def test_menu(self):
        with patch("users.admin.product_controller"):
            with patch("users.admin.order_controller"):
                with patch(
                    "builtins.input", side_effect=["1", "2", "3", "4", "5", "7", "6"]
                ):
                    assert not Admin("Pratiksha")
            # mock.assert_called_once()
        # mock.stop()
