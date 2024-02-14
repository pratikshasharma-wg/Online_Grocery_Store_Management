import unittest
from unittest.mock import patch, Mock, MagicMock

from config.config import Config
from controllers import product_controller


class TestShowAllProducts(unittest.TestCase):

    import unittest


from unittest.mock import patch, MagicMock
from controllers import product_controller


class TestShowAllProducts(unittest.TestCase):

    @patch("products.product_controller.DatabaseConnection")
    @patch("products.product_controller.tabulate")
    def test_show_all_products(self, mock_tabulate, mock_database_connection):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            (1, "Product 1", 10, 20.0),
            (2, "Product 2", 15, 30.0),
        ]

        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_database_connection.return_value.__enter__.return_value = (
            mock_connection  # Ensure __enter__ returns the mock_connection
        )

        product_controller.show_all_products()

        mock_database_connection.assert_called_once_with(Config.DB_NAME)
        mock_connection.cursor.assert_called_once()
        # mock_cursor.execute.assert_called_once_with(db_query_config.Config.SHOW_ALL_PRODUCTS)
        mock_tabulate.assert_called_once_with(
            [(1, "Product 1", 10, 20.0), (2, "Product 2", 15, 30.0)],
            headers=["Product ID", "Product Name", "Product Quantity", "Product Price"],
        )

    @patch("products.product_controller.DatabaseConnection")
    @patch("products.product_controller.tabulate")
    def test_show_all_avail_prod(self, mock_tabulate, mock_database_connection):
        mock_cursor = MagicMock()
        mock_database_connection = MagicMock()
        mock_database_connection.return_value = mock_database_connection
        mock_cursor.fetchall.return_value = [
            (1, "Product 1", 10, 20.0),
            (2, "Product 2", 15, 30.0),
        ]
        mock_connection = MagicMock()
        mock_database_connection.__enter__.return_value = mock_connection
        product_controller.show_all_avail_prod()
        mock_tabulate.assert_called_once_with(
            [(1, "Product 1", 10, 20.0), (2, "Product 2", 15, 30.0)],
            headers=["Product ID", "Product Name", "Product Quantity", "Product Price"],
        )


if __name__ == "__main__":
    unittest.main()
