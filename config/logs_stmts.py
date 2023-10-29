import yaml

FPATH='config\\logs_stmts.yml'

class Logs:

    @classmethod
    def load(cls):
        with open(FPATH,'r') as f:
            data=yaml.safe_load(f)
            cls.WELCOME_MSG = data['WELCOME_MSG']
            cls.LOGIN_ATTEMPTS_EXCEEDED = data['LOGIN_ATTEMPTS_EXCEEDED']
            cls.SUCCESS_LOGIN = data['SUCCESS_LOGIN']
            cls.SUCESS_SIGNUP = data['SUCCESS_SIGNUP']
            cls.ADMIN_MSG = data['ADMIN_MSG']
            cls.CUSTOMER_MSG = data['CUSTOMER_MSG']
            cls.PROD_DOES_NOT_EXIST = data['PROD_DOES_NOT_EXIST']