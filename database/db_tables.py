import sqlite3
import hashlib
from config.config import Config
from database.db_connection import DatabaseConnection
from database.database_queries import db_query_config


class CreateTables:
    def __init__(self):
        with DatabaseConnection(Config.DB_NAME) as connection:
            self.cursor=connection.cursor()
            self.create_login_table()
            self.create_order_table()
            self.create_billinghistory_table()
            self.create_products_table()
            self.create_user_table()
            
    def create_user_table(self):
        self.cursor.execute(db_query_config.Config.CREATE_USER_TABLE)
        
    def create_products_table(self):
        self.cursor.execute(db_query_config.Config.CREATE_PRODUCT_TABLE)
    
    def create_order_table(self):
        self.cursor.execute(db_query_config.Config.CREATE_ORDER_TABLE)
        
    def create_billinghistory_table(self):
        self.cursor.execute(db_query_config.Config.CREATE_BILLING_HISTORY_TABLE)
      
    def create_login_table(self):
        self.cursor.execute(db_query_config.Config.CREATE_LOGIN_TABLE)


if __name__=="__main__":
    cr=CreateTables()