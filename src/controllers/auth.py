import sys
import hashlib
import maskpass
import logging
from config.config import Config
from config.logs_stmts import Logs
from utils import validators
from models.db_connection import DatabaseConnection
from models.db_tables import CreateTables
from src.config.database_queries.db_query_config import DBConfig


logger = logging.getLogger('auth')


# def login():
    # attempts = 3
    # while attempts:
    # logged_in , role , username = login_details()
    # if logged_in == False:
    #     attempts -= 1
    #     print(f'{attempts}',Config.ATTEMPTS_LEFT_WARNING)
    # else:
    # return [logged_in , role , username]
    # if attempts == 0:
    #         logging.warning(Logs.LOGIN_ATTEMPTS_EXCEEDED)
    #         sys.exit()


def login(email, password):
    
    user_info =  CreateTables.fetch_one(email)
    print(user_info)
    if user_info is None:
        # print(Config.CREDENTIAL_WARNING)
        # return [False,"",""]
        return None
    
    db_pwd, role = user_info[1], user_info[2]
    is_auth_user = validate_user(db_pwd, password)
    print(is_auth_user)
    if is_auth_user:
        logger.info(Logs.SUCCESS_LOGIN)
        return [True,role,email]
    else:
        return [False,"",""]
    

def signUp(name, email, password, wallet_status):
    # name = input(Config.ASK_FOR_NAME)
    # email = validators.valid_email()
    # pwd = password_parser()
    # wallet_status = input(Config.ENTER_WALLET_AMOUNT)
    password = hashlib.md5(password.encode()).hexdigest()
    with DatabaseConnection(Config.DB_NAME) as connection:
        cursor = connection.cursor()
        known_user = (cursor.execute(DBConfig.USER_DATA,(email,))).fetchone()
        if known_user is None:
            cursor.execute(DBConfig.ADD_USER,(name,email,wallet_status,))
            cursor.execute(DBConfig.ADD_USER_TO_LOGIN,(email,password,))
        else:
            return
    logger.info(Logs.SUCESS_SIGNUP)
    return [False,"Customer",email]


def validate_user(db_pwd, password):
    password = hashlib.md5(password.encode()).hexdigest()

    if db_pwd == password:
        # if role == "Admin":
        #     role_choice=int(input(Config.ADMIN_ROLE_CHOICE))
        #     while role_choice != 1 and role_choice != 2:
        #         role_choice = input(Config.ENTER_VALID_PROMPT)
        # print(Config.LOGIN_SUCCESS)
        return True
    else:
        # print(Config.CREDENTIAL_WARNING)
        return False


def password_parser():
    while True:
        password = maskpass.askpass(prompt=Config.ASK_FOR_PWD)
        if not validators.validate_pwd(password):
            print(Config.PWD_WARNING)
        else:
            break
    password = hashlib.md5(password.encode()).hexdigest()
    return password