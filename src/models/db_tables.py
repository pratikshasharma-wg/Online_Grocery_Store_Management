from config.config import Config
from models.db_connection import DatabaseConnection
from config.database_queries.db_query_config import DBConfig


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
        self.cursor.execute(DBConfig.CREATE_USER_TABLE)
        
    def create_products_table(self):
        self.cursor.execute(DBConfig.CREATE_PRODUCT_TABLE)
    
    def create_order_table(self):
        self.cursor.execute(DBConfig.CREATE_ORDER_TABLE)
        
    def create_billinghistory_table(self):
        self.cursor.execute(DBConfig.CREATE_BILLING_HISTORY_TABLE)
      
    def create_login_table(self):
        self.cursor.execute(DBConfig.CREATE_LOGIN_TABLE)

    @staticmethod
    def fetch_one(email):
        with DatabaseConnection("src\models\grocery.db") as connection:
            cursor = connection.cursor()
            data = cursor.execute(DBConfig.USER_DATA, (email,)).fetchone()
            return data
        

if __name__=="__main__":
    cr=CreateTables()