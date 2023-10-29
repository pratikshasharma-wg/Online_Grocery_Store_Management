import sys
import hashlib
import maskpass
import logging
from config.config import Config
from config.logs_stmts import Logs
from utils import pwd_validation as pv , email_validation as ev
from database.db_connection import DatabaseConnection
from database.database_queries import db_query_config


logger = logging.getLogger('auth')


def login():
    attempts=3
    while attempts:
        logged_in , role , username = login_details()
        if logged_in == False:
            attempts -= 1
            print(f'{attempts}',Config.ATTEMPTS_LEFT_WARNING)
        else:
            return [logged_in , role , username]
    if attempts==0:
            logging.warning(Logs.LOGIN_ATTEMPTS_EXCEEDED)
            sys.exit()


def login_details():
    email = ev.valid_email()
    password = maskpass.askpass(prompt=Config.ASK_FOR_PWD)
    with DatabaseConnection(Config.DB_NAME) as connection:
        cursor = connection.cursor()
        cursor.execute(db_query_config.Config.USER_DATA,(email,))
        user_info = cursor.fetchone()    
        if user_info == None:
            print(Config.CREDENTIAL_WARNING)
            return [False,"",""]
    db_pwd,role = user_info[1],user_info[2]
    is_auth_user = validate_user(db_pwd,password,role)
    if is_auth_user == True:
        logger.info(Logs.SUCCESS_LOGIN)
        return [True,role,email]
    else:
        return [False,"",""]
    

def signUp():
    name = input(Config.ASK_FOR_NAME)
    email = ev.valid_email()
    pwd = password_parser()
    wallet_status = input(Config.ENTER_WALLET_AMOUNT)
    with DatabaseConnection(Config.DB_NAME) as connection:
        cursor = connection.cursor()
        while True:
            known_user = (cursor.execute(db_query_config.Config.USER_DATA,(email,))).fetchone()
            if known_user == None:
                cursor.execute(db_query_config.Config.ADD_USER,(name,email,wallet_status,))
                cursor.execute(db_query_config.Config.ADD_USER_TO_LOGIN,(email,pwd,))
                break
            else:
                print(Config.CREDENTIAL_WARNING)
                email = ev.valid_email()
    print(Config.SIGNUP_SUCCESS)
    logger.info(Logs.SUCESS_SIGNUP)
    return [False,"Customer",email]


def validate_user(db_pwd,password,role):
    password = hashlib.md5(password.encode()).hexdigest()
    if db_pwd == password:
        if role == "Admin":
            role_choice=int(input(Config.ADMIN_ROLE_CHOICE))
            while role_choice != 1 and role_choice != 2:
                role_choice = input(Config.ENTER_VALID_PROMPT)
        print(Config.LOGIN_SUCCESS)
        return True
    else:
        print(Config.CREDENTIAL_WARNING)
        return False


def password_parser():
    while True:
        password = maskpass.askpass(prompt=Config.ASK_FOR_PWD)
        if not pv.validate_pwd(password):
            print(Config.PWD_WARNING)
        else:
            break
    password = hashlib.md5(password.encode()).hexdigest()
    return password