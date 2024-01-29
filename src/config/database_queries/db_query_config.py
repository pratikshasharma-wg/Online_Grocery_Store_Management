import yaml

FPATH='src\\config\\database_queries\\db_queries.yml'

class DBConfig:

    CREATE_USER_TABLE = None
    CREATE_LOGIN_TABLE = None
    CREATE_PRODUCT_TABLE = None
    CREATE_ORDER_TABLE = None
    CREATE_BILLING_HISTORY_TABLE = None
    SHOW_ALL_ORDERS = None
    ADD_ORDER = None
    SHOW_ALL_PRODUCTS = None
    SHOW_ALL_AVAIL_PRODUCTS = None
    ADD_NEW_PRODUCT = None
    DELETE_PRODUCT = None
    UPDATE_PRODUCT_NAME = None
    UPDATE_PRODUCT_QUANTITY = None
    UPDATE_PRODUCT_PRICE = None
    GET_PRODUCT_PRICE = None
    CHECK_WALLET_STATUS = None
    UPDATE_WALLET_STATUS = None
    USER_DATA = None
    ADD_USER = None
    ADD_USER_TO_LOGIN = None
    GENERATE_BILL = None
    REDUCE_PROD_QUAN = None
    GET_PRODUCT_QUAN = None
    DEDUCT_MONEY_FROM_WALLET = None

    @classmethod
    def load(cls):

        with open("src\config\database_queries\db_queries.yml",'r') as f:
            data = yaml.safe_load(f)
            cls.CREATE_USER_TABLE = data['CREATE_USER_TABLE']
            cls.CREATE_LOGIN_TABLE = data['CREATE_LOGIN_TABLE']
            cls.CREATE_PRODUCT_TABLE = data['CREATE_PRODUCT_TABLE']
            cls.CREATE_ORDER_TABLE = data['CREATE_ORDER_TABLE']
            cls.CREATE_BILLING_HISTORY_TABLE = data['CREATE_BILLING_HISTORY_TABLE']
            cls.SHOW_ALL_ORDERS = data['SHOW_ALL_ORDERS']
            cls.ADD_ORDER = data['ADD_ORDER']
            cls.SHOW_ALL_PRODUCTS = data['SHOW_ALL_PRODUCTS']
            cls.SHOW_ALL_AVAIL_PRODUCTS = data['SHOW_ALL_AVAIL_PRODUCTS']
            cls.ADD_NEW_PRODUCT = data['ADD_NEW_PRODUCT']
            cls.DELETE_PRODUCT = data['DELETE_PRODUCT']
            cls.UPDATE_PRODUCT_NAME = data['UPDATE_PRODUCT_NAME']
            cls.UPDATE_PRODUCT_QUANTITY = data['UPDATE_PRODUCT_QUANTITY']
            cls.UPDATE_PRODUCT_PRICE = data['UPDATE_PRODUCT_PRICE']
            cls.GET_PRODUCT_PRICE = data['GET_PRODUCT_PRICE']
            cls.CHECK_WALLET_STATUS = data['CHECK_WALLET_STATUS']
            cls.UPDATE_WALLET_STATUS = data['UPDATE_WALLET_STATUS']
            cls.USER_DATA = data['USER_DATA']
            cls.ADD_USER = data['ADD_USER']
            cls.ADD_USER_TO_LOGIN = data['ADD_USER_TO_LOGIN']
            cls.GENERATE_BILL = data['GENERATE_BILL']
            cls.REDUCE_PROD_QUAN = data['REDUCE_PROD_QUAN']
            cls.GET_PRODUCT_QUAN = data['GET_PROD_QUAN']
            cls.DEDUCT_MONEY_FROM_WALLET = data['DEDUCT_MONEY_FROM_WALLET']

DBConfig.load()