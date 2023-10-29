import sys
import yaml
import sqlite3
import logging
from config.config import Config
from config.logs_stmts import Logs
from products import product_controller
from orders import order_controller
from database.db_connection import DatabaseConnection


logger = logging.getLogger('customer')


class Customer:
    def __init__(self,username):
        self.username=username
        logger.info(Logs.CUSTOMER_MSG.format(name = username))
        self.menu()
 
    def menu(self):
        operation=input(Config.CUSTOMER_CHOICE)
        while operation!='5':
            match operation:
                case '1':
                    product_controller.show_all_avail_prod()
                case '2':
                    order_controller.select_order_products(self.username)
                case '3':
                    print(Config.WALLET_MONEY,order_controller.get_wallet(self.username),"\n")
                case '4':
                    order_controller.update_wallet(self.username)
                case _:
                    print(Config.ENTER_VALID_PROMPT)
            operation=input(Config.CUSTOMER_CHOICE)
            