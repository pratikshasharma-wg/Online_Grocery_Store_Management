import pytest

from users.customer import Customer


class TestCustomer:

    def test_menu(self, mocker):
        mocker.patch("builtins.input", side_effect=["1", "2", "3", "4", "6", "5"])
        product_controller_mock = mocker.patch("users.customer.product_controller")
        order_controller_mock = mocker.patch("users.customer.order_controller")
        mocker.patch.object(product_controller_mock, "show_all_avail_prod")
        mocker.patch.object(order_controller_mock, "select_order_products")
        mocker.patch.object(order_controller_mock, "get_wallet")
        mocker.patch.object(order_controller_mock, "update_wallet")

        assert Customer("Pratiksha") is None
