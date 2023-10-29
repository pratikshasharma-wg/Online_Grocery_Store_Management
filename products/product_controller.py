import logging
from config.config import Config
from config.logs_stmts import Logs
from tabulate import tabulate
from database.database_queries import db_query_config
from database.db_connection import DatabaseConnection

logger = logging.getLogger('product_controller')

def show_all_products():
    with DatabaseConnection(Config.DB_NAME) as connection:
        cursor=connection.cursor()
        print(tabulate((cursor.execute(db_query_config.Config.SHOW_ALL_PRODUCTS)).fetchall(),
                        headers=["Product ID","Product Name","Product Quantity","Product Price"]),"\n")


def show_all_avail_prod():
    with DatabaseConnection(Config.DB_NAME) as connection:
        cursor=connection.cursor()
        print(tabulate((cursor.execute(db_query_config.Config.SHOW_ALL_AVAIL_PRODUCTS)).fetchall(),
                        headers=["Product ID","Product Name","Product Quantity","Product Price"]),"\n")


def add_product():
    prod_name=input(Config.ASK_PROD_NAME)
    prod_quan=input(Config.ASK_PROD_QUAN)
    prod_price=input(Config.ASK_PROD_PRICE)
    with DatabaseConnection(Config.DB_NAME) as connection:
        cursor=connection.cursor()
        cursor.execute(db_query_config.Config.ADD_NEW_PRODUCT,(prod_name,prod_quan,prod_price))


def update_product():
    show_all_products()
    prod_id=input(Config.ASK_PROD_ID)
    update_detail=int(input(Config.UPDATE_PRODUCT_PROMPT))
    with DatabaseConnection(Config.DB_NAME) as connection:
        cursor=connection.cursor()
        match update_detail:
            case 1:
                new_prod_name=input(Config.ENTER_NEW_PROD_NAME)
                cursor.execute(db_query_config.Config.UPDATE_PRODUCT_NAME,(new_prod_name,prod_id,))
            case 2:
                new_prod_quan=float(input(Config.ENTER_NEW_PROD_QUAN))
                cursor.execute(db_query_config.Config.UPDATE_PRODUCT_QUANTITY,(new_prod_quan,prod_id,))
            case 3:
                new_prod_price=float(input(Config.ENTER_NEW_PROD_PRICE))
                cursor.execute(db_query_config.Config.UPDATE_PRODUCT_PRICE,(new_prod_price,prod_id,))
            case _:
                print(Config.ENTER_VALID_PROMPT)


def delete_product():
    prod_id=input(Config.ASK_PROD_ID)
    with DatabaseConnection(Config.DB_NAME) as connection:
        cursor=connection.cursor()
        try:
            info = cursor.execute(db_query_config.Config.DELETE_PRODUCT,(prod_id,))
            if info.rowcount == 0:
                logger.critical(Logs.PROD_DOES_NOT_EXIST)
                raise Exception
        except Exception as e:
            print(Config.PROD_DOES_NOT_EXIST,"\n")


def reduce_prod_quan(p_id,p_quant):
    with DatabaseConnection(Config.DB_NAME) as connection:
        cursor=connection.cursor()
        cursor.execute(db_query_config.Config.REDUCE_PROD_QUAN,(p_quant,p_id,))


def check_prod_availability(p_id,p_quant):
    with DatabaseConnection(Config.DB_NAME) as connection:
        cursor = connection.cursor()
        prod_quan = (cursor.execute(db_query_config.Config.GET_PRODUCT_QUAN,(p_id,))).fetchone()
        if prod_quan[0] < p_quant:
            print(Config.ITEMS_REMAIN.format(number = prod_quan[0]))
            return False
        else:
            return True