import sys
import hashlib
import maskpass
import logging
from config.config import Config
from config.logs_stmts import Logs
from utils import validators
from models.db_connection import DatabaseConnection
from models.db_tables import CreateTables
from config.database_queries.db_query_config import DBConfig


logger = logging.getLogger("auth")


def login(email, password):
    user_info = None
    with DatabaseConnection(Config.DB_NAME) as connection:
        cursor = connection.cursor()
        user_info = cursor.execute(DBConfig.USER_DATA, (email,)).fetchone()

    if user_info is None:
        return None

    db_pwd, role = user_info[1], user_info[2]
    is_auth_user = validate_user(db_pwd, password)

    if is_auth_user:
        logger.info(Logs.SUCCESS_LOGIN)
        return [True, role, email]
    else:
        return False


def signUp(name, email, password, wallet_status):

    password = hashlib.md5(password.encode()).hexdigest()
    with DatabaseConnection(Config.DB_NAME) as connection:
        cursor = connection.cursor()
        known_user = (cursor.execute(DBConfig.USER_DATA, (email,))).fetchone()
        if known_user is None:
            cursor.execute(
                DBConfig.ADD_USER,
                (
                    name,
                    email,
                    wallet_status,
                ),
            )
            cursor.execute(
                DBConfig.ADD_USER_TO_LOGIN,
                (
                    email,
                    password,
                ),
            )
        else:
            return
    logger.info(Logs.SUCESS_SIGNUP)
    return [False, "Customer", email]


def validate_user(db_pwd, password):
    password = hashlib.md5(password.encode()).hexdigest()
    return db_pwd == password


def password_parser():
    while True:
        password = maskpass.askpass(prompt=Config.ASK_FOR_PWD)
        if not validators.validate_pwd(password):
            print(Config.PWD_WARNING)
        else:
            break
    password = hashlib.md5(password.encode()).hexdigest()
    return password
