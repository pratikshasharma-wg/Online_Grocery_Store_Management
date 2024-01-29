import shortuuid
from tabulate import tabulate
from config.config import Config
from controllers.product_controller import check_prod_availability , show_all_avail_prod
from config.database_queries import db_query_config
from models.db_connection import DatabaseConnection


def show_all_orders():
    with DatabaseConnection(Config.DB_NAME) as connection:
        cursor = connection.cursor()
        print(tabulate((cursor.execute(db_query_config.DBConfig.SHOW_ALL_ORDERS)).fetchall(), 
                       headers = ["Order ID","Product ID","Product Quantity","Customer username","Total Cost"]),"\n")


def select_order_products(username, choice):
    prod_list = []
    total_cost = 0
    
    show_all_avail_prod()
    prod_details = {"p_id":"" , "p_quan":"" , "cost":""}
    prod_details["p_id"] = input(Config.ASK_PROD_ID)
    prod_details["p_quan"] = int(input(Config.ASK_PROD_QUAN))
    if check_prod_availability(prod_details["p_id"],prod_details["p_quan"]):
        with DatabaseConnection(Config.DB_NAME) as connection:
            cursor=connection.cursor()
            try:
                p_info=(cursor.execute(db_query_config.DBConfig.GET_PRODUCT_PRICE,(prod_details["p_id"]))).fetchone()
                if p_info == None:
                    raise Exception
            except Exception as e:
                print(Config.SELECT_VALID_PRODUCT)
                
            prod_details["cost"] = int(p_info[0]) * prod_details["p_quan"]
            total_cost += prod_details["cost"]
            prod_list.append(prod_details)
    place_order(prod_list,username,total_cost)


def place_order(prod_list,username,total_cost):
    if len(prod_list) == 0:
        return
    # if place_order == 2:
    #     return
    O_ID = int(shortuuid.ShortUUID("1234").random(4))
    while float(get_wallet(username)) < total_cost:
        update_wallet(username)
    generate_bill(O_ID,username,total_cost)
    with DatabaseConnection(Config.DB_NAME) as connection:
        cursor = connection.cursor()
        for i in prod_list:
            cursor.execute(db_query_config.DBConfig.ADD_ORDER,(O_ID,username,i["p_id"],i["p_quan"],i["cost"]))
            cursor.execute(db_query_config.DBConfig.REDUCE_PROD_QUAN,(i["p_quan"],i["p_id"]))
        cursor.execute(db_query_config.DBConfig.DEDUCT_MONEY_FROM_WALLET,(total_cost,username,))
    
# def place_order(prod_list,username)
        

def get_wallet(username):
    try:
        with DatabaseConnection(Config.DB_NAME) as connection:
            cursor = connection.cursor()
            amount = (cursor.execute(db_query_config.DBConfig.CHECK_WALLET_STATUS,(username,))).fetchone()
            return amount[0]
    except Exception:
        return None


def update_wallet(username, amount):
    try:
        with DatabaseConnection(Config.DB_NAME) as connection:
            cursor = connection.cursor()
            cursor.execute(db_query_config.DBConfig.UPDATE_WALLET_STATUS,(amount,username,))
        return True
    except Exception:
        return False


def generate_bill(O_ID,username,total_cost):
    with DatabaseConnection(Config.DB_NAME) as connection:
        cursor = connection.cursor()
        cursor.execute(db_query_config.DBConfig.GENERATE_BILL,(O_ID,username,total_cost))