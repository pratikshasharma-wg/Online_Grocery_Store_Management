import re

def validate_pwd(password):
    pattern='^[a-zA-Z0-9]{8,20}$'
    if re.match(pattern,password) == None:
        return False
    else:
        return True