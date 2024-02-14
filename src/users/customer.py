import logging

from config.config import Config
from config.logs_stmts import Logs
from controllers import product_controller
from controllers import order_controller


logger = logging.getLogger("customer")


class Customer:
    def __init__(self, username):
        self.username = username
        logger.info(Logs.CUSTOMER_MSG.format(name=username))
        self.menu()

    def menu(self):
        operation = input(Config.CUSTOMER_CHOICE)
        while operation != "5":
            match operation:
                case "1":
                    product_controller.show_all_avail_prod()
                case "2":
                    order_controller.select_order_products(self.username)
                case "3":
                    print(
                        Config.WALLET_MONEY,
                        order_controller.get_wallet(self.username),
                        "\n",
                    )
                case "4":
                    order_controller.update_wallet(self.username)
                case _:
                    print(Config.ENTER_VALID_PROMPT)
            operation = input(Config.CUSTOMER_CHOICE)
