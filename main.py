import sys
import logging
from config.config import Config
from config.logs_stmts import Logs
from database.database_queries import db_query_config
from auth import signUp,login
from users import customer
from users.admin import Admin
from database.db_tables import CreateTables
from database.db_connection import DatabaseConnection


logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    level = logging.DEBUG,
                    filename = 'config\\logs.txt')
logger = logging.getLogger('main')


class Main:
    def __init__(self):
        print(Config.WELCOME_STRING)
        cr = CreateTables()

    def main(self):
        self.logged_in , self.role , self.username = False , "" , ""
        while self.logged_in == False:
            response=input(Config.ASK_FOR_LOGIN_SIGNUP)
            if response == "1":
                self.logged_in , self.role , self.username = login()
            elif response == "2":
                self.logged_in , self.role , self.username = signUp()
                continue
            elif response == '3':
                sys.exit(0)
            else:
                response = input(Config.ENTER_VALID_PROMPT)
                continue
            if self.logged_in == False:
                sys.exit()
            if self.role == "Customer":
                user = customer.Customer(self.username)
                self.logged_in=False
            elif self.role == "Admin":
                admin = Admin(self.username)
                self.logged_in=False
       
    
if __name__ == "__main__":  
    Config.load()
    db_query_config.Config.load()
    Logs.load()
    logger.info(Logs.WELCOME_MSG)
    Main().main()