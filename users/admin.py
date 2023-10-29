import sys
import yaml
import sqlite3
import logging
from config.config import Config
from config.logs_stmts import Logs
from products import product_controller
from orders import order_controller


logger = logging.getLogger('admin')


class Admin:
    def __init__(self,username):
        self.username=username
        logging.info(Logs.ADMIN_MSG)
        self.menu()

    def menu(self):
        admin_choice=input(Config.ADMIN_CHOICE)
        while admin_choice!='6':
            match admin_choice:
                case '1': 
                    product_controller.show_all_products()
                case '2':
                    product_controller.add_product()
                case '3':
                    product_controller.update_product()
                case '4':
                    product_controller.delete_product()
                case '5':
                    order_controller.show_all_orders()
                case _:
                    print(Config.ENTER_VALID_PROMPT)
            admin_choice=input(Config.ADMIN_CHOICE)    
