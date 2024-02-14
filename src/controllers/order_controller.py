import shortuuid
from tabulate import tabulate
from config.config import Config
from controllers.product_controller import check_prod_availability, show_all_avail_prod
from config.database_queries.db_query_config import DBConfig
from models.db_connection import DatabaseConnection
from sqlite3.dbapi2 import Error


def show_all_orders():

    with DatabaseConnection(Config.DB_NAME) as connection:
        cursor = connection.cursor()
        
        all_orders = (cursor.execute(DBConfig.SHOW_ALL_ORDERS)).fetchall()
        return_data = [
            {
                "order_id": orders[0],
                "product_id": orders[1],
                "product_quantity": orders[2],
                "customer_username": orders[3],
                "total_cost": orders[4],
            }
            for orders in all_orders
        ]
        
        return return_data


def select_order_products(username, choice):
    prod_list = []
    total_cost = 0

    show_all_avail_prod()
    prod_details = {"p_id": "", "p_quan": "", "cost": ""}
    prod_details["p_id"] = input(Config.ASK_PROD_ID)
    prod_details["p_quan"] = int(input(Config.ASK_PROD_QUAN))
    if check_prod_availability(prod_details["p_id"], prod_details["p_quan"]):
        with DatabaseConnection(Config.DB_NAME) as connection:
            cursor = connection.cursor()
            try:
                p_info = (
                    cursor.execute(DBConfig.GET_PRODUCT_PRICE, (prod_details["p_id"]))
                ).fetchone()
                if p_info == None:
                    raise Exception
            except Exception as e:
                print(Config.SELECT_VALID_PRODUCT)

            prod_details["cost"] = int(p_info[0]) * prod_details["p_quan"]
            total_cost += prod_details["cost"]
            prod_list.append(prod_details)
    place_order(prod_list, username, total_cost)


# def place_order(prod_list, username, total_cost):
#     if len(prod_list) == 0:
#         return
#     # if place_order == 2:
#     #     return
#     O_ID = int(shortuuid.ShortUUID("1234").random(4))
#     while float(get_wallet(username)) < total_cost:
#         update_wallet(username)
#     generate_bill(O_ID, username, total_cost)
#     with DatabaseConnection(Config.DB_NAME) as connection:
#         cursor = connection.cursor()
#         for i in prod_list:
#             cursor.execute(
#                 DBConfig.ADD_ORDER, (O_ID, username, i["p_id"], i["p_quan"], i["cost"])
#             )
#             cursor.execute(DBConfig.REDUCE_PROD_QUAN, (i["p_quan"], i["p_id"]))
#         cursor.execute(
#             DBConfig.DEDUCT_MONEY_FROM_WALLET,
#             (
#                 total_cost,
#                 username,
#             ),
#         )


# def place_order(prod_list, username):
#     if len(prod_list) == 0:
#         return {"message": "Please select atleast one product to place order!"}, 200
#     O_ID = int(shortuuid.ShortUUID("1234").random(4))
#     total_cost = 0
#     try:
#         with DatabaseConnection(Config.DB_NAME) as connection:
#             cursor = connection.cursor()
#             cost = []
#             for product_info in prod_list:
#                 p_info = (
#                     cursor.execute(DBConfig.GET_PRODUCT_PRICE, (product_info["product_id"]))
#                 ).fetchone()
#                 print(p_info)
#                 if p_info is None:
#                     return None
#                 total_cost += product_info["product_quantity"] * p_info[0]
#                 product_info["cost"] = p_info[0]
#             for i in prod_list:
#                 cursor.execute(
#                     DBConfig.ADD_ORDER,
#                     (O_ID, username, i["p_id"], i["p_quan"], i["cost"]),
#                 )
#                 cursor.execute(DBConfig.REDUCE_PROD_QUAN, (i["p_quan"], i["p_id"]))
#             cursor.execute(
#                 DBConfig.DEDUCT_MONEY_FROM_WALLET,
#                 (
#                     total_cost,
#                     username,
#                 ),
#             )

#     except Exception as error:
#         print(error)
#         return None

#     if float(get_wallet(username)) < total_cost:
#         return {
#             "message": "Your wallet does not have sufficient amount to place order!"
#         }, 200
    

def place_order(product_list, email):

    # check if cart is empty
    if not product_list:
        return None
    
    with DatabaseConnection(Config.DB_NAME) as connection:
        cursor = connection.cursor()

        # obtain total cost of order
        total_order_cost = 0
        for product in product_list:
            product_id = product["product_id"]
            product_qty = product["product_quantity"]

            per_product_cost = (
                cursor.execute(DBConfig.GET_PRODUCT_PRICE, (product_id,))
            ).fetchone()[0]

            total_product_cost = per_product_cost * product_qty

            product["total_product_cost"] = total_product_cost
            total_order_cost += total_product_cost

        # check money in wallet
        if float(get_wallet(email)) < total_order_cost:
            return {
                "message": "Your wallet does not have sufficient amount to place order!"
                }, 200

        for product in product_list:

            #reduce product quantity
            cursor.execute(DBConfig.REDUCE_PROD_QUAN, (
                product["product_quantity"], 
                product["product_id"]
                ))

            # update orders table
            O_ID = int(shortuuid.ShortUUID("1234").random(4))

            cursor.execute(
                    DBConfig.ADD_ORDER,(
                    O_ID, email, 
                    product["product_id"], 
                    product["product_quantity"], 
                    product["total_product_cost"])
                )
            
            # deduct money from wallet
            cursor.execute(
                DBConfig.DEDUCT_MONEY_FROM_WALLET,
                (
                    total_order_cost,
                    email,
                ),
            )
    return True


def get_wallet(username):
    
    with DatabaseConnection(Config.DB_NAME) as connection:
        cursor = connection.cursor()
        amount = (
            cursor.execute(DBConfig.CHECK_WALLET_STATUS, (username,))
        ).fetchone()
        return amount[0]


def update_wallet(username, amount):
    
    with DatabaseConnection(Config.DB_NAME) as connection:
        cursor = connection.cursor()
        cursor.execute(
            DBConfig.UPDATE_WALLET_STATUS,
            (
                amount,
                username,
            ),
        )
    return True
    

def generate_bill(O_ID, username, total_cost):
    with DatabaseConnection(Config.DB_NAME) as connection:
        cursor = connection.cursor()
        cursor.execute(DBConfig.GENERATE_BILL, (O_ID, username, total_cost))
