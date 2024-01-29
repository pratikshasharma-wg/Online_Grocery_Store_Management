import re
import functools
from config.config import Config
from flask_smorest import abort
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def valid_email():
    while True:
        email = input(Config.ASK_FOR_EMAIL)
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,7}$'
        if(re.match(pattern, email)):
            return email
        
def validate_pwd(password):
    pattern = '^[a-zA-Z0-9]{8,20}$'
    if re.match(pattern,password) == None:
        return False
    else:
        return True
    
def role_required(lst):

    def decorator(func):
    
        @functools.wraps(func)
        def wrap_func(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["role"] in lst:
                return func(*args, **kwargs)
            else:
                abort(400, message = "Permission not granted!")
        
        return wrap_func
    
    return decorator