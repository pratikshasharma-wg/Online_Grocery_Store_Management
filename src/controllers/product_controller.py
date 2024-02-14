import logging
from config.config import Config
from config.logs_stmts import Logs
from tabulate import tabulate
from config.database_queries.db_query_config import DBConfig
from models.db_connection import DatabaseConnection


logger = logging.getLogger("product_controller")


def show_all_products():
    try:
        with DatabaseConnection(Config.DB_NAME) as connection:
            cursor = connection.cursor()
            products = cursor.execute(DBConfig.SHOW_ALL_PRODUCTS).fetchall()
            json_data = [
                {
                    "product_id": product[0],
                    "product_name": product[1],
                    "product_quantity": product[2],
                    "product_price": product[3],
                }
                for product in products
            ]
            return json_data
    except Exception:
        return None


def show_all_avail_prod():
    try:
        with DatabaseConnection(Config.DB_NAME) as connection:
            cursor = connection.cursor()
            data = cursor.execute(DBConfig.SHOW_ALL_AVAIL_PRODUCTS).fetchall()

            json_data = [
                {
                    "product_id": product[0],
                    "product_name": product[1],
                    "product_quantity": product[2],
                    "product_price": product[3],
                }
                for product in data
            ]

            return json_data
            # print(tabulate((cursor.execute(DBConfig.SHOW_ALL_AVAIL_PRODUCTS)).fetchall(),
            #                 headers=["Product ID","Product Name","Product Quantity","Product Price"]),"\n")
    except Exception:
        return None


def add_product(prod_name, prod_price, prod_quan):
   
    with DatabaseConnection(Config.DB_NAME) as connection:
        cursor = connection.cursor()
        cursor.execute(DBConfig.ADD_NEW_PRODUCT, (prod_name, prod_quan, prod_price,))
    return True


def update_product(
    prod_id, new_prod_name=None, new_prod_price=None, new_prod_quan=None
):

    with DatabaseConnection(Config.DB_NAME) as connection:
        cursor = connection.cursor()
        if new_prod_name is not None:
            # new_prod_name=input(Config.ENTER_NEW_PROD_NAME)
            cursor.execute(
                DBConfig.UPDATE_PRODUCT_NAME,
                (
                    new_prod_name,
                    prod_id,
                ),
            )
        if new_prod_price is not None:
            # new_prod_quan=float(input(Config.ENTER_NEW_PROD_QUAN))
            cursor.execute(
                DBConfig.UPDATE_PRODUCT_QUANTITY,
                (
                    new_prod_quan,
                    prod_id,
                ),
            )
        if new_prod_quan is not None:
            # new_prod_price=float(input(Config.ENTER_NEW_PROD_PRICE))
            cursor.execute(
                DBConfig.UPDATE_PRODUCT_PRICE,
                (
                    new_prod_price,
                    prod_id,
                ),
            )
    return True


def delete_product(prod_id):

    with DatabaseConnection(Config.DB_NAME) as connection:
        cursor = connection.cursor()
        try:
            info = cursor.execute(DBConfig.DELETE_PRODUCT, (prod_id,))
            if info.rowcount == 0:
                logger.critical(Logs.PROD_DOES_NOT_EXIST)
                raise Exception
            return True
        except Exception as e:
            print(Config.PROD_DOES_NOT_EXIST, "\n")
            return False


def reduce_prod_quan(p_id, p_quant):
    with DatabaseConnection(Config.DB_NAME) as connection:
        cursor = connection.cursor()
        cursor.execute(
            DBConfig.REDUCE_PROD_QUAN,
            (
                p_quant,
                p_id,
            ),
        )


def check_prod_availability(p_id, p_quant):
    with DatabaseConnection(Config.DB_NAME) as connection:
        cursor = connection.cursor()
        prod_quan = (cursor.execute(DBConfig.GET_PRODUCT_QUAN, (p_id,))).fetchone()
        try:
            if prod_quan == None:
                raise Exception
            if prod_quan[0] < p_quant:
                print(Config.ITEMS_REMAIN.format(number=prod_quan[0]))
                return False
            else:
                return True
        except Exception as e:
            print(Config.PROD_DOES_NOT_EXIST)
