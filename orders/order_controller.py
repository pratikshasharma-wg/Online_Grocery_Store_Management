import shortuuid
from tabulate import tabulate
from config.config import Config
from products.product_controller import check_prod_availability , show_all_avail_prod
from database.database_queries import db_query_config
from database.db_connection import DatabaseConnection


def show_all_orders():
    with DatabaseConnection(Config.DB_NAME) as connection:
        cursor = connection.cursor()
        print(tabulate((cursor.execute(db_query_config.Config.SHOW_ALL_ORDERS)).fetchall(), 
                       headers = ["Order ID","Product ID","Product Quantity","Customer username","Total Cost"]),"\n")


def select_order_products(username):
    prod_list = []
    total_cost = 0
    choice = int(input(Config.SELECT_PRODUCT_PROMPT))
    while choice != 2:
        show_all_avail_prod()
        prod_details = {"p_id":"" , "p_quan":"" , "cost":""}
        prod_details["p_id"] = input(Config.ASK_PROD_ID)
        prod_details["p_quan"] = int(input(Config.ASK_PROD_QUAN))
        if check_prod_availability(prod_details["p_id"],prod_details["p_quan"]):
            with DatabaseConnection(Config.DB_NAME) as connection:
                cursor=connection.cursor()
                try:
                    p_info=(cursor.execute(db_query_config.Config.GET_PRODUCT_PRICE,(prod_details["p_id"]))).fetchone()
                    if p_info == None:
                        raise Exception
                except Exception as e:
                    print(Config.SELECT_VALID_PRODUCT)
                    continue
                prod_details["cost"] = int(p_info[0]) * prod_details["p_quan"]
                total_cost += prod_details["cost"]
                prod_list.append(prod_details)
            choice = int(input(Config.SELECT_PRODUCT_PROMPT))
    place_order(prod_list,username,total_cost)


def place_order(prod_list,username,total_cost):
    if len(prod_list) == 0:
        return
    place_order = int(input(Config.ASK_TO_PLACE_ORDER))
    if place_order == 2:
        return
    O_ID = int(shortuuid.ShortUUID("1234").random(4))
    while float(get_wallet(username)) < total_cost:
        print(Config.ADD_SUFFICIENT_MONEY.format(money = (total_cost - float(get_wallet(username)))))
        update_wallet(username)
    generate_bill(O_ID,username,total_cost)
    with DatabaseConnection(Config.DB_NAME) as connection:
        cursor = connection.cursor()
        for i in prod_list:
            cursor.execute(db_query_config.Config.ADD_ORDER,(O_ID,username,i["p_id"],i["p_quan"],i["cost"]))
            cursor.execute(db_query_config.Config.REDUCE_PROD_QUAN,(i["p_quan"],i["p_id"]))
        cursor.execute(db_query_config.Config.DEDUCT_MONEY_FROM_WALLET,(total_cost,username,))
        

def get_wallet(username):
    with DatabaseConnection(Config.DB_NAME) as connection:
        cursor = connection.cursor()
        amount = (cursor.execute(db_query_config.Config.CHECK_WALLET_STATUS,(username,))).fetchone()
        return amount[0]


def update_wallet(username):
        with DatabaseConnection(Config.DB_NAME) as connection:
            cursor = connection.cursor()
            amount = input(Config.ADD_AMOUNT_TO_WALLET)
            cursor.execute(db_query_config.Config.UPDATE_WALLET_STATUS,(amount,username,))


def generate_bill(O_ID,username,total_cost):
    with DatabaseConnection(Config.DB_NAME) as connection:
        cursor = connection.cursor()
        cursor.execute(db_query_config.Config.GENERATE_BILL,(O_ID,username,total_cost))